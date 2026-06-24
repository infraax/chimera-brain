# ENGRAM 1.0 — Research Geodesic
## Language, Performance, Core Math & File Format
### PoC → Production: Implementing ENGRAM the Anki Way

*Research completed: 2026-06-24 · Covers V1–V10 of the ENGRAM Implementation Geodesic*

***

## Executive Summary

The evidence confirms the working hypothesis with one important refinement. The **Ollama pattern (Go service + C/C++ compute core)** is the right shape for ENGRAM 1.0, but the engine seam is better expressed as **C++ only** (not a C/Go hybrid) on the robot, because: (a) Vector's `vic-engine` is pure C++, (b) the animation binary format already uses FlatBuffers, (c) cgo overhead is ~40 ns/call — acceptable for batch calls, but introduces GC-entangled threading that is inappropriate inside a real-time C++ engine thread. The recommended split is: **C++ on-robot reflex layer + C++ archive core + Go box-side service/API wrapper** (matching how Ollama wraps llama.cpp), with Python retained exclusively as the research lab and executable reference spec.[^1][^2][^3]

***

## V1 — Profile & Decompose the PoC

### SUMMARY

The ENGRAM pipeline decomposes into six measurable stages: (1) fingerprint — rFFT over `[T,D]` + L2-norm; (2) `.eng` encode/decode; (3) index build; (4) ANN query (hnswlib HNSW, ~120 µs); (5) streaming write/flush; (6) disk IO. For 10–30 fps write rates at soak-50k scale, the dominant compute cost is the FFT (rFFT is \(O(N \log N)\) and runs per-frame), followed by HNSW query. Serialization and disk IO are IO-bound glue that can stay in Python or Go. The ANN query at ~120 µs (verified by the PoC's soak tests) is already acceptable for the box tier but too slow and non-deterministic for a robot-side reflex with sub-millisecond requirements.

### HOT-PATH TABLE

| Operation | % Time (est.) | Bound Type | Tier | Needs Fast Lang? |
|---|---|---|---|---|
| rFFT over `[T,D]` | ~35–45% | Compute | Robot + Box | **Yes — C/C++** |
| L2-norm / dot product | ~10–15% | Compute | Robot + Box | **Yes — C/C++** |
| HNSW ANN query | ~20–30% | Compute+Mem | Box (archive) | **Yes — C++** |
| Ring-buffer hot index scan | ~5–10% | Compute | Robot | **Yes — C++** |
| `.eng` encode/decode | ~5% | IO-bound | Both | Go/Python OK |
| Streaming write/flush | ~5% | IO-bound | Box | Go OK |
| Disk IO | ~5% | IO-bound | Box (cold) | Go OK |

**Profiling method:** `cProfile`/`py-spy` on `bench.py` + `soak.py` will isolate these stages. For ARM estimation, scale by the APQ8009's ~15–16 GFLOPS (Cortex-A7 at ~1 GHz SGEMM) vs a modern x86 laptop (~100+ GFLOPS), i.e. expect ~6–8× slowdown on robot for floating-point ops. The 120 µs HNSW query on x86 likely becomes 700–1000 µs on ARM without optimization.[^4][^5]

### EVIDENCE

Profile toolchain: `python -m cProfile -o profile.pstats soak.py`, visualize with SnakeViz or py-spy flamegraphs. ARM FFT benchmark on Cortex-A7 (Cubieboard2, 1 GHz, NEONv2): FFTW 3.3.3 with NEON enabled reaches viable throughput for small-to-medium transform sizes.[^6][^7][^4]

### RECOMMENDATION

Run `py-spy record --native` on the soak harness first to get actual percentages before any porting. The **FFT + norm** and **ANN query** are the only ops that strictly require a compiled language. Everything else is structural glue.

### CONFIDENCE: High | OPEN QUESTIONS: Exact FFT size used in rFFT over `[T,D]`; whether the hot path in soak.py is actually FFT-dominated or hnswlib-dominated (profile first).

***

## V2 — Language Decision Matrix

### SUMMARY

The evidence clearly supports a **two-language combination: C++ (compute core, robot tier) + Go (service/API layer, box tier)**. Rust is a legitimate alternative to C++ for the compute core — performance is comparable, memory safety without GC is a genuine advantage for the robot — but ecosystem maturity for DSP/ANN C++ libraries, existing Anki C++ engine integration, and team familiarity make C++ the pragmatic choice for 1.0. Zig is premature for this use case. The Ollama pattern (Go wraps C++ via cgo) is validated as the industry reference.[^8][^9][^10][^2][^1]

### COMPONENT × LANGUAGE MATRIX

| Component | Language | Tier | Justification |
|---|---|---|---|
| DSP core (rFFT, norm, wavelet kernels) | **C++** | Robot + Box | NEON intrinsics, no GC, library richness (pffft, Ne10) |
| Hot ring-buffer index | **C++** | Robot | ETL containers, no heap, deterministic[^11] |
| Archive ANN index | **C++** (usearch core) | Box | Apache-2.0, SIMD, Go binding[^12][^13] |
| `.eng` format encoder/decoder | **C++** (codegen) | Both | FlatBuffers schema → C++ + Go + Python[^14] |
| Streaming writer / flush | **Go** | Box | Excellent IO concurrency, `vic-cloud` already Go[^15] |
| Service / gRPC API | **Go** | Box | Matches Vector's `vic-cloud` / wire-pod patterns[^16] |
| Engine integration (perception → fingerprint) | **C++** | Robot | Direct `vic-engine` linkage, no IPC overhead |
| Research / lab / codebook training | **Python** | Dev only | Experimentation velocity |

### FFI BOUNDARY MAP

```
[vic-engine C++] ──(direct call, same process)──▶ [ENGRAM reflex C++ lib]
[ENGRAM reflex C++ lib] ──(CLAD message / Unix socket)──▶ [ENGRAM box Go service]
[ENGRAM box Go service] ──(cgo, ~40 ns/call)──▶ [usearch C++ archive]
[ENGRAM box Go service] ──(cgo)──▶ [pffft C DSP lib]
[Python PoC] ──(reference spec only)──▶ [golden vector test suite]
```

### KEY FINDING: CGO OVERHEAD

cgo calls in Go 1.21 cost ~**40 ns/call** — comparable to `encoding/json` parsing a single digit. This is negligible when calls are batched (e.g., one cgo call per query returning a full result set). The real cgo risk is **threading**: cgo calls lock an OS thread, which can interact poorly with Go's goroutine scheduler under high concurrency. For ENGRAM's box-side archive queries (one query per recognition event, not tight loops), this is manageable.[^2][^17]

### GO GC RISK (BOX ONLY)

Go's GC does a brief STW pause ~twice per cycle — typically under 1 ms, tunable to ~400 µs peak with `GOGC=off` + `GOMEMLIMIT`. This is **acceptable for the box tier** (archive lookups, not reflex). It is **unacceptable on the robot**: Go must not run in `vic-engine`. The robot tier is pure C++.[^18][^19]

### LICENSE / RISK

No GPL in the recommended stack. C++ (MIT/BSD/Apache), Go (BSD), usearch (Apache-2.0), pffft (BSD-style). **FFTW is GPL — exclude entirely.**[^20][^21][^12][^22]

### CONFIDENCE: High | OPEN QUESTIONS: Whether Rust adoption by a small team is realistic for 1.0 (revisit for 2.0 if C++ memory bugs accumulate).

***

## V3 — The DSP / Math Core

### SUMMARY

The recommended DSP library for ENGRAM is **PFFFT** (BSD-style license, NEON-optimized, actively maintained in Android's external tree) for float32 on both robot and box. It is a drop-in, two-file C library with no dependencies. For the Cortex-A7 specifically, PFFFT with `-march=armv7-a -mfpu=neon -mfloat-abi=softfp -ffast-math` provides competitive performance. The FFTW license trap must be avoided unconditionally.[^23]

### LIBRARY COMPARISON

| Library | License | NEON | Robot feasible? | Notes |
|---|---|---|---|---|
| **PFFFT** | BSD-style | ✅ Yes (auto-vectorized) | ✅ Yes | Two C files, no deps, in Android[^23][^22] |
| **kissfft** | BSD | ⚠ Partial (float fast, fixed-point slow[^24]) | ✅ Yes | Simpler API, no NEON for fixed-point[^24] |
| **pocketfft** | BSD | ✅ (C++ template) | ✅ Yes | Used by NumPy; C++ header-only version available[^25] |
| **Ne10** | BSD | ✅ NEON-native | ⚠ Deprecated for Cortex-A | ARM has deprecated Ne10 for Cortex-A[^26] |
| **FFTW** | **GPL ⚠** | ✅ | ❌ **License trap** | Commercial license ~$12,500[^27]; GPL contaminates the whole project[^20][^21] |
| **FFTS** | BSD | ✅ | ✅ | Reported faster than FFTW on ARM[^28] |
| **gonum/fourier** | BSD | ❌ (pure Go) | ❌ | Box only; ~3–5× slower than C |

### ARM CORTEX-A7 SPECIFICS

The APQ8009 is `arm-linux-gnueabi` (soft-float ABI) with NEON available. The critical flag is `-mfloat-abi=softfp` (not `hard`) to match the system ABI, combined with `-mfpu=neon` to emit NEON instructions for vectorized math. NEON on Cortex-A7 provides float32 SIMD (4×f32 per cycle in 128-bit NEON registers). fp16 is **storage-only** on Cortex-A7/A8 — arithmetic requires conversion to float32 first, making fp16 a useful wire/disk format but not a compute format on this CPU.[^29][^30][^31][^32]

### WAVELET / SCATTERING EXTENSIBILITY

PFFFT and pocketfft both expose the raw FFT primitive needed to build convolution-based wavelet/scattering kernels. The architecture should define a `DSPCore` C++ interface with `rfft(float* in, float* out, int n)` and `convolve(...)` methods. PFFFT implements the former; small fixed convolution kernels can be written directly in C++ with NEON intrinsics for the latter, making the transition from 2-bin FFT to wavelet scattering a drop-in swap behind the interface.

### PARITY STRATEGY

Golden FFT vector approach: generate 1,000 random `[T,D]` input vectors in Python (numpy.fft.rfft as reference), store as `.npy`. The C/C++ implementation runs the same inputs through PFFFT and computes L2 difference. Acceptable tolerance: relative ≤ 1e-5 for float32 cross-language — consistent with float32 precision (7 decimal digits). Any output differing by more than this fails the golden test.[^33]

### RECOMMENDATION

**PFFFT** for both tiers. On robot: compile with `-O3 -march=armv7-a -mfpu=neon -mfloat-abi=softfp -ffast-math`. On box: compile with `-O3 -march=native`. Single codebase.

### LICENSE/RISK: PFFFT BSD-style ✅. Ne10 deprecated. FFTW GPL — hard exclude.[^26][^20]

### CONFIDENCE: High | OPEN QUESTIONS: Exact FFT size of the `[T,D]` input tensor (determines whether robot compute budget is tight); FFTS is another strong BSD candidate worth benchmarking.

***

## V4 — The Retrieval / ANN Engine

### SUMMARY

The recommended ANN solution is a **two-tier split**: on-robot, a hand-rolled bounded ring-buffer with exact linear scan (not a library); on box, **USearch** (Apache-2.0, C++ header-only core, native Go bindings). USearch's design mirrors the Ollama pattern perfectly: a single C++ header that Go wraps via cgo, with SIMD acceleration and cross-platform portability.[^12][^13][^34]

### ANN LIBRARY COMPARISON (BOX TIER)

| Library | License | Go binding | ARM build | Notes |
|---|---|---|---|---|
| **USearch** | Apache-2.0 ✅ | Native (cgo)[^13] | ✅ Portable | Header-only C++, SIMD, fp16[^34] |
| **hnswlib** | Apache-2.0 ✅ | Via cgo manually | ✅ Possible | Less portable; used in PoC |
| **FAISS** | MIT ✅[^35] | Via cgo manually | ⚠ Non-trivial[^36][^37][^38] | Heavy; SSE4/AVX flags hard-coded; aarch64 needs manual cmake hacking |
| **Annoy** | Apache-2.0 ✅ | Via cgo | ✅ Simple | No incremental insert; read-only after build |
| **DiskANN/SPANN** | MIT ✅ | No native Go | ⚠ Research-grade | Billion-scale on-disk; overkill for 1.0 archive |

**FAISS license note:** FAISS is now MIT (the old BSD+patents concern was resolved). However, FAISS ARM build remains non-trivial — no official ARM packages, manual CMake hacking required, SSE4/AVX flags hard-coded for x86. Excluded for 1.0.[^36][^37][^38][^35][^39]

### ON-ROBOT HOT INDEX

The robot reflex layer does **not** need an ANN library. The design is a **C++ ring buffer of N bounded entries** (ETL `etl::vector<StateVector, MAX_EPISODES>`) with exact dot-product scan. At N=256–1024 entries × D=64–128 float32 dimensions, a full linear scan takes ~10–50 µs on Cortex-A7 with NEON — well within a 33ms frame budget. This is deterministic, has zero dynamic allocation, and requires no external library.

### USEARCH KEY PROPERTIES

- Single C++ header (`usearch.hpp`) — no build system changes needed[^40][^34]
- Apache-2.0 license — clean[^12]
- Native Go bindings via cgo added in 2024[^13]
- Supports incremental insert and delete  
- SIMD-accelerated distance functions (NEON, AVX2, AVX-512)  
- fp16/int8 quantization built in  
- mmap-able persistence via memory-mapped files

### DISK-SCALE ARCHIVE (FUTURE)

For lifelong archives (>10M vectors), DiskANN/SPANN patterns (PQ in-memory + Vamana graph on SSD) are the right direction, but this is a post-1.0 concern. USearch's mmap persistence bridges the gap for 1.0.[^41][^42]

### CONFIDENCE: High | OPEN QUESTIONS: USearch Go binding maturity for production use; whether fp16 quantization in USearch is stable on ARM.

***

## V5 — The `.eng` / EGRV Format ("The Anki Way")

### SUMMARY

The production binary format for ENGRAM 1.0 should use **FlatBuffers** — this is literally what Anki chose for Vector's animation binary format. The animation `.bin` files are FlatBuffers encoded with a `.fbs` schema; `flatc` generates C++, Go, and Python readers from a single schema. This is the Anki way by direct evidence, not analogy.[^14][^43][^3][^44][^45]

### ANKI PRECEDENT (CONFIRMED)

> *"The animation binary files are based on Google's flatbuffers using a binary format."*[^3]
> *"When Vector reads and interprets the animation file it uses the flatbuffers library."*[^44]
> *"The tool used a plugin to emit the movements, as JSON using a format that the animation engine could read with the flatbuffers library."*[^45]

Anki chose FlatBuffers over CLAD for asset serialization because FlatBuffers provides: zero-copy mmap reads, schema versioning, forward/backward compatibility, and cross-language codegen. CLAD (Anki's custom IDL) is used for **IPC message definitions** (CLAD over sockets between vic-* processes), not for file formats.

### FORMAT COMPARISON

| Format | Zero-copy | Schema version | Cross-lang codegen | mmap-safe | License | Notes |
|---|---|---|---|---|---|---|
| **FlatBuffers** | ✅ Yes[^46][^47] | ✅ Yes | ✅ C++,Go,Python,Rust[^14] | ✅ Yes | Apache-2.0 | Anki's actual choice[^3] |
| Cap'n Proto | ✅ Yes[^46] | ✅ Yes | ✅ Many | ✅ Yes | MIT | Marginally slower builder[^48]; strong alternative |
| Protobuf | ❌ No[^46] | ✅ Yes | ✅ Many | ❌ No | Apache-2.0 | gRPC external API layer only |
| CLAD | ❌ (IPC only) | ⚠ Manual | C++/Python only | ❌ | Proprietary | Use for IPC messages, not files |
| Hand-rolled structs | ✅ (trivial) | ❌ Manual | ❌ Manual | ✅ Yes | — | Current EGRV v1; replace |
| Arrow/Parquet | ✅ | ✅ | ✅ | ✅ | Apache-2.0 | Cold archive analytics tier only |

### EGRV 2.0 FORMAT SPEC PROPOSAL

**Schema tooling:** FlatBuffers with `flatc` codegen. One `.fbs` file → C++ header, Go package, Python module.

**Proposed `.fbs` schema skeleton:**

```fbs
// engram.fbs
namespace Engram;

enum Precision : byte { F32 = 0, F16 = 1, I8 = 2 }

table StateVector {
  timestamp_us : uint64;           // microseconds since epoch
  session_id   : uint64;           // session/identity namespace
  label        : string;           // optional symbolic label
  dims         : uint16;           // vector dimensionality
  precision    : Precision = F32;
  data         : [ubyte] (required, force_align: 16); // raw fp32/fp16 bytes
  fingerprint  : [ubyte];          // pre-computed fingerprint hash
  crc32        : uint32;           // CRC of data field
}

table MemoryStore {
  version      : uint32 = 2;
  schema_hash  : uint64;           // SHA-64 of .fbs for format verification
  created_us   : uint64;
  label_ns     : string;           // identity namespace / robot ID
  vectors      : [StateVector];
}

root_type MemoryStore;
file_identifier "EGRV";
file_extension "eng";
```

**Key design decisions:**
- `force_align: 16` on `data` field ensures 16-byte alignment for NEON loads
- fp16 via `Precision = F16` stores half-size (2 bytes/dim), reads via NEON `vcvt_f32_f16` on decode
- `crc32` per-vector for integrity checking without full file scan
- `schema_hash` catches schema version drift across deployments
- `file_identifier "EGRV"` makes the magic bytes explicit (FlatBuffers 4-byte file ID)
- Forward/backward compat: FlatBuffers adds new fields at the end of tables transparently[^47][^49]

**Zero-copy read on ARM:** `mmap(fd, ...)` → `flatbuffers::GetRoot<MemoryStore>(ptr)` — no heap allocation, no parse step. Direct pointer access to `data` bytes aligned for NEON.[^46][^47]

**Migration from EGRV v1:** Write a one-time migration tool in Python that reads EGRV v1 (current hand-rolled format), re-encodes as EGRV v2 FlatBuffers, and validates CRC. Golden vectors are generated from v1 and verified against v2 reads.

### LICENSE/RISK: FlatBuffers Apache-2.0 ✅. Cap'n Proto is a safe fallback (MIT).[^14]

### CONFIDENCE: Very High (direct Anki precedent) | OPEN QUESTIONS: Whether CLAD is also used internally between vic-engine components for `StateVector`-type messages (likely yes for IPC, but FlatBuffers remains the right choice for file storage).

***

## V6 — Integration with Vector's Codebase

### SUMMARY

Vector runs five principal processes: `vic-engine` (C++), `vic-robot` (C++), `vic-anim` (C++), `vic-cloud` (Go), and `vic-gateway` (Go). The external SDK/cloud communication uses **gRPC + Protocol Buffers**; internal inter-process communication uses **CLAD messages over Unix sockets** (the Anki proprietary IDL for IPC). Animation assets use **FlatBuffers binary files**. ENGRAM maps cleanly onto this architecture.[^50][^15][^16][^3]

### INTEGRATION DIAGRAM

```
┌─────────────────────────────────────────────────────────┐
│  ROBOT (APQ8009 / Cortex-A7)                            │
│                                                         │
│  vic-engine (C++)                                       │
│  ├── perception path (camera/mic → feature extraction)  │
│  └── [ENGRAM reflex C++ lib, linked in-process]         │
│       ├── PFFFT DSP core (fingerprint)                  │
│       ├── ETL ring-buffer hot index (exact scan)        │
│       └── EGRV v2 mmap reader (FlatBuffers, no heap)    │
│                                                         │
│  ──── CLAD message over Unix socket ────────────────────┤
└───────────────────────────────────────────────────────  │
                                                          │
┌─────────────────────────────────────────────────────────┤
│  BOX (companion host — Linux/ARM64 or x86)              │
│                                                         │
│  vic-cloud / ENGRAM box service (Go)                    │
│  ├── gRPC server (matches behaviorComponentCloudServer) │
│  ├── streaming write / flush (goroutines, IO-bound)     │
│  ├── [cgo → usearch C++ archive, ~40 ns/call]           │
│  │    └── USearch HNSW index (mmap, fp16 quantized)     │
│  └── [cgo → PFFFT C for box-side fingerprinting]        │
│                                                         │
│  EGRV v2 archive (.eng files, FlatBuffers, mmap)        │
└─────────────────────────────────────────────────────────┘
```

### IPC MECHANISM

The on-robot ENGRAM reflex lib is **linked directly into `vic-engine`** (same process, no IPC overhead) to avoid stalling the real-time loop. The robot→box boundary uses the existing CLAD-over-socket or gRPC channel that `vic-cloud` already uses. This means ENGRAM adds no new IPC protocol — it reuses Vector's existing `vic-cloud` seam.[^16]

### PERCEPTION PATH

The mic/camera data flows into `vic-engine`, which calls the ENGRAM fingerprint function synchronously in the perception update loop. The result (a float32 StateVector) is pushed into the on-robot ring buffer (lock-free enqueue via moodycamel) and asynchronously forwarded to the box via the existing socket. This design ensures no blocking in the real-time loop.

### CONFIDENCE: High | OPEN QUESTIONS: Whether CLAD is fully defined for a `StateVector` message type or needs a new CLAD type added; exact integration point in the `behaviorComponentCloudServer` seam.

***

## V7 — ARM Real-Time & Memory Discipline

### SUMMARY

The on-robot ENGRAM component must operate within ~50–100 MB free RAM on the APQ8009 and produce no unpredictable pauses. The required primitives are: ETL containers (no heap), moodycamel ConcurrentQueue (lock-free MPMC), PFFFT with pre-allocated work buffers, mmap for the cold archive, and fp16 for compact storage. The soft-float ABI caveat on the APQ8009 (`arm-linux-gnueabi`, `-mfloat-abi=softfp`) means all floating-point must use the hardware VFP/NEON unit via `softfp` ABI, not pure soft-float emulation.[^51][^52][^30][^31][^32]

### ON-ROBOT REAL-TIME / MEMORY CHECKLIST

**Memory discipline:**
- [ ] Use `etl::vector<StateVector, N>` (ETL, MIT license) for the hot ring buffer — fixed compile-time capacity, no heap, cache-contiguous[^11]
- [ ] Pre-allocate all PFFFT work buffers at startup: `pffft_new_setup(n, PFFFT_REAL)` once; reuse across frames
- [ ] Store the cold archive mmap-only: `mmap(fd, 0, file_size, PROT_READ, MAP_SHARED, 0)` → FlatBuffers zero-copy reads
- [ ] Use fp16 on disk (`Precision::F16` in EGRV schema), convert to fp32 for compute via `vcvt_f32_f16` NEON intrinsic
- [ ] No `std::vector`, `std::map`, or `new`/`delete` in the hot path — ETL only

**Determinism:**
- [ ] Use `moodycamel::ConcurrentQueue` (lock-free, header-only, fully portable C++11) for the perception→fingerprint→ring-buffer pipeline[^52][^51]
- [ ] Never call `malloc`/`new` in the ISR or perception callback — arena-allocated only
- [ ] Consider `jemalloc` for arena allocation if any dynamic memory is unavoidable in startup paths
- [ ] Set thread priorities: perception callback at `SCHED_FIFO` to prevent preemption

**ARM / soft-float caveats:**
- [ ] Compile with `-march=armv7-a -mfpu=neon -mfloat-abi=softfp` (not `hard` — matches the robot's system ABI)[^30][^32]
- [ ] Validate: `arm-linux-gnueabi-gcc` is the correct toolchain (soft-float), not `arm-linux-gnueabihf` (hard-float)[^32]
- [ ] NEON is available and accelerates float32 ops even with `softfp` ABI
- [ ] FMA disable recommended for A7 (FMA counter-intuitively reduces FFT performance on A7/A9)[^7]

**Power / thermal:**
- [ ] Fingerprinting at 10–30 fps with NEON FFT on Cortex-A7: estimated ~5–15 mW DSP overhead. Monitor `cat /sys/class/thermal/thermal_zone*/temp` in soak tests.
- [ ] Implement a frame-skip strategy: only fingerprint when perception detects significant change (IMU-gated)

### ETL LIBRARY

ETL (Embedded Template Library) is MIT-licensed, header-only, tested with >10,000 unit tests, zero dynamic allocation, STL-compatible API. It is specifically designed for exactly this use case — deterministic fixed-capacity containers for embedded C++.[^53][^11]

### CONFIDENCE: High | OPEN QUESTIONS: Exact available RAM on APQ8009 with victor OS running (~512MB total, ~100–200MB available to user processes); whether `etl::vector` has sufficient capacity for a 1000-episode ring buffer at 128-dim fp16 (~256KB).

***

## V8 — Build, Cross-Compile, Test & Cross-Language Parity

### SUMMARY

Victor's existing build system is **CMake + Docker** (the `wire/build-d.sh` Docker-based build). The correct cross-compilation toolchain is `arm-linux-gnueabi-gcc` (soft-float) targeting `armv7-a`. Go cross-compilation for the box tier is trivially `GOOS=linux GOARCH=arm GOARM=7 go build`. The parity test harness uses **golden vectors**: Python generates canonical inputs/outputs, the C++/Go implementations are tested against them with float32 tolerance of 1e-5.[^54][^55][^56][^32]

### BUILD PLAN

**Robot (C++ via Victor's Docker):**
```cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_C_COMPILER arm-linux-gnueabi-gcc)
set(CMAKE_CXX_COMPILER arm-linux-gnueabi-g++)
set(CMAKE_C_FLAGS "-march=armv7-a -mfpu=neon -mfloat-abi=softfp -O3 -ffast-math")
```
Reuse the victor Docker image (`./wire/build-d.sh`) — it already contains the correct Linaro toolchain and sysroot.[^57][^54]

**Box (Go + cgo):**
```bash
CGO_ENABLED=1 CC=gcc CXX=g++ GOOS=linux GOARCH=amd64 go build ./...
# For ARM64 box:
CGO_ENABLED=1 CC=aarch64-linux-gnu-gcc GOOS=linux GOARCH=arm64 go build ./...
```
Pure Go cross-compile is trivially `GOOS=linux GOARCH=arm64 go build`; cgo requires the appropriate cross-compiler.[^55][^56]

**FlatBuffers codegen:**
```bash
flatc --cpp --go --python engram.fbs
# Generates: engram_generated.h (C++), engram/ (Go), engram_generated.py (Python)
```
Run `flatc` as a CMake `add_custom_command` so schema changes trigger regeneration automatically.[^43]

### GOLDEN VECTOR PARITY TEST DESIGN

```
golden_vectors/
├── generate_golden.py      # Python reference: reads random seeds, computes fingerprints via numpy
├── golden_inputs.npy       # 1000 × [T,D] float32 input tensors
├── golden_fingerprints.npy # 1000 × D float32 expected fingerprint outputs
├── golden.eng              # 100 EGRV v2 FlatBuffers records for format round-trip
└── test_parity.py          # pytest: loads golden, runs C ext / Go subprocess, checks tolerance
```

**Tolerance rules:**
- FFT/fingerprint: relative L2 difference ≤ 1e-5 per vector (float32 cross-language)[^33]
- EGRV encode/decode: **bit-exact** (deterministic FlatBuffers builder with canonical field order)
- ANN query: same top-1 result required (not float-level); recall@1 must remain 1.000 on the soak suite

**CI pipeline:**
1. `generate_golden.py` runs on Python reference (committed to repo as fixtures)
2. C++ unit test (`gtest`) links against the C++ DSP lib and reads golden fixtures
3. Go test (`go test ./...`) calls the cgo wrapper and compares against fixtures
4. Docker build runs robot cross-compile; `qemu-arm-static` smoke-tests the ARM binary

**Fuzz the format parser:**
Use `libFuzzer` or AFL++ on the FlatBuffers `ParseAndVerify` path to ensure malformed `.eng` files don't crash the robot process. FlatBuffers verifier catches out-of-bounds pointer arithmetic.[^58]

**Sanitizers:**
Compile the C++ DSP lib with `-fsanitize=address,undefined` in debug mode CI; `-fsanitize=thread` for the concurrent write path.

### CONFIDENCE: High | OPEN QUESTIONS: Whether victor's Docker image includes a recent enough `arm-linux-gnueabi-gcc` for C++17 features (ETL requires C++11 minimum, C++17 preferred[^11]).

***

## V9 — What (If Anything) Stays Python

### SUMMARY

Python's long-term role is precisely defined: it is the **executable specification** and the **research lab**. It runs in offline/development contexts only. No Python code ships on the robot or in the production box service.

### THE CLEAR BOUNDARY

**Python stays for:**
- `vector_engram/` — the canonical reference implementation; all golden vectors are generated here
- Offline training of the frozen codebook / scattering codebook (NumPy/SciPy/JAX)
- Frequency-symphony / VSA / wavelet scattering experiments (the other geodesic)
- Tooling: `.eng` file inspection, visualization, migration scripts, benchmarking harness
- The parity test suite (`pytest`) that validates C++ and Go implementations against Python output
- `soak.py` / `bench.py` — profiling and regression testing

**Python moves to C/Go for:**
- Any code in the robot's real-time path (fingerprint, ring-buffer query, EGRV read)
- The production box ANN query and EGRV write path
- The gRPC/cloud service layer

### NUMPY ↔ C PARITY GOTCHAS

NumPy's `rfft` uses `pocketfft` internally (not FFTW). PFFFT uses a slightly different butterfly ordering. To achieve cross-language parity, the C implementation should be validated against NumPy's output, not assumed to match. The golden vector suite catches these discrepancies. Key gotchas:[^26]
- NumPy `rfft` output is complex (alternating real/imag); ensure the C implementation matches the packing convention
- NumPy uses float64 internally for `rfft` even on float32 input unless `numpy.fft.rfft(x.astype(np.float32))` is explicitly used — pin to float32 in golden generation
- L2-norm tolerance for float32 cross-language: 1e-5 relative[^33]

### CONFIDENCE: Very High | OPEN QUESTIONS: None — this boundary is clean.

***

## V10 — The Order (Port Roadmap, Dependency-Sequenced)

### SUMMARY

The roadmap is dependency-ordered to maximize early value and minimize big-bang risk. The Anki way is **extend, don't replace**: each step adds a new implementation alongside the Python reference, validated by golden vectors before the Python path is deprecated.

### DEPENDENCY-ORDERED ROADMAP

```
PHASE 0 — Foundation (Week 1–2, zero code ported)
├── Profile PoC with py-spy to confirm hot-path table (V1)
├── Establish golden vector suite (1000 vectors, pytest, CI)
└── Commit EGRV v2 .fbs schema (V5) — this is the contract

PHASE 1 — Format Freeze (Week 2–3)
├── Run flatc to generate C++/Go/Python stubs from engram.fbs
├── Write migration tool: EGRV v1 → EGRV v2
└── Golden round-trip test passes (bit-exact)

PHASE 2 — C++ DSP Core (Week 3–5)   ← FIRST FAST CODE
├── Implement fingerprint() in C++ using PFFFT
├── Add golden parity tests (≤1e-5 relative)
├── Cross-compile for armv7-a (Docker + qemu smoke test)
└── On-robot timing: measure FFT latency at actual [T,D] size

PHASE 3 — C++ On-Robot Reflex (Week 5–7)
├── ETL ring-buffer hot index with exact scan
├── moodycamel ConcurrentQueue for async enqueue
├── EGRV v2 mmap reader (FlatBuffers zero-copy on ARM)
└── Integrate into vic-engine as a linked C++ library (CLAD IPC for box async path)

PHASE 4 — Go Box Service (Week 7–9)
├── Go service with gRPC (matches vic-cloud pattern)
├── cgo bridge to usearch C++ archive
├── cgo bridge to PFFFT for box-side fingerprinting
└── Streaming EGRV v2 writer with fsync

PHASE 5 — Box Archive (Week 9–11)
├── USearch HNSW index over EGRV v2 archive
├── Incremental insert / periodic persist (mmap)
└── ANN query parity: recall@1 = 1.000 on soak-50k suite

PHASE 6 — 1.0 Milestone (Week 11–13)
├── End-to-end integration test: robot fingerprint → box archive → query
├── Soak 50k at 30fps write rate on real hardware
├── Memory budget confirmed: on-robot <50MB footprint
├── Python runtime deprecated in production path
└── CI: golden vectors, sanitizers, fuzz the .eng parser
```

### MINIMAL 1.0 MILESTONE

**The smallest shippable 1.0 is Phases 0–4**: format frozen, DSP core in C++ with ARM cross-compile, Go service with cgo usearch, golden vector CI passing. Phase 5 (full archive) can ship as 1.1.

### FIRST STEP (MONDAY MORNING)

> **Run `py-spy record --native -o profile.svg -- python soak.py` and identify whether the hot path is FFT-dominated or hnswlib-dominated.** This single measurement gates everything — if HNSW is the bottleneck, Phase 3 (box archive) jumps ahead of Phase 2 (DSP core). If FFT dominates, proceed as ordered.

### WHAT CAN SHIP INCREMENTALLY

- The Python PoC remains the production system until Phase 6 gates pass
- Each Phase adds a parallel fast path validated against Python; the Python path is only removed when parity is confirmed
- The `.fbs` schema is the contract — commit it before writing any C++ or Go

***

## Final Synthesis

### 1. The Language Verdict

**C++ (robot reflex + compute core) + Go (box service) + Python (research lab only).** This is confirmed by: the Ollama architectural pattern, Vector's existing C++/Go process split, and the 40 ns cgo overhead being acceptable for batch box-side calls. Rust is a viable alternative to C++ for the compute core but adds ecosystem friction for 1.0. Go must **never** run on the robot (GC jitter, even sub-1ms STW, is unacceptable in `vic-engine`'s real-time loop).[^19][^15][^1][^2][^50]

### 2. Component → Language → Tier → IPC Table

| Component | Language | Tier | IPC Mechanism |
|---|---|---|---|
| rFFT fingerprint | C++ / PFFFT | Robot | In-process (linked) |
| L2-norm / distance | C++ / NEON | Robot | In-process |
| Hot ring-buffer index | C++ / ETL | Robot | In-process |
| EGRV v2 mmap reader | C++ / FlatBuffers | Robot | In-process |
| Async event forwarder | C++ | Robot | CLAD socket → box |
| Box gRPC service | Go | Box | gRPC (external SDK) |
| usearch archive | C++ (via cgo) | Box | cgo from Go |
| PFFFT box-side | C (via cgo) | Box | cgo from Go |
| EGRV v2 writer | Go | Box | Filesystem |
| Research / training | Python | Dev only | — |

### 3. EGRV 2.0 Format Spec Proposal

FlatBuffers + `engram.fbs` as specified in V5. Magic bytes `EGRV`, file extension `.eng`. One schema → `flatc` → C++ header + Go package + Python module. Zero-copy mmap on ARM. CRC per vector. fp16 storage. Forward/backward compat via table extension. Migration tool from v1 in Python. This is the Anki way — it is exactly how Vector's animation binaries work.[^3][^44][^45]

### 4. Dependency-Ordered Roadmap (PoC → 1.0)

```
Phase 0: Profile PoC → confirm hot path (py-spy, 1 day)
Phase 1: Freeze EGRV v2 .fbs schema + golden vectors (3 days)  ← FIRST STEP
Phase 2: C++ DSP core with PFFFT + ARM cross-compile (2 weeks)
Phase 3: C++ on-robot reflex + ETL + mmap reader (2 weeks)
Phase 4: Go box service + cgo usearch + gRPC (2 weeks)
Phase 5: Box archive + soak validation (2 weeks)
Phase 6: 1.0 integration, memory budget, deprecate Python runtime (1 week)
```

**Total to 1.0: ~10 weeks, serialized. First concrete deliverable: the `.fbs` schema file, commitable Day 1.**

---

## References

1. [On the architecture of ollama - Aili](https://aili.app/share/3vAn2Bn0Wn5yb6D32IMXDR) - On the architecture of ollama The article provides an in-depth overview of the architecture and impl...

2. [CGO Performance In Go 1.21 - Shane.ai](https://shane.ai/posts/cgo-performance-in-go1.21/) - Tl;Dr Cgo calls take about 40ns, about the same time encoding/json takes to parse a single digit int...

3. [How to convert animation bin files to JSON - Randall Maas](https://randym32.github.io/Anki.Vector.Documentation/how-to/How%20to%20convert%20animation%20bin%20files%20to%20JSON.html)

4. [How to Profile Python Code with cProfile and SnakeViz - how2](https://how2.sh/posts/how-to-profile-python-code-with-cprofile-and-snakeviz/) - Profile Python hotspots with cProfile, interpret results, and visualize call stacks with SnakeViz to...

5. [ARM Cortex-A7 GFLOPS Performance](https://gadgetversus.com/processor/arm-cortex-a7-gflops-performance/) - Performance of the ARM Cortex-A7 processor on the Geekbench 4 benchmark platform, with SGEMM, advanc...

6. [A tutorial for optimizing CPU bound applications in python](https://github.com/georgepar/python-performance-tutorial) - A tutorial for optimizing CPU bound applications in python - georgepar/python-performance-tutorial

7. [Fftw 3.3. 3 (official)](http://wits-hep.blogspot.com/2013/12/fftw-benchmarks-on-cortex-a7.html) - The Wits High Energy Physics Group blog for updates and info on research into the Higgs, Massive Aff...

8. [Is Rust C++-fast? Benchmarking System Languages on ...](https://arxiv.org/abs/2209.09127) - Rust is a relatively new system programming language that has been experiencing a rapid adoption in ...

9. [https://odr.chalmers.se/server/api/core/bitstreams...](https://odr.chalmers.se/server/api/core/bitstreams/e992c970-2824-498b-90fa-28f4504a2c37/content)

10. [Prefer Rust to C/C++ for new code.](https://cliffle.com/blog/prefer-rust/)

11. [GitHub - ETLCPP/etl: Embedded Template Library](https://github.com/ETLCPP/etl) - Embedded Template Library. Contribute to ETLCPP/etl development by creating an account on GitHub.

12. [usearch/LICENSE at main · unum-cloud/usearch](https://github.com/unum-cloud/usearch/blob/main/LICENSE) - Fast Open-Source Search & Clustering engine × for Vectors & Arbitrary Objects × in C++, C, Python, J...

13. [Add: Missing GoLang APIs (#435) · unum-cloud/usearch@a2719b9](https://github.com/unum-cloud/usearch/commit/a2719b9438164a9b474a087890dfed771c49a086) - Closes #409 --------- Co-authored-by: Ash Vardanian <1983160+ashvardanian@users.noreply.github.com>

14. [FlatBuffers: Memory Efficient Serialization Library - GitHub](https://github.com/google/flatbuffers) - FlatBuffers is a cross platform serialization library architected for maximum memory efficiency. It ...

15. [Source Code Location for each Program - Vector Documentation](https://randym32.github.io/Anki.Vector.Documentation/software-design/Source%20Code%20Location.html)

16. [Tutorial: How Anki Vector communicates? - Learn With A Robot](https://www.learnwitharobot.com/p/tutorial-secure-message-handling) - Part 1: Protocol Buffers: How to connect distributed systems with secure connections and streaming d...

17. [runtime: performance problem with many Cgo calls #19574](https://github.com/golang/go/issues/19574) - Please answer these questions before submitting your issue. Thanks! What version of Go are you using...

18. [Tuning Go Application, which has GC issues with a few steps - ITNEXT](https://itnext.io/tuning-go-application-which-has-gc-issues-with-a-few-steps-4487624b313e) - GC Pause Time is decreased from 40ms to 400µs at peak.

19. [Jeyhun Abbasov's Post - LinkedInwww.linkedin.com › posts › abbasovdev_gos-garbage-collector-does-not-s...](https://www.linkedin.com/posts/abbasovdev_gos-garbage-collector-does-not-stop-the-activity-7449819476415664130-S5eK) - Go's garbage collector does not stop the world like you think. Here is how it actually works. In Jav...

20. [License and Copyright (FFTW 3.3.10)](https://www.fftw.org/doc/License-and-Copyright.html) - License and Copyright (FFTW 3.3.10)

21. [License¶](https://pyfftw.readthedocs.io/en/latest/source/license.html)

22. [Consider pffft-fft library support · Issue #581 · MTG/essentia](https://github.com/MTG/essentia/issues/581) - https://bitbucket.org/jpommier/pffft High performance fft library BSD-style license ARM64 supported ...

23. [platform/external/pffft - Git at Google - Android GoogleSource](https://android.googlesource.com/platform/external/pffft/+/08f5ed2618ac06d7dcc83d209d7253dc215274d5)

24. [Neon · Issue #80 · mborgerding/kissfft](https://github.com/mborgerding/kissfft/issues/80) - kissfft on ARMv7 with fixed point is slow. A neon version would improve performance quite a bit. the...

25. [Which optimised lib for FFT is now current for Cortex A?](https://community.arm.com/support-forums/f/architectures-and-processors-forum/52830/which-optimised-lib-for-fft-is-now-current-for-cortex-a) - Is it the compute libs and that NE10 & cmsis are now depreciated for CortexA V8 64bit?

26. [Optimizing FFT Performance on ARM Cortex-A: Libraries, Trade-offs, and Implementation Strategies - System on Chips](https://www.systemonchips.com/optimizing-fft-performance-on-arm-cortex-a-libraries-trade-offs-and-implementation-strategies/) - The Fast Fourier Transform (FFT) is a cornerstone algorithm in digital signal processing (DSP), wide...

27. [FFTW - Fastest Fourier Transform in the West](https://tlo.mit.edu/industry-entrepreneurs/available-technologies/fftw-fastest-fourier-transform-west)

28. [FFTS -- Fastest FFT implementation, and Free/BSD License](https://forum.juce.com/t/ffts-fastest-fft-implementation-and-free-bsd-license/13056) - Check out FFTS. It has a permissive BSD license, and it is faster than FFTW, IPP, KissFFT, Apple vDS...

29. [Is arm_neon.h missing all float16_t types? - Stack Overflow](https://stackoverflow.com/questions/6588866/is-arm-neon-h-missing-all-float16-t-types) - The NEON intrinsic function prototypes that use __fp16 are only available for targets that have the ...

30. [GitHub - Christopher83/arm-cortex_a8-linux-gnueabi-linaro_4.9: Linaro GCC 4.9 Toolchain optimized for Cortex-A8 cpu](https://github.com/Christopher83/arm-cortex_a8-linux-gnueabi-linaro_4.9) - Linaro GCC 4.9 Toolchain optimized for Cortex-A8 cpu - Christopher83/arm-cortex_a8-linux-gnueabi-lin...

31. [TCWG-public - Confluence](https://linaro.atlassian.net/wiki/spaces/TCWGPUB/pages/25237062145/ARM+and+AArch64+Target+Triples)

32. [Downloads | 8.2-2019.01](https://developer.arm.com/downloads/-/gnu-a/8-2-2019-01) - The GNU Toolchain for the Cortex-A Family are integrated and validated packages featuring the GCC co...

33. [Truth for floating point types](https://truth.dev/floating_point.html) - For approximate equality, what tolerance should I use? You should aim to accept values within a rang...

34. [USearch: 10x Faster Vector Search Engine for Every Language](https://converter.brightcoding.dev/blog/usearch-10x-faster-vector-search-engine-for-every-language) - USearch delivers 10x faster vector search than FAISS in a single C++ header. Multi-language support,...

35. [faiss/LICENSE at main · facebookresearch/faiss](https://github.com/facebookresearch/faiss/blob/main/LICENSE) - A library for efficient similarity search and clustering of dense vectors. - facebookresearch/faiss

36. [Unable to install faiss-cpu on aarch64 with AWS Graviton Processor · Issue #1550 · facebookresearch/faiss](https://github.com/facebookresearch/faiss/issues/1550) - Summary Hi I'm trying to install faiss-cpu on an ubuntu machine with aarch64 configuration, but gett...

37. [Run on Arm (aarch64)](https://fast-image-retrieval.readthedocs.io/en/stable/arm.html)

38. [Compile in aarch64/arm64 #567 - facebookresearch/faiss - GitHub](https://github.com/facebookresearch/faiss/issues/567) - Does faiss support aarch64/arm64 ? I wanna compile faiss in nvidia Jestson TX2 which is the platform...

39. [How do licensing and community support differ among FAISS (MIT ...](https://zilliz.com/ai-faq/how-do-licensing-and-community-support-differ-among-faiss-mit-licensed-library-annoy-opensource-library-milvus-and-weaviate-open-source-databases-and-pinecone-closedsource-service) - **Licensing Differences** FAISS, developed by Meta, uses the **MIT License**, which is highly permis...

40. [GitHub - unum-cloud/USearch: Fast Open-Source Search & Clustering engine × for Vectors & Arbitrary Objects × in C++, C, Python, JavaScript, Rust, Java, Objective-C, Swift, C#, GoLang, and Wolfram 🔍](https://www.webkkk.net/unum-cloud/USearch) - Fast Open-Source Search & Clustering engine × for Vectors & Arbitrary Objects × in C++, C, Python, J...

41. [Scalable Disk-Based Approximate Nearest Neighbor Search ...](https://www.arxiv.org/pdf/2509.25487v1.pdf)

42. [DISKANN | Milvus Documentation](https://milvus.io/docs/diskann.md) - In large-scale scenarios, where datasets can include billions or even trillions of vectors, standard...

43. [FlatBuffers Compiler ( flatc )](https://flatbuffers.dev/flatc/)

44. [How to use Cozmo animation files - Vector Documentation](https://randym32.github.io/Anki.Vector.Documentation/how-to/How%20to%20use%20Cozmo%20animations.html) - When Vector reads and interprets the animation file it uses the flatbuffers library. This library us...

45. [Animation tool - Vector Documentation - Randall Maas](https://randym32.github.io/Anki.Vector.Documentation/tools/Animation%20tool.html) - The tool used a plugin to emit the movements, as JSON using a format that the animation engine could...

46. [Hacker News](https://news.ycombinator.com/item?id=23589117)

47. [FlatBuffers - Wikipedia](https://en.wikipedia.org/wiki/FlatBuffers) - FlatBuffers is a free software library implementing a serialization format similar to Protocol Buffe...

48. [Protobuf vs Flatbuffers vs Cap'n proto which is faster? - Stack Overflow](https://stackoverflow.com/questions/61347404/protobuf-vs-flatbuffers-vs-capn-proto-which-is-faster) - I decided to figure out which of Protobuf, Flatbuffers and Cap'n proto would be the best/fastest ser...

49. [What would a "FlatBuffers2" binary format look like? #5875](https://github.com/google/flatbuffers/issues/5875) - FlatBuffer's binary format has been set in stone for 6.5 years now, because we value binary forwards...

50. [Software error codes - Vector Documentation - Randall Maas](https://randym32.github.io/Anki.Vector.Documentation/troubleshooting/Software%20error%20codes.html)

51. [moodycamel::ConcurrentQueue download | SourceForge.net](https://sourceforge.net/projects/moodyc-concurrentqueue.mirror/) - Multi-producer, multi-consumer lock-free concurrent queue. This is an exact mirror of the moodycamel...

52. [A Fast Lock-Free Queue for C++ - moodycamel.com](https://moodycamel.com/blog/2013/a-fast-lock-free-queue-for-c++) - Lock-free programming is a way of writing thread-safe code such that in the case of contention, the ...

53. [Embedded Template Library (ETL) download](https://sourceforge.net/projects/embedded-template-lib.mirror/) - Download Embedded Template Library (ETL) for free. Embedded Template Library. C++ is a great languag...

54. [GitHub - kercre123/victor](https://github.com/kercre123/victor) - Contribute to kercre123/victor development by creating an account on GitHub.

55. [Cross compiling GO - Technical Discussion - Go Forum](https://forum.golangbridge.org/t/cross-compiling-go/34372) - I'm able to cross compile straight go to an arm target using: export GOARCH=arm export GOOS=linux go...

56. [Cross-compiling made easy with Golang | Opensource.com](https://opensource.com/article/21/1/go-cross-compiling) - To produce an Arm64 binary, all I had to do was set two environment variables when compiling the Go ...

57. [cmake-toolchains(7) — CMake 4.4.0-rc2 Documentation](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html)

58. [Cap&#39;n Proto, FlatBuffers, and SBE](https://www.cnblogs.com/wzjhoutai/p/6772658.html) - 转自：http://kentonv.github.io/capnproto/news/2014-06-17-capnproto-flatbuffers-sbe.html?utm_source=tuic...

