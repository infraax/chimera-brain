"""
vector_engram.compose — weaving a self (the COMPOSE pillar).

This is the layer the user's vision points at: Vector's "system prompt" should not be a
text file but an ENGRAM shape — many remembered moments woven, under a label, into ONE
big frequency the creature calls "self". And not only self: "environment", "person:dexter",
"place:desk" are each their own labelled shape. Recognition then becomes resonance — *does
this moment belong to me / my world / this person?* — a single dot-product against a shape.

Built on the binding algebra (`vsa.py`) and on the Phase-4 gate result (`CAPACITY_RESULTS.md`):
  • project each impression to a higher-D space (~2048) so bundles have VSA-grade capacity
    (the gate measured 8 → 32 recoverable members from this projection alone),
  • bind each member to a distinct role-key and bundle — with a hierarchy of leaves
    (≤ leaf_cap members each, default 24, safely under the measured 32),
  • keep an item-memory for cleanup so woven members can be enumerated back.

Two faculties, intentionally separated:
  • RESONANCE / belonging — cheap, unbounded: cos(projected moment, the identity's centroid).
    "Is this part of me?" This is the everyday faculty.
  • RECALL of members — capacity-bounded: unbind by role + cleanup. "What am I made of?"
    Used for inspection / sleep-consolidation, not every tick.

Creature naming returns here (weave / belong / recall), over the canonical algebra below.
"""
from __future__ import annotations

import hashlib

import numpy as np

from .vsa import RandomProjection, bind, bundle, cleanup, normalize, unbind

DIM_HI = 2048      # projected identity space (Phase-4: gives capacity ~32 @ ≥0.9)
LEAF_CAP = 24      # members per leaf bundle (safety margin under the measured 32)


def _key(name: str, dim: int, *, base_seed: int = 0) -> np.ndarray:
    """A deterministic random unit vector for a name (a label or a role/slot)."""
    h = int.from_bytes(hashlib.sha256(f"{base_seed}|{name}".encode()).digest()[:8], "little")
    return normalize(np.random.default_rng(h).normal(size=dim))


class Identity:
    """One labelled shape the creature recognises — "self", "environment", "person:dexter".

    Holds the moments woven into it as a single fixed-width frequency (`shape()`), answers
    belonging by resonance (`resonance()`), and can enumerate its members (`recall_members()`,
    capacity-bounded). Grows over time as the creature lives (`weave()`) — the self is not
    fixed, it accretes.
    """

    def __init__(self, label: str, projection: RandomProjection, *,
                 leaf_cap: int = LEAF_CAP, base_seed: int = 0):
        self.label = label
        self.proj = projection
        self.dim = projection.out_dim
        self.leaf_cap = leaf_cap
        self.base_seed = base_seed
        self.label_key = _key(f"label:{label}", self.dim, base_seed=base_seed)
        self._members: list[np.ndarray] = []   # projected+normalized members (cleanup memory)
        self._roles: list[np.ndarray] = []     # a distinct role-key per member slot
        self._centroid = np.zeros(self.dim)    # running sum of projected members (for resonance)
        self._leaves: list[list[int]] = [[]]   # capacity-bounded leaves (member indices)
        self._enum: list[np.ndarray] = [np.zeros(self.dim)]  # per-leaf Σ role⊛member (for recall)

    def weave(self, impression: np.ndarray) -> int:
        """Weave a moment into this identity (the self grows). Returns the member index."""
        p = normalize(self.proj.project(impression))
        idx = len(self._members)
        role = _key(f"{self.label}:slot:{idx}", self.dim, base_seed=self.base_seed)
        self._members.append(p)
        self._roles.append(role)
        self._centroid += p
        if len(self._leaves[-1]) >= self.leaf_cap:        # roll into a fresh leaf when full
            self._leaves.append([])
            self._enum.append(np.zeros(self.dim))
        self._leaves[-1].append(idx)
        self._enum[-1] = self._enum[-1] + bind(role, p)
        return idx

    def shape(self) -> np.ndarray:
        """The labelled self-frequency: one fixed-width vector = label_key ⊛ centroid.
        Binding with the label key puts each identity in its own rotated subspace, so many
        identities can be bundled into one big 'self' shape without colliding."""
        return bind(self.label_key, normalize(self._centroid)).astype(np.float32)

    def resonance(self, impression: np.ndarray) -> float:
        """Belonging by resonance: cos(projected moment, the identity's centroid).
        "Does this moment belong to / resemble me?" Cheap, unbounded — the everyday faculty."""
        if not self._members:
            return 0.0
        p = normalize(self.proj.project(impression))
        return float(np.dot(p, normalize(self._centroid)))

    def recall_members(self) -> list[tuple[int, int, bool]]:
        """Enumerate woven members via unbind + cleanup (capacity-bounded, per leaf).
        Returns (member_idx, recovered_idx, correct) per member. Used for inspection /
        consolidation, not every tick."""
        if not self._members:
            return []
        cb = np.stack(self._members)
        out: list[tuple[int, int, bool]] = []
        for leaf, enum in zip(self._leaves, self._enum):
            b = normalize(enum)
            for idx in leaf:
                rec = cleanup(unbind(b, self._roles[idx]), cb)
                out.append((idx, rec, idx == rec))
        return out

    def recall_accuracy(self) -> float:
        rec = self.recall_members()
        return float(np.mean([c for _, _, c in rec])) if rec else 0.0

    def __len__(self) -> int:
        return len(self._members)


class SelfModel:
    """The creature's set of labelled identities — and the one big shape labelled 'self'.

    This is the "ENGRAM file tree composed into one frequency" idea: every identity
    (self / environment / person:X / place:X) is a shape; `self_shape()` weaves them all
    into a single personality frequency. All identities share ONE projection so their
    shapes are comparable and bundleable.

    Feed it MEANING impressions (identity lives in the recognised/semantic sense — see the
    two-rate design); a moment is woven into a label, and recognition asks which identity it
    resonates with.
    """

    def __init__(self, in_dim: int, *, dim_hi: int = DIM_HI, leaf_cap: int = LEAF_CAP,
                 seed: int = 0):
        self.proj = RandomProjection(in_dim, dim_hi, seed=seed)
        self.dim_hi = dim_hi
        self.leaf_cap = leaf_cap
        self.seed = seed
        self.identities: dict[str, Identity] = {}

    def identity(self, label: str) -> Identity:
        if label not in self.identities:
            self.identities[label] = Identity(label, self.proj, leaf_cap=self.leaf_cap,
                                              base_seed=self.seed)
        return self.identities[label]

    def weave(self, label: str, impression: np.ndarray) -> int:
        """Weave a moment into the identity called `label` (creating it if new)."""
        return self.identity(label).weave(impression)

    def resonances(self, impression: np.ndarray) -> dict[str, float]:
        """How strongly this moment belongs to each known identity."""
        return {lbl: idn.resonance(impression) for lbl, idn in self.identities.items()}

    def recognize(self, impression: np.ndarray) -> str | None:
        """Which identity does this moment most belong to? ('this is dexter', 'this is home')"""
        r = self.resonances(impression)
        return max(r, key=r.get) if r else None

    def self_shape(self) -> np.ndarray | None:
        """The whole personality woven into ONE shape labelled 'self' — the living
        self-frequency. A single fixed-width vector summarising every identity."""
        if not self.identities:
            return None
        return bundle([idn.shape() for idn in self.identities.values()]).astype(np.float32)

    def shape_resonance(self, label: str, impression: np.ndarray) -> float:
        """Query the single composed self-shape *by label*: does this moment belong under
        `label`, read straight off the one big frequency? (the 'clever search over the
        composed shape' — recovers membership without touching the per-identity centroid)."""
        shp = self.self_shape()
        if shp is None or label not in self.identities:
            return 0.0
        p = normalize(self.proj.project(impression))
        probe = bind(self.identities[label].label_key, p)
        return float(np.dot(normalize(probe), normalize(shp)))

    def __len__(self) -> int:
        return len(self.identities)


# ---- FUTURE (hook): consolidation / the "sleep" pass ----------------------- #
# A periodic pass that prunes redundant members, merges near-duplicate identities, and
# re-bundles leaves to keep each identity sharp as it accretes — the report's "sleep
# compilation" / EIGENGRAM identity-stability tracking. Left as a documented seam; build
# once we have lived data to consolidate over.
