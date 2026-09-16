# Backward compatibility

What this project considers a protected contract surface, inventoried from the
repository's actual public surfaces (there is no published package/API — the
"public" here is *downstream projects that bootstrap from or update against
this repo*). Review skills check changes against this file; implementation
skills warn when a change violates it.

## CLI entry points

| Surface | What it does | Breaking change means | Required path |
|---|---|---|---|
| `os-init <project-name>` | Creates a new AGENTS-OS project (Antigravity IDE flavor): GitHub repo, commit+push, opens IDE. | Removing/renaming the positional arg, changing default target directory behavior, or changing what gets committed/pushed without opt-in. | Deprecation note in `README.md` + `CHANGELOG.md`; keep the old invocation working for at least one minor version with a warning. |
| `os-init-claude <project-name>` | Same as `os-init` but templates from `vault/CLAUDE.md` + `vault/.claude/commands/`, opens VS Code, sets `claude-code` role in `agents.yaml`. | Changing the vault template source path, or diverging the generated project layout from what `os-upgrade-project` expects to find later. | Same as `os-init`; also update `os-upgrade-project`'s detection logic in lockstep. |
| `os-upgrade-project [path]` | Migrates an existing project to the current Swarm standard: `.gitattributes` union-merge rules, lifecycle hooks, local git config (`pull.rebase`, `merge.conflictstyle`), `.claude/skills/om-*` symlinks, `MEMORY.md`/`task.md` init, skill sync from `vault/`. | Any change to *what* it writes into an existing project (`.gitattributes` rules, hook file locations/format, symlink targets) without a migration path for projects already upgraded once. | Idempotent by construction — re-running must never duplicate or corrupt state it already wrote. New/changed rules need an explicit migration step for previously-upgraded projects, not just for fresh ones. |
| `os-add-skill <skill-name>` | Fetches a skill from this repo's `global_skills/` (or a configured secondary source) via the GitHub Contents API and installs it locally. | Changing the source repos, the install target path, or the fetch mechanism (auth requirement, ref resolution, verification behavior) in a way that changes what a previously-working invocation does. | Version the fetch behavior explicitly; if pinning/checksum verification is added, keep the unpinned path working (warn, don't break) unless a strict/fail-closed flag is explicitly requested. |
| `INSTALL.sh` | One-time host setup (installs `gh` CLI, etc.). | Changing package sources/signing keys silently, or requiring a new prerequisite without detecting and reporting its absence. | Detect-and-report before installing; never fail with a bare non-zero exit and no explanation. |

## Cross-machine state format

| Surface | What it does | Breaking change means | Required path |
|---|---|---|---|
| `.agents/MEMORY.md` schema (`schema: agents-os-memory-v1` front matter) | Shared swarm memory, git-synced via `merge=union`. | Changing the front-matter schema key, section headings another tool parses, or the union-merge assumption (append-only) without updating every writer. | Bump the `schema:` value; keep old-schema files readable during a transition window. |
| `.agents/task.md` | Per-branch task backlog with checkbox state. | Changing the checkbox syntax (`- [ ]`/`- [x]`) or adding `merge=union` back onto this file (known-bad — duplicates lines on conflict). | Any `.gitattributes` change here requires the checklist-vs-append-only distinction documented in `CODE_REVIEW.md` to be re-verified, not assumed. |
| `.agents/hooks.json` | Antigravity/Coordinator-side lifecycle hook definitions (`SessionStart`, `SessionEnd`, `PreInvocation`, `Stop`). | Renaming event keys, or changing fail-open (`\|\| true`, `2>/dev/null`) semantics that the auto-sync hooks rely on to never block a session. | Keep event names stable; if a new fail-closed mode is added, make it opt-in. |
| `.claude/settings.json` | Claude Code's actual hook wiring (separate format/file from `.agents/hooks.json`). | Removing a hook event Claude Code fires on, or changing matcher scope in a way that silently stops re-grounding/sync from firing. | Verify against Claude Code's real hook event list before renaming or removing an entry — this file has no compiler to catch a typo. |
| `.agents/swarm/*_handshake.json` | Builder/Auditor/Coordinator handshake artifacts, produced by `scripts/generate-handshake.py`, checked by `scripts/validate-handshakes.py`. | Changing the JSON shape `validate-handshakes.py` expects without updating both the generator and the validator together, or changing `generate-handshake.py`'s CLI flags without updating every doc that shows an example invocation (`CLAUDE.md` §3 has drifted from the real signature before). | Generator and validator change together, in the same commit; grep the repo for documented example invocations and update them in the same PR. |

## Pipeline config

| Surface | What it does | Breaking change means | Required path |
|---|---|---|---|
| `.ai/agentic.config.json` | Dual-purpose: the repo's own `project`/`pipeline`/`swarm`/`context`/`evaluator` block (AGENTS-OS v6.5 native) **and** the om-* skill collection's `tracker`/`browser`/`validation`/`labels`/`qaGate`/`paths` block, coexisting in one file by convention. | Removing or reshaping either block without checking who reads it — the two schemas are not unified by a shared spec, only by sharing a file path. The top-level `version` key belongs to the native block (`"6.5-swarm"`); no om-* skill logic currently reads `config.version` at runtime (verified against the shipped skill sources), so it does not collide functionally, but a future om-* skill that starts reading `version` would. | Grep both this repo's own tooling and the installed `om-*` skill sources for the key before changing or removing it. |

## Skill distribution layout

| Surface | What it does | Breaking change means | Required path |
|---|---|---|---|
| `global_skills/<name>/` | Canonical skill source, fetched by `os-add-skill` and synced by `os-upgrade-project`. | Renaming a skill directory, or changing its internal file layout in a way `os-add-skill`'s fetch logic doesn't expect. | Keep the old directory name as an alias or update `os-add-skill`'s fetch logic in the same change. |
| `.claude/skills/<name>` | Symlinks into `.agents/skills/` (itself gitignored, populated at install time — not committed). | Changing the symlink target convention breaks every project that ran `os-upgrade-project` under the old convention. | `os-upgrade-project` must detect and migrate the old convention, not just write the new one for fresh installs. |
