# ENGRAM — Frequency, Music & Memory: Research Map
## Literature + repositories to evolve ENGRAM (situational Fourier memory) toward a music-theory-aligned, composable, resonance-retrieved system
## Created: 2026-06-24 · Dexter × Claude Opus 4.8 · companion to MUSIC_AND_FREQUENCY_CONCEPTS.md, ENGRAM_FOR_VECTOR.md

> Grounded in the current implementation (`vector_engram/fingerprint.py`): ENGRAM today = `|rFFT|`
> of a `[T,D]` window, amplitude at freqs {0,1}, each block L2-normalized, concat → `[D·2]`, cosine
> retrieval via hnswlib. Deterministic, training-free, **amplitude-only (phase discarded)**, single time-scale.
>
> Honesty: links/IDs gathered via web research; a few flagged as unverified. Separate **buildable** from
> **fringe** is enforced (see §5).

---

## 0. The convergent insight (why the four pillars are one design)

Dexter's intuitions ("memory as *frequency*", "f0/f1 are notes composed into a symphony", "personality =
one big shape from a labeled collection", "a constantly vibrating brain") line up with four mature research
lineages that **compose into a single upgraded architecture**:

```
REPRESENT  →  multi-scale, deformation-stable spectral features over a FIXED codebook
              (scattering/wavelets = "bars 4/8/16/32" · VQ dictionary = "the notes" · keep phase as index)
COMPOSE    →  VSA/HRR: bind (circular convolution = Fourier-domain multiply) + bundle, under LABELS,
              hierarchically (notes→motifs→themes→self) = the "identity shape / system-prompt-as-frequency"
RETRIEVE   →  Modern Hopfield = attention = a STRICT GENERALIZATION of our cosine-kNN ("retrieval by
              resonance", tunable sharpness β, multi-step pattern completion); resonator nets decompose motifs
GROUND     →  real neuroscience (theta-gamma ordering, associative memory) supports phase-as-index +
              resonance retrieval; drop the Schumann/"healing-frequency" mysticism entirely
```

The most striking validation: **"memory as frequency" + "compose into one personality shape" + "retrieve by
resonance" = HRR (frequency-domain binding) + Modern Hopfield (resonance retrieval)** — both real, both
open-source (MIT/BSD), and *our current cosine-kNN is already a special case of the retrieval half.*

---

## 1. Pillar A — Representation: music-aligned, multi-scale, robust fingerprints

### Key papers
| Work | Year | Why it matters | Link |
|---|---|---|---|
| Wang, "An Industrial-Strength Audio Search Algorithm" (Shazam) | 2003 | Constellation of spectral peaks → `(f1,f2,Δt)` landmark hashes; noise/codec-robust, scales to millions | https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf |
| Mallat, "A Theory for Multiresolution Signal Decomposition" | 1989 | Foundational wavelet MRA — long windows for low freq ("this hour"), short for high ("this instant") = the literal 4/8/16/32 "bars" | https://ieeexplore.ieee.org/document/192463/ |
| Bruna & Mallat, "Invariant Scattering Convolution Networks" | 2013 | Translation-invariant, **deformation-stable**, training-free representation (a CNN with fixed wavelet filters) | https://arxiv.org/pdf/1203.1513 |
| Andén & Mallat, "Deep Scattering Spectrum" | 2014 | 1-D/audio scattering; recovers modulation info MFCC discards; **best theoretical match for a robust fingerprint** | https://arxiv.org/pdf/1304.6763 |
| Brown, "Calculation of a constant-Q spectral transform" | 1991 | Log-frequency bins (Q=f/Δf) → musical/octave structure; scaling becomes a shift (invariance) | (JASA) |
| van den Oord et al., "VQ-VAE / Neural Discrete Representation Learning" | 2017 | Learns a discrete **codebook** = "the fixed notes" | https://arxiv.org/abs/1711.00937 |
| Zeghidour et al. "SoundStream" / Défossez "EnCodec" / Kumar "DAC" | 2021–23 | **Residual VQ** = coarse→fine code stacks (matches ENGRAM's coarse-to-fine spirit) | EnCodec https://github.com/facebookresearch/encodec · DAC https://github.com/descriptinc/descript-audio-codec |
| Olshausen & Field, "Sparse coding…" | 1996 | Origin of dictionary learning; atoms emerge as Gabor primitives | — |
| Aharon/Elad/Bruckstein, "K-SVD" | 2006 | Overcomplete dictionary learning | — |

### Repos (license-checked)
| Repo | License | Lang | Use |
|---|---|---|---|
| librosa | ISC | Py | STFT/CQT/chroma/tonnetz/beat — easiest testbed reference · https://github.com/librosa/librosa |
| kymatio | BSD-3 | Py | wavelet **scattering** (1D/2D), numpy frontend (CPU) · https://github.com/kymatio/kymatio |
| PyWavelets (`pywt`) | MIT | C/Py | DWT/CWT/wavelet packets · https://github.com/PyWavelets/pywt |
| ssqueezepy | MIT | Py | fast CWT + synchrosqueezing · https://github.com/OverLordGoldDragon/ssqueezepy |
| scikit-learn dict-learning | BSD-3 | Py | `MiniBatchDictionaryLearning`, `SparseCoder` (the "notes") |
| audfprint / Dejavu | MIT | Py | reference Shazam landmark-hashing impls · https://github.com/dpwe/audfprint · https://github.com/worldveil/dejavu |
| EnCodec / DAC | MIT | Py | production residual-VQ codecs / audio tokenizers |
| ⚠ Essentia, Panako | **AGPL-3.0** | C++/Java | rich MIR — **avoid** for a permissive/closed build |
| ⚠ aubio (GPL-3), Chromaprint (LGPL via FFmpeg), SPAMS (GPL-3) | copyleft | — | flagged; prefer permissive equivalents |

### Mapping to ENGRAM
1. **Notes (fixed codebook):** fit a small VQ/dictionary **once, offline, then freeze** over fused frames → each frame = nearest codeword. Stable primitive alphabet, stays deterministic at inference. RVQ keeps our coarse→fine spirit.
2. **Grammar (content vs timing split):** today f0/f1 conflate "what" and "how it changes." Split into a **content track** (token sequence) + a **rhythm/structure track** (onsets, inter-onset intervals, **rests** = low-energy frames, repetition via self-similarity matrix). This is the score-vs-timbre split = your "same notes, different song."
3. **Multi-scale "bars":** replace single-window 2-bin FFT with a **dyadic stack (4/8/16/32)** via DWT energy-per-level, or — recommended — **`Scattering1D`** (J≈5, Q≈1): 0th order="this hour", 1st≈envelope, 2nd=modulation; shift-invariant + warp-stable (fixes `|FFT|` jitter fragility).
4. **Constant-Q / chroma:** log-frequency binding → multiplicative magnitude scaling becomes a translation (robustness); chroma (octave-fold) = max invariance, min dims.
5. **Keep phase as an index** (we currently discard it) — see §3/§4.

---

## 2. Pillar B — Composition: identity shapes under labels (VSA / HRR / HDC)

**This is the rigorous home of "the system prompt is a composed ENGRAM shape under a label."**

### Key papers
| Work | Year | Why | Link |
|---|---|---|---|
| Smolensky, "Tensor Product Variable Binding" | 1990 | origin of distributed binding (dim grows → motivates "reduced" forms) | — |
| **Plate, "Holographic Reduced Representations"** | 1991/95 | **canonical**: bind = circular convolution (= multiply FFTs), bundle = add, unbind = correlation, + **cleanup memory** | https://redwood.berkeley.edu/wp-content/uploads/2020/08/Plate-HRR-IEEE-TransNN.pdf |
| Kanerva, "Hyperdimensional Computing: An Introduction" | 2009 | accessible whole-field tutorial; also originator of **Sparse Distributed Memory** (1988) | https://link.springer.com/article/10.1007/s12559-009-9009-8 |
| Gayler, "VSA answer Jackendoff's challenges" | 2003 | coined "VSA"; bind/bundle/permute requirements | https://arxiv.org/abs/cs/0412059 |
| Eliasmith, *How to Build a Brain* (SPA / Spaun) | 2013 | semantic pointers = compressed HRR vectors in spiking neurons | — |
| **Frady/Kent/Olshausen/Sommer, "Resonator Networks 1 & 2"** | 2020 | **factor a bound product back into its parts** (decompose person⊗place⊗feeling) | https://arxiv.org/abs/2007.03748 |
| Kleyko et al., "Survey on HDC/VSA, Parts I & II" | 2022 | best entry point; compares HRR/FHRR/MAP/BSC | https://arxiv.org/abs/2111.06077 · https://arxiv.org/abs/2112.15424 |
| "Capacity Analysis of VSA" | 2023 | how many vectors you can bundle vs dim D | arXiv:2301.10352 ⚠ (abstract 403 via proxy; exists) |
| "Linearithmic Clean-up… Kronecker Rotation Products" | 2025 | O(N log N) cleanup for large namespaces | https://arxiv.org/pdf/2506.15793 |

### Repos
| Repo | License | Use |
|---|---|---|
| **torchhd** | MIT | most complete VSA: HRR/**FHRR**/MAP/BSC, bundle/permute/cleanup, resonator examples — **best fit** (FHRR maps onto our Fourier fingerprints) · https://github.com/hyperdimensional-computing/torchhd |
| **hdlib** | MIT | pure-numpy VSA primitives — **most edge/ARM-friendly**, closest to our testbed · https://github.com/cumbof/hdlib |
| nengo-spa (+nengo) | MIT* (verify) | SPA / spiking-plausible; heavier · https://github.com/nengo/nengo-spa |

### Mapping to ENGRAM (the identity-shape architecture)
- **Labels/namespaces:** give each cert a label set (`self`, `environment`, person, place…). Per label, a fixed random **role-key** `K_label`.
- **Identity vector:** `IDENTITY_self = Σ_i (K_self ⊛ fp_i)` (⊛=circular convolution), normalized → one fixed-width "self" shape. Membership = `cos(K_self ⊛ q, IDENTITY_self)`. This **is** the "system prompt as a living self-frequency."
- **Motifs:** `motif = (PERSON⊛alice)+(PLACE⊛kitchen)+(FEELING⊛calm)`; query by unbind+cleanup; **resonator network** when factors unknown.
- **Hierarchy for capacity (the "bars"):** leaf bundles of ≤k memories → mid-level (bound with sub-keys) → top "self". hnswlib stays the per-leaf exact store + **cleanup memory**; VSA vectors are the routing/summary layer. *They compose, not compete.*
- ⚠ **Load-bearing caveat:** our fingerprints are **L2-normalized amplitude spectra, not random vectors** — VSA capacity theory assumes near-orthogonal randoms. Correlated fingerprints → lower capacity/more crosstalk. **Must quantify** (Experiment B1) before committing; may need random role-keys + projecting fingerprints into a higher-D near-random space.

---

## 3. Pillar C — Retrieval by resonance (Modern Hopfield = attention)

| Work | Year | Why | Link |
|---|---|---|---|
| Hopfield, "Neural networks and physical systems…" | 1982 | energy-descent content-addressable memory ("retrieval by resonance"); cap ~0.14·N | https://www.pnas.org/doi/10.1073/pnas.79.8.2554 |
| **Ramsauer et al., "Hopfield Networks is All You Need"** | 2020 | modern continuous Hopfield: **exponential capacity, 1-step retrieval, = transformer attention** | https://arxiv.org/abs/2008.02217 |
| **Millidge et al., "Universal Hopfield Networks"** | 2022 | Hopfield, SDM, **cosine-kNN, attention all = `separation(similarity(q,K))·V`** — our kNN is the β→∞ special case | https://arxiv.org/pdf/2202.04557 |
| Kanerva, *Sparse Distributed Memory* | 1988 | distributed content-addressable memory | — |

Repos: **`ml-jku/hopfield-layers`** (BSD-2) https://github.com/ml-jku/hopfield-layers · `torchhd` (resonator). 

**Mapping:** don't replace the store — **swap the separation function**. cosine-kNN = top-k argmax of `cos(q,kᵢ)`; Modern Hopfield = `softmax(β·qKᵀ)·V`. Low β = blends memories (smooth resonance), high β → 1-NN (current behavior). Gains: a **tunable "sharpness of resonance" knob** + **multi-step relaxation** = true **pattern completion** from partial/noisy cues (one-shot kNN can't). Resonator iteration adds retrieval+**decomposition**.

---

## 4. Pillar D — Biological grounding (honest)

| Work | Year | Status | Link |
|---|---|---|---|
| Lisman & Jensen, "The Theta-Gamma Neural Code" | 2013 | **supported** — items ordered by gamma-cycles-in-a-theta-cycle; phase = serial position | https://pubmed.ncbi.nlm.nih.gov/23522038/ |
| O'Keefe & Recce, theta **phase precession** | 1993 | **supported** — phase carries info rate codes don't | https://onlinelibrary.wiley.com/doi/10.1002/hipo.450030307 |
| Lega 2016 / Daume 2024, human theta-gamma PAC & memory | 2016/24 | **supported** (human intracranial, incl. causal tACS) | https://pmc.ncbi.nlm.nih.gov/articles/PMC4677977/ |
| von der Malsburg (1981); Singer 1999 — **binding-by-synchrony** | — | **real but contested** (rebuttal: Shadlen & Movshon 1999) — use as *inspiration*, not fact | https://www.cns.nyu.edu/~tony/Publications/shadlen-movshon-1999.pdf |
| Jaeger ESN 2001 / Maass LSM 2002 — **reservoir computing** | — | **supported & buildable** — memory as an evolving dynamical state ("constantly vibrating shape") | reservoirpy (MIT) https://github.com/reservoirpy/reservoirpy |
| "Artificial Kuramoto Oscillatory Neurons" | 2025 | binding-by-synchrony revived in differentiable nets | https://arxiv.org/pdf/2502.21077 |

**Takeaway:** phase/frequency demonstrably *organizes and orders* memory, and memory *is* resonance-based
content-addressable retrieval — both buildable. Use **phase as a soft index** over an associative store (not
as a literal storage carrier).

---

## 5. Buildable vs fringe (enforced)
- ✅ **Build on:** scattering/wavelets, fixed VQ dictionary, constant-Q/chroma, VSA/HRR composition + namespaces + resonator nets, Modern Hopfield = attention retrieval, reservoir computing, phase-as-index, theta-gamma ordering, associative memory.
- ⚠ **Inspiration only (cite both sides):** binding-by-synchrony.
- ❌ **Drop entirely (will discredit the real work):** "Schumann resonance tunes the brain" (7.83 Hz ≈ alpha is coincidence, no entrainment), "cellular/DNA healing frequencies", "a personality is a single standing waveform at frequency X." The defensible version: *a personality is a point/trajectory in a high-dim dynamical state, composed by frequency-domain binding and retrieved by resonance.*

---

## 6. Unified experiment plan (all runnable in our numpy/hnswlib testbed)
Ranked by leverage; each is <~100 lines and answers an architecture decision.

1. **Headline — robust representation:** build a **hard near-duplicate corpus** (time-shift, mild time-warp 0.9–1.1×, noise) and compare fingerprints on recall@1/AUC: current `f0+f1` vs `+phase` vs `+more harmonics` vs **DWT-stack** vs **`Scattering1D`** vs **log-freq/chroma**. *Hypothesis: scattering/multiscale keep near-duplicates close where f0/f1 breaks.*
2. **VSA capacity with REAL fingerprints:** bundling-capacity curve (accuracy vs #items, vs dim) on random vectors **and** on actual ENGRAM fingerprints → sets leaf-bundle size `k` and tells us if we need random role-keys / higher-D projection. *(The load-bearing test before adopting VSA.)*
3. **Identity vector + namespaces:** build `IDENTITY_self` / `IDENTITY_other`; ROC for "is q a self-memory?"; confirm namespaces don't leak. → validates "system-prompt-as-shape".
4. **Retrieval by resonance:** Modern-Hopfield read `X.Tᵀ softmax(β·Xq)` (1-step + iterated) vs cosine-kNN on **corrupted** cues; sweep β. *Hypothesis: matches kNN clean, beats it on partial/noisy cues (pattern completion).*
5. **Codebook "notes":** freeze a VQ/dictionary; encode windows as sparse codes; measure retrieval + **atom-firing stability** under perturbation + bytes/latency on ARM-like budget.
6. **(optional) Resonator decomposition:** recover person/place/feeling from a bound motif; decide if resonator nets are needed vs known-key unbind.

**Recommended order:** #1 (does a better representation even help on hard cases?) → #2 (is VSA viable on our real vectors?) → #4 (is resonance retrieval a free win over kNN?) → #3 → #5 → #6.

---

## 7. Top repos to pull when clonable (license-clean)
`torchhd` (MIT, VSA/FHRR/resonator) · `hdlib` (MIT, edge VSA) · `kymatio` (BSD, scattering) · `pywt` (MIT, wavelets) · `ml-jku/hopfield-layers` (BSD-2, resonance retrieval) · `reservoirpy` (MIT) · `librosa` (ISC) · `audfprint`/`dejavu` (MIT) · scikit-learn (BSD, dict-learning). **Avoid:** Essentia/Panako (AGPL), aubio (GPL), SPAMS (GPL), Chromaprint-with-FFmpeg (LGPL).

*Flags: arXiv 2301.10352 abstract 403'd via proxy (paper exists); EnCodec(2210.13438)/DAC(2306.06546) IDs from citation memory — verify before formal citation; nengo-spa & SDM repo licenses to confirm in-repo.*
