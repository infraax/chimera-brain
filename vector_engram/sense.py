"""
vector_engram.sense — the two senses of a moment (the two-rate hybrid).

A creature does not remember a moment in one register. It remembers it twice:

  • the REFLEX sense  — the body's instant, instinctive read of *what is happening*
                        and *how it is changing*. Raw fused sensation -> Fourier
                        fingerprint. Training-free, deterministic, cheap enough to
                        live in the brainstem (on-robot, fast / "gamma" rate).

  • the MEANING sense — the head's slower, considered read of *what this is* and
                        *what it means*. Learned encoder embeddings (vision/audio/
                        affect) -> Fourier fingerprint over the embedding window.
                        Richer, runs in the cortex (the box, slow / "theta" rate).

This mirrors how Anki modelled Vector: a fast reflexive layer that *feels* the world
and a slower layer that *recognises* it. The two senses produce the same SHAPE of
memory trace (a fingerprint vector) so they share the store/index machinery, but they
live in different cosine spaces and are never compared across senses — the creature
keeps "this felt like that" separate from "this means that".

Grounding: this is the theta/gamma split from `frequency_memory__UNIFIED.md` made
concrete, and the chimera L1(reflex)/L2(cortex) split made concrete. The MEANING
sense is the seam where the modern perception encoders from
`cutting_edge_oss__UNIFIED.md` (MobileCLIP, Depth Anything V2, emotion2vec, TitaNet…)
attach — see the `MeaningEncoder` hook below.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Protocol, runtime_checkable

import numpy as np

from .fingerprint import DEFAULT_FREQS, fingerprint, fingerprint_gdf
from .state import PerceptionState, StateVector


class Sense(IntEnum):
    """The two registers in which the creature takes in — and later recalls — a moment.

    Stored in every certificate so a recalled memory knows which sense formed it.
    Reflex and Meaning traces live in DIFFERENT vector spaces; do not compare across.
    """

    REFLEX = 0   # the body's instant impression (raw sensation -> fingerprint)
    MEANING = 1  # the head's considered recognition (embeddings -> fingerprint)


# ---- representation ids (the payload-version tag) -------------------------- #
# The *format envelope* (timestamps, labels, sense, crc…) is stable; the fingerprint
# *payload* is allowed to evolve. Each fingerprint carries a repr_id so a future
# representation can join without a format break (the envelope/payload split discussed
# for EGRV v2). Today there is one per sense; tomorrow expect "rfft+gdf.*",
# "scatter.*", "multiscale.*" as the frequency-report upgrades land.
REFLEX_REPR = "rfft.raw.v1"     # raw fused sensation, |rFFT| amplitude {0,1}
MEANING_REPR = "rfft.embed.v1"  # fused encoder embeddings, |rFFT| amplitude {0,1}
# Phase 2 — the GDF (group-delay / phase) complement. Same substrate, +temporal-order
# sensitivity (see fingerprint_gdf). Dim doubles. Opt-in until we flip the default.
REFLEX_GDF_REPR = "rfft+gdf.raw.v1"
MEANING_GDF_REPR = "rfft+gdf.embed.v1"


# ---- the MEANING sense: a window of *recognised* frames -------------------- #
# Where PerceptionFrame is raw sensation, an EmbeddingFrame is one fused frame of
# learned features the creature has already recognised (the encoders ran upstream).

@dataclass
class EmbeddingFrame:
    """One fused frame of learned perception embeddings (vision+audio+affect+…).

    The embedding is produced upstream by the encoders (see MeaningEncoder); ENGRAM
    only fingerprints it. Keep the fusion order stable across frames so the time-axis
    FFT is meaningful.
    """

    embedding: np.ndarray  # [De] fused embedding for this instant

    def vector(self) -> np.ndarray:
        return np.asarray(self.embedding, dtype=np.float64).ravel()


@dataclass
class MeaningState:
    """A short window of *recognised* frames + situational metadata.

    The MEANING-sense analogue of PerceptionState. Implements the StateVector
    protocol so it flows through the same fingerprint -> cert -> index path.
    """

    window: list[EmbeddingFrame] = field(default_factory=list)
    robot_id: str = "vector-0"
    person: str = ""
    activity: str = ""
    place: str = ""
    source_id: str = "vector_meaning"
    # optional affect summary carried for the certificate header (parity with
    # PerceptionState.emotion_vec4); zeros if the meaning sense doesn't supply it.
    affect: np.ndarray = field(default_factory=lambda: np.zeros(4, np.float32))

    def push(self, frame: EmbeddingFrame, max_window: int = 8) -> None:
        self.window.append(frame)
        if len(self.window) > max_window:
            self.window.pop(0)

    def frames(self) -> np.ndarray:
        if not self.window:
            raise ValueError("MeaningState has no frames")
        return np.stack([f.vector() for f in self.window], axis=0)

    def emotion_vec4(self) -> np.ndarray:
        a = np.asarray(self.affect, dtype=np.float32).ravel()
        out = np.zeros(4, dtype=np.float32)
        out[: min(4, a.shape[0])] = a[:4]
        return out


# ---- the two sensing faculties (form an impression vector from a moment) --- #

def reflex_impression(state: StateVector, freqs: tuple[int, ...] = DEFAULT_FREQS) -> np.ndarray:
    """The body's instant read: raw fused sensation -> situational fingerprint.

    Answers "what is happening / how is it changing", not "what is it". Training-free
    and deterministic — safe to run in the brainstem (on-robot, every moment).
    """
    return fingerprint(state.frames(), freqs)


def meaning_impression(state: StateVector, freqs: tuple[int, ...] = DEFAULT_FREQS) -> np.ndarray:
    """The head's considered read: learned embeddings -> situational fingerprint.

    Answers "who/what is this, what does it mean". The fingerprint math is identical to
    the reflex sense — the difference is the substrate (recognised embeddings, not raw
    sensation) and that it runs slower, in the cortex (the box).
    """
    return fingerprint(state.frames(), freqs)


# Phase 2: the same two faculties, but with the GDF phase complement (temporal order).
def reflex_impression_gdf(state: StateVector, freqs: tuple[int, ...] = DEFAULT_FREQS) -> np.ndarray:
    """REFLEX sense with the group-delay complement — feels *when*, not just *how much*."""
    return fingerprint_gdf(state.frames(), freqs)


def meaning_impression_gdf(state: StateVector, freqs: tuple[int, ...] = DEFAULT_FREQS) -> np.ndarray:
    """MEANING sense with the group-delay complement."""
    return fingerprint_gdf(state.frames(), freqs)


# ---- representation selection (sense × representation -> faculty + tag + dim) -- #
# Keeps the store generic: it just holds an impression callable + a repr_id. This maps
# a human choice ("raw" | "gdf") to the right pair for each sense, and gives the
# fingerprint dim so callers don't hand-compute it.
_REPRESENTATIONS = {
    # representation -> (reflex_repr, meaning_repr, reflex_fn, meaning_fn, dim_mult_per_freq)
    "raw": (REFLEX_REPR, MEANING_REPR, reflex_impression, meaning_impression, 1),
    "gdf": (REFLEX_GDF_REPR, MEANING_GDF_REPR, reflex_impression_gdf, meaning_impression_gdf, 2),
}


def impression_for(sense: Sense, representation: str = "raw"):
    """Return (impression_fn, repr_id) for a sense + representation choice."""
    try:
        rrepr, mrepr, rfn, mfn, _ = _REPRESENTATIONS[representation]
    except KeyError:
        raise ValueError(f"unknown representation {representation!r}; "
                         f"choices: {sorted(_REPRESENTATIONS)}")
    if Sense(sense) == Sense.REFLEX:
        return rfn, rrepr
    return mfn, mrepr


def fingerprint_dim(feature_dim: int, freqs: tuple[int, ...] = DEFAULT_FREQS,
                    representation: str = "raw") -> int:
    """The fingerprint length for a given feature dim, #freqs, and representation.

    raw  -> feature_dim * len(freqs)
    gdf  -> feature_dim * len(freqs) * 2   (amplitude blocks + group-delay blocks)
    """
    mult = _REPRESENTATIONS[representation][4]
    return feature_dim * len(freqs) * mult


# ---- HOOK (not yet wired): the encoder seam ------------------------------- #
@runtime_checkable
class MeaningEncoder(Protocol):
    """Seam where the modern perception encoders attach to feed the MEANING sense.

    NOT IMPLEMENTED HERE. The box-side encoders (MobileCLIP for open-vocab vision,
    Depth Anything V2 for a depth channel, emotion2vec for affect, TitaNet for speaker
    identity — see `cutting_edge_oss__UNIFIED.md`) implement `encode()` to turn raw
    perception into the fused embedding that becomes an EmbeddingFrame. We keep ENGRAM
    encoder-agnostic: it fingerprints whatever embedding it is handed.

    Left as a documented hook (the Anki way — define the seam before the part exists).
    """

    def encode(self, perception: PerceptionState) -> np.ndarray:
        """Return a fused embedding [De] for the latest perceived instant."""
        ...


# ---- FUTURE (gated): the COMPOSE layer ------------------------------------ #
# Identity composition — bundling MEANING impressions under labels (self / environment
# / person:X) into one "self-frequency" shape via HRR — lives one layer up and is
# GATED on the capacity experiment (#2 in `frequency_memory__UNIFIED.md`): our
# fingerprints are correlated, so VSA bundling must be measured before we trust it.
# It will land as `compose.py` once that experiment passes. Do not build it before then.
