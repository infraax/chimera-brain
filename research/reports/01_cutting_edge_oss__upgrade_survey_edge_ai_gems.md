# Vector-Chimera Upgrade Survey: Genius-Engineering Gems (2024–2026)

## TL;DR

- **Adopt now:** Apple **Depth Pro** + **FastVLM** (CoreML/MLX, on-device), **Moondream2 / SmolVLM2** for tiny-VLM perception, **Kokoro-82M** TTS + **Moonshine / Parakeet** STT + **Silero VAD** + **DeepFilterNet/GTCRN** denoise for the audio loop, **SAM2/EdgeSAM + a non-AGPL detector** for perception, and the **MASt3R-SLAM / VGGT** feed-forward-3D family + **gsplat** for a persistent 3D home map. All are real, reproducible, license-checkable, and edge-deployable.
- **The genius bar is hit by small teams as often as giants:** Moondream (lean training budget), Kokoro-82M (one developer, Apache-2.0, #1 on the TTS Spaces Arena), Moonshine (variable-length encoder), GTCRN (denoise at tens-of-thousands of params), and the DUSt3R→MASt3R→VGGT feed-forward-3D lineage are the truest “Anki-way” gems — clever architecture beating brute force.
- **Watch / skip:** NVIDIA **GR00T, Isaac Lab, Cosmos** and **π0/SmolVLA** are genuinely open but built for arms/humanoids and datacenter-or-Jetson-Thor-scale training — useful as a sim/training pipeline, not as on-robot brains for a desk creature. The **Genesis** simulator’s headline speed claim was independently debunked (see V6). Apple’s new on-device speech model is excellent but **platform-locked and non-exportable**.

## Key Findings

1. **Apple is quietly the best edge-ML vendor for Vector.** Depth Pro gives sharp **metric** depth from a single uncalibrated image in <1s; FastVLM’s FastViTHD encoder, per Apple’s own HF card, “outperforms LLaVA-OneVision-0.5B with **85× faster Time-to-First-Token (TTFT) and 3.4× smaller vision encoder**” (the Qwen2-7B variant gets 7.9× faster TTFT). Both ship Apple-silicon/CoreML/MLX checkpoints. A Dec-2025 drop, **ml-sharp**, does feed-forward Gaussian-splat 3D in <1s.
1. **The “hidden Mac audio model” is real, now API-exposed — and not portable.** Apple’s **SpeechAnalyzer/SpeechTranscriber** (WWDC June 10 2025; iOS 26 / macOS Tahoe) is a new on-device STT model. Hands-on tests by MacStories’ John Voorhees found it “tore through the 7GB video file a full **2.2× faster than MacWhisper’s Large V3 Turbo** model, with no noticeable difference in transcription quality” (0:45 vs 1:41). But it lives “outside your app’s memory space,” auto-updates via the OS, and is reachable only through the Speech framework on Apple OSes 26+ — usable if Vector’s dock box runs macOS 26+, never liftable onto a Jetson/ARM-Linux robot.
1. **On-device audio is now a complete, mostly-clean-license stack** spanning STT (Moonshine, Parakeet, Kyutai STT), TTS (Kokoro, Chatterbox, Kyutai TTS), denoise (DeepFilterNet, GTCRN), VAD (Silero), emotion (emotion2vec), and full-duplex conversation (Moshi).
1. **Feed-forward 3D reconstruction is the breakout category** — DUSt3R/MASt3R/VGGT and MASt3R-SLAM turn uncalibrated cameras into dense 3D in one forward pass: the closest 2025 analogue to Anki’s “two photos, triangulate” cleverness.
1. **Robotics foundation models (π0, SmolVLA, GR00T) are open but mostly aspirational for a tiny creature** — they target manipulation arms and humanoids and need GPU fine-tuning; LeRobot is the realistic entry point if Vector ever gets an actuated attachment.

## Details

### V1 — Apple’s quiet high-tech open-source drops

TOP FINDS (ranked):

- **Depth Pro** — github.com/apple/ml-depth-pro / arXiv 2410.02073 — Oct 2024, ICLR 2025 — Apple sample-code/weights license — ViT-based, <1s.
  GENIUS SCORE: cleverness 5/5 · efficiency 4/5 · quality 5/5 · fit 5/5
  WHAT IT IS: Sharp, zero-shot **metric** monocular depth at high resolution, with absolute scale even without camera intrinsics.
  WHY IT’S CLEVER: Outputs depth in real meters from one uncalibrated image in <1s — most monocular depth is scale-ambiguous.
  HOW IT UPGRADES VECTOR: Metric obstacle / edge-of-table sense from the single existing camera — the Anki “physics from one camera” spirit. EDGE FIT: box / quantized robot · CoreML (community conversions).
- **FastVLM** — github.com/apple/ml-fastvlm / HF apple/FastVLM — CVPR 2025, HF Sep 3 2025 — Apple ML research license — 0.5B/1.5B/7B; MLX checkpoints.
  GENIUS SCORE: cleverness 5/5 · efficiency 5/5 · quality 4/5 · fit 5/5
  WHAT IT IS: Mobile VLM with a hybrid CNN+Transformer FastViTHD encoder; “85× faster TTFT and 3.4× smaller vision encoder” vs LLaVA-OneVision-0.5B; runs in-browser on Apple Silicon.
  WHY IT’S CLEVER: Attacks the real bottleneck — vision-token count and high-res encoding latency — not just LLM size.
  HOW IT UPGRADES VECTOR: Real-time scene captioning / visual Q&A; 0.5B variant gives Vector “what am I looking at” narration. EDGE FIT: robot (0.5B) / box · MLX, CoreML-exportable.
- **ml-sharp** — github.com/apple/ml-sharp / arXiv 2512.10685 — Dec 2025 — repo LICENSE/LICENSE_MODEL — CUDA GPU needed for real-time viz.
  GENIUS SCORE: cleverness 5/5 · efficiency 3/5 · quality 4/5 · fit 3/5 — feed-forward 3D Gaussians in one <1s pass vs slow, inconsistent diffusion. Could bootstrap a 3D model of Vector’s surroundings on the box.
- **MobileCLIP/MobileCLIP2, AIMv2, OpenELM, DCLM, 4M, MobileOne** — Apple HF org — 2024–2025 — Apple licenses. MobileCLIP2 is the image encoder feeding FastVLM and a tiny open-vocab embedding backbone for Vector’s memory/retrieval.
- **MLX framework + mlx-examples + mlx-community zoo** — Apple’s Apple-Silicon array framework (unified memory + Neural Engine); the substrate for running the above on the box. Community servers macMLX (Apache 2.0) and vllm-mlx exist.

**The hidden Mac audio model — resolved:** the new **SpeechAnalyzer** class + **SpeechTranscriber** module (WWDC June 2025; iOS 26/macOS Tahoe) power Notes, Voice Memos, Journal and system dictation; ~2.2× faster than Whisper Large V3 Turbo with no quality loss. A `DictationTranscriber` exposes the older on-device model without Siri toggles. **Critical caveat: not exportable** — Apple-platform-only, no watchOS.

HONEST FLAGS: Apple research licenses are permissive-for-research but not classic OSI MIT/Apache — verify commercial terms per repo. Depth Pro is not metric-perfect on every surface. SpeechAnalyzer is platform lock-in, not a portable model.

### V2 — NVIDIA simulated physics worlds & perception

TOP FINDS (ranked):

- **Isaac ROS perception (nvblox, cuVSLAM/PyCuVSLAM, FoundationStereo, FoundationPose)** — developer.nvidia.com/isaac + NVIDIA-ISAAC-ROS GitHub — 2024–2025 — open code, NVIDIA licenses — Jetson/CUDA.
  GENIUS SCORE: cleverness 4/5 · efficiency 4/5 · quality 5/5 · fit 4/5 (only if Vector’s box is a Jetson)
  WHAT IT IS: nvblox (real-time 3D reconstruction ~100× faster than CPU), cuVSLAM (sub-1% trajectory-error stereo-visual SLAM, now Python via PyCuVSLAM), FoundationStereo (zero-shot stereo depth, CVPR 2025 best-paper nominee, 1M+ synthetic training pairs), FoundationPose (6-DoF pose for novel objects).
  HOW IT UPGRADES VECTOR: If the dock box is a Jetson Orin, a turnkey persistent-map + localization + object-pose stack. EDGE FIT: box/robot (Jetson) · TensorRT/CUDA.
- **Isaac GR00T N1/N1.5/N1.7** — github.com/NVIDIA/Isaac-GR00T / arXiv 2503.14734 — Mar–Jun 2025 — open weights, permissive — 2B/3B. Dual-system (VLM “thinker” + diffusion-transformer “actor”) **humanoid** manipulation model; GR00T-Dreams/Mimic synthetic flywheel generated 780k trajectories in 11h. Architecture inspiration only for Vector. GENIUS: 4/2/4/2.
- **Isaac Lab + Newton physics** (NVIDIA × Google DeepMind × Disney, on Warp/MJX) — Mar 2025 — open — GPU sim; MuJoCo-Warp claims >70× ML-workload speedup. Could train small expressive behaviors in sim then sim-to-real, but heavy setup. GENIUS: 4/3/4/2. Cloud/workstation only.
- **Parakeet/Canary STT (NeMo)** — see V4; Parakeet TDT 0.6B (~3GB, CPU-capable) is the genuinely usable NVIDIA piece.

HONEST FLAGS: GR00T/Cosmos/Isaac Lab are real and open but datacenter-or-Jetson-Thor scale. Cosmos world-foundation-models are video-generation-heavy, not on-robot.

### V3 — 3D reconstruction, Gaussian splatting & spatial AI

TOP FINDS (ranked):

- **VGGT (Visual Geometry Grounded Transformer)** — CVPR 2025 (Wang et al., Meta/Oxford VGG) — open code.
  GENIUS SCORE: cleverness 5/5 · efficiency 4/5 · quality 5/5 · fit 4/5
  WHAT IT IS: One transformer ingests N uncalibrated images and outputs full 3D geometry (poses, depth, point maps) in a single pass.
  WHY IT’S CLEVER: Replaces the entire classical SfM/MVS pipeline with one network; a fast-moving ecosystem (FastVGGT, LiteVGGT, VGGT-SLAM, streaming O(1) variants) is hardening it for edge.
  HOW IT UPGRADES VECTOR: Turns Vector’s roaming frames into a 3D home map for spatial memory. EDGE FIT: box (GPU) · PyTorch.
- **MASt3R-SLAM** — CVPR 2025 (Murai, Dexheimer, Davison) — open.
  GENIUS SCORE: cleverness 5/5 · efficiency 4/5 · quality 5/5 · fit 4/5
  WHAT IT IS: Real-time dense SLAM built on DUSt3R/MASt3R feed-forward 3D priors, no calibration required. A live, persistent, metric home map from one moving camera — the spatial-memory backbone. EDGE FIT: box (GPU) · PyTorch.
- **gsplat (nerfstudio)** — github.com/nerfstudio-project/gsplat / JMLR 2025 — **Apache 2.0** — CUDA; up to 4× less training memory and ~15% faster than reference 3DGS.
  GENIUS SCORE: cleverness 4/5 · efficiency 5/5 · quality 5/5 · fit 4/5 — the de-facto open 3DGS trainer/renderer; builds a photoreal home model Vector can localize within. EDGE FIT: box (CUDA), web/edge renderers (HiGS).
- **Depth Anything V2 / Video Depth Anything** — github.com/DepthAnything — 2024–2025 — open (verify per size); Core ML + Transformers integration.
  GENIUS SCORE: cleverness 4/5 · efficiency 5/5 · quality 5/5 · fit 5/5 — lightweight always-on depth on the robot; pair fast-relative DA-V2 with sharp-metric Depth Pro. EDGE FIT: robot/box · CoreML/ONNX.
- **UniDepth V2** — arXiv 2502.20110 — Feb 2025 — open — universal monocular **metric** depth with a clever self-promptable camera module (predicts intrinsics) + uncertainty output. GENIUS: 5/4/4/4.
- **SAM 2** — github.com/facebookresearch/segment-anything-2 / arXiv 2408.00714 — 2024 — **Apache 2.0** (SA-V dataset CC-BY) — streaming-memory video segmentation (FIFO memory bank for temporal mask propagation); pair with detector prompts (Det-SAM2). EdgeSAM/MobileSAM/PicoSAM2 for the robot tier. GENIUS: 5/3/5/4.

HONEST FLAGS: VGGT/MASt3R-SLAM want a GPU for real-time; raw VGGT is memory-hungry on long sequences (hence the efficiency forks). Dense feed-forward 3D is not yet real-time on a Pi.

### V4 — On-device audio (STT / TTS / denoise / diarization / VAD / emotion)

TOP FINDS by role:

- **STT — Moonshine** (github.com/moonshine-ai/moonshine) — v2 streaming Feb 2026 — **English models MIT; non-English = Moonshine Community License (non-commercial)** — 27M–245M params.
  GENIUS SCORE: cleverness 5/5 · efficiency 5/5 · quality 4/5 · fit 5/5
  WHY IT’S CLEVER: Variable-length encoder eliminates Whisper’s fixed 30s zero-padding, so compute scales with actual speech length, plus encoder/decoder state caching for streaming. Official README: “Moonshine Medium Streaming | 6.65% [WER] | 245 million | 107ms” on a MacBook Pro vs “Whisper Large v3 | 7.44% | 1.5 billion | 11,286ms”; runs at 802ms on a Raspberry Pi 5 (Whisper Large V3 can’t run on a Pi at all).
  HOW IT UPGRADES VECTOR: The always-listening ear — real-time wake/command transcription on robot or box. EDGE FIT: robot/box · ONNX, CPU-first.
- **STT — NVIDIA Parakeet TDT 0.6B** (NeMo / HF) — 2025 — open — ~3GB, CPU-capable, RTFx >2000 on GPU; CoreML build FluidInference/parakeet-tdt-0.6b-v3-coreml (**Apache 2.0**; the v2 CoreML weights are CC-BY-4.0 — check per model). Best when the box has a GPU, or via FluidAudio on Apple Silicon (~110× RTF on M4 Pro).
- **STT — Kyutai STT (stt-1b-en_fr / stt-2.6b-en)** — HF kyutai, github.com/kyutai-labs/delayed-streams-modeling — June 17 2025 — **CC-BY 4.0** — 1B model: 0.5s delay + semantic VAD; MLX variant tested on an iPhone 16 Pro. Streaming; commercial OK with attribution.
- **TTS — Kokoro-82M** (HF hexgrad/Kokoro-82M) — v1.0 Jan 27 2025 — **Apache 2.0** — 82M params, <2GB VRAM, CPU real-time; CoreML on Apple Neural Engine ~45ms.
  GENIUS SCORE: cleverness 5/5 · efficiency 5/5 · quality 5/5 · fit 5/5
  WHY IT’S CLEVER: Per the HF card, “Kokoro v0.19 was the #1🥇 ranked model in TTS Spaces Arena,” beating XTTS v2 (467M) and MetaVoice (1.2B) while “trained on <100 hours of audio” at 82M params — and it’s Apache-2.0 and deployed in many commercial APIs (<$1/M chars). The anti-slop poster child.
  HOW IT UPGRADES VECTOR: **The best default voice for Vector** — small, fast, license-clean, ANE-friendly. EDGE FIT: robot/box · CoreML/ONNX/CPU. NOTE: only `hexgrad/Kokoro-82M` is genuine — kokorottsai[.]com and similar are scam clones.
- **TTS — Chatterbox (Resemble AI)** — github.com/resemble-ai/chatterbox — May 2025; Turbo + Multilingual v3 June 2026 — **MIT** — 0.5B (Turbo 350M); vendor-reported sub-200ms / RTF ~0.5 on an RTX 4090; CUDA/ROCm/Apple-MPS. Good zero-shot voice cloning if Vector needs a custom voice. Mandatory PerTh watermark on outputs (provenance, not a usage restriction).
- **TTS — Kyutai TTS 1.6B** (actually ~1.8B params) — HF kyutai/tts-1.6b-en_fr — July 3 2025 — **CC-BY 4.0** — streaming ~200ms, MLX with 4/8-bit quant for Apple Silicon. Kyutai also shipped “Pocket TTS” (Jan 2026) for CPU-only voice cloning.
- **Full-duplex — Moshi** (kyutai-labs/moshi, arXiv 2410.00037) — Sep 18 2024 — **CC-BY 4.0** (card says “research only”) — ~7B + Mimi codec (1.1kbps); ~160–200ms latency on an L4; MLX int4 for Mac. Aspirational for a tiny robot but the reference for natural turn-taking.
- **Denoise — GTCRN** (ICASSP 2024) + **DeepFilterNet 2/3** — real-time full-band speech enhancement on embedded CPUs. **GTCRN is the genius pick: competitive enhancement at tens of thousands of parameters.**
- **VAD — Silero VAD** (github.com/snakers4/silero-vad) — 2024 — **MIT** — tiny ONNX, CPU real-time, hysteresis thresholds; the standard gate before STT.
- **Speaker/diarization — pyannote.audio / NeMo TitaNet / 3D-Speaker; FluidAudio on Apple.** pyannote is heavier (GPU helps); Silero/NeMo lighter.
- **Emotion — emotion2vec / emotion2vec+** (github.com/ddlBoJack/emotion2vec) — 2024, ACL 2024 — open — ~19M params, 9-class SER, “Whisper for emotion.” GENIUS: 5/5/4/5 — directly revives Vector’s emotional-response loop from voice tone.

HONEST FLAGS: Moonshine non-English is non-commercial; Moshi card says research-only despite CC-BY weights; Kyutai “1.6B” TTS = 1.8B params; Chatterbox latency/quality numbers are vendor benchmarks; FluidAudio is Apache-2.0 but per-model weight licenses vary (CC-BY vs Apache).

### V5 — Small/efficient vision & VLMs

TOP FINDS (ranked):

- **Moondream2** (HF vikhyatk/moondream2) — ongoing 2024–2025 — open — ~1.86B params, ~1.2GB quantized, runs on a Raspberry Pi.
  GENIUS SCORE: cleverness 5/5 · efficiency 5/5 · quality 4/5 · fit 5/5
  WHY IT’S CLEVER: “Top-left” philosophy — max intelligence per compute. Per moondream.ai, the new 9B MoE (2B active/token) is “Trained on ~450B tokens with reinforcement learning across 55+ vision-language tasks” (vs Qwen2.5-VL’s ~18T-token pretraining), the 2B dense workhorse has “over 5 million monthly downloads on HuggingFace,” and the int4 variant gives “42% memory reduction with only a 0.6% accuracy drop” — plus genuine zero-shot detection, rare in tiny VLMs.
  HOW IT UPGRADES VECTOR: On-robot/box visual Q&A, captioning, and detection — the modern replacement for the OKAO-era vision stack. EDGE FIT: robot (quantized) / box · ONNX/llama.cpp.
- **SmolVLM2** (HF, arXiv 2504.05299) — 2025 — **Apache 2.0** — 256M/500M/2.2B; RAM-efficient by design (argues RAM, not params, is the real edge metric). The 256M/500M run on a Jetson Orin Nano. GENIUS: 4/5/4/5.
- **FastVLM 0.5B** — see V1 — best Apple-silicon option.
- **YOLO11 / YOLOv10 / RT-DETRv2** — Ultralytics / open — 2024–2025 — **YOLO11 is AGPL-3.0 (license trap)** — fast detection/seg; ONNX. Use RT-DETRv2 (Apache-style) if shipping commercially.
- **EdgeSAM / MobileSAM / PicoSAM2** — 2023–2025 — open — EdgeSAM does image encoding in **26ms on an iPhone 14 (37× faster than SAM)**; PicoSAM2 runs in-sensor. The robot-tier segmenter.
- **Florence-2 (MIT) / Qwen2.5-VL-3B** — capable small VLMs for the box tier.
- **Face/affect: InsightFace (ArcFace/AdaFace), MediaPipe, RTMPose** — mature, edge-friendly face ID + pose/hands for Vector’s social perception.

HONEST FLAGS: **Ultralytics YOLO11/v8 are AGPL-3.0** — a real trap for a commercial product; prefer RT-DETRv2/YOLOX/Apache alternatives. Tiny-VLM “edge” claims usually assume an actively-cooled Orin Nano, not a passively-cooled MCU.

### V6 — Robotics learning & embodied policies

TOP FINDS (ranked):

- **HuggingFace LeRobot** (github / HF) — v0.4.0 2025 — **Apache 2.0** — datasets, ACT, π0/π0.5 ports, SmolVLA, distributed training.
  GENIUS SCORE: cleverness 4/5 · efficiency 4/5 · quality 4/5 · fit 4/5 — the “Transformers of robotics”; SmolVLA fine-tunes in ~8h on one A100. **The realistic entry point if Vector ever gets an actuated attachment.** EDGE FIT: train on GPU / infer on box · PyTorch.
- **SmolVLA** (HF, arXiv 2506.01844) — June 2025 — **Apache 2.0** — 450M params, “comparable to 10× larger models,” designed for affordable robots. The most Vector-appropriate VLA by size. GENIUS: 5/5/4/4.
- **π0 / π0-FAST / π0.5 (openpi)** — Physical Intelligence — Oct 2024–Sep 2025 (PyTorch Sep 2025) — open weights — flow-matching VLA; needs an NVIDIA GPU; built for PI’s own arms (“may or may not work for you”).  GENIUS: 5/2/5/2.
- **Genesis** (github.com/Genesis-Embodied-AI) — Dec 2024, v1.0 2026 — open — pure-Python multi-physics sim.
  GENIUS SCORE: cleverness 4/5 · efficiency 3/5 · quality 3/5 · fit 2/5
  **HONEST FLAG (benchmark-gamed):** Stone Tao’s independent Dec-2024 analysis found “Genesis is not as fast as reported (it is slower by >100x than claimed), and compared to an existing GPU sim Genesis is slower by 3-10x on environments with slightly more collisions / complex dynamics,” and “if you turn on a camera for the robot, the simulation speed drops to just 10x realtime speed.” Still a clever, easy-to-use sim — but treat the “430,000× / 43M FPS” marketing as not representative of real robot-learning workflows.

HONEST FLAGS: VLAs (π0, GR00T, OpenVLA, RDT-1B, Octo) are arm/humanoid-centric; “sim-to-real on a tiny robot” is aspirational. Realistic now: LeRobot + SmolVLA for any future actuated attachment; otherwise classic control beats VLAs for a desk creature.

### V7 — On-device runtimes & compression

RECOMMENDATIONS per tier:

- **Dock box, Apple Silicon:** **MLX** (Apache-style) — native unified-memory + Neural Engine;  runs FastVLM, Kokoro, Kyutai, Whisper. Pair with **Core ML** for ANE-pinned models (Depth Pro, Depth Anything, Kokoro, Parakeet). **FluidAudio** (Apache 2.0, github.com/FluidInference/FluidAudio) is the turnkey Apple-silicon audio SDK — Parakeet ASR ~110× RTF on M4 Pro, diarization, VAD, Kokoro TTS, all ANE-offloaded.
- **Dock box, Jetson:** **TensorRT** + Isaac ROS for perception; ONNX Runtime for portability.
- **Robot (ARM CPU/MCU):** **llama.cpp/ggml (GGUF)** for small LLM/VLM; **ncnn** (Tencent) and **MNN** (Alibaba, +KleidiAI ~57% faster prefill on Arm) for CNNs/VLMs; **ExecuTorch** (PyTorch, +KleidiAI >350 tok/s prefill on Arm) for tight-memory deployment; **TFLite** for the broadest mobile ecosystem.
- **Quantization:** int4/int8 GGUF for LLMs; AWQ/GPTQ for transformer weights; **Matryoshka embeddings** for adaptive-size memory/retrieval vectors.
- **BitNet b1.58 2B4T** (HF microsoft/bitnet-b1.58-2B-4T, arXiv 2504.12285) — Apr 2025 — **MIT** — native 1.58-bit ternary LLM, ~order-of-magnitude memory cut, ~2× CPU speedup.
  GENIUS SCORE: cleverness 5/5 · efficiency 5/5 · quality 3/5 · fit 3/5
  HONEST FLAG: Reproducible (open weights + code) and competitive with FP16 models <3B on benchmarks,  BUT Microsoft itself states it does “not recommend using BitNet b1.58 in commercial or real-world applications without further testing,” flags an elevated defect rate on some queries, and the speedup requires the bespoke bitnet.cpp kernels. Promising, not yet a drop-in.

### V8 — Hidden gems & cross-domain genius

- **Moonshine variable-length encoder** — the purest “Anki-way” 2025 audio move: don’t pad to 30s, compute only on the speech you have. 6× fewer params than Whisper, beats it on WER, runs on a Pi.
- **GTCRN** — speech enhancement at tens of thousands of parameters (ICASSP 2024) — genius-tier efficiency for Vector’s denoise stage on an MCU-class budget.
- **emotion2vec** — a 19M-param “Whisper for emotion,” self-supervised and multilingual — revives affective response cheaply.
- **The DUSt3R→MASt3R→VGGT feed-forward-3D lineage** — collapsing classical multi-view geometry into one network pass is the spatial-AI equivalent of Anki’s single-camera triangulation trick; the fast forks (FastVGGT, LiteVGGT, streaming O(1) variants) are where the edge-deployable gems are emerging.
- **EdgeSAM / PicoSAM2** — CNN-distilled SAM at 26ms on a phone / in-sensor segmentation — clever distillation, not brute force.
- **Kokoro-82M** — proof a solo developer with a tiny Apache-2.0 model can top the TTS Spaces Arena trained on <100 hours of audio; the anti-slop exemplar.
- **FluidAudio** — a small team’s Apache-2.0 SDK pinning Parakeet/Kokoro/diarization to the Apple Neural Engine — exactly the engineering that makes giants’ models usable on the edge.

## Recommendations

**Stage 1 — adopt now (perception + voice core):**

1. Put **Depth Anything V2 Small (CoreML/ONNX)** on the robot for always-on depth; add **Depth Pro** on the box for sharp metric depth when needed.
1. Vision: **Moondream2** (box) or **FastVLM-0.5B / SmolVLM2-500M** (robot/Jetson) for scene understanding; **EdgeSAM** + a non-AGPL detector (RT-DETRv2) for segmentation/detection. *Do not ship Ultralytics YOLO under AGPL.*
1. Audio loop: **Silero VAD → Moonshine (English, MIT) or Parakeet (via FluidAudio on Apple) STT → [intent] → Kokoro-82M TTS**, with **GTCRN/DeepFilterNet** denoise and **emotion2vec** for affect. The whole chain is small, real-time, and license-clean.
1. Runtime: **MLX + Core ML + FluidAudio** if the box is Apple Silicon; **TensorRT/Isaac ROS** if it’s a Jetson.

**Stage 2 — spatial memory (next phase):**
5. Stand up **gsplat** + **MASt3R-SLAM or VGGT** on the box to build and localize within a persistent 3D home map; benchmark frame-rate on your actual GPU before committing.

**Stage 3 — watch / experiment:**
6. Track **BitNet** (adopt when bitnet.cpp matures and defect rates drop), **Kyutai STT/TTS** (CC-BY, excellent streaming — adopt if French/duplex needed), and **streaming/quantized VGGT forks** for eventual on-robot dense 3D.
7. Only invest in **LeRobot + SmolVLA** if/when Vector gains an actuated attachment.

**Benchmarks that would change these calls:** if a streaming VGGT/MASt3R variant hits >15 FPS on your box GPU, promote it to Stage 1; if SpeechAnalyzer’s wake-word quality beats Moonshine AND your box runs macOS 26+, use it instead; if BitNet’s defect rate on your command set is acceptable, adopt it for onboard reasoning.

### Final synthesis — Adopt / Watch / Skip (ranked by genius × fit)

|Tool                      |Vector subsystem  |Verdict              |License flag                 |
|--------------------------|------------------|---------------------|-----------------------------|
|Kokoro-82M                |Voice/TTS         |**ADOPT**            |Apache 2.0 ✅                 |
|Moonshine                 |STT (ear)         |**ADOPT**            |EN MIT ✅ / non-EN NC ⚠       |
|Silero VAD                |Audio gate        |**ADOPT**            |MIT ✅                        |
|GTCRN / DeepFilterNet     |Denoise           |**ADOPT**            |open ✅                       |
|emotion2vec               |Affect            |**ADOPT**            |open ✅                       |
|Depth Anything V2 (Small) |Depth (robot)     |**ADOPT**            |check per size               |
|Apple Depth Pro           |Metric depth (box)|**ADOPT**            |Apple research ⚠             |
|FastVLM-0.5B              |VLM (Apple)       |**ADOPT**            |Apple research ⚠             |
|Moondream2 / SmolVLM2     |VLM (box/robot)   |**ADOPT**            |open / Apache ✅              |
|EdgeSAM / SAM2            |Segmentation      |**ADOPT**            |Apache (SAM2) ✅              |
|gsplat                    |3D map render     |**ADOPT**            |Apache 2.0 ✅                 |
|MASt3R-SLAM / VGGT        |3D map / SLAM     |**ADOPT (box, GPU)** |open ✅                       |
|FluidAudio / MLX / Core ML|Runtime (Apple)   |**ADOPT**            |Apache ✅                     |
|Parakeet TDT 0.6B         |STT (GPU/Apple)   |**ADOPT**            |check CoreML weights         |
|Kyutai STT / TTS          |STT/TTS streaming |**WATCH**            |CC-BY 4.0 ⚠(attrib)          |
|BitNet b1.58              |Onboard LLM       |**WATCH**            |MIT, but immature            |
|Isaac ROS perception      |Map (Jetson only) |**WATCH**            |NVIDIA, Jetson-only          |
|LeRobot + SmolVLA         |Future actuation  |**WATCH**            |Apache 2.0 ✅                 |
|Chatterbox                |Voice cloning     |**WATCH**            |MIT (watermark)              |
|Moshi                     |Full-duplex chat  |**WATCH**            |CC-BY “research” ⚠           |
|Ultralytics YOLO11        |Detection         |**SKIP for shipping**|AGPL-3.0 ⛔                   |
|Genesis sim               |Training          |**SKIP/caution**     |benchmark-gamed ⚠            |
|GR00T / Cosmos / Isaac Lab|Humanoid training |**SKIP**             |scale mismatch               |
|π0 / π0-FAST              |Arm manipulation  |**SKIP**             |GPU + arm-centric            |
|Apple SpeechAnalyzer      |STT (box)         |**CONDITIONAL**      |macOS-26-only, non-exportable|

## Caveats

- **License traps:** Ultralytics YOLO (AGPL-3.0), Moonshine non-English (non-commercial), Moshi (“research only” despite CC-BY weights), Apple research licenses (not classic OSI). Kyutai stack is CC-BY-4.0 (attribution required); FluidAudio is Apache-2.0 but its bundled model weights vary (CC-BY vs Apache). Verify per-model before shipping.
- **Platform lock-in:** Apple SpeechAnalyzer/SpeechTranscriber are not exportable — usable only on macOS/iOS 26+, never on a Jetson/Linux robot.
- **Benchmark gaming:** Genesis’s “430,000× real-time” claim was independently shown to be >100× off and 3–10× slower than existing GPU sims on realistic workloads. Treat any “Nx faster” headline skeptically and re-benchmark on your hardware. Chatterbox and several TTS quality/latency figures are vendor-supplied.
- **Edge reality:** “runs on edge” for feed-forward 3D (VGGT/MASt3R) and most 2B+ VLMs assumes a GPU or an actively-cooled Jetson Orin — not a passively-cooled microcontroller. Match the tier (robot vs box) to the model.
- **Recency:** dates are best-available from release pages and papers; some 2026 arXiv references are follow-on works confirming a lineage rather than primary releases. Qwen2.5-VL’s pretraining is ~18T tokens per its tech report (an earlier draft of this survey cited 22T); the Moondream “~450B tokens” figure refers to its recent 9B-MoE training run.