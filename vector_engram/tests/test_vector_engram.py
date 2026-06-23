"""
End-to-end tests for vector_engram (real pipeline, no mocking of the math).

Runnable two ways:
    pytest vector_engram/tests/test_vector_engram.py
    python3 -m vector_engram.tests.test_vector_engram     # plain runner, exits nonzero on fail

Covers: format round-trip, fingerprint determinism/stability/discrimination,
end-to-end write->index->retrieve recall, archive reload, hnsw-vs-exact agreement.
"""
from __future__ import annotations

import sys
import tempfile

import numpy as np

from vector_engram import SituationMemory, decode, encode, fingerprint
from vector_engram.fingerprint import cosine
from vector_engram.format import SituationCert
from vector_engram.state import RawState
from vector_engram.synth import D, build_corpus, make_situation, situation_key


def test_format_roundtrip_fp16_preserves_cosine():
    rng = np.random.default_rng(1)
    vec = rng.normal(0, 1, size=230).astype(np.float32)
    cert = SituationCert(vec=vec, person="dexter", activity="pet", place="desk",
                         emotion=np.array([0.6, 0.2, 0.7, 0.5], np.float32))
    back = decode(encode(cert))
    assert back.person == "dexter" and back.activity == "pet" and back.place == "desk"
    assert back.vec.shape == vec.shape
    # fp16 storage must preserve direction (cosine ~ 1)
    assert cosine(vec, back.vec) > 0.999, cosine(vec, back.vec)
    assert np.allclose(back.emotion, [0.6, 0.2, 0.7, 0.5], atol=1e-3)


def test_fingerprint_determinism_and_dim():
    rng = np.random.default_rng(2)
    frames = rng.normal(0, 1, size=(8, D))
    a = fingerprint(frames, (0, 1))
    b = fingerprint(frames, (0, 1))
    assert a.shape == (D * 2,)
    assert np.array_equal(a, b)  # deterministic


def test_fingerprint_stable_under_noise_and_discriminates():
    rng = np.random.default_rng(3)
    s1 = make_situation("dexter", "pet", "desk", rng=rng, noise=0.25)
    s1b = make_situation("dexter", "pet", "desk", rng=rng, noise=0.25)   # same situation, new noise
    s2 = make_situation("stranger", "poke", "kitchen", rng=rng, noise=0.25)
    f1, f1b, f2 = (fingerprint(s.frames()) for s in (s1, s1b, s2))
    same = cosine(f1, f1b)
    diff = cosine(f1, f2)
    assert same > diff, (same, diff)
    assert same > 0.8, same           # robust to sensor noise
    assert diff < same - 0.1, (same, diff)


def _recall_at_1(backend: str) -> float:
    states, keys = build_corpus(n_prototypes=40, copies=10, seed=10, noise=0.25)
    mem = SituationMemory(dim=D * 2, backend=backend)
    for st in states:
        mem.write_state(st, persist=False)
    # query with fresh noisy variants of each prototype
    rng = np.random.default_rng(999)
    hits = 0
    trials = 0
    seen = set()
    for k in keys:
        if k in seen:
            continue
        seen.add(k)
        p, a, pl = k.split("|")
        q = make_situation(p, a, pl, rng=rng, noise=0.25)
        res = mem.knn_state(q, k=1)
        trials += 1
        if res and res[0].cert.situation_key == k:
            hits += 1
    return hits / trials


def test_end_to_end_recall_exact():
    r = _recall_at_1("exact")
    assert r >= 0.90, f"exact recall@1 too low: {r}"


def test_end_to_end_recall_hnsw():
    r = _recall_at_1("hnsw")
    assert r >= 0.85, f"hnsw recall@1 too low: {r}"


def test_archive_write_reload_roundtrip():
    states, keys = build_corpus(n_prototypes=8, copies=4, seed=5, noise=0.2)
    with tempfile.TemporaryDirectory() as d:
        mem = SituationMemory(dim=D * 2, archive_dir=d, backend="exact")
        for st in states:
            mem.write_state(st, persist=True)
        n_before = len(mem)
        mem2 = SituationMemory.load(d, backend="exact")
        assert len(mem2) == n_before
        # a query returns a cert with valid metadata after reload
        rng = np.random.default_rng(7)
        p, a, pl = keys[0].split("|")
        q = make_situation(p, a, pl, rng=rng, noise=0.2)
        res = mem2.knn_state(q, k=1)
        assert res and res[0].cert.situation_key == keys[0]


def test_raw_state_path_decoupled_from_llama():
    # the decoupling: arbitrary [T,D] state fingerprints with the same pipeline
    rng = np.random.default_rng(4)
    st = RawState(rng.normal(0, 1, size=(6, 50)))
    fp = fingerprint(st.frames())
    assert fp.shape == (100,)


# --------------------------------------------------------------------------- #
def _run() -> int:
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    fails = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
        except Exception as e:  # noqa: BLE001
            fails += 1
            print(f"FAIL  {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(fns) - fails}/{len(fns)} passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(_run())
