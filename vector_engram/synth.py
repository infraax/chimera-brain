"""
vector_engram.synth — realistic perception corpus generator for testing/benchmarking.

NOTE: this generates *data* to exercise the pipeline; the pipeline itself
(fingerprint, format, index, retrieval, recall) is real, not simulated. Each
situation prototype (person, activity, place) has a stable latent signature; we
emit short temporal windows = prototype signature + a smooth trend + per-frame
sensor noise, so retrieval must recover situation identity through real noise.
"""
from __future__ import annotations

import hashlib

import numpy as np

from .state import PerceptionFrame, PerceptionState

# modality dims (D = 64+32+8+6+5 = 115 ; fingerprint dim = D * n_freqs)
CV, CA, CT, CI, CE = 64, 32, 8, 6, 5
D = CV + CA + CT + CI + CE
PEOPLE = ["dexter", "stranger", "kid", "partner"]
ACTIVITIES = ["pet", "talk", "ignore", "pick_up", "show_object", "poke", "play"]
PLACES = ["living_room", "desk", "kitchen", "charger"]


def _seed(key: str) -> int:
    return int.from_bytes(hashlib.sha256(key.encode()).digest()[:8], "little")


def situation_key(person: str, activity: str, place: str) -> str:
    return f"{person}|{activity}|{place}"


def _prototype(key: str) -> tuple[np.ndarray, np.ndarray]:
    """Stable (mean, trend) latent for a situation, [D] each."""
    rng = np.random.default_rng(_seed(key))
    mean = rng.normal(0, 1, size=D)
    trend = rng.normal(0, 0.15, size=D)  # gentle within-window dynamics (drives f1)
    return mean, trend


def make_situation(person: str, activity: str, place: str, *, rng: np.random.Generator,
                   T: int = 8, noise: float = 0.25) -> PerceptionState:
    key = situation_key(person, activity, place)
    mean, trend = _prototype(key)
    st = PerceptionState(person=person, activity=activity, place=place)
    for t in range(T):
        frame = mean + trend * (t - T / 2) + rng.normal(0, noise, size=D)
        st.window.append(PerceptionFrame(
            vision=frame[:CV], audio=frame[CV:CV + CA],
            touch=frame[CV + CA:CV + CA + CT], imu=frame[CV + CA + CT:CV + CA + CT + CI],
            emotion=frame[CV + CA + CT + CI:],
        ))
    return st


def build_corpus(n_prototypes: int, copies: int, *, seed: int = 0, T: int = 8,
                 noise: float = 0.25) -> tuple[list[PerceptionState], list[str]]:
    """Return (states, keys): n_prototypes distinct situations, each repeated `copies`
    times with independent noise. Total = n_prototypes * copies."""
    rng = np.random.default_rng(seed)
    combos = [(p, a, pl) for p in PEOPLE for a in ACTIVITIES for pl in PLACES]
    rng.shuffle(combos)
    if n_prototypes > len(combos):
        # extend space with synthetic ids if more prototypes requested
        combos = combos + [("p%d" % i, "a%d" % i, "l%d" % i) for i in range(n_prototypes - len(combos))]
    combos = combos[:n_prototypes]
    states, keys = [], []
    for (p, a, pl) in combos:
        for _ in range(copies):
            states.append(make_situation(p, a, pl, rng=rng, T=T, noise=noise))
            keys.append(situation_key(p, a, pl))
    return states, keys
