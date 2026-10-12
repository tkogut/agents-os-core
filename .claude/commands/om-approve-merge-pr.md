---
description: Approve (submit an approving review) and squash-merge a PR given only its number, refusing when the QA gate or a blocking label forbids it. Routes fixable blockers to om-auto-fix-pr (red CI via its --ci-only mode, or conflicts and review problems via the full loop). Optionally file a follow-up issue at the same time. Use when the user says \"approve and merge PR 123\", \"ship PR 123\", or gives a PR number with intent to merge.
---

Przeczytaj instrukcje ze skilla `om-approve-merge-pr` z pliku `.claude/skills/om-approve-merge-pr/SKILL.md` (lub `.agents/skills/om-approve-merge-pr/SKILL.md`) i wykonaj zadanie zgodnie z jego procedurą.
Trigger context: @om-approve-merge-pr

Dodatkowe argumenty/kontekst od użytkownika:
$ARGUMENTS
