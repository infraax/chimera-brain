# Power — Power Tree & Protection (research agent report)

*Returned by a research agent, 2026. Topic: the rail architecture, domains, protection, and budget —
the "power architecture" Flux.ai flagged. Fused into `design/benzy/POWER_ARCHITECTURE.md`.*

## TL;DR
- **Two hard-partitioned domains.** An always-on "lifeline" (STM32H743 + nano-LDO + pack gauge/wake,
  ~0.05–0.2 W) stays alive through swaps and deep-sleep; a switchable "application" domain (RK3588S,
  sensors, motors) is gated behind eFuses/load-switches the **L1 STM32 can cut independent of the SoC**.
- **3S pack (~9–12.6 V) → single ~12 V main bus** behind reverse-polarity + eFuse + bulk hold-up, then
  fan-out to a 5 V SoM rail (RK3588S has its own on-module RK806 PMIC — feed it raw 5 V, don't re-derive),
  3.3/1.8 V sensor rails, and an **isolated motor rail** (own eFuse + ferrite) so a stall can't brown out the SoC.
- Real 2026, solo-buildable: TPS2595 eFuse, LTC4359 ideal-diode, TPS54560/TPS563201 bucks, TPS22965/
  TPS22919 load switches, DRV8231A motor drivers, TPS3840 supervisor. ~30 Wh ≈ 3 h active; DVFS +
  STM32-owned throttle = graceful degradation before brownout.

## POWER TREE
```
3S BACKPACK PACK (9.0–12.6 V, ~20–40 Wh, own BMS+BQ40Z50 — sibling agent)
   │ hot-swap connector: staggered GND-first, then VBAT, then SMBus
   ▼
[REVERSE-POLARITY] LTC4359 ideal-diode + N-FET
   ▼
[SYSTEM eFUSE] TPS2595 (Ilim≈4A, dV/dt soft-start, OVP clamp, OCP, /FLT→STM32)
   ├─[BULK HOLD-UP] 2–4×470–1000µF + 10µF ceramics (swap ride-through / brownout buffer)
   ▼ VSYS (~9–12.6 V)
   ├── LIFELINE (ALWAYS-ON, ~0.05–0.2 W) ───────────────
   │     ├ TPS7A02/TLV75533 → 3V3_AON
   │     ├ STM32H743 (L1 SAFETY PARTITION)
   │     ├ power button + wake/latch logic
   │     ├ pack gas-gauge SMBus / ID detect
   │     └ TPS3840 supervisor (VSYS UVLO + reset)
   ├── APPLICATION (STM32-GATED; EN on every block → HARD CUT) ─────────
   │     ├ TPS54560 BUCK 5V (≤5A) → RK3588S SoM 5V in → (on-SoM RK806 makes CPU/GPU/NPU/DDR/IO + sequencing)
   │     ├ TPS62913/TPS563201 BUCK 3V3 (≤3A) [TPS22965 switch] → WiFi6, LCD, XVF3800, ToF/LiDAR, MLX90640, IMU, UWB, touch
   │     ├ TLV75518 LDO 1V8 (≤300mA) → sensor I/O + XVF3800 core
   │     └ MOTOR RAIL — ISOLATED: [eFUSE TPS2595]→VMOT +[BULK 2×470µF + ferrite/π]
   │            DRV8231A×2 (drive L/R, IPROPI stall→STM32), DRV8231A head, DRV8231A lift,
   │            DRV8231A×2 arms (aspirational), low-side FET+flyback electromagnet
   ▼ CHARGE: Qi2/pogo → charger → pack (sibling agents); system runs from VSYS while charging
```
Note: the RK3588S SoM integrates the RK806-2 PMIC (makes + sequences all RK3588 rails). The carrier
delivers clean 5 V (some SoMs want 12 V — confirm) + PG signals; **do not re-implement the SoC rail tree.**

## Lifeline vs switchable + swap/sleep
- **Lifeline (always-on):** LTC4359 + eFuse conducting; 3V3_AON LDO; STM32; button/wake; gauge SMBus;
  supervisor. The only thing alive in deep-sleep and during a swap.
- **Switchable (STM32-gated):** 5V0_SOM, 3V3_PER, 1V8_PER, the entire motor rail — all default-OFF on
  cold boot; STM32 can drop any/all instantly.
- **Swap:** staggered connector; on removal detect, bulk + lifeline carry the STM32 (size bulk ≥200–500 ms),
  or if active → clean quiesce (pause motors, suspend RK3588 to RAM, gate app domain). Optional 0.1–1 F
  supercap on 3V3_AON for true uninterrupted swaps.
- **Nap/deep-sleep:** gate the app domain (RK3588 off for deep-sleep; S2R for fast nap); wake on
  button/IMU-tap/timer/UWB-presence → approaches the ~0.05–0.2 W floor (days–weeks standby).

## Key ICs
- LTC4359 (ideal-diode, reverse to −40 V) ~$3–4 · TPS2595 (eFuse 2.7–18 V/4 A, adj Ilim+slew, OVP/OCP)
  ~$1.5–2 (one for system, one for motor; TPS2596 for higher I) · TPS54560 (60 V/5 A sync buck, Eco-mode)
  ~$2–3 (5 V SoM) · TPS563201 (4.5–17 V/3 A buck) ~$0.6 · TPS62913 (low-noise buck for radios) ~$2 ·
  TPS22965 (6 A load switch) ~$0.8 · TPS22919 (1.5 A load switch) ~$0.6 · DRV8231A (brushed H-bridge
  3.7 A, IPROPI current sense) ~$1.2 · DRV8214 (ripple-count/I²C stall) ~$1.5 · TPS3840 (nano-power
  supervisor 350 nA) ~$0.5 · TPS7A02/TLV75533 (nano-Iq LDO for 3V3_AON) ~$0.3–0.5 · BQ40Z50 (pack
  gauge+protection+auth; pack-side) ~$4–6. All have EVMs (dev-board-first).
- ⚠️ If "tracked-drive BLDC" is genuinely 3-phase, DRV8231A (brushed) is wrong for traction → use
  DRV8316/DRV8353 + FETs. DRV8231A is correct for brushed/geared head/lift/arm.

## Power-state & budget (W)
| Block | Deep-sleep | Nap (S2R) | Idle-aware | Active | Burst | Charging(idle) |
|---|---|---|---|---|---|---|
| Lifeline | 0.05 | 0.10 | 0.15 | 0.20 | 0.20 | 0.15 |
| 5V0_SOM (RK3588S) | 0 | 0.30 | 1.0 | 6.0 | 12.0 | 1.0 |
| 3V3_PER | 0 | 0.10 | 1.5 | 3.0 | 3.5 | 1.5 |
| 1V8_PER | 0 | 0 | 0.2 | 0.4 | 0.5 | 0.2 |
| Motor (VMOT) | 0 | 0 | 0 | 4.0 | 10.0 | 0 |
| Conv. losses (~12%) | 0.01 | 0.06 | 0.5 | 1.6 | 3.1 | 0.5 |
| **Total** | **~0.06** | **~0.66** | **~3.9** | **~15.2** | **~29.3** | **~4.4 +charge** |

Runtime (usable ≈ 90%): deep-sleep ~12/19/25 days · nap ~27/41/55 h · idle-aware ~4.6/6.9/9.2 h ·
active (realistic 8–10 W) ~2/3/4 h · heavy(15 W) ~1.2/1.8/2.4 h — for 20/30/40 Wh. **30 Wh baseline
≈ 3 h realistic active**; 40 Wh if the arms ship. **DVFS governor (STM32-owned):** watch eFuse/IPROPI
current + temps + pack SoC → step RK3588 DVFS down, shed LLM rail, cap motor PWM, then clean-suspend —
the creature "gets sleepy" before browning out/overheating.

## Protection
Inrush/soft-start (TPS2595 dV/dt + staggered EN); OVP (eFuse clamp + TVS); OCP (separate eFuse on VSYS
and VMOT, /FLT→STM32); reverse-polarity (LTC4359, zero drop); brownout/UVLO (TPS3840 + BQ40Z50 cell UV);
**motor-rail isolation** (separate branch, own eFuse, local 2×470µF + ferrite/π — stall di/dt absorbed
locally, doesn't pull the 5 V SoM input); flyback on the electromagnet; star-ground with separate motor
return. **L1 hard cut:** STM32 (lifeline-powered, never SoC-dependent) drives EN of motor eFuse + app
switches → kills motors+SoC on watchdog/over-temp/over-current/tilt/button-hold, backed by a hardware
**kill latch** clearable only by STM32. RK3588 ↔ STM32 handshake (host-alive GPIO + PG-gated rails +
heartbeat); STM32 always wins arbitration.

## Anki-way check
C: discrete-but-cheap (~$20–30; no big PMIC since the SoM has RK806). E: sync bucks + nano-LDO/supervisor
(sub-200 µW floor) + ideal-diode (no diode drop) + DVFS. Q: independent eFuses, supervisor UVLO, TVS,
motor isolation, per-rail fault flags. B: honest budget (8–10 W realistic → 3 h/30 Wh). F: true hard
safety partition + "gets sleepy then naps" degradation.

## Risks / confidence
Medium: exact SoM input voltage (5 V vs 12 V — confirm chosen SoM + that RK806 sequencing is on-module);
motor type per axis (3-phase vs brushed → driver choice); hot-swap ride-through ms (sets bulk/supercap);
stall current ceiling (sets motor eFuse Ilim + bulk); LLM-on-RK3588 sustained thermals (thermal-driven
DVFS). High that parts exist; verify live stock.

## Open decisions for Dexter
1. Exact RK3588S SoM + its input voltage (5 V vs 12 V) and on-module sequencing.
2. Bus voltage: single ~12 V VSYS vs run VSYS = raw pack and buck only where needed.
3. Motor types per axis (3-phase BLDC vs brushed/geared) → driver + eFuse sizing.
4. Swap contract: uninterrupted (supercap/large bulk) vs clean ~1 s nap (cheaper).
5. Pack size: 20/30/40 Wh (recommend 30 Wh baseline; 40 Wh if arms ship).
6. Wired-charge fallback (USB-C/barrel) in addition to Qi2/pogo? (LTC4359 OR-ing leaves room.)
7. Kill-latch: pure hardware (most robust) vs STM32-GPIO-only.
