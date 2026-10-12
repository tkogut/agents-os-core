---
description: > Decision guide for delegating to caveman-style subagents. Tells the main thread WHEN to spawn `cavecrew-investigator` (locate code), `cavecrew-builder` (1-2 file edit), or `cavecrew-reviewer` (diff review) instead of doing the work inline or using vanilla `Explore`. Subagent output is caveman-compressed so the tool-result injected back into main context is ~60% smaller — main context lasts longer across long sessions. Trigger: \"delegate to subagent\", \"use cavecrew\", \"spawn investigator/builder/reviewer\", save context\", \"compressed agent output\".
---

Przeczytaj instrukcje ze skilla `cavecrew` z pliku `.claude/skills/cavecrew/SKILL.md` (lub `.agents/skills/cavecrew/SKILL.md`) i wykonaj zadanie zgodnie z jego procedurą.
Trigger context: @cavecrew

Dodatkowe argumenty/kontekst od użytkownika:
$ARGUMENTS
