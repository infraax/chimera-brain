# RESEARCH GEODESIC — Cutting-Edge Open-Source Models, Papers & Tools (last ~2 years)
## Find the genius-engineering gems we can use to upgrade/enhance the Vector-Chimera system
## Created: 2026-06-24 · Dexter × Claude Opus 4.8

> **How to use:** hand each *vector* to a research agent / HuggingFace+web tool. Return findings in the
> **Output** format. Bias hard toward **quality of engineering**, not hype or model size.

---

## PRIME DIRECTIVE
> *Survey the last ~24 months of open-source releases (HuggingFace, GitHub, arXiv, company research blogs) —
> from giants (Apple, NVIDIA, Meta, Google/DeepMind, Microsoft) AND small teams / solo developers equally —
> and surface the models, papers, libraries, and tools of genuine **genius-engineering quality** that we can
> use, in any capacity, to upgrade or enhance the Vector-Chimera creature (perception, audio, 3D/mapping,
> on-device ML, memory, robotics learning).*

**The filter (this is the whole point — "the Anki way, not slop"):** Anki had ONE camera and used physics to
take two photos and triangulate depth. They got 1500-fps face tracking and on-device emotion on a phone chip.
That is the bar: *clever, efficient, outside-the-box engineering that delivers high-quality results with
modest resources* — NOT resource-hungry models that burn a GPU to deliver mediocre output. Rank everything by
**cleverness × quality × efficiency**, not by parameter count or press coverage.

---

## CROSS-CUTTING CONSTRAINTS (every vector)
1. **Recency:** prioritize 2024–2026 releases; note exact dates.
2. **Genius-engineering rubric (score each find 1–5 on each):** (a) **cleverness** — does it solve a hard
   problem in a non-obvious, elegant way? (b) **efficiency** — runs on modest hardware / on-device / real-time?
   (c) **quality** — are the results genuinely high-quality, verified, not cherry-picked? (d) **fit** — does it
   serve Vector (edge/ARM, the dock box, perception/audio/3D/memory/robotics)?
3. **Team-agnostic:** a brilliant solo-dev repo outranks a mediocre big-company drop. Surface the small gems.
4. **License + reproducibility:** license (favor MIT/Apache/BSD; flag NC/GPL/AGPL), weights availability,
   does the code actually run, are there real benchmarks.
5. **Edge reality:** note CoreML/MLX/ONNX/TFLite/GGUF availability, quantization, ARM/Apple-silicon/Jetson fit,
   on-robot vs dock-box placement.
6. **Map to us:** end each find with "how this upgrades Vector" (which subsystem in `VECTOR_ENG_UPGRADE_MAP.md`).
7. **Honesty:** flag overhyped/benchmark-gamed releases; call out what *looks* great but isn't reproducible.

---

## RESEARCH VECTORS

### V1 — Apple's quiet high-tech drops (the "they ship genius without noise" angle)
- **Questions:** What has Apple's ML research released open-source in 2024–2026 that's genuinely cutting-edge?
  Investigate the **`apple/` HuggingFace org and `apple/ml-*` GitHub repos**: Depth Pro (sharp metric monocular
  depth), FastVLM (efficient on-device VLM), MobileCLIP, AIMv2, OpenELM, CoreNet, DCLM, the **4M** multimodal
  model, Matryoshka/MobileOne, any 3D/Gaussian-splat or world-model work. The **MLX** framework + `mlx-examples`
  + community MLX model zoo. **The "hidden audio model on every Mac"** — investigate Apple's on-device speech:
  the new `SpeechTranscriber`/`SpeechAnalyzer` (2025), on-device dictation models, the system TTS voices /
  "Personal Voice", and whether any are usable/exportable. CoreML model gallery.
- **Return:** the Apple gems worth using, with CoreML/MLX export status and edge fit. Specifically resolve
  *what the "hidden Mac audio model" actually is* and whether we can use it.

### V2 — NVIDIA: simulated physics worlds for embodied/humanoid training + 3D
- **Questions:** NVIDIA's stack for training/simulating embodied agents in physically-realistic worlds, 2024–26:
  **Isaac Sim / Isaac Lab**, **Isaac GR00T** (humanoid foundation model + GR00T-Dreams), **Cosmos** (world
  foundation models / physical-AI video), **Newton** physics engine (NVIDIA × Google DeepMind × Disney, on
  Warp/MJX), **Warp** (differentiable sim), **nvblox** (real-time 3D reconstruction), **FoundationPose** (6-DoF
  pose), **FoundationStereo**, cuVSLAM. Also NVIDIA audio: **Parakeet**/**Canary** STT (top of HF leaderboards),
  **NeMo**. Which are open/usable for a small robot project (vs datacenter-only)? Could we use the *sim* to
  train Vector behaviors/policies, or the perception models directly?
- **Return:** which NVIDIA tools are realistically usable for us (esp. sim-for-training + the perception/audio
  models that run on a Jetson/box), license/hardware reality.

### V3 — 3D reconstruction, Gaussian splatting & spatial AI (the "mapping by genius" angle)
- **Questions:** Best 2024–26 open-source for turning camera(s) into 3D maps/models on modest hardware:
  **3D Gaussian Splatting** + fast trainers (**gsplat**/nerfstudio, splatting on mobile), feed-forward 3D
  (**DUSt3R / MASt3R / MASt3R-SLAM / VGGT / Fast3R / Spann3R / Spatially-grounded** variants), monocular depth
  (**Depth Anything V2**, **Metric3D v2**, **UniDepth**, Apple **Depth Pro**), segmentation/tracking (**SAM 2**),
  open-vocab detection (**YOLO-World**, **OWLv2**, **Grounding DINO**), point-tracking (**CoTracker / SpaTracker**),
  scene-graph/spatial-LLM (**SpatialLM**, **ConceptGraphs**). Which run real-time on a Jetson/Mac-mini box? Which
  could give Vector a **persistent 3D home map** (the splat/mesh leap)?
- **Return:** a ranked toolkit for Vector's 3D mapping/spatial memory, with hardware/latency + license.

### V4 — On-device audio (STT/TTS/denoise/diarization/VAD) — beyond what we already mapped
- **Questions:** The best *efficient* 2024–26 audio models for an always-on creature: STT (faster-whisper,
  **Moonshine**, NVIDIA **Parakeet/Canary**, Distil-Whisper, Kyutai **STT**), TTS (**Kokoro-82M**, **Piper**,
  **Sesame CSM**, **Orpheus**, **Chatterbox**, Kyutai **TTS/Moshi**), full-duplex/streaming conversation
  (**Moshi**), denoise/AEC (**DeepFilterNet3**, **GTCRN**), VAD (**Silero**), speaker ID/diarization
  (**pyannote**, NeMo **TitaNet**, **3D-Speaker**), audio embeddings (**CLAP**), emotion-from-voice
  (**emotion2vec**). Which are genuinely small/fast/high-quality and license-clean?
- **Return:** the audio shortlist per role (STT/TTS/denoise/VAD/spkr/emotion) with size/latency/license + the
  best "voice" candidate for Vector.

### V5 — Small/efficient vision & VLMs for an edge creature
- **Questions:** Best *tiny but capable* 2024–26 vision: VLMs (**Moondream2**, **SmolVLM2**, **FastVLM**,
  **Florence-2**, Qwen2.5-VL-3B), detection/seg (**YOLO11/v10**, **RT-DETRv2**, **MobileSAM/EdgeSAM**), face
  (modern ArcFace/AdaFace, **InsightFace**), pose/hands (**MediaPipe**, **RTMPose**), emotion/affect models.
  Which beat the OKAO-era stack while running on the box (or even the robot)?
- **Return:** the vision shortlist mapped to Vector's perception upgrades, with edge fit + license.

### V6 — Robotics learning & embodied policies (could Vector learn skills?)
- **Questions:** 2024–26 open embodied-AI: HuggingFace **LeRobot** (datasets, ACT, π0 port), **Physical
  Intelligence π0/π0.5**, **OpenVLA**, **Octo**, **RDT-1B**, **SmolVLA**; physics sims usable by small teams
  (**Genesis**, **MuJoCo/MJX**, **Newton**, Isaac Lab). Are any applicable to Vector's small form (learned
  behaviors, manipulation with future attachments, sim-to-real on a tiny robot)?
- **Return:** what's realistically usable for Vector now vs aspirational, with the simplest entry point.

### V7 — On-device runtimes & compression (how to actually run all this small)
- **Questions:** Best 2024–26 runtimes/quantization for edge: **MLX** (Apple), **llama.cpp/ggml**, **ncnn**,
  **MNN**, **ONNX Runtime**, **ExecuTorch**, **TensorRT/Jetson**, **CoreML**; quantization (GGUF, AWQ, GPTQ,
  int4/int8, **bitnet**), distillation, **Matryoshka** embeddings. What gives the best quality-per-watt on
  ARM/Apple-silicon/Jetson?
- **Return:** the runtime/quantization recommendations per tier (robot vs box).

### V8 — Hidden gems & cross-domain genius (small teams, solo devs, unexpected fields)
- **Questions:** Surface *under-the-radar* high-quality repos/papers a big survey would miss — clever solo/small-team
  work in: efficient SLAM/odometry, event cameras, neuromorphic, ultra-cheap depth tricks (structured light,
  ToF, defocus, single-camera physics like Anki's), audio source localization, sensor fusion, tiny-ML. Also
  cross-domain: astronomy/medical imaging tricks, DSP gems, classic-CV-meets-modern-ML. What's the "took two
  photos with one camera and triangulated" move of 2025?
- **Return:** a curated "hidden gems" list with why each is genius-tier and how it could serve Vector.

---

## OUTPUT — Return Format
```
### V# — <title>
TOP FINDS (ranked):
  - Name — URL (repo/HF/paper) — date — license — size/hardware
    GENIUS SCORE: cleverness _/5 · efficiency _/5 · quality _/5 · fit _/5
    WHAT IT IS (1–2 lines) · WHY IT'S CLEVER · HOW IT UPGRADES VECTOR (which subsystem)
    EDGE FIT: robot / box / cloud · runtime (CoreML/MLX/ONNX/GGUF/…)
HONEST FLAGS: overhyped / not reproducible / license trap.
```
Final synthesis: a single **"adopt now / watch / skip"** table across all vectors, mapped to
`VECTOR_ENG_UPGRADE_MAP.md` subsystems, ranked by genius-score × fit.

---

## SEED SEARCH TERMS
`apple ml-depth-pro` · `apple ml-fastvlm` · `apple MLX examples` · `apple 4M multimodal` · `apple OpenELM` ·
`macOS SpeechAnalyzer SpeechTranscriber on-device 2025` · `nvidia isaac lab gr00t` · `nvidia cosmos world
foundation model` · `newton physics engine mujoco warp` · `gaussian splatting gsplat real-time` ·
`MASt3R-SLAM` · `VGGT visual geometry transformer` · `depth anything v2` · `SAM2 segment anything` ·
`moondream2 smolvlm2` · `kokoro tts` · `sesame csm` · `moshi full duplex speech` · `parakeet canary STT` ·
`deepfilternet3` · `lerobot pi0` · `genesis physics simulator` · `executorch on device` · `ncnn mnn arm` ·
`bitnet 1.58` (with skeptical "reproducible?" follow-ups).

## INTERNAL CONTEXT
Upgrade targets: `VECTOR_ENG_UPGRADE_MAP.md`. Doctrine (genius/efficiency bar): `ANKI_WAY.md`. Prior curation:
`curation/awesome_go_cpp.md`. Hardware facts: `CHIMERA_REVERSE_ENGINEERING.md`.
