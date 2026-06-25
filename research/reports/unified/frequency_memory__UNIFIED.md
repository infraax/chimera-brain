# UNIFIED — AI Memory as Frequency & Symphony
## Evolving ENGRAM toward music-grammar representation, identity composition, resonance retrieval
### Source geodesic: `research/FREQUENCY_MEMORY_RESEARCH_GEODESIC.md` (companion to `MUSIC_AND_FREQUENCY_CONCEPTS.md`, `SOLVING_AI_MEMORY_WITH_FREQUENCY_AND_SYMPHONY.md`)

> **Fusion of the two independent research runs**, nothing dropped:
> - **[C12] = Claude Opus 4.8** — file `08_frequency_memory__symphony.md` ("AI Memory as Frequency &
>   Symphony — a Full 12-Vector Report"). 12 vectors (V1–V12) + converged architecture + ranked build
>   order + numpy pseudocode; **105 numbered references** (`[C^n]`).
> - **[RM] = Research Map** — file `07_frequency_memory__research_map.md` ("Frequency, Music & Memory:
>   Research Map"). Four-pillar framing (Represent / Compose / Retrieve / Ground) + license-checked repo
>   tables + 6-experiment plan + ENGRAM-v2 blueprint; **46 numbered references** (`[RM^n]`).
>   *Attribution note:* unlike the OSS/sensor/physical Perplexity files, this one carries **no explicit
>   model tag** — it is the companion literature-map run (the second pass in the project's pairing
>   pattern). Treated as the [RM] counterpart to the explicitly-Claude [C12] report.
>
> Tags: **[Both]** · **[C12-only]** / **[RM-only]** · **⚖️ DIVERGENCE**.

---

## 0. HEADLINE: the most convergent pair of all four — agreement is the finding

Unlike the other three geodesics (which had real adopt-vs-skip splits), **the two frequency runs
independently arrive at the same architecture, the same four pillars, the same library picks, and the
same anti-pseudoscience boundary.** There are **no contradictions** — only a scope difference: [C12]
is broader and more engineering-ready (adds fast-hash retrieval, an edge/box split, an evaluation
harness, and two novel ideas — EIGENGRAM and Graph-FT); [RM] is the cleaner conceptual map with the
strictest license vetting and a dependency-ordered experiment plan.

### The shared architecture (both, verbatim-equivalent): `represent → compose → retrieve → ground`
```
REPRESENT  multi-scale, deformation-stable spectral features over a FIXED codebook
           (scattering/wavelets = "bars" · VQ dictionary = "the notes" · keep phase as index)
COMPOSE    VSA/HRR: bind (circular convolution = Fourier-domain multiply) + bundle under LABELS,
           hierarchically (notes → motifs → themes → self) = "system prompt as a self-frequency"
RETRIEVE   Modern Hopfield = attention = strict generalization of cosine-kNN
           (tunable β sharpness, multi-step pattern completion); resonator nets decompose motifs
GROUND     real neuroscience (theta-gamma multiplexing, hippocampal indexing, phase-as-index);
           Schumann / 432-528 Hz / solfeggio mysticism dropped entirely
```

### What both independently conclude (high confidence)
- **The core thesis holds:** memory + personality *can* be represented, composed, stored, and retrieved
  as a frequency-domain structure organized by music's grammar — grounded in four mature traditions:
  **wavelet/scattering** (invariant fingerprints), **VSA/HRR** (proven binding algebra), **Modern
  Hopfield** (= attention; cosine-kNN is its β→∞ special case), and **theta-gamma neural coding**
  (the brain genuinely frequency-multiplexes memory). The "music grammar" metaphor is *structurally*
  real, not merely poetic.
- **Current ENGRAM is already a limiting case:** `|rFFT|` amplitude + cosine-kNN = the β→∞ corner of
  a much larger resonance framework. All upgrades build *on top of* it, not against it.
- **The "notes" = a fixed VQ codebook** (frozen offline); the "grammar" = timing/repetition/rests +
  multi-scale "bars" (wavelet scattering levels); the "leitmotif" = a labeled identity vector.
- **Composition is the missing layer:** today fingerprints exist in isolation. HRR binding+bundling
  under labels creates `I_self`, `I_env`, `I_person_X` — the user's "system-prompt-as-shape" idea,
  mathematically realized (binding = a single Fourier-domain elementwise multiply, which ENGRAM's rFFT
  pipeline already lives in).
- **⚠ The load-bearing caveat (both):** ENGRAM fingerprints are **L2-normalized amplitude spectra, not
  random vectors** — VSA capacity theory assumes near-orthogonality, so capacity degrades on correlated
  items. **Both prescribe the same fix:** random role-key projection + project to higher D (~4096) +
  cleanup memory; **must be empirically measured before adopting identity composition.**
- **Retrieval upgrade is nearly free:** swap the separation function — `softmax(β·qKᵀ)·V` over the same
  store — giving a tunable "sharpness of resonance" knob and multi-step pattern completion from partial
  cues (which one-shot kNN cannot do). Zero new storage.
- **Phase carries information** (both): O'Keefe–Recce phase precession + group-delay speech features
  show phase encodes timing/sequence. Both say keep it as an index (don't discard it).
- **Pseudoscience boundary (identical):** ❌ DROP Schumann 7.83 Hz entrainment, 432/528 Hz "healing",
  solfeggio frequencies, "vibrational personality"; ⚠ binding-by-synchrony = real but contested (cite
  the debate, don't assert); ✅ KEEP the DSP/VSA/neuroscience that is actually proven.

### Library picks both converge on (all permissive)
**kymatio** (scattering, BSD) · **PyWavelets** (MIT) · **torchhd** (VSA/FHRR, MIT) · **hdlib**
(numpy-only VSA, ARM-friendly, MIT) · **ml-jku/hopfield-layers** (BSD) · **reservoirpy** (ESN, MIT) ·
**scikit-learn** (K-means codebook, BSD) · **EnCodec / DAC** (RVQ reference, MIT) · **kissfft / pffft**
(ARM FFT, BSD). [RM] adds the explicit **AVOID list**: Essentia/Panako (AGPL), aubio (GPL),
Chromaprint-via-FFmpeg (LGPL), SPAMS (GPL).

### ⚖️ Differences (scope/depth, not conflicts)

| Aspect | **[C12] Claude (12-vector)** | **[RM] Research Map (4-pillar)** |
|---|---|---|
| Structure | 12 vectors — adds **fast-hash retrieval (V3)**, **edge/box split (V9)**, **evaluation harness (V10)**, **cross-domain wildcards (V12)** | 4 pillars + **6-experiment dependency plan** + **ENGRAM-v2 blueprint** |
| Phase handling | operationalizes it: **GDF (group-delay function) as a ~free phase complement** (concat to 2×D) | "keep phase as index" (principle, no specific mechanism) |
| Fast retrieval | **Shazam-style peak-hash pre-filter** → cosine/Hopfield rerank (10–100× at scale) | lists Wang/Shazam as a *representation* paper, not a retrieval stage |
| Novel ideas | **EIGENGRAM** (PCA/SVD of fingerprints = "eigen-personality"); **Graph Fourier Transform** for room-topology | — (focuses on the four proven pillars) |
| Implementation | **numpy pseudocode** for `compose_identity()` + `hopfield_retrieve()`; int8/Q15 quantization; HDC-on-FPGA | repo/license tables; mapping notes; capacity caveat |
| Extra citations | music cognition (earworms/Huron/Margulis), TRACE/ZeroFlow CL benchmarks | **Continuous-time Modern Hopfield** (arXiv:2502.10122); **Hopfield-Kuramoto** (arXiv:2505.03648); **Linearithmic Kronecker cleanup** (arXiv:2506.15793) |

---

## PILLAR A — REPRESENT: music-aligned, multi-scale, robust fingerprints

**[Both]** Replace single-scale `|rFFT|` with deformation-stable, multi-scale features over a fixed
codebook; keep phase as an index.
- **Scattering / wavelets [Both]:** **wavelet scattering** (Bruna & Mallat 2012, arXiv:1112.1120 —
  Lipschitz-stable to deformation; Andén & Mallat 2013/14 **Deep Scattering Spectrum** — recovers
  modulation info MFCC discards) is the recommended single upgrade to `fingerprint.py`: `Scattering1D`
  (J≈5, Q≈1) via **kymatio** — 0th order ≈ "this hour", 1st ≈ envelope, 2nd ≈ modulation; shift-
  invariant + warp-stable. **Constant-Q / chroma** (Brown 1991/92) → log-freq bins make multiplicative
  scaling a translation (overtone-shift invariance). `[RM^1–^16][C^3–^12]`
- **The "notes" (fixed codebook) [Both]:** fit a small **VQ/dictionary once, offline, then freeze**
  (scikit-learn `MiniBatchDictionaryLearning`/K-means, or **RVQ** à la SoundStream/EnCodec/DAC —
  coarse→fine code stacks). [C12-V6] sizing: "4–6 notes" is an order-of-magnitude underestimate for a
  115-D space — expect **K=32–128** primitives; residual codebooks (K=16 coarse + 2×16 residual ≈ 48
  codes) cover most situations. Olshausen–Field sparse overcomplete dictionaries beat PCA. `[RM^7,^8][C^57–^62]`
- **The "grammar" [Both]:** split today's conflated f0/f1 into a **content track** (token sequence) +
  a **rhythm/structure track** (onsets, inter-onset intervals, **rests = low-energy windows →
  segmentation/novelty**, repetition via self-similarity matrix) = "same notes, different song."
- **[C12-only] phase, operationalized (V1):** compute the **group-delay function** (negative derivative
  of the phase spectrum) alongside rFFT and concatenate → 2×D vector — adds phase-structure sensitivity
  for ≈zero overhead (the "immediate win"). GDF reveals spectral peaks more reliably than magnitude in
  noise. `[C^1,^2,^13]`
- **[C12-only] multi-scale recipe (V6):** Scale-0 instant (100 ms rFFT, 58-D) | Scale-1 medium (1 s
  kymatio scattering, ~64-D) | Scale-2 long (10 s VQ-compressed, 16-D) → concat ~138-D + quantize each
  scale = the notes/bars metaphor.
- **Repos [Both]:** kymatio (BSD), PyWavelets/pywt (MIT), librosa (ISC, reference), kissfft/pffft (BSD,
  ARM), EnCodec/DAC (MIT). [RM] adds ssqueezepy (MIT, synchrosqueezing), audfprint/Dejavu (MIT).

---

## PILLAR B — COMPOSE: identity shapes under labels (VSA / HRR / HDC)

**[Both]** **This is the rigorous home of "the system prompt is a composed ENGRAM shape under a
label."** HRR (Plate 1995): `a ⊛ b` (circular convolution = elementwise multiply in the Fourier
domain) **binds**; addition **bundles**; correlation **unbinds** — and ENGRAM's rFFT pipeline already
lives in the domain where binding is one elementwise multiply.
- **Identity vector [Both]:** `IDENTITY_self = Σᵢ (K_self ⊛ fp_i)`, L2-normalized → one fixed-width
  "self" shape; membership by `cos(K_self ⊛ q, IDENTITY_self)`. Motifs:
  `(PERSON ⊛ alice) + (PLACE ⊛ kitchen) + (FEELING ⊛ calm)`; query by unbind + cleanup, or a
  **resonator network** when factors are unknown (Frady/Kent/Olshausen/Sommer 2020 — "search in
  superposition"). Hierarchy: leaf bundles (≤k) → mid → top "self". `[RM^17–^25][C^35–^48]`
- **⚠ Capacity caveat (both, load-bearing):** correlated fingerprints break the blessing of
  dimensionality. **Fixes (both):** (1) random ±1 **role-key projection** before binding; (2) **project
  to higher D (~4096)** — FHRR capacity ≈0.7N bits, so 115-D → 4096-D for ~10K items; (3) **cleanup
  memory** (Hopfield/SDM snaps noisy reconstructions to clean codebook atoms — Plate explicitly
  recommends). [RM] cites Capacity Analysis (arXiv:2301.10352); [C12] cites hd-computing FAQ.
  **Must quantify before committing (Experiment B/2).**
- **[C12-only] numpy `compose_identity()`** pseudocode: bind each fp with a role vector via
  `ifft(fft(fp)*fft(role)).real`, bundle, L2-norm, label-bind. Query = `unbind(identity, label_key)` →
  resonator → individual fingerprints.
- **[RM-only] further reading:** Smolensky TPR 1990, Kanerva HDC 2009, Gayler VSA 2003, Eliasmith SPA
  2013, **Linearithmic O(N log N) cleanup via Kronecker rotation** (2025, arXiv:2506.15793) for large
  namespaces.
- **Repos [Both]:** **torchhd** (MIT, FHRR maps directly onto Fourier fingerprints, 100× faster),
  **hdlib** (MIT, pure-numpy, the ARM/edge option), nengo-spa (SPA/Spaun).

---

## PILLAR C — RETRIEVE: resonance (Modern Hopfield = attention)

**[Both]** Don't replace the store — **swap the separation function.** Current cosine-kNN = top-k argmax
of `cos(q,kᵢ)` = the **β→∞ special case** (Millidge et al. 2022, *Universal Hopfield Networks*: Hopfield,
SDM, cosine-kNN, attention all = `separation(similarity(q,K))·V`). Upgrade to `softmax(β·qKᵀ)·V`
(Ramsauer et al. 2020, *Hopfield Networks is All You Need*: continuous Hopfield, exponential capacity
2^(d/2), update rule = transformer attention; β=1/√D recovers single-head attention). `[RM^32–^35][C^49–^56]`
- **Gains [Both]:** tunable **β "sharpness of resonance"** (low β → blend/context, high β → sharp
  episodic recall); **multi-step relaxation = pattern completion from partial/noisy cues** (one-shot
  kNN can't); resonator iteration adds factor decomposition; zero new storage (same hnswlib index feeds
  the update rule).
- **[C12-only] `hopfield_retrieve()` numpy** (1-step suffices for separated patterns; multi-step
  completes fragments) + capacity warnings: classic Hopfield 0.138N (only 16 patterns at D=115 → must
  use the softmax/modern form or project to higher D); spurious attractors below the exponential limit;
  enforce a hard M << 2^(d/2) budget.
- **[RM-only]:** Continuous-time Modern Hopfield (2025, arXiv:2502.10122 — compresses discrete memories
  into continuous-time, smaller footprint). Kanerva SDM (1988).
- **Repo [Both]:** **ml-jku/hopfield-layers** (BSD) — drop-in retrieval layer with full attention
  equivalence; torchhd for the resonator component.

---

## PILLAR D — GROUND: biological grounding (honest)

**[Both]** The frequency framing is grounded in *real* neuroscience — and explicitly *not* in
frequency-mysticism.
- ✅ **Theta-gamma neural code** (Lisman & Jensen 2013): theta (4–8 Hz) organizes gamma (30–80 Hz)
  sub-cycles, ~7 items/theta cycle (Miller's Law) = **frequency-division multiplexing** of memory,
  directly analogous to ENGRAM's FFT multiplexing. → implement **dual-timescale FFT** (1 s "theta"
  context + 100 ms "gamma" item), bundle separately in HDC. `[RM^36,^37,^43][C^64–^66]`
- ✅ **Phase precession** (O'Keefe & Recce 1993): phase carries sequence info rate codes don't → phase
  as a soft serial index. ✅ Human iEEG (Lega 2016, Daume 2024). `[C^67–^70]`
- ✅ **Hippocampal indexing theory** (Teyler & DiScenna 1986 / Teyler & Rudy 2007, "aged well")
  [C12-V7, the strongest architecture validation]: the hippocampus stores a **pointer/index** to
  distributed neocortical activity, not the content. **ENGRAM's fingerprint *is* this index** — the
  "content" lives in the robot's sensor log. `[C^71–^74]`
- ✅ **Reservoir computing** (Jaeger ESN 2001 / Maass LSM 2002): memory as an evolving dynamical state =
  the "constantly vibrating shape." `[RM^39,^40][C^79–^84]`
- ⚠ **Binding-by-synchrony** (von der Malsburg / Singer): real but **contested** (Shadlen & Movshon
  1999 critique; partially revived by **Artificial Kuramoto Oscillatory Neurons**, AKOrN, ICLR 2025
  Oral, arXiv:2502.21077; Hopfield-Kuramoto 2025, arXiv:2505.03648). Use as inspiration; label contested.
  `[RM^41,^42][C^75–^78]`

---

## [C12-only] VECTORS THE RESEARCH MAP DIDN'T COVER

- **V3 — Audio fingerprinting / fast retrieval:** Shazam constellation hashing (Wang 2003) — top-K
  spectral peaks → `(f0,f1,Δt)` 32-bit hash → time-offset histogram (~10,000× speedup). Port as a
  **two-stage retrieval: peak-hash pre-filter → hnswlib cosine rerank** (10–100× at scale). Repos:
  audfprint/Dejavu (MIT); Chromaprint (LGPL, ARM64 binary — re-implement the logic in numpy, the chroma
  basis won't transfer). `[C^29–^34]`
- **V9 — Edge / hardware feasibility:** explicit **on-robot vs box split** — FFT, GDF, L2-norm, VQ
  lookup, small Hopfield, N=256 reservoir, hnswlib all run **on-robot (Cortex-A7)**; scattering, large-D
  HDC (4096), big Hopfield → **box**. **int8 quantization** <2% cosine error; **kissfft Q15 fixed-point**
  enables FFT with no FPU; HDC maps cleanly to **FPGA** (XOR/popcount/multiply). `[C^15–^18,^48,^86–^88]`
- **V10 — Evaluation harness:** 8 metrics — Recall@K, **Capacity C**, **Pattern Completion** (mask
  30–50% dims), **BWT** (forgetting; TRACE/ZeroFlow), **Crosstalk χ**, **Compositionality** (compose→
  unbind→cosine), **Identity Stability IS** (`cos(self_t0, self_t)` over episodes), **near-duplicate
  discrimination** (ROC on `(v, v+ε·noise)` pairs). `[C^89–^92]`
- **V12 — Cross-domain wildcards:**
  - **EIGENGRAM** (buildable): PCA/SVD over all fingerprints = empirical **eigenmodes = "eigen-
    personality"**; project new fp onto top eigenvectors → compact eigen-code; slow eigenvector drift =
    stable personality, fast drift = novelty. IncrementalPCA, trivial. `[C^100–^102]`
  - **Graph Fourier Transform** (buildable kernel): eigenvectors of the room-topology graph Laplacian →
    representations invariant to graph-domain shifts; for a robot that builds a map. `[C^103–^105]`
  - Optical holography → HRR (the "holographic" in HRR is literal: distributed, graceful under partial
    damage). Cymatics = metaphor only; quasicrystals = dead end.

## [C12-only] V2 — music cognition depth
Earworms/INMI (>90% of people, preserve absolute pitch+tempo → store compact spectral+rhythmic
fingerprints) · Huron *Sweet Anticipation* (expectation) · Margulis *On Repeat* (repetition) · chunking
(logarithmic compression) · **arch melodic contour** improves recognition → engineer the fingerprint
envelope to be **contoured/peaked, not flat** · **rest detection** (near-zero windows → boundary →
resets the HDC accumulator). `[C^20–^28]`

---

## CONVERGED ARCHITECTURE (the [C12] one-pager, validated by [RM]'s blueprint)

```
LAYER 0 — SENSE (on-robot, ARM, <1 ms)
  raw [T×D] → kissfft rFFT + L2-norm → fp ∈ ℝ¹¹⁵
  → optional GDF complement: [fp | gdf] ∈ ℝ²³⁰
  → VQ code lookup (K=64, offline-trained): symbol s ∈ {0..63}
LAYER 1 — MULTI-SCALE (box, 5–50 ms)
  fp(100ms) + fp_slow(1s kymatio scattering) → [fp_fast | fp_slow] ∈ ℝ¹⁷⁸
  → IncrementalPCA → eigen-code e ∈ ℝ³²  [EIGENGRAM]
LAYER 2 — COMPOSE (box, numpy, <5 ms)
  e → project to D=4096 (random Gaussian) → HRR bind with role r → bundle
  → I_self, I_env, I_person_X
LAYER 3 — RETRIEVE (box, <2 ms)
  Stage 1 peak-hash → candidates (top 50)
  Stage 2 Hopfield 1-step (β=2.0) → completed fp*
  Stage 3 hnswlib cosine kNN → top-5 episodes
  Stage 4 unbind from identity bundle → context
LAYER 4 — GROUND (box, continuous)
  ESN reservoir (N=256) = working memory; h_t modulates β = 1 + 2·‖h_t‖ (arousal dial)
  Identity stability IS = cos(I_self_t0, I_self_t) logged daily
```
*[RM]'s ENGRAM-v2 blueprint is the same pipeline at coarser grain: INPUT → REPRESENT (Scattering1D /
DWT → frozen codebook → content+rhythm tracks → phase-as-index) → COMPOSE (FHRR per-label role-keys,
hierarchy) → RETRIEVE (hnswlib + cleanup + Hopfield β) → GROUND (phase-as-index, reservoir state,
namespace ROC).*

---

## MERGED BUILD ORDER

**[C12] ranked P1–P9** (cost / payoff):
P1 GDF complement (1 d / free phase info) · P2 peak-hash index (2 d / 10–100× retrieval) · P3 K-means
codebook K=64 (2 d / discrete "notes") · P4 HRR identity bundle D=4096 (3 d / named identity shapes) ·
P5 β-tunable Hopfield head (1 d / pattern completion) · P6 IncrementalPCA EIGENGRAM (2 d / IS metric) ·
P7 multi-scale scattering kymatio (1 wk / deformation stability) · P8 ESN reservoir N=256 (3 d /
working memory) · P9 evaluation harness (1 wk / ground truth).

**[RM] experiment dependency order:** #1 Robust Representation (hard near-dup corpus: f0+f1 vs +phase
vs +harmonics vs DWT vs **Scattering1D** vs chroma) → #2 **VSA Capacity** with real fingerprints
(random vs ENGRAM vs projected; torchhd FHRR — *the load-bearing gate*) → #4 Resonance retrieval
(softmax(β·XᵀXq)·X vs kNN at noise) → #3 Identity vector + namespaces (self-vs-other ROC) → #5 Codebook
notes (atom-firing stability) → #6 Resonator decomposition.

**Synthesis:** start where both agree the leverage is highest and the risk is real —
**Experiment #1 (does a better representation help on hard cases?) and #2 (is VSA viable on *our*
correlated vectors?)**. P1 (GDF) and P5 (Hopfield head) are the cheapest standalone wins; P4 (identity
bundle) is gated by #2's capacity result.

---

## COMBINED HONESTY BOUNDARY (both agree)
- ✅ **Build on:** Fourier/wavelet amplitude + GDF, scattering (kymatio), fixed VQ/RVQ codebooks,
  CQT/chroma, VSA/HRR composition + namespaces + resonator nets (torchhd/hdlib), Modern Hopfield =
  attention retrieval (ml-jku), reservoir computing (reservoirpy), phase-as-index, theta-gamma temporal
  ordering, hippocampal-indexing as architecture validation, EIGENGRAM/Graph-FT, the full eval harness.
- ⚠ **Inspiration / contested (cite both sides):** binding-by-synchrony (Singer/von der Malsburg vs
  Shadlen & Movshon 1999; AKOrN 2025 partial revival) — label as ongoing debate, don't assert.
  ▲ Speculative: full 2nd-order scattering at ARM real-time, resonator nets at ARM real-time, literal
  phase precession on digital hardware, cymatics-as-information, quasicrystals.
- ❌ **Drop entirely:** Schumann resonance (7.83 Hz) entrainment; 432/528 Hz "healing"/"DNA repair";
  solfeggio frequencies; "personality is a single standing waveform at frequency X." **The defensible
  version (both):** *personality is a point/trajectory in a high-dimensional dynamical state, composed
  by frequency-domain binding (HRR) and retrieved by resonance (Hopfield).*
- **[C12] phrasing for the paper:** *"inspired by the structural properties of oscillatory coding —
  discreteness, hierarchy, periodicity, resonance — rather than by specific frequency values… the
  frequency domain is a computational tool for invariant representation, not a carrier of semantic
  meaning."* Anchor cites: Lisman & Jensen (2013), Plate (1995), Andén & Mallat (2013). `[C^93–^99]`

---

## APPENDIX A — [C12] Claude Opus 4.8 references (1–105, verbatim)
1. https://www.eurasip.org/Proceedings/Eusipco/Eusipco2006/papers/1568982294.pdf
2. https://mini.dcs.shef.ac.uk/wp-content/papercite-data/pdf/loweimi_icassp13.pdf
3. https://arxiv.org/pdf/1112.1120.pdf
4. https://www.mathworks.com/help/wavelet/ug/wavelet-scattering.html
5. https://www.semanticscholar.org/paper/Calculation-of-a-constant-Q-spectral-transform-Brown/a667221790229863b9778688969a2544508cdfeb
6. https://www.jmlr.org/papers/volume21/19-047/19-047.pdf
7. https://en.wikipedia.org/wiki/Constant-Q_transform
8. https://jmlr.org/papers/v21/19-047.html
9. https://www.kymat.io
10. https://arxiv.org/abs/1304.6763
11. https://www.semanticscholar.org/paper/Deep-Scattering-Spectrum-And%C3%A9n-Mallat/209826c2ce8352390ccd9f19864186a60739f3f3
12. https://www.di.ens.fr/~mallat/papiers/IEEESignalAndenLostanlen.pdf
13. https://pubmed.ncbi.nlm.nih.gov/35364933/
14. https://exarchakis.net/post/kymatio/
15. https://packages.gentoo.org/packages/sci-libs/kissfft
16. https://blog.csdn.net/xieliru/article/details/149406600
17. https://github.com/MTG/essentia/issues/581
18. https://android.googlesource.com/platform/external/pffft/+/786cf5ce750efa74401b421baac6cedabff366b6%5E1..786cf5ce750efa74401b421baac6cedabff366b6/
19. https://kinwaicheuk.github.io/nnAudio/master/_autosummary/nnAudio.features.cqt.CQT1992.html
20. https://featuredcontent.psychonomic.org/the-minds-spotify-the-remarkable-pitch-of-earworms/
21. https://musicscience.net/research/music-memory/earworms/
22. https://centaur.reading.ac.uk/5755/1/earworms_write-upBJP.pdf
23. https://pmc.ncbi.nlm.nih.gov/articles/PMC7704448/
24. https://pmc.ncbi.nlm.nih.gov/articles/PMC11588220/
25. https://cognitivesciencesociety.org/cogsci20/papers/0037/index.html
26. https://arxiv.org/pdf/2512.18665.pdf
27. https://robertpoortinga.com/2025/04/02/memorising-for-a-musician/
28. https://journals.sagepub.com/doi/10.1177/03057356211013396
29. https://www.linkedin.com/posts/lukapiplica_the-math-behind-shazam-activity-7468646774870732800-UpT5
30. https://xiahongze.github.io/tech/2019/11/17/Yet-Another-How-Shazam-Works.html
31. https://github.com/oguya/audio-fingerprint/blob/master/demo_fingerprint.m
32. https://acoustid.org/chromaprint
33. https://acoustid.org/license
34. https://build.opensuse.org/projects/home:rguenther:plgrnd/packages/chromaprint/files/chromaprint.spec
35. https://www.semanticscholar.org/paper/Holographic-reduced-representations-Plate/0c4d193b4e8520dbc583cc7ee59c8417869f67ce
36. https://arxiv.org/abs/2112.15424
37. https://proceedings.neurips.cc/paper_files/paper/2021/file/d71dd235287466052f1630f31bde7932-Paper.pdf
38. https://dl.acm.org/doi/10.1145/3558000
39. https://pubmed.ncbi.nlm.nih.gov/18263348/
40. https://arxiv.org/abs/2205.09208
41. https://github.com/orgs/hyperdimensional-computing/repositories
42. https://www.hd-computing.com/faq
43. https://arxiv.org/html/2604.11665v4
44. https://arxiv.org/abs/2007.03748
45. https://arxiv.org/abs/1906.11684
46. https://redwood.berkeley.edu/wp-content/uploads/2021/08/Module5_ResonatorNetworks_FocusReading.pdf
47. https://direct.mit.edu/neco/article/32/12/2332/95653/Resonator-Networks-2-Factorization-Performance-and
48. https://research.ibm.com/publications/vector-symbolic-architectures-as-a-computing-framework-for-emerging-hardware
49. https://pmc.ncbi.nlm.nih.gov/articles/PMC9713410/
50. https://proceedings.mlr.press/v162/millidge22a.html
51. https://www.cs.ox.ac.uk/publications/publication14879-abstract.html
52. https://iris.joshua-becker.com/lab/persistent-excitation-hopfield/
53. https://openreview.net/forum?id=tL89RnzIiCd
54. https://openreview.net/pdf/4dfbed3a6ececb7282dfef90fd6c03812ae0da7b.pdf
55. https://github.com/ml-jku/hopfield-layers/blob/master/examples/mnist_bags/mnist_bags_demo.ipynb
56. https://github.com/ml-jku
57. https://arxiv.org/pdf/2305.02765.pdf
58. https://research.google/blog/soundstream-an-end-to-end-neural-audio-codec/
59. https://zenn.dev/taku_sid/articles/2025-04-10_neural-audio-codec?locale=en
60. https://learnius.com/slp/9+Speech+Synthesis/2+Advanced+Topics/4+Neural+Codec+Language+Modeling/residual+vector+quantization+(RVQ)
61. https://www.sumofsquares.org/public/lec-sphere-dictionary.pdf
62. https://github.com/siplab-gt/Sparse-Coding-Dictionary-Learning-Library
63. https://openreview.net/pdf/887ef8cc2ce3e235359584279041197f58ffb7a1.pdf
64. https://netherlands.openaire.eu/search/publication?pid=10.1016%2Fj.neuron.2013.03.007
65. https://www.semanticscholar.org/paper/The-Theta-Gamma-Neural-Code-Lisman-Jensen/48cfa39ee9172f3a03f7599786d20b4dfcfbbc58
66. https://www.cs.cmu.edu/afs/cs/academic/class/15883-f13/slides/hc-rhythms.pdf
67. https://en.wikipedia.org/wiki/Phase_precession
68. https://pubmed.ncbi.nlm.nih.gov/28390862/
69. http://buzsakilab.org/content/PDFs/DragoiNeuron2006.pdf
70. https://elifesciences.org/reviewed-preprints/87055v3
71. https://pubmed.ncbi.nlm.nih.gov/17696170/
72. https://www.dbs.ifi.lmu.de/~tresp/papers/5927d71168ed3feb338a2576.pdf
73. https://pubmed.ncbi.nlm.nih.gov/3008780/
74. https://scienceon.kisti.re.kr/srch/selectPORSrchArticle.do?cn=NART36716841
75. https://pubmed.ncbi.nlm.nih.gov/10677027/
76. https://www.cse.iitk.ac.in/users/hk/cgs700/2019/temporalBindingHyp.pdf
77. https://openreview.net/forum?id=nwDRD4AMoN
78. https://en.wikipedia.org/wiki/Binding-by-synchrony
79. https://www.jmlr.org/papers/volume20/19-150/19-150.pdf
80. https://people.bath.ac.uk/jhpd20/publications/arxiv_version_2102.06258.pdf
81. https://www.jmlr.org/papers/volume19/18-020/18-020.pdf
82. https://www.ai.rug.nl/minds/uploads/2261_LukoseviciusJaeger09.pdf
83. https://github.com/reservoirpy/reservoirpy
84. https://inria.hal.science/hal-03699931
85. https://arxiv.org/abs/2311.03260v1
86. https://developer.arm.com/community/arm-community-blogs/b/operating-systems-blog/posts/ne10-fft-feature-radix-3-and-radix-5-fft-are-supported-neon-optimization
87. https://ieeexplore.ieee.org/document/10946177/
88. https://backend.orbit.dtu.dk/ws/portalfiles/portal/398648111/Samwi_Reconfigurable_Digital_FPGA_Implementations_for_Neuromorphic_Computing.pdf
89. https://towardsdatascience.com/the-metrics-of-continual-learning-08f2d1cd959b/
90. https://openreview.net/pdf?id=3qa4YLkcEw
91. https://huggingface.co/papers/2501.01045
92. https://proceedings.neurips.cc/paper/2021/file/54ee290e80589a2a1225c338a71839f5-Paper.pdf
93. https://en.wikipedia.org/wiki/Schumann_resonances_conspiracy_theories
94. https://www.scribd.com/document/1011331152/BrainWavesandtheSchumannResonance
95. https://popwave.ai/benn-jordan/blog/528hz-myth-debunked
96. https://www.facebook.com/groups/2787803246/posts/10161830972098247/
97. https://www.zonora.com/life/2025/03/31/debunking-myths-about-frequency-healing/
98. https://www.soundmedicineacademy.com/pages/sound-healing-blog/solfeggio-frequencies
99. https://www.pemfmagazine.com/debunking-the-myth-of-ancient-frequencies-science-music-and-the-law-of-octaves/
100. https://www.ijcai.org/Proceedings/91-1/Papers/006.pdf
101. https://www.nature.com/articles/343325a0
102. https://web.stanford.edu/class/psych209a/ReadingsByDate/01_30/Willshaw81.pdf
103. https://en.wikipedia.org/wiki/Graph_Fourier_transform
104. https://perraudin.info/publications/perraudin-note-019.pdf
105. https://pdfs.semanticscholar.org/aadf/d04f402c2fc7d5c4606bbef0788dc54c0910.pdf

## APPENDIX B — [RM] Research-Map references (1–46, verbatim)
1. https://proceedings.mlr.press/v162/millidge22a.html
2. https://arxiv.org/abs/2008.02217
3. https://arxiv.org/pdf/1203.1513.pdf
4. https://archive.org/details/arxiv-1203.1513
5. https://www.semanticscholar.org/paper/Deep-Scattering-Spectrum-And%C3%A9n-Mallat/209826c2ce8352390ccd9f19864186a60739f3f3
6. https://arxiv.org/abs/1304.6763
7. https://papers.nips.cc/paper/7210-neural-discrete-representation-learning
8. https://arxiv.org/abs/1711.00937
9. https://en.wikipedia.org/wiki/EnCodec
10. https://github.com/facebookresearch/encodec
11. https://github.com/kymatio/kymatio
12. https://matthewhirn.com/wp-content/uploads/2020/06/2020-andreux-et-al-kymatio-scattering-transforms-in-python.pdf
13. https://github.com/PyWavelets/pywt
14. https://github.com/OverLordGoldDragon/ssqueezepy
15. (scikit-learn dict-learning — MiniBatchDictionaryLearning / SparseCoder)
16. https://github.com/dpwe/audfprint
17. https://pages.ucsd.edu/~msereno/170/readings/06-Holographic.pdf
18. https://redwood.berkeley.edu/wp-content/uploads/2020/08/Plate-HRR-IEEE-TransNN.pdf
19. https://dl.acm.org/doi/abs/10.1162/neco_a_01329
20. https://ieeexplore.ieee.org/document/9272714/
21. https://arxiv.org/abs/2112.15424
22. https://arxiv.org/abs/2111.06077v1
23. https://arxiv.org/abs/2301.10352
24. https://arxiv.org/pdf/2301.10352.pdf
25. https://arxiv.org/abs/2506.15793
26. https://www.collectionscanada.gc.ca/obj/thesescanada/vol2/OKQ/TC-OKQ-5966.pdf
27. https://arxiv.org/abs/2205.09208
28. https://github.com/hyperdimensional-computing/torchhd/releases
29. https://pypi.org/project/hdlib/0.1.2/
30. https://github.com/cumbof/hdlib
31. https://www.theoj.org/joss-papers/joss.05704/10.21105.joss.05704.pdf
32. https://www.pnas.org/doi/10.1073/pnas.79.8.2554
33. https://openreview.net/pdf?id=tL89RnzIiCd
34. https://icml.cc/media/icml-2022/Slides/17308.pdf
35. https://arxiv.org/pdf/2502.10122.pdf
36. https://pubmed.ncbi.nlm.nih.gov/23522038/
37. https://onlinelibrary.wiley.com/doi/10.1002/hipo.450030307
38. https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2024.1326609/full
39. https://github.com/reservoirpy/reservoirpy
40. https://inria.hal.science/hal-03761440/document
41. http://arxiv.org/abs/2502.21077
42. http://www.arxiv.org/abs/2505.03648
43. https://www.cs.cmu.edu/afs/cs/academic/class/15883-f13/slides/hc-rhythms.pdf
44. https://torchhd.readthedocs.io/en/stable/torchhd.html
45. https://redwood.berkeley.edu/wp-content/uploads/2021/08/Module5_ResonatorNetworks_FocusReading.pdf
46. https://ml-jku.github.io/hopfield-layers/

---

*Fused 2026-06-24 from `08_frequency_memory__symphony.md` (Claude Opus 4.8, 12-vector) +
`07_frequency_memory__research_map.md` (Research Map, 4-pillar). Most convergent pair of the four — no
contradictions; differences are scope/depth. No finds or sources dropped.*
