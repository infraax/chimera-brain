# SESSION LOG & NEXT-SESSION HANDOFF

Running log for the Vector-Eng / Chimera multi-repo work.
Branch: `claude/multi-repo-architecture-npf6jv`

---

## NEXT SESSION — START HERE  ▶ Curate the awesome-list backlog

**Prerequisite (must happen first):** the session's egress policy currently **blocks
`git clone` of external GitHub orgs** (returns 403). Earlier clones worked only because
`infraax/*` and `kercre123/victor` are allow-listed. To do the work below you must first:
1. Edit the **environment's network policy** (Claude Code on the web → environment settings →
   network/egress) to allow github.com (or allowlist the orgs listed below), and
2. **Start a fresh session** (the new policy may only apply to a new session/environment).

**Task:** clone all 10 repos (shallow) into the **untracked** sibling folder
`/home/user/_curation_repos/` (same pattern as `_context_repos/`, never committed), then
curate each into `chimera-brain/curation/` mapped to our roadmap.

```bash
mkdir -p /home/user/_curation_repos && cd /home/user/_curation_repos
for r in \
  tmrts/go-patterns \
  ChristosChristofidis/awesome-deep-learning \
  ashishpatel26/500-AI-Machine-learning-Deep-learning-Computer-vision-NLP-Projects-with-code \
  kuchin/awesome-cto \
  fffaraz/awesome-cpp \
  ruvnet/RuView \
  avelino/awesome-go \
  trimstray/the-book-of-secret-knowledge \
  vinta/awesome-python \
  markqvist/Reticulum ; do
  git clone --depth 1 "https://github.com/$r.git" "$(basename "$r")"
done
```

**The 10 repos + how to handle each (priority order):**

| # | Repo | What it is | Relevance | How to curate |
|---|------|-----------|-----------|---------------|
| 1 ⭐ | ruvnet/RuView | WiFi-signal sensing → presence / vital-signs / spatial intel, **no camera** | HIGH — Vector's camera-less "knows you're in the room" proactivity + attunement | **Code repo** — read core src; assess hardware needs + whether usable on the box |
| 2 ⭐ | markqvist/Reticulum | LoRa/packet-radio/WiFi crypto networking stack (Python) | HIGH — N.A.P. out-of-band mesh + sovereignty/resilient comms | **Code repo** — read API/architecture; fit as N.A.P. transport |
| 3 | avelino/awesome-go | Go libs list | MED-HIGH — Go custom-cloud + vic-* services | **List** — full sweep, extend `curation/awesome_go_cpp.md` |
| 4 | fffaraz/awesome-cpp | C/C++ libs list | MED-HIGH — C++ engine + on-robot ENGRAM/DSP/ML | **List** — full sweep, extend `curation/awesome_go_cpp.md` |
| 5 | tmrts/go-patterns | Go design patterns | MED — idioms for the cloud/services code | **Small code/list** — extract patterns we'll use |
| 6 | ChristosChristofidis/awesome-deep-learning | DL resources list | MED — model mining (perception/TTS/STT/depth) | **List** — filter to on-device/edge models |
| 7 | ashishpatel26/500-AI-...-Projects-with-code | 500 AI/ML/CV/NLP projects | MED — concrete impls to borrow | **List** — filter to perception/TTS/STT/depth/3D |
| 8 | vinta/awesome-python | Python libs list | MED — box-side Python (ENGRAM/DU stack) | **List** — filter to ML/audio/vector-db/serial |
| 9 | trimstray/the-book-of-secret-knowledge | tools/cheatsheets/security | LOW-MED — AEGIS/security + ops tooling | **List** — skim for security/edge/ops |
| 10 | kuchin/awesome-cto | CTO/startup strategy | LOW — project/strategy | **List** — skim, optional |

**Curation method (per the awesome lists):** lists are huge; the web summarizer truncates,
so with full local clones do real `grep`/read of the README, extract entries by our
categories (memory/retrieval · on-device STT/TTS · depth/3D/Gaussian-splat/SLAM · perception ·
embedded/NEON · Go/C++ libs · agent/LLM · LoRa/mesh), note licenses (favor MIT/Apache; flag
GPL/non-commercial), and append to `curation/`. Produce one `curation/<name>.md` per source
plus a top-picks roll-up.

**Already curated (don't repeat — just deepen with full clones):**
`curation/awesome_go_cpp.md` — web-extracted picks from awesome-go & awesome-cpp
(ncnn, RNNoise, kissfft, libfacedetection, ETL, concurrentqueue, Cap'n Proto, FAISS;
grpc-go, NATS, Ollama/langchaingo, badger, libp2p, arpc). Has a top-10 list.

**After curation, resume the build** (see Open Threads below): wire `vector_engram` into the
Deep-Understanding skeleton's `MemoryStore` seam, and/or do the ADR "contract-first" do-now list.

---

## TODAY — 2026-06-23

### Done
- **ENGRAM for Vector — ALL phases implemented & tested end-to-end** (real code, no sims):
  - `vector_engram/` package (numpy + hnswlib). Phase 1A decouple (`StateVector`/
    `PerceptionState`, situational Fourier fingerprint, EGRV `.eng` codec, ANN index, store).
  - Phase 1B hardening: `HotIndex` ring buffer + `HotColdMemory` spill, `StreamingEngramWriter`
    (non-blocking, load-shedding), `ConfidenceLog` (IndexC), `soak.py`.
  - Phase 1C: `PerceptionSource` + `FingerprintWorker` + `recall_summary`.
  - Phase 2: metadata filters + training-free `SituationClassifier`.
  - **Verified: 16/16 tests pass.** Soak 50k: dropped=0, hot bounded@1000, post-soak
    recall@1=1.000, merged query ~347µs p50, ~2.1k situations/sec (≫ 10–30 fps). Found+fixed
    a real streaming concurrency race via the soak. See `vector_engram/{CHANGELOG,VERIFICATION}.md`.
- **ADR_ENGRAM_INTEGRATION_SEAMS.md** — decided **contract-first** for C/Go integration
  (freeze EGRV ABI + golden vectors + versioned CLAD/proto schemas + thin service boundary;
  defer all actual C/Go/FFI/NEON until robot integration). "Do-now" list pending.
- **curation/awesome_go_cpp.md** — web curation of awesome-go & awesome-cpp (clone blocked).
- Confirmed `git clone` of the 10 backlog repos is **egress-blocked (403)**; web channel works.

### Earlier in this branch (prior turns today)
- Convergence map, Vector-eng framework, Victor-base integration map (5 surgical edits),
  upgrade map (per-subsystem 2026 swaps), ANKI_WAY doctrine, Deep-Understanding Concept 01 +
  runnable `concepts/deep_understanding/three_brain_skeleton.py`, ENGRAM-for-Vector plan,
  Anki team outreach map.

### Where things live
- **Tracked (this repo):** all `*.md` docs, `vector_engram/` (16 tests green),
  `concepts/deep_understanding/`, `curation/`.
- **Untracked siblings (never committed):** `/home/user/_context_repos/` (vectorbrain,
  vectorax, engram, Chimera-extra-, victor) · `/home/user/_curation_repos/` (empty — pending
  network policy).
- **Env deps installed this session:** numpy 2.4.6, hnswlib (for vector_engram tests/bench).

---

## OPEN THREADS / PARKED DECISIONS
1. **Next build step (user's plan):** finish ENGRAM ✅ → then **Deep Understanding**: wire
   `vector_engram.SituationMemory` into the three-brain skeleton's `MemoryStore` seam and test
   them together. (User: "slowly moving to deep understanding, testing them together.")
2. **ADR contract-first "do-now" list** (optional, cheap): `FORMAT.md` ABI spec + golden
   `.eng`/fingerprint vectors + versioned CLAD/proto schemas + thin `service.py` boundary.
3. **Curation backlog** (this handoff) — needs network policy first.
4. **Network policy** — user to edit env settings (can't be done from inside the session);
   likely requires a fresh session to take effect.
5. Deep code reads still wanted once clonable: **RuView, Reticulum, go-patterns**.

---
