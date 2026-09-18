# 🤖 AGENTS.md — System Instructions & Task Routing

> **Instrukcja dla Agentów:** Przeczytaj ten plik przed rozpoczęciem wykonywania jakiegokolwiek zadania w projekcie. Zawiera on podział ról w architekturze Swarm Triad, tabelę routingu zadań Open Mercato oraz żelazne zasady wytwarzania oprogramowania.

## Overview

Ten projekt jest zarządzany w standardzie **AGENTS-OS v6.5 Swarm Edition**. Zapewnia to architektoniczny rygor za pośrednictwem asynchronicznego modelu **Swarm Triad** (Coordinator / Builder / Auditor), bezkonfliktową synchronizację stanu pamięci między maszynami (`.agents/MEMORY.md`, `.agents/task.md`) oraz dynamiczną bibliotekę skilli (Model Dwuwarstwowy).

---

## 👥 Podział Ról w Architekturze Swarm Triad

1. **Coordinator (Gemini 3.8 Flash Medium / Antigravity):** Planowanie, routing zadań, analiza backlogu `task.md` oraz zrzut stanu pamięci (`.agents/MEMORY.md`, `.agents/task.md`). NIE edytuje kodu aplikacyjnego/produkcyjnego poza `tmp/worktrees/`.
2. **Builder (Gemini 3.1 Pro / Antigravity / Cursor / Claude Code):** Implementacja kodu, tworzenie testów, lokalne walidacje, atomowe commity w izolowanym środowisku worktree (`tmp/worktrees/`).
3. **Auditor (Gemini 3.8 Flash Medium):** Linting, audyt bezpieczeństwa, weryfikacja logów, sprawdzanie kontraktów matematycznych/handshake oraz akceptacja PR przed scaleniem.

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
2. **Bramka Walidacyjna (Validation Gate)**: Żaden PR nie może zostać otwarty ani zmergowany bez przejścia komend sprawdzających skonfigurowanych w `.ai/agentic.config.json`.
3. **Bramka Jakości QA (QA Gate Guard)**: Etykieta `needs-qa` wymaga do scalenia obecności etykiety `qa-approved` z podpisem człowieka lub weryfikacji ze skilla `/om-auto-qa-pr --self-qa-signoff`.
4. **Human-in-the-Loop Mandate (`/plan`, `/grill-me`)**: Automatyczne zatwierdzanie polityk stop hooks ("Always Proceed") jest ZABRONIONE. Wymagana jest bezpośrednia autoryzacja człowieka przez interaktywny modal lub czat przed wykonaniem planu.
5. **Model Dwuwarstwowy Skilli (On-Demand Discovery)**: Projekt posiada preinstalowane skille bazowe Tier 1. Gdy napotkasz specjalistyczne zadanie dziedzinowe (np. WCAG, GDScript, Odoo, Active Directory), przeszukaj pasywny katalog `.agents/specs/awesome-skills-catalog.md` (`grep -i "<fraza>" .agents/specs/awesome-skills-catalog.md`) i zainstaluj brakujący skill poleceniem `os-add-skill <skill>`, zanim zgłosisz brak możliwości realizacji.

---

## 🧭 Subsystemy & Zasady Operacyjne

| Gdy zadanie dotyczy… | Przeczytaj najpierw | Kluczowe reguły |
|---|---|---|
| Role Swarm, SDLC, dyscyplina commitów | `CLAUDE.md`, `SDLC.md` | Implementacja wyłącznie w worktree; commity atomowe, Conventional Commits, tytuł ≤50 znaków. |
| Izolacja ról Swarm i bramki PreToolUse | `scripts/guard_coordinator_pretool.py`, `.agents/hooks/claude-pre-tool-guard.sh` | Coordinator NIE modyfikuje kodu poza `tmp/worktrees/`; PreToolUse blokuje bezpośredni zapis na main/master. |
| Planowanie architektoniczne (`/plan`, `/grill-me`) | `SDLC.md`, `.claude/commands/grill-me.md` | **Human-in-the-Loop**: Zakaz automatycznego akceptowania planu bez potwierdzenia człowieka. |
| Synchronizacja pamięci między maszynami | `.agents/MEMORY.md`, `.agents/task.md`, `.gitattributes` | `merge=union` dotyczy wyłącznie `MEMORY.md`. Plik `task.md` NIE może mieć `merge=union`. |
| Cykl życia sesji i hooki | `.claude/settings.json`, `.agents/hooks.json` | Automatyczny pull rebase na SessionStart i zrzut stanu pamięci na SessionEnd (z blokadą puszy na main/master). |
| Handshake protocol | `scripts/generate-handshake.py`, `scripts/validate-handshakes.py`, `.agents/swarm/` | Po implementacji wygeneruj handshake Builder (`--role builder --conversation-id <uuid> --status SUCCESS`). |
| Architektura skilli | `.agents/specs/awesome-skills-catalog.md` | Tier 1 w `.agents/skills/`, Tier 2 w rejestrze pasywnym; instalacja Just-In-Time przez `os-add-skill`. |

---

## 🧪 Komendy Walidacji (Validation Commands)

Zgodnie z `.ai/agentic.config.json` → `validation.commands`, uruchamiaj testy projektu przed otwarciem każdego PR.
