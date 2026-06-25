"""Write one EGRV MemoryStore using the flatc-generated Python code -> egram.bin.

Half of the cross-language contract test: Python writes, C++ reads (read_cert.cpp).
Proves the `schema/engram.fbs` contract is identical across languages — the premise of
the FlatBuffers selection (see curation/vector_brain_stack.md §3).
"""
import flatbuffers
import numpy as np

from VectorBrain.Engram import MemoryStore, Precision, Sense, SituationCert

b = flatbuffers.Builder(0)
repr_ = b.CreateString("rfft.embed.v1")
person = b.CreateString("dexter")
data = np.arange(1, 9, dtype=np.uint8).tobytes()          # stand-in fp16 vector bytes
dvec = b.CreateByteVector(data)

SituationCert.Start(b)
SituationCert.AddTimestampUs(b, 123456789)
SituationCert.AddSense(b, Sense.Sense.Meaning)
SituationCert.AddReprId(b, repr_)
SituationCert.AddDim(b, 4)
SituationCert.AddPrecision(b, Precision.Precision.F16)
SituationCert.AddData(b, dvec)
SituationCert.AddPerson(b, person)
cert = SituationCert.End(b)

MemoryStore.StartCertsVector(b, 1)
b.PrependUOffsetTRelative(cert)
certs = b.EndVector()
MemoryStore.Start(b)
MemoryStore.AddVersion(b, 2)
MemoryStore.AddCerts(b, certs)
store = MemoryStore.End(b)
b.Finish(store, b"EGRV")                                   # file_identifier

open("egram.bin", "wb").write(bytes(b.Output()))
print("python wrote egram.bin: person=dexter sense=Meaning repr=rfft.embed.v1 dim=4 data=1..8")
