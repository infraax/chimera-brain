"""
vector_engram.query — metadata filters + situation classifier (Phase 2).

Built on top of retrieval:
  * filter_retrieved : who/where/activity/time-range filtering of results
  * SituationClassifier : k-NN over remembered situations to predict the current
    situation's person / activity / place from its fingerprint (no training — uses
    the memory itself, like the rest of ENGRAM).
"""
from __future__ import annotations

from collections import Counter

from .store import Retrieved, SituationMemory


def filter_retrieved(results: list[Retrieved], *, person: str | None = None,
                     activity: str | None = None, place: str | None = None,
                     t_min: float | None = None, t_max: float | None = None) -> list[Retrieved]:
    out = []
    for r in results:
        c = r.cert
        if person is not None and c.person != person:
            continue
        if activity is not None and c.activity != activity:
            continue
        if place is not None and c.place != place:
            continue
        if t_min is not None and c.timestamp < t_min:
            continue
        if t_max is not None and c.timestamp > t_max:
            continue
        out.append(r)
    return out


class SituationClassifier:
    """Predict who/what/where for a query situation via weighted k-NN over memory."""

    def __init__(self, memory: SituationMemory, k: int = 9):
        self.memory = memory
        self.k = k

    def _vote(self, results: list[Retrieved], field: str) -> str:
        scores: Counter = Counter()
        for r in results:
            val = getattr(r.cert, field)
            scores[val] += max(r.score, 0.0)  # similarity-weighted vote
        return scores.most_common(1)[0][0] if scores else ""

    def predict(self, query_state) -> dict:
        res = self.memory.knn_state(query_state, k=self.k)
        return {
            "person": self._vote(res, "person"),
            "activity": self._vote(res, "activity"),
            "place": self._vote(res, "place"),
            "support": len(res),
        }
