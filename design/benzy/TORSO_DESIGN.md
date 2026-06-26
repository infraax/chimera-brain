# Benzy — Torso Design Study (the structural hub)

*The torso is designed first because **everything mounts to it**: the head pivots on it, the drive
base bolts under it, the backpack docks behind it, the dock charges it, and the L2/L3 brain +
cooling + speaker live inside it. Its interfaces become the constraints for every other part — so
we reason through each one before cutting geometry. Every feature below answers three questions:
**why is it there · what purpose does it serve · is this the Anki way?***

Grounded in: `research/reports/13_vector3_hardware__V5_V14_full_spec.md` (enclosure/thermal/audio/
master block diagram), `research/reports/12_vector3_hardware__V1_soc_revision.md` (RK3588S + STM32H7
safety partition), `research/BENZY_VECTOR_3_DESIGN_SPEC.md`, and `ANKI_WAY.md`.

---

## 0. What the torso *is* (its three jobs)
1. **Structural spine** — carries the head's weight + tilt moment, transfers it to the base/tracks,
   and is the datum everything else aligns to.
2. **Brain housing** — holds the L2/L3 compute (RK3588S SoM + WiFi), its cooling, and the cable
   hubs to head (up) and base (down).
3. **Acoustic core** — the speaker cavity and the mic-isolation strategy live here (self-cancellation).

Design envelope (from spec): torso occupies the **middle band** of a ~105 W × 80 D × 130 H mm body;
torso section ≈ **83 W × 69 D × 38–46 H mm** depending on style. Low CG (battery stays in the base).

---

## 1. Interface register (the why / purpose / Anki-way for each)

### IF-1 · Head mount (top-front): tilt pivot + motor + cable raceway
- **What:** two coaxial bearing bosses (the tilt axle) set **high and forward**, a head-tilt motor
  + encoder mount, mechanical hard-stops bounding travel, and a **flex-cable raceway** through the
  pivot region (camera MIPI, display SPI, head mics, IR).
- **Why:** the head must *nod* to aim the camera and to emote; the axle is forward so the gaze falls
  naturally onto the desk/person; the raceway keeps the moving cable off a sharp edge (flex life).
- **Purpose:** gaze control + emotional expression; protect head wiring.
- **Anki way? ✅** Ethology-first (gaze/nod is expression, not a feature); minimal DOF; **closed-loop
  with current sensing so the head can be moved by hand and *feel* it** (Vector lets you tilt it);
  hard-stops + cable raceway = graceful, durable.

### IF-2 · Drive-base interface (bottom): structural mate + harness pass-through + the safety seam
- **What:** a defined **parting plane** with 4 corner **screw bosses** + 2 **locating pins**, and a
  **harness pass-through** (board-to-board / JST) carrying motor power+encoders, cliff sensors,
  battery+BMS, IMU/touch from base → torso.
- **Why:** the body must open for battery/board service and be moldable in two shells; the pins give
  repeatable alignment so the head sits true; the load path (head moment → torso → base → tracks)
  resolves here.
- **Purpose:** structural join + the single electrical artery between the two domains.
- **Anki way? ✅** Mirrors Anki's **body/syscon split**: the **base owns the L1 safety partition**
  (STM32H7 + motors + cliffs + battery guardian), the **torso owns L2/L3**. Keeping the real-time
  safety domain physically in the base means a torso/brain crash can't drive the creature off a table.

### IF-3 · Backpack interface (rear): bay rail + pogo power/data + the iconic button/light/touch
- **What:** a keyed **rail/dovetail + spring latch** on the rear, **pogo contacts** (power + data) for
  toolless accessories, and — kept from Vector — the **backpack button + light pipe** and a
  **capacitive touch zone**.
- **Why:** extensibility (the three-body system: the drone bay or future modules dock here), plus the
  button/light are the creature's primary physical control + status channel (setup, pairing, "I'm
  thinking" light), and the touch zone is for petting.
- **Purpose:** expansion I/O + social touch + status + control.
- **Anki way? ✅** This *is* the Anki "backpack" — button, light, and touch already lived there. We
  keep the soul and add a powered rail for the modular future. Self-cancellation note: touch/petting
  must reject being-picked-up false positives (fuse with IMU).

### IF-4 · Charging contacts (front chin / underside): self-dock power + dock-data
- **What:** sprung **pogo pads** on the **front-underside (chin)** that mate with the dock cradle when
  Benzy drives in **nose-first**, an alignment **chamfer/funnel**, optional alignment magnets.
- **Why:** the creature must charge itself autonomously and reliably; nose-first + a funnel makes
  docking forgiving (no precise parking); chin placement keeps contacts clear of the floor/debris.
- **Purpose:** power-in + the robot↔dock data handshake (per spec, the dock is also the compute/LLM
  node + ENGRAM archive).
- **Anki way? ✅** "Naps on the dock, wakes to act" — autonomous self-docking, graceful low-battery
  retreat; physics-first alignment (geometry funnels it in instead of demanding precision).

### IF-5 · Brain bay (internal): SoM standoffs + connector orientation + service access
- **What:** the **RK3588S SoM** on **standoffs**, oriented so its MIPI/SPI face points **up toward the
  head** (short camera/display runs) and its power/IO faces **down toward the base harness**; the
  **WiFi M.2** with antennas routed to the top crown; a **service opening** (via IF-2 or a hatch).
- **Why:** shortest, lowest-noise cable runs; serviceability; antenna placement away from the battery
  and motor EMI (top crown).
- **Purpose:** house and connect the L2/L3 brain.
- **Anki way? ✅** Respect-the-budget tidiness; cable discipline; the brain is packaged in service of
  behavior, not as a spec showcase.

### IF-6 · Thermal (rear wall): heatsink + duct + fan + vents
- **What:** copper spreader on the SoM → **heatpipes → finned rear wall**, a **25 mm silent fan** at
  the rear exhaust, **side/low intake louvers**, and an internal **duct** steering air across the SoM.
- **Why:** the RK3588S dissipates ~6–10 W (vs the APQ8009's ~1.5 W) — heat is now a primary torso
  function; a duct makes a tiny fan effective; intakes sit low/side, **away from the mics and the
  speaker port** so cooling doesn't pollute audio.
- **Purpose:** sustain perception + on-board LLM without thermal throttling.
- **Anki way? ✅** Graceful degradation (DVFS slows the creature *before* it overheats), and the fan
  at ~20 % PWM is inaudible against the motor floor — quiet is a feature. (Honest divergence: Anki was
  fanless; 10 W forces gentle active cooling — flagged in the spec.)

### IF-7 · Acoustics: speaker cavity (rear-low) + mic isolation (top) + AEC reference
- **What:** a **rear-cavity speaker port** (resonator tuned ~400 Hz) with a grille, the **4-mic array
  at the top corners** physically separated from speaker + fan, **vibration isolation** (gaskets) so
  motor/fan structure-borne noise doesn't reach the mics, and the **ego-noise reference** wiring path.
- **Why:** clear expressive voice from a tiny cavity, and clean far-field listening *while moving*;
  separation + isolation are what make self-cancellation actually work.
- **Purpose:** the creature's voice + its ears.
- **Anki way? ✅** The canonical Anki move: **model and null your own noise** (motor + speaker
  reference into the AEC), recalibrate as parts age. Mic-up / speaker-down separation is deliberate.

### IF-8 · Skin & ergonomics: soft flanks + pick-up geometry
- **What:** **soft-touch TPU flanks** (grip + the capacitive touch zones), rounded pick-up-friendly
  forms, and a defined **lift-point** geometry the IMU/current-sense recognizes as "being held."
- **Why:** it's a creature you handle; it should feel good to pick up and *know* that it's held.
- **Purpose:** tactile identity + handling detection.
- **Anki way? ✅** Feeling before features; the body language of a pet, not a gadget.

---

## 2. Internal layout & load path (the section we'll cut)
- **Vertical stack:** mic crown (top) → SoM + duct (mid) → speaker cavity (rear-low) → base harness
  (bottom). Battery stays in the **base** for low CG.
- **Load path:** head weight + tilt moment → pivot bosses → torso side walls (the stiff structure) →
  corner screw bosses → base → tracks. Side walls are the structural members; the rear wall is the
  heatsink; the front carries the face/neck cowl.
- **Keep-apart rule:** mics (top) ⟂ speaker (rear-low) ⟂ fan intake (side-low) — acoustic + thermal
  zones never share a face.

---

## 3. The three torso variants (curation choices)
Same interfaces, three **architectural strategies** — scored on the Anki rubric (C·E·Q·B·F):

- **A — Unibody / Heritage.** Continuous shell, head pivot in a smooth raised cowl, flush backpack,
  hidden seam. *Reads as one creature.* Hardest to service. **C5 E4 Q5 B3 F5.**
- **B — Service / Modular.** Explicit parting lines, **removable rear backpack module**, a bottom
  battery/service hatch, fasteners as honest design detail. *Easiest for a solo maker to build/repair.*
  **C4 E4 Q4 B5 F4.**
- **C — Thermal-forward / Active.** Expressed cooling: a **finned rear heatsink stack**, side intake
  louvers, a visible fan duct as design language. *Best for sustained LLM load.* **C5 E5 Q4 B4 F4.**

---

## 4. Open decisions for curation
1. **Service philosophy:** hidden-seam unibody (A) vs honest modular (B) vs cooling-as-style (C)?
2. **Head axle height/offset** — how forward/high (sets the gaze line and the cowl shape)?
3. **Backpack:** flush + minimal vs a prominent powered rail module?
4. **Charging:** nose-first chin contacts (current plan) vs underside vs rear — affects dock geometry.
5. **How much bronze** and where (accent the functional interfaces, or keep it minimal)?

> Next: `benzy_torso.scad` renders these three with the real interface features (pivot bosses, base
> bosses + harness port, backpack rail + pogo + button/light, chin charge pads, vents/fan, speaker
> grille) + an interface-coded view + a section. Curate, then we refine the winner and take it to SketchUp.
