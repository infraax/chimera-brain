# RESEARCH GEODESIC — Solving AI Memory with Frequency & Symphony
## A self-contained research brief to collect everything on the "memory-as-frequency / symphony" idea
## Created: 2026-06-24 · Dexter × Claude Opus 4.8

> **How to use this:** hand each *vector* (or the whole file) to a research agent / deep-research tool.
> Each vector is independently runnable. Bring results back into chat in the **Return Format** (§Output).
> A first internal pass is already done — see `research/ENGRAM_FREQUENCY_RESEARCH.md`; this geodesic is for
> going **wider and deeper** with external tools, and to stress-test/expand those findings.

---

## PRIME DIRECTIVE (the thesis to investigate)
> *Can an AI's memory — and ultimately its personality — be represented, composed, stored, and retrieved as a
> structure in the **frequency domain**, organized by the grammar of **music** (a fixed alphabet of "notes" +
> timing/repetition/rests + multi-scale "bars"), composed into **labeled identity shapes** ("self",
> "environment", a person), and recalled by **resonance**?* Collect the strongest evidence FOR and AGAINST,
> the buildable techniques, the open-source implementations, and the honest boundary against pseudoscience.

Current system being evolved (context for every vector): **ENGRAM** = `|rFFT|` over a `[T,D]` window of fused
perception, amplitude at freqs {0,1}, L2-normalized, concatenated → vector; cosine-kNN retrieval (hnswlib).
Amplitude-only (phase discarded), single time-scale, deterministic, training-free. Runs box-side (numpy);
target deploys on ARM (Anki Vector) + a companion box.

---

## CROSS-CUTTING CONSTRAINTS (apply to every vector)
1. **Primary sources first** — papers (with links/DOIs/arXiv), then official repos (with **license** + language + edge-feasibility). No vibes; cite everything.
2. **Separate BUILDABLE from FRINGE** explicitly. Flag pseudoscience (e.g. "Schumann resonance tunes the brain", "DNA/cellular healing frequencies") and say *why*, but still record it under "inspiration/▲speculative" so we can talk about it honestly.
3. **Edge/ARM reality** — for any technique, note compute/memory cost and whether it can run on a Cortex-A7-class device vs must live on a Pi/Jetson/Mac box.
4. **Map back to ENGRAM** — every finding ends with "what this would change in our fingerprint / composition / retrieval."
5. **Prefer permissive licenses** (MIT/BSD/Apache/ISC); flag GPL/AGPL/non-commercial.
6. **Find the disconfirming evidence** — for each promising idea, actively search for the rebuttal / failure modes / capacity limits.

---

## RESEARCH VECTORS

### V1 — Spectral representation foundations (what to keep, and why)
- **Questions:** When is amplitude enough vs when does **phase** carry the information (phase retrieval, group delay, instantaneous frequency)? DFT vs STFT vs **constant-Q / log-frequency** vs **wavelets** vs **scattering transform** — which gives the best *invariances* (shift, scale, time-warp) for a "situation fingerprint"? What invariances do we actually want for memory?
- **Look at:** Mallat (wavelets, scattering), Andén–Mallat (deep scattering spectrum), Brown (CQT), phase-retrieval literature, group-delay features in speech.
- **Return:** a ranked table of representations × invariances × cost; recommendation for ENGRAM's fingerprint.

### V2 — Music theory & music cognition AS a memory grammar
- **Questions:** Why is **music** so memorable to humans (earworms, melodic contour, chunking)? What are the minimal structural primitives — scale/key, **rhythm & meter**, **repetition & form** (AABA, motif development), **rests/silence**, consonance/dissonance, **leitmotif**? How does music cognition encode/recall sequences? Can these map to a *grammar* for situation-memories (fixed "notes" + structural variation)?
- **Look at:** Müller *Fundamentals of Music Processing*; music cognition (Levitin, Huron *Sweet Anticipation*, Margulis *On Repeat*); MIR structure-analysis (self-similarity matrices, novelty curves); Schenkerian/Gestalt ideas of musical form; involuntary musical imagery research.
- **Return:** a concrete "music grammar → memory format" mapping (which musical concept → which data-structure), + evidence on *why music aids memory* and whether it transfers to non-audio signals.

### V3 — Audio fingerprinting & robust retrieval at scale
- **Questions:** What makes Shazam-style **constellation/landmark hashing** robust to noise/time-shift and scalable to millions? Chromaprint, Panako, Haitsma–Kalker bit-fingerprints — tradeoffs? Can constellation hashing be a **fast pre-filter** before cosine/resonance reranking on *non-audio* situational spectra?
- **Look at:** Wang 2003 (Shazam), Haitsma–Kalker 2002, Chromaprint/AcoustID, Panako, audfprint, Dejavu.
- **Return:** the robustness tricks worth porting + a recipe for a situational landmark-hash index.

### V4 — Composition: VSA / HRR / Hyperdimensional Computing (the identity-shape layer)
- **Questions:** How to **bundle** many fingerprints into one **identity vector** under a **label/namespace** and still retrieve members? Binding via **circular convolution = Fourier-domain multiply** (HRR/FHRR). **Capacity** limits of superposition vs dimension; **crosstalk** when items are *correlated* (our fingerprints are NOT random!). **Resonator networks** to factor bound motifs. Hierarchical composition (notes→motifs→self). Cleanup memory.
- **Look at:** Plate (HRR), Kanerva (HDC, SDM), Gayler (VSA), Eliasmith (SPA/Spaun), Frady/Kent/Sommer (resonator networks), Kleyko et al. (HDC/VSA surveys), capacity papers; repos `torchhd`, `hdlib`, `nengo-spa`.
- **Return:** a design for `compose_identity(label)` incl. how to handle correlated/amplitude-only vectors (random role-keys? higher-D projection?), and the empirical capacity numbers to expect.

### V5 — Retrieval by resonance: associative / energy-based memory
- **Questions:** Modern Hopfield = attention (Ramsauer); **Universal Hopfield** (cosine-kNN, SDM, attention all one template) — what does the **β "sharpness"** knob buy us? **Multi-step pattern completion** from partial cues. Energy landscapes, spurious minima, capacity (classic 0.14N vs modern exponential). When does resonance beat kNN?
- **Look at:** Hopfield 1982, Ramsauer 2020, Millidge "Universal Hopfield Networks" 2022, Kanerva SDM; repo `ml-jku/hopfield-layers`.
- **Return:** spec for a β-tunable Hopfield retrieval head over our store + when to prefer it over cosine-kNN.

### V6 — The "notes": multi-resolution + fixed codebooks
- **Questions:** Wavelets/scattering for **multi-scale ("bars")** capture of instant-vs-hour; **dictionary learning / sparse coding / VQ / residual-VQ** for a **frozen primitive alphabet**. How small can the codebook be while staying expressive (your "4–6 notes make any melody" intuition — what's the real number for our 115-D situations)? Stability of atom-firing under noise.
- **Look at:** Olshausen–Field, K-SVD, VQ-VAE, SoundStream/EnCodec/DAC (RVQ), kymatio (scattering), PyWavelets, scikit-learn dict-learning.
- **Return:** recommended codebook size/structure + multi-scale fingerprint recipe + ARM cost.

### V7 — Neuroscience of memory-as-oscillation (grounding + honesty)
- **Questions:** Theta-gamma code (Lisman–Jensen), **phase precession** (O'Keefe–Recce), cross-frequency coupling & human episodic memory, **replay/consolidation** during sleep, hippocampal **indexing theory** (memory as an index/pointer, not the content). **Binding-by-synchrony** — state of the debate (Singer vs Shadlen–Movshon). What's solid, what's contested?
- **Look at:** Lisman–Jensen 2013, O'Keefe–Recce 1993, Lega 2016/Daume 2024 (human), Buzsáki (rhythms of the brain), Teyler–Rudy (indexing theory), von der Malsburg/Singer vs Shadlen–Movshon.
- **Return:** what real brains do with phase/frequency for memory (buildable analogies) + an explicit "contested/▲" list.

### V8 — Memory as a living dynamical state ("the constantly vibrating shape")
- **Questions:** **Reservoir computing** (echo-state/liquid-state) as fading memory in an evolving high-D state; attractor dynamics; **Kuramoto** coupled oscillators & synchronization; oscillatory/complex-valued neural nets reviving binding-by-synchrony. Could "personality" be an **attractor landscape** rather than a stored vector?
- **Look at:** Jaeger (ESN), Maass (LSM), Kuramoto, "Artificial Kuramoto Oscillatory Neurons" (2025); repo `reservoirpy`.
- **Return:** assessment of whether memory should live in a *state* vs a *store* (or both), with cost.

### V9 — Edge / hardware feasibility
- **Questions:** Fast FFT/DWT/scattering on **ARM/NEON**; **HDC on FPGA/in-memory/neuromorphic** hardware; quantization of fingerprints/identity vectors; latency & memory budgets for µs retrieval on-device vs box. What's the smallest viable on-robot footprint?
- **Look at:** kissfft/PFFFT/pocketfft, ncnn, HDC hardware survey (Kleyko Part II), neuromorphic memory, in-memory computing for HDC.
- **Return:** on-robot vs box split for each technique with numbers.

### V10 — Evaluation: how do we even measure "good memory"?
- **Questions:** Metrics for **recall, capacity, pattern completion, compositionality, graceful forgetting, interference/crosstalk, continual-learning/forgetting**. Datasets/benchmarks for episodic/associative memory; how to build a **hard near-duplicate** test set; how to measure "did the personality stay itself."
- **Look at:** continual-learning benchmarks, associative-memory capacity tests, compositional-generalization tests, VSA capacity protocols.
- **Return:** a concrete evaluation harness spec for our testbed.

### V11 — The honesty boundary (anti-pseudoscience)
- **Questions:** Catalogue the frequency *mysticism* (Schumann resonance "entrainment", 432Hz/528Hz "healing", cymatics-as-information, "vibrational" personality) and the actual evidence (or absence). How do we **use the legitimate frequency/resonance science without inheriting the woo**? How to phrase it in the paper so it's credible to engineers?
- **Look at:** debunking literature on Schumann/“healing frequencies”, the binding-problem critiques, replication crises in adjacent claims.
- **Return:** a crisp "keep / drop / inspiration-only" table with one-line justifications.

### V12 — Cross-domain wild cards (flagged ▲ speculative, explore with skepticism)
- **Prompts:** **Holographic memory / optical holography** (distributed storage, graceful degradation — the literal root of "holographic" reduced representations); **harmonic analysis on graphs/manifolds** (graph Fourier transform — could situations live on a learned graph?); **eigenmodes/normal modes** (a personality as the resonant modes of a system — eigen-personality, ties to EIGENGRAM); **information theory / MDL** (a fingerprint as minimal description; compression = understanding); **cymatics** (▲ pattern from frequency — inspiration only); **quasicrystals/aperiodic order** (▲). For each: is there a *buildable* kernel or is it metaphor only?
- **Return:** for each wild card, "buildable kernel / metaphor only / dead end" + any real technique it points to.

---

## OUTPUT — Return Format (how to bring results back)
For each vector, return:
```
### V# — <title>
SUMMARY: 3–5 sentences of the state of the art + the answer to the core question.
PAPERS:  - Title (authors, year) — link — one-line why it matters
REPOS:   - name — URL — license — language — one-line + edge note
MAP→ENGRAM: what this changes in represent / compose / retrieve (be concrete)
BUILDABLE vs ▲SPECULATIVE: explicit
EXPERIMENT: 1–2 cheap tests to validate in a numpy testbed
CONFIDENCE + OPEN QUESTIONS / disconfirming evidence found
```
Final synthesis to produce after all vectors: a one-page **"converged architecture"** (represent→compose→
retrieve→ground) + a ranked build order + the honest boundary.

---

## SEED SEARCH TERMS (paste-ready)
`holographic reduced representations` · `vector symbolic architecture survey` · `hyperdimensional computing
capacity` · `resonator networks factoring` · `modern hopfield networks attention` · `universal hopfield
networks` · `wavelet scattering transform invariant` · `deep scattering spectrum` · `constant-Q transform` ·
`audio fingerprint constellation hashing` · `residual vector quantization audio codec` · `theta gamma neural
code memory` · `phase precession hippocampus` · `binding by synchrony critique` · `echo state network memory`
· `graph Fourier transform` · `sparse distributed memory` · `hippocampal memory indexing theory` ·
`continual learning catastrophic forgetting benchmark` · `Schumann resonance brain entrainment evidence`
(skeptical).

> Companion internal findings already gathered: `research/ENGRAM_FREQUENCY_RESEARCH.md`.
> Vision/design: `MUSIC_AND_FREQUENCY_CONCEPTS.md`. Paper: `SOLVING_AI_MEMORY_WITH_FREQUENCY_AND_SYMPHONY.md`.
