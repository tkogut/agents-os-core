---
name: code-reviewer
description: Auditor logic for PR and local changes. Standard v5.0.
trigger_words: ["review code", "review pr", "check changes", "zrób code review", "przeanalizuj zmiany"]
---

# 🔍 Code Reviewer (v5.0)

🎯 **Purpose**
Techniczny audyt poprawności zmian, bezpieczeństwa (wycieki sekretów) i czystości kodu przed wykonaniem commita lub Pull Requesta.

---

## 1. Automated Operation with `review_helper.py` (Recommended)

W katalogu `global_skills/code-reviewer/scripts/` (lub `.agents/skills/code-reviewer/scripts/` lokalnego projektu) znajduje się skrypt `review_helper.py` automatyzujący audyt zmian.

### Uruchomienie:
```bash
python3 scripts/review_helper.py
```

### Co analizuje skrypt:
1. **Critical / Security Check (Wycieki Sekretów):**
   * Wykrywa w zmodyfikowanym kodzie potencjalnie wklejone na stałe API Keys, hasła, tokeny czy klucze prywatne.
2. **Clean Code Check (Debugery):**
   * Wykrywa pozostawione w kodzie produkcyjnym instrukcje diagnostyczne (`console.log`, `print()`, `breakpoint()`, `pdb.set_trace()`).
3. **Quality Check (Brak testów):**
   * Wykrywa nowo utworzone/zmodyfikowane pliki źródłowe (`.py`, `.js`, `.ts`, `.go`) i ostrzega, jeśli w projekcie brakuje dla nich pliku testowego (np. `test_*.py` lub `*.test.js`).

### Werdykty:
*   Zwraca kod błędu `1` jeśli wykryto błędy krytyczne (sekrety).
*   Zwraca kod błędu `0` jeśli kod jest bezpieczny i gotowy.

---

## 2. Usage Rule for Agent

Agent **musi** wywołać `review_helper.py` przed zleceniem PR lub jako krok pre-commit, aby zapewnić najwyższą jakość kodu. Wynik audytu należy zaprezentować użytkownikowi w podsumowaniu prac.
