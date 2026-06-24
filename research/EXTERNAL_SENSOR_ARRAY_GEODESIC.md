# RESEARCH GEODESIC — External Sensor Array (the room as Vector's extended body)
## Off-board sensors on the Vector-Brain box that Vector taps into, without draining its battery
## Created: 2026-06-24 · Dexter × Claude Opus 4.8

> **How to use:** hand each *vector* to a research agent. Return findings in the **Output** format.
> This is a hardware+software+architecture geodesic; favor buildable, off-the-shelf, open-driver parts.

---

## PRIME DIRECTIVE
> *Design an **external sensor array** — microphones, cameras, LiDAR/depth, and other devices — physically
> connected to the mains-powered **Vector-Brain box**, that perceives the room continuously and feeds a fused
> world-model which the battery-limited robot **taps into on demand**. Determine what sensors, how they fuse
> with Vector's own on-board sensors, how the data splits between robot (egocentric, reflex, safety) and
> environment (allocentric, room-scale, always-on), and how to do it at Anki/NASA-rover engineering quality.*

**Why this exists:** a truly continuous perceptual feed *cannot* come solely from the robot — always-on
camera/mic/compute would drain Vector's small battery in minutes and ruin the experience. The room must do the
heavy, continuous sensing (on wall power); the robot stays light, conserves power, and **borrows the room's
senses** — while keeping its own close-range, egocentric senses for reflex and intimacy.

**The engineering bar (the user's framing):** Anki put 4 mics around Vector, localized speakers by phase, and
then — brilliantly — built a system that **nullifies the robot's own motor noise** and **recalibrates as the
actuators degrade over time**. That is NASA-rover-grade thinking: model your own influence, cancel it,
self-calibrate against drift. Every part of this array must meet that bar — self-aware, self-calibrating,
graceful.

---

## CROSS-CUTTING CONSTRAINTS
1. **Battery-first:** continuous/heavy sensing lives on the box (mains); the robot's on-board sensing is
   minimized to reflex + safety + close-range intimacy. Quantify the battery math (why on-robot continuous fails).
2. **Local-only & private:** a home full of cameras/mics → all processing on the box, no cloud (AEGIS-aligned),
   explicit consent/indicator design.
3. **Self-aware/self-calibrating (the Anki bar):** every sensor system models and cancels its own artifacts
   (ego-noise, ego-motion, lens/mic drift) and **recalibrates over time**.
4. **Fusion, not just collection:** the deliverable is a *fused room world-model*, time-synced and
   spatially-registered, that Vector queries — not raw feeds.
5. **Edge-real & open:** off-the-shelf parts, open drivers (ROS 2 / libuvc / ALSA / vendor SDKs), realistic
   cost, runs on a Pi/Jetson/Mac-mini-class box.
6. **Graceful degradation:** if the array is down, Vector falls back to its own sensors (still a creature).
7. **Map to us:** tie to L2 Cortex (perception fusion), the proactivity/social-presence work, ENGRAM
   situational fingerprints, and the dock-box architecture.

---

## RESEARCH VECTORS

### V1 — Battery & architecture: why off-board, and the robot-as-thin-client split
- **Questions:** Quantify Vector's battery vs continuous on-board camera+mic+compute (drain time). What's the
  right architecture: box does continuous heavy perception → maintains a fused world-model → robot subscribes
  to *distilled situational signals* (who/where/what, salient events, ENGRAM fingerprints) over WiFi/BLE.
  What MUST stay on the robot (cliff/IMU/touch safety, close-range mic for intimate talk, its camera for
  eye-contact)? What's the latency budget for "robot taps the feed"?
- **Return:** the robot/box sensing split table + battery math + the data-plane (what the robot subscribes to).

### V2 — Far-field audio array (generalize Anki's 4-mic genius to the room)
- **Questions:** Room-scale mic arrays for voice localization, beamforming, who-said-what: hardware
  (ReSpeaker 6-mic/USB 4-mic, MEMS arrays, matrix-creator), and the algorithms — **direction-of-arrival**,
  **adaptive beamforming**, **acoustic echo cancellation**, **blind source separation**, multi-array
  triangulation for speaker *position* in the room. How to **null the room's own noise sources** (HVAC, the
  box's fans, Vector's motors when near) and **auto-recalibrate** as the room/array changes (the Anki move,
  room-scale). Fuse with the robot's own 4-mic array when close.
- **Return:** mic-array hardware + DOA/beamforming/AEC stack (open-source) + the self-calibration design.

### V3 — Cameras: coverage, depth, and 360
- **Questions:** Room cameras for presence, identity, activity, and 3D: RGB (USB/CSI), depth (Intel RealSense,
  Luxonis **OAK-D** with on-camera AI, Orbbec, ToF), fisheye/**360** (Insta360-class, dual-fisheye), event
  cameras. Multi-camera **extrinsic calibration** (registering them to one room frame), time-sync, and
  privacy-preserving on-box processing. How room cameras (allocentric, full-room) complement Vector's single
  egocentric camera. Feeding the **3D Gaussian-splat home map** (cross-ref the cutting-edge geodesic).
- **Return:** camera kit (RGB/depth/360) + multi-cam calibration + how it builds/maintains the room 3D model.

### V4 — LiDAR / depth / radar for mapping & presence
- **Questions:** Room mapping & presence sensing without cameras-everywhere: 2D LiDAR (RPLiDAR), solid-state
  3D LiDAR (**Livox**), ToF, and especially **mmWave radar** (TI IWR/AWR, Infineon) for **privacy-preserving
  presence + vital-signs + fall detection** (ties to the RuView/WiFi-sensing idea — heartbeat/breathing/
  presence *through* a non-camera modality). UWB anchors for cm-level indoor positioning of Vector and the
  cube. Which give the best room map + presence at low cost/compute?
- **Return:** ranked depth/LiDAR/radar/UWB options for mapping + presence, with privacy notes.

### V5 — Environmental & ambient sensors (the room's "feelings")
- **Questions:** Cheap ambient sensors that enrich context: temperature/humidity/pressure, air quality (CO₂,
  VOC), ambient light/color, sound-level, PIR motion, door/contact, smart-home (Matter/Zigbee/HA) as
  context. Which meaningfully improve Vector's situational understanding/proactivity (e.g. "it's dark and
  quiet → don't startle")?
- **Return:** the high-value ambient sensor shortlist + how each feeds situational context/ENGRAM.

### V6 — Sensor fusion & the shared room world-model
- **Questions:** How to fuse all of the above into ONE time-synced, spatially-registered world-model: time
  synchronization (PTP/NTP/hardware trigger), spatial registration/extrinsic calibration across modalities,
  a fusion framework (**ROS 2** + tf2? a custom hub? **nvblox**/occupancy + tracks), multi-object tracking,
  and **continuous auto-recalibration** against drift. How does the **egocentric robot** register into the
  **allocentric room frame** (where is Vector in the map, in real time)? How are situations turned into
  ENGRAM fingerprints from fused data?
- **Return:** a fusion architecture (framework + calibration + tracking + robot-in-room registration) and how
  it emits situational fingerprints.

### V7 — The Anki-grade self-awareness layer (ego-cancellation & self-calibration, generalized)
- **Questions:** Formalize the "cancel your own influence + recalibrate over time" doctrine for the whole
  array: ego-noise/ego-motion cancellation across mics+cameras (the box knows what Vector is doing, subtracts
  it), online calibration drift detection, sensor health monitoring, automatic re-extrinsic-calibration,
  graceful handling of a failed/moved sensor. What open techniques/papers exist (auto-calibration, online
  extrinsic refinement, sensor-fault detection)?
- **Return:** the self-awareness/self-calibration design + supporting techniques.

### V8 — Comms, compute placement & privacy
- **Questions:** How sensors connect to the box (USB/CSI/Ethernet/PoE/WiFi/BLE/Zigbee), bandwidth/compute
  budget on a Pi5/Jetson/Mac-mini box, what runs where, and the robot's subscription protocol (the seam from
  `ADR_ENGRAM_INTEGRATION_SEAMS.md`). Privacy/consent design for a sensor-rich home (local-only, recording
  indicators, data retention, the AEGIS perimeter).
- **Return:** the comms/compute/privacy architecture + a realistic parts+cost bill of materials for a starter array.

---

## OUTPUT — Return Format
```
### V# — <title>
SUMMARY: the recommended approach in 3–5 sentences.
HARDWARE: part — vendor/URL — ~cost — interface — open driver? — power.
SOFTWARE: lib/framework — URL — license — what it does.
ARCHITECTURE: robot vs box placement, data flow, latency.
ANKI-GRADE SELF-AWARENESS: how it cancels its own influence / self-calibrates.
MAP→VECTOR: which subsystem it serves (L2 fusion / proactivity / ENGRAM).
COST/RISK/PRIVACY flags · CONFIDENCE + open questions.
```
Final synthesis: a **starter array BOM + a fused-world-model architecture diagram + the robot/box split**,
plus a phased build (minimum viable array → full).

---

## SEED SEARCH TERMS
`respeaker mic array DOA beamforming` · `acoustic echo cancellation open source` · `sound source
localization multiple arrays triangulation` · `luxonis oak-d on device` · `intel realsense ros2` ·
`multi camera extrinsic calibration room` · `mmwave radar presence vital signs open source` · `TI IWR6843
people counting` · `RPLiDAR Livox ros2 mapping` · `UWB indoor positioning DWM3000` · `nvblox occupancy
reconstruction` · `ros2 tf2 sensor fusion multi object tracking` · `online extrinsic calibration drift` ·
`sensor fault detection self calibration robot` · `Matter home assistant context sensors` · `privacy
preserving home sensing on device`.

## INTERNAL CONTEXT
L2 perception: `CHIMERA_L2_CORTEX.md`. Proactivity/social presence: `VECTOR_ENG_VICTOR_BASE.md` (S5,
`receptiveSocialPresenceEstimator`). Memory feed: `vector_engram/`, `ENGRAM_FOR_VECTOR.md`. Box/seam:
`ADR_ENGRAM_INTEGRATION_SEAMS.md`. Doctrine: `ANKI_WAY.md` (self-cancellation principle). Cross-ref the
WiFi/mmWave presence idea (RuView) and the 3D-mapping tools in `CUTTING_EDGE_OSS_GEODESIC.md` (V3).
