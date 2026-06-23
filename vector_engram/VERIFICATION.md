# Vector-ENGRAM — Verification

How to run the tests and verify behavior on larger corpuses, plus the **real measured
results** from this machine (no simulations — real numpy FFT, real fp16 `.eng`
serialization, real hnswlib ANN retrieval, real recall metrics on generated corpora).

## Environment
- Python 3.11.15
- numpy 2.4.6, hnswlib (installed via `pip install numpy hnswlib`)
- The upstream `engram` repo's own test suite needs `torch` + `faiss-cpu` + GGUF models
  and is **not** run here; `vector_engram` is the Vector adaptation built on top and is
  fully self-contained (numpy + optional hnswlib).

## 1. Run the unit/integration tests
From the repo root (`chimera-brain/`):
```bash
python3 -m vector_engram.tests.test_vector_engram     # plain runner, exits nonzero on failure
# or, if pytest is available:
pytest vector_engram/tests/ -q
```
**Result (this machine):** `7/7 passed`
- `test_format_roundtrip_fp16_preserves_cosine`  — fp16 `.eng` round-trip preserves direction (cosine > 0.999)
- `test_fingerprint_determinism_and_dim`         — deterministic, correct dim (D*2)
- `test_fingerprint_stable_under_noise_and_discriminates` — same-situation cosine > 0.8 and > cross-situation
- `test_end_to_end_recall_exact`                 — write→index→retrieve recall@1 ≥ 0.90 (exact)
- `test_end_to_end_recall_hnsw`                  — recall@1 ≥ 0.85 (hnsw)
- `test_archive_write_reload_roundtrip`          — `.eng` archive persists and reloads, retrieval intact
- `test_raw_state_path_decoupled_from_llama`     — arbitrary `[T,D]` state fingerprints (the decoupling)

## 2. Larger-corpus verification (the benchmark)
```bash
python3 -m vector_engram.bench --prototypes 300 --copies 100 --queries 500 --backend both
# knobs: --n <total>  --noise <float>  --backend hnsw|exact|both
```
Reports, per backend: build time, query latency p50/p99 (per single-situation query,
**including** the query's FFT fingerprint), and recall@1 / recall@5 (does the nearest
stored situation share the query's situation key?).

### Measured scaling (real runs)
| N | backend | build | query p50 | query p99 | R@1 | R@5 |
|---|---|---|---|---|---|---|
| 5,000  | exact | 0.35s | 3,541 µs | 8,481 µs | 1.000 | 1.000 |
| 5,000  | hnsw  | 1.30s | 113 µs | 250 µs | 1.000 | 1.000 |
| 10,000 | exact | 0.59s | 9,112 µs | 20,364 µs | 1.000 | 1.000 |
| 10,000 | hnsw  | 3.32s | 137 µs | 263 µs | 1.000 | 1.000 |
| 30,000 | exact | 1.82s | 39,381 µs | 56,559 µs | 1.000 | 1.000 |
| 30,000 | hnsw  | 10.13s | 125 µs | 255 µs | 0.994 | 0.994 |

**Takeaways (honest):**
- **HNSW retrieval stays ~120–140 µs regardless of N** (the µs-class retrieval claim holds; this figure
  *includes* computing the query fingerprint, so the raw index query is faster still).
- **Exact** is the recall ground truth and is fine up to ~10k, but scales linearly (39 ms at 30k) — it's the
  intended **on-robot small hot-index** backend, not the box archive backend.
- Recall is high because situations are well-separated prototypes mean-pooled over an 8-frame window; the
  DC (f0) component is intrinsically noise-robust (averaging cancels per-frame noise).

### Noise stress (to prove recall is meaningful, not rigged) — 10k, hnsw
| noise σ | R@1 | R@5 | query p50 |
|---|---|---|---|
| 0.5 | 1.000 | 1.000 | 164 µs |
| 1.0 | 1.000 | 1.000 | 179 µs |
| 1.5 | 1.000 | 1.000 | 196 µs |
| 2.0 | 0.992 | 1.000 | 237 µs |
At σ=2.0 (8× the within-window trend, 2× the unit-variance prototype spread) recall@1 only falls to 0.992 —
graceful degradation, exactly the "windowed DC fingerprint is robust" property we want.

## 3. What "verified" means here vs. what's still ahead
**Verified now (Phase 1A):** decoupling from llama.cpp (`StateVector`/`PerceptionState`/`RawState`), the
situational Fourier fingerprint over a frame window, the `.eng` v1 codec round-trip, ANN retrieval (hnsw +
exact), archive write/reload, recall + latency at 5k–30k with noise stress.

**Not yet (flagged honestly):**
- Real perception features (this uses a realistic synthetic generator; swap in actual vision/audio/IMU/emotion
  features from the Vector pipeline).
- On-robot fast path (C/NEON, DC-only, fp16) and the hot/cold split running on the APQ8009.
- Streaming continuous writes at 10–30 fps (Phase 1B `StreamingEngramWriter`).
- faiss-MKL parity (ENGRAM's note: conda-forge faiss is ~18× slower; hnswlib here is a clean stand-in).
- Fingerprint behavior on *near-duplicate* situations (harder regime than well-separated prototypes).

## 4. Verifying on your own / real data
1. Replace `vector_engram.synth` frames with real fused perception windows (`PerceptionFrame` per frame,
   `PerceptionState.push()` to maintain the rolling window).
2. Set `dim = D * len(freqs)` where `D` is your fused feature size.
3. Use `backend="exact"` to get **ground-truth recall**, then compare `backend="hnsw"` recall against it —
   the gap is your ANN approximation error (should be < ~1%).
4. Scale `--n` up; watch that hnsw p99 stays flat and recall holds; if recall drops, raise `ef_search`
   (`SituationMemory(..., ef_search=128)`) — the classic recall/latency knob.
