# ENGRAM × Frequency-Native Reasoning: A Decision, Not a Survey

## TL;DR

- **No base model today is both frequency-native AND ENGRAM-native.** The closest real artifacts are state-space models (Mamba-2, RWKV-7) — frequency-native in the precise sense that their long-convolution kernels ARE spectral operators — and modern Hopfield/HRR layers, which make associative memory first-class. But nobody has shipped a language model whose *core* memory is VSA/holographic rather than a KV-cache. ENGRAM’s training-free FFT fingerprints + Hopfield cleanup remain genuinely differentiated whitespace.
- **The decision is Path 0 → Path 3, not Path 1 or 2.** Build the bridge first: a frozen small LLM (Qwen2.5-0.5B or SmolLM2-360M) + a small Flamingo-style cross-attention adapter that injects ENGRAM fingerprints as memory tokens, with ENGRAM’s Hopfield resonance doing retrieval outside the model. This costs roughly $1–$30 and is decisive. Reserve an SSM small-model train-up (Path 1, on Mamba-130m / RWKV-7) only if a specific probe fails; greenfield (Path 2) is a no-go for a solo builder.
- **The honest edge is continual learning, not raw IQ.** ENGRAM’s win is training-free, updatable, no-forgetting memory — exactly where fine-tuning fails (catastrophic forgetting). Frame the whole system as Complementary Learning Systems: frozen reasoner = neocortex, ENGRAM = hippocampus, with a “sleep” replay path to optionally consolidate. The two senses (REFLEX raw-FFT / MEANING embedding-FFT) map cleanly onto robot vs box tiers.

-----

## Key Findings

1. **Frequency-native sequence mixing already exists and is mature — but as token mixers, not memory.** FNet replaces the self-attention sublayer with a standard, unparameterized Fourier Transform and “achieves 92-97% of the accuracy of BERT counterparts on the GLUE benchmark, but trains 80% faster on GPUs and 70% faster on TPUs at standard 512 input lengths” (Lee-Thorp et al., NAACL 2022). GFNet (learned global filters in the Fourier domain) and AFNO (adaptive Fourier neural operator) extend this. Hyena (implicit long convolutions, FFT-evaluated) reaches “Transformer quality with a 20% reduction in training compute required at sequence length 2K,” and is “100× faster at sequence length 64K” (Poli et al., ICML 2023), at the 335M–1.3B scale. The “frequency” in these is load-bearing for efficiency but incidental to memory — and all are encoder/vision-first, not autoregressive LM backbones.
1. **State-space models are the de-facto frequency-native LM family with the best open checkpoints.** A long convolution is a frequency-domain operator; HiPPO initialization is a spectral basis; Mamba-2’s State Space Duality proves SSMs and (linear) attention are two views of the same structured-matrix operation. Open Apache-2.0 checkpoints exist at exactly the box-tier scale: `state-spaces/mamba-130m/370m/790m/1.4b/2.8b` and `mamba2` equivalents (trained on 300B tokens of the Pile), and RWKV-7 “Goose” (0.19B–2.9B, Apache-2.0, a Linux Foundation AI project).
1. **SSMs have a documented, decision-relevant weakness: exact copying / associative recall.** Jelassi, Brandfonbrener, Kakade & Malach (ICML 2024, “Repeat After Me”) prove “that a two layer transformer can copy strings of exponential length while GSSMs are fundamentally limited by their fixed-size latent state… transformer models dramatically outperform state space models at copying and retrieving information from context.” The Zoology/MQAR study (Arora et al., arXiv:2312.04927) finds “82% of the gap is explained by each model’s ability to recall information that is previously mentioned in-context… a 70M parameter attention model outperforms a 1.4 billion parameter gated-convolution model,” with SoTA gated-convs still trailing attention “by up to 2.1 perplexity points on the Pile.” This matters directly: a pure-SSM reasoner would be WORSE at the recall ENGRAM needs — which argues for keeping attention (or an explicit Hopfield memory) in the loop.
1. **Associative-memory-native primitives are real and liftable.** Modern Hopfield Networks (Ramsauer et al., ICLR 2021, “Hopfield Networks is All You Need”) prove attention IS a Hopfield update — exactly what ENGRAM’s resonance module implements — with exponential storage capacity, one-step retrieval, and a ready PyTorch `Hopfield` layer (`ml-jku/hopfield-layers`). The Hrrformer (Alam et al., ICML 2023) recasts self-attention as Holographic Reduced Representations with FFT as the core binding operation: “O(T H log H) time complexity, O(T H) space complexity, and convergence in 10× fewer epochs… able to learn with just a single layer… up to 280× faster to train on the Long Range Arena benchmark.” This is the single most ENGRAM-aligned published architecture — same circular-convolution / FFT math ENGRAM already uses.
1. **The bridge path has strong, recent precedent.** Larimar (IBM, ICML 2024) bolts a distributed episodic memory onto a frozen LLM enabling one-shot, training-free knowledge updates with selective forgetting, “yielding speed-ups of 8-10x depending on the base LLM” (e.g., memory read of 0.36s vs 1.44s for a Mistral-7B base) — a direct analogue of “ENGRAM as plug-in memory.” Memorizing Transformers, kNN-LM, RETRO, LongMem, and Memformer establish that external memory via (cross-)attention reliably extends capability without retraining the backbone. Flamingo-style gated cross-attention (freeze the LLM, train only inserted adapter blocks) is the canonical “inject external embeddings into a frozen LLM” recipe.
1. **The tokenization seam is solvable without BPE.** Fingerprints are continuous spectral vectors; routes in are Perceiver-IO-style cross-attention over arbitrary modalities, ViT-style patch embedding, or a VQ “note codebook” (EnCodec/DAC residual vector quantization, which already discretize signals into a fixed alphabet via RVQ).  Byte Latent Transformer (Meta, Dec 2024) shows a route entirely away from fixed vocabularies.  ENGRAM’s two-senses split maps naturally onto separate input channels/adapters that are never cross-compared.
1. **Cost is not the barrier for the bridge.** At 2025–2026 rates (realistic on-demand H100 ≈ $2–$3.50/GPU-hr — RunPod ~$1.99, Lambda ~$2.49–$3.29, AWS P5 ~$3.90 after its June 2025 price cut; marketplace/spot as low as ~$1–$1.49 on Vast.ai), a Flamingo-style cross-attention adapter or LoRA on a frozen sub-3B model is a single-GPU, 1–12 hour job costing roughly $1–$30 (cf. QLoRA on a single A100 80GB at ~$8 total; QLoRA on one H100 8–12 hr ≈ $10–$16). Continued-pretraining a sub-1B model on hundreds of millions to a few billion tokens is ~$20–$300 (cf. nanoGPT GPT-2-124M reproduction ≈ $20; a 125M model continued-pretrained on 400M→1B tokens with MMLU +8.1% on modest compute, Faroz, April 2025). Full from-scratch SmolLM2-scale training (~$250K; the 1.7B alone used 384 H100s for 24 days) is the thing to avoid — and the bridge lets you avoid it.

-----

## Details — Per-Vector Findings

### V0 — The seam question: do we even need a new base model?

**FINDING:** No — not for the near term. A frozen reasoner can consume ENGRAM fingerprints via a small trained cross-attention adapter (fingerprint → memory tokens) while ENGRAM’s Hopfield network does retrieval externally, and this is well-precedented by Larimar (training-free one-shot memory writes on a frozen LLM), Memorizing Transformers (kNN-augmented attention),  and Flamingo (frozen LLM + gated cross-attention to injected embeddings). What’s lost vs native: resonance and HRR composition happen *outside* the reasoner, so the model can’t natively reason *in* the associative geometry — it reads memory, it doesn’t think in it. That is acceptable until a probe shows compositional queries over the self-shape require in-model binding.
**RUBRIC:** N 2/5 · M 5/5 · C 5/5 · I 4/5 · R 2/5 · H 5/5 — memory is bolted on (low N) but evidence and cost are excellent and risk is low.
**PRIOR ART:** Larimar — ICML 2024 — LLM-agnostic episodic memory, 8–10× faster edits — open (`github.com/IBM/larimar`). Memorizing Transformers — ICLR 2022 — kNN memory to 262K tokens.  RETRO — DeepMind 2022 — trillion-token retrieval, GPT-3-level at 25× fewer params.  kNN-LM, LongMem, Memformer (3.2× faster, 8.1× less memory). 
**ENGRAM-FIT:** Excellent for fingerprint I/O and training-free updates; weak for in-model resonance/composition.
**PATH IMPACT:** This IS Path 0; de-risks Paths 1/3; makes Path 2 unnecessary near-term.
**NULL-HYPOTHESIS TEST:** This essentially *is* the null hypothesis (“small token LLM + ENGRAM retrieval”) with a learned adapter — so it sets the bar others must beat.
**COST:** ~$1–$30 single GPU.
**SMALLEST EXPERIMENT:** Train the adapter; measure retrieval-augmented recall vs raw in-context.

### V1 — Spectral / Fourier-domain neural architectures

**FINDING:** Frequency-domain mixing is mature for efficiency but no production autoregressive LM backbone is built on pure FFT mixing. Ranked by LM-readiness + native-fit: (1) Hyena (implicit long convolutions, FFT-evaluated, reached Transformer quality at 335M–1.3B; the 1.3B model reached ~10.8 perplexity after 5B Pile tokens); (2) AFNO/FNO (principled Fourier operator, vision/PDE-proven, not LM); (3) FNet/GFNet (encoder/vision, FFT token mixing, not autoregressive). The most credible frequency-native LM backbones for ENGRAM are actually SSMs (V2) and the Hrrformer (V3), not these vision mixers.
**RUBRIC:** N 3/5 · M 4/5 · C 3/5 · I 3/5 · R 3/5 · H 5/5 — real and load-bearing but no LM-grade backbone to adopt directly.
**PRIOR ART:** FNet — NAACL 2022 — BERT-scale — 92–97% GLUE, 80% faster — open. GFNet — NeurIPS 2021 — vision — open (`raoyongming/GFNet`). AFNO — ICLR 2022 — vision/PDE — open.  Hyena — ICML 2023 — up to 1.3B — Pile-competitive — open.
**ENGRAM-FIT:** FFT mixing is conceptually aligned but these don’t provide associative memory or HRR binding.
**PATH IMPACT:** Informs Path 2 layer design; not a drop-in backbone.
**NULL TEST:** Would not beat the null on memory; only on long-context efficiency.
**COST:** N/A as adopt-directly; would require greenfield training.

### V2 — State-space models as the de-facto frequency-native family

**FINDING:** SSMs are the best available frequency-native substrate with mature open small checkpoints. Mamba-2’s State Space Duality formally connects SSM long-convolution kernels (spectral operators) to attention; HiPPO init is a spectral basis. BUT the known SSM weakness — exact copying / associative recall from a compressed fixed state — is precisely ENGRAM-relevant, because memory systems live or die on recall. RWKV-7 (“Goose,” Apache-2.0, 0.19B–2.9B) materially improves recall via its generalized delta rule and is a test-time-training in-context learner (it can recall 72.93% at one MQAR setting with only an 8192 WKV state), yet RWKV’s own docs admit weakness on lookback/review tasks.
**RUBRIC:** N 4/5 · M 4/5 · C 4/5 · I 5/5 · R 3/5 · H 5/5 — frequency-native “for free,” open, cheap to start, but recall weakness is a real risk.
**PRIOR ART:** Mamba-2 — ICML 2024 — to 2.7B — Pareto-dominant vs Transformer++ — Apache-2.0 (`state-spaces/mamba2-130m…2.7b`). RWKV-7 — 2025 — 0.19–2.9B — 3B multilingual SoTA on fewer tokens — Apache-2.0.  Jelassi et al. — ICML 2024 — copying limitation. Zoology/MQAR — Arora et al. — AR explains 82% of the recall gap; a 70M attention model beats a 1.4B gated-conv on AR.
**ENGRAM-FIT:** Native frequency mixing; the recall weakness *argues for* keeping ENGRAM’s Hopfield cleanup as the recall organ rather than relying on SSM state.
**PATH IMPACT:** Best Path 1 substrate (Mamba-130m / RWKV-7-0.4B); also the REFLEX-tier model.
**NULL TEST:** Beats null on on-device efficiency/latency and continual learning if paired with external memory; LOSES on pure recall unless augmented.
**COST:** Continued-pretrain 130m–370m: ~$20–$300.
**SMALLEST EXPERIMENT:** Run MQAR on the candidate SSM at your fingerprint sequence lengths before committing.

### V3 — Associative-memory & VSA/holographic models (ENGRAM’s natural substrate)

**FINDING:** This is where ENGRAM is least alone and most validated. Modern Hopfield Networks prove attention = Hopfield update (ENGRAM’s resonance module is therefore principled, not ad hoc), with exponential storage capacity and one-step retrieval. The Hrrformer is the single most ENGRAM-aligned published model: it implements attention as HRR binding with FFT at its core — the same circular-convolution math ENGRAM uses — learns in a single layer with 10× fewer epochs, and is up to 280× faster to train on Long Range Arena. Product-Key Memory, DNC/NTM, and Kanerva / sparse-distributed-memory provide additional liftable primitives. But: nobody has shipped a full LM whose *core* memory is VSA/holographic instead of a KV-cache. That is ENGRAM’s actual whitespace.
**RUBRIC:** N 5/5 · M 3/5 · C 3/5 · I 4/5 · R 3/5 · H 5/5 — maximal native-fit; medium maturity (components proven, full LM not).
**PRIOR ART:** Modern Hopfield — ICLR 2021 — open (`ml-jku/hopfield-layers`). Hrrformer — ICML 2023 — LRA near-SOTA, FFT-based — open. HDC/VSA two-part survey (Kleyko et al., 2022–2023, ACM Computing Surveys). Generalized HRR (2024). Product-Key Memory (Lample et al., 2019).
**ENGRAM-FIT:** Direct — HRR binding = composition, Hopfield = resonance, FFT = fingerprint. Lift the Hopfield layer and Hrrformer binding directly.
**PATH IMPACT:** Core of Path 2; supplies the memory module for Paths 1/3.
**NULL TEST:** Beats null on compositionality and capacity IF the capacity finding (random projection + cleanup) is respected.
**COST:** Hopfield/HRR layers are cheap to integrate; a full greenfield LM is not.

### V4 — The representation bridge: tokenization / “alphabet” problem

**FINDING:** Feed fingerprints in as continuous memory tokens via cross-attention (Perceiver-IO / Flamingo pattern), not via BPE. Project each `.eng` cert (amplitude + GDF phase) through a small MLP into the model’s latent dimension; decode cues back out through a symmetric head for ENGRAM to retrieve against. The two senses (REFLEX raw-FFT, MEANING embedding-FFT) become two separate adapters / channel sets that are never cross-compared, preserving the separate-cosine-spaces invariant. A VQ “note codebook” (EnCodec/DAC RVQ) is optional and only worth adopting if you want a discrete, finite alphabet for the reasoner to emit — defer it.
**RUBRIC:** N 4/5 · M 4/5 · C 4/5 · I 4/5 · R 2/5 · H 5/5 — well-trodden continuous-input machinery, low risk.
**PRIOR ART:** Perceiver IO (DeepMind 2021). Flamingo gated cross-attention (2022). EnCodec/SoundStream/DAC RVQ. Byte Latent Transformer (Meta, Dec 2024) — tokenizer-free, scales to 8B. 
**ENGRAM-FIT:** Preserves two-senses separation and training-free fingerprints; respects the capacity finding if the projection is high-D.
**PATH IMPACT:** Defines the I/O seam for every path.
**NULL TEST:** Enables the null/bridge to function at all.
**COST:** Part of the ~$1–$30 adapter budget.

### V5 — PATH 1: take a tiny base model and train it upward

**FINDING:** Viable as a fallback, not a first move. Best substrate: a small Mamba/RWKV-7 checkpoint (frequency-native) OR a token model (Qwen2.5-0.5B / SmolLM2-360M) if you want strong language priors. “Train upward” = continued pretraining with fingerprint-augmented context + adapters for the bridge + curriculum (text → +memory tokens → +resonance/retrieval auxiliary losses). Realistic failure mode: the graft changes what the model READS, not how it REASONS — you get a model that ingests fingerprints but still reasons token-by-token. Achievable on a solo+cloud budget but more expensive and riskier than the bridge.
**RUBRIC:** N 4/5 · M 3/5 · C 3/5 · I 4/5 · R 4/5 · H 5/5 — better native-fit than the bridge but higher risk it doesn’t change reasoning.
**PRIOR ART:** Domain-adaptive continued pretraining of a 125M model on 400M→1B tokens (Faroz, April 2025) — MMLU +8.1%, HellaSwag +7.6% on modest compute. SmolLM2 (Feb 2025). Mamba/RWKV-7 checkpoints.
**ENGRAM-FIT:** Good if auxiliary losses reward correct retrieval/composition.
**PATH IMPACT:** This is Path 1; triggered only if Path 0 probes fail.
**NULL TEST:** Must beat the bridge on compositionality/continual-learning to justify cost.
**COST:** ~$20–$300 continued pretraining of a sub-1B model.
**SMALLEST EXPERIMENT:** Continued-pretrain Mamba-130m with fingerprint memory tokens + retrieval loss; compare to the frozen-bridge on the same probes.

### V6 — PATH 2: greenfield frequency + ENGRAM-native from scratch

**FINDING:** No-go for a solo builder as a general model; possibly justified ONLY as a narrow “creature-mind.” A minimum-viable frequency-native architecture = spectral/SSM mixing layers + a Hopfield/HRR memory module as a first-class component (resonance = retrieval, HRR = composition, training-free `.eng` writes). The “greenfield tax” is severe: you forfeit all pretrained language priors and must beat the null with a from-scratch run. Full SmolLM2-scale pretraining is ~$250K — out of reach. A *narrow* creature-mind (not a chatbot) that never needs broad world knowledge is a fair, achievable target that sidesteps the scale war, but even this should follow, not precede, a working bridge.
**RUBRIC:** N 5/5 · M 2/5 · C 1/5 · I 4/5 · R 5/5 · H 5/5 — maximal native-fit, minimal evidence at scale, highest cost/risk.
**PRIOR ART:** Hrrformer + Mamba/Hyena layers + Hopfield layers as building blocks; no integrated precedent.
**ENGRAM-FIT:** Perfect by construction.
**PATH IMPACT:** This is Path 2; pursue only after the bridge + train-up both prove the concept, and only for a narrow domain.
**NULL TEST:** Hardest to beat the null; only wins if narrow-domain continual learning + composition decisively outperform.
**COST:** $1K–$10K+ even for a small narrow model; high variance.
**GO/NO-GO:** No-go now. Revisit only if Paths 0/1 validate the science and a narrow domain is defined.

### V7 — PATH 3: hybrid / distillation middle path

**FINDING:** This is the destination. Keep a strong pretrained token reasoner, make memory frequency-native around it (the V0 bridge), and split into two brains mirroring the two senses: a fast frequency-native REFLEX model (Mamba-130m / RWKV-7-0.4B) on the robot, a slow token reasoner (Qwen2.5-0.5B–3B) on the box, with ENGRAM as the shared memory bus. Optionally distill the box reasoner into a smaller SSM student over time — but watch license traps (some model licenses restrict using outputs to train other models). This maximizes capability-per-dollar while delivering ENGRAM’s continual-learning / no-forgetting edge.
**RUBRIC:** N 4/5 · M 4/5 · C 4/5 · I 5/5 · R 2/5 · H 5/5 — best balance; the recommended steady state.
**PRIOR ART:** Larimar (frozen LLM + episodic memory). Retrieval-aware SSM distillation work (2025–2026). Llamba/Mamba distillation.
**ENGRAM-FIT:** Excellent; ENGRAM is the shared plastic memory across both tiers.
**PATH IMPACT:** This is Path 3; the target architecture.
**NULL TEST:** Beats null on two-tier efficiency + continual learning.
**COST:** Bridge cost + optional distillation (~$100–$1000).

### V8 — Continual learning & the catastrophic-forgetting case (ENGRAM’s real edge)

**FINDING:** This reframes the entire question. ENGRAM’s strongest argument is training-free, updatable memory: learn new situations without gradient updates or forgetting. Complementary Learning Systems theory (McClelland, McNaughton & O’Reilly, 1995)  maps directly: hippocampus = fast/episodic  (ENGRAM, the MEANING/REFLEX senses), neocortex = slow/consolidated (the frozen reasoner). The base model stays frozen; ALL plasticity lives in ENGRAM. A “sleep/consolidation” mechanism = replay frequency memories to optionally, slowly update the slow model via generative replay (proven to reduce catastrophic forgetting).  This is the axis on which every path should be judged.
**RUBRIC:** N 5/5 · M 4/5 · C 5/5 · I 5/5 · R 1/5 · H 5/5 — strongest, best-evidenced, cheapest differentiator.
**PRIOR ART:** CLS theory (McClelland et al., 1995, Psychological Review). Sleep-replay reduces forgetting (Tadros et al., Nature Communications 2022). Generative replay (Shin et al. 2017; van de Ven 2020/2022). Larimar selective forgetting. Titans (test-time memory, NeurIPS 2025). 
**ENGRAM-FIT:** This IS ENGRAM’s thesis, externally validated.
**PATH IMPACT:** Justifies freezing the reasoner (Paths 0/3) over expensive retraining (Paths 1/2).
**NULL TEST:** Decisively beats fine-tuning baselines on no-forgetting / online learning.
**COST:** Near-zero (replay is cheap).

### V9 — Evaluation: how would we know it’s working?

**FINDING:** Build a cheapest-decisive-first experiment ladder. Probes: (1) memory recall fidelity — retrieve the right `.eng` (top-k accuracy); (2) long-horizon / many-session recall; (3) continual learning without forgetting (sequential tasks, measure backward transfer); (4) compositionality — query the self-shape by label (HRR unbinding accuracy); (5) resonance-vs-kNN retrieval quality; (6) on-device latency/energy on the robot tier. Public benchmarks: MQAR/Zoology (associative recall), needle-in-haystack / long-context, standard continual-learning suites (Split-MNIST-style backward transfer). Bespoke creature-mind probes are needed because public benchmarks don’t test self-shape composition. Avoid benchmark-gaming by holding out probe sets and reporting negative results.
**RUBRIC:** N/A (methodology) · H 5/5.
**SMALLEST DECISIVE EXPERIMENT:** With the frozen bridge, run an associative-recall + continual-learning probe: write N fingerprints, interleave distractor sessions, then test retrieval + composition accuracy vs (a) a raw in-context baseline and (b) a fine-tuned baseline on forgetting. If the bridge wins on no-forgetting and matches on recall, Path 0/3 is validated and you never need Path 1/2.

### V10 — Feasibility, licensing, cost & the decision

**FINDING:** Path 0 (bridge) and Path 3 (hybrid) are the answer; Path 1 is a gated fallback; Path 2 is shelved. Licensing is favorable: Qwen2.5 (0.5B–3B, Apache-2.0), SmolLM2 (Apache-2.0), Mamba/Mamba-2 checkpoints (Apache-2.0),  RWKV-7 (Apache-2.0, Linux Foundation).  The main license trap is distillation rights — verify the teacher’s license permits training students on its outputs before any Path-3 distillation. Two-tier: REFLEX (raw-FFT, fast) = small SSM on the robot; MEANING (embedding-FFT, slow) = token reasoner + bridge on the mains-powered box; ENGRAM is the shared memory bus.
**RUBRIC:** N/A (rollup).
**COST SUMMARY:** Bridge ~$1–$30; SSM train-up ~$20–$300; distillation ~$100–$1000; greenfield $1K–$10K+. H100 on-demand ~$2–$3.50/hr, spot ~$1–$1.49.

-----

## Recommendations — Staged, Gated Plan

**Stage 0 (now, ~$1–$30, days): Build the bridge.** Freeze Qwen2.5-0.5B (or SmolLM2-360M) on the box. Train a small Flamingo-style gated cross-attention adapter that ingests ENGRAM fingerprints (amplitude + GDF phase, high-D random-projected per the capacity finding) as memory tokens. Keep ENGRAM’s Hopfield resonance doing retrieval externally. Keep the two senses as two separate adapters that never cross-compare. *Benchmark to beat:* raw in-context retrieval and a fine-tuned baseline.

**Gate A:** Run the V9 smallest-decisive experiment (associative recall + continual-learning-without-forgetting + self-shape composition).

- If the bridge matches recall AND wins on no-forgetting → proceed to Stage 1 (productionize Path 3). **You are done with the architecture question.**
- If compositional queries over the self-shape fail (HRR unbinding accuracy low) → this is the trigger for deeper integration: go to Stage 2.

**Stage 1 (Path 3 steady state, ~$0–$1000): Two-brain hybrid.** Put a frequency-native REFLEX SSM (Mamba-130m or RWKV-7-0.4B) on the robot, the token reasoner + bridge on the box, ENGRAM as the shared bus. Add the CLS “sleep” replay path: optionally consolidate frequent memories into the slow model via generative replay. Optionally distill the box reasoner into a smaller SSM student (check the teacher license first).

**Stage 2 (Path 1 fallback, ~$20–$300, only if Gate A composition fails): SSM train-up.** Continued-pretrain Mamba-130m / RWKV-7 with fingerprint memory tokens + retrieval/composition auxiliary losses. *Before spending:* run MQAR at your fingerprint sequence lengths — if the SSM can’t do associative recall there, keep attention in the loop.
**Gate B:** Train-up must beat the Stage-0 bridge on compositionality to justify its cost. If not, revert to Path 3.

**Stage 3 (Path 2, shelved): Greenfield narrow creature-mind.** Pursue ONLY if (a) Paths 0/1 validate the science, (b) you can define a narrow domain that needs no broad world knowledge, and (c) you accept $1K–$10K+ and high risk. Build from Hrrformer binding + Mamba/Hyena mixing + Hopfield memory layers.

**Thresholds that change the plan:** SSM MQAR failure → keep attention. Distillation license restriction → no distillation, keep the frozen reasoner. Bridge shows no no-forgetting advantage → re-examine whether ENGRAM’s edge is real (kill-criterion for the whole thesis).

-----

## Architecture Sketch (Recommended: Path 0 → Path 3)

- **Backbone (box / MEANING tier):** Frozen Qwen2.5-0.5B–3B (Apache-2.0, open). Strong language priors, no retraining, no forgetting.
- **Reflex (robot / REFLEX tier):** Mamba-130m or RWKV-7-0.4B (Apache-2.0), frequency-native long-conv mixing, constant memory, fast on-device.
- **Memory module (ENGRAM, native):** FFT fingerprints (training-free) → high-D random projection (capacity finding) → Modern Hopfield network for resonance/retrieval (= attention-as-Hopfield) → HRR binding for self-shape composition (Hrrformer-style circular convolution).
- **Seam:** Per-sense cross-attention adapters (Perceiver/Flamingo pattern) project fingerprints → memory tokens; a symmetric decode head emits cues ENGRAM retrieves against. REFLEX and MEANING adapters are separate and never cross-compared.
- **Plasticity:** ALL learning lives in ENGRAM (write new `.eng`, no gradients). Optional CLS “sleep” replay consolidates into the slow model.

-----

## Cost, License & Two-Tier Deployment

|Path              |Compute          |$ Estimate|License                                     |Runs where                           |
|------------------|-----------------|----------|--------------------------------------------|-------------------------------------|
|0 Bridge          |1 GPU, 1–12 hr   |$1–$30    |Qwen / SmolLM2 / Mamba / RWKV all Apache-2.0|Box (MEANING)                        |
|1 SSM train-up    |1 GPU–small node |$20–$300  |Mamba / RWKV Apache-2.0                     |Box; small SSM → robot               |
|3 Hybrid + distill|bridge + optional|$100–$1000|check distillation rights of teacher        |Robot (REFLEX) + box (MEANING)       |
|2 Greenfield      |days–weeks       |$1K–$10K+ |own architecture                            |Box (then port narrow model to robot)|

H100 on-demand ≈ $2–$3.50/GPU-hr (RunPod ~$1.99, Lambda ~$2.49–$3.29, AWS P5 ~$3.90 post June-2025 cut); spot/marketplace as low as ~$1–$1.49 (Vast.ai). QLoRA on a single H100 ≈ 8–12 hr / $10–$16.

-----

## The Honest Boundary

**Proven:** FFT/spectral token mixing works (FNet 92–97% of BERT GLUE at 80% faster; GFNet; AFNO; Hyena Pile-competitive with 20% less compute, 100× faster at 64K). SSMs are frequency-native with open small Apache-2.0 checkpoints (Mamba-2, RWKV-7). Attention = Hopfield update (Ramsauer, ICLR 2021). HRR-as-attention works with FFT at its core (Hrrformer, 10× fewer epochs, 280× faster on LRA). Frozen-LLM + external memory works (Larimar 8–10× faster edits; Memorizing Transformers; RETRO). Continual-learning-via-external-memory beats fine-tuning on forgetting (CLS theory; generative replay). SSMs are genuinely worse at exact recall (Jelassi ICML 2024; Zoology — AR explains 82% of the gap, 70M attention > 1.4B gated-conv).

**Speculative / betting ahead of evidence:** That ENGRAM’s *specific* FFT fingerprints + GDF phase outperform learned embeddings for a reasoner is unproven — test it. That a frozen reasoner can reason compositionally *in* the associative geometry via a bridge alone (vs needing in-model binding) is the open question Gate A resolves. That a narrow greenfield creature-mind would beat the null is unproven and the riskiest bet.

**Kill-criteria:** (Path 0) bridge shows no no-forgetting advantage over fine-tuning → the core thesis is in doubt. (Path 1) SSM fails MQAR at your sequence lengths and can’t be fixed by mimetic init → don’t go pure-SSM. (Path 2) can’t define a narrow domain → don’t build greenfield. (Distillation) teacher license forbids it → skip.

**Dropped as mysticism (kept out, per the honesty boundary):** Schumann resonance, 432 Hz, any “vibrational” framing. The real science — wavelet scattering (Bruna & Mallat, invariant scattering convolution networks), HRR/VSA/hyperdimensional computing, Modern Hopfield networks, SSM/spectral operators (FNO, Mamba), random-Fourier-feature attention (Performer) — is retained and load-bearing.

-----

### Prior-art verdict (one line)

A frequency-native LM family exists (SSMs: Mamba-2, RWKV-7 — Apache-2.0, small open checkpoints) and an associative/holographic-memory-native primitive set exists (Modern Hopfield + Hrrformer, both FFT-grounded and directly liftable) — but **no single base model is both, and none makes training-free holographic memory its core.** ENGRAM’s thesis is therefore defensible; the right move is to bridge it onto a frozen token reasoner now (Path 0), settle into a two-brain hybrid (Path 3), and let one falsifiable experiment (Gate A) decide whether you ever need to go deeper.