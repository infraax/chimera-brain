"""
vector_engram.format — the EGRV (.eng) situational certificate codec.

Vector adaptation of the EIGENGRAM binary format (`engram/kvcos/engram/format.py`,
"EGR1"). We keep the spirit (compact, self-contained, fp16 vector, little-endian)
and add the embodied/lifelong metadata flagged as "format v1.3" in
ENGRAM_FOR_VECTOR.md: robot_id, timestamp, activity, place, person, emotion[4].

Layout (little-endian):
  magic        4   b"EGRV"
  version      1   uint8 (=2)
  dim          2   uint16   (length of the fingerprint vector)
  n_freqs      1   uint8    (freqs used, informational)
  sense        1   uint8    (Sense: 0=REFLEX, 1=MEANING)              [v2+]
  timestamp    8   float64  (unix seconds)
  emotion     16   4x float32 (valence-ish summary: first 4 emotion dims)
  --- variable, each str = uint16 length + utf-8 bytes ---
  repr_id,                                                            [v2+]
  robot_id, source_id, person, activity, place, situation_key
  --- vector ---
  vec        dim*2  float16

Versioning (the envelope/payload split):
  The *envelope* above is stable. The fingerprint *payload* may evolve; `repr_id`
  names which representation produced `vec` ("rfft.raw.v1", "rfft.embed.v1", later
  "scatter.*"…), so a new representation joins without a format break. `decode` still
  reads legacy v1 certs (no sense/repr_id) — they are treated as REFLEX / "rfft.raw.v1".
  This hand-rolled forward-compat is the bridge until EGRV moves to FlatBuffers
  (see 09_engram_rewrite__1.0_geodesic.md, V5) for true cross-language codegen.
"""
from __future__ import annotations

import struct
import time
from dataclasses import dataclass, field

import numpy as np

MAGIC = b"EGRV"
VERSION = 2          # current writer version
LEGACY_VERSIONS = (1,)  # versions decode still accepts


@dataclass
class SituationCert:
    vec: np.ndarray                      # float32 fingerprint [dim]
    robot_id: str = "vector-0"
    source_id: str = "vector_perception"
    person: str = ""
    activity: str = ""
    place: str = ""
    situation_key: str = ""
    emotion: np.ndarray = field(default_factory=lambda: np.zeros(4, np.float32))
    timestamp: float = field(default_factory=time.time)
    n_freqs: int = 2
    # v2: which sense formed this trace + which representation produced `vec`.
    # Defaults make a bare SituationCert(vec=…) a legacy-equivalent REFLEX trace.
    sense: int = 0                       # Sense.REFLEX
    repr_id: str = "rfft.raw.v1"


def _put_str(buf: bytearray, s: str) -> None:
    b = s.encode("utf-8")
    if len(b) > 0xFFFF:
        raise ValueError("string too long for uint16 length")
    buf += struct.pack("<H", len(b))
    buf += b


def _get_str(data: bytes, off: int) -> tuple[str, int]:
    (n,) = struct.unpack_from("<H", data, off)
    off += 2
    s = data[off : off + n].decode("utf-8")
    return s, off + n


def encode(cert: SituationCert) -> bytes:
    vec = np.asarray(cert.vec, dtype=np.float16)
    emo = np.asarray(cert.emotion, dtype=np.float32).ravel()
    emo4 = np.zeros(4, dtype=np.float32)
    emo4[: min(4, emo.shape[0])] = emo[:4]

    buf = bytearray()
    buf += MAGIC
    buf += struct.pack("<B", VERSION)
    buf += struct.pack("<H", int(vec.shape[0]))
    buf += struct.pack("<B", int(cert.n_freqs))
    buf += struct.pack("<B", int(cert.sense))              # v2
    buf += struct.pack("<d", float(cert.timestamp))
    buf += struct.pack("<4f", *emo4.tolist())
    _put_str(buf, cert.repr_id)                            # v2 (first string)
    for s in (cert.robot_id, cert.source_id, cert.person, cert.activity, cert.place, cert.situation_key):
        _put_str(buf, s)
    buf += vec.tobytes()  # fp16
    return bytes(buf)


def decode(data: bytes) -> SituationCert:
    if data[:4] != MAGIC:
        raise ValueError("bad magic; not an EGRV certificate")
    off = 4
    (version,) = struct.unpack_from("<B", data, off); off += 1
    if version != VERSION and version not in LEGACY_VERSIONS:
        raise ValueError(f"unsupported EGRV version {version}")
    (dim,) = struct.unpack_from("<H", data, off); off += 2
    (n_freqs,) = struct.unpack_from("<B", data, off); off += 1
    # v2 inserts `sense` here; v1 had no such field.
    if version >= 2:
        (sense,) = struct.unpack_from("<B", data, off); off += 1
    else:
        sense = 0  # legacy traces are REFLEX
    (ts,) = struct.unpack_from("<d", data, off); off += 8
    emo4 = np.array(struct.unpack_from("<4f", data, off), dtype=np.float32); off += 16
    if version >= 2:
        repr_id, off = _get_str(data, off)
    else:
        repr_id = "rfft.raw.v1"  # legacy default representation
    robot_id, off = _get_str(data, off)
    source_id, off = _get_str(data, off)
    person, off = _get_str(data, off)
    activity, off = _get_str(data, off)
    place, off = _get_str(data, off)
    situation_key, off = _get_str(data, off)
    vec = np.frombuffer(data, dtype=np.float16, count=dim, offset=off).astype(np.float32)
    return SituationCert(
        vec=vec, robot_id=robot_id, source_id=source_id, person=person,
        activity=activity, place=place, situation_key=situation_key,
        emotion=emo4, timestamp=ts, n_freqs=n_freqs, sense=sense, repr_id=repr_id,
    )
