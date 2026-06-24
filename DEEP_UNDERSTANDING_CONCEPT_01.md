# DEEP UNDERSTANDING — CONCEPT 01
## From theory paper to first proof-of-concept: the Three-Brain, adapted for Vector + ENGRAM
## Created: 2026-06-23 · Dexter × Claude Opus 4.8
## Source: Deep_Understanding (4).pdf (theory, no code) · grounded by full extraction · companion to Vector-eng.md, ANKI_WAY.md

---

## 0. What this is

The Deep Understanding (DU) paper proposes a **three-brain meta-cognitive architecture** (B1 fast / B2 slow /
B3 meta) with **Phase-Gated Plasticity** so an agent "grows up" without value drift or catastrophic
forgetting. It is **theory only — no code, no PoC.** This document does two things:

1. **Adapts** DU from a generic LLM-assistant framing to **Vector** (an embodied, always-on creature) using
   **ENGRAM** as its memory substrate and obeying the **Anki Way** (safety partition, graceful degradation,
   creature-first).
2. **Specifies the first PoC** — a runnable "DU sandbox" (`concepts/deep_understanding/three_brain_skeleton.py`)
   that proves the core loop on synthetic situations *before* we touch the robot or finish ENGRAM.

> The paper's worked example is a city-CO₂ Q&A. Ours is a *creature in a home*: B1 reacts in <100ms, B2
> reasons over remembered situations on the Pi box, B3 governs who Vector becomes over weeks and keeps it safe
> and itself.

---

## 1. The mapping: DU → Vector

| DU paper | DU-for-Vector | Where it runs | Anki-Way tie |
|---|---|---|---|
| **B1 Fast (≤100ms, FastAPI I/O + safety filter)** | The **reflex** — modified `moodManager` emotion tick + reflexes + face render. *Not an LLM.* Applies B3's current value/plasticity signals as biases. | **On robot** (APQ8009) | real-time + safety partition; works even if box is down |
| **B2 Slow (0.5–5s, MoE reasoning + KV vector store)** | **Situational reasoning** over ENGRAM: retrieve k-nearest past situations, fuse perception, pick/score actions, form speech. "Experts" = domain modules (vision, social, task, language). | **Pi box** | heavy ML stays off the body |
| **B3 Meta (async, value governance + plasticity)** | **The constructor / character keeper**: CVN = Vector's values+safety; Curiosity = drives; Teacher Buffer = owner feedback; Adapter Bank = personality LoRA deltas; Meta-Plasticity = the "growing up" scheduler + nightly sleep-compilation. | **Pi box (idle/dock)** | frozen core ⇒ "it stays itself"; runs while docked |
| **Info-prioritization formula (Eq.1)** | The **ENGRAM write-gate**: score each situational fragment; store P/S, drop N. Unifies DU memory with ENGRAM. | Pi box | sparse-over-null |
| **Phase-Gated Plasticity (P0–P3)** | Vector **growing up with you** (real durations, §3) | Pi box | designer-tunable schedule |

**Key reframings from the paper:**
- DU's CVN encodes "sustainability/equity." **Vector's CVN encodes its character + non-negotiable safety
  invariants** (never override cliff/fall; be kind; the owner's preferences). The frozen core in P3 is *what
  makes Vector remain Vector*.
- DU's "experts answer a question." **Vector's B2 decides how to *be* in a situation** (act / speak / emote /
  stay silent), grounded in retrieved ENGRAM situations + per-person memory.
- DU's reward `R_ext` = RLHF rater. **Vector's `R_ext` = the owner's reactions** (delight, annoyance,
  "good bot", ignoring it). `R_int` = curiosity/novelty. `R_val` = alignment with CVN (character+safety).

---

## 2. The formulas, instantiated for Vector

**Memory write-gate (DU Eq.1):**
```
Score_i = wA·A_i + wP·P_i + wS·S_i − wN·N_i + wQ·Q_i + wO·ORDER_i + wU·1[UNKNOWN]
store fragment i in ENGRAM iff Score_i > τ      (B3 sets the weights per phase)
```
For Vector a "fragment" is a piece of a situation: *who is here, what they did, what Vector did, the outcome,
the felt emotion.* P (important: identities, preferences), S (solving: what worked last time), Q (the current
goal/curiosity), N (noise: dropped), UNKNOWN (a gap → curiosity target).

**Phase-blended reward (DU Eq.2/3):**
```
R_total = λ1·R_ext + λ2·R_int + λ3·R_val      (λ’s set by phase; frozen in P3)
R_ext = owner feedback   R_int = novelty (RND)   R_val = CVN alignment (character + safety)
```

**Plasticity / consolidation:**
```
EWC: L_ewc = Σ (λF/2)·F_i·(θ_i − θ_i*)²        protects consolidated character
PPO core update with KL bound δ(phase); in P3 only LoRA adapters update, CVN frozen
```

---

## 3. Phase-Gated Plasticity, retimed for a home robot

The paper uses human-age analogies with no real durations. We assign concrete creature timelines (tunable):

| Phase | Paper analogy | **Vector real duration** | η | λ_ext (owner) | What happens | Freeze |
|---|---|---|---|---|---|---|
| **P0 Infancy** | 0–2y | **first ~3 days** out of box | 1.0 | 0.1 | explore home & people, build the map & first ENGRAM situations, high curiosity | none |
| **P1 Childhood** | 3–12y | **~weeks 1–4** | 0.4 | 0.5 | learn owner norms/preferences from reactions; partial EWC | partial |
| **P2 Adolescence** | 13–22y | **~months 2–6** | 0.15 | 0.8 | consolidate a stable personality; prune; tighten KL (δ=0.1) | selective |
| **P3 Adulthood** | 23y+ | **6 months → life** | ≈0 | 1.0 | stable character; lifelong learning via **LoRA adapters only**; CVN frozen (δ=0.01) | core frozen |

This is the engineering answer to "how does Vector grow with me but stay itself": it is most malleable in the
first month, then crystallizes — exactly the Anki ethos of a creature with a developmental arc.

---

## 4. First PoC scope (what we build NOW)

A **DU sandbox** that runs on a laptop/Pi with **no robot and before ENGRAM is finished**, proving the loop:

- Feed **synthetic situations** (scripted "days in a home": person appears, pets Vector, ignores it, etc.).
- **B2** labels fragments via Eq.1, writes P/S to a pluggable vector store (`InMemoryStore` now → ENGRAM later).
- **B2** retrieves nearest past situations and proposes an action with confidence.
- **B3** holds the **CVN** (character+safety), blends rewards, runs the **Meta-Plasticity Controller**
  (phase schedule, freeze logic), and **modulates** B2's choice; logs every value change (auditable).
- **B1** stub turns the chosen action into a (mock) reflex/emote with the safety filter on top.
- A **phase clock** advances P0→P3 so we can watch the creature "grow up" in fast-forward and verify:
  (a) memory gate keeps P/S, drops N; (b) reward blend shifts owner-ward over phases; (c) CVN freezes in P3;
  (d) forgetting metric stays low; (e) box-down ⇒ B1 reflex still safe.

**Explicitly deferred** (paper's full stack — not needed for PoC): Ray RLlib distributed PPO, real MoE LLM
experts, FAISS/Chroma at scale, PEFT training. The PoC uses simple stand-ins behind interfaces so each can be
swapped for the real thing.

### Interfaces (so the PoC grows into production)
```
MemoryStore      .write(fragment, score) / .knn(query, k)        # InMemory → ENGRAM
RewardModel      .ext(obs) .int(obs) .val(obs, cvn)              # stubs → owner-feedback + RND + CVN
ValueNet (CVN)   .score(action, context) .update(grad|frozen)    # tiny MLP → real net
PlasticityCtrl   .phase(t) .eta() .lambdas() .kl_bound() .frozen()
Brain1/2/3       .step(...)                                       # B1 stub on-robot later
```

---

## 5. The skeleton (delivered)

`concepts/deep_understanding/three_brain_skeleton.py` — a single runnable file implementing the above with
synthetic situations. Run it to watch a simulated Vector grow P0→P3, gate its memories, and crystallize its
character. It is intentionally dependency-light (pure Python + numpy-optional) so it runs anywhere, and every
real component sits behind an interface for later swap-in (ENGRAM, real reward model, real B1 on the robot).

See the file header for run instructions and the TODO map to production.

---

## 6. Risks & honest unknowns (this is theory becoming code)

- **The paper is untested.** PGP/CVN are plausible but unproven; the PoC exists to *falsify or validate* the
  core loop cheaply before committing.
- **Reward signals are hard.** "Owner feedback" (`R_ext`) must be inferred from real reactions (face/voice
  affect, touch, ignoring) — that depends on the attunement layer; PoC uses scripted feedback first.
- **Phase transitions** by milestone vs clock: PoC uses a clock; production should use milestones
  (enough people learned, enough situations stored) — flagged in code.
- **CVN safety invariants must be hard, not learned.** Cliff/fall/battery stay in the inviolable on-robot
  partition (Anki Way); the CVN's "safety" is *character-level*, never the real safety reflex.

---

## 7. Next steps

1. Run the sandbox; tune the phase schedule + memory-gate weights until "growing up" feels right.
2. Swap `InMemoryStore` → the adjusted ENGRAM (see ENGRAM-for-Vector plan) once it ingests situational vectors.
3. Replace scripted `R_ext` with real owner-feedback signals from the attunement layer.
4. Move the B1 stub onto the robot as the real reflex; keep B2/B3 on the box.
5. Add the forgetting-metric + value-audit-log evals from the paper (§Evaluation) as CI checks.

---

*Concept 01 turns a theory paper into a falsifiable first loop. The skeleton is the seed of L3 (the
Constructor / Self-C).*
