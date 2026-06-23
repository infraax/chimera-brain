"""
Tests for ENGRAM Phase 1B (streaming + hot/cold + confidence), 1C (perception worker),
and Phase 2 (filters + classifier). Real pipeline, real concurrency, real metrics.

Run:
    python3 -m vector_engram.tests.test_phases_1b_1c_2
    pytest vector_engram/tests/test_phases_1b_1c_2.py -q
"""
from __future__ import annotations

import sys
import tempfile
import time

import numpy as np

from vector_engram import (
    ConfidenceLog, FingerprintWorker, HotColdMemory, HotIndex, MockPerceptionSource,
    SituationClassifier, SituationMemory, StreamingEngramWriter, filter_retrieved,
    recall_summary,
)
from vector_engram.synth import D, build_corpus, make_situation, situation_key

FP = D * 2


# ---- Phase 1B: HotIndex ring buffer ---------------------------------------- #
def test_hotindex_bounded_and_evicts():
    hi = HotIndex(dim=FP, capacity=100)
    evictions = 0
    rng = np.random.default_rng(0)
    for i in range(250):
        ev = hi.add(i, rng.normal(0, 1, size=FP).astype(np.float32))
        if ev is not None:
            evictions += 1
    assert len(hi) == 100, len(hi)            # bounded
    assert evictions == 150, evictions        # everything past capacity evicted
    # oldest (labels 0..149) evicted; newest retained
    res = hi.query(hi._norm[(hi._head - 1) % hi.capacity], k=1)
    assert res and res[0][0] >= 150


# ---- Phase 1B: hot/cold spill + merged retrieval --------------------------- #
def test_hotcold_spill_and_recall():
    states, keys = build_corpus(n_prototypes=30, copies=10, seed=1, noise=0.25)  # 300
    with tempfile.TemporaryDirectory() as d:
        hc = HotColdMemory(dim=FP, archive_dir=d, hot_capacity=100, cold_backend="exact")
        for st in states:
            hc.write_state(st)
        s = hc.stats()
        assert s.hot == 100 and s.cold == 200 and s.total == 300, s
        # recall across hot+cold: query fresh variants, nearest must share key
        rng = np.random.default_rng(99)
        hits = trials = 0
        for k in dict.fromkeys(keys):
            p, a, pl = k.split("|")
            q = make_situation(p, a, pl, rng=rng, noise=0.25)
            res = hc.knn_state(q, k=1)
            trials += 1
            hits += int(bool(res) and res[0].cert.situation_key == k)
        recall = hits / trials
        assert recall >= 0.90, recall


# ---- Phase 1B: streaming writer is non-blocking + lossless when drained ----- #
def test_streaming_writer_drains_all():
    states, _ = build_corpus(n_prototypes=20, copies=10, seed=2, noise=0.25)  # 200
    mem = SituationMemory(dim=FP, backend="exact")
    with StreamingEngramWriter(mem, max_pending=4096, flush_interval_s=0.01, batch=64) as w:
        t0 = time.perf_counter()
        for st in states:
            w.write(st)               # non-blocking
        enqueue_s = time.perf_counter() - t0
        w.flush()
    st = w.stats()
    assert st.enqueued == 200
    assert st.dropped == 0
    assert len(mem) == 200, len(mem)
    # enqueue should be fast (non-blocking); generous bound for CI noise
    assert enqueue_s < 1.0, enqueue_s


def test_streaming_writer_sheds_load_when_full():
    mem = SituationMemory(dim=FP, backend="exact")
    # tiny buffer, no background thread started -> forced overflow drops
    w = StreamingEngramWriter(mem, max_pending=50, batch=10)
    states, _ = build_corpus(n_prototypes=10, copies=20, seed=3, noise=0.25)  # 200
    for st in states:
        w.write(st)
    s = w.stats()
    assert s.enqueued == 200
    assert s.dropped == 150 and s.pending == 50, s   # bounded memory, shed oldest


# ---- Phase 1B: confidence log / prior preemption --------------------------- #
def test_confidence_preemption():
    log = ConfidenceLog(min_trials_to_preempt=5, max_fail_rate=0.5)
    for _ in range(8):
        log.record("dexter|pet|desk", success=False)
    for _ in range(8):
        log.record("dexter|talk|desk", success=True)
    assert log.should_preempt("dexter|pet|desk") is True
    assert log.should_preempt("dexter|talk|desk") is False
    assert log.summary()["preempting"] == 1


def test_confidence_persistence():
    log = ConfidenceLog()
    log.record("a|b|c", True); log.record("a|b|c", False)
    with tempfile.TemporaryDirectory() as d:
        p = f"{d}/indexc.json"
        log.save(p)
        log2 = ConfidenceLog.load(p)
        assert abs(log2.fail_rate("a|b|c") - 0.5) < 1e-9


# ---- Phase 1C: perception worker emits situations -------------------------- #
def test_fingerprint_worker_emits_and_recalls():
    script = [("dexter", "pet", "desk"), ("kid", "play", "living_room"),
              ("stranger", "poke", "kitchen")]
    mem = SituationMemory(dim=FP, backend="exact")
    worker = FingerprintWorker(mem, window=8, stride=4)
    src = MockPerceptionSource(script, seed=5, frames_per_scene=12, noise=0.2)
    n = worker.run(src)
    assert n == 36                      # 3 scenes x 12 frames
    assert worker.emitted >= 3          # at least one situation per scene
    assert len(mem) == worker.emitted
    # recall on a fresh "dexter petting at desk" should surface that situation
    rng = np.random.default_rng(123)
    q = make_situation("dexter", "pet", "desk", rng=rng, noise=0.2)
    res = mem.knn_state(q, k=3)
    summary = recall_summary(res)
    assert "dexter" in summary and res[0].cert.situation_key == "dexter|pet|desk", summary


# ---- Phase 2: metadata filters --------------------------------------------- #
def test_filter_retrieved_by_metadata():
    states, _ = build_corpus(n_prototypes=12, copies=6, seed=4, noise=0.2)
    mem = SituationMemory(dim=FP, backend="exact")
    for st in states:
        mem.write_state(st, persist=False)
    rng = np.random.default_rng(7)
    q = make_situation("dexter", "pet", "desk", rng=rng, noise=0.2)
    res = mem.knn_state(q, k=50)
    only_dexter = filter_retrieved(res, person="dexter")
    assert all(r.cert.person == "dexter" for r in only_dexter)
    assert len(only_dexter) <= len(res)


# ---- Phase 2: situation classifier (training-free k-NN) -------------------- #
def test_situation_classifier_accuracy():
    states, keys = build_corpus(n_prototypes=24, copies=12, seed=8, noise=0.25)
    mem = SituationMemory(dim=FP, backend="exact")
    for st in states:
        mem.write_state(st, persist=False)
    clf = SituationClassifier(mem, k=9)
    rng = np.random.default_rng(2024)
    correct = total = 0
    for k in dict.fromkeys(keys):
        p, a, pl = k.split("|")
        q = make_situation(p, a, pl, rng=rng, noise=0.25)
        pred = clf.predict(q)
        total += 1
        correct += int(pred["person"] == p and pred["activity"] == a and pred["place"] == pl)
    acc = correct / total
    assert acc >= 0.85, acc


def _run() -> int:
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    fails = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
        except Exception as e:  # noqa: BLE001
            fails += 1
            import traceback
            print(f"FAIL  {fn.__name__}: {type(e).__name__}: {e}")
            traceback.print_exc()
    print(f"\n{len(fns) - fails}/{len(fns)} passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(_run())
