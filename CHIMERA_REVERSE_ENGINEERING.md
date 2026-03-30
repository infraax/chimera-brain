# CHIMERA REVERSE ENGINEERING SPECIFICATION
## Extracting and Decompiling Vector's Closed-Source Brain
## Created: 2026-03-31 | Session 0 (continued)

---

## Why This Matters

Anki open-sourced the cloud services, SDKs, and communication protocols. They never open-sourced the on-device brain — the vic-engine binary and libcozmo_engine shared library that contain:

- The emotion model implementation (MoodManager, affectors, decay math)
- The behavior tree execution engine (86 behavior classes, priority arbitration)
- The animation-emotion coupling (how emotional state modulates creature expression)
- The vision pipeline (face detection, SLAM, marker recognition)
- The sensor fusion layer (camera, IMU, ToF, cliff integration)
- Internal message passing between subsystems

The TRM describes *what* these systems do. The JSON configs define *parameters*. But the actual *implementation* — the code that makes Vector feel alive — lives only in the compiled ARM binaries on the robot. Recovering this code is the highest-leverage action for the chimera project.

---

## Target Binaries

### Primary Targets (highest value for chimera)

| Binary | Location on Robot | Purpose | Priority |
|--------|------------------|---------|----------|
| `vic-engine` | `/anki/bin/vic-engine` | Behavior tree, emotion engine, vision, SLAM | CRITICAL |
| `libcozmo_engine.so` | `/usr/lib/libcozmo_engine.so` | Core intelligence library linked by vic-engine | CRITICAL |
| `vic-anim` | `/anki/bin/vic-anim` | Animation engine, face compositing, audio sync | HIGH |
| `vic-robot` | `/anki/bin/vic-robot` | Motor control, sensor filtering, vic-spine | MEDIUM |

### Secondary Targets (useful but not blocking)

| Binary | Location | Purpose | Priority |
|--------|----------|---------|----------|
| `vic-gateway` | `/anki/bin/vic-gateway` | SDK/API server (gRPC) | LOW |
| `vic-cloud` | `/anki/bin/vic-cloud` | Cloud communication (replaced by WirePod) | LOW |
| `vic-switchboard` | `/anki/bin/vic-switchboard` | BLE communication, key management | LOW |

### Supporting Files (already accessible, not compiled)

| File/Folder | Location | Content |
|-------------|----------|---------|
| Behavior tree configs | `/anki/data/assets/cozmo_resources/config/engine/behaviorComponent/` | JSON behavior nodes, conditions, parameters |
| Emotion event configs | `/anki/data/assets/cozmo_resources/config/engine/emotionevents/` | JSON emotion event → affector mappings |
| Mood config | `/anki/data/assets/cozmo_resources/config/engine/mood_config.json` | Decay graphs, value ranges, audio parameter maps |
| Vision config | `/anki/data/assets/cozmo_resources/config/engine/vision/` | Vision pipeline parameters |
| Animation assets | `/anki/data/assets/cozmo_resources/assets/` | Binary animation files, sprites, audio |
| TF Lite models | `/anki/data/assets/cozmo_resources/config/engine/vision/` | Neural network models for detection |
| Platform config | `/anki/etc/config/platform_config.json` | Master path configuration |
| Feature flags | `/anki/data/assets/cozmo_resources/config/features.json` | Feature enable/disable toggles |

---

## Binary Architecture Details

- **CPU:** Qualcomm APQ8009 — ARM Cortex-A7, quad-core, ARMv7-a architecture
- **Instruction set:** ARM + Thumb-2 (mixed mode, typical for Cortex-A7)
- **Float ABI:** soft-float (`arm-linux-gnueabi`, NOT `gnueabihf`) due to Qualcomm proprietary blob requirements
- **Compiler flags for cross-compilation:** `-mfloat-abi=softfp -march=armv7-a -mfpu=neon-vfpv4`
- **OS:** Yocto Linux (custom build, not Android despite using Qualcomm SoC)
- **Binary format:** ELF 32-bit LSB shared object / executable, ARM
- **Key libraries:** OpenCV, TensorFlow Lite, various Qualcomm proprietary libs
- **Build system:** Anki used internal build tools; binaries are stripped (no debug symbols)

---

## PATH 1: Extract Binaries from OTA (No Robot Required)

This path lets you start reverse engineering immediately without touching your Vector.

### Step 1: Download the firmware

```bash
# Create a working directory
mkdir -p ~/chimera-re/firmware
cd ~/chimera-re/firmware

# Download production firmware (contains the same vic-engine as your robot)
curl -o prod-latest.ota http://ota.global.anki-services.com/vic/prod/full/latest.ota

# Download OSKR/dev firmware (may have additional debug tools)
curl -o oskr-latest.ota http://ota.global.anki-services.com/vic/oskr/full/latest.ota

# Alternative: Internet Archive has a complete firmware collection
# including older versions and developer branches
# https://archive.org/details/VectorFirmwareCollection
```

### Step 2: Extract the OTA archive

```bash
# OTA files are TAR archives
mkdir prod-extract oskr-extract

tar xf prod-latest.ota -C prod-extract/
tar xf oskr-latest.ota -C oskr-extract/

# You should see:
# manifest.ini
# manifest.sha256
# apq8009-robot-boot.img.gz    (kernel + initramfs)
# apq8009-robot-sysfs.img.gz   (root filesystem — THIS IS WHAT WE WANT)
```

### Step 3: Get the decryption key

```bash
# The encryption key is publicly known and intentionally weak
# It lives in the Project Victor repository
# Clone or download from: https://github.com/GooeyChickenman/victor

# The ota.pas file contains the decryption passphrase
# The password content is a Chinese phrase meaning "This is a password"
# (Anki engineer humor to satisfy a security consultant)

# If you can't find the key file, the community has documented it extensively
# Check: https://randym32.github.io/Anki.Vector.Documentation/how-to/How%20to%20unzip%20the%20OTA%20file.html
```

### Step 4: Decrypt and decompress the system image

```bash
cd prod-extract

# For OpenSSL 1.1.0+ (which you almost certainly have on macOS):
openssl enc -d -aes-256-ctr \
  -pass file:/path/to/ota.pas \
  -md md5 \
  -in apq8009-robot-sysfs.img.gz \
  -out apq8009-robot-sysfs.img.dec.gz

# Decompress
gunzip apq8009-robot-sysfs.img.dec.gz

# Result: apq8009-robot-sysfs.img.dec — an ext4 filesystem image
```

### Step 5: Mount or extract the filesystem

```bash
# On Linux:
sudo mkdir /mnt/vector-sysfs
sudo mount -o loop,ro apq8009-robot-sysfs.img.dec /mnt/vector-sysfs

# On macOS (ext4 is not natively supported):
# Option A: Use ext4fuse (brew install ext4fuse)
mkdir ~/vector-sysfs
ext4fuse apq8009-robot-sysfs.img.dec ~/vector-sysfs -o allow_other

# Option B: Use 7-Zip to extract
# 7z x apq8009-robot-sysfs.img.dec -o./vector-sysfs

# Option C: Use a Linux VM or Docker container
docker run -it --rm -v $(pwd):/firmware ubuntu bash
# Inside container:
apt update && apt install -y mount
mount -o loop,ro /firmware/apq8009-robot-sysfs.img.dec /mnt
ls /mnt/anki/bin/
```

### Step 6: Extract the target binaries

```bash
# Copy the critical binaries to your working directory
mkdir -p ~/chimera-re/binaries

cp /mnt/vector-sysfs/anki/bin/vic-engine ~/chimera-re/binaries/
cp /mnt/vector-sysfs/anki/bin/vic-anim ~/chimera-re/binaries/
cp /mnt/vector-sysfs/anki/bin/vic-robot ~/chimera-re/binaries/
cp /mnt/vector-sysfs/anki/bin/vic-gateway ~/chimera-re/binaries/
cp /mnt/vector-sysfs/anki/bin/vic-cloud ~/chimera-re/binaries/

# Copy shared libraries
mkdir -p ~/chimera-re/libs
cp /mnt/vector-sysfs/usr/lib/libcozmo*.so ~/chimera-re/libs/
cp /mnt/vector-sysfs/usr/lib/libankisdk*.so ~/chimera-re/libs/

# Copy ALL config files (these are not compiled — directly readable)
mkdir -p ~/chimera-re/configs
cp -r /mnt/vector-sysfs/anki/data/assets/cozmo_resources/config/ ~/chimera-re/configs/

# Copy TF Lite models
mkdir -p ~/chimera-re/models
find /mnt/vector-sysfs -name "*.tflite" -exec cp {} ~/chimera-re/models/ \;

# Verify what you got
file ~/chimera-re/binaries/vic-engine
# Expected: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked
```

### Step 7: Quick initial analysis

```bash
# Check binary size and type
ls -lh ~/chimera-re/binaries/

# List linked shared libraries
readelf -d ~/chimera-re/binaries/vic-engine | grep NEEDED

# Extract all strings (function names, error messages, config paths)
strings ~/chimera-re/binaries/vic-engine > ~/chimera-re/vic-engine-strings.txt
strings ~/chimera-re/libs/libcozmo_engine.so > ~/chimera-re/libcozmo-strings.txt

# Search for emotion-related strings
grep -i "emotion\|mood\|stimulat\|happy\|confident\|social\|trust\|affector\|decay" \
  ~/chimera-re/vic-engine-strings.txt

# Search for behavior-related strings
grep -i "behavior\|behaviour\|priority\|stack\|condition\|cooldown" \
  ~/chimera-re/vic-engine-strings.txt

# Count functions (gives rough idea of binary complexity)
nm -D ~/chimera-re/binaries/vic-engine 2>/dev/null | wc -l
nm -D ~/chimera-re/libs/libcozmo_engine.so 2>/dev/null | wc -l
```

---

## PATH 2: Unlock Your Vector for SSH Access

This gives you access to the live running system — essential for validating decompiled code against actual behavior.

### Check current status

1. **Double-tap the backpack button** while Vector is at eyes
2. The display shows firmware version info
3. Look at the version string:
   - `1.x.x.xxxxd` (ends in `d`) = dev/OSKR firmware, likely already unlocked
   - `1.x.x.xxxx` (no suffix) = production firmware, locked
   - Boot screen shows `OSKR` logo = OSKR installed

### If already running WirePod

Try connecting via SSH:
```bash
# If WirePod is set up, Vector should be on your network
# Find Vector's IP in your router's DHCP client list
# or check WirePod's web interface

ssh root@<vector-ip>
# If this connects: you're unlocked. Skip to "After Unlock" below
# If "Connection refused": production firmware, need to unlock
```

### Unlock a Production Vector (Free, Community Method)

**WARNING: This modifies critical boot partitions. Read everything before starting. Have your Vector on the charger with a block in front of it to prevent it driving off.**

**Method A: Via Recovery Mode (Recommended)**

1. Put Vector in recovery mode:
   - Place on charger
   - Hold backpack button for 15 seconds until light turns green/purple
   - Wait until display shows `anki.com/v`

2. Connect via Chrome browser:
   - Go to `https://devsetup.froggitti.net/` (community tool, more reliable)
   - OR `https://vector-setup.ddl.io` (official but sometimes flaky)
   - Click "Pair with Vector"
   - Enter the PIN shown on Vector's screen

3. In the terminal that appears:
   ```
   wifi-connect "YourSSID" "YourPassword"
   ```

4. Flash the unlock OTA:
   - The community provides unlock OTAs at `https://devsetup.froggitti.net/`
   - Select from the dropdown and apply
   - OR manually: `ota-start http://url-to-unlock.ota`

5. Vector reboots. If you see `OSKR` on the boot screen, the unlock succeeded.

6. Install a usable firmware:
   - WireOS (recommended): available at `https://devsetup.froggitti.net/`
   - OSKR latest: `ota-start http://ota.global.anki-services.com/vic/oskr/full/latest.ota`

**Method B: Via kercre123's unlock-prod.ota (Alternative)**

See: `https://github.com/kercre123/unlocking-vector`

This repo contains:
- `ankidev-nosigning.mbn` — replacement ABOOT that allows dev OTA installation
- `ssh_root_key` — SSH key for dev firmware
- Dev OTA files
- Detailed instructions for EDL/QDL access if needed

### After Unlock: Get SSH Access

```bash
# Download your SSH key via Chrome web setup
# The key is at data/ssh/id_rsa in the downloaded logs archive

# Install the key
cp id_rsa_Vector-XXXX ~/.ssh/
chmod 600 ~/.ssh/id_rsa_Vector-XXXX
ssh-add ~/.ssh/id_rsa_Vector-XXXX

# Connect
ssh root@<vector-ip>

# If using WireOS or dev firmware, the root key from kercre123's repo works:
# https://github.com/kercre123/unlocking-vector/blob/main/ssh_root_key

# Verify you're in
hostname  # should show "Vector-XXXX"
ls /anki/bin/  # should show vic-engine, vic-robot, etc.
```

### Extract Binaries from Live Robot

```bash
# From your Mac/PC (not on the robot):

# Copy all binaries
scp -i ~/.ssh/id_rsa_Vector-XXXX -O root@<vector-ip>:/anki/bin/vic-* ~/chimera-re/binaries/

# Copy shared libraries
scp -i ~/.ssh/id_rsa_Vector-XXXX -O root@<vector-ip>:/usr/lib/libcozmo*.so ~/chimera-re/libs/

# Copy all configs (readable JSON)
scp -i ~/.ssh/id_rsa_Vector-XXXX -O -r root@<vector-ip>:/anki/data/assets/cozmo_resources/config/ ~/chimera-re/configs/

# Note: add -O flag to scp on modern systems (Vector uses old SFTP protocol)

# Optional: observe running processes
ssh root@<vector-ip> "ps aux | grep vic-"
ssh root@<vector-ip> "cat /proc/meminfo"
ssh root@<vector-ip> "top -b -n 1"
```

---

## PHASE 1: Initial Ghidra Analysis

### Setup

```bash
# Install Ghidra (if not already)
# Download from https://ghidra-sre.org/
# Requires JDK 17+

# Create a Ghidra project for Vector
# File → New Project → "chimera-vector-re"
# File → Import File → select vic-engine
# Language: ARM:LE:32:v7 (ARM Cortex little-endian)
# When prompted, run auto-analysis with all defaults
```

### What to Look For First

1. **String cross-references for emotion system:**
   - Search strings for: `"Happy"`, `"Confident"`, `"Stimulated"`, `"Social"`, `"Trust"`
   - These appear in the JSON config loader — follow the XRefs back to the MoodManager class
   - The emotion dimension names are string literals that map to enum values

2. **JSON config loading functions:**
   - Search for paths like `config/engine/emotionevents` and `config/engine/mood_config.json`
   - These paths are hardcoded in libcozmo_engine — finding them reveals the config parsing code
   - The parsing code reveals the data structures used internally

3. **Behavior tree initialization:**
   - Search for `"InitNormalOperation"` — the root behavior ID
   - Search for `"behaviorID"`, `"behaviorClass"` — JSON parsing for behavior nodes
   - Follow the initialization chain to understand how the tree is built

4. **Tick functions:**
   - Look for timer-based callbacks or main loop functions
   - The emotion model updates on a regular tick — finding the tick function reveals the update math
   - The behavior engine also has a regular check cycle

### Export Pseudo-Code for LLM Analysis

```python
# Ghidra script to export all decompiled functions
# Run from Ghidra's Script Manager

import ghidra.app.decompiler as decomp

decompiler = decomp.DecompInterface()
decompiler.openProgram(currentProgram)

output_file = open("/path/to/decompiled_output.c", "w")
function_manager = currentProgram.getFunctionManager()

for func in function_manager.getFunctions(True):
    results = decompiler.decompileFunction(func, 60, None)
    if results.decompileCompleted():
        output_file.write(f"// Function: {func.getName()} at {func.getEntryPoint()}\n")
        output_file.write(results.getDecompiledFunction().getC() + "\n\n")

output_file.close()
decompiler.dispose()
```

---

## PHASE 2: LLM-Assisted Agentic Reverse Engineering

### Recommended Toolchain

| Tool | Purpose | Setup |
|------|---------|-------|
| **Ghidra 12.0+** | Base disassembly and decompilation | Download from ghidra-sre.org |
| **OGhidra** | Agentic LLM ↔ Ghidra bridge (Plan → Execute → Review loop) | `git clone https://github.com/llnl/OGhidra` |
| **GhidrAssist** | ReAct agentic mode with MCP tools | Ghidra extension ZIP from GitHub |
| **LLM4Decompile V2** | Specialized decompilation LLM (refines Ghidra pseudo-code) | HuggingFace model, 22B recommended |
| **Ollama** | Local LLM inference for agentic analysis | `ollama pull qwen2.5-coder:32b` or larger |
| **pyghidra-mcp** | Headless multi-binary analysis via MCP | For Claude Code integration |

### Agentic Analysis Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│  1. Load binary into Ghidra, run auto-analysis               │
│  2. OGhidra/GhidrAssist connects LLM to Ghidra via MCP      │
│  3. Prompt: "Find and analyze the MoodManager class.         │
│     Cross-reference emotion dimension strings.               │
│     Decompile all functions that modify emotion state.        │
│     Map the decay graph implementation."                     │
│  4. LLM autonomously:                                        │
│     - Searches strings → finds "Happy", "Confident" etc.     │
│     - Follows XRefs to MoodManager methods                   │
│     - Decompiles each function                               │
│     - Renames variables based on context                      │
│     - Maps data structures                                   │
│     - Cross-references against TRM descriptions               │
│  5. LLM4Decompile refines Ghidra pseudo-code to readable C   │
│  6. Human reviews, validates against observed behavior         │
│  7. Repeat for next subsystem                                │
└──────────────────────────────────────────────────────────────┘
```

### Target Analysis Order

| Order | Subsystem | Why First | Expected Difficulty |
|-------|-----------|-----------|-------------------|
| 1 | Emotion model (MoodManager) | Highest value for chimera L1. Clean data-driven code. String references from JSON keys give entry points. | MEDIUM — structured, data-driven |
| 2 | Emotion → Behavior coupling | How emotion state influences behavior selection. Reveals the arbitration algorithm. | MEDIUM — follows from #1 |
| 3 | Emotion → Animation coupling | How emotional state modulates animation parameters. The creature-feel secret sauce. | MEDIUM-HARD — may involve lookup tables |
| 4 | Behavior tree engine | How JSON configs become runtime behavior. The instantiation and execution loop. | HARD — complex C++ class hierarchy |
| 5 | Stimulation system | How raw sensor data becomes stimulation events. | MEDIUM — follows known sensor paths |
| 6 | Face recognition pipeline | Feature vector computation and matching. | HARD — heavy math, OpenCV internals |
| 7 | Navigation/SLAM | Map building and path planning. | VERY HARD — complex algorithms |

---

## PHASE 3: Validation

### Compare Decompiled Code Against Known Behavior

For each recovered subsystem:

1. **Config validation:** Do the decompiled data structures match the JSON config format documented in the TRM?
2. **Behavioral validation:** Modify a JSON config on the unlocked robot, observe the change, verify the decompiled code predicts the change correctly
3. **String validation:** Do hardcoded strings in the binary match paths and keys documented in the TRM?
4. **Cross-reference validation:** Does the decompiled call graph match the service architecture diagram in TRM Chapter 6?

### Example Validation Test

```
Test: Emotion decay curve
1. Read the decay graph parameters from mood_config.json
2. Find the decompiled decay function
3. Run the decompiled math with the JSON parameters as input
4. Observe Vector's actual emotion decay via SDK event stream
5. Compare: does the math produce the observed behavior?
If yes: high confidence in decompilation accuracy
If no: identify where the discrepancy is and refine
```

---

## What Success Looks Like

### Minimum Viable RE (good enough to proceed with chimera)
- Emotion model: complete implementation of MoodManager tick, affector application, decay math
- Behavior-emotion coupling: how emotion state feeds into behavior tree condition evaluation
- Stimulation aggregation: how sensor events become emotion events
- ~500-1000 functions recovered with meaningful names and understood purpose

### Full RE (enables direct firmware modification)
- All of the above plus:
- Behavior tree execution engine fully understood
- Animation parameter modulation math recovered
- Internal message passing protocol mapped
- Enough understanding to compile replacement vic-engine with chimera extensions

### Stretch Goal (maximum chimera integration)
- Rebuild vic-engine from decompiled source with chimera layers built in
- Eliminate need for external companion device for L1
- All three chimera layers running natively on the robot
- This is the most ambitious path but yields the deepest creature integration

---

## Estimated Effort

| Phase | Time Estimate | Solo Developer | Agentic (LLM-assisted) |
|-------|--------------|----------------|----------------------|
| Binary extraction | 2-4 hours | Manual | Not needed |
| Ghidra setup + auto-analysis | 1-2 hours | Manual | Not needed |
| Emotion model RE | 1-2 weeks | Hard | 2-4 days |
| Behavior-emotion coupling RE | 1-2 weeks | Hard | 3-5 days |
| Animation coupling RE | 1 week | Medium | 2-3 days |
| Behavior tree engine RE | 2-4 weeks | Very hard | 1-2 weeks |
| Full validation | Ongoing | Continuous | Continuous |

The agentic pipeline (OGhidra + LLM4Decompile + Claude) dramatically reduces the effort. A solo developer in 2024 would spend months. In 2026 with these tools, the emotion model recovery is a matter of days.

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Binaries are heavily stripped/obfuscated | LOW — Anki used standard toolchains, not obfuscation | Would slow RE significantly | Use string refs, JSON config names as anchors |
| OTA download links go offline | LOW — archived on Internet Archive | Can't get firmware | Download and archive locally NOW |
| Emotion model is simpler than expected in code | MEDIUM — may just be float arrays and add/decay | Less to recover but easier to extend | Still valuable — confirms implementation |
| Emotion model has undocumented complexity | MEDIUM — TRM may not describe everything | More to recover | The surprise is the discovery |
| Decompiled C++ is unreadable | LOW-MEDIUM — ARM C++ decompilation has improved greatly | Slows understanding | LLM4Decompile V2 specifically trained for this |
| Legal concerns with RE | LOW — firmware is on your device, personal research use | N/A for personal project | Don't distribute modified firmware commercially |

---

## Files to Archive Locally

Download and store these NOW in case any go offline:

```bash
mkdir -p ~/chimera-re/archive

# Production firmware
curl -o ~/chimera-re/archive/prod-latest.ota \
  http://ota.global.anki-services.com/vic/prod/full/latest.ota

# OSKR firmware
curl -o ~/chimera-re/archive/oskr-latest.ota \
  http://ota.global.anki-services.com/vic/oskr/full/latest.ota

# Internet Archive firmware collection (bookmark for later)
# https://archive.org/details/VectorFirmwareCollection

# Project Victor repo (contains decryption keys and documentation)
git clone https://github.com/GooeyChickenman/victor ~/chimera-re/archive/project-victor

# kercre123 unlocking guide and tools
git clone https://github.com/kercre123/unlocking-vector ~/chimera-re/archive/unlocking-vector

# Randall Maas documentation wiki
# https://randym32.github.io/Anki.Vector.Documentation/

# RE tools
git clone https://github.com/llnl/OGhidra ~/chimera-re/tools/OGhidra
git clone https://github.com/albertan017/LLM4Decompile ~/chimera-re/tools/LLM4Decompile
git clone https://github.com/jtang613/GhidrAssist ~/chimera-re/tools/GhidrAssist
git clone https://github.com/cyberkaida/reverse-engineering-assistant ~/chimera-re/tools/ReVa
```

---

## References

- Vector TRM (543 pages) — Randall Maas, 2021
- kercre123/unlocking-vector — Vector architecture, security, unlock methods
- ankibots.wiki/Unlocking_Vector — Community unlock documentation
- randym32/Anki.Vector.Documentation — OTA extraction, customization guides
- archive.org/details/VectorFirmwareCollection — Complete firmware archive
- OGhidra (LLNL) — Agentic LLM ↔ Ghidra bridge
- LLM4Decompile — Specialized decompilation LLM (1.3B-33B models)
- GhidrAssist — ReAct agentic mode for Ghidra with MCP
- ReVa (reverse-engineering-assistant) — MCP server for Ghidra RE tasks
- pyghidra-mcp — Headless multi-binary Ghidra analysis
