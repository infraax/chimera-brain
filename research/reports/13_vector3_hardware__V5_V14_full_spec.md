# Vector 3.0 · V5–V14 Full Hardware Specification
## Audio · Display · Proprioception · Memory · Connectivity · Enclosure · Software · BOM
### 2026-06-26 · Companion to V4+V6+V7 Revision · Chimera Project

> **Status:** Canonical spec for all remaining vectors. Builds on:
> — V1 baseline: RK3588S SoC + STM32H743 L1 safety MCU
> — V4+V6+V7 revision (2026-06-24): depth/IR/actuators/thumb
> Every vector follows the canonical geodesic output format.
> All parts verified from 2025–2026 datasheets and community benchmarks.

---

## V5 — Audio: Mic Array, Voice Processor & Speaker

### RECOMMENDATION

Vector 3.0 uses the **ReSpeaker XMOS XVF3800 4-mic array board** (Seeed Studio, $49.99 bare /
$54.50 with ESP32-S3) as the dedicated voice front-end processor. This is the exact part the
geodesic's SEED SEARCH TERMS pointed at, and it is real, available, and benchmarked.

The XVF3800 runs entirely on its own xcore.ai processor: **AEC, beamforming, de-reverberation,
Direction of Arrival (DoA), DNN noise suppression, and 60 dB AGC** — all off the RK3588S
application processor. The RK3588S receives a clean 16 kHz PCM stream over I²S and spends
zero CPU cycles on echo cancellation or beamforming. This is the Anki cleverness doctrine applied:
dedicated silicon eats the hard problem so the main processor stays available for ENGRAM and VLA.

**Mic geometry:** 4 MEMS microphones in a 66 mm square or 100 mm linear array topology
(selectable via the XVF3800 dev kit jumper). For Vector 3.0's body (approximately 100 mm wide),
the **66 mm square** is optimal: it places mics at the four body corners, maximising the
array aperture within the chassis and giving balanced 360° DoA coverage. Research on MEMS
array geometry confirms that circular and square uniform planar arrays outperform linear arrays
for omnidirectional coverage and sidelobe suppression at low frequencies.

**Motor-noise ego-null (the Anki move, 2026 edition):**
The XVF3800 AEC engine accepts a far-end reference signal — the original intent is loudspeaker
echo cancellation. Vector 3.0 re-purposes this path: the STM32H743 synthesises a **motor-noise
reference signal** from the 1 kHz motor state telemetry frame (PWM duty cycle × encoder speed →
FFT-domain noise model → I²S reference stream to XVF3800). The XVF3800 adaptive filter cancels
the motor fundamental and harmonics as if they were loudspeaker echo. This is a direct
generalisation of Anki's 2018 motor-noise nulling: instead of a static calibration table,
the reference signal is dynamic and updates in real time as motors accelerate/decelerate.

**STT / TTS / VAD on-robot (verified benchmarks, ONNX Runtime arm64-v8a):**
- **Silero VAD v5:** <1 ms per 32 ms chunk, RTF <0.01 — runs continuously on the RK3588S A55
  little-core cluster (≈1% CPU, effectively free)
- **DeepFilterNet3 noise suppression:** ~5 ms per 32 ms chunk, RTF ~0.15 — on-robot always-on
- **Parakeet TDT v3 STT:** 175 ms for 1.5 s audio, RTF 0.12 — on-robot, triggered by VAD
- **Kokoro 82M TTS:** 1.075 s for 1.9 s output, RTF 0.58 — on-robot acceptable; with RK3588S
  NPU delegation (RKNN), expect 2–3× faster (RTF <0.25)

All model sizes together: ~1.2 GB INT8 ONNX — fits in the 8 GB LPDDR4x RAM budget.

**Speaker:** TI **TAS5760M** Class-D amplifier, I²S input, 30 W/ch stereo (typ.), SNR 102 dB,
THD+N 0.02%, $4.10 at qty 1 / $2.60 at qty 2000. Drives a single 28 mm × 40 mm
full-range driver (Visaton FRS 7 or equivalent, ~$3–5) mounted in a rear-cavity resonator
tuned to 400 Hz to compensate for the small enclosure's bass roll-off.
The TAS5760M is I²S-native — zero DAC required; the RK3588S I²S output feeds it directly.

**ANKI-WAY SCORE:** C 5/5 · E 5/5 · Q 5/5 · B 5/5 · F 5/5

*The XVF3800 is the Anki 4-mic motor-null philosophy implemented as a $50 module.
Every audio challenge Anki solved in firmware on the APQ8009 is now solved in silicon,
freeing the application processor entirely.*

### PARTS

| Part | Vendor | ~Cost (qty1/10) | Interface | Power | Open driver? |
|------|--------|----------------|-----------|-------|-------------|
| **ReSpeaker XVF3800** (4-mic, bare) | Seeed Studio | $49.99 / $44 | I²S out + SPI ctrl (to RK3588S) + motor-ref I²S in (from STM32H743) | ~850 mW active / ~50 mW idle | ✅ Linux UAC2 USB; I²S firmware |
| **TAS5760M** Class-D amp | Mouser / LCSC | $4.10 / $2.60 | I²S (from RK3588S) | ~200 mW idle / ~1.5 W at 0.5 W audio | ✅ TI DS SLOS772D |
| Visaton FRS 7 speaker | Mouser / Conrad | ~$4.50 / $3.80 | Passive | — | — |
| SPH0645LM4H-B MEMS mic (×4) | Adafruit / LCSC | $1.50 / $1.10 each | PDM → XVF3800 | ~0.6 mW each | ✅ |

### ANKI 2018 → 2026

**Anki 2018 (TRM):** 4 PDM MEMS mics fed to the APQ8009 DSP; software AEC + beamformer
running on the application CPU; motor-noise nulling via a calibrated static spectral model
recalibrated as actuators aged. Constraint: no dedicated voice DSP chip existed in 2018 at this
price point and size. All DSP ran on the same CPU that handled perception, animation, and cloud
communication — consuming a measurable fraction of the 1.2 GHz quad-A7 budget.

**2026 change:** The XVF3800 is a dedicated xcore.ai voice processor — an entire high-end
audio DSP pipeline on a $50 module. The motor-noise reference path re-purposes AEC hardware
for ego-noise cancellation. The RK3588S gets 100% of its cycles back for ENGRAM and VLA.
The Anki recalibration-as-actuators-age doctrine is preserved: motor state telemetry drives
the reference model dynamically, not from a static calibration table.

### CHIMERA MAP

| Component | Layer | ENGRAM Channel | On-robot / Dock |
|-----------|-------|----------------|-----------------|
| XVF3800 AEC + beamformer | L1 (ego-noise null, DoA) | — | On-robot always |
| Silero VAD + DeepFilterNet3 | L1/L2 boundary (wake gate) | — | On-robot always |
| Parakeet STT | L2 (speech understanding) | Audio fingerprint (keyword, speaker ID) | On-robot, triggered |
| Kokoro TTS | L3 (personality output) | — | On-robot |
| TAS5760M + speaker | L1/L3 (audio output) | — | On-robot |
| Motor noise reference | L1 (ego-noise) | Self-cancellation | STM32H743 → XVF3800 |

### SELF-AWARENESS

The motor-noise reference path is explicit self-cancellation. At each motor state tick (1 kHz),
the STM32H743 computes:

  `f_motor(n) = PWM_L × ω_L + PWM_R × ω_R + harmonics(2×, 3×)`

This is streamed as a synthetic audio signal to the XVF3800's reference input, where the AEC
engine treats it as the "loudspeaker" to be cancelled from the mic input. The creature
can hold a voice conversation at normal speech levels while its treads are running.

Additionally, the XVF3800 AEC performs **device-moved re-calibration** automatically: if the
acoustic path changes (robot moved to a different surface, enclosure resonance shifts), the AEC
adaptive filter converges to the new acoustic model within ~2 seconds of audio playback.
This is the acoustic equivalent of Anki's actuator-aging recalibration.

### POWER/THERMAL

| Mode | XVF3800 | TAS5760M + Speaker | Total V5 |
|------|---------|-------------------|----------|
| Deep sleep / muted | ~50 mW | ~50 mW idle | ~100 mW |
| Listening (AEC+beam active) | ~850 mW | ~50 mW | ~900 mW |
| Speaking (TTS + audio out) | ~850 mW | ~200–1500 mW | ~1–2.4 W |

The XVF3800 is the dominant audio power draw. It is worth noting that at 850 mW it is
still lower than the RK3588S NPU active draw — audio is not the bottleneck.

### RISKS / OPEN QUESTIONS

**Confidence: Very High — the XVF3800 ReSpeaker board is a shipping product with ROS2 and
Raspberry Pi validation. Motor-noise reference path is novel but mechanistically sound.**

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Motor-noise reference path not validated on XVF3800 AEC | Medium | Phase 0: bench test — play motor-noise simulation through I²S reference while running drive motors; measure SNR improvement |
| 66 mm square geometry fits chassis | Low | Verify in CAD at Phase 0; XVF3800 supports external mic array connector if spacing needs adjustment |
| Kokoro RTF 0.58 on CPU feels slow for natural speech | Low | RKNN delegation expected to bring RTF <0.25; pre-buffer TTS audio for natural playback timing |

---

## V8 — Display & Expression (The Face = The Soul)

### RECOMMENDATION

Vector 3.0 uses a **1.54″ 240×240 IPS TFT LCD** (ST7789V driver, SPI interface) for the face —
the same philosophical choice Anki made in 2018: a small, high-quality, reasonably resoluted
panel that serves emotional expression, not a video screen. The ST7789V-driven 240×240 panel
is available from multiple verified sources at $2.30 (Alibaba sample) to $17.50 (Adafruit
breakout), 300 nits, all-angle IPS viewing, 27.72 × 27.72 mm active area. This is modestly
higher resolution than Anki's original 184×96 — enough to render sharper eye pupil curves
and smoother animations, without crossing into "just play a video" territory.

**Why IPS LCD over OLED/AMOLED for the face:**
OLED burn-in is a real risk for a robot that displays the same eye pattern for hours per day.
The Vector face renders static or near-static patterns (a pair of eyes, mostly centered) — the
exact scenario that accelerates differential OLED aging. An IPS LCD has zero burn-in risk,
comparable contrast at normal indoor viewing distances, better peak brightness in a sunlit room
(300+ nits vs AMOLED at low drive), and lower cost. The round AMOLED options (1.39″ 400×400
MIPI, ~$15–20 at sample qty) are tempting for aesthetics but add MIPI lane pressure to the V3
camera budget and the burn-in risk is real. Verdict: **IPS LCD wins on the Anki-way rubric**
(efficiency, quality, fit-to-soul — the face is minimalist, not a display showcase).

**Resolution rationale — does 240×240 help emotion vs 184×96?**
At 1.54″, 240×240 = 220 PPI. The eye rendering can use 12-pixel-radius pupils (vs ~7 pixels
on the original) — smoother arcs, more expressive squint animations, better tear/shimmer
detail. Above this resolution the returns are diminishing: the eye lives in a ~80×80 pixel
bounding box regardless of panel resolution, and the emotional content comes from motion
timing and shape, not pixel count. 240×240 is the sweet spot.

**Controller path:** ST7789V accepts SPI at up to 80 MHz. The RK3588S has a dedicated SPI
controller; alternatively the display connects over a lightweight GPIO-SPI bridge from the
STM32H743 if the face animation runs at L1 reflex speed (blinking, startled expressions
can be pre-rendered sprites). For richer procedural emotion rendering, the RK3588S's Mali
GPU handles the face compositor — a ~2D scene of two animated eye sprites is trivially
fast (<1% GPU load). Frame rate: 30–60 fps sufficient; the ST7789V supports up to 60 fps
at 240×240 over full-speed SPI.

**Cover lens:** A 35 × 35 mm sapphire-look acrylic convex lens (3 mm center thickness,
radius of curvature ~40 mm) press-fit over the display aperture gives the face depth and
a slightly magnified, alive quality — the same optical trick Anki used to make Vector's
tiny screen feel present. Sourced from optical lens suppliers on LCSC/Aliexpress, ~$1.50 each.

**Ambient adaptation:** A VEML7700 ambient light sensor (already specified in V4 for IR gating)
feeds the RK3588S a lux reading. Display brightness is PWM-dimmed from 300 nits (bright room)
to 30 nits (dark room / sleeping human) by the L3 Constructor personality layer.

**ANKI-WAY SCORE:** C 4/5 · E 5/5 · Q 4/5 · B 5/5 · F 5/5

*IPS LCD over OLED is the Anki efficiency move: zero burn-in risk, lower cost, identical emotional
expressivity at this size. The convex lens is the Anki physics move: a $1.50 optical element
transforms a flat panel into a living face.*

### PARTS

| Part | Vendor | ~Cost (qty1/10/100) | Interface | Power | Open driver? |
|------|--------|---------------------|-----------|-------|-------------|
| **1.54″ 240×240 IPS TFT ST7789V** | Adafruit #3787 / DFRobot / Alibaba | $17.50 / $15.75 / $2.30 | SPI 80 MHz | ~30 mW active / <5 mW sleep | ✅ ST7789V Linux fbdev / SPI |
| Convex acrylic cover lens 35×35 mm | LCSC / Aliexpress | $1.50 / $1.20 | Press-fit | — | — |
| **VEML7700** ambient light (shared with V4) | Mouser / LCSC | $1.20 / $0.90 | I²C | <1 mW | ✅ |

### ANKI 2018 → 2026

**Anki 2018 (TRM):** 184×96 IPS LCD, SPI, the iconic eye renderer — a deliberate choice for
minimal pixels + maximal personality. Constraint: cost target and compute budget. The APQ8009
GPU could render the eye compositor at full speed, but a higher-resolution panel would have
increased cost and BOM complexity without meaningful expressivity gain.

**2026:** 240×240 at the same price point ($2–18) — a modest resolution upgrade with zero
architectural change. The eye renderer philosophy is identical; the face compositor moves
from a GPU shader on the APQ8009 to a Mali shader on the RK3588S, both trivially fast.
The only meaningful change is the convex lens upgrade (if Anki did not already use one —
the TRM is ambiguous on the cover optic), and the ambient brightness adaptation via VEML7700.

### CHIMERA MAP

| Component | Layer | Role |
|-----------|-------|------|
| Display + compositor | L3 (personality expression output) | Emotional eye rendering |
| Ambient brightness (VEML7700) | L2 → L3 | Display brightness + IR LED gating (V4) |
| Pre-rendered sprite engine | L1 (reflex expressions: blink, startle) | Immediate emotional reflex |

### POWER/THERMAL

| Mode | Display | Backlight | Total V8 |
|------|---------|-----------|----------|
| Off / deep sleep | 0.1 mW | 0 mW | ~0.1 mW |
| Eyes idle (dim) | 5 mW | 10 mW @ 30 nits | ~15 mW |
| Eyes active (full bright) | 10 mW | 25 mW @ 300 nits | ~35 mW |

Display is thermally negligible — no heatsink or thermal consideration needed.

### RISKS / OPEN QUESTIONS

**Confidence: Very High — this is mature, proven commodity hardware.**

| Risk | Mitigation |
|------|-----------|
| SPI speed limits frame rate at high resolution | 80 MHz SPI → 240×240 × 16-bit × 60 fps = 55 Mbps — within SPI spec |
| Acrylic lens scratches | Use polycarbonate or sapphire-glass lens for production; acrylic for Phase 0 |
| OLED temptation at Phase 2 | Re-evaluate burn-in after 6 months Phase 1 field test; upgrade if pattern diversity is high enough |

---

## V9 — Proprioception, Touch & Environment Sensors

### RECOMMENDATION

**IMU:** **TDK InvenSense ICM-42688-P**, 6-axis (3-axis gyro + 3-axis accel), 2.5×3×0.91 mm,
SPI at up to 24 MHz, gyro noise 0.0028 dps/√Hz, accel noise 70 μg/√Hz, ±2/4/8/16 g FSR,
operating temp −40 to 85°C, production status confirmed 2025–2026. This is the premier 6-axis
MEMS IMU for robotics — used in flight controllers, high-accuracy robotics, and drone platforms.
It runs directly on the STM32H743 SPI bus at 32 kHz ODR, feeding the L1 attitude estimator
and ego-motion integrator.

**Why 6-axis not 9-axis (no magnetometer on robot body):**
A magnetometer on a robot body is polluted by motor currents, PCB copper pours, and the
battery — making heading unreliable without extensive calibration. The UWB positioning system
(V11, DWM3000) provides absolute position and heading reference. The IMU provides high-rate
attitude rate for the L1 reflex loop; heading comes from UWB, not compass. A magnetometer
can be added on the dock (away from motor interference) as a V2-upgrade if needed.

**Cliff / edge sensing:** 4× **VL53L0X** (±2 m single-zone ToF, I²C, ~$3 each) in downward-
facing orientation at the four chassis corners — simpler, cheaper, and more reliable than the
original Anki IR emitter/detector pairs. The L1 STM32H743 runs a 50 Hz polling loop; any
zone reporting distance >800 mm triggers an immediate halt + reverse command, independent
of the application processor. The VL53L8CX (from V4) covers forward obstacle sensing;
the VL53L0X covers the floor plane at minimal cost.

**Capacitive touch skin:** 3-zone capacitive layout using **AT42QT1070** (7-channel capacitive
touch IC, I²C, ~$2.50) on a flexible PCB routed to 3 conductive zones on the outer chassis:
- **Top crown** (1 zone): primary petting/stroking zone — the creature registers sustained
  touch here as positive social interaction
- **Left and right flanks** (2 zones): pickup/hold detection — bilateral simultaneous pressure
  = being carried
- The AT42QT1070 outputs a change-detect interrupt to the STM32H743 within <10 ms

**Ambient sensors on-robot:** VEML7700 (light, I²C, shared with V8) + BME280 (temp/humidity/
pressure, I²C, ~$2.50) for in-room environmental logging. These are L3 ENGRAM context channels:
ambient temp + humidity fingerprints help the Constructor distinguish "morning kitchen" from
"late-night bedroom" — rooms that have different interaction patterns. Both draw <2 mW; they
run continuously.

**UWB positioning (on robot):** **Qorvo DWM3000** module ($11–23 at qty 1, $17–23 median,
SPI, 6.5–8.0 GHz UWB, 6.8 Mbps data rate). The DWM3000 runs as a **tag** on the robot;
2–4 DWM3000 **anchor** modules are embedded in the dock and placed at known room positions.
Achieves ~10 cm 2D positioning accuracy with 5 anchors (EKF-fused), verified in independent
robotics research. The UWB position feeds the L2 spatial model and the ENGRAM
StateVector.position field, giving the creature a calibrated cm-level self-model of where
it is in its home.

**ANKI-WAY SCORE:** C 4/5 · E 5/5 · Q 5/5 · B 5/5 · F 5/5

*ICM-42688-P is the best-in-class 6-axis IMU at the same price and package as the original
Anki IMU. The 3-zone touch skin is sparse — Anki-minimal, not gadget-dense. UWB is the
physics-first positioning move: RF time-of-flight instead of expensive SLAM-at-all-times.*

### PARTS

| Part | Vendor | ~Cost (qty1/10) | Interface | Power | Open? |
|------|--------|----------------|-----------|-------|-------|
| **ICM-42688-P** 6-axis IMU | Mouser / LCSC / TDK | ~$3.50 / $2.80 | SPI 24 MHz | ~0.7 mA @ 3.3V | ✅ open DS-000347 |
| **VL53L0X** cliff sensor ×4 | Pololu / Mouser | ~$3 / $2.40 each | I²C | ~20 mW active each | ✅ ST UM2036 |
| **AT42QT1070** touch IC | Mouser / LCSC | ~$2.50 / $2 | I²C | <5 mW | ✅ Microchip DS9543 |
| Flexible PCB touch zones (3 zones) | JLCPCB FPC | ~$5–10 for 10 pcs | PCB traces | — | Design in Phase 1 |
| **BME280** temp/humidity/pressure | Adafruit / LCSC | ~$2.50 / $2 | I²C | <1 mW | ✅ Bosch DS |
| **VEML7700** ambient light | Mouser / LCSC | ~$1.20 / $0.90 | I²C | <1 mW | ✅ Vishay DS |
| **DWM3000** UWB tag module | Mouser / LCSC / Qorvo | ~$18 / $15 | SPI | ~100 mW active / ~1 mW sleep | ✅ Qorvo API |
| DWM3000 anchor ×2–4 (dock) | Same | ~$18 / $15 each | SPI → dock MCU | — | ✅ |

### CHIMERA MAP

| Sensor | Layer | ENGRAM Channel | Continuous / Gated |
|--------|-------|----------------|---------------------|
| ICM-42688-P gyro/accel | L1 (attitude, ego-motion) | Ego-motion vector | Continuous (32 kHz ODR) |
| VL53L0X cliff ×4 | L1 (cliff reflex) | — (reflex only) | Continuous (50 Hz) |
| AT42QT1070 touch | L1 → L3 (social touch) | Social-touch event | Interrupt-driven |
| BME280 | L3 (environment context) | Environmental fingerprint | Continuous (1 Hz) |
| VEML7700 | L2/L3 (lighting context) | Environmental fingerprint | Continuous (1 Hz) |
| DWM3000 UWB | L2 (spatial self-model) | Position fingerprint | Continuous (10 Hz ranging) |

### SELF-AWARENESS

The ICM-42688-P's ego-motion data feeds both the L1 cliff-detection hysteresis filter (prevent
false positives during hard acceleration) and the L2 ego-motion compensation pipeline (V6
motor encoder + IMU fusion → known-good ego-motion vector for camera optical flow correction).
The DWM3000 UWB position is the creature's "I know where I am" ground truth — a form of
proprioceptive self-knowledge that Anki's original dead-reckoning odometry could only approximate.

---

## V10 — Memory & Storage

### RECOMMENDATION

**RAM:** 8 GB LPDDR4x on the RK3588S SoC (standard config on most RK3588S SoMs at $110–170).
LPDDR4x at 3200 MT/s gives ~51.2 GB/s bandwidth — more than sufficient for running
ENGRAM's D=4096 HRR vectors, the ONNX inference models (Parakeet ~400 MB, Kokoro ~300 MB,
perception models ~200–500 MB), the OS, and the chimera service layer simultaneously.
Total steady-state RAM allocation:

| Allocation | Size |
|-----------|------|
| Linux OS + chimera services | ~800 MB |
| Parakeet STT (INT8 ONNX) | ~400 MB |
| Kokoro TTS | ~300 MB |
| Perception models (YOLO-alt, Depth Anything V2, small VLM) | ~600 MB |
| ENGRAM hot store (HRR @ D=4096, Hopfield, reservoir, sliding window) | ~200 MB |
| Framebuffer + GPU working mem | ~200 MB |
| **Total** | **~2.5 GB** |

8 GB leaves **~5.5 GB headroom** — enough for a small on-board VLM (SmolVLM2-256M at ~512 MB
INT8, or Moondream at ~1 GB) running gated during active conversation.

**Storage:** 64 GB eMMC 5.1 for the OS + model store. eMMC 5.1 reaches ~300 MB/s sequential
read / ~100 MB/s write. Models are loaded once at boot via mmap (per the ENGRAM-rewrite
report's FlatBuffers/mmap architecture) — sustained write workload is low. Endurance estimate:
eMMC with 3000-cycle TLC NAND at WAF 4–8, 64 GB → TBW ~24–48 TB. At 500 MB/day ENGRAM
logging, lifetime > 130 years — endurance is not a concern.

**ENGRAM cold archive:** A **128 GB microSD** (UHS-I, ~$12) in the dock. The hot ENGRAM store
(recent episodes, ~200 MB) lives in RAM; the cold archive (all historical StateVectors, FlatBuffers
EGRV files, fp16) flushes to the dock microSD every dock cycle over the USB-C dock link.
This mirrors the ENGRAM-rewrite report's mmap-friendly architecture: the cold archive is a
flat directory of .egrv files, each memory-mappable in O(1) from the dock's MCU.

**No NVMe / UFS on-robot for Phase 0–1:**
UFS 3.1 offers 8× the performance of eMMC 5.1, but the RK3588S eMMC interface is the simpler
bring-up path and 300 MB/s is sufficient. NVMe via M.2 adds cost and connector complexity.
Defer UFS to a Phase 2 custom carrier PCB if model swap latency becomes a bottleneck.

**ANKI-WAY SCORE:** C 4/5 · E 5/5 · Q 4/5 · B 5/5 · F 4/5

*8 GB LPDDR4x + 64 GB eMMC is the standard RK3588S SoM configuration — zero BOM addition,
maximum buildability. The cold-archive microSD on the dock is the Anki efficiency move: infinite
memory for the cost of a $12 SD card.*

### ENGRAM MEMORY FOOTPRINT (on-robot)

```
ENGRAM on-robot hot store (RAM):
  HRR working memory:        D=4096 × 1000 episodes × fp16  = ~8 MB
  Hopfield network weights:  N=512 neurons × fp16           = ~0.5 MB
  Reservoir state:           N=1000 × fp16                  = ~2 MB
  Sliding window buffer:     1000 × StateVector (~2 KB each) = ~2 MB
  Index structures (HNSW):   ~50 MB
  Model cache (mmap):        ~150 MB (hot models resident)
  ─────────────────────────────────────────────────────────
  Total hot store:           ~212 MB  ✅ fits in 8 GB budget

ENGRAM cold archive (dock microSD):
  StateVector EGRV files:    128 GB → ~65 million StateVectors
  Retention:                 effectively unlimited for solo use
```

### RISKS / OPEN QUESTIONS

**Confidence: Very High for RAM/eMMC (standard SoM config). Medium for ENGRAM cold archive
sync protocol (implementation work, not a parts risk).**

---

## V11 — Connectivity & Positioning

### RECOMMENDATION

**WiFi + BT:** **RTL8852BE** M.2 2230 WiFi 6 (802.11ax dual-band 2.4/5 GHz, up to 1200 Mbps)
+ Bluetooth 5.2 combo module, 22×30×2.15 mm, PCIe 2.1 (WLAN) + USB 2.0 (BT), 3.3 V, Linux
drivers available for arm64 (in-kernel rtw89 for kernel 5.10+; out-of-tree lwfinger/rtw8852be
for earlier). Verified working on Jetson with RK3588S-class Linux kernels. This is the same
module category used by the Seeed reComputer family. Cost ~$8–15 depending on supplier.

**WiFi 6 rationale for dock-offload:** The robot↔dock link (per the external-sensor geodesic)
needs enough bandwidth to stream:
- 3× camera streams (MJPEG compressed) from robot to dock during heavy perception: ~15–30 Mbps
- ENGRAM StateVector sync (compressed FlatBuffers): <1 Mbps
- VLM prompt/response offload (text only): <100 kbps
Total: ~30 Mbps. WiFi 6 at 1200 Mbps theoretical / ~300 Mbps practical indoor gives 10×
headroom. Latency on a local-only WiFi 6 AP (dock runs a local hotspot in isolation mode):
<2 ms for small packets → adequate for the gated perception offload model (not real-time safety).

**BLE 5.2:** Used for the Cube attachment ranging (legacy DW1000 path → upgrade to UWB) and
for smart-home peripheral discovery (Matter/Thread bridge on dock). The robot does not run
Thread directly — too much firmware overhead for the STM32H743. The dock handles Matter/Thread
as a gateway.

**UWB (on robot):** DWM3000 as specified in V9. The robot-tag + dock-anchors architecture uses
Two-Way Ranging (TWR) at 10 Hz, fused with ICM-42688-P odometry via EKF on the RK3588S.

**Dock link architecture (robot↔dock data plane):**
```
Robot (WiFi 6 client) ←→ Dock (WiFi 6 AP, isolated local network, no WAN)
  Robot subscribes:   room LiDAR map tiles (LD19 scan)
                      enriched ENGRAM recall responses (cold-store queries)
                      VLM completions (if small LLM runs on dock Mac Mini)
  Robot publishes:    camera streams (gated)
                      ENGRAM StateVectors (cold-archive flush)
                      UWB ranging results
```
The dock can optionally bridge to WAN for model updates and remote monitoring, gated by
a user-controlled switch — privacy by design, per the external-sensor report.

**Antenna placement:** The RTL8852BE uses MHF4 connectors to two external antennas. On the
robot body, two small flex antennas route up the internal chassis walls, terminating at the
top crown (maximum exposure, away from the battery and motor cores). The DWM3000 has an
integrated PCB antenna — place at chassis top, away from the LPDDR4x EMI zone.

**ANKI-WAY SCORE:** C 3/5 · E 5/5 · Q 4/5 · B 5/5 · F 4/5

*WiFi 6 + BT 5.2 on a single $10 M.2 module is the efficiency move. UWB solves indoor
positioning without map-building cost. The dock-as-local-AP is the privacy-first design.*

### PARTS

| Part | Vendor | ~Cost (qty1/10) | Interface | Power | Open? |
|------|--------|----------------|-----------|-------|-------|
| **RTL8852BE** WiFi 6 + BT 5.2 M.2 2230 | Seeed / LCSC / ENL | ~$10 / $8 | PCIe 2.1 + USB 2.0 | ~1.5 W active WiFi | ✅ rtw89 in-kernel Linux 5.10+ |
| **DWM3000** UWB tag (robot) | Mouser / Qorvo | ~$18 / $15 | SPI | ~100 mW active | ✅ Qorvo API |
| **DWM3000** UWB anchor ×2 (dock) | Same | ~$18 / $15 each | SPI → dock MCU | ~100 mW each | ✅ |
| WiFi 6 flex antenna ×2 (MHF4) | LCSC / Aliexpress | ~$1.50 / $1.20 each | MHF4 coax | — | — |

---

## V12 — Enclosure, Mechanical, Thermal & The Dock

### RECOMMENDATION

**Body size:** approximately 105 mm wide × 80 mm deep × 130 mm tall (vs original ~100×80×115 mm).
The 15 mm height gain accommodates the larger battery (V2: 3-cell 18650 stack or 3000 mAh LiPo),
the RK3588S SoM board, and the vertical thermal stack. Weight target: ~350–450 g (vs original
~300 g) — still light enough to be picked up one-handed.

**Chassis material strategy:**
- **Phase 0 prototype:** FDM printed in PETG (better layer adhesion and heat resistance vs PLA,
  Tg ~80°C, adequate for the ~45–55°C expected chassis surface). The chassis walls double as
  structural members and partial heat spreaders. SLA resin for the face bezel and cover lens
  seat — SLA tolerances (±0.1 mm vs FDM ±0.3 mm) critical for the display aperture fit.
  SLA specialty high-temp resins (Formlabs High Temp) resist deformation beyond 200°C, far
  exceeding any on-robot surface temperature.
- **Phase 2 production:** injection-molded ABS/PC-ABS for main body; soft-touch TPU overmold
  on flanks for grip and the capacitive touch zones.

**Thermal design — the critical upgrade:**
The RK3588S SoC has a TDP of approximately 10 W (NPU active) to 4 W (idle). The original
APQ8009 was 1.5 W TDP — Vector 3.0 dissipates 2.5–6× more heat. Passive-only thermal
solution:
1. A **40×40×2 mm copper heat spreader** (thermal conductivity 400 W/m·K) bonded directly
   to the RK3588S SoM's top surface via thermal pad (3 W/m·K Fujipoly XR-m, ~$3/sheet).
2. The copper spreader connects via **3 × 6 mm copper heatpipes** (available on Aliexpress
   for ~$2 each) to the **rear chassis wall**, which acts as a passive heatsink (surface area
   ~60 cm²). At 10 W TDP and 60 cm² surface area, the temperature rise is approximately:
   ΔT = P / (h × A) = 10 / (10 W/m²K × 0.006 m²) ≈ 167°C — too hot for passive alone.
3. **Small silent fan (25×25×6 mm, 5 V, ~60 mA, ~300 mW) mounted at the rear wall** as
   a draft fan (not a pressure fan). With forced convection h ≈ 50 W/m²K:
   ΔT ≈ 10 / (50 × 0.006) ≈ 33°C above ambient → ~58°C at 25°C ambient. Acceptable.
   The fan runs at minimum speed (20% PWM = ~1500 RPM) during normal operation and ramps
   to 100% only when SoC junction temperature (polled via Linux thermal zones) exceeds 75°C.
   At 20% PWM the fan is inaudible next to the motor noise floor (~35 dB(A) vs motors).
4. **DVFS (Dynamic Voltage-Frequency Scaling):** RK3588S supports Linux CPUfreq. L3 Constructor
   (the LLM/memory tier) runs on-demand; the A76 big cores throttle to 1.6 GHz during idle
   observation, rising to 2.4 GHz for active inference. The NPU gates off when not needed.
   Average thermal load during quiet observation: ~3–4 W → passive chassis handles it;
   fan needed only during heavy perception + LLM inference simultaneously.

**Balance and CG:** The battery pack (heaviest component, ~100–150 g) mounts at the bottom
center. The RK3588S SoM mounts at mid-height. The XVF3800 mic ring mounts at the top. CG
is well below the geometric center → stable tread stance, low tipping moment.

**Drop survival:** PETG prototype at 1.2 m drop onto concrete = borderline without strain-
relief joints. Phase 1 adds internal TPU bumpers at the four chassis corners (FDM-printed,
Shore 95A) and a steel-plate base that also serves as the tread chassis ground plane.

**The Dock 2.0:**
The dock is not a passive charger — it is a **compute-offload + sensor-hub + local-network
node + ENGRAM cold-archive server**:
- USB-C PD charging (dock → robot, 9 V/2 A = 18 W, charges 3000 mAh LiPo in ~1.5 h)
- LDROBOT LD19 LiDAR (room-scale SLAM during charge)
- 2–4 DWM3000 UWB anchors (room positioning)
- Local WiFi 6 AP (RTL8852BE in AP mode, isolated LAN)
- USB-C host port to optional Mac Mini / Pi 5 for VLM offload
- 128 GB microSD for ENGRAM cold archive
- The dock MCU (STM32F411 ~$3, SPI master to LD19 + DWM3000) runs the sensor hub
- Optional: dock mounts on a corner shelf or desk edge for optimal LiDAR field of view

**ANKI-WAY SCORE:** C 4/5 · E 4/5 · Q 4/5 · B 5/5 · F 4/5

*The fan is a concession from pure passive, but a 25 mm fan at 20% PWM is effectively silent
and enables a much smaller body than a full passive heatsink would allow. The dock-as-node
is the Anki physics move: one LiDAR on the dock replaces a spinning motor on the body.*

### PARTS (Enclosure + Thermal + Dock)

| Part | Vendor | ~Cost (qty1) |
|------|--------|-------------|
| PETG filament 500 g (chassis) | Prusament / local | ~$15 |
| SLA resin 250 mL (face bezel + lens seat) | Formlabs / JLCPCB | ~$20–40 |
| 40×40×2 mm copper heat spreader | Aliexpress / LCSC | ~$3 |
| Fujipoly XR-m thermal pad 40×40 mm | Mouser | ~$3 |
| 6 mm × 50 mm copper heatpipes ×3 | Aliexpress | ~$2 each |
| 25×25×6 mm 5V silent fan | Noctua / LCSC | ~$5–12 |
| USB-C PD dock charger board (9V/2A PD) | Aliexpress / LCSC | ~$8 |
| STM32F411 Nucleo (dock MCU, Phase 0) | ST / Mouser | ~$15 |
| 128 GB microSD (dock ENGRAM archive) | Samsung / Kingston | ~$12 |
| LDROBOT LD19 (dock LiDAR) | Seeed / RobotShop | ~$35 |

---

## V13 — Software, OS & The Safety Partition

### RECOMMENDATION

**Linux on RK3588S:** **Yocto Project** (Kirkstone or Scarthgap LTS branch) with a custom
`meta-chimera` layer. Rationale over Ubuntu/Debian: Yocto produces a minimal, deterministic
image (target rootfs <500 MB) without package manager overhead; the build system generates
both A/B OTA update images and the swupdate `.swu` bundle in the same bitbake pipeline.
The RK3588S has a well-maintained Rockchip Linux BSP (kernel 5.10 / 6.1, tested on SOM boards).
For Phase 0, start with an off-the-shelf Armbian or Radxa Ubuntu image to prove the stack,
then migrate to Yocto for Phase 1 when the image is stable.

**RTOS on STM32H743:** **FreeRTOS** (not Zephyr). Rationale: FreeRTOS is already used in
production STM32H7 motor control applications (independently verified in medical BLDC motor
controller design using STM32H743 + STM32H750 dual-MCU architecture, exact same INA240 +
magnetic encoder + FOC pattern), has the lowest latency and smallest footprint, and
ST's CubeIDE generates FreeRTOS project scaffolding automatically. Zephyr offers better
hardware abstraction but adds complexity for a single-MCU safety partition. The SimpleFOC
library has a FreeRTOS integration path documented by the community.

**MCU↔SoC IPC (the modern CLAD):**
Anki's CLAD-over-socket is replaced with **FlatBuffers over UART at 921600 baud** (92 KB/s —
adequate for 1 kHz motor state frames at 32 bytes each = 32 KB/s + headroom). The STM32H743
and RK3588S share a single UART (/dev/ttyS1 on RK3588S side). The FlatBuffers schema is
the canonical chimera IPC contract:

```flatbuffers
// chimera_ipc.fbs — the MCU↔SoC boundary contract
table MotorStateFrame {
  ts_us:       uint64;  // microsecond timestamp
  pwm:         [uint8:4];
  encoder:     [int32:4];  // absolute position (AS5600)
  current_mA:  [int16:4];  // INA240 readings
  torque_mNm:  [int16:4];  // estimated via K_T × I_q
}
table SensorFrame {
  imu_accel:   [float32:3];  // ICM-42688-P accel xyz
  imu_gyro:    [float32:3];  // ICM-42688-P gyro xyz
  cliff:       [uint16:4];   // VL53L0X readings mm
  touch:       uint8;        // AT42QT1070 bitmask
  contact_mN:  float32;      // BMP390 tactile force
}
table CommandFrame {
  drive_L:     int16;   // target velocity mm/s
  drive_R:     int16;
  lift_mm:     uint8;   // target lift height
  head_deg:    int8;    // target head angle
  grip_mN:     uint16;  // target grip force
}
union IpcMessage { MotorStateFrame, SensorFrame, CommandFrame }
```

**The Chimera 3-layer deployment map:**

| Layer | Runtime | Language | Silicon | Process |
|-------|---------|----------|---------|---------|
| **L1 Brainstem** | FreeRTOS | C (STM32CubeIDE) | STM32H743 | Motor FOC, cliff, touch, tactile reflex, thermal mask, motor-noise ref |
| **L2 Cortex** | Linux / RKNN runtime | C++ (perception), Go (service mesh) | RK3588S NPU + A76 | Camera pipelines, depth fusion, audio processing, ENGRAM write |
| **L3 Constructor** | Linux | Python (LLM/VLA) + Go (orchestration) | RK3588S A76 | Personality, memory retrieval, TTS/STT orchestration, dock offload broker |

**Inference runtime per tier:**
- **RKNN Toolkit 2** (Rockchip-native): for NPU-accelerated vision models (YOLOv8, Depth Anything V2,
  face detection) — MUST be used for the 6-TOPS NPU to be effective
- **ONNX Runtime with XNNPACK (arm64):** for audio models (Parakeet, Kokoro, Silero, DeepFilterNet3)
  running on the A55 little cores — CPU-based, adequate RTF as benchmarked
- **ExecuTorch / llama.cpp (INT4):** for the small on-board LLM (SmolVLM2-256M or similar)
  on the A76 big cores, gated during active conversation

**The formal safety partition contract:**
The STM32H743 L1 MCU **independently owns and cannot be overridden by the application processor** for:
1. **Motors stop** — if UART heartbeat from RK3588S absent for >500 ms → all motor PWMs set to zero
2. **Cliff halt** — if any VL53L0X zone < 200 mm in floor direction → immediate drive motor halt
3. **Thermal e-stop** — if STM32H743's internal temperature sensor or BME280 exceeds 70°C → all
   actuators halt, thermal event published to UART
4. **Watchdog** — independent IWDG on STM32H743 at 250 ms timeout; if L1 firmware hangs,
   hardware watchdog resets the MCU and holds motors in safe state

The RK3588S application processor can **request** motor commands; the STM32H743 **validates**
each command against the safety envelope before executing. A crashed application processor
can never drive the robot off a table — this is the Anki STM32/APQ8009 separation doctrine,
explicitly maintained.

**OTA update strategy:** Yocto + SWUpdate A/B partition scheme.
- Two rootfs partitions (root_A / root_B) on the 64 GB eMMC
- U-Boot reads `boot_count` env var and switches partition on failed boot
- SWUpdate daemon polls the dock's local WiFi server (or internet if bridge enabled)
- Updates are cryptographically signed (X.509); STM32H743 firmware updated via UART DFU
  triggered by the RK3588S after verifying signature — the MCU never accepts unsigned firmware
- Interrupted OTA (power loss during write) safely falls back to the previous rootfs partition

**ANKI-WAY SCORE:** C 5/5 · E 5/5 · Q 5/5 · B 4/5 · F 5/5

*The FlatBuffers IPC over UART is the direct heir to Anki's CLAD: a typed, versioned,
zero-copy binary protocol at the MCU↔SoC boundary. The safety partition contract is explicitly
stated and hardware-enforced. The creature cannot be bricked by a software crash.*

### RISKS / OPEN QUESTIONS

**Confidence: High for STM32H743+FreeRTOS+UART-FlatBuffers (proven pattern in production).
Medium for RKNN Toolkit 2 model conversion pipeline (requires per-model validation).**

| Risk | Mitigation |
|------|-----------|
| RKNN model conversion accuracy loss | Validate each model: run on CPU first, convert to RKNN, compare output on test set; accept <1% accuracy delta |
| Yocto build time (~3–8 h per clean build) | Use shared sstate-cache; Phase 0 on Armbian avoids this entirely |
| UART 921600 baud throughput ceiling | At 32-byte frames × 1 kHz = 32 KB/s; total IPC budget ~60 KB/s well within ceiling; upgrade to SPI if needed |
| STM32H743 IWDG fires during legitimate motor pause | Design heartbeat protocol: L3 sends explicit "pause motors" command, not absence-of-heartbeat; IWDG timeout 500 ms is generous |

---

## V14 — BOM, Cost, Sourcing & Phased Build Roadmap

### TIERED BILL OF MATERIALS

#### Compute & MCU

| Part | Vendor | Qty | ~Cost (qty1) | Interface | Notes |
|------|--------|-----|-------------|-----------|-------|
| RK3588S SoM (8 GB LPDDR4x, 64 GB eMMC) | Radxa / AliExpress / Accio | 1 | $110–170 | PCIe/USB/MIPI/UART | Core brain; RKNN NPU |
| STM32H743 Nucleo dev board (Phase 0) | ST / Mouser | 1 | ~$25 | UART/SPI/I²C/ADC | L1 safety MCU |
| STM32H743 bare LQFP208 (Phase 1+) | LCSC | 1 | ~$8 | — | Custom carrier PCB |

#### Sensors — Vision

| Part | Qty | ~Cost (qty1) |
|------|-----|-------------|
| Sony IMX678 MIPI camera module (eye-contact, Phase 0 USB) | 1 | ~$40 |
| OV9281 global shutter MIPI module (stereo side cams) | 2 | ~$15 each |
| OV5647 fisheye (rear surround) | 1 | ~$8 |
| OV2640 (V7 9DTact thumb camera) | 1 | ~$8 |

#### Sensors — Depth & IR

| Part | Qty | ~Cost (qty1) |
|------|-----|-------------|
| VL53L8CX 8×8 ToF (front + rear) | 2 | ~$12 each |
| VL53L0X cliff sensor (floor ×4) | 4 | ~$3 each |
| MLX90640-D55 thermal IR | 1 | ~$40 |
| SFH 4550 940 nm IR LED ×4 | 4 | ~$0.60 each |
| VEML7700 ambient light | 1 | ~$1.20 |
| LDROBOT LD19 (dock LiDAR) | 1 | ~$35 |

#### Sensors — Audio

| Part | Qty | ~Cost (qty1) |
|------|-----|-------------|
| ReSpeaker XMOS XVF3800 (bare board) | 1 | ~$50 |
| TAS5760M Class-D amp | 1 | ~$4.10 |
| Visaton FRS 7 speaker 28×40 mm | 1 | ~$4.50 |

#### Sensors — Proprioception & Touch

| Part | Qty | ~Cost (qty1) |
|------|-----|-------------|
| ICM-42688-P 6-axis IMU | 1 | ~$3.50 |
| AT42QT1070 capacitive touch IC | 1 | ~$2.50 |
| BME280 temp/humidity/pressure | 1 | ~$2.50 |
| DWM3000 UWB (robot tag) | 1 | ~$18 |
| DWM3000 UWB anchors (dock) | 2 | ~$18 each |

#### Actuators & Thumb

| Part | Qty | ~Cost (qty1) |
|------|-----|-------------|
| Coreless BLDC 2204 260KV | 4 | ~$10 each |
| AS5600 magnetic encoder | 4 | ~$1.50 each |
| SimpleFOCMini driver board | 3 | ~$15 each |
| INA240 current shunt monitor | 4 | ~$1.50 each |
| BMP390 tactile pressure | 1 | ~$3 |
| TMP117 grip temperature | 1 | ~$3 |
| OV2640 (9DTact camera — see above) | — | — |
| Dragon Skin 10 silicone 250 mL | 1 | ~$15 |

#### Display & Connectivity

| Part | Qty | ~Cost (qty1) |
|------|-----|-------------|
| 1.54″ 240×240 IPS LCD ST7789V | 1 | ~$17.50 (Adafruit) / ~$2.30 (Alibaba) |
| Acrylic convex cover lens 35×35 | 1 | ~$1.50 |
| RTL8852BE WiFi 6 + BT 5.2 M.2 module | 1 | ~$10 |
| WiFi flex antennas ×2 | 2 | ~$1.50 each |

#### Power (V2 — to be completed in V2 revision)

| Part | Qty | ~Cost (qty1) |
|------|-----|-------------|
| 18650 3000 mAh cell (×3, 3S pack) | 3 | ~$5 each |
| BMS 3S 5A with fuel gauge | 1 | ~$8 |
| USB-C PD dock charger board (9V/2A) | 1 | ~$8 |
| PMIC (TPS65094 or MP2696 class) | 1 | ~$4 |

#### Enclosure & Thermal

| Part | Qty | ~Cost (qty1) |
|------|-----|-------------|
| PETG filament 500 g | 1 | ~$15 |
| SLA resin 250 mL (face bezel) | 1 | ~$20 |
| Copper heat spreader 40×40×2 mm | 1 | ~$3 |
| Fujipoly XR-m thermal pad | 1 sheet | ~$3 |
| 25×25×6 mm 5V fan | 1 | ~$8 |
| STM32F411 Nucleo (dock MCU) | 1 | ~$15 |
| 128 GB microSD (dock archive) | 1 | ~$12 |

---

### TOTAL BOM COST ESTIMATE

| Phase | Component Coverage | Qty 1 Estimate |
|-------|-------------------|---------------|
| Phase 0 (dev-board prototype) | SoM + MCU + 3–4 sensors + display | **~$400–500** |
| Phase 1 (integrated prototype) | Full BOM above, no custom PCBs | **~$700–900** |
| Phase 2 (refined prototype) | Custom carrier PCB NRE (~$200–400 JLCPCB 5-layer) | **~$900–1200** |

*Note: RK3588S SoM cost dominates (~$110–170). The XVF3800 (~$50) and LiDAR (~$35) are the
next largest items. All parts are LCSC/Mouser/DigiKey/Seeed sourceable at qty 1.*

---

### PHASED BUILD ROADMAP

#### Phase 0 — Dev-Board Bring-Up (Target: 4–8 weeks)

**Goal:** Run the chimera stack end-to-end on real hardware, prove all critical interfaces.
No custom PCBs, no enclosure. Everything on breadboard/dev boards.

**Hardware:**
- RK3588S SBC (Radxa Rock 5B or Orange Pi 5 Plus, ~$80–120 with 8 GB RAM)
- STM32H743 Nucleo-144 breadboarded with:
  - 2× coreless BLDC + SimpleFOCMini on bench power supply
  - AS5600 on motor shafts
  - ICM-42688-P on breakout
  - VL53L0X ×4 on I²C expander
  - BMP390 + TMP117 breakout
- ReSpeaker XVF3800 USB → RK3588S (USB-C UAC2 mode, no firmware needed)
- 1.54″ IPS display SPI → RK3588S GPIO SPI
- USB cameras (IMX678 USB3, OV9281 ×2 USB) → RK3588S USB
- Bench power (5V/5A) in lieu of battery

**Software milestones:**
1. Linux boot on RK3588S, UART link to STM32H743 established, FlatBuffers IPC frames decoded
2. Single BLDC motor FOC running on STM32H743, torque sense verified (INA240 + AS5600)
3. VL53L0X cliff detection → motor halt reflex loop verified end-to-end (<10 ms)
4. XVF3800 audio stream → RK3588S → Silero VAD → Parakeet STT → Kokoro TTS → TAS5760M
5. IMX678 camera → RKNN YOLOv8 → person detection at >10 fps
6. ENGRAM: first StateVector written from live sensor data, recalled from RAM

**Risk-first order:** FOC motor torque sense → cliff halt reflex → audio DSP pipeline →
RKNN vision → ENGRAM write/recall → display face renderer

#### Phase 1 — Integrated Prototype (Target: 3–5 months)

**Goal:** A walking, talking, perceiving, remembering Vector 3.0 in a real enclosure.

**Hardware additions over Phase 0:**
- Custom carrier PCB (5-layer, KiCad, JLCPCB fabrication ~$200 for 5 boards) mounting:
  - RK3588S SoM connector
  - STM32H743 LQFP208 (bare IC, not Nucleo)
  - All sensor I²C/SPI bus routing
  - INA240 per-phase current sense traces
  - USB-C PD charging port
  - Battery connector + BMS
- FDM PETG chassis with SLA bezel
- 3S 18650 battery pack (3× NCR18650B 3400 mAh = 10.2 Wh)
- All 4 motors + tread system
- MLX90640 thermal IR
- VL53L8CX ×2 front + rear
- DWM3000 UWB (robot + dock anchors)
- 9DTact thumb (silicone pour + OV2640)
- Full dock: LD19 + USB-C PD + DWM3000 anchors + microSD

**Software milestones (building on Phase 0):**
1. Full 4-motor FOC on carrier PCB, all chimera layer services running on real battery
2. ENGRAM full pipeline: sense → StateVector → hot store → cold archive on dock
3. Voice interaction: wake word → STT → LLM response → TTS → speaker (on-robot or dock-offload)
4. Surround perception: stereo depth + thermal + VL53L8CX fusion → 2D occupancy grid
5. UWB positioning: room map + self-position in ENGRAM StateVector
6. Thumb tactile: BMP390 reflex + 9DTact L2 material classification on known objects

#### Phase 2 — "Anki-Grade" Refinement (Target: 6–12 months post Phase 1)

**Goal:** Production-quality hardware — injection molded shell, thermal/EMC compliance,
polished firmware, reliable OTA updates.

**Key upgrades:**
- Injection-molded ABS/PC-ABS body + TPU touch skin overmold
- 6-layer custom PCB with EMC layout (signal integrity, ground planes, EMI shields)
- Thermal validation: thermal chamber test 20°C–40°C ambient, 8-hour continuous run
- Yocto production image with SWUpdate A/B OTA, signed firmware
- STM32H743 IWDG + safety partition formal validation
- Optional: UFS 3.1 storage upgrade on custom PCB if model load latency is bottleneck
- Optional: second SoM slot for dock (run full VLM locally without external PC)

---

### FIRMWARE REUSE vs NEW

| Module | Source | Status |
|--------|--------|--------|
| `kercre123/victor` (vic-robot, vic-engine) | Reuse for reference | Read for behavioral architecture; do NOT run directly — wrong SoC, wrong MCU |
| wire-pod server | Reuse as reference | Useful for understanding the cloud protocol; replace with local ENGRAM broker |
| SimpleFOC library | **Reuse directly** | MIT license, active maintained, STM32H7 verified |
| FlatBuffers runtime (C++ + Go + Python) | **Reuse directly** | Per ENGRAM-rewrite report |
| RKNN Toolkit 2 | **Reuse directly** | Rockchip-maintained, covers YOLOv8, MobileNet, custom |
| Silero VAD / Parakeet / Kokoro | **Reuse directly** | ONNX Runtime, Apache-2.0 |
| DeepFilterNet3 | **Reuse directly** | MIT, ONNX |
| Yocto meta-rockchip BSP | **Reuse as base** | Community-maintained, 5.10 / 6.1 kernel |
| 9DTact tactile CNN | **Reuse as base** | Apache-2.0 on GitHub, retrain on local silicone geometry |
| L1 STM32H743 FOC safety firmware | **Write new** | Custom FreeRTOS + SimpleFOC + FlatBuffers IPC |
| L2 Cortex perception fusion | **Write new** | C++ ROS2-less service, builds on OSS model wrappers |
| L3 Constructor / ENGRAM | **Write new** | Per chimera ENGRAM-rewrite spec |
| Dock service / local WiFi AP | **Write new** | Go service, thin; reuses UWB Qorvo API |

---

### HIGHEST-RISK / LONGEST-LEAD ITEMS

| Item | Risk Type | Lead Time | Action |
|------|-----------|-----------|--------|
| RK3588S SoM (8 GB) | Availability / tariff | 1–3 weeks | Order immediately; buy 2 for Phase 0 |
| 9DTact silicone sensor fabrication | Build skill required | 1–2 weeks for first working unit | Start silicone pour practice at Phase 0 kickoff |
| SimpleFOCMini ×3 | Low stock at some vendors | 1–2 weeks | Order from DFRobot directly |
| XVF3800 ReSpeaker | Generally available | 1 week | Standard Seeed order |
| Motor-noise reference path (XVF3800 AEC) | Novel / unvalidated | N/A (bench test) | Phase 0 risk item #1 |
| RKNN model conversion per model | Engineering time | Days per model | Pipeline in Phase 0 week 2 |
| Custom carrier PCB (Phase 1) | NRE + iteration | 3–4 weeks per revision (JLCPCB) | Start KiCad schematic at end of Phase 0 |

---

## Cross-Vector Synthesis: The One Machine

### Master Block Diagram (Textual)

```
┌─────────────────────────────────────────────────────────────────┐
│                    VECTOR 3.0 ROBOT BODY                        │
│                                                                 │
│  ┌──────────────┐    UART 921600 baud     ┌─────────────────┐  │
│  │  STM32H743   │◄──── FlatBuffers IPC ──►│   RK3588S SoM   │  │
│  │  (L1 Safety) │                         │   (L2/L3 Brain) │  │
│  │              │                         │                 │  │
│  │ FreeRTOS     │    SPI (motor ref)      │ Linux + RKNN    │  │
│  │ FOC ×4 motors│──────────────────────► XVF3800           │  │
│  │ ICM-42688-P  │                         │                 │  │
│  │ VL53L0X ×4   │                         │ MIPI CSI ×3     │  │
│  │ AT42QT1070   │                         │ ├─ IMX678 (eye) │  │
│  │ BMP390       │                         │ ├─ OV9281 ×2    │  │
│  │ TMP117       │                         │ └─ OV5647 fish  │  │
│  │ Thermal mask │                         │                 │  │
│  │ IWDG safety  │                         │ I²C bus:        │  │
│  └──────────────┘                         │ VL53L8CX ×2     │  │
│         │                                 │ MLX90640        │  │
│         │ SPI / PWM                       │ BME280 VEML7700 │  │
│  ┌──────▼──────────────────────────────┐  │                 │  │
│  │  Actuator Layer                     │  │ M.2 PCIe:       │  │
│  │  4× BLDC + SimpleFOCMini + AS5600   │  │ RTL8852BE WiFi6 │  │
│  │  INA240 current sense ×4            │  │                 │  │
│  │  Thumb: BMP390 + 9DTact + TMP117    │  │ SPI:            │  │
│  └─────────────────────────────────────┘  │ DWM3000 UWB     │  │
│                                           │                 │  │
│  ┌──────────────────────┐                 │ I²S → TAS5760M  │  │
│  │  XVF3800 4-mic array │─── I²S PCM ───►│ → Speaker       │  │
│  │  AEC + beam + DoA    │                 │                 │  │
│  │  Motor-noise ref in  │                 │ SPI → Display   │  │
│  └──────────────────────┘                 │ 1.54″ 240×240   │  │
│                                           │ ST7789V IPS LCD │  │
│  ┌────────────────────────────────────┐   │                 │  │
│  │  Power: 3S 18650 / LiPo + BMS     │   │ LPDDR4x 8 GB    │  │
│  │  USB-C PD dock charge              │   │ eMMC 64 GB      │  │
│  │  25mm fan (thermal DVFS-gated)     │   └─────────────────┘  │
│  └────────────────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
                              │ WiFi 6 (local AP)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOCK 2.0                                     │
│  USB-C PD 9V/2A charge  │  LDROBOT LD19 LiDAR (room SLAM)     │
│  DWM3000 anchors ×2–4   │  STM32F411 dock MCU                  │
│  128 GB microSD ENGRAM   │  Optional: Mac Mini / Pi 5 (VLM)    │
│  WiFi 6 AP (isolated LAN)│  ENGRAM cold archive server          │
└─────────────────────────────────────────────────────────────────┘
```

### ENGRAM Pain Points Eliminated (vs Anki 2018)

| 2018 Pain Point (ENGRAM-rewrite report) | 2026 Solution |
|----------------------------------------|---------------|
| softfp ABI on APQ8009 — 6–8× fp16 slowdown | RK3588S aarch64 hard-float ABI, native fp16/int8 SIMD (NEON + dotprod) |
| fp16 storage-only, no compute | A76 supports fp16 arithmetic natively; NPU runs INT8 inference |
| No NPU — FFT on CPU (PFFFT expensive) | 6-TOPS NPU offloads vision; NEON dotprod accelerates HRR @ D=4096 |
| 512 MB RAM — no room for LLM or large ENGRAM | 8 GB LPDDR4x — SmolVLM2-256M + full ENGRAM hot store + OS simultaneous |
| No persistent memory — wipes on reboot | 64 GB eMMC hot store + 128 GB dock cold archive, mmap-friendly |
| No battery for continuous perception | 3S 18650 ~10–12 Wh → 2+ hour active runtime |
| Single camera, no depth | Multi-camera + VL53L8CX + MLX90640 + UWB position |

### The Honest Boundary

**Buildable now by a solo maker (Phase 0–1):**
- All compute and sensors at the part level — standard LCSC/Mouser/Seeed sourceable
- FDM/SLA enclosure — any Prusa-class printer
- SimpleFOC + FreeRTOS motor control — documented, community-supported
- RKNN vision inference — Rockchip SDK, documented
- 9DTact silicone sensor — open fabrication guide, ~4 hours, ~$25 in materials

**Needs custom PCB / engineering work (Phase 1):**
- Carrier PCB for RK3588S SoM + STM32H743 + all sensors — 5-layer KiCad, JLCPCB NRE ~$200
- Battery + PMIC integration — requires PCB layout and BMS validation
- MIPI CSI multi-camera routing — impedance-controlled traces, not breadboard-feasible

**Watch / next-rev (Phase 2 or later):**
- mmWave radar (TI IWR6843) — presence/vital signs compelling but firmware complex, defer
- UFS 3.1 storage — performance headroom available in eMMC; upgrade only if bottlenecked
- AMOLED display — revisit after Phase 1 field test of OLED burn-in risk
- Custom injection-molded shell — requires tooling investment ($2,000–10,000+)
- Hailo-8L NPU accelerator — adds 26 TOPS but requires custom driver integration; defer until
  RKNN NPU saturates for the perception workload

**Conscious divergences from Anki's 2018 choices:**
1. **BLDC over brushed DC** — quieter, but more complex motor driver (SimpleFOCMini adds $15/motor)
2. **Dedicated XVF3800 audio DSP** — replaces APQ8009 software DSP; adds $50 but saves all CPU
3. **Fan in enclosure** — Anki was fanless; 10 W SoC TDP requires forced convection
4. **LiDAR on dock, not body** — Anki had no LiDAR; the physics doctrine says dock LiDAR > body LiDAR
5. **WiFi 6 local-only AP** — Anki used cloud-connected WiFi; Vector 3.0 defaults offline-first

---

*V5–V14 full specification complete — 2026-06-26.*
*All 14 vectors now specified. Next step: V2 power/battery revision (quantify the 3S 18650 vs*
*LiPo pouch trade-off against the full power budget table from V1+V4+V5+V6+V7+V8+V9+V11+V12).*
