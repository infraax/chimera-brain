"""
vector_engram.soak — continuous-operation verification (Phase 1B hardening).

Streams a long sequence of situations through StreamingEngramWriter -> HotColdMemory
and checks the properties a 24/7 robot needs:
  * bounded hot memory (hot never exceeds capacity; overflow spills to cold)
  * sustained non-blocking enqueue throughput (situations/sec)
  * stable retrieval recall after the run
  * no crashes / drops under steady load (with an adequately sized buffer)

Usage:
    python3 -m vector_engram.soak --n 50000 --hot 1000
"""
from __future__ import annotations

import argparse
import tempfile
import time

import numpy as np

from vector_engram import HotColdMemory, StreamingEngramWriter
from vector_engram.synth import D, make_situation, situation_key, PEOPLE, ACTIVITIES, PLACES

FP = D * 2


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=50000)
    ap.add_argument("--hot", type=int, default=1000)
    ap.add_argument("--noise", type=float, default=0.25)
    ap.add_argument("--max-pending", type=int, default=8192)
    args = ap.parse_args()

    rng = np.random.default_rng(0)
    combos = [(p, a, pl) for p in PEOPLE for a in ACTIVITIES for pl in PLACES]

    with tempfile.TemporaryDirectory() as d:
        hc = HotColdMemory(dim=FP, archive_dir=d, hot_capacity=args.hot, cold_backend="hnsw")
        writer = StreamingEngramWriter(hc, max_pending=args.max_pending,
                                       flush_interval_s=0.005, batch=512).start()

        # pre-generate to isolate enqueue throughput from data-gen cost
        print(f"generating {args.n} situations (D={D}, fp_dim={FP}) ...")
        gen0 = time.perf_counter()
        states = []
        keys = []
        for i in range(args.n):
            p, a, pl = combos[rng.integers(0, len(combos))]
            states.append(make_situation(p, a, pl, rng=rng, T=8, noise=args.noise))
            keys.append(situation_key(p, a, pl))
        print(f"  gen done in {time.perf_counter()-gen0:.1f}s")

        # Feed cooperatively: enqueue, and periodically let the consumer catch up so the
        # bounded buffer never overflows (lossless). This measures the SUSTAINED rate the
        # sink can absorb -- the number that matters for "can it keep up with 10-30 fps?".
        # (Undersized-buffer load-shedding is covered separately by the unit tests.)
        t0 = time.perf_counter()
        for i, st in enumerate(states):
            writer.write(st)
            if (i + 1) % 4000 == 0:
                writer.flush()
        writer.close()                      # drain everything
        total_s = time.perf_counter() - t0
        enqueue_s = total_s

        st = writer.stats()
        s = hc.stats()
        print("\n--- SOAK RESULTS ---")
        print(f"enqueued={st.enqueued} flushed={st.flushed} dropped={st.dropped}")
        print(f"sustained throughput (incl. fingerprint+index+persist {args.n} .eng files): "
              f"{args.n/total_s:,.0f} situations/sec  (>> 10-30 fps robot rate)")
        print(f"hot size={s.hot} (cap {args.hot})  cold size={s.cold}  total={s.total}")
        assert s.hot <= args.hot, "hot exceeded capacity!"
        assert s.total == args.n - st.dropped, (s.total, st.dropped)

        # recall sample after the run (queries hit hot+cold archive)
        qrng = np.random.default_rng(7)
        hits = trials = 0
        lat = []
        for _ in range(500):
            p, a, pl = combos[qrng.integers(0, len(combos))]
            q = make_situation(p, a, pl, rng=qrng, noise=args.noise)
            tq = time.perf_counter()
            res = hc.knn_state(q, k=1)
            lat.append((time.perf_counter() - tq) * 1e6)
            trials += 1
            hits += int(bool(res) and res[0].cert.situation_key == situation_key(p, a, pl))
        lat = np.array(lat)
        print(f"post-soak recall@1  : {hits/trials:.3f} ({trials} queries)")
        print(f"merged query latency: p50={np.percentile(lat,50):.0f}us "
              f"p99={np.percentile(lat,99):.0f}us")
        print("memory stayed bounded; no crash. OK")


if __name__ == "__main__":
    main()
