# Sandbox Setup — giving Claude full capacity

*Laptop-actionable instructions for configuring the **Claude Code on the web**
cloud environment that this repo runs in. You (Dexter) mostly drive the sandbox
from the Claude **app on mobile**, where the environment settings can't be
edited — so the few one-time changes below are done **on your laptop/desktop**,
once. After that every session (mobile included) starts at full capacity.*

> TL;DR — Do three things on the laptop, once:
> 1. Paste `scripts/setup_env.sh` into the environment's **Setup script** field.
> 2. Leave **Network access** on **Trusted** (default) — it's already enough for
>    everything we build. Only widen it if we later need a domain not on the
>    default list.
> 3. If you want me to clone *other* repos (e.g. `awesome-go`), add them to the
>    **GitHub repository scope** for this environment.
>
> The repo already ships the matching `scripts/` + `.claude/settings.json`, so a
> resumed session self-heals even if the snapshot is cold.

---

## 0. First, the honest diagnosis (what was actually limiting me)

Two *different* gates were getting blamed on one vague word ("egress"):

| What you saw | The real cause | The fix |
|---|---|---|
| "I had to reinstall flatc / capnp / pip deps again" | The container is **ephemeral** — a fresh clone each session. Nothing I `apt install` mid-session survives. | **Setup script** (snapshot-cached) + SessionStart hook. §2 |
| "Can't clone `infraax/awesome-go`" (403) | **GitHub proxy repo-scope**, restricted to `infraax/chimera-brain`. This is *not* the general network policy. | Add repos to the **GitHub scope**. §4 |
| (hypothetical) "Can't reach some random domain" | **Network access policy** (default = Trusted). | Widen to Custom/Full only if needed. §3 |

The key correction: general web/package egress was **never** the blocker for our
work. `github.com`, `raw.githubusercontent.com`, PyPI, the Go proxy, npm, crates,
and the Ubuntu apt archives are **all on the default "Trusted" allow-list**. The
clone failure was the *GitHub app's repo scope*, and the "reinstalling tools"
pain was *ephemerality*. We fix the two that actually bit us.

---

## 1. How the environment works (the mental model)

A Claude Code on the web session runs in an **isolated, ephemeral container**:

- **Repo is cloned fresh** when the container starts; the container is reclaimed
  after inactivity. Anything not committed + pushed is lost.
- **Setup script** — bash, runs **as root on Ubuntu 24.04**, *before* I start,
  must finish in **< 5 min**. Its result is **cached as a snapshot** and reused;
  it only re-runs when the script text changes, the network policy changes, or
  the snapshot expires (~7 days). This is the right place for the toolchain.
- **SessionStart hooks** — defined in the repo's `.claude/settings.json`, run
  **every** time I launch (fresh *and* resumed). `CLAUDE_CODE_REMOTE=true` marks
  the cloud. Good for a fast idempotent *safety net*, not heavy installs.
- **Network access policy** — chosen when the environment is created/edited:
  - **None** — no outbound.
  - **Trusted** *(default)* — curated allow-list: github.com,
    raw.githubusercontent.com, codeload.github.com, PyPI, npm, Go proxy, crates,
    Ubuntu apt archives, and other common package hosts. **This is what we use.**
  - **Full** — unrestricted outbound.
  - **Custom** — Trusted-style list **plus** an "Allowed domains" box (one host
    per line, `*.` wildcards) and a checkbox to also include the default package
    managers.
- **GitHub proxy** — *separate* from network access. It scopes which repos I can
  read/write and pins `git push` to the working branch using scoped credentials.
  This is what returns **403** on out-of-scope repos.
- **Outbound TLS** goes through an agent proxy (CA bundle at
  `/root/.ccr/ca-bundle.crt`). Already trusted by the standard tools. If a tool
  ever fails TLS or gets 403/405/407, the playbook is `/root/.ccr/README.md` +
  `curl -sS "$HTTPS_PROXY/__agentproxy/status"`. Never disable TLS or unset
  `HTTPS_PROXY`; never retry a 403/407 policy denial — report the host instead.

---

## 2. Make the toolchain persistent (the main fix)  ✅ do this

This kills the "reinstalling tools every session" problem for good.

**On the laptop:** open this environment for editing (the cloud/environment icon
where you start a session or routine — there's no separate "Environments" page;
you edit it from the session/routine creation dialog). Find the **Setup script**
field and paste the **entire contents of [`scripts/setup_env.sh`](scripts/setup_env.sh)**.

That script installs, as root, snapshot-cached:

- **C++ tier:** `build-essential`, `pkg-config`, `cmake`,
  `flatbuffers-compiler` + `libflatbuffers-dev` (EGRV schema codegen),
  `capnproto` + `libcapnp-dev` (control-plane IPC),
  `libspdlog-dev` + `libfmt-dev` (logging — spdlog's bundled fmt needs `-lfmt`).
- **Go tier:** uses the preinstalled `/usr/local/go`; falls back to apt only if
  absent.
- **Python tier:** `numpy`, `pytest`, `flatbuffers`, `usearch`, `hnswlib` — what
  `vector_engram` imports and tests against.

It needs **only the default Trusted network** (apt + PyPI + Go proxy are all
allow-listed). Every command is `|| true`-guarded so one flaky mirror can't abort
the snapshot.

**The repo also ships the safety net** (already committed, no laptop action):
[`.claude/settings.json`](.claude/settings.json) registers a `SessionStart` hook
→ [`scripts/session_start.sh`](scripts/session_start.sh). On a **resumed** session
with a cold snapshot it quietly restores anything missing and returns fast. Setup
script = primary installer; hook = repair.

---

## 3. Network access — leave it on Trusted (change only if needed)

You do **not** need to touch this for our current work. Trusted already covers
github, raw.githubusercontent, PyPI, npm, Go proxy, crates, and apt.

Widen it only if a future task needs a domain that isn't on the default list:

- **Custom** (preferred over Full): set Network access → **Custom**, keep "also
  include default package managers" checked, and add the extra hostnames (one per
  line, `*.example.com` wildcards allowed). This keeps the safe default list and
  just adds what you need.
- **Full**: unrestricted — simplest, least contained. Use only if Custom is
  fiddly and you accept the trade-off.

If I ever hit a real egress wall, I'll name the exact blocked host so you can drop
it into the Custom list — no guessing.

---

## 4. Let me work with other repos (the clone-403 fix)

The `awesome-go` / `awesome-cpp` clones failed because the GitHub proxy scope for
this environment is just `infraax/chimera-brain`. To widen it:

- **In the environment's GitHub settings**, add the repositories I should reach
  (e.g. `infraax/awesome-go`, `infraax/awesome-cpp`) to the **repository scope /
  allowed repositories** for this environment, so the scoped credential covers
  them too.
- Mid-session, I can also call the remote helper `list_repos` to show what's
  available to add, and `add_repo` to pull one into the current session's scope —
  but persistent access is cleanest set on the laptop here.

Reminder for me (unchanged): I still **commit and push only to
`claude/multi-repo-architecture-npf6jv`**, and curation/context clones stay in
untracked sibling folders (`/home/user/_curation_repos/`,
`/home/user/_context_repos/`) — never committed into this repo.

---

## 5. Verification checklist

After the Setup script is saved, start a **fresh** session and have me run:

```bash
go version && flatc --version && capnp --version
python3 -c "import numpy,pytest,flatbuffers,usearch,hnswlib; print('py deps ok')"
cd vector_engram && python -m pytest -q          # expect: all green
cd ../vector_brain/test/contract_roundtrip && ./run.sh   # expect: PASS round-trip
```

All green = full capacity, nothing to reinstall. The cross-language EGRV
round-trip passing is the load-bearing proof that the C++ ⇄ Python contract
toolchain is intact.

If something is red, the fast triage is:

```bash
curl -sS "$HTTPS_PROXY/__agentproxy/status"   # proxy state + recent failures
cat /root/.ccr/README.md                       # per-tool TLS/proxy fixes
```

---

## 6. What changes on each surface

| Surface | Can edit env settings? | What to do |
|---|---|---|
| **Mobile app** (your main driver) | No | Just run sessions — they inherit the laptop config. |
| **Laptop / desktop / web** | Yes | Do §2 (Setup script) once; §3/§4 only if needed. |
| **This repo** | Always | `scripts/` + `.claude/settings.json` are committed, so the safety net travels with the code. |

One-time on the laptop, permanent for every session after.
