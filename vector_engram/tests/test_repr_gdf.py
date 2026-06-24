"""
Phase 2 — the GDF (group-delay) phase complement — end-to-end tests.

The point of GDF: amplitude alone is blind to *when* within a window a change happened
(a window and its time-reverse share an identical amplitude spectrum). GDF restores
temporal-order sensitivity for ~free. We verify:
  • shape + determinism of the gdf fingerprint
  • the killer property: amplitude can't tell a window from its time-reverse (cos≈1),
    gdf can (cos clearly < 1)
  • TwofoldMemory(representation="gdf") wires the right faculties, dims, and repr_ids,
    and still recalls situation identity through noise end-to-end
  • fingerprint_dim() agrees with the real fingerprint length
"""
import numpy as np

from vector_engram import TwofoldMemory, fingerprint, fingerprint_dim
from vector_engram.fingerprint import cosine, fingerprint_gdf
from vector_engram.sense import (MEANING_GDF_REPR, REFLEX_GDF_REPR, Sense,
                                 impression_for)
from vector_engram.synth import DE, build_corpus, make_meaning, make_situation


def test_gdf_shape_and_determinism():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(8, 40))
    fp = fingerprint_gdf(x)
    assert fp.shape == (40 * 2 * 2,)          # D * n_freqs * 2 (amp + gd)
    assert fp.dtype == np.float32
    assert np.allclose(fingerprint_gdf(x), fp)
    # leading half is byte-identical to the amplitude-only fingerprint (migration aid)
    assert np.allclose(fp[: 40 * 2], fingerprint(x))


def test_gdf_distinguishes_time_reversal_amplitude_cannot():
    rng = np.random.default_rng(1)
    base = rng.normal(0, 1, 40); trend = rng.normal(0, 0.4, 40)
    x = np.stack([base + trend * t + rng.normal(0, 0.05, 40) for t in range(8)])
    xr = x[::-1].copy()                        # same amplitude spectrum, reversed phase
    amp_cos = cosine(fingerprint(x), fingerprint(xr))
    gdf_cos = cosine(fingerprint_gdf(x), fingerprint_gdf(xr))
    assert amp_cos > 0.999                     # amplitude is blind to order
    assert gdf_cos < 0.6                       # gdf clearly separates them
    assert gdf_cos < amp_cos - 0.3             # strictly more discriminative


def test_impression_for_and_fingerprint_dim():
    rfn, rrepr = impression_for(Sense.REFLEX, "gdf")
    mfn, mrepr = impression_for(Sense.MEANING, "gdf")
    assert rrepr == REFLEX_GDF_REPR and mrepr == MEANING_GDF_REPR
    # dim helper matches the real fingerprint length
    rng = np.random.default_rng(2)
    st = make_meaning("dexter", "talk", "desk", rng=rng)
    assert mfn(st).shape[0] == fingerprint_dim(DE, representation="gdf")
    assert fingerprint_dim(DE, representation="gdf") == DE * 2 * 2
    assert fingerprint_dim(DE, representation="raw") == DE * 2


def test_twofold_gdf_recall_end_to_end():
    raw_states, raw_keys = build_corpus(6, 4, seed=5)
    mean_states, mean_keys = ([], [])
    from vector_engram.synth import ACTIVITIES, PEOPLE, PLACES
    rng = np.random.default_rng(5)
    combos = [(p, a, pl) for p in PEOPLE for a in ACTIVITIES for pl in PLACES]
    rng.shuffle(combos)
    for (p, a, pl) in combos[:6]:
        for _ in range(4):
            mean_states.append(make_meaning(p, a, pl, rng=rng)); mean_keys.append(f"{p}|{a}|{pl}")

    feat_raw = raw_states[0].frames().shape[1]
    mem = TwofoldMemory(
        reflex_dim=fingerprint_dim(feat_raw, representation="gdf"),
        meaning_dim=fingerprint_dim(DE, representation="gdf"),
        representation="gdf", backend="exact")
    assert mem.representation == "gdf"
    assert mem.reflex.repr_id == REFLEX_GDF_REPR
    assert mem.meaning.repr_id == MEANING_GDF_REPR

    for st in raw_states:
        mem.feel(st)
    for st in mean_states:
        mem.recognize(st)

    rq = make_situation(*raw_keys[0].split("|"), rng=rng)
    rres = mem.recall_reflex(rq, k=1)[0]
    assert rres.cert.situation_key == raw_keys[0]
    assert rres.cert.repr_id == REFLEX_GDF_REPR

    mq = make_meaning(*mean_keys[0].split("|"), rng=rng)
    mres = mem.recall_meaning(mq, k=1)[0]
    assert mres.cert.situation_key == mean_keys[0]
    assert mres.cert.repr_id == MEANING_GDF_REPR
    assert mres.cert.sense == int(Sense.MEANING)
