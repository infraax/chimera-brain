# UNIFIED — External Sensor Array (the room as Vector's extended body)
## Mains-powered "room brain" → Vector subscribes as a thin client
### Source geodesic: `research/EXTERNAL_SENSOR_ARRAY_GEODESIC.md`

> **Fusion of the two independent research runs**, merged with nothing dropped:
> - **[C] = Claude** — file `04_external_sensor_array__room_brain.md` ("Mains-Powered 'Room Brain'
>   Architecture"). TL;DR / Key-Findings / Caveats wrapper; geodesic SUMMARY/HARDWARE/SOFTWARE format
>   per vector; sources cited **inline** (named outlets + repos), no numbered list.
> - **[P] = Perplexity** — file `03_external_sensor_array__geodesic.md` ("The Room as Vector's
>   Extended Body"). Per-vector CONFIDENCE ratings, JSON examples, ASCII architecture, **89 numbered
>   references** (preserved at bottom as `[P^n]`).
>
> Tags: **[Both]** · **[C-only]** / **[P-only]** · **⚖️ DIVERGENCE** (decision-relevant disagreements).

---

## 0. HEADLINE: agreement is near-total; four things differ

**The two reports converge almost completely on architecture** — strong signal. The thesis,
the robot/box split, the audio pick, the camera pick, the radar-for-privacy stance, the fusion
framework, the ego-cancellation principle, and the privacy model are *identical*. They differ only
in specific part numbers, one license fact, and the depth of certain citation sets.

### What both independently conclude (high confidence)
- **Continuous on-robot sensing is physically impossible.** Vector's pack (~1.2–2 Wh) gives
  ~25–45 min; always-on camera+mic+inference (~3–5 W) drains it in **<15–24 min**. → All heavy,
  continuous perception **must** live on a mains-powered box; the robot becomes a **thin client**
  subscribing to a distilled situational signal over WiFi/MQTT.
- **Two orthogonal frames:** *egocentric* (robot: gated camera, 4-mic, cliff/IMU/touch, ToF laser —
  reflex/safety/intimacy only) vs *allocentric* (box: continuous room mics, cameras, depth/LiDAR/radar,
  ambient — the fused world-model).
- **Audio:** ReSpeaker **XVF3800 USB 4-mic array** + **ODAS** (SRP-PHAT SSL/DOA) + multi-array
  triangulation = generalize Anki's 4-mic beamforming to room scale.
- **Cameras:** Luxonis **OAK-D** (on-camera AI) + Intel **RealSense** for depth; **nvblox** TSDF/ESDF;
  ArUco/AprilTag multi-camera extrinsic calibration to one `room` frame.
- **Privacy radar:** **mmWave** for presence/vital-signs without cameras (both flag vitals as
  fragile/experimental). **Livox Mid-360** 3D LiDAR + **DWM3000 UWB** for cm robot/cube position.
- **Ambient:** **ESP32 + ESPHome** (CO₂/PIR/light/temp) → Home Assistant; CO₂ catches *stationary*
  occupants that PIR misses.
- **Fusion:** **ROS 2 + tf2** (+ PTP time-sync), person tracking, ENGRAM situational fingerprints
  published over **MQTT** to the robot.
- **The "Anki move" generalized:** box knows the robot's commanded motor/speech/screen state →
  subtracts its acoustic/visual signature room-wide (ego-noise cancellation) + online extrinsic
  recalibration + sensor-health/fault detection.
- **Privacy by architecture:** local-only, no cloud egress, hardware mute + recording LED,
  derived-metadata-only, short retention, AEGIS perimeter, **radar-first (no cameras) in bedrooms**.
- **Graceful degradation:** box offline → robot falls back to on-board sensing (the shipping Anki
  Vector behavior) via MQTT last-will.
- **Build order:** audio + ambient first (cheapest, highest situational value per €/$).

### ⚖️ The four real differences

| Topic | **[C] Claude** | **[P] Perplexity** | Our read |
|---|---|---|---|
| **ODAS license** | states **MIT** | states **GPL-2.0** (flags it; `odas_ros` bridge is MIT) | **Must verify the introlab/odas repo license** — if GPL-2.0 it's a real constraint for a closed build; Perplexity's flag is the safer assumption. |
| **Box compute pick** | **Jetson Orin Nano *Super*** (67 TOPS, $249) | **Jetson Orin Nano 8 GB** (40 TOPS, ~$200) + Mac Mini M4 option | Same family; Claude names the newer **Super** (67 TOPS) — prefer it. Both agree Pi 5 for Phase 0, Jetson for multi-cam+nvblox. |
| **mmWave entry hardware** | **TI IWR6843** ISK/AOPEVM (~$300 EVM + DCA1000) — people-counting/vitals | **Infineon BGT60TR13C** (~$30 eval) for presence/breathing **+** TI IWR6843AOP (~$80) | Complementary: **BGT60TR13C is the cheap presence-radar entry [P]**; IWR6843 is the higher-end people-counter [C]. Start cheap (BGT60), add IWR6843 for multi-person. |
| **mmWave vital-signs tone** | More **skeptical** — cites Pi-ViMo / Harmonic-MUSIC (arXiv:2505.08366): reliable only ~0.6 m, single still subject | More **optimistic** on BGT60 breathing (gives the phase math Δφ=4πΔd/λ) but still rates MEDIUM | **Both agree: validate empirically before relying on it.** Ship presence/fall first; treat vitals as experimental. |

### Coverage difference (one found, the other didn't)
- **[P-only]:** explicit battery spec (**320 mAh / 1.18 Wh** factory, charge circuit hard-wired);
  **SpeechBrain** (diarization) + local **Whisper** (STT); **Orbbec Gemini 336** camera;
  **GS-LTS / FreeSplat++** incremental splat; **Infineon BGT60TR13C** + breathing phase math;
  **PTP (IEEE 1588)** deep-dive (<10 µs) + USB fixed-offset; **FastCal** (arXiv:1902.10585) +
  **Levinson-Thrun** online calibration; **NASA Robonaut SHM** + variogram fault taxonomy;
  measured **WiFi ~20 ms avg / 38 ms p95**; the **JSON fingerprint** schema; 3-tier $ BOM
  (~$2,035 full); multi-room federation; privacy threat-model open question.
- **[C-only]:** **pyroomacoustics** (DOA/BSS: AuxIVA/ILRMA/FastMNMF), **SpeexDSP** (MDF AEC),
  **WebRTC AEC3**, **respeaker_ros**, **MATRIX Creator**; **OAK-D-Lite ($149)** + **RealSense D435i**
  + **event cameras (DVS)**; **ROSplat / SplaTAM / ORB-SLAM-3DGS**; **spencer_people_tracking**
  (IMM/group) + **robot_localization** (EKF/UKF); **OCAMO/LTO** (IEEE T-IV 98%+), **Cramariuc**
  (arXiv:2005.11711), **Peters** (J.Field Robotics 2024), **DSAE** autoencoder, ACM fault-diagnosis
  survey; **Hailo-8L AI HAT** (13 TOPS for Pi); **WirePod SDK** (wirepod-vector-python-sdk) as the
  robot subscription seam; € BOM; **BME680 BSEC** accuracy-state self-reporting.

---

## V1 — Battery & architecture (robot as thin client)

**[Both]** Same conclusion, slightly different numbers.
- **[P]** Factory **320 mAh / 3.7 V = 1.18 Wh**; charge circuit hard-wired to that capacity (won't
  fully charge larger cells via dock); aftermarket 600 mAh → ~40–45 min; continuous ~3–5 W → **<15 min**.
  Battery-math table per scenario. `[P^1–P^5]`
- **[C]** "~2 Wh usable; ~25 min active (Anki support page), ~45 min play (Tom's Guide)"; sources vary
  300–600 mAh but the off-board conclusion holds regardless.
- **Hardware (Vector) [Both]:** Qualcomm Snapdragon quad-core 1.2 GHz, 4-mic beamforming array,
  120° HD camera, IR ToF laser (~30–1200 mm / ~1 m, 25° FOV), 6-axis IMU, 4× cliff, capacitive touch.
- **Must stay on robot [Both]:** cliff/drop (reflex <1 ms / <50 ms), IMU, front ToF, gated 4-mic
  (wake/intimate), gated camera (eye-contact/face-lock), capacitive touch.
- **Data plane [P, explicit topics]:** box publishes MQTT `/room/world_model` (10 Hz),
  `/room/audio/speaker_doa` (20 Hz), `/room/engram/fingerprint` (1 Hz), `/room/presence/radar` (5 Hz),
  `/room/environment` (0.2 Hz), `/room/alerts` (event). Robot subscribes per behavioral mode
  (sleeping → `/alerts` only). ⚖️ Latency: **[P] measured ~20 ms / 38 ms p95**; **[C] budgets
  100–300 ms** for context (safety stays local <50 ms). `[P^6][P^12][P^13]`
- **[C-only] robot seam:** wirepod-vector-python-sdk (Apache-2.0) — WirePod replaces the dead Anki cloud.
- **MAP→VECTOR [Both]:** L2 Cortex perception fusion + proactivity + ENGRAM scene fingerprinting.

---

## V2 — Far-field audio array

**[Both]** ReSpeaker **XVF3800 USB 4-mic** (XMOS, on-board AEC/AGC/DoA/VAD/dereverb/beamforming,
360° to 5 m); two arrays at opposite corners → multi-array DOA triangulation to 3D speaker position.
- ⚖️ **ODAS license:** **[C] MIT** vs **[P] GPL-2.0** (odas_ros bridge MIT). Verify before shipping.
- **[P] stack:** ODAS (SRP-PHAT), odas_ros, **WebRTC AEC**, **SpeechBrain** (diarization/ID), local
  **Whisper** (STT); SRP-PHAT math + room-frame bearing intersection. `[P^14–P^22]`
- **[C] stack adds:** **pyroomacoustics** (SRP-PHAT/MUSIC DOA; BSS: AuxIVA/ILRMA/SparseAuxIVA/
  FastMNMF/FastMNMF2; NLMS/RLS), **SpeexDSP** MDF/AUMDF AEC (revised BSD), **WebRTC AEC3** (BSD-3),
  **respeaker_ros**; alt hardware **ReSpeaker 6-mic HAT**, **MATRIX Creator** (8-mic+FPGA, may be
  discontinued). ODAS DGSS + directivity model = explicit body-occlusion nulling.
- **Anki-grade [Both]:** box measures its own fan-noise spectral profile at startup → fixed spectral
  subtraction; when Vector is near, its **pre-measured per-actuator motor-noise signature is injected
  as an AEC reference** (the Anki move at room scale); online inter-array phase recalibration; dead/
  clipped mic → DOA outlier → alert.
- **Confidence [Both]:** HIGH on hardware/stack; MEDIUM on multi-array triangulation in reverberant
  rooms. [C] notes Seeed reduced ReSpeaker software maintenance (more DSP falls to the builder).

---

## V3 — Cameras: coverage, depth, 360°

**[Both]** OAK-D (on-camera AI, offloads box) + RealSense for depth; allocentric room cameras
complement Vector's single egocentric camera; feed nvblox TSDF/ESDF or a Gaussian-splat map.
- **[P] hardware:** OAK-D / **OAK-D Pro W** (wide 150°, $200), **RealSense D455** (<2% depth error @4 m,
  global shutter, IMU, $240), **Orbbec Gemini 336**, **Insta360** 360°. `depthai-ros`, `librealsense2`.
  `[P^23–P^31]`
- **[C] hardware:** **OAK-D-Lite ($149, 1.4 TOPS, 300k-pt stereo, 12.3 MP)**, OAK-D S2 (4 TOPS),
  **RealSense D435i** (~0.55 W idle/2.2 W active), fisheye/360, **event cameras (DVS)**. DepthAI (MIT),
  librealsense (Apache-2.0).
- **Calibration [Both]:** scattered ArUco/AprilTag → global solve → tf static transforms to `room_frame`.
  [P] `extrinsic_calibrator_core`, `ros2_calib` (IKA RWTH); [C] AprilTag array / Kalibr / MC-Calib.
- **3D map [Both]:** **nvblox** (GPU TSDF+ESDF, multi-camera on Orin). Splat: **[P]** GS-LTS,
  FreeSplat++ (incremental); **[C]** ROSplat, SplaTAM, ORB-SLAM-3DGS. `[P^32–P^40]`
- **Anki-grade [Both]:** box knows Vector's pose → masks robot-occluded frames before tracking;
  reprojection-error monitor → auto re-calibration; Luxonis on-the-fly recalibration (vibration/temp).
- **Privacy/Confidence [Both]:** on-box only, no raw frames stored, shutter/LED indicator; HIGH for
  OAK-D + RealSense; 360° fisheye UVC support partial — verify.

---

## V4 — LiDAR / depth / radar (mapping & presence)

**[Both] ranked:** mmWave radar (privacy presence/vitals) · 2D/3D LiDAR (geometry) · UWB (cm position).
- **mmWave ⚖️:** **[C] TI IWR6843** ISK/AOPEVM (~$300 EVM + DCA1000, 120°az/30°el, ~10 m; Radar
  Toolbox 3D People Counting / Vital Signs). **[P] Infineon BGT60TR13C** (~$30 eval, 60 GHz FMCW,
  breathing ~2–5 mm chest motion via Δφ=4πΔd/λ at λ≈5 mm, to 5 m; open Infineon RDK) **+** TI
  IWR6843AOP (~$80). → cheap presence entry [P] vs higher-end counter [C].
- **LiDAR [Both]:** **Livox Mid-360** (solid-state 360°×59°, $500–700, livox_ros2_driver); **RPLiDAR**
  (A1/A3, ~$99–180, 2D budget map). [C] pair Livox w/ GLIM/FAST-LIO; [P] livox_mapping.
- **UWB [Both]:** ESP32 + **DWM3000** ×4 anchors, **5–10 cm** via TWR/DS-TWR + EKF, ~100 Hz; anchors
  Vector + Cube into the room frame (arXiv:2403.10194). `[P^41–P^58]`
- **Anki-grade [Both]:** radar/LiDAR see the robot as a moving cluster → box subtracts its known track;
  nvblox occupancy decay (→0.5) forgets stale obstacles; empty-room radar baseline recalibrated when
  cameras confirm empty.
- **⚖️ Vital-signs confidence:** **[C] MEDIUM-LOW** (Pi-ViMo/Harmonic-MUSIC: ~0.6 m, single still
  subject); **[P] MEDIUM** (BGT60 eval-grade SDK needs C-wrapper work). **Both: validate empirically.**

---

## V5 — Environmental & ambient sensors (the room's "feelings")

**[Both]** Cheap I²C/Matter sensors via **ESP32 + ESPHome** → Home Assistant → box MQTT context topics.
CO₂ + PIR combination catches both active and stationary occupants.
- **Sensors [Both]:** **CO₂** (Sensirion **SCD40/41** NDIR [Both]; [P] also MH-Z19C with 7-day ABC
  auto-calibration), **PIR** (AM312/HC-SR501), **ambient light** (BH1750/TSL2561/TCS34725),
  **temp/humidity** (SHT31/DHT22), **sound level** (MAX9814), **door/contact** reed, **VOC/air**
  (**BME680** [C, with BSEC IAQ + self-reported accuracy state] / SGP30 [P]), **pressure** (BMP280).
- **Rule examples [P]:** `CO2>800 ∧ PIR<5min → OCCUPANCY_CONFIRMED`; `lux<50 ∧ hour>20 → NIGHT_QUIET
  → don't startle`; `noise<35 dB → QUIET_ROOM`. [C]: "dark+quiet → don't startle"; "CO₂ high → air out."
- **Anki-grade [Both]:** NDIR ABC self-calibration ([P] MH-Z19C 7-day window; [C] BME680 BSEC accuracy
  states Stabilizing/Uncertain/Calibrating/Calibrated). `[P^59–P^63]`
- **Confidence [Both]:** VERY HIGH / HIGH — proven maker stack; lowest privacy risk; ~$30 BOM.
  [C] caveat: CO₂/VOC need burn-in.

---

## V6 — Sensor fusion & the shared room world-model

**[Both]** **ROS 2 (Humble/Jazzy) + tf2** spatial backbone; **nvblox** geometry; multi-object person
tracker; emit ENGRAM situational fingerprints.
- **Time-sync ⚖️ depth:** **[P]** detailed **PTP (IEEE 1588)** <10 µs HW timestamp, <100 µs ROS msg,
  USB fixed-offset correction; **[C]** NTP/PTP/hardware-trigger + `message_filters` approximate-time.
- **Tracker ⚖️:** **[P]** custom **Kalman + Hungarian** (2D floor projection + height, persistent UUID,
  occlusion prediction); **[C]** off-the-shelf **spencer_people_tracking** (IMM, track init, group
  tracking, CLEAR-MOT/OSPA) + **robot_localization** EKF/UKF.
- **Robot-in-room [Both]:** UWB RTLS (+ IMU heading) places `/vector_base` in `room_frame` at ~100 Hz.
- **[P] fingerprint schema (JSON, <500 B, 1–5 Hz):** `{occupancy, active_speaker{id,doa,speech},
  room_state, thermal, audio_scene, robot_location{x,y,z,in_dock}, salient_events, confidence}`.
- **Anki-grade [Both]:** cross-sensor consistency (camera-empty vs radar-present → lower confidence +
  alert); online extrinsic recalibration ([P] FastCal/Levinson-Thrun <1 s @0.25°/10 cm; [C] OCAMO/LTO
  98%+). `[P^36][P^37][P^64–P^76]`
- **MAP→VECTOR [Both]:** this IS L2 perception fusion — every downstream subsystem subscribes to it.

---

## V7 — The Anki-grade self-awareness layer

**[Both]** Generalize "model your own influence → subtract it" across the whole array:
(1) ego-noise cancellation, (2) ego-motion/occlusion compensation, (3) continuous extrinsic drift
detection, (4) sensor-health/fault monitoring. A box-side **"self-model" service** ingests robot
state + sensor health + calibration residuals.
- **Ego-noise [Both]:** robot motor-command stream → box's per-actuator spectral model → AEC reference
  (Anki's onboard beamformer, room-scale). [P] cites SBSS-AEC for nonlinear distortion (arXiv:2312.08610,
  2010.13060).
- **Online calibration ⚖️ citations:** **[P]** FastCal (info-theoretic segment selection + observability-
  aware update + time-decay; arXiv:1902.10585) + Levinson-Thrun (1 s detection, 0.10° mean drift).
  **[C]** OCAMO/LTO (IEEE T-IV), Cramariuc miscalibration detection (arXiv:2005.11711), Peters offline-
  SLAM self-calibration (J.Field Robotics 2024), DSAE autoencoder self-diagnosis.
- **Fault detection ⚖️:** **[P]** variogram taxonomy (outlier/spike/variance/offset/gain/drift) +
  **NASA Robonaut SHM** (model-based observers + fuzzy logic). **[C]** ACM Computing Surveys 2018
  fault-diagnosis survey + Springer Autonomous Robots 2017.
- **[P] self-calibration schedule:** startup (baselines) / daily-low-activity (full ArUco + radar empty
  baseline + CO₂ ABC) / continuous (FastCal + consistency + mic health) / event (sensor moved → recal).
  `[P^75–P^82]`
- **Confidence [Both]:** MEDIUM — components published, but integration into one always-on self-model
  is bespoke.

---

## V8 — Comms, compute placement & privacy

**[Both]** USB 3.0 (cameras/mics), Ethernet/PoE (Livox), WiFi/BLE (ESP32 + robot), Zigbee/Matter (HA);
heavy inference where the GPU/NPU is; robot subscribes over local MQTT/DDS.
- **Compute ⚖️:** **[P]** Jetson Orin Nano **8 GB (40 TOPS, ~$200)** / Mac Mini M4 ($600) / Pi 5 ($80,
  Phase 0) / Intel NUC. **[C]** Jetson Orin Nano **Super (67 TOPS, $249)** / Pi 5 (+Hailo-8L 13 TOPS HAT)
  / Mac mini. Both: **Jetson for multi-cam+nvblox+radar; Pi 5 for audio+presence MVP.** `[P^83–P^87]`
- **Connectivity table [P]:** OAK-D ~400 Mbps USB3 (use VL812 hub), RealSense ~400 Mbps, XVF3800
  ~2 Mbps UAC2, Livox ~50 Mbps Ethernet, BGT60 ~5 Mbps, DWM3000 ~100 kbps, ESPHome ~10 kbps, Vector
  subscribe ~50 kbps.
- **Privacy / AEGIS [Both]:** no cloud egress (firewall the box); **hardware recording LED hardwired to
  camera power** (can't be software-disabled); **physical mic mute switch**; raw audio/video retention
  **0 s** (derived metadata ring buffer ≤60 min); per-sensor consent at setup; per-zone disabling
  (radar-only bedrooms). [P] MQTT QoS 0 world_model / QoS 1 alerts; docked → unsubscribe to all but
  `/alerts`. `[P^88][P^89][P^12][P^13]`

---

## FINAL SYNTHESIS — merged BOM, architecture, phased build, split

### Bill of materials (both, side by side)

**[C] € MVP (~€410):** Pi 5 (8 GB)+cooler/PSU/NVMe €110 · ReSpeaker XVF3800 €75 · OAK-D-Lite €140 ·
ESP32+BME680+SCD40+PIR €60 · USB hub €25. **+ TI IWR6843 €90 → ~€500.** Full adds: RPLiDAR A1M8 €95,
Livox Mid-360 €650, Jetson Orin Nano Super €249, 4× DWM3000 €110, 360 camera €200.

**[P] $ 3-tier (~$2,035 full):**
- *Phase 0 (~$240):* Pi 5 $80 · 2× XVF3800 $100 · BGT60TR13C $30 · ESP32 ambient $10 · VL812 hub $20.
  → audio DOA + presence + ambient, **no cameras (max privacy)**.
- *Phase 1 (+~$895):* 2× OAK-D Pro W $400 · RealSense D455 $240 · Jetson Orin Nano 8 GB $250 · ArUco $5.
  → person tracking + 3D map + activity.
- *Phase 2 (+~$900):* Livox Mid-360 $600 · 4× DWM3000 $100 · TI IWR6843AOP $80 · ceiling XVF3800 $50 ·
  PoE switch $40 · USB3 PCIe $30.

### Robot / box sensing split (merged)
| Capability | Robot | Box | Why |
|---|---|---|---|
| Far-field room voice | ❌ | ✅ XVF3800 arrays | battery + coverage |
| Intimate near-field voice | ✅ 4-mic gated | ❌ | latency + intimacy |
| Room presence/tracking | ❌ | ✅ cameras + radar | battery + coverage |
| Close obstacle / cliff | ✅ ToF + 4× cliff | ❌ | reflex <50 ms |
| Room 3D map | ❌ | ✅ nvblox + LiDAR | compute + persistence |
| Own position in room | ❌ | ✅ UWB RTLS | range + continuous |
| IMU / stabilization | ✅ always-on | ❌ | proprioception |
| Person recognition | ✅ gated (eye-contact) | ✅ continuous (tracking) | both |
| Ambient environment | ❌ | ✅ ESPHome | no battery impact |
| ENGRAM fingerprint | ❌ consumer | ✅ producer | compute + continuous |

### Fused architecture (both drew the same picture)
```
BRAIN BOX (mains, 24/7): XVF3800×2 → AEC/ODAS DOA → triangulation
                         OAK-D/RealSense → on-cam AI + depth → nvblox TSDF/ESDF
                         mmWave → presence/vitals · Livox → 3D map · ESP32 → ambient
                         UWB → robot+cube cm-position
        → ROS 2 + tf2 (+PTP) single `room` frame  [extrinsic_calibrator | FastCal drift]
        → FUSION: person tracker (KF+Hungarian / spencer) | ENGRAM fingerprint gen
                  | sensor-health | ego-noise cancellation
        → WORLD-MODEL NODE → MQTT broker (Mosquitto)
                ↓ WiFi 802.11n (~20 ms; budget 100–300 ms for context)
VECTOR (thin client): subscribes world_model/fingerprints/alerts; contributes motor cmds →
        ego-noise model, camera → eye-contact, gated 4-mic → intimate voice, IMU/cliff → safety (local)
```

### Phased build (merged, both agree on order)
- **Phase 0 — architecture:** Pi 5 + ROS 2 + WirePod; prove robot subscribes to a box MQTT event and
  reacts; establish local-only network + mute/indicator policy. *(Spine order V1 → V2 → V6.)*
- **Phase 1 — MVP (audio + ambient):** XVF3800 + ODAS room DOA; ESP32 ambient; first ENGRAM fingerprints.
- **Phase 2 — perception:** OAK-D + mmWave + RPLiDAR; ArUco extrinsic calibration to one room frame.
- **Phase 3 — fusion:** tf2 + nvblox + person tracker; UWB robot registration; self-model
  (ego-cancel + drift + graceful degradation); upgrade to Jetson when multi-cam+nvblox+tracking run
  concurrently (**[C] threshold: fusion loop >300 ms or GPU-bound → upgrade**).
- **Phase 4 — full array:** Livox 3D map + Gaussian-splat home model; 360 camera; full UWB; mmWave
  vital-signs (flagged reliability).

### Recommendations (merged)
1. Build the spine **V1 → V2 → V6**; don't buy hardware before Phase 0 proves subscribe-and-react.
2. **Audio + ambient first** (cheapest, highest value/€); then OAK-D + mmWave.
3. **Choose compute by load, not spec sheet** — Pi 5 MVP → Jetson Orin Nano (Super) when GPU-bound.
4. **Treat mmWave vital-signs as experimental** — validate vs chest strap / pulse-ox at real range/clutter.
5. **Privacy is a first-class build target** — local-only, hardware mute + recording LED, derived-
   metadata-by-default, short retention, firewalled AEGIS perimeter, radar-not-cameras in bedrooms.

---

## COMBINED CAVEATS
- **Battery figures vary** (320/500/600 mAh) — off-board conclusion holds regardless.
- **Research-grade, validate empirically [Both]:** mmWave vital-signs through clutter, multi-array audio
  triangulation in reverberant rooms, continuous auto-recalibration.
- **License watch:** ⚖️ ODAS (MIT per [C] vs GPL-2.0 per [P] — verify); ESPHome BSEC component is
  proprietary (license-accept); nvblox/Isaac ROS need an NVIDIA GPU (substitute slam_toolbox+OctoMap
  on Pi/Mac).
- **Hardware in flux [C]:** Seeed reduced ReSpeaker software maintenance; MATRIX Creator may be
  discontinued — verify stock/support.
- **Pricing** ±15%, region/currency dependent (€ vs $); TI IWR6843 figure is the EVM price.
- **[P] open questions:** motor-noise online recalibration as actuators degrade; tight `room`↔`vector_base`
  TF loop for gaze-following; multi-room federation (N boxes, federated world-model); GS-LTS/FreeSplat++
  splat integration; formal privacy threat model before household deployment.

---

## APPENDIX A — Claude [C] inline sources (no numbered list in original)
Anki support page ("~25 min active"), Tom's Guide (~45 min play), TechRadar (Snapdragon quad 1.2 GHz),
Seeed (ReSpeaker XVF3800), Intel Community (RealSense D435i 440 mA), Luxonis DepthAI, IntelRealSense
librealsense, NVIDIA-ISAAC-ROS/isaac_ros_nvblox, introlab/odas, LCAV/pyroomacoustics, xiph/speexdsp,
webrtc-audio-processing, furushchev/respeaker_ros, Livox-SDK/livox_ros_driver2, Slamtec/rplidar_ros,
TI Radar Toolbox, aldras/multiple_object_tracking_lidar_ros2, arXiv:2403.10194 (UWB), Pi-ViMo,
Harmonic-MUSIC arXiv:2505.08366 (mmWave vitals), spencer-project/spencer_people_tracking,
robot_localization, OCAMO/LTO (IEEE T-IV 2023/24), Cramariuc arXiv:2005.11711, Peters J.Field Robotics
2024, ACM Computing Surveys 2018, Springer Autonomous Robots 2017, ESPHome/Home Assistant, Bosch BSEC,
shadygm/ROSplat, SplaTAM, kercre123/wirepod-vector-python-sdk.

## APPENDIX B — Perplexity [P] references (1–89, verbatim)
1. https://www.reddit.com/r/AnkiVector/comments/1fogcer/im_curious_to_those_of_you_who_did_not_yet/
2. https://www.youtube.com/watch?v=11SVDt4l0s8
3. https://techshop82.com/shop/vector-battery-503040/
4. https://randym32.github.io/Anki.Vector.Documentation/service/Battery%20replacement.html
5. https://www.reddit.com/r/AnkiVector/comments/191qtf3/vector_battery_upgrade/
6. https://ecer.pria.at/archive/ecer-2024/papers/Comparing_the_Viability_of_Different_Communication_Methods_for_Botball.pdf
7. https://manuals.plus/video/4d01f2f34df5219156c64ff46da19e718d9f61511f881ba05b0f3fbeb6505a96
8. https://www.kinvert.com/whats-inside-anki-vector-hardware/
9. https://shop.pishrobot.com/en/product/anki-vector-robot/
10. https://www.youtube.com/watch?v=jiDEoGm6Tl0
11. https://www.reddit.com/r/AnkiVector/comments/mbyec5/vectors_battery/
12. https://discourse.openrobotics.org/t/announcing-mqtt-client-a-c-nodelet-for-bi-directionally-bridging-messages-between-ros-and-mqtt/26878
13. https://jschrier.github.io/blog/2023/02/10/MQTT-and-ROS2-integration.html
14. https://github.com/introlab/odas
15. https://www.semanticscholar.org/paper/ODAS:-Open-embeddeD-Audition-System-Grondin-L%C3%A9tourneau/45b1b900197e12551ed72e967c7223a3562788be
16. https://mashable.com/article/anki-vector-smart-home-robot
17. https://www.directindustry.com/prod/seeed-studio/product-241202-2822900.html
18. https://wiki.seeedstudio.com/respeaker_xvf3800_introduction/
19. https://www.xmos.com/plug-play-voice-control-xvf3800
20. https://michaelfatemi.com/posts/2022/05/sound-camera
21. https://docs.pal-robotics.com/ari/sdk/23.12/hardware/microphone.html
22. https://wiki.seeedstudio.com/respeaker_xvf3800_ros2/
23. https://docs.luxonis.com/hardware/products/OAK-D
24. https://husarion.com/tutorials/ros-equipment/oak-series/
25. https://github.com/Serafadam/depthai_ros_driver
26. https://github.com/westonrobot/depthai_ros
27. https://arxiv.org/html/2501.07421v1
28. https://github.com/IntelRealSense/librealsense/issues/7806
29. https://www.youtube.com/watch?v=GdbWJpBEYfA
30. https://docs.ros.org/en/jazzy/p/librealsense2/
31. https://flore.unifi.it/retrieve/85225dff-c578-4812-9e9b-68a5ac592ef0/Comparative_Evaluation_of_Intel_RealSense_D415_D435i_D455_an.pdf
32. https://docs.ros.org/en/humble/p/extrinsic_calibrator_core/
33. https://github.com/ika-rwth-aachen/ros2_calib
34. https://docs.ros.org/en/ros2_packages/humble/api/extrinsic_calibrator_examples/__README.html
35. https://github.com/arplaboratory/arpl_nvblox
36. https://wiki.seeedstudio.com/deploy_nvblox_jetson_agx_orin/
37. https://nvidia-isaac-ros.github.io/concepts/scene_reconstruction/nvblox/
38. https://www.scribd.com/document/977811198/Nvblox-GPU-Accelerated-Incremental-Signed-Distance-Field-Mapping
39. https://huggingface.co/papers/2503.17733
40. https://arxiv.org/abs/2503.22986
41. https://arxiv.org/abs/2403.10194
42. https://github.com/Livox-SDK/livox_mapping
43. https://github.com/DhamuVkl/ESP32-DWM3000-UWB-Indoor-RTLS-Tracker
44. https://github.com/Livox-SDK/livox_ros2_driver/blob/master/README_CN.md
45. https://www.slideshare.net/slideshow/build-an-uwb-indoor-positioning-system-using-esp32-and-qorvo-dwm3000-0e7a/283887428
46. https://github.com/Livox-SDK/livox_ros2_driver
47. https://par.nsf.gov/servlets/purl/10343337
48. https://github.com/Infineon/mtb-example-sensors-radar-presence
49. https://github.com/Infineon/sensor-xensiv-bgt60trxx
50. https://www.infineon.cn/assets/row/public/documents/24/42/infineon-an141319-ceiling-mounted-occupancy-detection-using-xensiv-demo-bgt60tr13c-60-ghz-radar-applicationnotes-en.pdf
51. https://www.infineon.com/assets/row/public/documents/24/44/infineon-ug120209-installation-guide-for-presence-detection-solution-using-xensiv-bgt60tr13c-radar-som-board-usermanual-en.pdf
52. https://www.youtube.com/watch?v=tOfg7Wiq4zE
53. https://www.livoxtech.com/news/mid360_launch
54. https://www.accio.com/business/lidar-livox-mid-360-lds-z300-e
55. https://github.com/KylinC/mmVital-Signs
56. https://e2e.ti.com/support/sensors-group/sensors/f/sensors-forum/1347216/iwr6843aopevm-request-example-codes-for-development
57. https://e2e.ti.com/support/sensors-group/sensors/f/sensors-forum/1586483/iwr6843aopevm-source-code-request-for-iwr6843aopevm-vital-signs-application
58. https://arxiv.org/html/2405.12659v1
59. https://community.home-assistant.io/t/occupancy-sensor-vs-motion-sensor/358689
60. https://community.home-assistant.io/t/esphome-temp-humidity-lux-co2-motion-sensor/282344
61. https://docs.everythingsmart.io/s/products/doc/b976424e-9d20-411e-a1c8-a62ce0a44b6b
62. https://github.com/espressif/esp-matter/issues/873
63. https://developers.home-assistant.io/docs/core/entity/sensor/
64. https://medium.com/hackernoon/time-synchronization-in-modular-collaborative-robots-d4c218fcb66d
65. https://discourse.openrobotics.org/t/experience-with-ptp-precision-time-protocol-for-mobile-robots/24707
66. https://docs.carnegierobotics.com/time/sync.html
67. https://github.com/sevensense-robotics/core_research_manual/blob/master/pages/time_synchronization.md
68. https://blog.csdn.net/2301_80079642/article/details/146779683
69. https://wiki.ros.org/industrial_extrinsic_cal/Tutorials/Multi_camera_calibration
70. https://github.com/CDonosoK/ros2_camera_lidar_fusion
71. http://cecas.clemson.edu/~stb/ece847/projects/Multiperson_Track_KF.pdf
72. https://github.com/mabhisharma/Multi-Object-Tracking-with-Kalman-Filter/blob/master/README.md
73. https://github.com/JYS997760473/Multi-Object-tracking-2D
74. https://github.com/klintan/ros2_pcl_object_detection
75. https://arxiv.org/abs/1902.10585
76. https://www.semanticscholar.org/paper/Automatic-Online-Calibration-of-Cameras-and-Lasers-Levinson-Thrun/73bed33a5aa661b183ae042783c9ccff2c5820df
77. https://arpg.github.io/papers/Nobre2017_Chapter_Multi-SensorSLAMWithOnlineSelf.pdf
78. https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/154673/eth-14434-02.pdf
79. http://arxiv.org/abs/2312.08610
80. https://arxiv.org/abs/2010.13060v1
81. https://pubs2.ascee.org/index.php/IJRCS/article/download/1136/pdf
82. https://www.academia.edu/112091782/Toward_intelligent_system_health_monitoring_for_NASA_robonaut
83. https://www.alibaba.com/product-insights/raspberry-pi-5-vs-nvidia-jetson-orin-nano-which-dev-board-actually-delivers-on-ai-edge-inference.html
84. https://www.alibaba.com/product-insights/raspberry-pi-5-vs-nvidia-jetson-orin-nano-which-diy-ai-edge-device-wins-for-home-robotics.html
85. https://www.alibaba.com/product-insights/raspberry-pi-5-vs-nvidia-jetson-orin-nano-which-tiny-computer-actually-delivers-on-ai-edge-computing-promises.html
86. https://www.alibaba.com/product-insights/raspberry-pi-5-vs-nvidia-jetson-orin-nano-which-tiny-ai-dev-board-actually-delivers-real-world-performance.html
87. https://www.alibaba.com/product-insights/raspberry-pi-5-vs-nvidia-jetson-orin-nano-which-is-actually-better-for-diy-home-ai-projects-in-2025.html
88. https://www.toolgenx.com/electronics/privacy-first-smart-homes
89. https://www.youtube.com/watch?v=UZ8gg-rrhgY

---

*Fused 2026-06-24 from `04_external_sensor_array__room_brain.md` (Claude) +
`03_external_sensor_array__geodesic.md` (Perplexity). No finds, confidence ratings, or sources dropped;
divergences flagged inline with ⚖️.*
