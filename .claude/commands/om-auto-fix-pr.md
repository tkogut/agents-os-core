---
description: Drive an open PR to merge-ready from its number — merges the latest base, then loops review-autofix (om-auto-review-pr), built-in CI stabilization, and UI verification (om-auto-qa-pr) until approvable, green, and QA-evidenced. A --ci-only mode drives just CI green on a PR or a plain branch. Files follow-up issues for nits, normalizes labels, hands off to om-approve-merge-pr — never merges itself. Use for \"get PR 123 merge-ready\".
---

Przeczytaj instrukcje ze skilla `om-auto-fix-pr` z pliku `.claude/skills/om-auto-fix-pr/SKILL.md` (lub `.agents/skills/om-auto-fix-pr/SKILL.md`) i wykonaj zadanie zgodnie z jego procedurą.
Trigger context: @om-auto-fix-pr

Dodatkowe argumenty/kontekst od użytkownika:
$ARGUMENTS
