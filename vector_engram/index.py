"""
vector_engram.index — situational ANN index.

Two REAL backends (no simulation):
  * "hnsw"  : hnswlib cosine index (the box-side production path; ENGRAM uses faiss
              HNSW, hnswlib is the same algorithm with an easier embedded build).
  * "exact" : numpy exact cosine — ground truth for recall verification, and a real
              option for the small on-robot hot index.

Both return (label, cosine_similarity) sorted descending.
"""
from __future__ import annotations

import numpy as np

try:
    import hnswlib  # type: ignore
    _HAVE_HNSW = True
except Exception:  # pragma: no cover
    _HAVE_HNSW = False


def _l2norm(m: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(m, axis=-1, keepdims=True)
    n[n == 0] = 1.0
    return m / n


class SituationIndex:
    def __init__(self, dim: int, backend: str = "hnsw", *, M: int = 16,
                 ef_construction: int = 200, ef_search: int = 64, max_elements: int = 100_000):
        self.dim = dim
        self.backend = backend if (backend != "hnsw" or _HAVE_HNSW) else "exact"
        self._ef_search = ef_search
        if self.backend == "hnsw":
            self._idx = hnswlib.Index(space="cosine", dim=dim)
            self._idx.init_index(max_elements=max_elements, ef_construction=ef_construction, M=M)
            self._idx.set_ef(ef_search)
        else:
            self._vecs: list[np.ndarray] = []
            self._labels: list[int] = []
        self._n = 0

    @property
    def have_hnsw(self) -> bool:
        return _HAVE_HNSW

    def add(self, label: int, vec: np.ndarray) -> None:
        v = np.asarray(vec, dtype=np.float32).reshape(1, -1)
        if self.backend == "hnsw":
            self._idx.add_items(v, np.asarray([label]))
        else:
            self._vecs.append(_l2norm(v)[0])
            self._labels.append(label)
        self._n += 1

    def add_batch(self, labels, vecs: np.ndarray) -> None:
        vecs = np.asarray(vecs, dtype=np.float32)
        if self.backend == "hnsw":
            self._idx.add_items(vecs, np.asarray(labels))
            self._n += len(labels)
        else:
            for lab, v in zip(labels, vecs):
                self.add(int(lab), v)

    def query(self, vec: np.ndarray, k: int = 5) -> list[tuple[int, float]]:
        if self._n == 0:
            return []
        k = min(k, self._n)
        v = np.asarray(vec, dtype=np.float32).reshape(1, -1)
        if self.backend == "hnsw":
            labels, dists = self._idx.knn_query(v, k=k)
            # hnswlib cosine "distance" = 1 - cosine_similarity
            return [(int(lab), float(1.0 - d)) for lab, d in zip(labels[0], dists[0])]
        mat = np.stack(self._vecs, axis=0)
        sims = mat @ _l2norm(v)[0]
        order = np.argsort(-sims)[:k]
        return [(int(self._labels[i]), float(sims[i])) for i in order]

    def set_ef(self, ef: int) -> None:
        self._ef_search = ef
        if self.backend == "hnsw":
            self._idx.set_ef(ef)

    def __len__(self) -> int:
        return self._n
