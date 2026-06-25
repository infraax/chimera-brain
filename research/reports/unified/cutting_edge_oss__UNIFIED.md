# UNIFIED — Cutting-Edge Open-Source Models, Papers & Tools (2024–2026)
## Vector-Chimera Upgrade Intelligence · Fused report
### Source geodesic: `research/CUTTING_EDGE_OSS_GEODESIC.md`

> **What this is.** A fusion of the **two independent research runs** that answered the
> cutting-edge-OSS geodesic, merged into one document with nothing dropped:
> - **[C] = Claude** research agent — file `01_cutting_edge_oss__upgrade_survey.md`
>   ("Vector-Chimera Upgrade Survey: Genius-Engineering Gems"). Sources cited **inline**
>   (named outlets / HF cards), no numbered list.
> - **[P] = Perplexity Deep Research** — file `02_cutting_edge_oss__geodesic.md`
>   ("GEODESIC SURVEY"). Per-find **genius scores** (C/E/Q/F /5) and **119 numbered
>   references** (preserved verbatim at the bottom).
>
> Tags used below: **[Both]** both agents found it · **[C-only]** / **[P-only]** unique
> to one · **⚖️ DIVERGENCE** the two disagree (these are the most decision-relevant lines).
> Perplexity reference numbers are kept as `[P^n]`; Claude's inline sources are named in place.

---

## 0. THE HEADLINE: where the two models AGREE and DISAGREE

This is the part worth reading first — independent confirmation is strong signal, and the
disagreements are exactly where we must decide for ourselves.

### Strong agreement (both rank top-tier, "adopt now")
- **Kokoro-82M** = Vector's voice. Both score it the maximum. Apache-2.0, 82M, trained on
  <100 h audio, #1 TTS Spaces Arena, CoreML/ANE-friendly. **The single most-confirmed pick.**
- **VGGT** (Meta, CVPR 2025 Best Paper, Apache-2.0) = the 3D-mapping core. Both top-rank it;
  both explicitly call it the modern analogue of Anki's "one camera + physics" trick.
- **MLX + mlx-community** = the dock-box runtime if the box is Apple Silicon. Both max-score.
- **Depth Anything V2 (Small, Apache-2.0)** = always-on robot depth; ~30 FPS CoreML on ANE.
- **MASt3R-SLAM** = persistent dense home map (box, GPU). Both adopt (license caveat below).
- **SmolVLM2 (256M/500M)** = on-box/edge scene understanding. Both adopt.
- **SmolVLA-450M + LeRobot** = the realistic robot-learning entry point. Both adopt
  (with the caveat Vector's wheeled action space needs custom data).
- **Parakeet TDT 0.6B** = top box-side STT. **Silero VAD** = the gate. **TitaNet-S (6M)** =
  speaker ID. **Moonshine (37M)** = on-robot STT/wake. **Apple Depth Pro** = sharp metric
  depth (box). All adopted by both.

### ⚖️ The four real disagreements

| Topic | **[C] Claude** | **[P] Perplexity** | Our read |
|---|---|---|---|
| **Genesis simulator** | **SKIP / caution** — cites Stone Tao's independent Dec-2024 analysis: "**>100× slower than claimed**," 3–10× slower than existing GPU sims on realistic loads, drops to ~10× realtime with a camera on. Treat "430,000× / 43M FPS" as marketing. | **🥇 ADOPT NOW (19/20)** — "100× faster than real-time, up to 43M FPS," Apache-2.0, THE answer to "how does Vector learn behaviors." | **Both can be true:** the Dec-2024 *physics engine* is solid & reproducible; the *headline FPS* is benchmark-gamed. Adopt as a sim **tool**, but re-benchmark on our hardware and ignore the marketing numbers. Claude's skepticism is the safer default. |
| **Apple SpeechAnalyzer** | **CONDITIONAL** — excellent but **non-exportable**, macOS-26-only, never liftable to Jetson/Linux. | **🥇 ADOPT NOW (20/20)** — for the Mac-mini box specifically. | Agree on the fact (lock-in); differ on framing. **Adopt only if the box is macOS 26+**, else use Moonshine/Parakeet. |
| **Ultralytics YOLO11** | **SKIP for shipping** — AGPL-3.0 trap; use RT-DETRv2. | **ADOPT NOW** — but flags "commercial license needed." | Same fact, opposite verdict. For a shippable product, **Claude is right: prefer RT-DETRv2 / YOLOX** (Apache); only use YOLO11 if we buy the Ultralytics Enterprise license. |
| **Moonshine non-English** | Flags **non-English = non-commercial** (Moonshine Community License); English = MIT. | Lists it MIT, Q 3/5, English-focused. | Claude's license nuance is the load-bearing one — **English-only if commercial.** |

### Coverage difference (what one found and the other missed)
- **[P-only] finds:** Genesis World 1.0 (May 2026 generative layer), **Mobile-GS** (116 FPS
  3DGS on Snapdragon 8 Gen 3 in 4.8 MB — *Vulkan renderer NOT released*), **SLAM3R** (20+ FPS
  neural SLAM), **NOVA-VAD** (solo-dev VAD, 93% vs Silero 87% on noisy UrbanSound8K),
  **ConceptGraphs / OpenFunGraph** (open-vocab 3D scene graphs), **Apple Personal Voice**,
  **Sesame CSM-1B** & **Orpheus** detailed, **Event-camera / neuromorphic SLAM** (watch),
  **Grounded-SAM** (Grounding DINO + SAM2), **FoundationStereo** "Fast" variant.
- **[C-only] finds:** **ml-sharp** (Apple, Dec 2025, feed-forward Gaussian splat <1s),
  **UniDepth V2** (metric depth + self-promptable intrinsics), **EdgeSAM / MobileSAM /
  PicoSAM2** (robot-tier segmenters, EdgeSAM 26 ms on iPhone 14), **FluidAudio** (Apache-2.0
  Apple-silicon audio SDK, Parakeet ~110× RTF on M4 Pro), **ncnn / MNN** (+KleidiAI) runtimes,
  **Chatterbox** (Resemble AI, MIT, PerTh watermark), **Video Depth Anything**, **OpenELM /
  DCLM / MobileOne**, **Octo / RDT-1B**, the **DUSt3R→MASt3R→VGGT** lineage framing + fast
  forks (FastVGGT, LiteVGGT), and the **recency corrections** (Qwen2.5-VL ~18T not 22T tokens;
  Moondream "~450B tokens" = the 9B-MoE run).

---

## V1 — Apple's quiet high-tech drops

**The "hidden Mac audio model," resolved [Both, identical conclusion]:** it is Apple's
**SpeechAnalyzer + SpeechTranscriber** (WWDC June 10 2025; iOS 26 / macOS Tahoe, GA Sept 2025).
- [C] MacStories' John Voorhees: tore through a 7 GB video **2.2× faster than MacWhisper
  Large V3 Turbo** (0:45 vs 1:41), no quality loss. A `DictationTranscriber` exposes the older
  on-device model without Siri toggles.
- [P] Same benchmark via the *Yap* CLI: 7 GB / 34-min video in **45 s**, 2.2× MacWhisper. `[P^1][P^2][P^3]`
- **⚖️/agreement:** both stress **NOT exportable** — SDK-only, no ONNX/CoreML artifact, Apple-OS-26+ only.
  Claude → "CONDITIONAL"; Perplexity → "Adopt Now (box only)." Genius [P]: C5 E5 Q5 F5.

**Depth Pro** (`apple/ml-depth-pro`, Oct 2024, ICLR 2025) — **[Both]**
- Sharp zero-shot **metric** monocular depth, absolute scale w/o intrinsics. [C] <1 s; [P] 504M
  params, fits 6 GB VRAM, 0.3 s on V100, sharp 1536×1536. Decouples focal-length head from depth
  head. Community CoreML port ~30 ms on M4 Pro ANE. `[P^6][P^7][P^8][P^9]`
- Flag [Both]: **Apple Sample Code / research license**, not OSI Apache — verify commercial use;
  504M is box-side only. Genius [P]: C5 E4 Q5 F5.

**FastVLM + MobileCLIP/MobileCLIP2** (`apple/ml-fastvlm`, `apple/ml-mobileclip`) — **[Both]**
- [C] FastViTHD encoder: "**85× faster TTFT and 3.4× smaller vision encoder**" vs
  LLaVA-OneVision-0.5B (per Apple's HF card); 7.9× faster TTFT on the Qwen2-7B variant; runs
  in-browser on Apple Silicon. MobileCLIP2 is the encoder feeding FastVLM.
- [P] MobileCLIP S0=11M…S3=86M, 3–15 ms latency; "reinforced datasets" bake knowledge into
  data not model; FastVLM demoed on Jetson Orin Nano alongside Parakeet + Kokoro. `[P^10][P^11][P^12][P^13]`
- Flag [Both]: Apple ML Research License + HF token gate. Genius [P]: C4 E5 Q4 F5.

**AIMv2** (`apple/ml-aim`, Nov 2024, CVPR 2025 Highlight, **Apache-2.0**) — **[Both]**
- Multimodal autoregressive vision encoders beating CLIP/SigLIP/DINOv2 (89.5% frozen-trunk
  ImageNet); causal multimodal decoder generates image patches AND text tokens. `[P^14][P^15][P^16][P^17]` Genius [P]: C4 E3 Q5 F4.

**4M: Massively Multimodal** (`apple/ml-4m`, Apr 2024, **Apache-2.0**) — **[Both]**
- Any-to-any (RGB/depth/normals/seg/text/3D tokens). Future: one model for depth+seg+caption.
  Box-only (large). `[P^18]` Genius [P]: C5 E3 Q4 F3.

**[C-only] ml-sharp** (`apple/ml-sharp`, Dec 2025) — feed-forward Gaussian-splat 3D in <1 s;
could bootstrap a 3D model of Vector's surroundings on the box. Genius [C]: cleverness 5/efficiency 3/quality 4/fit 3.

**[C-only] OpenELM, DCLM, MobileOne** — Apple HF org, 2024–25, Apple licenses.

**[P-only] Personal Voice** (on-device TTS, iOS 17/macOS Sonoma, refined through 2025) —
records 15 min, trains overnight on-device, private; exportable via third-party app; English-only,
weights not portable. Use: Vector speaks in the owner's familiar voice via Live Speech API. `[P^19][P^20]` Genius [P]: C5 E5 Q4 F3.

**MLX framework + mlx-community** — **[Both]** (Claude lists under runtimes V7; Perplexity under V7 too — see V7).
[C] also notes community servers **macMLX** (Apache-2.0) and **vllm-mlx**.

**V1 honest flags [Both]:** Apple research licenses are *permissive-for-research, not OSI*;
SpeechAnalyzer/Personal Voice weights not extractable; FastVLM behind HF approval; Depth Pro not
metric-perfect on every surface.

---

## V2 — NVIDIA: simulated physics worlds + 3D perception

**⚖️ Genesis** — *the headline disagreement* (`Genesis-Embodied-AI`, Dec 2024 sim; World 1.0 May 2026)
- [P] **🥇 Adopt Now, Genius C5 E5 Q5 F5 (19/20).** Universal multi-physics sim (rigid/MPM/SPH/FEM/PBD/
  fluids) in one Pythonic API; World 1.0 adds the Quadrants compiler, penetration-free contact, the
  Nyx renderer; "100× faster than real-time, up to 43M FPS," fully differentiable; "1 h real testing
  = 100 sim days." THE behavior-learning answer. `[P^21][P^22][P^23][P^24][P^25]`
- [C] **SKIP / caution — "benchmark-gamed."** Stone Tao's independent Dec-2024 analysis: Genesis is
  "**slower by >100× than claimed**," 3–10× slower than existing GPU sims on collision-heavy scenes,
  and "if you turn on a camera … drops to just 10× realtime." Clever & easy-to-use, but treat the
  marketing FPS as unrepresentative.
- **Reconciliation:** physics engine = real and usable; FPS claims = inflated. Adopt as a sim tool,
  re-benchmark ourselves, distrust the numbers. (Perplexity itself concedes World 1.0's generative
  layer is "modular/partial.")

**MASt3R-SLAM / SLAM3R** — **[Both for MASt3R-SLAM; SLAM3R is P-only]**
- [P] MASt3R-SLAM = plug-and-play monocular dense SLAM, **15 FPS**, uncalibrated RGB, 2 ms matching
  via CUDA. SLAM3R = end-to-end neural SLAM, **20+ FPS**, regresses pointmaps directly, zero camera
  calibration. **License CC-BY-NC-4.0 (research only)** — commercial needs negotiation; needs a real
  GPU (not Orin Nano). `[P^26][P^27][P^28][P^29][P^30]` Genius [P]: C5 E4 Q5 F5.
- [C] lists MASt3R-SLAM under V3 (real-time dense metric map from one moving camera); flags GPU need.

**nvblox + cuVSLAM + FoundationPose** (NVIDIA Isaac) — **[Both]**
- nvblox: GPU TSDF/ESDF, ~100× faster than CPU, 2D costmap to 5 m, **Apache-2.0**. cuVSLAM: <1%
  trajectory error, Jetson-native (NVIDIA EULA). FoundationPose: zero-shot 6-DoF pose/track of novel
  objects (CAD or few refs), handles textureless/glossy. `[P^31][P^32][P^33]` Genius [P]: C4 E4 Q5 F5.
- [C] groups these as "Isaac ROS perception" + adds **FoundationStereo, PyCuVSLAM**; verdict WATCH
  *only if the box is a Jetson Orin*.

**GR00T N1/N1.5/N1.6/N1.7 + Isaac Lab + Newton** — **[Both]**
- Dual-system (S1 fast action + S2 VLA planner) humanoid foundation model; +40% from synthetic
  (GR00T-Mimic/Dreams); 780k trajectories in 11 h. **Both: aspirational/skip for Vector** —
  humanoid embodiment gap too large; architecture/sim-to-real pipeline is the takeaway. [C] adds
  Isaac Lab + **Newton physics** (NVIDIA×DeepMind×Disney on Warp/MJX, MuJoCo-Warp >70× speedup).
  `[P^34][P^35][P^36]` Genius [P]: C4 E2 Q4 F2.

**Cosmos 2.5 (World Foundation Models)** — **[Both]** — physics-aware synthetic-data generator;
Cosmos-Transfer2.5 3.5× smaller than v1. **Both: skip-for-now**, cloud-scale GPU, data-gen not
on-robot. `[P^37][P^38][P^39][P^40]` Genius [P]: C4 E2 Q4 F2.

**FoundationStereo** (NVIDIA, CVPR 2025 Best-Paper nominee) — **[Both]** — zero-shot stereo depth,
1M+ synthetic pairs, side-tunes DepthAnythingV2 priors. [C] notes a community **"Fast-FoundationStereo"**
approaching real-time; useful only if Vector gets a second camera. `[P^41][P^42][P^43][P^44][P^45]` Genius [P]: C5 E3 Q5 F4.

**[C-only] Parakeet/Canary STT** also listed by Claude under V2 (see V4).

**V2 honest flags [Both]:** GR00T humanoid-first; Cosmos cloud-scale; Isaac Lab powerful but complex
(NVIDIA GPU + Omniverse deps).

---

## V3 — 3D reconstruction, Gaussian splatting & spatial AI

**VGGT** (Meta, CVPR 2025 **Best Paper**, **Apache-2.0**, ~300M–1B) — **[Both, 🥇]**
- One feed-forward transformer → camera intrinsics+extrinsics, depth, point maps, 3D tracks from
  1…hundreds of views in <1 s, no optimization. Alternating global/frame-wise attention; 50× faster
  than optimization methods. [Both flag] declining reliability on *hundreds* of views — best at 2–50
  (which fits home-scale). [C] frames the **DUSt3R→MASt3R→VGGT** lineage + fast forks (FastVGGT,
  LiteVGGT, streaming O(1), VGGT-SLAM). `[P^46][P^47][P^48][P^49]` Genius [P]: C5 E5 Q5 F5.

**[P-only] Mobile-GS** (ICLR 2026) — real-time 3DGS at **116 FPS on Snapdragon 8 Gen 3** in a
**4.8 MB** model; kills the depth-sort bottleneck with a learned order-independent renderer + opacity
MLP; 3-stage compression GB→4.8 MB. **⚠ Vulkan mobile renderer NOT released (company policy)** — only
CUDA reference is open, so direct porting is blocked. `[P^50][P^51][P^52][P^53]` Genius [P]: C5 E5 Q5 F4.

**Depth Anything V2** (NeurIPS 2024; Small/Base/Large **Apache-2.0**, Giant 1.3B CC-BY-NC) — **[Both]**
- Synthetic-only teacher → 62M pseudo-labeled real images for the student; >10× faster than Marigold;
  CoreML Small ~30 FPS on ANE. Relative (not metric) depth; metric is a fine-tune. [C] adds **Video
  Depth Anything** (Jan 2025, temporal consistency). `[P^54][P^55][P^56][P^8]` Genius [P]: C4 E5 Q4 F5.

**SAM 2** (Meta, ICLR 2025, **Apache-2.0**) — **[Both]** — unified image+video seg with streaming
memory; pair with Depth Anything V2 for 3D object tracking (`pablovela5620/sam2-depthanything`).
[C] adds robot-tier **EdgeSAM / MobileSAM / PicoSAM2** (EdgeSAM 26 ms iPhone 14, 37× faster than SAM).
`[P^57][P^58]` Genius [P]: C4 E3 Q5 F4.

**gsplat** (nerfstudio, **Apache-2.0**) — **[Both]** — CUDA 3DGS rasterizer, 4× less memory + 15%
faster training vs reference 3DGS; the standard splat backend. `[P^59]` Genius [P]: C4 E4 Q4 F4.

**[P-only] ConceptGraphs** (ICRA 2024, **MIT**) — open-vocab 3D scene graph from RGB-D + poses via
2D VLMs; natural-language queries over 3D space ("where is the blue mug?"); needs a depth sensor.
`[P^60][P^61][P^62]` Genius [P]: C5 E3 Q4 F4.

**[C-only] UniDepth V2** (Feb 2025) — universal monocular **metric** depth with a self-promptable
camera module (predicts intrinsics) + uncertainty output. Genius [C]: 5/4/4/4.

**V3 honest flags [Both]:** Mobile-GS Vulkan unreleased; VGGT weak on large image sets (combine with
SfM); ConceptGraphs needs RGB-D (pair with a depth model for Vector's mono camera).

---

## V4 — On-device audio (STT / TTS / denoise / VAD / diarization / emotion)

**Kokoro-82M** (hexgrad, Dec 2024, **Apache-2.0**) — **[Both, 🥇 = THE Vector voice]**
- 82M, <100 h training, #1 TTS Spaces Arena, beats XTTS-v2 (467M)/MetaVoice (1.2B)/Parler. 90–210×
  realtime; CPU + Mac M-series; ONNX + community **Kokoro-TTS-coreml** (~45 ms ANE per [C]). 54 voice
  packs. [C] warns **kokorottsai[.]com and clones are scams — only `hexgrad/Kokoro-82M` is genuine.**
  `[P^63][P^64][P^65][P^66][P^67]` Genius [P]: C5 E5 Q5 F5.

**Parakeet TDT 0.6B / 1.1B** (NVIDIA NeMo, **CC-BY-4.0**, commercial-OK-with-attribution) — **[Both]**
- Top Open-ASR-Leaderboard English; RTFx >2000 on GPU; Fast-Conformer ~3× compute / ~4× memory
  savings; INT8 TensorRT 1.82× on Jetson AGX Orin; community CoreML Swift wrapper. `[P^68][P^69][P^70][P^71][P^4]` Genius [P]: C4 E4 Q5 F5.

**Moonshine** (Useful Sensors) — **[Both]**
- ⚖️ License nuance: [C] **English MIT; non-English = Moonshine Community License (non-commercial)**;
  [P] lists MIT, English-focused. [C] 27M–245M, variable-length encoder (no 30 s zero-pad), 802 ms on
  Pi5, beats Whisper-L-v3 on WER; v2 streaming Feb 2026. [P] 37M Tiny/61M Base, 7.8% WER, ergodic
  streaming encoder. **On-robot wake/command STT.** `[P^80][P^68]` Genius [P]: C5 E5 Q3 F5.

**Moshi + Kyutai STT/TTS** (Kyutai) — **[Both]**
- Moshi: full-duplex speech-to-speech, sub-200 ms, native speech tokens via Mimi codec (no
  STT→LLM→TTS). [C] CC-BY but card says "research only," ~7B; [P] Apache-2.0, lists **MoshiVis**
  (image chat, Mar 2025), **moshi-swift** MLX port, **moshika-rl-seamless** (better turn-taking).
  Kyutai TTS [C] "1.6B = actually ~1.8B," + **Pocket TTS** (Jan 2026, CPU voice clone). **Both: WATCH**
  (7B heavy, box-only now). `[P^72][P^73][P^74][P^75][P^76]` Genius [P]: C5 E3 Q4 F4.

**[P-detailed] Sesame CSM-1B** (Feb 2025, Apache-2.0) — context-aware conversational TTS, Llama
backbone + codec. `[P^77][P^78]` · **Orpheus TTS** (Canopy Labs, Mar 2025, Apache-2.0, 150M–3B) —
Llama-based, emotion tags (laugh/sigh/sniffle), zero-shot clone, streaming. `[P^79][P^77][P^78]`
(Both appear in [C] too as TTS options.) Genius [P]: CSM 4/3/4/4; Orpheus 4/4/4/4.

**[C-only] Chatterbox** (Resemble AI, May 2025; Turbo 350M + Multilingual v3 Jun 2026, **MIT**) —
sub-200 ms / RTF ~0.5 on RTX 4090, CUDA/ROCm/Apple-MPS, good zero-shot clone; mandatory **PerTh
watermark** (provenance only). [C] verdict WATCH (voice cloning).

**DeepFilterNet3 / GTCRN** (denoise) — **[Both]** — real-time speech enhancement, sub-ms latency;
DeepFilterNet **MIT** ~2–8M; **GTCRN** the genius pick at *tens of thousands* of params (7.8 GMACs/s).
`[P^—]` Genius [P]: C4 E5 Q4 F5.

**Silero VAD + [P-only] NOVA-VAD** — **[Both for Silero]** — Silero **MIT**, ~1 MB, CPU real-time, the
standard gate. [P-only] **NOVA-VAD** (solo dev, HF, Jun 2026): **93% vs Silero 87%** on noisy
UrbanSound8K, no GPU, feature-level explainability — textbook "solo dev beats big drop." `[P^81][P^82]` Genius [P]: C4 E5 Q4 F5.

**NeMo TitaNet** (speaker ID/diarization, **CC-BY-4.0**, 23M Large / **6M Small**) — **[Both]** —
EER 0.68% VoxCeleb1, DER 1.73% AMI; channel-attention statistics pooling; "who is speaking" (owner vs
guest); CoreML port. [C] also lists **pyannote.audio** and **3D-Speaker**. `[P^83][P^84][P^85][P^4]` Genius [P]: C4 E5 Q5 F5.

**emotion2vec / emotion2vec+** (ACL 2024, **MIT**, ~19–20M) — **[Both]** — self-supervised "Whisper
for emotion," 9-class SER; revives Vector's affective-response loop from voice tone. Genius [C]: 5/5/4/5.

### V4 shortlist (Perplexity's table, preserved)
| Role | Winner | Size | License | Edge fit |
|---|---|---|---|---|
| STT (box) | Parakeet TDT 0.6B | 0.6B | CC-BY-4.0 | Box / Jetson |
| STT (robot) | Moonshine Tiny | 37M | MIT | Robot |
| TTS (voice) | **Kokoro-82M** | 82M | Apache-2.0 | Box + CPU |
| TTS (expressive) | Orpheus 400M | 400M | Apache-2.0 | Box |
| Full-duplex | Moshi | 7B | Apache-2.0 | Box only |
| Denoise/AEC | DeepFilterNet3 | ~2M | MIT | Robot |
| VAD | Silero / NOVA-VAD | 1–2 MB | MIT | Robot |
| Speaker ID | TitaNet-S | 6M | CC-BY-4.0 | Robot/Box |
| Emotion | emotion2vec | ~20M | MIT | Box |

---

## V5 — Small/efficient vision & VLMs

**SmolVLM2** (HF, Feb 2025, **Apache-2.0**, 256M/500M/2.2B) — **[Both, 🥇 P]** — smallest video LM ever;
2.2B beats Qwen2-VL-7B on WorldSense; aggressive pixel-shuffle token compression. [C] stresses the
"**RAM, not params, is the real edge metric**" argument; 256M/500M run on Jetson Orin Nano. `[P^86][P^87][P^88][P^12]` Genius [P]: C5 E5 Q4 F5.

**Moondream 2 / 3** (Apache-2.0; MD2 1.9B, MD3 9B-MoE/2B-active) — **[Both]** — "max intelligence per
compute"; [C] int4 = "42% memory reduction, 0.6% accuracy drop," 5M+ monthly HF downloads, genuine
zero-shot detection; [C] notes MD3 "~450B tokens" RL run vs Qwen2.5-VL's ~18T pretraining. `[P^89][P^87]` Genius [P]: C4 E5 Q4 F5.

**⚖️ YOLO11 + YOLO-World** (Ultralytics **AGPL-3.0**) — **[Both, opposite verdicts]** — YOLO11n 2.6M,
39.5% mAP ~56 ms CPU; YOLO-World open-vocab 52 FPS / 35.4 AP LVIS zero-shot, re-parameterizes text
embeddings at inference. **[C] SKIP for shipping (AGPL trap) → use RT-DETRv2.** **[P] Adopt Now** with
"commercial license needed." `[P^90][P^91][P^92][P^93][P^94]` Genius [P]: C4 E5 Q4 F5.

**Florence-2** (Microsoft, **MIT**, 230M/770M) — **[Both]** — unified detect/seg/ground/caption/OCR in
one pass. [C] also lists **Qwen2.5-VL-3B**. `[P^92][P^93]` Genius [P]: C4 E4 Q4 F4.

**InsightFace / ArcFace (+ [C] AdaFace)** (**MIT** lib) — **[Both]** — face detect+recognize, <10 ms GPU;
"is this my owner?" `[P^—]` Genius [P]: C4 E4 Q5 F5.

**RTMPose** (OpenMMLab, **Apache-2.0**) — **[Both]** — real-time multi-person pose, 13+ FPS CPU,
whole-body; gestures/body language. [C] also lists **MediaPipe**. `[P^—]` Genius [P]: C4 E5 Q4 F4.

**[C-only] EdgeSAM / MobileSAM / PicoSAM2** — robot-tier segmenters (also in V3 above).

**V5 honest flags [Both]:** Ultralytics AGPL needs Enterprise license; InsightFace per-model licenses
vary; tiny-VLM "edge" claims assume an actively-cooled Orin Nano, not a passive MCU.

---

## V6 — Robotics learning & embodied policies

**SmolVLA-450M** (HF, Jun 2025, **Apache-2.0**) — **[Both, 🥇]** — matches π0 (3.3B) on LIBERO (87.3%)
at 10× smaller; async inference stack decouples perception/planning from action; fine-tune with ~50
episodes; pretrained on 10M frames / 487 community datasets. **The realistic way to teach Vector
skills.** `[P^95][P^96][P^97][P^98]` Genius [P]: C5 E5 Q5 F4.

**LeRobot** (HF, **Apache-2.0**) — **[Both]** — hardware-agnostic ACT/Diffusion/TDMPC/OpenVLA/π0/
SmolVLA + deploy tooling; the "HF Hub for robot behaviors"; [C] "SmolVLA fine-tunes in ~8 h on one
A100." `[P^99][P^100]` Genius [P]: C4 E4 Q4 F5.

**Genesis** (also V2) — [P] standalone robotics entry: `pip install genesis-world` → Vector kinematics
→ sim navigation/gripper. **See the ⚖️ Genesis divergence in V2.** `[P^21][P^22][P^25]`

**π0 / π0-FAST / π0.5** (Physical Intelligence) — **[Both]** — PaliGemma + flow-matching, 50 Hz, 8
embodiments; [P] not fully open (HF research gate), 3.3B/5B; **Both: skip** (manipulation-arm-centric;
SmolVLA is the practical equivalent). `[P^101][P^102][P^103]` Genius [P]: C5 E2 Q5 F2.

**OpenVLA** (UC Berkeley, **Apache-2.0**, 7B) — **[Both]** — beats RT-2-X (55B) with 7× fewer params
(970K demos); too big for box inference unless Q4-quantized. [C] also lists **Octo, RDT-1B**. `[P^103][P^101]` Genius [P]: C4 E3 Q4 F3.

**V6 honest flags [Both]:** all current VLAs assume manipulator action spaces; **Vector's wheeled
nav (wheels + tilt, no gripper) needs custom dataset collection.** Realistic path [both converge]:
**Genesis sim (train nav) → SmolVLA fine-tuned on recorded Vector demos → deploy via LeRobot** —
adopt only if/when Vector gets an actuated attachment.

---

## V7 — On-device runtimes & compression

**MLX + mlx-community** (Apple, **MIT**) — **[Both, 🥇]** — unified CPU+GPU memory (zero-copy), lazy
eval, JIT, autodiff; thousands of quantized models; MLX-LM/-VLM/-audio; WWDC25 session. **The Mac-mini
dock-box runtime.** `[P^104][P^105][P^106][P^107]` Genius [P]: C5 E5 Q5 F5.

**BitNet b1.58 + bitnet.cpp** (Microsoft; weights **Apache-2.0**, framework **MIT**) — **[Both, WATCH]**
- Ternary weights {−1,0,+1} → dot products become lookups; 2.37–6.17× x86 / 1.37–5.07× ARM speedup,
  up to 82% energy cut; 100B model at human reading speed on one CPU. **Flag [Both]:** quality holds
  only for *natively* BitNet-trained models; only the 2B-4T is open; Microsoft says **don't use
  commercially without further testing**; needs bespoke bitnet.cpp kernels. `[P^108][P^109][P^110][P^111][P^112]` Genius [P]: C5 E5 Q4 F4.

**ExecuTorch 1.0 GA** (Meta/ARM, Oct 2025, **BSD-3**) — **[Both]** — PyTorch on-device runtime; ARM
Cortex-A/-M, Ethos-U NPU, Qualcomm, Apple ANE; CMSIS-NN; 4-bit via KleidiAI ([C]: >350 tok/s prefill
on Arm). Export SmolVLA/Moonshine/YOLO → robot ARM board. `[P^113][P^114][P^115]` Genius [P]: C4 E5 Q4 F4.

**llama.cpp / GGUF** (**MIT**) — **[Both]** — universal LLM engine, Q4_K_M sweet spot; `llama-server`
Jinja tool-calling; community Jetson demo runs Gemma 4 + Parakeet + Kokoro on 8 GB. `[P^13]`

**TensorRT / Jetson** — **[Both]** — INT8 Parakeet 1.82×, 3× memory cut; nvblox/cuVSLAM native.
**ONNX Runtime** — **[Both]** — universal export target (CoreML/ARM/TensorRT backends).

**[C-only] ncnn (Tencent), MNN (Alibaba, +KleidiAI ~57% faster prefill on Arm), TFLite, CoreML,
FluidAudio** (Apache-2.0 Apple-silicon audio SDK — Parakeet ~110× RTF on M4 Pro, diarization, VAD,
Kokoro TTS, all ANE-offloaded). [C] quantization menu: int4/int8 GGUF, AWQ, GPTQ, **Matryoshka**
embeddings (adaptive-size retrieval vectors).

### V7 runtime recs by tier (Perplexity's table, preserved)
| Tier | Device | Best runtime | Best quant |
|---|---|---|---|
| Robot (ARM CPU) | companion board | ONNX RT / TFLite / ExecuTorch | INT8 / Q4 GGUF |
| Box (Mac mini) | Apple Silicon | **MLX** + llama.cpp + CoreML | 4-bit MLX / BitNet 1.58 |
| Box (Jetson) | NVIDIA | TensorRT INT8 + ONNX RT | INT8/FP16 TensorRT |
| Training | Cloud/Workstation | PyTorch + CUDA + Genesis | FP16/BF16 |

---

## V8 — Hidden gems & cross-domain genius

- **VGGT single-camera 3D** [Both] — "one camera, no calibration, no optimization loop" = the literal
  "Anki move of 2025." CVPR 2025 Best Paper, Apache-2.0.
- **[P] SLAM3R** — throws out 30 years of SfM/SLAM matrix decomposition; neural pointmap regression. `[P^28][P^26]`
- **Moonshine variable-length / ergodic streaming encoder** [Both] — compute scales with actual speech,
  37M on a Pi. `[P^80][P^68]`
- **[P] Mobile-GS 4.8 MB splat** — GB→4.8 MB + learned order-independent render (Vulkan unreleased). `[P^50][P^51][P^53]`
- **BitNet ternary** [Both] — multiply→lookup, −82% energy. `[P^110][P^108]`
- **[P] NOVA-VAD** — solo-dev, 93% vs Silero 87%, explainable, no GPU. `[P^82]`
- **[P] TitaNet-S 6M** — speaker ID in 6M params via channel-attention pooling. `[P^84][P^83]`
- **[P] Event cameras / neuromorphic SLAM** (watch) — µs-resolution, no frames/blur, low power; 2026
  SNN-SLAM thesis sub-metre ATE; hardware still $200–2000. `[P^116][P^117][P^118]`
- **[P] Grounded-SAM** (Grounding DINO + SAM2) — text→detect→segment→track, zero retraining; Grounding
  DINO 1.5 Pro 52%+ zero-shot COCO AP. `[P^92][P^93]`
- **[P] ConceptGraphs + OpenFunGraph** — RGB-D → language-labeled 3D object graph for LLM task planning. `[P^119][P^60][P^61]`
- **[C] GTCRN, emotion2vec, EdgeSAM/PicoSAM2, Kokoro-82M, FluidAudio, the DUSt3R→MASt3R→VGGT lineage +
  fast forks** — Claude's genius-tier "efficiency beats brute force" picks.

---

## FINAL SYNTHESIS — merged Adopt / Watch / Skip

Merged from both tables. **Score /20** is Perplexity's (C+E+Q+F). **Verdict** flags where the two
models split.

| Tool | Subsystem | [P] /20 | Merged verdict | License |
|---|---|---|---|---|
| Kokoro-82M | TTS / voice | 20 | **ADOPT (both)** | Apache-2.0 ✅ |
| VGGT | 3D mapping | 20 | **ADOPT (both)** | Apache-2.0 ✅ |
| MLX + mlx-community | Runtime (Apple box) | 20 | **ADOPT (both)** | MIT ✅ |
| Apple SpeechAnalyzer | STT (box) | 20 | ⚖️ **ADOPT [P] / CONDITIONAL [C]** — macOS-26-only, non-exportable | Apple SDK ⚠ |
| SmolVLA-450M | Robot policies | 19 | **ADOPT (both)** — needs Vector data | Apache-2.0 ✅ |
| SmolVLM2-500M | Scene understanding | 19 | **ADOPT (both)** | Apache-2.0 ✅ |
| MASt3R-SLAM | SLAM / map | 19 | **ADOPT (both, box GPU)** | CC-BY-NC-4.0 ⚠ |
| Silero VAD (+NOVA-VAD) | VAD / robot | 19 | **ADOPT (both)** | MIT ✅ |
| TitaNet-S | Speaker ID | 19 | **ADOPT (both)** | CC-BY-4.0 ⚠ |
| **Genesis** | Sim training | 19 | ⚖️ **ADOPT [P] / SKIP-caution [C]** (benchmark-gamed) | Apache-2.0 ✅ |
| Depth Anything V2 Small | Depth (robot) | 18 | **ADOPT (both)** | Apache-2.0 ✅ |
| LeRobot | Policy orchestration | 18 | **ADOPT (both)** | Apache-2.0 ✅ |
| Parakeet TDT 0.6B | STT (box) | 18 | **ADOPT (both)** | CC-BY-4.0 ⚠ |
| Moonshine Tiny | STT (robot) | 18 | **ADOPT (both)** — EN only if commercial | MIT (EN) / NC (non-EN) ⚠ |
| Apple Depth Pro | Metric depth (box) | 18 | **ADOPT (both)** | Apple research ⚠ |
| **YOLO11n + YOLO-World** | Detection | 18 | ⚖️ **ADOPT-w/license [P] / SKIP-for-shipping [C]** → prefer RT-DETRv2 | AGPL-3.0 ⛔ |
| FastVLM-0.5B | VLM (Apple) | — | **ADOPT (both)** | Apple research ⚠ |
| Moondream2 / MD3 | VLM | 18 (MD2) | **ADOPT (both)** | Apache-2.0 ✅ |
| EdgeSAM / SAM2 | Segmentation | 16 (SAM2) | **ADOPT (both)** | Apache-2.0 ✅ |
| gsplat | Splat training | 16 | **ADOPT (both)** | Apache-2.0 ✅ |
| FluidAudio / CoreML | Runtime (Apple) | — | **ADOPT [C]** | Apache ✅ |
| emotion2vec | Affect | — | **ADOPT (both)** | MIT ✅ |
| GTCRN / DeepFilterNet3 | Denoise | — | **ADOPT (both)** | MIT ✅ |
| Mobile-GS | 3D render | 19 | **WATCH [P]** — Vulkan unreleased | CUDA open / Vulkan ❌ |
| SLAM3R | Neural SLAM | 18 | **WATCH [P]** | check repo |
| nvblox + FoundationPose | 3D perception | 18 | **WATCH (both)** — Jetson box | Apache / EULA |
| BitNet b1.58 | LLM runtime | 18 | **WATCH (both)** — 2B only, immature | MIT/Apache |
| ExecuTorch 1.0 | ARM runtime | 17 | **WATCH (both)** — future robot deploy | BSD-3 ✅ |
| Moshi + Kyutai | Full-duplex voice | 17 | **WATCH (both)** — 7B, box-only | Apache-2.0 / CC-BY |
| FoundationStereo | Stereo depth | 17 | **WATCH (both)** — needs 2nd camera | NVIDIA research |
| Orpheus / Sesame CSM | Expressive/convo TTS | 17/16 | **WATCH (both)** — backup voices | Apache-2.0 ✅ |
| Chatterbox | Voice cloning | — | **WATCH [C]** — PerTh watermark | MIT ✅ |
| ConceptGraphs | Spatial memory | 17 | **WATCH [P]** — needs RGB-D | MIT ✅ |
| AIMv2 / 4M | Vision encoder / any-to-any | 16/15 | **WATCH (both)** | Apache-2.0 ✅ |
| Florence-2 | Multi-task vision | 16 | **WATCH (both)** | MIT ✅ |
| Event cameras / neuromorphic | Future perception | 18 | **WATCH [P]** — hardware maturing | hardware |
| Apple Personal Voice | TTS (owner voice) | — | **WATCH [P]** — non-exportable | Apple ⚠ |
| UniDepth V2 | Metric depth | — | **WATCH [C]** | open (verify) |
| GR00T N1.x | Humanoid policy | 13 | **SKIP-now (both)** — embodiment gap | NVIDIA Open Model |
| Cosmos 2.5 | Synthetic data | 12 | **SKIP-now (both)** — cloud-only | NVIDIA Open Model |
| π0 / π0-FAST | Arm manipulation | — | **SKIP (both)** — GPU + arm-centric | research gate |

---

## PRIORITY BUILD STACK (Perplexity's, kept) + staged recs (Claude's, kept)

**[P] Tier 1 — deploy today (Apache/MIT/CC-BY, reproducible):** MLX → Kokoro-82M → SpeechAnalyzer
(or Moonshine if not macOS) → Moonshine Tiny (robot) → Depth Anything V2 Small → SmolVLM2-500M →
Genesis+LeRobot+SmolVLA → Silero VAD.
**[P] Tier 2 (3–6 mo):** MASt3R-SLAM → VGGT → YOLO-World(license) → TitaNet-S → Parakeet 0.6B → gsplat.
**[P] Tier 3 (watch/prototype):** Moshi → Mobile-GS (when Vulkan) → BitNet (when 7B+) → FoundationPose → ConceptGraphs.

**[C] Stage 1 — perception + voice core:** Depth Anything V2 Small (robot) + Depth Pro (box);
Moondream2 / FastVLM-0.5B / SmolVLM2-500M; EdgeSAM + **RT-DETRv2** (not YOLO); audio loop
**Silero VAD → Moonshine(EN)/Parakeet → Kokoro** + GTCRN/DeepFilterNet + emotion2vec; runtime
**MLX + CoreML + FluidAudio** (Apple) or TensorRT/Isaac ROS (Jetson).
**[C] Stage 2 — spatial memory:** gsplat + MASt3R-SLAM/VGGT; benchmark FPS on the actual GPU first.
**[C] Stage 3 — watch:** BitNet (when bitnet.cpp matures), Kyutai (if FR/duplex), streaming/quantized
VGGT forks. LeRobot+SmolVLA only if Vector gains an actuated attachment.

**[C] benchmarks that would change the calls:** streaming VGGT/MASt3R >15 FPS on our box GPU →
promote to Stage 1; SpeechAnalyzer wake-word beats Moonshine AND box is macOS 26+ → use it;
BitNet defect rate acceptable on our command set → adopt onboard.

---

## COMBINED HONEST FLAGS / CAVEATS

- **License traps [Both]:** Ultralytics YOLO (AGPL-3.0); Moonshine non-English (NC); Moshi
  ("research only" despite CC-BY); Apple research licenses (not OSI); MASt3R-SLAM/SLAM3R (CC-BY-NC);
  Kyutai (CC-BY attribution); FluidAudio Apache but bundled weights vary (CC-BY vs Apache);
  Depth Anything Giant 1.3B (NC). **Verify per-model before shipping.**
- **Platform lock-in [Both]:** Apple SpeechAnalyzer/SpeechTranscriber/Personal Voice — macOS/iOS 26+
  only, never on Jetson/Linux.
- **⚖️ Benchmark gaming [C, strongest]:** Genesis "430,000× / 43M FPS" shown >100× off and 3–10×
  slower than existing GPU sims on realistic loads (Stone Tao, Dec 2024). Re-benchmark everything
  "Nx faster" on our own hardware. Mobile-GS Vulkan path unreleased.
- **Edge reality [Both]:** "runs on edge" for feed-forward 3D (VGGT/MASt3R) and most 2B+ VLMs assumes
  a GPU or actively-cooled Jetson Orin — not a passive MCU. Match tier (robot vs box) to model.
- **Recency corrections [C]:** Qwen2.5-VL pretraining ≈ 18T tokens (not 22T); Moondream "~450B tokens"
  = the 9B-MoE run, not MD2. Some 2026 arXiv refs are follow-on works confirming a lineage, not
  primary releases.

---

## APPENDIX A — Claude [C] inline sources (no numbered list in original)
Named outlets/cards cited by the Claude report: Apple HF model cards (FastVLM, Kokoro), Apple ML
Research blog (Depth Pro, MobileCLIP), MacStories (John Voorhees, SpeechAnalyzer hands-on), Stone Tao
independent Genesis benchmark analysis (Dec 2024), HF blog (SmolVLM2), moondream.ai, the DUSt3R/MASt3R/
VGGT papers, Useful Sensors (Moonshine), hexgrad HF (Kokoro), Resemble AI (Chatterbox), Kyutai
(Moshi/TTS), rikorose/DeepFilterNet, snakers4/silero-vad, ddlBoJack/emotion2vec, Ultralytics docs,
NVIDIA Isaac/Newton, Apple MLX + WWDC25, microsoft/BitNet, FluidInference/FluidAudio.

## APPENDIX B — Perplexity [P] references (1–119, verbatim)

1. https://www.macrumors.com/2025/06/18/apple-transcription-api-faster-than-whisper/
2. https://9to5mac.com/2025/06/18/apple-devices-offer-amazing-speech-to-text-transcription-in-developer-betas-shows-test/
3. https://www.macstories.net/stories/hands-on-how-apples-new-speech-apis-outpace-whisper-for-lightning-fast-transcription/
4. https://forums.swift.org/t/speech-swift-on-device-speech-processing-for-apple-silicon-asr-tts-diarization-speech-to-speech/85182
5. https://www.reddit.com/r/swift/comments/1royaiz/ondevice_speech_toolkit_for_apple_silicon_asr_tts/
6. https://machinelearning.apple.com/research/depth-pro
7. https://learnopencv.com/depth-pro-monocular-metric-depth/
8. https://huggingface.co/mrgnw/depth-anything-v2-coreml
9. https://machinelearning.apple.com/research/iclr-2025
10. https://www.profilenews.com/en/apple-fastvlm-and-mobileclip2/
11. https://machinelearning.apple.com/research/mobileclip
12. https://x.com/LearnOpenCV/status/1965769149646540880
13. https://changecast.ai/story/huggingface-gemma-4-vla-demo-on-jetson-ori-31c24e/engineering
14. https://github.com/apple/ml-aim
15. https://huggingface.co/apple/aimv2-large-patch14-224
16. https://www.marktechpost.com/2024/11/22/apple-releases-aimv2-a-family-of-state-of-the-art-open-set-vision-encoders/
17. https://machinelearning.apple.com/research/multimodal-autoregressive
18. https://github.com/apple/ml-4m
19. https://machinelearning.apple.com/research/personal-voice
20. https://apps.apple.com/us/app/personal-voice-generator/id6473683146
21. https://digg.com/tech/tuo1sird
22. https://github.com/Genesis-Embodied-AI/Genesis
23. https://github.com/ruvnet/genesis
24. https://arxiv.org/html/2505.01458v1
25. https://github.com/Genesis-Embodied-AI/genesis-world
26. https://github.com/ruili3/awesome-dust3r
27. https://cvpr.thecvf.com/virtual/2025/poster/34871
28. https://cvpr.thecvf.com/virtual/2025/poster/34485
29. https://opencv.org/mast3r-slam/
30. https://github.com/rmurai0610/MASt3R-SLAM
31. https://developer.nvidia.com/isaac
32. https://research.nvidia.com/labs/srl/publication/wen-2024-foundation-pose/
33. https://research.nvidia.com/publication/2024-06_foundationpose-unified-6d-pose-estimation-and-tracking-novel-objects
34. https://research.nvidia.com/publication/2025-03_nvidia-isaac-gr00t-n1-open-foundation-model-humanoid-robots
35. https://www.hackster.io/news/nvidia-isaac-groot-n1-is-an-open-source-foundation-model-for-accelerated-humanoid-robot-development-effa04c90231
36. https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Accelerates-Robotics-Research-and-Development-With-New-Open-Models-and-Simulation-Libraries/default.aspx
37. https://research.nvidia.com/publication/2025-01_cosmos-world-foundation-model-platform-physical-ai
38. https://research.nvidia.com/publication/2025-09_world-simulation-video-foundation-models-physical-ai
39. https://www.facebook.com/groups/DeepNetGroup/posts/2659292184463647/
40. https://github.com/nvidia-cosmos
41. https://research.nvidia.com/publication/2025-06_foundationstereo-zero-shot-stereo-matching
42. https://developer.nvidia.com/blog/r2d2-building-ai-based-3d-robot-perception-and-mapping-with-nvidia-research
43. https://pixel-decoder.com/2025/02/18/foundationstereo-framework-explained-5-key-features-for-zero-shot-stereo-depth-estimation/
44. https://blog.muhammad-ahmed.com/2025/03/17/foundationstereo-revolutionizing-stereo-depth-estimation-with-zero-shot-learning/
45. https://community.stereolabs.com/t/native-nvidia-fast-foundation-stereo-support/11231
46. https://arxiv.org/abs/2503.11651
47. https://github.com/facebookresearch/vggt
48. https://www.youtube.com/watch?v=7ZYwJEpCUUA
49. https://arxiv.org/abs/2507.14798
50. https://ik3d.fr/mobile-gs-your-phone-just-became-a-real-time-gaussian-splat-renderer/
51. https://openreview.net/forum?id=vRegY0pgvQ
52. https://iclr.cc/virtual/2026/poster/10006810
53. https://github.com/xiaobiaodu/mobile-gs
54. https://playground.roboflow.com/models/compare/depth-anything-v2-vs-sam
55. https://proceedings.neurips.cc/paper_files/paper/2024/hash/26cfdcd8fe6fd75cc53e92963a656c58-Abstract-Conference.html
56. https://github.com/DepthAnything/Depth-Anything-V2
57. https://openreview.net/pdf/7c41968163abe4e3700e3e3a15174a9d679fcd52.pdf
58. https://github.com/pablovela5620/sam2-depthanything
59. https://github.com/nerfstudio-project/gsplat
60. https://arxiv.org/abs/2309.16650
61. https://canvas4sh.tistory.com/434
62. https://www.youtube.com/watch?v=mRhNkQwRYnc
63. https://www.linkedin.com/posts/markkovarski_...kokoro-82m...activity-7284610343065079810-XQTw
64. https://huggingface.co/hexgrad/Kokoro-82M
65. https://ageofllms.com/ai-howto-prompts/ai-fun/kokoro-tts
66. https://findskill.ai/blog/best-open-source-tts-2026/
67. https://huggingface.co/philippdxx/Kokoro-TTS-coreml
68. https://www.gladia.io/blog/best-open-source-speech-to-text-models
69. https://stt.ai/models/nvidia-parakeet/
70. https://developer.nvidia.com/blog/new-standard-for-speech-recognition-and-translation-from-the-nvidia-nemo-canary-model/
71. https://www.linkedin.com/posts/quantshah_nvidia-activity-7468650602265432065-aiot
72. https://kyutai.org/2024/09/18/moshi-release.html
73. https://localaimaster.com/blog/moshi-realtime-speech-guide
74. https://kyutai.org/blog
75. https://github.com/kyutai-labs/moshi-swift
76. https://huggingface.co/kyutai/moshika-rl-seamless
77. https://www.codesota.com/speech/best-open-source
78. https://modal.com/blog/open-source-tts
79. https://codersera.com/blog/tag/orpheus/
80. https://stt.ai/models/moonshine/
81. https://github.com/snakers4/silero-vad
82. https://discuss.huggingface.co/t/i-built-an-open-source-vad-that-beats-silero-pyannote-and-webrtc-on-noisy-audio-with-93-accuracy-no-gpu-required/177044
83. https://research.nvidia.com/labs/conv-ai/publications/category/speaker-recognition/
84. https://zenn.dev/rick_lyric/articles/1e48eeb396904d
85. https://huggingface.co/nvidia/speakerverification_en_titanet_large
86. https://pyimagesearch.com/2025/06/23/smolvlm-to-smolvlm2-compact-models-for-multi-image-vqa/
87. https://arxiv.org/html/2504.05299v1
88. https://huggingface.co/blog/smolvlm2
89. https://playground.roboflow.com/models/moondream-ai/moondream-2
90. https://www.scribd.com/document/1003192563/2510-09653v2
91. https://www.semanticscholar.org/paper/YOLO-World:-Real-Time-Open-Vocabulary-Object-Cheng-Song/37c112454a236ab91c9c6b5cc165a6c3251e9206
92. https://www.codesota.com/browse/computer-vision/zero-shot-object-detection
93. https://inteligenai.com/zero-shot-detection-enterprise/
94. https://playground.roboflow.com/models/baidu/rt-detr
95. https://ar5iv.labs.arxiv.org/html/2506.01844
96. https://pureai.com/articles/2025/06/10/hugging-face-releases-smolvla.aspx
97. https://www.marktechpost.com/2025/06/03/hugging-face-releases-smolvla-a-compact-vision-language-action-model-for-affordable-and-efficient-robotics/
98. https://huggingface.co/docs/lerobot/smolvla
99. https://humanoidintel.ai/brains/lerobot/
100. https://learnopencv.com/vision-language-action-models-lerobot-policy/
101. https://en.wikipedia.org/wiki/Vision-language-action_model
102. https://www.cloderic.com/content/2025-02-27-notes-on-pi0
103. https://dev.to/ankk98/from-perception-to-embodied-intelligence-evolution-architectures-and-the-humanoid-gap-3dhi
104. https://huggingface.co/mlx-community
105. https://github.com/ml-explore/mlx
106. https://developer.apple.com/videos/play/wwdc2025/298/
107. https://github.com/applecool/mlx-examples
108. https://agent-wars.com/news/2026-03-14-microsoft-bitnet-official-inference-framework-1-bit-llms-6x-cpu-speedup
109. https://www.linkedin.com/posts/mahmoudrabie2004_opensourceaiprojects-didyouknowthat-activity-7366518624573984769-xnuU
110. https://github.com/microsoft/BitNet
111. https://www.linkedin.com/posts/nelsonjeronimo_github-microsoftbitnet-official-inference-activity-7437628848302866432-9RIG
112. https://www.microsoft.com/en-us/research/publication/1-bit-ai-infra-part-1-1-fast-and-lossless-bitnet-b1-58-inference-on-cpus/
113. https://www.arm.com/zh-TW/company/news/2024/11/accelerating-edge-ai-with-executorch
114. https://newsroom.arm.com/news/executorch-1-0-ga-release-edge-ai
115. https://community.arm.com/arm-community-blogs/b/ai-blog/posts/executorch-and-tosa-enabling-pytorch-on-arm-platforms
116. https://spiral.imperial.ac.uk/entities/publication/ceb86b10-7390-4a41-ac2e-6395c1c28dd0
117. https://ro.ecu.edu.au/ecuworks2022-2026/4278/
118. https://ro.ecu.edu.au/theses/3012/
119. https://liner.com/review/openvocabulary-functional-3d-scene-graphs-for-realworld-indoor-spaces

---

*Fused 2026-06-24 from `01_cutting_edge_oss__upgrade_survey.md` (Claude) +
`02_cutting_edge_oss__geodesic.md` (Perplexity Deep Research). No finds, scores, or sources dropped;
divergences flagged inline with ⚖️.*
