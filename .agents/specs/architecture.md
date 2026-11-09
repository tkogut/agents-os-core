# Specyfikacja Architektoniczna AGENTS-OS v7.1 Swarm Edition

Niniejszy dokument przedstawia architekturę, strukturę oraz zasady działania systemu operacyjnego dla agentów — **AGENTS-OS v7.1 (Swarm Edition)**, wdrożonego w repozytorium `tkogut/agents-os-core`. Wersję systemu określa plik [`VERSION`](../../VERSION); zmiany względem wcześniejszych wydań opisuje [`CHANGELOG.md`](../../CHANGELOG.md). Zasady nadrzędne: [`AGENTS-OS.md`](AGENTS-OS.md) (konstytucja).

---

## 1. Wprowadzenie i Cel (Executive Summary)

**AGENTS-OS** to ustrukturyzowane środowisko i zestaw narzędzi integrujących edytor **Antigravity IDE** oraz **Claude Code** z agentami AI. Głównym celem systemu jest automatyzacja cyklu wytwórczego oprogramowania poprzez:
*   Standardyzację struktury projektów (szablon `vault/`).
*   Dynamiczne rozszerzanie możliwości agenta za pomocą pakietów umiejętności (skilli).
*   Autonomiczną synchronizację wiedzy o platformie w architekturze GitOps za pomocą protokołu MCP.
*   Bezpieczną pracę agentów z osobistą bazą wiedzy (Second Brain, ISO 27001) bez naruszania poufności.
*   Stabilność wykonania dzięki obejściom błędów silnika oraz bramkom jakości (hooki, QA gate, testy).

---

## 2. Architektura Roju (The Swarm Triad)

System dystrybuuje zadania pomiędzy trzy wyspecjalizowane role agentowe. Aktualne modele podaje [`CLAUDE.md`](../../CLAUDE.md) i [`agents.yaml`](../../agents.yaml); poniżej wartości z 2026-11-09:

| Rola | Model | Odpowiedzialność i Ograniczenia |
| :--- | :--- | :--- |
| **Coordinator** | Gemini 4 Argon / Gemini 3.8 Flash Medium (Antigravity) | Zarządca kontekstu i backlogu: `task.md`, plany w `.agents/plans/`, zrzut stanu (`.agents/MEMORY.md`). Zakaz modyfikowania kodu w głównym drzewie bez worktree (hook `guard-coordinator`, decyzja `force_ask`). |
| **Builder** | Gemini 3.1 Pro / Claude 3.7 / Claude Opus 5.5 (Claude Code, Cursor, Antigravity) | Implementacja, testy, lokalne walidacje, atomowe commity wyłącznie w izolowanym worktree. Zmiany w `scripts/*` i skryptach instalatora wymagają autoryzacji koordynatora. |
| **Auditor** | Gemini 3.8 Flash Medium / subagent Auditor | Linting, audyt bezpieczeństwa, weryfikacja logów, sprawdzanie matematyczne (`math_check`), akceptacja PR. |

---

## 3. Topologia Katalogu

Repozytorium źródłowe `agents-os-core`:

```
.
├── VERSION                 # Wersja systemu (źródło prawdy)
├── agents.yaml             # Definicja ról i modeli
├── CLAUDE.md, AGENTS.md    # Manifest sesji Claude Code / opis frameworka
├── SDLC.md, CHANGELOG.md   # Cykl wytwórczy, historia zmian
├── INSTALL.sh              # Instalator systemowy
├── os-init, os-init-claude, os-add-skill,
│   os-upgrade-project, os-run-builder, os-publish-knowledge   # CLI
├── .agents/
│   ├── hooks.json          # Hooki Antigravity/Gemini (lustra: .gemini/, .antigravity/)
│   ├── hooks/              # Skrypty hooków Claude Code
│   ├── scripts/            # Kopie strażników (identyczne z scripts/)
│   ├── mcp-servers/        # Lokalne węzły MCP (antigravity-docs)
│   ├── rules/, plans/      # Reguły zachowania, plany operacyjne
│   ├── specs/              # Specyfikacje, graph.json, knowledge/
│   ├── eval/               # Moduł ewaluacji promptów
│   ├── swarm/              # Handshake'e subagentów
│   └── MEMORY.md, task.md  # Stan i backlog (SSOT)
├── .claude/                # settings.json (hooki), commands/, skills/
├── .ai/                    # agentic.config.json, trackers/, browsers/, specs/
├── .github/workflows/      # mcp-docs-updater.yml, om-skills-sync.yml
├── global_skills/          # Skille systemowe
├── scripts/                # Strażnicy, skaner wycieków, publikacja do vaulta, handshake
├── tests/                  # pytest
└── vault/                  # Szablon projektu potomnego („The Vault”)
```

Projekt potomny dostaje podzbiór wg szablonu `vault/` (m.in. `.agents/`, `CLAUDE.md`, `agents.yaml`, `SDLC.md`, skille, strażnicy).

---

## 4. Analiza Komponentów i Narzędzi CLI

### 4.1 Instalator systemowy (`INSTALL.sh`)
Jednorazowa konfiguracja środowiska programisty (Windows WSL2, Ubuntu). Etapy (według komentarzy w skrypcie):
1.  **Zależności systemu** oraz izolowane środowisko Python (venv `~/.antigravity/venv`, m.in. `GitPython`, `PyGithub` dla bootstrappera).
2.  **Integracja z modułem kompresji tożsamości (Caveman)** oraz konfiguracja Gita.
3.  **Kopiowanie The Vault** do `~/.antigravity/templates/v<MAJOR.MINOR>-swarm` (obecnie `v7.1-swarm`); stare szablony są usuwane (lista w skrypcie obejmuje `v5.0`–`v7.0`).
4.  **Globalne umiejętności (skille)** oraz dowiązania narzędzi CLI (symlinki zamiast kopii).
5.  **Rozszerzenie WSL dla Antigravity IDE** i (tylko interaktywnie) logowanie do usług CLI.

### 4.2 `os-init` i `os-init-claude`
`os-init <nazwa-projektu>` tworzy projekt, repozytorium GitHub, pierwszy commit z push i otwiera IDE. Wywoływany jest przez powłokę jako wrapper, który przechwytuje zmienną `__PROJECT_DIR__` i zmienia katalog w bieżącej sesji (osobny proces nie zmieniłby katalogu powłoki nadrzędnej). Szablon pochodzi z lokalnego `vault/` repozytorium lub z `~/.antigravity/templates/v7.1-swarm`. `os-init-claude` tworzy wariant dla Claude Code (CLAUDE.md, `.claude/commands/`).

### 4.3 `os-add-skill`
Skrypt w Pythonie instalujący pakiet umiejętności do `.agents/skills/<nazwa>`. Zabezpieczony przed Path Traversal (blokuje `/`, `\`, `..` w nazwie). Kolejność źródeł: najpierw lokalny szablon (offline, bez wektora supply-chain), potem źródła zdalne (repozytorium `antigravity-awesome-skills` przez API GitHub).

### 4.4 `os-upgrade-project`
Modernizuje istniejący projekt do bieżącego standardu: reguły `.gitattributes` (`merge=union` dla `MEMORY.md`), parametry Gita, hooki Antigravity (`hooks.json` jest **scalany**, nie nadpisywany: `scripts/merge_hooks_json.py`, opcja `--refresh-hooks`), hooki Claude Code (`.claude/settings.json`), dowiązania `.claude/skills/*`, pamięć `MEMORY.md`. Odświeża strażników w `scripts/`, gdy różnią się od źródła.

### 4.5 `os-run-builder`, `os-publish-knowledge`
`os-run-builder <gałąź>` tworzy izolowany worktree Buildera w `tmp/worktrees/`. `os-publish-knowledge` publikuje notatki z `.agents/specs/knowledge` do `<vault>/raw/notes` (skan PII i sekretów, domyślnie dry-run; opcjonalny scaffolding INGEST).

---

## 5. Integracja GitOps & Model Context Protocol (MCP)

System dostarcza wiedzę o platformie i aktualizuje ją autonomicznie:

1.  **Węzeł Dokumentacji (MCP Server):** w `.agents/mcp-servers/antigravity-docs/` działa serwer Node.js ([mcp_server.js](../mcp-servers/antigravity-docs/mcp_server.js)) implementujący protokół MCP; udostępnia narzędzia wyszukiwania i odczytu dokumentacji Antigravity.
2.  **Lokalna Rejestracja:** plik [.gemini/mcp_config.json](../../.gemini/mcp_config.json) deklaruje ścieżkę do serwera, izolując go per-projekt (brak rejestracji globalnej chroni przed wyciekiem kontekstu).
3.  **Autonomiczna Aktualizacja (GitOps CI/CD):** cykliczny przepływ GitHub Actions [.github/workflows/mcp-docs-updater.yml](../../.github/workflows/mcp-docs-updater.yml).

### Przebieg aktualizacji
*   **Krok 1: Scraper (`scraper.py`):** bot uruchamia bezgłową przeglądarkę Playwright na `https://antigravity.google/docs/get-started`, parsuje pasek boczny i zapisuje linki do [links.json](../mcp-servers/antigravity-docs/links.json).
*   **Krok 2: Ekstrakcja (`extractor.py`):** [extractor.py](../mcp-servers/antigravity-docs/extractor.py) pobiera wyrenderowaną treść i zapisuje Markdown w [knowledge_base/](../mcp-servers/antigravity-docs/knowledge_base/).
*   **Krok 3: Dirty-Check & Auto-Commit:** `git diff`; przy zmianach commit `chore(mcp): auto-refresh Antigravity docs YYYY-MM-DD` i push.
*   **Krok 4: Lokalna aktualizacja:** `git pull`; serwer MCP serwuje pliki bezpośrednio z `knowledge_base/`, więc kolejna sesja ma najnowszą wiedzę bez reinstalacji.

---

## 6. Hooki i obejścia błędów silnika

*   **Blokada File Edit Hang (Antigravity):** wbudowany edytor diffów Antigravity potrafi zawiesić wątek; w agentach Antigravity pliki edytuje się przez terminal (Rule 3 w `.agents/rules/core-rule.md`). Claude Code używa własnych narzędzi edycji.
*   **Stale Worktree Crash:** dawny hook `before_model_call: git worktree prune` nie jest już zainstalowany w żadnym `hooks.json`. Osierocone worktree usuwa się ręcznie (`git worktree prune`) i po merge.
*   **Hooki Antigravity/Gemini** (`.agents/hooks.json`, lustra w `.gemini/` i `.antigravity/`): `guard-confidential-gemini` (PreToolUse, poufność vaulta), `guard-coordinator` (PreToolUse, R-ROLE-01) oraz `distributed-sync` (SessionStart, SessionEnd, PreInvocation, Stop).
*   **Hooki Claude Code** (`.claude/settings.json`, skrypty w `.agents/hooks/`): PreToolUse `claude-pre-tool-guard.sh`, re-grounding przy UserPromptSubmit, zrzut przed kompaktowaniem i zrzut stanu przy Stop/SessionEnd.
*   **Git pre-commit** (`scripts/install-git-hooks.sh`): `scripts/check_coordinator_role.sh` blokuje commit kodu na main/master i wymaga handshake'u Buildera.

---

## 7. Second Brain i poufność (ISO 27001)

*   **Dostęp:** Gemini (bez DPA) czyta tylko `index-public.md` i strony bez flagi poufności; Claude Code i Claude Desktop (konto organizacji, DPA) mają stałą zgodę na strony poufne bez prawa do kopiowania ich treści do repozytoriów i plików harnessu.
*   **Mechanizmy:** strażnik `scripts/guard_confidential_gemini.py` (odmowy odczytu stron poufnych, `index.md`, `wiki/overview.md`, rekurencyjnego wyszukiwania; cztery identyczne kopie), skaner `scripts/scan_confidential_leaks.py` (frazy kontrolne i wzorce sekretów w plikach harnessu), skill `second-brain`, publikacja `scripts/publish_knowledge_to_vault.py`.
*   **Dokumenty:** [second-brain-integration-plan.md](second-brain-integration-plan.md), [second-brain-propagation-report.md](second-brain-propagation-report.md).

---

## 8. Wersjonowanie, testy i bramka jakości

*   **Wersja:** plik `VERSION` (np. `7.1.0-swarm`); katalog szablonu `v<MAJOR.MINOR>-swarm`; Rule 4 w `core-rule.md`; spójność wymusza `tests/test_version_consistency.py`.
*   **Testy (`pytest tests`):** strażnicy (poufności i Coordinatora), skaner wycieków, scalanie `hooks.json`, publikacja do vaulta, spójność wersji.
*   **QA gate przed PR** (CLAUDE.md, sekcja 5): `shellcheck`, `py_compile`, `validate-handshakes`, skaner wycieków, opcjonalnie `execution/test_bootstrap.sh`.

---

## 9. Znane ograniczenia (stan 2026-11-09)

*   `claude-pre-tool-guard.sh` kończy się kodem 1, który w Claude Code nie blokuje wywołania (blokuje kod 2); ochrona main/master po stronie Claude'a to zasada, nie blokada techniczna (decyzja właściciela: bez zmian).
*   Strażnik poufności nie pilnuje Claude'a; dla narzędzi bez hooków (Cursor, Codex, aider) zakazy dostępu do vaulta są polityką.

---
*Dokument zaktualizowany dla wydania 7.1.0-swarm (2026-11-09); poprzednia treść opisywała wydanie 5.0-AG/6.5.*
