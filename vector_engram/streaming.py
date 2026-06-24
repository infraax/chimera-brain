"""
vector_engram.streaming — non-blocking continuous writes (Phase 1B).

The perception loop must never block on indexing/IO. StreamingEngramWriter buffers
incoming situations in a bounded queue and flushes them on a background thread.
Bounded queue = automatic load-shedding (drop oldest) under back-pressure, which is
the Anki-Way "degrade, never stall" behavior.

The sink is anything with `write_state(PerceptionState) -> int` (SituationMemory or
HotColdMemory).
"""
from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass


@dataclass
class WriterStats:
    enqueued: int
    flushed: int
    dropped: int
    pending: int


class StreamingEngramWriter:
    def __init__(self, sink, *, max_pending: int = 4096, flush_interval_s: float = 0.05,
                 batch: int = 256):
        self.sink = sink
        self._buf: deque = deque()
        self._max = max_pending
        self._interval = flush_interval_s
        self._batch = batch
        self._lock = threading.Lock()          # guards the buffer
        self._drain_lock = threading.Lock()    # serializes sink writes (single-consumer invariant)
        self._enq = 0
        self._flushed = 0
        self._dropped = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._started = False

    def start(self) -> "StreamingEngramWriter":
        if not self._started:
            self._thread.start()
            self._started = True
        return self

    def write(self, state) -> None:
        """Non-blocking. Drops oldest pending if the buffer is full (load-shedding)."""
        with self._lock:
            if len(self._buf) >= self._max:
                self._buf.popleft()
                self._dropped += 1
            self._buf.append(state)
            self._enq += 1

    def _drain_batch(self) -> int:
        # serialize all consumers so the (non-thread-safe) sink only ever sees one writer
        with self._drain_lock:
            with self._lock:
                n = min(self._batch, len(self._buf))
                items = [self._buf.popleft() for _ in range(n)]
            for st in items:
                self.sink.write_state(st)
            self._flushed += len(items)
            return len(items)

    def _loop(self) -> None:
        while not self._stop.is_set():
            if self._drain_batch() == 0:
                time.sleep(self._interval)

    def flush(self) -> None:
        """Synchronously drain everything currently buffered."""
        while True:
            with self._lock:
                empty = not self._buf
            if empty:
                break
            self._drain_batch()

    def close(self, timeout: float = 5.0) -> None:
        # stop the background consumer first, then drain the remainder single-threaded
        self._stop.set()
        if self._started:
            self._thread.join(timeout=timeout)
        self.flush()

    def stats(self) -> WriterStats:
        with self._lock:
            pending = len(self._buf)
        return WriterStats(enqueued=self._enq, flushed=self._flushed,
                           dropped=self._dropped, pending=pending)

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc):
        self.close()
