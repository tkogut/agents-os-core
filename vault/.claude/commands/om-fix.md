---
description: Implements the minimal code change identified by the om-root-cause step, adds regression tests, and runs the configured validation gate. Claims the tracker issue at start (assignee + in-progress label + claim comment) so concurrent automation backs off. Does not commit, push, or open a PR — that is the om-open-pr step's job.
---

Przeczytaj instrukcje ze skilla `om-fix` z pliku `.claude/skills/om-fix/SKILL.md` (lub `.agents/skills/om-fix/SKILL.md`) i wykonaj zadanie zgodnie z jego procedurą.
Trigger context: @om-fix

Dodatkowe argumenty/kontekst od użytkownika:
$ARGUMENTS
