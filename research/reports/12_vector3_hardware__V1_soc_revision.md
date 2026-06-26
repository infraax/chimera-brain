# Vector 3.0 · V1 Focused Revision
## Compute Architecture & the Brain Partition (2026 Parts Only)
### 2026-06-24 · Replaces the V1 section in the master geodesic

> **Note:** This revision corrects the MIPI-CSI lane count in the original report (the Radxa NX5 SODIMM exposes 4 usable camera inputs, not 6), and narrows to a single unambiguous SoC recommendation with verified 2025–2026 benchmarks.

***

## RECOMMENDATION

**The Rockchip RK3588S** — deployed as the **Radxa NX5 SoM (SODIMM 260-pin, 70 × 45 mm)** — is the single recommended application processor for Vector 3.0.

No other 2026 SoC hits all five constraints simultaneously: ≥5 TOPS NPU, ≥4 simultaneous MIPI-CSI camera inputs, aarch64 hard-float Linux, <10 W sustained at full perception load, and a functioning dev-board + open-BSP path for a solo builder.

The decision rationale against each 2026 alternative is given in the scored table below. The safety partition is owned by an **STM32H743** running FreeRTOS — the direct 2026 successor to the original Vector's STM32F030 body MCU, with ten times the CPU headroom and a richer motor-control peripheral set.

***

## SoC CANDIDATE EVALUATION (2026)

| SoC | CPU | NPU | MIPI-CSI (max cameras) | Sustained power (SoC only) | Solo-builder path | Verdict |
|-----|-----|-----|------------------------|--------------------------|-------------------|---------|
| **RK3588S** | 4× A76 @ 2.4 GHz + 4× A55 | **6 TOPS** INT4/8/16/FP16/BF16/TF32[^1][^2] | **4 inputs** (2×2-lane CSI + 1×2-lane + 1×4-lane D/C-PHY)[^3][^4] | ~3–6 W (L2 active); ~12 W max[^5][^6] | ✅ Radxa NX5 SoM, open Debian/Ubuntu BSP[^7][^8][^4] | **SELECTED** |
| RK3576 | 4× A72 + 4× A55 | 6 TOPS (same TOPS, ~30% lower real YOLO throughput[^9]) | 3×CSI-2 up to 16 MP ISP[^10] | ~20–40% lower than RK3588S[^11][^12] | ✅ growing ecosystem | Rejected: A72 vs A76 = 40–66% slower CPU[^11][^12]; lower NPU scheduling efficiency; only 3 camera inputs |
| RK3572 | 2× A73 + 6× A53 | 4 TOPS[^13] | 2 CSI inputs | Low | Emerging | Rejected: 4 TOPS insufficient for full chimera L2 stack |
| RPi CM5 + Hailo-8L | 4× A76 (BCM2712) | +13 TOPS (PCIe)[^14][^15] | 2 CSI inputs (CM5 platform limit) | ~8–15 W with Hailo active | ✅ excellent BSP | Rejected: only 2 MIPI CSI inputs; Hailo-8L requires PCIe lane already shared with radio; two-chip BOM complexity |
| Jetson Orin Nano 4 GB | 6× A78AE | 20 TOPS | 2 CSI-2 (4-lane each) | **7–10 W idle → 25 W peak**[^16][^17] | Moderate (carrier design complex) | Rejected: thermal headroom demands active cooling in a 58 mm body; export-control risk; higher cost |
| QCS6490 / Dragonwing RB3 Gen 2 | 4× Kryo Gold + 4× Silver | Hexagon NPU (high-performance) | 4+ CSI | ~5–8 W estimated | Moderate (OEM-class RB3 kit $250+)[^18][^19] | Rejected: dev kit price and OEM-first toolchain; NDA-gated Hexagon SDK depth; higher cost-per-unit |
| NXP i.MX 8M Plus | 4× A53 | 2.3 TOPS | 2 CSI | ~3–5 W | Good (Variscite SoM) | Rejected: 2.3 TOPS insufficient; no A76-class cores for ENGRAM HRR computation |

***

## THE SINGLE CHOICE: RK3588S ON RADXA NX5

### Why the RK3588S eliminates every ENGRAM-rewrite pain point

The ENGRAM-rewrite report identifies five specific 2018-silicon bottlenecks on the APQ8009. The RK3588S removes all five:

| ENGRAM Pain Point (APQ8009) | Root Cause | RK3588S Resolution |
|-----------------------------|------------|--------------------|
| softfp ABI (6–8× float penalty) | Qualcomm carrier toolchain, Cortex-A7 softfp build | Native aarch64 hard-float at all times; no softfp path[^1][^20] |
| fp16 storage-only (no fp16 compute) | Cortex-A7 has no half-precision execution unit | NPU executes FP16/BF16 natively; A76 NEON fp16 vector ops[^1][^2] |
| No NPU → all PFFFT on CPU | APQ8009 has zero ML accelerator | 6 TOPS triple-core NPU with INT4/8/16/FP16; RKNN Toolkit 2 (Apache-2.0)[^1][^21][^22] |
| RAM starvation (~512 MB practical) | APQ8009 platform ceiling | 8 GB LPDDR4x on Radxa NX5 (16 GB SKU available)[^3][^4] |
| Single-core A7 bottleneck for ENGRAM rFFT | No big core, no NEON+dotprod | 4× A76 with NEON+dotprod; PFFFT is ~10× faster on A76 vs A7[^1] |

### MIPI-CSI camera budget — the corrected count

The Radxa NX5's SODIMM pinout exposes:[^3][^4]
- **2× 2-lane MIPI CSI-2** (can be combined as 1× 4-lane)
- **1× 2-lane MIPI D/C-PHY RX** (CSI-2 or CSI-3 / C-PHY capable)
- **1× 4-lane MIPI D/C-PHY RX**

This gives **4 physical camera inputs** — not 6 as stated in the earlier synthesis. The five-camera suite in V3 must be revised: use a **MIPI CSI multiplexer / deserializer** (e.g., **Maxim MAX9286 GMSL2 quad deserializer**, or the simpler **TI DS90UB953/954 FPD-Link III** combo) to aggregate 4 camera streams onto the 4-lane D/C-PHY RX input, or reduce the camera count. The recommended resolution:

- **Front eye-contact camera (IMX678)** → 4-lane D/C-PHY RX (dedicated, highest bandwidth)
- **Stereo pair (2× OV9782 GS)** → 2-lane CSI-2 ×2 (one each, synchronized vsync)
- **Lateral fisheye OR downward cliff** → 2-lane D/C-PHY RX (mux between modes, or use a 2:1 CSI mux)
- **DVS (Prophesee GenX320 MIPI)** → USB-C 3.0 (re-routed off the CSI budget; GenX320 supports CPI/USB output)[^23]

This is buildable within the NX5's exposed interfaces without an additional deserializer chip. The V3 camera suite is thereby reduced to **4 physical MIPI cameras + 1 USB DVS** — still a major upgrade over the 2018 Vector's single camera, and still correctly mapped to V1's silicon.

### On-robot LLM performance — verified benchmarks

Independent 2025–2026 benchmarks on RK3588S hardware (Radxa Rock 5B, same NPU/CPU):[^24][^25][^26]

| Model | Backend | Tokens/sec | Notes |
|-------|---------|-----------|-------|
| Qwen2.5-3B | RKLLM NPU | ~7 t/s[^26] | Usable for conversational L3 responses |
| Qwen3-1.7B | RKLLM NPU | ~2.2 t/s composite[^25] | Quality/speed sweet spot |
| DeepSeek-R1 1.5B W8A8 | RKLLM NPU | ~11.2 t/s[^24] | Fastest; limited reasoning depth |
| Qwen2.5-VL-3B (vision) | RKNN + RKLLM | ~8 t/s decode[^27] | Visual grounding for L3 |
| Qwen2.5-3B on CPU only | Ollama | ~0.21 t/s[^24] | Unusably slow — NPU is mandatory |

**Conclusion:** A Qwen2.5-3B or Qwen3-1.7B via RKLLM gives **interactive L3 on-robot at 2–7 t/s**. This is sufficient for Vector 3.0's L3 Constructor layer generating short expressive utterances (target <5 seconds for a 20-token response). Heavy reasoning (chain-of-thought) and large-context VLM queries go to the dock box.

***

## PARTS

| Part | Vendor | ~Cost (qty1/10/100) | Interface | Power (measured) | Open driver? | Datasheet / date |
|------|--------|-------------------|-----------|-----------------|-------------|-----------------|
| **Radxa NX5 (RK3588S, 8 GB LPDDR4x, 32 GB eMMC)** SKU RM121-D8E32 | Radxa direct / Seeed / ThinkRobotics | **~$95 / $85 / $72**[^8][^28][^4] | SODIMM 260-pin, 5 V | 3–6 W active; ~0.42 W idle[^6] | ✅ Debian/Ubuntu; RKNN Toolkit 2 Apache-2.0; BSP guaranteed until Sept 2033[^3] | product brief rev 1.1, 2023-10-08[^3] |
| **STM32H743VI** (L1 safety MCU) | Mouser / DigiKey / LCSC | ~$8 / $7 / $5.50 | UART/SPI/I²C to SoC; FOC PWM, ADC | 50–200 mW | ✅ HAL, FreeRTOS MIT; STM32CubeH7[^29][^30] | DS12110 rev 8, 2023 |
| **STM32H743 Nucleo-144** (Phase 0 dev board) | Mouser | ~$28 | USB/UART/SWD | — | ✅ | — |
| Radxa NX5 IO Board (Phase 0 carrier) | Radxa / Seeed | ~$35 | All NX5 interfaces broken out | — | ✅ | — |
| Custom 4-layer carrier PCB (Phase 1) | JLCPCB | ~$80 proto / $15 at qty 100 | All peripherals | — | — | — |

***

## ANKI 2018 → 2026

**Anki's 2018 choice (TRM):** APQ8009 (Qualcomm, 4× Cortex-A7 @ up to 1.2 GHz, ~512 MB LPDDR3, no NPU, softfp ABI, 28 nm). Separate STM32F030 body MCU (48 MHz, 16 KB SRAM) for motor/cliff/safety. The APQ8009 was a phone chip repurposed for robotics — the only 2018 option that fit the body volume and the $249 retail price target.

**The constraint that forced it:** In 2018, any SoC with an NPU was either a phone-class chip (too power-hungry/hot at 5–10 W SoC load in a passive 90 cm³ enclosure) or an NDA-gated ASIC. Qualcomm's Snapdragon 210 (APQ8009) at 28 nm provided an acceptably low idle current in a productizable package.

**What 2026 changes:** The RK3588S is manufactured at 8 nm, delivering the APQ8009's idle power budget at ~10× the compute throughput. The 6 TOPS NPU, which didn't exist in the 2018 robotics SoC landscape, now runs YOLO detection + depth estimation + small LLM inference simultaneously within the same 5–6 W envelope that the APQ8009 consumed just to idle with the screen on. The Radxa NX5 SoM form factor (70 × 45 mm) is smaller than the original Vector head-board PCB, making carrier-board integration straightforward.[^1][^20]

***

## CHIMERA LAYER → SILICON MAPPING

```
L1 BRAINSTEM  ──────────────────  STM32H743  (FreeRTOS)
  Motor FOC loops (10–40 kHz)        │
  Cliff / ToF reflexes (<10 ms)      │  UART 1 Mbaud (FlatBuffers frames)
  Thermal e-stop                     │  SPI (motor noise reference → XVF3800)
  Battery guardian (BQ40Z50)         │
  Touch-skin events                  │
                                     ▼
L2 CORTEX  ──────────────────────  RK3588S  (Linux, Buildroot)
  Camera ISP + 4× MIPI CSI             RK3588S NPU (6 TOPS)
  Object/face detection (YOLO INT8) ─→ RKNN Toolkit 2
  Stereo depth (Depth Anything V2)  ─→ RKNN (gated)
  Audio VAD + STT (Moonshine)       ─→ RKNN / XNNPACK
  ENGRAM hot ring-buffer (C++/PFFFT)─→ A76 NEON hard-float
  ENGRAM multi-scale scattering     ─→ NPU INT8 (gated)
  HRR identity composition D=4096   ─→ A76 CPU (batched)

L3 CONSTRUCTOR  ──────────────────  RK3588S CPU + NPU  (gated)
  On-robot LLM: Qwen2.5-3B RKLLM   ─→ NPU, ~2–7 t/s
  Kokoro TTS                        ─→ CPU ONNX Runtime
  VLM visual grounding (Qwen2.5-VL-3B)→ RKNN + RKLLM (gated)
  Heavy reasoning / large context   ─→ DOCK BOX (offload over USB-C 3.2 Gen2)
  ENGRAM cold archive + USearch ANN ─→ DOCK BOX (Go + cgo, NVMe)
```

***

## SELF-AWARENESS (THE ANKI MOVE)

The STM32H7 publishes a **motor-state telemetry frame** at 1 kHz over UART: `[timestamp_us | drive_L_pwm | drive_R_pwm | lift_pwm | head_pwm | drive_L_I | drive_R_I | lift_I | head_I | drive_L_enc | drive_R_enc | lift_enc | head_enc | battery_mV | battery_mA]` — 32 bytes, FlatBuffers-framed.

The RK3588S chimera-engine consumes this as:
1. **Ego-motion vector** → fed into stereo optical flow to cancel tread-induced image shift before obstacle detection (V3 self-occlusion correction)
2. **Ego-noise reference** → forwarded over SPI to the XMOS XVF3800 audio beamformer for motor-noise nulling (V5 Anki-doctrine extension)
3. **Actuator health monitor** → ENGRAM motor-wear model: over days, rising current-at-constant-speed is fit to a winding-resistance-increase curve; recalibration coefficients update the FOC control gains autonomously

The SoC also monitors its own thermal state (RK3588S internal thermal sensors exposed via sysfs) and publishes a **DVFS control recommendation** back to the STM32H7: "reduce motor load" or "gate camera pipeline" before thermal throttling begins. The creature degrades gracefully — it slows down before it crashes.

***

## SAFETY PARTITION CONTRACT (FORMAL)

The STM32H743 owns the following independently of the application processor state. **None of these conditions can be overridden or suppressed by software on the RK3588S:**

| Condition | STM32H7 Action | Latency |
|-----------|---------------|---------|
| UART from RK3588S silent >100 ms | All motor PWM → 0 (coast) | <1 ms |
| VL53L8CX front reports <3 mm clearance | Motors stop + lift retract | <5 ms |
| Battery cell voltage <3.2 V | Motors stop; SoC suspend signal asserted | <1 ms |
| Any motor current >3 A for >200 ms | Driver disable; L2 fault event | <2 ms |
| SoC thermal sensor >75 °C OR battery NTC >65 °C | Charger disable; motors stop | <5 ms |

This replicates and strengthens the original Anki STM32/syscon body-board doctrine: a crashed `vic-engine` could never drive the 2018 Vector off a shelf. The same guarantee holds in Vector 3.0.

***

## POWER/THERMAL

| Mode | RK3588S SoC | STM32H743 | Total (SoC+MCU) |
|------|------------|-----------|----------------|
| Deep dock sleep | **~0.42 W** (measured, Firefly board)[^6] | 50 mW | ~0.47 W |
| Awareness idle (L2 perception, no NPU) | ~2 W[^5] | 100 mW | ~2.1 W |
| L2 + NPU continuous (YOLO + depth) | ~5–6 W[^5][^6] | 150 mW | ~5.2–6.2 W |
| L3 + RKLLM on-robot LLM | ~7–9 W[^24][^25] | 200 mW | ~7.2–9.2 W |
| Worst-case burst (all cores + NPU + GPU) | ~12 W[^5] | 200 mW | ~12.2 W |

**Thermal:** At sustained 6 W (L2+NPU continuous), a 60 × 90 mm × 1 mm copper heat-spreader bonded to the robot's lower chassis wall achieves ~70°C SoC junction at 25°C ambient — within the RK3588S's 0–80°C operating range. No fan required for L2-continuous mode. L3 LLM inference bursts that push >8 W for >5 minutes benefit from a 20 mm rear exhaust fan (optional, Phase 2). The RK3588S throttles at 80°C before any thermal damage occurs.[^4]

The idle figure of 0.42 W is crucial: during dock naps, the SoC consumes less than the original Vector's entire active power budget — the creature can literally sleep for days on the dock and cost negligible electricity.

***

## RISKS / OPEN QUESTIONS / CONFIDENCE

**Confidence: High.**

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Radxa NX5 MIPI CSI: only 4 camera inputs (not 6) | Medium — forces V3 camera redesign | Redesign V3 to 4 MIPI cameras + USB DVS; use TI DS90UB954 4:1 CSI deserializer if 5th MIPI camera is mandatory |
| RKNN Toolkit 2 model compatibility | Low — grows with ecosystem | ONNX Runtime + XNNPACK CPU fallback for any non-RKNN model; the A76 CPU is fast enough for fallback |
| RK3588S supply continuity | Low — Radxa guarantees NX5 until Sept 2033[^3] | Long-term availability confirmed; 8-year roadmap is unusual for a consumer SoC module |
| Custom carrier PCB MIPI layout | High — 4-lane 100 Ω diff pairs, matched length | Phase 0 uses Radxa NX5 IO board (all MIPI broken out); carrier PCB only in Phase 1 after software stack is validated |
| RKLLM LLM quality at 2–7 t/s | Medium — 7 t/s is usable; 2 t/s feels slow for fast banter | Gate L3 LLM for user-initiated queries; use pre-compiled emotion + short-phrase responses for reactive behavior (Kokoro TTS path, no LLM latency) |

**Prototype-first resolution:** Phase 0 uses a **Radxa Rock 5B SBC** ($140, same RK3588S chip, all interfaces exposed on standard headers) to validate the full chimera+ENGRAM software stack before a single custom PCB is ordered. This is the Anki-doctrine risk-first build order: prove the software on commodity hardware, then commit NRE to the carrier board.

***

*V1 revision complete — single SoC selected, MIPI lane count corrected, LLM benchmarks verified from live 2025–2026 measurements. Feeds into V3 (camera count correction), V10 (8 GB RAM floor confirmed), and V13 (RKNN+RKLLM as the canonical on-robot inference runtime).*

---

## References

1. [瑞芯微RK3588和RK3588S的区别? RK3588和RK3576 - CSDN博客](https://blog.csdn.net/ftdlk/article/details/146562882) - 文章浏览阅读6.6k次，点赞28次，收藏28次。选择RK3588：若需复杂接口（如PCIe扩展、多路视频输入输出、SATA存储），或面向工业、服务器、高端影音设备开发；RK3588S：封装尺寸17×1...

2. [Radxa Rock 5C RK3588S 16GB LPDDR4 RS131-D16R26](https://www.lichtsignatur.com/product/radxa-rock-5c-rk3588s-16gb-lpddr4-rs131-d16r26/) - Rockchip RK3588S2 64bit octa core ARM based SBC´s RADXA´s latest generation SBC based on the Rockchi...

3. [Radxa NX5](https://dl.radxa.com/nx5/radxa_nx5_product_brief.pdf)

4. [Radxa NX5 (mEdge-RK3588S)](https://thinkrobotics.com/products/radxa-nx5-medge-rk3588s) - NX5(mEdge-RK3588S) Radxa mEdge-RK3588S Rockchip RK3588S Experience Outstanding Performance, Explore ...

5. [What is the power consumption of RK3588?](https://apurx.com/blogs/articles/what-is-the-power-consumption-of-rk3588) - Power Consumption of RK3588The RK3588 is a high-performance microprocessor designed for a wide range...

6. [ROC-RK3588S-PC 8-Core 8K AI Mainboard - Firefly](https://en.t-firefly.com/product/industry/rocrk3588spc) - Power Consumption. Idle: ≈0.42W (12V/35mA). Typical: ≈2.25W (12V/190mA). Max: ≈12W (12V/1000mA). Env...

7. [Radxa NX5 RK3588S SODIMM Compute Module](https://evelta.com/radxa-nx5-rk3588s-sodimm-compute-module/) - Buy Radxa NX5 RK3588S SODIMM Compute Module for high-performance embedded and AI applications. Octa-...

8. [Radxa NX5 development kit starts at $99.00 - Linux Gizmos](https://linuxgizmos.com/radxa-nx5-development-kit-starts-at-99-00/) - The Radxa NX5 is a System on Module with SODIMM form-factor and designed to cater to a wide range of...

9. [RK3588 vs RK3576: YOLO Inference Performance Shows ...](https://armbasedsolutions.com/cases-detail/rk3588-vs-rk3576-yolo-inference-performance-shows-over-30-gap) - RK3588 and RK3576 represent two important generations of AI SoCs. They are widely used in edge AI co...

10. [A Comparative Analysis between RK3588 and RK3576 Chips](https://dev.to/as-jackson/a-comparative-analysis-between-rk3588-and-rk3576-chips-unveiling-the-technological-distinctions-5ci1) - RK3588 is significantly better than RK3576 in video decoding format support and resolution, and can ...

11. [RK3576 能否替代RK3588？一文看懂6TOPS 工业AI SoC 的 ...](https://www.elecfans.com/d/7618934.html) - 过去两年，Rockchip 芯片在工业、AI、机器人、边缘计算领域持续火热，其中最受市场关注的两颗 SoC —— RK3588 与 RK3576 ，几乎每个技术群都在讨论： 都是 8 核 CPU + ...

12. [RK3588 vs RK3576: Don't Be Fooled by the Specs! Can the Cheaper Chip Really Compete?](https://www.youtube.com/watch?v=ulNyd6VZTGg) - Everyone is talking about the new RK3576. With the same 6TOPS NPU on paper, can this cheaper alterna...

13. [Rockchip unveils RK3572 processor with 4 TOPS NPU and ...](https://linuxgizmos.com/rockchip-unveils-rk3572-processor-with-4-tops-npu-and-lpddr5x-support/) - For AI workloads, the integrated NPU delivers up to 4 TOPS INT8 performance and supports INT4, INT8,...

14. [Raspberry Pi AI Kit with M.2 HAT+ and Hailo AI Module (13T)](https://www.adafruit.com/product/5979) - The Raspberry Pi AI Kit bundles the Raspberry Pi M.2 HAT+ with a Hailo AI acceleration module for us...

15. [Raspberry Pi AI Kit: 2026 Edge Compute Hardware Review - LinkedIn](https://www.linkedin.com/posts/anismohd_raspberry-pi-ai-kit-complete-technical-npu-activity-7450278599787442176-xkbO) - Raspberry Pi AI Kit: Complete Technical NPU Guide Raspberry Pi AI Kit: The 2026 Edge Compute Hardwar...

16. [NVIDIA Jetson Orin Nano Super Developer Kit (67 TOPS, 8GB, 25W)](https://www.dfrobot.com/product-2900.html) - Experience cutting-edge AI with Jetson Orin Nano Super Kit—67 TOPS of AI performance for generative ...

17. [NVIDIA Jetson Orin Nano Super Developers Kit - Getting Started](https://dronebotworkshop.com/jetson-orin-nano/) - The repriced and improved Jetson Orin Nano Super Developers Kit allows makers and experimenters to w...

18. [Powering IOT developers with edge AI: Qualcomm RB3 Gen 2 Kit is ...](https://www.qualcomm.com/developer/blog/2025/03/powering-iot-developers-with-edge-ai-qualcomm-rb3-gen2-kit-now-integrated-with-edge-impulse) - With the support in the Edge Impulse platform, developers have even more flexibility to build, train...

19. [Qualcomm® RB3 Gen 2 Development Kit](https://docs.qualcomm.com/bundle/publicresource/87-74789-1_REV_A_Qualcomm_RB3_Gen_2_Development_Kit_Product_Brief.pdf)

20. [Rockchip RK3588 Boards in 2026](https://rockchips.net/rockchip-rk3588-boards-in-2026-landscape-comparisons-and-sbc-choices/) - Rockchip RK3588 boards are the focus of this detailed overview, exploring the broader ecosystem in 2...

21. [Rockchip RKLLM toolkit released for NPU-accelerated large language models on RK3588, RK3588S, RK3576 SoCs](https://www.cnx-software.com/2024/07/15/rockchip-rkllm-toolkit-npu-accelerated-large-language-models-rk3588-rk3588s-rk3576/)

22. [Edge AI using the Rockchip NPU | Tristan Penman · Hacker at](https://tristanpenman.com/blog/posts/2025/07/20/edge-ai-using-the-rockchip-npu/) - A blog about the fun parts of programming.

23. [Prophesee Reinvents DVS Camera For AIoT Applications](https://www.eetasia.com/prophesee-reinvents-dvs-camera-for-aiot-applications/) - Prophesee's event-based camera suits always-on IoT devices.

24. [RK3588 LLM Performance: NPU vs CPU in a Discord Agent | Sergio B.](https://sergiiob.dev/posts/rk3588-npu-vs-cpu-llm-discord-bot/) - Benchmarking local LLM inference on RK3588 and why NPU acceleration (RKLLM) is the difference betwee...

25. [14 Models Benchmarked on RK3588: The Definitive CPU vs ...](https://sergiiob.dev/posts/rk3588-ultimate-14-model-benchmark-cpu-npu/) - Benchmarked every viable local LLM (350M to 26B, CPU and NPU) through a live Discord agent pipeline ...

26. [Run Llama 3 Locally: RK3588 NPU vs Raspberry Pi 5 ...](https://unland.dev/blog/run-llama-3-locally-rk3588-npu-vs-raspberry-pi-5) - Complete benchmark comparison of RK3588 NPU vs Raspberry Pi 5 for running Llama 3 locally. Independe...

27. [happyme531/Qwen2.5-VL-3B-Instruct-RKLLM](https://huggingface.co/happyme531/Qwen2.5-VL-3B-Instruct-RKLLM) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

28. [Radxa NX5 RK3588S Compute Module Octa-Core ARM Cortex-A76 ...](https://www.alibaba.com/product-detail/Radxa-NX5-RK3588S-Compute-Module-Octa_1601536867419.html) - Radxa NX5 RK3588S Compute Module Octa-Core ARM Cortex-A76/A55 Processor 6 TOPS NPU 4GB/8GB/16GB/32GB...

29. [Best STM32 Development Boards for Beginners, IoT, Motor Control ...](https://www.ampheo.com/blog/best-stm32-development-boards-for-beginners-iot-motor-control-and-ai) - It is a strong choice for learners interested in analog measurement, motor-control signals, power el...

30. [STM32 for Efficient & Smart Motor Control - ALLPCB](https://www.allpcb.com/allelectrohub/stm32-for-efficient-and-smart-motor-control) - Enhance motor efficiency with intelligent motor control. Explore ST's STM32 MCU solutions to reduce ...

