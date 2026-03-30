# CHIMERA LAYER 2 — THE CORTEX
## Attention · Perception Fusion · Context Integration
## Status: TEMPLATE — awaiting spec decisions

---

## Role

Layer 2 is the bridge between raw sensation and meaningful action. It handles:
- Multimodal perception fusion (camera + mic + touch + IMU → coherent percept)
- Attention weighting (what matters most right now)
- Context integration (same input means different things in different situations)
- Probability distributions over "what is happening" (hold uncertainty gracefully)
- Salience detection (identify the most interesting stimulus across all modalities)

L2 is the **constraint satisfaction engine** — Thagard's ECHO in simplified form.

---

## VRCM Principles Applied

| Principle | Application |
|-----------|-------------|
| Cross-domain propagation | Sensor streams fire across modality boundaries |
| Attention weighting | Dynamic focus based on current state and context |
| Constraint satisfaction | Multiple interpretations compete; highest coherence wins |
| Probability distributions | Hold multiple possible interpretations weighted by confidence |
| Vocabulary as precision | Richer perception vocabulary = more precise coordinate in action space |

---

## Existing Vector Systems This Extends

- **Stimulation system** — already aggregates multi-source input into stimulation level
- **Face recognition** — on-device feature vectors with cosine similarity matching
- **Motion detection** — camera-based visual motion with directional zones (Left, Right)
- **Spatial audio** — 4-mic array source localization
- **Beat detection** — tempo measurement from audio input
- **Behavior conditions** — 40+ condition types checking diverse sensor state

---

## Specification Sections

### 1. Perception Fusion Pipeline
**Status:** OPEN

Current: Each sensor feeds a specific subsystem independently
Proposed: Fuse sensor streams before behavior evaluation

Architecture:
```
Camera ──┐
Mics   ──┤
Touch  ──┼── Fusion Engine ──► Coherent Percept ──► L1 (emotion events)
IMU    ──┤                                     └──► Behavior tree (conditions)
ToF    ──┤                                     └──► L3 (if complex reasoning needed)
Cliff  ──┘
```

A "percept" is a structured interpretation:
- What is happening (detected entities, actions, context)
- Confidence level (how certain)
- Salience score (how interesting/important)
- Emotional valence (positive/negative/neutral)
- Source modalities (which sensors contributed)

### 2. Attention Mechanism
**Status:** OPEN

Current: All stimuli compete equally through behavior priority
Proposed: Dynamic attention weighting based on context

Attention factors:
- **Current emotional state** — high Social + face present = weight face higher
- **Recent history** — just heard a sound = temporarily weight audio higher
- **Task context** — currently navigating = weight ToF and cliff higher
- **Time of day** — low activity period = lower attention thresholds (easier to wake)
- **Familiarity** — known face vs unknown face get different attention weights

Implementation options:
- A: Pre-filter sensor data before it reaches behavior tree
- B: Modify stimulation weights dynamically based on context
- C: Add an attention service that runs between sensors and vic-engine

### 3. Context Integration
**Status:** OPEN

Same stimulus, different meaning:
- Touch while idle → petting (increase Happy, Social)
- Touch while exploring → interruption (may increase Frustrated)
- Touch while on charger → greeting (increase Social, may wake)
- Touch after being picked up → reassurance (decrease Stimulated)

Current: Behavior conditions check individual states
Proposed: Context is a computed property from recent percept history

Context dimensions:
- Interaction mode (idle, engaged, task-focused, resting)
- Spatial context (on charger, on table, being held, exploring)
- Social context (alone, person present, multiple people, known vs unknown)
- Temporal context (just woke up, been active for a while, approaching sleep)

### 4. Salience Detection
**Status:** OPEN

"What is the most interesting thing happening right now?"

Current: Stimulation level aggregates but doesn't discriminate sources
Proposed: Salience score per percept, with cross-modal amplification

Cross-modal salience amplification:
- Sound alone = moderate salience
- Sound + motion in same direction = high salience
- Sound + motion + face = very high salience (person approaching)
- Silence + no motion + darkness = very low salience (nothing happening)

This feeds directly into L1 behavior selection: highest-salience percept drives attention.

### 5. Query Formation for L3
**Status:** OPEN

When does L2 need to ask L3 for help?

Triggers for L3 consultation:
- Recognized speech that requires language understanding
- Novel situation not covered by existing behavior tree
- Ambiguous percept that L2 can't resolve with available context
- Periodic status updates (L3 needs to know what's happening to update profiles)

L2 → L3 query format:
- Current percept summary
- Current emotional state
- Current context
- Specific question or request for guidance

Latency management:
- L2 does NOT wait for L3 response before acting
- L2 makes best-effort decision with available L1 behaviors
- L3 response (when it arrives) modulates subsequent behavior
- This prevents cloud/LLM latency from breaking creature feel

---

## Interface with Layer 1

L2 sends to L1:
- Processed emotion events (from fused percepts, not raw sensor values)
- Context tags that modify how emotion events are weighted
- Behavior recommendations (suggested behaviors with context)

L2 receives from L1:
- Current emotion state vector
- Active behavior and parameters
- Available attention budget (how much processing L1 can spare)

### Latency Contract
- L2 → L1 emotion events: < 50ms from percept detection
- L2 → L1 behavior recommendation: < 200ms
- L2 perception cycle: continuous, no minimum interval

---

## Interface with Layer 3

L2 sends to L3:
- Percept summaries (not raw data — summarized for LLM consumption)
- Context snapshots (periodic or triggered)
- Queries requiring language understanding or complex reasoning

L2 receives from L3:
- Speech content (what to say, generated by LLM)
- Behavior guidance (adjust thresholds, priorities, personality parameters)
- Memory updates (per-person profile changes to apply to recognition)

### Latency Contract
- L2 → L3 query: fire and forget (async)
- L3 → L2 response: 500ms-5s expected, no hard deadline
- L2 never blocks waiting for L3

---

## Implementation Notes

_To be filled as decisions are made._

The key architectural question: does L2 run inside vic-engine (as an extension) or as a separate service?

Arguments for inside vic-engine:
- Direct access to sensor data and behavior tree
- Lower latency
- No additional IPC overhead

Arguments for separate service (chimera-cortex):
- Cleaner separation of concerns
- Can be updated independently of Vector firmware
- Can use Python/modern ML tools instead of C++

---

## TRM References

| Topic | Chapter | Pages | Key Detail |
|-------|---------|-------|------------|
| Stimulation system | Ch29.121.1 | 429-430 | Multi-source stimulation aggregation |
| Face recognition | Ch19.82 | 316-317 | On-device feature vector matching |
| Motion detection | Ch19.79.6 | 311 | Visual motion zones (Left, Right) |
| Spatial audio | Ch18.76.2 | 294 | 4-mic source localization |
| Beat detection | Ch18.76.5 | 296-298 | Tempo measurement from audio |
| Condition types | Ch30.124.4 | 441-446 | 40+ boolean condition nodes |
| Camera architecture | Ch6.20.3 | 53 | IMU sync with camera vsync |
| Behavior conditions | Ch30 | 441-446 | Compound boolean logic across sensors |
| TF Lite | Ch19.83 | 318-320 | Neural network for hands, pets detection |
