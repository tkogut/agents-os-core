---
description: Review or re-review a PR by number in an isolated worktree. Runs the `om-code-review` skill — or, for spec-only design PRs, a specification review — submits approve/request-changes, manages pipeline labels. On changes-requested, the autofix loop (fix/test/validate/re-review until merge-ready) runs on the automation's own PRs or with --autofix; other authors' PRs get review + handoff only. Usage - /om-auto-review-pr <PR-number> [--autofix]
---

Przeczytaj instrukcje ze skilla `om-auto-review-pr` z pliku `.claude/skills/om-auto-review-pr/SKILL.md` (lub `.agents/skills/om-auto-review-pr/SKILL.md`) i wykonaj zadanie zgodnie z jego procedurą.
Trigger context: @om-auto-review-pr

Dodatkowe argumenty/kontekst od użytkownika:
$ARGUMENTS
