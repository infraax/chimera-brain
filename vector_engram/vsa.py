"""
vector_engram.vsa — the binding algebra (HRR), kept minimal and honest.

These are the Vector-Symbolic primitives the COMPOSE layer will need to weave many
memory-impressions into one labelled "identity shape" (self / environment / person:X).
They are NOT the COMPOSE layer itself — COMPOSE is gated on the capacity experiment
(`capacity_experiment.py`), which uses exactly these primitives to answer "how many
impressions can be bundled under a label and still be individually recovered?".

We keep the canonical HRR vocabulary (bind / bundle / unbind / cleanup) rather than
inventing creature-names, because this is a known algebra and faithfulness to the
literature matters more than metaphor here (Plate 1995; see `frequency_memory__UNIFIED.md`).
The creature-facing naming returns at the COMPOSE layer ("weave a self").

  bind(a, b)   = circular convolution  = ifft(fft(a)·fft(b))     — tie a role to a filler
  unbind(c, a) = circular correlation  = ifft(fft(c)·conj(fft(a))) — recover the filler
  bundle(...)  = normalized superposition (sum) — hold many bound pairs in one vector
  cleanup(v)   = snap a noisy estimate to the nearest clean item (the item-memory)

All real-valued, training-free, deterministic.
"""
from __future__ import annotations

import numpy as np


def normalize(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=np.float64)
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def random_vectors(n: int, dim: int, *, rng: np.random.Generator) -> np.ndarray:
    """n near-orthogonal unit vectors [n, dim] (iid Gaussian, normalized) — the VSA
    ideal: random high-dim vectors are ~orthogonal (the 'blessing of dimensionality')."""
    M = rng.normal(0.0, 1.0, size=(n, dim))
    return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-12)


def bind(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Circular convolution (HRR bind). Same dim in, same dim out. Binding with a random
    role vector approximately RANDOM-ROTATES the filler — which is what lets correlated
    items become near-orthogonal bundle components."""
    fa = np.fft.fft(np.asarray(a, dtype=np.float64))
    fb = np.fft.fft(np.asarray(b, dtype=np.float64))
    return np.real(np.fft.ifft(fa * fb))


def unbind(c: np.ndarray, a: np.ndarray) -> np.ndarray:
    """Circular correlation (HRR unbind): recover the filler bound with role `a`."""
    fc = np.fft.fft(np.asarray(c, dtype=np.float64))
    fa = np.fft.fft(np.asarray(a, dtype=np.float64))
    return np.real(np.fft.ifft(fc * np.conj(fa)))


def bundle(vectors: list[np.ndarray] | np.ndarray, *, renormalize: bool = True) -> np.ndarray:
    """Superpose (sum) bound pairs into one vector; L2-normalize by default."""
    s = np.sum(np.asarray(vectors, dtype=np.float64), axis=0)
    return normalize(s) if renormalize else s


def cleanup(noisy: np.ndarray, codebook: np.ndarray) -> int:
    """Index of the codebook item most similar to `noisy` (cosine). The 'item memory'
    that snaps a noisy unbind back to a clean stored item."""
    q = normalize(noisy)
    C = codebook / (np.linalg.norm(codebook, axis=1, keepdims=True) + 1e-12)
    return int(np.argmax(C @ q))


def pairwise_cosine_stats(M: np.ndarray) -> dict:
    """Off-diagonal cosine statistics of a set of vectors [N, D] — the correlation
    metric. Near 0 = near-orthogonal (VSA ideal); larger = correlated (capacity-limiting)."""
    C = np.asarray(M, dtype=np.float64)
    C = C / (np.linalg.norm(C, axis=1, keepdims=True) + 1e-12)
    S = C @ C.T
    n = S.shape[0]
    off = S[~np.eye(n, dtype=bool)]
    return {"mean_abs": float(np.mean(np.abs(off))),
            "std": float(np.std(off)),
            "max_abs": float(np.max(np.abs(off))),
            "p95_abs": float(np.percentile(np.abs(off), 95))}


class RandomProjection:
    """Fixed random Gaussian projection D -> Dhi (the candidate capacity fix).

    Johnson–Lindenstrauss: such a projection approximately PRESERVES pairwise cosines, so
    it does NOT by itself decorrelate items — a fact the capacity experiment exists to
    confirm/deny. It IS, however, how you lift a small fingerprint into the higher-D space
    VSA bundling wants. Deterministic (seeded)."""

    def __init__(self, in_dim: int, out_dim: int, *, seed: int = 0):
        rng = np.random.default_rng(seed)
        self.in_dim = in_dim
        self.out_dim = out_dim
        # 1/sqrt(out_dim) scaling keeps projected norms ~comparable
        self.R = rng.normal(0.0, 1.0, size=(in_dim, out_dim)) / np.sqrt(out_dim)

    def project(self, v: np.ndarray) -> np.ndarray:
        v = np.asarray(v, dtype=np.float64)
        return (v @ self.R) if v.ndim == 1 else (v @ self.R)
