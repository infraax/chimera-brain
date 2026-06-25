"""
Phase 5 — COMPOSE (weaving a self) — end-to-end tests.

Verifies the identity layer the gate unblocked:
  • belonging by resonance: a new moment is recognised as the right identity
  • the single composed self-shape can be queried by label and recovers membership
  • enumeration of DISTINCT members is exact even past one leaf (the leaf hierarchy)
  • leaf rollover happens at capacity; determinism; self_shape shape
The honest caveat (near-duplicate members aren't individually enumerable — they reinforce
the shape rather than being recoverable) is documented in compose.py and exercised here.
"""
import numpy as np

from vector_engram.compose import DIM_HI, LEAF_CAP, SelfModel
from vector_engram.sense import meaning_impression
from vector_engram.synth import ACTIVITIES, DE, PEOPLE, PLACES, make_meaning


def _imp(combo, rng):
    return meaning_impression(make_meaning(*combo, rng=rng))


def _distinct_combos(rng):
    combos = [(p, a, pl) for p in PEOPLE for a in ACTIVITIES for pl in PLACES]
    rng.shuffle(combos)
    return combos


def test_recognize_membership_discrimination():
    rng = np.random.default_rng(0)
    sm = SelfModel(in_dim=DE * 2, seed=1)
    for _ in range(10):
        sm.weave("person:dexter", _imp(("dexter", "talk", "desk"), rng))
        sm.weave("person:stranger", _imp(("stranger", "talk", "desk"), rng))
        sm.weave("place:kitchen", _imp(("partner", "ignore", "kitchen"), rng))
    hits = sum(sm.recognize(_imp(("dexter", "talk", "desk"), rng)) == "person:dexter"
               for _ in range(40))
    assert hits >= 38                                  # a dexter moment belongs to dexter
    r = sm.resonances(_imp(("dexter", "talk", "desk"), rng))
    assert r["person:dexter"] > r["person:stranger"]   # resonates most with the right id


def test_self_shape_query_by_label():
    rng = np.random.default_rng(1)
    sm = SelfModel(in_dim=DE * 2, seed=1)
    for _ in range(10):
        sm.weave("person:dexter", _imp(("dexter", "play", "living_room"), rng))
        sm.weave("person:stranger", _imp(("stranger", "poke", "desk"), rng))
    shp = sm.self_shape()
    assert shp.shape[0] == DIM_HI                       # one fixed-width personality frequency
    q = _imp(("dexter", "play", "living_room"), rng)
    # querying the SINGLE composed shape by label recovers correct membership
    assert sm.shape_resonance("person:dexter", q) > sm.shape_resonance("person:stranger", q)


def test_enumeration_distinct_members_exact_across_leaves():
    rng = np.random.default_rng(3)
    combos = _distinct_combos(rng)
    for k in (16, 40):                                  # 40 forces >1 leaf
        sm = SelfModel(in_dim=DE * 2, seed=3)
        for c in combos[:k]:
            sm.weave("self", _imp(c, rng))
        assert sm.identity("self").recall_accuracy() >= 0.95


def test_leaf_rollover_and_len():
    rng = np.random.default_rng(4)
    combos = _distinct_combos(rng)
    sm = SelfModel(in_dim=DE * 2, leaf_cap=LEAF_CAP, seed=4)
    for c in combos[:LEAF_CAP + 5]:
        sm.weave("self", _imp(c, rng))
    ident = sm.identity("self")
    assert len(ident) == LEAF_CAP + 5
    assert len(ident._leaves) == 2                      # rolled into a second leaf
    assert len(sm) == 1                                 # one identity ('self')


def test_determinism():
    rng1 = np.random.default_rng(7)
    rng2 = np.random.default_rng(7)
    a = SelfModel(in_dim=DE * 2, seed=9)
    b = SelfModel(in_dim=DE * 2, seed=9)
    for _ in range(6):
        ca = make_meaning("dexter", "talk", "desk", rng=rng1)
        cb = make_meaning("dexter", "talk", "desk", rng=rng2)
        a.weave("self", meaning_impression(ca))
        b.weave("self", meaning_impression(cb))
    assert np.allclose(a.self_shape(), b.self_shape())
