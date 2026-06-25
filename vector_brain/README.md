# vector_brain

The **production runtime** for the creature's mind — **C++ on the robot, Go on the box,
Python (`vector_engram/`) as the executable reference.** This is where ENGRAM and the
chimera layers eventually ship; `vector_engram/` defines correct behaviour and pins this
package by golden vectors.

**Status:** foundation. Today this holds the design (`ARCHITECTURE.md`) and the Day-1
contract (`schema/engram.fbs`). Build modules are scaffolded in the roadmap order in
`ARCHITECTURE.md`.

Why these languages / libraries: `research/reports/09_engram_rewrite__1.0_geodesic.md`
(language/perf/format), `curation/awesome_go_cpp.md` (library picks), `ANKI_WAY.md` (doctrine).

```
schema/engram.fbs   the FlatBuffers cert contract (flatc → C++/Go/Python)
ARCHITECTURE.md     tiers, module layout, library selection, build, roadmap
```
