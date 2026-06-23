# ENGRAM FOR VECTOR — Adjustment Plan
## Turning the ENGRAM proof-of-concept into Vector's continuous situational memory
## Created: 2026-06-23 · Dexter × Claude Opus 4.8
## Source: deep analysis of /engram repo · companion to Vector-eng.md, DEEP_UNDERSTANDING_CONCEPT_01.md

---

## 0. Verdict up front

ENGRAM today is a **working, tested PoC for LLM session memory** — not production, and tightly coupled to
llama.cpp KV-caches. But its **core mechanism generalizes cleanly** to Vector's need: a continuous,
confidence-scored, µs-retrievable memory of *situations*. The work is **mostly decoupling + embedding +
streaming**, not a rewrite. Estimated **~2–3 weeks** to a robot-grade PoC; the functional demo path is ~11 hours.

---

## 1. What ENGRAM actually does today (the real pipeline)

```
text → llama.cpp inference → extract KV-cache blob → parse to tensors
     → compute_fourier_fingerprint (rFFT over layers, take freqs [0,1] = DC+1st harmonic, L2-norm, concat)
     → write_eigengram (.eng binary certificate, ~856 B)
     → faiss IndexHNSWFlat → 4-stage "geodesic" retrieval (HNSW → trajectory → negative-constraint → metadata)
```
- **Fingerprint** (`kvcos/core/fingerprint.py`): deterministic geometric projection of the KV manifold —
  **no training, no corpus dependency**. f0 = mean attention state, f1 = layer-progression "rhythm".
- **Format** (`kvcos/engram/format.py`): EIGENGRAM `EGR1` v1.2 — 99-byte header + fp16 vectors + embedded
  128-d `joint_center` so any reader can fold-in a query without a separate basis. Carries a **Semantic
  Coverage Score** and **retrieval margin** — i.e. confidence is baked into the certificate.
- **Retrieval** (`kvcos/engram/retrieval.py`, `hnsw_index.py`): faiss HNSW (M=32, efSearch=64), **~51µs/query**,
  5.7× over brute force; plus an apophatic "negative-constraint" stage (penalize known confusion partners).
- **Embedder fallback chain** (`embedder.py`): llama_cpp KV → sentence-transformers (MiniLM) → hash. Source
  tag travels in the file.
- **Surfaces**: MCP server (`mcp/engram_memory.py`, 7 tools — alpha), partial REST API, markdown knowledge index.
- **Proven**: 220 tests; format round-trip (20/20); Recall@1 ~98–100% @ N=200; cross-model margin +0.013,
  same-model +0.37; basis stability 0.997–0.999; 6 LLM families + Gemma-4 ISWA.

## 2. Proven vs stubbed (so we don't trust the wrong parts)

| Solid (keep) | Research-grade / stubbed (careful) | Desktop/LLM-coupled (must change) |
|---|---|---|
| Fourier fingerprint (f0+f1) | xKV projection mode (untested) | llama.cpp/GGUF bridge (`integrations/llama_cpp_bridge.py`) |
| EIGENGRAM format + fp16 codec | PolarQuant 3-bit compression (placeholder) | KV-blob parser tied to llama.cpp version (`blob_parser.py`) |
| faiss HNSW retrieval (51µs) | Redis/S3 storage backends (stubs) | assumes 16k+ context (Vector percepts are tiny) |
| confidence/margin in certificate | IndexC confidence DB (untested at scale) | batch writes (no streaming) |
| 220 tests, FP16/Q8_0 compression | MCP session format (alpha, unstable) | full-precision fingerprint ~50–100ms on CPU |

## 3. The reusable idea: KV-cache → situational fingerprint

The generalization is exact: **any structured state vector → spectral decomposition → compact fingerprint.**
For Vector a "situation" replaces a KV cache:
```
situation_t = concat(vision_embed, audio_embed, touch, imu, emotion_vector)   # ~400–660 dims
fp = normalize(concat(|rFFT(situation_t)|[0], |rFFT(...)|[1]))                  # compact fingerprint
```
Same format, same HNSW, same 4-stage retrieval — **only the input changes** (KV cache → fused perception).
The certificate's built-in confidence score becomes the **"safe read" gate** (don't act on / don't store a
low-coverage situational read) — this is exactly the semantic-entropy discipline from the memory report and
the DU Eq.1 write-gate.

## 4. What must be adjusted/built for Vector

### 4.1 Decouple fingerprinting from llama.cpp (the key blocker)
Introduce a `StateVector` protocol (`kvcos/core/state_interface.py`) so `compute_fourier_fingerprint()` takes
*any* source. Keep the existing `LlamaKVState`; add `PerceptionState` (fuses vision/audio/touch/imu/emotion).
**~100 LOC, zero breaking changes** to format or retrieval.

### 4.2 Two-tier embedded split (honors the Anki Way + the hardware)
- **On robot (APQ8009, ~512MB):** a *fast* fingerprint path (C/NEON, DC-component-first, fp16, ~5ms) writing to
  a small **hot HNSW** (M=16, efSearch=32, last ~1000 situations, ~50MB). Reflex (B1) retrieves here in µs.
- **On the Pi/box:** full-precision fingerprint, **full lifelong archive**, IndexC confidence history, the
  4-stage retrieval, cross-session analysis. Robot syncs to box every ~60s.

### 4.3 Streaming, continuous writes (10–30 fps)
ENGRAM assumes session-end batch writes. Add a `StreamingEngramWriter`: lock-free circular buffer +
background flush thread, so the perception loop **never blocks on I/O**. Validated target: 30 fps write with
p99 write < 50µs, encode ~5µs/frame.

### 4.4 Format v1.3 for embodied/lifelong archive (backward-compatible)
Extend EIGENGRAM with: `robot_id`, `sensor_config`, `activity`, `place`, `emotion_state` (valence/arousal/
engagement/frustration), `timestamp`. Old readers skip the v1.3 tail. Enables time-range/who/where queries.

### 4.5 Retrieval & persistence
faiss HNSW already meets µs targets and should hold sub-100µs to ~100k frames on a Pi; add latency
histograms. Storage layout: `~/.engram/archive/<robot>/<date>/frame_*.eng` + a rolling HNSW index;
hot cache FIFO on robot, archive tiering on box.

### 4.6 Drop / defer
Drop PolarQuant (FP16 is enough). Defer S3/Redis, the markdown knowledge index, and the REST API for Phase 1
(use MCP-style queries). Simplify the session propagator from session-based to continuous snapshots.

## 5. Keep / rewrite / drop (summary)

| Component | Action |
|---|---|
| Fourier fingerprint (f0+f1) | **Keep** — already generic |
| EIGENGRAM format | **Keep + extend to v1.3** |
| faiss HNSW + 4-stage retrieval | **Keep + adapt** (M/ef for embedded) |
| confidence/margin (SCS) | **Keep** — becomes the safe-read gate |
| llama.cpp bridge + blob parser | **Decouple** behind `StateVector` |
| session propagator | **Simplify** → continuous |
| streaming writes / hot-cold | **Build new** |
| PolarQuant, S3/Redis, REST, md-index | **Drop/defer** |

## 6. Phased plan

- **Phase 1A — Situational PoC (~week 1, ~16h):** `StateVector` + `PerceptionState`; synthetic perception
  frames; EIGENGRAM v1.3; embedded HNSW; integration test (write→index→retrieve, cosine>0.5, search<1ms).
  *Functional demo path ≈ 11h: decouple (3h) + streaming writer (4h) + hardware-sim test (4h).*
- **Phase 1B — Hardening (~week 2, ~20h):** streaming writer, hot/cold archive, lightweight IndexC,
  continuous snapshots, graceful degradation (HNSW down → hash fallback), 24h soak test.
- **Phase 1C — Vector integration (~week 3, ~12h):** wire `PerceptionState` to the real vision/audio/sensor
  pipelines on the box; background fingerprint task; first recall behavior ("a moment like this before").
- **Phase 2 (optional):** S3 archive tiering, temporal/who/where filters, activity classification on
  fingerprints, cross-session/box analytics.

## 7. Open questions
- Fingerprint **stability at short contexts** (Vector percepts ≪ 16k tokens) — must be measured; may need to
  fingerprint over a sliding window of recent frames rather than one frame.
- On-robot **hot-index size** within ~50–100MB free RAM (sets the FIFO depth).
- Whether the fast DC-only on-robot fingerprint retrieves well enough for B1, or B1 must defer more to the box.
- Exact `situation_t` schema + which channels are NEON-cheap enough for the 5ms on-robot path.

---

*ENGRAM's core was always general; it was just wearing an LLM costume. Dressing it for Vector is decoupling +
embedding + streaming — not a rewrite. The `MemoryStore` interface in the Deep-Understanding skeleton is the
seam where this plugs in.*
