---
description: Fix or implement a tracker issue end to end from a single command — takes an issue id or a plain problem description (filed first via om-prepare-issue), classifies, then drives the bug autofix chain (om-verify-in-repo, om-root-cause, om-fix, om-open-pr, om-auto-review-pr, om-auto-qa-pr for UI fixes) or the feature route (spec via om-auto-write-spec, built via om-auto-implement-spec). Isolated worktree, claim protocol, clean stops. Use for \"fix issue 123\" or a pasted problem description.
---

Przeczytaj instrukcje ze skilla `om-auto-fix-issue` z pliku `.claude/skills/om-auto-fix-issue/SKILL.md` (lub `.agents/skills/om-auto-fix-issue/SKILL.md`) i wykonaj zadanie zgodnie z jego procedurą.
Trigger context: @om-auto-fix-issue

Dodatkowe argumenty/kontekst od użytkownika:
$ARGUMENTS
