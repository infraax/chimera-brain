# REFERENCES — repositories, context files & external sources

Canonical index so any next Claude instance can re-create the working context. The sandbox
is **ephemeral** (cloned fresh each session), so `_context_repos/` and `_curation_repos/` do
**not** persist — re-clone them from the URLs below.

Convention used this project:
- **Output repo** = `chimera-brain` (this repo, the only tracked/committed one).
- **Context/curation repos** = cloned into untracked sibling folders `/home/user/_context_repos/`
  and `/home/user/_curation_repos/` so they never enter git.

Egress note: this environment's network policy allow-lists **`infraax/*`** and
**`kercre123/victor`** (these clone fine); other GitHub orgs return **403** until the policy is
broadened (see SESSION_LOG.md).

---

## 1. The four core project repos (infraax — allow-listed, clone OK)

| Repo | URL | Role |
|------|-----|------|
| chimera-brain | https://github.com/infraax/chimera-brain | **Output** — architecture, docs, `vector_engram/`, concepts, curation |
| vectorbrain | https://github.com/infraax/vectorbrain | Runtime cognitive layer (Go + Python) — L1/L2/L3 implementation |
| vectorax | https://github.com/infraax/vectorax | Local RAG over Vector codebase + TRM (34,507 chunks) |
| engram | https://github.com/infraax/engram | KV-cache Fourier-fingerprint memory PoC (basis for `vector_engram`) |

```bash
mkdir -p /home/user/_context_repos && cd /home/user/_context_repos
for r in vectorbrain vectorax engram; do git clone https://github.com/infraax/$r.git; done
```

## 2. Extra context corpus (infraax — allow-listed)

| Repo | URL | Contents |
|------|-----|----------|
| Chimera-extra- | https://github.com/infraax/Chimera-extra-.git | 27 files: VRCM foundations, Deep_Understanding PDF, vectorbrain reports, N.A.P./AEGIS/sovereignty, influence research. Full per-file index + analysis in `CHIMERA_CONVERGENCE_MAP.md`. |

```bash
cd /home/user/_context_repos && git clone https://github.com/infraax/Chimera-extra-.git
```
Key files inside (analysis in CHIMERA_CONVERGENCE_MAP.md): `VRCM*.md`,
`Deep_Understanding (4).pdf` (→ DEEP_UNDERSTANDING_CONCEPT_01.md),
`vectorbrain-*-report.*`, `Eigengram Master Design Document.md`,
`N_A_P_ Track 3*.pdf`, `Research Report.pdf` (N.A.P. Track 5), `AEGIS *.pdf`,
`Physical Anchors *.md`, plus the influence/ethics cluster.
(Empty/irrelevant: `TGCH.pdf` 0 bytes; `Google 3.pdf` = Vatican Nostra Aetate.)

## 3. The Vector source base (kercre123 — allow-listed; LARGE ~1.4 GB)

| Repo | URL | Role |
|------|-----|------|
| victor | https://github.com/kercre123/victor | **Full open-source Anki Vector source** (C++ `engine/`, Go services, `animProcess/`, `coretech/`, `okaoVision/`, `snowboy/`, `cloud/`). Basis of VECTOR_ENG_VICTOR_BASE.md surgery points. |

```bash
cd /home/user/_context_repos && git clone --depth 1 https://github.com/kercre123/victor.git
```
Key paths referenced in our docs: `engine/moodSystem/moodManager.cpp` (5-D emotion),
`engine/aiComponent/behaviorComponent/` (arbitration, `behaviorComponentCloudServer.cpp` = cloud seam),
`engine/receptiveSocialPresenceEstimator/` (proactivity), `animProcess/src/cozmoAnim/micData/` (mics/wake-word),
`3rd/signalEssence` (beamforming/VAD/AEC), `3rd/acapela` (TTS), `okaoVision/` (faces).

## 4. Curation backlog (mostly egress-BLOCKED — need policy; see SESSION_LOG.md)

Clone loop + per-repo plan is in **SESSION_LOG.md**. URLs:
| Repo | URL | Tier |
|------|-----|------|
| ruvnet/RuView | https://github.com/ruvnet/RuView | ⭐ WiFi presence/vital-sign sensing (no camera) |
| markqvist/Reticulum | https://github.com/markqvist/Reticulum | ⭐ LoRa/packet-radio crypto mesh (N.A.P.) |
| avelino/awesome-go | https://github.com/avelino/awesome-go | Go libs (curated → curation/awesome_go_cpp.md) |
| fffaraz/awesome-cpp | https://github.com/fffaraz/awesome-cpp | C/C++ libs (curated → curation/awesome_go_cpp.md) |
| tmrts/go-patterns | https://github.com/tmrts/go-patterns | Go idioms |
| ChristosChristofidis/awesome-deep-learning | https://github.com/ChristosChristofidis/awesome-deep-learning | DL resources |
| ashishpatel26/500-AI-Machine-learning-Deep-learning-Computer-vision-NLP-Projects-with-code | https://github.com/ashishpatel26/500-AI-Machine-learning-Deep-learning-Computer-vision-NLP-Projects-with-code | 500 impls |
| vinta/awesome-python | https://github.com/vinta/awesome-python | Python libs |
| trimstray/the-book-of-secret-knowledge | https://github.com/trimstray/the-book-of-secret-knowledge | tools/security |
| kuchin/awesome-cto | https://github.com/kuchin/awesome-cto | strategy |

## 5. Other external sources referenced in our docs

**Vector community / docs (for ANKI_TEAM_OUTREACH.md):**
- Randall Maas (TRM author) — https://github.com/randym32 · TRM https://randym32.github.io/Vector-TRM.pdf · wiki https://randym32.github.io/Anki.Vector.Documentation
- kercre123 wire-pod — https://github.com/kercre123/wire-pod
- Digital Dream Labs (IP custodian) — https://github.com/digital-dream-labs (repos: `vector`, `vector-cloud`, `vector-go-sdk`, `oskr-owners-manual`)
- Project Victor — https://www.project-victor.org/

**Candidate libraries/models (from VECTOR_ENG_UPGRADE_MAP.md & curation/awesome_go_cpp.md)** — egress-blocked until policy change:
- On-robot C/ML/DSP: ncnn https://github.com/Tencent/ncnn · RNNoise https://github.com/xiph/rnnoise · kissfft https://github.com/mborgerding/kissfft · libfacedetection https://github.com/ShiqiYu/libfacedetection · ETL https://github.com/ETLCPP/etl · concurrentqueue https://github.com/cameron314/concurrentqueue
- Go box services: grpc-go https://github.com/grpc/grpc-go · NATS https://github.com/nats-io/nats-server · Ollama https://github.com/jmorganca/ollama · langchaingo https://github.com/tmc/langchaingo · badger https://github.com/dgraph-io/badger · libp2p https://github.com/libp2p
- Vision/depth/3D (upgrade map): Apple Depth Pro `apple/ml-depth-pro` · FastVLM `apple/ml-fastvlm` · Depth Anything V2 · DUSt3R/MASt3R/VGGT · 3D Gaussian Splatting (verify exact repos when clonable)
- Audio (box): faster-whisper · Moonshine · Kokoro-82M · Piper · Sesame CSM · Silero VAD · DeepFilterNet (verify when clonable)

---

## 6. Tracked deliverables in THIS repo (chimera-brain)
Docs: `CHIMERA_CONVERGENCE_MAP.md`, `Vector-eng.md`, `VECTOR_ENG_VICTOR_BASE.md`,
`VECTOR_ENG_UPGRADE_MAP.md`, `ANKI_WAY.md`, `DEEP_UNDERSTANDING_CONCEPT_01.md`,
`ENGRAM_FOR_VECTOR.md`, `ANKI_TEAM_OUTREACH.md`, `ADR_ENGRAM_INTEGRATION_SEAMS.md`,
`SESSION_LOG.md`, the original `CHIMERA_*` specs.
Code: `vector_engram/` (16 tests pass), `concepts/deep_understanding/three_brain_skeleton.py`.
Curation: `curation/awesome_go_cpp.md`.
Env deps for the Python code: `numpy`, `hnswlib` (`pip install numpy hnswlib`).
