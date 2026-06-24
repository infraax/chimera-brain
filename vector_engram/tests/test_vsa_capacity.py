"""
Phase 4 — VSA substrate + the capacity gate — tests.

Asserts the primitives are correct and the gate findings hold:
  • HRR bind→unbind roundtrip recovers the filler
  • bundle→unbind→cleanup recovers a small bundle exactly
  • random high-dim vectors are near-orthogonal; repeated/correlated ones are not
  • RandomProjection ~preserves cosines (Johnson–Lindenstrauss) — it does NOT decorrelate
  • the headline ordering: capacity(random@D) > capacity(raw@D), and projection to higher
    D restores capacity above raw  (the verdict that unblocks COMPOSE)
"""
import numpy as np

from vector_engram.capacity_experiment import (_corpus_fingerprints, capacity_at,
                                               capacity_curve)
from vector_engram.fingerprint import cosine
from vector_engram.vsa import (RandomProjection, bind, bundle, cleanup,
                               pairwise_cosine_stats, random_vectors, unbind)


def test_hrr_bind_unbind_roundtrip():
    rng = np.random.default_rng(0)
    V = random_vectors(2, 512, rng=rng)
    role, item = V[0], V[1]
    rec = unbind(bind(role, item), role)
    assert cosine(rec, item) > 0.5            # filler recovered (noisy but clear)
    assert bind(role, item).shape == item.shape


def test_bundle_cleanup_small_bundle():
    rng = np.random.default_rng(1)
    items = random_vectors(20, 512, rng=rng)
    roles = random_vectors(5, 512, rng=rng)
    bun = bundle([bind(roles[j], items[j]) for j in range(5)])
    rec = [cleanup(unbind(bun, roles[j]), items) for j in range(5)]
    assert rec == [0, 1, 2, 3, 4]             # all five recovered exactly


def test_random_orthogonality_vs_correlation():
    rng = np.random.default_rng(2)
    rand = random_vectors(64, 512, rng=rng)
    assert pairwise_cosine_stats(rand)["mean_abs"] < 0.10   # near-orthogonal
    # a correlated set: a base + small perturbations
    base = rng.normal(size=512)
    corr = np.stack([base + 0.15 * rng.normal(size=512) for _ in range(64)])
    assert pairwise_cosine_stats(corr)["mean_abs"] > 0.5    # very correlated


def test_random_projection_preserves_cosine_jl():
    rng = np.random.default_rng(3)
    a = rng.normal(size=230); b = rng.normal(size=230)
    proj = RandomProjection(230, 4096, seed=5)
    before = cosine(a, b)
    after = cosine(proj.project(a), proj.project(b))
    assert abs(before - after) < 0.1          # JL: cosine ~preserved (NOT decorrelated)


def test_capacity_gate_ordering():
    # the headline: correlation halves capacity; projection to higher D restores it.
    N = 32
    ks = [2, 4, 8, 16]
    raw, _ = _corpus_fingerprints(N, 1, gdf=False, seed=1)   # correlated real fingerprints
    D = raw.shape[1]
    rnd = random_vectors(N, D, rng=np.random.default_rng(9))
    proj = RandomProjection(D, 2048, seed=3)
    prj = np.stack([proj.project(v) for v in raw])

    cap_rand = capacity_at(capacity_curve(rnd, ks, n_trials=8, rng=np.random.default_rng(0)))
    cap_raw = capacity_at(capacity_curve(raw, ks, n_trials=8, rng=np.random.default_rng(0)))
    cap_proj = capacity_at(capacity_curve(prj, ks, n_trials=8, rng=np.random.default_rng(0)))

    assert cap_rand >= cap_raw                 # random (orthogonal) >= correlated
    assert cap_proj >= cap_raw                 # projection to higher D restores capacity
    # and projection keeps the correlation (JL) — it's the dim that buys capacity
    assert pairwise_cosine_stats(prj)["mean_abs"] > 0.3
