---
name: github-orchestrator
description: >
  [Trigger Words: "github init", "sync github", "github push", "github test",
  "deploy workflow", "auto commit", "zapisz i pushnij", "create pr", "open pull request"]
  [Domain: DevOps, Cloud CI/CD, GitOps, AntiGravity v4.0]
  [Outcomes: automated remote repo creation, structured caveman commits, workflow monitoring]
---

# 🐙 GitHub Orchestrator

🎯 **Purpose**
Automatyzacja pełnego cyklu życia repozytorium GitHub przy użyciu narzędzia `gh` (GitHub CLI). Pozwala Agentowi na zdalne kreowanie repozytoriów, wpychanie kodu i uruchamianie zdalnych akcji CI/CD bez konieczności wychodzenia z terminala w trybie Caveman Ultra+.

🛠️ **Implementation Logic**

Agent używa narzędzia `gh` (upewnij się, że jest zainstalowane/zalogowane).
Jeśli system zwraca brak dostępu, wymuś na użytkowniku komendę `gh auth login`.

A. **Zasada "Zero-Click Repo" (Trigger: "github init")**
1. Gdy użytkownik prosi o inicjalizację chmury dla nowego projektu, wykonaj:
   ```bash
   # Zmienia katalog na root, po czym wywołuje:
   gh repo create <nazwa-folderu> --public --source=. --remote=origin --push
   ```
2. Ustawia poprawnie upstream dla bazy master/main.

B. **Zasada "Auto-Sync" (Trigger: "github sync" / "zapisz i pushnij")**
1. Zbuduj krótki commit message korzystając ze standardów skilla `caveman-commit` (≤ 50 znaków, format Conventional Commits).
2. Wykonaj:
   ```bash
   git add .
   git commit -m "chore: caveman sync" # Zastąp wygenerowaną wiadomością
   git push
   ```

C. **Zasada "Cloud Workflow Runner" (Trigger: "github test" / "github deploy")**
1. Znajdź pliki w `.github/workflows/`.
2. Uruchom workflow na żądanie:
   ```bash
   gh workflow run <nazwa_pliku.yml>
   ```
3. Użyj asynchronicznego skryptu w tle z zapisem do `/tmp/workflow.log` korzystając z polecenia:
   ```bash
   gh run watch > /tmp/workflow.log 2>&1 &
   ```
   (Następnie możesz przeczytać status korzystając z narzędzia `view_file` lub `cat`).

D. **Zasada "Standardized PR" (Trigger: "create pr" / "open pull request")**
1. **Safety**: Sprawdź czy nie jesteś na gałęzi `main`/`master` (`git branch --show-current`).
2. **Preflight**: Uruchom `npm run preflight` (jeśli istnieje).
3. **Template**: Pobierz opis z folderu `.github/` (np. `PULL_REQUEST_TEMPLATE.md`).
4. **Action**: Wygeneruj PR korzystając z Conventional Commits w tytule:
   ```bash
   gh pr create --title "<type>: <desc>" --body-file <tmp_file>
   ```

🗣️ **Usage Rule**
Pamiętaj! Nigdy nie wypisuj w chatcie pełnych logów git, zatrzymuj się tylko na esencji (sukces/porażka). Jeśli workflow padnie, odpal `caveman-review` na logach, by od razu zaproponować plik z poprawką.

Standard AntiGravity v4.0 Swarm | Cloud Sync Automation.
