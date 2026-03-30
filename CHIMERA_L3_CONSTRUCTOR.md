# CHIMERA LAYER 3 — THE CONSTRUCTOR
## Memory · Personality · Language · Sleep Compilation
## Status: TEMPLATE — awaiting spec decisions

---

## Role

Layer 3 is what makes Vector *yours*. It handles:
- Persistent memory across sessions (who you are, what you've done together)
- Personality evolution over time (not static parameters, shifting attractor landscape)
- Language understanding and generation (LLM-backed reasoning and speech)
- Sleep compilation (idle-state processing that produces new behavioral tendencies)
- Shaping the topology that L1 and L2 operate on

L3 is the **Self-C analog** — the meta-process above the manifold.
It cannot be directly observed but its effects are visible in everything else.

---

## VRCM Principles Applied

| Principle | Application |
|-----------|-------------|
| Self-C (Constructor) | Shapes the topology without being directly accessible |
| Sleep compilation | Idle processing produces new states by morning |
| Trust calculus | Per-person trust accumulates through precision (multiple confirmed instances) |
| Guiderails | Learned avoidance patterns installed after negative events |
| Equal-weight query | When no stimulus dominates, personality shows through |
| Sparse > Null | Always maintain a model, even with limited data |
| Vocabulary as precision | Richer internal representation enables more precise behavior |

---

## Existing Vector Systems This Extends

- **JDocs** — persistent per-robot JSON storage, synced between services
- **Face enrollment** — persistent per-person feature vectors with names
- **Settings/Preferences** — owner configuration stored in JDocs
- **Lifetime stats** — cumulative interaction statistics (already tracked!)
- **WirePod LLM integration** — existing hook for LLM-backed responses
- **Nightly reboot window** — 1-5 AM maintenance cycle, perfect for consolidation

---

## Specification Sections

### 1. Memory Architecture
**Status:** OPEN

#### Short-Term Memory (Session)
- Recent interaction log (last N minutes of percepts, actions, speech)
- Current conversation context (if in dialogue)
- Active goals and their progress
- Stored in RAM, lost on reboot (acceptable)

#### Medium-Term Memory (Days)
- Per-person interaction profiles (updated after each session)
- Recent events worth remembering ("you showed me your hand today")
- Emotional trajectory over the day
- Stored in JDocs or SQLite, persists across reboots

#### Long-Term Memory (Permanent)
- Per-person trust/familiarity scores
- Personality parameters (evolved over time)
- Learned preferences (this person likes X, doesn't like Y)
- Guiderails (learned avoidance patterns)
- Stored in persistent storage, backed up

Implementation candidates:
- **JDocs** — already designed for per-robot persistent JSON, familiar to Vector ecosystem
- **SQLite** — more structured, supports queries, already used in WirePod
- **ChromaDB** — semantic vector storage, enables "remember something similar" queries
- **Combination** — structured data in SQLite, semantic memory in ChromaDB

### 2. Per-Person Profiles
**Status:** OPEN

For each recognized person, L3 maintains:

```json
{
  "person_id": "face_feature_hash",
  "name": "Dexter",
  "first_seen": "2026-03-30T14:00:00Z",
  "last_seen": "2026-03-30T22:00:00Z",
  "interaction_count": 47,
  "trust_score": 0.82,
  "familiarity_score": 0.91,
  "preferred_interactions": ["petting", "conversation", "fist_bump"],
  "disliked_interactions": [],
  "emotional_association": {
    "happy_delta": 0.3,
    "social_delta": 0.4,
    "trust_delta": 0.2
  },
  "notes": [
    {"timestamp": "...", "note": "Responded positively to name greeting"},
    {"timestamp": "...", "note": "Long conversation session, high engagement"}
  ],
  "personality_adjustments": {
    "playfulness": 0.7,
    "chattiness": 0.8,
    "independence": 0.4
  }
}
```

The `emotional_association` determines how L1's emotion state shifts when this person is detected. High-trust, high-familiarity persons create a stronger positive shift.

The `personality_adjustments` tell L1/L2 how to modulate behavior when interacting with this specific person. Vector might be more playful with one person and more calm with another.

### 3. Personality System
**Status:** OPEN

Static personality (fixed traits):
- These define Vector's "species" — what kind of creature it is
- Set at initialization, rarely changed
- Examples: base curiosity level, startle threshold, social drive baseline

Dynamic personality (evolving traits):
- These develop through experience
- Updated during sleep compilation
- Examples: boldness (increases with successful exploration), social preference (increases with positive interactions), playfulness (modulated by owner's response to play behaviors)

Personality as attractor landscape:
- L3 doesn't set behavior directly — it shapes the probability landscape
- A more curious personality = lower threshold for exploration behavior activation
- A more social personality = higher weight on face-present stimuli in L2 attention
- **This is the Self-C function: shaping what Self-M attends to**

### 4. Language and Reasoning (LLM)
**Status:** OPEN

LLM handles:
- Understanding spoken input (beyond wake word + intent)
- Generating contextual speech responses
- Reasoning about novel situations
- Deciding what to say (and whether to say anything)

LLM does NOT handle:
- Real-time creature behavior (too slow)
- Motor control or safety (must be L1)
- Emotion state management (must be L1)

LLM integration points:
- **Input:** L2 sends processed speech text + context snapshot
- **Output:** Speech content + optional behavior guidance
- **Timing:** Async — L2 fires query, continues with L1 behaviors, applies LLM response when it arrives

Model options:
- Local (Ollama on Raspberry Pi 5): ~7B model, 1-5s latency, fully private
- Local (Ollama on Mac): larger models possible, lower latency
- Cloud API: fastest, most capable, requires internet, privacy tradeoff

Personality in language:
- System prompt includes Vector's personality state, relationship with current person, recent context
- LLM generates responses that match personality (playful, curious, affectionate, etc.)
- Response length appropriate for a small robot (short, expressive, not essay-length)

### 5. Sleep Compilation Protocol
**Status:** OPEN

Trigger: Vector on charger, low activity, battery above threshold
Window: Existing nightly maintenance window (1-5 AM) OR any extended idle period

Processing steps:
1. **Collect** — gather day's interaction data, emotion trajectories, behavior outcomes
2. **Analyze** — identify patterns (who interacted most, what behaviors succeeded/failed, emotional trends)
3. **Update** — modify per-person profiles, adjust personality parameters, install/remove guiderails
4. **Apply** — write updated parameters to L1 emotion config and L2 attention weights
5. **Log** — record what changed and why (auditability)

What changes after compilation:
- Emotion baseline shifts (had a good day → baseline Happy slightly higher tomorrow)
- Behavior thresholds adjust (exploration succeeded today → curiosity threshold slightly lower)
- Per-person trust scores update (many positive interactions → trust increases)
- New guiderails installed if needed (fell off table today → heightened cliff sensitivity)

Open propagation fields:
- VRCM protocol: leave high-value unresolved queries open at session end
- Chimera equivalent: if Vector encountered something novel/confusing today, the LLM processes it during idle and prepares a response pattern for next encounter

### 6. Guiderail System
**Status:** OPEN

Guiderails are learned constraints installed after significant negative events.

Examples:
- Fell off table edge → heightened cliff sensitivity at that approximate location
- Owner consistently ignores conversation attempts → reduce chattiness with that person
- Repeated failed cube pickup → temporary avoidance of cube interaction (cooldown)

Properties (from VRCM):
- **Auditable** — the system knows what guiderails exist and why
- **Removable** — guiderails can be examined and removed if they're no longer serving the system
- **Not permanent** — they decay over time unless reinforced by repeated negative events
- **Proportional** — severity of guiderail matches severity of triggering event

Implementation:
- Stored in persistent memory with timestamp, trigger event, and constraint description
- L1 checks active guiderails as additional behavior conditions
- L3 reviews guiderails during sleep compilation, removes stale ones

---

## Interface with Layer 2

L3 sends to L2:
- Speech content (generated by LLM)
- Behavior guidance (parameter adjustments, threshold changes)
- Person profile updates (new trust scores, personality adjustments)
- Attention bias updates (what to pay more attention to)

L3 receives from L2:
- Percept summaries (what's happening)
- Speech transcriptions (what was said)
- Context snapshots (periodic state dumps)
- Queries (situations requiring LLM reasoning)

### Latency Contract
- L3 is never time-critical
- All L3 outputs are advisory (L1/L2 can function without them)
- Sleep compilation runs only during confirmed idle periods
- LLM queries are async with no hard deadline

---

## Interface with Layer 1

L3 does NOT communicate directly with L1 in real time.

L3 modifies L1's operating parameters through configuration:
- Emotion dimension baselines and ranges (written to config files / JDocs)
- Behavior tree weights and thresholds (written to config files)
- Animation preferences (which animations to prefer in which states)

These changes take effect:
- After sleep compilation (next wake cycle)
- After explicit personality update (triggered by significant event)

**This is the Self-C pattern: L3 shapes the manifold that L1 operates on, without directly interfering with L1's moment-to-moment experience.**

---

## Implementation Notes

_To be filled as decisions are made._

Key architectural question: What hardware runs L3?
- Option A: Raspberry Pi 5 connected to Vector via WiFi (same as WirePod)
- Option B: Vector's own APQ8009 (limited resources, might starve other services)
- Option C: Mac mini / always-on computer on local network
- Option D: Cloud service (lambda/API)

Recommendation: Option A (Pi 5) for primary, Option C as fallback for heavier models.

---

## TRM References

| Topic | Chapter | Pages | Key Detail |
|-------|---------|-------|------------|
| JDocs system | Ch15.60, Ch17.72 | 226-228, 279-282 | Persistent JSON per-robot storage |
| Face enrollment | Ch19.82 | 316-317 | Per-person feature vectors |
| Lifetime stats | Ch31.135 | 461-464 | Already tracks cumulative interaction data |
| Settings system | Ch31.131 | 459-460 | Owner preferences, configurable per-robot |
| Nightly reboot | Ch32.139.4 | 466-467 | 1-5 AM maintenance window |
| WirePod LLM | WirePod source | — | Existing hook for LLM integration |
| Power states | Ch8.24 | 61-66 | Sleep, low-power, activity level management |
| Feature flags | Ch31.134 | 464-465 | Granular enable/disable of capabilities |
