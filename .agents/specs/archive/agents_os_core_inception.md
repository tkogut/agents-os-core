# WIEDZA: AGENTS-OS Core Inception (Repozytorium Systemowe)
**Tag:** #NotebookLM | **Priorytet:** KRYTYCZNY
**Cel:** Przebudowa repozytorium `tkogut/agents-os-core` pod standard AGENTS-OS v5.0 / Antigravity 2.0.

## 1. Problem Architektoniczny
* Repozytorium źródłowe instalatora nie posiada własnej struktury agentowej. Agent GEM nie może nim autonomicznie zarządzać bez folderu `.agents/` oraz plików konfiguracyjnych.

## 2. Wymagana Topologia (Skill Anatomy v2.3)
Należy wdrożyć pełną strukturę w głównym katalogu (root) repozytorium:
* `agents.yaml` - Rejestr ról (GEM, Coordinator, Builder, Auditor).
* `task.md` - Dynamiczny backlog dla agenta GEM.
* `design-tokens.md` - Pusty plik (lub zasady formatowania terminala).
* `.agents/skills/` - Pusty katalog przygotowany na skille systemowe.
* `.agents/rules/` - Reguły (w tym zakaz używania File Edit Tool).
* `.agents/specs/graph.json` - Pusty szkielet Graph RAG dla śledzenia zależności między `INSTALL.sh`, a `vault/`.
* `.agents/plans/` oraz `.agents/swarm/` - Katalogi na logi i planowanie asynchroniczne.

## 3. Adaptacja katalogu src/
W standardowych projektach kod ląduje w `src/`. Ponieważ jest to repozytorium systemowe/instalacyjne, pliki takie jak `INSTALL.sh`, `os-init` oraz folder `vault/` i `global_skills/` zostają w głównym katalogu, ale należy je opisać w `graph.json` jako "Core Infrastructure".

## 4. [CRITICAL] Bezpieczeństwo Edycji
Nadal obowiązuje ominięcie krytycznego błędu Antigravity 1.23.2+: Agent ma kategoryczny ZAKAZ używania natywnego narzędzia edycji plików (powodującego nieskończoną pętlę +0 -0). Wszystkie nowe katalogi i pliki muszą zostać wygenerowane wyłącznie przez komendy terminala (`mkdir`, `touch`, `cat`, `bash heredoc`).
