"""
vector_engram.confidence — IndexC, lightweight retrieval-confidence history (Phase 1B).

Vector-grade reduction of ENGRAM's IndexC (`engram/kvcos/engram/index_c.py`): track
per-situation hit/miss outcomes so the system can (a) preempt chronically-wrong
matches ("prior preemption", retrieval Stage 0) and (b) expose confusion stats.

In-memory + optional JSON persistence. No heavy DB; designed to stay < a few MB.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field


@dataclass
class _Stat:
    hits: int = 0
    misses: int = 0

    @property
    def trials(self) -> int:
        return self.hits + self.misses

    @property
    def fail_rate(self) -> float:
        return self.misses / self.trials if self.trials else 0.0


@dataclass
class ConfidenceLog:
    min_trials_to_preempt: int = 5
    max_fail_rate: float = 0.5
    _stats: dict[str, _Stat] = field(default_factory=dict)

    def record(self, key: str, success: bool) -> None:
        s = self._stats.setdefault(key, _Stat())
        if success:
            s.hits += 1
        else:
            s.misses += 1

    def fail_rate(self, key: str) -> float:
        return self._stats[key].fail_rate if key in self._stats else 0.0

    def should_preempt(self, key: str) -> bool:
        """True if this situation has a chronic failure history → skip/penalize it."""
        s = self._stats.get(key)
        return bool(s and s.trials >= self.min_trials_to_preempt and s.fail_rate > self.max_fail_rate)

    def summary(self) -> dict:
        return {
            "tracked": len(self._stats),
            "preempting": sum(1 for k in self._stats if self.should_preempt(k)),
        }

    # ---- persistence -------------------------------------------------------- #
    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as fh:
            json.dump({k: [v.hits, v.misses] for k, v in self._stats.items()}, fh)

    @classmethod
    def load(cls, path: str, **kw) -> "ConfidenceLog":
        log = cls(**kw)
        if os.path.exists(path):
            with open(path) as fh:
                for k, (h, m) in json.load(fh).items():
                    log._stats[k] = _Stat(hits=h, misses=m)
        return log
