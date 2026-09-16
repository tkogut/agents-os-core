# Code review rules

Derived from this repository's actual stack and observed conventions. Applied
automatically by `om-code-review` (and therefore `om-auto-review-pr`) alongside
any `reviewChecklist` set in `.ai/agentic.config.json`.

## Stack

Primarily Bash (installer/bootstrap scripts, hooks) and Python (handshake and
validation tooling), with Markdown as a first-class artifact (skills, specs,
process docs). There is no compiled build step and no package manager lockfile
at the repo root — the validation gate is shell/lint-based, not a build.

## Review priorities

1. **Correctness of the swarm protocol.** A change to `.agents/hooks.json`,
   `.claude/settings.json`, `scripts/generate-handshake.py`, or
   `scripts/validate-handshakes.py` affects every machine in the swarm, not
   just the one it was written on. Verify the change against the *actual*
   CLI/event contract (e.g. `--help` output, Claude Code's real hook event
   names), not against what a doc string claims — this repo has shipped at
   least one drifted example (`CLAUDE.md`'s handshake command block) that did
   not match the script it documented.
2. **`merge=union` scope.** Any `.gitattributes` change touching `MEMORY.md`
   or `task.md`-shaped files must distinguish append-only logs (safe for
   `merge=union`) from checklist/state files with `- [ ]`/`- [x]` items
   (unsafe — union duplicates lines instead of resolving the conflict).
3. **Security (`R-SEC-01`).** No `.env` content, API keys, tokens, or raw
   credentials in code, comments, commit messages, or generated docs. A hook
   or skill that reads `tool_input` on every `Write`/`Edit`/`Bash` call is a
   potential exfiltration path — flag it explicitly when reviewing a new
   hook, even if this repo's own current hooks don't do this today.
4. **Blast radius of installer/skill changes.** `os-init`, `os-init-claude`,
   `os-upgrade-project`, `os-add-skill`, `INSTALL.sh`, and anything under
   `global_skills/` ship to downstream projects. Treat these as a public
   surface (see `BACKWARD_COMPATIBILITY.md`) even though the repo has no
   package registry — the distribution channel is `os-add-skill` fetching
   from this repo's own GitHub API, unauthenticated, by default without ref
   pinning or checksum verification unless that has been explicitly added.
5. **Atomic commits, Conventional Commits, worktree discipline.** Per
   `CLAUDE.md`: one commit per unit of work, ≤50-char subject, never a direct
   commit to `master`/`main`. A PR whose commits mix unrelated changes or
   whose branch was built directly on `master` should be flagged, not waved
   through.

## Repo-specific checks

- Shell scripts pass `shellcheck` with no new warnings introduced by the diff.
- Python scripts touched by the diff pass `python3 -m py_compile`.
- Any change to `scripts/generate-handshake.py` or its callers keeps
  `scripts/validate-handshakes.py` passing, and keeps `CLAUDE.md` §3's
  documented command block in sync with the script's actual `argparse`
  signature.
- A change to `.gitattributes`, `.agents/hooks.json`, or `.claude/settings.json`
  is exercised (manually or via `execution/test_bootstrap.sh`) rather than
  reviewed as inert config — these files have no compiler to catch a typo.
- A change under `global_skills/` or `.claude/skills/` that is meant to reach
  downstream projects is checked against how `os-add-skill` actually fetches
  it (ref pinning, checksum, or lack thereof).

## Severity guidance

- **Blocker** — breaks the swarm protocol (hooks stop firing, handshake
  validation fails, sync produces divergent/duplicated state), or introduces
  a credential/secret leak.
- **Major** — silently wrong behavior in installer/bootstrap scripts, drift
  between a documented command and the real CLI, or a `.gitattributes`/hook
  change with no exercised test.
- **Minor** — style, missing comment, non-blocking doc drift elsewhere.

Every finding cites the concrete failure mode (what breaks, for whom, under
what trigger), not just "this looks off."
