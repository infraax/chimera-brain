# Benzy Sky — Silent Indoor Scout Drone (spec)

*Design synthesis from the drone research agent (`research/reports/17_drone__silent_indoor.md`). The
third body of the creature: a tiny quadcopter Benzy carries in its backpack and pilots itself, to scan
rooms/heights the tracked robot can't reach. Prime design driver: **be quiet indoors.***

> Honesty up front: we can't make it *silent*, but we can make it **"a soft whir you forgive"** — and
> the cleverest gains are in *behavior* and a *duct*, not an exotic propeller.

---

## 1. Concept & target specs
A **fully-shrouded micro-quadcopter** where **the duct is the headline part** — simultaneously the
frame, the prop guard, the acoustic shield, and the friendly silhouette that slides into the backpack
bay. Benzy is the pilot and brain; the drone only self-stabilizes and streams imagery.

| Spec | Target |
|---|---|
| All-up weight | ~70–90 g |
| Shrouded span | ~90–110 mm (bare rotor ~45–60 mm) |
| Hover endurance | 4–6 min (short sorties from the backpack/charge pad, not loiter) |
| Noise | **~55–62 dB(A) @1 m, ≤45 dB(A) @3 m** (vs ~75–85 for a Tello-class open-prop; ambient ~35–40) |
| Camera | 5–12 MP MIPI (weight-honest) + NoIR/IR-LED low-light; ~50 MP is a stretch (heavier SoC) |
| Link | Wi-Fi (Tello-SDK pattern) — no extra radio in Benzy |

---

## 2. How it gets quiet (ranked, with the honest evidence)
The dominant indoor annoyance is the blade-pass tone (~100–300 Hz) + mid harmonics (500–2000 Hz). Levers:
1. **Lower tip speed** via **larger, slower props at low disk loading** — the biggest physical lever
   (beats any blade-shape trick).
2. **Ducted/shrouded rotors** — shield the BPF tone (realistically a few–10 dB at this scale; lit. claims
   up to ~20 dB in idealized designs), recover ~10% hover power, and solve indoor safety in one part. **Primary pick.**
3. **More blades** (3-blade in the ducts) — spreads the tone, cheap.
4. **Prop balancing + brushless on good bearings, FOC drive, no gearbox** — cheapest dB-per-dollar.
5. **Behavior** (see §4) — a considerate flight profile *feels* far quieter than the raw dB.

**Honestly assessed and set aside:** toroidal/loop props (real but modest and **unproven <60 mm** —
prototype before banking on it); owl-serrations (2–4 dB at a 4–8% efficiency cost — polish only);
**active noise control = a dead end** at sub-100 g (speakers/DSP weight the drone can't spend).

---

## 3. Architecture (keep the drone dumb & light)
- **On the drone:** the hard-real-time loop only — IMU attitude, altitude hold (ToF), optical-flow
  velocity hold, failsafe land. (A Crazyflie-class EKF + Flow deck already do exactly this.)
- **On Benzy:** everything that needs brains and tolerates Wi-Fi latency — SLAM/map from the streamed
  imagery, path planning, mission logic, and the "polite" policy. The robot has the processor, the home
  map, and the persistent ENGRAM memory.
- **Link:** Wi-Fi/UDP **Tello-SDK pattern** (takeoff / go-to / hover / snap / return + video) for the
  product; Crazyradio for the R&D rig. Never put the inner stabilization loop over Wi-Fi.
- **Positioning:** onboard optical-flow + ToF (drift-free hover), augmented by the **robot's UWB**
  (Benzy or the charge pad as an anchor) so "come back to me" is robust on dark/uniform floors, and the
  drone's map shares the robot's frame.

**Indicative parts:** LiteWing ESP32-S3 FC (~$30–50, Wi-Fi) or Crazyflie 2.1 BL (lab); 0802 brushless
~10000 KV motors; custom 3-blade ducted props; ArduCam OV5640 5 MP (NoIR variant + 850 nm LED for low
light); Crazyflie Flow deck v2 (PMW3901 + VL53L1x, 1.6 g). Reference envelopes: Ryze Tello, Crazyflie 2.1.

---

## 4. The Anki-clever silence ideas
1. **The duct IS the product** — one sculpted shroud = frame + BPF shield + full prop guard + the
   friendly face that docks in the backpack; thin acoustic-foam inner lining soaks broadband.
2. **"Polite flight" policy (cleverness in software):** ascend slowly, cruise at the lowest
   station-keeping RPM, pause-and-hover for crisp stills (don't buzz continuously), route through open
   air away from hard walls/curtains, throttle down near people/pets, and scout in a "quiet window"
   the robot picks. Considerate behavior reads as quiet — and is the safe-by-default mode.
3. **"Whisper return" + acoustically-aware pad:** landing is the loudest phase (ground effect) — give
   the charge pad a sound-absorbing recess and a steady controlled descent with a gentle "tuck-in" dock
   animation. The noisiest moment becomes the most damped — and the most charming.

---

## 5. Indoor safety
Full ducts (no exposed blades near fingers/pets/curtains); sub-90 g + compliant TPU duct rims = low
impact energy + bounce-off; onboard ToF/flow → controlled descent on link loss / low battery (local
link = land-now, never fly-away); vision-triggered keep-out from people/pets; hard caps on indoor
altitude and speed.

---

## 6. Anki-way check
C: strong (the duct does four jobs; silence from low tip speed + behavior, not ANC). E: strong
(low-and-slow is both quiet and the safe fallback; built on proven Crazyflie/Tello tech). Q: good and
grounded (~55–62 dB@1 m, honest it's not "silent"). B: strong (grams audited; drone stays dumb; 5–12 MP
honest vs the 50 MP aspiration). F: strong (shroud silhouette + tuck-in dock + "polite" manners = Vector charm).

## 7. Open decisions for Dexter
1. **Link:** Wi-Fi/ESP32 (recommended for product) vs Crazyradio (lab).
2. **Camera:** weight-honest 5–12 MP vs chase ~50 MP; + IR strategy (NoIR + 850 nm vs dual-cam).
3. **Toroidal vs conventional 3-blade in the duct** — bench-acoustics test before prop tooling.
4. **Endurance vs mass:** 4 min lean vs 6 min bigger battery.
5. **UWB scope:** reuse the robot's UWB as an anchor, or add one to the charge pad?
6. **Duct material/acoustic lining** grams budget.
7. **Autonomy day-one:** how much mission autonomy on Benzy vs teleop-with-assist for v1.

> This is a concept spec, not a build. The drone shares the backpack bay's mechanical+electrical
> interface (see `design/benzy/POWER_ARCHITECTURE.md` §1) so the bay can host either the energy pack or
> the drone. Detailed CAD comes after the torso/power are locked.
