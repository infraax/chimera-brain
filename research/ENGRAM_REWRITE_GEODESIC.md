# RESEARCH GEODESIC — ENGRAM 1.0: Language, Performance, Core Math & File Format
## How to rewrite/optimize ENGRAM from a Python PoC into a fast, Vector-native 1.0 — the Anki way
## Created: 2026-06-24 · Dexter × Claude Opus 4.8

> **How to use:** hand each *vector* (or the whole file) to a research agent / deep-research tool. Each is
> independently runnable. Return findings in the **Output** format. This geodesic is ONLY about the
> *implementation* of ENGRAM (language, speed, math core, file format, Vector integration) — NOT the
> conceptual/frequency-symphony direction (that's `FREQUENCY_MEMORY_RESEARCH_GEODESIC.md`).
>
> **State of play:** the Python PoC works and is verified (`vector_engram/`, 16/16 tests, soak 50k:
> recall@1=1.000, ~120µs hnsw queries, bounded memory). It proved the *concept*. Now we design 1.0.

---

## PRIME DIRECTIVE
> *Determine the optimal language (or combination of languages), library stack, core-math implementation,
> and binary file-format design to take ENGRAM from a working Python proof-of-concept to a production 1.0
> that (a) is fast and deterministic, (b) runs split across an ARM Cortex-A7 robot and a companion box,
> (c) integrates seamlessly with Vector's existing C++ engine + Go services, and (d) follows "the Anki way."
> Decide WHAT to optimize, in WHICH language, in WHAT ORDER, and HOW to design the `.eng` format.*

**Working hypothesis to test (not assume):** the right shape mirrors **Ollama**, which the user cited — a
**Go service/orchestration layer wrapping a C/C++ compute core (llama.cpp)**. I.e. *Go for the box-side
services and the custom-cloud seam (matches Vector's `vic-*` Go), C/C++ for the hot math + the on-robot
engine integration (matches Vector's C++ engine), Python demoted to the research/lab role.* Confirm, refute,
or refine this with evidence.

---

## CROSS-CUTTING CONSTRAINTS (apply to every vector — these ARE the Anki way)
1. **Measure before optimizing.** Profile the real PoC first; optimize the proven hot path, not guesses.
2. **Determinism & real-time.** On-robot code must avoid unpredictable pauses (e.g. Go GC stop-the-world,
   malloc in the hot loop). Flag any tech that injects jitter.
3. **ARM-first, edge-real.** Target the APQ8009 (Cortex-A7, ~512MB, NEON, soft-float caveats — see
   `CHIMERA_REVERSE_ENGINEERING.md`). Every choice notes on-robot vs box feasibility + footprint.
4. **License-clean.** Prefer MIT/BSD/Apache/ISC. Flag GPL/LGPL/AGPL (e.g. **FFTW is GPL**; some FAISS paths).
5. **Contract-first / parity.** Any rewrite must match the Python reference via **golden vectors** (`.eng`
   bytes + fingerprint outputs) — see `ADR_ENGRAM_INTEGRATION_SEAMS.md`. Cross-language bit/▵-tolerance parity is a hard requirement.
6. **Match Anki's existing patterns** — study how `kercre123/victor` actually does serialization (CLAD,
   FlatBuffers, the animation binary format), IPC, build, and ARM cross-compile; don't invent what Anki
   already solved.
7. **Two-tier split is assumed** (robot reflex + box archive); every component is placed in a tier.
8. **Keep the seam swappable** — the Python `StateVector`/`fingerprint`/`SituationIndex`/`MemoryStore`
   interfaces define the contract the new languages must honor.

---

## RESEARCH VECTORS

### V1 — Profile & decompose the PoC (where does time/memory actually go?)
- **Questions:** Break the pipeline into ops — fingerprint (rFFT over `[T,D]` + L2-norm), `.eng` encode/decode,
  index build, ANN query (hnswlib), streaming write/flush, disk IO. For a realistic load (10–30 fps write,
  µs query, 50k–1M archive): which ops are **compute-bound** vs **IO-bound** vs **glue**? What % of time is in
  each? Which truly need a fast language, and which are fine left as thin Python/Go glue?
- **Method:** profile `vector_engram` (`bench.py`, `soak.py`) with cProfile/py-spy; isolate FFT vs ANN vs
  serialize vs IO; estimate the same on ARM.
- **Return:** a hot-path table (op → %time → bound-type → tier → "needs fast lang? y/n") — the optimization
  priority list. **This gates everything else.**

### V2 — Language decision matrix (Go vs C vs C++ vs Rust vs Zig), per component
- **Questions:** For each ENGRAM component (DSP core, ANN index, serialization, streaming writer, service/API,
  on-robot reflex), score the candidate languages on: latency/throughput, **determinism (GC?)**, ARM/NEON
  support, library ecosystem (FFT/ANN/linalg), **FFI/interop cost**, integration with Vector
  (C++ engine / Go services), build complexity, maintainability for a small team. Is **one** language enough,
  or is a **combination** strictly better? Where exactly are the language boundaries (and their FFI seams)?
- **Look at:** the **Ollama (Go) + llama.cpp (C/C++)** pattern as the reference; cgo overhead & pitfalls; Go
  GC pause behavior under real-time load (we measured GC concerns in `Reesearch-Rapport.md`); Rust for
  determinism/safety vs ecosystem maturity; Zig for C-interop/cross-compile; C for the engine seam.
- **Return:** a component × language decision matrix with a recommended assignment + justification + the FFI
  boundary map. Explicitly answer: "Go, C/C++, Rust, or a combination — and which part is which."

### V3 — The DSP/math core (FFT/DWT/scattering) across languages
- **Questions:** Which FFT/DSP library per platform and language? Fixed-point vs float on Cortex-A7;
  **NEON** intrinsics; memory layout for cache efficiency. Note: the *transform itself may change* (the
  frequency/symphony research may move us from 2-bin FFT → wavelet/scattering) — so pick a math core that can
  do FFT **and** small wavelet/conv kernels. How do we keep the math **bit/▵-identical across Python↔C↔Go**?
- **Look at:** **kissfft** (MIT, tiny, embeddable), **PFFFT**/**pocketfft** (permissive), **Ne10** (ARM NEON
  DSP), **KFR** (DSP, check license), ⚠**FFTW (GPL)**, Go FFT options (gonum/fourier, scientificgo) and their
  speed vs C; SIMD in Go (Avo) vs cgo-to-C. Fixed wavelet/scattering kernels in C.
- **Return:** recommended DSP lib per tier/language + precision/SIMD plan + a parity strategy (golden FFT
  vectors). Flag the FFTW license trap.

### V4 — The retrieval/ANN engine, per tier
- **Questions:** On-robot **hot index** (small, bounded, deterministic — we have an exact ring buffer) vs box
  **archive** (large, ANN). Which ANN lib for the box: hnswlib, **usearch** (modern, portable, SIMD, great
  bindings), FAISS (heavy/ARM-unfriendly, license), annoy, ScaNN, vald/qdrant (external services)? Incremental
  insert, deletion, persistence/mmap, memory per vector at our dims, ARM feasibility, **Go vs C++ bindings**.
  Could the box archive be a Go-native ANN or must it wrap a C++ lib (the ollama pattern again)?
- **Look at:** usearch (Apache, C++ core + Go/Python/… bindings — strong candidate), hnswlib (C++), FAISS
  (license + ARM), DiskANN/SPANN for huge on-disk archives, the modern-Hopfield retrieval head (future).
- **Return:** ANN choice per tier with footprint/latency numbers + language-binding plan.

### V5 — The `.eng` / EGRV file format — "the Anki way" (this is a core deliverable)
- **Questions:** Design the production binary format. Decide: **schema/codegen approach** — hand-rolled
  little-endian structs (current EGRV v1) vs **FlatBuffers** (zero-copy, what Anki used for animations) vs
  **Cap'n Proto** vs **CLAD** (Anki's own IDL). Requirements: **versioning & forward/backward compat**,
  **mmap/zero-copy** read on ARM, alignment, **fp16/quantization**, **CRC/integrity**, **labels/namespaces**
  (for identity-shapes), timestamps, **cross-language codegen** (one schema → C, Go, Python readers),
  compactness for a lifelong archive, and a **migration path from EGRV v1**. How did Anki design *their*
  binary formats (study `victor/clad/`, `victor/animProcess` animation format, TRM Ch27)?
- **Look at:** FlatBuffers (zero-copy, Apache, Anki precedent), Cap'n Proto, CLAD (in the victor tree),
  Protocol Buffers (not zero-copy), Arrow/Parquet for the cold archive, content-addressing/Merkle (ties to
  N.A.P. durability), the EIGENGRAM format in `engram/kvcos/engram/format.py` and our `vector_engram/format.py`.
- **Return:** a concrete **EGRV 2.0 format spec proposal** (layout, schema tooling choice, versioning,
  zero-copy, integrity, labels) + migration plan + why-this-is-the-Anki-way justification.

### V6 — Integration with Vector's codebase (where ENGRAM physically lives)
- **Questions:** How do the C++ **engine** and Go **services** consume ENGRAM? On-robot: is the hot index a
  C++ library linked into `vic-engine`, or a separate process? Box: Go custom-cloud server (the
  `behaviorComponentCloudServer` seam) wrapping the C++ archive? IPC: **shared memory / mmap vs Unix sockets
  vs CLAD messages vs FFI**? Where's the language boundary that matches Anki's architecture? How does the
  perception path feed fingerprints in without stalling the real-time loop?
- **Look at:** `VECTOR_ENG_VICTOR_BASE.md` (the seams), `ADR_ENGRAM_INTEGRATION_SEAMS.md` (contract-first),
  victor's vic-* IPC (CLAD over sockets), `behaviorComponentCloudServer.cpp`, the micData→engine path.
- **Return:** an integration diagram: ENGRAM components × (robot/box) × language × IPC mechanism, honoring
  Anki's existing patterns.

### V7 — ARM real-time & memory discipline
- **Questions:** Techniques to keep the on-robot path deterministic & bounded in ~50–100MB free RAM: no-heap/
  arena allocation, **ETL (Embedded Template Library)** containers, ring buffers, mmap of the archive, fp16,
  lock-free queues (**concurrentqueue**), avoiding GC entirely on-device. Soft-float vs NEON on APQ8009
  (the `arm-linux-gnueabi` soft-float caveat from the RE doc). Power/thermal cost of continuous fingerprinting.
- **Look at:** ETL, concurrentqueue, jemalloc/arena allocators, mmap patterns, fixed-point DSP, the
  curation picks in `curation/awesome_go_cpp.md`.
- **Return:** an on-robot real-time/memory checklist + recommended primitives.

### V8 — Build, cross-compile, test & cross-language parity
- **Questions:** Toolchain to build/cross-compile for the robot (victor uses CMake + Buck + Vagrant/Docker —
  reuse it?). How to enforce **parity** between Python reference and C/Go impls (golden `.eng` + fingerprint
  vectors, ▵-tolerance tests in CI)? Reproducible builds, benchmarking harness, fuzzing the format parser,
  sanitizers. How to keep the Python PoC as the **executable spec** the fast langs are tested against.
- **Look at:** victor's build (`CMakeLists.txt`, `docker/`, `Vagrantfile`, Buck), cgo build, cross-compile for
  armv7, golden-vector testing patterns, the ADR's golden-vector plan.
- **Return:** a build+parity+CI plan + the golden-vector test design.

### V9 — What (if anything) stays Python
- **Questions:** Long-term role of Python: the **research lab** (scattering/codebook/VSA prototyping, the
  frequency-symphony experiments), training the frozen codebook offline, tooling/inspection, the executable
  reference spec? Where is Python a liability (production hot path, on-robot) vs an asset (experimentation
  velocity)? Numpy↔C parity gotchas.
- **Return:** a crisp "Python stays for X, moves to C/Go for Y" boundary.

### V10 — The ORDER (port roadmap, dependency-sequenced)
- **Questions:** Given V1's hot-path data, in what ORDER do we port/build for fastest risk reduction and
  earliest value? E.g.: freeze format spec (V5) → golden vectors → port DSP core (C) → port hot index (C) →
  Go service wrapper → engine integration → box archive → deprecate Python runtime. What's the minimal
  **1.0 milestone** vs later? What can ship incrementally without a big-bang rewrite (Anki way: extend, don't
  replace)?
- **Return:** a dependency-ordered roadmap PoC→1.0 with milestones, and the smallest first step.

---

## OUTPUT — Return Format (bring results back like this)
```
### V# — <title>
SUMMARY: 3–5 sentences answering the core question.
EVIDENCE: benchmarks / papers / docs / repo examples — links.
RECOMMENDATION: the concrete choice (language/lib/format/order) + why.
TIER & LANG: robot (C/C++/…) | box (Go/…) — placement.
LICENSE/RISK: flags.
PARITY/TEST: how we verify it matches the Python reference.
CONFIDENCE + OPEN QUESTIONS.
```
Final synthesis after all vectors:
1. **The language verdict** (one language vs the combination, with the boundary map).
2. **The component→language→tier→IPC table.**
3. **The EGRV 2.0 format spec proposal.**
4. **The dependency-ordered roadmap (PoC → 1.0) with the first step.**

---

## SEED SEARCH TERMS (paste-ready)
`ollama llama.cpp architecture go cgo` · `cgo overhead benchmark` · `go garbage collector pause real-time` ·
`kissfft vs pffft vs pocketfft benchmark arm neon` · `Ne10 ARM NEON FFT` · `FFTW license GPL` ·
`usearch vs hnswlib vs faiss benchmark` · `hnswlib arm` · `faiss arm aarch64 build` ·
`flatbuffers zero copy mmap` · `flatbuffers vs cap'n proto vs protobuf benchmark` · `CLAD Anki cozmo` ·
`zero-copy binary format versioning design` · `embedded template library etl` · `lock free queue moodycamel` ·
`cross compile armv7 cmake docker` · `rust vs go vs c++ embedded determinism` · `golden test cross language
parity floating point` · `mmap vector database on disk ann diskann spann` · `fp16 half precision arm neon`.

---

## INTERNAL CONTEXT (read alongside)
- Implementation to optimize: `vector_engram/` (PoC) — `fingerprint.py`, `format.py`, `index.py`, `store.py`,
  `archive.py`, `streaming.py`; verified in `vector_engram/VERIFICATION.md`.
- Decisions already made: `ADR_ENGRAM_INTEGRATION_SEAMS.md` (contract-first, golden vectors).
- Integration seams: `VECTOR_ENG_VICTOR_BASE.md`. Library picks: `curation/awesome_go_cpp.md`.
- Hardware/RE facts: `CHIMERA_REVERSE_ENGINEERING.md` (APQ8009, soft-float, NEON), `Reesearch-Rapport.md`
  (Go GC caveat). Doctrine: `ANKI_WAY.md`.
- The Vector source to mirror: `kercre123/victor` — `clad/`, `animProcess/`, `engine/`, build files.

> Note: keep this geodesic's language/format conclusions consistent with the **conceptual** direction —
> if the frequency-symphony research changes the transform (e.g. → scattering) or the metadata (labels/
> namespaces for identity-shapes), the DSP core (V3) and format (V5) must accommodate it.
