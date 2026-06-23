"""
vector_engram.store — SituationMemory: the end-to-end substrate.

Ties the pieces together:
  PerceptionState --fingerprint--> SituationCert --encode--> .eng file
                                          |                       |
                                          +--> SituationIndex <---+ (reload)

Exposes a MemoryStore-compatible surface (write/knn/__len__) so it can drop into
the Deep-Understanding three-brain skeleton's `MemoryStore` seam, plus richer
situation-level helpers.

This is the box-side reference (numpy + hnswlib). The on-robot hot path (C/NEON,
small exact index) is a future drop-in behind the same SituationIndex(backend=...).
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass

import numpy as np

from .fingerprint import fingerprint
from .format import SituationCert, decode, encode
from .index import SituationIndex
from .state import PerceptionState, StateVector


@dataclass
class Retrieved:
    cert: SituationCert
    score: float
    label: int


class SituationMemory:
    def __init__(self, dim: int, *, archive_dir: str | None = None, backend: str = "hnsw",
                 freqs: tuple[int, ...] = (0, 1), hot_size: int | None = None, **index_kw):
        self.dim = dim
        self.freqs = freqs
        self.archive_dir = archive_dir
        self.hot_size = hot_size
        self.index = SituationIndex(dim, backend=backend, **index_kw)
        self._certs: dict[int, SituationCert] = {}
        self._order: list[int] = []          # insertion order (for hot eviction view)
        self._next = 0
        if archive_dir:
            os.makedirs(archive_dir, exist_ok=True)

    # ---- core write/read ---------------------------------------------------- #
    def fingerprint_state(self, state: StateVector) -> np.ndarray:
        return fingerprint(state.frames(), self.freqs)

    def write_state(self, state: PerceptionState, *, persist: bool = True) -> int:
        vec = self.fingerprint_state(state)
        if vec.shape[0] != self.dim:
            raise ValueError(f"fingerprint dim {vec.shape[0]} != index dim {self.dim} "
                             f"(check feature dim D and #freqs)")
        cert = SituationCert(
            vec=vec, robot_id=getattr(state, "robot_id", "vector-0"),
            source_id=getattr(state, "source_id", "vector_perception"),
            person=getattr(state, "person", ""), activity=getattr(state, "activity", ""),
            place=getattr(state, "place", ""),
            situation_key=f"{getattr(state,'person','')}|{getattr(state,'activity','')}|{getattr(state,'place','')}",
            emotion=state.emotion_vec4() if isinstance(state, PerceptionState) else np.zeros(4, np.float32),
            n_freqs=len(self.freqs),
        )
        label = self._next
        self._next += 1
        self.index.add(label, cert.vec)
        self._certs[label] = cert
        self._order.append(label)
        if persist and self.archive_dir:
            with open(os.path.join(self.archive_dir, f"{label:08d}.eng"), "wb") as fh:
                fh.write(encode(cert))
        return label

    def knn_state(self, query: StateVector, k: int = 5) -> list[Retrieved]:
        vec = self.fingerprint_state(query)
        return self.knn_vec(vec, k)

    def knn_vec(self, vec: np.ndarray, k: int = 5) -> list[Retrieved]:
        out = []
        for label, score in self.index.query(vec, k):
            out.append(Retrieved(cert=self._certs[label], score=score, label=label))
        return out

    # ---- MemoryStore-compatible surface (for the DU skeleton) --------------- #
    def write(self, fp: np.ndarray, meta: dict, score: float = 1.0) -> int:
        cert = SituationCert(vec=np.asarray(fp, dtype=np.float32),
                             situation_key=str(meta.get("key", "")),
                             source_id=str(meta.get("source_id", "raw")))
        label = self._next; self._next += 1
        self.index.add(label, cert.vec)
        self._certs[label] = cert
        self._order.append(label)
        return label

    def knn(self, fp: np.ndarray, k: int) -> list[tuple[float, dict]]:
        res = self.knn_vec(np.asarray(fp, dtype=np.float32), k)
        return [(r.score, {"key": r.cert.situation_key, "label": r.label}) for r in res]

    def __len__(self) -> int:
        return len(self._certs)

    # ---- archive reload ----------------------------------------------------- #
    @classmethod
    def load(cls, archive_dir: str, *, backend: str = "hnsw", freqs: tuple[int, ...] = (0, 1),
             **index_kw) -> "SituationMemory":
        files = sorted(f for f in os.listdir(archive_dir) if f.endswith(".eng"))
        if not files:
            raise FileNotFoundError(f"no .eng files in {archive_dir}")
        first = decode(open(os.path.join(archive_dir, files[0]), "rb").read())
        mem = cls(dim=first.vec.shape[0], archive_dir=archive_dir, backend=backend, freqs=freqs, **index_kw)
        for f in files:
            cert = decode(open(os.path.join(archive_dir, f), "rb").read())
            label = mem._next; mem._next += 1
            mem.index.add(label, cert.vec)
            mem._certs[label] = cert
            mem._order.append(label)
        return mem
