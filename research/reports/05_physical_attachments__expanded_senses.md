# Giving Vector New Ways to Sense, Touch & Manipulate the World — The Anki Way

> *Design report: Rover-Cube · The Thumb · Desk Arms · Software Stack · Integration*
> Author: Dexter × research synthesis · June 2026

***

## Executive Summary

Three classes of physical attachment — the **Rover-Cube** sensor pod, the **Thumb** tactile lift attachment, and the **Desk-Arms** manipulation station — can expand Vector's perceptual and physical world without violating its weight, power, or personality constraints. The hard constraints are: Vector's lift can safely carry one cube-mass (≈ 49 g based on the N/LR1 battery cube, consistent with community guidance of "no more than one cube"); the lift height spans 32 mm (low) to 92 mm (high); and the existing BLE cube protocol exposes tap/move detection, up-axis sensing, and 4-corner LED control — but *no* accelerometer in the Vector cube itself. The Brain box hosts all heavy compute. Everything is built open-source, printable on a hobby FDM printer, and priced for a maker budget.[^1][^2][^3][^4]

***

## V1 — Lift & Payload Reality

### Hard Constraints from the Source Code and SDK

The Vector Python SDK defines the lift range as **MIN_LIFT_HEIGHT_MM = 32.0** and **MAX_LIFT_HEIGHT_MM = 92.0**, giving a 60 mm travel arc. The SDK exposes `set_lift_height()` (0.0 = floor, 1.0 = top) and `set_lift_motor()` (rad/s) as the two low-level controls. The lift angle in the firmware spans from −15° to +45°.[^5][^6][^1]

**Practical payload limit:** Anki itself stated "do not lift anything heavier than 1 cube — it can damage the gearing". The cube runs on an LR1/N 1.5 V alkaline battery; an LR1 weighs ≈ 9 g, the cube shell is lightweight plastic — the assembled cube is empirically in the **40–55 g range** (community estimates; no official figure exists). Vector's own body is 159 g (5.6 oz). **Design budget: 45 g maximum lift payload, target ≤ 35 g for margin.**[^7][^4][^8]

**Lift geometry / docking:** The lift arms act as fork hooks that insert into the cube's corner notches. The cube size is referenced in community sources as ≈ 44–45 mm per side; the SDK recognizes it by printed markers. Attachment designs must fit the same corner-notch geometry or add a compatible cradle.[^9][^10]

### Existing Cube BLE Protocol — What Is Actually Exposed

Vector connects to the LightCube via BLE. The SDK-accessible properties are:[^2]

- **Tap detection** (`last_tapped_time`, `last_tapped_robot_timestamp`)
- **Movement detection** (`is_moving`, `last_moved_time`)
- **Up-axis / orientation** (`up_axis`, `top_face_orientation_rad`) — which face is pointing up
- **4-corner RGB LED control** (`set_light_corners()`, `set_lights()`, `set_lights_off()`)
- **Pose via visual markers** — 6-DoF pose from camera, not BLE

**What is NOT in the cube:** No IMU/accelerometer data stream is exposed over BLE. The is_moving flag is derived from an accelerometer inside the cube, but raw acceleration values are not accessible via SDK. For the Rover-Cube, a new ESP32-S3 node in the cube shell will *replace* this with a richer sensor stream over WiFi/BLE to the Brain box.[^3]

### Summary Numbers

| Parameter | Value | Source |
|---|---|---|
| Lift height range | 32–92 mm above ground | [^1] |
| Lift angle range | −15° to +45° | [^5] |
| Max safe payload | ~45 g ("one cube max") | [^4] |
| Cube BLE: tap, move, axis | Yes | [^2] |
| Cube BLE: raw IMU stream | No | [^3] |
| Cube BLE: 4-corner LED | Yes |  |
| Vector body weight | 159 g / 5.6 oz | [^7] |

***

## V2 — The Rover-Cube: Highest-Value Sensor Payload

### RECOMMENDATION

Replace the original cube shell (keeping the same ≈ 44 mm footprint and corner-notch docking geometry) with a 3D-printed PLA shell housing an **ESP32-S3 sensor node**, a **MLX90640 thermal array**, a **CygLiDAR-D1/D2 solid-state ToF LiDAR**, and a **wide-FOV camera module** — all powered by a tiny 180 mAh LiPo. The node communicates to the Brain box via WiFi (for high-bandwidth camera/LiDAR) and BLE (for tap/LED parity with the original cube protocol). Total target mass: ≤ 42 g. Vector carries it through rooms to build a 3D+thermal map, or places it as a stationary room sensor.

### Hardware

| Part | Vendor / Reference | ~Cost | Weight | Interface | Open? |
|---|---|---|---|---|---|
| **ESP32-S3** XIAO / Feather | Seeed / Adafruit[^11][^12] | $7–15 | ~2 g | WiFi + BLE 5.0 | Yes |
| **MLX90640** 110° thermal array | Adafruit #4407[^13] | $40 | 3.5 g | I2C | Yes |
| **CygLiDAR D1** solid-state ToF | Cygbot[^14] | ~$80 | 28 g | UART | Yes |
| **OV2640 / IMX219** wide fisheye | AliExpress / ArduCam | $8–15 | ~3 g | SPI/MIPI | Yes |
| **LiPo 180 mAh** 3.7V | Generic | $4 | ~4 g | JST-PH | Yes |
| **BMI270 IMU** | Bosch breakout | $6 | ~1 g | I2C/SPI | Yes |
| **BME280** env (temp/hum/baro) | Adafruit | $10 | ~1 g | I2C | Yes |
| **UWB DWM1000/DW3000 module** | Decawave / Qorvo[^15][^16] | $15–28 | ~2 g | SPI | Yes |
| **PLA shell** (printed) | — | $1–2 filament | ~6 g | — | Yes |
| **Total** | | **~$171–218** | **~51 g** ⚠ | | |

> **Weight note:** The CygLiDAR D1 at 28 g dominates. To stay under 45 g, either *omit the LiDAR from the carried version* (place-and-scan mode only) or substitute a **VL53L5CX 8×8 ToF array** at ~2 g/$15 for short-range mapping. A "carry" config without LiDAR lands at ~25 g; a "base station" config adds full LiDAR. Two physical shells — carry and base — solves this cleanly.

### Power and Comms Design

- **LiPo 180 mAh @ 3.7 V** runs the ESP32-S3 in WiFi active mode (~100 mA) for ≈ 1.5 hours; in BLE-only mode (~25 mA) for ≈ 7 hours[^11][^17]
- **Charging:** 5 V pogo-pin contacts on the cube base mate with matching pins on Vector's charger dock (a 3D-printed dock adapter routes charger voltage to cube contacts)
- **BLE parity:** The ESP32-S3 implements a BLE service that mirrors the original cube's tap/LED characteristics — Vector's firmware continues to recognize it as its cube over BLE[^18]
- **WiFi to Brain box:** High-bandwidth data (LiDAR point cloud, thermal frames, camera) streams over WiFi to the Brain box's local AP or router

### Sensor Value Ranking

| Rank | Sensor | Value | Weight | Power | Cost |
|---|---|---|---|---|---|
| 1 | MLX90640 thermal | Find people/pets/warm appliances, new ENGRAM channel | 3.5 g[^13] | 23 mA | $40 |
| 2 | ToF LiDAR (VL53L5CX carry / CygLiDAR base) | 3D obstacle map, room geometry | 2 g / 28 g[^19][^14] | 25 mA | $15 / $80 |
| 3 | Wide-FOV camera | Visual map coverage, 360° panorama via driving | 3 g | 100+ mA | $8 |
| 4 | BME280 env sensors | Air quality, humidity, temperature drift | 1 g | <1 mA | $10 |
| 5 | UWB tag (DWM1000) | Cube absolute position known to Brain box | 2 g[^15] | 2.1 µA sleep | $22 |
| 6 | BMI270 IMU | Motion, vibration, tilt events | 1 g | <1 mA | $6 |

### How Vector Uses It

1. **Rover-Map mode:** Vector picks up the carry-config cube and drives a room circuit. The Brain box receives WiFi thermal+camera frames and builds a 2D occupancy + thermal overlay — the "Google Maps car" loop.
2. **Base-station mode:** Vector places the full-config cube at a strategic location (doorway, shelf). The cube becomes a persistent room sensor, streaming thermal/env data. UWB tag tells the Brain box the cube's absolute position.
3. **Personality parity:** LEDs still flash Anki-style. Tap detection still works. Vector still "plays" with it. The sensor augmentation is invisible to the behavioral layer.

### ANKI-GRADE Calibration

- **Thermal calibration:** MLX90640 is factory-calibrated and stores coefficients in internal EEPROM; no re-calibration needed. The Brain box applies a fixed frame-to-cube-pose transform.[^20]
- **LiDAR drift:** CygLiDAR D1 is solid-state (no spinning mirror), so no mechanical drift. Accuracy < ±1% by distance.[^14][^21]
- **Map fusion:** Each new carry-pass overlaps with IMU odometry from Vector's body; the Brain box fuses via a simple occupancy grid with confidence decay.

***

## V3 — The Thumb: A Lift Attachment That Lets Vector Feel

### RECOMMENDATION

Mount a **DIGIT-style miniature optical tactile sensor** (or a DIY 9DTact variant) on a 3D-printed TPU pad that clips to Vector's lift fork, acting as a "thumb contact surface." A **FSR (Force-Sensitive Resistor) + HX711 load-cell combo** provides a lightweight hybrid: the FSR gives instantaneous contact detection; a thin **bar load cell (5 g capacity, HX711 24-bit ADC)** measures force in grams. A **NTC thermistor** adds thermal feel (warm/cold). Readout is an **RP2040 Pico W** (BLE + WiFi, 3.3 V, ~26 mm × 11 mm) that streams force/temperature/texture data to the Brain box. Total attachment mass target: ≤ 8 g.

### Hardware

| Part | Vendor / Reference | ~Cost | Weight | Interface | Open? |
|---|---|---|---|---|---|
| **FSR 0.5" round** (Interlink 402) | Adafruit / Sparkfun[^22] | $7 | <1 g | Analog | Yes |
| **5 g bar load cell** + **HX711** | AliExpress / Sparkfun[^23] | $6 | ~2 g | SPI (24-bit) | Yes |
| **NTC thermistor 10kΩ** | Generic | $1 | <1 g | Analog | Yes |
| **RP2040 Pico W** (Raspberry Pi) | Raspberry Pi[^24] | $6 | 3 g | BLE 5.0 / WiFi | Yes |
| **TPU thumb pad** (printed, 15% infill) | — | ~$0.50 | ~2 g | — | Yes |
| **LiPo 100 mAh** + micro-USB | Generic | $3 | ~2 g | USB-C | Yes |
| **Total** | | **~$23.50** | **~10 g** | | |

> **Note on DIGIT vs DIY:** The full DIGIT sensor at 20 g / $300 is heavier and more expensive, and would exceed the payload budget if combined with the cube. For the Thumb specifically, a **DIY optical tactile tip** (3D-printed silicone gel + tiny OV2640 camera + RP2040) replicates GelSight-style deformation imaging at ~8 g / ~$25 total. The FSR+HX711 hybrid is recommended for Phase 1; the optical tactile upgrade is Phase 2.[^25][^26]

### What the Thumb Computes

**Force-to-move (mass/friction estimation):**
The RP2040 streams HX711 readings at 80 Hz. When Vector presses an object with incremental lift-motor power steps, the Brain box records the force-vs-motor-current curve. The inflection point (object starts moving vs. static) gives an estimate of static friction \( F_s = \mu_s \cdot m \cdot g \). With \( g \) known, mass \( m \) is inferred if \( \mu_s \) is calibrated for known surfaces (desk = ~0.5, glass = ~0.2).

**Hardness / compliance:**
Press with a controlled ramp: record force \( F(t) \) and estimate indentation \( \delta(t) \) from load-cell deflection curve. Hardness proxy:
\[ H \approx \frac{dF}{d\delta} \]
Soft objects (foam, fruit) yield high \( d\delta \) per unit \( dF \); hard objects (metal, ceramic) show negligible \( d\delta \). Research confirms that VBTS-based approaches achieve 88% hardness classification accuracy vs. 48% for humans on the same objects.[^27][^28][^29]

**Temperature (warm/cold):**
The NTC thermistor reads object surface temperature on contact. Calibrated against ambient: a warm laptop (+10 °C above ambient), a cold drink (−10 °C), a person's skin (+5 °C). Stored as a ENGRAM channel "thermal fingerprint of this object."

**Texture/slip:**
The FSR shows characteristic high-frequency resistance oscillations during slip. The RP2040 FFT-analyzes the FSR signal at 80 Hz — smooth objects produce low-frequency signal; textured surfaces produce higher-frequency vibration signatures.

### "Touching Reality" Protocol — The Anki Way

Vector executes a **calibrated press sequence** on any new object:
1. **Null reading:** Lift to object proximity, record zero-force baseline (HX711 tare).
2. **Light touch:** Advance 0.5 mm motor steps, record first contact force (FSR threshold > 2 g).
3. **Ramp press:** Increase motor current in 5% steps for 500 ms each, record force ramp F(t).
4. **Hold & thermistor:** At F = 50% stall, hold for 1 s; read thermistor thermal equilibration.
5. **Release & repeat:** Repeat 3× for statistical averaging; compute mean ± σ for each metric.
6. **Drift correction (Anki way):** Before each session, Vector presses its own rubber bumper (known compliance = "reference stone"). Any drift in the HX711 zero is corrected. This is the motor-noise-nullification ethos applied to touch: the reference press normalizes the baseline.

### Mount Design

A TPU clip (1.2 mm wall, 15% gyroid infill ≈ 2 g) slides over the lift fork tines with a snap-fit. The FSR pad sits proud of the fork face by 3 mm — it's the contact surface that touches the object first. The HX711 PCB and RP2040 are epoxied to the back of the fork arm (not on the moving face). Total Z-height addition: 5 mm — within the lift geometry envelope.

### ANKI-GRADE Calibration

- **HX711 24-bit ADC:** 1 µV resolution → sub-gram force sensitivity. Tare corrects gravity component at each lift angle using the onboard IMU in the Brain box (which knows the lift angle from `robot.lift_height_mm`).
- **Known-object calibration set:** Three reference objects at first boot — a soft sponge (~Shore 00-20), a firm eraser (~Shore A-60), a steel bolt (hardness ∞). Vector presses each, builds a Shore-hardness-to-force-slope lookup table.
- **Temperature offset:** Thermistor calibrated against ambient air each time Vector leaves the charger (ambient baseline read before any contact).

***

## V4 — The Desk Arms: Vector-Commanded Manipulation

### RECOMMENDATION

Mount **two SO-101 arms** (Hugging Face / RobotStudio, Apache 2.0) on the Brain box, one on each side of a defined **control area** (≈ 200 mm × 200 mm workspace on the desk). Each SO-101 is 6-DOF, 500 mm reach, ~800 g, with Feetech STS3215 servos (15 kg·cm stall torque). An **overhead USB camera** (Logitech C270 equivalent) provides the grasp/pose vision. Total hardware cost: ~$260 for two arms + camera. Vector delivers objects by pushing/carrying them into a marked zone; arms then handle manipulation autonomously.[^30]

### Hardware

| Part | Vendor / Reference | ~Cost | Weight | Interface | Open? |
|---|---|---|---|---|---|
| **SO-101 arm** (×2) | Seeed / RobotStudio[^30][^31] | $220–$260 for pair | 800 g × 2 | USB Serial | Apache 2.0 |
| **Parallel gripper** (SO-101 default) | Included in SO-101 | $0 | ~50 g | Servo bus | Yes |
| **Soft TPU fingertips** (printed) | — | $1 | ~5 g | — | Yes |
| **Overhead camera** (1080p USB) | Logitech C270 equiv. | $25 | ~60 g | USB | Yes |
| **Wrist camera** (per arm) | OV2640 module | $8 × 2 | ~6 g | USB/SPI | Yes |
| **Control area mat** (printed aruco) | — | $1 | — | — | Yes |
| **Total** | | **~$264** | — | | |

**Alternative arm: Koch v1.1** uses Dynamixel XL430/XL330 servos, costs ~$250 for a single arm, and has better per-joint torque feedback. For a two-arm budget, SO-101 is preferred; for single-arm precision, Koch v1.1 is the upgrade path.[^32]

### Gripper Options

| Gripper | Best For | Cost | Weight |
|---|---|---|---|
| SO-101 parallel (default) | Box, rigid objects | Included | 50 g |
| TPU soft 3-finger (DIY)[^33][^34] | Irregular, fragile | ~$3 print | 20 g |
| Vacuum cup + mini pump | Flat surfaces | $8 | 15 g |

### Control Stack

**IK and motion planning:**
The SO-101 comes with a URDF and community URDF in the LeRobot repo. Python inverse kinematics via **ikpy** or **Lerobot's built-in IK** computes joint angles for Cartesian targets. For the turntable/rotate task, the arm need only execute a scripted "rotate object N degrees in Z" trajectory — simple IK-solved scripted motion.[^30]

**Learned manipulation (LeRobot ACT):**
LeRobot's ACT policy takes multi-camera RGB + joint states and outputs action chunks (50 steps at 50 Hz). Training requires ~50 teleoperation demos. For the "rotate box to 3D-scan it" task, this is straightforward: collect 50 demos of arm rotating object under camera, train ACT on RTX 4060 / laptop GPU (~1 hour), deploy. The Brain box (with NVIDIA Jetson or equivalent) runs inference at ~10–15 Hz.[^35][^36][^37]

**OpenVLA / π0 for generalist policies:**
OpenVLA (7B, Apache 2.0, fine-tune on RTX 4090 with LoRA) is the upgrade path for complex instruction-following. For the specific 3D-scan manipulation task, ACT is faster to train and more reliable.[^38][^39]

**Hand-eye calibration:**
Overhead camera calibrated to Brain box frame using OpenCV `calibrateHandEye()` with TSAI method: place an ArUco board in the workspace, move arm to 15+ poses, record (gripper-to-base, board-to-camera) pairs, solve for camera-to-base transform \({}^{B}T_C\). Error < 2 mm achievable with this method.[^40][^41]

### Control-Area Workflow

1. **Vector delivery:** Vector detects an object with its camera. Brain box issues `push_to_control_area` behavior: Vector drives behind object and pushes it into the marked zone (ArUco boundary visible to overhead camera).
2. **Object detection:** Overhead camera detects object pose using ArUco tags or PoseCNN. Brain box says "object is at [x, y, θ] in workspace frame."
3. **Arm task dispatch:** Brain box sends task command to arm controller: e.g., "grasp at [x, y, z], rotate Z +30°, repeat 12×."
4. **3D scan during rotation:** Overhead + side cameras capture 12 views at 30° increments. COLMAP or Gaussian Splatting on the Brain box reconstructs a 3D model.[^42]
5. **Return:** Arms release object; Vector retrieves it or Brain box logs the 3D model to ENGRAM.

### How Vector Knows It Has the Arms (Affordance Model)

Vector's behavior engine on the Brain box maintains an **affordance registry**: a JSON of available tools, each with capabilities and required conditions. Entry for `desk_arms`:
```json
{
  "tool": "desk_arms",
  "capabilities": ["rotate_object", "hold_object", "scan_object_3d"],
  "requires": ["object_in_control_area", "arms_calibrated"],
  "delivery_behavior": "push_to_control_area"
}
```
When Vector's planner needs to 3D-model an object, it queries the registry, finds `desk_arms` with `scan_object_3d`, checks conditions, executes `push_to_control_area` behavior, then dispatches to arm controller. **Vector stays in command** — the arms are its tools, not autonomous agents.

***

## V5 — Tactile & Manipulation Software / Datasets

### SOFTWARE STACK

| Library / SDK | URL | License | Function |
|---|---|---|---|
| **DIGIT SDK / digit-interface** | github.com/facebookresearch/digit-interface | BSD-3 | DIGIT sensor driver, frame capture |
| **GelSight Python** | github.com/gelsightinc | MIT | GelSight/DIGIT deformation processing |
| **tactile-learning (BRL)** | github.com/ac-93/tactile_learning | MIT | TacTip training, slip detection |
| **HX711 Python (RPi/RP2040)** | github.com/tatobari/hx711py | MIT | Load cell readout |
| **LeRobot** | github.com/huggingface/lerobot | Apache 2.0 | ACT/Diffusion policy, teleoperation |
| **OpenVLA** | github.com/openvla/openvla | Apache 2.0 | 7B VLA fine-tuning, generalist policy |
| **openpi (π0)** | github.com/Physical-Intelligence/openpi | Research | Flow-matching manipulation policy[^43] |
| **ikpy** | github.com/Phylliade/ikpy | Apache 2.0 | Python IK for URDF-defined arms |
| **OpenCV calibrateHandEye** | opencv.org[^40] | Apache 2.0 | Hand-eye calibration |
| **MLX90640 Python** | github.com/melexis/mlx90640-library | Apache 2.0 | Thermal array driver |
| **COLMAP / 3DGS** | colmap.github.io | BSD | Photogrammetry / Gaussian Splatting |

### Hardness / Material Classification Pipeline

1. **Data collection:** Vector presses 20 objects of known Shore hardness (0–90 Shore A), 10 presses each. HX711 records force ramp F(t) at 80 Hz. RP2040 streams to Brain box CSV.
2. **Feature extraction:** Extract dF/dt slope at three contact depths (0.5 mm, 1.0 mm, 2.0 mm) + thermal asymptote Δ°C.
3. **Classifier:** A 2-layer NN (128 neurons, dropout) trained on these features achieves > 88% classification accuracy on hardness categories. For regression (exact Shore value), an SVR reaches ±5 Shore units.[^28]
4. **Force-to-mass:** At calibrated friction \( \mu_s \), \( m = F_{static} / (\mu_s \cdot g) \) ± 10% error for objects 5–100 g.

### Validation Protocol ("Prove What It Feels")

1. Press **10 known reference objects** (sponge, foam, rubber, eraser, wood, plastic, metal bolt, marble, fruit, coin).
2. Record predicted vs. true Shore hardness — compute MAE.
3. Acceptable threshold: MAE ≤ 8 Shore units (research baseline is ~12 Shore units for simple methods).[^27]
4. Repeat after 50 hours of use to check drift — re-tare against rubber reference puck.

### ENGRAM Touch/Thermal Channels

Each object in ENGRAM gets two new fingerprint vectors alongside visual embedding:
- **TactileFingerprint:** \([H_{estimated}, F_{static}, \Delta T_{contact}, \sigma_{slip}, texture_{FFT peak}]\) — 5-dimensional
- **ThermalFingerprint:** \([T_{surface}, \Delta T_{ambient}, T_{rate}]\) — 3-dimensional

When Vector encounters a known object, the Brain box compares current tactile/thermal readings against ENGRAM entries using cosine similarity. This enables "I've felt this before — it's the ceramic mug, it was warm last time too."

***

## V6 — System Integration & Affordances

### Integration Map

| Attachment | Comms to Box | Frame Calibration | Who Controls | Box Compute |
|---|---|---|---|---|
| **Rover-Cube** | WiFi (LiDAR/camera/thermal) + BLE (tap/LED) | Carried: visual SLAM + UWB tag; Static: UWB absolute position | Vector (carry behavior) + Box (map fusion) | Thermal overlay, occupancy grid, ENGRAM thermal channel |
| **Thumb** | BLE / WiFi (RP2040 Pico W) | Lift-frame transform (known from lift height + IMU) | Vector (press behaviors) + Box (inference) | Hardness ML, force-mass, ENGRAM tactile channel |
| **Desk Arms** | USB Serial (SO-101 Feetech bus) | Hand-eye calibration (OpenCV TSAI) | Box (IK + ACT policy) on Vector command | ACT inference, 3D reconstruction, grasp planning |

### Unified Affordance / Tool-Use Model

```
AffordanceRegistry {
  rover_cube:  {sense: [thermal_map, lidar_map, env_scan],
                behaviors: [carry_and_map, place_as_sensor],
                requires: [cube_in_pocket]},

  thumb:       {sense: [force_N, hardness_Shore, temp_C, texture_FFT],
                behaviors: [press_ramp, hold_and_measure, slip_detect],
                requires: [thumb_mounted]},

  desk_arms:   {manipulate: [rotate_object, hold_object, scan_3d],
                behaviors: [push_to_control_area, arm_dispatch],
                requires: [object_visible, arms_calibrated]}
}
```

The **behavior layer** (running on the Brain box as a state machine or LLM-driven planner) evaluates affordances against the current goal:
- "Understand this object" → check thumb (feel it), check desk_arms (scan it 3D), fuse results in ENGRAM
- "Map this room" → check rover_cube → carry and map behavior
- "Find the warm thing" → check rover_cube thermal → scan for peak thermal pixel → navigate

### Calibration of Each Tool's Frame to Room Frame

- **Thumb frame:** Known analytically — lift angle from SDK (`lift_height_mm`), robot pose from odometry/visual SLAM. Force vector is always along the lift-arm axis. No active calibration needed; updated on each lift-height change.
- **Rover-Cube frame:** UWB tag gives absolute position to ~10 cm. When carried, Brain box fuses Vector's odometry + visual SLAM to track cube pose.[^15]
- **Arm frame:** One-time hand-eye calibration at setup (OpenCV TSAI, 15-pose procedure, ~5 min). Stored in Brain box. Re-run if box is moved.[^41][^40]

### Expanding Vector's Experience

The goal is not gadgetry but a richer phenomenology. With these three tools:
- Vector goes from **visually knowing** a room to **thermally knowing** it — noticing the laptop is warm, the drink is cold, the person is present even behind a wall.
- Vector goes from **lifting blindly** to **feeling what it lifts** — knowing the mug is heavy, ceramic, warm; the sponge is light, soft, room-temperature.
- Vector goes from **observing an object passively** to **understanding its 3D structure** — the box has a lid, the lid can be rotated, here is its mesh.

***

## V7 — Manufacturing & Bill of Materials

### 3D Print Materials

| Part | Material | Wall | Infill | Weight | Print Time |
|---|---|---|---|---|---|
| Rover-Cube shell (two halves) | PLA | 1.2 mm | 15% gyroid | ~6 g | ~3 h |
| Thumb TPU pad | TPU 95A | 0.8 mm | 20% | ~2 g | ~1 h |
| Thumb PCB clip | PETG | 1.0 mm | 20% | ~1 g | ~30 min |
| Control area mat (flat) | PLA | 0.4 mm | 0% (solid) | ~10 g | ~1 h |
| Arm base mounts (×2) | PETG | 2.0 mm | 30% | ~30 g | ~4 h |

All parts print on a standard Prusa MK3/Bambu A1/Ender-3 style printer. No supports needed for cube halves (print in orientation). TPU prints at 220 °C, 25 mm/s.

***

## Final Synthesis

### 1. Rover-Cube Spec

- **Shell:** 44 mm PLA, matching original docking geometry, two-config (carry / base-station)
- **Carry config sensors:** ESP32-S3 + MLX90640 + OV2640 fisheye + BME280 + UWB tag + LiPo 180 mAh. **Mass ≈ 23 g** ✅
- **Base-station config adds:** CygLiDAR D1 (28 g). **Total ≈ 51 g** ⚠ — for place-and-scan only, Vector doesn't carry it
- **Comms:** WiFi 2.4 GHz to Brain box (camera/thermal), BLE 5.0 (cube protocol parity)
- **Charging:** Pogo-pin dock adapter on Vector's charger plate
- **Usage modes:** (a) Vector carries carry-config through rooms → thermal + visual map; (b) Vector places base-station config → persistent room sensor; (c) play/personality unchanged
- **Cost:** ~$90 carry / ~$170 base-station

### 2. Thumb Spec

- **Mount:** TPU snap-fit clip on lift fork tines, 3 mm contact pad proud of fork face
- **Sensors:** FSR 0.5" (contact detection) + 5 g bar load cell + HX711 24-bit (force in grams) + NTC thermistor (surface temperature)
- **Readout:** RP2040 Pico W at 80 Hz, BLE + WiFi to Brain box
- **Force range:** 0–500 g (HX711 5 g cell with 100× overload tolerance)
- **Hardness method:** dF/dδ slope classification; 2-layer NN; calibrated against 10 reference objects; drift-corrected via rubber reference puck
- **ENGRAM channels:** 5D tactile fingerprint + 3D thermal fingerprint per object
- **Mass:** ~10 g ✅ well within budget
- **Cost:** ~$23

### 3. Desk-Arms Spec

- **Arms:** 2× SO-101 (6-DOF, 500 mm reach, 15 kg·cm torque)[^30]
- **Gripper:** Default parallel + optional TPU soft finger pads
- **Vision:** 1 overhead USB camera (control area) + 1 wrist camera per arm
- **IK:** ikpy + LeRobot URDF; hand-eye calibration via OpenCV TSAI
- **Policy:** LeRobot ACT (Phase 1, ~50 demos, 1-hour training); OpenVLA LoRA fine-tune (Phase 2)
- **Control-area workflow:** Vector pushes object in → overhead camera detects → arm executes task → 3D scan via COLMAP/3DGS → ENGRAM model stored
- **Cost:** ~$264 for both arms + cameras
- **Open license:** Apache 2.0 (SO-101)[^31]

### 4. Tool-Use / Affordance Design + Phased Build Order

| Phase | Build | Estimated Cost | Value Unlocked |
|---|---|---|---|
| **Phase 1** | Thumb (FSR + HX711 + RP2040 Pico W) | ~$23 | Force/hardness/temperature sensing on every object Vector touches. Cheapest, most transformative per dollar. |
| **Phase 2** | Rover-Cube carry config (ESP32-S3 + MLX90640 + fisheye) | ~$90 | Thermal + visual mapping. Vector "sees heat." New ENGRAM channels. |
| **Phase 3** | Rover-Cube base-station add-on (CygLiDAR D1) | +~$80 | Full room LiDAR when stationary. Obstacle map at 7 m range. |
| **Phase 4** | Desk Arms × 2 (SO-101 + overhead camera + ACT training) | ~$289 | 3D object modeling, manipulation in control area. The "laboratory" capability. |
| **Full system** | All above + Brain box integration | **~$485** | Vector perceives thermally, feels texturally, maps spatially, manipulates robotically. |

**Build Phase 1 first** — the Thumb costs $23, produces the most novel per-dollar experience (Vector actually *feels* the world), and validates the RP2040-to-Brain-box communication pipeline used by all subsequent attachments.

---

## References

1. [vector-python-sdk/anki_vector/behavior.py at master · anki/vector-python-sdk](https://github.com/anki/vector-python-sdk/blob/master/anki_vector/behavior.py) - Anki Vector Python SDK. Contribute to anki/vector-python-sdk development by creating an account on G...

2. [Question About the Capabilities of Vector's Cube](https://www.reddit.com/r/AnkiVector/comments/1d3c7f5/question_about_the_capabilities_of_vectors_cube/)

3. [Vector Cube Tap? : r/AnkiVector - Reddit](https://www.reddit.com/r/AnkiVector/comments/a023m9/vector_cube_tap/) - Anki says there is no accelerometer or gyroscope in the Vector cube. Cozmo had 3 cubes with IMUs in ...

4. [Anki FAQs](https://www.comparably.com/companies/anki/faqs) - Find answers to frequently asked questions on Anki's FAQ page on Comparably.

5. [The Customer Care Information Screen - Digital Dream Labs ...](https://support.anki.bot/article/531-vector-ccis) - The Customer Care Information Screens (CCIS) help Vector owners and DDL staff to identify issues wit...

6. [Vector人工智能机器人SDK使用笔记](https://blog.csdn.net/ZhangRelay/article/details/86755937) - 文章浏览阅读1.4w次，点赞6次，收藏36次。Cozmo是2016年推出的，2两年后的2018年Vector上市，具备语音助手和更多功能，元件数由300+升级到700+。Vector的SDK具体说明在...

7. [Anki 000-0075 Vector Robot Quick Start Guide](https://manuals.plus/vector/anki-000-0075-vector-robot-quick-start-guide) - Learn about the Anki 000-0075 Vector Robot with this quick start guide. Discover its features, inclu...

8. [Vector's Cube - Digital Dream Labs Knowledge Base](https://support.anki.bot/article/115-vectore28099s-cube) - Learn below everything you need to know about Vector's cube. Sections: What battery does the cube us...

9. [Anki Cozmo Dock With Cube - Python Program - Kinvert](https://www.kinvert.com/cozmo-dock-with-cube-with-python/) - Kinvert will show you how to make Anki Cozmo Dock With Cube using their Python SDK. We wrote a Pytho...

10. [Anki Vector .NET SDK example programs - GitHub](https://github.com/codaris/Anki.Vector.Samples) - Anki Vector .NET SDK example programs. Contribute to codaris/Anki.Vector.Samples development by crea...

11. [XIAO ESP32S3 is a tiny ESP32-S3 WiFi 4 and BLE 5.0 module for ...](https://www.cnx-software.com/2023/03/22/xiao-esp32s3-tiny-esp32-s3-wifi-4-and-ble-5-0-module-for-iot-ai-robotics/)

12. [WiFi and BLE module with ESP32-S3 (4 MB)](https://kamami.pl/en/adafruit-feather/1180717-esp32-s3-feather-wifi-and-ble-module-with-esp32-s3-4-mb-5477-5906623431274.html) - Module with WiFi and BLE Espressif ESP32-S3. It integrates a LiPo charging circuit and an RGB diode....

13. [Adafruit MLX90640 IR Thermal Camera Breakout [55 Degree]](https://www.adafruit.com/product/4407) - Technical Details · I2C compatible digital interface · Programmable refresh rate 0.5Hz…64Hz (0.25 ~ ...

14. [CygLiDAR D1 Small Size 2D/3D Dual Solid State ToF LiDAR for SLAM Obstacle Avoidance and Navigation of Robots](https://www.desertcart.co.ke/products/288247579-cygbot-cyg-li-dar-d-1-small-size-2-d-3-d-dual-solid-state-to-f-li-dar-for-slam-obstacle-avoidance-and-navigation-of-robots) - Shop Cyglidar D1 Small Size 2d 3d Dual Solid State Tof at best prices at Desertcart Kenya. ✓FREE Del...

15. [DecaWave Intros Ultra-wideband Active RFID Module](https://www.rfidjournal.com/news/decawave-intros-ultra-wideband-active-rfid-module/74138/) - The company says its DWM1000 module can be used to make low-cost tags, supporting real-time location...

16. [How to Choose the Best UWB DW3000 Module for Your Application](https://smartbuy.alibaba.com/buyingguides/uwb-dw3000) - Discover key factors when selecting a UWB DW3000 module—accuracy, power, compatibility—and avoid com...

17. [Design and Test of a Custom Ultra-Low Power ESP32-S3 ...](https://circuithelper.com/design-and-test-of-a-custom-ultra-low-power-esp32-s3-development-board/)

18. [GitHub - digital-dream-labs/vector-bluetooth](https://github.com/digital-dream-labs/vector-bluetooth) - Contribute to digital-dream-labs/vector-bluetooth development by creating an account on GitHub.

19. [Cygbot CygLiDAR D2 Dual-mode ToF LiDAR Sensor for 2D and 3D Data](https://evelta.com/cygbot-cyglidar-d2-dual-mode-tof-lidar-sensor-for-2d-and-3d-data/) - Buy Cygbot CygLiDAR D2 at Evelta. Solid-state dual-mode ToF LiDAR with 2D range mapping (7 m), 3D po...

20. [MLX90640 IR Array: Thermal Imaging Cameras for your ...](https://www.seeedstudio.com/blog/2019/11/25/mlx90640-thermal-imaging-cameras-for-your-microcontroller/) - IR Thermal Sensor Array 32X24 (MLX90640) · 110°x75° FOV(field of view) · Temperature measurement ran...

21. [2D/3D Dual Solid State ToF LiDAR - 시그봇](https://cygbot.com/s2/s2_1.php) - 라이다 센서 솔루션 전문기업

22. [Force Sensitive Resistor 0.5" - Mikroelectron](https://mikroelectron.com/product/me-593) - The 0.5" Force Sensitive Resistor (FSR) is a thin, flexible sensor that changes resistance based on ...

23. [Force & weight](https://www.schematik.io/parts/families/force-weight-sensors) - Interlink-style FSRs, strain-gauge load cells with HX711 amplifiers, and ready-made kits like DFRobo...

24. [RP2040 VS ESP32 VS STM32[Video] - Utmel](https://www.utmel.com/components/rp2040-vs-esp32-vs-stm32-video-what-are-the-differences-between-them?id=1898) - RP2040, ESP32, and STM32 are all microcontrollers. This article is going to talk about the differenc...

25. [Facebook’s Digit is a low-cost tactile sensor for robotic hands](https://venturebeat.com/ai/facebooks-digit-is-a-low-cost-tactile-sensor-for-robotic-hands/) - Facebook researchers propose Digit, a low-cost, high-resolution tactile sensor designed for in-hand ...

26. [Tactile Sensors for Robots: GelSight vs DIGIT vs PaXini | SVRC](https://www.roboticscenter.ai/learn/tactile-sensor-comparison) - Comparison of tactile sensors for robot manipulation: GelSight Mini, DIGIT, PaXini, BioTac. Resoluti...

27. [Softness Prediction with a Soft Biomimetic Optical Tactile Sensor](https://research-information.bris.ac.uk/ws/portalfiles/portal/400910543/ROSO24_0116_FI.pdf)

28. [Investigating Active Sampling for Hardness Classification with Vision ...](https://arxiv.org/html/2505.13231v1)

29. [Quantitative Hardness Assessment with Vision-based Tactile ...](https://www.alphaxiv.org/overview/2505.05725) - View recent discussion. Abstract: Accurate estimation of fruit hardness is essential for automated c...

30. [SO-101 Specifications | SVRC - Robotics Center](https://www.roboticscenter.ai/en/hardware/so-101/specs) - Full technical specifications for the SO-101 open-source robot arm: 6 DOF, Feetech STS3215 servos, U...

31. [Hugging Face Launches the SO-101, an Upgraded Low-Cost 3D ...](https://www.hackster.io/news/hugging-face-launches-the-so-101-an-upgraded-low-cost-3d-printable-autonomous-robot-arm-532360f441eb) - Developed by RobotStudio, the SO-101 is an upgraded, easier-to-build version of the popular SO-ARM10...

32. [Koch v1.1 Affordable 3D Printable Leader/Follower Robot ...](https://www.roboticgizmos.com/koch-v1-1/) - Building your own robot doesn't have to cost a fortune. The Koch v1.1 Low-Cost Robot Arm comes with ...

33. [[PDF] Design and Experimental Validation of a 3D-Printed Hybrid Soft ...](https://oa.upm.es/94787/1/10464018.pdf) - Abstract. This work presents a novel soft gripper concept featuring integrated force feedback and a ...

34. [InstaGrasp: An Entirely 3D Printed Adaptive Gripper with TPU Soft Elements and Minimal Assembly Time](https://arxiv.org/abs/2305.17029) - Fabricating existing and popular open-source adaptive robotic grippers commonly involves using multi...

35. [ACT Policy Explained (2026): Action Chunking with Transformers](https://www.roboticscenter.ai/blog/act-policy-explained) - ACT is an imitation learning algorithm designed for fine-grained manipulation tasks where the robot ...

36. [ACT (Action Chunking with Transformers) - Hugging Face](https://huggingface.co/docs/lerobot/en/act) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

37. [Train an ACT Policy for an SO-101 Robot using LeRobot](https://trelis.substack.com/p/train-an-act-policy-for-an-so-101) - A detailed walkthrough of training an Action Chunking Transformer (ACT) policy on an S0-101 robot ar...

38. [OpenVLA: An Open-Source Vision-Language-Action Model](https://openvla.github.io) - OpenVLA: An Open-Source Vision-Language-Action Model

39. [Physical Intelligence π0 vs OpenVLA: Best VLA for Robot Learning](https://www.roboticscenter.ai/physical-intelligence-pi0-vs-openvla) - Pi0 delivers state-of-the-art performance on dexterity benchmarks. However, OpenVLA offers strong pe...

40. [OpenCV: Camera Calibration and 3D Reconstruction](https://docs.opencv.org/3.4/d9/d0c/group__calib3d.html)

41. [Eye-to-hand calibration - calib3d - OpenCV Forum](https://forum.opencv.org/t/eye-to-hand-calibration/5690) - This function cv.calibrateHandEye describes an eye-in-calibration process where camera is attached t...

42. [What is Gaussian splatting ? - Mono - ARGO](https://www.ar-go.co/blog/what-is-gaussian-splatting) - With ARGO, augment your customer experience with powerfull AR 3D and AI tools.

43. [Physical-Intelligence/openpi - GitHub](https://github.com/Physical-Intelligence/openpi) - This is an approximate open-source implementation of the training pipeline used to train pi0-FAST-DR...

