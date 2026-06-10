# Specyfikacja Architektoniczna AGENTS-OS v5.0 Swarm Edition

Niniejszy dokument przedstawia kompletną architekturę, strukturę oraz zasady działania systemu operacyjnego dla agentów — **AGENTS-OS v5.0 (Swarm Edition)**, wdrożonego w repozytorium `tkogut/agents-os-core`.

---

## 1. Wprowadzenie i Cel (Executive Summary)

**AGENTS-OS** to ustrukturyzowane środowisko i zestaw skryptów narzędziowych integrujących edytor **Antigravity IDE** z agentami AI (w tym CLI `agy` bazującym na Claude Code). Głównym celem systemu jest automatyzacja cyklu wytwórczego oprogramowania poprzez:
*   Standardyzację struktury projektów (Złoty Standard).
*   Dynamiczne rozszerzanie możliwości agenta za pomocą pakietów umiejętności (Skilli).
*   Autonomiczną synchronizację wiedzy o platformie w architekturze GitOps za pomocą protokołu MCP.
*   Zapewnienie stabilności wykonania poprzez implementację sprzętowo-programowych obejść (workarounds) na błędy silnika uruchomieniowego.

---

## 2. Architektura Roju (The Swarm Triad)

System dystrybuuje zadania i logikę pomiędzy trzy wyspecjalizowane role agentowe, eliminując monolityczną odpowiedzialność pojedynczego modelu:

| Rola | Model Domyślny | Odpowiedzialność i Ograniczenia |
| :--- | :--- | :--- |
| **Coordinator** | Gemini 3.5 Flash | Zarządca kontekstu i backlogu. Analizuje plik `task.md` i planuje pracę w `.agents/plans/`. **Kategoryczny zakaz modyfikowania kodu źródłowego.** |
| **Builder** | Claude 4.6 (Thinking) | Wdraża zmiany, refaktoryzuje i optymalizuje kod. Pracuje wyłącznie na wydzielonych gałęziach roboczych (Git Worktrees). |
| **Auditor** | Gemini 3 Flash | Weryfikuje poprawność kodu, uruchamia testy jednostkowe i statyczne, analizuje logi. Działa w tle (Scheduled Tasks). |

---

## 3. Topologia Katalogu Projektu (Skill Anatomy v2.4)

Struktura nowo utworzonego projektu (szablon **The Vault**) ustrukturyzowana jest następująco:

```
.
├── agents.yaml             # Definicja aktywnych ról i przypisanych do nich modeli
├── task.md                 # Dynamiczny backlog i status synchronizacji systemu
├── design-tokens.md        # Wizualne wytyczne projektu (kolory, typografia, style)
├── .gemini/
│   └── mcp_config.json     # Lokalna konfiguracja per-projekt dla serwerów MCP
├── .github/
│   └── workflows/          # Potoki CI/CD (automatyzacja i harmonogramy)
├── .agents/
│   ├── mcp-servers/        # Lokalne węzły Model Context Protocol (np. antigravity-docs)
│   ├── skills/             # Paczki rozszerzeń zainstalowane lokalnie
│   ├── hooks.json          # Hooki bezpieczeństwa i stabilizacji (np. pre-model calls)
│   ├── rules/              # Rygorystyczne instrukcje i ograniczenia zachowania agenta
│   ├── plans/              # Plany operacyjne i podział zadań na subagenty
│   ├── specs/              # Dokumentacja techniczna i Graph RAG (specs/graph.json)
│   └── swarm/              # Pamięć podręczna logów i handshake subagentów
└── src/                    # Folder przeznaczony na zweryfikowany kod źródłowy
```

---

## 4. Analiza Komponentów i Narzędzi CLI

### 4.1 Instalator systemowy (`INSTALL.sh`)
Skrypt odpowiedzialny za jednorazową konfigurację środowiska systemowego programisty w środowisku Windows WSL2 (Ubuntu):
1.  **Zależności systemowe:** Instaluje menedżer pakietów `snapd` oraz GitHub CLI (`gh`).
2.  **Antigravity CLI (`agy`):** Pobiera oficjalny binarny plik wykonywalny napisany w Go i instaluje go w `/usr/local/bin` lub `~/.local/bin`.
3.  **Środowisko Python (venv):** Inicjalizuje odizolowany wirtualny folder `~/.antigravity/venv` i instaluje biblioteki `GitPython` oraz `PyGithub` niezbędne do działania bootstrappera.
4.  **Konfiguracja Shell:** Tworzy plik konfiguracyjny `~/.bashrc.d/antigravity` zawierający definicję aliasu dla `antigravity` (zdalne otwieranie IDE z poziomu WSL za pomocą ścieżki Windows AppData) oraz funkcję powłoki `os-init`.

### 4.2 Narzędzie `os-init`
Funkcja-opakowanie (shell wrapper) wywołująca binarny skrypt `os-init-run`.
*   **Dlaczego funkcja shell, a nie skrypt?** Tradycyjne skrypty uruchamiane jako osobny proces nie mogą modyfikować katalogu roboczego (`cd`) powłoki nadrzędnej. Wrapper przechwytuje zmienną `__PROJECT_DIR__` wypisywaną przez skrypt pythonowy i wykonuje zmianę katalogu w bieżącej sesji terminala.
*   **Proces bootstrapu:** Inicjalizuje repozytorium git $\rightarrow$ Kopiuje szablony z **Vault** $\rightarrow$ Tworzy pierwszy commit $\rightarrow$ Tworzy repozytorium GitHub za pomocą `gh repo create` $\rightarrow$ Wykonuje push $\rightarrow$ Uruchamia Antigravity IDE w nowo powstałym katalogu.

### 4.3 Dynamiczny instalator skilli (`os-add-skill`)
Skrypt w Pythonie pobierający w locie zdefiniowane pakiety umiejętności z repozytorium `antigravity-awesome-skills`.
*   **Bezpieczeństwo:** Zabezpieczony przed atakami typu Path Traversal (blokuje znaki `/`, `\`, `..` w nazwie skilla).
*   **Mechanizm działania:** Odpytuje API GitHub, pobiera rekurencyjnie całą strukturę plików i katalogów określonego skilla i zapisuje go bezpośrednio w katalogu `.agents/skills/<nazwa>`.

---

## 5. Integracja GitOps & Model Context Protocol (MCP)

Wersja 5.0 wdraża system dynamicznego dostarczania wiedzy i autonomicznego aktualizowania bazy dokumentacji:

1.  **Węzeł Dokumentacji (MCP Server):** W folderze `.agents/mcp-servers/antigravity-docs/` uruchomiony jest serwer Node.js ([mcp_server.js](file:///home/tkogut/projects/agents-os-core/.agents/mcp-servers/antigravity-docs/mcp_server.js)) implementujący protokół MCP. Dostarcza on do agenta narzędzia wyszukiwania i odczytu oficjalnej dokumentacji Antigravity.
2.  **Lokalna Rejestracja:** Plik [.gemini/mcp_config.json](file:///home/tkogut/projects/agents-os-core/.gemini/mcp_config.json) deklaruje ścieżkę do serwera MCP, izolując go per-projekt (brak rejestracji globalnej chroni przed wyciekiem kontekstu).
3.  **Autonomiczna Aktualizacja Dokumentacji (GitOps CI/CD):**
    System automatycznie synchronizuje zmiany w oficjalnej dokumentacji bez zaangażowania dewelopera. Całość opiera się na cyklicznym przepływie pracy GitHub Actions zdefiniowanym w [.github/workflows/mcp-docs-updater.yml](file:///home/tkogut/projects/agents-os-core/.github/workflows/mcp-docs-updater.yml).

### Przebieg Przepływu Autonomicznej Aktualizacji (Workflow Sequence):
*   **Krok 1: Inicjalizacja & Scraper (`scraper.py`):** Co miesiąc (lub przy ręcznym uruchomieniu) bot uruchamia bezgłową przeglądarkę Playwright ([scraper.py](file:///home/tkogut/projects/agents-os-core/.agents/mcp-servers/antigravity-docs/scraper.py)) na stronie `https://antigravity.google/docs/get-started`. Parsuje strukturę paska bocznego i zapisuje listę linków do pliku [links.json](file:///home/tkogut/projects/agents-os-core/.agents/mcp-servers/antigravity-docs/links.json).
*   **Krok 2: Ekstrakcja Treści (`extractor.py`):** Skrypt [extractor.py](file:///home/tkogut/projects/agents-os-core/.agents/mcp-servers/antigravity-docs/extractor.py) iteruje po linkach z indeksu, pobiera wyrenderowaną przez JS treść z kontenera `.docs-main-content` i zapisuje czysty tekst do plików Markdown w folderze [knowledge_base/](file:///home/tkogut/projects/agents-os-core/.agents/mcp-servers/antigravity-docs/knowledge_base/).
*   **Krok 3: Dirty-Check & Auto-Commit:** System sprawdza różnice w plikach (`git diff`). W przypadku wykrycia modyfikacji, bot automatycznie tworzy commit `chore(mcp): auto-refresh Antigravity docs YYYY-MM-DD` i wypycha zmiany do repozytorium zdalnego.
*   **Krok 4: Lokalna Aktualizacja i Użycie:** Deweloper pobiera zmiany za pomocą `git pull`. Ponieważ lokalny serwer MCP serwuje pliki bezpośrednio z podkatalogu `knowledge_base/`, agenci roju w kolejnej sesji pracy natychmiast zyskują dostęp do najnowszej wiedzy bez potrzeby restartu czy reinstalacji środowiska.

---

## 6. Zapobieganie Błędom Silnika (Defensive Workarounds)

Z powodu niestabilności wbudowanych mechanizmów IDE, system wymusza rygorystyczne procedury bezpieczeństwa:
*   **Blokada File Edit Hang:** Wbudowane narzędzie edycji diffów w Antigravity generuje pętle zawieszające wątek. Zastąpiono je obowiązkiem edycji plików wyłącznie za pomocą basha (heredoc / cat).
*   **Stale Worktree Crash:** Osierocone gałęzie robocze powodują paraliż agenta. W pliku `.agents/hooks.json` wdrożono automatyczny hook przed każdym zapytaniem do modelu:
    ```json
    {
      "before_model_call": "git worktree prune"
    }
    ```

---
*Dokumentacja wygenerowana zgodnie ze standardem docs-architect. Wersja 5.0-AG.*
