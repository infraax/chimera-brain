# RESEARCH GEODESIC — A Frequency-Native Base Model for ENGRAM
## Does a base model exist (or an architecture) that thinks in the frequency domain and treats ENGRAM-style memory as native — and if not, what's the path?
## Created: 2026-06-26 · Dexter × Claude Opus 4.8

> **How to use:** hand each *vector* (V1…V10) to a deep-research agent. Return findings in the
> **Output** format (per vector), then the **Final Synthesis**. This is an **ML-architecture +
> prior-art + feasibility** geodesic. Its output is a **decision with a staged plan**, not a survey:
> *can we run ENGRAM's frequency memory under a model that natively understands it, and if so how —
> bridge, train-up, rebuild, or distill?*
>
> **CRITICAL — build on what we already have, treat it as INPUT, do not redo it.** ENGRAM already
> exists as working code and a fused research map. Read these first:
> - `research/reports/unified/frequency_memory__UNIFIED.md` — the four pillars (represent → compose →
>   retrieve → ground); wavelet scattering, HRR binding, Modern Hopfield retrieval, theta-gamma.
> - `SOLVING_AI_MEMORY_WITH_FREQUENCY_AND_SYMPHONY.md` — the thesis (memory as frequency; the music grammar).
> - `vector_engram/` — the implemented system: the **two senses** (`sense.py`: REFLEX raw-FFT vs
>   MEANING embedding-FFT), `fingerprint.py` (+GDF phase), `resonance.py` (Hopfield), `vsa.py` (HRR +
>   random projection), `compose.py` (the self-shape), and `CAPACITY_RESULTS.md` (the honest capacity gate).
> - `research/reports/unified/cutting_edge_oss__UNIFIED.md` — the 2024–26 model/runtime landscape.
>
> **The pivotal framing.** ENGRAM's memory is **training-free** — a fingerprint is a deterministic FFT
> of sensation/embeddings, not a learned weight. The open question is the *reasoner* that consumes and
> produces these memories. Today's plan pairs ENGRAM with an **off-the-shelf LLM that was trained
> token/text-native** — it reasons over discrete BPE tokens, not spectra. So there is a representational
> seam: **the memory speaks frequency; the mind speaks tokens.** This geodesic asks whether that seam
> should be *bridged*, *grown out of a small model*, *rebuilt from scratch*, or *distilled* — and what
> the evidence says is actually best for a long-term, solo-buildable, iterable foundation.

---

## PRIME DIRECTIVE
> *Determine the best architecture/base-model strategy for a system whose long-term memory is ENGRAM's
> frequency-domain fingerprints, the two senses (REFLEX/MEANING), HRR composition, and Hopfield
> resonance retrieval. First establish the **prior art** — has anyone built a frequency-domain or
> associative-memory-native base model / framework? Then, grounded in that evidence, recommend a
> **path and a staged plan**: (0) a learned **bridge** so a normal model reads/writes ENGRAM (maybe no
> new base model is needed); (1) take a **very small base model and train it upward** with the
> frequency design; (2) **rethink the transformer** to be frequency- and ENGRAM-native from scratch;
> or (3) a **hybrid/distillation** middle path. The deliverable is a decision, a justification, and a
> falsifiable experiment ladder — honest about cost and about what is real vs speculative.*

**Explicit owner requirements (each must be satisfied and traced in the synthesis):**
1. **Answer the prior-art question first** — frequency-native and memory-native architectures: what
   exists, how mature, at what scale, with what results. Don't reinvent if it exists.
2. **If it exists**, say how to adopt/extend it for ENGRAM. **If it doesn't**, decide between Path 1
   (small-model train-up) and Path 2 (greenfield rearchitecture) — and weigh the added Path 0/3.
3. **Long-term iterability** — the chosen foundation must be one we can build on for years (open
   weights/architecture, extensible, not a dead end).
4. **Solo-buildable budget** — realistic on a solo maker + modest cloud (a few GPUs / rented H100-hours),
   not a frontier-lab training run. Price every path honestly.
5. **Keep ENGRAM's gains** — training-free memory, continual updates without catastrophic forgetting,
   portable `.eng` certificates, and the two-rate (theta/gamma) split must survive whatever model we pick.

---

## THE RUBRIC (rank every option and every path on these — this is the point)
Score 1–5 per axis. A modest architecture that genuinely makes frequency/ENGRAM first-class and is
cheap to iterate beats a glamorous one we can't afford or verify.
- **(N) Native-fit** — does it let frequency representation + ENGRAM memory be *first-class*
  (composition, resonance, training-free updates), or is memory bolted on as an afterthought?
- **(M) Maturity / Evidence** — real published results at relevant scale vs a clever idea with no proof.
  Re-benchmark mindset; distrust "Nx better" claims.
- **(C) Cost-to-build** — compute + data + engineering time on a solo+modest-cloud budget.
- **(I) Iterability / Longevity** — open weights/architecture; extensible; a foundation we can grow for years.
- **(R) Risk** — probability it underperforms a plain small token model at equal effort (the null hypothesis).
- **(H) Honesty** — cleanly separates real spectral ML / associative-memory science (FNO, SSMs, Hopfield,
  VSA/HRR, RFF attention) from numerology/hype (no Schumann/432 Hz/"vibrational" anything).

---

## CROSS-CUTTING CONSTRAINTS (apply to every vector)
1. **The null hypothesis is respected.** A small, ordinary token LLM + ENGRAM-as-retrieval is the
   baseline every path must *beat* to justify its extra cost. State, per path, what specifically would
   make it better (memory fidelity, long-horizon recall, continual learning, compositionality, on-device
   efficiency) and how we'd know.
2. **Honor the honesty boundary** (project doctrine): keep wavelet scattering, HRR/VSA, Modern Hopfield,
   state-space/spectral operators, random-Fourier-feature attention; drop frequency mysticism. Negative
   results are kept and reported.
3. **Preserve ENGRAM's properties.** Training-free fingerprints; the two senses live in separate cosine
   spaces (never compared); HRR composition; the capacity finding (raw fingerprints are correlated →
   random-projection to high-D restores VSA capacity; cleanup memory mandatory — see `CAPACITY_RESULTS.md`).
   Any model that ingests fingerprints must not silently break these.
4. **Two-tier deployment is real.** The reasoner may live on the **box/dock** (MEANING, slow) while a
   tiny reflex runs on the **robot** (REFLEX, fast). Map each path to where it would run and at what
   cost/latency (cross-ref the Benzy three-body design and the ENGRAM C++/Go/Python runtime plan).
5. **Open & licensable.** Rearchitecting or continued-pretraining requires **open-weights / open
   architecture**. Flag license traps (non-commercial, gated, distillation-prohibited) explicitly.
6. **Recency + citations.** 2023–2026 work; cite papers/repos/dates; note scale (params, tokens) and
   whether results were independently reproduced.

---

## RESEARCH VECTORS

### V0 — The seam question: do we even need a new base model? (rule this out first)
- **Why first:** ENGRAM memory is training-free and external. The cheapest win is a **learned bridge**
  that lets an *unmodified* model read/write `.eng` fingerprints — if that suffices, Paths 1/2 are moot.
- **Questions:** Survey **external/associative memory augmentation** of frozen LLMs: RETRO, kNN-LM,
  Memorizing Transformers, REALM/RAG, Larimar (episodic memory control), Recurrent Memory Transformer
  (RMT), Memformer, LongMem, and "memory tokens"/soft-prompt injection. Can a frozen reasoner consume
  ENGRAM fingerprints via a small trained **adapter** (fingerprint → memory tokens via cross-attention),
  and emit cues that ENGRAM retrieves against? What's lost vs native (the model still *thinks* in tokens,
  but *remembers* in frequency)? Is retrieval-as-cross-attention enough to get resonance/composition
  benefits, or do those need to be inside the model?
- **Return:** a verdict — **is a bridge sufficient for the near term?** — with the concrete adapter
  design, what it can/can't deliver, and the trigger conditions that would force a deeper path.

### V1 — Prior art I: spectral / Fourier-domain neural architectures
- **Questions:** Map the field of models that compute in the frequency domain. **FNet** (Fourier token
  mixing replacing attention), **GFNet** (global filter networks), **AFNO / Fourier Neural Operators
  (FNO)** (learned spectral convolutions; PDE origin but general), **Hyena / Hyena Hierarchy** and
  **H3** (implicit long convolutions = spectral mixing), spectral/wavelet transformers, **WaveletNet**,
  **SpectFormer**, **Performer/FAVOR+** (random Fourier features approximating softmax attention —
  literally Fourier-feature attention). For each: what scale has it reached, does a *language* base model
  exist using it, results vs vanilla attention, and is the "frequency" genuinely load-bearing or
  incidental. Which of these is closest to a usable **frequency-native LM backbone**?
- **Return:** a ranked map of spectral architectures by maturity + LM-readiness + native-fit, naming
  the 1–3 most credible backbones to build on.

### V2 — Prior art II: state-space models as the de-facto frequency-native family
- **Hypothesis to test:** SSMs may already *be* the frequency-native base architecture, since a long
  convolution is a frequency-domain operator. **S4/S4D/S5**, **Mamba / Mamba-2**, **RWKV (v6/v7)**,
  **RetNet**, **linear-attention** families. Mamba-2's duality with attention; the convolutional/spectral
  view of SSM kernels; HiPPO initialization as a spectral basis.
- **Questions:** Do SSMs give us frequency-native sequence mixing "for free," with mature open weights at
  small scale (130M–3B) ideal for the box tier? How well do they handle long context / associative recall
  (note the known SSM weakness on exact copying/recall — relevant to memory!)? Could an SSM backbone +
  ENGRAM external memory be the pragmatic frequency-native foundation? Which open SSM checkpoints are best
  to start from, and under what license?
- **Return:** an assessment of SSMs as the base, the recall-weakness caveat, and the best small open SSM
  checkpoint(s) to prototype with.

### V3 — Prior art III: associative-memory & VSA/holographic models (ENGRAM's natural substrate)
- **Questions:** Survey architectures where **associative/holographic memory is first-class** — the
  closest thing to "ENGRAM-native." **Modern Hopfield Networks / Hopfield Layers** (Ramsauer et al. —
  attention *is* a Hopfield update, exactly ENGRAM's `resonance.py`), **Holographic Reduced
  Representations / VSA / Hyperdimensional Computing** integrated with deep nets (Plate; HRR embeddings;
  "Lego"/HRR-transformer work), **Product-Key Memory** (Lample), **Neural Turing Machines / DNC**,
  **Kanerva machines / sparse distributed memory**. How close is each to natively supporting HRR binding
  (`vsa.py`) + Hopfield retrieval (`resonance.py`) + the composed self-shape (`compose.py`)? Has anyone
  built an LM whose *core* memory is VSA/holographic rather than a KV-cache?
- **Return:** the associative-memory architectures most aligned with ENGRAM, what they prove, and which
  primitives we could lift directly (since we already implement Hopfield + HRR).

### V4 — The representation bridge: the tokenization / "alphabet" problem
- **Questions:** Text models ingest discrete BPE tokens; ENGRAM speaks continuous spectral fingerprints.
  How do fingerprints *enter and exit* a model? Survey **continuous/patch input** (ViT patch embeds,
  **Perceiver IO** cross-attending arbitrary modalities), **neural audio codecs** as the "fixed alphabet
  of notes" (**EnCodec, SoundStream, DAC**, residual-VQ; **VQ-VAE** codebooks — directly echoing the
  project's "frozen codebook of notes" idea), and **byte/patch-level** models (MegaByte, **BLT** —
  Byte-Latent Transformer) as a route away from BPE. Design the **fingerprint ⇄ model** seam: project
  `.eng` certs (amplitude + GDF phase) into the model's latent space and decode cues back for ENGRAM
  retrieval. How does the two-senses split (separate spaces) map onto input channels/heads?
- **Return:** the recommended input/output representation for fingerprints, whether to adopt a VQ
  "note codebook," and the concrete fingerprint↔latent bridge spec.

### V5 — PATH 1 in depth: take a tiny base model and train it upward (frequency-grafted)
- **Questions:** If we grow from a small model: which **open small base** is the best substrate — a
  token model (**SmolLM2-135M/360M, Qwen2.5-0.5B, Pythia-160M, TinyLlama**) or a small **Mamba/RWKV**
  checkpoint (favored by V2)? What does "train it upward with the frequency design" concretely mean —
  **continued pretraining** with fingerprint-augmented context, **adapters/LoRA** for the bridge,
  **curriculum** (text → +memory tokens → +resonance objectives), auxiliary losses that reward correct
  retrieval/composition? Estimate **compute/data/time** for a meaningful run on a solo+cloud budget.
  What capability could we realistically get, and what's the failure mode (the graft doesn't change how
  it *reasons*, only what it *reads*)?
- **Return:** the recommended base checkpoint + the train-up recipe (method, data, objectives, schedule)
  + a concrete compute/cost estimate + the expected capability and the honest risk.

### V6 — PATH 2 in depth: rethink the transformer — frequency + ENGRAM native from scratch
- **Questions:** Design the **minimum viable frequency-native architecture** where ENGRAM is the memory,
  not an add-on: spectral/SSM mixing layers (from V1/V2) + a **Hopfield/VSA memory module** as a
  first-class component (resonance = retrieval, HRR binding = composition, training-free `.eng` writes).
  What is the smallest such model that is *useful*? What training data and scale does greenfield need to
  beat the null hypothesis? Honest assessment of the **greenfield tax** — frontier models cost millions;
  what can a solo builder actually reach, and is a *narrow* creature-mind (not a general chatbot) a fair,
  achievable target that sidesteps the scale war? What's the long-term iteration story if this is the
  foundation?
- **Return:** a concrete minimal architecture sketch (layers, the native memory module, I/O), the scale
  needed to be useful, the data/compute reality, and a sober go/no-go on greenfield for a solo maker.

### V7 — PATH 3: the hybrid / distillation middle path (the pragmatic third option)
- **Questions:** Keep a strong pretrained **token reasoner** but make memory frequency-native around it,
  or **distill** it into a frequency-native student. Options: a frozen LLM reasoner + ENGRAM frequency
  memory via the V0 bridge (hybrid); **distillation** of a big teacher into a small SSM/spectral student
  (note license limits on distillation); a **two-brain** split mirroring the two senses — a fast
  frequency-native REFLEX model on the robot + a slow token reasoner on the box, with ENGRAM as the
  shared memory bus. Which hybrid maximizes capability-per-dollar while still delivering ENGRAM's
  continual-learning/no-forgetting edge?
- **Return:** the best hybrid configuration, what it buys vs Paths 1/2, distillation feasibility +
  license caveats, and how it maps to the robot/box two-tier.

### V8 — Continual learning & the catastrophic-forgetting case (ENGRAM's real edge)
- **Questions:** ENGRAM's strongest argument is **training-free, updatable memory** — learn new
  situations without gradient updates or forgetting. Survey the continual-learning / lifelong-learning
  literature and where external frequency memory wins over fine-tuning (catastrophic forgetting,
  test-time/online learning, episodic memory, complementary-learning-systems theory — hippocampus
  (fast, episodic) vs neocortex (slow, consolidated), which the two senses literally mirror). Does this
  reframe the whole question — i.e., the base model stays mostly frozen and *all* plasticity lives in
  ENGRAM? What's the "**sleep/consolidation**" mechanism (replay frequency memories to slowly update the
  slow model)?
- **Return:** the continual-learning justification for each path, whether plasticity should live in
  memory vs weights, and a concrete consolidation ("sleep") design.

### V9 — Evaluation: how would we even know it's working? (don't fool ourselves)
- **Questions:** Define the **experiment ladder** and metrics that validate or *falsify* each path,
  before we spend compute. Probes for: memory recall fidelity (retrieve the right `.eng`), long-horizon /
  many-session recall, continual learning without forgetting, **compositionality** (query the self-shape
  by label), resonance-vs-kNN retrieval quality, and on-device latency/energy. What public benchmarks
  apply (long-context, associative-recall e.g. MQAR, continual-learning suites) and what **bespoke
  creature-mind probes** do we need? How to avoid benchmark-gaming (the project's standing rule). What's
  the **smallest decisive experiment** that tells us bridge-vs-train-up-vs-rebuild?
- **Return:** the metric set + the staged experiment ladder (cheap→expensive) + the single smallest
  experiment that most reduces our uncertainty.

### V10 — Feasibility, licensing, cost & the decision
- **Questions:** Roll it up. For each path (0/1/2/3): **compute** (GPU-hours, can it run on rented
  H100s/consumer GPUs), **data** (what corpus, how much), **time**, **license** (open-weights/arch,
  distillation rights), **risk** vs the null hypothesis, and **iterability** for a multi-year project.
  Where does each path run in the two-tier (robot REFLEX / box MEANING)? Produce a **recommended path +
  staged plan** with explicit decision gates (e.g., "bridge first; if probe X fails, attempt SSM
  train-up; pursue greenfield only if Y").
- **Return:** the comparison table across all paths on the rubric + the recommended path + a staged,
  gated roadmap with costs.

---

## OUTPUT — Return Format (per vector)
```
### V# — <title>
FINDING: what the evidence actually shows in 3–6 sentences (the conclusion, not a reading list).
RUBRIC SCORE: N _/5 · M _/5 · C _/5 · I _/5 · R _/5 · H _/5  (+ one line: why)
PRIOR ART: work — venue/date — scale (params/tokens) — result — reproduced? — open weights/license — link
ENGRAM-FIT: how it does/doesn't support frequency repr + HRR composition + Hopfield resonance + training-free updates
PATH IMPACT: what this implies for Path 0 (bridge) / 1 (train-up) / 2 (greenfield) / 3 (hybrid)
NULL-HYPOTHESIS TEST: would this actually beat "small token LLM + ENGRAM retrieval"? on what axis, with what evidence?
COST/COMPUTE: realistic budget to try it on a solo+cloud setup
RISKS / OPEN QUESTIONS / CONFIDENCE + the smallest experiment to resolve them
```

## FINAL SYNTHESIS — the deliverable
1. **Prior-art verdict** — does a frequency-native and/or ENGRAM-native base model/framework already
   exist? Name the closest candidates (likely among SSMs, spectral mixers, Hopfield/VSA models) with an
   honest maturity read.
2. **The path decision** — a ranked recommendation across Path 0 (bridge) / 1 (small-model train-up) /
   2 (greenfield rearchitecture) / 3 (hybrid-distill), scored on the rubric, with the reasoning.
3. **The architecture sketch** for the recommended path — backbone, the native/bridged memory module
   (Hopfield resonance + HRR composition + the fingerprint I/O), and where the two senses live.
4. **The experiment ladder** — cheapest-decisive-first, with metrics and falsification criteria, and the
   single smallest experiment to run next.
5. **Cost, license & two-tier deployment** — budget per path, open-weights/license traps, and what runs
   on the robot (REFLEX) vs the box (MEANING).
6. **The honest boundary** — what is proven vs speculative, where we'd knowingly bet ahead of the
   evidence, and the kill-criteria for each path. Keep the real spectral/associative-memory science;
   drop the mysticism.

---

## SEED SEARCH TERMS
`FNet Fourier token mixing` · `GFNet global filter network` · `Fourier neural operator FNO AFNO language` ·
`Hyena hierarchy implicit long convolution LM` · `H3 state space language model` · `Performer FAVOR
random Fourier features attention` · `SpectFormer wavelet transformer` · `S4 S4D S5 structured state
space` · `Mamba Mamba-2 selective state space` · `RWKV v7 architecture` · `state space model associative
recall MQAR weakness` · `Modern Hopfield networks attention Ramsauer` · `Hopfield layers pytorch` ·
`Holographic Reduced Representations transformer` · `vector symbolic architecture deep learning
hyperdimensional` · `product key memory Lample` · `Neural Turing Machine DNC differentiable memory` ·
`Kanerva sparse distributed memory neural` · `RETRO retrieval transformer` · `kNN-LM nearest neighbor
language model` · `Memorizing Transformers` · `Recurrent Memory Transformer RMT` · `Larimar episodic
memory LLM` · `LongMem memory augmented` · `Perceiver IO continuous inputs` · `EnCodec SoundStream DAC
neural audio codec tokens` · `VQ-VAE residual vector quantization codebook` · `Byte Latent Transformer
BLT MegaByte tokenizer-free` · `SmolLM2 Qwen2.5 0.5B Pythia small base model` · `Mamba 130M open
checkpoint` · `continual learning catastrophic forgetting external memory` · `complementary learning
systems hippocampus neocortex replay` · `test-time training online learning LLM` · `distillation small
language model license` · `long context associative recall benchmark`.

## INTERNAL CONTEXT (read these first — build on them)
- **The memory we're serving:** `research/reports/unified/frequency_memory__UNIFIED.md`,
  `SOLVING_AI_MEMORY_WITH_FREQUENCY_AND_SYMPHONY.md`, `MUSIC_AND_FREQUENCY_CONCEPTS.md`.
- **The implemented ENGRAM (lift primitives directly):** `vector_engram/sense.py` (two senses),
  `fingerprint.py` (FFT + GDF phase), `resonance.py` (Modern Hopfield), `vsa.py` (HRR + random
  projection + JL), `compose.py` (Identity/SelfModel self-shape), `CAPACITY_RESULTS.md` (the capacity gate),
  `CHANGELOG.md` (the build story).
- **The model/runtime landscape:** `research/reports/unified/cutting_edge_oss__UNIFIED.md`.
- **Where the reasoner runs:** the two-tier split — `research/BENZY_VECTOR_3_DESIGN_SPEC.md` (robot
  REFLEX / dock MEANING) + the C++/Go/Python runtime plan (`vector_brain/ARCHITECTURE.md`,
  `curation/vector_brain_stack.md`).
- **Doctrine:** the honesty boundary (keep real DSP/VSA/Hopfield/SSM science; drop frequency
  pseudoscience); the null hypothesis must be beaten, negative results kept.

---

*The point of this geodesic is to decide, with evidence, what mind ENGRAM should live inside — and
whether that mind already exists, can be grown, must be built, or is best distilled. Honest about cost,
honest about the null hypothesis. — 2026-06-26*
