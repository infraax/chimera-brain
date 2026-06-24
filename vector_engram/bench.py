"""
vector_engram.bench — larger-corpus verification.

Measures, on a real corpus, for each backend:
  * build time
  * query latency p50 / p99 (per single-situation query)
  * recall@1 and recall@5 (does the nearest stored situation share the query's key?)

Usage:
    python3 -m vector_engram.bench                 # default sweep
    python3 -m vector_engram.bench --n 30000 --prototypes 300 --backend hnsw
    python3 -m vector_engram.bench --backend both
"""
from __future__ import annotations

import argparse
import time

import numpy as np

from vector_engram import SituationMemory
from vector_engram.synth import D, build_corpus, make_situation


def _bench_once(n_prototypes: int, copies: int, backend: str, noise: float, queries: int):
    states, keys = build_corpus(n_prototypes=n_prototypes, copies=copies, seed=0, noise=noise)
    n = len(states)
    mem = SituationMemory(dim=D * 2, backend=backend)

    t0 = time.perf_counter()
    for st in states:
        mem.write_state(st, persist=False)
    build_s = time.perf_counter() - t0

    # queries: fresh noisy variants of random prototypes
    rng = np.random.default_rng(12345)
    uniq = list(dict.fromkeys(keys))
    qkeys = [uniq[rng.integers(0, len(uniq))] for _ in range(queries)]
    qstates = []
    for k in qkeys:
        p, a, pl = k.split("|")
        qstates.append((k, make_situation(p, a, pl, rng=rng, noise=noise)))

    lat = []
    hit1 = hit5 = 0
    for k, q in qstates:
        t = time.perf_counter()
        res = mem.knn_state(q, k=5)
        lat.append((time.perf_counter() - t) * 1e6)  # microseconds
        rkeys = [r.cert.situation_key for r in res]
        if rkeys[:1] == [k]:
            hit1 += 1
        if k in rkeys:
            hit5 += 1

    lat = np.array(lat)
    return {
        "backend": mem.index.backend, "N": n, "dim": D * 2,
        "build_s": build_s, "build_per_item_ms": build_s / n * 1e3,
        "q_p50_us": float(np.percentile(lat, 50)), "q_p99_us": float(np.percentile(lat, 99)),
        "recall@1": hit1 / queries, "recall@5": hit5 / queries, "queries": queries,
    }


def _print(r: dict) -> None:
    print(f"[{r['backend']:5}] N={r['N']:>7} dim={r['dim']} | "
          f"build={r['build_s']:.2f}s ({r['build_per_item_ms']:.3f} ms/item) | "
          f"query p50={r['q_p50_us']:.1f}us p99={r['q_p99_us']:.1f}us | "
          f"R@1={r['recall@1']:.3f} R@5={r['recall@5']:.3f} (q={r['queries']})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0, help="total corpus size (overrides prototypes*copies)")
    ap.add_argument("--prototypes", type=int, default=100)
    ap.add_argument("--copies", type=int, default=50)
    ap.add_argument("--noise", type=float, default=0.25)
    ap.add_argument("--queries", type=int, default=500)
    ap.add_argument("--backend", choices=["hnsw", "exact", "both"], default="both")
    args = ap.parse_args()

    prototypes, copies = args.prototypes, args.copies
    if args.n:
        copies = max(1, args.n // prototypes)

    backends = ["exact", "hnsw"] if args.backend == "both" else [args.backend]
    print(f"corpus: {prototypes} prototypes x {copies} copies = {prototypes*copies} situations, "
          f"noise={args.noise}, D={D}, fp_dim={D*2}")
    for b in backends:
        _print(_bench_once(prototypes, copies, b, args.noise, args.queries))


if __name__ == "__main__":
    main()
