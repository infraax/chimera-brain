#!/usr/bin/env bash
# Cross-language contract round-trip: flatc codegen -> Python writes -> C++ reads & asserts.
# Proves schema/engram.fbs is identical across Python and C++ (the FlatBuffers premise).
#
# Requires: flatc, python3 + flatbuffers, g++ (C++17), libflatbuffers-dev.
#   apt-get install -y flatbuffers-compiler libflatbuffers-dev ; pip install flatbuffers
set -euo pipefail
cd "$(dirname "$0")"
SCHEMA=../../schema/engram.fbs

echo "[1/4] flatc codegen (C++ + Python) from $SCHEMA"
flatc --cpp --python "$SCHEMA"

echo "[2/4] Python writes egram.bin"
python3 write_cert.py

echo "[3/4] g++ builds the reader"
g++ -std=c++17 -I. read_cert.cpp -o read_cert

echo "[4/4] C++ reads & asserts"
./read_cert
