"""
vector_engram — Vector adaptation of the ENGRAM mechanism.

Continuous *situational* memory for the Anki Vector robot: fuse perception into a
short time window, Fourier-fingerprint it (DC + 1st harmonic), store as a compact
.eng certificate, retrieve nearest past situations via ANN — training-free,
corpus-independent, µs-class retrieval.

See ENGRAM_FOR_VECTOR.md (plan), CHANGELOG.md (what changed), VERIFICATION.md (how to test).
"""
from .fingerprint import cosine, fingerprint, fingerprint_gdf
from .format import SituationCert, decode, encode
from .index import SituationIndex
from .state import PerceptionFrame, PerceptionState, RawState, StateVector
from .sense import (EmbeddingFrame, MeaningEncoder, MeaningState, Sense,
                    fingerprint_dim, impression_for, meaning_impression,
                    meaning_impression_gdf, reflex_impression, reflex_impression_gdf)
from .resonance import resonate, softmax
from .vsa import (RandomProjection, bind, bundle, cleanup, normalize,
                  pairwise_cosine_stats, random_vectors, unbind)
from .compose import Identity, SelfModel
from .store import Retrieved, SituationMemory, TwofoldMemory
from .archive import HotColdMemory, HotIndex, HotColdStats
from .streaming import StreamingEngramWriter, WriterStats
from .confidence import ConfidenceLog
from .perception import FingerprintWorker, MockPerceptionSource, PerceptionSource, recall_summary
from .query import SituationClassifier, filter_retrieved

__version__ = "0.7.0"

__all__ = [
    "fingerprint", "fingerprint_gdf", "cosine",
    "SituationCert", "encode", "decode",
    "SituationIndex",
    "StateVector", "RawState", "PerceptionState", "PerceptionFrame",
    "SituationMemory", "Retrieved",
    # phase 1 (two-rate hybrid — the two senses)
    "Sense", "EmbeddingFrame", "MeaningState", "MeaningEncoder",
    "reflex_impression", "meaning_impression", "TwofoldMemory",
    # phase 2 (the GDF phase complement)
    "reflex_impression_gdf", "meaning_impression_gdf", "impression_for", "fingerprint_dim",
    # phase 3 (recall by resonance — Modern Hopfield)
    "resonate", "softmax",
    # phase 4 (VSA substrate + the capacity gate)
    "bind", "unbind", "bundle", "cleanup", "normalize", "random_vectors",
    "RandomProjection", "pairwise_cosine_stats",
    # phase 5 (COMPOSE — weaving a self)
    "Identity", "SelfModel",
    # phase 1B
    "HotIndex", "HotColdMemory", "HotColdStats",
    "StreamingEngramWriter", "WriterStats", "ConfidenceLog",
    # phase 1C
    "FingerprintWorker", "PerceptionSource", "MockPerceptionSource", "recall_summary",
    # phase 2
    "SituationClassifier", "filter_retrieved",
    "__version__",
]
