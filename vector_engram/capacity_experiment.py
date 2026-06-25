"""
vector_engram.capacity_experiment — THE gate (Phase 4).

Answers the load-bearing question before we build COMPOSE (identity bundles / the
"self-frequency"): *how many memory-impressions can be woven under a label and still be
individually recovered, given that ENGRAM fingerprints are CORRELATED, not random?*
(`frequency_memory__UNIFIED.md`, Experiment #2 — the gate that also unblocks clean
resonant completion from Phase 3.)

Two parts, both run by `main()`:
  1. inspect_fingerprints()  — what the fingerprints actually look like (stats, block
     structure, and the within- vs across-situation cosine gap = discriminability).
  2. run_capacity()          — HRR bundle/unbind/cleanup capacity across conditions:
       random@D · raw-amplitude@D · gdf@2D · projected→Dhi · random@Dhi
     to separate three effects: dimensionality, representation (GDF), and projection.

Runnable:  python -m vector_engram.capacity_experiment
"""
from __future__ import annotations

import numpy as np

from .fingerprint import cosine, fingerprint, fingerprint_gdf
from .synth import build_corpus, situation_key
from .vsa import (RandomProjection, bind, bundle, cleanup, pairwise_cosine_stats,
                  random_vectors, unbind)


# ---- part 1: what do the fingerprints look like? --------------------------- #
def _corpus_fingerprints(n_proto: int, copies: int, *, gdf: bool, seed: int):
    states, keys = build_corpus(n_proto, copies, seed=seed)
    fn = fingerprint_gdf if gdf else fingerprint
    fps = np.stack([fn(s.frames()) for s in states])
    return fps, keys


def _within_across_gap(fps: np.ndarray, keys: list[str]) -> tuple[float, float]:
    """mean cosine for same-situation pairs vs different-situation pairs."""
    within, across = [], []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            c = cosine(fps[i], fps[j])
            (within if keys[i] == keys[j] else across).append(c)
    return (float(np.mean(within)) if within else float("nan"),
            float(np.mean(across)) if across else float("nan"))


def inspect_fingerprints() -> None:
    print("=" * 70)
    print("PART 1 — WHAT THE FINGERPRINTS LOOK LIKE")
    print("=" * 70)
    for label, gdf in (("amplitude (rfft.raw.v1)", False), ("amplitude+gdf (rfft+gdf.v1)", True)):
        fps, keys = _corpus_fingerprints(8, 6, gdf=gdf, seed=0)
        v = fps[0]
        n_freqs = 2
        block = v.shape[0] // (4 if gdf else 2)   # = D (feature dim)
        norms = [float(np.linalg.norm(v[b * block:(b + 1) * block]))
                 for b in range((4 if gdf else 2))]
        within, across = _within_across_gap(fps, keys)
        print(f"\n• {label}")
        print(f"    dim={v.shape[0]}  dtype={fps.dtype}  full-norm={np.linalg.norm(v):.3f}")
        print(f"    value range [{v.min():+.3f}, {v.max():+.3f}]  mean={v.mean():+.4f}  "
              f"sparsity(|x|<1e-3)={float(np.mean(np.abs(v) < 1e-3)):.2%}")
        print(f"    per-block L2 norms (each ~1 by construction): "
              f"{', '.join(f'{x:.3f}' for x in norms)}")
        print(f"    first 6 of amp-f0 block: {np.round(v[:6], 3).tolist()}")
        print(f"    DISCRIMINABILITY  within-situation cos={within:.3f}  "
              f"across-situation cos={across:.3f}  gap={within - across:+.3f}")
    print("\n  (bigger within-minus-across gap = situations separate better = easier"
          " cleanup\n   and higher VSA capacity.)")


# ---- part 2: bundling capacity --------------------------------------------- #
def capacity_curve(items: np.ndarray, ks: list[int], *, n_trials: int, rng: np.random.Generator
                   ) -> dict[int, float]:
    """For each bundle size k: bind k distinct items to k random roles, bundle, then
    unbind+cleanup each. Returns k -> mean recovery accuracy (cleanup over the FULL
    item-memory, the realistic case)."""
    N, D = items.shape
    out: dict[int, float] = {}
    for k in ks:
        if k > N:
            continue
        acc = 0.0
        for _ in range(n_trials):
            idx = rng.choice(N, size=k, replace=False)
            roles = random_vectors(k, D, rng=rng)
            bun = bundle([bind(roles[j], items[idx[j]]) for j in range(k)])
            correct = sum(cleanup(unbind(bun, roles[j]), items) == idx[j] for j in range(k))
            acc += correct / k
        out[k] = acc / n_trials
    return out


def capacity_at(curve: dict[int, float], thresh: float = 0.9) -> int:
    cap = 0
    for k in sorted(curve):
        if curve[k] >= thresh:
            cap = k
        else:
            break
    return cap


def run_capacity() -> None:
    print("\n" + "=" * 70)
    print("PART 2 — BUNDLING CAPACITY (HRR bind/bundle/unbind+cleanup)")
    print("=" * 70)
    N, Dhi = 64, 2048
    ks = [2, 4, 8, 16, 32, 48]
    rng = np.random.default_rng(7)

    raw_fps, _ = _corpus_fingerprints(N, 1, gdf=False, seed=1)   # [N, 230] correlated
    gdf_fps, _ = _corpus_fingerprints(N, 1, gdf=True, seed=1)    # [N, 460] correlated
    D = raw_fps.shape[1]
    proj = RandomProjection(D, Dhi, seed=3)
    proj_fps = np.stack([proj.project(v) for v in raw_fps])      # [N, 2048]

    conditions = {
        f"random @ D={D}":      random_vectors(N, D, rng=np.random.default_rng(11)),
        f"raw-amplitude @ {D}": raw_fps,
        f"gdf @ {gdf_fps.shape[1]}": gdf_fps,
        f"projected raw @ {Dhi}": proj_fps,
        f"random @ {Dhi}":      random_vectors(N, Dhi, rng=np.random.default_rng(12)),
    }

    print(f"\n{'condition':<24}{'corr(mean|cos|)':>16}{'capacity@0.9':>14}   accuracy by k")
    print("-" * 70)
    for name, items in conditions.items():
        corr = pairwise_cosine_stats(items)["mean_abs"]
        curve = capacity_curve(items, ks, n_trials=15, rng=rng)
        cap = capacity_at(curve)
        accs = " ".join(f"k{k}:{curve.get(k, float('nan')):.2f}" for k in ks)
        print(f"{name:<24}{corr:>16.3f}{cap:>14}   {accs}")

    print("\nReading it:")
    print("  • random@D vs random@Dhi  → the pure dimensionality effect (the ceiling).")
    print("  • raw vs gdf              → does the Phase-2 representation separate items"
          " better (easier cleanup)?")
    print("  • projected vs raw        → does lifting dim help, given JL preserves cosines"
          " (i.e. keeps correlation)?")


def main() -> None:
    inspect_fingerprints()
    run_capacity()


if __name__ == "__main__":
    main()
