"""
vector_engram.fingerprint — the situational Fourier fingerprint.

Faithful generalization of ENGRAM's `kvcos/core/fingerprint.py`
`compute_fourier_fingerprint()`:

    ENGRAM:  rFFT over the LLM *layer* axis of [n_layers, dim], keep amplitude at
             freqs [0, 1], L2-normalize each, concat  ->  [dim * 2]

    Vector:  rFFT over the *time* axis of a perception window [T, D], keep amplitude
             at freqs [0, 1], L2-normalize each, concat  ->  [D * 2]

Interpretation:
    f0 (DC)        = the steady "what is happening" component of the situation
    f1 (1st harm.) = the "how it is changing / trending" component

Deterministic, training-free, corpus-independent — same properties as ENGRAM.
"""
from __future__ import annotations

import numpy as np

DEFAULT_FREQS = (0, 1)


def fingerprint(frames: np.ndarray, freqs: tuple[int, ...] = DEFAULT_FREQS) -> np.ndarray:
    """Compute a situational fingerprint from a [T, D] frame window.

    Returns a float32 vector of length D * len(freqs), with each frequency block
    L2-normalized independently (so cosine similarity compares spectral *shape*).
    """
    x = np.asarray(frames, dtype=np.float64)
    if x.ndim == 1:
        x = x[None, :]
    if x.ndim != 2:
        raise ValueError(f"frames must be [T, D], got shape {x.shape}")
    T, D = x.shape

    spectrum = np.abs(np.fft.rfft(x, axis=0))  # [n_bins, D]
    n_bins = spectrum.shape[0]

    blocks = []
    for f in freqs:
        if f < n_bins:
            v = spectrum[f]
            norm = np.linalg.norm(v)
            v = v / norm if norm > 0 else v
        else:
            # harmonic not present (window too short for this freq): zero block.
            # Documented degradation; use T >= max(freqs)+1 to avoid.
            v = np.zeros(D, dtype=np.float64)
        blocks.append(v)

    return np.concatenate(blocks).astype(np.float32)


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=np.float64).ravel()
    b = np.asarray(b, dtype=np.float64).ravel()
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))
