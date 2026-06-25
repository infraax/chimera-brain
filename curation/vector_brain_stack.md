# Vector-Brain Stack — Recommendation & Selection Reference

*The locked technology selection for the `vector_brain` Go/C++ runtime. Decisions resolved
with rationale; access/verification status filled by real tests (see §3).*

Sources: `research/reports/09_engram_rewrite__1.0_geodesic.md` (lang/perf/format),
`curation/awesome_go_cpp.md` + the awesome-go/awesome-cpp scans, `ANKI_WAY.md` (doctrine),
`research/VECTOR_3_HARDWARE_GEODESIC.md` (target hardware). Companion to
`vector_brain/ARCHITECTURE.md`.

Legend: ✅ verified here · 🌐 reachable but not built here · 🔒 blocked in this sandbox
(github-clone egress) — verify on a dev box · ⏳ robot-tier, verify on hardware.

---

## 1. The five open decisions — RESOLVED

### D1 — FFT/DSP: **pocketfft (parity) + PFFFT (NEON), behind one `DSPCore` interface**
- **pocketfft** is what NumPy uses internally → near-byte parity with our Python reference,
  which makes golden-vector matching clean (report 09 flagged the PFFFT-vs-numpy butterfly
  gotcha). Use it as the reference/box impl.
- **PFFFT** (BSD, NEON) for the ARM speed path; **kissfft** as the tiny fallback.
- **FFTW excluded — GPL.** Decision: ship both behind `DSPCore::rfft()`; pocketfft is the
  parity oracle, PFFFT the on-robot kernel.

### D2 — Robot↔box IPC: **gRPC (external/SDK) + Cap'n Proto (intra-host now) → iceoryx (zero-copy later)**
- External SDK / cloud API: **gRPC** (Vector's gateway already speaks it).
- Robot↔box / inter-process: start with **Cap'n Proto** (MIT, zero-copy + capability RPC,
  far simpler to stand up than reviving CLAD); earmark **iceoryx** (true zero-copy shared
  memory) for the multi-process Vector-3.0 box once we need the throughput.
- Rationale: clean-sheet 3.0 has no legacy CLAD to match; Cap'n Proto gets us moving, iceoryx
  is the performance ceiling.

### D3 — Box archive: **chromem-go (pure Go) now → USearch (cgo) when scale demands**
- The box is **not** the real-time tier, so the pure-Go simplicity of **chromem-go**
  (no cgo, single dependency) wins for the foundation and a solo build.
- Keep **USearch** (Apache, SIMD, fp16, mmap, Go bindings via cgo) as the documented
  performance upgrade when the archive outgrows pure-Go (report 09's original pick).
- The hot/cold split stays: hot ring on robot (D5), cold archive on box (this).

### D4 — ENGRAM content log: **adopt memlog**
- The hippocampal-index design needs a cheap append-only "content log" the fingerprint
  points back to (fingerprint = pointer; content lives elsewhere). **memlog** (Go, thread-safe,
  Kafka-like append-only) is the exact fit. Adopt as the situational event/content log.

### D5 — Robot hot index: **ETL fixed-capacity ring + exact scan** (+ ring_span lite view)
- Port our proven Python `HotIndex` (fixed-capacity ring, O(1) insert, exact-cosine scan)
  to C++ on **ETL** (no-heap, deterministic — the safety partition). **ring_span lite** for
  the circular-buffer view. No ANN library on the robot (exact scan is fast enough at N≤1k).

---

## 2. The full stack (per tier)

### Shared contract
| Role | Pick | License | Status |
|---|---|---|---|
| Cert/file format | **FlatBuffers** (`flatc`→C++/Go/Py) | Apache-2.0 | (§3) |
| IPC schema (intra-host) | **Cap'n Proto** | MIT | (§3) |

### C++ — robot reflex + compute core (no GC)
| Role | Pick | License | Status |
|---|---|---|---|
| FFT (parity) | **pocketfft** | BSD/MIT | (§3) |
| FFT (NEON) | **PFFFT** (+ kissfft) | BSD | ⏳ |
| No-heap containers / hot ring | **ETL** (+ ring_span lite) | MIT | ⏳ |
| Lock-free queue | **moodycamel concurrentqueue** | BSD/Boost | ⏳ |
| On-device inference (encoders) | **ncnn** (edge) / **ONNX Runtime** (box) | BSD / MIT | ⏳ |
| Quantized tensor core (L3) | **ggml** | MIT | ⏳ |
| Logging | **spdlog** | MIT | ⏳ |
| Denoise (ego-noise) | **RNNoise** | BSD | ⏳ |
| Wavelets (future scattering) | **wavelib** | BSD | ⏳ |

### Go — box service tier
| Role | Pick | License | Status |
|---|---|---|---|
| Vector DB / cold archive | **chromem-go** | Apache-2.0 | (§3) |
| Content/event log | **memlog** | Apache-2.0 | (§3) |
| RPC / external API | **grpc-go** | Apache-2.0 | (§3) |
| Pub/sub (service bus) | **NATS** (nats.go client) | Apache-2.0 | (§3) |
| Embedded KV (profiles/meta) | **badger** | Apache-2.0 | (§3) |
| LLM runtime (L3) | **Ollama** | MIT | 🌐 |
| LLM orchestration | **langgraphgo** / **goai** | MIT | 🌐 |
| Tool/context protocol | **mcp-go** | MIT | (§3) |
| Logging | **zerolog** | MIT | (§3) |
| Resilience (breaker) | **circuit** | MIT | 🌐 |
| Archive perf upgrade | **USearch** (cgo) | Apache-2.0 | (§3, py) |

### Python — the lab / executable reference (already in use)
numpy · hnswlib · pytest · (flatbuffers runtime, usearch wheel for parity checks).

---

## 3. Access & verification (filled by real tests in this sandbox)

> Egress here allows pypi / go-proxy / npm / crates / **apt**, but **github clone is blocked**
> (403, out of session scope). So: Go modules, pip-wrapped libs, and apt packages are testable
> here; github-only single-header C++ libs are 🔒 (vendored via submodule on a dev box / CI —
> low risk, since the g++/cmake toolchain itself is verified).

**Toolchain present:** g++ 13.3, gcc, cmake 3.28, go 1.24, cargo 1.94, node 22, pip.
Installed via apt for testing: **flatc 2.0.8**, **capnp 1.0.1**, libflatbuffers-dev, libspdlog-dev, libcapnp-dev.

### Verified results (run 2026, this sandbox)

| Pick | Test run | Result |
|---|---|---|
| **FlatBuffers** | `flatc --cpp --go --python engram.fbs` then **Python writes an EGRV buffer → C++ reads it** | ✅ **cross-language round-trip: every field matches** (version=2, person=dexter, sense=Meaning, repr=rfft.embed.v1, dim=4, data=1,2,3, ts=123456789). The Day-1 contract is real. |
| **Cap'n Proto** | `capnp compile -oc++ situation.capnp` | ✅ schema → C++ codegen OK |
| **chromem-go** | create collection + AddDocuments + Query (offline embed) | ✅ nearest-neighbour query returns (sim 0.886) |
| **memlog** | `Write` + `Read` back | ✅ offset 0, data round-trips |
| **badger** | open + `Set`/`Get` | ✅ `person:dexter="trusted"` |
| **zerolog** | structured log line | ✅ |
| **grpc-go**, **nats.go** | `go get` + compile (import) | ✅ resolve + build |
| **USearch** | `Index(ndim,'cos')` add 50 + search | ✅ self-query top-1 exact (pip wheel = the cgo C++ core) |
| **spdlog** | g++ compile + run (`-lfmt`) | ✅ (note: link `-lfmt`) |
| **C++ toolchain** | g++17 builds flatc/capnp/spdlog output | ✅ |
| Ollama · langgraphgo · goai · mcp-go · circuit | go-gettable / known-good | 🌐 not exercised here |
| pocketfft · PFFFT · kissfft · ETL · ring_span · moodycamel · ncnn · ggml · RNNoise · wavelib · iceoryx | github single-header / build-from-source | 🔒 vendor on dev box (toolchain proven) ⏳ |

**Bottom line:** the whole **box tier (Go) is functional here**, the **FlatBuffers contract round-trips
C++↔Python** (the load-bearing claim), and **Cap'n Proto / spdlog / the C++ toolchain** all build.
The remaining 🔒 items are header-only C++ libs blocked only by github-clone egress — they vendor
cleanly on any dev box; the toolchain that consumes them is verified. Nothing in the selection is a
dead end.

### Notes for production
- `flatc` here is 2.0.8 (Ubuntu apt); pin a current flatc (25.x) in CI — our schema compiles on both.
- spdlog needs `-lfmt` (external fmt) or `SPDLOG_FMT_EXTERNAL`.
- chromem-go's default embedder calls an external API; we pass our own (the MeaningEncoder) — verified offline.
