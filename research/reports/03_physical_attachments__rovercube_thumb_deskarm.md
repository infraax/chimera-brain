# Anki Vector Augmentation: Rover-Cube, Tactile “Thumb,” and Desk-Arm Manipulation System

## TL;DR

- **Feasible, but governed by one hard, unpublished number.** Vector’s lift travels only 32→92 mm (~60 mm) and is rated qualitatively to handle “no more than its own cube” (~44 mm cube). The safe design budget for anything Vector *lifts/carries* is ≈30–40 g (pending empirical measurement); anything it *pushes* across the floor can be heavier. Offload all heavy compute to a Raspberry Pi-class “Brain box,” and reuse the existing cube BLE protocol as the comms template.
- **Highest value-per-gram payloads:** for the Rover-Cube, an MLX90640 thermal array + VL53L5CX solid-state ToF + BME688 environmental sensor on an ESP32-S3 Feather with a small LiPo; for the Thumb, a barometric/MEMS “force pad” + thermistor (lightest) or a 9DTact optical-tactile fingertip (richest); for manipulation, two SO-101 arms running LeRobot policies.
- **Build cheapest-highest-value first:** measure the true payload, then build the ~$25–40 Thumb, then the Rover-Cube pod, then the two desk arms, then unify everything into a shared world-model with touch/thermal ENGRAM channels.

## Key Findings

1. **Vector’s mechanical envelope is tight and well-documented except for payload.** Confirmed via the Vector SDK and Technical Reference Manual (Randall Maas): lift min 32.00 mm / max 92.00 mm (~60 mm travel), 66 mm lift arm, 45 mm pivot; brushed DC motor on a DMC2038LVT H-bridge with a dual-channel optical encoder, driven by an STM32F030C8T6 body-board MCU; ~2 A peak motor current, ~5 A over-current cutoff, and a 15 s stall burn-out limit. **Lift payload in grams, cube mass, gear ratio, and torque are not published anywhere** — the single biggest open question.
1. **The cube BLE stack is an extensible template.** The Light Cube uses a Dialog DA14580 BLE SoC and exposes (per TRM Ch.14, pp.126–129) accelerometer streaming, tap/move detection, 4 RGB LED control, and a combined battery-voltage/accelerometer characteristic — exactly the hooks needed to extend into a sensor pod. (Note: the cube runs on a **1.5 V cylindrical N/E90/LR1 cell, not a coin cell.**)
1. **Open tactile hardware spans the full cost/fidelity range:** barometric-rubber and FSR/load-cell DIY paths (a few dollars), 9DTact (~$50 DIY, open hardware+software, 3D shape + 6D force), DIGIT ($350), and the GelSight Mini ($499 system, $49 replacement gels).
1. **The SO-101 arm is genuinely buildable and fully open** (~$100–130 in parts, ~$220 Seeed kit + ~$35 prints) with a complete software stack (Hugging Face LeRobot: ACT, Diffusion, VQ-BeT, SmolVLA, Pi0/Pi0-Fast; plus OpenVLA) and standard OpenCV hand-eye calibration.

## Details

### V1 — Lift & payload reality

RECOMMENDATION: Treat Vector’s lift as a ~60 mm-travel hook that safely manipulates a single ~44 mm cube. Design every carried attachment to the mass and footprint of the original Light Cube, and **confirm true payload empirically before committing electronics.** Reuse the cube BLE protocol (accelerometer stream + LED control + battery characteristic) as the comms template, extending it with new sensor characteristics or, where bandwidth demands, a parallel ESP32 BLE/Wi-Fi link.
HARDWARE: Lift min 32.00 mm / max 92.00 mm (~60 mm travel) — confirmed via the Vector Python SDK `behavior` constants; lift arm length 66.0 mm, pivot height 45.0 mm (from the Cozmo SDK; Vector reuses the design); brushed DC motor on a DMC2038LVT H-bridge with a dual-channel optical photo-interrupter encoder, driven by the STM32F030C8T6 body-board MCU; ~2 A peak current on a lift-flip, ~5 A over-current cutoff, 15 s stall burn-out limit; Vector itself ~170 g (review figure, not an Anki spec) on a 3.7 V 320 mAh Li-ion. Light Cube ~44 mm/side, 1.5 V N/E90/LR1 cell, Dialog DA14580 BLE SoC, 4 RGB LEDs, an (unnamed) accelerometer.
SOFTWARE: `anki/vector-python-sdk` (Apache-2.0) — `set_lift_height`, `dock_with_cube`, cube connect / LED / accelerometer-and-tap events; `kercre123/victor` + `kercre123/wire-pod` (open) for the on-robot engine and a local server. The Brain box runs the Python SDK against wire-pod.
DESIGN: Anything Vector lifts mounts on a printed shell matching the cube’s lift-hook geometry (the corner holes the lift arm engages) and ~44 mm footprint; the attachment’s frame origin is the cube marker pose, which Vector already localizes for navigation.
HOW VECTOR USES IT: Vector docks and picks up the attachment exactly as it docks the cube; the Brain box reads it over BLE and commands Vector through wire-pod. Affordance: *“this is my cube → I can carry it and set it down.”*
ANKI-GRADE: Mirror Anki’s encoder-feedback motor control and burn-out protection; self-calibrate the lift against known heights; never command stalls >15 s.
WEIGHT/POWER/COST: design budget ≈30–40 g carried; CONFIDENCE **high** on geometry/electronics, **low** on payload grams. **Open question: exact lift payload and cube mass — must be weighed on a scale and load-tested.**

### V2 — The Rover-Cube sensor payload

RECOMMENDATION: Rebuild the cube as a self-powered sensor pod on an ESP32-S3 (BLE + Wi-Fi) carrying a thermal array, a solid-state ToF depth sensor, and environmental sensors — the modalities Vector most lacks — while preserving cube play (keep RGB LEDs + accelerometer + tap). Stream light data over BLE and bulk frames (thermal/depth) over Wi-Fi to the Brain box, which fuses them into the home map. Power from a small LiPo charged off Vector’s charger contacts or the pod’s own USB-C.
HARDWARE (ranked by value × weight × power × cost):

- **MCU/comms:** Adafruit ESP32-S3 Feather (~$18, board 52×23×7 mm, BLE+Wi-Fi, MAX17048 fuel gauge, LiPo charging, STEMMA QT; ~100 µA deep-sleep) — open.
- **Thermal (top pick):** MLX90640 32×24 IR array, I2C, ~$60, **±2 °C accuracy in the 0–100 °C range**, **16 Hz max frame rate**, available in **110°×70°** (wide) or **55°×35°** (narrow) FOV versions (Adafruit #4469/#4407, Pimoroni, SparkFun Qwiic); breakout ~19×18×10 mm — open. Finds people/pets/warm appliances.
- **Depth/obstacle:** ST VL53L5CX 8×8 multizone ToF (~4 m, ~$20) gives a light, low-power solid-state depth field. A full RPLiDAR (A1 ~$100; C1 110 g, IP54) is too heavy/power-hungry to carry — reserve LiDAR for a stationary room-scan mode only.
- **Environmental:** Bosch BME688 (temp/humidity/pressure/VOC gas) ~$20; ambient light from the same module.
- **Optional UWB tag:** Qorvo DW3000 (10 cm ranging, FiRa-compliant, very low power ~3.3 µA/ms beacon; modules from ~$15.50, ESP32-UWB combos ~$54.80) for room-frame positioning.
- **IMU + mic:** ESP32-S3 + an I2S MEMS mic (~$5).
- **Power:** 250–400 mAh LiPo (~6–9 g).
  SOFTWARE: ESP-IDF/Arduino (open) on the pod; on the Brain box, the Pimoroni/SparkFun MLX90640 drivers, the ST VL53L5CX driver, and an occupancy/thermal map builder fusing thermal + depth into a 2.5D map.
  DESIGN: Print a PETG shell at the cube’s ~44 mm footprint (or a slightly taller “pod”), preserving the lift-hook corner geometry; sensors face outward on the top/sides; LiPo + ESP32-S3 stacked inside; charging pads on the bottom matching Vector’s charger, or a side USB-C jack.
  HOW VECTOR USES IT: Vector carries the pod through rooms (“Google-Maps-car” mode) building a thermal/obstacle map, or sets it down as a remote room sensor. Affordance: *“my cube can now see heat and depth.”*
  ANKI-GRADE: Per-pixel thermal flat-field (FFC) calibration, ToF cross-talk/ambient calibration, drift-corrected gas baseline; the pod reports sensor health to the Brain box.
  WEIGHT/POWER/COST: ~30–45 g total, ~$130–160 BOM, hours of runtime on 400 mAh. CONFIDENCE **medium-high**. Open question: whether total mass stays within Vector’s true carry limit (ties to V1).

### V3 — The Thumb tactile finger

RECOMMENDATION: Build an ultra-light printed cap that clips onto Vector’s lift arm and adds force + temperature sensing. For the lightest/cheapest “feel,” use a barometric-MEMS force pad (a sealed barometer under a cast silicone/TPU dome) plus a thermistor; for richer contact geometry and true multi-axis force, use a 9DTact optical fingertip read by a tiny camera on the Brain box. The Thumb computes force-to-move (→ mass/friction), hardness (force vs. deformation), texture/slip, and temperature.
HARDWARE:

- **Light path:** NXP MPL115A2 barometer (~$13, 5×3×1.2 mm LGA, I2C, ±1 kPa, 5 µA active / 1 µA shutdown) or a BMP280-class sensor sealed under silicone as a DIY force cell; NTC thermistor (~$1); read by the Thumb’s ESP32-S3 or a tiny RP2040.
- **Quant path:** a thin bar/disc load cell + HX711 24-bit ADC for calibrated newtons; with proper calibration and stable mounting, a load-cell+HX711 scale reaches ~0.1% of capacity (≈±5 g on a 5 kg cell), versus ±10–25% for raw FSRs.
- **Rich path:** 9DTact (open hardware + software, ~$50 DIY, translucent gel + small camera → 3D shape reconstruction and generalizable 6D force from a NN trained on ~100k image-force pairs). DIGIT ($350, $40 gels) and the GelSight Mini ($499 system, $49 replacement gels) are higher-fidelity commercial options.
  SOFTWARE: `linchangyi1/9DTact` (open — shape + 6D force); `facebookresearch/sparsh` (self-supervised touch representations); GelSight `gsrobotics` SDK + `digit.ml` driver; `linchangyi1/Awesome-Touch` (curation hub); HX711 libraries (bogde / Olav Kallhovd `HX711_ADC`); **3D Cal** (arXiv 2511.03078), an open Python library that repurposes an FDM 3D printer to auto-calibrate vision-based tactile sensors (DIGIT, GelSight Mini).
  DESIGN: Print the finger cap in PLA with a TPU 95A contact pad (TPU prints support-free); embed the barometer/thermistor under the pad; clip onto the 66 mm lift arm; frame = lift-arm tip pose. For the optical path, mount the gel pad on the cap with a micro camera viewing it.
  HOW VECTOR USES IT: Active “touching reality” loop — press with increasing lift force, watch the sensor response, build a tactile model, classify hard/soft, and estimate mass/friction; the Brain box runs inference and commands Vector’s lift/wheels. Affordance: *“I can press on things and feel back.”*
  ANKI-GRADE: Calibrate against known reference objects (durometer foams, known weights), tare/zero each session, temperature-compensate the barometer/load cell (both drift with temperature), and self-correct drift over time — the motor-noise-nullification ethos applied to touch.
  WEIGHT/POWER/COST: cap+sensor ~5–12 g; ~$15 (baro+thermistor) → ~$50 (9DTact) → $350+ (DIGIT/GelSight). CONFIDENCE **high** on approach. Open question: achievable force resolution in newtons at <10 g mount mass.

### V4 — The two desk arms

RECOMMENDATION: Mount two SO-101 follower arms on top of the Brain box flanking a defined “control area.” Vector pushes/carries an object into the control area; an overhead camera localizes it (hand-eye calibrated to the arm base frame); the arms rotate/hold/open it — e.g., spin a box in a turntable grasp so the overhead camera builds a 3D model — so Vector doesn’t have to drive around the object. Use LeRobot for teleop data + ACT/SmolVLA policies, with scripted IK for simple pose moves.
HARDWARE: **SO-101** (TheRobotStudio × Hugging Face), 6-DOF, Feetech **STS3215** bus servos with 360° magnetic encoders. The officially-recommended C001 servo is rated **19.5 kg·cm stall torque @ 7.4 V** (1:345 gear, ~5 kg·cm rated); the 12 V C018 variant is **30 kg·cm @ 12 V / 19 kg·cm @ 7.4 V**, 0.222 s/60°, ~55 g each. Cost ~$100–130 in parts / ~$220 Seeed kit + ~$35 printed parts; open (Apache-2.0). Grippers: stock parallel jaw; print a **TPU 95A compliant finger** for better/safer grasp; add a touch-sensing fingertip (V3) for force feedback. Overhead camera: any 720p+ USB webcam.
SOFTWARE: `huggingface/lerobot` (open) — teleoperation, dataset creation, and policies (ACT, Diffusion, VQ-BeT, SmolVLA, Pi0/Pi0-Fast); `openvla/openvla` (MIT) for language-conditioned tasks; OpenCV `calibrateHandEye` for eye-to-hand calibration; `gsplat` (Apache-2.0) / COLMAP / SuperSplat (MIT) for 3D / Gaussian-splat reconstruction from the rotated views. A few dozen teleop episodes suffice to train ACT to reproduce a demonstrated manipulation.
DESIGN: Arms bolt to the Brain box lid; the control area is a marked mat with an ArUco/checkerboard origin; the overhead camera sits on a printed gantry. Frame chain: room ↔ arm base (hand-eye) ↔ Vector (via the cube marker / shared fiducials).
HOW VECTOR USES IT: Vector recognizes the control-area fiducial, delivers the object, and signals the Brain box; the arms execute a learned/scripted manipulation and return pose/scan data. Tool-use model: *“I have arms over there; I bring things to them.”*
ANKI-GRADE: Re-run hand-eye calibration periodically; verify grasps with the fingertip force sensor; the magnetic encoders give repeatable poses, reducing training noise.
WEIGHT/POWER/COST: arms are stationary (weight is not Vector’s concern); ~$300–550 for two arms + cameras; a 12 V 5 A+ supply if using the high-torque servos. CONFIDENCE **high**. Open question: reliability of learned policies on novel objects vs. scripted IK.

### V5 — Tactile & manipulation software/datasets

RECOMMENDATION: Standardize on vision-based tactile (9DTact / DIGIT) + LeRobot, and turn raw force/deformation into reliable “hard/soft, weighs X, needs Y N” outputs via supervised calibration against known objects, validated by press-test error metrics. Add touch and thermal as new ENGRAM fingerprint channels so Vector remembers how objects feel and how warm they are.
SOFTWARE: `facebookresearch/sparsh` (self-supervised touch reps, pretrained on Touch-and-Go / ObjectFolder-Real); `linchangyi1/9DTact` (6D force + shape); `gelsightinc/gsrobotics` + `digit.ml` SDK; `linchangyi1/Awesome-Touch` (dataset hub); **Touch100k** and **TAG** datasets (material / hard-soft / rough-smooth classification subtasks);  `huggingface/lerobot` (policies). For context on achievable accuracy: research triaxial-tactile frameworks report ~99% roughness and ~98.8% hardness classification, and a tactile-glove graph-attention network reports ~89.6% object classification  — strong but from richer sensor arrays than a single fingertip.
VALIDATION: Press a panel of reference objects (durometer-rated foams, known-mass weights, textured plates); measure force-estimate error against a load-cell ground truth, hardness-classification accuracy, and mass-estimate error; recalibrate whenever error exceeds a set threshold.
ENGRAM CHANNEL DESIGN: add per-object channels {peak_force_to_move, compliance/hardness, surface_texture_signature, temperature}; these touch/thermal fingerprints fuse with the visual ID for robust recognition and persistent memory of “how a thing feels.”
CONFIDENCE: **high** on the stack; **medium** on absolute mass/friction accuracy from one lightweight fingertip.

### V6 — System integration & affordances

RECOMMENDATION: Run a single world-model on the Brain box that registers every tool into a shared room frame and gives Vector an explicit affordance/tool-use model. The Brain box is the hub: it talks BLE/Wi-Fi to the Rover-Cube and Thumb, commands the arms over USB, and commands Vector via wire-pod/SDK; each tool’s frame is calibrated to the room frame; a behavior layer decides which tool to use when.
INTEGRATION MAP (attachment × comms × frame × who-controls × box-compute):

- **Rover-Cube** — BLE (light data) + Wi-Fi (frames) — frame = cube marker pose — controlled by Brain box, carried by Vector — compute: thermal/depth map fusion on the Pi.
- **Thumb** — I2C → ESP32/RP2040 → BLE (or camera → USB for 9DTact) — frame = lift-arm tip — Vector’s lift acts under Brain-box inference — compute: tactile inference on the Pi.
- **Arms** — USB serial to Brain box — frame = arm base via hand-eye calibration — controlled by Brain box — compute: IK + learned policies on the Pi.
- **Vector** — wire-pod/SDK over Wi-Fi — frame = robot pose / cube — self + Brain box — compute: engine on the robot, high-level reasoning on the Pi.
  AFFORDANCE/TOOL-USE: L2 perception gains thermal/depth/touch modalities; the 3D home map ingests Rover-Cube scans and arm-reconstructed object models; ENGRAM gains touch/thermal channels; tool-use behaviors are explicit — *“map a room”* (carry the pod), *“understand this object”* (deliver to the arms), *“feel this”* (press with the Thumb).
  CONFIDENCE: **high** conceptually; the main risk is integration effort, not feasibility.

### V7 — Manufacturing & BOM

RECOMMENDATION: Print structural shells in PETG (durability/heat resistance) and contact pads in TPU 95A; use PLA for non-structural jigs and arm parts. Standardize on ESP32-S3 for self-powered attachments and RP2040 where only simple sensing is needed. All parts are hobby-printer-friendly and off-the-shelf.
PER-ATTACHMENT BOM (approximate):

- **Rover-Cube:** ESP32-S3 Feather $18 / MLX90640 $60 / VL53L5CX $20 / BME688 $20 / 400 mAh LiPo $8 / ~10 g PETG shell. **~$130–160, ~30–45 g, ~3–5 h print.**
- **Thumb (light path):** RP2040 or ESP32-S3 $6–18 / MPL115A2 $13 / NTC thermistor $1 / TPU 95A pad. **~$25–40, ~5–12 g, ~1–2 h print.** (9DTact variant: +~$50 and a micro camera.)
- **Desk arms:** 2× SO-101 (~$220 kit each, or ~$100–130 parts) + ~$35 prints each + 2 USB webcams ~$40 + 12 V 5 A+ supply. **~$300–550 total, ~12–20 h print for both arms.**
  DESIGN FILES TO FORK: `TheRobotStudio/SO-ARM100` (arm, compliant TPU gripper, camera mounts, BOM under Apache-2.0), `linchangyi1/9DTact` (tactile hardware + software), Adafruit/Pimoroni sensor-mount STLs, `kercre123/wire-pod` (server).
  CONFIDENCE: **high**.

## Recommendations

1. **Phase 0 — measure the truth (week 1).** Weigh the cube and find Vector’s real payload by incrementally loading a printed cube shell until docking/lift fails or stalls. This single number gates the Rover-Cube and Thumb electronics budgets and is the most important deliverable of the whole project.
1. **Phase 1 — cheapest, highest value: the Thumb (light path).** ~$25–40 in parts; immediately multiplies what the lift can do (force, hardness, temperature). Validate against reference objects with a load-cell ground truth.
1. **Phase 2 — Rover-Cube sensor pod.** Add thermal + ToF + environmental sensing; build the carry-and-map (“Google-Maps-car”) behavior. Confirm total mass against the Phase-0 limit before finalizing the LiPo size.
1. **Phase 3 — desk arms.** Two SO-101s + an overhead camera + LeRobot; start with scripted IK + OpenCV hand-eye calibration, then graduate to ACT/SmolVLA once you have teleop data.
1. **Phase 4 — integration & ENGRAM.** Unify all tool frames into the room frame, add touch/thermal fingerprint channels to ENGRAM, and ship the tool-use behavior layer.

**Thresholds that change the plan:** if measured carry payload is <20 g, demote the Rover-Cube to a tethered/stationary room sensor rather than a carried pod; if learned policies underperform scripted IK on grasp success in bench tests, keep IK for production manipulation and use policies only for exploratory tasks; if the light-path force pad can’t resolve <0.5 N reliably, step up to the load-cell+HX711 or 9DTact path.

## Caveats

- **Vector’s payload in grams, the cube’s mass, the lift gear ratio, and lift torque are not published anywhere** — confirmed absent from the TRM, SDK, and teardowns. These are the most load-bearing assumptions in the design; treat all carried-mass figures as estimates until physically measured.
- The cube runs on a **1.5 V cylindrical N/E90/LR1 cell, not a coin cell** — correct any BOM or charging design that assumes a CR2032. (The TRM warns a same-size 12 V A23 will destroy the cube.)
- **Vector’s overall dimensions/weight (~170 g) come from product reviews and the quick-start guide (model 000-0075), not an official mass spec.** Anki’s published specs cite size (~3.9 in tall × 4.7 in wide, including base), a 184×96 IPS display, and a 1.2 GHz quad-core Qualcomm SoC, but omit mass in grams.
- The lift arm length (66 mm) and pivot height (45 mm) are inherited from the Cozmo SDK; Vector’s own published lift constants are only the 32 mm / 92 mm height limits.
- Commercial tactile-sensor and arm-kit prices fluctuate (and the GelSight Mini/DIGIT require licenses/gels) — verify current pricing before purchase.
- Several tactile-classification accuracies cited (98–99%) are from research setups with richer sensor arrays and may not transfer directly to a single lightweight fingertip on Vector — validate on-platform.
- Deploying custom firmware/SDK control assumes an unlocked (OSKR) bot or wire-pod setup; a stock retail Vector has limited lift/dock control via the SDK.