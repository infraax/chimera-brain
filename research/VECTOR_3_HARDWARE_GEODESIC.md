# RESEARCH GEODESIC — Vector 3.0: a Clean-Sheet Creature on Today's Silicon
## The evolution of Vector — same Anki soul, 2026 hardware — designed to actually be built
## Created: 2026-06-24 · Dexter × Claude Opus 4.8

> **How to use:** hand each *vector* (V1…V14) to a research agent. Return findings in the **Output**
> format. This is a **hardware + systems-architecture + power + manufacturing** geodesic — the most
> consequential one we've written, because its output is a **buildable spec for real hardware we
> intend to fabricate**, not a retrofit of the 2018 robot.
>
> **CRITICAL — build on what we already have, do not redo it.** Five research reports already came back
> and are fused in `research/reports/unified/`. **Read them first and treat them as INPUT**, not as
> open questions:
> - `unified/cutting_edge_oss__UNIFIED.md` — the 2024–26 model/runtime gems (perception, audio, 3D, VLA).
> - `unified/external_sensor_array__UNIFIED.md` — room-scale sensing, the robot/box split, privacy.
> - `unified/physical_attachments__UNIFIED.md` — Rover-Cube, the **Thumb (tactile)**, desk-arms.
> - `unified/frequency_memory__UNIFIED.md` — ENGRAM as frequency/symphony (represent→compose→retrieve→ground).
> - `09_engram_rewrite__1.0_geodesic.md` — ENGRAM's **language/perf/ARM** reality (C++/Go/Python, PFFFT,
>   FlatBuffers, the 2018-silicon pain points).
>
> The ground truth for "what Anki actually did" is the **Vector Technical Reference Manual (TRM, Randall
> Maas)** + the **open-source firmware `kercre123/victor`**. Every vector below should reason in the
> arc: **Anki's 2018 choice (TRM) → the constraint that forced it → what 2026 tech now enables → the
> Vector 3.0 recommendation.**
>
> **Concrete design → `research/BENZY_VECTOR_3_DESIGN_SPEC.md`.** This geodesic is the *research
> brief*; "Benzy" is the sketch-derived **product design** it feeds — the three-body creature
> (robot + compute-dock + scout drone), the exploded-view component manifest, and the
> image-generation prompt pack. Findings here should land there.

---

## PRIME DIRECTIVE
> *Design **Vector 3.0**: a clean-sheet, tabletop companion robot that preserves Anki's engineering
> philosophy and emotional soul, but is built on 2026 silicon, sensors, actuators, and batteries — and
> is **realistically fabricable by a small/solo builder** as the long-term evolution of the chimera
> project. It may be **somewhat larger** than the original Vector to fit a **bigger battery and more
> compute**; it must run the full chimera cognitive stack on-board where possible (L1 Brainstem reflex,
> L2 Cortex perception fusion, L3 Constructor memory/personality) with ENGRAM as native situational
> memory. The deliverable is a **coherent, prioritized, buildable hardware specification** — block
> diagram, compute partition, power/thermal budget, sensor & actuator suite, BOM tiers, and a
> dev-board-first prototype path — not a survey.*

**Explicit owner requirements (must each be satisfied and traced in the synthesis):**
1. **Same Anki philosophy, today's technology.** Cleverness × efficiency × quality, not brute force.
2. **A little larger is allowed** → fit a **better battery** (we will run far more compute) + proper thermals.
3. **More compute & memory** — run perception + ENGRAM + a small on-board LLM/VLA where feasible.
4. **Better motors** (quiet, precise, force-sensing), **better screen**, **better microphones**.
5. **Surround perception:** **multiple cameras for full surrounding-area understanding** + **LiDAR** + **infrared**.
6. **The Thumb is NATIVE** — built-in manipulation with **pressure / force / tactile sensing**, not a bolt-on.
7. **Designed to be built on our own hardware** — sourceable parts, a prototype path, a real BOM.

---

## THE ANKI-WAY RUBRIC (rank every option on these — this is the whole point)
Score each candidate 1–5 on each axis; a clever solo-friendly part beats a powerful unbuildable one.
- **(C) Cleverness** — does it solve a hard problem with physics/architecture instead of brute force?
  (Anki's canon: ONE camera + controlled motion → triangulated depth; 4 mics that *null the robot's
  own motor noise* and recalibrate as actuators age. That is the bar.)
- **(E) Efficiency** — performance-per-watt and per-dollar; respects a battery and a passive/near-passive
  thermal budget; doesn't melt a tiny enclosure.
- **(Q) Quality** — genuinely good, verified results; reliable; "Anki-grade" fit, finish, and feel.
- **(B) Buildability** — can a small/solo builder actually source, assemble, and bring it up?
  Module/dev-board path first, custom PCB later. Open drivers. Realistic MOQ and cost.
- **(F) Fit-to-soul** — preserves the creature: expressive face, intimacy, ethological behavior,
  graceful degradation, the safety partition. Hardware in service of personality, never gadgetry.

---

## CROSS-CUTTING CONSTRAINTS (apply to every vector)
1. **Honor the Anki doctrine** (`ANKI_WAY.md`): self-cancellation (model & subtract your own influence —
   ego-noise, ego-motion, self-occlusion); physical priors (cheap sensing via physics); ethology-first;
   graceful degradation (every subsystem has a degraded-but-alive fallback); a **hard safety partition**
   (a separate real-time MCU owns motors/cliffs/thermal, independent of the application processor — as
   Anki separated the STM32 body-board/syscon from the APQ8009); designer-tunable; **respect the budget**.
2. **Power is the master constraint.** The entire external-sensor geodesic existed *because* the 320 mAh
   pack couldn't sustain continuous perception. Vector 3.0 relaxes this (bigger body/battery + far better
   perf/watt) but must still **quantify the compute-power-thermal budget** and decide, per subsystem,
   **what runs on-robot continuously vs gated vs offloaded to the dock/box.** The dock-box from the
   external-sensor report remains a first-class part of the architecture.
3. **Map every choice to the chimera stack and ENGRAM.** Each sensor/compute decision must say which
   layer it serves: **L1 Brainstem** (reactive, <10 ms, MCU), **L2 Cortex** (perception fusion/attention,
   SoC/NPU), **L3 Constructor** (LLM/memory/personality), and how it feeds **ENGRAM** (new fingerprint
   channels: vision, audio, depth, thermal/IR, tactile). Reference the ENGRAM-rewrite report: a modern
   aarch64 SoC with native fp16/int8 + NPU **erases** the 2018 pain points (softfp ABI, fp16
   storage-only, 6–8× CPU slowdown, no NPU) — state explicitly which pain points each SoC choice removes.
4. **Buildable & open.** Favor parts with open drivers, dev-board availability, public datasheets, and
   sane sourcing (LCSC/Mouser/DigiKey/Seeed). Prefer modules for the prototype; note the custom-PCB path.
5. **Recency + honesty.** 2024–2026 parts; cite datasheets/prices/dates; flag vaporware, NRE traps,
   automotive-only or NDA-gated parts, and "Nx faster" marketing (re-benchmark mindset).
6. **One coherent machine.** Vectors interact (SoC choice gates camera MIPI lanes, NPU TOPS, RAM
   bandwidth, power, thermals). The synthesis must reconcile them into ONE consistent design, not a
   pile of best-in-class parts that can't co-exist.

---

## RESEARCH VECTORS

### V1 — Compute architecture & the brain partition (the keystone)
- **Anki baseline (TRM):** APQ8009 (4× Cortex-A7 @ up to 1.2 GHz, ~512 MB RAM, no NPU, softfp) for the
  application engine + a separate **STM32F0-class body MCU / syscon** for hard-real-time motor/safety.
- **Questions:** What is the right **2026 on-robot SoC** to run L2 perception + ENGRAM + (ideally) a
  small on-board VLM/LLM, at a tabletop-robot power/thermal budget? Evaluate **Rockchip RK3588/RK3588S**
  (6-TOPS NPU, 8K, many MIPI lanes), **Qualcomm QCS6490 / Dragonwing**, **NXP i.MX 8M Plus** (2.3-TOPS
  NPU), **Amlogic A311D2**, **Horizon/Ambarella/Hailo-paired** vision SoCs, **Raspberry Pi CM5 (+Hailo-8L)**,
  and the **Jetson Orin Nano/NX** (only if power/thermal can be tamed). Pair with a **real-time MCU for
  the L1 safety partition** — **STM32H7 / STM32N6 (with NPU) / RP2350 / Teensy-class** — and define the
  MCU↔SoC seam (the modern CLAD/IPC). Decide the **on-robot vs dock-box split**: which of L2/L3 runs
  on-robot continuously, which is gated, which offloads (reuse the external-sensor report's robot/box
  data-plane). Quantify TOPS, RAM bandwidth, MIPI-CSI lane count, power envelope, Linux/driver maturity,
  and which **ENGRAM-rewrite pain points** each SoC eliminates (aarch64 hard-float, fp16/int8 compute,
  NEON+dotprod, NPU offload of FFT/ANN).
- **Return:** a ranked SoC recommendation + the MCU safety-partition choice + the chimera-layer→silicon
  mapping + the on-robot/dock split, with power, thermal, lane budget, and driver reality.

### V2 — Power, battery & charging (the master constraint, quantified)
- **Anki baseline:** ~320 mAh LiPo (~1.2 Wh), ~25–45 min active, dock pogo-pin charge.
- **Questions:** Given V1's compute draw, **size the battery** for a target active runtime (propose
  options for 1 h / 2 h / "all-day-with-naps") and a 24/7-with-dock-naps usage model. Compare chemistries
  for a slightly-larger body: **Li-ion 18650/21700**, **LiPo pouch**, **LiFePO4** (safety/cycle life),
  **Si-anode** cells; cycle life, C-rate for compute bursts, safety, mass, volume. Specify the **PMIC /
  fuel gauge / BMS**, **dynamic voltage-frequency scaling** strategy, sleep/wake power states, and the
  **compute-power budget table** (idle / perception-active / full-stack / charging). Charging: dock
  pogo-pins vs **USB-C PD** vs **Qi2 wireless**; dock as compute-offload + charge + sensor hub. The Anki
  move: the robot naps on the dock and wakes to act — quantify "awareness uptime" vs raw runtime.
- **Return:** battery spec (chemistry, capacity, cells, mass/volume), PMIC/BMS choice, the power-budget
  table, charge architecture, and the runtime math per usage mode.

### V3 — Vision I: multi-camera surround perception
- **Anki baseline:** a single fixed 120° HD camera + the "two frames from one camera → depth" physics trick.
- **Questions:** Design a **multi-camera suite for full surround understanding.** How many cameras and
  where (front stereo pair for depth + eye-contact, side/rear or fisheye for 360° awareness, a downward
  cliff/near-field cam)? **Global vs rolling shutter**; sensor families (**Sony IMX**, **OmniVision OVxx**),
  resolution vs MIPI-lane/NPU budget from V1; HDR for mixed lighting; low-light performance. Which
  on-device models from `cutting_edge_oss__UNIFIED.md` run on V1's NPU (FastVLM / Moondream / SmolVLM2
  for understanding; YOLO-alt/RT-DETRv2 for detection; SAM2/EdgeSAM for seg; Depth Anything V2 / VGGT /
  MASt3R-SLAM for 3D) — and which are robot-side vs dock-side. Preserve the **eye-contact intimacy
  camera** as a distinct role. Consider an **event camera (DVS)** as a low-power always-on motion sense.
- **Return:** camera count/placement/sensor choice + shutter/HDR/low-light rationale + the per-camera
  role (eye-contact / depth / surround / cliff) + the model→camera→NPU mapping + robot/dock split.

### V4 — Vision II: depth, LiDAR & infrared (3D + dark + presence)
- **Owner ask:** explicitly wants **LiDAR** and **infrared**.
- **Questions:** What depth/3D + IR suite fits a tiny moving platform? Compare **solid-state dToF/iToF**
  (ST **VL53L8CX** 8×8 zones, **CygLiDAR**), **mini solid-state LiDAR**, **structured-light IR**, and
  **stereo-from-cameras (V3)** — for surround obstacle/edge sensing and the **3D home map** (cross-ref
  the splat/VGGT mapping stack and the external-sensor LiDAR/mmWave findings). **Infrared** roles:
  near-IR illuminator for **dark/night vision** (so the creature still perceives in a dark room),
  IR cliff/edge sensing, and **thermal IR** (MLX90640-class) as a new ENGRAM channel (find people/pets/
  warm objects). Consider **mmWave radar** for privacy-preserving presence/vital-signs (per the sensor
  report — flagged experimental). Decide which depth modality is the primary navigation sense vs
  redundant safety. Respect power: which run continuous vs gated.
- **Return:** the depth+IR sensor stack (modality × placement × range × power × ENGRAM channel) + the
  primary-vs-redundant role assignment + night-vision design + what's continuous vs gated.

### V5 — Audio: mic array, voice processor & speaker
- **Anki baseline:** 4-PDM-mic beamforming array (read over 2 lines, 16 kHz) with **motor-noise nulling
  + actuator-aging recalibration** — the canonical self-cancellation move; Acapela TTS; Wwise; a small speaker.
- **Questions:** Design a **better on-robot audio front-end.** How many MEMS mics and geometry (keep 4,
  or go 6–8 for better DOA/separation)? Use a dedicated **voice-processor / hardware AEC+beamformer**
  (XMOS **XVF3800**-class) on-robot so the SoC isn't burdened? Generalize Anki's ego-noise nulling with
  modern DSP. Add a **contact/bone-conduction mic** for robustness? Speaker/amp choice for expressive,
  clear voice in a small cavity. Which STT/TTS/VAD/denoise/speaker-ID/emotion models from
  `cutting_edge_oss__UNIFIED.md` (Moonshine, Parakeet, Kokoro, Silero, GTCRN/DeepFilterNet, TitaNet,
  emotion2vec) run on-robot vs dock. Keep near-field intimate voice on-robot; far-field room audio can
  lean on the external array.
- **Return:** mic count/geometry + voice-processor choice + speaker/amp + the on-robot audio DSP design
  (AEC, beamform, ego-noise null, recalibration) + the STT/TTS/etc model placement.

### V6 — Actuators & motion (treads, lift, head — quiet, precise, force-sensing)
- **Anki baseline (TRM):** brushed DC motors on a **DMC2038LVT** H-bridge with **optical encoders**;
  treads; a lift (32–92 mm); head tilt; current-sensing that lets Vector *feel* being picked up/held.
- **Questions:** What 2026 actuators give **quieter, more precise, force-aware** motion? Compare
  **brushed vs BLDC vs coreless** motors; **magnetic absolute encoders** (AS5600-class; the SO-101 arm
  uses Feetech magnetic-encoder servos); gearboxes/backlash; closed-loop **current/torque sensing** so
  the creature can feel contact and self-calibrate as gears wear (the Anki recalibration doctrine).
  Treads vs wheels for a slightly larger body; head/neck DOF for expression; quiet operation targets
  (dB). The motor-driver IC + the **L1 MCU** motion-control loop. How motor state feeds **ego-noise
  cancellation** (V5) and ego-motion compensation (V3).
- **Return:** motor type + encoder + driver + DOF layout (drive/lift/head) + closed-loop force-sensing
  design + quietness target + self-calibration approach + how motor state is published to L1/L2.

### V7 — The NATIVE Thumb: built-in manipulation & tactile sensing
- **Owner ask:** the Thumb is **native** with **pressure/force sensors** — Vector 3.0 can *feel* what it
  touches and manipulate, not just lift blindly. Cross-ref `physical_attachments__UNIFIED.md` (Thumb section).
- **Questions:** Design a **native gripper/thumb** integrated into the lift/hand. What tactile modality
  built-in: **barometric-MEMS force pad** (MPL115A2/BMP-under-silicone), **load-cell + HX711** (real
  newtons), or **miniaturized optical-tactile** (9DTact/DIGIT-class — 3D contact + 6-axis force)? Native
  integration of **force-to-move (mass/friction), hardness (dF/dδ), temperature, slip** sensing. The
  **active "touching-reality" loop** (press → measure → model → drift-correct against a known reference)
  built into firmware. Mechanical: does Vector 3.0 get a true opposable thumb / parallel micro-gripper,
  or an instrumented lift fork? How tactile becomes a **native ENGRAM channel** (tactile + thermal
  fingerprints). Keep it light, reliable, and within V2's power/V6's actuator budget.
- **Return:** the native thumb/gripper mechanism + the integrated tactile sensor choice + the force/
  hardness/temp/slip inference + the active-sensing firmware loop + the ENGRAM tactile channel design.

### V8 — Display & expression (the face = the soul)
- **Anki baseline:** a **184×96 IPS LCD** rendering the iconic expressive eyes — minimal pixels, maximal
  personality; the single most important "soul" component.
- **Questions:** What 2026 micro-display best serves the face **without losing the Anki minimalism**?
  Compare small **round/rectangular LCD/OLED/AMOLED** panels (resolution, refresh, viewing angle,
  sunlight readability, power, burn-in for OLED), the display controller / GPU path on V1's SoC, and
  whether higher resolution actually helps emotion or just costs power. Keep the **ethological eye-
  rendering** philosophy (procedural emotion, not a video screen). Consider a curved/contoured cover lens.
- **Return:** display type/size/res/refresh + controller path + power + the "keep-it-minimal" rationale
  + any expression-hardware (eye lens, brightness/ambient adaptation).

### V9 — Proprioception, touch & environment sensors
- **Anki baseline:** 6-axis IMU; 4 cliff/drop IR sensors; capacitive touch back (petting detection); the
  half-built receptive-social-presence estimator.
- **Questions:** Upgrade the body senses: **9-axis IMU** (add magnetometer) for heading/orientation;
  **ToF-array cliff/edge** sensing vs IR; richer **capacitive/pressure touch "skin"** (where, and how
  many zones, for petting/holding/social touch); ambient sensors worth putting on-robot vs on the dock
  (temp/humidity/light/air per the external-sensor report); the **UWB tag** for the robot's cm-position
  in the room frame (dock anchors). Which feed L1 reflexes vs L2 context vs ENGRAM.
- **Return:** the proprioception+touch+environment sensor list (part × placement × zone count × layer
  served) + the touch-skin design + UWB positioning decision.

### V10 — Memory & storage (run the chimera stack + ENGRAM)
- **Anki baseline:** ~512 MB RAM, modest flash; no room for an LLM or a large situational archive.
- **Questions:** Size **RAM and non-volatile storage** for Vector 3.0's workload: L2 perception models +
  ENGRAM hot/cold store + (optionally) a small on-board LLM/VLA + the OS. **LPDDR4x vs LPDDR5** capacity/
  bandwidth (gate from V1); **eMMC vs UFS vs NVMe** for the model store and the **ENGRAM cold archive**
  (FlatBuffers EGRV, fp16, mmap — per the ENGRAM-rewrite report). How much RAM does the converged ENGRAM
  architecture (`frequency_memory__UNIFIED.md`: scattering + HRR @ D≈4096 + Hopfield + reservoir) need,
  and what stays on-robot vs dock? Endurance/wear for continuous situational logging.
- **Return:** RAM + storage spec (capacity, type, bandwidth, endurance) + the ENGRAM on-robot memory
  footprint + the model-store sizing + on-robot/dock data placement.

### V11 — Connectivity & positioning
- **Anki baseline:** WiFi (2.4 GHz) + BLE; dock pogo contacts; cube over BLE (DA14580).
- **Questions:** The 2026 radio suite: **WiFi 6/6E/7** (bandwidth for dock-offload of perception/3D),
  **BLE 5.x**, **Thread/Matter** (smart-home context), **UWB** (positioning, cube/attachment ranging),
  and the **robot↔dock-box link** (the latency-bounded data-plane from the external-sensor report —
  what the robot subscribes to vs computes locally). Antenna placement in a small metal-ish body;
  coexistence; the module choice (combo SoC radio vs discrete).
- **Return:** the radio/module suite + the robot↔dock link spec (bandwidth, latency, what flows each way)
  + positioning (UWB) decision + antenna/coexistence notes.

### V12 — Enclosure, mechanical, thermal & the dock
- **Anki baseline:** ~3.9″ tall, drop-survivable, treaded, a passive dock; tight thermals on a phone chip.
- **Questions:** For a **slightly larger** body with **more compute**: chassis material/layout, weight &
  balance (treads + payload + battery), drop survival, ingress. **Thermal design** is now critical —
  passive (heat-spreader/chassis-as-heatsink) vs a tiny quiet fan vs throttling; map V1's SoC TDP +
  V2's battery heat + V3/V4 sensors to a thermal budget. Redesign the **dock** as charge + compute-
  offload + sensor hub + the AEGIS-perimeter network node (per the external-sensor report). Prototype
  fabrication: 3D-print (FDM/SLA/SLS) for the prototype, injection-molding path for "Anki-grade" later.
- **Return:** enclosure concept (size, material, layout, balance) + the thermal design + the dock 2.0
  spec + the prototype-fabrication path.

### V13 — Software, OS & the safety partition
- **Anki baseline:** Linux on the APQ8009 (vic-engine/vic-robot/vic-anim in C++, vic-cloud/vic-gateway
  in Go) + a separate real-time MCU; FlatBuffers assets; CLAD-over-socket IPC.
- **Questions:** The 2026 software substrate: which **Linux** (Yocto/Buildroot/Ubuntu-core) on the SoC;
  the **RTOS** (Zephyr/FreeRTOS) on the L1 safety MCU; the **MCU↔SoC IPC** (modern CLAD / protobuf /
  shared-memory). How the chimera 3-layer + ENGRAM (C++ reflex + Go service + Python lab, per the
  ENGRAM-rewrite report) deploy across this hardware; the **inference runtime** per the OSS report
  (ONNX Runtime / ExecuTorch / RKNN / MLX-if-dock-is-Mac / TensorRT-if-Jetson). The **safety partition
  contract**: what the L1 MCU owns independently (motors, cliffs, thermal e-stop) so a crashed app
  processor can never drive the creature off a table. OTA/update strategy.
- **Return:** OS + RTOS choice + the MCU↔SoC IPC + the chimera/ENGRAM deployment map + the inference
  runtime per tier + the formal safety-partition contract + OTA approach.

### V14 — BOM, cost, sourcing & the phased build roadmap
- **Questions:** Roll the whole design into a **realistic bill of materials** with sourcing (LCSC/Mouser/
  DigiKey/Seeed), unit costs at qty 1 / 10 / 100, and lead-time/MOQ/NRE flags. Define the **buildable
  path for a solo maker**: **Phase 0** = dev-board bring-up (e.g., RK3588 SBC + MCU dev board + USB/MIPI
  sensors on a breadboard chassis) proving the stack end-to-end; **Phase 1** = integrated prototype
  (custom carrier PCB, real enclosure, real battery); **Phase 2** = "Anki-grade" refinement (custom PCB,
  injection-molded shell, thermal/EMC). Identify the **highest-risk / longest-lead parts** to prototype
  first, and what can be deferred. Note where we reuse `kercre123/victor` firmware vs write new.
- **Return:** the tiered BOM + sourcing + a phased dev-board→prototype→product roadmap + the risk-first
  build order + the firmware reuse-vs-new map.

---

## OUTPUT — Return Format (per vector)
```
### V# — <title>
RECOMMENDATION: the concrete design choice in 3–6 sentences (the decision, not a menu).
ANKI-WAY SCORE: C _/5 · E _/5 · Q _/5 · B _/5 · F _/5  (+ one line: why this beats the alternatives)
PARTS: part — vendor/URL — ~cost(qty1/10/100) — interface — power — open driver? — datasheet/date
ANKI 2018 → 2026: what Anki did (TRM) · the constraint that forced it · what today's tech changes
CHIMERA MAP: which layer (L1/L2/L3) + which ENGRAM channel it serves · on-robot / gated / dock
SELF-AWARENESS: how it models/cancels its own influence or self-calibrates (the Anki move)
POWER/THERMAL: draw (idle/active) · heat · effect on V2 budget
RISKS / OPEN QUESTIONS / CONFIDENCE + what to prototype to resolve them
```

## FINAL SYNTHESIS — the deliverable
Reconcile all 14 vectors into ONE coherent, buildable machine:
1. **Vector 3.0 master block diagram** — SoC + L1 MCU + sensors + actuators + display + radios + power,
   with the bus/lane/IPC map and the safety partition drawn explicitly.
2. **Compute partition table** — every chimera layer + ENGRAM stage → silicon (on-robot/dock), with the
   ENGRAM-rewrite pain points it eliminates.
3. **Power & thermal budget** — the full draw table per usage mode + battery sizing + runtime math +
   thermal solution.
4. **Sensor & actuator suite** — the complete surround-perception (cameras + LiDAR + IR + audio),
   proprioception/touch, the **native Thumb**, and motion list, each mapped to a chimera layer + ENGRAM channel.
5. **Tiered BOM + sourcing + the phased dev-board → prototype → product roadmap** (risk-first build order).
6. **The honest boundary** — what is buildable now by a solo maker, what needs custom PCB/NRE, what is
   "watch / next-rev," and where we knowingly diverge from Anki's choices and why.

---

## SEED SEARCH TERMS
`RK3588 NPU robotics SBC MIPI CSI lanes` · `Qualcomm QCS6490 robotics SoM` · `i.MX 8M Plus NPU camera` ·
`Jetson Orin Nano power thermal tabletop robot` · `STM32N6 NPU real-time motor control` · `RP2350 robot
safety MCU` · `21700 vs 18650 vs LiPo pouch robot battery runtime` · `Si-anode cell 2025 energy density`
· `USB-C PD vs Qi2 robot dock charging` · `BMS fuel gauge PMIC small robot` · `Sony IMX global shutter
MIPI module` · `OV9281 OV5647 surround camera robot` · `event camera DVS low power motion` ·
`VL53L8CX 8x8 ToF` · `solid state LiDAR small robot` · `near-IR illuminator night vision camera` ·
`MLX90640 thermal array robot` · `mmWave radar presence vital signs` · `XMOS XVF3800 mic array AEC
beamforming` · `MEMS mic array DOA 6 mic` · `BLDC coreless motor magnetic encoder AS5600 robot` ·
`closed loop torque sensing small robot` · `9DTact DIGIT miniature tactile sensor` · `barometric tactile
force sensor newtons` · `round AMOLED LCD micro display SPI MIPI` · `LPDDR5 eMMC UFS SoM` · `WiFi 6E
BLE UWB combo module robot` · `DWM3000 UWB ranging` · `Zephyr RTOS motor safety partition` ·
`RKNN ONNX Runtime ExecuTorch edge inference` · `Yocto Buildroot robot Linux` · `small robot passive
thermal heatsink chassis` · `LCSC Mouser robot SoM BOM cost`.

## INTERNAL CONTEXT (read these first — build on them)
- **Ground truth (what Anki did):** Vector **TRM** (Randall Maas, `randym32.github.io/Anki.Vector.Documentation`)
  + open firmware **`kercre123/victor`** (+ `wire-pod`). Hardware facts already established:
  `CHIMERA_REVERSE_ENGINEERING.md`, `VECTOR_ENG_VICTOR_BASE.md`, `VECTOR_ENG_UPGRADE_MAP.md`.
- **The five returned research reports (PRIMARY INPUT):** `research/reports/unified/cutting_edge_oss__UNIFIED.md`,
  `external_sensor_array__UNIFIED.md`, `physical_attachments__UNIFIED.md`, `frequency_memory__UNIFIED.md`,
  and `research/reports/09_engram_rewrite__1.0_geodesic.md`.
- **Doctrine:** `ANKI_WAY.md` (cleverness/efficiency/self-cancellation/safety-partition/budget-respect).
- **Cognitive target the hardware must run:** the chimera 3-layer (`CHIMERA_L2_CORTEX.md`,
  `DEEP_UNDERSTANDING_CONCEPT_01.md`) + ENGRAM (`vector_engram/`, `ENGRAM_FOR_VECTOR.md`,
  `ADR_ENGRAM_INTEGRATION_SEAMS.md`) + the frequency/symphony direction
  (`SOLVING_AI_MEMORY_WITH_FREQUENCY_AND_SYMPHONY.md`).
- **Convergence/north star:** `CHIMERA_CONVERGENCE_MAP.md`, `MACHINA_ANIMA.md` (creature-not-a-toy framing).

---

*This is the capstone hardware geodesic: its job is to turn everything we've learned into a real machine
we can build. Same soul, today's silicon. — 2026-06-24*
