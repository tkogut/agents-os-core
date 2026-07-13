---
name: pr-creator
description: Coordinator logic for PR creation and validation. Standard v5.0.
trigger_words: ["create pr", "submit pull request", "make pr", "utwórz pr", "zrób pull request"]
---

# 🌿 PR Creator (v5.0)

🎯 **Purpose**
Automatyzacja tworzenia Pull Requestów na GitHubie po przejściu testów jakościowych i walidacji gałęzi.

---

## 1. Automated Operation with `pr_helper.py` (Recommended)

W katalogu `global_skills/pr-creator/scripts/` (lub w folderze `.agents/skills/pr-creator/scripts/` lokalnego projektu) znajduje się skrypt `pr_helper.py` automatyzujący proces tworzenia PR.

### Uruchomienie:
```bash
python3 scripts/pr_helper.py
```

### Co robi skrypt:
1. **Branch Guard:** Blokuje wykonanie, jeśli agent znajduje się bezpośrednio na gałęziach `master` lub `main`.
2. **Quality Gate:** Automatycznie wykrywa środowisko testowe (npm test / pytest) i uruchamia testy przed PR.
3. **Auto Metadata:** Generuje automatyczny tytuł i opis PR na podstawie historii commitów wykonanych na tej gałęzi.
4. **GitHub CLI Submission:** Otwiera proces tworzenia PR w GitHub CLI.

### Opcje zaawansowane:
*   Pominięcie uruchamiania testów:
    ```bash
    python3 scripts/pr_helper.py --skip-tests
    ```
*   Własny tytuł i opis:
    ```bash
    python3 scripts/pr_helper.py --title "feat(api): add auth endpoint" --body "Implement JWT token login flow"
    ```

---

## 2. Manual Fallback

Jeśli GitHub CLI nie jest skonfigurowany, agent musi wykonać te kroki ręcznie:
1. **Quality Check:** Wywołaj `npm run test` lub `pytest`.
2. **Branch Check:** Upewnij się, że nie jesteś na gałęzi głównej (`git branch --show-current`).
3. **PR Creation:**
   ```bash
   gh pr create --title "<type>: <short description>" --body "<summary of changes>"
   ```

🗣️ **Usage Rule for Agent**
Skrypt `pr_helper.py` powinien być domyślnym narzędziem używanym przez agenta w celu weryfikacji i wdrożenia kodu na GitHubie.
