# Benzy Sky — Tiny Silent Indoor Drone (research agent report)

*Returned by a research agent, 2026. Topic: a very small, quiet, Benzy-piloted scout drone. Fused into
`research/BENZY_SKY_DRONE.md`.*

## TL;DR
- **The win is flight behavior + a duct, not a magic propeller.** Dominant indoor annoyance = blade-pass
  tone (~100–300 Hz) + mid harmonics (500–2000 Hz). Biggest physical lever = **lower tip speed via
  larger, slower props at low disk loading**; cleverest lever = **operating profile** (fly slow, close,
  low-RPM; let the robot think so the drone stays tiny).
- **Ducted/shrouded rotors are the best Anki-clever structural choice**: shields the BPF tone (lit.
  claims up to ~20 dB ideal; realistically a few-to-10 dB at this scale), recovers ~10% hover power, AND
  is the indoor-safety answer (no exposed blades) — one part, multiple jobs. Toroidal props are real but
  modest/unproven at micro scale; owl-serrations give 2–4 dB at 4–8% efficiency cost. **Active noise
  control is a dead end at this size.**
- **Recommended: a Crazyflie-class ducted nano-quad, ~70–90 g AUW, ~90–110 mm shrouded span, 4–6 min
  hover, target ~55–62 dB(A) @1 m** (vs ~75–85 for a Tello-class open-prop), piloted by Benzy over Wi-Fi
  (Tello-SDK pattern), with onboard optical-flow + ToF and SLAM/mapping offloaded to the robot.

## Why it's loud & the biggest levers (ranked)
1. **Disk loading / tip speed** (biggest) — tiny rotor → high RPM → high tip speed → loud whine; fix:
   larger diameter, lower RPM. Halving tip speed beats any blade trick.
2. **Blade-pass frequency + harmonics** — fundamental 100–300 Hz, harmonics to several kHz in the most
   annoying band; fix: more blades / duct shielding / lower RPM.
3. **Tip vortices** — air spilling around blade tips; fix: a shroud kills tip leakage (also adds thrust).
4. **Inflow turbulence / room reflections** — avoid hugging walls (robot plans paths); acoustic pad on return.
5. **Motor/drivetrain whine** — quality brushless on good bearings, FOC drive, no gearbox, meticulous
   prop balancing (cheapest dB-per-dollar fix).

## Quiet-propulsion options
| Approach | Measured effect | Tradeoff | Verdict |
|---|---|---|---|
| **Ducted/shrouded rotor** | up to ~20 dB ideal; realistically few–10 dB; can raise broadband >7×BPF | +~4% thrust, ~10% less hover power; +wetted area/weight | **PICK (primary)** + safety |
| **Larger-dia, lower-RPM, low disk loading** | the dominant physical lever (no single headline #) | bigger footprint, less agility | **PICK (co-primary)** |
| **More blades** | noise ↓ with blade count at fixed thrust | slight efficiency/mass cost | **Adopt (cheap)** — 3-blade in ducts |
| **Toroidal/loop prop (MIT)** | axial −19.6 dB(A), radial −5.2 dB(A); config-specific, unproven <60 mm | comparable thrust; hard to mold tiny/balanced | **Prototype/optional** |
| **Owl serrations** | ~2–4 dB | 4–8% FoM penalty | **Maybe (polish)** |
| **Active noise control** | ~9.4 dB lab; global only at low f | speakers/DSP weight a 70 g drone can't spend | **REJECT at this scale** |

## Recommended platform
Fully-shrouded micro-quad, ~70–90 g AUW, where **the duct is the headline element** (frame + prop guard
+ acoustic shield + friendly "face"). Four small brushless motors swinging the largest props the ducts
allow at the lowest hover RPM. Robot is pilot+brain; drone runs only stabilization + streams imagery.
Default "polite flight envelope": slow ascents, hover-pauses for stills, proximity-aware low-and-slow.
Specs: shrouded span ~90–110 mm; bare rotor ~45–60 mm; AUW ~70–90 g; hover 4–6 min; ~55–62 dB(A)@1 m,
≤45 dB(A)@3 m (ambient ~35–40).

## Key parts
- FC/radio: Crazyflie 2.1 Brushless board (STM32+nRF51, open EKF) ~$215 kit; or **LiteWing ESP32-S3**
  (~$30–50, Wi-Fi, Tello-style) for the Benzy-pilots-it path.
- Motors: 0802-class brushless ~10000 KV (~30 g thrust ea) ~$8–12.
- Props: custom 3-blade sized to fill the ducts ~$2–5/set.
- Camera (day): ArduCam OV5640 5 MP ~$15–25 (has IR-cut — not for low light as-is); ~50 MP needs a
  phone-class MIPI sensor + heavier SoC (treat as stretch; 5–12 MP is weight-honest).
- IR/low-light: NoIR sensor variant + 850 nm IR LED ~$5–15.
- Positioning: Crazyflie Flow deck v2 (PMW3901 optical flow + VL53L1x ToF, 1.6 g) ~$45.
- Reference envelopes: Ryze **Tello** (80 g, 13 min, 5 MP, Wi-Fi + open SDK); **Crazyflie 2.1** (27 g,
  ~7 min, 40 g payload).

## Control & positioning
- **Link:** Benzy = ground station. Wi-Fi/UDP **Tello-SDK pattern** (high-level: takeoff/go-to/hover/
  snap/return + video stream) for the consumer build (no extra radio in Benzy); Crazyradio for the R&D rig.
- **Compute split (keep the drone dumb+light):** on-drone = attitude/altitude/optical-flow hold + failsafe
  land (the Crazyflie EKF + Flow deck already do this); on-Benzy = SLAM/map, planning, mission, "polite"
  policy (the robot has the processor, the home map, and persistent memory).
- **Positioning:** primary onboard optical-flow + ToF; augment with the **robot's UWB** (Benzy/charge-pad
  as anchor) for a robust "come back to me" + shared map frame.

## The Anki-clever silence ideas
1. **The duct IS the product** — one sculpted shroud = frame + BPF shield + full prop guard + friendly
   silhouette that slides into the backpack; thin acoustic-foam inner lining for broadband.
2. **"Polite flight" policy (cleverness in software):** ascend slowly, cruise at lowest station-keeping
   RPM, pause-and-hover for stills, avoid hard walls, throttle near people/pets, scout in a "quiet window."
   Considerate behavior *feels* far quieter than the raw dB — and doubles as the safe-by-default mode.
3. **"Whisper return" + acoustically-aware pad:** landing is the loudest phase (ground effect) — give the
   charge pad a sound-absorbing recess and a steady controlled descent + a gentle "tuck-in" dock animation.

## Indoor safety
Full ducts (no exposed blades); sub-90 g + compliant TPU duct rims = low impact energy + bounce-off;
onboard ToF/flow → controlled descent on link loss/low battery (local link = land-now, never fly-away);
vision-triggered keep-out from people/pets; hard caps on indoor altitude/speed.

## Anki-way check
C: strong (duct does 4 jobs; silence from low tip speed + behavior, not ANC). E: strong (low-and-slow =
quiet *and* safe fallback; built on proven Crazyflie/Tello tech). Q: good/grounded (~55–62 dB@1 m honest;
not "silent" but "a soft whir you forgive"). B: strong (grams audited; drone dumb; 5–12 MP honest vs 50 MP).
F: strong (shroud silhouette + tuck-in dock animation + "polite" manners = Vector-style charm).

## Risks / confidence
Low: toroidal micro-scale claims (validate empirically). Medium: duct dB at micro scale (expect few–10 dB,
measure on the real rotor/duct); the 50 MP+IR+sub-90 g+4–6 min combo (likely lands at 5–12 MP + NoIR/IR-LED);
endurance (plan short sorties from the backpack pad); Wi-Fi latency (OK only because the drone self-stabilizes).
High: ANC correctly ruled out.

## Open decisions for Dexter
1. Link: Wi-Fi/ESP32 (no extra radio, recommended for product) vs Crazyradio (lower latency, lab).
2. Camera: weight-honest 5–12 MP vs chase ~50 MP (heavier SoC, less endurance); + IR strategy.
3. Toroidal vs conventional 3-blade in the duct — bench-acoustics test before tooling.
4. Endurance vs mass: 4 min lean vs 6 min bigger battery.
5. UWB scope: reuse the robot's UWB as anchor, or add one to the charge pad?
6. Duct material/acoustic lining: TPU rim + foam grams budget.
7. Mission autonomy on Benzy day-one vs teleop-with-assist for v1.
