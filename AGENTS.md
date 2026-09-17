# AGENTS.md

## Overview

AGENTS-OS is a coordination and containerization framework for AI agent swarms
(Antigravity IDE, Claude Code, Cursor, Zed). It provides architectural rigor via
the async **Swarm Triad** model (Coordinator / Builder / Auditor), conflict-free
distributed state sync across machines (Laptop WSL, VPS, Desktop) through
`.agents/MEMORY.md` and `.agents/task.md`, and dynamic skill-library
distribution to downstream projects via `os-init`, `os-upgrade-project`, and
`os-add-skill`. This repo is itself the framework's source — changes here
propagate outward to every project that bootstraps from it.

## Task-routing table

| When the task involves… | Read first | Key rules |
|---|---|---|
| Swarm role definitions, SDLC flow, commit discipline | `CLAUDE.md`, `SDLC.md` | Worktree-only implementation — never commit directly to `master`/`main`; atomic commits, Conventional Commits, ≤50-char subject |
| Swarm role isolation & PreToolUse gates | `scripts/guard_coordinator_pretool.py`, `.agents/hooks/claude-pre-tool-guard.sh`, `scripts/check_coordinator_role.sh` | Coordinator NEVER writes production code outside `tmp/worktrees/`; PreToolUse gate physically blocks `write_to_file` and `replace_file_content` in root; `/plan` mandates Builder subagent delegation. |
| Cross-machine state sync (`MEMORY.md` / `task.md`) | `.agents/MEMORY.md`, `.agents/task.md`, `.gitattributes` | `merge=union` belongs only on append-only files (`MEMORY.md`). Checklist files (`task.md`, `- [ ]`/`- [x]`) must NOT carry `merge=union` — it duplicates lines instead of resolving the conflict. |
| Lifecycle hooks (session start/end, stop, pre-compact) | `.claude/settings.json`, `.agents/hooks.json` | `.claude/settings.json` is what Claude Code actually reads. `.agents/hooks.json` is the Antigravity/Coordinator-side format. The two are not interchangeable and must be kept in sync by hand when hook logic changes. |
| Handshake protocol / swarm coordination artifacts | `scripts/generate-handshake.py`, `scripts/validate-handshakes.py`, `.agents/swarm/` | Real CLI signature: `--role {builder,auditor,coordinator} --conversation-id <uuid> --status {SUCCESS,FAILURE,PARTIAL} [--files] [--notes]`. `--task`/`--branch`/`--status complete` do not exist on this script — verify with `--help` before scripting a call. |
| Installer / bootstrap scripts (`os-init`, `os-init-claude`, `os-upgrade-project`, `os-add-skill`, `INSTALL.sh`) | `scripts/*`, `os-*`, `execution/test_bootstrap.sh` | Builder role must not open these for functional edits without Coordinator approval (`CLAUDE.md` §2.5). QA gate before any PR: `shellcheck scripts/*.sh`, `python3 -m py_compile scripts/*.py`, `python3 scripts/validate-handshakes.py` must all pass. |
| Skill library / distribution to downstream projects | `global_skills/`, `.claude/skills/`, `vault/` | This repo is a **distributor**, not just an app: a change here propagates to every project that later runs `os-init` / `os-upgrade-project` / `os-add-skill`. Treat the blast radius as repository-wide, not file-local. |
| Claude Code slash commands | `.claude/commands/*.md` | Five commands shipped today: `/worktree-init`, `/handshake`, `/qa-gate`, `/commit`, `/grill-me`. |
| om-* agent pipeline (PR review, issue triage, spec writing) | `.ai/agentic.config.json`, `.ai/trackers/github.md`, `.ai/browsers/agent-browser.md`, `SDLC.md` | `tracker=github`, `browser=agent-browser`, `qaGate=true`, full label taxonomy. This config block lives additively alongside the repo's own `project`/`pipeline`/`swarm`/`context`/`evaluator` keys in the same JSON file — the two schemas coexist by convention, not by a shared spec. |
| Tests | `execution/test_bootstrap.sh`, `scripts/validate-handshakes.py` | The bootstrap end-to-end test creates throwaway **public** GitHub repos as a side effect. If a run aborts mid-test, clean up manually — the default `gh` token has no `delete_repo` scope. |

## Validation commands

From `.ai/agentic.config.json` → `validation.commands`, run in order:

1. `shellcheck scripts/*.sh`
2. `python3 -m py_compile scripts/*.py`
3. `python3 scripts/validate-handshakes.py`
4. `bash execution/test_bootstrap.sh`

## Pointers

- Process: `SDLC.md`
- Review rules: `CODE_REVIEW.md`
- Protected surfaces: `BACKWARD_COMPATIBILITY.md`
- Pipeline config: `.ai/agentic.config.json`
