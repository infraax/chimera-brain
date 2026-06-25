// Read the Python-written egram.bin using the flatc-generated C++ header, and assert the
// fields match what write_cert.py wrote. Other half of the cross-language contract test.
//   build: flatc --cpp ../../schema/engram.fbs && g++ -std=c++17 read_cert.cpp -o read_cert
#include "engram_generated.h"
#include <fstream>
#include <iostream>
#include <vector>

using namespace VectorBrain::Engram;

int main() {
  std::ifstream f("egram.bin", std::ios::binary);
  std::vector<char> buf((std::istreambuf_iterator<char>(f)), {});
  if (!MemoryStoreBufferHasIdentifier(buf.data())) { std::cerr << "FAIL: bad EGRV identifier\n"; return 1; }
  auto store = GetMemoryStore(buf.data());
  auto cert = store->certs()->Get(0);

  bool ok = store->version() == 2
         && cert->person()->str() == "dexter"
         && cert->sense() == Sense_Meaning
         && cert->repr_id()->str() == "rfft.embed.v1"
         && cert->dim() == 4
         && cert->timestamp_us() == 123456789ULL
         && cert->data()->size() == 8
         && cert->data()->Get(0) == 1 && cert->data()->Get(7) == 8;

  std::cout << "C++ read: version=" << store->version()
            << " person=" << cert->person()->str()
            << " sense=" << EnumNameSense(cert->sense())
            << " repr=" << cert->repr_id()->str()
            << " dim=" << cert->dim()
            << " data[0],[7]=" << (int)cert->data()->Get(0) << "," << (int)cert->data()->Get(7) << "\n";
  std::cout << (ok ? "PASS: cross-language contract round-trips\n" : "FAIL: field mismatch\n");
  return ok ? 0 : 1;
}
