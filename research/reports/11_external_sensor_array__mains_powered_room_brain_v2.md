# External Sensor Array for Anki Vector: A Mains-Powered “Room Brain” Architecture

## TL;DR

- **Continuous on-robot sensing is physically impossible on Vector** — its ~3.7 V lithium-polymer pack (~2 Wh) runs only ~25 minutes active (Anki’s own support page: “If he is active, he will operate approx. 25 minutes before going back to his charger”; Tom’s Guide measured up to ~45 min), so all heavy room-scale perception must move to a mains-powered “brain box” (Raspberry Pi 5, NVIDIA Jetson Orin Nano Super at $249/67 TOPS, or a Mac mini) that maintains a fused world-model the robot queries over WiFi/BLE.
- **The recommended priority spine is V1 (architecture split) → V2 (far-field audio via ReSpeaker + ODAS/pyroomacoustics) → V6 (ROS 2 + tf2 fusion)** into one time-synced, spatially-registered world-model that emits situational “fingerprints,” with mmWave radar (TI IWR6843) and an on-camera-AI depth camera (Luxonis OAK-D / Intel RealSense) as the highest-value perception adds.
- **A buildable MVP array lands in the €300–500 band** (ReSpeaker mic array + OAK-D-Lite + Pi 5 + ESP32 ambient sensors ≈ €410); the full array adds TI mmWave radar, RPLiDAR/Livox LiDAR, a 360 camera, UWB anchors and a Jetson compute upgrade.

## Key Findings

- Vector already embodies the “self-nulling” principle at small scale — a 4-mic beamforming array, IR time-of-flight laser (~30–1200 mm, 25° FOV), 6-axis IMU, four cliff sensors and capacitive touch, driven by a Qualcomm Snapdragon quad-core 1.2 GHz chip (TechRadar: “a Qualcomm Snapdragon, Quad Core 1.2GHz chip, offering up the same power as some smartphones and tablets”). The design goal is to generalize this self-awareness to the whole room.
- Open, ROS 2-ready stacks exist for every vector: respeaker_ros + ODAS + pyroomacoustics (audio), librealsense/DepthAI (cameras), livox_ros_driver2/rplidar_ros (LiDAR), TI Radar Toolbox (mmWave), nvblox (occupancy/reconstruction), ESPHome/Home Assistant (ambient), spencer_people_tracking (multi-object tracking).
- The hardest claims to stand behind are **mmWave vital-signs through clutter** (works in controlled tests at <1 m, single still subject; degrades with motion/multiple people) and **continuous auto-recalibration** (research-grade, not turnkey). Both are flagged Medium-to-Low confidence below.

## Details

### V1 — Battery & architecture

SUMMARY: Vector’s battery cannot sustain continuous camera+mic+compute, so the box must own continuous heavy perception while the robot becomes a thin client subscribing to distilled signals. Vector ships with a small lithium-polymer pack (third-party replacements cite 300–500 mAh at 3.7 V ≈ 1.1–1.85 Wh; some refurbished units use a 600 mAh pack) and, per Anki’s own support page, “If he is active, he will operate approx. 25 minutes before going back to his charger” and “Vector will be fully charged after approximately 30 minutes”; Tom’s Guide measured up to ~45 minutes of play time. Continuous camera streaming + 4-mic capture + Snapdragon compute is exactly the load that drains it fastest.  The right split: the box runs 24/7 perception and fusion; the robot keeps only safety-critical and intimate-interaction sensing and subscribes to who/where/what + salient events.

HARDWARE: Anki Vector — Qualcomm Snapdragon quad-core 1.2 GHz CPU, 4-mic beamforming array, 120° wide-angle HD camera, IR ToF laser (~30–1200 mm, 25° FOV), 6-axis IMU, 4 cliff/drop sensors, capacitive touch — ~3.7 V battery — interface: WiFi/BLE + gRPC SDK — open driver? yes (wirepod-vector-sdk, Apache-2.0) — power: battery-limited (~25 min active, ~45 min light play).

SOFTWARE: wirepod-vector-python-sdk — github.com/kercre123/wirepod-vector-python-sdk — Apache-2.0 — gives SDK access to camera, audio, proximity, IMU, events; lets the robot subscribe to box-published signals locally (WirePod replaces the dead Anki cloud).

ARCHITECTURE: Box = continuous heavy perception + fused world-model. Robot keeps: cliff/IMU/touch safety reflexes (must be local, hard real-time), close-range mic for intimate talk, its own camera for eye-contact framing. Box owns: room mics, room cameras, depth/LiDAR/radar, ambient sensors. Data plane: robot subscribes to distilled “situational signals” — person IDs + room-frame positions, salient events, situational fingerprints. Latency budget: on-robot safety reflexes <50 ms; “robot taps the feed” for situational context tolerates ~100–300 ms (it’s context, not collision avoidance).

BATTERY MATH: ~2 Wh usable. Continuous camera+mic+radio+Snapdragon compute ≈ 3–5 W → 2 Wh ÷ 4 W ≈ 0.5 h, matching the observed 25–45 min. Off-loading perception lets the robot idle/sleep on its charger and wake only to act, multiplying effective “awareness uptime” from <1 h to 24/7.

ANKI-GRADE SELF-AWARENESS: Vector already models/cancels its own motor noise in its 4-mic beamformer; the box generalizes this by knowing the robot’s commanded state (motion, speech, screen) and subtracting its contribution room-wide.

MAP→VECTOR: L2 perception fusion + situational fingerprints (defines the whole client/server contract).

COST/RISK/PRIVACY: Cost low. Risk: WiFi/BLE latency and dropouts; mitigate with local-only MQTT/DDS and on-robot safety autonomy. CONFIDENCE: High on architecture; Medium on exact battery Wh (sources vary 300–600 mAh, but the drain-time conclusion holds regardless).

### V2 — Far-field audio array

SUMMARY: Generalize Vector’s 4-mic beamforming to the room with one or more USB mic arrays feeding an open SSL/beamforming/AEC/BSS stack. A ReSpeaker USB 4-Mic Array (XVF3800)  gives hardware AEC/DOA/beamforming  with “360° far-field voice pickup (up to 5m)” (Seeed) for ~$79; ODAS adds robust multi-source localization + tracking; pyroomacoustics adds beamforming, DOA (SRP-PHAT/MUSIC) and blind source separation; SpeexDSP/WebRTC provide AEC. Multiple arrays triangulate speaker position in room coordinates. Self-nulling cancels HVAC/fan/robot-motor noise and auto-recalibrates as the room changes.

HARDWARE: ReSpeaker USB 4-Mic Array (XMOS XVF3800) — Seeed — ~$79 — USB UAC1.0 — open driver? yes (libusb/ALSA + respeaker_ros); on-board AEC, AGC, DoA, VAD, dereverberation, beamforming, noise suppression — power: USB-bus. | ReSpeaker 6-Mic Circular Array (Pi HAT) — Seeed — ~$65–80 — I²S on Pi — yes (seeed-voicecard) — USB/HAT power. | MATRIX Creator (8 MEMS mics + FPGA + sensors) — MATRIX Labs — ~$99 last-known (may be discontinued/low stock) — USB/GPIO — yes.

SOFTWARE: ODAS — github.com/introlab/odas — MIT — SRP-PHAT-HSDA localization + M3K modified-3D-Kalman tracking + directive geometric source separation (DGSS); explicitly models mic directivity/body occlusion (the “self-nulling” robot-body move). | pyroomacoustics — github.com/LCAV/pyroomacoustics — MIT — STFT beamforming, DOA (SRP-PHAT, MUSIC), BSS (AuxIVA, ILRMA, SparseAuxIVA, FastMNMF, FastMNMF2), NLMS/RLS adaptive filtering. | SpeexDSP — github.com/xiph/speexdsp — revised BSD — multidelay block frequency (MDF/AUMDF) AEC with double-talk-robust variable learning rate,  multi-channel. | WebRTC Audio Processing (AEC3) — webrtc.googlesource.com / packaged webrtc-audio-processing — BSD-3 — AEC + noise suppression + AGC (“applying speech enhancements… echo cancellation (AEC), noise suppression (NS) and automatic gain control (AGC)”). | respeaker_ros — github.com/furushchev/respeaker_ros — publishes /sound_direction, /sound_localization,  VAD.

ARCHITECTURE: Arrays → box (USB). Box runs AEC (reference = whatever the box/robot is playing) → SSL/DOA → tracking → BSS → ASR/keyword. Multi-array DOA rays triangulate (x,y) speaker position into the room frame. Fuse with the robot’s own 4-mic array when the robot is close (robot publishes its DOA; box does multi-array data association). Latency: DOA/tracking at 20–30 Hz; ~50–150 ms.

ANKI-GRADE SELF-AWARENESS: Continuously adaptive AEC subtracts known playback (robot speech; TV if line-available); ODAS’s directivity model nulls static noise sources; periodic re-estimation of array geometry/noise field handles room/array changes. The box knows robot motor state and gates/subtracts ego-noise when the robot is near an array.

MAP→VECTOR: L2 perception fusion (who-said-what + speaker position) + proactivity (sound-level/quiet context) + situational fingerprints.

COST/RISK/PRIVACY: Seeed has reduced software maintenance for the ReSpeaker family (some algorithm work may fall to the builder). Privacy: always-listening room mics are the most sensitive element — local-only ASR, hardware mute, recording indicator. CONFIDENCE: High on hardware/stack; Medium on robust multi-array triangulation accuracy in reverberant rooms.

### V3 — Cameras: coverage, depth, 360

SUMMARY: Use an on-camera-AI depth camera (Luxonis OAK-D) and/or Intel RealSense for presence/identity/activity + 3D, optionally a fisheye/360 for whole-room coverage, all registered to one room frame and processed on-box for privacy. OAK-D runs neural inference on-device (the Myriad X-based RVC2 delivers “4 TOPS of processing power (1.4 TOPS for AI)” at ~4.5 W max), offloading the box; RealSense D435i gives depth + IMU  with first-class ROS 2 support. Room cameras are allocentric (whole-room), complementing Vector’s single egocentric camera. Depth + pose feeds a 3D reconstruction (nvblox TSDF/ESDF) or a 3D Gaussian-splat map.

HARDWARE: Luxonis OAK-D-Lite — ~$149 — USB3 — open driver? yes (DepthAI, MIT) — USB power; on-device 1.4 TOPS neural inference, 300,000-point stereo depth, 12.3 MP/4K RGB. | OAK-D (S2) — ~$199–249 — USB3/PoE variants — yes; 4 TOPS RVC2. | Intel RealSense D435i — ~$300+ — USB-C — yes (librealsense + realsense2_camera) — ~0.55 W idle / ~2.2 W active (Intel Community: “440mA after launching” at 5 V), ≤3.5 W peak. | Fisheye/360: dual-fisheye USB or Insta360-class — RGB only, libuvc. | Event cameras (DVS) — niche, expensive.

SOFTWARE: DepthAI — github.com/luxonis/depthai — MIT — on-device detection/depth/tracking (YOLO decoding on-device). | librealsense + realsense-ros — github.com/IntelRealSense — Apache-2.0 — depth/IMU/pointcloud topics, depth-to-color extrinsics published. | nvblox / isaac_ros_nvblox — github.com/NVIDIA-ISAAC-ROS/isaac_ros_nvblox — GPU TSDF/ESDF reconstruction + people/dynamic reconstruction + occupancy decay  (Jetson/x86+NVIDIA GPU). | 3DGS: ROSplat (github.com/shadygm/ROSplat, ROS 2 splat visualizer) + SplaTAM/ORB-SLAM-3DGS pipelines for a navigable splat home map.

ARCHITECTURE: Cameras → box; OAK-D does detection on-device, box fuses. Multi-camera extrinsic calibration via an AprilTag array  / Kalibr / MC-Calib registers all cameras to one room frame; time-sync via PTP/host timestamps. Privacy-preserving: run detection/skeleton on-box, never store raw frames by default.

ANKI-GRADE SELF-AWARENESS: Luxonis advertises on-the-fly recalibration through vibration/temperature shifts; the box detects camera miscalibration via a reprojection-error metric and triggers re-extrinsic-calibration; the robot’s silhouette in frame is masked so it doesn’t self-track.

MAP→VECTOR: L2 perception fusion + ENGRAM (3D home map) + situational fingerprints.

COST/RISK/PRIVACY: Cameras are the second most privacy-sensitive element. Mitigate: on-box processing, no cloud, physical shutter/indicator. CONFIDENCE: High.

### V4 — LiDAR / depth / radar for mapping & presence

SUMMARY: For privacy-preserving presence + mapping, rank: (1) **mmWave radar (TI IWR6843)** for presence/people-counting/fall + vital-signs without cameras; (2) **2D LiDAR (RPLiDAR A1)** for cheap floor-plan mapping; (3) **solid-state 3D LiDAR (Livox Mid-360)** for full 3D room map; (4) **UWB (DWM3000) anchors** for cm-level robot/cube positioning. mmWave is the standout for “presence without watching.” Vital-signs are real but fragile through clutter/motion.

HARDWARE: TI IWR6843ISK / IWR6843AOPEVM — TI — ~$300 EVM (DCA1000EVM for raw IF data) — UART/Ethernet — open driver? Radar Toolbox + community ROS examples — low power; 120° azimuth / 30° elevation FOV, ~10 m. | RPLiDAR A1M8 — Slamtec — ~$99 — USB — yes (rplidar_ros) — ~1.5–2 W, 360°, 12 m, ~8000 samples/s. | Livox Mid-360 — ~$600–750 — Ethernet (static IP) — yes (livox_ros_driver2) — 360°×59° FOV,  70 m, 10 cm min range, IP67. | DWM3000 + ESP32 anchors — Qorvo — ~$20–30/node — SPI/WiFi — DIY firmware — low power.

SOFTWARE: TI Radar Toolbox — 3D People Counting, Overhead 3D People Counting, and Vital Signs labs (vital-signs source open for IWRL6432; prebuilt binary + config available for IWR6843; published academic chains use SRP/MUSIC-family + Kalman). | livox_ros_driver2 — github.com/Livox-SDK/livox_ros_driver2 — publishes PointCloud2 + IMU;  pair with GLIM/FAST-LIO for SLAM and pointcloud_to_2dmap for occupancy. | rplidar_ros + slam_toolbox. | multiple_object_tracking_lidar (ROS 2, github.com/aldras/multiple_object_tracking_lidar_ros2). | UWB: ESP32-DWM3000 RTLS — DS-TWR + on-board EKF, “localization with an accuracy of up to 10 cm” (arXiv:2403.10194); field reports 10–15 cm.

ARCHITECTURE: Radar/LiDAR → box. Radar gives presence/positions/vitals as low-bandwidth tracks (privacy-friendly); LiDAR builds/refreshes occupancy + 2D/3D map; UWB anchors (3+) localize the robot and its cube in room coordinates, anchoring the egocentric robot into the allocentric frame.

ANKI-GRADE SELF-AWARENESS: Radar/LiDAR see the robot as a moving cluster; the box subtracts the robot track (known pose from UWB/odometry) so it doesn’t pollute presence counts; nvblox-style occupancy decay forgets stale obstacles (“voxel occupancy probabilities are decayed towards 0.5 over time”).

MAP→VECTOR: ENGRAM (map) + L2 perception (presence/vitals) + proactivity (fall/agitation alerts).

COST/RISK/PRIVACY: Radar = best privacy/compute trade for presence. Risk: in published work (e.g. Pi-ViMo, Harmonic-MUSIC, arXiv:2505.08366) mmWave vital-signs are reliable mainly at close range (~0.6 m) for a single, largely still subject, validated against chest-strap/optical ground truth; accuracy degrades with multiple people, motion and clutter. CONFIDENCE: High for presence/counting; **Medium-Low for vital-signs through clutter** — validate empirically before relying on it.

### V5 — Environmental & ambient sensors (the room’s “feelings”)

SUMMARY: Cheap I²C/Matter sensors add the room’s “feelings” — temp/humidity/pressure, air quality (CO₂/VOC), light/color, sound-level, PIR motion, door/contact — that meaningfully drive proactivity (“dark + quiet → don’t startle”; “CO₂ high → suggest airing out”). Best integrated via ESP32+ESPHome into Home Assistant, then surfaced to the box as low-rate context topics.

HARDWARE: BME680 (temp/humidity/pressure + VOC/IAQ via Bosch BSEC) — ~$15–20 — I²C (0x76/0x77). | Sensirion SCD40/41 (true NDIR CO₂) — ~$25–50 — I²C. | BH1750 / TCS34725 (ambient light / color) — ~$5–10 — I²C. | PIR (HC-SR501) — ~$2 — GPIO. | reed/contact switches + mmWave occupancy as motion. | ESP32 dev board — ~$8 — host.

SOFTWARE: ESPHome (bme680_bsec, scd4x components) — esphome.io — MIT core (BSEC is proprietary, license-accept required) — sensor ingestion; BSEC outputs IAQ, CO₂-equivalent, breath-VOC. | Home Assistant — home-assistant.io — Apache-2.0 — Matter/Zigbee hub + automations; expose entities to the box via MQTT/REST.

ARCHITECTURE: ESP32 nodes → WiFi → Home Assistant → box (context topics) at Hz-to-per-minute rates.

ANKI-GRADE SELF-AWARENESS: BME680 BSEC auto-calibrates its IAQ baseline over time and self-reports accuracy state (Stabilizing / Uncertain / Calibrating / Calibrated); the box treats ambient readings as slow-drift context tagged with those accuracy flags.

MAP→VECTOR: Proactivity + situational fingerprints (the cheap, high-value context layer).

COST/RISK/PRIVACY: Lowest privacy risk of any vector. Caveat: CO₂/VOC sensors need burn-in and the BME680’s VOC channel can read erratically early on. CONFIDENCE: High.

### V6 — Sensor fusion & the shared room world-model

SUMMARY: Fuse everything into one time-synced, spatially-registered world-model on ROS 2 with tf2 as the spatial backbone, nvblox/occupancy for geometry, and a multi-object tracker for people/pets. NTP/PTP (or a hardware trigger) for time-sync; AprilTag-array/Kalibr extrinsic calibration registers all modalities to one room frame; the robot registers into that frame via UWB + AprilTag/visual localization. Fused tracks + context become situational “fingerprints.”

HARDWARE: the box (Pi 5 / Jetson Orin Nano Super / Mac mini) + a PoE/USB hub + (optional) a PTP-capable switch.

SOFTWARE: ROS 2 (Humble/Jazzy) + tf2 — ros.org — Apache-2.0 — transform tree / spatial registration. | nvblox — TSDF/ESDF occupancy + people layer + dynamic reconstruction. | spencer_people_tracking — github.com/spencer-project/spencer_people_tracking — multi-modal people detection + tracking (IMM, track initiation, group tracking; CLEAR-MOT/OSPA metrics; ~20–30 Hz). | robot_localization (EKF/UKF) for fusing odometry/IMU/UWB. | message_filters for approximate-time sync.

ARCHITECTURE: Each sensor node timestamps + publishes in its own frame → tf2 composes to a single `room` frame → a fusion node associates detections across modalities (radar tracks + camera detections + audio DOA) → a unified track list with IDs + positions. The robot publishes its pose (UWB + visual) into `room`; the box answers “where is the robot in the map.” Fingerprints = compact vectors {who present, where, activity, sound/light level, time, salient events} emitted as events.

ANKI-GRADE SELF-AWARENESS: Continuous calibration-drift monitoring (OCAMO/LTO-style residual checks, IEEE T-IV 2023/24) flags decalibration; automatic re-extrinsic-calibration refreshes tf; a failed/moved sensor is detected by covariance/health checks and dropped gracefully.

MAP→VECTOR: This IS L2 perception fusion + situational fingerprints + the ENGRAM glue.

COST/RISK/PRIVACY: Complexity is the main risk; start with two modalities and grow. CONFIDENCE: High on framework; Medium on turnkey continuous recalibration.

### V7 — The Anki-grade self-awareness layer (ego-cancellation & self-calibration)

SUMMARY: Formalize “cancel your own influence + recalibrate over time” across the array. The box knows the robot’s commanded state (motion, speech, screen) and subtracts its contribution from mics (ego-noise/AEC) and cameras/LiDAR (mask the robot’s own track). It runs online drift detection, sensor-health monitoring, automatic re-extrinsic-calibration, and graceful degradation when a sensor fails or moves. The techniques are research-grade but published.

SOFTWARE/TECHNIQUES: AEC (SpeexDSP MDF  / WebRTC AEC3) for audio ego-cancellation; ODAS directivity model for body-occlusion nulling; online camera–LiDAR calibration monitoring/drift tracking (OCAMO and LTO, IEEE Trans. Intelligent Vehicles, “98%+ monitoring accuracy”); “Learning Camera Miscalibration Detection” (Cramariuc, Petrov et al., arXiv:2005.11711) for an RGB miscalibration metric and detection; robot self-calibration framed as offline-SLAM with actuated 3D sensors (Peters et al., J. Field Robotics 2024, “precision comparable to a dedicated external tracking system at a fraction of its cost”); fault detection/diagnosis surveys (ACM Computing Surveys 2018, “On Fault Detection and Diagnosis in Robotic Systems”; Springer Autonomous Robots 2017); autoencoder-based sensor self-diagnosis (denoising shrinkage autoencoder, DSAE, with adaptive online thresholds).

ARCHITECTURE: A “self-model” service on the box ingests robot state + sensor health + calibration residuals and (a) gates/subtracts ego artifacts, (b) raises recalibration jobs, (c) marks degraded sensors and reweights fusion.

ANKI-GRADE SELF-AWARENESS: This is the layer itself — the generalization of Vector’s onboard self-nulling to the whole array.

MAP→VECTOR: L2 perception robustness + ENGRAM integrity.

COST/RISK/PRIVACY: Mostly software effort. CONFIDENCE: Medium — components exist and are published, but integration into one always-on self-model is bespoke.

### V8 — Comms, compute placement & privacy

SUMMARY: Connect sensors by the cheapest reliable bus (USB for mics/RealSense/RPLiDAR; CSI for Pi cameras; Ethernet/PoE for Livox/IP cams; WiFi/BLE for ESP32 ambient + the robot link; Zigbee/Matter via Home Assistant). Place heavy inference where there’s a GPU/NPU. The robot subscribes over local MQTT/DDS. Privacy = local-only, recording indicators, retention limits, an AEGIS-style perimeter.

COMPUTE: Raspberry Pi 5 (~$80; ~8–13 W under sustained CPU+camera load, ~16 W peak with cooler; CPU-only ≈1–4 TOPS; add a Hailo-8L AI HAT for 13 TOPS) vs **NVIDIA Jetson Orin Nano Super** (official: “up to 67 TOPS of AI performance… At just $249,” 7–25 W envelope, CUDA + Isaac ROS, runs nvblox) vs Mac mini (strong general compute but no CUDA / no GPU-accelerated ROS perception). For multi-camera + nvblox + radar fusion, **Jetson is the sweet spot**; Pi 5 suffices for audio + radar + one depth cam; the Mac mini fits builders already in that ecosystem doing CPU-side fusion.

SOFTWARE: ROS 2 DDS or MQTT (Mosquitto) for the robot’s subscription protocol; Home Assistant for smart-home context; WirePod for local Vector voice (no cloud).

PRIVACY / AEGIS PERIMETER: All processing local; firewall the box to block cloud egress. Hardware mute + LED recording indicator on mics/cameras. Default to publishing derived metadata (tracks, fingerprints) rather than raw media; short retention windows; encrypted storage; explicit consent for any logging. Radar-first presence keeps the most sensitive rooms camera-free.

BILL OF MATERIALS — STARTER / MVP (target €300–500):

- Compute: Raspberry Pi 5 (8 GB) + active cooler + PSU + NVMe — ~€110
- Audio: ReSpeaker USB 4-Mic Array (XVF3800) — ~€75
- Depth/AI vision: Luxonis OAK-D-Lite — ~€140
- Ambient: ESP32 + BME680 + SCD40 + PIR — ~€60
- Networking: USB hub + cabling — ~€25
- **MVP subtotal ≈ €410**; add TI IWR6843 radar (~€90) to reach ~€500.

CONFIDENCE: High on parts/prices (±15%, region-dependent).

## FINAL SYNTHESIS

### (1) Starter Array Bill of Materials

|Item                  |Part                                   |~Cost    |Interface|Open driver         |
|----------------------|---------------------------------------|---------|---------|--------------------|
|Compute box           |Raspberry Pi 5 (8 GB) + cooler/PSU/NVMe|€110     |—        |Yes                 |
|Far-field audio       |ReSpeaker USB 4-Mic (XMOS XVF3800)     |€75      |USB      |respeaker_ros / ODAS|
|Depth + on-cam AI     |Luxonis OAK-D-Lite (1.4 TOPS)          |€140     |USB3     |DepthAI (MIT)       |
|Ambient context       |ESP32 + BME680 + SCD40 + PIR           |€60      |WiFi/I²C |ESPHome             |
|Networking            |USB hub + cabling                      |€25      |—        |—                   |
|**MVP total**         |                                       |**~€410**|         |                    |
|(Phase 2) Presence    |TI IWR6843 EVM                         |+€90     |UART     |Radar Toolbox       |
|(Phase 2) Map         |RPLiDAR A1M8                           |+€95     |USB      |rplidar_ros         |
|(Full) 3D map         |Livox Mid-360                          |+€650    |Ethernet |livox_ros_driver2   |
|(Full) Compute upgrade|Jetson Orin Nano Super (67 TOPS)       |+€249    |—        |Isaac ROS / nvblox  |
|(Full) Positioning    |4× DWM3000 + ESP32 UWB                 |+€110    |WiFi     |DIY (DS-TWR + EKF)  |
|(Full) 360 coverage   |dual-fisheye / Insta360-class          |+€200    |USB      |libuvc              |

### (2) Fused-World-Model Architecture

```
              ┌────────────────── BRAIN BOX (mains, 24/7) ──────────────────┐
  Room mics ──USB──►│ AEC → SSL/DOA (ODAS) → BSS → ASR/keyword              │
  OAK-D/RealSense ─USB─►│ on-cam AI detect → depth → nvblox TSDF/ESDF       │
  mmWave radar ──UART──►│ presence / fall / (vitals*) tracks                │
  RPLiDAR/Livox ─Eth/USB►│ occupancy + 2D/3D map                           │
  ESP32 ambient ─WiFi/HA─►│ temp / CO₂ / light / PIR context                │
  UWB anchors ──WiFi──►│ robot + cube cm-position                           │
                       │                 ▼                                  │
                       │   ROS 2 + tf2  (single `room` frame)               │
                       │   multi-modal association → MOT (spencer)          │
                       │   → FUSED WORLD-MODEL (tracks + geometry + context)│
                       │   → SELF-MODEL (ego-cancel, drift/health, recal)   │
                       │   → SITUATIONAL FINGERPRINTS (events)              │
                       └───────────────┬────────────────────────────────────┘
                                       │ MQTT / DDS  (local-only, ~100–300 ms)
                                       ▼
                          VECTOR (thin client, battery)
        keeps: cliff/IMU/touch safety (<50 ms), intimate mic, eye-contact cam
        subscribes: who/where/what, salient events, situational fingerprints
                       (* mmWave vital-signs = experimental, validate first)
```

### (3) Phased Build Plan (minimum viable array → full array)

- **Phase 0 — architecture:** Stand up Pi 5 + ROS 2 + WirePod; prove the robot can subscribe to a box-published MQTT event and react. Establish the local-only network + hardware mute/indicator policy first.
- **Phase 1 — MVP (V2 + V5), ~€410:** ReSpeaker + ODAS room DOA / who-said-what; ESP32 ambient context; emit the first situational fingerprints (“dark + quiet → gentle wake,” “name spoken from the kitchen → orient there”).
- **Phase 2 — perception (V3 + V4):** Add OAK-D-Lite (presence/identity/activity) + TI IWR6843 (privacy presence/fall) + RPLiDAR (floor map); AprilTag extrinsic calibration to one room frame.
- **Phase 3 — fusion (V6 + V7):** Stand up tf2 + nvblox + spencer MOT; the robot registers into the room frame via UWB; add the self-model (ego-cancellation, drift detection, graceful degradation). Upgrade to the Jetson Orin Nano Super once multi-camera + nvblox + tracking run concurrently.
- **Phase 4 — full array:** Livox Mid-360 3D map + a 3D Gaussian-splat home model; 360 camera; full UWB constellation; mmWave vital-signs (flagged reliability).

## Recommendations

1. **Build the spine in order V1 → V2 → V6.** Don’t buy hardware before Phase 0 proves the subscribe-and-react loop end-to-end.
1. **Start with audio + ambient** (cheapest, highest situational value per euro), then add the OAK-D and mmWave radar.
1. **Choose compute by load, not by spec sheet:** Pi 5 for the MVP; switch to the Jetson Orin Nano Super (67 TOPS, $249) the moment you run multi-camera + nvblox + tracking together. **Threshold:** if the fusion loop exceeds ~300 ms or the pipeline becomes GPU-bound, upgrade. Reserve the Mac mini for builders already invested in macOS doing CPU-side fusion only.
1. **Treat mmWave vital-signs as experimental** — validate against a known-good reference (chest strap / pulse oximeter) at the intended range and clutter before any product relies on it; ship presence/fall first.
1. **Make privacy a first-class build target:** local-only processing, hardware mute + recording indicators, derived-metadata-by-default (publish tracks/fingerprints, not raw media), short retention, and a firewalled AEGIS-style perimeter. Prefer radar over cameras in bedrooms/bathrooms.

## Caveats

- Vector battery-capacity figures vary across sources (300 / 500 / 600 mAh); Anki’s own “~25 minutes active” and Tom’s Guide’s “~45 minutes play” bound the range, and the off-board conclusion holds regardless of the exact Wh.
- **mmWave vital-signs through clutter, robust multi-array audio triangulation in reverberant rooms, and continuous auto-recalibration are all research-grade** — confidence Medium-to-Low; validate each empirically rather than assuming datasheet/paper performance transfers to a cluttered living room.
- Some hardware status is in flux: Seeed has scaled back ReSpeaker-family software maintenance (you may need to own more of the DSP), and the MATRIX Creator (~$99 last-known) may be discontinued — verify stock and support before purchase.
- Prices are approximate (±15%) and region-dependent (€ vs $); the TI IWR6843 figure is the EVM price, and a productized radar module would differ.
- nvblox and Isaac ROS require an NVIDIA GPU (Jetson or x86+GPU); on a Pi 5 or Mac mini, substitute CPU/Hailo-based occupancy mapping (e.g., slam_toolbox + OctoMap) for the 3D reconstruction layer.