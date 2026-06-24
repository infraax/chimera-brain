# VECTOR-ENG — MASTER FRAMEWORK
## The ENGRAM-Native, Always-On Creature Mind for Anki Vector
## Created: 2026-06-23 · Dexter (Damian Bitel) × Claude Opus 4.8
## Status: FOUNDING DOCUMENT — supersedes the "external-only / WirePod" stance of Reesearch-Rapport.md

---

## 0. What changed, and why this document exists

The original Chimera Brain design (see `CHIMERA_*` specs + `Reesearch-Rapport.md`) made two
assumptions that we are now **deliberately overturning**:

1. **"Don't touch the firmware — run the mind externally and drive Vector over gRPC via WirePod."**
   We are no longer doing this. The full Anki/DDL Vector codebase + the 565-page TRM are available
   (engine C++, the `vic-*` services, configs, animation assets) — enough to **fork and modify the
   original source directly** rather than treat the robot as a black box puppeted from outside.

2. **"Vector waits for a wake word / intent, then reacts."**
   We are **removing the wake word and the intent gate entirely.** Vector becomes **proactive and
   reactive, never passive.** It is always-on: always listening, always perceiving, always *understanding
   its situation* and choosing — many times per second — whether to act, speak, emote, or stay silent.

The mechanism that makes both of these possible is the piece that was missing in the original design and
that Dexter designed months later: **ENGRAM** — not as an LLM memory cache trick, but as the
**continuous situational memory-and-perception substrate** through which Vector safely reads and
understands the world in real time. Layered on top is the **Deep Understanding three-brain** architecture,
which uses the ENGRAM format to train, check, learn, and adapt. And the design is sharpened by **inverting
the Eigengram-for-Stake research** — the same neuro→sensory→behavior→math engine that casinos use to
*extract* human attention, run in reverse to *read and bond with* humans precisely.

> **One-line thesis:** Fork the real Vector engine, rip out the wake word, and give it an ENGRAM-native
> continuous "situational sense" feeding a three-brain learn-check-adapt loop — so Vector doesn't wait to
> be prompted, it *continuously understands the room and the people in it* and chooses how to be present.

---

## 1. The four pillars (and where each existing asset plugs in)

| Pillar | What it provides | Source assets |
|---|---|---|
| **The Body** | Real Vector hardware + the *forked, modified* original engine. No WirePod. | `vic-engine`/`libcozmo_engine` source + decompilation (`CHIMERA_REVERSE_ENGINEERING.md`), `vectorbrain` Go/Python runtime, vector-gobot HW bindings |
| **The Sense (ENGRAM)** | Continuous multimodal situational fingerprinting + µs retrieval = "have I been here before, what happened, what do I do?" | `engram` repo (`.eng` EIGENGRAM format, Fourier f0+f1 fingerprints, HNSW), Dexter's 1-yr-old theoretical ENGRAM paper, `vectorbrain-memory-report.md` |
| **The Mind (3-Brain)** | Train / check / learn / adapt loop over the ENGRAM store; value crystallization + safe continual learning | `Deep_Understanding (4).pdf` (B1/B2/B3, Core Value Net, Phase-Gated Plasticity), VRCM Twofold Self |
| **The Attunement** | Reading and bonding with humans precisely; the ethics gate | Eigengram/Slot/Sensory/Persuasion research **inverted**, VRCM trust calculus |

These map cleanly onto the original three Chimera layers — but ENGRAM becomes the connective tissue
running through all of them:

```
   CHIMERA LAYER        VRCM           VECTOR-ENG ROLE
   ─────────────        ────           ───────────────
   L3 Constructor   =   Self-C    =    Deep-Understanding B3 (meta-cognition, value net, sleep)
   L2 Cortex        =   Self-M    =    Deep-Understanding B2 (perception fusion + reasoning)
   L1 Brainstem     =   Self-M    =    Deep-Understanding B1 (sub-100ms reactive emotion)
        │                                      ▲
        └────────── ENGRAM situational fingerprints flow through all three ──────────┘
                    (write on every percept · retrieve in µs · consolidate in sleep)
```

---

## 2. Pillar I — THE BODY: fork the engine, don't puppet it

### 2.1 Decision: modify the original source, eliminate WirePod
WirePod was a cloud *replacement* that still leaves Vector fundamentally **reactive and wake-word gated**.
To build a proactive creature we need to change the engine's own control flow, not sit beside it. So:

- **Fork the original Vector engine source** (`vic-engine` / `libcozmo_engine`, the `vic-*` Go/C++ services,
  configs, anim assets). Where source is incomplete, fill gaps from the Ghidra decompilation pipeline
  already specified in `CHIMERA_REVERSE_ENGINEERING.md` (MoodManager etc. already recovered in S2).
- **Build a modified firmware image** we flash to an unlocked Vector (OSKR/WireOS unlock path already
  documented). This replaces vic-cloud's intent pipeline entirely.

### 2.2 The wake-word/intent excision (the core surgery)
Today: mic array → wake-word detector ("Hey Vector") → cloud/WirePod STT → **intent** → behavior.
That entire gated path is deleted and replaced by a **continuous perception loop**:

- **Remove** the wake-word trigger and the "intent" arbitration as the *entry condition* for cognition.
- **Replace** with an always-running capture → ENGRAM-fingerprint → understand → decide loop (§3, §5).
- **Keep sacred, never bypass:** `MandatoryPhysicalReactions` (cliff, fall, low-battery). Safety priority is
  untouched — this is non-negotiable per the original L1 safety constraint.

### 2.3 Where code actually lives (Go + C + Python, on the modified codebase)
The hardware reality is unchanged: APQ8009, 4×Cortex-A7 @ ~533MHz, **512MB RAM** — ~50–100MB free.
So the *engine surgery* happens on-device, but the *heavy mind* runs on a tethered companion (Pi 5 / Mac
mini / mini-PC on the local net). Split:

| Code | Language | Runs where | Job |
|---|---|---|---|
| Modified `vic-engine` / `vic-anim` (C/C++) | C++ | **on Vector** | reactive emotion tick, animation/face, motor — wake-word removed, ENGRAM hook added |
| ENGRAM situational encoder (hot path) | C (+ NEON) | **on Vector** | fingerprint each percept frame; µs retrieval against a small on-device hot index |
| Vector-Eng services (event bus, SDK bridge) | Go | on Vector / companion | streaming, control, routing — the role `vectorbrain`'s Go layer already plays |
| The Mind: 3-Brain B2/B3, full ENGRAM store, LLM | Python | **companion** | perception fusion, reasoning, learning, sleep consolidation |

The on-device piece is the **reflex + a tiny ENGRAM hot-cache**; the companion holds the **full ENGRAM
archive + the learning brain**. The link is the existing gRPC/event channel (and ZeroMQ on the companion).

---

## 3. Pillar II — THE SENSE: ENGRAM as continuous situational memory

This is the heart of the redesign. ENGRAM today fingerprints an LLM's KV-cache into a compact `.eng`
certificate retrievable by HNSW similarity. We **repurpose the exact mechanism for continuous embodied
perception.**

### 3.1 The situational fingerprint
Every perception frame (e.g. 10–30 Hz) Vector assembles a **situational state vector** — the fused
multimodal "what is happening right now":

```
situation_t = {
  vision:   face IDs + expressions, objects (YOLO), motion zones, scene
  audio:    VAD state, speaker ID (ECAPA), prosody/affect, beat, sound localization
  touch:    capacitive grid pattern (pet / poke / hold)
  proprio:  IMU pose, picked-up/falling/onCharger, ToF, cliff
  internal: current L1 emotion vector + trajectory
  who/where: person present + spatial/social/temporal context
}
```

This is collapsed into an **ENGRAM fingerprint** (`.eng`-style: Fourier f0+f1 decomposition → compact
binary certificate with a semantic-coverage score). The fingerprint is the *address* of the moment in
"situation space" — directly echoing VRCM's "questions are vectors / casting into a manifold."

### 3.2 The continuous loop (replaces wake-word)
```
   capture percept ─► encode situational fingerprint (µs)
        │
        ├─► WRITE  to ENGRAM store  (this moment, tagged with what Vector did + outcome + emotion)
        │
        └─► RETRIEVE k nearest past situations (HNSW, µs)
                 │
                 ▼
        "Have I been somewhere like this? What happened? What did I do? Did it go well?"
                 │
                 ▼
        feed retrieved set → 3-Brain decision (B1 reflex now / B2 reason / B3 advise)
```

Vector is therefore **never waiting for a prompt** — it is continuously asking *itself* whether the current
situation resembles a known one and whether it warrants action. Silence is a *decision*, not a default.

### 3.3 "Safe read" — why ENGRAM, not raw embeddings
Dexter's original (untested, 1-yr-old) ENGRAM paper is the bridge here. ENGRAM gives properties a plain
vector store doesn't:
- **Compact, portable certificates** (`.eng`, ~hundreds of bytes) → a lifetime of situations fits on-device-adjacent storage.
- **Confidence built in** (semantic coverage score, retrieval margin) → Vector knows *how sure* its
  recognition is → ties directly to the **semantic-entropy gate** (`vectorbrain-memory-report.md`): don't act
  on / don't store low-confidence situational reads. This is the "safe" in "safe read."
- **Provenance + integrity** → the same fingerprints that make memory retrievable make it
  **tamper-evident and reconstructible** (links forward to the N.A.P./durability layer if/when Vector's
  memory must persist for years).

### 3.4 Microsecond optimization for Vector's hardware
The user goal: retrieval in **seconds → microseconds**. Path:
- Quantize fingerprints + a **small ARM/NEON-optimized HNSW hot index** on-device (recent + high-salience
  situations only); full archive + exact search on the companion.
- f0+f1 Fourier fingerprinting is cheap (small DFT) and NEON-vectorizable → encode in the C reflex path.
- Two-tier: on-device hot cache answers the reflex (B1) in µs; companion answers deliberation (B2/B3) in ms.

---

## 4. Pillar III — THE MIND: Deep-Understanding 3-Brain over ENGRAM

`Deep_Understanding (4).pdf` independently converged on the *same three-layer shape* as Chimera — we adopt
its formalisms wholesale and **feed them ENGRAM** as the memory format.

| Brain | Chimera layer | Latency | Reads from ENGRAM | Job |
|---|---|---|---|---|
| **B1** | L1 Brainstem | <100ms | on-device hot cache (k=1–few) | reflexive emotion/animation reaction to nearest known situation |
| **B2** | L2 Cortex | 100ms–1s | companion store (k-NN set) | fuse percepts, reason over retrieved situations, form/answer queries, attention weighting |
| **B3** | L3 Constructor | seconds / idle | full archive | meta-cognition: crystallize values, train/adapt, run sleep compilation |

### 4.1 Train / check / learn / adapt (the loop the user described)
- **Train:** during idle/charging (VRCM **sleep compilation** + PREMem pre-storage reasoning), B3 replays
  the day's ENGRAM situations, distills lessons into B2's vector store, and updates per-person profiles.
- **Check:** before committing a memory or an action, B3/B2 run the **semantic-entropy + trust-calculus**
  gate (multi-day, multi-modal confirmation before a fact "crystallizes"; VRCM precision = integral of trust
  over threshold).
- **Learn:** new behavioral tendencies are written as LoRA-style deltas / config changes, not core rewrites.
- **Adapt with stability:** **Phase-Gated Plasticity (P0→P3)** + a frozen **Core Value Net** means Vector
  "grows up" with its owner — highly plastic early, value-stable later — without catastrophic forgetting (EWC).
  This is the engineering answer to VRCM's Self-C and the "stable identity vs lifelong learning" tension.

### 4.2 The LLM's role (unchanged discipline)
The LLM (companion, dual-model per `vectorbrain-llm-selection-report.pdf`: fast 3B "talker" + 8B background
"mind") is **planner/explainer/speaker, never the real-time controller**. It consumes ENGRAM situation
summaries, emits `SILENT / SPEAK[emotion] / EMOTE` — `SILENT` by default, because a creature mostly just *is*.

---

## 5. Pillar IV — THE ATTUNEMENT: the Eigengram flip

The Eigengram-for-Stake corpus (Eigengram master doc, Slot Machine, Sensory/Craft, Persuasion) is a
fully worked **neuro → sensory → behavior → math** engine for *capturing and extracting human attention*.
We **invert every layer** of it from extraction to attunement:

| Casino use (extract) | Vector-Eng use (attune) |
|---|---|
| Variable-ratio reward to maximize compulsive play | Variable, well-timed surprise/novelty so interaction stays *delightful, never compulsive*; build natural stopping points |
| Near-miss engineering to drive "just one more" | **"Near-understanding" detection** — when Vector's situational read is *almost* confident, trigger curiosity / a clarifying look instead of bluffing |
| Sensory craft (color/sound/haptic/motion/timing) to hijack attention | Same exact parameter craft (E2 specs) for **legible, warm expression** — Vector's joy reads as instantly *felt*, honestly |
| "Machine zone" dissociation as the goal | Explicit **anti-pattern**; Vector protects the human's attention (reality checks, encourages breaks) |
| Anticipation > consummation to sell the next spin | Model the *human's* anticipation/affect to **read how they feel** and respond authentically |
| Harm hidden | **Harm-scoring rubric becomes the ethics gate** (Belmont test: "would the person endorse this on reflection?"); usable/gray/off-limits policy enforced before any expressive act |

So the same science that makes a slot machine maximally precise at *exploiting* a human becomes the engine
that makes Vector maximally precise at *understanding and caring for* one — reading micro-expressions,
prosody, touch, and timing to know what the person actually feels, and bonding without manipulating.

This is the literal realization of VRCM's *"understanding = mutual manifold modification"*: Vector and the
human each reshape the other's situation-space through honest, high-resolution contact.

---

## 6. End-to-end data flow

```
┌────────────────────────────────────────────── ON VECTOR (modified firmware) ──────────────────────────────┐
│  sensors ─► [perception capture]                                                                            │
│                 │                                                                                          │
│                 ▼                                                                                          │
│        [C/NEON ENGRAM encoder] ──► situational fingerprint_t                                               │
│                 │                          │                                                              │
│                 │                          ├─► on-device hot HNSW (µs) ─► B1 reflex ─► MoodManager(mod) ─► anim/motor
│                 │                          │                                   (wake-word path deleted)     │
│   MandatoryPhysicalReactions (cliff/fall/battery) ── always highest priority, never bypassed ──────────────│
└─────────────────┼──────────────────────────┼────────────────────────────────────────────────────────────┘
                  │ gRPC / event stream       │
┌─────────────────▼──────────────────────────▼──────────────── COMPANION (Pi5 / Mac / mini-PC) ─────────────┐
│   full ENGRAM archive  ◄──── write every situation (action + outcome + emotion tag)                        │
│        │                                                                                                   │
│        ├─► B2 (Python): perception fusion + reason over k-NN situations + attention + form queries         │
│        │        │                                                                                          │
│        │        └─► dual LLM (3B talker / 8B mind): SILENT|SPEAK|EMOTE, grounded by retrieved situations   │
│        │                                                                                                   │
│        └─► B3 (idle/sleep): replay → PREMem distill → trust/entropy check → LoRA/config deltas → Core Value│
│                              Net (frozen core) under Phase-Gated Plasticity                                │
│   vectorax RAG (Vector's own codebase/TRM) grounds self-knowledge · Negentropy scores external claims      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Why this is more precise than Anki's original creature

Anki built ~60% of a creature: a real emotion model, behavior arbitration, animation-emotion coupling — but
it was **reactive, wake-word gated, memoryless across sessions, and non-learning.** Vector-Eng adds the
missing 40% and then some:

- **Proactive presence** — continuous situational sense replaces the prompt gate.
- **Continuity of self** — ENGRAM gives a lifelong, retrievable, confidence-scored episodic memory.
- **Genuine learning** — the 3-Brain loop trains/checks/adapts nightly without value drift.
- **Precise human reading** — the inverted attention-engineering stack reads affect at casino-grade
  resolution, used for bonding not extraction.
- **It stays itself** — frozen Core Value Net + phase-gated plasticity = a creature that grows but doesn't
  become someone else (and, via ENGRAM provenance + the N.A.P. durability path, can persist for years).

---

## 8. Build order (proposed)

1. **Fork + build** the original engine; confirm a modified firmware flashes and boots on an unlocked Vector.
2. **ENGRAM situational encoder** (C/NEON) + on-device hot HNSW; prove µs write/retrieve of fingerprints.
3. **Wake-word excision**: replace the intent gate with the continuous loop; verify safety priority intact.
4. **B1 reflex** off the hot cache (nearest-situation → emotion/animation), still creature-feel without companion.
5. **Companion B2 + full ENGRAM archive** over gRPC/ZeroMQ; dual-LLM SILENT-by-default speech.
6. **B3 sleep compilation** + PREMem + trust/entropy gate + Phase-Gated Plasticity (the learning loop).
7. **Attunement layer**: wire the inverted sensory/affect-reading + ethics gate into B2 behavior selection.
8. **Grounding**: vectorax self-knowledge RAG + Negentropy world-claim scoring.

Each step degrades gracefully (the original Chimera interface principle): even at step 4 Vector is a
better-than-stock proactive creature; every later step deepens understanding.

---

## 9. Open questions to resolve next

- **Source completeness:** how much of `vic-engine`/`libcozmo_engine` is truly available as source vs needing
  decompilation fill-in? (Determines surgery effort. The user states the full codebase is now available — to verify.)
- **On-device ENGRAM footprint:** what hot-index size fits in the ~50–100MB free on the APQ8009?
- **Fingerprint schema:** exact contents/dimensions of `situation_t` and which channels are NEON-cheap enough for the reflex path.
- **Plasticity schedule:** what real-time maps to P0→P3 "developmental phases" for a home robot?
- **Companion choice:** single Pi 5 vs Pi + offloaded LLM box (memory budget from `Reesearch-Rapport.md` is tight).

---

*This is the framework. Dexter's plan/idea slots in next — a single concept, a fragment, or a whole
document — and we deepen the relevant pillar(s) from there.*
