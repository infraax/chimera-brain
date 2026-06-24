# ENGRAM — Frequency, Music & Memory: Research Map
### Literature + Repositories to Evolve ENGRAM Toward a Music-Theory-Aligned, Composable, Resonance-Retrieved System
*Created: 2026-06-24 · Companion to `MUSIC_AND_FREQUENCY_CONCEPTS.md`, `ENGRAM_FOR_VECTOR.md`*

***

## Current State Baseline

ENGRAM today (`vector_engram/fingerprint.py`) computes `|rFFT|` of a `[T, D]` window — amplitude at frequencies {0, 1}, each block L2-normalized, concatenated to `[D·2]`, with cosine retrieval via hnswlib. The system is deterministic, training-free, **amplitude-only** (phase is discarded), and operates at a **single time-scale**. This is an important architectural fact: all four upgrade pillars build *on top of* — not against — this foundation. As established in [^1], cosine-kNN is a provably special (β → ∞) case of Modern Hopfield retrieval, meaning the current implementation is already a limiting case of a broader resonance framework.

***

## 0. The Convergent Insight: Four Pillars, One Architecture

The design intuitions motivating ENGRAM ("memory as frequency," "f0/f1 as notes composed into a symphony," "personality = one big shape from a labeled collection," "a constantly vibrating brain") map directly onto four mature research lineages that compose into a single coherent upgrade:

```
REPRESENT  →  Multi-scale, deformation-stable spectral features over a FIXED codebook
              (scattering/wavelets = "bars 4/8/16/32" · VQ dictionary = "the notes" · keep phase as index)

COMPOSE    →  VSA/HRR: bind (circular convolution = Fourier-domain multiply) + bundle under LABELS,
              hierarchically (notes → motifs → themes → self) = identity shape / system-prompt-as-frequency

RETRIEVE   →  Modern Hopfield = attention = strict generalization of cosine-kNN
              (tunable sharpness β, multi-step pattern completion); resonator nets decompose motifs

GROUND     →  Real neuroscience (theta-gamma ordering, associative memory) supports phase-as-index
              + resonance retrieval; Schumann/"healing-frequency" mysticism dropped entirely
```

The most striking validation: **"memory as frequency" + "compose into one personality shape" + "retrieve by resonance"** = HRR (frequency-domain binding) + Modern Hopfield (resonance retrieval) — both are real, both are open-source (MIT/BSD), and the current cosine-kNN is already a special case of the retrieval half.[^1][^2]

***

## 1. Pillar A — Representation: Music-Aligned, Multi-Scale, Robust Fingerprints

### 1.1 Foundational Papers

| Work | Year | Why It Matters | Link / Status |
|---|---|---|---|
| Wang, "An Industrial-Strength Audio Search Algorithm" (Shazam) | 2003 | Constellation of spectral peaks → `(f1, f2, Δt)` landmark hashes; noise- and codec-robust, scales to millions | https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf |
| Mallat, "A Theory for Multiresolution Signal Decomposition" | 1989 | Foundational wavelet MRA — long windows for low freq ("this hour"), short for high ("this instant") = the literal 4/8/16/32 "bars" | IEEE Xplore 10.1109/34.192463 |
| Bruna & Mallat, "Invariant Scattering Convolution Networks" | 2013 | Translation-invariant, **deformation-stable**, training-free representation (a CNN with fixed wavelet filters)[^3][^4] | https://arxiv.org/abs/1203.1513 |
| Andén & Mallat, "Deep Scattering Spectrum" | 2014 | 1D/audio scattering; recovers modulation info MFCC discards; **best theoretical match for a robust fingerprint**[^5][^6] | https://arxiv.org/abs/1304.6763 |
| Brown, "Calculation of a constant-Q spectral transform" | 1991 | Log-frequency bins (Q = f/Δf) → musical/octave structure; scaling becomes a shift (invariance) | JASA 89(1) |
| van den Oord et al., "VQ-VAE / Neural Discrete Representation Learning" | 2017 | Learns a discrete **codebook** = "the fixed notes"[^7][^8] | https://arxiv.org/abs/1711.00937 |
| Zeghidour et al., "SoundStream" / Défossez, "EnCodec" / Kumar, "DAC" | 2021–23 | **Residual VQ** = coarse→fine code stacks; EnCodec is a state-of-the-art neural audio codec developed by Meta AI[^9][^10] | EnCodec: https://github.com/facebookresearch/encodec · DAC: https://github.com/descriptinc/descript-audio-codec |
| Olshausen & Field, "Sparse coding of natural signals" | 1996 | Origin of dictionary learning; atoms emerge as Gabor primitives | — |
| Aharon, Elad & Bruckstein, "K-SVD" | 2006 | Overcomplete dictionary learning (see scikit-learn `MiniBatchDictionaryLearning`) | — |

The Deep Scattering Spectrum (Andén & Mallat 2014) extends MFCC representations by computing modulation spectra, defining a locally translation-invariant representation stable to time-warping deformations. This is the recommended single upgrade for `fingerprint.py` — `Scattering1D` (J≈5, Q≈1) from kymatio gives 0th-order ≈ "this hour," 1st-order ≈ envelope, 2nd-order ≈ modulation, all shift-invariant and warp-stable.[^11][^12][^5][^13]

### 1.2 Repositories (License-Checked)

| Repo | License | Lang | Purpose |
|---|---|---|---|
| **librosa** | ISC | Py | STFT / CQT / chroma / tonnetz / beat — easiest testbed reference · https://github.com/librosa/librosa |
| **kymatio** | BSD-3 | Py | Wavelet scattering (1D/2D), numpy frontend[^11][^12] · https://github.com/kymatio/kymatio |
| **PyWavelets (`pywt`)** | MIT | C/Py | DWT / CWT / wavelet packets · https://github.com/PyWavelets/pywt |
| **ssqueezepy** | MIT | Py | Fast CWT + synchrosqueezing · https://github.com/OverLordGoldDragon/ssqueezepy |
| **scikit-learn dict-learning** | BSD-3 | Py | `MiniBatchDictionaryLearning`, `SparseCoder` (the "notes") |
| **audfprint** | MIT | Py | Reference Shazam landmark-hashing impl[^14] · https://github.com/dpwe/audfprint |
| **Dejavu** | MIT | Py | Audio fingerprinting and recognition · https://github.com/worldveil/dejavu |
| **EnCodec** | MIT | Py | Production residual-VQ neural audio codec[^10] · https://github.com/facebookresearch/encodec |
| **DAC (Descript Audio Codec)** | MIT | Py | Residual VQ audio tokenizer[^15] · https://github.com/descriptinc/descript-audio-codec |
| ⚠ Essentia, Panako | **AGPL-3.0** | C++/Java | Rich MIR — **avoid** for permissive/closed builds |
| ⚠ aubio | **GPL-3** | C/Py | Flagged; prefer permissive equivalents |
| ⚠ Chromaprint (via FFmpeg) | **LGPL** | — | Flagged; prefer permissive equivalents |
| ⚠ SPAMS | **GPL-3** | C++/Py | Flagged; prefer scikit-learn dict-learning |

### 1.3 Mapping to ENGRAM

1. **Notes (fixed codebook):** Fit a small VQ/dictionary **once, offline, then freeze** over fused frames — each frame becomes the nearest codeword. This provides a stable primitive alphabet that remains deterministic at inference. Residual VQ (EnCodec/DAC style) keeps the coarse→fine spirit already implicit in ENGRAM's multi-block concat.[^9][^10]

2. **Grammar (content vs timing split):** Today f0/f1 conflate "what" and "how it changes." Split into a **content track** (token sequence) + a **rhythm/structure track** (onsets, inter-onset intervals, rests = low-energy frames, repetition via self-similarity matrix). This is the score-vs-timbre split = "same notes, different song."

3. **Multi-scale "bars":** Replace single-window 2-bin FFT with a **dyadic stack (4/8/16/32)** via DWT energy-per-level, or — recommended — **`Scattering1D`** (J≈5, Q≈1)[^11]: 0th order = "this hour", 1st ≈ envelope, 2nd = modulation; shift-invariant + warp-stable (fixes `|FFT|` jitter fragility).

4. **Constant-Q / chroma:** Log-frequency binding means multiplicative magnitude scaling becomes a translation (robustness); chroma (octave-fold) gives maximum invariance at minimum dimensions.[^5][^16]

5. **Keep phase as an index** (currently discarded) — see §3 and §4 for the neuroscience grounding.

***

## 2. Pillar B — Composition: Identity Shapes Under Labels (VSA / HRR / HDC)

**This is the rigorous home of "the system prompt is a composed ENGRAM shape under a label."**

### 2.1 Foundational Papers

| Work | Year | Why It Matters | Link |
|---|---|---|---|
| Smolensky, "Tensor Product Variable Binding" | 1990 | Origin of distributed binding (dim grows → motivates "reduced" forms) | — |
| **Plate, "Holographic Reduced Representations"** | 1991/95 | **Canonical:** bind = circular convolution (= multiply FFTs), bundle = add, unbind = correlation, + cleanup memory[^17][^18] | https://redwood.berkeley.edu/wp-content/uploads/2020/08/Plate-HRR-IEEE-TransNN.pdf |
| Kanerva, "Hyperdimensional Computing: An Introduction" | 2009 | Accessible whole-field tutorial; also originator of Sparse Distributed Memory (1988) | https://link.springer.com/article/10.1007/s12559-009-9009-8 |
| Gayler, "VSA answer Jackendoff's challenges" | 2003 | Coined "VSA"; defines bind / bundle / permute requirements | https://arxiv.org/abs/cs/0412059 |
| Eliasmith, *How to Build a Brain* (SPA / Spaun) | 2013 | Semantic pointers = compressed HRR vectors in spiking neurons | — |
| **Frady, Kent, Olshausen & Sommer, "Resonator Networks 1 & 2"** | 2020 | **Factor a bound product back into its parts** (decompose person⊗place⊗feeling)[^19][^20] | https://arxiv.org/abs/2007.03748 |
| Kleyko et al., "Survey on HDC/VSA, Parts I & II" | 2022 | Best entry point; compares HRR/FHRR/MAP/BSC[^21][^22] | arXiv:2111.06077 · arXiv:2112.15424 |
| "Capacity Analysis of VSA" | 2023 | How many vectors can be bundled vs dim D[^23][^24] | arXiv:2301.10352 ✅ (confirmed accessible) |
| "Linearithmic Clean-up… Kronecker Rotation Products" | 2025 | O(N log N) cleanup for large namespaces[^25] | https://arxiv.org/abs/2506.15793 |

HRRs use circular convolution to encode associations and circular correlation to decode — and unlike aperiodic convolution, circular convolution produces a vector of the same dimensionality as the item vectors, allowing arbitrarily complex hierarchical associations without dimension explosion. Crucially, the convolution can be computed in O(n log n) via FFT — and the 2025 Kronecker rotation paper extends this to O(N log N) cleanup over large namespaces, directly relevant to ENGRAM's scale requirements.[^26][^17][^25]

### 2.2 Repositories

| Repo | License | Purpose |
|---|---|---|
| **torchhd** | MIT | Most complete VSA: HRR/FHRR/MAP/BSC, bundle/permute/cleanup, resonator examples — **best fit** (FHRR maps onto Fourier fingerprints)[^27][^28] · https://github.com/hyperdimensional-computing/torchhd |
| **hdlib** | MIT | Pure-numpy VSA primitives — **most edge/ARM-friendly**, provides `bind`, `bundle`, `permute`[^29][^30][^31] · https://github.com/cumbof/hdlib |
| **nengo-spa (+nengo)** | MIT* (verify in-repo) | SPA / spiking-plausible; heavier · https://github.com/nengo/nengo-spa |

The `torchhd` library runs HD/VSA experiments up to 100× faster than baseline implementations and supports FHRR (Fourier Holographic Reduced Representations), which maps directly onto ENGRAM's Fourier fingerprints. For edge deployment, `hdlib` (MIT) provides pure-numpy `bind`, `bundle`, `permute` with cosine/hamming/euclidean search, available via `pip install hdlib`.[^27][^29][^30]

### 2.3 Mapping to ENGRAM (The Identity-Shape Architecture)

- **Labels/namespaces:** Give each cert a label set (`self`, `environment`, person, place…). Per label, assign a fixed random **role-key** `K_label`.
- **Identity vector:** `IDENTITY_self = Σᵢ (K_self ⊛ fp_i)` (⊛ = circular convolution), normalized → one fixed-width "self" shape. Membership: `cos(K_self ⊛ q, IDENTITY_self)`. This **is** the "system prompt as a living self-frequency."
- **Motifs:** `motif = (PERSON ⊛ alice) + (PLACE ⊛ kitchen) + (FEELING ⊛ calm)`; query by unbind + cleanup; **resonator network** when factors are unknown.[^19][^20]
- **Hierarchy for capacity ("the bars"):** Leaf bundles of ≤k memories → mid-level (bound with sub-keys) → top "self." hnswlib stays the per-leaf exact store + **cleanup memory**; VSA vectors are the routing/summary layer. *They compose, not compete.*

> ⚠ **Load-bearing caveat:** ENGRAM fingerprints are **L2-normalized amplitude spectra, not random vectors** — VSA capacity theory assumes near-orthogonal random vectors. Correlated fingerprints → lower capacity and more crosstalk. **Must quantify (Experiment B1, §6)** before committing. May need random role-keys + projection of fingerprints into a higher-D near-random space.[^23]

***

## 3. Pillar C — Retrieval by Resonance (Modern Hopfield = Attention)

### 3.1 Foundational Papers

| Work | Year | Why It Matters | Link |
|---|---|---|---|
| Hopfield, "Neural networks and physical systems…" | 1982 | Energy-descent content-addressable memory ("retrieval by resonance"); capacity ~0.14·N | https://www.pnas.org/doi/10.1073/pnas.79.8.2554 |
| **Ramsauer et al., "Hopfield Networks is All You Need"** | 2020 | Modern continuous Hopfield: **exponential capacity** \(N = 2^{d/2}\), 1-step retrieval, = transformer attention[^32][^2] | https://arxiv.org/abs/2008.02217 |
| **Millidge et al., "Universal Hopfield Networks"** | 2022 | Hopfield, SDM, **cosine-kNN, attention all = `separation(similarity(q,K))·V`** — ENGRAM's cosine-kNN is the β→∞ special case[^1][^33] | https://arxiv.org/abs/2202.04557 |
| Kanerva, *Sparse Distributed Memory* | 1988 | Distributed content-addressable memory (SDM) | — |
| Continuous-time Modern Hopfield (2025) | 2025 | Compresses discrete Hopfield memories into continuous-time representations; competitive performance with smaller memory[^34] | arXiv:2502.10122 |

The key insight from Ramsauer et al. is that setting the scaling parameter β = 1/√D recovers the single-head attention mechanism in transformers, with identical projection layers. This creates a direct bridge: ENGRAM's cosine-kNN is a degenerate (β→∞, one-winner-takes-all) Hopfield retrieval. Lowering β continuously transitions from sharp 1-NN behavior to smooth "memory blending" (resonance across multiple stored patterns).[^34][^32][^1]

### 3.2 Repositories

| Repo | License | Purpose |
|---|---|---|
| **`ml-jku/hopfield-layers`** | BSD-2[^35] | PyTorch Hopfield layer; plug-in retrieval upgrade · https://github.com/ml-jku/hopfield-layers |
| **`torchhd`** (resonator component) | MIT | Resonator networks for factorization decomposition[^27] |

### 3.3 Mapping to ENGRAM

Don't replace the store — **swap the separation function.** Current: cosine-kNN = top-k argmax of `cos(q, kᵢ)`. Upgraded: `softmax(β · qKᵀ) · V`. The gains:[^32][^2]

- A **tunable "sharpness of resonance" knob** (β)
- **Multi-step relaxation** = true pattern completion from partial/noisy cues (one-shot kNN cannot do this)[^34]
- **Resonator iteration** adds retrieval + decomposition (recover person/place/feeling from a bound motif)[^20][^19]
- Zero new storage overhead — the same hnswlib index feeds the Hopfield update rule

***

## 4. Pillar D — Biological Grounding (Honest Assessment)

| Work | Year | Status | Link |
|---|---|---|---|
| Lisman & Jensen, "The Theta-Gamma Neural Code" | 2013 | ✅ **Supported** — items ordered by gamma-cycles-within-theta; ~7 gamma slots per theta = ~7 WM items; phase = serial position[^36][^37] | https://pubmed.ncbi.nlm.nih.gov/23522038/ |
| O'Keefe & Recce, theta phase precession | 1993 | ✅ **Supported** — phase carries information that rate codes don't; place cells fire at progressively earlier phases within theta[^36] | https://onlinelibrary.wiley.com/doi/10.1002/hipo.450030307 |
| Lega 2016 / Daume 2024, human theta-gamma PAC & memory | 2016/24 | ✅ **Supported** (human intracranial, including causal tACS) | https://pmc.ncbi.nlm.nih.gov/articles/PMC4677977/ |
| Theta-gamma coupling & sequential episodic memory | 2024 | ✅ **Supported** — gamma oscillations nested in theta are assumed to play a key role in sequential episodic memory[^38] | Frontiers Neural Circuits 2024 |
| von der Malsburg (1981); Singer 1999 — binding-by-synchrony | — | ⚠ **Real but contested** (rebuttal: Shadlen & Movshon 1999) — use as *inspiration*, not fact | — |
| Jaeger ESN 2001 / Maass LSM 2002 — reservoir computing | — | ✅ **Supported & buildable** — memory as an evolving dynamical state ("constantly vibrating shape")[^39][^40] | https://github.com/reservoirpy/reservoirpy |
| "Artificial Kuramoto Oscillatory Neurons" | 2025 | ✅ **Novel and buildable** — binding-by-synchrony revived in differentiable nets; outperforms real-valued counterparts in multi-object tasks[^41] | arXiv:2502.21077 |
| Hopfield-Kuramoto associative memory model | 2025 | ✅ **Novel** — oscillatory neurons implement low-rank correction to Hopfield weight matrix; equivalent to a form of Hebbian learning or LoRA[^42] | arXiv:2505.03648 |

The theta-gamma framework is directly actionable: gamma cycles within theta order ~7 items in working memory, theta power increases with WM load, and maximum gamma power for distinct memory items occurs at different theta phases. This is the biological substrate for **phase-as-index**: phase doesn't store content, but it orders retrieval. The key design implication is to treat phase not as a storage medium but as a **soft serial index** over an associative store.[^36][^43]

### 4.1 Repository: ReservoirPy

`reservoirpy` (MIT) implements Echo State Networks and Next-Generation Reservoir Computing. Memory as an evolving dynamical state ("constantly vibrating brain") is precisely what reservoir computing provides — a high-dimensional, non-linear, recurrent readout of temporal context. Compatible with numpy/hnswlib testbed, low overhead.[^39][^40]

***

## 5. Buildable vs. Fringe (Enforced Classification)

### ✅ Build On
- Wavelet scattering / kymatio (`Scattering1D`) — deformation-stable, training-free[^11][^5]
- Fixed VQ dictionary (scikit-learn `MiniBatchDictionaryLearning`, or RVQ via EnCodec/DAC)[^7][^9]
- Constant-Q / chroma — musical invariance[^16][^5]
- VSA/HRR composition + namespaces + resonator nets (torchhd/hdlib)[^30][^27]
- Modern Hopfield = attention retrieval (ml-jku/hopfield-layers)[^35][^2]
- Reservoir computing (reservoirpy)[^39]
- Phase-as-index (not phase-as-storage carrier)[^37][^36]
- Theta-gamma temporal ordering[^43][^38][^36]
- Artificial Kuramoto neurons for binding (2025)[^41][^42]

### ⚠ Inspiration Only (Cite Both Sides)
- Binding-by-synchrony (Singer 1999 / von der Malsburg) — real phenomenon, actively contested in cortex; use as architecture motivation, not empirical fact

### ❌ Drop Entirely
These claims will discredit the real work and have no engineering traction:
- "Schumann resonance (7.83 Hz) tunes the brain" — 7.83 Hz ≈ alpha is coincidence; no evidence of entrainment from Earth's electromagnetic resonance
- "Cellular/DNA healing frequencies" (528 Hz, 432 Hz etc.) — no peer-reviewed mechanism
- "A personality is a single standing waveform at frequency X" — the defensible version: *a personality is a point/trajectory in a high-dimensional dynamical state, composed by frequency-domain binding (HRR) and retrieved by resonance (Hopfield).*

***

## 6. Unified Experiment Plan (All Runnable in numpy/hnswlib Testbed)

Ranked by leverage; each experiment is ~100 lines and answers a concrete architecture decision.

### Experiment 1 — Robust Representation (Headline)
**Hypothesis:** Scattering and multi-scale features keep near-duplicates close where f0+f1 breaks.

Build a **hard near-duplicate corpus** (time-shift, mild time-warp 0.9–1.1×, noise) and compare fingerprints on recall@1/AUC:

| Fingerprint | Tool |
|---|---|
| `f0 + f1` (current baseline) | fingerprint.py |
| `+ phase` | np.angle(rFFT) |
| `+ more harmonics (f0..f7)` | fingerprint.py extended |
| `DWT energy-per-level (4/8/16/32)` | pywt[^11] |
| **`Scattering1D` (J=5, Q=1)** | kymatio[^11][^12] |
| `log-freq / chroma` | librosa[^5] |

**Decision gate:** does any fingerprint substantially improve recall@1 over baseline on noisy/shifted inputs? If yes, it justifies replacing the FFT core.

### Experiment 2 — VSA Capacity with Real Fingerprints (Load-Bearing)
**Hypothesis:** ENGRAM fingerprints are too correlated for full VSA capacity. Random role-keys + projection restore it.

Plot bundling-capacity curve (accuracy vs #items bundled, vs dim D) on:
1. Random vectors (VSA theory baseline)
2. Actual ENGRAM fingerprints (amplitude spectra)
3. ENGRAM fingerprints projected to higher-D with random Gaussian matrix

Use `torchhd` FHRR bundling + cosine cleanup. **This sets leaf-bundle size `k` and determines whether random role-keys are required.**[^44][^27]

### Experiment 3 — Identity Vector + Namespaces
**Goal:** Validate "system-prompt-as-shape."

Build `IDENTITY_self` and `IDENTITY_other` via HRR bundling. Compute ROC for "is query q a self-memory?" Confirm namespaces don't leak (cosine similarity between different role-key branches should be ≤ noise floor). Requires Experiment 2 to set k first.

### Experiment 4 — Retrieval by Resonance
**Hypothesis:** Modern Hopfield matches kNN on clean queries and beats it on partial/noisy cues.

Implement `softmax(β · XᵀX_q) · X` (1-step + iterated):[^2][^32]
- Compare vs cosine-kNN at varying noise levels (0%, 10%, 30%, 50% Gaussian)
- Sweep β ∈ {0.1, 0.5, 1, 2, ∞}
- Use `ml-jku/hopfield-layers` for β sweeps[^35]

**Cheap win:** if 1-step Hopfield at finite β outperforms kNN on corrupted cues, this is a **free upgrade** to the retrieval layer with no storage cost change.

### Experiment 5 — Codebook "Notes"
**Goal:** Validate the frozen VQ/dictionary as a stable atom alphabet.

Freeze a VQ/dictionary (scikit-learn `MiniBatchDictionaryLearning` or EnCodec RVQ); encode windows as sparse codes. Measure:
- Retrieval accuracy under perturbation vs raw amplitude fingerprint
- **Atom-firing stability** (does the same codeword fire consistently?)
- Bytes/frame and latency on ARM-like budget

### Experiment 6 — Resonator Decomposition (Optional)
**Goal:** Recover person/place/feeling from a bound motif `(PERSON ⊛ alice) + (PLACE ⊛ kitchen)` without knowing the keys.

Use resonator network iteration from `torchhd`. Decide if resonator nets are needed in ENGRAM vs simpler known-key unbind. Low priority until experiments 1–4 are complete.[^45][^27]

### Recommended Execution Order
```
#1 (Better representation on hard cases?)
  → #2 (Is VSA viable with real vectors?)
    → #4 (Is resonance retrieval a free win over kNN?)
      → #3 (Identity vector + namespace validation)
        → #5 (Codebook notes feasibility)
          → #6 (Resonator decomposition, if needed)
```

***

## 7. Top Repositories to Pull (License-Clean)

| Repo | License | Primary Use |
|---|---|---|
| `torchhd` | MIT | VSA/FHRR/resonator — best fit for Pillar B[^27][^28] |
| `hdlib` | MIT | Edge VSA, pure numpy[^30][^31] |
| `kymatio` | BSD-3 | Scattering transforms — Pillar A headline upgrade[^11][^12] |
| `pywt` | MIT | DWT/CWT/wavelet packets — Pillar A baseline multi-scale |
| `ml-jku/hopfield-layers` | BSD-2 | Resonance retrieval layer — Pillar C[^35][^46] |
| `reservoirpy` | MIT | Reservoir computing / dynamical memory state[^39][^40] |
| `librosa` | ISC | Reference: STFT/CQT/chroma/tonnetz/beat |
| `audfprint` | MIT | Reference: Shazam landmark hashing[^14] |
| `dejavu` | MIT | Reference: audio fingerprinting |
| `scikit-learn` | BSD-3 | Dict-learning / sparse coding (`MiniBatchDictionaryLearning`) |
| `EnCodec` | MIT | Residual VQ audio tokenizer[^10] |
| `DAC` | MIT | Residual VQ audio tokenizer (alternative)[^15] |

**Avoid:** Essentia/Panako (AGPL-3.0), aubio (GPL-3), SPAMS (GPL-3), Chromaprint-with-FFmpeg (LGPL).

***

## 8. Verification Flags

The following items were unverified or had access issues during research compilation. Verify before formal citation:

| Item | Flag | Action |
|---|---|---|
| arXiv:2301.10352 ("Capacity Analysis of VSA") | ✅ Confirmed accessible[^23][^24] | Cite freely |
| arXiv:2506.15793 (Kronecker linearithmic cleanup) | ✅ Confirmed accessible[^25] | Cite freely |
| arXiv:2502.21077 (Kuramoto oscillatory neurons) | ✅ Confirmed accessible[^41] | Cite freely |
| EnCodec arXiv:2210.13438 | ✅ Confirmed (Meta AI, MIT license)[^9][^10] | Cite freely |
| DAC arXiv:2306.06546 | ✅ Confirmed (Descript, MIT license)[^15] | Cite freely |
| nengo-spa license | ⚠ Listed as MIT\* | **Verify in-repo LICENSE file before use** |
| Kanerva SDM repository | ⚠ No canonical open-source repo | Use torchhd SDM implementation instead |
| Bruna & Mallat arXiv:1203.1513 | ✅ Confirmed accessible[^3][^4] | Cite freely |

***

## 9. Architecture Summary: ENGRAM v2 Blueprint

Combining all four pillars, the upgraded architecture decomposes as follows:

```
INPUT WINDOW [T, D]
       │
       ▼
[REPRESENT]  Scattering1D (kymatio, J=5, Q=1)
             or DWT energy-per-level (pywt)
             → multi-scale feature vector [scales × D]
             → quantized to frozen codebook (scikit-learn / RVQ)
             → content track + rhythm/structure track (separated)
             → phase retained as soft index (not discarded)
       │
       ▼
[COMPOSE]    VSA binding (torchhd FHRR / hdlib)
             per-label role-key K_label
             IDENTITY_label = Σᵢ (K_label ⊛ fp_i)  [normalized]
             motif = Σ_roles (K_role ⊛ value_role)
             hierarchy: leaf bundles (≤k) → mid → top "self"
       │
       ▼
[RETRIEVE]   hnswlib (per-leaf exact store) + cleanup memory
             Modern Hopfield read: softmax(β · XᵀX_q) · X
             tunable β: low → resonance blend, high → kNN (current)
             multi-step iteration → pattern completion from partial cues
             resonator nets → decompose motif into roles (optional)
       │
       ▼
[GROUND]     phase-as-index: soft serial ordering (θ-γ inspired)
             reservoir state (reservoirpy): persistent vibrating context
             namespace ROC: confirm self vs other don't leak
```

This architecture is fully composable with the current hnswlib+numpy testbed. The four pillars share no hard dependencies on each other — each experiment in §6 is independently runnable and independently informative.

---

## References

1. [Universal Hopfield Networks: A General Framework for Single-Shot ...](https://proceedings.mlr.press/v162/millidge22a.html) - A large number of neural network models of associative memory have been proposed in the literature. ...

2. [[2008.02217] Hopfield Networks is All You Need - arXiv](https://arxiv.org/abs/2008.02217) - We introduce a modern Hopfield network with continuous states and a corresponding update rule. The n...

3. [Invariant Scattering Convolution Networks](https://arxiv.org/pdf/1203.1513.pdf)

4. [Invariant Scattering Convolution Networks : Joan Bruna : Free Download, Borrow, and Streaming : Internet Archive](https://archive.org/details/arxiv-1203.1513) - A wavelet scattering network computes a translation invariant image representation, which is stable ...

5. [[PDF] Deep Scattering Spectrum | Semantic Scholar](https://www.semanticscholar.org/paper/Deep-Scattering-Spectrum-And%C3%A9n-Mallat/209826c2ce8352390ccd9f19864186a60739f3f3) - Deep Scattering Spectrum · J. Andén, S. Mallat · Published in IEEE Transactions on Signal… 24 April ...

6. [[1304.6763] Deep Scattering Spectrum - arXiv](https://arxiv.org/abs/1304.6763) - Abstract: A scattering transform defines a locally translation invariant representation which is sta...

7. [Neural Discrete Representation Learning - NIPS](https://papers.nips.cc/paper/7210-neural-discrete-representation-learning) - Neural Discrete Representation Learning. Aaron van den Oord, Oriol Vinyals, koray kavukcuoglu. Advan...

8. [[1711.00937] Neural Discrete Representation Learning - arXiv](https://arxiv.org/abs/1711.00937) - In this paper, we propose a simple yet powerful generative model that learns such discrete represent...

9. [EnCodec - Wikipedia](https://en.wikipedia.org/wiki/EnCodec)

10. [EnCodec: High Fidelity Neural Audio Compression - GitHub](https://github.com/facebookresearch/encodec) - State-of-the-art deep learning based audio codec supporting both mono 24 kHz audio and stereo 48 kHz...

11. [Kymatio: Wavelet scattering in Python - GitHub](https://github.com/kymatio/kymatio) - Kymatio is an implementation of the wavelet scattering transform in the Python programming language,...

12. [[PDF] Kymatio: Scattering Transforms in Python | Matthew Hirn](https://matthewhirn.com/wp-content/uploads/2020/06/2020-andreux-et-al-kymatio-scattering-transforms-in-python.pdf) - This article presents Kymatio, a scattering transform implementation that is user-friendly, well-doc...

13. [[PDF] Deep Scattering Spectrum](https://www.di.ens.fr/~mallat/papiers/AudioScatSpectrum.pdf) - This paper studies the construc- tion of stable, invariant signal representations over such larger t...

14. [dpwe/audfprint: Landmark-based audio fingerprinting - GitHub](https://github.com/dpwe/audfprint) - Landmark-based audio fingerprinting. Create a new fingerprint dbase with "new", append new files to ...

15. [DAC-JAX: A JAX Implementation of the Descript Audio Codec - arXiv](https://arxiv.org/html/2405.11554v1)

16. [[PDF] Joint Time-Frequency scattering for audio classification](https://www.lostanlen.com/wp-content/uploads/2019/06/anden2015mlsp.pdf) - Andén and S. Mallat, “Deep scattering spectrum,”. IEEE Trans. Sig. Proc., vol. 62, pp. 4114–4128, 20...

17. [[PDF] Holographic reduced representations - Cog Sci](https://pages.ucsd.edu/~msereno/170/readings/06-Holographic.pdf)

18. [[PDF] Holographic reduced representations](https://redwood.berkeley.edu/wp-content/uploads/2020/08/Plate-HRR-IEEE-TransNN.pdf) - Memory models using circular convolution provide a way of representing compositional structure in di...

19. [Resonator Networks, 2: : Factorization Performance and Capacity ...](https://dl.acm.org/doi/abs/10.1162/neco_a_01329) - We develop theoretical foundations of resonator networks, a new type of recurrent neural network int...

20. [Resonator Networks, 1: An Efficient Solution for Factoring High ...](https://ieeexplore.ieee.org/document/9272714/) - Here we show how this may be accomplished within the framework of Vector Symbolic Architectures (VSA...

21. [[2112.15424] A Survey on Hyperdimensional Computing aka Vector ...](https://arxiv.org/abs/2112.15424) - Part I of this survey covered foundational aspects of the field, such as the historical context lead...

22. [A Survey on Hyperdimensional Computing aka Vector Symbolic Architectures, Part I: Models and Data Transformations](https://arxiv.org/abs/2111.06077v1) - This two-part comprehensive survey is devoted to a computing framework most commonly known under the...

23. [[2301.10352] Capacity Analysis of Vector Symbolic Architectures](https://arxiv.org/abs/2301.10352) - We analyze the representation capacities of four common VSAs: MAP-I, MAP-B, and two VSAs based on sp...

24. [[PDF] Capacity Analysis of Vector Symbolic Architectures - arXiv](https://arxiv.org/pdf/2301.10352.pdf) - Bundles of bindings via matrices. Some VSA systems implement binding using the. Hadamard (element-wi...

25. [Linearithmic Clean-up for Vector-Symbolic Key-Value Memory with ...](https://arxiv.org/abs/2506.15793) - We present a new codebook representation that supports efficient clean-up, based on Kroneker product...

26. [[PDF] Thesis Body](https://www.collectionscanada.gc.ca/obj/thesescanada/vol2/OKQ/TC-OKQ-5966.pdf)

27. [Torchhd: An Open Source Python Library to Support Research on Hyperdimensional Computing and Vector Symbolic Architectures](https://arxiv.org/abs/2205.09208) - Hyperdimensional computing (HD), also known as vector symbolic architectures (VSA), is a framework f...

28. [Releases · hyperdimensional-computing/torchhd](https://github.com/hyperdimensional-computing/torchhd/releases) - Torchhd is a Python library for Hyperdimensional Computing and Vector Symbolic Architectures - hyper...

29. [hdlib](https://pypi.org/project/hdlib/0.1.2/) - Hyperdimensional Computing Library for building Vector Symbolic Architectures in Python

30. [cumbof/hdlib: Hyperdimensional Computing Library for ... - GitHub](https://github.com/cumbof/hdlib) - Here we present hdlib, a Python library for designing Vector-Symbolic Architectures. It is distribut...

31. [[PDF] hdlib: A Python library for designing Vector-Symbolic Architectures](https://www.theoj.org/joss-papers/joss.05704/10.21105.joss.05704.pdf) - Authors of papers retain copyright and release the work under a. Creative Commons Attribution 4.0. I...

32. [[PDF] Hopfield Networks is All You Need - OpenReview](https://openreview.net/pdf?id=tL89RnzIiCd) - This energy leads to an exponential storage capacity of N = 2d/2 for binary patterns. Furthermore, w...

33. [UNIVERSAL HOPFIELD NETWORKS](https://icml.cc/media/icml-2022/Slides/17308.pdf)

34. [modern hopfield networks](https://arxiv.org/pdf/2502.10122.pdf)

35. [ml-jku/hopfield-layers: Hopfield Networks is All You Need - GitHub](https://github.com/ml-jku/hopfield-layers) - License. This repository is BSD-style licensed (see LICENSE), except where noted otherwise. About. H...

36. [The Theta-Gamma Neural Code | Fewer Lacunae](https://kevinbinz.com/2021/12/09/the-theta-gamma-neural-code/) - This theta-gamma neural code is important for learning and memory ( Lisman & Jensen 2013 ). Theta Se...

37. [The Theta-Gamma Neural Code - ScienceDirect.com](https://www.sciencedirect.com/science/article/pii/S0896627313002316) - Theta and gamma frequency oscillations occur in the same brain regions and interact with each other,...

38. [Modeling the contribution of theta-gamma coupling to sequential ...](https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2024.1326609/full) - Gamma oscillations nested in a theta rhythm are observed in the hippocampus, where are assumed to pl...

39. [A simple and flexible code for Reservoir Computing ...](https://github.com/reservoirpy/reservoirpy) - A simple and flexible code for Reservoir Computing architectures like Echo State Networks - reservoi...

40. [Create Efficient and Complex Reservoir Computing Architectures with ReservoirPy](https://inria.hal.science/hal-03761440/document)

41. [Enhancing deep neural networks through complex-valued representations and Kuramoto synchronization dynamics](http://arxiv.org/abs/2502.21077) - Neural synchrony is hypothesized to play a crucial role in how the brain organizes visual scenes int...

42. [Binding threshold units with artificial oscillatory neurons](http://www.arxiv.org/abs/2505.03648) - Artificial Kuramoto oscillatory neurons were recently introduced as an alternative to threshold unit...

43. [Theta, Gamma, and Working Memory](https://www.cs.cmu.edu/afs/cs/academic/class/15883-f13/slides/hc-rhythms.pdf)

44. [torchhd](https://torchhd.readthedocs.io/en/stable/torchhd.html)

45. [[PDF] Resonator circuits: a neural network for efficiently solving ...](https://redwood.berkeley.edu/wp-content/uploads/2021/08/Module5_ResonatorNetworks_FocusReading.pdf) - The connectionist literature proposed “vector-symbolic architectures” (VSA) to solve this problem. S...

46. [Hopfield Networks is All You Need](https://ml-jku.github.io/hopfield-layers/) - This blog post explains the paper Hopfield Networks is All You Need and the corresponding new PyTorc...

