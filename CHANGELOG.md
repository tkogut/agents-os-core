# 🛸 Historia Zmian / Changelog — AGENTS-OS v6.5 (Enterprise Swarm Edition)

## 🛸 Historia Zmian / Changelog — AGENTS-OS v6.5 (Enterprise Swarm Edition)
Dokumentującą:
- Pełną refaktoryzację rdzenia i przejście na model asynchronicznych agentów (Swarm Triad).
- Usunięcie martwego kodu (dead code) i przestarzałych skryptów.
- Pełną integrację z bazą 1400+ skilli z repozytorium sickn33.
- Integrację 36 skilli Open-Mercato SDLC oraz architektury Cezar Runtime.

## [6.5.0] - 2026-08-07

### 🏗️ Enterprise Architecture: Open-Mercato Integration & Cezar Runtime
- **36 skilli Open-Mercato SDLC**: Pełna integracja pipeline'u deweloperskiego (`om-auto-*`, `om-setup-agent-pipeline`, `om-code-review`, `om-ux-*`) do `global_skills/` i `vault/.agents/skills/`.
- **`.ai/agentic.config.json`**: Nowy centralny plik konfiguracyjny definiujący gate commands (lint, typecheck, test, build), role Swarm Triad, heartbeat, evaluator i context routing.
- **`SDLC.md`**: Source of Truth dla 6-fazowego cyklu życia kodu (Issue → Branch → Worktree → Implementation → Handshake → QA Gate → PR Merge).
- **`vault/HANDOFF.md`**: Template Cezar Runtime dla fault-tolerance i wznowienia sesji agentów.
- **Task Router** (`.agents/agents.md`): Lean entry-point router z budget kontekstowym (max 3 moduły domenowe).
- **Domain Modules**: `agents-pipeline.md` (SDLC workflow), `agents-qa.md` (QA gate policy), `agents-ux.md` (Visual Proof-of-Work).
- **Evaluator Module**: `.agents/eval/evaluator.md` + test case `tc-001` dla walidacji down-scalingu promptów.
- **Pre-commit hook** (`vault/.git-hooks/pre-commit`): Swarm Triad role enforcement z blokowaniem commita dla niedozwolonych ról.
- **Specyfikacja architektoniczna**: `vault/.agents/specs/integracja archotectury open-mercato.md` — pełna dokumentacja Enterprise Swarm.

### 🧹 Pre-Push Cleanup
- Usunięto stale artifacts: `task.md`, `design-tokens.md`, `implementation_plan.md`, `walkthrough.md`.
- Usunięto `rendered_page.html` (108KB build artifact) z tracked files.
- Zaktualizowano `.gitignore` — 50+ wzorców (pyc, pem, IDE, coverage, session artifacts).
- Wyrównano wersje: `agents.yaml`, `INSTALL.sh`, `README.md`, `CHANGELOG.md` → `v6.5-swarm`.
- Usunięto stale worktree `feature/core-init-zed`.

---

## [6.2.0] - 2026-08-06

### 🚀 Quality Infrastructure: test-creator Skill (v2.2)
- **Nowy globalny skill `test-creator`**: Dodano skill do `global_skills/test-creator/` w celu ujednolicenia standardu testów jednostkowych (Vitest), integracyjnych API (Pytest) oraz end-to-end (Playwright).
- **Szablony referencyjne**: Wdrożono wzorcowe konfiguracje `references/vitest_template.js`, `references/pytest_template.py` i `references/playwright_template.js` umożliwiające natychmiastowe generowanie pokrycia testowego w nowych projektach.

---

## [6.1.0] - 2026-07-21

### 🛡️ Hardening: Coordinator Safety Gate (R-ROLE-01)

- **Rule 6** dodana do `core-rule.md`: kategoryczny zakaz edycji kodu `/src` przez Coordinator bez delegacji.
- **`scripts/validate-handshakes.py`**: Safety Gate wykrywa self-signed Builder handshake (exit 2 `DIRECT_COORDINATOR_EDIT_FORBIDDEN`).
- **`scripts/check_coordinator_role.sh`**: Guard blokujący commit zmian w `src/` bez ważnego Builder handshake od subagenta.

---

## [5.0.0] - 2026-06-10

### 🚀 Aktualizacja Systemowa do v5.0 (System-wide Version Increment)
* **Konstytucja i Dokumentacja**: Zaktualizowano Konstytucję AGENTS-OS oraz wszystkie powiązane specyfikacje i raporty do wersji v5.0, zapewniając pełną spójność topologii systemowej w repozytorium.
* **Synchronizacja Vault**: Zsynchronizowano szablony w katalogu Vault (`vault/`), w tym Konstytucję, reguły GOVERNANCE i specyfikację diagramu zależności `graph.json`.

## [4.2.1] - 2026-05-25

### 🚀 Hardening i Zabezpieczenia (Hardening & Security)
* **Ścieżki relatywne w teście E2E**: Zaimplementowano pobieranie ścieżek relatywnych względem lokalizacji pliku skryptu `test_bootstrap.sh`, co umożliwia uruchomienie testów z dowolnego katalogu w systemie.
* **Zabezpieczenie przed Path Traversal w `os-add-skill`**: Dodano walidację nazwy skilla (blokada znaków `..`, `/`, `\`) chroniącą przed zapisem plików poza docelowym folderem projektu.

## [4.2.0] - 2026-05-24

### 🚀 Poprawki i Automatyzacja (Portability & Automation)

* **Dynamiczne dogrywanie skilli (On-Demand & RAG Catalog)**:
  * Wdrożono komendę `os-add-skill` (skrypt python `os-add-skill-run`) umożliwiający pobieranie pojedynczych skilli z repozytorium GitHub za pomocą API.
  * Zaimplementowano katalog `awesome-skills-catalog.md` w szablonie (Vault) umożliwiający asystentom AI dopasowywanie potrzeb programisty przez RAG i sugerowanie wgrania skilli za pomocą `os-add-skill`.
  * Zastąpiono pobieranie całego repozytorium `awesome-skills` lekkim dociąganiem on-demand podczas inicjalizacji.
* **Instalacja wtyczki Caveman przez URL**:
  * Zmieniono cel instalacji wtyczki `caveman` w [INSTALL.sh](file:///home/tkogut/projects/agents-os-core/INSTALL.sh) na bezpośredni link GitHub (`https://github.com/juliusbrussee/caveman`). Rozwiązuje to błąd instalacji lokalnej.
* **Automatyczne czyszczenie starych szablonów**:
  * Dodano moduł czyszczący w [INSTALL.sh](file:///home/tkogut/projects/agents-os-core/INSTALL.sh), usuwający stare wersje szablonów (np. `v4.0-swarm`) przed kopiowaniem nowych.
* **Automatyczny test E2E**:
  * Utworzono skrypt testowy [test_bootstrap.sh](file:///home/tkogut/projects/agents-os-core/execution/test_bootstrap.sh) weryfikujący tworzenie projektów, strukturę Złotego Standardu, repozytorium git, dynamiczne dociąganie skilla `postgresql-optimization` oraz push na GitHub.

---

## [4.1.0] - 2026-05-24

### 🚀 Nowości i Ulepszenia Przenaszalności (Portability)

* **Dynamiczny odczyt nazwy użytkownika GitHub (Fix 3.1)**:
  * Zastąpiono zahardkodowaną nazwę użytkownika `tkogut` w skrypcie [bootstrap.py](file:///home/tkogut/projects/agents-os-core/global_skills/swarm-bootstrapper/scripts/bootstrap.py) oraz [os-init](file:///home/tkogut/projects/agents-os-core/os-init) dynamicznym odpytywaniem przez `gh api user -q .login`.
  * Wdrożono solidny mechanizm fallback do zmiennych konfiguracyjnych git (`git config github.user` / `git config user.name`) w przypadku braku zalogowania w CLI.

* **Dynamiczne mapowanie użytkownika Windows w WSL2 (Fix 3.2)**:
  * Zastąpiono zahardkodowany profil Windows `admin_tk` w ścieżce do IDE w [os-init](file:///home/tkogut/projects/agents-os-core/os-init) dynamicznym wywołaniem systemowym `cmd.exe /c "echo %USERNAME%"`.
  * Dzięki temu edytor Antigravity IDE uruchamia się poprawnie u każdego użytkownika WSL.

* **Instalacja GitHub CLI (gh) przez APT zamiast Snap (Fix 3.3)**:
  * Zmieniono metodę instalacji `gh` w [INSTALL.sh](file:///home/tkogut/projects/agents-os-core/INSTALL.sh) ze `snap` na oficjalne repozytorium APT Debiana/Ubuntu.
  * Rozwiązuje to błąd braku demona `snapd`/`systemd` na domyślnych dystrybucjach WSL2.

* **Izolacja zależności Python w Virtualenv (Fix 3.4)**:
  * Wprowadzono tworzenie dedykowanego środowiska wirtualnego w katalogu `~/.antigravity/venv` podczas instalacji w [INSTALL.sh](file:///home/tkogut/projects/agents-os-core/INSTALL.sh).
  * Przeniesiono instalację bibliotek `GitPython` oraz `PyGithub` do venv, eliminując potrzebę używania ryzykownej flagi `--break-system-packages`.
  * Zaktualizowano [os-init](file:///home/tkogut/projects/agents-os-core/os-init), aby automatycznie używał interpretera z venv przy wywoływaniu bootstrappera.

---

*Zarządzanie wersją i dokumentacją: Antigravity Agent & tkogut.*
