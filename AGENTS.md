# 🤖 AGENTS.md — System Instructions & Task Routing

> **Instrukcja dla Agentów:** Przeczytaj ten plik przed rozpoczęciem wykonywania jakiegokolwiek zadania. Zawiera on tabele routingu intencji, podział ról w Swarm Triad oraz żelazne zasady wytwarzania oprogramowania w projekcie.

## Overview

AGENTS-OS is a coordination and containerization framework for AI agent swarms (Antigravity IDE, Claude Code, Cursor, Zed). It provides architectural rigor via the async **Swarm Triad** model (Coordinator / Builder / Auditor), conflict-free distributed state sync across machines (Laptop WSL, VPS, Desktop) through `.agents/MEMORY.md` and `.agents/task.md`, and dynamic skill-library distribution to downstream projects via `os-init`, `os-upgrade-project`, and `os-add-skill`. This repo is itself the framework's source — changes here propagate outward to every project that bootstraps from it.

---

## 👥 Podział Ról w Architekturze Swarm Triad

1. **Coordinator (Gemini / Antigravity):** Planowanie, routing zadań, analiza backlogu `task.md` oraz zrzut stanu pamięci (`.agents/MEMORY.md`, `.agents/task.md`). NIE edytuje kodu aplikacyjnego/produkcyjnego poza `tmp/worktrees/`.
2. **Builder (Claude Code / Cursor):** Implementacja kodu, tworzenie testów, lokalne walidacje, atomowe commity w izolowanym środowisku worktree (`tmp/worktrees/`).
3. **Auditor (Gemini):** Linting, audyt bezpieczeństwa, weryfikacja logów, sprawdzanie kontraktów matematycznych/handshake oraz akceptacja PR przed scaleniem.

---

## 🧭 Tabela Routingu Zadań Open Mercato (Task Routing Table)

| Intencja / Cel Użytkownika | Wywoływany Skill (Entrypoint) | Zintegrowany ⛓️ Łańcuch Automatyczny | Rezultat (Artifact) |
| :--- | :--- | :--- | :--- |
| **Brak kodu / Dyskusja / Architektura** | `/om-brainstorm` | Analiza repo → Debata z challengerem → Rozstrzygnięcie | Brief zadaniowy / Decyzja architektoniczna |
| **Tworzenie Specyfikacji & Mockupów UI** | `/om-auto-write-spec` | `om-spec-writing` → `om-open-pr` → `om-prepare-test-env` | PR ze specyfikacją i zrzutami ekranu |
| **Szybkie / Zwykłe Zadanie (Task Brief)** | `/om-auto-create-pr` | Worktree → Build → Validation Gate → Auto-Review Loop | Zautomatyzowany, gotowy PR |
| **Długie / Złożone Zadanie (Wielokrokowe)** | `/om-auto-create-pr-loop` | Folder `.ai/runs/` → Commit co krok → Checkpoint co ~5 kroków | Odporny na `/clear` PR z historią |
| **Obsługa Zgłoszenia z Issue (Bug/Feature)** | `/om-auto-fix-issue` | • **Bug**: Triage → Root-Cause → Fix → PR<br />• **Feature**: Write Spec → Implement Spec | Gotowy PR ze zweryfikowaną poprawką lub funkcją |
| **Wdrożenie Gotowej Specyfikacji** | `/om-auto-implement-spec` | Read Spec → `om-auto-create-pr` → Review Loop → QA | Zweryfikowany PR z dowodami ze zrzutów UI |
| **Weryfikacja Interfejsu PWA/UI w Przeglądarce** | `/om-auto-qa-pr` | Boot App → Playwright/Agent-Browser → Screenshot QA | Raport Pass/Fail ze zrzutami na PR |
| **Prowadzenie & Dociąganie PR do Merge'a** | `/om-pr-autopilot` | Diagnoza stanu PR → Fix CI → Re-review → Base Merge | PR gotowy do zmerge'owania (Merge-Ready) |
| **Wydanie & Aktualizacja Changeloga** | `/om-auto-update-changelog` | Agregacja PR-ów → Dedykowany PR z plikiem CHANGELOG.md | Dokumentacja wydania z przypisaniem autorów |

---

## 🛡️ Żelazne Zasady Projektu (Core Governance Rules)

1. **Izolacja prac w Worktree (Worktree Mandate)**: Wszystkie zadania programistyczne wykonywane przez skille z prefiksem `om-auto-*` oraz rolę Builder MUSZĄ odbywać się w odizolowanych katalogach `tmp/worktrees/`. Nigdy nie commituj bezpośrednio do `master`/`main`.
2. **Bramka Walidacyjna (Validation Gate)**: Żaden PR nie może zostać otwarty ani zmergowany bez przejścia komend sprawdzających skonfigurowanych w `.ai/agentic.config.json` (`shellcheck scripts/*.sh`, `python3 -m py_compile scripts/*.py os-add-skill`, `python3 scripts/validate-handshakes.py`).
3. **Bramka Jakości QA (QA Gate Guard)**: Etykieta `needs-qa` wymaga do scalenia obecności etykiety `qa-approved` z podpisem człowieka lub weryfikacji ze skilla `/om-auto-qa-pr --self-qa-signoff`.
4. **Human-in-the-Loop Mandate (`/plan`, `/grill-me`)**: Automatyczne zatwierdzanie polityk stop hooks ("Always Proceed") jest ZABRONIONE. Wymagana jest bezpośrednia autoryzacja człowieka przez interaktywny modal lub czat przed wykonaniem planu.
5. **Dyscyplina dystrybutora (Blast Radius)**: To repozytorium jest **dystrybutorem** (`os-init`, `os-upgrade-project`, `os-add-skill`, `vault/`). Zmiany tutaj propagują się do wszystkich projektów potomnych. Traktuj wpływ zmian jako ogólnosystemowy.

---

## 🧭 Specyficzne Zasady Rdzenia Frameworka (Core Subsystems Routing)

| Gdy zadanie dotyczy… | Przeczytaj najpierw | Kluczowe reguły |
|---|---|---|
| Swarm role definitions, SDLC flow, commit discipline | `CLAUDE.md`, `SDLC.md` | Worktree-only implementation — never commit directly to `master`/`main`; atomic commits, Conventional Commits, ≤50-char subject |
| Swarm role isolation & PreToolUse gates | `scripts/guard_coordinator_pretool.py`, `.agents/hooks/claude-pre-tool-guard.sh`, `scripts/check_coordinator_role.sh` | Coordinator NEVER writes production code outside `tmp/worktrees/`; PreToolUse gate physically blocks `write_to_file` and `replace_file_content` in root; `/plan` mandates Builder subagent delegation. |
| Architectural planning & interview (`/plan`, `/grill-me`) | `SDLC.md`, `global_skills/grill-me/SKILL.md` | **Human-in-the-Loop Mandate**: Automated review policies ("Always Proceed" / stop hook auto-approval) MUST BE REJECTED. Explicit human confirmation (via `ask_question` modal or chat input) is required before executing. |
| Cross-machine state sync (`MEMORY.md` / `task.md`) | `.agents/MEMORY.md`, `.agents/task.md`, `.gitattributes` | `merge=union` belongs only on append-only files (`MEMORY.md`). Checklist files (`task.md`, `- [ ]`/`- [x]`) must NOT carry `merge=union` — it duplicates lines instead of resolving the conflict. |
| Lifecycle hooks (session start/end, stop, pre-compact) | `.claude/settings.json`, `.agents/hooks.json` | `.claude/settings.json` is what Claude Code actually reads. `.agents/hooks.json` is the Antigravity/Coordinator-side format. The two are not interchangeable and must be kept in sync by hand when hook logic changes. |
| Handshake protocol / swarm coordination artifacts | `scripts/generate-handshake.py`, `scripts/validate-handshakes.py`, `.agents/swarm/` | Real CLI signature: `--role {builder,auditor,coordinator} --conversation-id <uuid> --status {SUCCESS,FAILURE,PARTIAL} [--files] [--notes]`. `--task`/`--branch`/`--status complete` do not exist on this script — verify with `--help` before scripting a call. |
| Installer / bootstrap scripts (`os-init`, `os-init-claude`, `os-upgrade-project`, `os-add-skill`, `INSTALL.sh`) | `scripts/*`, `os-*`, `execution/test_bootstrap.sh` | Builder role must not open these for functional edits without Coordinator approval (`CLAUDE.md` §2.5). QA gate before any PR: `shellcheck scripts/*.sh`, `python3 -m py_compile scripts/*.py os-add-skill`, `python3 scripts/validate-handshakes.py` must all pass. |
| Skill library / distribution to downstream projects | `global_skills/`, `.claude/skills/`, `vault/`, `docs/SKILLS_ARCHITECTURE.md` | This repo is a **distributor**, not just an app: a change here propagates to every project that later runs `os-init` / `os-upgrade-project` / `os-add-skill`. Treat the blast radius as repository-wide, not file-local. |
| Claude Code slash commands | `.claude/commands/*.md` | Five core commands shipped today: `/worktree-init`, `/handshake`, `/qa-gate`, `/commit`, `/grill-me`. |
| om-* agent pipeline (PR review, issue triage, spec writing) | `.ai/agentic.config.json`, `.ai/trackers/github.md`, `.ai/browsers/agent-browser.md`, `SDLC.md` | `tracker=github`, `browser=agent-browser`, `qaGate=true`, full label taxonomy. This config block lives additively alongside the repo's own `project`/`pipeline`/`swarm`/`context`/`evaluator` keys in the same JSON file — the two schemas coexist by convention, not by a shared spec. |
| Tests | `execution/test_bootstrap.sh`, `scripts/validate-handshakes.py` | The bootstrap end-to-end test creates throwaway **public** GitHub repos as a side effect. If a run aborts mid-test, clean up manually — the default `gh` token has no `delete_repo` scope. |

---

## 🧪 Komendy Walidacji (Validation Commands)

Zgodnie z `.ai/agentic.config.json` → `validation.commands`, uruchamiaj w kolejności:

1. `shellcheck scripts/*.sh`
2. `python3 -m py_compile scripts/*.py os-add-skill`
3. `python3 scripts/validate-handshakes.py`
4. `bash execution/test_bootstrap.sh`

---

## 🔗 Wskaźniki (Pointers)

- Cykl procesu: [`SDLC.md`](SDLC.md)
- Reguły code review: [`CODE_REVIEW.md`](CODE_REVIEW.md)
- Kompatybilność wsteczna: [`BACKWARD_COMPATIBILITY.md`](BACKWARD_COMPATIBILITY.md)
- Architektura skilli (Model Dwuwarstwowy): [`docs/SKILLS_ARCHITECTURE.md`](docs/SKILLS_ARCHITECTURE.md)
- Konfiguracja pipeline'u: [`.ai/agentic.config.json`](.ai/agentic.config.json)
