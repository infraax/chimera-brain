# Vector-ENGRAM — CHANGELOG

All notable changes to the `vector_engram` package (the Vector adaptation of the ENGRAM
mechanism: continuous *situational* memory via Fourier fingerprints + ANN retrieval).

Format: reverse-chronological. Each entry = what changed + why + how it was verified.

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
