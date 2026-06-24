"""
Phase 3 — recall by resonance (Modern Hopfield head) — end-to-end tests.

Asserts the rock-solid properties (the implementation is correct and generalizes kNN):
  • shape + determinism of resonate()
  • β→∞ collapses to a one-hot at the most-similar pattern (== argmax == kNN)
  • sharp resonance top-1 == cosine-kNN top-1 on a clean corpus (the proven special case)
  • steps=1 resonant recall does no harm and works end-to-end via TwofoldMemory(beta=…)
  • pattern completion: in a separable regime, settling pulls a noisy cue toward its
    true attractor (the property that, on correlated fingerprints, is gated — see
    resonance.py LIMITATION + the capacity experiment).
"""
import numpy as np

from vector_engram import TwofoldMemory, Sense
from vector_engram.fingerprint import cosine
from vector_engram.resonance import resonate, softmax
from vector_engram.synth import build_corpus, make_situation


def test_softmax_and_resonate_shape_determinism():
    w = softmax(np.array([1.0, 2.0, 3.0]))
    assert abs(w.sum() - 1.0) < 1e-9 and np.argmax(w) == 2
    rng = np.random.default_rng(0)
    P = rng.normal(size=(10, 32)); cue = rng.normal(size=32)
    c1, w1 = resonate(cue, P, beta=8.0, steps=2)
    c2, w2 = resonate(cue, P, beta=8.0, steps=2)
    assert c1.shape == (32,) and w1.shape == (10,)
    assert np.allclose(c1, c2) and np.allclose(w1, w2)


def test_beta_to_infinity_is_argmax():
    rng = np.random.default_rng(1)
    P = rng.normal(size=(8, 64)); P /= np.linalg.norm(P, axis=1, keepdims=True)
    cue = P[3] + rng.normal(0, 0.1, 64)          # clearly nearest pattern 3
    _c, w = resonate(cue, P, beta=1e6, steps=1)
    assert np.argmax(w) == 3
    assert w[3] > 0.999                           # one-hot in the sharp limit


def test_sharp_resonance_equals_knn_topk():
    states, keys = build_corpus(8, 4, seed=2)
    fd = states[0].frames().shape[1] * 2
    mem = TwofoldMemory(reflex_dim=fd, backend="exact")
    for s in states:
        mem.feel(s)
    rng = np.random.default_rng(3)
    for _ in range(25):
        p, a, pl = keys[rng.integers(len(keys))].split("|")
        q = make_situation(p, a, pl, rng=rng)
        knn_top = mem.recall_reflex(q, 1)[0].label
        sharp_top = mem.recall_reflex(q, 1, beta=1e6, steps=1)[0].label
        assert knn_top == sharp_top              # kNN is the β→∞ special case


def test_resonant_recall_end_to_end_and_no_harm():
    states, keys = build_corpus(6, 4, seed=5)
    fd = states[0].frames().shape[1] * 2
    mem = TwofoldMemory(reflex_dim=fd, backend="exact")
    for s in states:
        mem.feel(s)
    rng = np.random.default_rng(6)
    knn_ok = res_ok = 0
    for _ in range(40):
        p, a, pl = keys[rng.integers(len(keys))].split("|"); key = f"{p}|{a}|{pl}"
        q = make_situation(p, a, pl, rng=rng)
        knn_ok += mem.recall_reflex(q, 1)[0].cert.situation_key == key
        r = mem.recall_reflex(q, 1, beta=10.0, steps=1)[0]   # safe default: 1 step
        res_ok += r.cert.situation_key == key
        assert r.cert.sense == int(Sense.REFLEX)
    assert res_ok == knn_ok                        # steps=1 does no harm (identical ranking)
    assert knn_ok >= 38                            # both recall well on a clean corpus


def test_settling_completes_separable_cue():
    # in a clearly-separable, low-noise regime, settling moves a noisy cue closer to its
    # true attractor (the completion property; gated on correlated raw fingerprints).
    rng = np.random.default_rng(1)
    M, D = 8, 128
    P = rng.normal(size=(M, D)); P /= np.linalg.norm(P, axis=1, keepdims=True)
    wins = 0; N = 200
    for _ in range(N):
        i = rng.integers(M)
        cue = P[i] + rng.normal(0, 0.2, D)
        comp, _ = resonate(cue, P, beta=20.0, steps=3)
        wins += cosine(comp, P[i]) > cosine(cue, P[i])
    assert wins / N >= 0.9
