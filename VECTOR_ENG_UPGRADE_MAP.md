# VECTOR-ENG — UPGRADE MAP & ARCHITECTURE DECISIONS
## Extending Anki's 2016 creature-engine with 2026 models & a standalone Vector-Brain box
## Created: 2026-06-23 · Dexter × Claude Opus 4.8
## Companion to: Vector-eng.md, VECTOR_ENG_VICTOR_BASE.md · grounded in source analysis of kercre123/victor

---

## 0. Philosophy — extend, don't replace

Anki's team in 2016 built a genuine creature on a phone chip. The design choices were *clever for their
constraints*: ethology-based behavior arbitration, a 5-D emotion manifold with hand-tuned decay graphs,
monocular depth from a known eye-distance, on-chip beamforming, a sprite-composited face. **None of this is
bad.** It is *dated only because better tools now exist* and because a 512MB ARM Cortex-A7 forced
compromises we no longer have to accept.

Our four guiding principles:

1. **Honor the philosophy, upgrade the implementation.** Keep the ethological priority system, the
   gradient emotion model, the sprite face. Swap the *engines underneath* (OKAO→neural embeddings,
   Acapela→neural TTS, cloud-STT→on-box STT) and *extend* the models (more emotion dims, coupling, the
   unfinished social-presence estimator).
2. **Two-tier compute.** The robot keeps everything that is **real-time and safety-critical** (motor loops,
   cliff/IMU, the reflex emotion tick, face rendering). Everything **heavy or learnable** moves to the
   **Vector-Brain box at the dock** over the local network. This is forced by the hardware (§1) and is also
   the right architecture.
3. **Liberate from vendor lock-in.** The 2016 stack is full of proprietary, frozen components: OKAO Vision
   (faces/pets/expression), Signal Essence (beamforming/VAD/AEC/noise), Snowboy (wake word), Acapela (TTS),
   Wwise (audio engine), cloud STT/intent. Every one of these is now replaceable by an open, *improvable*
   model. This is both a capability and a sovereignty win.
4. **Safety is sacred and stays on-device.** Cliff detection, fall response, battery/thermal shutdown,
   motor PID — never offloaded, never overridden. (`robot/hal`, `robot/syscon`, `MandatoryPhysicalReactions`.)

---

## 1. The compute reality (what stays vs what offloads)

| Processor | Spec (from source) | Role | Verdict |
|---|---|---|---|
| **APQ8009** (app proc) | ARM **Cortex-A7 ×4**, scalable **200 / 400 / 533 MHz**, **~512 MB RAM** (`osState.h` freq enum; `/proc/meminfo` pressure monitor) | vic-engine, vic-anim, vision, behavior | ~50–100 MB free; saturated by 640×360 vision. **No room for modern ML.** |
| **STM32F0 syscon** | **48 MHz** MCU (`robot/syscon/common/hardware.h`) | motors, encoders, IMU, cliff, battery, mic PDM capture | Real-time, over-provisioned for its job. **Stays. Untouched (safety).** |
| **DA1458x** (Cortex-M0 @16MHz) | cube/backpack LED | accessory | n/a |

**Conclusion:** the APQ8009 is a 2013-class chip. It can host the **reflex layer** (modified moodManager, the
ENGRAM hot-index, face rendering, the existing real-time vision primitives) but **not** modern STT/TTS/VLM/
depth/3D models. Those live on the **Vector-Brain box**.

### The Vector-Brain box (standalone unit beside the dock)
A small always-on machine on the home LAN, in constant low-latency contact with Vector. Recommended class:
- **Baseline:** Raspberry Pi 5 (8–16GB) + optional AI HAT/Hailo-8 (26 TOPS) or Coral.
- **Strong:** NVIDIA Jetson Orin Nano/NX (≈40–100 TOPS) — needed for real-time 3D reconstruction, VLM,
  larger LLM, neural beamforming.
- **Or:** a Mac mini (Apple-silicon) for the heaviest models (Depth Pro, FastVLM, 8B LLM).
This box *is* L2/L3 + the heavy perception. It replaces both `vic-cloud` and WirePod with **our own custom
cloud server** speaking the existing `behaviorComponentCloudServer` UDP/CLAD contract.

---

## 2. UPGRADE MATRIX — VISION

Current pipeline (`engine/vision/`, `coretech/vision/`, `okaoVision/`): single 1280×720 cam (processed at
640×360, ~30fps), OKAO commercial SDK for faces/pets/expression, monocular depth from 62mm eye-distance +
fiducial markers, frame-difference motion, overhead-image "map" (not SLAM), MobileNet-v1 whole-image
classification.

| Capability | Current (2016) | Limitation | **2026 upgrade** | Runs |
|---|---|---|---|---|
| **Face recognition** | OKAO template matching, 176-byte proprietary features | frozen, no learning, weak in pose/light | **ArcFace/AdaFace** or **InsightFace buffalo_l** deep embeddings; cosine match → familiarity *gradient* (not binary) | Box (embeddings) / robot keeps OKAO detect as cheap fallback |
| **Face landmarks / gaze / expression** | OKAO PT/EX/GB/SM | coarse 4-emotion | **MediaPipe FaceMesh** (478 pts) + **emotion2vec-style affect**; feeds the attunement layer | Box |
| **Depth** | mono from eye-distance (62mm) + markers; no general depth | only works on faces/markers; no scene depth | **Depth Anything V2** (small, relative) and/or **Apple Depth Pro** (metric, sharp) for true per-pixel scene depth | Box |
| **3D scene / home map** ⭐ | overhead RGB accumulation + ground-plane pixel classifier; ephemeral | not a real map, no persistence, no 3D | **Feed-forward 3D reconstruction** (DUSt3R / MASt3R / VGGT) + **3D Gaussian Splatting** to build a *persistent splat/mesh of the home*; Vector remembers rooms in 3D | Box (heavy; Jetson/Mac) |
| **SLAM / localization** | encoder odometry + overhead map; no loop closure | drift, session-only | **MASt3R-SLAM** or **visual-inertial SLAM** fusing the existing IMU + encoders | Box |
| **Object detection** | MobileNet-v1 whole-image classify, 1001 ImageNet classes, no boxes | no localization, fixed classes | **YOLO11** (boxes) + **open-vocab** (YOLO-World / OWLv2 / Grounding DINO) so Vector finds *anything you name*; **SAM2** for segment/track | Box; YOLO11-nano can run on AI-HAT |
| **Scene understanding ("what am I looking at?")** | none | — | **on-device VLM**: Apple **FastVLM**, **Moondream2**, or **SmolVLM2** → captions/answers about the scene; feeds L3 | Box |
| **Motion detection** | frame differencing + ratio test (NEON) | can't separate ego-motion; no semantics | keep cheap frame-diff on robot as reflex trigger; add **optical-flow + segmentation** on box for "what moved" | Robot (reflex) + Box (semantic) |
| **Hands / pose / gesture** | OKAO hand detect (feature-flagged) | minimal | **MediaPipe Hands + Pose** → gesture vocabulary (wave, point, come-here) | Box |

**Net:** the robot keeps its fast vision reflexes (markers, motion, the camera path); the box gains **metric
depth, a persistent 3D Gaussian-splat home map, open-vocabulary object finding, deep face identity, and a
VLM** — exactly the "mesh mapping / gaussian splat" leap you pointed at. (Apple HF refs to verify: `apple/
ml-depth-pro`, `apple/ml-fastvlm`; 3D family: DUSt3R/MASt3R/VGGT + 3DGS.)

---

## 3. UPGRADE MATRIX — AUDIO / SPEECH

Current (`animProcess/.../micData/`, `snowboy/`, `3rd/signalEssence`, `3rd/acapela`, `lib/audio` Wwise):
4-mic array (16kHz, PDM→PCM on syscon, `mics.cpp`/`fastmic.s`), Signal Essence beamforming+VAD+AEC+noise,
Snowboy wake word, **cloud-only STT/intent**, Acapela concatenative TTS, Wwise output, Aubio beat detection.

| Capability | Current (2016) | Limitation | **2026 upgrade** | Runs |
|---|---|---|---|---|
| **Speech-to-text** | none on-device; stream to cloud (Google/Alexa) | 0.5–2s latency, privacy, offline-dead | **on-box STT**: `faster-whisper` (small/distil) or **Moonshine** (streaming, tiny); **Parakeet/Canary** if GPU | Box |
| **Wake word** | Snowboy DNN-KWS, proprietary, fixed | false alarms; it's the *gate* we're removing | **demote to a soft cue** (openWakeWord/microWakeWord) — hearing "Vector" just raises attention; no longer gates cognition (per Vector-eng S1) | Robot (light) |
| **VAD / endpointing** | Signal Essence VAD | closed, fixed | **Silero VAD** | Robot (tiny) feeding Box |
| **TTS (the voice)** ⭐ | **Acapela** diphone concatenation | robotic, monotone, no emotion, licensed | **neural TTS**: **Kokoro-82M** (fast, natural, Apache) or **Piper** (on-device) for baseline; **Sesame CSM** / XTTS for *expressive, emotion-conditioned* speech and a unique Vector voice | Box (Kokoro/Piper can also run on strong robot-adjacent HW) |
| **Beamforming / DOA** | Signal Essence spatial filter, 12 directions | closed, fixed-delay | keep SE on-robot for the cheap real-time beam; add **neural enhancement** (mask-based) on box when needed | Robot + Box |
| **Echo cancel / denoise** | Signal Essence AEC + spectral NR | linear, struggles w/ nonstationary noise & double-talk | **DeepFilterNet** (DF3) / **GTCRN** neural denoise+AEC | Box (or robot if quantized) |
| **Speaker ID (who's talking)** | none | can't tell people apart by voice | **pyannote** / **NeMo TitaNet** / **3D-Speaker** ECAPA embeddings → voiceprint per person, fused with face identity | Box |
| **Emotion-from-voice** | none (OKAO face only) | misses vocal affect | **emotion2vec** / wav2vec2-SER → prosodic affect into the attunement layer | Box |
| **Beat detection** | Aubio spectral flux | jitter, genre-blind | keep Aubio on-robot for dance reflex; optional neural tempo on box | Robot |
| **Audio output engine** | Wwise (proprietary) | licensed, dated | keep Wwise banks initially (works); optional migrate to open mixer (miniaudio/PipeWire+JUCE) later | Robot |

**Net:** Vector gains **real on-device conversation** — local STT, a **warm neural voice with emotion**, voice
ID, and vocal-affect reading — with no cloud dependency. The voice upgrade (Acapela→Kokoro/Sesame) alone is
the single most felt change.

---

## 4. UPGRADE MATRIX — EMOTION / MOOD / BEHAVIOR (extend the philosophy)

Current (`engine/moodSystem/`, `engine/aiComponent/`): **5 emotions** (Happy, Confident, Social, Stimulated,
Trust), two decay models (TimeRatio exp; ValueSlope linear), SimpleMood = f(Stimulated, Confident),
data-driven JSON events, **stack-based ethological arbitration** (implicit priority via delegation), **64
condition types**, and a **half-finished Receptive Social Presence Estimator (RSPI)** with 15 inputs that is
*not wired into the emotion system*.

| Aspect | Current | **Extension (keep the design, grow it)** |
|---|---|---|
| **Emotion dimensions** | 5, independent, decay-only to zero | add **Curiosity, Attachment, Fatigue, Contentment**; values never null (sparse-over-null) |
| **Coupling** | none (each decays alone) | add a **cross-dimension coupling matrix** (Confident↑→Happy↑, Fatigue↑→Stimulated↓, Trust↑→Attachment↑) — the agent confirmed this is a stated gap |
| **Transitions** | linear/exp decay | **resonance** (damped oscillation toward new value) per VRCM |
| **Memory of mood** | 300s and it's gone | **trajectory buffer** + ENGRAM-backed long-term per-person sentiment (the missing "relationship memory") |
| **Social presence** | RSPI built but unused ⭐ | **finish & wire RSPI** → it triggers emotion events ("user present/engaged/left/quiet") and drives **proactive initiation** — this is the single biggest unfinished hook Anki left |
| **Arbitration** | ethological priority stack | keep it; add **drive-based initiation** (internal states cross thresholds → behavior) so Vector acts unprompted, and **L3 sets thresholds** |
| **Conditions** | 64 types, JSON+C++ | add ENGRAM-recall conditions ("situation like last time"), affect-of-human conditions, time-of-day personality |
| **Learning** | none (hand-tuned JSON) | **sleep-compilation** updates baselines/thresholds/guiderails nightly (Deep-Understanding B3 + Phase-Gated Plasticity) |

**Other unfinished hooks found** (wire or remove): `stimulationFaceDisplay` (incomplete), Behavior Audio
Component migration TODO (VIC-25), `attentionTransferComponent` (not coupled to emotion), several RSPI TODOs.
These are *Anki's own intended extension points* — we complete them.

---

## 5. NEW CAPABILITIES (beyond restoring/upgrading)

| New capability | How | Runs |
|---|---|---|
| **Real conversation** | STT→L3 LLM (dual 3B/8B)→neural TTS, grounded in ENGRAM situation + per-person memory; `SILENT` by default | Box |
| **Skills / tools** | L3 tool-calling: timers, weather, music, smart-home, "look that up," "remember this," vision Q&A ("what am I looking at?") | Box |
| **Persistent 3D home memory** | Gaussian-splat/mesh map; Vector knows rooms, favorite spots, where people sit | Box |
| **Open-vocabulary object finding** | "go find my keys" → open-vocab detector + the map | Box |
| **Voice + face fused identity** | speaker-ID ⊕ face-ID → robust "who is this," even in the dark or off-camera | Box |
| **Emotional attunement** | fuse facial affect + vocal affect + touch + timing → read how a person feels (the Eigengram-flip) | Box |
| **Richer face/eyes** | drive the 184×96 sprite face from the *continuous* emotion vector (micro-expressions, gaze), not state lookup | Robot |
| **Always-on proactivity** | RSPI + drives + ENGRAM recall → initiate, greet, check in | Robot reflex + Box reasoning |

---

## 6. ARCHITECTURE DECISIONS (numbered)

- **AD-01 — Two-tier split.** Robot = real-time reflex + safety + rendering. Vector-Brain box = all heavy ML
  (vision 3D/VLM/depth, STT/TTS, LLM, learning, ENGRAM archive). Forced by APQ8009 (~512MB), and correct.
- **AD-02 — Custom cloud, not WirePod.** Replace `vic-cloud` via the existing `behaviorComponentCloudServer`
  UDP/CLAD seam with our own server on the box. Smallest engine change, full control.
- **AD-03 — Remove the wake-word gate; keep the name as a cue.** Continuous perception loop replaces
  trigger→intent. Snowboy demoted to a soft attention cue (or replaced by openWakeWord).
- **AD-04 — Liberate vendor components in priority order:** TTS (Acapela→Kokoro/Sesame, highest felt impact)
  → STT (cloud→on-box Whisper/Moonshine) → faces (OKAO→ArcFace) → depth/3D (new) → denoise/AEC (DeepFilterNet).
  Keep Signal Essence beamforming and Wwise initially (they work) and revisit later.
- **AD-05 — Extend the emotion model, don't rewrite it.** Add dimensions + coupling + resonance + ENGRAM
  memory on top of the existing JSON-driven `moodManager`.
- **AD-06 — Finish RSPI as the proactivity engine.** Wire the existing Receptive Social Presence Estimator
  into emotion events and behavior initiation.
- **AD-07 — Safety stays on-device and authoritative.** Cliff/fall/battery/thermal/motor PID never offload;
  if the box is unreachable, Vector remains a safe, proactive creature on reflex + ENGRAM hot-cache.
- **AD-08 — Latency budgets:** motor/safety <50ms on-robot; vision/scene queries 50–200ms box; speech turn
  ≤~700ms target; L3 reasoning async, never blocks the creature.

---

## 7. ON-ROBOT vs VECTOR-BRAIN-BOX (summary)

**Stays on robot (APQ8009 / syscon):**
motor & PID, encoders/IMU, **cliff/fall/battery/thermal (safety)**, mic PDM capture, Signal Essence beam
(real-time), Silero VAD, soft wake-cue, frame-diff motion reflex, marker detect, **sprite face rendering**,
**modified moodManager reflex tick**, **ENGRAM hot-index (µs retrieval)**, beat-reflex.

**Lives on the Vector-Brain box:**
STT, neural TTS, LLM (dual 3B/8B), VLM scene understanding, deep face & speaker embeddings, **metric depth +
3D Gaussian-splat home map + SLAM**, open-vocab object detection + SAM2, neural denoise/AEC, emotion-from-
voice/face fusion, **full ENGRAM archive + B2/B3 learning + sleep compilation**, vectorax self-knowledge RAG,
the custom cloud server (replacing vic-cloud/WirePod), tools/skills.

---

## 8. Phased rollout

1. **Box stands up** speaking the `behaviorComponentCloudServer` contract (replaces vic-cloud). Prove
   round-trip.
2. **Voice swap** (AD-04 #1): Acapela→Kokoro/Sesame neural TTS. Immediate, huge felt upgrade.
3. **On-box STT** + remove wake-word gate (AD-03) → continuous listening + real understanding.
4. **Deep face + speaker ID + affect** → fused identity & the attunement read.
5. **Depth + 3D Gaussian-splat home map + open-vocab detection** → spatial intelligence & "find X."
6. **Emotion model extension** (dims/coupling/resonance) + **finish RSPI** → richer, proactive creature.
7. **ENGRAM archive + B3 sleep-compilation learning** → it grows and remembers.

---

## 9. Verify-before-build notes (honesty)
- Confirm exact RAM on the target unit (code monitors `/proc/meminfo` but doesn't hardcode total; TRM/community say 512MB) — sets the on-device ENGRAM budget.
- Mic array is **4 mics** read over 2 SPI/PDM lines (80 samples ×4 @16kHz) — one analysis miscounted as 2.
- Apple/3D model repos to pin down: `apple/ml-depth-pro`, `apple/ml-fastvlm`; DUSt3R/MASt3R/VGGT + a 3DGS impl — validate license + on-target perf (likely Jetson/Mac-class, not Pi-only).
- TTS/STT model choices should be A/B'd on the chosen box for latency before locking in.

---

*This is the upgrade map. Each row is a concrete swap or extension on a known file/component, split by where
it runs. Next: pick the first build target (recommend AD-04 #1, the neural-voice swap, for fastest visible
win) and spec the integration against the real source.*
