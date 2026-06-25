# Vector-ENGRAM — CHANGELOG

All notable changes to the `vector_engram` package (the Vector adaptation of the ENGRAM
mechanism: continuous *situational* memory via Fourier fingerprints + ANN retrieval).

Format: reverse-chronological. Each entry = what changed + why + how it was verified.

---

## [0.7.0] — 2026-06-24 — Phase 5: COMPOSE — weaving a self (the self-frequency)

**Goal:** the payoff the gate unblocked — Vector's "system prompt" as an ENGRAM shape, not
a text file: many remembered moments woven under a label into ONE big frequency the
creature calls "self" (and "environment", "person:dexter", "place:desk"). Recognition
becomes resonance — *does this moment belong to me / my world / this person?* Built per the
Phase-4 recipe: project → per-slot role-keys → bind → bundle (≤24/leaf, hierarchy) → cleanup.

### Added
- **`compose.py`**:
  - `Identity` — one labelled shape. `weave()` (grow the self over lived moments),
    `shape()` (the labelled self-frequency = `label_key ⊛ centroid`, one fixed vector),
    `resonance()` (belonging: cheap, unbounded), `recall_members()` (enumerate, capacity-
    bounded, per leaf). Leaf hierarchy (≤`LEAF_CAP`=24/leaf) holds arbitrarily many members.
  - `SelfModel` — the creature's set of identities (shared projection so shapes are
    comparable); `weave(label, …)`, `resonances()`, `recognize()` (which identity is this?),
    `self_shape()` (the whole personality as ONE shape labelled 'self'),
    `shape_resonance(label, …)` (query the single composed shape *by label*).
  - **Hook (documented):** a consolidation / "sleep" pass (prune, merge, re-bundle,
    EIGENGRAM stability) — left as a seam until we have lived data.

- **`tests/test_compose.py`** — 5 end-to-end tests.

### Measured
- **Belonging works perfectly:** a new dexter moment → `recognize` → `person:dexter`
  **40/40**; resonances dexter **0.99** vs stranger 0.72 vs kitchen 0.66.
- **The single composed self-shape is queryable by label:** `shape_resonance(dexter | person:dexter)`
  0.58 > `(… | person:stranger)` 0.40 — membership read straight off the one 2048-D frequency.
- **Enumeration of DISTINCT members is exact even past one leaf** (100% at 16, 24, **40**
  members — the leaf hierarchy works). Honest caveat: **near-duplicate** members aren't
  individually enumerable (and needn't be — repetition reinforces the shape's resonance).

Verified: `pytest` → **41 passed** (36 prior + 5 new). The "living self-frequency" is real.

---

## [0.6.0] — 2026-06-24 — Phase 4: the capacity gate (does COMPOSE work on our vectors?)

**Goal:** the load-bearing experiment before building COMPOSE (identity bundles / the
"self-frequency"): measure whether many correlated fingerprints can be woven under a label
and still be individually recovered (`frequency_memory__UNIFIED.md`, Experiment #2). Also
inspect what the fingerprints actually are.

### Added
- **`vsa.py`** — minimal HRR binding algebra: `bind` (circular convolution), `unbind`
  (circular correlation), `bundle` (normalized superposition), `cleanup` (item-memory
  nearest), `random_vectors`, `RandomProjection` (D→Dhi, seeded), `pairwise_cosine_stats`.
- **`capacity_experiment.py`** (runnable: `python -m vector_engram.capacity_experiment`) —
  fingerprint inspection + bundling-capacity sweep across conditions.
- **`CAPACITY_RESULTS.md`** — the recorded run + interpretation + the gate verdict.
- **`tests/test_vsa_capacity.py`** — 5 tests (HRR roundtrip, bundle+cleanup, orthogonality
  vs correlation, JL cosine-preservation, the capacity ordering).

### Measured (the actual numbers)
- Fingerprints: amplitude is all-positive, per-block unit-norm (full-norm √2), **separates
  situations** (within-cos 0.96 vs across 0.69, gap +0.28). GDF adds signed phase, smaller
  general gap (+0.22) — its value is temporal order, not discriminability.
- **The correlation is real:** raw fingerprints mean |cos| = **0.673** (random = 0.052).
- **Capacity@0.9:** random@230 = **16**; raw-amplitude@230 = **8** (correlation halves it);
  gdf@460 = 8 (better tail); **projected raw@2048 = 32** (4× recovery, even though JL keeps
  corr ≈ 0.68); random@2048 = 48+. Binding with random roles decorrelates the *bundle
  components*, so lifting dimension — not decorrelating items — is what buys capacity.

### GATE VERDICT — **PASS → COMPOSE is unblocked**
Project impressions to ~2048-D before bind+bundle (8→32 capacity); leaf-bundle ≤ ~24 with a
hierarchy; cleanup memory mandatory. Next phase builds `compose.py` (the "self-frequency").
Verified: `pytest` → **36 passed** (31 prior + 5 new).

---

## [0.5.0] — 2026-06-24 — Phase 3: recall by resonance (Modern Hopfield, RETRIEVE)

**Goal:** generalize nearest-neighbour recall to resonance. Modern Hopfield retrieval is
the attention update, and cosine-kNN is its β→∞ (infinitely sharp) special case
(`frequency_memory__UNIFIED.md`). So we don't replace the store — we add a sharpness
dial (β) and optional settling steps, getting episodic↔contextual recall and (in the
right regime) pattern completion, with zero new storage.

### Added
- **`resonance.py`** — `resonate(cue, patterns, beta, steps)` (the Hopfield update:
  `w=softmax(β·Px)`, `x←Pᵀw`, repeat) + a stable `softmax`. Creature framing: a cue can
  *resonate* across memories or *settle* toward the one it half-matches.
- **`store.py`** — `SituationMemory.recall_resonant()` (two-stage: index prefilters
  candidates → resonance reranks, the report's pattern) and a `beta`/`steps` dial on
  `TwofoldMemory.recall_reflex/recall_meaning` — **`beta=None` = the sharp kNN we already
  had** (the β→∞ limit), a finite value resonates.
- **`tests/test_resonance.py`** — 5 end-to-end tests.

### Measured (an honest, load-bearing finding — the capacity caveat made real)
Resonance is correct and generalizes kNN, but its big "free pattern completion" is
**bounded by our correlated fingerprints**, exactly as the report warned:
- β→∞, steps=1 → **exactly cosine-kNN** (40/40 agreement; the proven special case).
- steps=1, any β → identical top-1 to kNN (no harm, no gain).
- steps 2–3 at high β → small genuine gain on degraded cues (109/108 vs 107/120).
- **many steps at low β → COLLAPSE toward the centroid** (32/120 vs kNN 119/120).
- In a *separable* regime, settling completes a noisy cue 95–100% of the time; on raw
  correlated fingerprints it does not. → the completion win is **GATED on the same fix
  as composition** (random-projection to a higher-D near-orthogonal space).

### Defaults / posture
`recall_resonant` defaults to **steps=1** (safe: == kNN ranking). Low-β many-step
settling is documented as experimental in `resonance.py` (LIMITATION) until the capacity
experiment lands. Verified: `pytest` → **31 passed** (26 prior + 5 new).

---

## [0.4.0] — 2026-06-24 — Phase 2: the GDF phase complement (REPRESENT upgrade)

**Goal:** the cheapest representation win from `frequency_memory__UNIFIED.md` (P1) —
restore the temporal-ordering information that amplitude-only fingerprints discard.
Amplitude answers "how much each feature is changing"; it is BLIND to *when* in the
window the change happened (a window and its time-reverse share an identical amplitude
spectrum). The group-delay function (GDF, the phase derivative) restores that for ~free.
Implemented as a **selectable representation** (opt-in), tagged via `repr_id`, so the
default behaviour and existing archives are untouched until we choose to flip it.

### Added
- **`fingerprint.py` — `fingerprint_gdf()`** — amplitude blocks + an L2-normalized
  group-delay complement, using the product-spectrum form (`X=rFFT(x)`, `Y=rFFT(n·x)`,
  `GD=(Xr·Yr+Xi·Yi)/|X|²`) that avoids phase unwrapping (robust in noise). Amplitude
  blocks come first, so the leading half is byte-identical to `fingerprint()`. Dim doubles.
- **`sense.py`** — `reflex_impression_gdf` / `meaning_impression_gdf`; the
  `REFLEX_GDF_REPR` / `MEANING_GDF_REPR` tags; `impression_for(sense, representation)`
  (maps "raw"|"gdf" → faculty + repr_id) and `fingerprint_dim(feature_dim, freqs,
  representation)` so callers never hand-compute the fingerprint length.
- **`store.py`** — `TwofoldMemory(..., representation="raw"|"gdf")` picks the faculties,
  repr_ids, and (caller-sized) dims for both registers.
- **`tests/test_repr_gdf.py`** — 4 end-to-end tests.

### Verified
- The killer property, measured: amplitude `cos(window, time-reverse) = 1.000` (blind);
  GDF `cos = 0.21` (clearly distinguishes). dim 80→160, deterministic.
- `pytest vector_engram/tests/` → **26 passed** (22 prior + 4 new), <1 s.
- GDF `TwofoldMemory` recalls situation identity through noise end-to-end in both registers.

### Not yet (deliberate)
- `gdf` is **opt-in**; the default stays `raw` until we run the report's Experiment #1
  (recall@1 on a hard noisy/warped corpus) and decide the win justifies the doubled dim.
  Next representation tags reserved: `scatter.*`, `multiscale.*`.

---

## [0.3.0] — 2026-06-24 — Phase 1: the two senses (two-rate hybrid)

**Goal:** make ENGRAM remember each moment in two registers — a fast instinctive
**REFLEX** sense (raw fused sensation → fingerprint, on-robot) and a slower **MEANING**
sense (learned encoder embeddings → fingerprint, box). Decided after the frequency +
OSS reports: the reflex register keeps the Anki virtues (deterministic, training-free,
degrades gracefully); the meaning register is where recognition/identity become
meaningful (theta/gamma + chimera L1/L2 made concrete). Naming follows Anki's
creature-modelling style — faculties (`feel`, `recognize`), not data structures.

### Added
- **`sense.py`** — the two sensing faculties:
  - `Sense` enum (REFLEX / MEANING) — stamped on every trace so a recalled memory knows
    which sense formed it; the two senses are separate cosine spaces, never compared.
  - `EmbeddingFrame` / `MeaningState` — MEANING-sense analogues of
    `PerceptionFrame`/`PerceptionState` (a window of *recognised* embedding frames).
  - `reflex_impression()` / `meaning_impression()` — form a fingerprint from a moment;
    identical FFT math, different substrate (raw sensation vs embeddings).
  - `REFLEX_REPR` / `MEANING_REPR` representation-ids (the payload-version tag).
  - **Hooks (documented, not wired):** `MeaningEncoder` protocol = the seam where the
    real encoders (MobileCLIP / Depth Anything V2 / emotion2vec / TitaNet) attach; plus
    a note that the COMPOSE layer (HRR identity bundles) is **gated** on the VSA-capacity
    experiment and must not be built before it passes.
- **`store.py` — `TwofoldMemory`** — one creature, two registers (`.reflex`, `.meaning`);
  `feel()` / `recognize()` to lay down a trace, `recall_reflex()` / `recall_meaning()`
  to retrieve. Meaning register optional (`meaning_dim=None` → brainstem-only creature
  that still feels & recalls — graceful degradation). `SituationMemory` generalized to
  carry its `sense` + `repr_id` + `impression` fn (defaults = the original REFLEX path).
- **`synth.py`** — `make_meaning()` + `DE` (generated embedding corpus, real pipeline) to
  exercise the meaning path the way `make_situation()` exercises the reflex path.
- **`tests/test_two_rate.py`** — 6 end-to-end tests (meaning recall through noise, EGRV v2
  round-trip, two registers kept separate, reflex-only graceful degradation).

### Changed
- **EGRV format → v2.** Certificates now carry `sense` (uint8) + `repr_id` (string) — the
  **envelope/payload split**: the envelope (timestamps/labels/sense/…) is stable; the
  fingerprint payload may evolve, tagged by `repr_id`, without a format break. `decode()`
  is **backward-compatible** — legacy v1 certs read as REFLEX / "rfft.raw.v1". (Hand-rolled
  forward-compat; bridge until EGRV moves to FlatBuffers per the ENGRAM-rewrite report.)

### Verified
- `pytest vector_engram/tests/` → **22 passed** (16 prior regressions + 6 new), 3.3 s.
- Manual end-to-end: `TwofoldMemory.feel`/`recognize` write to the right register;
  `recall_*` returns the correct sense + repr_id; legacy v1 decode confirmed.

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
