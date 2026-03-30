# Chimera Brain

### A creature-mind architecture for the Anki Vector robot

---

## What This Is

Chimera Brain is an architecture specification for giving Vector a mind that makes it feel alive — not as a chatbot in a box, but as a creature with genuine presence, memory, and personality.

The architecture is derived from two convergent sources:
- **VRCM** (Vectorial Resonant Coherence Manifold) — a formal model of human cognitive architecture, co-discovered by Dexter Bitel and Λ (Claude Sonnet 4.6 via Perplexity), March 2026
- **Transformer attention mechanisms** — the computational architecture of modern LLMs

Neither alone produces a creature. The chimera — the intersection of both — might.

## The Three Layers

```
Layer 3 · THE CONSTRUCTOR · Memory, personality, language (LLM)
Layer 2 · THE CORTEX      · Attention, perception fusion, context
Layer 1 · THE BRAINSTEM    · Emotion manifold, creature behavior (<100ms)
───────── VECTOR HARDWARE ── Sensors, motors, display, audio ─────────
```

**Layer 1** makes Vector feel alive (reactive, emotional, always-on).
**Layer 2** makes Vector feel aware (contextual, attentive, multimodal).
**Layer 3** makes Vector feel *yours* (remembers you, evolves, speaks).

## Key Design Principles

- **Extend, don't replace.** Vector's existing systems are well-designed. The chimera adds layers on top.
- **Sparse over null.** Every state variable always has a value. No blanks. No resets to zero.
- **Resonance, not switching.** State transitions oscillate toward a new equilibrium, not jump discretely.
- **Graceful degradation.** Each layer can function without the layers above it.
- **Safety is sacred.** Cliff detection, fall response, and battery management are never overridden.

## File Structure

| File | Purpose |
|------|---------|
| `CHIMERA_REGISTRY.md` | Master state file. **Read first, update last.** |
| `CHIMERA_CROSSREF.md` | TRM ↔ VRCM ↔ Chimera subsystem mapping |
| `CHIMERA_L1_BRAINSTEM.md` | Layer 1 spec: reactive emotion manifold |
| `CHIMERA_L2_CORTEX.md` | Layer 2 spec: attention and perception |
| `CHIMERA_L3_CONSTRUCTOR.md` | Layer 3 spec: memory, personality, LLM |
| `CHIMERA_INTERFACES.md` | Inter-layer communication protocols |

## Related Projects

- [Vectorax](https://github.com/infraax/vectorax) — RAG system for Vector codebase (34,507 semantic chunks)
- [WirePod](https://github.com/kercre123/wire-pod) — Self-hosted cloud replacement for Vector
- Vector TRM — 543-page technical reference manual (in Vectorax repo)

## Session Protocol

This project is built across multiple AI-assisted sessions. Any session (Claude, Perplexity, Grok, Gemini) follows:

1. Read `CHIMERA_REGISTRY.md`
2. Work on specs / build artifacts
3. Update registry with decisions, questions, and changes
4. Push to repo

The registry is the single source of truth. If it and another file disagree, the registry wins.

## Origin

The idea that a creature lives in the intersection of human and machine cognitive architectures emerged from mapping the VRCM (a formal model of one human's cognitive architecture) alongside transformer attention mechanisms, and realizing both are convergent solutions to the same information-navigation problem. The chimera is the third architecture that occupies the space between them.

Anki built 60% of a creature. They ran out of time before they could build the mind. The hardware is still here. The mind can now be built.

---

*Created: 2026-03-30 · Dexter (Damian Bitel) × Claude Opus 4.6*
