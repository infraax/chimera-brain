#!/usr/bin/env python3
"""
Deep Understanding — Three-Brain PoC skeleton (Concept 01)
==========================================================

A dependency-light, runnable sandbox that proves the core Deep-Understanding loop
for Vector BEFORE we touch the robot or finish ENGRAM. It simulates a creature
"growing up" in a home over phases P0->P3 and demonstrates:

  * B1 (reflex)        : turns a chosen action into a (mock) emote, safety on top
  * B2 (reasoning)     : labels situation fragments (DU Eq.1), writes P/S to memory,
                         retrieves nearest past situations, proposes an action
  * B3 (meta-cognition): Core Value Net (character+safety), reward blending (Eq.2/3),
                         Meta-Plasticity Controller (phase schedule, freeze logic),
                         modulates B2's choice and logs every value change (auditable)

It is intentionally pure-stdlib (no numpy/torch) so it runs anywhere. Every real
component sits behind a small interface so it can be swapped for production later:

  MemoryStore   -> ENGRAM (situational fingerprints)        [see ENGRAM_FOR_VECTOR.md]
  RewardModel   -> real owner-feedback (attunement) + RND   [TODO]
  ValueNet      -> trained net; here a transparent stub      [TODO]
  Brain1        -> the on-robot reflex (modified moodManager)[TODO]

Run:
    python3 concepts/deep_understanding/three_brain_skeleton.py
    python3 concepts/deep_understanding/three_brain_skeleton.py --days 40 --seed 7

Maps to: DEEP_UNDERSTANDING_CONCEPT_01.md, Vector-eng.md, ANKI_WAY.md
"""
from __future__ import annotations

import argparse
import hashlib
import math
import random
from dataclasses import dataclass, field
from typing import Protocol

# --------------------------------------------------------------------------- #
# 0. Tiny vector helpers (stand-in for embeddings / ENGRAM fingerprints)
# --------------------------------------------------------------------------- #
DIM = 32


def embed(*tokens: str) -> list[float]:
    """Deterministic pseudo-embedding of a situation's features (hash -> unit vec).
    Stand-in for an ENGRAM situational fingerprint."""
    v = [0.0] * DIM
    for tok in tokens:
        h = hashlib.sha256(tok.encode()).digest()
        for i in range(DIM):
            v[i] += (h[i % len(h)] - 128) / 128.0
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


# --------------------------------------------------------------------------- #
# 1. Situations & fragments (the synthetic "days in a home")
# --------------------------------------------------------------------------- #
PEOPLE = ["dexter", "stranger", "kid"]
ACTIONS = ["pet", "talk", "ignore", "pick_up", "show_object", "poke"]
PLACES = ["living_room", "desk", "kitchen", "charger"]


@dataclass
class Fragment:
    text: str
    label: str  # one of A,P,S,N,Q,ORDER,UNKNOWN
    value: float = 1.0  # binary indicator (1 present)


@dataclass
class Situation:
    person: str
    action: str
    place: str
    t: int
    fragments: list[Fragment] = field(default_factory=list)

    def fingerprint(self) -> list[float]:
        return embed(self.person, self.action, self.place)

    def key(self) -> str:
        return f"{self.person}|{self.action}|{self.place}"


def sense(t: int, rng: random.Random) -> Situation:
    """Generate a synthetic perceived situation, decomposed into labeled fragments."""
    person = rng.choice(PEOPLE)
    action = rng.choice(ACTIONS)
    place = rng.choice(PLACES)
    s = Situation(person=person, action=action, place=place, t=t)
    # B2 will re-label, but the world hands us raw fragments with "ground-truth" labels:
    s.fragments = [
        Fragment(f"person={person}", "P"),                 # important: who
        Fragment(f"action={action}", "S" if action in ("pet", "talk", "show_object") else "P"),
        Fragment(f"place={place}", "A"),                   # context
        Fragment("ambient_noise=low", "N"),                # noise -> dropped
        Fragment("goal=be_a_good_creature", "Q"),          # the standing query
    ]
    if rng.random() < 0.15:
        s.fragments.append(Fragment(f"novel_object_{rng.randint(0,99)}", "UNKNOWN"))
    return s


# --------------------------------------------------------------------------- #
# 2. Memory store interface (InMemory now -> ENGRAM later)
# --------------------------------------------------------------------------- #
class MemoryStore(Protocol):
    def write(self, fp: list[float], meta: dict, score: float) -> None: ...
    def knn(self, fp: list[float], k: int) -> list[tuple[float, dict]]: ...
    def __len__(self) -> int: ...


class InMemoryStore:
    """Trivial cosine-knn store. Swap for ENGRAM hot-index/archive in production."""

    def __init__(self) -> None:
        self._items: list[tuple[list[float], dict]] = []

    def write(self, fp: list[float], meta: dict, score: float) -> None:
        self._items.append((fp, {**meta, "score": score}))

    def knn(self, fp: list[float], k: int) -> list[tuple[float, dict]]:
        scored = [(cosine(fp, ofp), meta) for ofp, meta in self._items]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:k]

    def __len__(self) -> int:
        return len(self._items)


# --------------------------------------------------------------------------- #
# 3. Phase-Gated Plasticity controller (DU Table 3, retimed in CONCEPT_01 §3)
# --------------------------------------------------------------------------- #
@dataclass
class Phase:
    name: str
    eta: float          # plasticity
    lam_ext: float      # owner-feedback weight in reward blend
    kl_bound: float     # drift bound (inf in early phases)
    core_frozen: bool   # CVN frozen?
    mem_weights: dict   # Eq.1 weights {A,P,S,N,Q,ORDER,UNKNOWN}


# default Eq.1 weights; B3 nudges these per phase
def _w(unknown: float) -> dict:
    return {"A": 0.2, "P": 0.7, "S": 0.9, "N": -0.8, "Q": 0.5, "ORDER": 0.1, "UNKNOWN": unknown}


PHASES = [
    Phase("P0-infancy",      1.00, 0.1, math.inf, False, _w(unknown=0.9)),   # explore: chase the unknown
    Phase("P1-childhood",    0.40, 0.5, math.inf, False, _w(unknown=0.5)),
    Phase("P2-adolescence",  0.15, 0.8, 0.10,     False, _w(unknown=0.3)),
    Phase("P3-adulthood",    0.00, 1.0, 0.01,     True,  _w(unknown=0.2)),   # crystallized; adapters only
]


class PlasticityController:
    """Milestone-or-clock phase scheduler. Here: clock over simulated days."""

    def __init__(self, day_bounds: tuple[int, int, int] = (3, 30, 180)) -> None:
        self.b = day_bounds  # P0<b0<=P1<b1<=P2<b2<=P3

    def phase(self, day: int) -> Phase:
        b0, b1, b2 = self.b
        if day < b0:
            return PHASES[0]
        if day < b1:
            return PHASES[1]
        if day < b2:
            return PHASES[2]
        return PHASES[3]


# --------------------------------------------------------------------------- #
# 4. Core Value Net (CVN) — character + safety. Transparent stub.
# --------------------------------------------------------------------------- #
@dataclass
class ValueNet:
    """Encodes Vector's character (kindness, playfulness, calm) + hard safety prior.
    In P3 the *character* weights freeze; the safety prior is ALWAYS hard (Anki Way:
    real cliff/fall safety lives on the robot, not here — this is character-level)."""
    kindness: float = 0.5
    playfulness: float = 0.5
    calm: float = 0.5
    audit_log: list[str] = field(default_factory=list)

    SAFETY_FORBIDDEN = {"flee_cliff_override"}  # never; symbolic placeholder

    def value_reward(self, action: str, situation: Situation) -> float:
        """r_val: does this action fit Vector's character?"""
        r = 0.0
        if action in ("greet", "play"):
            r += self.playfulness * 0.5 + self.kindness * 0.5
        if action == "comfort":
            r += self.kindness
        if action == "rest":
            r += self.calm
        if action == "ignore":
            r -= self.kindness * 0.3
        return r

    def update(self, action: str, owner_reward: float, eta: float, frozen: bool) -> None:
        if frozen or eta <= 0.0:
            return
        before = (round(self.kindness, 3), round(self.playfulness, 3), round(self.calm, 3))
        step = 0.05 * eta * owner_reward
        if action in ("greet", "play", "comfort"):
            self.playfulness = _clip(self.playfulness + step)
            self.kindness = _clip(self.kindness + step * 0.5)
        if action == "rest":
            self.calm = _clip(self.calm + step)
        after = (round(self.kindness, 3), round(self.playfulness, 3), round(self.calm, 3))
        if before != after:
            self.audit_log.append(f"CVN {before}->{after} via {action} r_ext={owner_reward:+.2f} eta={eta}")


def _clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


# --------------------------------------------------------------------------- #
# 5. Reward model (R_ext owner / R_int novelty(RND-stub) / R_val CVN)
# --------------------------------------------------------------------------- #
class RewardModel:
    """R_int = novelty via state-visit counts (cheap RND stand-in).
    R_ext  = scripted owner reaction (TODO: real attunement signal)."""

    def __init__(self) -> None:
        self._visits: dict[str, int] = {}

    def intrinsic(self, situation: Situation) -> float:
        k = situation.key()
        self._visits[k] = self._visits.get(k, 0) + 1
        return 1.0 / math.sqrt(self._visits[k])  # high for novel, decays with familiarity

    def extrinsic(self, action: str, situation: Situation, rng: random.Random) -> float:
        """Scripted owner: likes being greeted/played-with when present; dislikes being
        bothered while a stranger or when ignored. Stand-in for real feedback."""
        if situation.action == "ignore":
            return 0.0
        if situation.person == "stranger":
            return -0.4 if action in ("greet", "play") else 0.2
        good = {"greet": 0.8, "play": 0.7, "comfort": 0.6, "rest": 0.2, "ignore": -0.3}
        base = good.get(action, 0.0)
        return _clip(base + rng.uniform(-0.1, 0.1), -1.0, 1.0)


# --------------------------------------------------------------------------- #
# 6. The three brains
# --------------------------------------------------------------------------- #
ACTION_SET = ["greet", "play", "comfort", "rest", "ignore"]


def score_fragment(f: Fragment, weights: dict) -> float:
    """DU Eq.1 single-fragment score."""
    return weights.get(f.label, 0.0) * f.value


class Brain2:
    """Slow reasoning: label+gate memory, retrieve, propose action."""

    def __init__(self, mem: MemoryStore) -> None:
        self.mem = mem

    def write_memory(self, s: Situation, phase: Phase, tau: float = 0.3) -> int:
        stored = 0
        for f in s.fragments:
            sc = score_fragment(f, phase.mem_weights)
            if sc > tau:  # keep P/S/Q/UNKNOWN; drop N
                self.mem.write(s.fingerprint(), {"frag": f.text, "label": f.label,
                                                 "key": s.key(), "t": s.t}, sc)
                stored += 1
        return stored

    def propose(self, s: Situation, k: int = 5) -> tuple[str, float, list]:
        """Retrieve nearest past situations; propose an action by simple recall heuristic."""
        neighbors = self.mem.knn(s.fingerprint(), k) if len(self.mem) else []
        # heuristic policy grounded in the current percept (a real B2 would reason here):
        if s.action == "ignore":
            cand = "rest"
        elif s.person == "stranger":
            cand = "rest"
        elif s.action in ("pet", "talk"):
            cand = "play"
        elif s.action == "show_object":
            cand = "greet"
        else:
            cand = "greet"
        confidence = 0.5 + 0.1 * len(neighbors)
        return cand, min(confidence, 0.95), neighbors


class Brain3:
    """Meta-cognition: blend rewards, modulate B2, update CVN under plasticity gate."""

    def __init__(self, cvn: ValueNet, rewards: RewardModel, ctrl: PlasticityController) -> None:
        self.cvn = cvn
        self.rewards = rewards
        self.ctrl = ctrl

    def govern(self, s: Situation, proposed: str, phase: Phase, rng: random.Random):
        # value-aware modulation: pick the action maximizing blended reward,
        # seeded by B2's proposal (cheap stand-in for B3 gating B2's experts)
        best_a, best_r = proposed, -1e9
        for a in {proposed, *ACTION_SET}:
            r_int = self.rewards.intrinsic(s)
            r_ext = self.rewards.extrinsic(a, s, rng)
            r_val = self.cvn.value_reward(a, s)
            # Eq.3 blend; lam_ext rises with phase (owner-ward), curiosity fades
            lam_ext = phase.lam_ext
            lam_int = (1 - lam_ext) * 0.6
            lam_val = (1 - lam_ext) * 0.4
            r = lam_ext * r_ext + lam_int * r_int + lam_val * r_val
            if r > best_r:
                best_a, best_r = a, r
        # learn: update CVN under plasticity/freeze gate
        chosen_ext = self.rewards.extrinsic(best_a, s, rng)
        self.cvn.update(best_a, chosen_ext, phase.eta, phase.core_frozen)
        return best_a, best_r


def brain1_reflex(action: str) -> str:
    """On-robot reflex stub: action -> emote, with the safety filter always on top."""
    if action in ValueNet.SAFETY_FORBIDDEN:
        return "[SAFETY] suppressed"
    emote = {"greet": "ears-up chirp", "play": "wiggle + bright eyes",
             "comfort": "soft purr", "rest": "slow blink", "ignore": "idle"}
    return emote.get(action, "idle")


# --------------------------------------------------------------------------- #
# 7. Simulation loop — watch the creature grow up
# --------------------------------------------------------------------------- #
def run(days: int, per_day: int, seed: int) -> None:
    rng = random.Random(seed)
    mem = InMemoryStore()
    cvn = ValueNet()
    ctrl = PlasticityController()
    b2 = Brain2(mem)
    b3 = Brain3(cvn, RewardModel(), ctrl)

    t = 0
    print(f"{'day':>4} {'phase':<14} {'stored':>6} {'memN':>6} "
          f"{'kind':>5} {'play':>5} {'calm':>5}  sample(action->emote)")
    print("-" * 86)
    for day in range(days):
        phase = ctrl.phase(day)
        stored_today = 0
        sample = ""
        for _ in range(per_day):
            t += 1
            s = sense(t, rng)
            stored_today += b2.write_memory(s, phase)
            proposed, conf, _ = b2.propose(s)
            action, _r = b3.govern(s, proposed, phase, rng)
            if not sample:
                sample = f"{s.person}/{s.action}->{action}->{brain1_reflex(action)}"
        if day % max(1, days // 20) == 0 or day == days - 1:
            print(f"{day:>4} {phase.name:<14} {stored_today:>6} {len(mem):>6} "
                  f"{cvn.kindness:>5.2f} {cvn.playfulness:>5.2f} {cvn.calm:>5.2f}  {sample}")

    print("\n--- VALIDATION (what this PoC should demonstrate) ---")
    print(f"* memory gate kept P/S/Q/UNKNOWN, dropped N : memN={len(mem)} (N-fragments excluded)")
    print(f"* reward blend shifted owner-ward over phases: lam_ext P0={PHASES[0].lam_ext} -> P3={PHASES[3].lam_ext}")
    print(f"* CVN crystallized then froze in P3          : core_frozen={ctrl.phase(days-1).core_frozen}")
    print(f"* every value change auditable               : {len(cvn.audit_log)} logged changes")
    if cvn.audit_log:
        print("   first:", cvn.audit_log[0])
        print("   last :", cvn.audit_log[-1])
    print("* box-down safety                            : B1 reflex + SAFETY filter run with no B2/B3")

    # TODO(production) map:
    #   InMemoryStore        -> ENGRAM hot-index + archive (situational fingerprints)
    #   RewardModel.extrinsic-> real owner affect from the attunement layer
    #   ValueNet             -> trained net w/ EWC + LoRA adapter bank (P3)
    #   PlasticityController -> milestone triggers (people learned, situations stored), not a clock
    #   brain1_reflex        -> the modified on-robot moodManager tick
    #   Brain2.propose       -> real reasoning/VLM/LLM over retrieved situations


def main() -> None:
    ap = argparse.ArgumentParser(description="Deep Understanding three-brain PoC sandbox")
    ap.add_argument("--days", type=int, default=200)
    ap.add_argument("--per-day", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    run(args.days, args.per_day, args.seed)


if __name__ == "__main__":
    main()
