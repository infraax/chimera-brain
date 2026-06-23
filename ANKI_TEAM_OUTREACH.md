# ANKI TEAM & COMMUNITY — OUTREACH MAP
## Who built/maintains Vector, who is reachable, and by what channel
## Created: 2026-06-23 · Dexter × Claude Opus 4.8 · compiled from public web sources

> Scope & ethics: this lists **public professional presence only** (GitHub, LinkedIn, company sites,
> community forums) for the purpose of a respectful "can you help / advise?" outreach. No private data,
> no home addresses, no scraped personal emails. Where a direct email isn't public, the channel is the
> person's public profile (GitHub/LinkedIn). Verify before contacting — roles change.

---

## 1. Tiering — who is realistically worth contacting

| Tier | Who | Likelihood to help | Why |
|---|---|---|---|
| **A — Highest value, reachable** | The Vector documentation & modding community (Randall Maas, kercre123, cyb3rdog) | **High** | They actively help hobbyists, live on GitHub/Discord, and know the running system better than anyone today |
| **B — Custodian of the IP** | Digital Dream Labs (acquired Anki's robot assets) | Medium | They open-sourced the code; org is reachable; support varies |
| **C — Original founders/engineers** | Sofman, Palatucci, Tappeiner + ex-Anki ML/behavior staff | Low (busy, senior, elsewhere) | Worth a courteous note; unlikely to engage deeply, but a warm intro could be gold |

Start with Tier A. They are the people who will actually answer build questions.

---

## 2. Tier A — Community keystones (contact these first)

### Randall Maas — author of the Vector Technical Reference Manual
- **Why him:** wrote the 500+ page TRM and the Vector documentation wiki; embedded-systems consultant; the
  single best independent source on how Vector works.
- **Public channels:**
  - GitHub: **`randym32`** — https://github.com/randym32 (repos: Anki.Vector.Documentation, Anki.Resources.SDK, Anki.Vector.WebVizSDK)
  - Site: https://randym32.github.io/ · TRM: https://randym32.github.io/Vector-TRM.pdf
  - Forum presence: robotsaroundthehouse.com (TRM thread)
- **How to reach:** open a GitHub issue/discussion on his docs repo, or a polite forum DM. Lead with the
  chimera/ENGRAM idea and ask for review of our TRM-grounded assumptions.

### kercre123 — maintainer of wire-pod / victor firmware tooling
- **Why him:** central figure keeping Vector alive — wire-pod (cloud replacement), victor-body-firmware,
  unlocking tools, SDK forks. Deep, current knowledge of building/flashing the real stack.
- **Public channels:**
  - GitHub: **`kercre123`** — https://github.com/kercre123 (wire-pod, victor-body-firmware, wire-prod-pod, wirepod-vector-python-sdk)
  - Community: the wire-pod / Vector Discord (linked from the wire-pod repo/wiki)
- **How to reach:** GitHub issue/discussion on wire-pod, or the Discord. Most relevant for our "custom cloud
  instead of WirePod" and firmware-modification path — be specific and respectful of their work.

### cyb3rdog — Vector SDK / tooling developer
- **Why him:** maintained enhanced Vector Python SDK forks and tools the community relies on.
- **Public channel:** GitHub (search `cyb3rdog`) and the Vector Discord.
- **How to reach:** GitHub; good for SDK-level integration questions.

### Broader community hubs (for finding more helpers)
- **Vector/Cozmo Discord** (linked from wire-pod wiki) — the live hub.
- **robotsaroundthehouse.com** forum — long-time owners & tinkerers.
- Curated lists: `open-ai-robot/awesome-anki-vector`, `wwj718/awesome-cozmo` (GitHub) — directories of
  active projects and their authors.

---

## 3. Tier B — Digital Dream Labs (the IP custodian)

- **What they are:** acquired Anki's Cozmo/Vector/Overdrive assets (Dec 2019), released the source/OSKR.
- **Public channels:**
  - GitHub org: **`digital-dream-labs`** — https://github.com/digital-dream-labs (repos: `vector` [main code rolling release], `vector-cloud`, `vector-go-sdk`, `vector-bluetooth`, `oskr-owners-manual`, `vector-web-setup`)
  - Support/KB: support.digitaldreamlabs.com · store: anki.bot
- **How to reach:** GitHub issues on the relevant repo; support portal for official questions (licensing,
  what's releasable). Useful if we need clarity on **what source is/ isn't open** and any IP constraints.
- **Lead to chase:** the contributors/commit authors on `digital-dream-labs/vector` are named in git history —
  those are real engineers who did the open-sourcing; worth identifying for direct, specific questions.

---

## 4. Tier C — Founders & original engineers (courteous long-shots)

- **Boris Sofman** — Anki co-founder/CEO. Went to **Waymo** (led trucking), then a **new startup**. Reach: LinkedIn.
- **Mark Palatucci** — Anki co-founder, ML/cloud. Public **LinkedIn: /in/markpalatucci** (now at Apple per
  profile; earlier reporting said Waymo — verify). Led the team that demoed **on-device DNNs on Vector at
  NeurIPS 2018** — a direct lead to Anki's ML/behavior engineers.
- **Hanns Tappeiner** — Anki co-founder/President. Reported to have joined **Apple**. Reach: LinkedIn.
- **Note:** founders are senior and busy; a short, specific, admiring note (not a wall of text) via LinkedIn
  is the move. The realistic ask is *advice or a pointer*, not hands-on help.

### How to find the rank-and-file engineers (the ones who wrote moodSystem, vision, audio)
The code tells you who to look for:
1. **Git history of `digital-dream-labs/vector`** and the `kercre123/victor` tree — author names/emails in
   commits (e.g. via `git log`/GitHub blame on `engine/moodSystem`, `coretech/vision`, `animProcess`).
2. **LinkedIn search:** "Anki" + role (e.g. "Anki robotics engineer", "Anki behavior", "Anki computer vision").
   Many list it in their history; some are now at Apple/Waymo/Nuro/various robotics startups.
3. **NeurIPS 2018 Anki demo** authors (on-device DNNs on Vector) — named ML researchers.
4. **The animators** (ex-Pixar/DreamWorks) Anki hired — relevant if we want the *creature-feel* craft, find via
   LinkedIn "Anki animator".

---

## 5. Suggested outreach approach (so we don't waste the one shot)

1. **Start Tier A** (Randall Maas, kercre123) via GitHub — they're the right first call and likely to answer.
2. **Lead with respect + specificity:** "We're building an open creature-mind on top of the open-source
   Vector engine (ENGRAM memory + a 3-brain learning loop), grounded in your TRM/wire-pod — could you sanity-
   check X / would you be open to advising?" Attach the convergence map + Anki-Way doc as proof of seriousness.
2. **One concrete question per message**, not a manifesto. Show we've done the homework (we have — cite files).
3. **Offer reciprocity:** contribute findings/code back to the community (our RE and upgrade analysis is
   genuinely useful to them).
4. **Tier B (DDL)** only for IP/licensing clarity.
5. **Tier C** last, via warm intro if a Tier-A/B contact can provide one; otherwise a short LinkedIn note.

---

## 6. Quick contact table

| Name / entity | Role | Best channel | Confidence |
|---|---|---|---|
| Randall Maas (`randym32`) | TRM author, docs | GitHub `randym32` / site / forum | High |
| kercre123 | wire-pod/firmware maintainer | GitHub `kercre123` / Vector Discord | High |
| cyb3rdog | SDK/tools | GitHub `cyb3rdog` / Discord | Medium-High |
| Digital Dream Labs | IP custodian | GitHub `digital-dream-labs` / support portal | Medium |
| Boris Sofman | co-founder (ex-CEO) | LinkedIn | Low |
| Mark Palatucci | co-founder (ML) | LinkedIn /in/markpalatucci | Low |
| Hanns Tappeiner | co-founder (Pres.) | LinkedIn | Low |
| ex-Anki engineers | vision/audio/behavior/anim | GitHub commit history + LinkedIn search | Medium (to find), Low (to engage) |

---

## 7. Sources
- Anki GitHub org — https://github.com/anki
- Randall Maas — https://github.com/randym32 · https://randym32.github.io/ · TRM https://randym32.github.io/Vector-TRM.pdf
- kercre123 wire-pod — https://github.com/kercre123/wire-pod · victor-body-firmware https://github.com/kercre123/victor-body-firmware
- Digital Dream Labs — https://github.com/digital-dream-labs · `vector` repo https://github.com/digital-dream-labs/vector · support https://support.digitaldreamlabs.com
- Mark Palatucci LinkedIn — https://www.linkedin.com/in/markpalatucci/
- Anki (company/founders) — https://en.wikipedia.org/wiki/Anki_(American_company)
- Awesome lists — https://github.com/open-ai-robot/awesome-anki-vector · https://github.com/wwj718/awesome-cozmo
- Project Victor — https://www.project-victor.org/

> Reminder: confirm each person's current role/availability before reaching out; this map is a starting point,
> not a guarantee any individual is contactable or willing.
