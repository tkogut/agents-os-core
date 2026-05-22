# WIEDZA: AGENTS-OS v3.2 -> Antigravity 2.0 (Refactoring Specs)
**Tag:** #NotebookLM | **Priorytet:** KRYTYCZNY
**Środowisko docelowe:** Windows WSL (Brak wsparcia dla macOS/brew)

## 1. Aktualizacja Zależności (Terminal)
* **Wygaszenie gemini-cli:** Środowisko `gemini-cli` zostało wchłonięte przez nowe narzędzie `Antigravity CLI` napisane w języku Go. 
* **Zadanie dla instalatora:** Skrypty `INSTALL.sh` i `os-init` muszą zostać zaktualizowane, aby pobierały i inicjowały `Antigravity CLI` z natywnym wsparciem dla wieloagentowości w terminalu.

## 2. Refaktoryzacja Bootstrappera (`bootstrap.py`)
* **Problem:** Obecny system wykorzystuje ryzykowne, surowe wywołania systemowe (np. `subprocess.run` dla komend gita).
* **Rozwiązanie (Dynamic Bootstrapping):** Należy całkowicie usunąć wywołania terminalowe dla GitHuba i Gita. Wymagane jest zaimplementowanie natywnych bibliotek Pythona: `GitPython` (do lokalnego zarządzania i natywnych Worktrees) oraz `PyGithub` (do autoryzacji i tworzenia repozytoriów).

## 3. Przebudowa Konfiguracji Ról
* **Migracja do YAML:** Zgodnie z natywnym formatem `SKILL.md` (wykorzystującym frontmatter YAML), główny plik konfiguracyjny `agents.md` musi zostać zmigrowany na format `agents.yaml`. 
* **Cel:** Umożliwi to nowym dynamicznym subagentom (Subagents) Antigravity 2.0 bezbłędne i natychmiastowe parsowanie swoich ról i uprawnień (np. "Coordinator", "Builder", "Auditor").

## 4. Instalacja Umiejętności (Awesome Skills)
* Ręczne kopiowanie plików skilli zostaje zastąpione oficjalnym instalatorem CLI.
* Skrypt `os-init` ma wywoływać komendę: `npx antigravity-awesome-skills --path .agents/skills --risk safe,none`.

## 5. [CRITICAL] JSON Hooks i Obejścia Błędów
Platforma w wersji 1.23.2+ posiada krytyczne błędy wymagające twardych obejść (workarounds):
* **Stale Worktree Crash:** W pliku `hooks.json` należy zdefiniować skrypt wykonywany *zanim* uruchomi się agent ("before model call"), który uruchamia polecenie `git worktree prune`. Zapobiega to cichemu zawieszaniu się agenta w środowisku Linux/WSL.
* **File Edit Hang (+0 -0):** Narzędzie do wbudowanej edycji plików zawiesza się w nieskończoność. W regułach agentów (szczególnie *The Buildera*) musi zostać wpisany kategoryczny ZAKAZ używania wbudowanego narzędzia edycji plików. Agent musi nadpisywać i edytować pliki wyłącznie za pomocą terminala bash (np. `cat` lub `bash heredoc`).