# ADR — Cross-language integration seams for ENGRAM (Python ↔ Vector's C++/Go)
## Should we prepare hooks/entry-points/comms in ENGRAM now, for later C/Go integration?
## Created: 2026-06-23 · Dexter × Claude Opus 4.8 · status: PROPOSED (recommend Approach 2)

---

## The situation

`vector_engram` is Python (numpy/hnswlib), runs on the **box** (Pi/Jetson/Mac). Vector's
own code is **C++** (`engine/`, the real-time brain) + **Go** (the `vic-*` services / cloud
seam). The box↔robot link is already decided (AD-02: our custom cloud server speaks the
existing `behaviorComponentCloudServer` UDP/CLAD contract).

Question: do we bake integration hooks / entry-points / message contracts into ENGRAM
**now**, or defer until we actually wire the robot?

**TL;DR recommendation: Approach 2 (contract-first).** Define and freeze the *interface*
now — the binary format as a cross-language ABI, golden fingerprint vectors, message
schemas, and one thin Python service boundary — but write **no** C/Go code, FFI, or NEON
kernels yet. This is precisely the Anki way; the bridges themselves are YAGNI until the
robot side is the active task.

---

## The three approaches

### Approach 1 — Defer everything ("pure Python now, integrate later")
Keep ENGRAM purely internal; design the contract only when C/Go work begins.
- **For:** fastest now; maximal YAGNI; requirements clarify before we commit to a contract;
  zero premature abstraction.
- **Against:** Python-isms leak into the design (object shapes, implicit assumptions) and
  become painful to cross later; no way to validate a future C/NEON fingerprint against the
  Python reference; cross-language debugging is bolted on at the end (the worst time);
  contradicts Anki's own practice of defining inter-process contracts up front (CLAD).
- **Risk:** rework + a hard, late integration crunch.

### Approach 2 — Contract-first ("define the seam now, implement only Python") ★ recommended
Freeze the *interface* and keep the Python implementation behind it. Concretely, the cheap
high-value moves:
1. **Treat the `EGRV` `.eng` format as the shared ABI.** It already is one: fixed
   little-endian layout + fp16, trivially parseable in C and Go. Document it as the
   cross-language contract and ship **golden test vectors** (bytes → expected decode).
2. **Make the fingerprint a language-neutral spec + golden vectors** (input frames →
   expected fingerprint), so the future C/NEON on-robot path can be verified bit-approx
   against the numpy reference. The math is just `rFFT` + L2-norm — portable.
3. **Define (don't implement) the robot↔box message schemas** — `SituationWrite`,
   `SituationQuery`, `RetrievalResult` — ideally in **CLAD** (Anki's own IDL, already in the
   tree) or protobuf, **versioned**, mapped onto the existing `behaviorComponentCloudServer`
   seam. No Go server yet — just frozen shapes.
4. **One thin Python service boundary** (`service.py`): functions that take/return **bytes +
   plain dicts/JSON**, never numpy objects or pickles across the line. Add a tiny local
   HTTP/UDP wrapper as a **debug entry-point now** so ENGRAM is pokeable from any language or
   the CLI immediately.
- **For:** this is the Anki way (contract-first, CLAD, clean process boundaries, debuggable
  from day one); enables the C/NEON fast path to be validated against Python; lets robot-side
  and box-side proceed on independent timelines; the binary format is *already* C/Go-friendly
  so the cost is mostly documentation + a few fixtures; versioning absorbs requirement changes.
- **Against:** modest work now; must pick the IPC (HTTP vs gRPC vs UDP/CLAD) and risk
  designing a slightly-wrong contract early — mitigated by schema versioning and keeping the
  surface tiny (write / query / result).

### Approach 3 — Build the bridges now ("full integration scaffolding")
Write the Go cloud-server stub, C fingerprint stub, CLAD-generated bindings, FFI, NEON, etc.
- **For:** everything wired end-to-end immediately.
- **Against:** heavy premature work in two more languages before the robot side exists; high
  churn/rework; you'd maintain C/Go with no consumer; violates YAGNI and our own doctrine
  ("evidence before building"); slows the things we actually need next (DU). Real failsafe
  testing of those bridges isn't even possible without the robot.
- **Risk:** large sunk cost that gets rewritten.

---

## Why Approach 2 is the Anki way (not just a compromise)

- **Anki defined contracts first.** CLAD exists precisely so C++/Go/Python share typed
  message definitions across process boundaries. Freezing schemas now mirrors that.
- **Clean, legible boundaries.** Our own `CHIMERA_INTERFACES.md` and `ANKI_WAY.md` ("clean
  process boundaries", "designer-tunable/auditable") argue for an explicit, inspectable seam.
- **Debuggable from day one.** A binary-format spec + golden vectors + a thin local server =
  you can inspect, replay, diff, and cross-check across languages *immediately* — the "ease of
  access / debugging" you asked about, achieved by a contract, not by bridges.
- **Self-cancellation / verification discipline.** Golden fingerprint vectors let the future
  on-robot C/NEON implementation be proven equivalent to the trusted Python reference — the
  same "validate against ground truth" rule we used in the soak.
- **It respects YAGNI where it should.** No C/Go/FFI/NEON until the robot integration is the
  task — those are exactly the parts that need the robot to be testable.

---

## Concrete "do now" list (small, behind Approach 2)
1. `vector_engram/FORMAT.md` — the `EGRV` ABI spec (offsets, types, endianness) + a
   `tests/golden/` with `.eng` byte fixtures and a decode round-trip test (already de-facto
   covered; formalize as the cross-language contract).
2. `tests/golden/fingerprint_vectors.*` — frozen (frames → fingerprint) fixtures + a test
   asserting the Python reference matches them (the spec the C/NEON path must meet).
3. `schemas/engram.clad` (or `.proto`) — `SituationWrite` / `SituationQuery` /
   `RetrievalResult`, **versioned**; no server impl.
4. `vector_engram/service.py` — one thin boundary (bytes/JSON in, bytes/JSON out) + an
   optional local HTTP/UDP debug endpoint. Keep numpy strictly *inside* it.

## Explicitly defer (Approach 3, until robot-integration is active)
- The Go custom-cloud server implementation; C/NEON fingerprint kernel; FFI bindings;
  CLAD codegen wiring; on-device hot-index in C. These slot into the **frozen contract** later.

---

## Decision
Adopt **Approach 2**. It costs little (the format is already cross-language), removes the
biggest future-integration risks (leaked Python-isms, no cross-language verification, late
debugging), and is faithful to how Anki actually built Vector — while keeping us from
sinking time into C/Go bridges before there's anything on the robot to connect them to.

*Open choice to confirm: IPC mechanism for the eventual robot↔box link — reuse the existing
UDP/CLAD `behaviorComponentCloudServer` seam (most Anki-native) vs. a simple local HTTP/gRPC.
Recommendation: define schemas in CLAD to match Anki, expose an HTTP debug endpoint now for
convenience, keep the production transport decision with AD-02.*
