# RESEARCH GEODESIC: External Sensor Array
## The Room as Vector's Extended Body
*Dexter × Perplexity · 2026-06-24 · Version 1.0*

> **Architecture in one sentence:** The Vector-Brain box runs always-on, mains-powered room perception; Vector subscribes over WiFi to a distilled, fused situational signal — the room's world-model — and brings its own four sensors only for reflexes, close-range intimacy, and safety.

***

## Executive Summary

Vector's stock battery is a 320 mAh LiPo at 3.7 V — roughly **1.18 Wh** of usable energy. A continuously running RGB camera at HD typically draws 0.5–1.5 W, a mic array with DSP 0.5–1 W, and embedded inference 2–5 W. Even at the lowest estimate of ~3 W total for always-on sensing, the battery would be exhausted in **less than 24 minutes** — matching the observed 30–45 minute real-world life under normal use where sensing is gated. The architectural conclusion is stark: **continuous room-scale perception is physically impossible on Vector**. It must live on the box.[^1][^2][^3][^4][^5]

The proposed system divides perception into two orthogonal frames:

| Frame | Owner | Sensing mode | Power source | World model |
|-------|-------|--------------|--------------|-------------|
| **Egocentric** | Vector | Gated, reflex-triggered | 320 mAh LiPo | Cliff/proximity safety, eye-contact camera, intimate voice |
| **Allocentric** | Vector-Brain box | Continuous, always-on | Mains (AC adapter) | Fused 3D room map, person tracks, ENGRAM situational fingerprints |

The box emits a **distilled situational signal** (JSON/MQTT over WiFi) at ~10–50 Hz, which Vector subscribes to on demand with WiFi round-trip latency averaging under 20 ms in practical home conditions.[^6]

***

## V1 — Battery & Architecture: Why Off-Board, and the Robot-as-Thin-Client Split

### SUMMARY

Vector ships with a **320 mAh / 3.7 V LiPo** as its factory battery; the charging circuit is hard-wired to this capacity and will not fully charge larger cells through the dock. Aftermarket 600 mAh cells provide ~40–45 minutes of normal operation; the original 320 mAh gives 25–35 minutes under active use. A continuous camera+mic+inference load of ~3–5 W would drain even the 600 mAh battery in **under 15 minutes**, destroying the experience. The architecture therefore **offloads all continuous heavy perception to the mains-powered box** and keeps Vector's on-board sensing minimal: cliff/drop (4× IR), IMU (6-axis), front laser TOF (1 m range), capacitive touch, 720p camera, and 4-mic array — all gated, not continuous.[^3][^7][^8][^9][^10][^11][^5][^1]

### Battery Math

| Scenario | Load estimate | Battery (600 mAh / 2.22 Wh) | Runtime |
|----------|--------------|------------------------------|---------|
| Normal use (as-shipped) | ~0.8 W average | 600 mAh | ~40–45 min[^1][^3] |
| Always-on camera HD | +0.8 W | — | −20 min (cuts to ~20 min) |
| Always-on mic DSP | +0.5 W (XMOS class) | — | −10 min further |
| On-robot inference (MobileNet) | +1–2 W | — | Would reach ~8 min total |
| **Full continuous sensing** | **~3–4 W** | 2.22 Wh | **≈ 33 min → < 15 min** |

The box (Jetson Orin Nano or Mac Mini) draws 10–15 W but runs on AC mains indefinitely.

### What MUST Stay On the Robot

- **Cliff/drop sensors (4× IR):** cannot be delegated — reflex safety, <1 ms latency required
- **IMU (accelerometer + gyro):** stabilization, fall detection, pick-up response
- **Front NIR laser TOF (1 m):** close-range obstacle, cube detection
- **4-mic array (gated):** intimate conversational voice ("Hey Vector"), wake-word; NOT always streaming
- **720p camera (gated):** eye-contact, face lock, emotional response. Face ID on demand only
- **Capacitive touch:** tactile interaction

### Data Plane: What the Robot Subscribes To

The box publishes over WiFi (802.11n) via an internal MQTT broker:[^12][^13]

```
/room/world_model          (10 Hz) — person positions (x,y,z), activity, orientation
/room/audio/speaker_doa    (20 Hz) — speaker direction, identity, speech content
/room/engram/fingerprint   (1 Hz)  — ENGRAM situational descriptor (scene, mood, occupancy)
/room/presence/radar       (5 Hz)  — presence/absence, vital-sign state (breathing, motion)
/room/environment          (0.2 Hz)— temp, CO2, lux, ambient sound level
/room/alerts               (event) — salient events: new person, loud noise, door open
```

Vector subscribes only to topics relevant to its current behavioral mode (sleeping → only `/alerts`; active → full subscription). WiFi latency under practical home conditions averages **~20 ms**, with a 95th percentile of ~38 ms — sufficient for proactive social behavior (not safety-critical reflexes, which stay on-board).[^6]

### ANKI-GRADE SELF-AWARENESS
On-robot sensing remains passive/gated: mic streams only after wake-word detection, camera activates for face-lock. This "lazy activation" model preserves battery and is the correct robot/box split.

### MAP→VECTOR
This is the architectural root: feeds L2 Cortex perception fusion, the proactivity engine (situational fingerprints), and ENGRAM scene fingerprinting.

***

## V2 — Far-Field Audio Array: Generalizing Anki's 4-Mic Genius to the Room

### SUMMARY

Anki's 4-mic beamforming on Vector is a near-field ego-noise-aware design: the robot knows its own motor noise spectrum and nulls it via adaptive beamforming — a live, actuator-aware AEC system. The room array generalizes this to 5–8 m range using MEMS arrays running ODAS (Open embeddeD Audition System), a C library for sound source localization, tracking, separation, and post-filtering that is free, open-source, and runs on embedded hardware. The recommended hardware is the **ReSpeaker XVF3800 USB 4-Mic Array** (XMOS XVF3800 core), which provides on-device AEC, multi-beamforming, DoA, VAD, noise suppression, and de-reverberation up to 5 m at 360°, via standard USB/ALSA.[^14][^7][^15][^16][^17][^18][^19]

### HARDWARE

| Part | Vendor | ~Cost | Interface | Open driver? | Power |
|------|--------|-------|-----------|--------------|-------|
| **ReSpeaker XVF3800 USB 4-Mic Array** | Seeed Studio | ~$50 | USB 2.0 / ALSA | ✅ Yes (XMOS UAC2) | USB bus (0.5 W) |
| **ReSpeaker 6-Mic Circular Array (Pi HAT)** | Seeed Studio | ~$30 | I2S / HAT | ✅ Yes (ALSA) | Pi HAT (0.3 W) |
| **Matrix Creator / Voice** | Matrix Labs | ~$60 | USB | ✅ Yes (ALSA) | USB bus |
| **XMOS XVF3800 bare board** | XMOS / Seeed | ~$35 | USB / I2S | ✅ Yes | 0.4 W |

For room-scale coverage: **two XVF3800 arrays** placed at opposite corners of the room enable **multi-array triangulation** — DoA from each array is fused geometrically to yield a 3D speaker position, not just an angle. ODAS supports multiple simultaneous sound sources and publishes JSON angle + energy metadata.[^15][^20]

### SOFTWARE

| Library | URL | License | Function |
|---------|-----|---------|----------|
| **ODAS** | github.com/introlab/odas | GPL-2.0 | SSL, tracking, separation, post-filter (SRP-PHAT) |
| **odas_ros** | github.com/introlab/odas_ros | MIT | ROS 2 bridge for ODAS |
| **WebRTC AEC** | chromium-derived | BSD | Acoustic echo cancellation |
| **SpeechBrain** | speechbrain.github.io | Apache 2.0 | Speaker diarization, identity |
| **Whisper** (local) | github.com/openai/whisper | MIT | On-box STT, no cloud |

ODAS uses **SRP-PHAT** (Steered-Response Power with Phase Transform) for localization — it convolves microphone phase relationships over a sphere of candidate positions and identifies peaks. Multi-array triangulation is then performed by intersecting the bearing vectors from each spatially-registered array using the SLAM-derived room coordinate frame.[^20][^15]

### ARCHITECTURE
```
[XVF3800 Array #1 USB]──┐
[XVF3800 Array #2 USB]──┼──► ODAS engine (box) ──► DOA angles ──► multi-array fusion
                         │          │                              │
                         │       AEC: knows box fan noise         ►  speaker_doa topic
                         └──► When Vector is nearby: Vector's      ►  speech_id topic
                              motor noise model injected into AEC
```

### ANKI-GRADE SELF-AWARENESS

The "Anki move" generalized to room scale: the box knows its own fan noise (measured at startup as a spectral profile, stored as a noise model) and applies it as a fixed spectral subtraction before ODAS. When Vector is nearby (position known from room map), its motor noise signature (also pre-measured per-actuator) is injected into the AEC as a known reference signal — exactly the Anki approach, now at room scale. ODAS supports online calibration of inter-array phase offsets, which recalibrates automatically when a new acoustic event occurs. Microphone health is monitored by comparing energy levels across mics in the array; a dead or clipped mic causes a DOA outlier, triggering an alert.[^15]

### MAP→VECTOR
Feeds: far-field speech → STT → NLU pipeline; speaker DOA/ID → person tracking in world-model; acoustic fingerprint → ENGRAM `AUDIO_SCENE` field.

### COST/RISK/PRIVACY
All audio processing on-box. Raw audio never stored; only metadata (DOA, energy, speaker ID token) persists. Physical mute switch on array recommended. **CONFIDENCE: HIGH** — ODAS + XVF3800 is proven in robotics deployments. Open question: multi-array cross-calibration requires careful spatial registration.[^21][^22]

***

## V3 — Cameras: Coverage, Depth, and 360°

### SUMMARY

Room cameras serve three distinct functions: *presence/identity* (who is in the room), *activity recognition* (what they are doing), and *3D map construction* (where everything is). These map onto three camera tiers: **RGB wide-angle** for activity and identity, **depth/stereo** for 3D mapping, and **fisheye/360** for full-room coverage. The Luxonis **OAK-D** family provides all three in one unit: RGB + stereo depth + on-device neural inference (1.4 TOPS) at 4W via a USB 3.0 connection, with a full ROS 2 driver. Intel **RealSense D455** is the best choice for long-range depth: <2% depth error at 4 m, global shutter, integrated IMU, and well-maintained `librealsense2` ROS 2 driver.[^23][^24][^25][^26][^27][^28][^29][^30][^31]

### HARDWARE

| Part | Function | ~Cost | Interface | Depth range | Open driver? |
|------|----------|-------|-----------|-------------|--------------|
| **Luxonis OAK-D** | RGB + stereo depth + on-device AI | ~$150 | USB 3.0 | 0.2–12 m | ✅ depthai-ros |
| **Luxonis OAK-D Pro W** | Wide 150° FOV version | ~$200 | USB 3.0 | 0.2–15 m | ✅ depthai-ros |
| **Intel RealSense D455** | Long-range stereo depth | ~$240 | USB 3.1 | 0.4–10 m | ✅ librealsense2 |
| **Orbbec Gemini 336** | Depth + RGB alternative | ~$130 | USB 3.0 | 0.3–10 m | ✅ Orbbec ROS2 SDK |
| **Insta360 Link / 1RS** | 4K fisheye / 360° coverage | ~$150–300 | USB 3.0 | — (RGB only) | Partial (UVC) |

For a **minimum viable room array**: one OAK-D Pro W in a corner (wide FOV catches most of the room), one RealSense D455 for the opposite angle. For full rooms: two OAK-D Pro W (corner placement) + optional ceiling 360° camera.

The OAK-D's on-device VPU runs person detection, face recognition, and 2D object tracking entirely on-camera, reducing box CPU load significantly. The ROS 2 `depthai-ros` driver streams RGBD as standard ROS topics (`sensor_msgs/Image`, `sensor_msgs/PointCloud2`).[^24][^25][^26][^23]

### Multi-Camera Extrinsic Calibration

The ROS 2 package `extrinsic_calibrator_core` calibrates any number of room cameras using **randomly scattered ArUco markers**: each camera detects markers, the algorithm reconstructs marker positions globally, then solves for camera extrinsics relative to a common room frame. The `ros2_calib` package (IKA RWTH Aachen) extends this to LiDAR-Camera cross-calibration with an interactive GUI.[^32][^33][^34]

**Calibration procedure:**
1. Print ArUco markers (various sizes), scatter around room
2. Run `extrinsic_calibrator_core` — cameras observe markers, global map reconstructed
3. Export TF static transforms → loaded into ROS 2 `robot_state_publisher`
4. Result: all cameras registered to a common `room_frame` TF

### 3D Map Integration

nvblox (NVIDIA Isaac ROS) builds a dense **TSDF + ESDF** volumetric map from RGBD streams in real time on Jetson hardware. It supports multiple simultaneous cameras on Orin 64 GB and produces occupancy grids, mesh outputs, and cost maps directly usable by navigation planners. For the longer-term "3D Gaussian splat home map" referenced in the geodesic, `GS-LTS` and `FreeSplat++` provide incremental Gaussian splat updates as the room changes (furniture moved, object added).[^35][^36][^37][^38][^39][^40]

### ANKI-GRADE SELF-AWARENESS

The box knows Vector's position in the room (from UWB + world model). When Vector is moving, its visual odometry produces known ego-motion; the box uses this to predict camera occlusion artifacts caused by the robot passing in front of a room camera and masks those frames before person tracking. Lens drift is detected by monitoring ArUco-based re-projection error over time; if error exceeds a threshold, `extrinsic_calibrator_core` is triggered automatically (offline, at low-activity time).

### MAP→VECTOR
Feeds: 3D room map (nvblox ESDF) → Vector navigation assistance; person tracks → world model; activity recognition → ENGRAM `ACTIVITY` field.

### COST/RISK/PRIVACY
All video processing on-box. Raw video never stored; only derived features (bounding boxes, person tokens, 3D points). Physical lens cap / LED indicator required. No cloud upload. **CONFIDENCE: HIGH** for OAK-D + RealSense stack. Risk: fisheye 360° cameras have partial UVC support — verify before purchase.

***

## V4 — LiDAR / Depth / Radar for Mapping & Presence

### SUMMARY

Three modalities serve distinct roles in the room model: **2D/3D LiDAR** for high-fidelity geometric mapping, **mmWave radar** for privacy-preserving presence and vital-sign sensing, and **UWB** for cm-accurate robot + cube positioning. The **Livox Mid-360** is the recommended room LiDAR: 360° horizontal, 59° vertical, solid-state (no spinning), priced at ~$500–700, with ROS 2 driver (`livox_ros2_driver`). For privacy-preserving presence, the **Infineon XENSIV BGT60TR13C** 60 GHz FMCW radar detects macro and micro motion (including breathing at rest) up to 5 m, is non-optical, and has an open SDK. For sub-10 cm robot/cube positioning: **ESP32 + DWM3000** UWB anchors achieve ~5–10 cm accuracy at update rates near 100 Hz.[^41][^42][^43][^44][^45][^46][^47][^48][^49][^50][^51][^52]

### HARDWARE RANKED

| Part | Modality | Best for | ~Cost | Interface | Open driver? |
|------|----------|----------|-------|-----------|--------------|
| **Livox Mid-360** | Solid-state 3D LiDAR | Room geometry, people tracking | ~$500–$700[^53][^54] | Ethernet / USB | ✅ livox_ros2_driver |
| **RPLiDAR A3** | 2D spinning LiDAR | Budget 2D map, occupancy | ~$180 | USB | ✅ rplidar_ros |
| **Infineon BGT60TR13C** | 60 GHz mmWave | Presence, vital signs, fall detection | ~$30 eval board | SPI/USB | ✅ Infineon RDK |
| **TI IWR6843AOP** | 60 GHz mmWave | People counting, 3D point cloud | ~$80 | USB | ✅ mmWave SDK |
| **ESP32 + DWM3000 (×4 anchors)** | UWB RTLS | Robot/cube cm-position | ~$20/node | WiFi/serial | ✅ Qorvo SDK |
| **Intel RealSense L515** | ToF LiDAR | Short-range indoor depth | ~$180 (discontinued) | USB 3.0 | ✅ librealsense2 |

### mmWave Radar Deep Dive

The BGT60TR13C uses **FMCW phase measurement** to detect micro-motion: breathing causes chest displacement of ~2–5 mm at 0.1–0.5 Hz, detectable as a phase change \(\Delta\phi = \frac{4\pi\Delta d}{\lambda}\) at 60 GHz where \(\lambda \approx 5\) mm. This enables **non-contact vital sign monitoring** (breathing rate, presence) without any camera — a critical privacy feature for bedroom/bathroom zones. The IWR6843 extends this with 3D people counting and tracking up to 8.6 m range.[^55][^56][^57][^58]

### UWB Positioning

A 4-anchor DWM3000 deployment achieves 5–10 cm accuracy using Two-Way Ranging (TWR) with an Extended Kalman Filter on the tag. Vector wears a tag (attached to dock-box anchor, or embedded in a future revision), and the Power Cube also gets a tag. The anchors are placed at room corners at known positions, uploaded once during setup. The RTLS provides continuous 3D position of both Vector and the Cube at ~100 Hz — enabling the box to know exactly where the robot is in the room coordinate frame at all times.[^43][^45][^47][^41]

### ANKI-GRADE SELF-AWARENESS

The Livox Mid-360 performs continuous **background consistency checking**: a stored static map is differenced against the live scan; moving blobs are tracked, and the static background is updated slowly (furniture drift). The mmWave radar baseline (empty-room calibration) is captured at startup and recalibrated automatically during confirmed-empty periods (e.g., after all persons leave per camera confirmation). UWB clock drift is corrected by the EKF on the tag.

### MAP→VECTOR
LiDAR → occupancy/ESDF map for Vector navigation assistance; mmWave → presence/vital → ENGRAM `OCCUPANCY`, `VITAL_STATE`; UWB → Vector/Cube 3D position → world model.

### COST/RISK/PRIVACY
mmWave is fully non-optical — no image of persons is ever formed. Only abstract presence + vital rate. LiDAR point clouds are retained only as aggregated maps, not raw scan logs. **CONFIDENCE: HIGH** for Livox + DWM3000; **MEDIUM** for BGT60TR13C (open SDK is eval-grade, production integration requires C wrapper work). Risk: Livox Mid-360 is expensive as a Phase 1 component — RPLiDAR A3 is adequate for room mapping at lower cost.

***

## V5 — Environmental & Ambient Sensors: The Room's "Feelings"

### SUMMARY

A small set of cheap ambient sensors dramatically enriches Vector's situational context without privacy concerns, since they produce no personally identifiable information. The highest-value sensors are **CO₂** (NDIR, e.g., SCD40 or MH-Z19C), **ambient light/color** (TSL2561 or TEMT6000), **temperature/humidity** (SHT31 or DHT22), and **PIR motion** (AM312 or HC-SR501). These can be combined on a single **ESPHome ESP32 node** on the local network, exposed to Home Assistant via Matter or Zigbee. The CO₂ sensor is particularly powerful: it provides reliable human-presence detection (CO₂ rises with occupancy) that complements PIR (which times out if a person sits still) — the combination catches both active and stationary occupants.[^59][^60][^61][^62]

### HIGH-VALUE SENSOR SHORTLIST

| Sensor | Part | ~Cost | Detects | ENGRAM signal |
|--------|------|-------|---------|---------------|
| **CO₂ (NDIR)** | SCD40 / MH-Z19C | $5–$20 | Human presence (long-term), ventilation state | `OCCUPANCY_CONFIRMED`, `AIR_QUALITY` |
| **PIR motion** | AM312 / HC-SR501 | $1–$3 | Motion (fast, any warm body) | `MOTION_DETECTED`, `ACTIVE_ROOM` |
| **Ambient light** | TSL2561 / BH1750 | $2–$5 | Lux + color temp, circadian time, scene context | `LIGHT_STATE`, `TIME_OF_DAY_PROXY` |
| **Temperature + humidity** | SHT31 / DHT22 | $3–$10 | Thermal comfort, season, AC state | `THERMAL_COMFORT` |
| **Sound level** | MAX9814 + ADC | $5 | dB ambient noise → "quiet room" detection | `NOISE_FLOOR` |
| **Door/contact** | Reed switch | $1 | Room entry/exit, privacy transitions | `ROOM_ENTRY`, `PRIVACY_ZONE` |
| **Air quality (VOC)** | SGP30 / BME680 | $5–$15 | Cooking, cleaning, air freshener events | `ACTIVITY_PROXY` |
| **Barometric pressure** | BMP280 | $2 | Weather, HVAC state | `PRESSURE_CONTEXT` |

### Integration Architecture

All sensors run on **ESPHome firmware** on an ESP32 (~$4), connected via WiFi or Zigbee to the box's Home Assistant instance. Home Assistant exposes them as MQTT topics, consumed by the ROS 2 bridge on the box. A rule engine converts raw values to ENGRAM-ready signals:[^60][^63]

```
CO2 > 800 ppm AND PIR_triggered_last_5min  → OCCUPANCY_CONFIRMED
lux < 50 AND hour > 20                     → NIGHT_QUIET_MODE  → "don't startle"
noise_floor_dB < 35                        → QUIET_ROOM
temp > 26°C AND humidity > 70%             → THERMAL_DISCOMFORT → behavioral adaptation
```

### ANKI-GRADE SELF-AWARENESS
The MH-Z19C CO₂ sensor supports **automatic baseline calibration (ABC)** — it recalibrates its zero-point over a sliding 7-day window assuming the daily minimum CO₂ (~400 ppm outdoors) corresponds to fresh air. This is self-calibration without user intervention. The light sensor uses factory calibration; the PIR gain is auto-adjusted based on observed false-positive rate in known-empty periods.[^60]

### MAP→VECTOR
Feeds ENGRAM situational fingerprint fields: `THERMAL`, `ACOUSTIC`, `OCCUPANCY`, `AIR_QUALITY`. Proactivity engine: "it's dark and quiet → reduce approach speed and voice volume"; "CO₂ rising → someone just arrived, prepare greeting."

### COST/RISK/PRIVACY
All data stays local. No PII in any sensor reading. ESPHome is fully open-source with Home Assistant integration. Total BOM for a full ambient node: ~$30. **CONFIDENCE: VERY HIGH** — proven consumer/maker stack.[^59][^60]

***

## V6 — Sensor Fusion & the Shared Room World-Model

### SUMMARY

All sensor streams must be unified into a single **time-synced, spatially-registered world-model** before Vector can query it. The recommended framework is **ROS 2 (Humble/Jazzy) + tf2** for coordinate frame management, **PTP (IEEE 1588)** for sub-millisecond time synchronization across sensors, **nvblox** for GPU-accelerated volumetric mapping (on Jetson), and a custom **World-Model Node** that aggregates person tracks, speech events, environmental state, and ENGRAM fingerprints into a single publishable structure. Time synchronization via PTP achieves ROS 2 message timestamping accuracy under 100 microseconds, enabling reliable multi-modal fusion.[^36][^37][^64][^65][^66][^67]

### Time Synchronization

PTP (IEEE 1588) synchronizes all Ethernet/WiFi-connected sensors to a shared clock with hardware-timestamp accuracy <10 µs. For USB sensors (cameras, mic arrays) that lack PTP support, the host ROS 2 node applies a **fixed offset correction** measured during initialization (comparing USB interrupt latency against the PTP-synchronized system clock). The result: all sensor messages timestamped within <1 ms of each other.[^68][^64][^65][^67]

### Spatial Registration

```
room_frame (origin: floor center or room corner)
    ├── /mic_array_1      (from extrinsic calibration)
    ├── /mic_array_2
    ├── /camera_oak_1
    ├── /camera_realsense
    ├── /lidar_mid360
    ├── /radar_bgt60
    └── /vector_base      (from UWB RTLS, updated 100 Hz)
```

All transforms are stored as tf2 static or dynamic transforms. Vector's position in `room_frame` is the UWB RTLS solution, continuously updated, enabling the box to know where the robot is at all times and project room-frame observations into Vector's egocentric frame.[^33][^69][^70]

### Fusion Pipeline

```
[Sensor Drivers] → [ROS 2 Topics] → [World-Model Node]
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
             [nvblox TSDF map]   [Person Tracker]       [ENGRAM Fingerprint]
                    │              (KF + Hungarian)            Generator
                    │                          │
             [3D occupancy]     [person_tracks topic]    [fingerprint topic]
                    │                      │                      │
                    └──────────────────────┴──────────────────────┘
                                           │
                                [World Model Publisher]
                                  (MQTT → Vector WiFi)
```

Multi-object person tracking uses a **Kalman filter + Hungarian algorithm** for data association across camera, LiDAR, and radar detections. Each person gets a persistent UUID; tracks survive brief occlusions via prediction-only mode. The tracker runs in 2D floor-plane projection (x, y, heading) plus height estimate from depth cameras.[^71][^72][^73][^74]

### ENGRAM Fingerprint Generation

The World-Model Node computes a situational fingerprint every second:
```json
{
  "timestamp": 1750768800.0,
  "occupancy": "2_persons",
  "active_speaker": {"id": "person_A", "doa": [2.3, 0.8, 1.1], "speech": true},
  "room_state": "EVENING_QUIET",
  "thermal": "COMFORTABLE",
  "audio_scene": "TV_BACKGROUND",
  "robot_location": {"x": 1.2, "y": 0.8, "z": 0.08, "in_dock": false},
  "salient_events": ["door_opened_3s_ago"],
  "confidence": 0.91
}
```

This fingerprint is the primary payload Vector subscribes to. It summarizes the room state in <500 bytes, publishable at 1–5 Hz with negligible WiFi bandwidth.

### ANKI-GRADE SELF-AWARENESS
Continuous **cross-sensor consistency checking**: if person tracker from camera disagrees with mmWave radar presence (e.g., camera says empty, radar says person present), a confidence flag is lowered and an alert issued. Online extrinsic recalibration (FastCal, Levinson-Thrun) runs continuously in the background, detecting camera-LiDAR drift within 1 second of miscalibration >0.25° or 10 cm.[^75][^76]

### MAP→VECTOR
This IS the architecture. The world-model is the interface between L2 Cortex perception and the room. Every downstream subsystem (proactivity, ENGRAM, navigation) subscribes to it.

***

## V7 — The Anki-Grade Self-Awareness Layer

### SUMMARY

Anki's motor-noise-nullifying beamforming is a specific instance of a general principle: **a system that models its own influence can subtract it**. Generalized to the full room array, this produces four self-awareness mechanisms: (1) **ego-noise cancellation** (box knows Vector's actuator state → predicts its acoustic/visual signature → subtracts it from room sensors), (2) **ego-motion compensation** (Vector's UWB position + IMU used to predict camera occlusions and motion blur), (3) **continuous extrinsic drift detection** (online camera-LiDAR calibration monitoring), and (4) **sensor health monitoring** (fault detection via cross-sensor consistency and outlier analysis).[^76][^77][^78][^75]

### Ego-Noise Cancellation

Vector's motor command stream is available over WiFi (or potentially BLE) to the box. The box maintains a **motor noise model**: a per-actuator spectral profile measured in an anechoic procedure at setup. When Vector's left motor runs at PWM X, the expected acoustic signature (frequency, amplitude, direction relative to Vector's position) is computed and injected as a reference signal into the room AEC — exactly as Anki's onboard beamformer does, now extended to the room-scale array. Papers on semi-blind source separation (SBSS) for AEC provide the theoretical framework for handling nonlinear distortions in this cancellation.[^79][^80]

### Online Extrinsic Calibration

The **FastCal** algorithm performs sensor extrinsic self-calibration with:[^75]
- **Information-theoretic segment selection**: stores only novel, non-redundant measurement sequences
- **Observability-aware parameter update**: rank-revealing decomposition prevents updating unobservable directions
- **Drift-correcting time-decay**: segments age out, preventing stale calibration from locking parameters

The **Levinson-Thrun** online camera-LiDAR calibration detects miscalibration within 1 second of the error exceeding 0.25° or 10 cm with 100% accuracy in experiments, and tracks rotational drift in real-time with mean error of 0.10°. Both algorithms are integrated as background ROS 2 nodes.[^76]

### Sensor Fault Detection

A variogram-based fault detection framework classifies sensor faults into: outlier, spike, variance, offset, gain, and drift faults. Data-centric models use magnitude, gradient, and variance of raw readings; system-centric models compare readings across spatially-related sensors. For the array:[^81]
- **Mic fault**: a dead/clipped mic causes DOA outlier → removed from beamforming, alert issued
- **Camera fault**: re-projection error spike from ArUco → recalibration triggered
- **LiDAR fault**: sudden scan geometry inconsistency with stored map → health alert
- **Radar fault**: baseline drift → recalibration with empty-room procedure

The NASA Robonaut system health monitoring (SHM) approach — combining model-based observers and fuzzy logic for fault detection — provides the conceptual architecture for the box's system health node.[^82]

### Self-Calibration Schedule

| Trigger | Action |
|---------|--------|
| Startup | Mic array noise-floor baseline; camera ArUco extrinsic calibration; LiDAR static map init; UWB anchor survey |
| Daily (low-activity) | Full ArUco re-calibration; mmWave empty-room baseline; CO₂ ABC recalibration |
| Continuous (background) | FastCal extrinsic drift monitor; cross-sensor consistency checks; mic health outlier detection |
| Event-triggered | Sensor moved (geometry inconsistency) → full recalibration of that sensor chain |

### MAP→VECTOR
This layer is invisible to Vector — it ensures the world-model it subscribes to is always accurate, drift-free, and self-healing. It maps to the reliability layer of L2 Cortex.

***

## V8 — Comms, Compute Placement & Privacy

### SUMMARY

All sensors connect to the box via USB 3.0 (cameras, mic arrays) or Ethernet/PoE (LiDAR, future UWB anchors). The box runs ROS 2 Humble/Jazzy on either a **Jetson Orin Nano 8GB** (~$200, 40 TOPS, native MIPI CSI, hardware-accelerated nvblox) or a **Mac Mini M4** (~$600, excellent for local LLM + inference, no ROS-native camera support without USB). For the minimum viable Phase 1 build, a **Raspberry Pi 5 (8 GB)** (~$80) is sufficient for 2D presence + audio, though it cannot run nvblox or YOLOv8 at useful FPS without thermal throttling. Vector subscribes over its existing **802.11n WiFi** to MQTT topics published by the box, with average latency ~20 ms. Privacy is enforced by architecture: all processing is local, raw audio/video is never stored, hardware recording indicators are always-on when sensors are active.[^83][^84][^85][^86][^87][^88][^89][^6]

### Sensor-to-Box Connectivity

| Sensor | Connection | Bandwidth | Notes |
|--------|-----------|-----------|-------|
| OAK-D (2×) | USB 3.0 | ~400 Mbps each | Shared USB root hub → use USB 3.0 hub with VIA VL812 chip |
| RealSense D455 | USB 3.1 | ~400 Mbps | USB 3.1 Gen 1, 7 ms latency[^29] |
| XVF3800 mic array (2×) | USB 2.0 | ~2 Mbps each | UAC2 audio device, plug-and-play |
| Livox Mid-360 | Ethernet (100 Mbps) | ~50 Mbps | UDP point cloud, direct to box NIC |
| BGT60TR13C radar | USB (via MCU) | ~5 Mbps | UART/USB bridge |
| DWM3000 anchors (4×) | WiFi / serial | ~100 kbps | Each anchor ESP32 → MQTT |
| ESPHome ambient node | WiFi | ~10 kbps | MQTT/Home Assistant |
| Vector subscription | 802.11n WiFi | ~50 kbps | MQTT subscribe to world-model |

### Compute Placement

```
[Vector-Brain Box]
├── USB hub (VL812)
│   ├── OAK-D #1 → depthai-ros node (CPU: 1 core, GPU: VPU on camera)
│   ├── OAK-D #2 → depthai-ros node
│   ├── RealSense D455 → librealsense2 node
│   ├── XVF3800 #1 → ALSA → ODAS → odas_ros
│   └── XVF3800 #2 → ALSA → ODAS (multi-array)
├── Ethernet → Livox Mid-360 → livox_ros2_driver
├── WiFi → DWM3000 anchors → UWB RTLS node
├── WiFi → ESPHome ambient → HA MQTT bridge
├── [GPU: Jetson] → nvblox (TSDF mapping) + YOLOv8 (person detect)
├── [CPU] → Person tracker (KF + Hungarian)
├── [CPU] → ENGRAM fingerprint generator
├── [CPU] → FastCal / extrinsic drift monitor
└── [MQTT broker] → Vector WiFi subscription
```

### Box Hardware Options

| Board | AI throughput | Power | ROS 2 | nvblox | ~Cost |
|-------|---------------|-------|-------|--------|-------|
| **Jetson Orin Nano 8GB** | 40 TOPS | 10–15 W | ✅ Native | ✅ Yes[^36] | ~$200 |
| **Raspberry Pi 5 (8GB)** | ~5 FPS YOLOv8n | 5–8 W | ✅ Yes | ❌ No GPU | ~$80 |
| **Mac Mini M4** | High (CoreML) | 10–18 W | Partial | Partial | ~$600 |
| **Intel NUC i5/i7** | Moderate | 15–28 W | ✅ Yes | ❌ No CUDA | ~$350 |

**Recommendation:** Jetson Orin Nano 8GB for Phase 1+; Raspberry Pi 5 for Phase 0 proof-of-concept (audio + presence only).

### Privacy & Consent Architecture (AEGIS-Aligned)

**Principle: local-only, indicator-mandatory, retention-minimal**

1. **No cloud egress**: all inference runs on-box. Zero telemetry to external services.
2. **Hardware recording indicators**: red LED hardwired to camera sensor power (on = recording). Cannot be software-disabled.[^88][^89]
3. **Physical mute switch**: hardware interrupt on mic array power line for each array.
4. **Raw data retention**: audio — 0 s (streaming only, never written to disk). Video — 0 s. Derived metadata (person_id tokens, positions) — ring buffer, 60 minutes maximum.
5. **Consent mode**: at first setup, user explicitly enables each sensor modality. System supports per-zone disabling (e.g., radar-only in bedroom, no cameras).
6. **AEGIS perimeter alignment**: the box is the AEGIS perimeter node. All data stays within the local LAN. No external DNS queries from sensor drivers.

### Robot Subscription Protocol (ENGRAM Seam)

Vector connects to the box MQTT broker at startup. Topic QoS: `world_model` at QoS 0 (best-effort, low latency); `alerts` at QoS 1 (at-least-once delivery). When Vector is docked/sleeping, it unsubscribes from all topics except `/room/alerts` (event-driven wake). This reduces WiFi radio active time and saves battery during dock charging. The MQTT `mqtt_client` ROS 2 package provides the bridge on the box side.[^13][^12]

***

## Final Synthesis: Starter Array BOM + Architecture + Phased Build

### Starter Array Bill of Materials

#### Phase 0 — Minimum Viable Array (~$200)

| Part | Qty | Unit cost | Total | Purpose |
|------|-----|-----------|-------|---------|
| Raspberry Pi 5 (8 GB) | 1 | $80 | $80 | Box compute |
| ReSpeaker XVF3800 USB 4-Mic | 2 | $50 | $100 | Far-field audio, DOA |
| Infineon BGT60TR13C eval board | 1 | $30 | $30 | Presence detection |
| ESPHome ESP32 ambient node | 1 | $10 | $10 | CO₂, PIR, lux, temp |
| USB hub (powered, VL812) | 1 | $20 | $20 | Multi-device USB |
| **Phase 0 Total** | | | **~$240** | Audio presence + ambient |

Capability: room-scale speaker DOA, far-field voice, presence/vital detection, ambient context, ENGRAM fingerprints. No room cameras (audio + radar only = maximum privacy).

#### Phase 1 — Full Starter Array (~$800 additional)

| Part | Qty | Unit cost | Total | Purpose |
|------|-----|-----------|-------|---------|
| Luxonis OAK-D Pro W | 2 | $200 | $400 | Wide-angle RGBD, on-device AI |
| Intel RealSense D455 | 1 | $240 | $240 | Long-range depth for mapping |
| Jetson Orin Nano 8GB + carrier | 1 | $250 | $250 | GPU inference (replaces Pi 5) |
| ArUco marker sheet (A3 prints) | 10 | $0.50 | $5 | Extrinsic calibration |
| **Phase 1 Addition** | | | **~$895** | Full RGBD + AI inference |

Capability adds: person tracking with identity, 3D room map (nvblox), activity recognition, multi-camera extrinsic calibration.

#### Phase 2 — Full Geodesic Array (~$1,100 additional)

| Part | Qty | Unit cost | Total | Purpose |
|------|-----|-----------|-------|---------|
| Livox Mid-360 | 1 | $600 | $600 | 360° 3D LiDAR, precise mapping |
| DWM3000 UWB anchor kit (ESP32) | 4 | $25 | $100 | cm-accurate Vector/Cube position |
| TI IWR6843AOP eval | 1 | $80 | $80 | Multi-person 3D radar tracking |
| Additional XVF3800 (ceiling) | 1 | $50 | $50 | Ceiling-mount omnidirectional array |
| PoE switch (5-port) | 1 | $40 | $40 | Livox + future PoE sensors |
| USB 3.0 PCIe card (Jetson) | 1 | $30 | $30 | Extra USB bandwidth |
| **Phase 2 Addition** | | | **~$900** | Full LiDAR + cm positioning |

**Grand total for full Phase 2 array: ~$2,035**

### Robot / Box Sensing Split Table

| Sensor | On Robot | On Box | Rationale |
|--------|----------|--------|-----------|
| Far-field voice (room-scale) | ❌ | ✅ (XVF3800 arrays) | Battery; coverage |
| Near-field intimate voice | ✅ (4-mic array, gated) | ❌ | Latency; eye-contact intimacy |
| Room presence/tracking | ❌ | ✅ (cameras + radar) | Battery; coverage |
| Close-range obstacle avoidance | ✅ (NIR laser, 4× cliff) | ❌ | Safety reflex, <1 ms |
| Room 3D map | ❌ | ✅ (nvblox + LiDAR) | Compute; persistent map |
| Own position in room | ❌ | ✅ (UWB RTLS) | Range; continuous |
| IMU / stabilization | ✅ (6-axis, always-on) | ❌ | Proprioception |
| Visual recognition (persons) | ✅ (gated, on wake) | ✅ (continuous) | Both: robot for eye-contact, box for tracking |
| Ambient environment | ❌ | ✅ (ESPHome node) | No battery impact |
| ENGRAM fingerprint | ❌ (consumer) | ✅ (producer) | Compute; continuous |

### Fused World-Model Architecture Diagram

```
╔══════════════════════════════════════════════════════════╗
║          VECTOR-BRAIN BOX  (mains-powered)               ║
║                                                          ║
║  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐  ║
║  │XVF3800 ×2│  │OAK-D ×2 │  │RealSense │  │Mid-360   │  ║
║  │(mic DOA) │  │(RGBD+AI)│  │(D455     │  │(3D LiDAR)│  ║
║  └────┬─────┘  └────┬────┘  └────┬─────┘  └────┬─────┘  ║
║       │             │            │              │        ║
║  ┌────▼─────────────▼────────────▼──────────────▼─────┐  ║
║  │              ROS 2 + tf2 + PTP sync                 │  ║
║  │  [extrinsic_calibrator] [FastCal drift monitor]     │  ║
║  └────────────────────────┬────────────────────────────┘  ║
║                           │                              ║
║  ┌────────────────────────▼────────────────────────────┐  ║
║  │         FUSION LAYER                                 │  ║
║  │  nvblox (GPU TSDF)  │  Person Tracker (KF+Hungarian) │  ║
║  │  Speaker DOA fusion │  ENGRAM Fingerprint Generator  │  ║
║  │  Sensor Health Mon. │  Ego-noise Cancellation        │  ║
║  └────────────────────────┬────────────────────────────┘  ║
║                           │                              ║
║  ┌────────────────────────▼────────────────────────────┐  ║
║  │         WORLD MODEL NODE                             │  ║
║  │  /room/world_model    /room/engram/fingerprint       │  ║
║  │  /room/audio/doa      /room/presence/radar           │  ║
║  │  /room/environment    /room/alerts                   │  ║
║  │         MQTT BROKER (Mosquitto)                      │  ║
║  └────────────────────────┬────────────────────────────┘  ║
╚═══════════════════════════╪══════════════════════════════╝
                            │ WiFi 802.11n (~20 ms latency)
╔═══════════════════════════▼══════════════════════════════╗
║                  VECTOR (robot)                          ║
║  Subscribes: world_model, fingerprints, alerts           ║
║  Contributes: motor commands → ego-noise model           ║
║               camera frame → person eye-contact          ║
║               4-mic gated stream → intimate voice        ║
║               IMU + cliff → safety reflexes (local)      ║
╚══════════════════════════════════════════════════════════╝
```

### Graceful Degradation

If the box goes offline, Vector falls back to purely on-robot sensing: gated camera + 4-mic for wake-word + cliff/IMU safety. This is exactly the shipping Anki Vector behavior — a fully functional creature, just without room-scale awareness. The fallback is transparent and automatic via MQTT last-will messages.

***

## Open Questions & Future Work

1. **Motor noise model online update**: as Vector's actuators degrade, their noise signature changes (as Anki addressed). An online motor noise recalibration procedure (Vector performs a standardized motion sequence while mics record) would extend the Anki approach. Frequency: monthly or on actuator replacement.
2. **Vector ↔ box TF loop**: for tight fusion (e.g., projecting room-camera person detections into Vector's visual frame for gaze-following), a low-latency transform from `/room_frame` to `/vector_base` must be maintained. UWB provides position; heading must come from Vector's IMU or camera odometry.
3. **Multi-room extension**: the architecture supports N boxes in N rooms with a shared federated world-model — each box is a room node, and Vector roams between rooms, re-associating with the appropriate MQTT broker via WiFi SSID or BLE beacon.
4. **3D Gaussian Splat integration**: GS-LTS and FreeSplat++ can provide a persistent, visually-rich room map that updates incrementally as the room changes. Integration requires hooking the nvblox ESDF output as a geometric prior for the Gaussian splat optimizer.[^39][^40]
5. **Privacy certification path**: the AEGIS-aligned local-only design is technically sound. A formal threat model (adversarial firmware, physical access to box) should be completed before household deployment.

---

## References

1. [im curious, to those of you who did not yet replace your vector's ...](https://www.reddit.com/r/AnkiVector/comments/1fogcer/im_curious_to_those_of_you_who_did_not_yet/) - 40 minutes is plenty of time running longer only increases the chance of overheating. The 600mah is ...

2. [Replacement Battery For Cozmo and Vector - YouTube](https://www.youtube.com/watch?v=11SVDt4l0s8) - When you Cozmo or Vector battery stops holding a charge it is time to replace them. The typical 5030...

3. [Vector Battery - 600 mah 3.7v Lipo (No international Shipping)](https://techshop82.com/shop/vector-battery-503040/) - Your Cozmo stops working less than 5 minutes after being charged or is DOA on the charger? A new Coz...

4. [Replacing the Battery¶](https://randym32.github.io/Anki.Vector.Documentation/service/Battery%20replacement.html)

5. [Vector Battery upgrade. : r/AnkiVector - Reddit](https://www.reddit.com/r/AnkiVector/comments/191qtf3/vector_battery_upgrade/) - I forget Vector has a predetermined time set to charge or it is based on voltgae drop - either way i...

6. [Comparing the Viability of Different Communication Methods ...](https://ecer.pria.at/archive/ecer-2024/papers/Comparing_the_Viability_of_Different_Communication_Methods_for_Botball.pdf)

7. [Anki Vector Robot: In-Depth Feature Demonstration & AI ...](https://manuals.plus/video/4d01f2f34df5219156c64ff46da19e718d9f61511f881ba05b0f3fbeb6505a96) - This video provides a detailed demonstration of the Anki Vector AI robot companion, highlighting its...

8. [What's Inside Anki Vector - Kinvert](https://www.kinvert.com/whats-inside-anki-vector-hardware/) - What’s inside Anki Vector? What hardware did we use? What are some of the things that set’s Vector a...

9. [Anki Vector Robot | Interactive home robot with artificial ...](https://shop.pishrobot.com/en/product/anki-vector-robot/) - Vector is a smart, curious, funny and lovly home robot that easily communicates with humans and the ...

10. [Vector by Anki - Snapdragon AI Robot- Step Forward for RobotKind](https://www.youtube.com/watch?v=jiDEoGm6Tl0) - Anki Vector - Snapdragon AI Robot- Step Forward for RobotKind
➡️  Buy from Amazon US:  https://amzn....

11. [Vectors battery](https://www.reddit.com/r/AnkiVector/comments/mbyec5/vectors_battery/) - Vectors battery

12. [Announcing mqtt_client, a C++ nodelet for bi-directionally ...](https://discourse.openrobotics.org/t/announcing-mqtt-client-a-c-nodelet-for-bi-directionally-bridging-messages-between-ros-and-mqtt/26878) - We would like to introduce our recently released package mqtt_client! The mqtt_client package provid...

13. [MQTT and ROS2 integration](https://jschrier.github.io/blog/2023/02/10/MQTT-and-ROS2-integration.html) - My previous failure to successfully compile micro-ros-agent illustrates some of the challenges of se...

14. [introlab/odas - Open embeddeD Audition System - GitHub](https://github.com/introlab/odas) - ODAS stands for Open embeddeD Audition System. This is a library dedicated to perform sound source l...

15. [[PDF] ODAS: Open embeddeD Audition System | Semantic Scholar](https://www.semanticscholar.org/paper/ODAS:-Open-embeddeD-Audition-System-Grondin-L%C3%A9tourneau/45b1b900197e12551ed72e967c7223a3562788be) - ODAS, the Open embeddeD Audition System framework, is presented, which includes strategies to reduce...

16. [Meet Vector, Anki's charming new robot](https://mashable.com/article/anki-vector-smart-home-robot) - A powerful, tiny, and charismatic robot.

17. [Recording speaker-microphone - ReSpeaker 4-Mic - Seeed Studio](https://www.directindustry.com/prod/seeed-studio/product-241202-2822900.html) - <b>Product Overview</b><br>This is the enclosed version of the ReSpeaker XVF3800 USB 4‑microphone ci...

18. [Getting Started with reSpeaker XVF3800 USB Mic Array](https://wiki.seeedstudio.com/respeaker_xvf3800_introduction/) - Microphone Array, Quad PDM MEMS microphones in circular pattern, supporting 360° far-field voice cap...

19. [Revolutionising audio manufacturing with DSP and xcore.ai - XMOS](https://www.xmos.com/plug-play-voice-control-xvf3800) - The new ReSpeaker USB microphone array series from Seeed Studio leverages the XMOS VocalFusion® XVF3...

20. [Sound Camera - Michael Yoo Fatemi](https://michaelfatemi.com/posts/2022/05/sound-camera) - This is the method that ODAS uses for sound localization. Code to perform beamforming for one grid s...

21. [Microphone array and audio recording - PAL SDK 23.12 ...](https://docs.pal-robotics.com/ari/sdk/23.12/hardware/microphone.html)

22. [ROS2 on reSpeaker XVF3800 | Seeed Studio Wiki](https://wiki.seeedstudio.com/respeaker_xvf3800_ros2/) - Learn to integrate the ReSpeaker XVF3800 with ROS2 for robotic applications. This tutorial covers si...

23. [OAK-D - Luxonis Docs](https://docs.luxonis.com/hardware/products/OAK-D) - Comprehensive documentation and tutorials for using Luxonis software and tools. Find guides, API ref...

24. [Luxonis - OAK Series - Husarion](https://husarion.com/tutorials/ros-equipment/oak-series/) - The OAK cameras by Luxonis are small cameras for robotic vision with an on-device Neural Network inf...

25. [Serafadam/depthai_ros_driver: ROS2 driver for OAK ...](https://github.com/Serafadam/depthai_ros_driver) - ROS2 driver for OAK cameras. Contribute to Serafadam/depthai_ros_driver development by creating an a...

26. [GitHub - westonrobot/depthai_ros: Official ROS Driver for DepthAI Sensors.](https://github.com/westonrobot/depthai_ros) - Official ROS Driver for DepthAI Sensors. Contribute to westonrobot/depthai_ros development by creati...

27. [Empirical Comparison of Four Stereoscopic Depth Sensing ... - arXiv](https://arxiv.org/html/2501.07421v1) - The D435 should, according to the specifications, be twice less accurate with error of < < < 2% at 2...

28. [How to calculate depth accuracy of D435 and D455? · Issue #7806 · IntelRealSense/librealsense](https://github.com/IntelRealSense/librealsense/issues/7806) - In the datasheet, the depth accuracy of D435 at 2 meter working distance is less than 2%. And D455's...

29. [RealSense D435iF 3D Room Mapping | ROS2 + RViz + SLAM Toolbox (Fast Implementation)](https://www.youtube.com/watch?v=GdbWJpBEYfA) - 🚀 PROFESSIONAL DEMO: Real-Time 3D Room Mapping with Intel® RealSense™ D435iF | ROS2 + SLAM + RViz In...

30. [librealsense2 2.57.6 documentation](https://docs.ros.org/en/jazzy/p/librealsense2/)

31. [Comparative Evaluation of Intel RealSense D415, D435i, ...](https://flore.unifi.it/retrieve/85225dff-c578-4812-9e9b-68a5ac592ef0/Comparative_Evaluation_of_Intel_RealSense_D415_D435i_D455_an.pdf)

32. [extrinsic_calibrator_core 0.1.0 documentation](https://docs.ros.org/en/humble/p/extrinsic_calibrator_core/)

33. [ika-rwth-aachen/ros2_calib: LiDAR-Camera Calibration ...](https://github.com/ika-rwth-aachen/ros2_calib) - Make your calibration dreams come true. ros2_calib is a Multi-Sensor Calibration Tool using ROS2 mca...

34. [README — extrinsic_calibrator_examples 0.1.0 documentation](https://docs.ros.org/en/ros2_packages/humble/api/extrinsic_calibrator_examples/__README.html)

35. [arplaboratory/arpl_nvblox: A GPU-accelerated TSDF and ...](https://github.com/arplaboratory/arpl_nvblox) - A GPU-accelerated TSDF and ESDF library for robots equipped with RGB-D cameras. - arplaboratory/arpl...

36. [Deploy NVBlox with Orbbec Camera on Jetson AGX Orin](https://wiki.seeedstudio.com/deploy_nvblox_jetson_agx_orin/) - This wiki provides a comprehensive, step-by-step guide for deploying NVBlox with Orbbec RGB-D camera...

37. [Nvblox — Isaac ROS](https://nvidia-isaac-ros.github.io/concepts/scene_reconstruction/nvblox/)

38. [Nvblox GPU-Accelerated Incremental Signed Distance ...](https://www.scribd.com/document/977811198/Nvblox-GPU-Accelerated-Incremental-Signed-Distance-Field-Mapping) - Scribd is the world's largest social reading and publishing site.

39. [GS-LTS: 3D Gaussian Splatting-Based Adaptive Modeling ...](https://huggingface.co/papers/2503.17733) - Join the discussion on this paper page

40. [FreeSplat++: Generalizable 3D Gaussian Splatting for Efficient Indoor Scene Reconstruction](https://arxiv.org/abs/2503.22986) - Recently, the integration of the efficient feed-forward scheme into 3D Gaussian Splatting (3DGS) has...

41. [Ultra-Wideband Positioning System Based on ESP32 and DWM3000 Modules](https://arxiv.org/abs/2403.10194) - In this paper, an Ultra-Wideband (UWB) positioning system is introduced, that leverages six identica...

42. [GitHub - Livox-SDK/livox_mapping: A mapping package for Livox LiDARs](https://github.com/Livox-SDK/livox_mapping) - A mapping package for Livox LiDARs. Contribute to Livox-SDK/livox_mapping development by creating an...

43. [DhamuVkl/ESP32-DWM3000-UWB-Indoor-RTLS-Tracker ...](https://github.com/DhamuVkl/ESP32-DWM3000-UWB-Indoor-RTLS-Tracker) - Real-time indoor positioning system using ESP32 & Qorvo DWM3000 UWB modules. Achieve centimeter-leve...

44. [livox_ros2_driver/README_CN.md at master · Livox-SDK/livox_ros2_driver](https://github.com/Livox-SDK/livox_ros2_driver/blob/master/README_CN.md) - Livox device driver under Ros2, support Lidar Mid-40, Mid-70, Tele-15, Horizon, Avia. - Livox-SDK/li...

45. [Build an UWB Indoor Positioning System using ESP32 and Qorvo DWM3000](https://www.slideshare.net/slideshow/build-an-uwb-indoor-positioning-system-using-esp32-and-qorvo-dwm3000-0e7a/283887428) - This project shows how to build an indoor positioning system with centimetre-level accuracy using th...

46. [GitHub - Livox-SDK/livox_ros2_driver: Livox device driver under Ros2, support Lidar Mid-40, Mid-70, Tele-15, Horizon, Avia.](https://github.com/Livox-SDK/livox_ros2_driver) - Livox device driver under Ros2, support Lidar Mid-40, Mid-70, Tele-15, Horizon, Avia. - Livox-SDK/li...

47. [Low Cost Real Time Location Tracking with Ultra-Wideband](https://par.nsf.gov/servlets/purl/10343337)

48. [Infineon/mtb-example-sensors-radar-presence - GitHub](https://github.com/Infineon/mtb-example-sensors-radar-presence) - This code example demonstrates Infineon's radar presence solution to detect human presence within a ...

49. [Infineon/sensor-xensiv-bgt60trxx](https://github.com/Infineon/sensor-xensiv-bgt60trxx) - Contribute to Infineon/sensor-xensiv-bgt60trxx development by creating an account on GitHub.

50. [Ceiling-mounted occupancy detection](https://www.infineon.cn/assets/row/public/documents/24/42/infineon-an141319-ceiling-mounted-occupancy-detection-using-xensiv-demo-bgt60tr13c-60-ghz-radar-applicationnotes-en.pdf)

51. [Installation guide for presence detection solution](https://www.infineon.com/assets/row/public/documents/24/44/infineon-ug120209-installation-guide-for-presence-detection-solution-using-xensiv-bgt60tr13c-radar-som-board-usermanual-en.pdf)

52. [How to get started with XENSIV™ 60GHz BGT60TR13C radar demo board | Infineon](https://www.youtube.com/watch?v=tOfg7Wiq4zE) - Unlock the power of 60GHz radar technology with Infineon's XENSIV BGT60TR13C radar demo board! 🚀

In...

53. [Livox Revolutionizes Smart Robotics with a Compact ...](https://www.livoxtech.com/news/mid360_launch) - Livox and Xpeng Partner to Bring Mass Produced, Automotive-grade Lidar to the Market

54. [Lidar Livox Mid-360: Compact 3D Sensing Solution - Accio](https://www.accio.com/business/lidar-livox-mid-360-lds-z300-e) - Discover the Livox Mid-360 lidar sensor with 360° FOV and 10cm detection range. Ideal for robotics, ...

55. [mmVital-Signs project aims at vital signs detection and ... - GitHub](https://github.com/KylinC/mmVital-Signs) - The mmVital-Signs project aims at vital signs detection and provide standard python API from Texas I...

56. [IWR6843AOPEVM: Request example codes for development](https://e2e.ti.com/support/sensors-group/sensors/f/sensors-forum/1347216/iwr6843aopevm-request-example-codes-for-development) - Part Number: IWR6843AOPEVM Other Parts Discussed in Thread: IWR6843 , IWRL6432 Hi TI, While I compar...

57. [Source Code Request for IWR6843AOPEVM Vital Signs ...](https://e2e.ti.com/support/sensors-group/sensors/f/sensors-forum/1586483/iwr6843aopevm-source-code-request-for-iwr6843aopevm-vital-signs-application) - Part Number: IWR6843AOPEVM Other Parts Discussed in Thread: IWR6843 , IWRL6432 Project Overview We a...

58. [Comprehensive mm-Wave FMCW Radar Dataset for Vital Sign ...](https://arxiv.org/html/2405.12659v1) - This paper introduces a novel dataset, the first of its kind, derived from mm-Wave FMCW radar, metic...

59. [Occupancy Sensor Vs Motion Sensor - Home Assistant Community](https://community.home-assistant.io/t/occupancy-sensor-vs-motion-sensor/358689) - Can anyone recommend a true occupancy sensor… A sensor that “Continuously” reports on room occupancy...

60. [ESPHome Temp Humidity LUX CO2 Motion Sensor](https://community.home-assistant.io/t/esphome-temp-humidity-lux-co2-motion-sensor/282344) - After endless research online for a sensor that does all these things in one and preferably without ...

61. [Home Assistant Entities - Outline](https://docs.everythingsmart.io/s/products/doc/b976424e-9d20-411e-a1c8-a62ce0a44b6b) - Home Assistant Entities

62. [Air quality measurement issue (CON-1090) · Issue #873 · espressif/esp-matter](https://github.com/espressif/esp-matter/issues/873) - Hello, I have problem with setting up the AirQualitySensor device. I want to add CO2 measurement to ...

63. [Sensor entity | Home Assistant Developer Docs](https://developers.home-assistant.io/docs/core/entity/sensor/) - A sensor is a read-only entity that provides some information. Information has a value and optionall...

64. [Time Synchronization in modular collaborative robots](https://medium.com/hackernoon/time-synchronization-in-modular-collaborative-robots-d4c218fcb66d) - Introducing M-cobots, modular collaborative robots

65. [Experience with PTP (Precision Time Protocol) for mobile robots](https://discourse.openrobotics.org/t/experience-with-ptp-precision-time-protocol-for-mobile-robots/24707) - Hello everybody, I would like to collect some ideas on using the Precision Time Protocol (IEEE 1588v...

66. [Time Synchronization — MultiSense Docs documentation](https://docs.carnegierobotics.com/time/sync.html) - Time synchronization allows the data of multiple sensors to be fused into a single system state that...

67. [core_research_manual/pages/time_synchronization.md at master · sevensense-robotics/core_research_manual](https://github.com/sevensense-robotics/core_research_manual/blob/master/pages/time_synchronization.md) - Manual for the Core Research Development Kit. Contribute to sevensense-robotics/core_research_manual...

68. [ROS2---时间戳对齐](https://blog.csdn.net/2301_80079642/article/details/146779683) - 文章浏览阅读1.7k次，点赞43次，收藏12次。ROS2的时间戳对齐是多传感器融合的核心技术，其实现涉及硬件同步、软件算法、通信协议和实时性配置等多个层面。通过硬件触发、PTP协议、库和动态校准算法的...

69. [industrial_extrinsic_cal/Tutorials/Multi_camera_calibration](https://wiki.ros.org/industrial_extrinsic_cal/Tutorials/Multi_camera_calibration)

70. [CDonosoK/ros2_camera_lidar_fusion: ROS2 Package to ... - GitHub](https://github.com/CDonosoK/ros2_camera_lidar_fusion) - ROS2 Package to calculate the intrinsic and extrinsic camera calibration. Adding an easy way to fuse...

71. [D:/PH.D/Fall 08-DIP/Project/Report/Multiperson_Track_KF.dvi](http://cecas.clemson.edu/~stb/ece847/projects/Multiperson_Track_KF.pdf)

72. [Multi-Object-Tracking-with-Kalman-Filter/README.md at master · mabhisharma/Multi-Object-Tracking-with-Kalman-Filter](https://github.com/mabhisharma/Multi-Object-Tracking-with-Kalman-Filter/blob/master/README.md) - Contribute to mabhisharma/Multi-Object-Tracking-with-Kalman-Filter development by creating an accoun...

73. [GitHub - JYS997760473/Multi-Object-tracking-2D: Use Kalman Filter and Hungarian algorithm to do tracking work based on 2D Lidar dataset of KITTI dataset](https://github.com/JYS997760473/Multi-Object-tracking-2D) - Use Kalman Filter and Hungarian algorithm to do tracking work based on 2D Lidar dataset of KITTI dat...

74. [GitHub - klintan/ros2_pcl_object_detection: ROS2 3D object detection and tracking using pointclouds](https://github.com/klintan/ros2_pcl_object_detection) - ROS2 3D object detection and tracking using pointclouds - klintan/ros2_pcl_object_detection

75. [FastCal: Robust Online Self-Calibration for Robotic Systems](https://arxiv.org/abs/1902.10585) - We propose a solution for sensor extrinsic self-calibration with very low time complexity, competiti...

76. [[PDF] Automatic Online Calibration of Cameras and Lasers | Semantic Scholar](https://www.semanticscholar.org/paper/Automatic-Online-Calibration-of-Cameras-and-Lasers-Levinson-Thrun/73bed33a5aa661b183ae042783c9ccff2c5820df) - Two new real-time techniques that enable camera-laser calibration online, automatically, and in arbi...

77. [Multi-Sensor SLAM with Online](https://arpg.github.io/papers/Nobre2017_Chapter_Multi-SensorSLAMWithOnlineSelf.pdf)

78. [DISS. ETH NO. 21912](https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/154673/eth-14434-02.pdf)

79. [A computationally efficient semi-blind source separation based approach for nonlinear echo cancellation based on an element-wise iterative source steering](http://arxiv.org/abs/2312.08610) - While the semi-blind source separation-based acoustic echo cancellation (SBSS-AEC) has received much...

80. [Semi-Blind Source Separation for Nonlinear Acoustic Echo Cancellation](https://arxiv.org/abs/2010.13060v1) - The mismatch between the numerical and actual nonlinear models is a challenge to nonlinear acoustic ...

81. [International Journal of Robotics and Control Systems](https://pubs2.ascee.org/index.php/IJRCS/article/download/1136/pdf)

82. [Toward intelligent system health monitoring for NASA robonaut](https://www.academia.edu/112091782/Toward_intelligent_system_health_monitoring_for_NASA_robonaut?uc-sb-sw=37261115) - This paper presents an intelligent system health monitoring technique for a humanoid robot, Robonaut...

83. [Raspberry Pi 5 Vs NVIDIA Jetson Orin Nano Which Dev Board ...](https://www.alibaba.com/product-insights/raspberry-pi-5-vs-nvidia-jetson-orin-nano-which-dev-board-actually-delivers-on-ai-edge-inference.html) - Raspberry Pi 5 vs NVIDIA Jetson Orin Nano: real-world AI edge inference benchmarks, power efficiency...

84. [Raspberry Pi 5 Vs NVIDIA Jetson Orin Nano Which DIY AI Edge ...](https://www.alibaba.com/product-insights/raspberry-pi-5-vs-nvidia-jetson-orin-nano-which-diy-ai-edge-device-wins-for-home-robotics.html) - Raspberry Pi 5 vs NVIDIA Jetson Orin Nano: a hands-on, real-world comparison for home robotics build...

85. [Raspberry Pi 5 Vs NVIDIA Jetson Orin Nano Which Tiny ...](https://www.alibaba.com/product-insights/raspberry-pi-5-vs-nvidia-jetson-orin-nano-which-tiny-computer-actually-delivers-on-ai-edge-computing-promises.html) - Raspberry Pi 5 vs NVIDIA Jetson Orin Nano: A real-world, benchmark-backed comparison for AI edge com...

86. [Raspberry Pi 5 Vs NVIDIA Jetson Orin Nano Which Tiny AI Dev ...](https://www.alibaba.com/product-insights/raspberry-pi-5-vs-nvidia-jetson-orin-nano-which-tiny-ai-dev-board-actually-delivers-real-world-performance.html) - Raspberry Pi 5 vs NVIDIA Jetson Orin Nano: real-world benchmarks, power efficiency, AI inference lat...

87. [Raspberry Pi 5 Vs NVIDIA Jetson Orin Nano Which Is Actually Better ...](https://www.alibaba.com/product-insights/raspberry-pi-5-vs-nvidia-jetson-orin-nano-which-is-actually-better-for-diy-home-ai-projects-in-2025.html) - Raspberry Pi 5 vs NVIDIA Jetson Orin Nano: A practical, real-world comparison for DIY home AI projec...

88. [Privacy-First Smart Homes: Cameras with Shutters, Visual ...](https://www.toolgenx.com/electronics/privacy-first-smart-homes) - Complete guide to building a privacy-focused smart home in 2025. Expert reviews of cameras with phys...

89. [USENIX Enigma 2023 - Meaningful Hardware Privacy for a Smart and Augmented Future](https://www.youtube.com/watch?v=UZ8gg-rrhgY) - Meaningful Hardware Privacy for a Smart and Augmented Future

Marcus Hodges, Meta

Smart home device...

