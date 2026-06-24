# RESEARCH GEODESIC — Physical Attachments: the Rover-Cube, the Thumb, and the Desk Arms
## Giving Vector new ways to sense, touch, and manipulate the world — the Anki way
## Created: 2026-06-24 · Dexter × Claude Opus 4.8

> **How to use:** hand each *vector* to a research agent. Return findings in the **Output** format.
> This is hardware + 3D-design + sensing + control. Favor light, 3D-printable, open-hardware, buildable.

---

## PRIME DIRECTIVE
> *Design three classes of physical attachment that expand what Vector can sense, feel, and do — without
> bloating the robot or draining it — each at Anki-grade engineering quality:*
> 1. **An improved "Rover-Cube"** — a redesigned cube carrying high-value sensors Vector lacks (LiDAR/ToF,
>    thermal, 360 camera, env sensors), which Vector picks up / drives around with to map the world like a
>    Google-Maps car.
> 2. **The "Thumb"** — a universal, ultra-light, 3D-printable lift attachment with **force/pressure & material
>    sensing**, turning Vector's lift into a finger that can *feel* — measure how hard it must push, how hard a
>    thing is — the opposable "thumb" that multiplies what its hands can do.
> 3. **Two desk robot arms** on top of the Vector-Brain box, controlled by Vector, with a "control area" where
>    Vector can deliver objects (push/carry them over) and have the arms manipulate them — e.g. rotate a box to
>    3D-model it — so Vector doesn't have to drive around an object to understand it.

**The bar:** Anki-grade. Light, elegant, clever, genuinely useful — the goal is to *expand Vector's ability to
experience and feel the world*, not to bolt on gadgets. The Thumb especially must let Vector **touch reality**
and *prove* what it feels by testing (press, measure, infer hardness/force) — like a human thumb accelerates
what a hand can do.

---

## CROSS-CUTTING CONSTRAINTS
1. **Weight & power are sacred:** anything Vector lifts/carries must be within its **lift payload & motor
   limits** (research the real numbers from `kercre123/victor` / TRM) and ideally self-powered (own tiny
   battery) so it doesn't drain Vector. 3D-printable, minimal mass.
2. **Anki-grade sensing:** force/touch sensing must be *calibrated, self-aware, drift-corrected* (the
   motor-noise-nullification ethos applied to a tactile finger).
3. **Open & buildable:** off-the-shelf sensors, open hardware (ESP32/RP2040, FSR/load-cell/tactile),
   open arm platforms; realistic cost; printable on a hobby printer.
4. **Vector stays in control:** attachments are *tools Vector knows it has and how to use* (affordances) —
   not external automation. Define the control/feedback loop.
5. **Integrate via the box:** heavy compute (3D modeling, arm policies, tactile inference) on the Brain box;
   the cube/arms talk to the box; Vector commands through the box. Reuse Vector's existing cube BLE protocol
   (`victor/cubeBleClient`) where possible.
6. **Map to us:** ties to L2 perception (new modalities), the 3D home map, ENGRAM (touch/thermal become new
   fingerprint channels), and tool-use behaviors.

---

## RESEARCH VECTORS

### V1 — Lift & payload reality (the hard constraints that bound everything)
- **Questions:** What are Vector's real **lift mechanics** — payload mass, lift height/torque, the cube
  docking/pickup geometry, grip method, and the lift's force resolution? (Source: `kercre123/victor`
  `engine`/`robot` lift code + TRM Ch on lift/docking.) What's the true weight/size budget for anything the
  lift carries or the body pushes? What does the existing **cube BLE protocol** expose (`cubeBleClient`,
  accelerometer, LEDs, tap) that we can extend?
- **Return:** the hard numbers (payload, torque, geometry, BLE capabilities) that constrain V2–V4 designs.

### V2 — The Rover-Cube: highest-value sensors to embed
- **Questions:** Redesign the cube as a sensor pod Vector carries for mapping/sensing. What fits in a
  light, self-powered, ~cube-sized package and gives the **highest value** Vector lacks: **2D/solid-state
  LiDAR or ToF** (mapping/obstacles), **thermal camera** (FLIR Lepton / Seek / MLX90640 — find people/pets/
  warmth/appliances), **360 or fisheye camera**, extra **wide-FOV RGB**, **IMU** (already has), **mic**,
  **env sensors** (temp/humidity/air/light), **UWB tag** (so the box knows the cube's position). Power
  (tiny LiPo + charging via Vector's charger or its own), comms (BLE/WiFi to box), weight budget, heat. How
  does Vector *use* it — carry it through rooms to build the 3D/thermal map (the "Maps car"), or place it as a
  remote room-sensor? Keep the play/personality value of the original cube.
- **Return:** a ranked sensor payload for the Rover-Cube (value × weight × power × cost), a power/comms design,
  and the "how Vector uses it" usage modes.

### V3 — The Thumb: a lift attachment that lets Vector FEEL
- **Questions:** Design an ultra-light, 3D-printable universal mount on Vector's lift that adds **touch**:
  - **Force/pressure sensing:** FSRs, thin **load cells** + HX711, barometric/MEMS force (the Press-fit
    "barometer-in-rubber" trick), capacitive, or **optical tactile** (GelSight/**DIGIT**/TacTip/9DTact —
    camera-based skin that sees deformation). Which give real force in newtons + contact geometry at low
    weight/cost?
  - **What it computes:** force-to-move an object (→ infer mass/friction), **hardness/compliance** (press and
    measure deformation vs force → soft vs hard), texture/slip, temperature (add a thermistor → feel warm/cold).
  - **The "thumb" concept:** how an opposable/contact surface multiplies manipulation — a fork/finger with a
    pressure pad so Vector can gauge grip, not just lift blindly.
  - **"Touching reality" methodology:** how Vector *actively senses* — press with increasing force, watch the
    response, build a tactile model, **calibrate against known objects**, and self-correct drift (Anki way).
- **Return:** a recommended tactile-sensing approach (sensor + readout + mount design concept), the force/
  hardness inference method, the calibration/active-sensing protocol, and weight/cost.

### V4 — The two desk arms: Vector-commanded manipulation in a "control area"
- **Questions:** Two affordable, open robot arms mounted on the Brain box with a defined **control-area**
  workspace where Vector pushes/delivers objects for manipulation (rotate a box to 3D-scan it, hold it up,
  open it). Which arms: **SO-100/SO-101** (LeRobot/TheRobotStudio, ~cheap, open), **Koch v1.1**, **WidowX**,
  **xArm/uFactory**, **Trossen** — payload/reach/precision/cost? Grippers (parallel, soft, vacuum). **Control:
  Vector in command** — hand-eye calibration to the room/box frame, how Vector "hands off" an object to the
  control area, motion planning/IK, and learned manipulation (**LeRobot ACT / π0 / OpenVLA**) vs scripted.
  Vision for the arms (a camera over the control area → pose, grasp). How does Vector *know it has the arms and
  how to use them* (affordance model, tool-use behaviors) — e.g. "to 3D-model this box, place it in the control
  area and have the arms rotate it under the camera."
- **Return:** arm hardware recommendation + gripper + control stack (IK/planning + learned policy options) +
  the hand-off/control-area workflow + vision-for-grasp, with cost and open-source software.

### V5 — Tactile & manipulation software / datasets ("prove what it feels")
- **Questions:** Open software for tactile sensing & manipulation: **DIGIT/GelSight** SDKs and tactile
  datasets, force/slip estimation, **material/hardness classification from touch**, tactile-visual fusion,
  grasp-quality/affordance models, **LeRobot** for teleop+learning. How to turn raw force/deformation into
  reliable "this is hard/soft, this weighs X, this needs Y newtons" — and how to *validate* it (press known
  objects, measure error). How do touch/thermal become new **ENGRAM fingerprint channels** so Vector
  *remembers* how things feel?
- **Return:** the tactile/manipulation software stack + the validation protocol + the ENGRAM channel design.

### V6 — System integration & affordances (how it all becomes one creature)
- **Questions:** How the cube, thumb, and arms register into the shared world-model and how **Vector reasons
  about its tools**: a unified affordance/tool-use model ("I have a thumb that feels force; a cube that maps;
  arms in the control area that manipulate"), the command/feedback loops through the Brain box, calibration of
  each tool's frame to the room frame, and the behavior layer that decides *when* to use which tool. How does
  this expand Vector's *experience* (the goal: feel and understand reality more richly)?
- **Return:** an integration map (each attachment × comms × frame × who-controls × box-compute) + the
  affordance/tool-use behavior design.

### V7 — Manufacturing & bill of materials
- **Questions:** 3D-print materials/weights (PLA/PETG/TPU, thin-wall, infill) for the thumb & cube shell;
  microcontrollers (ESP32-S3/RP2040) + sensors + tiny LiPo + charging; total cost per attachment; printability
  on a hobby printer; where to source. A starter BOM for each of the three.
- **Return:** per-attachment BOM (parts, cost, weight, print time) + design files to look for / fork.

---

## OUTPUT — Return Format
```
### V# — <title>
RECOMMENDATION: the concrete design choice in 3–5 sentences.
HARDWARE: part — vendor/URL — ~cost — weight — interface — open?
SOFTWARE: lib/SDK — URL — license — function.
DESIGN: mount/shape/integration concept (printable, light) + frame/calibration.
HOW VECTOR USES IT: the control/feedback loop + affordance.
ANKI-GRADE: calibration / self-correction / cleverness.
WEIGHT/POWER/COST + CONFIDENCE + open questions.
```
Final synthesis:
1. **Rover-Cube spec** (sensor payload + power/comms + usage modes).
2. **Thumb spec** (sensor + readout + mount + force/hardness method + calibration).
3. **Desk-arms spec** (arm + gripper + control stack + control-area workflow).
4. A unified **tool-use / affordance** design + BOMs + a phased build order (cheapest-highest-value first).

---

## SEED SEARCH TERMS
`anki vector lift payload torque specs` · `vector cube BLE protocol reverse engineered` · `FLIR lepton
thermal camera raspberry pi` · `MLX90640 thermal array` · `RPLiDAR vs ToF small robot mapping` ·
`GelSight DIGIT tactile sensor open source` · `TacTip soft optical tactile` · `barometer rubber force sensor
DIY` · `FSR load cell HX711 force newtons` · `hardness estimation tactile sensing` · `SO-101 lerobot arm` ·
`koch low cost robot arm` · `lerobot ACT policy teleoperation` · `OpenVLA pi0 manipulation` · `hand eye
calibration desk arm camera` · `robot arm IK motion planning python open source` · `object 3D scan turntable
photogrammetry gaussian splatting` · `ESP32-S3 sensor BLE LiPo` · `3D printable robot gripper TPU`.

## INTERNAL CONTEXT
Lift/cube/robot facts: `kercre123/victor` (`engine`, `robot`, `cubeBleClient`) + TRM. New modalities feed
L2 (`CHIMERA_L2_CORTEX.md`) and become ENGRAM channels (`vector_engram/`, touch/thermal). 3D-modeling tools:
`research/CUTTING_EDGE_OSS_GEODESIC.md` (V3, splats/turntable). Doctrine (light, clever, self-calibrating):
`ANKI_WAY.md`. Goal framing (expand experience / feel the world): `SOLVING_AI_MEMORY_WITH_FREQUENCY_AND_SYMPHONY.md`,
`MACHINA_ANIMA.md`.
