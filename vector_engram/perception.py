"""
vector_engram.perception — perception source + background fingerprint worker (Phase 1C).

Bridges raw perception frames to situational memory:
  PerceptionSource (interface) -> FingerprintWorker (rolling window) -> writer/memory

The real robot provides a PerceptionSource backed by the vision/audio/IMU/emotion
pipelines; here we ship the interface + a Mock source (real loop, mock data) so the
worker is fully testable. `recall_summary` turns retrieved situations into a sentence
the L3/voice layer can use.
"""
from __future__ import annotations

import copy
from typing import Protocol, runtime_checkable

from .state import PerceptionFrame, PerceptionState
from .store import Retrieved


@runtime_checkable
class PerceptionSource(Protocol):
    def next(self) -> tuple[PerceptionFrame, dict] | None:
        """Return (frame, meta) or None when exhausted. meta carries who/what/where
        as currently perceived: {'person','activity','place'}."""
        ...


class FingerprintWorker:
    """Maintains a rolling perception window; emits a situational write every `stride`
    frames (and on metadata change). Synchronous stepping for tests; can be driven by a
    thread in production."""

    def __init__(self, sink, *, window: int = 8, stride: int = 4, robot_id: str = "vector-0"):
        self.sink = sink            # has write_state(PerceptionState)
        self.window = window
        self.stride = stride
        self.robot_id = robot_id
        self._frames: list[PerceptionFrame] = []
        self._meta = {"person": "", "activity": "", "place": ""}
        self._since = 0
        self.emitted = 0

    def push(self, frame: PerceptionFrame, meta: dict) -> int | None:
        changed = any(meta.get(k) != self._meta.get(k) for k in ("person", "activity", "place"))
        self._meta = {k: meta.get(k, "") for k in ("person", "activity", "place")}
        self._frames.append(frame)
        if len(self._frames) > self.window:
            self._frames.pop(0)
        self._since += 1
        ready = len(self._frames) >= 2 and (self._since >= self.stride or changed)
        if ready:
            return self._emit()
        return None

    def _emit(self) -> int:
        st = PerceptionState(window=copy.copy(self._frames), robot_id=self.robot_id, **self._meta)
        label = self.sink.write_state(st)
        self._since = 0
        self.emitted += 1
        return label

    def run(self, source: PerceptionSource, max_frames: int | None = None) -> int:
        n = 0
        while True:
            if max_frames is not None and n >= max_frames:
                break
            nxt = source.next()
            if nxt is None:
                break
            frame, meta = nxt
            self.push(frame, meta)
            n += 1
        return n


def recall_summary(results: list[Retrieved]) -> str:
    """Turn retrieved situations into a one-line, speakable recollection."""
    if not results:
        return "I don't recall a moment like this."
    top = results[0]
    who = top.cert.person or "someone"
    what = top.cert.activity or "something"
    where = f" in the {top.cert.place}" if top.cert.place else ""
    return (f"This feels like {len(results)} past moment(s). "
            f"Closest: {who} {what}{where} (similarity {top.score:.2f}).")


# ---- Mock source for tests (real loop, generated data) --------------------- #
class MockPerceptionSource:
    def __init__(self, script: list[tuple[str, str, str]], *, seed: int = 0,
                 frames_per_scene: int = 8, noise: float = 0.25):
        import numpy as np
        from .synth import make_situation
        self._np = np
        self._make = make_situation
        self._rng = np.random.default_rng(seed)
        self._queue: list[tuple[PerceptionFrame, dict]] = []
        for (p, a, pl) in script:
            st = make_situation(p, a, pl, rng=self._rng, T=frames_per_scene, noise=noise)
            meta = {"person": p, "activity": a, "place": pl}
            for fr in st.window:
                self._queue.append((fr, meta))
        self._i = 0

    def next(self) -> tuple[PerceptionFrame, dict] | None:
        if self._i >= len(self._queue):
            return None
        item = self._queue[self._i]
        self._i += 1
        return item
