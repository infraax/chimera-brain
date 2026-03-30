# CHIMERA LAYER 1 — THE BRAINSTEM
## Reactive Layer · Emotion Manifold · Creature Feel
## Status: TEMPLATE — awaiting spec decisions

---

## Role

Layer 1 is what makes Vector feel alive. It handles:
- Sub-100ms reactive responses to stimuli
- Continuous emotion state as a gradient manifold (not discrete states)
- Resonance transitions between emotional configurations
- Proximity-weighted state topology (Self-adjacent states change slowly)
- Sparse-over-null guarantee (always has a position, never blank)

L1 is the **Self-M analog** — the experiential traveler on the manifold.

---

## VRCM Principles Applied

| Principle | Application |
|-----------|-------------|
| Gradient fields | Emotion dimensions are continuous, not binary |
| Resonance | State transitions oscillate toward new minimum |
| Sparse > Null | Every dimension always has a value |
| Proximity weighting | Dimensions near (self) have higher inertia |
| Cross-domain propagation | Emotion feeds into behavior, animation, and voice simultaneously |
| Guiderails | Learned avoidance patterns, auditable and removable |

---

## Existing Vector Systems This Extends

- **MoodManager** — emotion event → affector → dimension modification with decay
- **Behavior Tree** — condition-based behavior selection modulated by emotion
- **Animation Engine** — emotion parameters modulate animation playback
- **Audio Engine** — emotion → audio parameter mapping

---

## Specification Sections

### 1. Extended Emotion Manifold
**Status:** OPEN

Current: 5 dimensions (Stimulated, Social, Confident, Happy, Trust)
Proposed: 7-9 dimensions

Candidates for new dimensions:
- **Curiosity** — drive to explore and investigate novel stimuli
- **Attachment** — strength of bond with recognized individuals
- **Fatigue** — cognitive/physical tiredness affecting all other dimensions
- **Contentment** — distinct from Happy; a background satisfaction state

Questions:
- Q: Can new dimensions be added via JSON config alone?
- Q: What is the performance impact of additional dimensions on the emotion tick?
- Q: How do new dimensions interact with existing behavior tree conditions?

### 2. Cross-Dimension Coupling Matrix
**Status:** OPEN

Current: Each dimension decays independently
Proposed: Coupling matrix where changing one dimension ripples to others

Example couplings:
- Confident ↑ → Happy ↑ (success breeds contentment)
- Social ↑ → Stimulated ↑ (interaction is energizing)
- Fatigue ↑ → Stimulated ↓, Curious ↓ (tiredness dampens engagement)
- Trust ↑ for specific person → Attachment ↑ for that person

Implementation approaches:
- A: Modify MoodManager to apply coupling after each emotion event
- B: Add a separate coupling tick that runs at lower frequency
- C: Implement as additional emotion events that fire on threshold crossings

### 3. Resonance Transitions
**Status:** OPEN

Current: Emotion values change via additive affectors with decay graphs
Proposed: Changes oscillate toward target value with damping

The difference: if Trust is at 0.3 and an event pushes it toward 0.7:
- **Current:** Jumps to 0.7, then decays toward baseline
- **Resonance:** Overshoots to ~0.8, oscillates back through 0.7, settles at 0.65

Implementation: Replace linear decay with damped oscillation function
- Parameters: frequency, damping ratio, overshoot allowance
- These can vary per dimension (Trust oscillates slowly, Stimulated oscillates fast)

### 4. Trajectory Memory
**Status:** OPEN

Current: Only current emotion values stored
Proposed: Ring buffer of recent emotion states (last N ticks or last T seconds)

Purpose:
- Detect emotional momentum (trending happy vs trending frustrated)
- Enable "mood" to be a computed property of trajectory, not a separate variable
- Feed trajectory data to L2 for context-aware behavior selection

### 5. Proximity Weighting
**Status:** OPEN

Current: All dimensions equal weight
Proposed: Dimensions closer to (self) resist change more

Proximity assignments (candidates):
- **Core (highest inertia):** Trust, Attachment
- **Mid (medium inertia):** Confident, Happy
- **Peripheral (lowest inertia):** Stimulated, Curious, Fatigue

Effect: A loud sound can spike Stimulated instantly, but Trust only shifts over many interactions. This matches how biological organisms work — startle response is instant, trust is earned.

### 6. Idle Behavior (Creature Feel)
**Status:** OPEN

What Vector does when nothing is happening:
- Current: Scripted idle animations, occasional exploration drive
- Proposed: Emotion state drives micro-behaviors continuously

Examples:
- Low Stimulated + High Curious → slow exploratory head movements, tracking sounds
- High Social + No face detected → turn toward last known person location
- High Fatigue + On charger → reduced eye blink rate, slower movements, "drowsy" face
- Moderate everything (baseline) → subtle breathing rhythm in body + eye movements

---

## Interface with Layer 2

L1 exposes to L2:
- Current emotion state vector (all dimensions)
- Trajectory buffer (recent history)
- Active behavior and its parameters
- Interrupt capability (L2 can inject high-priority emotion events)

L1 receives from L2:
- Processed perception events (fused multimodal stimuli)
- Attention-weighted salience scores
- Behavior recommendations with context

---

## Interface with Hardware

L1 talks to hardware through existing Vector services:
- vic-engine: emotion model, behavior tree, vision
- vic-robot: motor commands (via behavior actions)
- vic-anim: animation triggers with emotion parameters
- Body board: sensor data (via vic-robot → vic-engine)

**Safety constraint:** L1 never bypasses MandatoryPhysicalReactions priority. Cliff detection, fall response, and low-battery handling remain at highest priority always.

---

## Implementation Notes

_To be filled as decisions are made._

---

## TRM References

| Topic | Chapter | Pages | Key Detail |
|-------|---------|-------|------------|
| Emotion dimensions | Ch29.121.2 | 430-431 | 5 dimensions defined |
| Decay graphs | Ch29.121.5.2 | 431-432 | XY time/value decay structure |
| Emotion config files | Ch29.121.5 | 431 | `/config/engine/emotionevents/` |
| Mood config | Ch29.121.6 | 432 | `/config/engine/mood_config.json` |
| Simple moods | Ch29.121.3 | 431 | Named attractor basins |
| Behavior-emotion link | Ch29.121.4 | 431 | Behavior tree posts emotion events |
| Animation emotion params | Ch6.16.2 | 64-65 | Emotion state modulates animation |
| Audio emotion params | Ch29.121.6 | 432 | audioParameterMap in mood config |
