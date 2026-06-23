"""
vector_engram.archive — hot/cold split (Phase 1B).

Architecture (ENGRAM_FOR_VECTOR.md §4.2):
  * HOT  : small, fixed-capacity, exact cosine ring buffer — the on-robot index
           (bounded RAM, O(1) insert, O(capacity) query). FIFO eviction.
  * COLD : the lifelong archive on the box (hnswlib + .eng files on disk).

On eviction from hot, the situation is spilled to cold (indexed + persisted), so
nothing is lost. Retrieval merges hot + cold. This is the real bounded-memory
behavior a 24/7 robot needs — not a simulation.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .fingerprint import fingerprint
from .format import SituationCert, encode
from .state import PerceptionState
from .store import Retrieved, SituationMemory


class HotIndex:
    """Fixed-capacity exact-cosine ring buffer (the on-robot hot index)."""

    def __init__(self, dim: int, capacity: int = 1000):
        self.dim = dim
        self.capacity = capacity
        self._mat = np.zeros((capacity, dim), dtype=np.float32)
        self._norm = np.zeros((capacity, dim), dtype=np.float32)
        self._labels = np.full(capacity, -1, dtype=np.int64)
        self._count = 0
        self._head = 0  # next slot to write (oldest when full)

    def add(self, label: int, vec: np.ndarray) -> int | None:
        """Insert; return evicted label if the ring was full, else None."""
        v = np.asarray(vec, dtype=np.float32).ravel()
        slot = self._head
        evicted = int(self._labels[slot]) if self._count == self.capacity else None
        self._mat[slot] = v
        n = np.linalg.norm(v)
        self._norm[slot] = v / n if n > 0 else v
        self._labels[slot] = label
        self._head = (self._head + 1) % self.capacity
        self._count = min(self._count + 1, self.capacity)
        return evicted

    def query(self, vec: np.ndarray, k: int = 5) -> list[tuple[int, float]]:
        if self._count == 0:
            return []
        active = self._labels != -1
        mat = self._norm[active]
        labs = self._labels[active]
        v = np.asarray(vec, dtype=np.float32).ravel()
        nv = np.linalg.norm(v)
        if nv == 0:
            return []
        sims = mat @ (v / nv)
        k = min(k, sims.shape[0])
        order = np.argpartition(-sims, k - 1)[:k]
        order = order[np.argsort(-sims[order])]
        return [(int(labs[i]), float(sims[i])) for i in order]

    def __len__(self) -> int:
        return self._count


@dataclass
class HotColdStats:
    hot: int
    cold: int
    total: int


class HotColdMemory:
    """Hot ring buffer + cold disk archive, with spill-on-evict and merged search."""

    def __init__(self, dim: int, *, archive_dir: str, hot_capacity: int = 1000,
                 freqs: tuple[int, ...] = (0, 1), cold_backend: str = "hnsw", **cold_kw):
        self.dim = dim
        self.freqs = freqs
        self.hot = HotIndex(dim, hot_capacity)
        self.cold = SituationMemory(dim, archive_dir=archive_dir, backend=cold_backend,
                                    freqs=freqs, **cold_kw)
        self._certs: dict[int, SituationCert] = {}   # label -> cert (hot certs; cold also keeps its own)
        self._next = 0

    def _make_cert(self, state: PerceptionState, vec: np.ndarray) -> SituationCert:
        return SituationCert(
            vec=vec, robot_id=state.robot_id, source_id=state.source_id,
            person=state.person, activity=state.activity, place=state.place,
            situation_key=f"{state.person}|{state.activity}|{state.place}",
            emotion=state.emotion_vec4(), n_freqs=len(self.freqs),
        )

    def write_state(self, state: PerceptionState) -> int:
        vec = fingerprint(state.frames(), self.freqs)
        if vec.shape[0] != self.dim:
            raise ValueError(f"fingerprint dim {vec.shape[0]} != {self.dim}")
        cert = self._make_cert(state, vec)
        label = self._next
        self._next += 1
        self._certs[label] = cert
        evicted = self.hot.add(label, vec)
        if evicted is not None:
            self._spill(evicted)
        return label

    def _spill(self, label: int) -> None:
        cert = self._certs.pop(label, None)
        if cert is None:
            return
        clabel = self.cold._next
        self.cold._next += 1
        self.cold.index.add(clabel, cert.vec)
        self.cold._certs[clabel] = cert
        self.cold._order.append(clabel)
        if self.cold.archive_dir:
            import os
            with open(os.path.join(self.cold.archive_dir, f"{clabel:08d}.eng"), "wb") as fh:
                fh.write(encode(cert))

    def knn_state(self, query: PerceptionState, k: int = 5) -> list[Retrieved]:
        vec = fingerprint(query.frames(), self.freqs)
        return self.knn_vec(vec, k)

    def knn_vec(self, vec: np.ndarray, k: int = 5) -> list[Retrieved]:
        merged: list[Retrieved] = []
        for label, score in self.hot.query(vec, k):
            merged.append(Retrieved(cert=self._certs[label], score=score, label=label))
        merged.extend(self.cold.knn_vec(vec, k))
        merged.sort(key=lambda r: r.score, reverse=True)
        # dedup by (situation content) is unnecessary; labels are disjoint hot/cold
        return merged[:k]

    def stats(self) -> HotColdStats:
        return HotColdStats(hot=len(self.hot), cold=len(self.cold), total=len(self.hot) + len(self.cold))

    def __len__(self) -> int:
        return len(self.hot) + len(self.cold)
