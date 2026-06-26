# GEODESIC — A Frequency-Native Base Model for ENGRAM
**Dexter × Claude · 2026-06-26**

> *Does a base model exist (or an architecture) that thinks in the frequency domain and treats ENGRAM-style memory as native — and if not, what is the path?*

***

## Executive Summary

No single existing architecture is fully frequency-native **and** ENGRAM-native. The closest living candidates are: (1) **SSMs (Mamba-2, RWKV-7, DeltaNet)** — de facto frequency-domain sequence mixers with open small checkpoints; (2) **Modern Hopfield Networks / Hopfield Layers** — the exact mathematical basis of ENGRAM's `resonance.py`; and (3) nascent **VSA/HRR-in-transformers** work, still research-scale. The recommendation is a **staged hybrid**: start with **Path 0 (learned bridge)** immediately, pivot to **Path 3 (SSM backbone + Hopfield memory head)** after a probe validates retrieval fidelity, and treat Path 2 (greenfield) as a 2–3-year aspirational target if the project outgrows narrow creature-mind scope.

***

## V0 — The Seam Question: Do We Even Need a New Base Model?

### FINDING
A learned cross-attention **adapter** that projects ENGRAM `.eng` fingerprints (amplitude + GDF phase vectors) into a frozen LLM's latent space is technically feasible and is the cheapest near-term win. The pattern is well-established: RETRO uses chunked cross-attention over retrieved embeddings against a frozen backbone; LongMem adds a decoupled SideNet that reads 65k-token memory into a frozen LLM via a single memory-augmented cross-attention layer; Memorizing Transformers add a kNN external memory with softmax over cached key-value pairs; Larimar (IBM/Princeton, ICML 2024) attaches a distributed episodic memory to a frozen LLM enabling one-shot knowledge writes without retraining. The critical limitation for ENGRAM: these approaches let the *frozen reasoner* consume retrieved content, but the model still reasons in token-space. Hopfield resonance (the dot-product energy minimisation over stored patterns) and HRR binding (circular convolution) are not performed *inside* the model's compute graph — they happen in ENGRAM's external modules and only the *result* (a retrieved embedding) passes through the bridge. Composition benefits and resonance-vs-kNN quality differences are therefore not first-class to the model.[^1][^2][^3][^4][^5][^6][^7][^8]

### RUBRIC SCORE
N 2/5 · M 5/5 · C 5/5 · I 3/5 · R 1/5 · H 5/5
*N is low because memory is bolted on, not native; everything else is excellent — proven, cheap, safe.*

### PRIOR ART
| Work | Venue/Date | Scale | Result | Repro? | License | Link |
|------|-----------|-------|--------|--------|---------|------|
| RETRO | DeepMind, Dec 2021 | 7B params, 2T token DB | GPT-3 parity at 25× fewer params | Yes (multiple) | Research only | [^1] |
| Memorizing Transformers | Google Brain, Mar 2022 | 53M–8B + kNN cache | ~3× perplexity drop at 65k ctx | Partial | Research | [^7] |
| LongMem | NeurIPS 2023 | 65k token window | +5–10 PPL vs base | Limited | Research | [^5] |
| Larimar | ICML 2024 (IBM/Princeton) | Frozen LLM + episodic mem | One-shot knowledge update, no retrain | Partial | Apache 2.0 (code) | [^2][^9] |
| RMT | 2022 | Segment-level recurrent | 2M+ effective context | Partial | Open | [^10] |

### ENGRAM-FIT
The bridge can be implemented as: (a) a small projection MLP (`fingerprint_projector`: R^N → R^d_model) that maps `.eng` amplitude+phase into the model's embedding space, plus (b) a cross-attention layer injecting up to *K* retrieved fingerprints as soft memory tokens before the model's main context. The **two-senses split** maps cleanly onto two parallel cross-attention heads (REFLEX channel, MEANING channel) gated by inference time. However, HRR binding and Hopfield resonance are pre-computed outside — the model only sees cosine-nearest vectors after retrieval, not the energy landscape.

### PATH IMPACT
**Path 0 is the mandatory first step.** It costs almost nothing, risks nothing, and provides real data on whether retrieval fidelity is the bottleneck or whether model reasoning is. If the bridge probe passes (see V9), Paths 1/2/3 may never be necessary.

### NULL-HYPOTHESIS TEST
The bridge *is* the null hypothesis. It adds retrieval to a stock token LLM and is the baseline every other path must beat.

### COST/COMPUTE
Adapter training on top of a frozen 360M–1.7B model: ~50–200 H100-hours at ~$1.50/hr (Vast.ai/RunPod) = **$75–$300 total**. The fingerprint projector is ~2–5M parameters.[^11][^12]

### RISKS / OPEN QUESTIONS
- Does the model attend to fingerprint-injected tokens reliably, or does it ignore them? (Test: probing accuracy of retrieval tokens in attention weights.)
- Does the model's token-space reasoning "understand" what a retrieved spectral fingerprint *means*, or just pattern-match on proximity?
- **Smallest decisive experiment**: inject ENGRAM-retrieved embeddings as prefix tokens into SmolLM2-360M and test whether answer accuracy on a crafted creature-mind QA set improves over a no-retrieval baseline. Run on a single H100 in under 4 hours.

***

## V1 — Prior Art I: Spectral / Fourier-Domain Neural Architectures

### FINDING
Five distinct Fourier-domain architectures exist; none is a deployable frequency-native *language model*. **FNet** (Google, 2021) replaces self-attention with an unparameterised DFT achieving 92–97% of BERT accuracy on GLUE at 80% faster training on GPUs — but it is an encoder-only classifier, not a generative LM. **GFNet** (global filter networks, 2021/2023) learns spatial frequency filters in the 2-D FFT of image patches — vision-only, no LM. **AFNO** (Adaptive Fourier Neural Operator) applies learned spectral mixing for high-resolution vision/PDE tasks — no language model. **Hyena Hierarchy** (Stanford HazyResearch, ICML 2023) constructs sub-quadratic long convolutions via implicit parametrisation, reaching attention quality at 220M parameters on language tasks with lower time complexity — closest to a usable spectral LM backbone. **SpectFormer** (Microsoft/Bath, 2023) combines spectral layers with attention heads in vision transformers, improving ImageNet top-1 by ~2% — vision-only. **FNetAR** (2021) extended FNet to autoregressive generation but is unpublished and tiny. The Performer/FAVOR+ uses random Fourier features to approximate softmax attention linearly — the Fourier kernel is incidental to capacity, not a deliberate frequency representation.[^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25]

### RUBRIC SCORE
N 2/5 · M 3/5 · C 4/5 · I 2/5 · R 3/5 · H 5/5
*The "frequency" in most of these is an efficiency trick, not a native representational commitment; Hyena is the closest exception.*

### PRIOR ART
| Work | Venue/Date | Scale | Result | Repro? | License |
|------|-----------|-------|--------|--------|---------|
| FNet | Google, NLP 2021 | BERT-scale (110M) | 92–97% BERT GLUE | Yes | Apache 2.0 |
| GFNet | NeurIPS 2021 / IEEE TPAMI 2023 | 15M–80M vision | ImageNet SoTA comparable | Yes | MIT |
| AFNO | ICLR-adjacent 2022 | FourCastNet (830M) | Weather SoTA | Yes | Open |
| Hyena | ICML 2023 | 153M–1B LM | Matches Transformer PPL at 2× speed | Partial | Apache 2.0 |
| SpectFormer | 2023 | 20M–100M vision | +2% ImageNet vs GFNet | Limited | Open |
| Performer | ICLR 2021 | 300M–540M | Linear attention, ~2% PPL gap | Yes | Apache 2.0 |

### ENGRAM-FIT
Hyena's long convolutions are computed in the frequency domain (FFT→multiply→iFFT), making its kernel inherently spectral — closer to ENGRAM's signal than vanilla attention. However, Hyena does not natively support training-free memory writes; its convolutional filters are *learned weights*, not dynamic associative stores. FNet's FFT is unparameterised and useful for fast mixing, but not for storing structured frequency fingerprints.

### PATH IMPACT
Hyena is the best spectral candidate for Path 1 (train-up substrate) if SSMs (V2) are rejected. For Path 2, an ENGRAM-native architecture would naturally inherit Hyena-style spectral mixing layers alongside Hopfield memory heads. Hyena's 153M Apache 2.0 checkpoint is a viable starting point.

### NULL-HYPOTHESIS TEST
Hyena has matched Transformer perplexity on language at ~1/3 compute cost, but has not been tested on associative recall or MQAR benchmarks — a key gap. The null hypothesis is not beaten unless Hyena's spectral mixing improves ENGRAM fingerprint recall quality.[^23]

### COST/COMPUTE
Continued pretraining of Hyena-153M on fingerprint-augmented text: ~200–500 H100-hours (~$300–$750 at spot rates).[^12]

***

## V2 — Prior Art II: State-Space Models as the De-Facto Frequency-Native Family

### FINDING
SSMs are the most mature frequency-adjacent architecture family and the pragmatic answer for a solo builder. **S4** (Stanford, NeurIPS 2021) parameterises the SSM kernel using HiPPO orthogonal polynomial bases — a spectral initialisation that makes the convolution kernel frequency-structured by construction. **S4D** diagonalises this with 2-line-of-code kernel computation. **Mamba** (selective SSM, Dec 2023) adds input-dependent state transitions, closing most of the Transformer gap on language; **Mamba-2** (2024) establishes the State Space Duality (SSD): an SSM with scalar-times-identity A matrix is exactly equivalent to a 1-semiseparable masked linear attention — meaning SSMs *are* linear-complexity frequency-domain operators. **RWKV-7 "Goose"** (2025) achieves new 3B SoTA on multilingual tasks with constant memory and expressive dynamic state evolution via a generalised Delta Rule. **IBM Granite 4.0** (Oct 2025) ships a production hybrid Mamba-2/Transformer with 70% memory reduction at 3B scale under Apache 2.0 — the strongest evidence that hybrid SSMs are viable at real scale. The **critical weakness**: SSMs have known struggles with exact associative recall (MQAR) due to their recurrent state compression — a direct concern for ENGRAM's retrieval quality. Recent work (2024–2025) shows this weakness is primarily an *optimisation* artefact (learning-rate sensitivity) and can be significantly mitigated with careful tuning and width-scaling, while DeltaNet solves MQAR to Transformer level by removing decay from the state transition matrix.[^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42][^43][^44]

### RUBRIC SCORE
N 3/5 · M 5/5 · C 5/5 · I 5/5 · R 2/5 · H 5/5
*Highly mature, real production deployments (Granite 4.0), cheap open checkpoints, frequency-domain by construction — but the MQAR recall weakness is a real risk for ENGRAM retrieval correctness.*

### PRIOR ART
| Work | Venue/Date | Scale (params/tokens) | Result | Repro? | License |
|------|-----------|----------------------|--------|--------|---------|
| S4 | NeurIPS 2021 | 8M–350M | Long-range arena SoTA | Yes | Apache 2.0 |
| Mamba-130M/370M | Dec 2023 | 130M/370M, Pile | Matches Transformer PPL | Yes | Apache 2.0 [^45][^46] |
| Mamba-2 | Jun 2024 | Up to 2.8B | +8× state size, SSD duality | Yes | Apache 2.0 [^31] |
| RWKV-7 "Goose" | Mar 2025 | 2.9B | 3B multilingual SoTA | Yes | Apache 2.0 [^35] |
| IBM Granite 4.0 | Oct 2025 | 3B–32B hybrid | 70% memory reduction | Yes | Apache 2.0 [^37] |
| DeltaNet | NeurIPS 2024 | 340M–1.3B | Solves MQAR to Transformer level | Partial | Apache 2.0 [^40] |
| Together Mamba-3B | Apr 2026 | 3B, 600B SlimPajama tokens | SSMs rival Transformers | Yes | Apache 2.0 [^47] |

### ENGRAM-FIT
The SSD equivalence means an SSM backbone already performs frequency-domain sequence mixing. The Mamba S6 layer can represent projections onto Haar wavelets — a direct bridge to ENGRAM's wavelet scattering in the MEANING sense. The HiPPO initialisation gives S4-family models a spectral basis matching different memory time-scales — analogous to ENGRAM's theta/gamma two-rate split. The SSM *state* is the de facto frequency memory, but it is a *compressed* recurrent state, not ENGRAM's explicit `.eng` certificate store. ENGRAM's external Hopfield retrieval must therefore remain as an *external* module, queried by the SSM backbone. DeltaNet's delta-rule update rule resembles a gradient descent on the SSM state — a potential write pathway for ENGRAM fingerprints without gradient descent on model weights.[^33]

### BEST CHECKPOINTS TO START WITH
- `state-spaces/mamba-130m` (130M, Apache 2.0, HuggingFace)[^45][^46]
- `state-spaces/mamba-370m` (370M, Apache 2.0)[^48]
- RWKV-7 2.9B (Apache 2.0)[^35]
- IBM Granite 4.0 Nano (350M–1B hybrid, Apache 2.0)[^49]

### NULL-HYPOTHESIS TEST
SSMs do not beat a stock token LLM on associative recall out of the box. They beat it on long-context throughput and memory efficiency. The benefit for ENGRAM would be: (a) the SSM's recurrent state naturally compresses frequency-like information, reducing the representational gap with ENGRAM fingerprints; (b) the SSM can run efficiently on-device (robot REFLEX tier). Beat condition: SSM + ENGRAM retrieval outperforms Transformer + same retrieval on long-horizon multi-session creature-mind recall benchmarks with identical parameter budgets.

### COST/COMPUTE
Continued pretraining of Mamba-370M on 5B fingerprint-augmented tokens: ~100–200 H100-hours ≈ **$150–$300** spot (Vast.ai ~$1.50/hr). Full pretraining of a 1–3B SSM from scratch: ~500–2000 H100-hours ≈ **$750–$3,000**.[^11][^12]

***

## V3 — Prior Art III: Associative-Memory & VSA/Holographic Models

### FINDING
This is ENGRAM's natural scientific substrate, and the foundational theory is mature. **Modern Hopfield Networks** (Ramsauer et al., ICLR 2021) prove that the transformer's attention update rule is *exactly* a modern Hopfield energy minimisation step — meaning ENGRAM's `resonance.py` (Hopfield retrieval) is already attention, just run against ENGRAM's stored patterns instead of KV caches. The `ml-jku/hopfield-layers` library provides drop-in PyTorch modules. **Learning with HRR** (NeurIPS 2021) and **Generalised HRR** (2024) integrate circular-convolution binding into deep networks. **LARS-VSA** (2024) builds a compositional hyperdimensional architecture with a novel HD attention mechanism, outperforming baselines on symbolic reasoning while being significantly more efficient. **Recasting Self-Attention with HRR** (2022) directly replaces attention with holographic operations — the most ENGRAM-aligned published work. **Product-Key Memory** (Lample, 2019) adds a large-capacity associative memory layer to transformers (up to 12B slots), used in LM pretraining at 30B tokens. **DNC/NTM** (DeepMind 2016) are full MANN architectures with external memory — mature but not LM-scale. **Kanerva's Sparse Distributed Memory** (SDM, 1988) is the theoretical ancestor: a content-addressable store over distributed binary addresses that directly prefigures ENGRAM's cosine similarity retrieval structure. No existing *production LM* uses VSA/holographic binding as its *core* memory mechanism. The closest attempted systems are research prototypes.[^50][^51][^52][^53][^54][^55][^56][^57][^58][^59][^60][^61][^62][^63][^64][^65][^66][^67]

### RUBRIC SCORE
N 5/5 · M 3/5 · C 3/5 · I 3/5 · R 2/5 · H 5/5
*Perfect native-fit because ENGRAM primitives are provably equivalent to these; maturity is moderate (good theory, limited LM-scale deployment); cost is intermediate.*

### PRIOR ART
| Work | Venue/Date | Scale | Proves | Open |
|------|-----------|-------|--------|------|
| Modern Hopfield (Ramsauer) | ICLR 2021 | Benchmark / 100M | Attention = Hopfield update | Yes (Apache 2.0) |
| Hopfield Layers (ml-jku) | 2020–ongoing | Drop-in PyTorch | Plug-and-play Hopfield attention | Yes (MIT) |
| NeurIPS 2021 HRR nets | NeurIPS 2021 | Small-scale | HRR binding in deep nets works | Yes |
| Recasting SA with HRR | 2022 | Small-scale | Attention replaceable with HRR | Limited |
| LARS-VSA | 2024 | Small-scale | HD binding improves compositional reasoning | Yes |
| Product-Key Memory | NeurIPS 2019 | 220M LM | Large associative memory in LM pretraining | Yes |
| DNC | DeepMind 2016 | RNN+memory | External differentiable memory | Yes |

### ENGRAM-FIT
This is the strongest theoretical alignment. ENGRAM's `resonance.py` is a Hopfield update; `vsa.py` is HRR binding; the random projection for capacity restoration (CAPACITY_RESULTS) is the standard VSA hyperdimensional trick; the cleanup memory is SDM retrieval. A model with native Hopfield + HRR memory would not require a bridge at all — it would *natively speak* the same mathematical language as ENGRAM. The specific design: replace the KV-cache with ENGRAM's `.eng` certificate store, where each memory write is a deterministic FFT fingerprint projected to a hyperdimensional space, and retrieval is a Hopfield energy minimisation over the stored patterns.

### PATH IMPACT
This family is the primary motivation for Path 2 (greenfield) and provides the memory module for Path 3. Hopfield Layers can be added to any existing SSM/Transformer backbone immediately (Path 0/1) — no new architecture required, just a new head.

### NULL-HYPOTHESIS TEST
Hopfield retrieval (ENGRAM's resonance) beats kNN by: exponential vs linear capacity scaling in theory; composition support (query the composed self-shape by label); and the ability to store overlapping patterns without interference at sufficient dimensionality. The question is whether this advantage materialises in practice at ENGRAM's operating capacity (as per CAPACITY_RESULTS). The random-projection path already addresses the raw-FFT correlation problem.[^54]

### COST/COMPUTE
Adding a Hopfield layer as a memory head to an existing backbone: ~2–5M extra parameters, negligible training cost. The dominant cost is building and maintaining the `.eng` certificate store and the cleanup memory index.

***

## V4 — The Representation Bridge: The Tokenisation / "Alphabet" Problem

### FINDING
The tokenisation gap is bridgeable but requires a deliberate design decision. Four strategies exist, in order of invasiveness:

**Strategy A — Projection adapter (cheapest).** A linear or small MLP maps ENGRAM fingerprint vectors (amplitude + GDF phase, e.g. R^2048) into the model's d_model space (R^512–R^2048) before cross-attention injection. This is the V0 bridge. The two-senses (REFLEX / MEANING) can enter as separate prefix token sequences gated by a sense-selector token. Cost: minimal; loss: the model never *learns* spectral structure, only approximate semantic proximity.

**Strategy B — VQ "note codebook" (recommended for Path 1).** Inspired by EnCodec/SoundStream RVQ, train a Residual Vector Quantiser over ENGRAM fingerprints to produce a discrete "note alphabet" of K codebook entries. This is the project's "frozen codebook of notes" idea. Fingerprints become sequences of codebook indices, which the LM can treat as tokens. The RVQ multi-scale structure mirrors ENGRAM's theta (slow/MEANING) and gamma (fast/REFLEX) layers. A fingerprint codebook of 4096 entries × 8 residual levels requires ~10M parameters to train. Matching the "music grammar" thesis, this approach gives the model a fixed, interpretable "alphabet" of spectral patterns. RVQ codebooks are trained independently from the LM, so fingerprint granularity can be updated without retraining the reasoner.[^68][^69][^70][^71][^72]

**Strategy C — Byte/patch-level model (no BPE).** Meta's **BLT** (Byte Latent Transformer, ACL 2025) processes raw byte sequences with dynamic entropy-based patching, matching LLaMA-3 with up to 50% fewer inference FLOPs. A fingerprint-native BLT variant would treat the raw FFT amplitude array as a byte stream and patch it dynamically by spectral entropy — i.e., high-variance frequency bins become fine-grained patches, smooth regions become coarse. This is conceptually elegant and avoids the codebook training step but requires pretraining a new model on fingerprint-enriched data.[^73][^74]

**Strategy D — Perceiver IO (maximum flexibility).** Cross-attend arbitrary modalities including ENGRAM's continuous spectral arrays directly. Highest native-fit but highest engineering overhead.[^75][^76][^77]

### RUBRIC SCORE
N 3/5 (Strategy B) · M 4/5 · C 4/5 · I 4/5 · R 2/5 · H 5/5

### RECOMMENDED DESIGN
**Use Strategy A for Path 0 immediately; build Strategy B (RVQ codebook) in parallel for Path 1.** The codebook approach:
1. Collect 10M+ ENGRAM fingerprints from synthetic and real data.
2. Train a 4096 × 8 RVQ on the fingerprint distribution (~20 H100-hours).
3. Use codebook indices as tokens in the model's vocabulary (extend tokeniser by 4096 entries).
4. The REFLEX sense uses lower RVQ levels (coarser, faster); MEANING uses all 8 levels (fine-grained, slower).
5. The model can now natively read and generate fingerprint sequences as token streams.

### TWO-SENSES MAPPING
| Sense | Domain | RVQ levels | Input channel | Latency target |
|-------|--------|-----------|--------------|---------------|
| REFLEX (raw-FFT) | Amplitude spectrum | 1–2 (coarse) | Separate prefix sequence, fast | <10ms (robot) |
| MEANING (embedding-FFT) | Embedding spectrum | All 8 (fine) | Separate prefix sequence, slow | <100ms (box) |

The two sequences *never cross* in cosine space (project doctrine preserved).

***

## V5 — PATH 1 IN DEPTH: Take a Tiny Base Model and Train It Upward

### FINDING
Path 1 is the **recommended short-to-medium-term build path** (6–18 months). The core recipe: start from **Mamba-370M** (Apache 2.0, state-spaces), extend the vocabulary with RVQ fingerprint codebook tokens (V4 Strategy B), and run a three-phase curriculum:[^48]

**Phase 1 — Adapter injection (1–2 weeks, ~$200).** Freeze Mamba backbone; train a fingerprint_projector (R^fingerprint_dim → R^d_model) and cross-attention Hopfield head using ENGRAM retrieval pairs. Validate bridge probe (V9) before proceeding.

**Phase 2 — Continued pretraining (2–4 weeks, ~$1,500–$3,000).** Unfreeze the model; run on a mixed corpus of text + fingerprint-augmented context (fingerprints inserted as codebook-token sequences alongside text descriptions of the creature-mind situations that generated them). Target: 5–20B tokens. Auxiliary losses: retrieval correctness (cross-entropy over codebook prediction), resonance quality (Hopfield energy minimisation objective), composition consistency (retrieved composed self-shape matches labelled self-shape).

**Phase 3 — Resonance fine-tuning (1–2 weeks, ~$300).** Fine-tune only the Hopfield memory head on ENGRAM retrieval pairs. Validate with MQAR-style creature-mind probe.

**Why Mamba-370M over token alternatives (SmolLM2, Qwen2.5-0.5B, Pythia-160M)?**
- Mamba's SSM kernel is a frequency-domain operator (frequency-native fit, V2)[^28][^33]
- Its recurrent state naturally accumulates spectral information over context
- Apache 2.0, open weights, no distillation prohibition[^46][^45]
- SmolLM2-360M (Apache 2.0, trained on 4T tokens) is the best *token* alternative — stronger general reasoning at equal size, worse frequency-native fit[^78][^79][^80]
- Qwen2.5-0.5B (Apache-like, strong 32k context) is excellent for text but pure token model[^81]
- Pythia-160M (Apache 2.0, EleutherAI) is useful for interpretability ablations due to 154 partially-trained checkpoints[^82][^83]

**Expected capability:** A creature-mind reasoner that can: (a) store new situations as ENGRAM fingerprints in real time without weight updates; (b) retrieve and compose past situations via resonance; (c) reason over the frequency-native codebook with a reasoning quality intermediate between a pure retrieval system and a full LLM. It will *not* be a general chatbot and should not be evaluated as one.

**Failure mode:** The continued pretraining grafts new token types onto the model but does not change the *model's internal reasoning style*. The SSM still processes sequences recurrently; it does not perform Hopfield energy minimisation internally. Retrieval correctness may not propagate into better downstream reasoning.

### RUBRIC SCORE
N 3/5 · M 4/5 · C 4/5 · I 4/5 · R 2/5 · H 5/5

### COST ESTIMATE (REALISTIC SOLO BUDGET)
| Phase | Compute | Cost (Vast.ai spot ~$1.50/hr H100) |
|-------|---------|-------------------------------------|
| RVQ codebook training | ~20 H100-hrs | ~$30 |
| Phase 1: adapter | ~50 H100-hrs | ~$75 |
| Phase 2: continued pretraining (5B tokens) | ~300–500 H100-hrs | ~$450–$750 |
| Phase 3: resonance fine-tune | ~50 H100-hrs | ~$75 |
| **Total Path 1** | **~420–620 H100-hrs** | **~$630–$930** |

For 20B tokens (deeper pretraining): ~$2,000–$3,500. Well within solo budget.[^84][^12][^11]

### RISKS
- The graft may not change reasoning quality meaningfully (the model sees new tokens but doesn't understand them differently)
- Mamba's MQAR weakness may limit retrieval correctness at high memory density (mitigated by DeltaNet-style fixes or external Hopfield head)
- Data: need sufficient fingerprint-annotated creature-mind scenarios (synthetically generatable from ENGRAM's `sense.py`)

***

## V6 — PATH 2 IN DEPTH: Rethink the Transformer — Frequency + ENGRAM Native from Scratch

### FINDING
Path 2 is architecturally correct but financially and strategically premature for a solo builder. The **minimum viable frequency-native architecture** design:

```
Input: [text tokens | fingerprint RVQ tokens | sense-type token]
    ↓ (token embedding + sense embedding)
[SSM mixing layers × L_ssm] ← frequency-domain sequence mixing (Mamba-2/S4D)
    ↓
[Hopfield Memory Head] ← stores/retrieves .eng fingerprints via energy minimisation
    ↓                    (resonance.py logic embedded in architecture)
[VSA Binding Layer] ← HRR composition (circular convolution over hyperdimensional states)
    ↓
[SSM mixing layers × L_out]
    ↓
Output: [text tokens | fingerprint RVQ tokens]
```

**Scale needed to be useful:** A creature-mind reasoner (not general LM) at ~300M–1B parameters with 20–100B tokens of domain-specific pretraining. At this scale the model would *natively* understand the "music grammar" — frequency fingerprints are first-class computational objects, not injected tokens.

**Greenfield tax for a solo builder:** Training a 500M-parameter model on 20B tokens costs ~500–2000 H100-hours (~$750–$3,000 spot). Training a 1B model on 100B tokens costs ~5,000–20,000 H100-hours (~$7,500–$30,000). These figures are feasible *if compute is amortised over many months and run in stages*. The harder problem is **data**: a frequency-native LM needs a corpus that includes both natural language and fingerprint-annotated data in sufficient density for the model to develop cross-modal understanding. Constructing this corpus is a months-long engineering project.[^84]

**The narrow creature-mind escape hatch:** A model that is *not* a general LM but only understands the creature-mind domain (robot sensorimotor, session memory, self-shape composition) can be trained on much less data. 1–5B tokens of domain-specific data + ENGRAM fingerprints may suffice for a useful narrow model. This sidesteps the scale war entirely.

**Long-term iteration story:** Greenfield is the best foundation *if* the creature-mind domain is the permanent target. The architecture is permanently extensible: add modality heads (audio, vision), grow the `.eng` certificate store without retraining, add new VSA binding operations for new relationship types. No external model licence constrains the build.

### RUBRIC SCORE
N 5/5 · M 2/5 · C 2/5 · I 5/5 · R 3/5 · H 5/5
*Perfect native-fit and best long-term foundation; the cost and maturity scores are low because this is research-grade work with no proven instantiation at this exact design.*

### GO/NO-GO FOR SOLO MAKER
**No-go for 0–12 months.** Yes-go as a 12–36 month aspirational target *after* Path 0 proves retrieval fidelity and Path 1 proves the SSM backbone's compatibility with ENGRAM fingerprints. The trigger: if the Path 1 graft demonstrably fails to change reasoning quality (not just retrieval accuracy), that is the green light for greenfield.

***

## V7 — PATH 3: The Hybrid / Distillation Middle Path

### FINDING
Path 3 is the **recommended medium-term architecture** (12–24 months, overlapping Path 1). It consists of two components:

**Component A — Frozen/lightly-trained token reasoner (box / MEANING tier).** Keep a strong pretrained small LLM (SmolLM2-1.7B or Qwen2.5-0.5B/1.5B) as the slow reasoning engine. Augment with the V0 bridge (cross-attention over ENGRAM-retrieved embeddings). This component handles language, planning, and high-level composition. License: both Apache 2.0.[^85][^78][^81]

**Component B — SSM/spectral REFLEX model (robot / REFLEX tier).** A Mamba-370M or RWKV-7 small checkpoint trained up per Path 1 as the fast frequency-native processor. Handles: real-time sensor fingerprinting (REFLEX sense), immediate resonance retrieval from ENGRAM, quick habitual pattern responses. Latency: sub-10ms on device.

**ENGRAM as the shared memory bus:** Both components read from and write to the same `.eng` certificate store. The MEANING reasoner reads composed self-shapes; the REFLEX model reads raw fingerprints. The two-senses split maps cleanly onto two-tier deployment.

**Distillation option:** Distil a strong token LLM (e.g. Llama-3.1-8B) into a small SSM/spectral student. **Caution:** Llama-3 uses a non-commercial-for-distillation licence (Meta's licence prohibits training *new* models on Llama outputs for competing services). Mistral models have similar restrictions. Safe distillation targets: Pythia series (EleutherAI, Apache 2.0), SmolLM2 (Apache 2.0), Qwen2.5 (commercial-permissive but check downstream). Distillation of token→SSM students has been demonstrated at small scale but not published for the specific spectral+memory use case; treat as ~40% risk.[^86]

**The two-brain split (Benzy three-body design mapping):**
| Tier | Model | Sense | Memory access | Latency | Hardware |
|------|-------|-------|---------------|---------|----------|
| Robot (REFLEX) | Mamba-130M trained up | REFLEX (raw-FFT) | `.eng` raw fingerprints | <10ms | On-device ARM/NPU |
| Box (MEANING) | SmolLM2-1.7B + bridge | MEANING (embedding-FFT) | `.eng` composed self-shapes | <100ms | Box GPU (RTX 4060 or better) |
| Cloud (optional) | Larger LLM (if needed) | Text only | ENGRAM summary | <1s | Rented H100 |

### RUBRIC SCORE
N 3/5 · M 4/5 · C 4/5 · I 4/5 · R 2/5 · H 5/5
*Good capability-per-dollar, clear two-tier fit, moderate native-fit because the MEANING reasoner still thinks in tokens.*

### COST ESTIMATE
| Component | Cost |
|-----------|------|
| Path 1 SSM train-up (REFLEX model) | ~$630–$930 |
| Bridge adapter for MEANING model | ~$150–$300 |
| **Total Path 3** | **~$800–$1,230** |

No distillation required — uses open pretrained weights + bridge + trained-up REFLEX model.

***

## V8 — Continual Learning & the Catastrophic-Forgetting Case

### FINDING
ENGRAM's strongest architectural argument is that **all plasticity lives in the memory, not the weights**. This reframes the entire question. The base model (any path) stays mostly frozen after initial training; it is ENGRAM's `.eng` store that accumulates new knowledge. This maps precisely onto the **Complementary Learning Systems (CLS) theory** of hippocampus (fast, episodic, one-shot encoding) and neocortex (slow, distributed, consolidation): ENGRAM is the hippocampus; the base model is the neocortex. New experiences are stored immediately as ENGRAM fingerprints (hippocampal fast learning); the base model is only updated during offline "sleep" consolidation.[^87][^88][^89][^90]

**Catastrophic forgetting** in standard fine-tuning is severe: empirical studies show 1B–7B models exhibit significant forgetting during continual instruction tuning. External memory systems (ENGRAM-style) are the clearest solution — new knowledge is written to the memory store without touching model weights, and forgetting is architecturally impossible for stored memories (subject to CAPACITY_RESULTS limits).[^91][^92][^93][^94]

**Sleep/consolidation design:** The slow consolidation process (neocortex update) can proceed as follows:
1. During "sleep" windows (idle periods), sample K `.eng` fingerprints from recent ENGRAM sessions.
2. Reconstruct natural language or sensorimotor descriptions from the fingerprints (using the MEANING model itself — "replay").
3. Run lightweight LoRA fine-tuning on the base model using these reconstructed texts as training examples.
4. Update the base model's internal representations to reflect the accumulated ENGRAM experiences without catastrophic forgetting (use EWC or LoRA-only updates on new parameters).

**NeurIPS 2024 "Continual Learning in the Frequency Domain"**  directly validates frequency-domain representations for continual learning: wavelet-transformed features show substantially reduced catastrophic forgetting and improved accuracy on edge devices — a direct empirical support for ENGRAM's frequency-domain encoding approach.[^95][^96][^97]

### RUBRIC SCORE
N 5/5 · M 4/5 · C 4/5 · I 5/5 · R 1/5 · H 5/5
*ENGRAM's training-free memory is uniquely suited to the continual learning problem; this is ENGRAM's decisive edge over any fine-tuning approach.*

### PATH IMPACT
- **Path 0/3:** The frozen/lightly-trained model accumulates no new knowledge in weights; all session-to-session persistence lives in ENGRAM. This is a feature, not a limitation.
- **Path 1:** Same; the SSM backbone is trained once, then frozen. ENGRAM provides all online adaptation.
- **Path 2:** Greenfield model inherits the same design principle — weights are largely frozen post-training; ENGRAM is the dynamic memory.
- **Consolidation trigger:** After N new `.eng` certificates exceed a novelty threshold (cosine distance from existing clustered fingerprints), queue a sleep consolidation run.

***

## V9 — Evaluation: How Would We Even Know It's Working?

### FINDING
The experiment ladder must be cheap-decisive-first and must falsify each path, not just confirm it.

### Metric Set

**Core metrics (path-agnostic):**
| Metric | What it tests | Benchmark / probe |
|--------|-------------|-------------------|
| Fingerprint recall fidelity (FR@K) | Does the model retrieve the right `.eng` given a query? | ENGRAM internal MQAR-style probe |
| Long-horizon multi-session recall (LH-MSR) | Are fingerprints from 10+ sessions ago still retrievable? | Bespoke creature-mind recall suite |
| Continual learning (CL-Δ) | Does adding 100 new fingerprints degrade recall of the first 100? | CAPACITY_RESULTS gate + recall test |
| Compositionality (Comp-SQ) | Can a query "retrieve the self-shape containing X AND Y" return the correct composed fingerprint? | `compose.py` label probe |
| Resonance vs kNN (Δ-R/kNN) | Does Hopfield resonance beat cosine-kNN on composed or noisy queries? | Held-out ENGRAM test set |
| On-device latency | REFLEX model: <10ms? MEANING model: <100ms? | Wall-clock benchmark on target hardware |
| Null-hypothesis beat | Does Path N outperform "SmolLM2-360M + ENGRAM kNN retrieval" on creature-mind QA? | Creature-mind QA set (bespoke) |

**Public benchmarks that apply:**
- MQAR (Multi-Query Associative Recall) — tests associative recall depth, directly tests ENGRAM retrieval quality[^32][^98][^99]
- Long Range Arena — tests long-context sequence mixing (SSM advantage)
- Continual learning suites (e.g. Split-CIFAR101 adapted to creature-mind scenarios)

**Anti-gaming rules:** All probes use held-out fingerprints generated after the model checkpoint was frozen. No data leakage between training and eval `.eng` stores. The null hypothesis baseline is always run at identical parameter count and compute budget.

### The Experiment Ladder (cheapest-decisive-first)

| Step | Experiment | Cost | Falsifies |
|------|-----------|------|-----------|
| E0 | Inject top-K ENGRAM retrieval embeddings as prefix tokens into SmolLM2-360M; test creature-mind QA accuracy vs no-retrieval baseline | 2–4 H100-hrs (~$5) | Whether *any* bridge is useful |
| E1 | Run MQAR benchmark on Mamba-370M vs SmolLM2-360M at equal parameter count, with ENGRAM-retrieved context | 4–8 H100-hrs (~$10) | Whether SSM backbone gives better retrieval than token model |
| E2 | Train RVQ codebook on 1M ENGRAM fingerprints; test reconstruction fidelity (PSNR, cosine similarity) | 20 H100-hrs (~$30) | Whether fingerprints can be quantised without critical information loss |
| E3 | Continued pretraining of Mamba-370M on 1B fingerprint-augmented tokens; run FR@K, Comp-SQ, Δ-R/kNN | 100 H100-hrs (~$150) | Whether train-up improves reasoning quality beyond retrieval accuracy |
| E4 | Add Hopfield memory head (ml-jku hopfield-layers) to Mamba-370M; compare Hopfield vs kNN retrieval on composed fingerprints | 50 H100-hrs (~$75) | Whether native Hopfield head beats external kNN |
| E5 | Sleep consolidation pilot: replay 500 recent fingerprints as reconstructed text; LoRA fine-tune; measure CL-Δ | 20 H100-hrs (~$30) | Whether consolidation mechanism can update base model without forgetting |
| E6 (optional) | Greenfield 150M model: SSM + Hopfield head + VSA binding; train on 5B creature-mind tokens; compare to SmolLM2-360M bridge | 300–500 H100-hrs (~$600) | Whether greenfield is worth the cost vs Path 1 |

**The single smallest decisive experiment: E0.** Total cost: ~$5–$15, runtime: 2–4 hours on a single H100. This directly tests whether the bridge strategy can deliver value before any further investment.

***

## V10 — Feasibility, Licensing, Cost & The Decision

### Path Comparison on the Rubric

| Path | Description | N | M | C | I | R | H | Total | Two-tier fit |
|------|------------|---|---|---|---|---|---|-------|-------------|
| **Path 0** — Bridge (adapter over frozen LLM) | Best immediate win | 2 | 5 | 5 | 3 | 1 | 5 | **21/30** | Box only |
| **Path 1** — SSM train-up (Mamba-370M + RVQ) | Recommended medium-term | 3 | 4 | 4 | 4 | 2 | 5 | **22/30** | Both tiers |
| **Path 2** — Greenfield (SSM+Hopfield+VSA) | Long-term aspiration | 5 | 2 | 2 | 5 | 3 | 5 | **22/30** | Both tiers |
| **Path 3** — Hybrid (SSM REFLEX + token MEANING) | Recommended 12–24mo | 3 | 4 | 4 | 4 | 2 | 5 | **22/30** | Both tiers ✓ |

*Paths 1/2/3 tie on raw score; the differentiator is cost, timing, and risk.*

### Recommended Path: Staged Gated Roadmap

```
NOW (0–3 months): Path 0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Build fingerprint_projector adapter (~2M params)
• Cross-attention injection into frozen SmolLM2-360M
• Run E0 probe: does retrieval improve creature-mind QA?
• Cost: ~$150–$300 total
• GATE 0: if E0 accuracy ≥ 20% above no-retrieval baseline → proceed
• GATE 0 fail: the bridge is not the bottleneck; the model cannot
  reason about spectral structure → skip directly to Path 1

3–12 months: Path 1 (parallel with Path 0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Train RVQ codebook on ENGRAM fingerprints (E2)
• Continued pretraining of Mamba-370M (5–20B tokens, $630–$3,500)
• Add Hopfield memory head (E4)
• GATE 1: if Mamba-370M + Hopfield head beats SmolLM2-360M + bridge
  on FR@K AND Comp-SQ with identical compute budget → commit to
  SSM backbone as permanent foundation
• GATE 1 fail: SSM doesn't help; stay with token backbone + bridge

12–24 months: Path 3 (if GATE 1 passes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Deploy Mamba-130M (REFLEX tier, robot) + SmolLM2-1.7B (MEANING
  tier, box) + ENGRAM as shared memory bus
• Implement sleep consolidation (E5)
• Total additional cost: ~$300–$500

24–36 months: Path 2 (if Path 3 shows reasoning quality plateau)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Greenfield 300M–1B creature-mind model: SSM + Hopfield + VSA
• Train on 20–100B creature-mind tokens (~$5,000–$30,000 amortised)
• GATE 2 trigger: Path 3 hits a hard capability ceiling that cannot
  be resolved by more ENGRAM fingerprints — only then is greenfield
  justified
```

### License Summary

| Model | License | Distillation safe? | Notes |
|-------|---------|-------------------|-------|
| Mamba-130M/370M | Apache 2.0 | Yes | state-spaces/mamba[^47][^100] |
| RWKV-7 | Apache 2.0 | Yes | Full open[^34][^35] |
| SmolLM2-360M/1.7B | Apache 2.0 | Yes | HuggingFace[^78][^85] |
| Qwen2.5-0.5B/1.5B | Qwen licence (commercial permissive) | Check version | Not Apache[^81] |
| Pythia series | Apache 2.0 | Yes | EleutherAI[^82][^83] |
| Larimar (IBM) | Apache 2.0 (code) | Yes (code, not weights) | Weights gated[^101] |
| IBM Granite 4.0 | Apache 2.0 | Yes | Full open weights[^37] |
| Hopfield Layers (ml-jku) | MIT | Yes | Drop-in[^57] |
| Llama-3.x | Meta licence | **No (for new model training)** | Distillation prohibited |

### Two-Tier Deployment Map

| Component | Tier | Hardware | Path |
|-----------|------|----------|------|
| REFLEX model (Mamba-130M trained-up) | Robot | ARM/NPU on-device | Path 1/3 |
| ENGRAM REFLEX sense + `.eng` write | Robot | On-device memory | All paths |
| MEANING model (SmolLM2-1.7B + bridge) | Box | RTX 4060 Ti (16GB) | Path 0/3 |
| ENGRAM MEANING sense + Hopfield retrieval | Box | Box GPU | All paths |
| Sleep consolidation | Box (idle) | Same box GPU | Path 3+ |
| Optional larger reasoner | Cloud | Rented H100 | Optional |

***

## Final Synthesis

### 1. Prior-Art Verdict

No frequency-native *and* ENGRAM-native base model exists in deployable form. The closest living candidates are:

- **SSMs (Mamba-2, RWKV-7, DeltaNet, IBM Granite 4.0):** Frequency-native by construction (SSD equivalence to linear attention, HiPPO spectral initialisation), production-deployable, Apache 2.0, mature. **Not** ENGRAM-native — no built-in Hopfield retrieval or HRR binding. Maturity: 5/5.
- **Hopfield Layers (ml-jku):** Exactly ENGRAM's resonance.py in PyTorch, plug-and-play, MIT licence. Not a full LM backbone. Maturity: 4/5.
- **Hyena Hierarchy:** The only spectral LM backbone with published language modelling results; explicitly computes in frequency domain. Not ENGRAM-native. Maturity: 3/5.
- **VSA/HRR-in-transformers (LARS-VSA, Generalised HRR):** ENGRAM's natural mathematical substrate; most aligned with vsa.py + compose.py. Research-scale only. Maturity: 2/5.

The gap that needs closing is: combine SSM frequency mixing + Hopfield memory head + HRR binding layer into a unified architecture. All three components exist independently as open-source, well-understood building blocks. They have not been integrated at LM scale.

### 2. Path Decision

**Ranked recommendation:**
1. **Path 0 (bridge) — Do this week.** ~$150–$300, 2–4 hours to first result, zero risk.
2. **Path 1 (SSM train-up) — Do in parallel.** ~$630–$3,500, 6–18 months, correct frequency-native direction.
3. **Path 3 (hybrid, two-tier) — The target state at 12–24 months.** ~$800–$1,230, maximises capability-per-dollar, maps perfectly to robot/box deployment.
4. **Path 2 (greenfield) — Long-term aspiration.** ~$5,000–$30,000, 2–3 years, only justified if Path 3 hits a hard ceiling.

### 3. Architecture Sketch (Path 3 — Recommended Target)

```
ROBOT TIER (REFLEX):
  Input: raw sensor stream
  Model: Mamba-130M (trained up, Apache 2.0)
  Memory: ENGRAM .eng write (raw-FFT fingerprint, immediate, training-free)
  Retrieval: cosine kNN → REFLEX candidates → Hopfield energy check (fast)
  Output: reflexive action + fingerprint ID
  Latency: <10ms

BOX TIER (MEANING):
  Input: REFLEX fingerprint IDs + text context
  Embedding model: any (MiniLM, BGE, etc.)
  Model: SmolLM2-1.7B (Apache 2.0) + fingerprint_projector bridge
  Memory: ENGRAM .eng write (embedding-FFT, composed self-shape)
  Retrieval: Hopfield resonance over composed self-shapes
  Output: reasoned response + self-shape update
  Latency: <100ms
  Sleep: offline LoRA consolidation from fingerprint replay

SHARED MEMORY BUS:
  .eng certificate store (portable, training-free)
  Two cosine spaces (REFLEX / MEANING — never cross-compared)
  HRR composition layer (compose.py, unchanged)
  Cleanup memory (mandatory, per CAPACITY_RESULTS)
```

### 4. Experiment Ladder (Cheapest Decisive First)

**E0 → E1 → E2 → E3 → E4 → E5 → E6** (see V9). Total budget for E0–E5: ~$300. The single smallest experiment is **E0: bridge probe on SmolLM2-360M, ~$5–$15, 2–4 hours.**

### 5. Cost, License & Deployment

- Path 0: ~$150–$300, Apache 2.0 everywhere, box only
- Path 1: ~$630–$3,500 total, Apache 2.0 everywhere, both tiers
- Path 3: ~$800–$1,230 above Path 0/1, Apache 2.0 everywhere, both tiers
- Path 2: ~$5,000–$30,000, Apache 2.0 (greenfield), long-term
- **License trap to avoid:** Llama-family models (distillation prohibited)[^86]
- GPU spot rates: H100 from ~$1.38/hr (Thunder Compute) to ~$2.89/hr (RunPod)[^12][^11]

### 6. The Honest Boundary

**Proven:**
- Modern Hopfield = attention = ENGRAM resonance (mathematical proof, ICLR 2021)
- SSMs are frequency-domain operators (SSD duality, Mamba-2 2024)
- Frequency-domain representations reduce catastrophic forgetting in continual learning (NeurIPS 2024)
- Cross-attention adapters can inject external memory into frozen LLMs (RETRO, LongMem, Larimar)
- ENGRAM's training-free fingerprints avoid catastrophic forgetting by construction

**Speculative (bet ahead of evidence):**
- That the Mamba SSM backbone's frequency-domain mixing will *actually improve reasoning quality* over a token LLM + ENGRAM retrieval bridge — not just efficiency. This is the key unproven claim of Path 1/3.
- That a RVQ "note codebook" over ENGRAM fingerprints will give the model genuine spectral understanding, not just a lookup table of spectral tokens.
- That a narrow creature-mind model trained on 20–100B domain tokens will be *useful enough* to justify Path 2.

**Kill criteria:**
- **Kill Path 0:** E0 shows <5% improvement over no-retrieval baseline → model cannot use spectral memory
- **Kill Path 1:** E3 shows no improvement in Comp-SQ or LH-MSR beyond what Path 0 achieves → SSM train-up is not worth the compute over a bridge
- **Kill Path 2:** Path 3 meets all creature-mind capability targets and there is no evidence of a hard ceiling → greenfield cost is unjustified
- **Kill entire frequency-native direction:** If a plain SmolLM2-360M + kNN ENGRAM retrieval (the null hypothesis) consistently matches or beats all other paths on all metrics at equal compute → the seam does not matter and the cheapest bridge wins forever

**Dropped from scope (honesty boundary):**
- Schumann resonances, 432 Hz "vibrational" claims, numerological frequency significance — none of these have any bearing on the architecture and none appear in the cited literature
- Claims that spectral models are "inherently more brain-like" without specific mechanistic justification — the relevant claims (SSMs ≈ frequency operators, Hopfield ≈ attention, CLS theory) are grounded in published proofs and empirical results

---

## References

1. [Improving language models by retrieving from trillions of tokens - arXiv](https://arxiv.org/abs/2112.04426) - RETRO combines a frozen Bert retriever, a differentiable encoder and a chunked cross-attention mecha...

2. [Larimar: Large Language Models with Episodic Memory Control](https://research.ibm.com/publications/larimar-large-language-models-with-episodic-memory-control) - Larimar: Large Language Models with Episodic Memory Control for ICML 2024 by Payel Das et al.

3. [This AI Paper from IBM and Princeton Presents Larimar: A Novel ...](https://www.marktechpost.com/2024/03/21/this-ai-paper-from-ibm-and-princeton-presents-larimar-a-novel-and-brain-inspired-machine-learning-architecture-for-enhancing-llms-with-a-distributed-episodic-memory/) - This AI Paper from IBM and Princeton Presents Larimar: A Novel and Brain-Inspired Machine Learning A...

4. [Improving language models by retrieving from trillions of tokens](https://deepmind.google/blog/improving-language-models-by-retrieving-from-trillions-of-tokens/) - We explore an alternate path for improving language models: we augment transformers with retrieval o...

5. [[2306.07174] Augmenting Language Models with Long-Term Memory](https://arxiv.org/abs/2306.07174) - Enhanced with memory-augmented adaptation training, LongMem can thus memorize long past context and ...

6. [[PDF] Augmenting Language Models with Long-Term Memory](https://neurips.cc/media/neurips-2023/Slides/72461.pdf) - We proposed LongMem framework to augment language models with long-term memory to read and comprehen...

7. [[PDF] arXiv:2203.08913v1 [cs.LG] 16 Mar 2022](https://arxiv.org/pdf/2203.08913.pdf) - Unlike other forms of attention, kNN retrieval can be easily scaled up to huge memory sizes, and is ...

8. [[Literature Review] Larimar: Large Language Models with Episodic ...](https://www.themoonlight.io/en/review/larimar-large-language-models-with-episodic-memory-control) - The paper introduces Larimar, a novel architecture designed to enhance Large Language Models (LLMs) ...

9. [Larimar: large language models with episodic memory control](https://dl.acm.org/doi/10.5555/3692070.3692472) - This paper presents Larimar - a novel, brain-inspired architecture for enhancing LLMs with a distrib...

10. [[2207.06881] Recurrent Memory Transformer - arXiv](https://arxiv.org/abs/2207.06881) - We propose and study a memory-augmented segment-level recurrent Transformer (RMT). Memory allows to ...

11. [NVIDIA H100 Price: Cloud GPU Rental Rates Compared (2026 ...](https://deploybase.ai/articles/nvidia-h100-price) - NVIDIA H100 cloud rental pricing ranges from $1.38 to $11.68 per GPU-hour across 28+ providers. Comp...

12. [NVIDIA H100 Pricing (June 2026): Cheapest Cloud GPU Rates](https://www.thundercompute.com/blog/nvidia-h100-pricing) - Compare NVIDIA H100 80GB cloud GPU prices across AWS, Azure, Google Cloud, Nebius, and low-cost prov...

13. [FNet: Mixing Tokens with Fourier Transforms](https://arxiv.org/abs/2105.03824) - We show that Transformer encoder architectures can be sped up, with limited accuracy costs, by repla...

14. [[2107.00645] Global Filter Networks for Image Classification - arXiv](https://arxiv.org/abs/2107.00645) - In this paper, we present the Global Filter Network (GFNet), a conceptually simple yet computational...

15. [ADAPTIVE FOURIER NEURAL OPERATORS: EFFICIENT ...](https://openreview.net/pdf?id=EXHG-A3jlM)

16. [GFNet: Global Filter Networks for Visual Recognition - IEEE Xplore](https://ieeexplore.ieee.org/iel7/34/4359286/10091201.pdf) - In this section, we briefly review recent progress in several related topics: vision Transformers, M...

17. [Adaptive Fourier Neural Operator (AFNO) - Emergent Mind](https://www.emergentmind.com/topics/adaptive-fourier-neural-operator-afno) - AFNO is a neural operator that replaces self-attention with adaptive spectral mixing, enabling effic...

18. [Google Replaces BERT Self-Attention with Fourier Transform](https://syncedreview.com/2021/05/14/deepmind-podracer-tpu-based-rl-frameworks-deliver-exceptional-performance-at-low-cost-19/) - Transformer architectures have come to dominate the natural language processing (NLP) field since th...

19. [GFNet: Global Filter Networks for Visual Recognition](https://dl.acm.org/doi/abs/10.1109/TPAMI.2023.3263824)

20. [[2107.10932] FNetAR: Mixing Tokens with Autoregressive Fourier ...](https://ar5iv.labs.arxiv.org/html/2107.10932) - In this note we examine the autoregressive generalization of the FNet algorithm, in which self-atten...

21. [Hyena Hierarchy: Towards Larger Convolutional Language Models](https://hazyresearch.stanford.edu/blog/2023-03-07-hyena) - Hyena is a new operator for large language models that uses long convolutions and gating, reaching a...

22. [Performer: Efficient Transformer Architecture - Emergent Mind](https://www.emergentmind.com/topics/performer) - Discover Performer, a linear-complexity transformer that uses random feature approximations to enabl...

23. [Hyena Hierarchy: Towards Larger Convolutional Language Models](https://arxiv.org/abs/2302.10866) - We propose Hyena, a subquadratic drop-in replacement for attention constructed by interleaving impli...

24. [What is: Fast Attention Via Positive Orthogonal Random Features?](https://www.vietanh.dev/glossary/favor) - **FAVOR+**, or **Fast Attention Via Positive Orthogonal Random Features**, is an efficient attention...

25. [SpectFormer: Frequency and Attention is what you need in a Vision Transformer](https://arxiv.org/abs/2304.06446v1) - Vision transformers have been applied successfully for image recognition tasks. There have been eith...

26. [Efficiently Modeling Long Sequences with Structured State Spaces](https://arxiv.org/abs/2111.00396) - We propose the Structured State Space sequence model (S4) based on a new parameterization for the SS...

27. [state-spaces/s4: Structured state space sequence models - GitHub](https://github.com/state-spaces/s4) - This repository provides the official implementations and experiments for models related to S4, incl...

28. [Mamba and State Space Models (SSM): The Next-Generation ...](https://qubittool.com/blog/mamba-ssm-beyond-transformer-architecture) - A deep technical analysis of Mamba and State Space Models (SSM). Covers the evolution from S4 to Mam...

29. [4.1 Ssd (state Space Dual)...](https://www.youngju.dev/blog/ai-papers/mamba_selective_state_space_models.en) - An in-depth review of the Mamba (Selective State Space Models) paper. Analyzing the evolution from S...

30. [[PDF] On the Parameterization and Initialization of Diagonal State Space ...](https://proceedings.neurips.cc/paper_files/paper/2022/file/e9a32fade47b906de908431991440f7c-Paper-Conference.pdf) - Our final model S4D is a simple diagonal version of S4 whose kernel computation requires just 2 line...

31. [State Space Duality (Mamba-2) Part I - The Model | Tri Dao](https://tridao.me/blog/2024/mamba2-part1-model/) - The SSD model refers to a specific standalone layer, like attention or an SSM, that can be incorpora...

32. [[Literature Review] When recalling in-context, Transformers are not ...](https://www.themoonlight.io/en/review/when-recalling-in-context-transformers-are-not-ssms) - While SSMs can be viewed as structured attention matrices, their recurrent nature may introduce dist...

33. [Understanding Input Selectivity in Mamba: Impact on Approximation Power, Memorization, and Associative Recall Capacity](http://arxiv.org/abs/2506.11891) - State-Space Models (SSMs), and particularly Mamba, have recently emerged as a promising alternative ...

34. [RWKV Architecture History](https://wiki.rwkv.com/basic/architecture.html) - RWKV-7 comprehensively surpasses the Transformer and the previous RWKV-6 architecture in terms of co...

35. [[PDF] RWKV-7 "Goose" with Expressive Dynamic State Evolution](https://openreview.net/pdf/74011cffc1082ac9394afde92802c810c51baabf.pdf) - We present RWKV-7 "Goose", a new sequence modeling architecture our 2.9 billion parameter language m...

36. [IBM releases Granite 4.0 with hybrid Mamba-2/Transformer ...](https://www.linkedin.com/posts/umar-iftikhar-1b7458135_ibm-granite-40-hyper-efficient-high-performance-activity-7379963418679611392-ucmh) - IBM Unveils Granite 4.0: Hybrid Mamba-2/Transformer Models IBM has released Granite 4.0, an open-wei...

37. [IBM Granite 4.0: Hyper-efficient, High Performance Hybrid Models ...](https://www.ibm.com/new/announcements/ibm-granite-4-0-hyper-efficient-high-performance-hybrid-models) - Granite 4.0 features a new hybrid Mamba/transformer architecture that greatly reduces memory require...

38. [Hybrid thinking: Inside the architecture of IBM's Granite 4.0](https://www.ibm.com/think/news/hybrid-thinking-inside-architecture-granite-4-0) - Introducing IBM Granite 4.0, a family of open-weight models that aim for higher efficiency. Learn mo...

39. [DeltaNet Explained (Part I) - Songlin Yang](https://sustcsonglin.github.io/blog/2024/deltanet-1/) - Linear attention is essentially a linear RNN with a matrix-valued state S that accumulates key-value...

40. [[2406.06484] Parallelizing Linear Transformers with the Delta Rule ...](https://arxiv.org/abs/2406.06484) - This work describes a hardware-efficient algorithm for training linear transformers with the delta r...

41. [State Space Duality (Mamba-2) Part II - The Theory | Goomba Lab](https://goombalab.github.io/blog/2024/mamba2-part2-theory/) - We'll derive the SSD “duality” in two completely separate ways, one starting from the SSM perspectiv...

42. [Mamba-2: Algorithms and Systems](https://pli.princeton.edu/blog/2024/mamba-2-algorithms-and-systems) - One of our primary goals with Mamba-2 is to leverage tensor cores to speed up the SSM. As SSD (part ...

43. [Transformers are SSMs: Generalized Models and Efficient ... - arXiv](https://arxiv.org/abs/2405.21060) - State-space models (SSMs) such as Mamba have recently been shown to match or outperform Transformers...

44. [[PDF] RWKV-7 "Goose" with Expressive Dynamic State Evolution](https://openreview.net/pdf?id=ayB1PACN5j) - We present RWKV-7 "Goose", a new sequence modeling architecture with con- stant memory usage and con...

45. [state-spaces/mamba-130m-hf - Hugging Face](https://huggingface.co/state-spaces/mamba-130m-hf) - This repository contains the transfromers compatible mamba-2.8b. The checkpoints are untouched, but ...

46. [state-spaces/mamba-130m at main - Hugging Face](https://huggingface.co/state-spaces/mamba-130m/tree/main) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

47. [Mamba-3B-SlimPJ: State-space models rivaling the ... - Together AI](https://www.together.ai/blog/mamba-3b-slimpj) - We are releasing a Mamba model with 3B parameters trained on 600B tokens on the SlimPajama dataset, ...

48. [state-spaces/mamba-370m - Hugging Face](https://huggingface.co/state-spaces/mamba-370m) - Instructions to use state-spaces/mamba-370m with libraries, inference providers, notebooks, and loca...

49. [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/1983611955668775411)

50. [[PDF] Modern Hopfield Networks and Attention for Immune Repertoire ...](https://proceedings.neurips.cc/paper/2020/file/da4902cb0bc38210839714ebdcf0efc3-Paper.pdf) - A central mechanism in machine learning is to identify, store, and recognize patterns. How to learn,...

51. [[PDF] Recasting Self-Attention with Holographic Reduced Representations](https://kdd-milets.github.io/milets2022/papers/MILETS_2022_paper_5942.pdf) - The HRR has seen successful use in cognitive science re- search [5, 7, 8, 12, 19, 48, 52], but compa...

52. [Modern Hopfield Networks meet Encoded Neural Representations](https://arxiv.org/html/2409.16408v2) - The Modern Hopfield network (MHN) introduced a continuous relaxation of the original method and in t...

53. [modern hopfield networks](https://arxiv.org/pdf/2502.10122.pdf)

54. [Modern Hopfield Networks - Emergent Mind](https://www.emergentmind.com/topics/modern-hopfield-networks-mhns) - Modern Hopfield Networks are continuous-state attractor models defined by energy minimization with n...

55. [LARS-VSA: A Vector Symbolic Architecture For Learning ...](https://arxiv.org/abs/2405.14436) - Human cognition excels at symbolic reasoning, deducing abstract rules from limited samples. This has...

56. [Differentiable neural computer - Wikipedia](https://en.wikipedia.org/wiki/Differentiable_neural_computer) - In artificial intelligence, a differentiable neural computer (DNC) is a memory augmented neural netw...

57. [ml-jku/hopfield-layers: Hopfield Networks is All You Need](https://github.com/ml-jku/hopfield-layers) - Hopfield Networks is All You Need. Contribute to ml-jku/hopfield-layers development by creating an a...

58. [[PDF] KANERVA'S SPARSE DISTRIBUTED MEMORY:](https://ntrs.nasa.gov/api/citations/19890017031/downloads/19890017031.pdf)

59. [hopfield-layers/hflayers/transformer.py at master · ml-jku/hopfield-layers](https://github.com/ml-jku/hopfield-layers/blob/master/hflayers/transformer.py) - Hopfield Networks is All You Need. Contribute to ml-jku/hopfield-layers development by creating an a...

60. [hopfield-layers](https://best-of-web.builder.io/library/ml-jku/hopfield-layers) - Find and compare the best open-source projects

61. [Sparse Distributed Memory](https://www.cs.hmc.edu/~jpadgett/nnfinal/NNPrsntnJP1.pdf)

62. [Sparse distributed memory - Wikipedia](https://en.wikipedia.org/wiki/Sparse_distributed_memory)

63. [LARS-VSA: A Vector Symbolic Architecture For](http://arxiv.org/pdf/2405.14436.pdf)

64. [Large Product Key Memory for Pretrained Language Models](https://aclanthology.org/2020.findings-emnlp.362.pdf)

65. [[1907.05242] Large Memory Layers with Product Keys - arXiv](https://arxiv.org/abs/1907.05242) - This memory layer allows us to tackle very large scale language modeling tasks. In our experiments w...

66. [Generalized Holographic Reduced Representations - arXiv](https://arxiv.org/html/2405.09689v2)

67. [[PDF] Learning with Holographic Reduced Representations - NIPS](https://proceedings.neurips.cc/paper_files/paper/2021/file/d71dd235287466052f1630f31bde7932-Paper.pdf) - Holographic Reduced Representations (HRR) are a method for performing symbolic AI on top of real-val...

68. [[PDF] High Fidelity Neural Audio Compression - arXiv.org](https://arxiv.org/pdf/2210.13438.pdf)

69. [EnCodec: Neural Audio Codec Framework](https://www.emergentmind.com/topics/encodec) - EnCodec is a neural audio codec framework that leverages convolutional-LSTM and residual vector quan...

70. [Principle:Facebookresearch Audiocraft Encoder Decoder Architecture](https://leeroopedia.com/index.php/Principle:Facebookresearch_Audiocraft_Encoder_Decoder_Architecture)

71. [EnCodec From Scratch: Lets Build a Neural Audio Codec!!](https://www.youtube.com/watch?v=hoTccaj5mxI) - The EnCodec architecture was one of the first major Audio Codec models released by Meta (following c...

72. [What is Residual Vector Quantization? - AssemblyAI](https://www.assemblyai.com/blog/what-is-residual-vector-quantization) - In the audio domain, in particular, neural audio codecs based on Residual Vector Quantization supers...

73. [[PDF] Byte Latent Transformer: Patches Scale Better Than Tokens](https://aclanthology.org/2025.acl-long.453.pdf) - We introduce the Byte Latent Transformer (BLT), a tokenizer-free architecture that learns from raw b...

74. [Meta AI Introduces Byte Latent Transformer (BLT)](https://www.marktechpost.com/2024/12/13/meta-ai-introduces-byte-latent-transformer-blt-a-tokenizer-free-model-that-scales-efficiently/) - Meta AI Introduces Byte Latent Transformer (BLT): A Tokenizer-Free Model That Scales Efficiently

75. [DeepMind's Perceiver IO: A General Architecture for a Wide Variety ...](https://syncedreview.com/2021/08/09/deepmind-podracer-tpu-based-rl-frameworks-deliver-exceptional-performance-at-low-cost-78/) - Perceiver IO meanwhile uses a cross-attention mechanism to map from latents to arbitrarily sized and...

76. [Published as a conference paper at ICLR 2022](https://arxiv.org/pdf/2107.14795.pdf)

77. [Perceiver IO: a scalable, fully-attentional model that works on any ...](https://huggingface.co/blog/perceiver) - The first Transformer-based neural network that works on all kinds of modalities (text, images, audi...

78. [HuggingFaceTB/SmolLM2-135M · Hugging Face](https://huggingface.co/HuggingFaceTB/SmolLM2-135M) - SmolLM2 is a family of compact language models available in three size: 135M, 360M, and 1.7B paramet...

79. [SmolLM: Hugging Face's small language models for edge - noze](https://www.noze.it/en/insights/smollm-open-source/) - Hugging Face releases SmolLM on 16 July 2024: 135M, 360M and 1.7B parameters, SmolLM-Corpus dataset,...

80. [ai/smollm2 - Docker Image](https://hub.docker.com/r/ai/smollm2) - A compact language model with 360 million parameters, designed to run efficiently on-device while pe...

81. [Qwen/Qwen2.5-0.5B - Hugging Face](https://huggingface.co/Qwen/Qwen2.5-0.5B) - Qwen2.5 is the latest series of Qwen large language models. For Qwen2.5, we release a number of base...

82. [EleutherAI/pythia-160m](https://huggingface.co/EleutherAI/pythia-160m) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

83. [Pythia - EleutherAI](https://www.eleuther.ai/artifacts/pythia) - A suite of 16 models with 154 partially trained checkpoints designed to enable controlled scientific...

84. [AI & LLM Training Cost Calculator | Spheron](https://www.spheron.network/tools/training-cost-calculator/) - Estimate the GPU cost to train or fine-tune an LLM. Live pricing on H100, B200, H200, A100, benchmar...

85. [Hugging Face Releases SmolLM2: A Small Language Model ...](https://news.aibase.com/news/12987)

86. [[PDF] From Prompt to Clone: Copyright Challenges in AI Model Distillation](https://repository.uclawsf.edu/cgi/viewcontent.cgi?article=1151&context=hastings_science_technology_law_journal) - This paper examines the legality of model distillation in the context of large language models (LLMs...

87. [A model of autonomous interactions between hippocampus and neocortex driving sleep-dependent memory consolidation | PNAS](https://www.pnas.org/doi/10.1073/pnas.2123432119) - How do we build up our knowledge of the world over time? Many theories of memory formation and conso...

88. [Exploring the roles of memory replay in targeted memory reactivation and birdsong development: Insights from computational models of complementary learning systems](https://www.biorxiv.org/content/biorxiv/early/2024/10/28/2024.10.28.620229.full.pdf)

89. [A Neural Network Model of Complementary Learning Systems: Pattern Separation and Completion for Continual Learning](http://www.arxiv.org/pdf/2507.11393.pdf)

90. [Learning in deep neural networks and brains with similarity-weighted interleaved learning | PNAS](https://www.pnas.org/doi/10.1073/pnas.2115229119) - Understanding how the brain learns throughout a lifetime remains a long-standing challenge. In artif...

91. [Stability-Plasticity: Solving Continual Learning - rewire.it](https://rewire.it/blog/the-stability-plasticity-dilemma-how-memory-architectures-are-solving-continual-learning/) - This approach reduces forgetting to just 11% compared to 89% for full fine-tuning. What are the main...

92. [Catastrophic Forgetting in Large Language Models](https://arxiv.org/abs/2308.08747) - Catastrophic forgetting (CF) is a phenomenon that occurs in machine learning when a model forgets pr...

93. [Forget Forgetting: Continual Learning in a World of Abundant Memory](https://arxiv.org/html/2502.07274v5)

94. [Continual Learning and Catastrophic Forgetting - arXiv](https://arxiv.org/html/2403.05175v1)

95. [[PDF] Continual Learning in the Frequency Domain](https://neurips.cc/media/neurips-2024/Slides/94751.pdf) - Our framework leverages frequency domain transformations for efficient continual learning, addressin...

96. [Official code for "Continual Learning in the Frequency Domain ...](https://github.com/EMLS-ICTCAS/CLFD) - The official repository for NeurIPS'24 paper "Continual Learning in the Frequency Domain". Overview....

97. [Continual Learning in the Frequency Domain - researchr publication](https://researchr.org/publication/LiuDHAA024) - Continual Learning in the Frequency Domain. Ruiqi Liu, Boyu Diao, Libo Huang ... NeurIPS 2024, Vanco...

98. [MQAR: Multi-Query Associative Recall - Emergent Mind](https://www.emergentmind.com/topics/multi-query-associative-recall-mqar-99600239-c8a9-49da-a81b-9ce2f354c1aa) - MQAR is a task where models retrieve multiple key–value pairs amid distractors using dynamic, parame...

99. [REVISITING ASSOCIATIVE RECALL](https://openreview.net/pdf/f7e9f322ba15e88dcc818ab70866648650a5e319.pdf)

100. [mamba/LICENSE at main · state-spaces/mamba](https://github.com/state-spaces/mamba/blob/main/LICENSE) - Mamba SSM architecture. Contribute to state-spaces/mamba development by creating an account on GitHu...

101. [GitHub - IBM/larimar: Code for ICML 2024 paper](https://github.com/IBM/larimar) - Code for ICML 2024 paper. Contribute to IBM/larimar development by creating an account on GitHub.

