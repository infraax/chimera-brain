"""
vector_engram.resonance — recall by resonance (the RETRIEVE pillar).

Plain nearest-neighbour recall asks "which one stored moment is closest?" — a single,
sharp winner. A creature recalls more richly than that: a cue can *resonate* across
several remembered moments, and a partial or noisy cue can *settle* toward the moment it
half-matches. Both are the same faculty at different sharpness.

Modern Hopfield networks (Ramsauer 2020) make this exact: the retrieval update is the
attention mechanism, and ordinary cosine-kNN is its β→∞ (infinitely sharp) special case
(Universal Hopfield, Millidge 2022 — see `frequency_memory__UNIFIED.md`). So we don't
replace the store; we swap the *separation function*:

    sims = P · x                 (P = stored fingerprints, x = cue)
    w    = softmax(β · sims)      (β = sharpness of resonance — the "confidence dial")
    x'   = Pᵀ · w                 (the cue settles toward a weighted blend of memories)
    repeat `steps` times          (multi-step = pattern completion from partial cues)

  • low β   → the cue resonates across many similar memories (a blended, contextual sense)
  • high β  → it snaps to one memory (sharp episodic recall); β→∞ == argmax == kNN
  • steps>1 → iterative settling completes a degraded cue before ranking

Training-free, zero new storage (reuses the same fingerprints). One step is cheap enough
for the brainstem; multi-step settling is a box-side faculty.

LIMITATION (measured, not theoretical — the capacity caveat made real):
  Clean attractor completion assumes near-orthogonal patterns. ENGRAM fingerprints are
  *correlated* L2-normalized spectra, so settling can blend toward the centroid of
  similar memories instead of completing toward the right one. Empirically (Phase 3):
    • steps=1, any β       → identical top-1 to cosine-kNN (no harm, no gain)
    • β→∞,   steps=1       → exactly cosine-kNN (the proven special case)
    • steps 2–3, high β    → small genuine gain on degraded cues
    • many steps, low β    → COLLAPSE toward the centroid (much worse than kNN)
  So the big "free pattern completion" win is GATED on the same fix as composition:
  random-projection of fingerprints into a higher-D near-orthogonal space (the capacity
  experiment in `frequency_memory__UNIFIED.md`). Until then, default to safe settings
  (steps=1; or steps≤3 at high β) and treat low-β many-step settling as experimental.
"""
from __future__ import annotations

import numpy as np


def softmax(z: np.ndarray) -> np.ndarray:
    """Numerically-stable softmax over the last axis."""
    z = np.asarray(z, dtype=np.float64)
    z = z - np.max(z)
    e = np.exp(z)
    s = e.sum()
    return e / s if s > 0 else np.full_like(e, 1.0 / e.shape[0])


def _l2(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def resonate(cue: np.ndarray, patterns: np.ndarray, *, beta: float = 8.0,
             steps: int = 1) -> tuple[np.ndarray, np.ndarray]:
    """Let `cue` resonate against stored `patterns` (Modern Hopfield update).

    cue:      [D] query fingerprint
    patterns: [M, D] stored fingerprints (rows are L2-normalized internally)
    beta:     resonance sharpness (low = blend, high = sharp; → kNN as beta → ∞)
    steps:    settling iterations (>=2 completes partial/noisy cues)

    Returns (completed_cue [D], weights [M]) — `weights` is the resonance distribution
    over the patterns (what the cue resonates with), summing to 1.
    """
    P = np.asarray(patterns, dtype=np.float64)
    if P.ndim != 2:
        raise ValueError(f"patterns must be [M, D], got {P.shape}")
    P = P / (np.linalg.norm(P, axis=1, keepdims=True) + 1e-12)  # row-normalize for cosine energy
    x = _l2(np.asarray(cue, dtype=np.float64).ravel())
    w = np.full(P.shape[0], 1.0 / P.shape[0])
    for _ in range(max(1, steps)):
        sims = P @ x                 # [M] cosine similarities
        w = softmax(beta * sims)     # [M] resonance weights
        x = _l2(P.T @ w)             # settle toward the weighted blend
    return x.astype(np.float32), w.astype(np.float64)
