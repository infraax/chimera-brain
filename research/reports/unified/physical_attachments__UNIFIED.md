# UNIFIED — Physical Attachments: Rover-Cube · The Thumb · Desk-Arms
## Giving Vector new ways to sense, touch & manipulate — the Anki way
### Source geodesic: `research/PHYSICAL_ATTACHMENTS_GEODESIC.md`

> **Fusion of the two independent research runs**, nothing dropped:
> - **[C] = Claude** — file `06_physical_attachments__rovercube_thumb_deskarm.md` ("Anki Vector
>   Augmentation"). TL;DR / Key-Findings / Caveats + geodesic V1–V7 (RECOMMENDATION/HARDWARE/SOFTWARE/
>   DESIGN/HOW-VECTOR-USES-IT/ANKI-GRADE/WEIGHT). Sources **inline** (TRM, SDK, arXiv, repos).
> - **[P] = Perplexity** — file `05_physical_attachments__expanded_senses.md` ("Expanded Senses
>   Design"). Executive Summary + V1–V7 with hardware tables, math, JSON affordance registry, **43
>   numbered references** (`[P^n]`, preserved at bottom).
>
> Tags: **[Both]** · **[C-only]** / **[P-only]** · **⚖️ DIVERGENCE**.

---

## 0. HEADLINE: same three attachments, one factual conflict, one discipline gap

Both reports independently design **the same three attachments** and converge on almost every part
choice. They differ on **one hard fact** (is the cube's accelerometer streamable over BLE?), on **how
conservative the payload budget should be**, and on the **primary Thumb force sensor**. Claude is the
more rigorous on the *unknowns* (it makes "measure the payload first" the #1 deliverable and pulls the
low-level mechanicals from the TRM); Perplexity is the more complete on *buildable specifics* (full
BOMs, the affordance-registry JSON, ENGRAM channel dimensions).

### What both independently conclude
- **Three attachments:** (1) **Rover-Cube** sensor pod, (2) the **Thumb** tactile lift attachment,
  (3) **Desk-Arms** manipulation station. All open-source, hobby-FDM-printable, maker-priced; **all
  heavy compute on the Brain box.**
- **Lift envelope [Both, exact agreement]:** `MIN_LIFT_HEIGHT_MM = 32.0`, `MAX = 92.0` (~60 mm travel);
  controls `set_lift_height()` / `set_lift_motor()`; angle −15° → +45°; lift arm 66 mm, pivot 45 mm
  (inherited from the Cozmo SDK). Payload rated qualitatively "**no more than one cube**" (~44 mm).
- **Reuse the cube BLE protocol** as the comms template; extend it with new sensor characteristics or a
  parallel ESP32 BLE/WiFi link for bandwidth. Cube runs a **1.5 V cylindrical N / E90 / LR1 cell**
  (NOT a coin cell) — both correct this explicitly.
- **Rover-Cube payload [Both]:** ESP32-S3 + **MLX90640 thermal** (#1 value) + **VL53L5CX 8×8 ToF**
  (carry-weight) + environmental sensor + small LiPo; preserve cube play (LEDs/tap). Two configs:
  light "carry" (~23–30 g) vs heavier "base-station" (adds bigger LiDAR). Pogo-pin charging off the dock.
- **Thumb [Both]:** ultra-light printed clip on the lift fork; **force + temperature + hardness**
  sensing; **9DTact-style optical tactile** as the rich option; an **active "touching-reality" loop**
  (press with increasing force, watch response, build a tactile model) with **drift-correction against
  a known reference object** (Anki's motor-noise-nullification ethos applied to touch).
- **Desk-Arms [Both]:** two **SO-101** arms (6-DOF, Feetech STS3215 servos, Apache-2.0, ~$220 kit /
  ~$100–130 parts) flanking a marked **control area**; overhead camera; **LeRobot ACT** (~50 demos) /
  OpenVLA for policies, scripted IK for simple moves; **OpenCV `calibrateHandEye`** hand-eye
  calibration; rotate object → **COLMAP / Gaussian-splat** 3D scan. Vector pushes objects in;
  **Vector stays in command** (arms are tools, not autonomous agents).
- **ENGRAM gets touch + thermal channels [Both]:** per-object tactile + thermal fingerprints fused with
  the visual ID ("I've felt this before — the ceramic mug, warm again").
- **Build cheapest-highest-value first [Both]:** the **Thumb (~$25)** is Phase 1 — most novel experience
  per dollar, and it validates the MCU→box comms pipeline reused by everything else.

### ⚖️ The real differences

| Topic | **[C] Claude** | **[P] Perplexity** | Our read |
|---|---|---|---|
| **Cube accelerometer over BLE** | **Exposes accelerometer *streaming*** (TRM Ch.14 pp.126–129, Dialog DA14580 SoC) | **NO raw accelerometer stream** over BLE/SDK — `is_moving` is derived, raw values not accessible | **Both can be true at different layers:** the cube *has* an accelerometer; the **BLE protocol (TRM) can stream it [C]**, but the **Python SDK does not surface it [P]**. For a custom build via wire-pod we'd target the BLE layer — so the raw stream is likely reachable. Verify on hardware. |
| **Carried-payload budget** | **≈30–40 g, conservative** — and makes "**weigh it empirically (Phase 0)**" the #1 deliverable; threshold: <20 g → demote Rover-Cube to tethered/stationary | **45 g max / 35 g target** (cube ~49 g; 40–55 g range) | **Claude's discipline wins:** payload/cube-mass/gear-ratio/torque are **unpublished** (absent from TRM, SDK, teardowns). **Measure before buying electronics.** Use ~35 g as a working target, confirm by load-test. |
| **Primary Thumb force sensor** | **Barometric-MEMS pad** (MPL115A2/BMP280 sealed under silicone, lightest) **or load-cell+HX711** (±5 g vs FSR's ±10–25%); 9DTact for rich | **FSR + HX711 hybrid** (FSR=contact, load-cell=force) Phase 1; DIGIT-style optical Phase 2 | **Claude is more accurate** on sensing: raw FSRs are imprecise (±10–25%); prefer **barometric-rubber or a calibrated load cell** for real newtons. Use FSR only for fast contact detection. |

### Coverage difference
- **[C-only]:** low-level mechanicals from the **TRM (Randall Maas)** — brushed DC lift motor on a
  **DMC2038LVT H-bridge**, dual-channel optical encoder, **STM32F030C8T6** body MCU, **~2 A peak /
  ~5 A over-current cutoff / 15 s stall burn-out**; cube **Dialog DA14580** SoC; the **barometric-rubber
  force trick**; **3D Cal** (arXiv:2511.03078 — repurposes an FDM printer to auto-calibrate tactile
  sensors); **facebookresearch/sparsh** (self-supervised touch reps), **Touch100k / TAG** datasets;
  **C001 (19.5 kg·cm @7.4 V, 1:345) / C018 (30 kg·cm @12 V)** servo specs; the **OSKR / wire-pod**
  caveat (stock retail Vector has limited lift/dock SDK control); the A23-destroys-the-cube warning;
  explicit **Phase-0 measurement protocol** + decision thresholds.
- **[P-only]:** full per-attachment **hardware tables w/ weights & costs**; **CygLiDAR D1/D2** as the
  base-station LiDAR; **BMI270 IMU** + **UWB DWM1000** in the cube payload; **sensor value ranking
  table**; the explicit **affordance-registry JSON**; **ENGRAM TactileFingerprint (5D) / ThermalFingerprint
  (3D)** dimensions; the 6-step "touching-reality" press protocol; the friction/hardness math
  (Fs = μs·m·g, H ≈ dF/dδ); **tactile-learning (BRL)**; full phased cost roll-up (~$485).

---

## V1 — Lift & payload reality

**[Both]** Lift 32–92 mm (~60 mm travel), arm 66 mm, pivot 45 mm; `set_lift_height`/`set_lift_motor`;
angle −15°→+45°; payload "no more than one cube." Vector body ~159 g [P] / ~170 g [C] (review figures,
not an official spec). Cube ~44 mm, **1.5 V N/E90/LR1 cell** (not coin) [Both].
- **[C-only] mechanicals (TRM):** brushed DC motor on **DMC2038LVT H-bridge**, dual optical encoder,
  **STM32F030C8T6** body MCU; **~2 A peak, ~5 A cutoff, 15 s stall burn-out**. Cube SoC **Dialog DA14580**.
- **⚖️ Cube BLE accelerometer:** **[C]** TRM exposes accelerometer *streaming* + tap/move + 4 RGB LED +
  battery-voltage characteristic (Ch.14 pp.126–129). **[P]** SDK exposes tap/move/up-axis/4-LED + pose
  (via camera markers) but **NOT a raw accelerometer stream**. → reachable at BLE layer, not via SDK.
- **⚖️ Payload budget:** **[C]** ≈30–40 g + *measure first*; **[P]** 45 g max / 35 g target.
- **Design rule [Both]:** carried attachment mounts on a printed shell matching the cube's corner-notch
  lift-hook geometry + ~44 mm footprint; frame origin = the cube marker pose Vector already localizes.
- **[C] open question (the big one):** payload grams, cube mass, gear ratio, lift torque are **all
  unpublished** — weigh & load-test before committing. `[P^1–P^10]`

---

## V2 — The Rover-Cube (sensor pod)

**[Both]** Rebuild the cube shell (~44 mm, corner-notch geometry preserved) as a self-powered ESP32-S3
pod adding the modalities Vector most lacks, keeping cube play (LEDs/tap). Stream light data over BLE,
bulk frames (thermal/depth/camera) over WiFi to the box.
- **[P] payload (ranked):** MLX90640 thermal (#1, $40/3.5 g/23 mA) · ToF LiDAR — **VL53L5CX carry /
  CygLiDAR D1 base** (#2) · wide-FOV camera (#3) · BME280 env (#4) · UWB DWM1000 (#5) · BMI270 IMU (#6);
  180 mAh LiPo; **carry config ≈23–25 g, base-station ≈51 g** (CygLiDAR D1 28 g dominates → place-and-
  scan only). Pogo-pin dock charging; BLE service mirrors original cube characteristics. `[P^11–P^21]`
- **[C] payload:** MLX90640 (±2 °C, 16 Hz, **110°×70°** or **55°×35°** FOV, $60) + **VL53L5CX 8×8 ToF**
  (~4 m, $20) — explicitly **rejects full RPLiDAR as too heavy** (A1 ~$100, C1 110 g) for carrying +
  **BME688** (adds VOC gas) + optional **UWB DW3000** (~$15.50, 3.3 µA beacon); 250–400 mAh LiPo (6–9 g);
  **~30–45 g, ~$130–160**.
- **Usage [Both]:** (a) Rover-Map mode — Vector carries the carry-config and drives a circuit → box
  builds 2D occupancy + thermal overlay ("Google-Maps car"); (b) base-station — placed as a persistent
  room sensor (UWB gives absolute position); (c) play/personality unchanged.
- **Anki-grade [Both]:** MLX90640 factory-calibrated EEPROM coefficients + per-pixel flat-field (FFC);
  CygLiDAR solid-state (no mechanical drift, <±1%); map fusion via occupancy grid + confidence decay,
  overlapped with Vector's IMU odometry.

---

## V3 — The Thumb (a lift attachment that lets Vector feel)

**[Both]** Ultra-light printed clip on the lift fork adding force + temperature + hardness; **9DTact-
style optical tactile** as the rich path; an active press-and-measure loop with drift correction.
- **⚖️ Primary sensor:** **[C]** barometric-MEMS pad (**MPL115A2** ~$13/5 µA, or BMP280, sealed under
  silicone) = lightest, **or load-cell+HX711** (±0.1% ≈ ±5 g on a 5 kg cell, vs FSR ±10–25%). **[P]**
  **FSR (Interlink 402, contact) + 5 g load-cell + HX711 (force) + NTC thermistor**, read by **RP2040
  Pico W**, ~10 g, ~$23.
- **Rich path [Both]:** **9DTact** (open HW+SW, ~$50 DIY, translucent gel + camera → 3D shape + 6D force
  from a NN on ~100k image-force pairs); DIGIT ($350/$40 gels), GelSight Mini ($499/$49 gels) higher-
  fidelity commercial.
- **What it computes [Both]:** force-to-move → mass/friction (**Fs = μs·m·g** [P]); hardness
  **H ≈ dF/dδ** ([P]; VBTS ~88% vs human 48%); temperature (thermistor vs ambient); texture/slip (FSR
  high-freq oscillation, FFT'd on the MCU).
- **"Touching reality" protocol [P, 6 steps]:** null/tare → light touch → ramp press (5% steps/500 ms)
  → hold + thermistor → release/repeat 3× → **drift-correct by pressing its own rubber bumper (the
  "reference stone")**. [C] frames the same as "calibrate vs durometer foams + known weights,
  temperature-compensate (baro & load cell both drift), self-correct over time."
- **[C-only] software ecosystem:** **facebookresearch/sparsh** (self-supervised touch), **linchangyi1/
  9DTact**, GelSight `gsrobotics` + `digit.ml`, **linchangyi1/Awesome-Touch**, HX711 libs, and **3D Cal**
  (arXiv:2511.03078 — auto-calibrate vision-based tactile sensors with an FDM printer).
- **Mount [Both]:** TPU snap-fit clip on the fork tines, contact pad ~3 mm proud; readout PCB epoxied to
  the static fork arm; +5 mm Z within the lift envelope. **~5–12 g, ~$15 (baro+thermistor) → ~$50
  (9DTact) → $350+ (DIGIT/GelSight).** `[P^22–P^29]`

---

## V4 — The Desk-Arms (Vector-commanded manipulation)

**[Both]** Two **SO-101** arms (6-DOF, **Feetech STS3215** magnetic-encoder servos, Apache-2.0) flank a
marked **control area** on the box; overhead USB camera; Vector pushes/delivers objects, arms manipulate.
- **Servos ⚖️:** **[P]** STS3215 ~15 kg·cm stall, 500 mm reach, ~800 g, ~$260/pair. **[C]** more precise:
  **C001 19.5 kg·cm @7.4 V (1:345 gear, ~5 kg·cm rated); 12 V C018 30 kg·cm @12 V / 19 kg·cm @7.4 V,
  0.222 s/60°, ~55 g each**; ~$100–130 parts / ~$220 kit; needs a 12 V 5 A+ supply for the high-torque
  variant.
- **Grippers [Both]:** stock parallel jaw + printed **TPU soft fingers** (compliant/safer); [P] adds
  vacuum-cup option; touch-sensing fingertip from V3 for force feedback.
- **Control stack [Both]:** **ikpy / LeRobot IK** for Cartesian targets + scripted "rotate N°" for the
  turntable task; **LeRobot ACT** (~50 / "few dozen" demos, ~1 h training on a laptop GPU, deploy at
  ~10–15 Hz) for learned manipulation; **OpenVLA / π0** upgrade path (ACT is faster/more reliable for
  the 3D-scan task). LeRobot policy menu [C]: ACT, Diffusion, VQ-BeT, SmolVLA, Pi0/Pi0-Fast.
- **Hand-eye [Both]:** OpenCV `calibrateHandEye` (TSAI), ArUco board, 15+ poses → camera-to-base
  transform, **<2 mm** error; re-run if the box moves.
- **Workflow [Both]:** Vector detects object → `push_to_control_area` → overhead camera localizes
  (ArUco/PoseCNN) → arm dispatch ("grasp [x,y,z], rotate Z +30°, ×12") → **COLMAP / gsplat / SuperSplat**
  3D reconstruction from the rotated views → model logged to ENGRAM. **Vector stays in command.**
- **[C] alt arm:** Koch v1.1 (Dynamixel XL430/XL330, better torque feedback, single-arm precision).
  `[P^30–P^43]`

---

## V5 — Tactile & manipulation software / datasets ("prove what it feels")

**[Both]** Standardize on vision-based tactile (9DTact/DIGIT) + LeRobot; turn raw force/deformation into
"hard/soft, weighs X, needs Y N" via supervised calibration vs known objects; validate by press-test
error; add touch + thermal as ENGRAM channels.
- **Software [Both]:** DIGIT `digit-interface`, GelSight `gsrobotics`, **9DTact**, HX711 libs, **LeRobot**
  (ACT/Diffusion/SmolVLA/π0), **OpenVLA**, **openpi (π0)**, **ikpy**, OpenCV `calibrateHandEye`,
  MLX90640 driver, COLMAP/3DGS. **[C] adds** `facebookresearch/sparsh`, **Touch100k / TAG** datasets,
  3D Cal. **[P] adds** `tactile-learning` (BRL).
- **Accuracy figures ⚖️:** **[P]** 88% hardness (VBTS), 2-layer NN 88%, SVR ±5 Shore, mass ±10% @
  calibrated friction. **[C]** ~99% roughness / ~98.8% hardness / ~89.6% glove-object — but **explicitly
  flags these come from richer sensor arrays than a single fingertip** (won't transfer directly).
- **Validation [Both]:** press a panel of reference objects (sponge/foam/eraser/bolt/marble/fruit/coin),
  measure predicted-vs-true; **[P] MAE ≤ 8 Shore** acceptance; re-check drift after ~50 h, re-tare vs
  rubber puck.
- **ENGRAM channels:** **[P]** TactileFingerprint 5D `[H, F_static, ΔT_contact, σ_slip, texture_FFT]` +
  ThermalFingerprint 3D `[T_surface, ΔT_ambient, T_rate]`. **[C]** `{peak_force_to_move,
  compliance/hardness, texture_signature, temperature}`. Cosine-similarity match against prior entries.

---

## V6 — System integration & affordances

**[Both]** One world-model on the box registers every tool into a shared room frame; Vector reasons over
an explicit affordance/tool-use model; a behavior layer decides which tool to use when.
- **Integration map [Both]:** Rover-Cube = BLE (light) + WiFi (frames), frame = cube marker / UWB;
  Thumb = I²C→ESP32/RP2040→BLE (or camera→USB for 9DTact), frame = lift-arm tip (analytic from
  `lift_height_mm` + IMU); Arms = USB serial, frame = arm base via hand-eye; Vector = wire-pod/SDK,
  frame = robot pose / cube.
- **[P] affordance registry (JSON):** `rover_cube{sense:[thermal_map,lidar_map,env], behaviors:
  [carry_and_map, place_as_sensor]}`, `thumb{sense:[force,hardness,temp,texture], behaviors:[press_ramp,
  hold_measure, slip_detect]}`, `desk_arms{manipulate:[rotate,hold,scan_3d], behaviors:[push_to_control_
  area, arm_dispatch]}`. Behavior layer: "understand this object" → thumb + arms → fuse in ENGRAM; "map
  this room" → rover_cube; "find the warm thing" → rover_cube thermal.
- **Goal framing [Both]:** richer phenomenology, not gadgetry — Vector goes from *visually* knowing a
  room to *thermally* knowing it; from lifting blindly to *feeling* what it lifts; from observing an
  object to *understanding its 3D structure*.

---

## V7 — Manufacturing & BOM

**[Both]** PETG structural shells, TPU 95A contact pads, PLA jigs; ESP32-S3 for self-powered
attachments, RP2040 where only simple sensing is needed; all hobby-printer-friendly.
- **[P] per-attachment:** Rover-Cube shell PLA ~6 g/3 h; Thumb TPU pad ~2 g/1 h; control-area mat;
  arm base mounts PETG ~30 g/4 h.
- **[C] per-attachment BOM:** Rover-Cube ~$130–160 / ~30–45 g; Thumb light-path ~$25–40 / ~5–12 g
  (9DTact +$50); Desk-arms ~$300–550. **Design files to fork:** `TheRobotStudio/SO-ARM100`,
  `linchangyi1/9DTact`, Adafruit/Pimoroni sensor-mount STLs, `kercre123/wire-pod`.

---

## FINAL SYNTHESIS — merged specs + phased build

### Rover-Cube
- Shell ~44 mm, corner-notch geometry, **two configs**: carry (ESP32-S3 + MLX90640 + VL53L5CX + env +
  UWB + 180–400 mAh LiPo, **~23–45 g** ✅) / base-station (adds CygLiDAR D1, ~51 g, place-and-scan only).
- Comms WiFi (frames) + BLE (cube parity); pogo-pin dock charging. **~$90 carry / ~$130–170 base.**

### Thumb
- TPU clip on fork tines; **[merged sensing]** barometric-MEMS pad or 5 g load-cell+HX711 for real
  newtons (FSR only for fast contact), + NTC thermistor; 9DTact optical as the rich upgrade.
- Readout RP2040/ESP32-S3 @80 Hz → BLE/WiFi; hardness via dF/dδ; calibrated vs reference objects +
  rubber-puck drift correction; ENGRAM 5D tactile + 3D thermal. **~5–12 g, ~$23–50** ✅.

### Desk-Arms
- 2× SO-101 (C001 19.5 kg·cm / C018 30 kg·cm @12 V), parallel + TPU soft gripper, overhead + wrist
  cameras; ikpy/LeRobot IK + ACT (~50 demos); OpenCV TSAI hand-eye (<2 mm); push-to-control-area →
  rotate → COLMAP/gsplat 3D scan → ENGRAM. **~$264–550.** Apache-2.0.

### Phased build (merged — both agree on order, Claude adds Phase 0)
- **Phase 0 [C, critical] — MEASURE THE TRUTH (week 1):** weigh the cube; find real payload by loading
  a printed shell until docking/lift fails or stalls. **This single number gates the whole project.**
  Thresholds: payload <20 g → Rover-Cube becomes tethered/stationary; force pad can't resolve <0.5 N →
  step up to load-cell/9DTact; learned policies < scripted IK on grasp success → keep IK for production.
- **Phase 1 — Thumb (light path, ~$25–40):** force/hardness/temperature on everything Vector touches;
  validates the MCU→box pipeline. *(Cheapest, most transformative per dollar.)*
- **Phase 2 — Rover-Cube:** thermal + ToF + env; carry-and-map behavior; confirm mass vs Phase-0 limit.
- **Phase 3 — Desk-Arms:** 2× SO-101 + overhead camera + LeRobot; scripted IK + OpenCV hand-eye first,
  then ACT/SmolVLA once teleop data exists.
- **Phase 4 — integration & ENGRAM:** unify tool frames into the room frame; add touch/thermal
  fingerprint channels; ship the tool-use behavior layer. **Full system ~$485 [P].**

---

## COMBINED CAVEATS
- **⚖️ The load-bearing unknown [C]:** Vector's lift **payload in grams, cube mass, gear ratio, and
  torque are not published anywhere** (absent from TRM, SDK, teardowns). All carried-mass figures are
  estimates until physically measured.
- **⚖️ Cube accelerometer:** TRM (BLE layer) says streamable [C]; Python SDK doesn't surface it [P] —
  reconcile on hardware via wire-pod.
- **Cube battery [C]:** 1.5 V cylindrical **N/E90/LR1** cell (not CR2032). A same-size **12 V A23 will
  destroy the cube** (TRM warning).
- **Body mass:** ~159 g [P] / ~170 g [C] are review/quick-start figures, not an official Anki spec.
- **Tactile accuracy [C]:** 98–99% figures come from richer sensor arrays than a single fingertip —
  validate on-platform.
- **Control caveat [C]:** custom firmware/SDK lift control assumes an **unlocked (OSKR) bot or wire-pod**;
  a stock retail Vector has limited lift/dock SDK control.
- **Prices fluctuate** (DIGIT/GelSight need licenses/gels); verify current pricing + stock before purchase.

---

## APPENDIX A — Claude [C] inline sources
Vector Technical Reference Manual & docs (Randall Maas — randym32.github.io), `anki/vector-python-sdk`
(Apache-2.0), `kercre123/victor` + `kercre123/wire-pod`, `TheRobotStudio/SO-ARM100`, `linchangyi1/9DTact`,
`facebookresearch/sparsh`, GelSight `gsrobotics`, `digit.ml`, `linchangyi1/Awesome-Touch`, HX711 libs
(bogde / Olav Kallhovd HX711_ADC), **3D Cal arXiv:2511.03078**, InstaGrasp **arXiv:2305.17029**,
Touch100k / TAG datasets, `huggingface/lerobot`, `openvla/openvla`, OpenCV `calibrateHandEye`.

## APPENDIX B — Perplexity [P] references (1–43, verbatim)
1. https://github.com/anki/vector-python-sdk/blob/master/anki_vector/behavior.py
2. https://www.reddit.com/r/AnkiVector/comments/1d3c7f5/question_about_the_capabilities_of_vectors_cube/
3. https://www.reddit.com/r/AnkiVector/comments/a023m9/vector_cube_tap/
4. https://www.comparably.com/companies/anki/faqs
5. https://support.anki.bot/article/531-vector-ccis
6. https://blog.csdn.net/ZhangRelay/article/details/86755937
7. https://manuals.plus/vector/anki-000-0075-vector-robot-quick-start-guide
8. https://support.anki.bot/article/115-vectore28099s-cube
9. https://www.kinvert.com/cozmo-dock-with-cube-with-python/
10. https://github.com/codaris/Anki.Vector.Samples
11. https://www.cnx-software.com/2023/03/22/xiao-esp32s3-tiny-esp32-s3-wifi-4-and-ble-5-0-module-for-iot-ai-robotics/
12. https://kamami.pl/en/adafruit-feather/1180717-esp32-s3-feather-wifi-and-ble-module-with-esp32-s3-4-mb-5477-5906623431274.html
13. https://www.adafruit.com/product/4407
14. https://www.desertcart.co.ke/products/288247579-cygbot-cyg-li-dar-d-1-small-size-2-d-3-d-dual-solid-state-to-f-li-dar-for-slam-obstacle-avoidance-and-navigation-of-robots
15. https://www.rfidjournal.com/news/decawave-intros-ultra-wideband-active-rfid-module/74138/
16. https://smartbuy.alibaba.com/buyingguides/uwb-dw3000
17. https://circuithelper.com/design-and-test-of-a-custom-ultra-low-power-esp32-s3-development-board/
18. https://github.com/digital-dream-labs/vector-bluetooth
19. https://evelta.com/cygbot-cyglidar-d2-dual-mode-tof-lidar-sensor-for-2d-and-3d-data/
20. https://www.seeedstudio.com/blog/2019/11/25/mlx90640-thermal-imaging-cameras-for-your-microcontroller/
21. https://cygbot.com/s2/s2_1.php
22. https://mikroelectron.com/product/me-593
23. https://www.schematik.io/parts/families/force-weight-sensors
24. https://www.utmel.com/components/rp2040-vs-esp32-vs-stm32-video-what-are-the-differences-between-them?id=1898
25. https://venturebeat.com/ai/facebooks-digit-is-a-low-cost-tactile-sensor-for-robotic-hands/
26. https://www.roboticscenter.ai/learn/tactile-sensor-comparison
27. https://research-information.bris.ac.uk/ws/portalfiles/portal/400910543/ROSO24_0116_FI.pdf
28. https://arxiv.org/html/2505.13231v1
29. https://www.alphaxiv.org/overview/2505.05725
30. https://www.roboticscenter.ai/en/hardware/so-101/specs
31. https://www.hackster.io/news/hugging-face-launches-the-so-101-an-upgraded-low-cost-3d-printable-autonomous-robot-arm-532360f441eb
32. https://www.roboticgizmos.com/koch-v1-1/
33. https://oa.upm.es/94787/1/10464018.pdf
34. https://arxiv.org/abs/2305.17029
35. https://www.roboticscenter.ai/blog/act-policy-explained
36. https://huggingface.co/docs/lerobot/en/act
37. https://trelis.substack.com/p/train-an-act-policy-for-an-so-101
38. https://openvla.github.io
39. https://www.roboticscenter.ai/physical-intelligence-pi0-vs-openvla
40. https://docs.opencv.org/3.4/d9/d0c/group__calib3d.html
41. https://forum.opencv.org/t/eye-to-hand-calibration/5690
42. https://www.ar-go.co/blog/what-is-gaussian-splatting
43. https://github.com/Physical-Intelligence/openpi

---

*Fused 2026-06-24 from `06_physical_attachments__rovercube_thumb_deskarm.md` (Claude) +
`05_physical_attachments__expanded_senses.md` (Perplexity). No finds or sources dropped; divergences
flagged inline with ⚖️.*
