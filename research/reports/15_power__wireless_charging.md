# Power — Wireless Charging vs Pogo (research agent report)

*Returned by a research agent, 2026. Topic: replacing Anki's pogo-pin dock rails with wireless
(Qi2/MagSafe-style) charging. Fused into `design/benzy/POWER_ARCHITECTURE.md`.*

## TL;DR
- Wireless is feasible but **heat-bottlenecked, not power-bottlenecked**. A 15 W Qi2/MPP link refills a
  20–40 Wh pack in ~2.5–4.5 h — fine for a creature that *naps*. The real cost is **3–5 W of waste heat
  inches from a lithium pack** — the worst place to put heat in this robot.
- **The honest answer is a hybrid that leans pogo.** The owner's actual desire ("snaps on like an
  iPhone") comes from the **magnets**, not the coil. Magnet-aligned **pogo** gives the snap-on UX at
  ~95% efficiency, <1 W heat, ~$3 BoM, no EMI cert. Pure Qi2 costs efficiency, heat, ~$15–30, EMI work.
- If a fully sealed (no exposed metal) shell is mandatory: ST STWLC38 (RX) + STWBC-MC (TX) at 15 W +
  N52 MagSafe ring, with a dedicated heat path from the RX coil to the shell, and pogo/USB-C fallback.

## Recommendation
**Magnetic-pogo primary + USB-C limp-home; wireless as an optional Rev-B** (only if a sealed shell
becomes a hard requirement). Decouple "snap-align" (magnets) from "transfer" (contacts).

```
Primary: Dock USB-C PD → magnet ring self-aligns nose → spring pogo (≈0.05 Ω) →
         reverse-polarity ideal-diode + eFuse → BMS charger in the swappable pack → cells
Fallback (if wireless mandated): USB-C PD 20V → STWBC-MC TX → TX coil ╎air╎ N52 ring →
         RX coil → STWLC38 (rectifier+LDO, ~85%) → eFuse/OR with USB-C → BMS → cells (FOD+temp telemetry)
```

## Charge-time math (wall→pack: wireless ~75%, pogo/USB-C ~92%)
| Pack | Method | Link W | Eff | Into pack | 0→80% | ~full (CV taper) |
|---|---|---|---|---|---|---|
| 20 Wh | Qi2 15W | 15 | 75% | 11.3 W | ~1.4 h | ~2.2 h |
| 20 Wh | Qi2.2 25W | 25 | 75% | 18.8 W | ~0.85 h | ~1.4 h |
| 20 Wh | Pogo/USB-C 20W | 20 | 92% | 18.4 W | ~0.9 h | ~1.4 h |
| 30 Wh | Qi2 15W | 15 | 75% | 11.3 W | ~2.1 h | ~3.3 h |
| 30 Wh | Pogo/USB-C 30W | 30 | 92% | 27.6 W | ~0.9 h | ~1.4 h |
| 40 Wh | Qi2 15W | 15 | 75% | 11.3 W | ~2.8 h | ~4.5 h |
| 40 Wh | Pogo/USB-C 45W | 45 | 92% | 41 W | ~0.8 h | ~1.3 h (C-rate limited) |

15 W wireless = fine overnight, marginal for a 30-min top-up. Pogo/USB-C is faster *and* lets the
cell's own safe C-rate (not the link) be the limit. **Wireless throws away cell headroom you paid for.**

## Key parts
- TX: ST **STWBC-MC** (~$3–5, Qi TX PMIC, FOD); ST **STWBC2/STSC 50 W** board (targets mobile robots/drones);
  TI **BQ501210** (~$4–6, 15 W TX, FOD). Qi2 caps at 15 W, Qi2.2 at 25 W; >15 W needs proprietary mode.
- RX: ST **STWLC38** (~$3–6, 15 W EPP, sync rectifier+LDO, 4–12 V out, ~85%); ST **STWLC98** (up to 50 W STSC);
  NXP **MWPR1516** (15 W); TI **BQ51013B** (5 W, cheapest to prototype the chain).
- Coils: Würth 760308xxx / TDK WT-series TX/RX pairs ~$1–4; 15 W coils ~30–50 mm dia.
- Magnet ring: MagSafe-style N52 (~54×46×2.5 mm) ~$1–2 — **method-agnostic: aligns a coil OR a pogo cluster.**
- FOD: Qi mandates Q-factor (pre-power) + power-loss accounting (in-power). Dock-side FOD must run even
  with no robot present (a coin on the coil heats via eddy currents).

## Thermal & standby (the big risk, quantified)
- 15 W delivered at ~78% → ~3–4 W waste heat (worse at 75% → ~5 W), ~half on the robot near the cell.
  In a sealed ~105×80×130 mm shell that's +10–25 °C locally without a deliberate heat path → pushes a
  charging Li-ion toward its 0–45 °C ceiling. Pogo/USB-C dissipates <1 W, none near the battery.
- TX standby (polling pings): ~0.1–0.5 W vs ~0 W idle pogo dock — a real always-on appliance cost on a
  dock that already runs compute.

## Trade table
| Criterion | Wireless (Qi2/custom) | Pogo (magnet-aligned) | USB-C |
|---|---|---|---|
| Wall→pack eff | 75–80% | 92–95% | 92–95% |
| Heat near cell | 3–5 W (worst spot) | <1 W | <1 W |
| BoM | $15–30 | ~$3 | ~$1–2 |
| Complexity | High (coil tune, FOD, EMC) | Low | Lowest |
| UX/self-dock | Best (sealable) | Very good (snap+magnets) | Worst (human plugs) |
| Standby | 0.1–0.5 W | ~0 W | ~0 W |
| Anki-fit | Mixed | Strong | Weak as primary |

## Anki-way check (recommended magnetic-pogo)
C4 (reuse the magnet trick without the coil tax) · E5 (magnets misalign→still docks; pins dirty→USB-C
limp-home; dead pack→swap) · Q4 (pogo wear the only ding) · B5 (~$3, no EMC line item) · F5 (a napping
robot needs to land reliably and wake warm-not-hot). Pure wireless ≈ C5/E3/Q3/B2/F3.

## Risks / confidence
High on physics + part availability; medium on exact chain efficiency (measure it). **Cell C-rate
(sibling agent) sets the real floor** — if the cell only takes 0.5C, even 50 W wireless is wasted.
Wireless adds FCC Part 15/18 EMC effort; pogo/USB-C avoids it.

## Open decisions for Dexter
1. Is a sealed, no-exposed-metal shell a hard requirement? (Yes → wireless justified; No → magnetic-pogo wins.)
2. **Charge-in-place vs charge-a-spare** — highest-leverage: spare-charging kills the speed argument and
   rehabilitates 15 W wireless. (Resolve jointly with the backpack agent's second-bay idea.)
3. Acceptable charge time for the target pack Wh?
4. Watt of continuous waste heat the nose can shed without exceeding the pack's charge-temp ceiling?
5. Appetite for FCC Part 18 EMC (wireless) vs staying conducted (pogo/USB-C)?
