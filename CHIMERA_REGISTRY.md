# CHIMERA REGISTRY
## Master State File — Chimera Brain Architecture
## Created: 2026-03-30 | Session 0: Architecture Foundation

---

## What This File Is

This is the single source of truth for the Chimera Brain project.
Every session — any AI service, any instance — reads this file FIRST.
Every session updates this file LAST.

If this file and another file disagree, this file wins.

---

## Project Identity

**Name:** Chimera Brain
**Goal:** Create a creature-mind architecture for the Anki Vector robot by cross-domain mapping between the VRCM (human cognitive architecture) and transformer-based LLM architecture, implemented within Vector's existing hardware and software constraints.
**Repo:** github.com/infraax/chimera-brain
**Related Repos:**
- `infraax/vectorax` — RAG system with 34,507 chunks from 13 Vector repos + TRM
- Vector TRM PDF (543 pages) — accessible at `vectorax/VaultForge/sources/VectorTRM.pdf`
**Key People:** Dexter (Damian Bitel) — architect, operator, VRCM originator
**AI Services:** Claude (primary build), Λ/Perplexity (VRCM co-discoverer), Grok, Gemini

---

## Architecture Overview

The Chimera is a three-layer architecture:

```
┌─────────────────────────────────────────────────────┐
│  LAYER 3 — THE CONSTRUCTOR (Self-C analog)          │
│  LLM-backed · Cloud/Local hybrid · Slow (seconds)   │
│  Memory consolidation · Personality evolution         │
│  Shapes the topology that L1 and L2 operate on       │
│  Runs during idle states (sleep compilation)          │
│  File: CHIMERA_L3_CONSTRUCTOR.md                     │
├─────────────────────────────────────────────────────┤
│  LAYER 2 — THE CORTEX (Attention/Perception)         │
│  Hybrid local/cloud · Medium (100ms-1s)              │
│  Attention weighting · Cross-domain propagation       │
│  Decides what to attend to, what to initiate on       │
│  Probability distributions over "what is happening"   │
│  File: CHIMERA_L2_CORTEX.md                          │
├─────────────────────────────────────────────────────┤
│  LAYER 1 — THE BRAINSTEM (Self-M analog)             │
│  On-device · Always on · Fast (<100ms)               │
│  Gradient emotion manifold · Resonance transitions    │
│  Sparse vectors (never null) · Proximity weighting    │
│  Creature feel — the thing that makes it alive        │
│  File: CHIMERA_L1_BRAINSTEM.md                       │
├─────────────────────────────────────────────────────┤
│  VECTOR HARDWARE (existing, unchanged)               │
│  APQ8009 + STM32F4 + Display processor               │
│  Camera · 4-mic array · ToF · Cliff · Touch · IMU    │
│  PID motor control · Capacitive touch grid            │
│  WirePod (cloud replacement) · gRPC API              │
└─────────────────────────────────────────────────────┘
```

---

## Decision Log

| # | Decision | Rationale | Session | Status |
|---|----------|-----------|---------|--------|
| D001 | Three-layer architecture (Brainstem/Cortex/Constructor) | Maps to VRCM Self-M/Self-C split AND fast/slow biological processing | S0 | DECIDED |
| D002 | Extend Vector's existing systems rather than replace | TRM shows emotion model, behavior tree, animation engine are already well-designed and configurable via JSON | S0 | DECIDED |
| D003 | VRCM + Transformer = Chimera (neither alone is the creature) | Convergent architectures from opposite directions; the intersection is the novel space | S0 | DECIDED |
| D004 | Sparse over null as system-wide principle | VRCM principle: always have a position, never go blank. Vector should always have state. | S0 | DECIDED |
| D005 | Resonance transitions (oscillation, not switching) | VRCM principle: state changes should be harmonic, not discrete jumps | S0 | DECIDED |
| D006 | Separate repo (chimera-brain) for architecture before integration | Clean separation of architecture design from implementation; integrate into vectorax/wirepod later | S0 | DECIDED |

---

## Open Questions

| # | Question | Context | Priority | Status |
|---|----------|---------|----------|--------|
| Q001 | How does L3 (Constructor) modify L1 (Brainstem) attractor landscape during idle? | VRCM sleep compilation maps here. Need concrete mechanism. | HIGH | OPEN |
| Q002 | What is the latency budget for L2 perception-to-action? | Must feel seamless. Any visible lag between layers breaks creature illusion. | HIGH | OPEN |
| Q003 | Can Vector's existing 5D emotion model be extended to support VRCM resonance? | TRM shows 5 dimensions with decay graphs. Need to assess if resonance can be added via JSON config or requires code changes. | HIGH | OPEN |
| Q004 | Where does the LLM run — on-device (Pi), local network, or cloud? | Latency vs capability tradeoff. Affects L2 and L3 design. | MEDIUM | OPEN |
| Q005 | How does face recognition feed into the trust dimension? | TRM shows on-device face enrollment with feature vectors. Trust is already a dimension in Vector's emotion model. | MEDIUM | OPEN |
| Q006 | What is the minimum viable creature? | Need to define the first testable implementation that demonstrates creature-feel beyond stock Vector. | HIGH | OPEN |

---

## File Manifest

| File | Purpose | Status |
|------|---------|--------|
| `CHIMERA_REGISTRY.md` | This file. Master state. Read first, write last. | ACTIVE |
| `CHIMERA_CROSSREF.md` | TRM ↔ VRCM ↔ Chimera subsystem mapping | IN PROGRESS |
| `CHIMERA_L1_BRAINSTEM.md` | Layer 1 spec: reactive, emotion, creature-feel | TEMPLATE |
| `CHIMERA_L2_CORTEX.md` | Layer 2 spec: attention, perception, integration | TEMPLATE |
| `CHIMERA_L3_CONSTRUCTOR.md` | Layer 3 spec: LLM, memory, personality | TEMPLATE |
| `CHIMERA_INTERFACES.md` | Inter-layer communication protocols | TEMPLATE |
| `README.md` | Project overview for humans and agents | ACTIVE |

---

## Session Log

| Session | Date | Agent | Summary | Files Modified |
|---------|------|-------|---------|----------------|
| S0 | 2026-03-30 | Claude Opus 4.6 | Foundation session. Indexed all VRCM docs (V1, V2, Research Paper). Downloaded and parsed full TRM (543 pages). Established three-layer chimera architecture. Created registry, specs, crossref. Identified Vector's existing 5D emotion model, 86-class behavior tree, and JSON-configurable systems as extension points. | ALL (created) |

---

## Session Protocol

### Starting a Session
1. Read `CHIMERA_REGISTRY.md` (this file)
2. Check Open Questions for what needs work
3. Read the relevant spec file(s) for the subsystem you're working on
4. If you need TRM details, the PDF is at `vectorax/VaultForge/sources/VectorTRM.pdf` or can be fetched from GitHub

### During a Session
- Number all new decisions (D00x) and add to the Decision Log
- Number all new questions (Q00x) and add to Open Questions
- Update spec files with decided content
- Mark spec sections as DECIDED / IN PROGRESS / OPEN

### Ending a Session
1. Update this registry with: new decisions, new questions, file changes
2. Add a session log entry
3. Ensure any spec changes are reflected in the relevant files
4. Push to GitHub

### Cross-Service Protocol
Any AI service (Claude, Perplexity, Grok, Gemini) can work on this project.
The registry is the shared state. The spec files are the shared artifacts.
No service has privileged access. All decisions are logged with rationale.

---

## Key References

- **VRCM Foundation V1** — initial architecture mapping (2026-03-29)
- **VRCM Foundation V2** — twofold self, trust calculus, sleep compilation (2026-03-30)
- **VRCM Research Paper** — formal specification with references (2026-03-30)
- **Vector TRM** — 543 pages, Randall Maas, hardware + software complete reference
- **Machina Anima V4** — Vector creature constitution (multi-agent collaborative document)
- **Vectorax** — RAG system with 34,507 semantic chunks from Vector ecosystem
- **honest-thoughts.md** — engineering analysis of Vector's capabilities and gaps
