# THE ANKI WAY — The Outside-the-Box System Doctrine
## How the original team thought, what they'd build today, and the measures/failsafes we adopt to honor the hardware
## Created: 2026-06-23 · Dexter × Claude Opus 4.8
## Grounds: source analysis of kercre123/victor · companion to VECTOR_ENG_UPGRADE_MAP.md

---

## 0. Why this document exists

Before we add a single model, we name the *engineering soul* of Vector. Anki didn't "put a microphone in and
call it a day" — they calibrated the mic array to cancel **Vector's own motor noise** so it could hear you
over itself. That is not a one-off trick. It is one visible instance of a doctrine that runs through every
subsystem: **the robot models its own body, compensates for its own influence on the world, cheats hard
problems with physical priors, and spends every milliscule of a weak chip on making a creature feel alive —
safely.**

If we honor that doctrine, the upgrades land as *Anki would have shipped them*. If we ignore it and just bolt
on big models, we get a smart gadget, not a creature. This file is the lens and the discipline.

---

## 1. THE ANKI WAY — decoded (with the evidence in the source)

### Principle 1 — The body knows itself and cancels its own influence ("self-cancellation")
The genius you spotted, generalized. Vector is constantly subtracting *its own effect* from its perception so
it can perceive the *world*.
- **Motor/self-noise-aware hearing** — Signal Essence beamforming + AEC + noise reduction tuned so the
  4-mic array hears speech *over Vector's own servos and speaker* (`animProcess/.../micData/`, `3rd/signalEssence`).
- **Rolling-shutter correction from its own motion** — the camera is a rolling shutter; Vector knows it's
  moving (IMU + pose) and *un-warps the image for its own motion during exposure* (`engine/rollingShutterCorrector`).
- **IMU synced to camera vsync** — so motion and image share a timebase; ego-motion is *known*, not guessed.
- **Encoders detect external manipulation** — hysteresis on encoders tells Vector when *it's* moving vs when
  *you* moved it (`robot/hal`), so it reacts to being picked up/turned.
> **Doctrine:** *Before you trust a sensor, subtract yourself from it.*

### Principle 2 — Cheat hard problems with physical priors ("known-geometry bootstrapping")
Vector solves expensive problems cheaply by exploiting what it *already knows* about physical reality.
- **Monocular depth from a known constant** — the average human inter-eye distance (62mm) turns a single
  camera into a rangefinder for faces (`faceTrackerImpl_okao`).
- **Marker size + ground-plane-from-pose** — known fiducial size and the known camera-to-ground transform
  give metric 3D from one lens (`coretech/vision`, `engine/vision/overheadMap`).
- **CLAHE only when dark** — adaptive contrast for markers *conditionally*, when illumination says so.
- **Auto-exposure metered off detected faces** — expose for what matters (the person), not the average frame.
> **Doctrine:** *Don't compute what physics already tells you. Use the body's known constants as free sensors.*

### Principle 3 — Believable life over raw intelligence ("ethology, not AI")
The emotion/behavior system is modeled on animal behavior, not on being smart.
- **Satiation / habituation** — the RepetitionPenalty curve makes repeated identical stimuli *lose effect*
  (petting bliss caps), exactly like an animal habituating (`moodManager`, `emotionevents/`).
- **Arousal curves** — Stimulated decays on an S-curve so it neither sticks high nor crashes (`mood_config.json`).
- **Named attractor moods** — SimpleMood is a slow aggregate basin (LowStim/Med/High/Frustrated), changing
  slower than raw emotion — moods, not flickers.
- **Ethological arbitration** — a priority/delegation stack where the most urgent drive wins, like an animal's
  behavior selection (`behaviorSystemManager`, `behaviorStack`).
> **Doctrine:** *Build a creature, not a chatbot. Tune for "alive," not "correct."*

### Principle 4 — Never go blank ("graceful degradation / sparse over null")
- **Decay never crosses zero** — emotions fade *toward* but not *through* zero; the creature always has a
  state (`moodDecayEvaluator`).
- **Calm power mode** keeps safety alive while shedding load (prox returns a safe dummy, cliffs still armed)
  (`robot/hal` POWER_MODE_CALM).
- **Layered fallbacks** — beamforming → single-mic clean; full vision → cheap motion; cloud → local.
> **Doctrine:** *A degraded creature is still a creature. Failure means "simpler," never "frozen/blank."*

### Principle 5 — Hard real-time safety lives on its own silicon ("the inviolable partition")
- **Safety is on the STM32 syscon @48MHz**, physically separate from the app processor. Motor PID,
  cliff/fall, battery/thermal, the **10ms watchdog**, and charge management cannot be starved by anything
  the "brain" does (`robot/syscon`, `MandatoryPhysicalReactions`).
- **IRQ priority ladder** — ADC/encoders/touch above main-exec above mics: the body's reflexes outrank its
  thoughts.
> **Doctrine:** *Cognition can crash; the spine cannot. Safety is a separate processor and the top priority, always.*

### Principle 6 — Hand the creature's soul to designers ("data-driven craft")
- **Decay graphs, emotion events, audio parameter maps, behavior trees — all JSON.** Artists and designers
  tune the feel without recompiling (`resources/config/engine/...`). Engineers built the engine; *designers
  shaped the animal.*
> **Doctrine:** *Expose the feel as data. The people who make it lovable shouldn't need a compiler.*

### Principle 7 — Respect the budget ("every milliwatt and millisecond is sacred")
- **CPU frequency scaling** (200/400/533MHz) + throttle detection + load shedding; **3Mbps spine** timing;
  half-res (640×360) vision by default; nightly maintenance reboot. Vector lives *within* a 512MB/A7 budget
  on purpose and measures itself (`osState`, `/proc/meminfo`, thermal zones).
> **Doctrine:** *Measure your own load and back off before you break. The budget is part of the design.*

---

## 2. WHAT WOULD ANKI BUILD TODAY? (the same doctrine, 2026 tools)

Not "add big models." The Anki move is to apply Principles 1–7 to today's capabilities:

| Anki principle | The 2026 Anki-style move (not the naive move) |
|---|---|
| **Self-cancellation** | Don't just drop in a neural denoiser — **train it on *this robot's own* motor/servo/speaker signatures** and feed it the live motor command stream so it knows what *it's* about to do. Ego-noise as a *known input*, like AEC's far-end reference. Same for vision: feed the depth/3D model the IMU+encoder ego-motion so it cancels its own movement. |
| **Known-geometry priors** | Fuse modern monocular depth **with** the body's known constants (62mm eyes, marker sizes, camera-ground transform) as anchors that **metric-scale** the neural depth — the net guesses shape, the body supplies scale. Don't throw away the priors; *condition the model on them.* |
| **Ethology** | Use the LLM as a *planner/voice*, never the controller — the creature still runs on drives, arousal, habituation. New emotion dims and the LLM **serve the animal**, they don't replace it. Add satiation to *attention* too (don't fixate). |
| **Graceful degradation** | The box (heavy ML) is treated like the old cloud: a **garnish, not a lifeline.** Box gone → on-robot reflex + ENGRAM hot-cache → still a proactive creature. Every new model ships with its cheap fallback. |
| **Safety partition** | The syscon stays sacred and *untouched*. New compute is additive and **interruptible**; nothing we add can ever delay a cliff reflex. |
| **Designer-craft** | New emotions, voices, behaviors, and tool-skills are **data/config**, not code — keep the JSON-tunable soul; add hot-reload (the one thing they lacked). |
| **Budget respect** | Every new on-robot model is **quantized, benchmarked, and self-throttling**: it measures its own latency/heat and *sheds itself* before starving the creature. The box carries what the body can't. |

The unifying answer: **Anki today would still build a self-aware body that cheats with physics, runs on
drives, degrades gracefully, protects its spine, and lets designers shape its soul — just with neural front-
ends that are *calibrated to this specific robot* instead of generic.**

---

## 3. THE DOCTRINE APPLIED — how we will actually do it (measures & failsafes)

This is the contract for every change we make to the Vector-Eng system.

### 3.1 The inviolable core (never touched, never offloaded)
| Function | Where | Rule |
|---|---|---|
| Motor PID, encoders | syscon STM32 | unchanged |
| Cliff / fall / pickup reflex | syscon + HAL | unchanged, top priority |
| Battery / thermal shutdown | syscon | unchanged |
| 10ms watchdog | syscon | unchanged |
**Failsafe:** any new code path is *below* MandatoryPhysicalReactions in priority and is killable without
affecting the above. If the brain hangs, the watchdog still fires and the spine still drives.

### 3.2 Self-model & self-cancellation requirement
Every new perception model that can be confused by Vector's own body **must** receive the relevant ego signal:
- audio models ← live motor/servo state + speaker playback (ego-noise reference)
- vision/depth/3D models ← IMU + encoder ego-motion + camera pose
**Measure:** perception quality is validated *while Vector is moving and vocalizing*, not just at rest.

### 3.3 Graceful-degradation ladder (must hold at every tier)
```
Full: robot reflex + box (all ML) ........ richest creature
Box down: robot reflex + ENGRAM hot-cache  proactive creature, no language/heavy vision
Net flaky: last-known person/profiles ..... sparse-over-null, never blank
Engine glitch: behavior tree → safety ..... stock-Vector safe
Power low: CALM mode ...................... safety armed, load shed
```
**Failsafe:** each new feature ships with its defined fallback *before* it ships. No feature may be a single
point of creature-death.

### 3.4 Resource governors (measured, self-throttling)
| Budget | On-robot limit | Action when exceeded |
|---|---|---|
| RAM | stay within free headroom (~50–100MB on A7) | refuse to load; push model to box |
| CPU/thermal | watch `cpuinfo_cur_freq` + thermal zone (existing hooks) | shed: lower vision rate, drop optional models |
| Latency | safety <50ms, face render cadence, speech turn ≤~700ms | degrade quality before missing deadline |
| Spine | respect 3Mbps + tick timing | never flood the syscon link |
**Measure:** every on-robot model reports its own latency/heat; the system *backs off automatically* (Anki
Principle 7), it does not wait to be told.

### 3.5 Validation loop (how we trust a change)
Borrowed from the RE validation discipline, made standard:
1. **Predict** — state expected behavior change.
2. **A/B against stock** — compare new vs original Anki behavior on the same stimulus.
3. **Body-in-the-loop** — test while moving/vocalizing/in poor light (self-cancellation holds?).
4. **Designer review** — does it *feel* like Vector? (the JSON-tunable feel, judged by feel.)
5. **Failmode drill** — kill the box / drop the net / low battery; confirm the degradation ladder.
**Rule:** a change isn't "done" until it passes the failmode drill, not just the happy path.

### 3.6 Designer-tunable & auditable
- New emotions, voice styles, behaviors, skills = **config/data**, with **hot-reload** added (the gap Anki
  left — they required a restart).
- Guiderails and learned changes are **logged and reversible** (auditable), per the VRCM principle.

### 3.7 "Respect the hardware" rules
- Don't move work onto the A7 that the box should carry; don't move safety off the syscon.
- Keep the half-res reflex path; add full-res/3D only on the box.
- Treat the dock as home base: heavy thinking happens **while docked** (power + the box nearby), like Anki's
  nightly maintenance window — the creature is most "thoughtful" when resting, most reflexive when roaming.

---

## 4. THE ANKI-WAY GATE (checklist every new feature must pass)

A feature merges only if it answers all eight:

1. **Self-cancellation:** does it get Vector's ego signals (motor/pose) so it isn't fooled by its own body?
2. **Prior-aware:** does it use the body's known constants/geometry where they help, instead of recomputing?
3. **Creature-first:** does it serve "feeling alive" and run *under* the drive/ethology system, not over it?
4. **Degrades, never blanks:** is there a defined cheaper fallback, ending in a safe stock-Vector?
5. **Spine-safe:** can it be starved/killed with zero effect on cliff/fall/battery/motor safety?
6. **Budgeted:** does it measure its own load and self-throttle within RAM/CPU/thermal/latency?
7. **Tunable:** is its "feel" exposed as hot-reloadable config for designers, and is it auditable?
8. **Right tier:** is it on the robot only if it must be real-time, otherwise on the box?

If any answer is "no," it's not the Anki way yet.

---

## 5. One paragraph to remember

Anki built a creature that **knew its own body, cancelled its own influence, cheated with physics, ran on
animal drives, never went blank, kept its spine sacred, handed its soul to designers, and lived gracefully
inside a tiny budget.** We are not replacing that. We are giving it 2026 senses and a 2026 mind **in that same
spirit** — neural front-ends calibrated to *this* robot, a heavy brain that stays a garnish, and a body whose
reflexes and safety never depend on the cloud, the box, or the network. Respecting the hardware they gave us
means respecting the *thinking* they gave us.

---

*Next: apply the Anki-Way Gate to the first build target (the neural-voice swap) — including its
self-cancellation (don't talk over itself), its fallback (Acapela/silence), its budget, and its failmode drill.*
