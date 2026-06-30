# Benzy — Power Architecture (fused)

*The power architecture Flux.ai flagged as missing, synthesized from three research agents
(`research/reports/14_power__swappable_backpack.md`, `15_power__wireless_charging.md`,
`16_power__power_tree_protection.md`). The three converge cleanly into one design; where they
diverge (wireless vs pogo) it's surfaced as a decision, not hidden.*

> Owner direction driving this: the **battery is a swappable "backpack" module**, charging should feel
> **"snap-on like an iPhone,"** and the system must **power down gracefully when the pack is pulled.**

---

## 1. The architecture in one picture
**Two power domains + split storage + a magnet-aligned charge interface.**

```
            ┌── SWAPPABLE BACKPACK PACK (2S/3S Li-ion, ~12–30 Wh) ──┐
            │   Molicel P45B/P50B cells + BQ40Z50 BMS (auth+SMBus)  │
            └── PACK+/PACK−/SDA/SCL/PRES (keyed magnetic-pogo 8–10A)─┘
                              │ (PRES make-last/break-first)
   [LTC4359 ideal-diode (reverse-polarity, OR-ing)] ─ [TPS2595 system eFuse (inrush/OVP/OCP)]
                              │  + BULK HOLD-UP (470–1000µF ×2–4)
        ┌─────────────────── VSYS (~9–12.6 V) ───────────────────┐
        │                                                          │
   LIFELINE DOMAIN (always-on ~0.05–0.2 W)          APPLICATION DOMAIN (STM32-gated, default-OFF)
   ├ nano-LDO → 3V3_AON                              ├ TPS54560 buck 5V → RK3588S SoM (on-SoM RK806 makes its rails)
   ├ STM32H743  ← L1 SAFETY PARTITION                ├ buck 3V3 + LDO 1V8 → sensors/radios (load-switched)
   ├ power button + wake (IMU/timer/UWB)             └ ISOLATED MOTOR RAIL: TPS2595 eFuse + ferrite/π + bulk
   ├ pack gas-gauge SMBus                                 → DRV8231A drivers (drive/head/lift/arms) + e-magnet
   └ TPS3840 supervisor (+ hardware KILL LATCH)
        │
   FIXED BASE BUFFER: supercap bank (+ LTC3110) ── low & central for CG ── rides the swap → "nap"
        │
   CHARGE IN: magnet-aligned pogo (primary) / USB-C limp-home / [Qi2 wireless = optional Rev-B]
```

Three ideas do all the work:
1. **Split the storage** — a small **fixed low-CG supercap buffer in the base** + the **bulk energy in
   the swappable backpack**. Keeps Vector-grade tip stability *and* delivers the swappable UX *and*
   leaves the bay free to also host the drone (shared interface).
2. **Two hard-partitioned domains** — an always-on **lifeline** (the L1 STM32 + gauge + wake) and a
   **switchable application domain** the STM32 can cut unilaterally (hardware kill-latch the RK3588
   can't override). This is the safety partition, now extended to *power*.
3. **Magnets ≠ coils** — the "snap-on like an iPhone" feel comes from a **MagSafe-style magnet ring**;
   put **pogo contacts** behind it for ~95% efficiency and ~0 heat. True wireless is a later option.

---

## 2. The swap = a "nap" (the graceful-shutdown behavior)
On `PRES` break (or VSYS droop), the **L1 STM32 owns the sequence**, riding on the base supercap +
bulk hold-up (~10–13 J, sized for a clean shutdown — *not* a UPS):
1. command motors to a **safe stop** (and only allow swaps when stopped + arms parked),
2. signal the RK3588S to **flush ENGRAM/working state** (suspend-to-RAM for a fast nap, or full off),
3. **gate the application domain** off,
4. **sleep** on the lifeline floor.
Re-inserting a charged pack **wakes** it. Framed to the user: Benzy settles, parks its arms, closes its
eyes, and naps while you change its pack — the constraint becomes a character beat (the Anki way).

---

## 3. Budget & runtime (reconciled)
| State | System draw | Runtime @20/30/40 Wh |
|---|---|---|
| Deep-sleep | ~0.06 W | ~12 / 19 / 25 days |
| Nap (suspend-to-RAM) | ~0.66 W | ~27 / 41 / 55 h |
| Idle-aware | ~3.9 W | ~4.6 / 6.9 / 9.2 h |
| Active (realistic 8–10 W) | ~9 W | ~2 / 3 / 4 h |
| Heavy (LLM+drive+arms) | ~15 W | ~1.2 / 1.8 / 2.4 h |
| Burst (peak, transient) | ~29 W | pack + supercap supply it |

**Baseline recommendation: a ~30 Wh pack ≈ 3 h realistic active + multi-day nap**, with a lighter
~12–16 Wh SKU for an arms-free build and a charged **spare in a second dock bay** so untethered time is
effectively unlimited. An **STM32-owned DVFS governor** (watching eFuse/IPROPI current + temps + pack
SoC) steps the RK3588 down, sheds the LLM rail, caps motor PWM, then clean-suspends — Benzy visibly
"gets sleepy" before it browns out or overheats.

---

## 4. Protection (the Flux gap, closed)
- **Reverse-polarity:** LTC4359 ideal-diode (−40 V tolerant, zero drop — preserves runtime, leaves OR-ing headroom).
- **Inrush/soft-start:** TPS2595 dV/dt + staggered rail enables (caps charge through a controlled ramp).
- **OVP:** eFuse clamp + a TVS across VSYS for hot-plug/ESD spikes.
- **OCP / e-fuse:** independent TPS2595 on VSYS *and* on the motor rail (a motor short trips the motor
  fuse without killing the brain); each `/FLT` → STM32.
- **Brownout/UVLO:** TPS3840 nano-power supervisor + the pack BMS cell-UV as last line.
- **Motor-rail isolation (key):** physically separate branch — own eFuse, local 2×470 µF + ferrite/π —
  so stall di/dt and PWM ripple can't pull down the 5 V SoM input. Flyback clamp on the electromagnet.
- **L1 hard cut:** the lifeline-powered STM32 drives the EN of the motor eFuse + app switches and a
  hardware **kill latch** (clearable only by STM32) → kills motors+SoC on watchdog/over-temp/over-current/
  tilt/drop/button-hold, independent of the RK3588.

---

## 5. Charging — the wireless-vs-pogo call (honest divergence)
You asked for iPhone-style wireless. The agents' honest finding: **the magnets give you the snap-on UX;
the coil costs you 3–5 W of heat right next to the lithium pack, ~75% efficiency, ~$15–30, and FCC Part
18 work.** So:

| | Magnetic-pogo (recommended) | Pure Qi2 wireless |
|---|---|---|
| Wall→pack | ~92–95% | ~75–80% |
| Heat near cell | <1 W | 3–5 W (worst spot) |
| BoM / cert | ~$3 / none | $15–30 / FCC Part 18 |
| Snap-on feel | ✅ (same magnet ring) | ✅ |
| Sealed no-metal shell | ✗ | ✅ |

**Recommendation: magnet-aligned pogo primary + USB-C limp-home; reserve true Qi2 wireless for a Rev-B**
*if* a fully sealed (washable, no exposed metal) shell becomes a hard requirement. **Key unlock:** if the
**dock charges a *spare* pack** while Benzy runs on the installed one, charge *speed stops mattering* —
which would rehabilitate 15 W wireless. So the wireless question is downstream of the spare-charging
decision. (Parts if wireless: ST STWLC38 RX + STWBC-MC TX + N52 ring; the ring is method-agnostic.)

---

## 6. Bill of core ICs (all real, 2026, dev-board-first)
Pack: Molicel P45B/P50B 21700 · BQ40Z50-R2 BMS. Front-end: LTC4359 ideal-diode · TPS2595 eFuse ×2 ·
LTC3110 supercap manager + supercaps · TVS. Rails: TPS54560 (5 V SoM) · TPS563201/TPS62913 (3V3) ·
TLV75518 (1V8) · TPS22965/TPS22919 (load switches) · TPS7A02 (3V3_AON) · TPS3840 (supervisor). Motors:
DRV8231A (brushed head/lift/arm) — **or DRV8316/DRV8353 + FETs if traction is true 3-phase BLDC**.
Connector: high-current magnetic-pogo (Mill-Max fallback). Est. added BoM ~$35–55 over a fixed pack.

---

## 7. Consolidated open decisions (your call) + validation gates
**Decisions the agents agree need you:**
1. **Pack size SKU** — 30 Wh baseline (recommended) vs 12–16 Wh light vs 40 Wh "arms" build.
2. **Charge-in-place vs charge-a-spare** (highest leverage — also decides whether wireless is worth it).
3. **Wireless vs magnetic-pogo** (gated on #2 and "is a sealed shell mandatory?").
4. **Swap contract** — uninterrupted (bigger supercap/bulk) vs clean ~1 s nap (cheaper). Recommend nap.
5. **Base buffer** — supercap-only (recommended, safe) vs a small base cell (more runtime, adds Li-ion).
6. **Bus voltage** — single ~12 V VSYS vs run VSYS = raw pack.
7. **Wired-charge fallback** (USB-C/barrel) in addition? **Kill-latch** — pure hardware (recommended) vs GPIO-only.

**Validation gates (measure before committing PCB):**
- **Motor stall/inrush current** (sets connector rating, motor-eFuse Ilim, bulk) — biggest unknown.
- **Exact RK3588S SoM input voltage** (5 V vs 12 V) and that RK806 sequencing is fully on-module.
- **Motor type per axis** (3-phase BLDC vs brushed/geared → driver choice).
- **Real swap duration + EOL supercap derating** (sets hold-up size).
- **Pack C-rate** (sets the real charge-speed ceiling — wireless wattage is moot if the cell can't take it).
- **Magnetic-pogo mate-cycle life at full current** (Mill-Max fallback if the cheap parts don't last).

> Next step once you pick #1–#7: draw the schematic-level power tree (KiCad/Flux) from §1, then the
> torso CAD gets the real volumes for the pack bay, supercap, eFuse board, and the magnet-ring charge face.
