# Power — Swappable Hot-Swap Battery Backpack (research agent report)

*Returned by a research agent, 2026. One of four power/drone agents. Topic: the battery as a
user-swappable, hot-swap "backpack" module for Benzy. Fused into `design/benzy/POWER_ARCHITECTURE.md`.*

## TL;DR
- Build it as a 2S1P 21700 "backpack" (~12 Wh baseline, up to ~29 Wh usable for a long-life SKU)
  with an in-pack BQ40Z50 BMS, mated by a keyed high-current magnetic-pogo connector, OR-ed against
  a small internal supercap bridge via an LTC4368-class ideal-diode/hot-swap front end. The supercap
  rides the ~2–5 s swap only long enough for the STM32H7 to halt motors, flush ENGRAM/working state,
  and drop into a clean "nap" — a graceful-shutdown bridge, not a run-through UPS.
- A 2S 21700 pack hits "all-day-with-naps" easily and ~1 h continuous-active; 2 h continuous needs
  2S2P (~24 Wh) and gets heavy. Recommend ~12–16 Wh baseline + a charged spare.
- Moving the pack from base to rear-back hurts CG/tipping and collides with the drone-bay claim.
  Resolution: keep a small fixed low-CG buffer (supercap) in the base; make only the bulk energy
  pack the swappable backpack; standardize the bay as a shared mech/electrical interface.

## Recommendation
Two-tier system with a hard safety partition. Tier 1: a small permanently-installed base buffer
(supercap, low + central for CG) owning keep-alive/RTC/ride-through. Tier 2: the user-swappable
backpack — 2S1P 21700 (Molicel P45B or Si-anode P50B) with its own BQ40Z50-R2 BMS/gas-gauge (balancing,
protection, SHA-1 pack auth, SMBus telemetry to the RK3588S). Sources combined by an LTC4368
ideal-diode/hot-swap front end (inrush limit/soft-start + OR-ing). An LTC3110-managed supercap gives
the seconds of hold-up for a clean state-save-and-sleep. The STM32H7 (L1) owns the swap state machine:
on pack-removal detect → safe-stop motors → flush ENGRAM → cut motor rail → sleep (framed as a "nap").

```
   SWAPPABLE BACKPACK PACK: 2S1P 21700 (~12 Wh) + BQ40Z50 BMS
     PACK+/PACK-/SMBus/PRES  (keyed magnetic-pogo, 6-contact, 8–10A)
        │
   [ LTC4368 ideal-diode + hot-swap FETs ] ──► VSYS ─► RK3588S / sensors / motor-rail / STM32H7(AON)
        ▲ OR-ing
   [ base supercap buffer + LTC3110 ]  → rides the swap → STM32H7 runs the "nap" shutdown
```

## Pack sizing & runtime math
Usable ≈ 90% rated. 21700 P45B = 16.2 Wh/cell.

| Usage mode | Avg load | @2S1P 21700 (~29 Wh usable) | @~12 Wh usable |
|---|---|---|---|
| Idle/sleep | ~3.5 W | ~8.3 h | ~3.4 h |
| Awareness | ~6 W | ~4.8 h | ~2.0 h |
| Active drive+perception | ~12 W | ~2.4 h | ~1.0 h |
| Heavy (LLM+drive+arms) | ~22 W | ~1.3 h | ~0.55 h |
| Full burst | ~30 W | transient (pack+supercap) | — |

- 1 h target: met by ~12 Wh at active load; comfortable on 2S1P.
- 2 h continuous: needs full 2S1P 21700 (~140 g of cells — heavy on a 350–450 g robot).
- All-day-with-naps: any pack meets it (low duty cycle) → favors the lighter ~12 Wh pack + spare.

## Key findings (parts)
**Cells**
- Molicel INR-21700-P45B — Molicel/18650BatteryStore — ~$9–11 — 4.5 Ah, 16.2 Wh, 45 A cont., low DCR
  (good for motor inrush) — datasheet rev 1.2 (2024).
- Molicel INR-21700-P50B — ~$11–13 — ~5.0 Ah Si-C anode, ~1400 cycles (2025) — long-life SKU.
- Skip LiFePO4 (3.2 V nominal, lower volumetric density — too much size/weight for 350 g); NMC is right.

**Connector** (frequently-mated power+comms; 6 contacts: PACK+, PACK−, SDA, SCL, PRES, ID; ≥8–10 A)
- CFE/SUNMON high-current magnetic pogo (5–30 A) — ~$2–5 — self-aligning, low contact R.
- Mill-Max spring-loaded pogo — DigiKey/Mouser — ~$1–4/pin — US-sourceable prototype fallback.
- Keying: recessed PACK+ + magnet polarity; PRES make-last/break-first so controller sees removal first.

**Hot-swap bridge / OR-ing**
- TI BQ40Z50-R2 (pack BMS/gauge, SHA-1 auth, SMBus) — ~$4–6.
- ADI LTC4368 (ideal-diode + hot-swap, 2.5–60 V; over/under/reverse-V + OC) — ~$4–6.
- ADI LTC3110 (bidirectional supercap charger/backup, 0.1–5.5 V cap range) — ~$5–7.
- Supercap sizing: ~10 J needed (≈2 W × ~5 s); a 2-cell 2.5 F/2.7 V stack ≈ 13 J usable (margin for EOL).
- ⚠️ TPS2490 has 9 V min start — wrong on a 7.2 V 2S bus; use LTC4368 + a low-V e-fuse on motor rail.

**Swap UX & safety**
- Mid-motion is the danger case: on PRES break, STM32 must safe-stop *before* the rail drops (supercap
  buys this window). Gate "swap allowed" on stopped + arms parked; Benzy settles/sits before "sleeping."
- Guarded two-stage latch (press-guard + pull) so it can't pop off on a bump.
- Ideal-diode FET turns off before contacts part → contacts open de-energized (arcing/wear mitigation).
- BQ40Z50 FET protection + pack fuse + drop-rated enclosure; charge-status LED on the pack.
- UN38.3 (2026): 30% SoC air-transport limit now applies to batteries packed *with* devices — ship spares at 30%.

**Charging — where**
- Do both asymmetrically: dock charges the *installed* pack in-situ (nightly nap), AND a second dock bay
  charges the *spare* — so a fresh pack is always ready and the robot isn't the spare's charger.

## CG & stability
Battery is the heaviest single item (20–35% of mass). In-base = lowest CG, best tip margin, but not
user-accessible. In rear-backpack = raised + rearward CG → worse forward-tip under braking/arm reach;
also monopolizes the drone bay. **Resolution: split storage** — fixed low-CG base buffer (supercap)
+ swappable bulk backpack; standardize the bay as a shared power+SMBus+PRES interface the drone can
also use; mount cells low in the bay; software-limit arm extension/accel when a heavy long-life pack
is fitted (BMS reports pack ID → STM32 adapts the motion envelope — Anki-Way cleverness).

## Anki-way check
C: strong (supercap sized for a nap, not a UPS; pack-ID auto-tunes motion). E: strong (graceful
nap+ENGRAM flush, no brownout). Q: good (~$15–25 added BoM). B: strong (L1 owns the swap state machine
+ ideal-diode enable). F: strong (the swap *is* a nap — character beat; spare's LED = "feeding the creature").

## Risks / confidence
High on ICs + cells. Medium on magnetic-pogo vendor part numbers (validate mate-cycle life at full
current; Mill-Max is the safe fallback). Verified: TPS2490 unsuitable on 7.2 V. Unknown: real motor
stall/inrush (sets connector rating + inrush limit) and human swap duration (sets supercap size).

## Open decisions for Dexter
1. Pack SKU: ~12–16 Wh light (recommended default) vs 2S1P 21700 ~29 Wh long-life.
2. Base buffer = supercap-only (recommended, safe) vs a small base cell (more runtime, adds non-swappable Li-ion).
3. Connector: magnetic-pogo (creature feel) + guarded latch (retention) — recommended combo.
4. Commit to a shared drone/battery bay interface now, even if the drone slips? (Recommended.)
5. Pack auth: hard-reject vs warn-and-limit non-genuine packs (recommend warn-and-limit).
6. Validate before commit: motor stall/inrush, pogo mate-cycle life, user swap duration.
