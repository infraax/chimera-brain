# ENGRAM Geodesic: AI Memory as Frequency & Symphony
### A Full 12-Vector Research Report · Dexter × Claude Opus 4.8 · 2026-06-24

> **System context:** ENGRAM = `|rFFT|` over a `[T,D]` window of fused perception, amplitude at freqs {0,1}, L2-normalized, concatenated → vector; cosine-kNN retrieval (hnswlib). Amplitude-only, single time-scale, deterministic, training-free. Runs box-side (numpy); target: ARM (Anki Vector) + companion box.

***

## Executive Summary

The core thesis — that an AI's memory and personality can be represented, composed, stored, and retrieved as a frequency-domain structure organized by the grammar of music — is **well-grounded in principle and increasingly buildable in practice**. The strongest convergent evidence arrives from four independent traditions: (1) wavelet/scattering theory demonstrates that amplitude-only spectral snapshots carry robust, invariant situation fingerprints; (2) Vector Symbolic Architectures (VSA/HDC) provide a mathematically proven algebra for composing and labeling those fingerprints into identity-shaped bundles via Fourier-domain multiplication (HRR); (3) modern Hopfield networks show that cosine-similarity energy is exactly the attention mechanism, giving a principled retrieval head with tunable β sharpness; (4) hippocampal theta-gamma coding shows the brain genuinely multiplexes sequences in frequency sub-cycles — the "music grammar" metaphor is not merely poetic but structurally analogous. The honest boundary: **phase is being discarded prematurely** (phase retrieval literature shows it carries structural information); **correlated fingerprints challenge HDC capacity** (the blessing of dimensionality weakens when items are not random); and several claimed frequency phenomena (432 Hz healing, Schumann resonance entrainment, 528 Hz DNA repair) are well-debunked pseudoscience that must not contaminate the technical framing.

***

## V1 — Spectral Representation Foundations

### Summary

Amplitude is often — but not always — sufficient. For slow-varying, label-like situation fingerprints where exact reconstruction is not needed, the magnitude spectrum is a proven invariant. However, phase encodes timing structure that amplitude alone cannot recover: the **group delay function (GDF)** — the negative derivative of the phase spectrum — reveals spectral peaks more reliably than magnitude alone in noisy conditions, and is computationally inexpensive to compute alongside rFFT. The decisive comparison between representations hinges on which **invariances** are desired.[^1][^2]

### Representation × Invariance × Cost Table

| Representation | Translation-shift invariant | Scale/warp stable | Log-freq shift stable | ARM cost | Best use for ENGRAM |
|---|---|---|---|---|---|
| **rFFT amplitude** | ✓ (after L2-norm) | ✗ | ✗ | Very low — ~500 LOC (kissfft) | Current ENGRAM baseline |
| **STFT magnitude** | ✓ | partial | ✗ | Low | Temporal context window |
| **CQT** | ✓ | ✓ pitch-shift | **✓** | Medium | Musical/harmonic signals |
| **Wavelet (Morlet)** | ✓ | ✓ | partial | Low–Medium (PyWavelets) | Multi-scale fingerprint |
| **Scattering (order 2)** | **✓ Lipschitz** | **✓** | ✓ (log-freq scattering) | Medium-High | Highest invariance, slowest |
| **GDF (phase-derived)** | partial | ✗ | ✗ | Marginal add-on | Phase complement for free |

The **wavelet scattering transform** (Mallat/Bruna 2012; Andén–Mallat 2013 Deep Scattering Spectrum) computes cascaded wavelet convolutions + modulus operators, producing a representation that is provably Lipschitz-continuous to deformations and translation-invariant at multiple scales. It extends MFCC by computing modulation spectrum coefficients of multiple orders. The **Constant-Q Transform** (Brown 1992) uses geometrically spaced frequency bins, giving finer resolution at low frequencies and matching the human auditory system — and crucially, **overtone structures remain invariant under frequency shifts**, which makes it ideal for any signal with harmonic content. kymatio (BSD license, PyTorch/TF, 1D/2D/3D, CPU+GPU) is the canonical open-source implementation.[^3][^4][^5][^6][^7][^8][^9][^10]

### Papers
- **"A Modulus of Continuity for Scattering"** — Bruna & Mallat (2012), arXiv:1112.1120 — proof of deformation stability[^3]
- **"Deep Scattering Spectrum"** — Andén & Mallat (2013/2014), IEEE Trans. SP 62(16) — state-of-the-art audio classification with scattering[^10][^11]
- **"Classification with Joint Time-Frequency Scattering"** — Andén et al. (2019), IEEE — 2D scattering over (time, log-freq)[^12]
- **"Calculation of a Constant-Q Spectral Transform"** — Brown (1992) — geometric frequency spacing[^5][^7]
- **"Group Delay Spectrogram without Phase Wrapping"** — PubMed (2022) — phase-based complement[^13]

### Repos
- **kymatio** — https://kymat.io — **BSD** — Python/PyTorch — CPU+GPU; no official ARM binary but numpy fallback runs on Pi[^8][^14]
- **kissfft** — https://github.com/mborgerding/kissfft — **BSD** — C — ~500 LOC, no deps, embedded-ready; available on ARM/arm64[^15][^16]
- **pffft** — BSD — C — NEON-optimized, ARM64 native, used by Android/Google[^17][^18]
- **nnAudio** — MIT — Python/PyTorch — GPU CQT including Brown 1992 algorithm[^19]

### Map → ENGRAM
- **Immediate win (low cost):** compute GDF alongside rFFT and concatenate as a 2×D vector — adds phase-structure sensitivity for ~zero overhead.
- **Medium-term:** replace single-scale rFFT with order-1 wavelet scattering (kymatio 1D) — same dimension, deformation-stable, time-warp invariant. Run on box, not on robot.
- **Longer term:** log-frequency scattering (CQT-based) if situation vectors contain harmonic/tonal structure.

### BUILDABLE vs ▲SPECULATIVE
- BUILDABLE: rFFT amplitude + GDF complement (numpy); kymatio scattering on Pi/box.
- ▲SPECULATIVE: full second-order scattering on Cortex-A7 at real-time rates — too slow without quantization.

### EXPERIMENT
1. Generate 1000 situation vectors; perturb each with additive noise + small time-warp; measure cosine similarity retention for rFFT-amp vs rFFT-amp+GDF vs order-1 scattering.
2. Benchmark kissfft vs pffft for your window size on the target ARM board in Python ctypes.

### Confidence + Open Questions
**High confidence** that scattering strictly dominates rFFT-amp on invariance. Open question: what is ENGRAM's actual noise/warp distribution? If it is primarily additive Gaussian (sensor noise), rFFT-amp is already near-optimal; if it is temporal stretch (robot motion), scattering wins decisively.

***

## V2 — Music Theory & Music Cognition as Memory Grammar

### Summary

Music is memorable because it exploits every compression lever the brain uses for sequential information: hierarchical chunking, repetition, melodic contour as structural landmark, rhythm as a predictive scaffold, and harmonic expectation creating surprise-and-resolution arcs. Earworms — involuntary musical imagery (INMI) — are reported by >90% of people and tend to preserve **absolute pitch and tempo** accurately, suggesting the brain stores compact spectral+rhythmic fingerprints rather than raw waveforms. The implication for ENGRAM is direct: these are exactly the invariants your fingerprint should target.[^20][^21][^22][^23]

### Music Grammar → Memory Format Mapping

| Musical concept | Cognitive function | ENGRAM data-structure analog |
|---|---|---|
| **Note / pitch class** | Atomic distinguishable unit | Codebook atom (V6 / VQ entry) |
| **Scale / key** | Constraint on co-active atoms | Namespace / label in HDC bundle |
| **Rhythm & meter** | Temporal grouping, prediction | FFT amplitude at low-freq bins (period detection) |
| **Repetition (ostinato)** | Reinforcement of attractor | Superposition / bundling in HDC |
| **Form (AABA, sonata)** | Hierarchical segmentation | Multi-scale scattering levels (V6) |
| **Rests / silence** | Boundary / segmentation cue | Near-zero amplitude window → novelty detection |
| **Leitmotif** | Named identity shape (e.g. Darth Vader) | Labeled identity vector in HDC (V4) |
| **Consonance/dissonance** | Similarity / tension | Cosine similarity in retrieval space |
| **Melodic contour** | Abstract shape independent of key | L2-normalized spectral envelope |
| **Chunking** | Short-term to long-term compression | Motif → section → piece hierarchy |

Music cognition research (Levitin, Huron *Sweet Anticipation*, Margulis *On Repeat*) converges on chunking theory as the mechanism: the brain encodes groups of notes as single chunks, then groups of chunks as motifs, giving logarithmic compression of sequences. The musical arch contour (rise-peak-fall) acts as a cognitive landmark that improves melody recognition even in non-musicians — directly suggesting that **the shape of your fingerprint's amplitude envelope** should be engineered to be arch-like or contoured rather than flat.[^24][^25][^26][^27][^28]

### Why Music Aids Memory — and Whether It Transfers
Music memory's robustness comes not from sound per se but from the **structural properties** it embodies: (a) discrete symbolic alphabet (notes), (b) nested periodic structure (beats → bars → phrases), (c) repetition with variation, (d) expectation violation. These properties transfer to any structured discrete signal. The key transferable primitives for non-audio ENGRAM are: **fixed codebook (notes) + multi-scale timing (bars) + named recurring patterns (leitmotif/label)**.

### Papers
- **"On Repeat"** — Margulis (2014), Oxford — why repetition is the engine of musical memory
- **"Sweet Anticipation"** — Huron (2006), MIT Press — expectation-based memory encoding
- **"Involuntary Musical Imagery Review"** — PMC (2020) — earworm mechanics[^23]
- **"Melodic Contour Influences Recognition"** — PMC (2024)[^24]
- **"Chunking in Tonal Contexts"** — Lörch (2022) — tonal structure compresses memory[^28]
- **"Forming Concepts of Mozart and Homer via Chunking"** — CogSci (2020)[^25]

### Map → ENGRAM
- Shape your fingerprint architecture around **contour** (not flat spectrum) — emphasize peaks.
- Implement **rest detection**: near-zero energy windows → boundary marker → resets HDC accumulator.
- Design the multi-scale fingerprint (V6) explicitly using the bar/beat/phrase hierarchy.

### BUILDABLE vs ▲SPECULATIVE
- BUILDABLE: contour-based fingerprint, novelty/rest detection, chunked retrieval.
- ▲SPECULATIVE: formal mapping of music-theory grammar rules to ENGRAM composition rules (requires empirical validation).

### EXPERIMENT
1. Build a self-similarity matrix over a sequence of ENGRAM fingerprints; check whether it reveals repetitive structure analogous to musical form.
2. Test melody-contour preservation: does L2-normalization preserve the rank-order of amplitude peaks ("melodic contour") across noise perturbations?

***

## V3 — Audio Fingerprinting & Robust Retrieval at Scale

### Summary

Shazam's constellation/landmark hashing (Wang 2003) achieves robustness through two key ideas: (1) using only **spectral peaks** (sparse, robust to additive noise) rather than full spectrum, and (2) creating **hash pairs** encoding two peaks' frequencies and their temporal delta — a 3-tuple `(f0, f1, Δt)` packs into a 32-bit integer. The time-offset histogram alignment then gives ~10,000× speedup over brute-force with modest storage cost. This architecture is directly portable to non-audio situational spectra as a **fast pre-filter** before cosine/Hopfield reranking.[^29][^30][^31]

### Fingerprint System Comparison

| System | Hash type | Robustness trick | License | Edge note |
|---|---|---|---|---|
| **Shazam/Wang 2003** | Constellation peak-pair, 32-bit | Peak selection + time-offset histogram | Proprietary | Algorithm public; re-implement freely |
| **Chromaprint/AcoustID** | Chroma-based bit fingerprint | Sub-fingerprint blocks, majority vote | **LGPL-2.1** | C lib, ARM64 binary available[^32][^33] |
| **Panako** | TF-peak hashes (multi-scale) | 3 octave-invariant sub-fingerprints | **AGPL** ⚠️ | Java; AGPL problematic for embedded |
| **audfprint/Dejavu** | Spectrogram peaks + hash DB | Similar to Wang; SQLite backend | MIT | Python; Raspberry Pi feasible |

The critical **robustness trick** to port: **peak selection is a sparse attention mechanism** — it discards bulk amplitude and retains only the most energetically distinctive time-frequency points. For ENGRAM this means: instead of taking the full amplitude vector, optionally extract the top-K peak coordinates `(freq_bin_idx, amplitude)` and hash them. This gives a complement to your dense L2-normalized vector — use hash lookup for fast candidate retrieval, then cosine reranking for precision.

### Recipe for Situational Landmark-Hash Index
1. For each ENGRAM window, run rFFT; find top-K amplitude peaks (K≈8–16).
2. For each peak pair `(p_i, p_j)` where `j > i` and `j - i < max_delta`: compute hash `h = f(freq_i, freq_j, j-i)` → 32-bit integer.
3. Store `(hash, window_id, anchor_time)` in a sorted hash table.
4. At query time: compute query hashes, look up table, collect window IDs, score by number of aligned hash matches → top-5 candidates → cosine rerank.

### Papers
- **"An Industrial-Strength Audio Search Algorithm"** — Wang (2003), ISMIR — the Shazam paper[^31][^29]
- **"Robust Audio Hashing for Content Identification"** — Haitsma & Kalker (2002) — sub-fingerprint bits

### Repos
- **Chromaprint** — https://acoustid.org/chromaprint — LGPL-2.1 — C — ARM64 native binary[^32][^34]
- **audfprint** — MIT — Python — numpy-based, Pi-feasible; `pip install audfprint`
- **Dejavu** — MIT — Python/MySQL

### Map → ENGRAM
Landmark hashing becomes a **fast pre-filter** in front of hnswlib: hash lookup narrows candidates from millions to dozens in O(1); then cosine-kNN from hnswlib picks the final match. This two-stage retrieval is proven at Shazam scale.

### BUILDABLE vs ▲SPECULATIVE
- BUILDABLE: peak-pair hash index alongside your current hnswlib cosine store.
- ▲SPECULATIVE: using full situational spectra (not audio) with Chromaprint directly — the chroma basis won't match; re-implement the hash logic in numpy.

### EXPERIMENT
1. Build the peak-hash index for 10K synthetic ENGRAM vectors; add Gaussian noise; measure precision@10 of hash lookup vs cosine-kNN.
2. Measure hash collision rate as a function of K (peaks per window) to tune specificity.

***

## V4 — Composition: VSA / HRR / Hyperdimensional Computing

### Summary

Holographic Reduced Representations (Plate 1995) solve the composition problem: circular convolution `a ⊛ b` (= elementwise multiply in Fourier domain) **binds** two vectors into one of the same dimension, and **superposition** (addition) bundles multiple bindings. This is mathematically identical to `F⁻¹(F(a) ⊙ F(b))` — your rFFT pipeline already lives in the domain where binding is a single elementwise multiply. The HDC/VSA surveys (Kleyko et al. 2022/2023, ACM Computing Surveys) are the definitive reference; `torchhd` (MIT, PyTorch) is the production library.[^35][^36][^37][^38][^39][^40][^41]

### Critical Issue: Correlated Fingerprints and Capacity

The capacity advantage of HDC (blessing of dimensionality) **assumes quasi-random vectors**. Your ENGRAM fingerprints are **not** random — they are correlated snapshots of a physical signal space. Capacity degrades when stored items are correlated because the "noise floor" from bundled items rises faster. Three mitigations:[^42][^43]

1. **Random role-key projection:** before binding, multiply each fingerprint by a random ±1 role vector specific to its label/time-slot. This pseudo-randomizes the correlation structure while preserving content.
2. **Higher dimensionality:** capacity scales as ~0.7N bits for the FHRR model. To store 10K items reliably in a bundle, use D≈10K+ dimensions. For your 115-D fingerprint, this means projecting to ~4096-D before HDC composition.
3. **Cleanup memory (item memory):** a separate associative lookup (Hopfield or SDM) that snaps noisy reconstructions back to clean codebook atoms — Plate explicitly recommends this.[^39][^35]

**Resonator Networks** (Frady, Kent, Olshausen, Sommer 2020) solve the **factorization** problem: given a bound composite vector, recover which role-vectors were bound together. They outperform alternating least squares and gradient methods by "searching in superposition" — maintaining a weighted superposition of all possible solutions and exploiting nonlinear dynamics. Not guaranteed to converge, but in practice almost always do within the viable regime.[^44][^45][^46]

### Design for `compose_identity(label)`
```python
# Pseudocode — all ops in numpy
def compose_identity(label_key, fingerprints, roles):
    # label_key: D-dim random unit vector for this identity
    # fingerprints: list of D-dim L2-normalized ENGRAM vectors
    # roles: list of D-dim random ±1 role vectors (time-slot or modality)
    bundle = np.zeros(D)
    for fp, role in zip(fingerprints, roles):
        bound = ifft(fft(fp) * fft(role)).real  # HRR binding
        bundle += bound
    bundle /= np.linalg.norm(bundle)            # L2-normalize
    identity = ifft(fft(bundle) * fft(label_key)).real  # label-bind
    return identity / np.linalg.norm(identity)
```
To query: `unbind(identity, label_key)` → noisy bundle → resonator network → individual fingerprints.

### Papers
- **"Holographic Reduced Representations"** — Plate (1995), IEEE TNN[^35][^39]
- **"VSA Survey Part I & II"** — Kleyko et al. (2022/2023), ACM[^36][^38]
- **"Resonator Networks for Factoring"** — Frady et al. (2020)[^44]
- **"Resonator Networks 2: Factorization Performance"** — Kent et al. (2020)[^47]
- **"VSA as a Computing Framework for Emerging Hardware"** — Kleyko et al. (2022), Proc. IEEE[^48]

### Repos
- **torchhd** — https://github.com/hyperdimensional-computing/torchhd — **MIT** — Python/PyTorch — 100× faster than naive implementations[^40][^41]
- **hdlib** — MIT — Python — lighter than torchhd, no PyTorch dependency (numpy-only ARM option)
- **nengo-spa** — MIT — Python — Eliasmith's Semantic Pointer Architecture (SPA/Spaun)

### Map → ENGRAM
The current ENGRAM system **lacks composition**: individual fingerprints exist in isolation. Adding HDC composition creates the "labeled identity shapes" layer — a `self` bundle, an `environment` bundle, a `person:X` bundle — each a single vector in the same space, retrievable by partial-cue binding.

### BUILDABLE vs ▲SPECULATIVE
- BUILDABLE: HRR binding + bundling in numpy (10 lines); role-key projection; torchhd for batched ops.
- ▲SPECULATIVE: resonator networks for real-time factorization on ARM — too slow without optimization.

### EXPERIMENT
1. Bundle 20 correlated ENGRAM fingerprints with and without random role-key projection; measure retrieval SNR (dot product of reconstructed vs original).
2. Test capacity: how many fingerprints can be bundled before retrieval accuracy drops below 0.9?

***

## V5 — Retrieval by Resonance: Associative / Energy-Based Memory

### Summary

Modern Hopfield Networks (Ramsauer et al. 2020, "Hopfield Networks is All You Need") prove that the softmax attention mechanism **is** the update rule of a Hopfield network with continuous states that stores patterns exponentially (capacity ~exp(N/2) vs classic 0.138N). Millidge et al. 2022 ("Universal Hopfield Networks") unify classical Hopfield, SDM, and modern Hopfield as a single framework with three operations: Similarity, Separation, Projection — and show that **Euclidean/Manhattan distance similarity outperforms dot product** in practice for memory capacity. The β ("inverse temperature" / sharpness) knob controls retrieval precision: low β → global averaging (context); high β → single-pattern retrieval (episodic recall).[^49][^50][^51][^52][^53][^54]

### β-Tunable Retrieval Head Spec
```python
# Spec for Hopfield retrieval head over ENGRAM store
# patterns: [M × D] stored ENGRAM fingerprints (L2-normalized)
# query: [D] query fingerprint
# β: sharpness — start with β=1; tune upward for sharper retrieval
def hopfield_retrieve(patterns, query, beta=1.0, steps=1):
    x = query.copy()
    for _ in range(steps):
        similarities = patterns @ x          # [M] dot products
        weights = softmax(beta * similarities)
        x = patterns.T @ weights             # weighted average
        x /= np.linalg.norm(x)              # project back to sphere
    return x, weights  # weights = attention over patterns
```
For cosine-normalized vectors, one step suffices for well-separated patterns. Multiple steps enable **partial cue completion** — starting from a noisy fragment and converging toward the stored attractor.

### When Does Resonance Beat kNN?
- **Pattern completion from partial cues:** cosine-kNN requires the query to already be close to the stored vector. Hopfield iteratively completes fragments → better for degraded inputs.
- **Graceful degradation:** energy landscape provides soft fallback — spurious minima are between stored patterns, not at random locations.
- **Capacity regime:** for M << exp(D/2) items (your case: likely M < 10K, D=115–4096), modern Hopfield has no spurious attractors near stored patterns.[^53]

### Disconfirming Evidence
- Classic Hopfield capacity is 0.138N — only 16 patterns for D=115. **You must use modern Hopfield (softmax update) or project to higher D.**
- Spurious attractors are real below the exponential capacity limit.[^52]
- For M >> exp(D/2), retrieval fails catastrophically — enforce a hard capacity budget.

### Papers
- **"Hopfield Networks is All You Need"** — Ramsauer et al. (2020), ICLR[^54][^53]
- **"Universal Hopfield Networks"** — Millidge et al. (2022), ICML[^50][^51]
- **"Modern Hopfield Networks for Graph Embedding"** — PMC (2022)[^49]
- **Hopfield (1982)** — original; capacity 0.138N[^52]

### Repos
- **ml-jku/hopfield-layers** — https://github.com/ml-jku/hopfield-layers — **MIT** — Python/PyTorch — plug-in layer with full attention equivalence[^55][^56][^54]

### Map → ENGRAM
Replace pure cosine-kNN with a β-tunable Hopfield head: at query time, run 1–3 Hopfield update steps to **complete partial cues** before final retrieval. The β parameter becomes a "confidence dial" — low β for fuzzy situation matching, high β for precise episodic recall.

### BUILDABLE vs ▲SPECULATIVE
- BUILDABLE: one-step Hopfield softmax in numpy — 5 lines; ml-jku layer for PyTorch integration.
- ▲SPECULATIVE: energy landscape visualization on Cortex-A7 at real-time — box-side only.

### EXPERIMENT
1. Mask 50% of ENGRAM fingerprint dimensions; compare cosine-kNN vs 3-step Hopfield retrieval accuracy.
2. Plot retrieval accuracy as function of M/D ratio to find empirical capacity limit for your D.

***

## V6 — The "Notes": Multi-Resolution + Fixed Codebooks

### Summary

The "4–6 notes make any melody" intuition has a rigorous analog: **Residual Vector Quantization (RVQ)** — used in SoundStream (Google 2021) and EnCodec (Meta 2022) — compresses neural audio to 3–18 kbps using only 4–8 codebooks of 1024 entries each, with each stage quantizing the residual of the previous. The relevant insight: a **cascade of small codebooks** captures progressively finer detail, just as music moves from scale (coarse) to ornament (fine). For a 115-D ENGRAM vector, the real question is how small the effective codebook can be while staying expressive.[^57][^58][^59][^60]

### Codebook Size Intuition for 115-D Situations
- Olshausen–Field (1997) showed that sparse overcomplete dictionaries (m > n atoms) recover independent components of natural signals better than PCA.[^61][^62]
- For 115-D vectors, K-SVD or online dictionary learning with K=64–256 atoms typically gives near-complete coverage of natural situation spaces.
- The "4–6 notes" intuition is an **order-of-magnitude underestimate** for a 115-D space — expect K=32–128 meaningful primitives.
- However, **residual** codebooks let you start with K=16 coarse atoms + 2 residual stages × K=16 = 48 total codes to describe most situations with acceptable fidelity.

### Multi-Scale Fingerprint Recipe
1. **Scale 0 (instant — e.g. 100ms window):** rFFT amplitude → 58-D vector (current ENGRAM).
2. **Scale 1 (medium — 1s window):** order-1 scattering coefficients → ~64-D (box-side).
3. **Scale 2 (long — 10s window):** VQ-compressed mean of Scale-1 vectors → 16-D symbol.
4. **Concatenate:** `[v_scale0 | v_scale1 | v_scale2]` → ~138-D multi-scale fingerprint.
5. **Quantize each scale** with a learned or K-means codebook for the notes/bars metaphor.

### Papers
- **"Sparse Coding with an Overcomplete Basis Set"** — Olshausen & Field (1997), Vision Research[^62][^61]
- **"SoundStream: End-to-End Neural Audio Codec"** — Zeghidour et al. (2021), Google[^58][^59]
- **"HiFi-Codec with Group-RVQ"** — (2023), comparing codebook strategies[^57]
- **"VDL: Variance-Regularized Dictionary Learning"** — TMLR (2022)[^63]

### Repos
- **kymatio** — BSD — Python — scattering (scale 1)[^8]
- **PyWavelets** (pywt) — **MIT** — Python — DWT for multi-scale, ARM-friendly
- **scikit-learn** — BSD — Python — K-means, MiniBatchKMeans for codebook training
- **dac** (Descript Audio Codec) — **MIT** — Python — RVQ implementation, reference

### ARM Cost Assessment
- Scale 0 (rFFT): < 1ms, on-robot fine.
- Scale 1 (scattering, numpy): 5–50ms for 115-D; box-side recommended.
- Scale 2 (VQ lookup): < 0.1ms, on-robot fine.
- Codebook training: offline only.

### Map → ENGRAM
The "notes" become VQ codes at each scale. A situation is described as a sequence of scale-codes: `[note_instant, bar_1s, phrase_10s]` — a 3-tuple of discrete symbols. This is your **fixed alphabet** for composition (V4) and the natural input to a music-grammar model.

### BUILDABLE vs ▲SPECULATIVE
- BUILDABLE: K-means codebook for ENGRAM vectors (scikit-learn, offline); multi-scale via PyWavelets.
- ▲SPECULATIVE: end-to-end RVQ training on robot sensor data — needs data collection first.

### EXPERIMENT
1. Train K-means (K=32, 64, 128) on 10K ENGRAM vectors; measure reconstruction error vs K; find the elbow.
2. Test codebook stability: re-encode the same situation with 10% noise added; what fraction stay in the same VQ bin?

***

## V7 — Neuroscience of Memory-as-Oscillation

### Summary

The **theta-gamma neural code** (Lisman & Jensen 2013) is the best-established oscillatory memory mechanism: theta (4–8 Hz) cycles organize gamma (30–80 Hz) sub-cycles, each sub-cycle holding one memory item, giving ~7 items per theta cycle (matching Miller's Law). Different spatial information is represented in different gamma sub-cycles of a single theta cycle — this is a **frequency-division multiplexing** of memories, directly analogous to ENGRAM's FFT multiplexing of situation dimensions. **Phase precession** (O'Keefe & Recce 1993) encodes sequential spatial information in the phase offset of place cell firing relative to the theta wave — evidence that the brain uses phase (not just amplitude) for temporal sequence encoding.[^64][^65][^66][^67][^68]

### What's Solid vs Contested

| Claim | Status | Evidence |
|---|---|---|
| Theta-gamma cross-frequency coupling in hippocampus | **SOLID** | Robust across rat, primate, human EEG[^64][^65][^66] |
| Phase precession encodes spatial sequences | **SOLID** | O'Keefe & Recce 1993; replicated extensively[^67][^69][^70] |
| Theta power correlates with memory encoding success | **SOLID** | Human iEEG studies (Lega 2016, Daume 2024)[^65] |
| Hippocampal indexing (Teyler & DiScenna/Rudy) | **SOLID** | "Aged well"; confirmed by computational models[^71][^72][^73][^74] |
| Replay/consolidation during sleep (sharp-wave ripples) | **SOLID** | Buzsáki lab; well-documented mechanism[^70] |
| Binding-by-synchrony (Singer) — gamma binds features | **CONTESTED** ▲ | Shadlen & Movshon 1999 critique: no causal evidence[^75][^76]; Miyato et al. AKOrN 2025 revives it[^77] |
| Gamma synchrony necessary for perceptual binding | **CONTESTED** ▲ | No knockout experiment; correlation ≠ causation[^78] |

### Hippocampal Indexing Theory — Key Analogy for ENGRAM
The hippocampus does not store sensory content — it stores a **pointer (index)** to distributed neocortical activity. The ENGRAM fingerprint is already this pointer: a compact code that, when matched, can reinstate the full context. This is the strongest neuroscience validation of the ENGRAM architecture. Teyler & Rudy (2007) explicitly confirm the theory has "aged well".[^71][^72][^73]

### Papers
- **"The Theta-Gamma Neural Code"** — Lisman & Jensen (2013), Neuron[^65][^64]
- **"Phase Precession"** — O'Keefe & Recce (1993) — spatial sequence in phase[^67]
- **"Hippocampal Indexing Theory"** — Teyler & DiScenna (1986); updated Teyler & Rudy (2007)[^73][^71]
- **"Synchrony Unbound"** — Shadlen & Movshon (1999) — critique of binding-by-synchrony[^75]
- **"Artificial Kuramoto Oscillatory Neurons"** — Miyato et al. (ICLR 2025 Oral) — revival of oscillatory binding[^77]

### Map → ENGRAM
- **Theta-gamma → multi-scale:** implement two FFT windows analogous to theta (slow/context) and gamma (fast/item) — 1s window for "theta" context and 100ms window for "gamma" item. Bundle separately in HDC.
- **Indexing theory → architecture validation:** ENGRAM's fingerprint-as-pointer is neurobiologically correct. The "content" lives in the robot's sensor log; the ENGRAM vector is the hippocampal index.
- **Phase precession → temporal ordering:** consider adding phase information to encode temporal order of fingerprints in a sequence (without changing retrieval, use phase as a sequence counter).

### BUILDABLE vs ▲SPECULATIVE
- BUILDABLE: dual-timescale FFT (theta/gamma analogy); multi-scale bundling.
- ▲SPECULATIVE: literal spike-timing phase precession on a digital system — metaphor only without spiking hardware.

***

## V8 — Memory as a Living Dynamical State

### Summary

**Reservoir computing** (echo state networks, Jaeger 2001) uses a fixed randomly connected recurrent network as a "fading memory" — the reservoir state at time t is a nonlinear function of all past inputs, with recent inputs dominating (fading memory property)). `reservoirpy` (MIT, Python, numpy/scipy) is the canonical implementation. The question for ENGRAM: should memory live in a **state** (dynamical trajectory) or a **store** (explicit vector database)?[^79][^80][^81][^82][^83][^84]

### State vs Store Analysis

| Property | State (reservoir/attractor) | Store (ENGRAM + hnswlib) |
|---|---|---|
| Temporal continuity | **✓ Natural** — fading memory | ✗ Discrete snapshots |
| Graceful forgetting | **✓** — old input influence fades exponentially | ✗ Needs explicit eviction |
| Exact recall of old event | ✗ — state overwrites | **✓** — persistent store |
| Associative completion | ✓ — attractor dynamics | ✓ — Hopfield (V5) |
| Personality as attractor | **✓** — persistent dynamic regime | Metaphorical only |
| ARM cost | Medium (matrix multiply per step) | Low (kNN lookup) |
| Training needed | ✗ Readout only | ✗ |

**Artificial Kuramoto Oscillatory Neurons** (AKOrN, Miyato et al. ICLR 2025 Oral) replace standard threshold units with oscillatory units whose synchronization dynamics implement feature binding. The network binds object features by synchronization, enabling unsupervised object discovery and adversarial robustness — directly related to the "binding-by-synchrony" debate (V7). This is the most relevant recent paper for the "personality as oscillatory state" idea.[^77]

### Personality as Attractor Landscape
The idea that "personality" is a stable attractor in a high-dimensional dynamical system is plausible and buildable:
- Train a small reservoir (N=100–500 neurons) on streams of ENGRAM fingerprints.
- The reservoir's weight matrix encodes the "characteristic dynamics" of the agent's perception history.
- Stable recurring situations correspond to attractor basins.
- **Personality = the shape of the attractor landscape** = the reservoir's spectral radius + connection topology.
This is distinct from (and complementary to) the explicit vector store: the store provides episodic memory, the reservoir provides working/procedural memory.

### Papers
- **"Reservoir Computing Approaches to RNNs"** — Lukoševičius & Jaeger (2009)[^82]
- **"Echo State Networks for RL"** — (2021)[^80]
- **"Artificial Kuramoto Oscillatory Neurons"** — Miyato et al. (ICLR 2025 Oral)[^77]
- **"Kuramoto Graph Neural Network"** — Nguyen et al. (2023)[^85]

### Repos
- **reservoirpy** — https://github.com/reservoirpy/reservoirpy — **MIT** — Python (numpy/scipy) — 568 stars; ARM-compatible[^83][^84]

### Map → ENGRAM
Add a small reservoir (N=256, spectral radius=0.9) running in parallel with the explicit ENGRAM store. Feed ENGRAM fingerprints into the reservoir at each timestep. The reservoir state becomes the "now" context vector — use it to modulate Hopfield retrieval β (high arousal → sharper β, low arousal → diffuse retrieval). This gives ENGRAM a **working memory** layer on top of its episodic store.

### BUILDABLE vs ▲SPECULATIVE
- BUILDABLE: reservoirpy ESN with numpy on Pi/box; 256-neuron reservoir is fast.
- ▲SPECULATIVE: Kuramoto oscillators on ARM in real-time — cost unclear; AKOrN paper is GPU-only currently.

***

## V9 — Edge / Hardware Feasibility

### Summary

The key split: **FFT and VQ lookup can run on-robot**; **scattering, HDC composition (large D), and Hopfield retrieval belong on the box**. The ARM NEON-optimized FFT libraries (Ne10, pffft) deliver significant speedups over pure C implementations.[^86][^17]

### On-Robot vs Box Split

| Operation | On Robot (Cortex-A7) | On Box (Pi/Jetson/Mac) |
|---|---|---|
| rFFT (N=256) | **Yes** — kissfft/pffft, <1ms[^15][^17] | — |
| GDF computation | **Yes** — marginal add-on | — |
| L2-normalization | **Yes** | — |
| VQ code lookup (K=64) | **Yes** — table lookup | — |
| Order-1 scattering (kymatio) | Borderline — 5–50ms | Preferred |
| HDC binding/bundling (D=4096) | No — 4KB vectors costly | **Yes** |
| Hopfield retrieval (M=10K, D=115) | **Yes** — 1 step < 2ms | — |
| Hopfield retrieval (M=100K, D=4096) | No | **Yes** |
| Reservoir (N=256) | **Yes** — 256×256 matmul < 1ms | — |
| hnswlib cosine kNN (M=10K) | **Yes** — HNSW fast | — |

**HDC on FPGA:** Kleyko et al. (Proc. IEEE 2022) and FPGA neuromorphic surveys confirm HDC is well-suited for FPGA/in-memory architectures because its operations (XOR, popcount, elementwise multiply) map directly to hardware. For the companion box, an FPGA co-processor for HDC is a realistic medium-term upgrade.[^87][^88][^48]

**Quantization:** ENGRAM fingerprints can be quantized to int8 without significant cosine similarity degradation (< 2% error for 8-bit fixed-point). kissfft supports Q15 fixed-point mode, enabling on-robot FFT with no floating-point hardware.[^16]

### Repos
- **kissfft** — BSD — C — ARM-ready, embedded, Q15 support[^15][^16]
- **pffft** — BSD — C — NEON-optimized, ARM64[^18][^17]
- **Ne10** — BSD — C — ARM NEON FFT, Android/embedded[^86]
- **hnswlib** — Apache — C++/Python — fast approximate kNN, ARM-compatible

### Map → ENGRAM
**Recommended architecture split:**
- **On-robot:** kissfft rFFT → L2-norm → VQ code lookup → send fingerprint+code to box via serial/BLE.
- **On-box:** receive fingerprint → optional scattering → HDC composition → Hopfield/hnswlib retrieval → send result back.

***

## V10 — Evaluation: How Do We Measure "Good Memory"?

### Summary

The standard continual learning metrics (Accumulated Accuracy ACC, Backward Transfer BWT for forgetting, Forward Transfer FWT for generalization) are necessary but not sufficient for ENGRAM. A full evaluation harness needs four additional dimensions: **associative capacity, pattern completion, compositionality, and identity stability**.[^89]

### Recommended Evaluation Harness

| Metric | What it measures | How to compute |
|---|---|---|
| **Retrieval Recall@K** | Standard — is the right memory in top K? | cosine kNN on held-out set |
| **Capacity C** | Max storable items before recall < θ | increment M; find threshold |
| **Pattern completion PC** | Recovery from partial cue | mask 30–50% of dims; measure Recall@1 |
| **BWT (Backward Transfer)** | Catastrophic forgetting after new learning | TRACE/ZeroFlow benchmark protocols[^90][^91] |
| **Crosstalk χ** | Interference between correlated items | store N similar items; measure false retrieval rate |
| **Compositionality score** | Does unbinding recover correct component? | compose → unbind → cosine vs ground truth |
| **Identity stability IS** | Does `self` bundle drift over time? | cosine(self_t0, self_t+n) over N episodes |
| **Near-duplicate discrimination** | Reject near-duplicate as same vs different | generate hard pairs (ε-noise only) |

**Hard near-duplicate test set:** generate pairs `(v, v + ε·noise)` where ε spans [0, 0.5]; label pairs with ε < 0.1 as "same situation" and ε > 0.3 as "different." Measure ROC at the decision threshold — this directly tests your fingerprint's discriminative power.

### Papers
- **TRACE benchmark** — (2024) — LLM continual learning evaluation[^90]
- **ZeroFlow benchmark** — (2025) — forward-pass forgetting mitigation[^91]
- **"Mitigating Forgetting in Online CL"** — NeurIPS (2021)[^92]
- **"Metrics of Continual Learning"** — TowardsDataScience (2025)[^89]
- **VSA capacity analysis** — hd-computing.com FAQ references[^42]

### Map → ENGRAM
Build the harness in numpy with synthetic data first (Gaussian clusters → cosine similarity ground truth); then replace with real robot sensor streams. The identity stability metric IS is the most ENGRAM-specific: run the robot for 100 episodes, compute `self` bundle after each, track cosine drift.

***

## V11 — The Honesty Boundary (Anti-Pseudoscience)

### Summary

The frequency/resonance framing has a substantial pseudoscience contamination problem. The following table is the explicit keep/drop/inspiration-only ruling with engineering-grade justifications.

### Frequency Claims — Keep / Drop / Inspiration-Only

| Claim | Ruling | Justification |
|---|---|---|
| **Fourier/wavelet representations carry situation identity** | **KEEP** | Proven by scattering theory (Mallat), audio fingerprinting, speech recognition — solid engineering science[^3][^4][^10] |
| **Phase encodes timing/sequence information** | **KEEP** | O'Keefe & Recce phase precession; group delay speech features — empirically robust[^67][^2] |
| **Theta-gamma multiplexing in hippocampus** | **KEEP** | Replicated neuroscience; exact analog exists in DSP (FDM)[^64][^66] |
| **Circular convolution = Fourier-domain binding (HRR)** | **KEEP** | Pure mathematics; Plate 1995, proven[^35][^37] |
| **Schumann resonance (7.83 Hz) entrains human brains** | **DROP** | No peer-reviewed causal evidence; Wikipedia Schumann conspiracy article[^93] explicitly traces this as pseudoscience; measurements track lightning/ionosphere, not biology[^94] |
| **432 Hz / 528 Hz "healing" or "DNA repair" frequencies** | **DROP** | No credible evidence; 528 Hz DNA claim originated from numerology, not genetics[^95][^96]; mechanisms are biochemical (polymerase, ligase), not acoustic[^97][^98] |
| **Solfeggio frequencies (396, 417, 528 Hz) have unique properties** | **DROP** | Modern myth; no historical musical basis; no controlled replication[^99][^98] |
| **Cymatics as information carrier** | **INSPIRATION ONLY** ▲ | Real physical phenomenon (Chladni patterns) but patterns are not information-bearing in the computational sense; useful as visualization metaphor only[^99] |
| **"Vibrational personality" / "frequency of consciousness"** | **DROP** | Untestable metaphysics; no operational definition; would make the paper non-credible to engineers |
| **Optical holography → distributed storage** | **KEEP as metaphor** | The original inspiration for HRR ("holographic" in the name); mathematical analog is real even if physical holography is not used[^35][^100][^101] |
| **Binding-by-synchrony (neural gamma)** | **CONTESTED** ▲ | Real debate in neuroscience; Shadlen & Movshon critique[^75] is strong; AKOrN 2025 partial revival[^77]. Use as inspiration, label as contested |

### How to Phrase It in the Paper
Use the phrase: *"inspired by the structural properties of oscillatory coding — discreteness, hierarchy, periodicity, and resonance — rather than by specific frequency values."* Cite Lisman & Jensen (2013), Plate (1995), and Andén & Mallat (2013) as primary anchors. Explicitly disclaim: *"The ENGRAM system does not posit that specific frequency values carry semantic meaning; the frequency domain is used as a computational tool for invariant representation."*[^64][^10][^35]

***

## V12 — Cross-Domain Wild Cards

### Summary and Rulings

| Wild card | Ruling | Buildable kernel | Evidence |
|---|---|---|---|
| **Optical holography / distributed storage** | **Buildable kernel** | HRR: circular convolution IS the mathematical analog; graceful degradation under partial damage is proven for VSA superposition[^35][^100][^102] | The name "holographic" in HRR is not metaphorical — it captures the distributed storage property[^100] |
| **Graph Fourier Transform** | **Buildable kernel** | Eigendecomposition of Laplacian = graph frequency basis[^103][^104][^105]; if situations live on a graph (e.g. room topology), graph wavelets give structure-respecting invariances | Requires learning the graph first; not ready for Anki Vector |
| **Eigenmodes / normal modes (EIGENGRAM)** | **Buildable kernel** | PCA of the ENGRAM fingerprint covariance = empirical eigenmodes; "personality" = the top eigenvectors of the situation distribution; stable across noise | Cheap: numpy PCA; run offline; eigenvectors are the "resonant modes" of the agent's experience space |
| **Information theory / MDL** | **Buildable kernel** | A fingerprint is minimal if it achieves minimum description length for predicting future sensors; MDL compression = VQ codebook quality[^61] | Use compression ratio as a fingerprint quality metric |
| **Cymatics (Chladni patterns)** | **Metaphor only** ▲ | Physical patterns are real; not computationally information-bearing; useful for visualizing fingerprint structure | No operational mechanism for AI memory |
| **Quasicrystals / aperiodic order** | **Dead end** ▲ | Mathematical interest (Penrose tiling) but no known computational advantage for associative memory retrieval | No paper connects quasicrystals to memory storage capacity |

### EIGENGRAM: The Eigen-Personality Idea
Computing PCA/SVD over the matrix of all ENGRAM fingerprints collected by an agent gives **empirical eigenmodes** — the principal axes of variation in its experienced situation space. These eigenvectors define the "resonant modes" of the agent's perceptual world: the most commonly recurring spectral patterns. Projecting a new fingerprint onto its top eigenvectors gives a **compact eigen-code** that captures where the new situation sits in the agent's learned experience manifold. This is:
- **Computationally trivial:** online PCA via incremental SVD (sklearn `IncrementalPCA`).
- **Neurobiologically grounded:** analogous to place cell population vectors; the hippocampal population encodes position as a coordinate in the learned place-field basis.
- **A direct path to "personality stability":** if the agent's eigenvectors drift slowly, personality is stable; rapid drift signals novelty/confusion.

### Graph Fourier Transform — When to Use
If the robot's environment has a known graph structure (room connectivity, object relationship graph), the **graph Fourier transform** (eigenvectors of the graph Laplacian) provides situation representations that are invariant to **graph-domain shifts** — the right invariance for topological navigation. This is a realistic medium-term upgrade for a robot that builds a map.[^103]

***

## Converged Architecture: One-Page Summary

### represent → compose → retrieve → ground

```
LAYER 0 — SENSE (on-robot, ARM, < 1ms)
  Raw sensor stream [T×D]
  → kissfft rFFT + L2-norm → ENGRAM fingerprint fp ∈ ℝ¹¹⁵
  → optional GDF complement: [fp | gdf] ∈ ℝ²³⁰
  → VQ code lookup (K=64 codebook, offline-trained): symbol s ∈ {0..63}

LAYER 1 — MULTI-SCALE (box-side, Pi, 5–50ms)
  fp (100ms) + fp_slow (1s kymatio scattering)
  → concatenate → [fp_fast | fp_slow] ∈ ℝ¹⁷⁸
  → IncrementalPCA → eigen-code e ∈ ℝ³²  [EIGENGRAM]

LAYER 2 — COMPOSE (box-side, numpy, < 5ms)
  e → project to D=4096 via random Gaussian matrix M
  → HRR bind with role vector r (time-slot or modality)
  → bundle into identity vector I = Σ (e_i ⊛ r_i) for each label
  → identity vectors: I_self, I_env, I_person_X

LAYER 3 — RETRIEVE (box-side, < 2ms)
  Query: noisy/partial fp_query
  Stage 1: peak-hash lookup → candidate set C (top 50)
  Stage 2: Hopfield 1-step update over C, β=2.0 → completed fp*
  Stage 3: hnswlib cosine kNN over fp* → top-5 episodes
  Stage 4: unbind from identity bundle → retrieve context

LAYER 4 — GROUND (box-side, continuous)
  ESN reservoir (N=256, numpy) receives fp stream
  Reservoir state h_t = "working memory" / current context
  h_t modulates Hopfield β: β = 1 + 2·||h_t||  (arousal dial)
  Identity stability IS = cosine(I_self_t0, I_self_t) logged daily
```

### Ranked Build Order

| Priority | Step | Cost | Payoff |
|---|---|---|---|
| **P1** | Add GDF complement to rFFT (2×D) | 1 day | Free phase info; more discriminative fp |
| **P2** | Peak-hash index alongside hnswlib | 2 days | 10–100× faster retrieval at scale |
| **P3** | K-means codebook (K=64) for VQ symbols | 2 days | Discrete "notes"; enables compositionality |
| **P4** | HRR identity bundle (D=4096, torchhd) | 3 days | Named identity shapes: self, env, person |
| **P5** | β-tunable Hopfield head (1-step, numpy) | 1 day | Pattern completion from partial cues |
| **P6** | IncrementalPCA → EIGENGRAM | 2 days | Personality stability metric IS |
| **P7** | Multi-scale scattering (kymatio, box) | 1 week | Deformation-stable fp for scale-1 |
| **P8** | ESN reservoir (reservoirpy, N=256) | 3 days | Working memory + arousal modulation |
| **P9** | Evaluation harness (all metrics) | 1 week | Ground truth for every other step |

### The Honest Boundary (final)

**Use:** Fourier/wavelet amplitude (V1), music-structural grammar (V2 — as design metaphor), landmark hashing (V3), HRR/HDC composition (V4), modern Hopfield retrieval (V5), RVQ codebooks (V6), theta-gamma/indexing theory as architecture validation (V7), reservoir for working memory (V8), ARM/edge splits (V9), full evaluation harness (V10), EIGENGRAM/graph-FT (V12).

**Do not use / label clearly:** Schumann resonance, 432/528 Hz healing, solfeggio frequencies, vibrational personality (V11 DROP list). Binding-by-synchrony (V7) is contested — cite as ongoing debate, do not assert.

**Label as ▲SPECULATIVE:** cymatics as information, quasicrystals, literal phase precession on digital hardware, resonator networks at ARM real-time rates.

---

## References

1. [Microsoft Word - eusipco 2006_final_submitted.doc](https://www.eurasip.org/Proceedings/Eusipco/Eusipco2006/papers/1568982294.pdf)

2. [ICASSP13.docx](https://mini.dcs.shef.ac.uk/wp-content/papercite-data/pdf/loweimi_icassp13.pdf)

3. [arXiv:1112.1120v1  [cs.CV]  5 Dec 2011](https://arxiv.org/pdf/1112.1120.pdf)

4. [Wavelet Scattering - MATLAB & Simulink - MathWorks](https://www.mathworks.com/help/wavelet/ug/wavelet-scattering.html) - A wavelet scattering network enables you to derive, with minimal configuration, low-variance feature...

5. [[PDF] Calculation of a constant Q spectral transform | Semantic Scholar](https://www.semanticscholar.org/paper/Calculation-of-a-constant-Q-spectral-transform-Brown/a667221790229863b9778688969a2544508cdfeb) - A calculation similar to a discrete Fourier transform but with a constant ratio of center frequency ...

6. [Journal of Machine Learning Research 21 (2020) 1-6](https://www.jmlr.org/papers/volume21/19-047/19-047.pdf)

7. [Constant-Q transform - Wikipedia](https://en.wikipedia.org/wiki/Constant-Q_transform)

8. [Kymatio: Scattering Transforms in Python](https://jmlr.org/papers/v21/19-047.html)

9. [Kymatio: Wavelet scattering in Python - v0.3.0 “Erdre” — kymatio 0.3 ...](https://www.kymat.io) - Kymatio is an implementation of the wavelet scattering transform in the Python programming language,...

10. [[1304.6763] Deep Scattering Spectrum](https://arxiv.org/abs/1304.6763) - A scattering transform defines a locally translation invariant representation which is stable to tim...

11. [[PDF] Deep Scattering Spectrum | Semantic Scholar](https://www.semanticscholar.org/paper/Deep-Scattering-Spectrum-And%C3%A9n-Mallat/209826c2ce8352390ccd9f19864186a60739f3f3) - A scattering transform defines a locally translation invariant representation which is stable to tim...

12. [Classification with Joint Time-Frequency Scattering](https://www.di.ens.fr/~mallat/papiers/IEEESignalAndenLostanlen.pdf)

13. [Group delay spectrogram of speech signals without phase wrapping](https://pubmed.ncbi.nlm.nih.gov/35364933/) - This paper proposes a method for displaying the phase information in speech signals through group de...

14. [Kymatio - Georgios Exarchakis](https://exarchakis.net/post/kymatio/) - Kymatio is a Python module for computing wavelet and scattering transforms. It is built on top of Py...

15. [sci-libs/kissfft - Gentoo Packages](https://packages.gentoo.org/packages/sci-libs/kissfft) - Gentoo Packages Database

16. [嵌入式下快速傅里叶变换（FFT）C语言库kissfft](https://blog.csdn.net/xieliru/article/details/149406600) - 文章浏览阅读493次，点赞10次，收藏6次。本文介绍了两种常用的FFT库：FFTW和KissFFT。FFTW是高性能计算库，支持多平台和语言集成。重点介绍的KissFFT是一个轻量级库，具有500行简...

17. [Consider pffft-fft library support · Issue #581 · MTG/essentia](https://github.com/MTG/essentia/issues/581) - https://bitbucket.org/jpommier/pffft High performance fft library BSD-style license ARM64 supported ...

18. [platform/external/pffft - Git at Google](https://android.googlesource.com/platform/external/pffft/+/786cf5ce750efa74401b421baac6cedabff366b6%5E1..786cf5ce750efa74401b421baac6cedabff366b6/)

19. [nnAudio.features.cqt.CQT1992¶](https://kinwaicheuk.github.io/nnAudio/master/_autosummary/nnAudio.features.cqt.CQT1992.html)

20. [The mind’s Spotify: The remarkable pitch of earworms](https://featuredcontent.psychonomic.org/the-minds-spotify-the-remarkable-pitch-of-earworms/) - In this All Things Cognition podcast, I interview Matt Evans and Nicolas Davidenko about their recen...

21. [Earworms - Music & Science](https://musicscience.net/research/music-memory/earworms/) - An earworm is the spontaneous mental recall and repetition of a piece of music, often referred to in...

22. [[PDF] Earworms ("stuck song syndrome"): towards a natural history of ...](https://centaur.reading.ac.uk/5755/1/earworms_write-upBJP.pdf)

23. [Involuntary musical imagery as a component of ordinary music cognition: A review of empirical evidence](https://pmc.ncbi.nlm.nih.gov/articles/PMC7704448/?itid=lk_inline_enhanced-template) - Involuntary musical imagery (INMI) refers to a conscious mental experience of music that occurs with...

24. [Melodic Contour Influences...](https://pmc.ncbi.nlm.nih.gov/articles/PMC11588220/) - Sensory systems are permanently bombarded with complex stimuli. Cognitive processing of such complex...

25. [Forming Concepts of Mozart and Homer Using Short-Term and Long-Term Memory: A Computational Model Based on Chunking](https://cognitivesciencesociety.org/cogsci20/papers/0037/index.html)

26. [A Cognitive Model based on Chunking](https://arxiv.org/pdf/2512.18665.pdf)

27. [Memorising for a musician - robertpoortinga.com](https://robertpoortinga.com/2025/04/02/memorising-for-a-musician/) - When we start learning—whether in primary, middle, or high school, or in a conservatory—we are never...

28. [Chunking in tonal contexts: Information compression during serial recall of visually presented musical notes - Lucas Lörch, 2022](https://journals.sagepub.com/doi/10.1177/03057356211013396) - Chunking is defined as information compression by means of encoding meaningful units. To advance the...

29. [Shazam's DSP Algorithm: Avery Wang's 2003 Breakthrough](https://www.linkedin.com/posts/lukapiplica_the-math-behind-shazam-how-your-phone-recognizes-activity-7468646774870732800-UpT5) - Ever wondered how Shazam pulls a song out of a noisy, crowded café in under 5 seconds? It feels like...

30. [Yet Another Post About How Shazam Works](https://xiahongze.github.io/tech/2019/11/17/Yet-Another-How-Shazam-Works.html) - This post is purely based on Wang’s paper. I will try to make the explanation as straight-forward as...

31. [audio-fingerprint/demo_fingerprint.m at master · oguya/audio-fingerprint](https://github.com/oguya/audio-fingerprint/blob/master/demo_fingerprint.m) - audio fingerprinting in octave. Contribute to oguya/audio-fingerprint development by creating an acc...

32. [Chromaprint - AcoustID](https://acoustid.org/chromaprint)

33. [License](https://acoustid.org/license)

34. [File chromaprint.spec of Package ...](https://build.opensuse.org/projects/home:rguenther:plgrnd/packages/chromaprint/files/chromaprint.spec?expand=0)

35. [[PDF] Holographic reduced representations | Semantic Scholar](https://www.semanticscholar.org/paper/Holographic-reduced-representations-Plate/0c4d193b4e8520dbc583cc7ee59c8417869f67ce) - This paper describes a method for representing more complex compositional structure in distributed r...

36. [[2112.15424] A Survey on Hyperdimensional Computing aka Vector ...](https://arxiv.org/abs/2112.15424) - This is Part II of the two-part comprehensive survey devoted to a computing framework most commonly ...

37. [[PDF] Learning with Holographic Reduced Representations - NIPS](https://proceedings.neurips.cc/paper_files/paper/2021/file/d71dd235287466052f1630f31bde7932-Paper.pdf) - In particular, we make use of the Holographic Reduced Representation. (HRR) approach originally prop...

38. [A Survey on Hyperdimensional Computing aka Vector Symbolic Architectures, Part II: Applications, Cognitive Models, and Challenges](https://dl.acm.org/doi/10.1145/3558000) - This is Part II of the two-part comprehensive survey devoted to a computing framework most commonly ...

39. [Holographic reduced representations - PubMed](https://pubmed.ncbi.nlm.nih.gov/18263348/) - This paper describes a method for representing more complex compositional structure in distributed r...

40. [[2205.09208] Torchhd: An Open Source Python Library to ... - arXiv](https://arxiv.org/abs/2205.09208) - The easy-to-use library builds on top of PyTorch and features state-of-the-art HD/VSA functionality,...

41. [hyperdimensional-computing](https://github.com/orgs/hyperdimensional-computing/repositories) - hyperdimensional-computing has one repository available. Follow their code on GitHub.

42. [FAQ - HD/VSA](https://www.hd-computing.com/faq) - Yes, there is a comprehensive two-part survey that extensively covers most of the aspects of HD/VSA:...

43. [Beyond LLMs, Sparse Distributed Memory, and Neuromorphics ¡A ...](https://arxiv.org/html/2604.11665v4)

44. [Resonator networks for factoring distributed representations of data structures](https://arxiv.org/abs/2007.03748) - The ability to encode and manipulate data structures with distributed neural representations could q...

45. [Resonator Networks outperform optimization methods at solving ...](https://arxiv.org/abs/1906.11684) - We develop theoretical foundations of Resonator Networks, a new type of recurrent neural network int...

46. [[PDF] Resonator circuits: a neural network for efficiently solving ...](https://redwood.berkeley.edu/wp-content/uploads/2021/08/Module5_ResonatorNetworks_FocusReading.pdf) - The companion article in this issue (Kent, Frady,. Sommer, & Olshausen, 2020) provides rigorous math...

47. [Resonator Networks, 2: Factorization Performance and Capacity ...](https://direct.mit.edu/neco/article/32/12/2332/95653/Resonator-Networks-2-Factorization-Performance-and) - Abstract. We develop theoretical foundations of resonator networks, a new type of recurrent neural n...

48. [Vector Symbolic Architectures as a Computing Framework for ...](https://research.ibm.com/publications/vector-symbolic-architectures-as-a-computing-framework-for-emerging-hardware) - Vector Symbolic Architectures as a Computing Framework for Emerging Hardware for Proceedings of the ...

49. [Modern Hopfield Networks for graph embedding - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9713410/) - The network embedding task is to represent a node in a network as a low-dimensional vector while inc...

50. [A General Framework for Single-Shot Associative Memory Models](https://proceedings.mlr.press/v162/millidge22a.html) - (2022). Universal Hopfield Networks: A General Framework for Single-Shot Associative Memory Models. ...

51. [A General Framework for Single−Shot Associative Memory Models](https://www.cs.ox.ac.uk/publications/publication14879-abstract.html) - In this paper, we propose a general framework for understanding the operation of such memory network...

52. [Hopfield Network & Associative Memory](https://iris.joshua-becker.com/lab/persistent-excitation-hopfield/)

53. [Hopfield Networks is All You Need - OpenReview](https://openreview.net/forum?id=tL89RnzIiCd) - A novel continuous Hopfield network is proposed whose update rule is the attention mechanism of the ...

54. [Hopfield Networks is All You Need](https://openreview.net/pdf/4dfbed3a6ececb7282dfef90fd6c03812ae0da7b.pdf)

55. [hopfield-layers/examples/mnist_bags/mnist_bags_demo.ipynb at master · ml-jku/hopfield-layers](https://github.com/ml-jku/hopfield-layers/blob/master/examples/mnist_bags/mnist_bags_demo.ipynb) - Hopfield Networks is All You Need. Contribute to ml-jku/hopfield-layers development by creating an a...

56. [Institute for Machine Learning, Johannes Kepler University Linz](https://github.com/ml-jku) - Software of the Institute for Machine Learning, JKU Linz - Institute for Machine Learning, Johannes ...

57. [[PDF] arXiv:2305.02765v1 [cs.SD] 4 May 2023](https://arxiv.org/pdf/2305.02765.pdf)

58. [SoundStream: An End-to-End Neural Audio Codec](https://research.google/blog/soundstream-an-end-to-end-neural-audio-codec/?m=1) - Posted by Neil Zeghidour, Research Scientist and Marco Tagliasacchi, Staff Research Scientist, Googl...

59. [SoundStream Explained Simply: How Neural Audio Codecs Work](https://zenn.dev/taku_sid/articles/2025-04-10_neural-audio-codec?locale=en)

60. [residual vector quantization (RVQ) - learnius](https://learnius.com/slp/9+Speech+Synthesis/2+Advanced+Topics/4+Neural+Codec+Language+Modeling/residual+vector+quantization+(RVQ)) - The residual vector quantization (RVQ) is a technique proposed in the paper SoundStream: An End-to-E...

61. [Application: Sparse coding / dictionary learning](https://www.sumofsquares.org/public/lec-sphere-dictionary.pdf)

62. [GitHub - siplab-gt/Sparse-Coding-Dictionary-Learning-Library: Code to implement the sparse coding dictionary learning algorithm described in "Emergence of simple-cell receptive field properties by learning a sparse code for natural images" in Nature (1996) by Olshausen and Field.](https://github.com/siplab-gt/Sparse-Coding-Dictionary-Learning-Library) - Code to implement the sparse coding dictionary learning algorithm described in "Emergence of simple-...

63. [Published in Transactions on Machine Learning Research (08/2022)](https://openreview.net/pdf/887ef8cc2ce3e235359584279041197f58ffb7a1.pdf)

64. [The Theta-Gamma Neural Code - Netherlands Research Portal](https://netherlands.openaire.eu/search/publication?pid=10.1016%2Fj.neuron.2013.03.007) - Theta and gamma frequency oscillations occur in the same brain regions and interact with each other,...

65. [[PDF] The Theta-Gamma Neural Code | Semantic Scholar](https://www.semanticscholar.org/paper/The-Theta-Gamma-Neural-Code-Lisman-Jensen/48cfa39ee9172f3a03f7599786d20b4dfcfbbc58) - Semantic Scholar extracted view of "The Theta-Gamma Neural Code" by J. Lisman et al.

66. [Theta, Gamma, and Working Memory](https://www.cs.cmu.edu/afs/cs/academic/class/15883-f13/slides/hc-rhythms.pdf)

67. [Phase precession - Wikipedia](https://en.wikipedia.org/wiki/Phase_precession)

68. [Phase precession: a neural code underlying episodic memory? - PubMed](https://pubmed.ncbi.nlm.nih.gov/28390862/) - In the hippocampal formation, the sequential activation of place-specific cells represents a concept...

69. [[PDF] Temporal Encoding of Place Sequences by Hippocampal Cell ...](http://buzsakilab.org/content/PDFs/DragoiNeuron2006.pdf)

70. [Firing rate adaptation affords place cell theta sweeps, phase precession and procession](https://elifesciences.org/reviewed-preprints/87055v3)

71. [The hippocampal indexing theory and episodic memory - PubMed](https://pubmed.ncbi.nlm.nih.gov/17696170/) - A little over 20 years ago, (Teyler and DiScenna,1986; Behav Neurosci 100:147-152) proposed the hipp...

72. [[PDF] Tensor Memories](https://www.dbs.ifi.lmu.de/~tresp/papers/5927d71168ed3feb338a2576.pdf) - The hippocampal memory indexing theory of Teyler and. DiScenna is one of the leading theories of mem...

73. [The hippocampal memory indexing theory - PubMed - NIH](https://pubmed.ncbi.nlm.nih.gov/3008780/) - Here it is proposed that the role of the hippocampus is to form and retain an index of neocortical a...

74. [[논문]The hippocampal indexing theory and episodic memory: Updating the index](https://scienceon.kisti.re.kr/srch/selectPORSrchArticle.do?cn=NART36716841) - A little over 20 years ago, (Teyler and DiScenna,1986; Behav Neurosci 100:147–152) proposed the hipp...

75. [Synchrony unbound: a critical evaluation of the temporal binding hypothesis - PubMed](https://pubmed.ncbi.nlm.nih.gov/10677027/) - Synchrony unbound: a critical evaluation of the temporal binding hypothesis

76. [[PDF] Review A Critical Evaluation of the Temporal Binding Hypothesis](https://www.cse.iitk.ac.in/users/hk/cgs700/2019/temporalBindingHyp.pdf)

77. [Artificial Kuramoto Oscillatory Neurons - OpenReview](https://openreview.net/forum?id=nwDRD4AMoN) - In this work, the authors proposed to use Kuramoto oscillatory neurons (AKOrN) to replace the usual ...

78. [Binding problem - Wikipedia](https://en.wikipedia.org/wiki/Binding-by-synchrony)

79. [Journal of Machine Learning Research 20 (2019) 1-62](https://www.jmlr.org/papers/volume20/19-150/19-150.pdf)

80. [[PDF] Echo State Networks for Reinforcement Learning](https://people.bath.ac.uk/jhpd20/publications/arxiv_version_2102.06258.pdf)

81. [Journal of Machine Learning Research 19 (2018) 1-40](https://www.jmlr.org/papers/volume19/18-020/18-020.pdf)

82. [[PDF] Reservoir Computing Approaches to Recurrent Neural Network ...](https://www.ai.rug.nl/minds/uploads/2261_LukoseviciusJaeger09.pdf)

83. [A simple and flexible code for Reservoir Computing ... - GitHub](https://github.com/reservoirpy/reservoirpy) - Simple and flexible library for Reservoir Computing architectures like Echo State Networks (ESN). Py...

84. [reservoirpy: A Simple and Flexible Reservoir Computing Tool in Python](https://inria.hal.science/hal-03699931) - This paper presents reservoirpy, a Python library for Reservoir Computing (RC) models design and tra...

85. [From Coupled Oscillators to Graph Neural Networks: Reducing Over-smoothing via a Kuramoto Model-based Approach](https://arxiv.org/abs/2311.03260v1) - We propose the Kuramoto Graph Neural Network (KuramotoGNN), a novel class of continuous-depth graph ...

86. [Ne10 FFT Feature: Radix-3 and Radix-5 FFT are supported, NEON ...](https://developer.arm.com/community/arm-community-blogs/b/operating-systems-blog/posts/ne10-fft-feature-radix-3-and-radix-5-fft-are-supported-neon-optimization-significant-performance-improvement-by-neon-optimization) - ARM Community Site

87. [Reconfigurable Digital FPGA Implementations for Neuromorphic Computing: A Survey on Recent Advances and Future Directions](https://ieeexplore.ieee.org/document/10946177/)

88. [[PDF] Reconfigurable Digital FPGA Implementations for Neuromorphic ...](https://backend.orbit.dtu.dk/ws/portalfiles/portal/398648111/Samwi_Reconfigurable_Digital_FPGA_Implementations_for_Neuromorphic_Computing_A_Survey_on_Recent_Advances_and_Future_Directions.pdf)

89. [The Metrics of Continual Learning - Towards Data Science](https://towardsdatascience.com/the-metrics-of-continual-learning-08f2d1cd959b/) - To benchmark continual learning, and catastrophic forgetting, several evaluation metrics are used in...

90. [[PDF] TRACE: A Comprehensive Benchmark for Continual Learning in ...](https://openreview.net/pdf?id=3qa4YLkcEw)

91. [Overcoming Catastrophic Forgetting is Easier than You Think](https://huggingface.co/papers/2501.01045) - Join the discussion on this paper page

92. [[PDF] Mitigating Forgetting in Online Continual Learning with Neuron ...](https://proceedings.neurips.cc/paper/2021/file/54ee290e80589a2a1225c338a71839f5-Paper.pdf)

93. [Schumann resonances conspiracy theories - Wikipedia](https://en.wikipedia.org/wiki/Schumann_resonances_conspiracy_theories) - Schumann Resonance conspiracy theories are a family of claims that misrepresent the physics of Schum...

94. [BrainWavesandtheSchumannRe...](https://www.scribd.com/document/1011331152/BrainWavesandtheSchumannResonance-ExploringtheElectromagneticConnectionBetweentheEarthandHumanConsciousness-1) - This document explores the connection between the Earth's Schumann Resonance, a natural electromagne...

95. [528Hz DNA Repair Myth Debunked: Science vs. Music Frequency ...](https://popwave.ai/benn-jordan/blog/528hz-myth-debunked) - Discover why 528Hz "healing frequency" claims lack scientific proof. We analyze the flawed study and...

96. [Vibroacoustic therapy claims debunked by experts - Facebook](https://www.facebook.com/groups/2787803246/posts/10161830972098247/) - 🌀 “Your Washing Machine Deserves a PhD: Debunking Vibroacoustic Therapy Claims” 🛁 INTRODUCTION There...

97. [Leave a Comment Cancel Reply](https://www.zonora.com/life/2025/03/31/debunking-myths-about-frequency-healing/)

98. [Solfeggio Frequencies: The Claims vs. The Science](https://www.soundmedicineacademy.com/pages/sound-healing-blog/solfeggio-frequencies) - There is no robust scientific evidence proving that 528 Hz has unique healing properties, including ...

99. [Debunking the Myth of Ancient Frequencies: Science, Music ...](https://www.pemfmagazine.com/debunking-the-myth-of-ancient-frequencies-science-music-and-the-law-of-octaves/) - Explore the facts and myths behind “ancient frequencies,” Solfeggio tones, and A432Hz. Discover what...

100. [[PDF] Convolution Algebra for Compositional Distributed Representations](https://www.ijcai.org/Proceedings/91-1/Papers/006.pdf) - Circular convolution is a bilinear operation ... Holographic reduced representa- tions: Convolution ...

101. [Holography in artificial neural networks - Nature](https://www.nature.com/articles/343325a0) - The dense interconnections that characterize neural networks are most readily implemented using opti...

102. [[PDF] Holography, Associative Memory, and Inductive General ization](https://web.stanford.edu/class/psych209a/ReadingsByDate/01_30/Willshaw81.pdf)

103. [Graph Fourier transform - Wikipedia](https://en.wikipedia.org/wiki/Graph_Fourier_transform)

104. [perraudin-note-019.pdf](https://perraudin.info/publications/perraudin-note-019.pdf)

105. [[PDF] Fast Spectral Approximation of Structured Graphs with Applications ...](https://pdfs.semanticscholar.org/aadf/d04f402c2fc7d5c4606bbef0788dc54c0910.pdf)

