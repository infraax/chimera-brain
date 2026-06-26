#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# chimera-brain — Cloud sandbox SETUP SCRIPT
#
# Paste the CONTENTS of this file into the environment's "Setup script" field
# (Claude Code on the web -> edit environment -> Setup script). It runs ONCE as
# root on a fresh container, and the result is cached as a snapshot, so every
# future session starts with the full toolchain already present — no more
# reinstalling C++/Go/Python deps mid-task.
#
# Constraints the platform enforces on setup scripts:
#   * runs as root on Ubuntu 24.04, before Claude Code starts
#   * must finish in < 5 min
#   * re-runs only when this script changes, the network policy changes, or the
#     ~7-day snapshot expires
#
# Non-critical steps end with `|| true` so a single hiccup never aborts the
# whole snapshot build. Everything here only needs the DEFAULT "Trusted"
# network policy (apt archives + pypi + go proxy are all on the default
# allow-list); none of it needs Full/Custom egress.
# ---------------------------------------------------------------------------
set -uo pipefail
echo "=== chimera-brain setup: begin ==="

# --- 1. System / C++ tier (vector_brain robot + box contract) -------------
# flatc + headers  -> EGRV cert schema (schema/engram.fbs) cross-lang codegen
# capnp + headers  -> chosen control-plane IPC
# spdlog + fmt     -> C++ logging (spdlog's bundled fmt needs -lfmt at link)
# build-essential  -> g++/make for the contract round-trip + future C++ nodes
export DEBIAN_FRONTEND=noninteractive
apt-get update -y || true
apt-get install -y --no-install-recommends \
  build-essential pkg-config cmake git curl ca-certificates \
  flatbuffers-compiler libflatbuffers-dev \
  capnproto libcapnp-dev \
  libspdlog-dev libfmt-dev \
  || true

# --- 2. Go tier (box services) --------------------------------------------
# Go is preinstalled at /usr/local/go in this image; only install if absent.
if ! command -v go >/dev/null 2>&1; then
  echo "Go not found — installing the apt golang package as a fallback."
  apt-get install -y --no-install-recommends golang-go || true
fi

# --- 3. Python tier (vector_engram reference + tests) ---------------------
# Pinned to what the package actually imports. usearch/hnswlib are the ANN
# backends; flatbuffers is the cross-language cert codec.
python3 -m pip install --upgrade pip || true
python3 -m pip install --upgrade \
  numpy pytest flatbuffers usearch hnswlib \
  || true

# --- 4. Verify (prints versions; never fails the snapshot) ----------------
echo "--- versions ---"
command -v go     >/dev/null 2>&1 && go version              || echo "go: MISSING"
command -v flatc  >/dev/null 2>&1 && flatc --version         || echo "flatc: MISSING"
command -v capnp  >/dev/null 2>&1 && capnp --version         || echo "capnp: MISSING"
python3 - <<'PY' || true
mods = ["numpy", "pytest", "flatbuffers", "usearch", "hnswlib"]
for m in mods:
    try:
        mod = __import__(m)
        print(f"py {m}: {getattr(mod, '__version__', 'ok')}")
    except Exception as e:
        print(f"py {m}: MISSING ({e})")
PY
echo "=== chimera-brain setup: done ==="
