# 🛸 Historia Zmian / Changelog — AGENTS-OS v6.5 (Enterprise Swarm Edition)

## 🛸 Historia Zmian / Changelog — AGENTS-OS v6.5 (Enterprise Swarm Edition)
Dokumentującą:
- Pełną refaktoryzację rdzenia i przejście na model asynchronicznych agentów (Swarm Triad).
- Usunięcie martwego kodu (dead code) i przestarzałych skryptów.
- Pełną integrację z bazą 1400+ skilli z repozytorium sickn33.
- Integrację 41 skilli Open-Mercato SDLC & Product Discovery oraz architektury Cezar Runtime.

## [6.5.6] - 2026-09-25

### 🛸 Cezar Orchestrator GitOps & CI/CD Zero-Passphrase Standard
- 🚀 **Repozytorium Cezar Runtime (`tkogut/cezar`)**:
  - Utworzono dedykowane repozytorium GitHub dla środowiska Cezar Cockpit / Runtime w Złotym Standardzie v6.5 (`os-init cezar`).
  - Wyeksportowano i zintegrowano konfigurację ze środowiska VPS (`Dockerfile`, `docker-compose.yml`, `entrypoint.sh` z patchami modeli DeepSeek, `update-password.sh`).
- 🔑 **Standard Bezhasłowego CI/CD Deploy (`vps_ci_deploy_key`)**:
  - Wprowadzono architektoniczną regułę `Zero-Passphrase` w workflowach GitHub Actions (`deploy.yml`).
  - Zastąpiono osobiste klucze z passphrase dedykowanym kluczem deploy `vps_ci_deploy_key` (ed25519) w sekretach `VPS_SSH_KEY`, eliminując zależność od sekretu `VPS_PASSPHRASE`.
  - Zaktualizowano skill `vps-ops` (Krok 0.6) oraz szablony Vault.
- 🌐 **Architektura Sieciowa Cross-Container (Cezar <-> Aplikacje VPS)**:
  - Zdefiniowano standard bezpośredniej komunikacji między kontenerami na tym samym VPS po sieci Dockera (`traefik-proxy` -> `http://<container_name>:<port>`) oraz zarządzania kontenerami przez gniazdo `/var/run/docker.sock` zamiast loopback SSH.

## [6.5.5] - 2026-09-18

### 🚀 Open-Mercato Product Discovery & Validation Layer
- ✨ **Nowe skille produktowe z upstreamu (`open-mercato/skills`)**:
  - `om-discover`: Prowadzenie ustrukturyzowanych rozmów discovery, drzewa szans/rozwiązań oraz generowanie `product-brief.md`.
  - `om-synthetic-users`: Statystyczne panele syntetycznych person testujące flow i decyzje pod presją z uziemieniem dowodowym.
  - `om-mockup-prototype`: Generowanie neutralnych, klikalnych prototypów low-fi z symulacją danych przed wejściem w implementację.
  - `om-backlog`: Dekompozycja zwalidowanego briefu na drzewo epików, user stories i tasków z egzekwowaniem Definition of Ready.
  - `om-setup-discovery-pipeline`: Konfiguracja warstwy produktowej, ról Product Owner/Designer oraz Definition of Ready w `SDLC.md`.
- 🔄 **Pełna synchronizacja 36 istniejących skilli `om-*`**: Zaktualizowano wszystkie skille do najnowszej wersji upstream (m.in. śledzenie `QA head: <sha>`, pre-intake bramki Definition of Ready, kontrakt repo-local `.ai/skills/<name>/SKILL.md`).
- 🛠️ **Rozszerzenie `os-add-skill`**: Dodano `open-mercato/skills` jako bezpośrednie źródło instalacji skilli w CLI oraz zaktualizowano referencję w `docs/API.md`.
- 🔗 **Dystrybucja i dowiązania**: Zsynchronizowano skille we wszystkich lokalizacjach dystrybucyjnych (`global_skills/`, `.agents/skills/`, `vault/.agents/skills/`, `.claude/skills/`, `vault/.claude/skills/`).

### 🧹 Pruning biblioteki skilli & Optymalizacja Tokenowa (/grill-me)
- ✂️ **Usunięcie zbędnych skilli Caveman Cloud**: Wyeliminowano 11 skilli zależnych od zewnętrznej bramki Caveman Cloud lub dublujących narzędzia repozytorium (`caveman-setup`, `caveman-stats`, `caveman-manage`, `caveman-optimize`, `caveman-evidence-review`, `caveman-learn`, `caveman-discover`, `caveman-compress`, `caveman-commit`, `caveman-init`, `caveman-help`), redukując narzut system promptu o >1200 tokenów na każdą turę.
- 💎 **Zachowanie kluczowych lokalnych token-saverów**: Utrzymano dwuwarstwowy model agentów — zachowano `cavecrew` (niskokosztowe subagenty zwracające skompresowane odpowiedzi), `caveman-explore` (szybki lokalizator kodu `path:line`) oraz `caveman-review` (jednolinijkowe audyty).
- 📐 **Format Concise Engineering**: Zastąpiono tryb "jaskiniowca" profesjonalną zwięzłością inżynierską (logic-first Markdown) bez łamanej składni pidgin.
- ⚙️ **Aktualizacja harnessu**: Zaktualizowano `os-upgrade-project`, `docs/API.md` oraz skrypt `scripts/sync-skills.sh` do stanu 63+ skilli.
- 🧼 **Sanityzacja szablonu startowego (Vault)**: Zmodernizowano `vault/.ai/agentic.config.json` do uniwersalnego schematu Swarm v6.5 z dynamicznym placeholderem `{{PROJECT_NAME}}` oraz oczyszczono pliki `HANDOFF.md`, `agents.md` i testy z pozostałości projektu źródłowego (`mms4tk`).

## [6.5.4] - 2026-09-17

### 🛡️ Governance & Swarm Triad Protection (R-ROLE-01 & PreToolUse)
- ✨ **Hybrydowy Strażnik PreToolUse (`scripts/guard_coordinator_pretool.py`)**: Interaktywna bramka `force_ask` dla Antigravity/Gemini i Claude Code — chroni kod produkcyjny przed edycją w głównym drzewie projektu, umożliwiając 1-klikową akceptację dla szybkich hotfixów oraz wymuszając worktree dla dużych zadań. (#11) *(@tkogut)*
- 🔒 **Human-in-the-Loop Mandate (`/plan` & `/grill-me`)**: Wprowadzono Hard Rule #8 w `SDLC.md`, `AGENTS.md` oraz `global_skills/grill-me/SKILL.md` — unieważniono automatyczne systemowe sygnały IDE ("Always Proceed"), wymuszając bezpośrednie manualne potwierdzenie człowieka przed wdrożeniem planu. (#11) *(@tkogut)*
- 🛠️ **Team-wide PR Merge Permissions**: Zezwolono na polecenie `gh pr merge` w `.claude/settings.json`. (#9) *(@tkogut)*
- 🛠️ **Gitignore Claude Code Local Settings**: Dodano ignorowanie `settings.local.json` do `.gitignore`. (#8) *(@tkogut)*

### 🚀 Agentic Pipeline & Swarm Modernization
- ✨ **Konfiguracja pipeline'u `om-*` (`.ai/agentic.config.json`)**: Pełna integracja taksonomii etykiet, bramek QA, deskryptora trackera GitHub oraz providera przeglądarki `agent-browser`. (#6) *(@tkogut)*
- ✨ **Modernizacja Swarmu v6.5**: Wdrożono skill `swarm-onboarding`, wymuszono `core.symlinks true` oraz bezpieczne dowiązania `ln -sfn`. (#10) *(@tkogut)*
- ✨ **Natywne hooki Claude Code w `os-upgrade-project`**: Automatyczne wdrażanie `.claude/settings.json` z obsługą `reground.sh` i `precompact-snapshot.sh` oraz instalacja pre-commit hooków w projektach potomnych. (#7) *(@tkogut)*

### 🐛 Fixes & Supply Chain Hardening
- 🐛 **Korekta reguły `merge=union` w `.gitattributes`**: Usunięto union merge z checklisty `task.md` (pozostawiając wyłącznie na append-only `MEMORY.md`), eliminując ryzyko duplikacji wpisów zadań. (#5) *(@tkogut)*
- 🔒 **Pinning i weryfikacja SHA-256 w `os-add-skill`**: Zabezpieczono łańcuch dostaw skilli poprzez weryfikację sum kontrolnych i pinowanie referencji git. (#5) *(@tkogut)*
- 📝 **Specyfikacja podpisywania commitów**: Opracowano plan wdrożenia kryptograficznego podpisywania commitów w miejsce nieskutecznej lokalnej atestacji SHA-256 (`.agents/specs/commit-signing.md`). (#5) *(@tkogut)*

### 👥 Contributors
- @tkogut

---

## [6.5.3] - 2026-09-09

### 🛡️ Hardening: Lifecycle Hooks Branch Safety & Main/Master Protection
- **Protected Branch Guard in `hooks.json`**: Hooki `SessionEnd` i `Stop` zostały zabezpieczone warunkiem wykrywającym bieżącą gałąź (`CURR`). Automatyczny `git push origin HEAD` wykonuje się wyłącznie na gałęziach funkcyjnych/roboczych (`feature/*`, `fix/*`, `tmp/worktrees/`), kategorycznie blokując bezpośrednie commity i pushe na `main`/`master` (zgodnie z regułą SDLC).
- **Dynamic Branch Pull**: Hooki `SessionStart` i `PreInvocation` dynamicznie pobierają zmiany z właściwej gałęzi nadrzędnej (`origin "$CURR"`).
- **Synchronizacja Wdrożeniowa**: Zaktualizowano `vault/`, `os-upgrade-project`, `INSTALL.sh`, `docs/API.md` oraz pliki konfiguracyjne rdzenia.

## [6.5.2] - 2026-09-08

### 🛸 Native Executable Grill-Me Skill & Universal Symlink Automation
- **Physical Executable Skill (`vault/.agents/skills/grill-me.js`)**: Wdrożono skrypt CLI (Node.js + Python fallback `grill_me.py`) z 5 krytycznymi pytaniami pre-flight (topologia, auto-sync, bazy fail-closed, edge cases, state-dump).
- **Claude Code & Antigravity Dual Integration**: Zdefiniowano `SKILL.md` w `vault/.agents/skills/grill-me/` i `global_skills/grill-me/` oraz manifest komendy slash `.claude/commands/grill-me.md`.
- **Universal Skill Symlink Automation**: Rozszerzono automatyczne mapowanie symlinków w `INSTALL.sh`, `os-init`, `os-init-claude`, `bootstrap.py`, `bootstrap-claude.py` i `os-upgrade-project` na wszystkie skille w `.agents/skills/*` (w tym `grill-me` i `grill-me.js`).
- **E2E Test Verification**: Rozbudowano zestaw testów w `execution/test_bootstrap.sh` o weryfikację obecności i poprawności dowiązań skilla `/grill-me`.

## [6.5.1] - 2026-09-08

### ⚡ Distributed Multi-Agent Asynchronous Auto-Sync Core
- **Conflict-Free Merge (.gitattributes)**: Wdrożono regułę `merge=union` dla plików pamięci (`.agents/MEMORY.md`) i zadań (`.agents/task.md`) w szablonie Vault i repozytorium bazowym.
- **Natywne Hooki Synchronizacji Cyklu Życia**: Zdefiniowano zdarzenia `SessionStart` / `PreInvocation` (automatyczny `git pull origin main --rebase`) oraz `SessionEnd` / `Stop` (automatyczny zrzut pamięci `git add` + `git commit` + `git push origin HEAD`).
- **Globalne i Lokalne Ustawienia Git**: W instalatorze `INSTALL.sh`, `os-init`, `os-init-claude` i skryptach bootstrappera zautomatyzowano konfigurację `pull.rebase true` oraz `merge.conflictstyle diff3`.
- **Złoty Standard Pamięci (MEMORY.md v0.42.1)**: Dodano szablon pamięci maszynowej z rejestrem węzłów Swarm i logami sesji.
- **Żelazna Zasada Koordynatora (R-SYNC-01)**: Wprowadzono bezwzględny obowiązek wykonania zrzutu stanu (state-dump) przed finalnym raportem do użytkownika.
- **Claude Code Skill Visibility (.claude/skills/)**: Zaimplementowano automatyczne dowiązania symboliczne (`ln -sf`) z `.agents/skills/om-*` do `.claude/skills/` w szablonie Vault, instalatorze i bootstrapperach.
- **Project Modernizer (`os-upgrade-project`)**: Dodano dedykowane narzędzie CLI do bezpiecznej aktualizacji starszych projektów do standardu v6.5 Swarm.
- **E2E Test Suite**: Zaktualizowano `execution/test_bootstrap.sh` z pełną asercją reguł `.gitattributes`, hooków, parametrów gita, dowiązań Claude Code oraz weryfikacją `os-upgrade-project`.

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
