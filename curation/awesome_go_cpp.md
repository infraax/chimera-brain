# CURATION — awesome-go & awesome-cpp (for Vector-Eng)

Curated from web-extracted entries of the two lists, filtered to **our actual build**:
the Go custom-cloud/services layer on the box, and the C++ engine + on-robot ENGRAM/DSP/ML.

> **Method & honesty:** `git clone` of these external orgs is blocked by the session's
> egress policy (403), so this was extracted via web fetch of the raw READMEs. Both lists
> are *enormous* and the fetch summarizer only surfaces slices, so this captures
> **confirmed-present, high-relevance** entries — not the complete lists. A full sweep
> needs the repos allow-listed for cloning. Everything below was returned as *present* in
> the list (not guessed); license/fit notes are my assessment.

Legend: ⭐ = standout pick for us · ⚠ = caveat (license/weight/ARM fit)

---

## A. C++ — engine + on-robot (ARM Cortex-A7)

### A1. On-device neural inference (vision/audio model upgrades)
| Lib | URL | Fit for us |
|---|---|---|
| ⭐ **ncnn** (Tencent) | https://github.com/Tencent/ncnn | ARM/mobile-optimized inference — the **prime candidate for running upgraded vision/audio models on the robot** (NEON, no-dep, tiny). |
| **ONNX Runtime** | https://github.com/microsoft/onnxruntime | Broad model support incl. ARM; heavier than ncnn — better on the **box** than the APQ8009. |
| **tiny-dnn** | https://github.com/tiny-dnn/tiny-dnn | Header-only, dependency-free — handy for a tiny custom net on-device. |
| ⚠ **TensorFlow / TFLite** | https://github.com/tensorflow/tensorflow | What Vector already uses (TFLite); keep for continuity, but ncnn likely faster on ARM. |
| **flashlight** | https://github.com/facebookresearch/flashlight | Fast C++ ML; box-side, heavy. |

### A2. Computer vision
| Lib | URL | Fit |
|---|---|---|
| **OpenCV** | https://github.com/Itseez/opencv | **Already in Vector's pipeline** — keep; basis for any classical CV we add. |
| ⭐ **libfacedetection** | https://github.com/ShiqiYu/libfacedetection | Ultra-fast on-device face *detection* — a modern, free replacement/complement to the OKAO detector. |
| **Dlib** | https://github.com/davisking/dlib | Face landmarks/embeddings + ML utils — option for the face-identity upgrade. |

### A3. Audio / DSP / FFT  (upgrade the Signal-Essence-locked pipeline + ENGRAM on-robot)
| Lib | URL | Fit |
|---|---|---|
| ⭐ **kissfft** | https://github.com/mborgerding/kissfft | Tiny, simple FFT — **ideal for the on-robot ENGRAM C/NEON fingerprint path** (the DC+f1 transform) and cheap spectral features. |
| ⭐ **RNNoise** (Xiph) | https://github.com/xiph/rnnoise | Neural denoise — a modern, open upgrade to the mic noise-reduction / self-cancellation (the "hear over its own motors" Anki trick, 2026 edition). |
| **Speex / speexdsp** | http://www.speex.org/ | Classic AEC + resampler + VAD — open building blocks if we partially replace Signal Essence. |
| **Opus** | http://opus-codec.org/ | Low-latency audio codec — for streaming audio box↔robot. |
| **libsndfile** | https://github.com/erikd/libsndfile/ | Audio file IO (assets, logging, test fixtures). |
| ⚠ **FFTW** | http://www.fftw.org/ | Fastest FFT but **GPL** — avoid in a permissively-licensed shipping binary; use kissfft/KFR instead. |
| **KFR** | https://www.kfrlib.com/ | Modern C++ DSP (FFT, FIR/IIR, sample-rate conversion) — good for box-side audio. |

### A4. Serialization / IPC (box↔robot + inter-service)
| Lib | URL | Fit |
|---|---|---|
| ⭐ **Cap'n Proto** | https://github.com/capnproto/capnproto | Zero-copy serialization + capability RPC — strong candidate for the box↔robot contract (cf. ADR; alongside/again st CLAD). |
| **Apache Thrift** | https://thrift.apache.org/ | Cross-language IPC/RPC — another contract option. |
| **nanomsg** | https://github.com/nanomsg/nanomsg | Scalability protocols (pub/sub, pipeline) — lightweight inter-process messaging on the robot/box. |

### A5. Concurrency (real-time-safe)
| Lib | URL | Fit |
|---|---|---|
| ⭐ **concurrentqueue** | https://github.com/cameron314/concurrentqueue | Lock-free MPMC queue — the **C++ analog of our StreamingEngramWriter buffer** (non-blocking perception→memory). |
| **BS::thread_pool** | https://github.com/bshoshany/thread-pool | Tiny C++17 pool for background fingerprinting/IO. |
| ⚠ **Intel TBB** | https://www.threadingbuildingblocks.org/ | Powerful but heavy for the APQ8009; box-side. |

### A6. JSON & embedded utilities
| Lib | URL | Fit |
|---|---|---|
| **nlohmann/json** | https://github.com/nlohmann/json | Ergonomic config/JSON (Vector configs are JSON). |
| **RapidJSON** / **simdjson** | https://github.com/miloyip/rapidjson · https://github.com/lemire/simdjson | Fast parse when throughput matters. |
| ⭐ **ETL (Embedded Template Library)** | https://github.com/ETLCPP/etl | **No-heap, fixed-size containers** — exactly right for the real-time engine/syscon partition (deterministic, no malloc). |
| **Abseil** / **Boost** | https://github.com/abseil/abseil-cpp · https://github.com/boostorg | General utilities (use sparingly on ARM). |

### A7. Vector search / ANN
| Lib | URL | Fit |
|---|---|---|
| ⚠ **FAISS** | https://github.com/facebookresearch/faiss | What ENGRAM uses; **heavy for ARM** — box-side archive only. For the on-robot hot index our exact ring-buffer (already built) or a tiny ANN is better. (hnswlib not confirmed in-list but is our Python choice.) |

---

## B. Go — custom cloud server + box services

### B1. RPC / transport (the custom cloud replacing vic-cloud)
| Lib | URL | Fit |
|---|---|---|
| ⭐ **grpc-go** | https://github.com/grpc/grpc-go | Vector's SDK/gateway already speak gRPC — the natural base for our custom cloud server. |
| **Kitex** (CloudWeGo) | https://github.com/cloudwego/kitex | High-perf RPC if we outgrow plain gRPC. |
| ⭐ **arpc** | https://github.com/lesismal/arpc | **Two-way calling + broadcast** — interesting for the bidirectional box↔robot situational stream. |
| **gorpc** / **jsonrpc** | https://github.com/valyala/gorpc · https://github.com/osamingo/jsonrpc | Simpler RPC options. |

### B2. Messaging / pub-sub (the box-side "nervous system" between services)
| Lib | URL | Fit |
|---|---|---|
| ⭐ **NATS** | https://github.com/nats-io/nats-server | Lightweight pub/sub to wire perception ↔ ENGRAM ↔ brain services on the box cleanly (decoupled, observable). |
| **liftbridge** | https://github.com/liftbridge-io/liftbridge | Durable streams over NATS (event log of situations). |
| **mochi mqtt** | https://github.com/mochi-co/mqtt | Embedded MQTT broker — local IoT/home integration. |
| **emitter-io** | https://github.com/emitter-io/emitter | MQTT + WebSocket pub/sub. |

### B3. LLM / ML orchestration (L3 / Deep Understanding on the box, in Go)
| Lib | URL | Fit |
|---|---|---|
| ⭐ **Ollama** | https://github.com/jmorganca/ollama | Local LLM runtime — already our plan for the dual-model brain. |
| **LocalAI** | https://github.com/mudler/LocalAI | OpenAI-compatible self-host — alt/มcomplement to Ollama. |
| **langchaingo** | https://github.com/tmc/langchaingo | If the Go cloud server orchestrates the LLM/tools directly. |

### B4. Audio I/O (box side, Go)
| Lib | URL | Fit |
|---|---|---|
| **PortAudio** | https://github.com/gordonklaus/portaudio | Cross-platform audio I/O bindings. |
| **malgo** / **Oto** / **beep** | https://github.com/gen2brain/malgo · https://github.com/hajimehoshi/oto · https://github.com/gopxl/beep | Lightweight playback/capture for the box. |

### B5. Embedded KV (cloud-server state: metadata, IndexC, profiles)
| Lib | URL | Fit |
|---|---|---|
| ⭐ **badger** | https://github.com/dgraph-io/badger | Fast embedded KV — per-person profiles, confidence log, situation metadata sidecars. |
| **bbolt** | https://github.com/etcd-io/bbolt | Simple, rock-solid B+tree KV. |
| **buntdb** | https://github.com/tidwall/buntdb | In-memory KV with persistence + spatial/TTL indexes. |

### B6. Config / logging / resilience
| Lib | URL | Fit |
|---|---|---|
| **viper** / **koanf** | https://github.com/spf13/viper · https://github.com/knadh/koanf | Config for the services. |
| **circuit** | https://github.com/schigh/circuit | Circuit breaker — graceful degradation when a service/model is down (Anki-Way). |

### B7. Distributed / mesh (N.A.P. multi-node, sovereignty layer)
| Lib | URL | Fit |
|---|---|---|
| ⭐ **libp2p** | https://github.com/libp2p | P2P networking stack — candidate substrate for the N.A.P. multi-node archive/mesh (pairs with the Reticulum idea for out-of-band). |

---

## C. Top picks to actually pull next (when allow-listed)
Ranked by leverage for the current roadmap:
1. ⭐ **ncnn** — on-robot neural inference (vision/audio upgrades).
2. ⭐ **RNNoise** — modern open mic-denoise / self-cancellation.
3. ⭐ **kissfft** — the on-robot ENGRAM C/NEON fingerprint transform.
4. ⭐ **NATS** — box-side service nervous system.
5. ⭐ **Ollama** (already planned) + **langchaingo** — Go-side brain orchestration.
6. ⭐ **ETL** + **concurrentqueue** — real-time-safe C++ building blocks (incl. the C++ streaming-writer analog).
7. ⭐ **libfacedetection** / **Dlib** — face upgrade beyond OKAO.
8. ⭐ **badger** — Go cloud-server state store.
9. ⭐ **Cap'n Proto** — box↔robot serialization/contract candidate (with the ADR).
10. ⭐ **libp2p** — N.A.P. mesh substrate.

> Next: to get the *complete* lists (and the 3 code repos — RuView, Reticulum, go-patterns)
> we need those GitHub orgs allow-listed for cloning; then I can grep the full trees and
> deepen this with versions, license files, and ARM build notes.
