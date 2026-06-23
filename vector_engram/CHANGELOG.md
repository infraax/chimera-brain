# Vector-ENGRAM — CHANGELOG

All notable changes to the `vector_engram` package (the Vector adaptation of the ENGRAM
mechanism: continuous *situational* memory via Fourier fingerprints + ANN retrieval).

Format: reverse-chronological. Each entry = what changed + why + how it was verified.

---

## [0.2.0] — 2026-06-23 — Phases 1B + 1C + 2: hardening, perception worker, query

**Goal:** finish the ENGRAM adjustments end-to-end before moving on — continuous
operation hardening (1B), the perception→memory bridge (1C), and useful query layers (2).

### Added
- **Phase 1B — hardening**
  - `archive.py` — `HotIndex` (fixed-capacity exact-cosine **ring buffer** = the on-robot
    hot index, O(1) insert, FIFO evict) + `HotColdMemory` (hot ring + cold hnsw/disk
    archive, **spill-on-evict**, merged hot+cold retrieval). Bounded RAM for 24/7 use.
  - `streaming.py` — `StreamingEngramWriter`: non-blocking bounded-queue writes on a
    background flush thread; **load-sheds (drops oldest)** under back-pressure so the
    perception loop never stalls.
  - `confidence.py` — `ConfidenceLog` (IndexC): per-situation hit/miss history,
    `should_preempt()` for chronically-wrong matches, JSON persistence.
  - `soak.py` — continuous-operation verification (bounded memory, sustained throughput,
    stable recall over 50k writes).
- **Phase 1C — perception bridge**
  - `perception.py` — `PerceptionSource` protocol, `FingerprintWorker` (rolling window →
    emits a situation every `stride` frames / on metadata change), `MockPerceptionSource`
    (real loop, generated data), `recall_summary()` (speakable recollection for L3/voice).
- **Phase 2 — query**
  - `query.py` — `filter_retrieved()` (who/where/activity/time-range) + `SituationClassifier`
    (training-free weighted k-NN predicting person/activity/place from a fingerprint).
  - `tests/test_phases_1b_1c_2.py` — 9 tests across all three phases.

### Fixed
- **Concurrency race in `StreamingEngramWriter`** (found by the soak test, not a unit test):
  the background flush thread and `close()`'s synchronous flush both called the
  non-thread-safe sink concurrently, losing/corrupting writes. Fixed with a `_drain_lock`
  (single-consumer invariant) + `close()` now stops/joins the thread before the final drain.

### Verified (real runs, this machine)
- `test_phases_1b_1c_2`: **9/9 passed** (+ the original `7/7` still green).
- HotIndex: bounded at capacity, correct FIFO eviction (250 inserts→100 retained, 150 evicted).
- HotCold spill: 300 writes → hot=100, cold=200; merged recall@1 **≥ 0.90**.
- Streaming: 200 enqueued → 200 flushed, **0 dropped** when drained; undersized buffer
  **sheds 150/200** (bounded memory) as designed.
- Classifier: person+activity+place exact-match accuracy **≥ 0.85** (24 prototypes).
- **Soak (50k situations, hot cap 1000):** dropped=0, hot bounded at 1000, cold=49000,
  **post-soak recall@1 = 1.000**, merged query p50≈347µs/p99≈501µs, sustained throughput
  ~2.1k situations/sec incl. fingerprint+index+persisting 50k `.eng` files (≫ 10–30 fps).

---

## [0.1.0] — 2026-06-23 — Phase 1A: decouple + situational fingerprint, end-to-end

**Goal:** Realize Phase 1A of `ENGRAM_FOR_VECTOR.md` — take ENGRAM's proven core (Fourier
fingerprint → compact certificate → ANN retrieval) and **decouple it from llama.cpp KV-caches**
so it ingests an arbitrary *situational* state, then prove it works end-to-end with real code
(real numpy FFT, real binary serialization, real hnswlib retrieval, real recall metrics).

### Added
- `state.py` — `StateVector` protocol (the decoupling seam) + `PerceptionState`
  (vision/audio/touch/imu/emotion → a `[T, D]` window) + `RawState` (arbitrary `[T, D]`).
  Mirrors the `kvcos/core` "anything fingerprintable" idea; replaces the hard llama.cpp coupling.
- `fingerprint.py` — `fingerprint(frames, freqs=(0,1))`: real `rFFT` over the **time axis** of a
  short frame window (DC = "what is happening", 1st harmonic = "how it is changing"). This is the
  faithful generalization of ENGRAM's `compute_fourier_fingerprint` (which FFT'd over LLM layers)
  and directly answers the open "short-context stability" question from the plan by fingerprinting a
  *window* of frames instead of a single frame.
- `format.py` — `EGRV` v1 binary certificate (`.eng`): little-endian, fp16 vector, with the
  Vector-specific metadata from format-v1.3 in the plan (robot_id, timestamp, activity, place,
  person, emotion[4], source_id). Real `struct` encode/decode + round-trip.
- `index.py` — `SituationIndex` with two **real** backends: `hnswlib` (cosine) and an exact
  numpy cosine index (ground-truth for recall verification / embedded-small fallback).
- `store.py` — `SituationMemory`: write `PerceptionState`→fingerprint→`.eng`→index; `knn`;
  reload an archive from disk; optional hot-cache cap. Exposes a `MemoryStore`-compatible surface
  so it drops into the Deep-Understanding skeleton (`MemoryStore` seam).
- `tests/` — real end-to-end tests (format round-trip, fingerprint determinism/stability/
  discrimination, write→index→retrieve recall, archive reload, hnsw-vs-exact agreement).
- `bench.py` — larger-corpus verification (recall@1, build time, query p50/p99 latency) at
  configurable N (1k/10k/30k).
- `VERIFICATION.md` — how to run tests + how to verify on larger corpuses.

### Verified (real runs, this machine — Python 3.11.15, numpy 2.4.6, hnswlib)
- Tests: **7/7 passed** (`python3 -m vector_engram.tests.test_vector_engram`).
- Recall@1 (write→index→retrieve, fresh noisy query variants):
  - exact: **1.000** at 5k/10k/30k
  - hnsw:  **1.000** at 5k/10k, **0.994** at 30k
- Noise stress (10k, hnsw): R@1 **1.000** up to σ=1.5, **0.992** at σ=2.0 (graceful).
- Query latency incl. fingerprint FFT: hnsw **~113–237 µs p50** (flat as N grows);
  exact linear (3.5 ms@5k → 39 ms@30k) — intended as the small on-robot hot index.
- fp16 `.eng` round-trip preserves direction (cosine > 0.999); archive reload intact.
- Full numbers + how-to in `VERIFICATION.md`.

### Notes / honesty
- This is the **box-side** reference implementation (numpy). The on-robot fast path (C/NEON,
  DC-only, fp16) is future work (Phase 1B); the format + index are designed for that split.
- We did **not** modify the upstream `engram` clone (separate repo); this package is the Vector
  adaptation built on top, mirroring the engram mechanism with citations in code comments.
