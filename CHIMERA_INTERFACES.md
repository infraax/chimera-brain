# CHIMERA INTERFACES
## Inter-Layer Communication Protocols
## Status: TEMPLATE — awaiting spec decisions

---

## Overview

The three chimera layers communicate through defined interfaces.
The design principle: **each layer can function without the others, but functions better with them.**

- L1 alone = stock Vector (creature feel, no learning, no language)
- L1 + L2 = contextually aware Vector (smarter reactions, no memory)
- L1 + L2 + L3 = full chimera (creature feel + context + memory + personality + language)

This graceful degradation is essential. If L3 is offline (no Pi, no cloud), Vector should still feel alive. If L2 has an error, L1's existing behavior tree still works.

---

## Communication Topology

```
                    ┌─────────────┐
                    │   LAYER 3   │
                    │ Constructor  │
                    │ (Pi / Cloud) │
                    └──────┬──────┘
                           │
              Async API    │    Config writes
              (HTTP/gRPC)  │    (JDocs/JSON)
                           │
                    ┌──────┴──────┐
                    │   LAYER 2   │
                    │   Cortex    │
                    │  (Pi / bot) │
                    └──────┬──────┘
                           │
              Events       │    Commands
              (socket/API) │    (SDK gRPC)
                           │
                    ┌──────┴──────┐
                    │   LAYER 1   │
                    │  Brainstem  │
                    │  (on-bot)   │
                    └──────┬──────┘
                           │
                    Vector Hardware
```

---

## L1 ↔ L2 Interface

### L2 → L1 (Perception to Reaction)

| Message Type | Content | Latency Target | Delivery |
|-------------|---------|----------------|----------|
| EmotionEvent | Processed stimulus → emotion affector | < 50ms | Fire and forget |
| BehaviorSuggestion | Recommended behavior + priority + context | < 200ms | Advisory |
| AttentionDirective | "Look at this" / "Listen for that" | < 100ms | Soft override |
| ContextTag | Current interaction mode, spatial context | < 500ms | State update |

**EmotionEvent** — L2 processes raw sensor data into coherent percepts, then translates each percept into one or more emotion events that L1's MoodManager understands. This uses the existing emotion event system — no new protocol needed.

**BehaviorSuggestion** — L2 can suggest behaviors to L1, but L1's priority system has final say. Safety behaviors always override. This maps to the existing SDK behavior control mechanism.

**AttentionDirective** — L2 can ask L1 to orient toward a stimulus (turn head, move toward sound). Implemented as behavior submissions at appropriate priority.

### L1 → L2 (State to Context)

| Message Type | Content | Frequency | Delivery |
|-------------|---------|-----------|----------|
| EmotionStateVector | All dimension values + trajectory | Every emotion tick (~100ms) | Stream |
| BehaviorState | Active behavior, priority, progress | On change | Event |
| SensorSnapshot | Raw sensor summary | On request | Pull |

L2 needs L1's emotional state to contextualize new percepts. A touch when Happy means something different than a touch when Frustrated.

---

## L2 ↔ L3 Interface

### L2 → L3 (World to Mind)

| Message Type | Content | Timing | Delivery |
|-------------|---------|--------|----------|
| PerceptSummary | What's happening (entities, actions, confidence) | On significant event | Async |
| SpeechTranscription | What was said + speaker identity | On speech detected | Async |
| ContextSnapshot | Full state dump (emotion, behavior, spatial, social) | Periodic (every 30s during active interaction) | Async |
| ReasoningQuery | "I don't know how to handle this" + context | On novel situation | Async + wait |

**All L2 → L3 messages are async.** L2 never blocks waiting for L3.

**PerceptSummary** format (candidate):
```json
{
  "timestamp": "2026-03-30T22:15:00Z",
  "percept_type": "person_interaction",
  "entities": [
    {"type": "face", "id": "dexter_001", "confidence": 0.94, "expression": "smiling"}
  ],
  "audio": {"speech_detected": true, "text": "Hey Vector, how are you?"},
  "context": {"mode": "engaged", "spatial": "on_table", "social": "one_person_known"},
  "emotion_state": {"stimulated": 0.6, "social": 0.7, "happy": 0.5, "confident": 0.4, "trust": 0.8},
  "salience": 0.85
}
```

### L3 → L2 (Mind to World)

| Message Type | Content | Timing | Delivery |
|-------------|---------|--------|----------|
| SpeechResponse | Text to speak + emotion modifiers | After LLM processing | Async |
| BehaviorGuidance | Adjust thresholds, weights, priorities | Periodic or on profile update | Async |
| PersonUpdate | Updated per-person profile data | After interaction analysis | Async |
| AttentionBias | "Pay more attention to X" | After pattern recognition | Async |

**SpeechResponse** includes not just text but emotional metadata:
```json
{
  "text": "Hi Dexter! I missed you today.",
  "emotion_modifiers": {"social": 0.3, "happy": 0.2},
  "animation_suggestion": "greeting_happy",
  "energy_level": "high"
}
```

L2 translates this into:
1. TTS command to WirePod
2. Emotion events to L1
3. Animation trigger to vic-anim

---

## L3 → L1 Interface (Indirect)

L3 does NOT send real-time messages to L1.
L3 modifies L1's configuration files, which L1 reads:

| Modification | Target | When Applied |
|-------------|--------|--------------|
| Emotion baselines | mood_config.json | After sleep compilation |
| Behavior thresholds | behavior tree JSON | After sleep compilation |
| Dimension ranges | mood_config.json ValueRange | After sleep compilation |
| New emotion events | emotionevents/ JSON files | After sleep compilation |
| Guiderail conditions | behavior tree condition nodes | After significant event |

**Application trigger:** L3 writes config updates. A signal (file flag or service notification) tells vic-engine to reload configs. On Vector's existing architecture, this likely requires a service restart — which the nightly reboot already provides.

For more urgent updates, the SDK API provides real-time emotion event injection (via the HTTPS API), allowing L3 to influence L1 through L2 as a relay.

---

## Error Handling

### L3 Offline
- L2 continues with last-known person profiles
- L1 continues with current emotion parameters
- No language/speech responses (or fall back to WirePod's built-in intent system)
- Vector functions as a smarter-than-stock creature without personality evolution

### L2 Offline
- L1 continues with stock Vector behavior tree
- No multimodal perception fusion
- No contextual interpretation
- Vector functions as stock Vector (still 60% creature)

### L1 Degraded
- If emotion model fails, behavior tree falls through to safety behaviors
- MandatoryPhysicalReactions always function (cliff, fall, battery)
- This is already handled by Vector's existing architecture

### Communication Failure
- All inter-layer messages are fire-and-forget or async
- No layer ever blocks on another layer's response
- Timeouts produce graceful degradation, not crashes
- **Sparse over null:** if a message is lost, use last-known state (don't reset to zero)

---

## Protocol Candidates

### Option A: HTTP/REST (simplest)
- L2 and L3 run as HTTP services
- Standard JSON payloads
- Works across any network topology (local, WiFi, internet)
- Higher latency than direct socket

### Option B: gRPC (Vector-native)
- Vector already uses gRPC for SDK communication
- Binary protobuf = lower overhead
- Streaming support for continuous state updates
- More complex setup

### Option C: Unix sockets (lowest latency)
- If L2 runs on the same device as Vector
- Mimics existing vic-* service communication
- Not suitable for cross-device communication

### Recommendation
- **L1 ↔ L2:** SDK gRPC (already exists) + emotion events via existing MoodManager interface
- **L2 ↔ L3:** HTTP/REST for simplicity. Can upgrade to gRPC if latency becomes an issue
- **L3 → L1 config writes:** Direct file writes (if on same device) or SSH/SCP (if on Pi)

---

## Implementation Phases

### Phase 1: Minimum Viable Interface
- L2 sends emotion events to L1 via SDK API
- L3 sends speech via WirePod's existing LLM hook
- No persistent memory yet, no personality evolution
- Proves the layer separation works

### Phase 2: Full L2 ↔ L3 Pipeline
- L2 sends percept summaries to L3
- L3 sends speech + behavior guidance back
- Per-person profiles begin accumulating
- LLM personality in responses

### Phase 3: Sleep Compilation
- L3 processes idle-state consolidation
- Config writes modify L1 parameters
- Personality evolution begins
- Guiderail system active

### Phase 4: Full Chimera
- All interfaces operational
- Resonance in L1 emotion transitions
- Attention mechanism in L2
- Memory and personality in L3
- The creature lives

---

## TRM References

| Topic | Chapter | Pages | Key Detail |
|-------|---------|-------|------------|
| Service architecture | Ch6.16.1 | 62-64 | vic-* services, communication patterns |
| Inter-process comms | Ch6.16.1 | 64 | Unix sockets, CLAD/JSON, message threads |
| SDK HTTPS API | Ch15 | 148-272 | Full API surface for external control |
| gRPC protocol | Ch15.43 | 148 | SDK message groupings |
| Event stream | Ch15.52.2 | 177 | Continuous event subscription |
| Behavior control | Ch15.46.4 | 153-154 | SDK behavior assume/release |
| Emotion events | Ch29.121.4 | 431 | How behavior posts to MoodManager |
| JDocs protocol | Ch17.72 | 279-282 | Persistent data read/write |
| WirePod integration | WirePod source | — | gRPC server, intent pipeline, LLM hooks |
