"""
vector_engram — Vector adaptation of the ENGRAM mechanism.

Continuous *situational* memory for the Anki Vector robot: fuse perception into a
short time window, Fourier-fingerprint it (DC + 1st harmonic), store as a compact
.eng certificate, retrieve nearest past situations via ANN — training-free,
corpus-independent, µs-class retrieval.

See ENGRAM_FOR_VECTOR.md (plan), CHANGELOG.md (what changed), VERIFICATION.md (how to test).
"""
from .fingerprint import cosine, fingerprint
from .format import SituationCert, decode, encode
from .index import SituationIndex
from .state import PerceptionFrame, PerceptionState, RawState, StateVector
from .store import Retrieved, SituationMemory
from .archive import HotColdMemory, HotIndex, HotColdStats
from .streaming import StreamingEngramWriter, WriterStats
from .confidence import ConfidenceLog
from .perception import FingerprintWorker, MockPerceptionSource, PerceptionSource, recall_summary
from .query import SituationClassifier, filter_retrieved

__version__ = "0.2.0"

__all__ = [
    "fingerprint", "cosine",
    "SituationCert", "encode", "decode",
    "SituationIndex",
    "StateVector", "RawState", "PerceptionState", "PerceptionFrame",
    "SituationMemory", "Retrieved",
    # phase 1B
    "HotIndex", "HotColdMemory", "HotColdStats",
    "StreamingEngramWriter", "WriterStats", "ConfidenceLog",
    # phase 1C
    "FingerprintWorker", "PerceptionSource", "MockPerceptionSource", "recall_summary",
    # phase 2
    "SituationClassifier", "filter_retrieved",
    "__version__",
]
