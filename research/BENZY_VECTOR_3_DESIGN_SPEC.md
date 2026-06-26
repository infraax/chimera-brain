# Benzy — Vector 3.0 Design Spec ("the creature with three bodies")

*A generation-ready product/design specification for **Benzy**, the clean-sheet Vector 3.0,
derived directly from Dexter's hand sketches (May planning pages). This is the concrete design
doc — the companion to `research/VECTOR_3_HARDWARE_GEODESIC.md` (the research geodesic). Its job
is twofold: (1) be a precise, buildable description of the design, and (2) be rich enough that an
image generator (NotebookLM slides/video, or a 3D tool later) renders **Benzy specifically** and
consistently — not a generic cute robot. §8 holds the ready-to-paste image prompts.*

> Status: concept design, sketch-derived. Details are deliberately changeable — feasibility tiers
> in §7 mark what's near-term vs aspirational, in the project's honest spirit.
>
> **Canonical hardware now exists.** The Vector 3.0 engineering research came back (V1 + V5–V14):
> `research/reports/12_vector3_hardware__V1_soc_revision.md` and
> `research/reports/13_vector3_hardware__V5_V14_full_spec.md`. Where this sketch-derived spec and the
> engineering reports differ, the reports win on parts (e.g. the brain is an **RK3588S**, not the
> sketch's RPi5). For accurate renders/blueprints use `NOTEBOOKLM_BENZY_RENDER.md`, which fuses both.

---

## 1. What Benzy is

**Lineage (as sketched): Cozmo → Vector → Benzy.** Benzy is the third creature in the line —
same Anki soul (a small companion robot with real *feeling*, built clever-over-brute-force), but
on 2026 hardware and with a body that can finally *act on* and *reach into* the world instead of
only trundling across a desk.

The leap from Vector to Benzy is three moves:
1. **Hands** — humanoid arms, so the creature can manipulate, not just bump.
2. **A brain that lives in its home** — the charging dock doubles as the compute/LLM server.
3. **Flight** — a detachable scout drone for the places a tracked robot can't reach.

Benzy is the **embodiment target** for chimera-brain: ENGRAM is its memory, the two senses are
its nervous system, and these three bodies are where they run.

---

## 2. The three-body system (and how it maps to our architecture)

Benzy isn't one device; it's a **trio that shares one mind**. This is the sketch's deepest idea,
and it lines up exactly with the two-rate ENGRAM design.

| Body | Sketch source | Role | Maps to |
|---|---|---|---|
| **Benzy (robot)** | IMG_4772, 4771 | The body on the ground: senses, drives, manipulates. Fast, instinctive, always-on. | **REFLEX sense** — raw fused sensation → fingerprint, on-board (RPi5). |
| **Benzy Station (dock)** | IMG_4773 | Home base: charges Benzy, and *houses the compute* that runs the LLM + slow understanding + the memory archive. | **MEANING sense** + the ENGRAM archive — learned embeddings, on the "box". |
| **Benzy Sky (drone)** | IMG_4774, 4775 | Detachable quad scout: flies where Benzy can't drive, maps and scans rooms, returns images. | A new **perception organ** feeding both senses; aerial SLAM/mapping. |

The robot handles the world in real time; the dock thinks slowly and remembers deeply; the drone
extends perception into the third dimension. One creature, three bodies, one ENGRAM.

---

## 3. Benzy — the robot (ground body)

**Overall form.** A Vector-descended silhouette scaled up: a friendly **head** that tilts and
emotes on a compact **tracked drive base**, with a **torso** between them carrying two
**humanoid arms** and, on the back, a **modular backpack bay**. Low center of gravity (heavy
battery in the base), tracks for stability and the signature Anki "tank" charm.

### 3.1 Head ("Vector head", evolved) — IMG_4772
- **Face display** — the emotive screen (Benzy's "eyes"); the soul of the creature, kept from Vector.
- **Camera cluster** — front HDR camera + an ultra-wide for situational awareness; optional small
  rear/surround cams (toward the geodesic's "surround vision").
- **Far-field mic array** + speaker — voice, and self-cancellation of its own motor/track noise
  (the Anki Way).
- Tilts/pans on a neck actuator for gaze and expression.

### 3.2 Perception — IMG_4771, 4772
- **LiDAR / AR-movement sensor** (solid-state ToF) — navigation, obstacle and depth mapping.
- **IR depth + cliff/ToF sensors** — edge safety, close-range depth.
- **IMU** (accel + gyro) — pose, pickup detection, balance of the arms.
- Time-synced so REFLEX fingerprints fuse a coherent instant.

### 3.3 Drive — "Vector drive basis" — IMG_4772, 4771
- **Rubberized tracks**, two independent drive motors — climb small thresholds, turn in place.
- Designed to dock nose-first into the Benzy Station.

### 3.4 Arms & hands ("humanoid arms") — IMG_4772, 4771
- **Two arms**, ~4 DoF each, shoulder-mounted on the torso.
- **Right hand: electromagnet end-effector** — "if metal, activate" — pick up paperclips, keys,
  small steel objects (a genuinely Benzy trick).
- **Left hand: tactile gripper** with **pressure sensors** (the "native thumb" from the geodesic) —
  feel contact, grip force, simple manipulation.
- Arms tuck/fold when driving; safety-partitioned, force-limited (Anki Way: a creature that can
  touch must touch *gently*).

### 3.5 Brain & power — IMG_4771
- **Onboard compute: RK3588S SoM** (Radxa NX5; the sketch said "big CPU RPi5" — the engineering
  spec settled on the more capable RK3588S with a 6-TOPS NPU) + an **STM32H743** real-time safety
  MCU. Runs the **REFLEX** tier and on-robot L2/L3: sensor fusion, fingerprinting, motion, safety.
- **Large battery** in the base — hours of runtime; recharges on the dock.
- Heavy compute (the LLM, MEANING sense) is deliberately **offloaded to the dock** — keeps the
  robot cool, cheap, and long-lived (respect the budget).

### 3.6 Backpack bay — IMG_4774
- A **modular dock on Benzy's back** that carries and charges the **Benzy Sky** drone, or other
  attachments. Pogo-pin power + data; mechanical latch.

### 3.7 Look & finish (for consistent renders)
- Matte charcoal/graphite body with **warm bronze/copper accents** (the palette from the slide
  you liked), friendly rounded forms, a glowing face display. Premium-toy-meets-companion-robot.

---

## 4. Benzy Station — the dock & brain — IMG_4773

- **Charging cradle** Benzy drives into nose-first (pogo contacts; self-aligning ramp).
- **Compute server inside** — "Benzy Station + compute (LLM)": a more powerful SBC (e.g. Jetson
  Orin / mini-PC / RPi-cluster) that runs the **on-prem LLM**, the **MEANING sense** (slow,
  embedding-based), and stores the **ENGRAM archive** (the creature's long memory). Private,
  local, no cloud required.
- **Drone pad on top** — integrated **"H" landing/charge pad** for Benzy Sky.
- Quiet, well-ventilated, lives on a shelf or desk like a little home for the creature.

This is the literal hardware for the project's "box" tier — the slow brain that lives at home
while the fast body roams.

---

## 5. Benzy Sky — the scout drone — IMG_4774, 4775

- **Micro quadcopter** (DJI-Tello-inspired), prop-guarded, palm-sized — lives in Benzy's
  backpack bay, **detaches to fly**.
- **50 MP camera** — high-res capture for scanning and mapping.
- **Infrared + AR mapping** — builds room maps, sees in low light, reaches shelves/rooms Benzy
  can't drive to.
- **Lands & charges** on the Station's "H" pad (or a standalone charge pad).
- **Role in the mind:** an aerial perception organ. It flies a sweep, captures the space, and the
  images flow back into perception → ENGRAM, giving the creature a memory of places its wheels
  never touched.

---

## 6. Exploded-view component manifest (for diagrams/renders)

Numbered parts for exploded and see-through graphics. Use these labels verbatim in callouts.

**Benzy (robot)**
1. Emotive **face display** (head)
2. **Camera cluster** (front HDR + ultra-wide)
3. **Far-field mic array + speaker**
4. **LiDAR / AR-movement sensor**
5. **IR depth + cliff sensors**
6. **Neck tilt/pan actuator**
7. **Left arm** — tactile gripper w/ **pressure sensors**
8. **Right arm** — **electromagnet** end-effector
9. **Torso shell** (arm mounts)
10. **Raspberry Pi 5 / CM5 compute board** (REFLEX brain)
11. **IMU**
12. **Tracked drive module** (motors + treads — "Vector drive basis")
13. **Main battery pack** (base)
14. **Backpack bay** (drone dock, rear)

**Benzy Station (dock)**
15. **Charging cradle** + pogo contacts
16. **Compute server / SBC** (LLM + MEANING + ENGRAM archive)
17. **Cooling / vents**
18. **Drone "H" landing-charge pad**

**Benzy Sky (drone)**
19. **Quad frame** + **prop guards**
20. **50 MP camera**
21. **IR + AR mapping sensor**
22. **Drone battery + landing feet**

---

## 7. Feasibility tiers (the honest cut)

Keeping the project's honesty boundary — what's realistic vs. a stretch:

- **MUST (near-term, clearly buildable):** Vector-style head + face, tracked base, camera, mic
  array, IMU, RPi5 brain, battery, dock-as-charger, the drone as a *separate* off-the-shelf quad
  (Tello-class) whose images we ingest.
- **SHOULD (feasible with effort):** LiDAR/ToF + IR depth, dock-as-compute (LLM box), pressure-
  sensing gripper, backpack bay, drone IR/AR mapping pipeline.
- **STRETCH (aspirational — flag honestly):** two dexterous humanoid arms on a small mobile base
  (power, weight, safety, cost are real), the electromagnet manipulation as a reliable everyday
  feature, fully autonomous drone launch/land/recharge from Benzy's back.

None of this is mysticism — it's an honest ladder from "ship this" to "dream this".

---

## 8. Image-generation prompt pack (paste into NotebookLM Studio)

Add **this file** as a source (and the sketch images if NotebookLM accepts them), then paste a
prompt below. Keep visual-box prompts short if the box truncates — the source carries the detail.
Palette for all: matte charcoal body, warm bronze/copper accents, soft studio light; blueprint
(indigo + cyan line) style for the technical diagrams.

**A — Hero render (the pitch shot)**
```
A premium ¾ product render of "Benzy" — a Vector 3.0 companion robot: a friendly emotive face-display head that tilts, on a compact rubber-tracked tank base, with a torso carrying two small humanoid arms (left hand a tactile gripper, right hand an electromagnet tool), and a backpack bay on the rear holding a tiny quadcopter. Matte charcoal body, warm bronze/copper accents, glowing face. Soft studio lighting, shallow depth of field, clean background. Cute but premium — a real creature you'd want on your desk.
```

**B — Exploded view (separated components)**
```
A clean exploded-view diagram of the Benzy robot, components separated along vertical and horizontal axes with thin leader lines and numbered callouts: face display, camera cluster, mic array, LiDAR/AR sensor, IR/cliff sensors, neck actuator, left tactile gripper arm, right electromagnet arm, torso shell, Raspberry Pi 5 brain board, IMU, tracked drive module, main battery, rear backpack bay. Blueprint aesthetic — dark indigo background, cyan/white technical linework, precise and labelled.
```

**C — See-through / ghosted internals**
```
A see-through "x-ray" render of Benzy: the charcoal outer shell rendered as translucent glass so the internals glow inside — highlight the Raspberry Pi 5 brain board, the main battery in the base, the track motors, the LiDAR module in the head, and the arm actuators. Neon cyan internal highlights against a dark body, cinematic and technical. Cutaway callouts naming each highlighted system.
```

**D — The three bodies (system diagram)**
```
A single elegant diagram titled "One creature, three bodies": LEFT — Benzy the tracked robot (the fast body); CENTER — the Benzy Station dock (charger + compute server running the LLM and the memory archive — the slow brain); RIGHT — Benzy Sky, the scout quadcopter (eyes in the air). Thin connecting lines show power/data/vision flowing between them. Blueprint style, labelled, premium. A caption: the robot acts, the dock remembers, the drone scouts.
```

**E — Benzy Station (dock + brain)**
```
A product render of the "Benzy Station": a charging cradle the tracked robot docks into nose-first, with a compute server housed inside (labelled: runs the on-prem LLM, slow understanding, and the ENGRAM memory archive) and an "H" drone landing-charge pad on top. Matte charcoal with bronze accents, a glowing status light. Show Benzy half-docked and the little quadcopter resting on the pad. Warm, homey, premium.
```

**F — Benzy Sky (the drone)**
```
A close product render of "Benzy Sky", a palm-sized prop-guarded scout quadcopter that lives in Benzy's backpack: a 50 MP camera on a small gimbal and an IR/AR mapping sensor on the nose, charcoal-and-bronze to match the robot, mid-hover scanning a room with faint mapping lines projecting from its sensor. Landing on an "H" charge pad in the background. Sleek, friendly, technical.
```

**G — Lineage (Cozmo → Vector → Benzy)**
```
A clean evolution lineup, left to right: Cozmo (small forklift toy robot), Vector (the curved tracked desk companion), and Benzy (the new Vector 3.0 — bigger, head + tracked base + two humanoid arms + backpack drone). Same family DNA growing across three generations, consistent lighting, charcoal/bronze palette, museum-style spacing with subtle name labels and year tags. A caption: the same soul, a new body.
```
