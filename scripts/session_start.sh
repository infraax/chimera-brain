#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# chimera-brain — SessionStart hook (safety net, NOT the primary installer)
#
# Wired in .claude/settings.json. Runs every time Claude Code launches in this
# repo (fresh OR resumed). The Setup script (scripts/setup_env.sh) is the real
# installer and runs from a cached snapshot; this hook only repairs the rare
# case where the snapshot is cold or a package is missing, so a resumed session
# is never blindsided. It is idempotent and fast: if the toolchain is already
# present it does almost nothing and returns immediately.
#
# CLAUDE_CODE_REMOTE=true in the cloud sandbox; locally this is a near no-op.
# ---------------------------------------------------------------------------
set -uo pipefail

need_apt=0
for bin in flatc capnp g++; do
  command -v "$bin" >/dev/null 2>&1 || need_apt=1
done

if [ "$need_apt" = "1" ] && command -v apt-get >/dev/null 2>&1; then
  echo "[session_start] C++ toolchain incomplete — restoring via apt."
  export DEBIAN_FRONTEND=noninteractive
  apt-get install -y --no-install-recommends \
    build-essential flatbuffers-compiler libflatbuffers-dev \
    capnproto libcapnp-dev libspdlog-dev libfmt-dev >/dev/null 2>&1 || true
fi

# Python deps the engram tests import.
python3 - <<'PY' >/dev/null 2>&1 || python3 -m pip install --quiet numpy pytest flatbuffers usearch hnswlib >/dev/null 2>&1 || true
import numpy, pytest, flatbuffers, usearch, hnswlib  # noqa: F401
PY

exit 0
