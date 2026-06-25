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


def fingerprint_gdf(frames: np.ndarray, freqs: tuple[int, ...] = DEFAULT_FREQS,
                    eps: float = 1e-8) -> np.ndarray:
    """Amplitude fingerprint + a group-delay (phase) complement — repr "rfft+gdf".

    The plain amplitude fingerprint above answers "what is happening / how much is each
    feature changing" but is BLIND to *when* within the window a change happened: two
    windows that are time-reverses of each other have an identical amplitude spectrum.
    The group-delay function (GDF) — the negative derivative of the phase spectrum —
    restores that timing/ordering information, and it is the cheapest representation win
    in `frequency_memory__UNIFIED.md` (P1): a few extra FFTs, no training.

    We use the product-spectrum form that avoids phase unwrapping (robust in noise):
        X  = rFFT(x) ,  Y = rFFT(n * x)         (n = time index)
        GD = (Xr*Yr + Xi*Yi) / |X|^2            per bin, per feature
    GD at f0 is the signal's temporal centroid; at f1 it is the trend's position/direction.

    Layout: the amplitude blocks come FIRST (so the leading half is byte-identical to
    `fingerprint()` — easy migration/debugging), then the L2-normalized GD blocks.
    Returns float32 of length D * len(freqs) * 2.
    """
    x = np.asarray(frames, dtype=np.float64)
    if x.ndim == 1:
        x = x[None, :]
    if x.ndim != 2:
        raise ValueError(f"frames must be [T, D], got shape {x.shape}")
    T, D = x.shape

    n = np.arange(T, dtype=np.float64)[:, None]      # time index [T,1]
    X = np.fft.rfft(x, axis=0)                        # [n_bins, D] complex
    Y = np.fft.rfft(n * x, axis=0)                    # [n_bins, D] complex
    n_bins = X.shape[0]

    amp = np.abs(X)                                   # [n_bins, D]
    power = (X.real ** 2 + X.imag ** 2) + eps
    gd = (X.real * Y.real + X.imag * Y.imag) / power  # group delay (samples) [n_bins, D]

    amp_blocks, gd_blocks = [], []
    for f in freqs:
        if f < n_bins:
            a = amp[f]; na = np.linalg.norm(a); a = a / na if na > 0 else a
            g = gd[f];  ng = np.linalg.norm(g); g = g / ng if ng > 0 else g
        else:
            a = np.zeros(D); g = np.zeros(D)          # window too short for this freq
        amp_blocks.append(a)
        gd_blocks.append(g)

    return np.concatenate(amp_blocks + gd_blocks).astype(np.float32)


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=np.float64).ravel()
    b = np.asarray(b, dtype=np.float64).ravel()
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))
