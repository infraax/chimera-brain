# MUSIC & FREQUENCY CONCEPTS FOR ENGRAM
## Design vision: memory-as-frequency, music-aligned format, and personality as a composed identity shape
## Created: 2026-06-24 · Dexter × Claude Opus 4.8 · evidence in research/ENGRAM_FREQUENCY_RESEARCH.md

This captures the brainstorm so it isn't lost, and turns it into concrete, buildable architecture.
It is the "why/what"; the literature + repos + experiments are in `research/ENGRAM_FREQUENCY_RESEARCH.md`.

---

## 1. The reframe: memory as **frequency**, not "sound"
Sound is just one signal that lives in the frequency domain. The substrate of this mind is the **frequency
domain itself** — and audio engineering is the most mature human toolkit for working in it. The operations we
want — *compose, compare, superpose, resonate, forget* — all have natural, rigorous forms there.

## 2. Dexter's three ideas, formalized

### Idea 1 — Music-theory-aligned data format ("fixed notes + a grammar of timing")
A fixed alphabet of primitives never changes (the 12 notes / a scale); infinite unique songs come from
**timing, repetition, rests, dynamics, and added layers**. Applied to ENGRAM:
- **Notes = a fixed, frozen perceptual codebook** (VQ / dictionary learned once, then frozen → stays
  deterministic). Each fused-sensor frame → nearest codeword.
- **Grammar = temporal structure encoded *separately* from content**: onsets, inter-onset intervals,
  **repetition** (self-similarity matrix), and **rests** (low-energy frames). Today's f0/f1 conflate
  "what" with "how it changes"; we split them, like a musical score vs. its timbre.
- **Added layers = extra modalities / harmonics** that enrich without changing the alphabet.
- **Bars = multi-scale time windows (4/8/16/32)** captured at once (wavelets / scattering), so two memories
  built from the same notes stay distinct via their *rhythm and structure*.

### Idea 2 — Personality as a composed **identity shape under a label** (the keystone)
Vector's "who am I" is **not a text prompt** — it's one big shape composed from every fingerprint tagged
`self`/`me`/`I`, recomputed as experience accumulates. Generalize to any identifier: `environment`, a person,
a place, a concept. Querying a label **grabs all its fingerprints and composes them into one queryable
vector**.
- Rigorous machinery: **Vector Symbolic Architectures / Holographic Reduced Representations** —
  **bundle** (add) to superpose, **bind** (circular convolution = multiply in the Fourier domain) to attach
  roles (`PERSON ⊛ alice`), **namespaces** via fixed role-keys, **cleanup / resonator networks** to pull
  items/motifs back out.
- Capacity is finite, so compose **hierarchically (the "bars")**: notes → motifs → themes → song → self.
  Each layer cached and updated incrementally (the Anki way: bounded, hierarchical, legible).

### Idea 3 — "System prompt = a living self-frequency"
The brain (L3) conditions on the composed `self` shape and on the situations most **resonant** with it —
a self that *integrates experience* instead of a frozen `.txt`. Retrieval itself becomes **resonance**:
Modern Hopfield networks (= attention) generalize our cosine-kNN, with a tunable "sharpness" and multi-step
**pattern completion** from partial cues. "The brain rings; the resonant memories light up" — literally.

## 3. The convergent architecture (all four research pillars → one design)
```
REPRESENT : fixed VQ codebook ("notes") + content/rhythm split ("grammar") +
            multi-scale scattering/wavelets ("bars") + constant-Q/chroma (scale-invariance) + phase-as-index
COMPOSE   : VSA/HRR bind+bundle under LABELS, hierarchically (notes→motifs→self) = identity shapes
RETRIEVE  : Modern Hopfield = attention = generalized cosine-kNN ("resonance", β knob, pattern completion);
            resonator nets decompose motifs
GROUND    : phase-as-index + retrieval-by-resonance are real neuroscience; reservoir computing = the
            "constantly vibrating shape"
```
Validation worth savoring: our **current cosine-kNN is already the β→∞ special case** of resonance retrieval,
and HRR binding is **already in the Fourier domain** — so Dexter's instincts map onto existing, open-source,
permissively-licensed math (`torchhd` MIT, `hopfield-layers` BSD, `kymatio` BSD).

## 4. Honest boundaries (so the real work isn't discredited)
- ✅ Build on: scattering/wavelets, frozen VQ dictionary, constant-Q/chroma, VSA/HRR + namespaces + resonator
  nets, Modern Hopfield retrieval, reservoir computing, phase-as-index, theta-gamma ordering, associative memory.
- ⚠ Inspiration only: binding-by-synchrony (real but contested).
- ❌ Drop: "Schumann resonance tunes the brain", "cellular/DNA healing frequencies", "personality = one
  standing waveform at frequency X". Defensible version: *personality = a point/trajectory in a
  high-dimensional dynamical state, composed by frequency-domain binding, retrieved by resonance.*

## 5. What this changes in `vector_engram` (incremental, testable)
1. Add **labels** to certs + `compose_identity(label)` (VSA bundle, hierarchical) → the identity-shape layer.
2. Swap/augment the fingerprint: **multi-scale (scattering/DWT)** + optional **phase** + **constant-Q** + a
   frozen **codebook** path — behind the existing `StateVector`/`fingerprint` seam, A/B'd against f0/f1.
3. Add a **Modern-Hopfield retrieval head** (β-tunable, iterated) over the existing store; keep cosine-kNN as
   the β→∞ default and ground truth.
4. Keep everything deterministic, bounded, ARM-feasible, and license-clean (see research doc §7).

## 6. Prioritized next experiments (detail in research doc §6)
1. **Representation on a hard near-duplicate corpus**: f0/f1 vs +phase vs scattering/DWT vs chroma. *Does a better representation even help where today's breaks?*
2. **VSA capacity on REAL fingerprints**: the load-bearing test before adopting identity-shapes.
3. **Retrieval by resonance**: Modern-Hopfield vs cosine-kNN on corrupted cues (pattern completion).
4. Identity vector + namespaces → 5. codebook "notes" → 6. resonator decomposition.

> Status: research complete and committed. Next action = run experiment #1 and/or #2 in the testbed
> (and/or prototype `compose_identity(label)`), then let evidence rank the ideas before we refactor ENGRAM.
