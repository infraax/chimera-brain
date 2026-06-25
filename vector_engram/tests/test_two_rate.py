"""
Phase 1 — the two senses (two-rate hybrid) — end-to-end tests.

Verifies, with the real pipeline (no mocked math):
  • the MEANING sense forms a fingerprint and retrieves situation identity through noise
  • the REFLEX sense still works unchanged (regression)
  • EGRV v2 round-trips sense + repr_id, and still decodes legacy v1 certs
  • TwofoldMemory keeps the two registers separate and recalls each correctly
  • graceful degradation: a reflex-only creature (no meaning_dim) still feels & recalls
"""
import numpy as np
import pytest

from vector_engram import SituationCert, decode, encode
from vector_engram.sense import (MEANING_REPR, REFLEX_REPR, EmbeddingFrame,
                                 MeaningState, Sense, meaning_impression,
                                 reflex_impression)
from vector_engram.store import TwofoldMemory
from vector_engram.synth import DE, build_corpus, make_meaning, make_situation


def _meaning_corpus(n_proto=6, copies=4, seed=0):
    """n_proto distinct situations x copies, in the MEANING (embedding) sense."""
    from vector_engram.synth import ACTIVITIES, PEOPLE, PLACES
    rng = np.random.default_rng(seed)
    combos = [(p, a, pl) for p in PEOPLE for a in ACTIVITIES for pl in PLACES]
    rng.shuffle(combos)
    combos = combos[:n_proto]
    states, keys = [], []
    for (p, a, pl) in combos:
        for _ in range(copies):
            states.append(make_meaning(p, a, pl, rng=rng))
            keys.append(f"{p}|{a}|{pl}")
    return states, keys


def test_meaning_impression_shape_and_determinism():
    rng = np.random.default_rng(1)
    st = make_meaning("dexter", "talk", "desk", rng=rng)
    fp = meaning_impression(st)
    assert fp.shape == (DE * 2,)            # D_embed * n_freqs
    assert fp.dtype == np.float32
    # deterministic: same frames -> same fingerprint
    assert np.allclose(meaning_impression(st), fp)


def test_egrv_v2_roundtrip_sense_and_repr():
    vec = np.random.default_rng(0).normal(size=96).astype(np.float32)
    cert = SituationCert(vec=vec, person="dexter", activity="talk",
                         sense=int(Sense.MEANING), repr_id=MEANING_REPR)
    back = decode(encode(cert))
    assert back.sense == int(Sense.MEANING)
    assert back.repr_id == MEANING_REPR
    assert back.person == "dexter"
    assert np.allclose(back.vec, vec.astype(np.float16).astype(np.float32))


def test_egrv_v2_decodes_legacy_v1():
    # hand-build a legacy v1 cert (no sense/repr_id) and confirm decode tolerates it.
    import struct
    from vector_engram.format import MAGIC
    vec = np.zeros(8, np.float16)
    buf = bytearray()
    buf += MAGIC
    buf += struct.pack("<B", 1)            # version 1
    buf += struct.pack("<H", 8)            # dim
    buf += struct.pack("<B", 2)            # n_freqs
    buf += struct.pack("<d", 123.0)        # timestamp
    buf += struct.pack("<4f", 0, 0, 0, 0)  # emotion
    for s in ("vector-0", "src", "p", "a", "pl", "k"):
        b = s.encode(); buf += struct.pack("<H", len(b)) + b
    buf += vec.tobytes()
    back = decode(bytes(buf))
    assert back.sense == int(Sense.REFLEX)        # legacy -> reflex
    assert back.repr_id == "rfft.raw.v1"
    assert back.person == "p"


def test_meaning_register_recall_through_noise():
    states, keys = _meaning_corpus()
    # reflex register left empty here; this test exercises the meaning register only.
    mem = TwofoldMemory(reflex_dim=230, meaning_dim=DE * 2, backend="exact")
    for st in states:
        mem.recognize(st)
    # query with a fresh noisy copy of a known situation
    p, a, pl = keys[0].split("|")
    q = make_meaning(p, a, pl, rng=np.random.default_rng(999))
    res = mem.recall_meaning(q, k=1)
    assert res and res[0].cert.situation_key == keys[0]
    assert res[0].cert.sense == int(Sense.MEANING)
    assert res[0].cert.repr_id == MEANING_REPR


def test_twofold_keeps_registers_separate():
    # one creature, both registers; a moment laid down in both, recalled in each.
    rng = np.random.default_rng(3)
    raw_states, raw_keys = build_corpus(5, 3, seed=3)
    mean_states, mean_keys = _meaning_corpus(5, 3, seed=3)

    raw_dim = raw_states[0].frames().shape[1] * 2
    mem = TwofoldMemory(reflex_dim=raw_dim, meaning_dim=DE * 2, backend="exact")

    for st in raw_states:
        mem.feel(st)
    for st in mean_states:
        mem.recognize(st)

    assert len(mem.reflex) == len(raw_states)
    assert len(mem.meaning) == len(mean_states)
    assert len(mem) == len(raw_states) + len(mean_states)

    # reflex recall returns reflex-sense certs only
    rq = make_situation(*raw_keys[0].split("|"), rng=rng)
    rres = mem.recall_reflex(rq, k=1)
    assert rres[0].cert.sense == int(Sense.REFLEX)

    # meaning recall returns meaning-sense certs only
    mq = make_meaning(*mean_keys[0].split("|"), rng=rng)
    mres = mem.recall_meaning(mq, k=1)
    assert mres[0].cert.sense == int(Sense.MEANING)


def test_reflex_only_creature_degrades_gracefully():
    # no meaning_dim -> brainstem only; feel/recall still work, recognize raises.
    raw_states, raw_keys = build_corpus(4, 3, seed=7)
    raw_dim = raw_states[0].frames().shape[1] * 2
    mem = TwofoldMemory(reflex_dim=raw_dim, backend="exact")  # no cortex
    assert mem.meaning is None
    for st in raw_states:
        mem.feel(st)
    q = make_situation(*raw_keys[0].split("|"), rng=np.random.default_rng(7))
    assert mem.recall_reflex(q, k=1)[0].cert.situation_key == raw_keys[0]
    with pytest.raises(RuntimeError):
        mem.recognize(make_meaning("dexter", "talk", "desk", rng=np.random.default_rng(0)))
