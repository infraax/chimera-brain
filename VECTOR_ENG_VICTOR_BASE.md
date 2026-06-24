# VECTOR-ENG ON THE VICTOR BASE
## Concrete integration map: building Chimera on the open-source Vector source
## Created: 2026-06-23 · Dexter × Claude Opus 4.8
## Companion to: Vector-eng.md (the framework) · supersedes the RE/decompilation plan

---

## 0. The base is real source, not a black box

`kercre123/victor` (a.k.a. the open-sourced Anki/DDL Vector codebase) is the **full engine source** —
~1.4 GB, ~21,700 files, real C++/Go/CLAD, not stripped binaries. This **retires the reverse-engineering
plan** (`CHIMERA_REVERSE_ENGINEERING.md`) and the "external-only / WirePod" stance
(`Reesearch-Rapport.md`). We now:

- **Use `victor` as the base of truth** — read it to understand exactly how Vector already works.
- **Build Chimera on top by *slight* modification** of that source — surgical hooks, not rewrites.
- **Keep a Pi as a separate brain/LLM resource**, but reached through **our own custom cloud server**
  (replacing `vic-cloud`/WirePod entirely), not WirePod.

> Principle carried over from the original interfaces spec: **extend, don't replace.** Anki's emotion model,
> behavior arbitration, vision, and animation are good. We add layers and redirect a few control points.

---

## 1. How the real source maps onto the Chimera layers

| Chimera layer | What it is | **Real victor source** |
|---|---|---|
| **L1 Brainstem** (emotion/reflex) | the 5-D mood model + decay | `engine/moodSystem/` — `moodManager.cpp/.h`, `emotion.cpp`, `emotionAffector.cpp`, `moodDecayEvaluator.cpp`, `emotionEvent.cpp`, `emotionEventMapper.cpp`, `staticMoodData.cpp`, `emotionScorer.cpp`, `moodScorer.cpp` |
| **L1/L2 behavior** | arbitration, the behavior tree | `engine/aiComponent/behaviorComponent/` — `behaviorSystemManager.cpp`, `behaviorStack.cpp`, `behaviorContainer.cpp`, `behaviorFactory.cpp`, `iBehavior.cpp`; conditions in `engine/aiComponent/beiConditions/` |
| **L2 Cortex** (perception/attention) | vision, faces, mic, attention | `engine/vision/`, `okaoVision/`, `engine/faceWorld.cpp`, `engine/smartFaceId.cpp`, `engine/petWorld.cpp`, `animProcess/src/cozmoAnim/micData/`, `engine/aiComponent/behaviorComponent/attentionTransferComponent.cpp` |
| **L2 proactivity** | "is someone here / receptive to me?" | `engine/receptiveSocialPresenceEstimator/socialPresenceEstimator.cpp` ⭐ |
| **L3 Constructor** (mind) | memory/personality/language | currently `cloud/` intent + JDocs; **we replace with our Pi brain + ENGRAM** |
| **Hardware/HAL** | motors, mics, syscon | `robot/` — `robot/syscon/src/mics.cpp`, body/motor; `animProcess` (vic-anim) |

The single most valuable existing component for our redesign is
**`receptiveSocialPresenceEstimator`** — Anki already built a module that estimates whether a person is
socially present and attending to Vector. That is *exactly* the signal a proactive (non-wake-word) creature
needs, and exactly where the **attunement layer** (the Eigengram-flip) plugs in.

---

## 2. The surgery points — the "slight modifications"

Five precise edits turn stock Vector into the Chimera. Everything else stays.

### S1 — Excise the wake word (make it always-on)
**Where:** `animProcess/src/cozmoAnim/micData/` — `micDataProcessor.cpp`, `micTriggerConfig.cpp`,
`micDataSystem.cpp`; low-level `robot/syscon/src/mics.cpp`. Trigger condition:
`engine/aiComponent/beiConditions/conditions/conditionTriggerWordPending.cpp`; reaction:
`behaviors/reactions/behaviorReactToVoiceCommand.cpp`. Wake-word model: `snowboy/`.
**Change:** stop gating cognition on a detected trigger word. Keep the mic capture + direction
(`micImmediateDirection`), but route the *continuous* audio stream into the ENGRAM perception loop instead
of into "trigger-word pending → wake." Snowboy can be removed or demoted to just one ordinary salience cue
(e.g. hearing its name raises attention) rather than the entry gate to thought.

### S2 — Redirect "cloud/intent" to our Pi brain
**Where:** `engine/aiComponent/behaviorComponent/behaviorComponentCloudServer.cpp` is the engine-side
bridge to `vic-cloud` (STT/intent). `cloud/` builds the cloud process.
**Change:** replace the vic-cloud/WirePod target with **our own custom cloud server on the Pi** (the L3
brain + LLM + ENGRAM store). Same socket/gRPC contract where possible (minimal engine change), but the
other end is ours. The engine streams situation summaries up and receives `SILENT/SPEAK/EMOTE` + guidance
down — async, never blocking (the L2↔L3 latency contract from `CHIMERA_INTERFACES.md`).

### S3 — Add the ENGRAM hook in the perception/mood path
**Where:** the mic/vision data path (`micData/`, `engine/vision/`, `faceWorld.cpp`) and the emotion tick in
`moodManager.cpp`.
**Change:** at each perception frame, assemble the `situation_t` vector (vision + audio + touch + IMU +
current emotion) and emit an **ENGRAM situational fingerprint** (C/NEON, on-device hot path). Write it to the
hot index and retrieve k-nearest in µs → feed B1 reflex. Full archive lives on the Pi. (See Vector-eng.md §3.)

### S4 — Make `moodManager` chimera-aware (resonance + coupling + ENGRAM)
**Where:** `engine/moodSystem/moodManager.cpp`, `emotionAffector.cpp`, `moodDecayEvaluator.cpp`.
**Change:** the original code is data-driven (decay graphs in JSON). Slight edits:
(a) optional **cross-dimension coupling** after affector application; (b) **resonance/damped-oscillation**
decay option alongside the existing curves; (c) accept emotion events derived from **ENGRAM-retrieved
situations** ("last time this happened it went badly → caution"). New dimensions (Curiosity/Attachment/
Fatigue) can extend `staticMoodData`. This is the L1 spec made concrete on real code.

### S5 — Drive proactivity from the social-presence estimator
**Where:** `engine/receptiveSocialPresenceEstimator/socialPresenceEstimator.cpp`,
`attentionTransferComponent.cpp`, behavior arbitration in `behaviorSystemManager.cpp`.
**Change:** let internal drive states + social-presence + ENGRAM situational recall **initiate** behavior
(Vector decides "someone's here and engaged, and last time we played they liked it → approach"), not just
react to triggers. This is where the **attunement layer** reads human affect (face/prosody/touch/timing) and
chooses presence — the Eigengram-flip, gated by the ethics rubric.

---

## 3. Revised topology (victor on-device + custom Pi brain)

```
┌───────────────── ON VECTOR — modified `victor` firmware ─────────────────┐
│  robot/ (HAL, mics, motors)  ──►  animProcess (vic-anim, micData)         │
│        │                              │                                   │
│        │   [S1] continuous mic stream (NO wake-word gate)                 │
│        ▼                              ▼                                   │
│  engine/ (vic-engine)                                                     │
│    ├─ vision/ + okaoVision + faceWorld  ── perceive                       │
│    ├─ [S3] ENGRAM encoder + on-device hot HNSW (µs)  ── situational sense │
│    ├─ moodSystem/moodManager [S4]  ── L1 reflex emotion (resonance/coupling)
│    ├─ receptiveSocialPresenceEstimator [S5]  ── proactive initiation      │
│    └─ behaviorComponent (arbitration)  ── act; MandatoryPhysicalReactions kept
│        │                                                                  │
│        │  [S2] behaviorComponentCloudServer ─► OUR custom cloud (not vic-cloud/WirePod)
└────────┼──────────────────────────────────────────────────────────────────┘
         │ gRPC/socket (async, non-blocking)
┌────────▼───────────────── ON THE PI — our custom brain/LLM ──────────────┐
│  custom cloud server (replaces vic-cloud)                                 │
│   ├─ full ENGRAM archive (lifelong situations)                            │
│   ├─ Deep-Understanding B2/B3 (reason · learn · sleep-consolidate)        │
│   ├─ dual LLM (3B talker / 8B mind): SILENT|SPEAK|EMOTE                    │
│   ├─ vectorax RAG (Vector's own source/TRM) for self-knowledge            │
│   └─ Negentropy world-claim scoring + trust/semantic-entropy gate         │
└──────────────────────────────────────────────────────────────────────────┘
```

Graceful degradation still holds: if the Pi is unreachable, on-device L1 (modified moodSystem) + ENGRAM hot
cache keep Vector a proactive creature; the Pi deepens understanding, language, and learning.

---

## 4. Build / understand order

1. **Read victor deeply** — `engine/moodSystem`, `behaviorComponent`, `micData`, `socialPresenceEstimator`,
   `behaviorComponentCloudServer`. Confirm build (`CMakeLists.txt`, `project/`, Vagrant/Docker toolchain).
2. **Stand up our custom cloud server** on the Pi speaking the `behaviorComponentCloudServer` contract — first
   just echoing, then wired to LLM + ENGRAM. (Replaces vic-cloud; no WirePod.)
3. **S1 wake-word excision** in `micData` → continuous stream; verify safety priority intact.
4. **S3 ENGRAM hook** → situational fingerprints + µs hot retrieval.
5. **S4 moodManager** resonance/coupling/ENGRAM-events.
6. **S5 proactivity** off `socialPresenceEstimator` + drives + ENGRAM recall.
7. **Attunement + ethics gate**, then **B3 sleep-compilation** learning loop.

---

## 5. Open questions now answerable against real code

- **Build toolchain:** victor uses CMake + Buck + a Vagrant/Docker cross-compile to ARM (`docker/`,
  `Vagrantfile`, `project/`, `tools/`). Confirm we can produce a flashable OTA from a modified tree.
- **Engine↔cloud contract:** read `behaviorComponentCloudServer.cpp` to define exactly what our Pi server
  must implement (the cleanest, smallest seam for L3).
- **micData internals:** how `micDataProcessor` hands off trigger vs raw stream — defines the S1 edit surface.
- **socialPresenceEstimator signals:** what it already computes (gaze? motion? audio?) — defines how much of
  the attunement layer is *extend* vs *new*.
- **On-device ENGRAM budget:** hot-index size within the APQ8009's free RAM (~50–100 MB).

---

*Base understood. The chimera is five surgical edits on real, readable source — plus our own Pi brain in
place of the cloud. Next: pick the first seam (recommend S2 custom-cloud server or S1 wake-word excision) and
go deep into that file set.*
