---
description: One-time pipeline configurator. Inspects the repo (default branch, validation scripts, labels), asks a few questions, writes .ai/agentic.config.json — the file every other skill reads — installs the tracker descriptor, and generates missing project docs (SDLC.md, CODE_REVIEW.md, BACKWARD_COMPATIBILITY.md, AGENTS.md starter). Re-run when the toolchain or label taxonomy changes. Verifies cross-skill coverage and prints the install command for missing skills.
---

Przeczytaj instrukcje ze skilla `om-setup-agent-pipeline` z pliku `.claude/skills/om-setup-agent-pipeline/SKILL.md` (lub `.agents/skills/om-setup-agent-pipeline/SKILL.md`) i wykonaj zadanie zgodnie z jego procedurą.
Trigger context: @om-setup-agent-pipeline

Dodatkowe argumenty/kontekst od użytkownika:
$ARGUMENTS
