# Chimera RE — Session Handoff
## Date: 2026-03-31 | Sessions: S1 + S2 | Agent: Antigravity

---

## Status: PAUSED — Resume Ghidra Decompilation

### What Was Accomplished

#### S1: Environment + Extraction (COMPLETE)
- Firmware OTA 0.13.1545 downloaded from Internet Archive, decrypted, extracted
- All binaries, libraries, configs, models extracted via Docker ext4 mount
- 17,409 demangled symbols cataloged, 536 emotion/behavior-related
- DDL open-source engine code cloned (299 C++ files)
- Ghidra 12.0.4 installed with JDK 21

#### S2: Ghidra Analysis (PARTIALLY COMPLETE)
- Auto-analysis completed (303s, 35,291 functions identified)
- **78 exported** MoodManager functions decompiled → `mood_manager_decompiled.c` (3,247 lines)
- **18 core internal** MoodManager functions decompiled → `mood_core_decompiled.c` (2,103 lines)
- **Q007 ANSWERED:** `GetSimpleMood(stim, conf)` uses only Stimulated + Confident dimensions
- Full subsystem extraction script created but was still running at session end (resource-intensive)

---

## File Locations

### Extracted Firmware (`~/chimera-re/`)
```
~/chimera-re/
├── binaries/          # vic-engine, vic-anim, vic-robot, vic-gateway, etc.
├── libs/              # libcozmo_engine.so (13.6 MB — THE target)
├── configs/           # 429 JSON files
│   └── engine/
│       ├── mood_config.json              # Decay graphs, value ranges
│       ├── emotionevents/                # 11 emotion event JSON files
│       └── behaviorComponent/            # 286 behavior JSON configs
├── models/            # 2 TFLite models
├── archive/
│   ├── ddl-vector/    # DDL open-source (engine/, clad/, docs/)
│   └── project-victor/ # Decryption key
├── tools/
│   ├── ghidra_12.0.4_PUBLIC/    # Ghidra installation
│   └── ExtractMoodFunctions.py  # Ghidra scripts (Python won't work, use Java)
├── ghidra-project/
│   └── chimera-vector/          # Ghidra project with analyzed binary
└── ghidra-output/               # Decompiled output
    ├── mood_manager_decompiled.c # 78 exported functions (3,247 lines)
    ├── mood_core_decompiled.c   # 18 core internal functions (2,103 lines)
    ├── mood_function_index.txt  # Exported function address map
    ├── mood_core_index.txt      # Core function address map
    └── libcozmo-symbols-demangled.txt  # Full 17,409 symbol table
```

### Project Files (`~/Chimera/chimera-brain/`)
```
CHIMERA_REGISTRY.md              # Master state — decisions, questions, sessions
CHIMERA_REVERSE_ENGINEERING.md   # RE spec and methodology
CHIMERA_RE_HANDOFF.md            # This file
Reesearch-Rapport.md             # Architecture research
```

---

## What Needs To Be Done Next (Priority Order)

### 1. IMMEDIATE: Targeted Function Decompilation
The big 3-subsystem Ghidra job was too resource-intensive. Instead, run **small targeted extractions**:

```bash
# Set up env
export JAVA_HOME=/opt/homebrew/Cellar/openjdk@21/21.0.10/libexec/openjdk.jdk/Contents/Home
GHIDRA=~/chimera-re/tools/ghidra_12.0.4_PUBLIC/support/analyzeHeadless
PROJECT=~/chimera-re/ghidra-project
```

**Priority functions to decompile** (address → what it does):

| Address | Identified As | Why Needed |
|---------|--------------|------------|
| `0x004722c4` | Decay curve evaluator | Core math — called in tick loop |
| `0x00472378` | AddToEmotion helper | How emotions are incremented |
| `0x0047242c` | SetEmotion helper | How emotions are directly set |
| `0x004728e0` | Repetition penalty calc | Cooldown math |
| `0x004759e8` | SimpleMood updater | The Stimulated+Confident→SimpleMoodType mapping |
| `0x00475570` | Audio parameter updater | How mood drives audio |
| `0x00475720` | WebViz mood sender | External reporting format |

**Use small, targeted Ghidra scripts** — one function at a time, or write a script with a small address list instead of scanning all strings in the binary.

### 2. Behavior System Extraction
**9 directories were NOT open-sourced by DDL:**
- `moodSystem/` — Partially recovered (see above)
- `behaviorComponent/` — Behavior tree engine, behavior arbitration
- `aiComponent/` — AI decision making core
- `components/` — Robot component system
- `userDefinedBehaviorTree/` — Custom behavior tree support
- `emotionevents/`, `lights/`, `math/`, `imageBuffer/`

Use the same string cross-reference technique that worked for moodSystem. Target strings like:
- "BehaviorManager", "BehaviorStack", "BehaviorComponent"
- "ICozmoBehavior", "DelegateIfInControl", "BehaviorSystemManager"

### 3. Create Clean Knowledge Base
Package everything into agent-consumable format:
- Organized symbol table by namespace/subsystem
- Struct layouts with field offsets
- Function signature map (address → name → decompiled C)
- JSON config schema documentation

### 4. Begin L1 Brainstem Implementation
With the emotion model understood, implement a Python/Rust replica:
- 5D emotion vector with [-1, 1] range
- Decay graphs loaded from `mood_config.json`
- EmotionAffector system with repetition penalties
- `GetSimpleMood(stim, conf)` classifier
- gRPC interface for external injection

---

## Key Technical Notes

### Ghidra Tips
- **Python scripts DON'T work** — Ghidra 12 needs PyGhidra which isn't available in headless. Use `.java` scripts only.
- **Place scripts in** `ghidra_12.0.4_PUBLIC/Ghidra/Features/Base/ghidra_scripts/` for them to be found.
- **Don't scan all strings** — it takes forever on a 13.6 MB binary. Instead, find specific address ranges you want and decompile directly.
- The Ghidra project is saved at `~/chimera-re/ghidra-project/chimera-vector` — analysis is cached, no need to re-run auto-analysis.

### Command Gotchas
- `grep` is aliased to `rg` (ripgrep) — use `/usr/bin/grep` for standard behavior
- `find` is aliased to `fd` — use `/usr/bin/find` for standard behavior
- Homebrew binutils are at `/opt/homebrew/opt/binutils/bin/`

### Emotion Model Summary
```
EmotionType enum (5 values):
  Happy=0, Confident=1, Social=2, Stimulated=3, Trust=4
  Each ranges [-1.0, 1.0], decays toward 0.0 over time

SimpleMoodType enum (5 categories):
  Default=0, LowStim=1, MedStim=2, HighStim=3, Frustrated=4
  Computed from: GetSimpleMood(Stimulated, Confident) only!

Decay: piecewise linear graph (mood_config.json)
  Default: 0s→100%, 10s→100%, 30s→90%, 75s→60%, 150s→0%
  
Emotion Events: JSON files in emotionevents/
  Each event has: name, emotionAffectors[{type, value}], repetitionPenalty graph

MoodManager struct stride: 0x28 (40 bytes) per emotion
Tick loop iterates emotions 0-3 (skips Trust=4 for decay)
```

---

## Session Protocol Reminder
When resuming:
1. Read `CHIMERA_REGISTRY.md` first
2. Read this handoff file
3. Check `~/chimera-re/ghidra-output/` for what's already decompiled
4. The Ghidra project is pre-analyzed — just run `-process -noanalysis -postScript`
