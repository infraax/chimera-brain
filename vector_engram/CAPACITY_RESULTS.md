# Phase 4 — Capacity Experiment Results (THE gate)

*Run: `python -m vector_engram.capacity_experiment` · 2026-06-24 · vector_engram v0.6.0*

This is the experiment that decides whether **COMPOSE** (weaving many memory-impressions
into one labelled "identity shape" / the "self-frequency") is viable, given that ENGRAM
fingerprints are **correlated**, not random. It also informs the Phase-3 resonance
limitation. Reproduce any time with the command above.

---

## Part 1 — what the fingerprints actually look like

| representation | dim | full-norm | value range | within-situation cos | across-situation cos | **gap** |
|---|---|---|---|---|---|---|
| amplitude (`rfft.raw.v1`) | 230 | 1.414 (=√2) | `[0.000, +0.263]` (non-negative) | 0.964 | 0.686 | **+0.278** |
| amplitude+gdf (`rfft+gdf.v1`) | 460 | 2.000 | `[-0.888, +0.452]` (signed) | 0.603 | 0.384 | **+0.219** |

- **Amplitude fingerprints are all-positive** (they're spectral magnitudes), each frequency
  block L2-normalized to 1 → full-norm √2. They are **not sparse** (<1% near-zero).
- **They genuinely separate situations**: same-situation pairs cos≈0.96, different≈0.69 —
  a clear +0.28 gap. Retrieval works because of this gap.
- **GDF adds signed phase info** → lower absolute cosines and a slightly *smaller* general
  gap (+0.219). Its win is specifically **temporal order** (it tells time-reversed windows
  apart, which amplitude can't — Phase 2), not general separation. Use GDF for order, not
  for discriminability.

---

## Part 2 — bundling capacity (HRR bind → bundle → unbind → cleanup)

`capacity@0.9` = the largest bundle size k whose items are still recovered ≥90% of the
time (cleanup over the full item-memory, N=64). `corr` = mean |cosine| between items
(0 = ideal/random, higher = correlated = capacity-limiting).

| condition | corr (mean\|cos\|) | **capacity@0.9** | accuracy by k (k2…k48) |
|---|---|---|---|
| random @ D=230 | 0.052 | **16** | 1.00 1.00 0.98 0.93 0.62 0.42 |
| raw-amplitude @ 230 | 0.673 | **8** | 1.00 1.00 0.98 0.87 0.57 0.38 |
| gdf @ 460 | 0.374 | **8** | 1.00 0.95 0.97 0.85 0.69 0.55 |
| **projected raw @ 2048** | 0.679 | **32** | 1.00 1.00 1.00 1.00 0.96 0.87 |
| random @ 2048 | 0.018 | **48+** | 1.00 1.00 1.00 1.00 1.00 1.00 |

### What it means
1. **The correlation problem is real and quantified.** Raw fingerprints have mean |cos| =
   **0.673** (vs 0.052 for random). That correlation **halves capacity**: random@230 holds
   16, raw@230 holds only **8**. This is the Phase-3 limitation and the report's caveat,
   measured.
2. **Random projection to higher D is an effective fix — 8 → 32 (4×).** Projecting raw
   fingerprints to 2048-D recovers most of the capacity that dimension affords — even
   though projection does **not** decorrelate them (corr stays 0.679 ≈ raw 0.673, exactly
   as Johnson–Lindenstrauss predicts: cosines preserved). The gain comes from
   dimensionality + the fact that **binding with random roles already decorrelates the
   *bundle components*** (so item correlation matters less than feared); higher D simply
   gives the bundle more room. It doesn't reach the random@2048 ceiling (48+), so
   correlation still costs something — but 32 is plenty.
3. **GDF helps the tail, not the threshold.** gdf@460 matches raw's capacity@0.9 (8) but
   degrades more gracefully at large k (k32: 0.69 vs raw 0.57). Confirms GDF's value is
   order-sensitivity, with a mild capacity bonus from its lower correlation (0.374).

---

## GATE VERDICT: **PASS — proceed to COMPOSE on projected fingerprints**

- **Project impressions to ~2048-D (random Gaussian) before bind+bundle.** This lifts
  per-bundle capacity from an unusable **8** to a comfortable **32**.
- **Leaf-bundle size ≤ ~24** (a safety margin under the measured 32 @ ≥90%); use a
  **hierarchy** (leaf bundles → mid → top "self") to hold more than one leaf's worth, as
  the report prescribes.
- **Cleanup memory is mandatory** (snap noisy unbinds to clean items) — already implemented
  (`vsa.cleanup`).
- This also indicates the path to better **resonant completion** (Phase 3): operate in the
  projected higher-D space, not on raw correlated fingerprints.

**Decision:** COMPOSE is unblocked. Build it (`compose.py`) with: random projection →
per-label role-keys → bind → bundle (≤24/leaf) → hierarchy → cleanup. The "self-frequency"
is buildable.
