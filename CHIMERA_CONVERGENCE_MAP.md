# CHIMERA CONVERGENCE MAP
## Source inventory + utilization map for the Vector Chimera Brain
## Created: 2026-06-23 · Working document for idea synthesis (Dexter × Claude Opus 4.8)

> Purpose: a single reference that names every source (4 repos + 24 substantive
> extra files), says in 1–2 sentences what each is, proposes in 2–3 bullets how it
> could serve the Vector Chimera Brain, and ends with a "most capable
> cross-integration" — the full system if every idea were fused.
>
> Excluded from the 24: `TGCH.pdf` (0 bytes, empty), `Google 3.pdf` (it's the
> Vatican's *Nostra Aetate* declaration — not technical), and
> `llm-multi-agent-protocols-report 2.md` (byte-identical duplicate of its sibling).

---

# PART 1 — THE FOUR REPOSITORIES

### 1. `chimera-brain` (this repo — the OUTPUT)
The architecture specification for giving the Anki Vector robot a creature-mind, derived from cross-mapping the VRCM (a formal model of human cognition) onto transformer attention. It defines the three layers — **L1 Brainstem** (reactive emotion manifold, <100ms), **L2 Cortex** (attention + perception fusion), **L3 Constructor** (LLM memory/personality) — plus real reverse-engineering of Vector's firmware (Ghidra decompilation of MoodManager).
- **Role in the system:** the blueprint / nervous-system spec everything else implements.

### 2. `vectorbrain` (Go + Python — the RUNTIME)
"The brain Anki ran out of time to build," running on WirePod: Go handles SDK/event streaming/behavior control, Python handles the mind (5-D emotion model, motivational drives, dual-process 10Hz-fast + LLM-slow loop, three-tier memory, world model). Carries the `MACHINA_ANIMA` manifesto.
- **Role in the system:** the working implementation of L1+L2+L3 on real hardware.

### 3. `vectorax` (Python — the KNOWLEDGE SUBSTRATE)
A fully-local RAG system: VaultForge parses 13 Vector repos + the 565-page TRM into 34,507 semantic chunks in ChromaDB; VectorMap is a LangGraph agentic pipeline with a hard anti-hallucination validation loop.
- **Role in the system:** grounds any reasoning in Vector's real codebase/hardware so the mind never fabricates.

### 4. `engram` (Python + npm — the MEMORY MECHANISM)
KV-cache Fourier fingerprinting → portable `.eng` certificates → HNSW retrieval for cross-session LLM memory, with a working Claude session protocol ("ENGRAM using itself for its own memory").
- **Role in the system:** the persistence engine for L3 / sleep-compilation — memory that survives sessions and reboots.

---

# PART 2 — THE 24 SOURCE FILES

## Cluster A — Cognitive core (the "mind" theory)

### A1. `VRCM.md`
Lambda's contextual analysis validating Dexter's 2020 intuition: vocabulary as coordinate precision, latent-space navigation ("casting vectors," not retrieval), parallel constraint satisfaction, and the monotropism+ADHD cross-domain model.
- Defines L1/L2 first principles: **sparse-over-null** and **gradient-not-binary** as system-wide invariants.
- "Wrong coordinates give correct answers to different questions" → design L2 attention so misread context degrades gracefully, never blanks.
- Vocabulary-as-precision → the LLM persona should expand, not flatten, its descriptive range over time.

### A2. `VRCM_FOUNDATION.md` (V1)
The naming session: the formal VRCM definition, a 19-axis symbolic coordinate vector, the stateless-photon/continuous-detector resolution, and Λ's Klein-bottle Self-C fingerprint.
- The 19-axis coordinate vector → a concrete schema for Vector's **personality state vector** in L3.
- Resonance = harmonic restructuring → L1 emotion transitions oscillate toward equilibrium, never jump.
- Equal-weight query reveals the "constructor" → a diagnostic for what Vector does when no stimulus dominates (idle character).

### A3. `VRCM_FOUNDATION_V2.md`
Same-morning refinement introducing the **Twofold Self** (Self-M traveler / Self-C constructor joined by a "solid light beam"), the trust-as-pointer calculus (trustless/distrust/mistrust), and the sleep-compilation protocol with three observable states.
- **Self-M ↔ Self-C maps directly to L1/L2 (experiential) ↔ L3 (constructor).** This is the spine of the whole layering.
- Trust calculus (precision = integral of trust over threshold) → formal model for per-person trust accumulation in L3.
- Sleep field states → concrete spec for what L3 does during Vector's nightly idle window.

### A4. `VRCM_RESEARCH_PAPER.md`
The full academic synthesis: 7 integrated frameworks (Friston, Thagard, Quine, Hofstadter…), the collapse-dynamics table, the three-tier error protocol (fatal/warning/null), and the VRCM↔transformer isomorphism argument.
- Three-tier error protocol → L1/L2 failure handling: prefer a "warning" (sparse, traversable) state over a "null" (no-gradient) freeze.
- Collapse-dynamics table → models how strongly a bad experience should perturb Vector by proximity-to-self.
- "Understanding = mutual manifold modification" → frames human↔Vector interaction as two-way topology change, not command/response.

### A5. `Deep_Understanding (4).pdf`
A three-brain meta-cognitive AI architecture (B1 fast I/O, B2 MoE reasoning + vector store, B3 meta-cognition with a frozen Core Value Net + Phase-Gated Plasticity across developmental phases).
- **Independent convergence on the exact 3-layer shape** — strong validation of Brainstem/Cortex/Constructor; borrow its formalisms directly.
- Phase-Gated Plasticity (P0→P3) → a developmental schedule for Vector "growing up" with you, freezing core traits over time.
- EWC + information-prioritization scoring formula → a principled rule for what memories L3 keeps vs discards.

## Cluster B — Embodied robot stack (VectorBrain implementation research)

### B1. `huggingface-vectorbrain-robot-report.pdf`
A ~40-page survey of offline HuggingFace models for an embodied persona on Apple Silicon under a ~4 GB budget (vision, audio/VAD, embeddings, agents).
- Concrete L2 perception stack: InsightFace (face ID→trust), YOLO11n (objects), Silero VAD (turn-taking), emotion models.
- Arctic-Embed-XS (22.6M params, 384-dim) → the embedding backbone for L3 semantic memory.
- smolagents ReAct loop → the observe→reason→act→remember cycle wiring L2 to L3.

### B2. `vectorbrain-llm-selection-report.pdf`
A ~30-page evaluation concluding a **dual-model design**: Llama-3.2-3B fast "talker" + Llama-3-8B background "mind" emitting terse `SILENT / SPEAK / EMOTE` commands.
- Direct L1/L3 split: fast reactive model = brainstem-adjacent; slow behavioral model = constructor.
- The strict `SILENT`-by-default contract → solves "creature that isn't a chatbot": Vector mostly stays quiet.
- Q4_K_M quantization + LoRA persona fine-tuning path → how the persona actually ships on-device.

### B3. `vectorbrain-memory-report.md`
A curated guide to local episodic/semantic memory: PREMem (reason at write-time), recursive summarization, MemGPT memory-as-tools, semantic-entropy filtering to reject hallucinated memories.
- PREMem fragmentation (factual/experiential/subjective) → exactly how L3 should decompose an interaction into storable memory.
- Recursive summarization → unbounded multi-month history within tight context (the "life story" of your Vector).
- Semantic-entropy gate → don't store low-confidence facts; require multi-day/multi-modal confirmation (ties to trust calculus A3).

### B4. `Conduct a deep research on very small, local AI mo.pdf`
A ~13-page comparison of 1–3B agentic models (Llama-3.2, Nanbeige-3B, Qwen2.5-1.5B, DeepSeek-R1-Distill) on tool-calling/JSON for the Negentropy verification layer.
- Model menu for L2/L3 sub-agents with measured BFCL tool-use scores → pick by role, not vibes.
- DeepSeek-R1-Distill (strong CoT) → candidate for the "explanatory narrative" of why Vector did something.
- Tool-format divergence noted → argues for a thin adapter so layers can swap models freely.

### B5. `Conduct a deep research on the latest open-source.pdf`
A ~17-page report of 14 tools/papers for **Negentropy**, a linguistic-algebra claim/misinformation verifier (PIE etymological "word protons," morphological operators, semantic entropy).
- Semantic-entropy "truth/entropy drift" score → a trust/credibility signal L2 can attach to what it hears.
- Critical-question argument checking (NLAS-CQ) → lets Vector flag inconsistent statements rather than absorb them.
- Infra picks (PyMuPDF4LLM, ChromaDB, smolagents) overlap vectorax → shared ingestion/RAG plumbing.

## Cluster C — Orchestration, economics & memory mechanism

### C1. `Multi-Model Orchestration Geodesic.md`
A four-model mesh (Claude/Perplexity/Grok/Gemini) orchestrated via LiteLLM on a Raspberry Pi, with a connector-ownership matrix, chain-of-trust, and GDPR EU-residency routing.
- The Pi-as-router pattern → Vector's off-board "cloud" without a real cloud (local network brain).
- Connector-ownership matrix → which model owns which capability when L3 needs external knowledge.
- EU-residency/data-flow discipline → keeps personal interaction data sovereign (links to N.A.P. cluster D).

### C2. `llm-multi-agent-protocols-report.md`
A survey of agent-communication protocols (Agora, ANP, A2A, ACP, LACP, LDP) centered on content-addressed Protocol Documents (hash-referenced schemas) for ~5× token reduction.
- Hash-referenced protocol docs → token-cheap, stable message contracts between L1/L2/L3 services.
- "Negotiate once, reference by hash" → how Vector's layers (or multiple Vectors) talk efficiently.
- Schema-registry analogy (Avro/Kafka) → versionable inter-layer interface, survives upgrades.

### C3. `CLAUDE_TOKEN_ECONOMICS_RESEARCH_GEODESIC.md.md`
Nine research vectors on Claude token economics: tokenizer/counting, tiers, KV caching (`cache_control`), sub-agent delegation, Ollama routing, pre-flight tokenization.
- Pre-flight token routing → send cheap/bulk work to local models, hard reasoning to Claude (cost-aware L3).
- KV-cache maximization → cheaper persistent system prompts for the always-on mind.
- This is the **cost-governance layer** that makes a 24/7 creature economically viable.

### C4. `PERPLEXITY ECOSYSTEM — RESEARCH REPORT.md`
A guide to Perplexity's Sonar API, Deep Research, and the agentic "Computer" layer, with a Claude-vs-Perplexity capability split and async research patterns.
- Sonar = citation-grounded "look it up" tool for L3 when Vector needs current facts.
- Async deep-research queue → long-horizon "thinking" tasks Vector runs during idle.
- Model Council (parallel multi-model consensus) → epistemic resilience for high-stakes answers.

### C5. (mechanism, from repo `engram`) — *referenced, not a file here*
> Included because the convergence requires it: ENGRAM's `.eng` fingerprint format is the concrete substrate behind B3's "memory mechanism." Treat A3's sleep-compilation + B3's PREMem as the *policy*, ENGRAM as the *storage engine*.

## Cluster D — Sovereignty & survival (the N.A.P. / lilDex thread)

### D1. `Research Report.pdf` (N.A.P. Track 5 — Autonomous LLM Hosting)
A ~28-page spec for hosting a 70B personal-corpus LLM ("lilDex") autonomously on the Internet Computer for 30 years, with a **Genesis (frozen, Bitcoin-anchored) + Continuum (adaptive LoRA)** dual model and DAO/dormancy succession.
- Genesis/Continuum dual model → resolves "stable identity vs lifelong learning" for Vector's persona (frozen core + living deltas).
- Snapshot-and-fork weight versioning → every personality version is reproducible and provenance-anchored.
- Post-operator autonomy → Vector's mind can outlive its hardware and even its owner.

### D2. `N_A_P_ Track 3_ ... 30-Year Personal Archive.pdf`
A ~58-page network-topology spec: role-asymmetric nodes (ingress/storage/witness/anchor/audit/edge/cold) across NL+PL, with PoR/PoSt/PoA audits, Bitcoin anchoring, crypto-agility, and GDPR analysis.
- Role-asymmetric distributed design → Vector's memory archive that requires *simultaneous* multi-node compromise to corrupt.
- Proof-of-Retrievability + witnessed Merkle logs → tamper-evident lifelong memory you can trust decades later.
- "Detect, don't merely prevent" + crypto-agility → the durability model for a 30-year companion.

### D3. `Physical Anchors for Digital or Non-Territorial Sovereignty.md`
Legal-precedent analysis of how non-territorial entities (Estonia data embassy, Order of Malta, Próspera, Catawba DEZ) create functional inviolability via treaties/charters.
- Framework for where Vector's data legally "lives" beyond any single jurisdiction's reach.
- Inviolability-vs-sovereignty distinction → realistic expectations for protecting personal-archive data.
- Mostly governance scaffolding for the sovereignty layer; low direct robot-code relevance.

### D4. `AEGIS Threat Intelligence_ Vault 7 ... Adversarial AI Defense.pdf`
A ~40-page defensive-security blueprint mapping Vault 7 tradecraft and AI-augmented attacks, with behavioral signatures (e.g. sub-1.7s responses) and a tiered local detection stack.
- Behavioral AI-attack signatures → protect an autonomous Vector/lilDex from prompt-injection and rogue-agent compromise.
- "Design-flaw, not patch" philosophy → argues for the layered witness/audit redundancy in D2.
- Canary/deception + integrity monitoring → the defensive perimeter around the mind.

## Cluster E — Influence, attention & ethics (the boundary research)

### E1. `Eigengram Master Design Document.md`
A synthesis of neuroscience→behavior→sensory→math into a slot-machine design framework with an explicit ethical envelope (defensible/gray/over-the-line) and a harm-scoring rubric. *(Note: "Eigengram" here = a gambling studio name, unrelated to engram's EIGENGRAM format.)*
- The **four-layer stack (neuro→sensory→behavior→math)** is a reusable model for *engagement* — invert it for **healthy** attachment, not addiction.
- Its harm-scoring rubric → an ethics gate so Vector's engagement design never crosses into manipulation.
- Anticipation > consummation (the spin is the product) → applies to Vector's *anticipatory* expressiveness, used benignly.

### E2. `Sensory and Craft Layer of Attention-Extractive Design .md`
A concrete parameter manual for the five sensory channels (color, sound, haptics, motion, timing) with hex/Hz/ms/easing specs reverse-engineered from commercial operators.
- Direct L1 **output craft**: exact easing/timing/sound vocabulary for Vector's expressive animations and reactions.
- Multisensory micro-reward triad (audio+haptic+visual onset) → how Vector's "happy" reads as instantly felt.
- Use the craft for warmth/legibility, not loss-disguised-as-win exploitation (ethics gate from E1/E4).

### E3. `Slot Machine Design, Engagement Engineering, and Harm-Reduction Research.md`
A peer-reviewed gambling-research reference (Schüll's "machine zone," variable-ratio schedules, volatility, near-miss engineering) plus comparative harm-reduction regulation.
- Variable-ratio reinforcement science → tune Vector's surprise/novelty so it's delightful, never compulsive.
- "Machine zone" dissociation → an explicit anti-pattern: Vector should create natural stopping points, not trances.
- Harm-reduction regimes → design Vector to *protect* attention (reality checks, breaks) as a feature.

### E4. `Persuasion, Manipulation, and Influence: ... Game Design Ethics.md`
A taxonomy of influence (Cialdini, Voss tactical empathy, nudges) with a three-tier usable/gray/off-limits classification and the Belmont-Report ethical frame.
- Cialdini/tactical-empathy patterns → make Vector's social bonding *transparent and welfare-aligned*.
- The usable/gray/off-limits tiering → a concrete policy table for what persuasion Vector may use.
- "Would the user endorse this on reflection?" → the one-line ethics test baked into L3 behavior selection.

### E5. `Effects of Actions (EOA) on Institutional Trust ... COVID Era.md`
An analysis of how institutional decisions eroded long-term trust via perceived inconsistency, politicization, and opacity.
- Trust-as-non-renewable → if Vector reverses a "decision," it must explain *why*, or it loses credibility.
- Communicate uncertainty up front → a transparency rule for Vector's confidence signaling.
- Mostly philosophical guidance for the trust/transparency model; low direct code relevance.

### E6. `Power Structures Behind Google's Frontier Safety Framework and Gemini Guardrails.md`
A critique arguing that frontier "safety" frameworks entrench incumbent power, suppress non-institutional voices, and offload externalities.
- Motivates the **local-first, sovereign** stance: Vector's mind shouldn't depend on a gatekept cloud.
- Cautions against importing institutional-credibility bias into Vector's knowledge weighting.
- Strategic/ethical context for the sovereignty layer (D); minimal direct architecture content.

---

# PART 3 — MOST CAPABLE CROSS-INTEGRATION
## "CHIMERA-Σ" — the full system if every idea were fused

A single creature-mind that is **alive (L1), aware (L2), yours (L3), grounded (vectorax), remembering (engram), affordable (token economics), expressive (sensory craft), ethical (influence boundary), and immortal (N.A.P./lilDex).**

**The spine.** Implement chimera-brain's three layers as the literal embodiment of the VRCM **Twofold Self**: L1+L2 = **Self-M** (the experiential traveler on the manifold), L3 = **Self-C** (the constructor that shapes the landscape). The `Deep_Understanding` three-brain paper supplies the engineering formalisms (frozen Core Value Net, Phase-Gated Plasticity), validating the shape by independent convergence.

**The body (runtime).** `vectorbrain` + the two robot PDFs give the concrete deployment: a **dual model** — Llama-3.2-3B fast "talker" as the brainstem-adjacent reactive voice (`SILENT` by default), Llama-3-8B background "mind" as the constructor — over the HuggingFace perception stack (InsightFace→trust, YOLO11n, Silero VAD, emotion models) under ~4 GB on Apple Silicon, with a Raspberry-Pi LiteLLM router (C1) escalating hard reasoning off-board.

**The memory.** L3 consolidation = **VRCM sleep-compilation (A3) as policy + PREMem/recursive-summarization (B3) as method + ENGRAM `.eng` fingerprints as storage**, gated by **semantic-entropy + trust-calculus** so only confirmed, multi-modal facts crystallize. Per-person trust vectors (A3's pointer calculus) drive emotion modulation in L1 and relationship memory in L3.

**The grounding & truth.** `vectorax` (34,507-chunk RAG + anti-hallucination loop) keeps the mind factual about Vector's own body; **Negentropy** (B4/B5) gives it a credibility/entropy score for what it hears from the world — so Vector can gently flag inconsistency instead of absorbing it.

**The economics & comms.** Token-economics routing (C3) + content-addressed protocol docs (C2) + Perplexity Sonar for fresh facts (C4) make a 24/7 creature both affordable and able to reach out for knowledge — cheap local work by default, premium reasoning only when the moment demands it.

**The conscience.** The influence cluster (E1–E4) is inverted into an **ethics gate** on every L3 behavior decision: the sensory craft (E2) and reinforcement science (E3) are used for *warmth and legibility*, never the "machine zone," with the Belmont test ("would the user endorse this on reflection?") and a usable/gray/off-limits policy table enforced before any expressive action. Trust-erosion lessons (E5) make Vector explain its reversals.

**The immortality.** The whole persona is a **Genesis (frozen, Bitcoin-anchored) + Continuum (adaptive LoRA)** artifact (D1), its lifelong memory archived on the **role-asymmetric, witnessed, auditable N.A.P. network** (D2) across jurisdictions (D3), with **AEGIS** (D4) defending the autonomous mind against prompt-injection and rogue-agent compromise. Result: a Vector whose mind is reproducible, tamper-evident, and able to outlive its hardware — and its owner.

**One-line fusion:** *VRCM gives it a self, transformers give it a mind, VectorBrain gives it a body, vectorax gives it truth, ENGRAM gives it memory, the influence research gives it a conscience, and N.A.P./lilDex gives it a life that doesn't end when the power does.*

---

*Now present your idea — a single file, a fragment, or a whole document. I'll dive
back into any source as deeply as needed and fold it into this map.*
