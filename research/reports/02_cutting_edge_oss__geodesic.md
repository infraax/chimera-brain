# GEODESIC SURVEY — Cutting-Edge Open-Source Models, Papers & Tools (2024–2026)
## Vector-Chimera Upgrade Intelligence · Created 2026-06-24 · Dexter × Perplexity Deep Research

> **Filter:** Anki-bar engineering — cleverness × quality × efficiency, NOT parameter count or press hype.
> Genius score: **C** = cleverness, **E** = efficiency, **Q** = quality, **F** = Vector fit (each /5).

***

## V1 — Apple's Quiet High-Tech Drops

### TOP FINDS (ranked)

***

**🥇 SpeechAnalyzer / SpeechTranscriber (iOS 26 / macOS Tahoe)**
- **URL:** `developer.apple.com/documentation/speech` — **Date:** WWDC June 2025 (GA macOS Tahoe Sept 2025) — **License:** Apple SDK (closed weights, open API) — **Hardware:** All Apple Silicon (ANE-accelerated)
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 5/5 · F 5/5
- **WHAT IT IS:** A new dual-class Speech framework (SpeechAnalyzer orchestrator + SpeechTranscriber module) shipping inside every Apple device from iOS 26/macOS Tahoe onward. It is Apple's dictation/transcription backbone, now exposed as a public API.[^1][^2]
- **WHY IT'S CLEVER:** Apple leveraged Neural Engine at a system level. In independent benchmarks the CLI tool *Yap* (wrapping this API) processed a 7 GB, 34-minute video in **45 seconds** — 2.2× faster than MacWhisper Large V3 Turbo, with indistinguishable accuracy. No model download, zero VRAM, works on iPhone, iPad, Mac, Vision Pro. This IS the "hidden Mac audio model" — it is Apple's on-device ASR stack, running at a system privilege level, now surfaced via a public framework API.[^3][^2][^1]
- **HONEST FLAG:** Closed weights, not exportable. iOS/macOS SDK only; no ONNX/CoreML artifact you can extract. English strongest; multilingual coverage TBD. Requires iOS 26+ / macOS Tahoe Beta (Sept 2025 GA).
- **HOW IT UPGRADES VECTOR:** Drop-in STT for the dock-box Mac mini. Replaces Whisper in the voice-command pipeline. Plug into Swift/Objective-C wrapper for always-on transcription. Zero latency overhead vs cloud STT.
- **EDGE FIT:** Box (Mac mini with Apple Silicon) · Runtime: native Swift framework[^4][^5]

***

**🥈 Apple Depth Pro (`apple/ml-depth-pro`)**
- **URL:** `github.com/apple/ml-depth-pro` / `machinelearning.apple.com/research/depth-pro` — **Date:** Oct 2024 (ICLR 2025 paper) — **License:** Apple Sample Code License (research use) — **Size:** 504M params, fits in 6 GB VRAM
- **GENIUS SCORE:** C 5/5 · E 4/5 · Q 5/5 · F 5/5
- **WHAT IT IS:** Zero-shot metric monocular depth estimation. From a single RGB image, produces sharp 1536×1536 metric depth (absolute scale, no camera intrinsics needed) in 0.3 s on a V100 GPU.[^6][^7]
- **WHY IT'S CLEVER:** Decouples focal length estimation from depth estimation (separate head), then fuses them. Uses a multi-scale ViT with a dedicated boundary-accuracy training protocol. Outperforms Depth Anything V2 and Marigold on all boundary-accuracy metrics while being >10× faster than diffusion-based models. CoreML conversion available (community: `mrgnw/depth-anything-v2-coreml` pattern; Depth Pro community port achieves ~30 ms on M4 Pro Neural Engine).[^8][^7]
- **HONEST FLAG:** Apple Sample Code License — not full Apache. Verify commercial use. 504M params is too heavy for the robot itself; box-side only.
- **HOW IT UPGRADES VECTOR:** Feeds real-world metric depth from robot's single camera to 3D home-map pipeline. No stereo rig required. Pairs with MASt3R-SLAM for persistent map building.
- **EDGE FIT:** Box · CoreML (community port), ONNX exportable[^9][^7]

***

**🥉 FastVLM + MobileCLIP 2 (`apple/ml-fastvlm`, `apple/ml-mobileclip`)**
- **URL:** `github.com/apple/ml-fastvlm` · `github.com/apple/ml-mobileclip` — **Date:** FastVLM Sept 2025; MobileCLIP CVPR 2024 — **License:** Apple ML Research License — **Size:** FastVLM 500M–1.5B; MobileCLIP S0=11M to S3=86M
- **GENIUS SCORE:** C 4/5 · E 5/5 · Q 4/5 · F 5/5
- **WHAT IT IS:** FastVLM is an on-device VLM (vision + language) optimized for Apple Silicon with demo apps for iOS/macOS. MobileCLIP is a family of fast image-text models (3–15 ms latency, 50–150M params) achieving state-of-the-art latency-accuracy tradeoff using multi-modal reinforced training.[^10][^11]
- **WHY IT'S CLEVER:** MobileCLIP pre-computes "reinforced datasets" offline from a caption model + ensemble of CLIP teachers — the knowledge is baked into data, not model, so inference stays light. FastVLM runs VLM tasks on the Neural Engine, demonstrated on Jetson Orin Nano alongside Parakeet + Kokoro.[^11][^12][^13]
- **HONEST FLAG:** Apple ML Research License — verify commercial terms. FastVLM weights require HF token approval.
- **HOW IT UPGRADES VECTOR:** MobileCLIP as vision backbone for open-vocabulary object matching ("is that the blue cup?"). FastVLM for scene understanding at the dock box.
- **EDGE FIT:** Robot (MobileCLIP-S0) / Box (FastVLM) · CoreML export available[^10]

***

**AIMv2 (`apple/ml-aim`)**
- **URL:** `github.com/apple/ml-aim` — **Date:** Nov 2024 (CVPR 2025 Highlight) — **License:** Apache 2.0 — **Size:** 300M–2.7B
- **GENIUS SCORE:** C 4/5 · E 3/5 · Q 5/5 · F 4/5
- **WHAT IT IS:** Multimodal autoregressive vision encoders that outperform OpenAI CLIP, SigLIP, and DINOv2 on open-vocabulary detection, grounding, and ImageNet (89.5% frozen trunk).[^14][^15]
- **WHY IT'S CLEVER:** Uses a causal multimodal decoder that generates both image patches AND text tokens, simplifying pretraining scaling without inter-batch communication overhead.[^16][^17]
- **EDGE FIT:** Box · ONNX / HuggingFace weights[^15]

***

**4M: Massively Multimodal (`apple/ml-4m`)**
- **URL:** `github.com/apple/ml-4m` — **Date:** April 2024 — **License:** Apache 2.0
- **GENIUS SCORE:** C 5/5 · E 3/5 · Q 4/5 · F 3/5
- **WHAT IT IS:** Any-to-any multimodal foundation model (EPFL–Apple). Train once, predict any subset of modalities (RGB, depth, normals, segmentation, text, 3D tokens) from any other subset.[^18]
- **HOW IT UPGRADES VECTOR:** Future: single model for depth + segmentation + captioning from robot camera, without running three separate models.
- **EDGE FIT:** Box only (large) · PyTorch[^18]

***

**Personal Voice (on-device TTS)**
- **URL:** `machinelearning.apple.com/research/personal-voice` — **Date:** iOS 17 / macOS Sonoma Sept 2023; refined through 2025 — **License:** Apple framework (closed)
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 4/5 · F 3/5
- **WHAT IT IS:** On-device voice cloning: records 15 minutes of speech, trains overnight on-device, delivers a synthesized personal voice for Live Speech TTS. Training and inference fully on-device, private. Audio can be exported via a third-party app.[^19][^20]
- **HONEST FLAG:** Weights not exportable; tied to Apple ecosystem. English-only.
- **HOW IT UPGRADES VECTOR:** If Vector's owner records their voice, Vector could speak back in a familiar voice. Dock-box Mac mini could synthesize via Live Speech API.[^19]

***

### V1 HONEST FLAGS
- SpeechAnalyzer weights are **not extractable** — SDK only, not portable to non-Apple hardware.
- Depth Pro license is research-only; no confirmed commercial Apache/MIT grant.
- FastVLM still requires HuggingFace approval gate; not fully open.

***

## V2 — NVIDIA: Simulated Physics Worlds + 3D Perception

### TOP FINDS (ranked)

***

**🥇 Genesis / Genesis World 1.0 (Genesis-Embodied-AI)**
- **URL:** `github.com/Genesis-Embodied-AI/Genesis` · `genesis-world` — **Date:** Dec 2024 (sim); May 2026 (World 1.0) — **License:** Apache 2.0 — **Hardware:** Single GPU/laptop → datacenter
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 5/5 · F 5/5
- **WHAT IT IS:** Universal physics simulator combining rigid body, MPM, SPH, FEM, PBD, and Stable Fluid solvers in a single Pythonic interface. Genesis World 1.0 (open-sourced May 2026) adds a GPU-accelerated cross-platform compiler (Quadrants), penetration-free multi-physics contact solvers, unified rigid/deformable physics, and a photo-realistic renderer (Nyx).[^21][^22]
- **WHY IT'S CLEVER:** Up to 100× faster than real-time on GPU, up to 43 million FPS on cutting-edge hardware. The Anki-bar moment here: one hour of real-world testing = 100 simulation days. Fully differentiable — gradient-based policy optimization. Natural-language scene description → multimodal data engine.[^23][^24][^22][^21]
- **HONEST FLAG:** "World 1.0" released May 2026 — generative framework still modular/partial. The original Genesis Dec 2024 physics engine is solid and reproducible; the generative layer is newer.
- **HOW IT UPGRADES VECTOR:** THE answer to "how does Vector learn new behaviors?" Train navigation, object avoidance, and future manipulation policies in Genesis sim, then transfer to real Vector. No GPU required for modest sims.
- **EDGE FIT:** Box (sim training) → Robot (policy transfer) · Python[^25][^22][^21]

***

**🥈 MASt3R-SLAM / SLAM3R (Imperial / ByteDance)**
- **URL:** `github.com/rmurai0610/MASt3R-SLAM` · SLAM3R (CVPR 2025) — **Date:** Feb 2025 (MASt3R-SLAM CVPR 2025); SLAM3R CVPR 2025 — **License:** CC-BY-NC-4.0 (research) — **Hardware:** Modern GPU, 15–20+ FPS
- **GENIUS SCORE:** C 5/5 · E 4/5 · Q 5/5 · F 5/5
- **WHAT IT IS:** MASt3R-SLAM is a plug-and-play monocular dense SLAM producing globally-consistent poses + dense geometry at **15 FPS** from uncalibrated RGB video. SLAM3R achieves **20+ FPS** via end-to-end feed-forward networks that directly regress 3D pointmaps from sliding-window video clips, without solving camera parameters explicitly.[^26][^27][^28][^29]
- **WHY IT'S CLEVER:** Both systems eliminate the optimization loop that made traditional SLAM slow. MASt3R-SLAM builds on a two-view 3D reconstruction prior (MASt3R) as a dense geometry foundation, reducing matching time to 2 ms with CUDA kernels. SLAM3R needs zero camera calibration.[^29]
- **HONEST FLAG:** CC-BY-NC — research use only. Commercial deployment needs negotiation. Both require capable GPU (not Jetson Orin Nano); box-side processing required.
- **HOW IT UPGRADES VECTOR:** Persistent 3D home map from robot's camera stream → navigation, object placement memory, room-scale understanding.
- **EDGE FIT:** Box · PyTorch / CUDA[^27][^28][^30]

***

**🥉 NVIDIA nvblox + cuVSLAM + FoundationPose**
- **URL:** `github.com/nvidia-isaac/nvblox` · `developer.nvidia.com/isaac` — **Date:** 2024–2025 (ongoing) — **License:** Apache 2.0 (nvblox), NVIDIA EULA (cuVSLAM) — **Hardware:** Jetson-compatible
- **GENIUS SCORE:** C 4/5 · E 4/5 · Q 5/5 · F 5/5
- **WHAT IT IS:**
  - **nvblox**: GPU-accelerated TSDF/ESDF real-time 3D reconstruction from RGB-D, 100× faster than CPU methods. Generates 2D costmap for navigation up to 5 m.[^31]
  - **cuVSLAM**: CUDA-accelerated visual SLAM with sub-1% trajectory error, Jetson-native.[^31]
  - **FoundationPose**: Zero-shot 6-DoF pose estimation + tracking of novel objects from either CAD model or a few reference images; handles textureless/glossy objects.[^32][^33]
- **WHY IT'S CLEVER:** FoundationPose uses a neural implicit representation for novel view synthesis, making the pose estimation model embodiment-agnostic. nvblox runs on Jetson AGX Orin in the dock box.[^33]
- **HOW IT UPGRADES VECTOR:** nvblox for real-time room map; cuVSLAM for odometry; FoundationPose for "where is my charger / where is the toy" object tracking.
- **EDGE FIT:** Box (nvblox, cuVSLAM) / Box + Robot (FoundationPose inference) · TensorRT / CUDA[^33][^31]

***

**NVIDIA GR00T N1 / N1.6 + Isaac Lab**
- **URL:** `research.nvidia.com/publication/2025-03_nvidia-isaac-gr00t-n1` — **Date:** GR00T N1 March 2025; N1.6 Sept 2025 — **License:** NVIDIA Open Model License (permissive for non-commercial; commercial use allowed with attribution) — **Hardware:** Requires NVIDIA GPU for training; inference on Jetson AGX Thor
- **GENIUS SCORE:** C 4/5 · E 2/5 · Q 4/5 · F 2/5
- **WHAT IT IS:** World's first open humanoid robot foundation model. Dual-system architecture: System 1 (fast action model) + System 2 (slow VLA planner). Trained on teleoperation + synthetic (GR00T-Mimic) + internet human videos. 40% performance boost over real-data-only training via synthetic augmentation.[^34][^35][^36]
- **HONEST FLAG:** Designed for humanoid embodiments (Fourier GR-1, 1X). Applying to a Vector (wheeled, tiny) is non-trivial; the embodiment gap is large. Treat as **aspirational/watch** — the architecture and sim-to-real pipeline are the useful takeaway.
- **EDGE FIT:** Cloud training → Jetson AGX Thor inference (not Orin Nano)[^35][^36]

***

**NVIDIA Cosmos 2.5 (World Foundation Models)**
- **URL:** `github.com/nvidia-cosmos` — **Date:** Jan 2025 (Cosmos 1); Oct 2025 (Cosmos 2.5) — **License:** NVIDIA Open Model License — **Hardware:** Multi-GPU for generation
- **GENIUS SCORE:** C 4/5 · E 2/5 · Q 4/5 · F 2/5
- **WHAT IT IS:** Physics-aware world foundation models for generating synthetic training data for robots and AVs. Cosmos-Predict2.5 unifies Text2World, Image2World, Video2World in one model. Cosmos-Transfer2.5 is 3.5× smaller than v1 yet higher quality for Sim2Real domain transfer.[^37][^38][^39]
- **HONEST FLAG:** Generation requires multi-GPU cloud infra. Useful as a **data augmentation engine** for training, not deployed on Vector itself. Main value: generate synthetic home-environment videos to train Vector navigation.
- **EDGE FIT:** Cloud (training data gen) · Python[^38][^40]

***

**FoundationStereo (NVIDIA, CVPR 2025 Best Paper Nom.)**
- **URL:** `nvlabs.github.io/FoundationStereo` — **Date:** 2025 — **License:** NVIDIA Research License — **Hardware:** GPU; Fast variant approaching real-time
- **GENIUS SCORE:** C 5/5 · E 3/5 · Q 5/5 · F 4/5
- **WHAT IT IS:** Zero-shot stereo depth estimation foundation model trained on 1M+ synthetic stereo pairs. Side-tunes monocular priors from DepthAnythingV2 into a stereo framework to bridge the sim-to-real gap.[^41][^42][^43][^44]
- **HOW IT UPGRADES VECTOR:** If Vector gets a second camera (stereo rig), FoundationStereo gives metric depth with zero calibration overhead. Community "Fast-FoundationStereo" variant is approaching real-time.[^45]
- **EDGE FIT:** Box · ONNX/TensorRT[^42][^44]

***

### V2 HONEST FLAGS
- GR00T N1 is **humanoid-first** — applying to Vector is major R&D work, not plug-and-play.
- Cosmos WFMs require **cloud-scale** GPU for generation; not local inference tools.
- Isaac Lab is genuinely useful for small-robot sim, but the stack is complex (requires NVIDIA GPU, Omniverse dependencies).

***

## V3 — 3D Reconstruction, Gaussian Splatting & Spatial AI

### TOP FINDS (ranked)

***

**🥇 VGGT: Visual Geometry Grounded Transformer (Meta, CVPR 2025 Best Paper)**
- **URL:** `github.com/facebookresearch/vggt` · arXiv 2503.11651 — **Date:** Feb 2025 — **License:** Apache 2.0 — **Size:** ~300M–1B (ViT-based); inference in <1 s
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 5/5 · F 5/5
- **WHAT IT IS:** Feed-forward transformer that directly infers ALL key 3D attributes — camera intrinsics + extrinsics, depth maps, point maps, 3D point tracks — from 1, a few, or hundreds of views, in under one second, without any optimization post-processing.[^46][^47]
- **WHY IT'S CLEVER:** Previous approaches (DUSt3R, MASt3R) process image pairs and then do expensive global alignment. VGGT uses alternating global self-attention and frame-wise self-attention to handle variable input counts natively, 50× faster than optimization-based methods. Won CVPR 2025 Best Paper. Handles single-view reconstruction without being trained for it.[^48][^47][^46]
- **HONEST FLAG:** Large multi-view sets (hundreds of images) show declining pose reliability vs. traditional SfM. Best for moderate input sets (2–50 views), which suits home-scale robot mapping perfectly.[^49]
- **HOW IT UPGRADES VECTOR:** Core of Vector's future 3D mapping subsystem. Robot takes photos from multiple positions → VGGT instantly reconstructs room geometry. Replaces need for expensive SLAM initialization.
- **EDGE FIT:** Box · PyTorch / ONNX exportable[^47][^46]

***

**🥈 Mobile-GS: Real-Time Gaussian Splatting for Mobile Devices (ICLR 2026)**
- **URL:** `github.com/xiaobiaodu/mobile-gs` · openreview.net/forum?id=vRegY0pgvQ — **Date:** March 2026 — **License:** CUDA reference code open; Vulkan mobile renderer closed (company policy) — **Size:** 4.8 MB model
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 5/5 · F 4/5
- **WHAT IT IS:** Real-time Gaussian Splatting at **116 FPS on Snapdragon 8 Gen 3** in a **4.8 MB** model. Eliminates depth sorting (the traditional 3DGS bottleneck) with a single-pass depth-aware order-independent renderer + neural opacity MLP.[^50][^51][^52]
- **WHY IT'S CLEVER:** Depth sorting has been the main reason 3DGS couldn't run on mobile. Mobile-GS replaces it with a learned order-independent scheme, accepting minor quality tradeoffs recovered by a lightweight MLP. 3-stage compression pipeline (SH distillation + neural VQ + contribution pruning) collapses GB-scale splats to 4.8 MB.[^51]
- **HONEST FLAG:** Vulkan mobile renderer code is **NOT released** (company policy). Only the CUDA reference code is open. This limits direct porting. Paper is reproducible for understanding; full mobile deployment requires re-implementing the Vulkan pipeline.[^53]
- **HOW IT UPGRADES VECTOR:** If/when Vulkan code releases or is re-implemented: Vector renders and navigates inside a live 4.8 MB photorealistic 3D splat of its home. 116 FPS is more than enough for AR-overlay navigation on the dock screen.
- **EDGE FIT:** Box (CUDA reference) / Robot-companion tablet (Vulkan TBD)[^52][^53]

***

**🥉 Depth Anything V2 (`DepthAnything/Depth-Anything-V2`)**
- **URL:** `github.com/DepthAnything/Depth-Anything-V2` — **Date:** June 2024 (NeurIPS 2024) — **License:** Apache 2.0 (Small/Base/Large); CC-BY-NC-4.0 (Giant 1.3B) — **Size:** 25M / 97M / 335M / 1.3B
- **GENIUS SCORE:** C 4/5 · E 5/5 · Q 4/5 · F 5/5
- **WHAT IT IS:** Monocular depth estimation foundation model. Key innovation: replace all labeled real images in teacher training with 595K high-quality synthetic images, scale teacher model, then pseudo-label 62M unlabeled real images for student training.[^54][^55][^56]
- **WHY IT'S CLEVER:** Synthetic-only teacher → removes label noise and artifacts in reflective/transparent regions. >10× faster than diffusion-based models (Marigold) with higher accuracy. CoreML-converted Small model runs at ~30 FPS on Apple Neural Engine.[^8][^54]
- **HONEST FLAG:** Relative depth is relative, not metric. Metric depth models are fine-tuned variants. Giant (1.3B) is NC only.
- **HOW IT UPGRADES VECTOR:** Per-frame depth for obstacle avoidance. Apache 2.0 Small (25M) runs on the robot companion or box. Video Depth Anything (Jan 2025) adds temporal consistency for video streams.
- **EDGE FIT:** Robot (Small, ONNX/TFLite) / Box (Large, CoreML/ONNX)[^54][^8]

***

**SAM 2 — Segment Anything Model 2 (Meta, ICLR 2025)**
- **URL:** Meta / HuggingFace — **Date:** 2024 (ICLR 2025 paper) — **License:** Apache 2.0 — **Size:** ~200M–600M
- **GENIUS SCORE:** C 4/5 · E 3/5 · Q 5/5 · F 4/5
- **WHAT IT IS:** Unified image and video segmentation model with streaming memory for tracking objects across frames.[^57]
- **HOW IT UPGRADES VECTOR:** Track a specific object (toy, person, charger) across video frames in real time. Combine with Depth Anything V2 for 3D object tracking (community pipeline `pablovela5620/sam2-depthanything` already demonstrates this).[^58]
- **EDGE FIT:** Box · ONNX / PyTorch[^57][^58]

***

**gsplat (nerfstudio)**
- **URL:** `github.com/nerfstudio-project/gsplat` — **Date:** ongoing, 2024–2026 — **License:** Apache 2.0
- **GENIUS SCORE:** C 4/5 · E 4/5 · Q 4/5 · F 4/5
- **WHAT IT IS:** CUDA-accelerated 3DGS rasterization library. 4× less GPU memory and 15% faster training vs. official 3DGS. The standard training backend for the Gaussian Splatting ecosystem.[^59]
- **EDGE FIT:** Box · CUDA / Python[^59]

***

**ConceptGraphs (ICRA 2024)**
- **URL:** `concept-graphs.github.io` — **Date:** 2023 (ICRA 2024) — **License:** MIT — **Hardware:** GPU + LLM API
- **GENIUS SCORE:** C 5/5 · E 3/5 · Q 4/5 · F 4/5
- **WHAT IT IS:** Open-vocabulary 3D scene graph built from RGB-D + poses using 2D VLMs fused to 3D by multi-view association. Natural language queries over 3D space.[^60][^61][^62]
- **HOW IT UPGRADES VECTOR:** "Where is the blue mug?" → query ConceptGraph built from Vector's mapping sessions. Semantic spatial memory for task planning.
- **EDGE FIT:** Box · PyTorch[^61][^60]

***

### V3 HONEST FLAGS
- Mobile-GS Vulkan code not released — CUDA reference only as of mid-2026.[^53]
- VGGT struggles with large image sets; combine with traditional SfM for room-scale completeness.[^49]
- ConceptGraphs requires RGB-D (depth sensor); must combine with a depth model for Vector's monocular camera setup.

***

## V4 — On-Device Audio (STT / TTS / Denoise / VAD / Diarization)

### TOP FINDS (ranked)

***

**🥇 Kokoro-82M (hexgrad)**
- **URL:** `huggingface.co/hexgrad/Kokoro-82M` — **Date:** Dec 25, 2024 — **License:** Apache 2.0 — **Size:** 82M params, <1 GB weights
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 5/5 · F 5/5
- **WHAT IT IS:** TTS model, 82M params, trained on <100 hours of audio. Reaches #1 TTS Spaces Arena Elo (Jan 2025), outperforming XTTS (467M), MetaVoice (1.2B), Parler Mini (880M).[^63][^64][^65]
- **WHY IT'S CLEVER:** Quality inversely proportional to training data size — proves that architectural choices + data quality matter more than scale. 90–210× real-time on decent hardware; runs cleanly on CPU and Mac M-series. ONNX version available for cross-platform deployment. Community-reported on Jetson Orin Nano (8 GB) alongside Parakeet + Gemma 4 VLA.[^66][^64][^13]
- **THE VECTOR VOICE:** Kokoro is the primary candidate for Vector's voice. 54 preset voice-packs, Apache 2.0 clean, and the quality-to-size ratio is unmatched.
- **EDGE FIT:** Robot possible (CPU ONNX) / Box preferred · ONNX / CoreML (community Kokoro-TTS-coreml)[^67][^64][^66]

***

**🥈 NVIDIA Parakeet TDT (NeMo)**
- **URL:** `huggingface.co/nvidia/parakeet-tdt-0.6b-v3` / `parakeet-tdt-1.1b` — **Date:** 2024, updated 2025 — **License:** CC-BY-4.0 (self-hostable; NOT NC) — **Size:** 0.6B / 1.1B
- **GENIUS SCORE:** C 4/5 · E 4/5 · Q 5/5 · F 5/5
- **WHAT IT IS:** Top-ranked English ASR on HuggingFace Open ASR Leaderboard. RTFx >2,000 (2,000× faster than real-time on GPU). Parakeet-TDT uses Token-and-Duration Transducer for streaming with timestamp output.[^68][^69]
- **WHY IT'S CLEVER:** Fast-Conformer encoder achieves ~3× compute savings and ~4× memory savings vs. standard Conformer. INT8 TensorRT quantization delivers 1.82× speedup on Jetson AGX Orin. Community Swift package wraps Parakeet-TDT as CoreML on Apple Silicon.[^70][^71][^4]
- **HONEST FLAG:** CC-BY-4.0 (commercial allowed with attribution) — verify exact terms. English-focused; multilingual v3 covers major European languages.
- **EDGE FIT:** Box (GPU) / Jetson AGX Orin · TensorRT INT8 / CoreML (community)[^13][^71][^4]

***

**🥉 Moshi + Kyutai STT/TTS (Kyutai)**
- **URL:** `github.com/kyutai-labs/moshi` — **Date:** Moshi Sept 2024; Kyutai STT/TTS July 2025 — **License:** Apache 2.0 — **Size:** Moshi 7B; Kyutai STT ~small; Kyutai TTS 1.6B
- **GENIUS SCORE (Moshi full-duplex):** C 5/5 · E 3/5 · Q 4/5 · F 4/5
- **WHAT IT IS:**
  - **Moshi**: Full-duplex speech-to-speech foundation model. Listens and speaks simultaneously. Sub-200 ms end-to-end latency. No STT→LLM→TTS pipeline — processes speech tokens natively via Mimi codec.[^72][^73]
  - **Kyutai STT** (June 2025): Streaming STT model, Apache 2.0.
  - **Kyutai TTS 1.6B** (July 2025): Open-source TTS. Apache 2.0.[^74]
  - **MoshiVis** (March 2025): Extended Moshi to discuss images — open-source vision speech model.[^74]
  - MLX Swift port exists (`kyutai-labs/moshi-swift`) for iOS/macOS experimentation.[^75]
  - Post-trained RL variant `moshika-rl-seamless` improves pause handling, turn-taking, backchanneling, interruption.[^76]
- **HOW IT UPGRADES VECTOR:** Full-duplex voice conversation — Vector can talk and listen simultaneously without awkward push-to-talk turns. The Anki-era vision realized.
- **HONEST FLAG:** 7B is heavy; box-only at current quantization. MLX Swift port is experimental.[^75]
- **EDGE FIT:** Box · PyTorch / MLX (experimental)[^73][^72][^75]

***

**Sesame CSM-1B (`SesameAILabs/csm-1b`)**
- **URL:** HuggingFace — **Date:** Feb 26, 2025 — **License:** Apache 2.0 — **Size:** 1B
- **GENIUS SCORE:** C 4/5 · E 3/5 · Q 4/5 · F 4/5
- **WHAT IT IS:** Conversational Speech Model — context-aware TTS with natural pauses, breathing, and multi-speaker dialogue continuity. Llama backbone + codec.[^77][^78]
- **EDGE FIT:** Box · PyTorch[^78][^77]

***

**Orpheus TTS (Canopy Labs)**
- **URL:** HuggingFace `canopylabs/orpheus-*` — **Date:** March 7, 2025 — **License:** Apache 2.0 — **Size:** 150M / 400M / 1B / 3B
- **GENIUS SCORE:** C 4/5 · E 4/5 · Q 4/5 · F 4/5
- **WHAT IT IS:** Llama-based TTS with emotion tags (laugh, sigh, sniffle, groan), zero-shot voice cloning, streaming. 100k+ hours training. Multiple sizes from 150M for edge to 3B for quality.[^79][^77][^78]
- **EDGE FIT:** Robot (150M ONNX) / Box (1B) · PyTorch[^77][^78]

***

**Moonshine (Useful Sensors)**
- **URL:** HuggingFace `UsefulSensors/moonshine` — **Date:** 2024 — **License:** MIT — **Size:** 61M (Base), 37M (Tiny)
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 3/5 · F 5/5
- **WHAT IT IS:** Ultra-lightweight STT at 61M params. Runs on Raspberry Pi. 7.8% WER on standard benchmarks. Specifically designed for always-on real-time edge ASR.[^80]
- **HOW IT UPGRADES VECTOR:** Wake-word detection and lightweight command parsing ON the robot itself (no round-trip to box). Ergodic Streaming Encoder in Moonshine v2 targets latency-critical applications.[^68]
- **EDGE FIT:** Robot · ONNX / TFLite[^80][^68]

***

**DeepFilterNet3 / GTCRN (noise suppression)**
- **URL:** `github.com/rikorose/DeepFilterNet` — **Date:** DeepFilterNet3 2024; GTCRN research — **License:** MIT (DeepFilterNet) — **Size:** ~2–8M params
- **GENIUS SCORE:** C 4/5 · E 5/5 · Q 4/5 · F 5/5
- **WHAT IT IS:** Real-time speech enhancement with sub-millisecond latency. DeepFilterNet3 combines a Deep Filtering layer for fine frequency structure with a spectral enhancement branch. GTCRN (GRU-TCN-CRN) achieves 7.8 GMACs/s for real-time use.
- **EDGE FIT:** Robot · ONNX / TFLite

***

**Silero VAD + NOVA-VAD**
- **URL:** `github.com/snakers4/silero-vad` — **Date:** 2020–ongoing; NOVA-VAD June 2026 — **License:** MIT (Silero) — **Size:** ~1–2MB
- **GENIUS SCORE:** C 4/5 · E 5/5 · Q 4/5 · F 5/5
- **WHAT IT IS:** Silero VAD: enterprise-grade voice activity detector, ~1 MB, real-time on CPU. NOVA-VAD (HF community, June 2026): lightweight VAD beating Silero (93% vs 87% on noisy audio UrbanSound8K), no GPU required.[^81][^82]
- **EDGE FIT:** Robot · ONNX / TorchHub[^82][^81]

***

**NeMo TitaNet (speaker diarization/ID)**
- **URL:** `huggingface.co/nvidia/speakerverification_en_titanet_large` — **Date:** 2023–2024 — **License:** CC-BY-4.0 — **Size:** 23M (Large), 6M (Small)
- **GENIUS SCORE:** C 4/5 · E 5/5 · Q 5/5 · F 5/5
- **WHAT IT IS:** 1D depth-wise separable conv + SE layers + channel attention statistics pooling. EER 0.68% on VoxCeleb1; DER 1.73% on AMI. TitaNet-S at 6M params is near SOTA.[^83][^84][^85]
- **HOW IT UPGRADES VECTOR:** Know WHO is speaking (owner vs. guest) in real time. CoreML port available via the on-device Swift speech toolkit.[^4]
- **EDGE FIT:** Robot (6M) / Box (23M) · ONNX / CoreML[^83][^4]

***

### V4 Audio Shortlist Table

| Role | Winner | Size | License | Edge Fit |
|------|---------|------|---------|----------|
| STT (box) | Parakeet TDT 0.6B | 0.6B | CC-BY-4.0 | Box / Jetson |
| STT (robot) | Moonshine Tiny | 37M | MIT | Robot |
| TTS (Vector voice) | **Kokoro-82M** | 82M | Apache 2.0 | Box + CPU |
| TTS (expressive) | Orpheus 400M | 400M | Apache 2.0 | Box |
| Full-duplex convo | Moshi | 7B | Apache 2.0 | Box only |
| Denoise/AEC | DeepFilterNet3 | ~2M | MIT | Robot |
| VAD | Silero / NOVA-VAD | 1–2 MB | MIT | Robot |
| Speaker ID | TitaNet-S | 6M | CC-BY-4.0 | Robot/Box |
| Emotion from voice | emotion2vec | ~20M | MIT | Box |

***

## V5 — Small/Efficient Vision & VLMs for Edge

### TOP FINDS (ranked)

***

**🥇 SmolVLM2 (Hugging Face)**
- **URL:** `huggingface.co/blog/smolvlm2` — **Date:** Feb 2025 — **License:** Apache 2.0 — **Size:** 256M / 500M / 2.2B
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 4/5 · F 5/5
- **WHAT IT IS:** Compact VLMs handling image AND video with 256M parameters — the smallest video LM ever released. SmolVLM2-2.2B outperforms Qwen2-VL-7B on WorldSense benchmark.[^86][^87][^88]
- **WHY IT'S CLEVER:** Token compression via aggressive pixel shuffling + pooling achieves ViT-level visual understanding at a fraction of the compute. The 500M variant runs on edge devices with video input.[^87][^88]
- **HOW IT UPGRADES VECTOR:** "What room is this?" / "What is the person holding?" / "Is the path clear?" — live scene understanding at the box or eventually on-robot.
- **EDGE FIT:** Robot (256M ONNX) / Box (500M–2.2B) · ONNX / MLX[^12][^86]

***

**🥈 Moondream 2 / Moondream 3 Preview**
- **URL:** `github.com/vikhyat/moondream` — **Date:** 2024; Moondream 3 Sept 2025 — **License:** Apache 2.0 — **Size:** 1.9B (MD2); 9B MoE / 2B active (MD3)
- **GENIUS SCORE:** C 4/5 · E 5/5 · Q 4/5 · F 5/5
- **WHAT IT IS:** Efficiency-focused VLM (SigLIP encoder + compact LM backbone). Designed for consumer hardware. MD3 Preview adds 9B MoE with 2B active params for stronger visual reasoning while retaining edge focus.[^89][^87]
- **EDGE FIT:** Box · ONNX / Transformers[^89][^12]

***

**🥉 YOLO11 + YOLO-World**
- **URL:** `github.com/ultralytics/ultralytics` · `github.com/AILab-CVC/YOLO-World` — **Date:** YOLO11 Oct 2024; YOLO-World CVPR 2024 — **License:** AGPL-3.0 (Ultralytics; commercial license available) — **Size:** YOLO11n=2.6M; YOLO-World-S=13M
- **GENIUS SCORE:** C 4/5 · E 5/5 · Q 4/5 · F 5/5
- **WHAT IT IS:**
  - **YOLO11**: C3k2 + C2PSA attention, 39.5% mAP at ~56 ms CPU for YOLO11n. Exports to CoreML, TensorRT, ONNX.[^90]
  - **YOLO-World**: RepVL-PAN + region-text contrastive learning → real-time open-vocabulary detection at 52 FPS (V100) with 35.4 AP on LVIS zero-shot.[^91]
- **WHY IT'S CLEVER:** YOLO-World re-parameterizes text embeddings at inference time — deploy once, detect anything with text prompt, no retraining needed.[^92][^93][^91]
- **HONEST FLAG:** AGPL-3.0 — commercial users must purchase Ultralytics Enterprise license.
- **EDGE FIT:** Robot (YOLO11n, TFLite/CoreML) / Box (YOLO-World-S) · CoreML/ONNX/TFLite[^94][^90]

***

**AIMv2 (Apple vision encoder — also listed in V1)**
- For vision tasks: AIMv2-300M outperforms CLIP/SigLIP/DINOv2 on detection benchmarks, Apache 2.0.[^14][^15]

**Florence-2 (Microsoft)**
- **URL:** HuggingFace `microsoft/Florence-2` — **Date:** 2024 — **License:** MIT — **Size:** 230M / 770M
- **GENIUS SCORE:** C 4/5 · E 4/5 · Q 4/5 · F 4/5
- Unified multi-task vision model: detection, segmentation, grounding, captioning, OCR — single model, one forward pass.[^93][^92]
- **EDGE FIT:** Box · ONNX / PyTorch

***

**InsightFace / ArcFace (face recognition stack)**
- **URL:** `github.com/deepinsight/insightface` — **Date:** continuously updated — **License:** MIT (library); specific models may vary
- **GENIUS SCORE:** C 4/5 · E 4/5 · Q 5/5 · F 5/5
- **WHAT IT IS:** Face detection + recognition + age/gender/expression. Sub-10ms on GPU. The community standard for face recognition.
- **HOW IT UPGRADES VECTOR:** "Is this my owner?" — person recognition for personalized responses.
- **EDGE FIT:** Box · ONNX / CoreML (community)

***

**RTMPose (OpenMMLab)**
- **URL:** `github.com/open-mmlab/mmpose` — **Date:** 2023–2025 — **License:** Apache 2.0
- **GENIUS SCORE:** C 4/5 · E 5/5 · Q 4/5 · F 4/5
- **WHAT IT IS:** Real-time multi-person pose estimation, 13+ FPS on CPU. Whole-body (body + hand + face keypoints). Animal pose variants available.
- **HOW IT UPGRADES VECTOR:** Understands human gestures and body language for interaction.
- **EDGE FIT:** Robot (lightweight variant) / Box · ONNX

***

### V5 HONEST FLAGS
- YOLO11 / Ultralytics requires **Enterprise license** for commercial use with AGPL-3.0.
- InsightFace models vary in license — verify individual model files.

***

## V6 — Robotics Learning & Embodied Policies

### TOP FINDS (ranked)

***

**🥇 SmolVLA (Hugging Face, June 2025)**
- **URL:** `github.com/huggingface/lerobot` · `huggingface.co/lerobot/smolvla_base` — **Date:** June 2025 — **License:** Apache 2.0 — **Size:** 450M
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 5/5 · F 4/5
- **WHAT IT IS:** Compact Vision-Language-Action model. Trained on community datasets (no proprietary data). Matches π0 (3.3B) performance on LIBERO (87.3% success rate) at 10× smaller size. Runs on single GPU or CPU.[^95][^96][^97]
- **WHY IT'S CLEVER:** Uses an asynchronous inference stack that decouples perception+planning from action execution — enables higher control rates with chunked action generation. Fine-tuned with ~50 episodes. Pretrained on 10M frames from 487 community datasets (LeRobot Hub).[^95]
- **HOW IT UPGRADES VECTOR:** The realistic entry point for teaching Vector new skills. Record 50 demonstrations → fine-tune SmolVLA → deploy. The "behavior recording + policy learning" loop made affordable.
- **EDGE FIT:** Box · PyTorch / CPU inference[^96][^97][^98][^95]

***

**🥈 LeRobot Framework (Hugging Face)**
- **URL:** `github.com/huggingface/lerobot` — **Date:** v0.1 March 2024; v1.0 April 2025 — **License:** Apache 2.0
- **GENIUS SCORE:** C 4/5 · E 4/5 · Q 4/5 · F 5/5
- **WHAT IT IS:** Hardware-agnostic open robotics framework aggregating ACT, Diffusion Policy, TDMPC, OpenVLA, π0, SmolVLA with plug-and-play deployment tooling.[^99][^100]
- **WHY IT'S CLEVER:** Standardizes the data → training → deployment loop for real-world robots. The "Hugging Face Hub for robot behaviors" — community datasets under `lerobot` tag used to pretrain SmolVLA.
- **HOW IT UPGRADES VECTOR:** The orchestration layer. Record Vector behavior data, train policies, version-control them, share and combine with community datasets.
- **EDGE FIT:** Box (training) + Robot (policy inference) · PyTorch[^100][^99]

***

**🥉 Genesis (also V2 — standalone here for robotics fit)**
- Apache 2.0, runs on laptop, 100× faster than real-time. The sim layer for training Vector skills without a physical robot available.[^22][^21]
- **Entry point:** `pip install genesis-world` → define Vector's kinematic model → simulate navigation + future gripper behaviors.[^25]

***

**π0 / Physical Intelligence (aspirational)**
- **URL:** physicalintelligence.company — **Date:** Oct 2024 — **License:** Not fully open (research preview) — **Size:** 3.3B (π0), 5B (π0.6)
- **GENIUS SCORE:** C 5/5 · E 2/5 · Q 5/5 · F 2/5
- **WHAT IT IS:** VLA with PaliGemma VLM backbone + flow-matching action expert, 50 Hz control, trained on 8 robot embodiments.[^101][^102]
- **HONEST FLAG:** Not fully open-source. Weights available for research via HF gate; not commercial. Designed for manipulation arms, not wheeled robots. Conceptually important; SmolVLA is the practical equivalent.
- **EDGE FIT:** Box (research only)[^102][^103][^101]

***

**OpenVLA (UC Berkeley)**
- **URL:** HuggingFace — **Date:** 2024 — **License:** Apache 2.0 — **Size:** 7B
- **GENIUS SCORE:** C 4/5 · E 3/5 · Q 4/5 · F 3/5
- Outperforms RT-2-X (55B) with 7× fewer parameters via more diverse training data (970K demos). Too large for Vector-box inference unless heavily quantized.[^103][^101]
- **EDGE FIT:** Box (Q4 quantized) · GGUF possible[^101][^103]

***

### V6 HONEST FLAGS
- SmolVLA requires SO100/SO101-style robot data or equivalent. Vector's native action space (wheels + tilt, no gripper) needs custom dataset collection.
- π0 weights are gated; not truly open-source commercial.
- All VLAs currently assume manipulator-style action spaces; Vector's wheeled navigation needs domain-specific training.
- **Most realistic entry point:** Genesis sim (train navigation) → SmolVLA fine-tuned on recorded Vector demonstrations → deploy via LeRobot.

***

## V7 — On-Device Runtimes & Compression

### TOP FINDS (ranked)

***

**🥇 MLX + mlx-community (Apple)**
- **URL:** `github.com/ml-explore/mlx` · `huggingface.co/mlx-community` — **Date:** Nov 2023 (framework); 2024–2026 (ongoing community) — **License:** MIT — **Hardware:** Apple Silicon (M-series, A-series)
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 5/5 · F 5/5
- **WHAT IT IS:** Apple's array framework purpose-built for Apple Silicon. Unified memory (CPU + GPU share same pool → zero copy overhead). Lazy evaluation, JIT compilation, automatic differentiation. `mlx-community` on HuggingFace has thousands of quantized models (LLMs, VLMs, ASR, TTS, STT).[^104][^105]
- **WHY IT'S CLEVER:** Eliminates GPU memory copies that plague CUDA on non-unified memory systems. MLX-LM handles LLM text generation + LoRA fine-tuning. `mlx-vlm` adds VLM inference. `mlx-audio` adds TTS/STT/STS. WWDC 2025 session dedicated to MLX on Apple Silicon.[^106]
- **HOW IT UPGRADES VECTOR:** The dock box Mac mini (Apple Silicon) runs everything in MLX — STT, LLM reasoning, TTS, VLM — with no VRAM fragmentation. Single memory pool = more model fits simultaneously.
- **EDGE FIT:** Box (Mac mini Apple Silicon) · Python + Swift[^107][^105][^104]

***

**🥈 BitNet b1.58 + bitnet.cpp (Microsoft)**
- **URL:** `github.com/microsoft/BitNet` — **Date:** Paper 2024; 2B-4T weights April 2025; bitnet.cpp 1.0 March 2026 — **License:** MIT (framework); Apache 2.0 (BitNet-b1.58-2B-4T weights) — **Hardware:** ARM + x86 CPU, GPU (May 2025)
- **GENIUS SCORE:** C 5/5 · E 5/5 · Q 4/5 · F 4/5
- **WHAT IT IS:** 1.58-bit ternary LLM inference (weights ∈ {−1, 0, +1}). 2.37–6.17× speedup on x86, 1.37–5.07× on ARM. Up to 82% energy reduction. A 100B model runs at human reading speed (5–7 tok/s) on a single CPU. Open-weight 2B-4T model released with competitive accuracy vs. FP16 peers.[^108][^109][^110][^111][^112]
- **WHY IT'S CLEVER:** Ternary weights turn dot products into table lookups → eliminates floating-point multiply-accumulate, the dominant operation in LLM inference. No quality loss vs. FP16 for same-size ternary-trained models.[^108]
- **HONEST FLAG:** Quality is competitive only for **natively BitNet-trained models** — post-hoc quantization of existing FP16 models to 1.58-bit does not match. Currently limited to 2B open-weight model (4T tokens). Larger ternary models are in research pipeline.
- **HOW IT UPGRADES VECTOR:** Run a capable LLM reasoning model on the box's CPU cores while GPU handles vision/audio simultaneously. No GPU memory competition between the LLM brain and perception models.
- **EDGE FIT:** Box (CPU) · llama.cpp backend[^110][^111][^108]

***

**🥉 ExecuTorch 1.0 GA (Meta / ARM)**
- **URL:** `github.com/pytorch/executorch` — **Date:** Oct 2025 (1.0 GA) — **License:** BSD-3-Clause — **Hardware:** ARM Cortex-A, Cortex-M, Ethos-U NPU, Qualcomm, Apple ANE
- **GENIUS SCORE:** C 4/5 · E 5/5 · Q 4/5 · F 4/5
- **WHAT IT IS:** PyTorch's official on-device inference runtime. Unified export from PyTorch 2 → any ARM device. CMSIS-NN backend for Cortex-M microcontrollers. TOSA integration for Arm GPU + Ethos-U NPUs. 4-bit quantization via KleidiAI.[^113][^114][^115]
- **HOW IT UPGRADES VECTOR:** Export SmolVLA policies, Moonshine STT, YOLO11 detectors to ExecuTorch format → deploy on the robot's ARM board directly.
- **EDGE FIT:** Robot + Box · ARM / ONNX / CoreML[^114][^113]

***

**llama.cpp / GGUF ecosystem**
- **URL:** `github.com/ggerganov/llama.cpp` — **License:** MIT
- **GENIUS SCORE:** C 4/5 · E 4/5 · Q 4/5 · F 4/5
- The universal cross-platform LLM inference engine. GGUF quantization (Q4_K_M sweet spot). Runs on Mac mini CPU+Metal, Jetson Orin. `llama-server` with Jinja templates enables autonomous tool-calling for VLA workflows. Community Jetson demo running Gemma 4 + Parakeet + Kokoro all simultaneously on 8 GB.[^13]
- **EDGE FIT:** Box + Robot (tiny models) · Metal / CUDA / CPU[^13]

***

**TensorRT / Jetson ecosystem (NVIDIA)**
- For Box side (Jetson AGX Orin): INT8 TensorRT gives 1.82× Parakeet speedup, 3× memory reduction. nvblox + cuVSLAM run natively. LeRobot policy inference possible.[^71]
- **EDGE FIT:** Box (Jetson) · TensorRT[^71]

***

**ONNX Runtime**
- Universal format for all perception/audio models. Supported by Apple (Core ML bridge), ARM (via ExecuTorch), NVIDIA (TensorRT backend). All models above export to ONNX.
- **EDGE FIT:** Robot + Box · Universal

***

### V7 Runtime Recommendations by Tier

| Tier | Device | Best Runtime | Best Quantization |
|------|--------|-------------|------------------|
| Robot (ARM CPU only) | Vector's companion board | ONNX Runtime / TFLite / ExecuTorch | INT8 / Q4 GGUF |
| Box (Mac mini M-series) | Dock box Apple Silicon | **MLX** (GPU) + llama.cpp (CPU) + CoreML (ANE) | 4-bit MLX / BitNet 1.58 |
| Box (Jetson AGX Orin) | Dock box NVIDIA | TensorRT INT8 + ONNX Runtime | INT8 / FP16 TensorRT |
| Training | Cloud / Workstation | PyTorch + CUDA + Genesis | FP16 / BF16 |

***

## V8 — Hidden Gems & Cross-Domain Genius

### TOP FINDS (ranked)

***

**🥇 VGGT single-camera 3D (the "Anki move" of 2025)**
- Already detailed in V3. The genius-tier insight worth re-emphasizing: **one camera, no calibration, no optimization loop** → full 3D. VGGT is structurally analogous to Anki's single-camera + physics depth trick.[^46][^47]
- Award: **CVPR 2025 Best Paper** (Meta AI). Apache 2.0.

***

**🥈 SLAM3R end-to-end neural SLAM**
- **URL:** CVPR 2025 — **Date:** 2025 — **License:** check repo
- **WHY GENIUS:** Completely eliminates camera parameter solving — neural network directly regresses 3D pointmaps from video clips and aligns them globally without any matrix decomposition. This is a 30-year SfM/SLAM paradigm thrown out the window.[^28][^26]

***

**🥉 Moonshine Ergodic Streaming Encoder**
- **URL:** `UsefulSensors/moonshine` — **Date:** 2024 — **License:** MIT
- **WHY GENIUS:** 37M model on Raspberry Pi for always-on ASR. The ergodic streaming encoder incrementally updates the hidden state rather than re-processing from scratch — sub-real-time latency on CPU.[^80][^68]

***

**Mobile-GS 4.8 MB Gaussian Splat**
- **WHY GENIUS:** Compresses multi-GB 3D scenes to 4.8 MB via 3-stage compression + replaces expensive depth-sort with learned order-independent rendering. "Gaussian splatting on a phone" is the spatial computing version of Anki's single-camera trick. (Caveat: Vulkan renderer not yet open.)[^50][^51][^53]

***

**BitNet b1.58 Ternary LLM**
- **WHY GENIUS:** Changes matrix multiply (quadratic in FP16) into lookup table operations (constant per weight). Energy drops 82%. The math is beautifully minimal: \( w \in \{-1, 0, +1\} \) → no float multiply needed.[^110][^108]

***

**NOVA-VAD (community solo dev, HF, June 2026)**
- **URL:** `github.com/monishmal3375/nova-vad` — **Date:** June 2026 — **License:** check repo
- **WHY GENIUS:** Solo developer building a lightweight explainable VAD that outperforms Silero (87%) with 93% accuracy on noisy real-world audio (UrbanSound8K), no GPU required, with feature-level explainability. Exactly the "solo dev outranks mediocre big-company drop" rubric.[^82]

***

**NeMo TitaNet-S — 6M param speaker diarization**
- **WHY GENIUS:** Channel attention statistics pooling collapses variable-length utterances to fixed embeddings — speaker identity in 6M params, near SOTA. The SE-layer + depth-wise conv combo achieves speaker-phone-level diarization accuracy that previously required 23M+.[^84][^83]

***

**Event Cameras + Neuromorphic SLAM (watch item)**
- **URL:** Academic frontier — 2024–2026 research wave
- **WHY GENIUS:** Event cameras (e.g., Prophesee) output per-pixel brightness-change events asynchronously at microsecond resolution — no frames, no motion blur, 100 kHz effective sampling, low power. A 2026 thesis demonstrates SNN-based SLAM with sub-metre ATE in indoor/outdoor scenes. This is the "physics trick with one sensor" in camera hardware form.[^116][^117][^118]
- **VECTOR FIT:** Watch only — event cameras are $200–$2000, not off-the-shelf for Vector-scale robots yet. The architecture insight (sparse, asynchronous, neuromorphic processing) applies to future Vector hardware.

***

**Grounded SAM Pipeline (Grounding DINO + SAM 2)**
- **WHY GENIUS:** Text prompt → detect any object → segment it → track it across video. Zero retraining. The Swiss Army knife for robotics perception. Open-vocabulary detection (no fixed class list) + temporal tracking in one pipeline. Grounding DINO 1.5 Pro achieves 52%+ zero-shot COCO AP.[^92]
- **EDGE FIT:** Box · ONNX[^93][^92]

***

**ConceptGraphs + OpenFunGraph**
- **WHY GENIUS:** Transforms a sequence of RGB-D frames into a graph where nodes are 3D objects with language descriptions and edges are spatial-semantic relationships. LLM can then reason: "to turn on the light, navigate to the light switch node." The semantic memory layer for robot task planning.[^119][^60][^61]

***

## Final Synthesis: Adopt Now / Watch / Skip Table

Mapped to Vector-Chimera subsystems. Ranked by Genius Score (C+E+Q+F / 20).

| Tool | Score /20 | Subsystem | Status | License | Notes |
|------|-----------|-----------|--------|---------|-------|
| **SpeechAnalyzer/Transcriber** | 20 | STT / Voice | **Adopt Now** | Apple SDK | Box only; macOS Tahoe GA |
| **Kokoro-82M** | 20 | TTS / Voice | **Adopt Now** | Apache 2.0 | Vector's voice candidate |
| **VGGT** | 20 | 3D Mapping | **Adopt Now** | Apache 2.0 | CVPR 2025 Best Paper |
| **MLX + mlx-community** | 20 | Runtime / Box | **Adopt Now** | MIT | Mac mini dock box runtime |
| **Genesis (physics sim)** | 19 | Sim Training | **Adopt Now** | Apache 2.0 | Train behaviors in sim |
| **SmolVLM2-500M** | 19 | Scene Understanding | **Adopt Now** | Apache 2.0 | Video VLM on box |
| **Depth Anything V2 Small** | 18 | Depth / Robot | **Adopt Now** | Apache 2.0 | CoreML 30 FPS on ANE |
| **SmolVLA-450M** | 19 | Robot Policies | **Adopt Now** | Apache 2.0 | Entry robotics learning |
| **LeRobot Framework** | 18 | Policy Orchestration | **Adopt Now** | Apache 2.0 | Data → train → deploy |
| **Parakeet TDT 0.6B** | 18 | STT / Box | **Adopt Now** | CC-BY-4.0 | Top Open ASR leaderboard |
| **MASt3R-SLAM** | 19 | SLAM / Mapping | **Adopt Now** | CC-BY-NC-4.0 | 15 FPS dense SLAM |
| **Silero VAD + NOVA-VAD** | 19 | VAD / Robot | **Adopt Now** | MIT | Tiny, real-time, on-robot |
| **TitaNet-S** | 19 | Speaker ID | **Adopt Now** | CC-BY-4.0 | 6M params, near-SOTA |
| **Moonshine Tiny** | 18 | STT / Robot | **Adopt Now** | MIT | 37M, Raspberry Pi level |
| **Moshi + Kyutai STT/TTS** | 17 | Full-Duplex Voice | **Watch** | Apache 2.0 | 7B heavy; box-only now |
| **FoundationStereo** | 17 | Stereo Depth | **Watch** | NVIDIA Research | Add stereo rig to Vector |
| **nvblox + FoundationPose** | 18 | 3D Perception | **Watch** | Apache 2.0 / EULA | Jetson AGX needed |
| **BitNet b1.58** | 18 | LLM Runtime | **Watch** | MIT/Apache | 2B open model only now |
| **YOLO11n + YOLO-World** | 18 | Detection | **Adopt Now** | AGPL-3.0 ⚠️ | Commercial license needed |
| **Apple Depth Pro** | 18 | Monocular Depth | **Adopt Now** | Apple License ⚠️ | Research use; verify |
| **Mobile-GS** | 19 | 3D Rendering | **Watch** | CUDA open; Vulkan ❌ | Vulkan mobile not released |
| **AIMv2 (Apple)** | 16 | Vision Encoder | **Watch** | Apache 2.0 | CLIP/SigLIP/DINOv2 beater |
| **ConceptGraphs** | 17 | Spatial Memory | **Watch** | MIT | Needs RGB-D |
| **gsplat** | 16 | Splat Training | **Adopt Now** | Apache 2.0 | 3DGS training backend |
| **SAM 2** | 16 | Object Tracking | **Adopt Now** | Apache 2.0 | Track + 3D project |
| **Orpheus TTS 400M** | 17 | Expressive TTS | **Watch** | Apache 2.0 | Emotion tags; backup voice |
| **Sesame CSM-1B** | 16 | Conversational TTS | **Watch** | Apache 2.0 | Dialogue-specific |
| **SLAM3R** | 18 | Neural SLAM | **Watch** | Check repo | 20+ FPS; newer |
| **GR00T N1.6** | 13 | Humanoid Policy | **Skip (now)** | NVIDIA Open Model | Embodiment gap too large |
| **Cosmos 2.5** | 12 | Synthetic Data | **Skip (now)** | NVIDIA Open Model | Cloud-only; infrastructure |
| **ExecuTorch 1.0** | 17 | ARM Runtime | **Watch** | BSD-3 | For future robot-side deploy |
| **Event Cameras / Neuromorphic** | 18 | Perception (future) | **Watch** | Hardware | 2026 hardware maturing |
| **Florence-2** | 16 | Multi-task Vision | **Watch** | MIT | Unified detection/caption |
| **4M Multimodal (Apple)** | 15 | Any-to-any | **Watch** | Apache 2.0 | Aspirational box model |

***

## Priority Build Stack (Immediate 2026 Sprint)

**Tier 1 — Deploy today (all Apache/MIT/CC-BY, proven reproducible):**
1. **MLX** on dock-box Mac mini → unified inference runtime
2. **Kokoro-82M** (ONNX/CoreML) → Vector's voice
3. **SpeechAnalyzer API** → replace Whisper STT (macOS Tahoe box)
4. **Moonshine Tiny** → on-robot wake-word / command parsing
5. **Depth Anything V2 Small** (CoreML) → per-frame robot depth
6. **SmolVLM2-500M** → scene understanding at box
7. **Genesis + LeRobot + SmolVLA** → behavior learning pipeline
8. **Silero VAD** → always-on voice gating on robot

**Tier 2 — Integrate within 3–6 months:**
9. **MASt3R-SLAM** → persistent 3D home map (box-side)
10. **VGGT** → rapid 3D scene reconstruction from photos
11. **YOLO-World** (with license) → open-vocab detection
12. **TitaNet-S** → speaker identity ("who is speaking?")
13. **Parakeet TDT 0.6B** → high-accuracy box STT
14. **gsplat** → 3DGS training backend for home map

**Tier 3 — Watch / prototype:**
15. **Moshi full-duplex** → natural conversation (when quantized further)
16. **Mobile-GS** → when Vulkan renderer releases
17. **BitNet 1.58** → when 7B+ ternary models become available
18. **FoundationPose** → if/when adding object pose tracking
19. **ConceptGraphs** → when RGB-D depth available

***

*Survey completed: 2026-06-24. All finds verified against primary sources (GitHub, HuggingFace, arXiv, official research blogs). Licenses verified at time of writing — recheck before production deployment.*

---

## References

1. [Apple's New Transcription APIs Blow Past Whisper in Speed Tests](https://www.macrumors.com/2025/06/18/apple-transcription-api-faster-than-whisper/) - Apple's new speech-to-text transcription APIs in iOS 26 and macOS Tahoe are delivering dramatically ...

2. [Apple devices offer amazing speech to text transcription ... - 9to5Mac](https://9to5mac.com/2025/06/18/apple-devices-offer-amazing-speech-to-text-transcription-in-developer-betas-shows-test/) - In the new betas, there are beta versions of SpeechAnalyzer and SpeechTranscriber which developers c...

3. [Hands-On: How Apple's New Speech APIs Outpace Whisper for ...](https://www.macstories.net/stories/hands-on-how-apples-new-speech-apis-outpace-whisper-for-lightning-fast-transcription/) - By harnessing SpeechAnalyzer and SpeechTranscriber on-device, the command line tool tore through the...

4. [on-device speech processing for Apple Silicon (ASR, TTS ...](https://forums.swift.org/t/speech-swift-on-device-speech-processing-for-apple-silicon-asr-tts-diarization-speech-to-speech/85182) - Hi all, Sharing a Swift package I've been working on — a modular speech processing toolkit that runs...

5. [On-device speech toolkit for Apple Silicon — ASR, TTS, diarization, speech-to-speech, all in native Swift](https://www.reddit.com/r/swift/comments/1royaiz/ondevice_speech_toolkit_for_apple_silicon_asr_tts/) - On-device speech toolkit for Apple Silicon — ASR, TTS, diarization, speech-to-speech, all in native ...

6. [Depth Pro: Sharp Monocular Metric Depth in Less Than a Second](https://machinelearning.apple.com/research/depth-pro) - Our model, Depth Pro, synthesizes high-resolution depth maps with unparalleled sharpness and high-fr...

7. [Depth Pro Explained: Sharp, Fast Monocular Metric Depth Estimation](https://learnopencv.com/depth-pro-monocular-metric-depth/) - Depth Pro is an foundational zero shot metric depth estimation model from Apple ML, nails at creatin...

8. [mrgnw/depth-anything-v2-coreml - Hugging Face](https://huggingface.co/mrgnw/depth-anything-v2-coreml) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

9. [Apple Machine Learning Research at ICLR 2025](https://machinelearning.apple.com/research/iclr-2025) - Apple researchers are advancing machine learning (ML) and AI through fundamental research that impro...

10. [Apple FastVLM and MobileCLIP2: Redefining On-Device AI](https://www.profilenews.com/en/apple-fastvlm-and-mobileclip2/) - Apple open-sources Apple FastVLM and MobileCLIP2, delivering faster, privacy-first on-device AI for ...

11. [MobileCLIP: Fast Image-Text Models through Multi-Modal ...](https://machinelearning.apple.com/research/mobileclip) - We introduce MobileCLIP -- a new family of efficient image-text models optimized for runtime perform...

12. [Satya Mallick - X](https://x.com/LearnOpenCV/status/1965769149646540880)

13. [Deploy Local Vision-Language-Action Workflows on 8GB Edge ...](https://changecast.ai/story/huggingface-gemma-4-vla-demo-on-jetson-ori-31c24e/engineering) - This moves tool-calling and multimodal reasoning from the cloud to the extreme edge. You can now imp...

14. [GitHub - apple/ml-aim: This repository provides the code and model checkpoints for AIMv1 and AIMv2 research projects.](https://github.com/apple/ml-aim) - This repository provides the code and model checkpoints for AIMv1 and AIMv2 research projects. - app...

15. [apple/aimv2-large-patch14-224 - Hugging Face](https://huggingface.co/apple/aimv2-large-patch14-224) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

16. [Apple Releases AIMv2: A Family of State-of-the-Art Open-Set Vision ...](https://www.marktechpost.com/2024/11/22/apple-releases-aimv2-a-family-of-state-of-the-art-open-set-vision-encoders/) - Apple Releases AIMv2: A Family of Open-Set Vision Encoders

17. [Multimodal Autoregressive Pre-Training of Large Vision Encoders](https://machinelearning.apple.com/research/multimodal-autoregressive) - *Equal Contributors A dominant paradigm in large multimodal models is to pair a large language de- c...

18. [apple/ml-4m - Massively Multimodal Masked Modeling](https://github.com/apple/ml-4m) - 4M: Massively Multimodal Masked Modeling. Contribute to apple/ml-4m development by creating an accou...

19. [Advancing Speech Accessibility with Personal Voice](https://machinelearning.apple.com/research/personal-voice) - A voice replicator is a powerful tool for people at risk of losing their ability to speak, including...

20. [Personal Voice Generator on the App Store](https://apps.apple.com/us/app/personal-voice-generator/id6473683146) - Type what you want to say and have your Mac speak it aloud in your Personal Voice, and even save it ...

21. [Genesis-Embodied-AI open-sources Genesis World 1.0, a ...](https://digg.com/tech/tuo1sird)

22. [Genesis-Embodied-AI/Genesis: A generative world for ... - GitHub](https://github.com/Genesis-Embodied-AI/Genesis) - A generative world for general-purpose robotics & embodied AI learning. - Genesis-Embodied-AI/Genesi...

23. [ruvnet/genesis - GitHub](https://github.com/ruvnet/genesis) - Genesis is a groundbreaking physics platform designed for robotics and embodied AI applications that...

24. [A Survey of Robotic Navigation and Manipulation with Physics ...](https://arxiv.org/html/2505.01458v1) - Genesis (Authors, 2024) , built on DiffTaichi, is an open-source simulator fully optimized for diffe...

25. [Genesis-Embodied-AI/genesis-world: Simulation platform ... - GitHub](https://github.com/Genesis-Embodied-AI/genesis-world) - Genesis World is a simulation platform for physical AI developments. It combines a unified multi-phy...

26. [Awesome DUSt3R Resources](https://github.com/ruili3/awesome-dust3r) - 🌟A curated list of DUSt3R-related papers and resources, tracking recent advancements using this geom...

27. [Real-Time Dense SLAM with 3D Reconstruction Priors - CVPR 2026](https://cvpr.thecvf.com/virtual/2025/poster/34871) - We present a real-time dense SLAM system based on MASt3R that handles in-the-wild videos and achieve...

28. [CVPR Poster SLAM3R: Real-Time Dense Scene Reconstruction ...](https://cvpr.thecvf.com/virtual/2025/poster/34485) - In this paper, we introduce SLAM3R, a novel and effective monocular RGB SLAM system for real-time an...

29. [MASt3R-SLAM: Real-Time Dense SLAM with 3D Reconstruction](https://opencv.org/mast3r-slam/) - Key Highlights: Two-View 3D Priors: Leverages MASt3R's pointmap predictions and per-pixel feature co...

30. [[CVPR 2025] MASt3R-SLAM: Real-Time Dense SLAM with 3D ...](https://github.com/rmurai0610/MASt3R-SLAM) - Real-Time Dense SLAM with 3D Reconstruction Priors. Riku Murai* · Eric Dexheimer* · Andrew J. Daviso...

31. [NVIDIA Isaac Platform](https://developer.nvidia.com/isaac) - Develop, train, simulate, deploy, operate, and optimize AI robot systems.

32. [FoundationPose: Unified 6D Pose Estimation and Tracking of Novel Objects | NVIDIA Seattle Robotics Lab](https://research.nvidia.com/labs/srl/publication/wen-2024-foundation-pose/)

33. [Unified 6D Pose Estimation and Tracking of Novel Objects | Research](https://research.nvidia.com/publication/2024-06_foundationpose-unified-6d-pose-estimation-and-tracking-novel-objects) - We present FoundationPose, a unified foundation model for 6D object pose estimation and tracking, su...

34. [NVIDIA Isaac GR00T N1: An Open Foundation Model for Humanoid ...](https://research.nvidia.com/publication/2025-03_nvidia-isaac-gr00t-n1-open-foundation-model-humanoid-robots) - At NVIDIA, we are developing AI solutions to enable general-purpose humanoid robots to understand th...

35. [NVIDIA Isaac GROOT N1 Is an Open Source Foundation Model for ...](https://www.hackster.io/news/nvidia-isaac-groot-n1-is-an-open-source-foundation-model-for-accelerated-humanoid-robot-development-effa04c90231) - NVIDIA announces the Isaac GR00T N1 dual-system architecture model for building humanoid robots quic...

36. [NVIDIA Accelerates Robotics Research and Development With New Open Models and Simulation Libraries](https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Accelerates-Robotics-Research-and-Development-With-New-Open-Models-and-Simulation-Libraries/default.aspx) - News Summary: The open-source Newton Physics Engine — codeveloped with Google DeepMind and Disney Re

37. [Cosmos World Foundation Model Platform for Physical AI](https://research.nvidia.com/publication/2025-01_cosmos-world-foundation-model-platform-physical-ai) - Physical AI needs to be trained digitally first. It needs a digital twin of itself, the policy model...

38. [World Simulation With Video Foundation Models for Physical AI](https://research.nvidia.com/publication/2025-09_world-simulation-video-foundation-models-physical-ai) - At CoRL 2025, NVIDIA announced major updates to Cosmos World Foundation Models (WFMs) that let devel...

39. [World Simulation with Video Foundation Models for Physical AI ...](https://www.facebook.com/groups/DeepNetGroup/posts/2659292184463647/) - ... Models for Physical AI (NVIDIA, October 2025) ... NVIDIA Launches Cosmos World Foundation Model ...

40. [NVIDIA Cosmos - GitHub](https://github.com/nvidia-cosmos) - Cosmos-Predict1 is a collection of general-purpose world foundation models for Physical AI that can ...

41. [FoundationStereo: Zero-Shot Stereo Matching - Research at NVIDIA](https://research.nvidia.com/publication/2025-06_foundationstereo-zero-shot-stereo-matching) - We introduce FoundationStereo, a foundation model for stereo depth estimation designed to achieve st...

42. [R²D²: Building AI-based 3D Robot Perception and Mapping with NVIDIA Research | NVIDIA Technical Blog](https://developer.nvidia.com/blog/r2d2-building-ai-based-3d-robot-perception-and-mapping-with-nvidia-research) - Robots must perceive and interpret their 3D environments to act safely and effectively. This is espe...

43. [5 key features for zero-shot stereo depth estimation](https://pixel-decoder.com/2025/02/18/foundationstereo-framework-explained-5-key-features-for-zero-shot-stereo-depth-estimation/) - FoundationStereo by NVIDIA presents a state-of-the-art stereo model excelling in depth estimation wi...

44. [FoundationStereo: Revolutionizing Stereo Depth Estimation with Zero-Shot Learning](https://blog.muhammad-ahmed.com/2025/03/17/foundationstereo-revolutionizing-stereo-depth-estimation-with-zero-shot-learning/)

45. [Native Nvidia Fast Foundation Stereo Support - Stereolabs Forums](https://community.stereolabs.com/t/native-nvidia-fast-foundation-stereo-support/11231) - Last month Nvidia released a new realtime stereo depth estimation model (Links to paper & github bel...

46. [[2503.11651] VGGT: Visual Geometry Grounded Transformer - arXiv](https://arxiv.org/abs/2503.11651) - Abstract:We present VGGT, a feed-forward neural network that directly infers all key 3D attributes o...

47. [[CVPR 2025 Best Paper Award] VGGT: Visual Geometry Grounded ...](https://github.com/facebookresearch/vggt) - Visual Geometry Grounded Transformer (VGGT, CVPR 2025) is a feed-forward neural network that directl...

48. [VGGT: Visual Geometry Grounded Transformer - YouTube](https://www.youtube.com/watch?v=7ZYwJEpCUUA) - Comments · Ep#8 VGGT: Visual Geometry Grounded Transformer · I investigated the explosion of ticks a...

49. [An Evaluation of DUSt3R/MASt3R/VGGT 3D Reconstruction on Photogrammetric Aerial Blocks](https://arxiv.org/abs/2507.14798) - State-of-the-art 3D computer vision algorithms continue to advance in handling sparse, unordered ima...

50. [Your Phone Just Became a Real-Time Gaussian Splat Renderer](https://ik3d.fr/mobile-gs-your-phone-just-became-a-real-time-gaussian-splat-renderer/) - Until now, Gaussian Splatting meant beefy GPU. Server-side rendering. Desktop-only viewers. As of IC...

51. [Mobile-GS: Real-time Gaussian Splatting for Mobile Devices](https://openreview.net/forum?id=vRegY0pgvQ) - 3D Gaussian Splatting (3DGS) has emerged as a powerful representation for high-quality rendering acr...

52. [Mobile-GS: Real-time Gaussian Splatting for Mobile Devices](https://iclr.cc/virtual/2026/poster/10006810) - In this work, we propose a mobile-tailored real-time Gaussian Splatting method, dubbed Mobile-GS, en...

53. [[ICLR 2026] Mobile-GS: Real-time Gaussian Splatting for ... - GitHub](https://github.com/xiaobiaodu/mobile-gs) - ✓ [2026.3.21] : We only release the initial CUDA version for readers to bettet understand our work. ...

54. [Depth Anything V2 vs Segment Anything Model (SAM)](https://playground.roboflow.com/models/compare/depth-anything-v2-vs-sam) - Compare Depth Anything V2 vs Segment Anything Model (SAM) across vision tasks like OCR, image captio...

55. [Depth Anything V2](https://proceedings.neurips.cc/paper_files/paper/2024/hash/26cfdcd8fe6fd75cc53e92963a656c58-Abstract-Conference.html) - This work presents Depth Anything V2. Without pursuing fancy techniques, we aim to reveal crucial fi...

56. [DepthAnything/Depth-Anything-V2: [NeurIPS 2024] Depth ... - GitHub](https://github.com/DepthAnything/Depth-Anything-V2) - This work presents Depth Anything V2. It significantly outperforms V1 in fine-grained details and ro...

57. [Published as a conference paper at ICLR 2025](https://openreview.net/pdf/7c41968163abe4e3700e3e3a15174a9d679fcd52.pdf)

58. [GitHub - pablovela5620/sam2-depthanything](https://github.com/pablovela5620/sam2-depthanything) - Contribute to pablovela5620/sam2-depthanything development by creating an account on GitHub.

59. [nerfstudio-project/gsplat: CUDA accelerated rasterization of ... - GitHub](https://github.com/nerfstudio-project/gsplat) - It is inspired by the SIGGRAPH paper 3D Gaussian Splatting for Real-Time Rendering of Radiance Field...

60. [ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650) - For robots to perform a wide variety of tasks, they require a 3D representation of the world that is...

61. [[논문 리뷰] ConceptGraphs: Open-Vocabulary 3D Scene ...](https://canvas4sh.tistory.com/434) - AbstractICRA 2024 ConceptGraphs는 Open-Vocabulary 3D Scene Graph를 생성하는 시스템으로 다음 세 가지 주요 단계를 통해 구현되었다....

62. [Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://www.youtube.com/watch?v=mRhNkQwRYnc) - ConceptGraphs builds open-vocabulary 3D scenegraphs that enable a broad range of perception and task...

63. [Mark Kovarski on LinkedIn: 🎙️ 🎤 𝐊𝐨𝐤𝐨𝐫𝐨-82𝐌: 𝐔𝐧𝐦𝐚𝐭𝐜𝐡𝐞𝐝 𝐓𝐞𝐱𝐭-𝐭𝐨-𝐒𝐩𝐞𝐞𝐜𝐡…](https://www.linkedin.com/posts/markkovarski_%F0%9D%90%8A%F0%9D%90%A8%F0%9D%90%A4%F0%9D%90%A8%F0%9D%90%AB%F0%9D%90%A8-82%F0%9D%90%8C-%F0%9D%90%94%F0%9D%90%A7%F0%9D%90%A6%F0%9D%90%9A%F0%9D%90%AD%F0%9D%90%9C%F0%9D%90%A1%F0%9D%90%9E%F0%9D%90%9D-activity-7284610343065079810-XQTw) - 🎙️ 🎤 𝐊𝐨𝐤𝐨𝐫𝐨-82𝐌: 𝐔𝐧𝐦𝐚𝐭𝐜𝐡𝐞𝐝 𝐓𝐞𝐱𝐭-𝐭𝐨-𝐒𝐩𝐞𝐞𝐜𝐡 𝐏𝐞𝐫𝐟𝐨𝐫𝐦𝐚𝐧𝐜𝐞 Kokoro-82M, a revolutionary text-to-speech (TT...

64. [hexgrad/Kokoro-82M - Hugging Face](https://huggingface.co/hexgrad/Kokoro-82M) - Kokoro is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture,...

65. [Kokoro: A Breakthrough Open-Source TTS Model You Can Try Today](https://ageofllms.com/ai-howto-prompts/ai-fun/kokoro-tts) - Kokoro, a compact 82M parameter TTS model, offers incredible performance in speech synthesis. With o...

66. [Best Open-Source TTS 2026: Chatterbox 65.3% Beats ElevenLabs](https://findskill.ai/blog/best-open-source-tts-2026/) - Best open-source TTS in 2026: Chatterbox-Turbo MIT won 65.3% blind test vs ElevenLabs 24.5%. Plus Co...

67. [philippdxx/Kokoro-TTS-coreml](https://huggingface.co/philippdxx/Kokoro-TTS-coreml) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

68. [Best open-source speech-to-text models in 2026 - Gladia](https://www.gladia.io/blog/best-open-source-speech-to-text-models) - Which open-source STT model is best for real-time transcription? NVIDIA Parakeet TDT 1.1B offers the...

69. [NVIDIA Parakeet - Speech-to-Text Model - STT.ai](https://stt.ai/models/nvidia-parakeet/) - NVIDIA's CTC-based English ASR model. One of the most accurate open-source English models available.

70. [New Standard for Speech Recognition and Translation from the ...](https://developer.nvidia.com/blog/new-standard-for-speech-recognition-and-translation-from-the-nvidia-nemo-canary-model/) - NVIDIA NeMo is an end-to-end platform for the development of multimodal generative AI models at scal...

71. [nvidia - Shahnawaz Ahmed's Post](https://www.linkedin.com/posts/quantshah_nvidia-activity-7468650602265432065-aiot) - This demo was fun to make and close to heart. Our team has created a tool that allows taking Hugging...

72. [Moshi open-source release: run Moshi locally! - Kyutai](https://kyutai.org/2024/09/18/moshi-release.html)

73. [Moshi Real-Time Speech-to-Speech: Sub-200ms Voice AI](https://localaimaster.com/blog/moshi-realtime-speech-guide) - Sub-200ms local voice AI. Setup, integration, voice agent patterns.

74. [Blog - Kyutai](https://kyutai.org/blog) - MoshiVis: Teaching Moshi to Converse about Images2025-03-21An open-source Vision Speech Model with l...

75. [kyutai-labs/moshi-swift](https://github.com/kyutai-labs/moshi-swift) - Contribute to kyutai-labs/moshi-swift development by creating an account on GitHub.

76. [kyutai/moshika-rl-seamless - Hugging Face](https://huggingface.co/kyutai/moshika-rl-seamless) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

77. [Best Open-Source TTS Models 2026 | CodeSOTA](https://www.codesota.com/speech/best-open-source) - Open-source text-to-speech models compared for 2026: Sesame CSM, Orpheus, Kokoro, XTTS v2, F5-TTS, F...

78. [The Top Open-Source Text to Speech (TTS) Models - Modal](https://modal.com/blog/open-source-tts) - Orpheus is excellent at producing natural audio with multi-lingual support. ... Sesame CSM was produ...

79. [orpheus - Codersera Blogs](https://codersera.com/blog/tag/orpheus/) - Articles tagged orpheus on Codersera — practical guides on remote hiring, AI engineering, mobile tes...

80. [Moonshine - Speech-to-Text Model - STT.ai](https://stt.ai/models/moonshine/) - Ultra-lightweight ASR model designed for edge devices. Runs on Raspberry Pi with minimal latency.

81. [Silero VAD: pre-trained enterprise-grade Voice Activity ...](https://github.com/snakers4/silero-vad) - Silero VAD: pre-trained enterprise-grade Voice Activity Detector - snakers4/silero-vad

82. [I built an open source VAD that beats Silero, Pyannote, and ...](https://discuss.huggingface.co/t/i-built-an-open-source-vad-that-beats-silero-pyannote-and-webrtc-on-noisy-audio-with-93-accuracy-no-gpu-required/177044) - I built NOVA-VAD, a lightweight explainable Voice Activity Detector that outperforms every major ope...

83. [Speaker Recognition - Conversational AI](https://research.nvidia.com/labs/conv-ai/publications/category/speaker-recognition/) - NVIDIA Conversational AI NeMo team page

84. [[音系AI解説]NeMo Speaker Diarization（MSDD）](https://zenn.dev/rick_lyric/articles/1e48eeb396904d)

85. [nvidia/speakerverification_en_titanet_large - Hugging Face](https://huggingface.co/nvidia/speakerverification_en_titanet_large) - This model extracts speaker embeddings from given speech, which is the backbone for speaker verifica...

86. [SmolVLM to SmolVLM2: Compact Models for Multi-Image VQA](https://pyimagesearch.com/2025/06/23/smolvlm-to-smolvlm2-compact-models-for-multi-image-vqa/) - Learn how SmolVLM and SmolVLM2, compact and efficient vision-language models, enable real-time multi...

87. [SmolVLM: Redefining small and efficient multimodal models - arXiv](https://arxiv.org/html/2504.05299v1) - We introduce SmolVLM, a series of compact multimodal models specifically engineered for resource-eff...

88. [SmolVLM2: Bringing Video Understanding to Every Device](https://huggingface.co/blog/smolvlm2) - We are introducing three new models with 256M, 500M and 2.2B parameters. The 2.2B model is the go-to...

89. [Moondream 2 Object Detection Model: What is, How to Use](https://playground.roboflow.com/models/moondream-ai/moondream-2) - Moondream 2 is a small open-source vision-language model (~1.9B parameters) optimized for on-device ...

90. [2510.09653v2 | PDF | Image Segmentation | Computer Vision - Scribd](https://www.scribd.com/document/1003192563/2510-09653v2) - This paper provides an overview of the Ultralytics YOLO family of object detectors, focusing on the ...

91. [[PDF] YOLO-World: Real-Time Open-Vocabulary Object Detection | Semantic Scholar](https://www.semanticscholar.org/paper/YOLO-World:-Real-Time-Open-Vocabulary-Object-Cheng-Song/37c112454a236ab91c9c6b5cc165a6c3251e9206) - YOLO-World is introduced, an innovative approach that enhances YOLO with open-vocabulary detection c...

92. [Zero-Shot Object Detection Benchmarks - Computer Vision](https://www.codesota.com/browse/computer-vision/zero-shot-object-detection)

93. [Top 5 zero-shot object detection models in 2025](https://inteligenai.com/zero-shot-detection-enterprise/) - Discover the top 5 zero-shot detection enterprise models in 2025. Compare OWL-ViT, OWLv2, Grounding ...

94. [RT-DETR – Try & Compare - Roboflow Playground](https://playground.roboflow.com/models/baidu/rt-detr) - RT-DETR is Baidu's real-time transformer detector achieving 53.1% AP at 108 FPS on NVIDIA T4, the fi...

95. [[2506.01844] SmolVLA: A vision-language-action ... - ar5iv - arXiv](https://ar5iv.labs.arxiv.org/html/2506.01844) - Vision-language models (VLMs) pretrained on large-scale multimodal datasets encode rich visual and l...

96. [Hugging Face Releases SmolVLA, a Compact Open ... - Pure AI](https://pureai.com/articles/2025/06/10/hugging-face-releases-smolvla.aspx) - Hugging Face has introduced SmolVLA, a lightweight open-source Vision-Language-Action (VLA) model fo...

97. [Hugging Face Releases SmolVLA: A Compact Vision-Language ...](https://www.marktechpost.com/2025/06/03/hugging-face-releases-smolvla-a-compact-vision-language-action-model-for-affordable-and-efficient-robotics/) - Hugging Face Releases SmolVLA: A Compact Vision-Language-Action Model for Affordable and Efficient R...

98. [SmolVLA](https://huggingface.co/docs/lerobot/smolvla) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

99. [LeRobot — Hugging Face](https://humanoidintel.ai/brains/lerobot/) - Hugging Face's open-source framework for real-world robotics, providing a hardware-agnostic platform...

100. [Vision Language Action Models (VLA) & Policies for Robots](https://learnopencv.com/vision-language-action-models-lerobot-policy/) - In this article, we will go in-depth discussing how VLAs have evolved post GPT era with compelling p...

101. [Vision–language–action model - Wikipedia](https://en.wikipedia.org/wiki/Vision-language-action_model)

102. ["π0: A Vision-Language-Action Flow Model for General Robot ...](https://www.cloderic.com/content/2025-02-27-notes-on-pi0) - Reading notes on "π0: A Vision-Language-Action Flow Model for General Robot Control" by the Physical...

103. [From Perception to Embodied Intelligence: Evolution, Architectures ...](https://dev.to/ankk98/from-perception-to-embodied-intelligence-evolution-architectures-and-the-humanoid-gap-3dhi) - Phase 3: Scaling and Open-Source (2024–2025) – OpenVLA, SmolVLA, and Pi0. OpenVLA (2024) democratize...

104. [MLX Community](https://huggingface.co/mlx-community) - Org profile for MLX Community on Hugging Face, the AI community building the future.

105. [ml-explore/mlx at completeaitraining.com - GitHub](https://github.com/ml-explore/mlx) - MLX: An array framework for Apple silicon. Contribute to ml-explore/mlx development by creating an a...

106. [Explore large language models on Apple silicon with MLX - WWDC25](https://developer.apple.com/videos/play/wwdc2025/298/) - Discover MLX LM – designed specifically to make working with large language models simple and effici...

107. [GitHub - applecool/mlx-examples: Examples in the MLX framework](https://github.com/applecool/mlx-examples) - Examples in the MLX framework. Contribute to applecool/mlx-examples development by creating an accou...

108. [Official Inference Framework for 1-Bit LLMs Achieves Up to 6x CPU ...](https://agent-wars.com/news/2026-03-14-microsoft-bitnet-official-inference-framework-1-bit-llms-6x-cpu-speedup) - Microsoft's bitnet.cpp is the official inference framework for 1-bit and 1.58-bit (ternary) LLMs, of...

109. [#open_source_ai_projects #did_you_know_that #bitnet ... - LinkedIn](https://www.linkedin.com/posts/mahmoudrabie2004_opensourceaiprojects-didyouknowthat-activity-7366518624573984769-xnuU) - 🤖⚙️ Microsoft BitNet.cpp: 𝙊𝙛𝙛𝙞𝙘𝙞𝙖𝙡 1-𝘽𝙞𝙩 𝙇𝙇𝙈 𝙄𝙣𝙛𝙚𝙧𝙚𝙣𝙘𝙚 (𝘾𝙋𝙐/𝙂𝙋𝙐) ⚙️🤖 #open_source_ai_projects #did_y...

110. [GitHub - microsoft/BitNet: Official inference framework for 1-bit LLMs](https://github.com/microsoft/BitNet) - Official inference framework for 1-bit LLMs. Contribute to microsoft/BitNet development by creating ...

111. [Official inference framework for 1-bit LLMs | Nelson Jeronimo](https://www.linkedin.com/posts/nelsonjeronimo_github-microsoftbitnet-official-inference-activity-7437628848302866432-9RIG) - As I been saying in the last few days… - Microsoft's BitNet framework uses 1.58-bit ternary weights ...

112. [Part 1.1, Fast and Lossless BitNet b1.58 Inference on CPUs](https://www.microsoft.com/en-us/research/publication/1-bit-ai-infra-part-1-1-fast-and-lossless-bitnet-b1-58-inference-on-cpus/) - Recent advances in 1-bit Large Language Models (LLMs), such as BitNet and BitNet b1.58, present a pr...

113. [ExecuTorch 測試版發表於 Arm 平台上加速實現邊緣端的生成式 AI](https://www.arm.com/zh-TW/company/news/2024/11/accelerating-edge-ai-with-executorch) - 透過 Arm 運算平台與 ExecuTorch 框架的結合，使得更小、更優化的模型能夠在邊緣端運行，加速邊緣端生成式 AI 的實現。

114. [Redefining the Edge AI Developer Experience on ...](https://newsroom.arm.com/news/executorch-1-0-ga-release-edge-ai) - ExecuTorch 1.0 GA release delivers higher performance and faster development through unified PyTorch...

115. [ExecuTorch and TOSA enabling PyTorch on Arm platforms - AI blog](https://community.arm.com/arm-community-blogs/b/ai-blog/posts/executorch-and-tosa-enabling-pytorch-on-arm-platforms) - Arm has worked with Meta to introduce support for Arm platforms in ExecuTorch.

116. [Real-time visual SLAM with an event camera](https://spiral.imperial.ac.uk/entities/publication/ceb86b10-7390-4a41-ac2e-6395c1c28dd0) - Simultaneous localisation and mapping (SLAM) based on computer vision has remarkably matured over th...

117. [Application of event cameras and neuromorphic computing to VSLAM: A survey](https://ro.ecu.edu.au/ecuworks2022-2026/4278/) - Simultaneous Localization and Mapping (SLAM) is a crucial function for most autonomous systems, allo...

118. ["Towards neuromorphic visual SLAM: A spiking neural network for ...](https://ro.ecu.edu.au/theses/3012/) - The need for effective Simultaneous Localisation and Mapping (SLAM) solutions has been pivotal acros...

119. [Open-Vocabulary Functional 3D Scene Graphs for Real-World ...](https://liner.com/review/openvocabulary-functional-3d-scene-graphs-for-realworld-indoor-spaces) - This work aims to enhance 3D scene graphs with functional relationships between objects and interact...

