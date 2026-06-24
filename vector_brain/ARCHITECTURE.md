# vector_brain — architecture & module design

The **production runtime** for the creature's mind, in the languages it will actually ship
in: **C++ on the robot, Go on the box, Python as the lab/reference.** This is the C++/Go
counterpart to `vector_engram/` (the Python package), which stays the **executable
reference spec** — every C++/Go module is pinned to it by golden vectors.

> Status: **foundation / sketch.** Today this directory holds the design + the Day-1
> contract (`schema/engram.fbs`). Code modules are scaffolded in roadmap order.
> Sources: `research/reports/09_engram_rewrite__1.0_geodesic.md` (language/perf/format),
> `curation/awesome_go_cpp.md` (library picks), `research/reports/unified/cutting_edge_oss__UNIFIED.md`
> (V7 runtimes / encoders), `ANKI_WAY.md` (doctrine), `research/VECTOR_3_HARDWARE_GEODESIC.md`
> (the hardware this eventually runs on).

---

## Principles (the Anki way, applied)
1. **Contract-first.** The FlatBuffers schemas in `schema/` are the seam; commit them before
   writing C++/Go. One `.fbs` → `flatc --cpp --go --python` → three languages in lockstep.
2. **Python is the reference, not the product.** `vector_engram` defines correct behaviour;
   C++/Go are pinned to it by **golden vectors** (≤1e-5 for fingerprints, bit-exact for the
   cert envelope, identical top-1 for retrieval).
3. **Safety partition.** The L1 reflex tier (C++) is independent of the application
   processor — a crashed brain can never drive the creature off a table.
4. **No GC on the robot.** Go's GC jitter is disqualifying in the real-time loop; the robot
   tier is C++-only. cgo (Go↔C++) is used **only** on the box, for batch archive calls.
5. **Graceful degradation.** Every tier has a degraded-but-alive fallback (box down → robot
   reflex still works; model down → circuit-breaker, not a dead creature).
6. **Respect the budget.** Cleverness/efficiency over brute force; ARM-real, NEON-friendly,
   permissively licensed (no GPL in shipping binaries — FFTW excluded).

---

## Tiers × language × IPC

| Component | Language | Tier | IPC / linkage |
|---|---|---|---|
| DSP core (rFFT, GDF, L2) | C++ / PFFFT | robot + box | in-process (linked) |
| ENGRAM reflex (fingerprint + hot ring index) | C++ / ETL | robot | in-process, links into engine |
| VSA / compose (bind/bundle/cleanup) | C++ | box (robot later) | in-process |
| Cert codec (`.eng`) | FlatBuffers (C++/Go/Py) | both | file / mmap |
| Cold archive (USearch) | C++ via cgo | box | cgo from Go |
| Box service / API | Go / gRPC | box | gRPC (external SDK) |
| Robot → box situational stream | CLAD / Cap'n Proto over Unix socket | seam | socket |
| Research / codebook training / golden gen | Python | dev only | — |

Maps to the chimera layers: **L1 Brainstem** = robot reflex (C++) · **L2 Cortex** = box
perception fusion (Go orchestrates, C++/ncnn/ONNX encoders) · **L3 Constructor** = box
LLM/memory (Go + Ollama). The **two-rate ENGRAM** lands as: reflex fingerprint on-robot
(C++ DSP + ETL hot index), meaning fingerprint + COMPOSE on-box.

---

## Module layout

```
vector_brain/
  schema/         FlatBuffers CONTRACT (language-agnostic, committed first)
    engram.fbs        EGRV cert (mirrors vector_engram/format.py v2)         [present]
    perception.fbs    fused perception / situation message                  [next]
    ipc.fbs           robot↔box messages                                    [later]
    golden/           golden-vector fixtures (parity)                       [later]
  core/           C++ compute core — shared robot+box, no GC                [roadmap]
    dsp/              PFFFT fingerprint: rfft, gdf, L2   (← fingerprint.py)
    engram/           cert encode/decode + ETL hot ring index (← format.py/archive.py)
    vsa/              bind/bundle/unbind/cleanup (← vsa.py/compose.py)
    third_party/      PFFFT · ETL · moodycamel · USearch · flatbuffers (vendored/submodule)
    CMakeLists.txt
  robot/          C++ on-robot reflex tier (L1 + engram reflex)            [roadmap]
  box/            Go box tier                                              [roadmap]
    service/          gRPC service (vic-cloud pattern)
    archive/          cgo → USearch cold archive + EGRV writer
    cmd/braind/       the box daemon
  test/           cross-language golden-vector parity harness              [roadmap]
```

---

## Selected libraries (from the reports — see ARCHITECTURE sources)

| Role | Pick | License | Note |
|---|---|---|---|
| Format/codegen | **FlatBuffers** | Apache-2.0 | Anki precedent; `flatc` → C++/Go/Py |
| FFT/DSP | **PFFFT** (+ kissfft fallback) | BSD | NEON; **FFTW excluded (GPL)** |
| Cold ANN (box) | **USearch** | Apache-2.0 | header-only C++, Go bindings, fp16, mmap |
| Hot index (robot) | **ETL ring buffer** | MIT | no-heap exact scan |
| Lock-free queue | **moodycamel concurrentqueue** | BSD/Boost | non-blocking perception→memory |
| No-heap containers | **ETL** | MIT | real-time/safety partition |
| Box RPC/API | **grpc-go** | Apache-2.0 | matches SDK/gateway |
| Box pub/sub (opt.) | **NATS** | Apache-2.0 | service nervous-system |
| Box KV (opt.) | **badger** | Apache-2.0 | profiles / confidence log / metadata |
| Edge/box encoders | **ncnn** (edge) / **ONNX Runtime** (box) | BSD / MIT | feed the MeaningEncoder seam |
| Local LLM (L3) | **Ollama** | MIT | the "Ollama pattern" reference |
| Denoise / ego-noise | **RNNoise** | BSD | the "hear over its motors" trick, 2026 |
| Resilience | **circuit** (Go) | MIT | graceful degradation |

---

## Build & parity
- **C++:** CMake + Docker cross-compile (the victor toolchain), `flatc` as a CMake custom
  command so schema edits regenerate. Sanitizers (ASan/UBSan) in CI; libFuzzer on the cert parser.
- **Go:** `go build` for the service; cgo only for the USearch/PFFFT bridges on the box.
- **Parity:** `vector_engram` generates `schema/golden/` fixtures; C++ (gtest) and Go (`go test`)
  must reproduce them within tolerance. Retrieval recall@1 must stay 1.000 on the soak suite.

---

## Roadmap (dependency-ordered, from report 09 V10)
- **P0 — foundation (now):** `schema/engram.fbs` committed; this doc. *(done)*
- **P1 — format freeze:** `flatc` C++/Go/Python stubs from `engram.fbs`; a Python `vector_engram`
  EGRV-v2 ⇄ FlatBuffers migration + round-trip golden test (bit-exact).
- **P2 — C++ DSP core:** `core/dsp` fingerprint (PFFFT), GDF; golden parity ≤1e-5; ARM cross-compile.
- **P3 — C++ on-robot reflex:** `core/engram` ETL hot ring + moodycamel queue + mmap cert reader.
- **P4 — Go box service:** `box/service` gRPC + `box/archive` cgo→USearch + EGRV writer.
- **P5 — integration:** robot fingerprint → box archive → query end-to-end; soak parity.

First concrete step after this foundation: **P1 — run `flatc` against `engram.fbs` and add the
round-trip golden test in `vector_engram`** (no robot needed; it locks the contract).
