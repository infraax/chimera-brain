"""
vector_engram.state — the decoupling seam.

ENGRAM today is hard-wired to llama.cpp KV-caches
(`engram/integrations/llama_cpp_bridge.py` + `kvcos/core/blob_parser.py`).
This module introduces a tiny `StateVector` protocol so the *same* Fourier
fingerprint pipeline can ingest ANY structured state — in particular a Vector
robot's fused multimodal perception window.

A "state" is a short temporal window of frames, shape [T, D]:
  T = number of recent frames (>= 2 so a 1st harmonic exists)
  D = feature dimension of one fused perception frame

This window-over-time is the faithful analogue of ENGRAM fingerprinting over an
LLM's layer axis, and it is what makes the fingerprint stable at the very short
contexts a robot produces (the open question flagged in ENGRAM_FOR_VECTOR.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class StateVector(Protocol):
    """Anything fingerprintable. The one method the fingerprint pipeline needs."""

    def frames(self) -> np.ndarray:
        """Return a float array of shape [T, D] (T frames, D features)."""
        ...

    @property
    def source_id(self) -> str:
        """e.g. 'vector_perception' | 'llama_kv' | 'raw'."""
        ...


@dataclass
class RawState:
    """Generic [T, D] state (tests, or a non-perception source)."""

    data: np.ndarray
    source_id: str = "raw"

    def frames(self) -> np.ndarray:
        x = np.asarray(self.data, dtype=np.float64)
        return x[None, :] if x.ndim == 1 else x


# ---- Perception (the Vector case) ------------------------------------------ #
# A single perception frame fuses the modalities Anki already has on the robot
# (vision/audio/touch/imu) plus the L1 emotion vector. We stack the last T frames
# into a [T, D] window and fingerprint that window.

@dataclass
class PerceptionFrame:
    vision: np.ndarray      # e.g. pooled CNN/scene features [Cv]
    audio: np.ndarray       # e.g. pooled spectrogram/affect [Ca]
    touch: np.ndarray       # capacitive grid summary [Ct]
    imu: np.ndarray         # [ax,ay,az,gx,gy,gz, ...] [Ci]
    emotion: np.ndarray     # L1 emotion vector [Ce] (Happy,Confident,Social,Stim,Trust,...)

    def vector(self) -> np.ndarray:
        return np.concatenate([
            np.asarray(self.vision, dtype=np.float64).ravel(),
            np.asarray(self.audio, dtype=np.float64).ravel(),
            np.asarray(self.touch, dtype=np.float64).ravel(),
            np.asarray(self.imu, dtype=np.float64).ravel(),
            np.asarray(self.emotion, dtype=np.float64).ravel(),
        ])


@dataclass
class PerceptionState:
    """A short window of fused perception frames + situational metadata."""

    window: list[PerceptionFrame] = field(default_factory=list)
    # situational metadata (rides along into the .eng certificate)
    robot_id: str = "vector-0"
    person: str = ""
    activity: str = ""
    place: str = ""
    source_id: str = "vector_perception"

    def push(self, frame: PerceptionFrame, max_window: int = 8) -> None:
        self.window.append(frame)
        if len(self.window) > max_window:
            self.window.pop(0)

    def frames(self) -> np.ndarray:
        if not self.window:
            raise ValueError("PerceptionState has no frames")
        return np.stack([f.vector() for f in self.window], axis=0)

    def emotion_vec4(self) -> np.ndarray:
        """First 4 emotion dims for the certificate header (valence-ish summary).
        Pads/truncates to 4."""
        e = np.asarray(self.window[-1].emotion, dtype=np.float32).ravel() if self.window else np.zeros(4, np.float32)
        out = np.zeros(4, dtype=np.float32)
        out[: min(4, e.shape[0])] = e[:4]
        return out
