---
description: Read-only triage gate for an autofix chain. Decides whether a tracker issue is a real, still-unfixed defect on the current branch. Stops the chain cleanly with NO_ACTION_NEEDED when the issue is already fixed, already in progress by someone else, already covered by an open PR, or not actually a bug.
---

Przeczytaj instrukcje ze skilla `om-verify-in-repo` z pliku `.claude/skills/om-verify-in-repo/SKILL.md` (lub `.agents/skills/om-verify-in-repo/SKILL.md`) i wykonaj zadanie zgodnie z jego procedurą.
Trigger context: @om-verify-in-repo

Dodatkowe argumenty/kontekst od użytkownika:
$ARGUMENTS
