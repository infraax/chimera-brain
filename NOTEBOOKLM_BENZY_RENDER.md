# NotebookLM Render Brief — Benzy (Vector 3.0)

*A focused source for generating **accurate blueprints, renders, exploded views, and see-through
graphics** of Benzy in NotebookLM (or any image tool). Unlike a generic prompt, this grounds every
visual in the **real, sourced hardware spec** so the output looks like *Benzy specifically* — correct
proportions, real components, real internal layout. Load this file (+ the sources in §8), pick a
Style, then paste a prompt from §6.*

> **The honesty line (read first).** Two layers exist and the renders must not blur them:
> - **CANONICAL** = the buildable engineering spec (V1 + V5–V14 reports). A tracked desk creature
>   with a real parts list. Use this for blueprints/exploded/see-through — it's *true*.
> - **ASPIRATIONAL** = the Benzy sketch dream on top: **humanoid arms, the electromagnet hand, and
>   the Benzy Sky scout drone.** These are NOT in the engineering spec yet (the spec has a single
>   *native thumb/gripper*, no arms, no drone). Render them as clearly-labelled **concept**, never as
>   "the build." §5 draws the line; §6 separates the prompt sets.

---

## 1. What this is and how to use it
1. Add this file as a NotebookLM source, plus the spec sources in §8 (and the sketch photos if you have them).
2. Pick a **Style** (e.g. blueprint, product render, anime for the dream shots).
3. Paste one prompt from §6 (canonical or aspirational) into the customize box. If the box truncates,
   use the first 2 sentences — the loaded sources carry the rest.

---

## 2. Canonical Benzy at-a-glance (render-relevant facts)
The buildable creature, distilled from the hardware reports for visual accuracy:

- **Silhouette:** Vector's descendant — an emotive **face-display head** that tilts, on a compact
  **rubber-tracked tank base**, with a short torso between them. A **native thumb/gripper** on the
  lift; a **modular backpack bay** on the rear.
- **Size:** **~105 mm wide × 80 mm deep × 130 mm tall**, **~350–450 g** (slightly larger than the
  2018 Vector's 100×80×115 mm / ~300 g — the extra height is battery + brain + thermal stack).
- **The face:** a **1.54″ 240×240 IPS LCD** rendering minimalist expressive eyes, behind a **convex
  acrylic cover lens** (~35 mm, gives the "alive," slightly magnified look). Minimal pixels, maximal
  personality — never a video screen.
- **Palette / finish:** **matte charcoal/graphite** body with **warm bronze/copper accents**
  (the look from the slide you liked), **soft-touch TPU flanks** (also the touch zones), a glowing face.
- **Stance:** heavy battery in the base → low center of gravity → planted, stable tread stance.

---

## 3. Exploded-view component manifest (REAL parts — for accurate diagrams)
Numbered for callouts. Every item is from the canonical spec. Use these labels verbatim.

**Benzy robot — head & face**
1. **1.54″ 240×240 IPS LCD face** (ST7789V) + **convex acrylic cover lens**
2. **Eye-contact camera** (Sony IMX678) — front, highest-bandwidth
3. **Stereo camera pair** (2× OV9281 global-shutter) — depth + eye contact
4. **Rear fisheye camera** (OV5647) — surround awareness
5. **4-mic array** (XMOS XVF3800, 66 mm square at the top corners) — AEC/beamforming/DoA
6. **Front depth ToF** (VL53L8CX 8×8) + **thermal-IR** (MLX90640) + **IR night LEDs** (4× 940 nm)

**Benzy robot — torso & sensing**
7. **RK3588S compute module** (Radxa NX5 SoM, 70×45 mm) — the L2/L3 brain (6-TOPS NPU)
8. **STM32H743 safety MCU** — the L1 real-time partition (motors/cliffs/thermal)
9. **6-axis IMU** (ICM-42688-P)
10. **Capacitive touch skin** (AT42QT1070 — top crown + 2 flanks) + **BME280** ambient + **VEML7700** light
11. **UWB tag** (DWM3000) — cm-level position in the room
12. **WiFi 6 + BT module** (RTL8852BE) + antennas routed to the top crown

**Benzy robot — motion, hand, power, thermal**
13. **Tracked drive module** — 4× coreless BLDC + AS5600 magnetic encoders + SimpleFOCMini + INA240 current sense
14. **Native thumb/gripper** — BMP390 tactile + **9DTact** optical-tactile (OV2640 cam) + TMP117 temp
15. **Main battery** — 3S 18650 (~10–12 Wh) / 3000 mAh LiPo + BMS, in the base (low CG)
16. **Speaker** — TAS5760M Class-D + 28×40 mm full-range driver in a rear cavity
17. **Thermal stack** — copper heat-spreader + heatpipes to the rear wall + a 25 mm silent rear fan
18. **Modular backpack bay** (rear) — pogo power/data (carries the aspirational drone, §5)

**Benzy Station — the Dock 2.0 (this is your "Station + compute (LLM)" sketch, confirmed)**
19. **Charging cradle** (USB-C PD 9 V/2 A) Benzy docks into nose-first
20. **Compute/LLM server** — Mac Mini / Pi 5 class, runs the slow reasoner + the **ENGRAM cold archive** (128 GB)
21. **Room LiDAR** (LDROBOT LD19) — maps the room while Benzy charges
22. **UWB anchors** (2–4× DWM3000) + **WiFi 6 local AP** + **STM32F411 dock MCU**

---

## 4. Internal layout (for SEE-THROUGH / x-ray accuracy)
So ghosted renders place parts correctly:
- **Bottom of base:** the battery pack (heaviest) — low CG.
- **Mid-body:** the RK3588S SoM board (vertical), the STM32H743 nearby, the M.2 WiFi module.
- **Rear wall:** the copper spreader + heatpipes + the 25 mm fan exhaust; the speaker cavity.
- **Top crown:** the 4-mic ring at the corners; the WiFi antennas; the touch crown zone.
- **Front face:** the LCD + convex lens; the camera cluster and front ToF just around it.
- **Front lift:** the native thumb/gripper with its tactile pad and tiny camera.
- **Drive:** tracks low on both flanks, motors inboard.

---

## 5. The canonical ↔ aspirational boundary (don't blur it in renders)
| Feature | Status | How to render |
|---|---|---|
| Tracked base, face, cameras, mics, RK3588S brain, native thumb, battery, dock-with-compute+LiDAR | **CANONICAL** (in the spec) | Blueprint / exploded / see-through — as the real build |
| **Two humanoid arms** | **ASPIRATIONAL** (sketch only; spec has one thumb/gripper) | Label "concept"; show as a future variant, not the build |
| **Electromagnet hand** ("if metal, activate") | **ASPIRATIONAL** | Concept callout only |
| **Benzy Sky drone** (50 MP + IR, backpack scout) | **ASPIRATIONAL** (separate accessory; not in spec) | Concept / "the dream" shots only |

When in doubt: the spec-accurate machine is the hero of blueprints; the arms+drone belong in the
"dream/concept" renders, watermarked as such.

---

## 6. The render / blueprint prompt pack
Palette for all: **matte charcoal body, warm bronze/copper accents, soft-touch TPU flanks, glowing
face**; technical diagrams in **blueprint style (indigo background, cyan/white linework)**.

### 6A · CANONICAL (spec-accurate — use for the real blueprints)

**A1 — Hero render (buildable Benzy)**
```
A premium ¾ product render of "Benzy", a Vector 3.0 desk companion robot, built to spec: ~105×80×130 mm, an emotive 1.54-inch face-display behind a convex glassy lens, on a compact rubber-tracked tank base, a short torso with a single front gripper/thumb, a small backpack bay on the rear, and a 4-mic ring at the top corners. Matte charcoal body, warm bronze/copper accents, soft-touch flanks, glowing eyes. Soft studio light, shallow depth of field, clean background. Cute but premium — a real creature, accurately proportioned.
```

**A2 — Exploded view (real components)**
```
A clean exploded-view engineering diagram of the Benzy robot with thin leader lines and numbered callouts, components separated vertically: the 1.54" IPS face LCD + convex lens; the camera cluster (IMX678 eye-contact + 2 OV9281 stereo + OV5647 rear fisheye); the XVF3800 4-mic ring; the VL53L8CX depth + MLX90640 thermal sensors; the RK3588S compute module; the STM32H743 safety MCU; the ICM-42688-P IMU; the tracked drive module with 4 BLDC motors; the native thumb/gripper; the 3S battery pack in the base; the speaker cavity; the copper heatsink + 25mm fan; the rear backpack bay. Blueprint aesthetic — dark indigo background, cyan/white technical linework, precise and labelled.
```

**A3 — See-through / x-ray internals**
```
A see-through "x-ray" render of Benzy with the charcoal shell as translucent glass and the internals glowing: the battery pack low in the base (low center of gravity), the RK3588S board vertical mid-body, the STM32H743 beside it, the copper heat-spreader + heatpipes + rear fan on the back wall, the camera cluster and face LCD at the front, the 4-mic ring at the top crown, the tracks low on the flanks. Neon cyan internal highlights on a dark body, cinematic and technical, with cutaway callouts naming each system.
```

**A4 — Blueprint orthographic plate (front / side / top)**
```
A technical blueprint plate of Benzy: front, side, and top orthographic views with dimension lines (≈105 mm wide, 80 mm deep, 130 mm tall), a title block, grid background, and callouts for the face display, camera cluster, mic ring, tracked base, thumb/gripper, and backpack bay. White/cyan lines on deep indigo, drafting-style, precise — like a real mechanical drawing.
```

**A5 — Benzy Station (Dock 2.0, spec-accurate)**
```
A product render of the "Benzy Station" dock: a charging cradle Benzy rolls into nose-first (USB-C PD), with a compute/LLM server housed inside (labelled: runs the slow reasoner + the ENGRAM memory archive), a room-mapping LiDAR puck on top, UWB anchors, and a local WiFi node. Matte charcoal with bronze accents, a soft status glow, Benzy half-docked. Warm, homey, premium — the creature's home base and its brain.
```

**A6 — Size & lineage vs the 2018 Vector**
```
A clean comparison render: the original 2018 Vector (100×80×115 mm) beside Benzy / Vector 3.0 (105×80×130 mm), same charcoal/bronze family look, with subtle dimension labels showing Benzy is slightly taller for its bigger battery and brain. Museum lighting, side by side, "same soul, new body" caption.
```

### 6B · ASPIRATIONAL (the Benzy dream — label as concept)

**B1 — Benzy with humanoid arms (concept)**
```
A concept render (labelled "concept — beyond current spec") of Benzy imagined with two small humanoid arms on its torso: a left tactile gripper and a right hand with an electromagnet tool, arms folded near the tracked base. Same charcoal/bronze Benzy design language as the canonical build. Premium concept-art lighting, clearly a future variant, not an engineering drawing.
```

**B2 — Benzy Sky (the scout drone, concept)**
```
A concept render of "Benzy Sky", a palm-sized prop-guarded scout quadcopter that docks in Benzy's backpack: a 50 MP camera and an IR/AR mapping sensor on the nose, charcoal-and-bronze to match, mid-hover scanning a room with faint mapping lines. Labelled "concept accessory." Sleek, friendly, technical.
```

**B3 — The three bodies (system concept)**
```
An elegant diagram "One creature, three bodies": LEFT — Benzy the tracked robot (the fast body, REFLEX); CENTER — the Benzy Station dock (charger + compute server running the LLM and the ENGRAM memory archive — the slow brain, MEANING); RIGHT — Benzy Sky the scout drone (eyes in the air, a concept accessory). Thin lines show power/data/vision flowing between them. Blueprint style, labelled; note the drone + arms are aspirational.
```

**B4 — Lineage (Cozmo → Vector → Benzy)**
```
A clean left-to-right evolution lineup: Cozmo (small forklift toy robot), Vector (the curved tracked desk companion), and Benzy (Vector 3.0 — slightly larger, face + tracked base + front gripper + backpack bay). Same family DNA across three generations, consistent charcoal/bronze palette, museum spacing with name + year labels. Caption: the same soul, a new body.
```

---

## 7. Style tokens & tips
- **Palette tokens:** `matte charcoal / graphite body`, `warm bronze + copper accents`, `soft-touch
  TPU flanks`, `glowing minimalist eyes`, `convex glassy face lens`.
- **Blueprint tokens:** `deep indigo background`, `cyan + white technical linework`, `leader lines +
  numbered callouts`, `dimension lines + title block`.
- **Accuracy anchors** (drop into any prompt to keep it Benzy): `tracked tank base`, `1.54-inch
  face display`, `4-mic ring at the top corners`, `single front thumb/gripper`, `rear backpack bay`,
  `~105×80×130 mm`.
- **If the customize box truncates (~500 chars):** paste the first 2 sentences of a prompt; the
  loaded sources fill in the components and layout.
- **Keep canonical and aspirational separate generations** — don't ask one image for "accurate
  exploded view" *and* "with arms and a drone"; you'll get a fictional machine.

---

## 8. Sources to load for these renders
- **This file** (`NOTEBOOKLM_BENZY_RENDER.md`) — the render brief.
- `research/BENZY_VECTOR_3_DESIGN_SPEC.md` — the three-body design + component manifest.
- `research/reports/12_vector3_hardware__V1_soc_revision.md` — the brain/SoC (RK3588S) + the dock split.
- `research/reports/13_vector3_hardware__V5_V14_full_spec.md` — audio, display, sensors, enclosure,
  thermal, the Dock 2.0, the full BOM (the master block diagram is here).
- `research/VECTOR_3_HARDWARE_GEODESIC.md` — the research brief the specs answer.
- *(optional)* the original sketch photos, if NotebookLM accepts the images.

> Raw-URL form (repo is public): swap the path onto
> `https://raw.githubusercontent.com/infraax/chimera-brain/refs/heads/claude/multi-repo-architecture-npf6jv/<path>`
