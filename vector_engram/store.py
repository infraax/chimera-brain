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
from .sense import REFLEX_REPR, Sense, reflex_impression
from .state import PerceptionState, StateVector


@dataclass
class Retrieved:
    cert: SituationCert
    score: float
    label: int


class SituationMemory:
    """One register of situational memory: a single cosine space of one *sense*.

    Defaults to the REFLEX sense (raw fused sensation -> fingerprint), which keeps the
    original behaviour. The MEANING register is the same class configured with the
    meaning impression. `TwofoldMemory` below holds one of each — the creature
    remembering a moment twice.
    """

    def __init__(self, dim: int, *, archive_dir: str | None = None, backend: str = "hnsw",
                 freqs: tuple[int, ...] = (0, 1), hot_size: int | None = None,
                 sense: Sense = Sense.REFLEX, repr_id: str = REFLEX_REPR,
                 impression=reflex_impression, **index_kw):
        self.dim = dim
        self.freqs = freqs
        self.archive_dir = archive_dir
        self.hot_size = hot_size
        self.sense = Sense(sense)
        self.repr_id = repr_id
        self.impression = impression   # how this register forms a trace from a moment
        self.index = SituationIndex(dim, backend=backend, **index_kw)
        self._certs: dict[int, SituationCert] = {}
        self._order: list[int] = []          # insertion order (for hot eviction view)
        self._next = 0
        if archive_dir:
            os.makedirs(archive_dir, exist_ok=True)

    # ---- core write/read ---------------------------------------------------- #
    def fingerprint_state(self, state: StateVector) -> np.ndarray:
        # routes through this register's sense (reflex or meaning); same FFT math.
        return self.impression(state, self.freqs)

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
            emotion=state.emotion_vec4() if hasattr(state, "emotion_vec4") else np.zeros(4, np.float32),
            n_freqs=len(self.freqs), sense=int(self.sense), repr_id=self.repr_id,
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
                             source_id=str(meta.get("source_id", "raw")),
                             sense=int(self.sense), repr_id=self.repr_id)
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


class TwofoldMemory:
    """The creature remembers each moment twice — by feel and by meaning.

    Holds two registers (the VRCM "Twofold Self" made concrete):
      .reflex  — the body's instinctive impressions (raw sensation, fast, on-robot)
      .meaning — the head's recognitions (encoder embeddings, slow, box)

    They are SEPARATE cosine spaces, never compared across senses. A moment can be
    laid down in one register or both; recall is per-sense. The reflex register works
    even if the meaning register (which needs the box + encoders) is absent — graceful
    degradation, the Anki way.

    The MEANING register is only created if `meaning_dim` is given (you don't pay for
    the cortex if you only have a brainstem).
    """

    def __init__(self, reflex_dim: int, *, meaning_dim: int | None = None,
                 archive_dir: str | None = None, backend: str = "hnsw",
                 freqs: tuple[int, ...] = (0, 1), **index_kw):
        # local imports keep the sense vocabulary in one place + avoid a cycle
        from .sense import MEANING_REPR, REFLEX_REPR, Sense, meaning_impression, reflex_impression

        reflex_dir = os.path.join(archive_dir, "reflex") if archive_dir else None
        self.reflex = SituationMemory(
            reflex_dim, archive_dir=reflex_dir, backend=backend, freqs=freqs,
            sense=Sense.REFLEX, repr_id=REFLEX_REPR, impression=reflex_impression, **index_kw)

        self.meaning: SituationMemory | None = None
        if meaning_dim is not None:
            meaning_dir = os.path.join(archive_dir, "meaning") if archive_dir else None
            self.meaning = SituationMemory(
                meaning_dim, archive_dir=meaning_dir, backend=backend, freqs=freqs,
                sense=Sense.MEANING, repr_id=MEANING_REPR, impression=meaning_impression, **index_kw)

    # ---- lay down a memory -------------------------------------------------- #
    def feel(self, perception, *, persist: bool = True) -> int:
        """Lay down a REFLEX trace: the body felt this moment. Always available."""
        return self.reflex.write_state(perception, persist=persist)

    def recognize(self, meaning, *, persist: bool = True) -> int:
        """Lay down a MEANING trace: the head recognised this moment.

        Requires the meaning register (raises if this creature has no cortex)."""
        if self.meaning is None:
            raise RuntimeError("no MEANING register (construct with meaning_dim=…)")
        return self.meaning.write_state(meaning, persist=persist)

    # ---- recall ------------------------------------------------------------- #
    def recall_reflex(self, perception, k: int = 5) -> list[Retrieved]:
        """'Has my body felt a moment like this before?'"""
        return self.reflex.knn_state(perception, k)

    def recall_meaning(self, meaning, k: int = 5) -> list[Retrieved]:
        """'Do I recognise what this is?'"""
        if self.meaning is None:
            raise RuntimeError("no MEANING register (construct with meaning_dim=…)")
        return self.meaning.knn_state(meaning, k)

    def __len__(self) -> int:
        n = len(self.reflex)
        return n + (len(self.meaning) if self.meaning is not None else 0)
