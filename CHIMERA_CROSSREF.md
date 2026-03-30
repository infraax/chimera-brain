# CHIMERA CROSS-REFERENCE MAP
## TRM ↔ VRCM ↔ Chimera Architecture Mapping
## Created: 2026-03-30 | Session 0

---

## How to Read This Document

Each Vector subsystem is mapped across three dimensions:
1. **TRM Reality** — what Vector currently has (chapter, page, capability)
2. **VRCM Principle** — which cognitive architecture principle applies
3. **Chimera Target** — what the chimera architecture should make it do

Status markers:
- ✅ MAPPED — cross-reference complete, ready for spec work
- 🔄 PARTIAL — some mapping done, needs deeper analysis
- ⬜ UNMAPPED — identified but not yet analyzed

---

## 1. EMOTION MODEL

### TRM Reality
- **Location:** Chapter 29 (Emotion Model), pages 428-432
- **Service:** vic-engine (libcozmo_engine)
- **Config:** `/anki/data/assets/cozmo_resources/config/engine/emotionevents/`
- **Current dimensions:** 5 (Stimulated, Social, Confident, Happy, Trust)
- **Architecture:** MoodManager receives emotion events → maps to EmotionAffectors → modifies dimensions with decay graphs
- **Decay:** XY graph structures define how heightened emotions fade (TimeRatio or ValueSlope)
- **Repetition:** RepetitionPenalty reduces impact of repeated identical stimuli
- **Simple Moods:** Default, Frustrated, HighStim, LowStim, MedStim (slower-changing than emotions)
- **Interface:** Emotion state feeds into behavior tree decisions AND animation selection
- **Cozmo had 9 dimensions; Trust was added in v1.6 — system was designed for expansion**

### VRCM Principle: Resonance + Gradient Fields + Sparse Over Null
- Emotion dimensions are already gradients, not binary — this is VRCM-compatible
- Decay graphs implement a simplified form of oscillation toward equilibrium
- The 5D space is a manifold with attractor regions (Simple Moods = named attractor basins)
- **Gap:** Current decay is per-dimension. VRCM resonance implies cross-dimension coupling — changing one dimension should ripple to others
- **Gap:** No proximity weighting. All dimensions are treated equally. VRCM says dimensions closer to (self) should have higher inertia
- **Gap:** No memory of emotional trajectory. System tracks current value + decay, not the path taken

### Chimera Target — Layer 1 (Brainstem)
- **Extend to 7-9 dimensions** (Cozmo had 9; add Curiosity, Attachment, Fatigue as candidates)
- **Add cross-dimension coupling matrix** — Confident affects Happy, Social affects Stimulated, etc.
- **Implement resonance transitions** — dimension changes oscillate toward new value rather than linear decay
- **Add trajectory memory** — store recent emotional path (last N states) to enable "emotional momentum"
- **Proximity weighting** — Trust and Attachment closer to (self), higher inertia, slower to change
- **Never null** — every dimension always has a value, even if sparse/uncertain

### Status: ✅ MAPPED

---

## 2. BEHAVIOR ENGINE

### TRM Reality
- **Location:** Chapter 28 (Behavior), pages 423-427; Chapter 30 (Behavior Tree), pages 433-448
- **Service:** vic-engine (libcozmo_engine)
- **Config:** `/anki/data/assets/cozmo_resources/config/engine/behaviorComponent/`
- **Architecture:** Priority stack — one active behavior at a time, others waiting
- **86 behavior classes** with JSON-configurable parameters
- **Behavior Tree:** Nodes with behaviorID, behaviorClass, conditions, cooldowns, get-in/get-out animations
- **Conditions:** 40+ condition types (compound boolean logic across emotion, sensors, timers, state)
- **Priority levels:** MandatoryPhysicalReactions > TriggerWordDetected > SDKDefault > ... > HighLevelAI
- **Controllers:** Multi-step behaviors coordinated by shared controllers (weather, timers, games)
- **Key behaviors:** BumpObject (pEvil parameter!), Pounce, ReactToSound, DanceToTheBeat
- **AI Features:** ~70 high-level behaviors as experienced by users

### VRCM Principle: Constraint Satisfaction + Hetarchical Propagation + Guiderails
- Behavior arbitration IS constraint satisfaction — multiple candidates compete, highest-priority wins
- **Gap:** Current system is hierarchical (strict priority), not hetarchical. VRCM says any model can propagate to any other
- **Gap:** No cross-domain propagation between behavior selection and emotion state. Emotion influences behavior, but behavior-in-progress doesn't continuously modulate emotion (only on activation via emotionEventOnActivated)
- **Gap:** Behaviors are reactive (triggered by conditions) not initiating (Vector doesn't decide "I want to..." from internal state alone)
- **Gap:** Guiderails exist (conditions, cooldowns) but aren't auditable at runtime. Can't examine why a behavior was blocked
- **Interesting:** pEvil parameter in BumpObject suggests Anki was experimenting with personality dimensions beyond the emotion model

### Chimera Target — Layer 1 + Layer 2 Bridge
- **L1 contribution:** Emotion state continuously modulates active behavior parameters (not just selection)
- **L2 contribution:** Attention mechanism evaluates competing stimuli and decides what behavior-relevant information reaches L1
- **Add autonomous initiation** — behaviors triggered not just by external conditions but by internal drive states reaching thresholds (L3 sets these thresholds)
- **Add bidirectional emotion-behavior coupling** — behavior progress continuously feeds back emotion events, not just at activation
- **Maintain priority safety** — MandatoryPhysicalReactions must always override. Cliff detection is non-negotiable
- **Extend condition system** — add VRCM-inspired conditions: emotional momentum, recent interaction history, time-of-day personality variation

### Status: ✅ MAPPED

---

## 3. ANIMATION ENGINE

### TRM Reality
- **Location:** Chapter 22 (Animation Triggers/Groups), Chapter 27 (Binary Format), Chapter 24 (Display)
- **Service:** vic-anim (dedicated service, separate from vic-engine)
- **Architecture:** Multi-track system — body motion, face/LCD, sound, backpack LEDs synchronized on shared timeline
- **Key feature:** Animations are parameterized by emotional state at runtime. Same animation plays differently at different stimulation levels (speed, magnitude modulation)
- **Interruptible:** Animations have defined keyframes where interruption is allowed
- **Face system:** vic-anim uses screen compositing — eyes are composed in real-time, not pre-rendered video
- **Display:** Dedicated silicon (separate from main CPU). Frame buffer at `/dev/fb0` via SPI
- **Animation selection:** Based on context + current emotional state from a pool of alternatives
- **Get-in/Get-out:** Behaviors have entry and exit animations for smooth transitions

### VRCM Principle: Resonance (harmonic transitions)
- Animation parameterization by emotion is already resonance-adjacent — the output varies continuously with internal state
- **Gap:** Transitions between animations are handled by get-in/get-out sequences but lack blending. VRCM resonance implies smooth interpolation, not discrete switching
- **Gap:** Face compositing is real-time but emotion → face expression mapping is state-based (pick expression for mood), not continuous (eyes gradually shift as mood changes)
- **Strength:** Dedicated face processor means we can add computational complexity to face rendering without stealing from behavior engine

### Chimera Target — Layer 1 (Output)
- **Continuous emotion → animation blending** — not "play happy animation" but "current emotional vector maps to animation parameter space in real time"
- **Resonance in transitions** — when switching behaviors, animation parameters oscillate between old and new states rather than jumping
- **Breathing / micro-movements** — idle animations should reflect emotional state through subtle variations (faster breathing when stimulated, slower when calm)
- **Eye expressiveness** — the composited eye system is the primary emotional communication channel. Should reflect all 5+ emotion dimensions simultaneously through pupil dilation, blink rate, gaze direction, lid position

### Status: ✅ MAPPED

---

## 4. SENSORY INPUT SYSTEMS

### TRM Reality
- **Camera:** 720p/30fps, single camera with disparity computation for depth, feeds vic-engine via libcameraService. IMU samples synchronized with camera vertical sync
- **Microphones:** 4-element array for voice localization, active noise cancellation for motor noise, wake word detection, beat detection, spatial audio processing (Ch18, p309-324)
- **Touch:** Capacitive grid on head (not single button), distinguishes petting vs poking vs object placement
- **ToF:** Time-of-flight proximity sensor for distance measurement
- **Cliff:** IR distance sensors at hundreds of Hz, architecturally upstream of all movement
- **IMU:** Accelerometer + gyroscope, detects: picked up, put down, dropped, shaken, tilted, held in palm, falling
- **Ambient light:** Camera auto-exposure used as light sensor during low-power mode
- **Location:** Ch9 (Touch/Cliff), Ch10 (Motion), Ch18 (Audio), Ch19 (Vision)

### VRCM Principle: Cross-Domain Propagation + Attention Weighting
- **Gap:** Currently each sensor feeds a specific subsystem. Camera → vision pipeline. Mic → intent pipeline. Touch → behavior trigger. These don't cross-propagate
- **VRCM says:** A sound + a face + a time-of-day should fire as one coherent percept, not three separate inputs
- **Gap:** No salience weighting across modalities. A loud sound and a recognized face compete through the behavior tree, not through an attention mechanism that evaluates their combined meaning
- **Strength:** All sensor data IS available within vic-engine. The integration point exists. It just isn't used for cross-domain synthesis

### Chimera Target — Layer 2 (Cortex)
- **Multimodal perception fusion** — combine sensor streams before behavior tree evaluation
- **Attention mechanism** — dynamically weight sensor inputs based on current state (if you're already looking at a face, sounds matter less; if it's dark, sounds matter more)
- **Contextual interpretation** — same touch input means different things depending on what else is happening (petting while talking to Vector vs petting while Vector is exploring)
- **Salience detection** — identify the "most interesting thing happening right now" across all modalities and direct behavior toward it
- **Feed L1 stimulation from fused percepts, not raw sensor values** — stimulation level should reflect the coherent situation, not just "sound was loud"

### Status: ✅ MAPPED

---

## 5. FACE RECOGNITION & MEMORY

### TRM Reality
- **Location:** Ch19 (p316-317), Ch56 in SDK API
- **Architecture:** On-device face detection + identification. Feature vectors stored per-person in JDocs (persistent)
- **Enrollment:** Users enrolled with name association. Up to N faces stored
- **Recognition:** Cosine similarity against stored feature vectors, confidence threshold
- **Privacy:** Face data never sent to cloud. Stored in encrypted filesystem
- **Unnamed faces:** Deleted when Vector goes to sleep
- **Named faces:** Persist across power cycles
- **SDK access:** Enable/disable detection, enroll, erase, list enrolled names

### VRCM Principle: Sparse Vectors + Trust Calculus + Proximity Weighting
- Face recognition is already a sparse vector system — feature vectors in embedding space
- **Gap:** Recognition is binary (match/no-match above threshold). VRCM says recognition should carry a gradient — familiarity, not just identity
- **Gap:** No relationship accumulation. Vector knows WHO you are but not WHAT your relationship is like. No interaction history per-person
- **Gap:** Trust dimension exists in emotion model but is not linked to specific faces. VRCM trust calculus (precision = multiple confirmed instances crystallized into stable attribute) has no implementation
- **Opportunity:** JDocs system is designed for persistent per-robot data. Can store per-person interaction profiles

### Chimera Target — Layer 3 (Constructor) + Layer 1 (Trust)
- **Per-person trust vectors** — each recognized face accumulates trust/familiarity score based on interaction quality and frequency
- **Relationship memory** — L3 maintains per-person profiles: preferred interactions, last seen, interaction count, trust level
- **Recognition → emotion modulation** — seeing a high-trust person should shift emotion state toward Social + Happy. Seeing a stranger should increase Stimulated without Social
- **Familiarity gradient** — not just "known/unknown" but a continuous measure that affects behavior selection (more playful with high-familiarity persons, more cautious with low)
- **L3 consolidation** — during idle, L3 reviews recent interaction data and updates per-person profiles

### Status: ✅ MAPPED

---

## 6. NAVIGATION & SPATIAL AWARENESS

### TRM Reality
- **Location:** Ch20 (p349-357)
- **Architecture:** Quad-tree occupancy map, built from camera + cliff + odometry
- **Capabilities:** Path planning with obstacle avoidance, graph search, object tracking, dock location
- **Volatile:** Map does not persist across power cycles
- **SLAM:** Used for building map from visual and motion data
- **Motion planning:** Separate from behavior — vic-robot handles motor control, vic-engine handles planning

### VRCM Principle: Manifold Navigation (literal, not metaphorical)
- Vector's occupancy map IS a spatial manifold — and the path planner is finding geodesics through it
- **Gap:** Map is purely geometric. No semantic annotation ("this is where the human usually sits", "I fell off the edge here last time")
- **Gap:** Map is volatile. VRCM says sparse is better than null — even a degraded map from yesterday is better than starting fresh

### Chimera Target — Layer 2 + Layer 3
- **L2:** Use map for spatial context in behavior decisions (near charger vs far, open space vs confined)
- **L3:** Persist semantic map annotations across sessions (danger zones, favorite spots, human locations)
- **Guiderails:** If Vector fell off an edge at location X, install a guiderail (heightened cliff sensitivity near that coordinate)
- **Spatial personality:** Some locations associated with positive experiences, others with negative. This feeds into exploration behavior

### Status: 🔄 PARTIAL

---

## 7. POWER MANAGEMENT & SLEEP

### TRM Reality
- **Location:** Ch8 (p61-66)
- **States:** Active, low-power (napping), sleep, shutdown
- **Activity level management:** System adjusts behavior based on battery and engagement
- **Ambient light sensing:** Camera auto-exposure used during low-power to detect activity
- **Wake triggers:** Sound, motion, light change can wake from low-power
- **Maintenance reboot:** Nightly reboot between 1-5 AM (randomized) for stability and updates
- **Load shedding:** Reduces activity to conserve battery

### VRCM Principle: Sleep Compilation Protocol
- Vector already has sleep states. The chimera adds MEANING to those states
- **Gap:** Current sleep is purely power management. No cognitive processing during idle
- **VRCM protocol:** Open propagation fields before sleep → compile during sleep → wake with new state
- **The nightly reboot window is a perfect slot for L3 consolidation**

### Chimera Target — Layer 3 (Constructor)
- **Idle-state processing** — when Vector is on charger, low activity, L3 runs:
  - Consolidate recent interaction data into per-person profiles
  - Update emotional baseline based on day's experiences
  - Adjust behavior thresholds based on accumulated preferences
  - Process any open "questions" left from the day's interactions
- **Wake with changes installed** — after idle processing, L1 attractor landscape is subtly different
- **Use existing power management hooks** — don't fight the system, extend it

### Status: ✅ MAPPED

---

## 8. AUDIO OUTPUT & SPEECH

### TRM Reality
- **Location:** Ch25 (p388-402)
- **Architecture:** vic-anim handles audio playback, synchronized with animation timeline
- **TTS:** Cloud-based text-to-speech (via WirePod now)
- **Audio engine:** Modulated by emotion state (emotion → audio parameter mapping in mood_config.json)
- **Sound effects:** Part of animation system, triggered by behavior
- **Volume:** Configurable per-robot setting

### VRCM Principle: Cross-Domain Propagation
- Audio already responds to emotion state — this is VRCM-compatible
- **Gap:** Audio is one-directional (emotion → audio). VRCM says the sound Vector makes should also feed back into its own emotional state (hearing itself speak affects mood)
- **Gap:** TTS is generic. No personality in voice. VRCM would say the voice should carry emotional state (speed, pitch, energy variation)

### Chimera Target — Layer 2 + Layer 3
- **L2:** Emotional state continuously modulates voice parameters (not just sound effect selection)
- **L3:** Generates speech content through LLM with personality and context
- **Self-monitoring:** Vector's own audio output feeds back as low-weight input to emotion system
- **Prosody:** If possible within TTS constraints, vary speech rhythm with emotional state

### Status: 🔄 PARTIAL

---

## 9. CLOUD / WIREPOD INTERFACE

### TRM Reality
- **Location:** Ch17 (p296-308), Ch15 (SDK API, p148-272)
- **Original:** Anki cloud — gRPC, JWT auth, JDocs sync, STT/intent/TTS pipelines
- **Current:** WirePod replacement — local gRPC server, STT, intent, LLM integration, plugin system
- **SDK API:** Full HTTPS-based API with 100+ endpoints covering all robot functions
- **Key services:** vic-cloud (preferences, audio), vic-gateway (local API), vic-engine (behavior)

### VRCM Principle: Interface Axis (Human ↔ LLM architectural convergence)
- WirePod is the existing bridge between Vector and external intelligence
- **This is where L2 and L3 connect to Vector's existing system**

### Chimera Target — All Layers
- **L1:** Runs within vic-engine (emotion/behavior extensions via JSON config + potential code modifications)
- **L2:** Runs as a service alongside WirePod — receives sensor data, outputs behavior commands via SDK API
- **L3:** Runs as a background process — accesses LLM (Ollama local or cloud), reads/writes persistent memory, communicates with L2
- **Protocol:** L2 ↔ L3 via local API. L2 ↔ L1 via SDK gRPC. L1 ↔ Hardware via existing vic-engine internals

### Status: 🔄 PARTIAL

---

## 10. SERVICES ARCHITECTURE

### TRM Reality
- **Location:** Ch6 (p61-72)
- **Services:** vic-engine, vic-robot, vic-anim, vic-cloud, vic-gateway, vic-switchboard, vic-dasmgr
- **Communication:** Inter-process via Unix sockets, CLAD/JSON message serialization
- **Threading:** Event-driven communication threads with message queues per service
- **vic-engine:** Vision + behavior + emotion engine (the brain)
- **vic-robot:** Motor control + sensor filtering + power management
- **vic-anim:** Animation playback (multi-track: body, face, sound, LEDs)
- **vic-gateway:** Local SDK/API access via gRPC/HTTPS

### VRCM Principle: The Twofold Self (Self-M / Self-C)
- vic-engine is Self-M — the experiential component that processes the world
- L3 (Constructor) will be Self-C — the meta-process that shapes what vic-engine attends to
- **The connection between them (solid light beam in VRCM terms) is the API/socket interface**

### Chimera Target — Integration Architecture
- **Do not modify vic-robot** — motor control and safety must remain untouched
- **Extend vic-engine** — emotion model and behavior tree via JSON configuration where possible
- **Add chimera-cortex service** — new process that handles L2 perception fusion and L3 communication
- **Add chimera-constructor service** — new background process for L3 memory and personality
- **Communicate via existing patterns** — Unix sockets or local HTTP, same as other vic- services

### Status: ✅ MAPPED

---

## Summary Matrix

| Subsystem | TRM Chapter | VRCM Principle | Chimera Layer | Status |
|-----------|------------|----------------|---------------|--------|
| Emotion Model | Ch29 | Resonance, Gradients, Sparse>Null | L1 | ✅ |
| Behavior Engine | Ch28, Ch30 | Constraint Satisfaction, Hetarchical | L1+L2 | ✅ |
| Animation Engine | Ch22, Ch24, Ch27 | Resonance (harmonic transitions) | L1 output | ✅ |
| Sensory Input | Ch9, Ch10, Ch18, Ch19 | Cross-Domain, Attention | L2 | ✅ |
| Face Recognition | Ch19, SDK Ch56 | Trust Calculus, Proximity Weight | L3+L1 | ✅ |
| Navigation | Ch20 | Manifold Navigation | L2+L3 | 🔄 |
| Power/Sleep | Ch8 | Sleep Compilation Protocol | L3 | ✅ |
| Audio Output | Ch25 | Cross-Domain Propagation | L2+L3 | 🔄 |
| Cloud/WirePod | Ch15, Ch17 | Interface Axis | All | 🔄 |
| Services Arch | Ch6 | Twofold Self | Integration | ✅ |
