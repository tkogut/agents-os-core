---
name: test-creator
description: Universal test-writing and configuration assistant for Vitest (frontend), Pytest (backend), and Playwright (E2E) in AGENTS-OS.
triggers:
  - "test-creator"
  - "create tests"
  - "write unit tests"
  - "add E2E tests"
  - "configure vitest/playwright/pytest"
version: "2.2"
---

# 🛠️ Test Creator (v2.2)

🎯 **Purpose**
Dostarczanie standaryzowanych wzorców, konfiguracji oraz zautomatyzowanych szablonów do szybkiego tworzenia i rozbudowy wielowarstwowych testów (Unit, Integration, E2E) w strukturze AGENTS-OS. Zapewnia pełną pokrywalność kodu i stabilność komunikacji (bridge) frontend-backend.

---

## 🛠️ Implementation Logic

Wydzielamy trzy niezależne warstwy testowania, z których każda odpowiada za inny aspekt systemu:

### 1. Unit Tests Frontendu (Vitest + JSDOM)
- **Kiedy stosować**: Testowanie funkcji czysto logicznych, obliczeniowych (np. wyliczanie współczynników KPI, współrzędnych wykresu SVG) oraz izolowanych manipulacji DOM.
- **Zasada działania**: Uruchamianie w node-jsdom z wstrzykniętą strukturą HTML i zamockowanymi obiektami globalnymi (`window`, `fetch`).
- **Szablon wdrożenia**: [Vitest Template](file:///home/tkogut/projects/osint-lead-tracker/.agents/skills/test-creator/references/vitest_template.js).

### 2. Unit/Integration Tests Backendu (Pytest + httpx)
- **Kiedy stosować**: Testy logiki biznesowej API, modeli bazodanowych SQLAlchemy, weryfikacja schematów Pydantic i deduplikacji szans.
- **Zasada działania**: Użycie asynchronicznych fixturek pytest z asynchronicznym klientem HTTPX (`ASGITransport`) i tymczasowym połączeniem z testową bazą danych.
- **Szablon wdrożenia**: [Pytest Template](file:///home/tkogut/projects/osint-lead-tracker/.agents/skills/test-creator/references/pytest_template.py).

### 3. End-to-End (E2E) / Bridge Verification (Playwright)
- **Kiedy stosować**: Testowanie pełnych ścieżek użytkownika (User Journeys) w rzeczywistej przeglądarce, logowanie sesyjne, interakcje UI z bazą danych w tle.
- **Zasada działania**: Playwright automatycznie podnosi serwer uvicorn ze wskazanego katalogu roboczego (`cwd`), konfiguruje bazę danych i przeprowadza testy w trybie headless.
- **Szablon wdrożenia**: [Playwright Template](file:///home/tkogut/projects/osint-lead-tracker/.agents/skills/test-creator/references/playwright_template.js).

---

## 🗣️ Usage Rule
Wywołaj `test-creator` w sesji subagenta lub głównego wątku zawsze gdy:
- Wdrażasz nową funkcję produkcyjną (wymóg dodania pokrycia testowego przed push/handshake).
- Refaktoryzujesz strukturę bazodanową lub API (aby zapobiec regresjom i problemom z kontraktami API).
- Rozbudowujesz potok CI/CD o automatyczne testy regresji.

---

## 📋 Workflow

1. **Wybór Warstwy**: Określ, którą warstwę testujesz (Frontend Unit / Backend Integration / E2E).
2. **Setup Folderu**: Upewnij się, że pliki trafiają do właściwej ścieżki (`frontend-tests/unit/`, `tests/backend/` lub `frontend-tests/e2e/`).
3. **Pobranie Szablonu**: Skopiuj odpowiedni szablon z folderu `references/`.
4. **Mockowanie Zewnętrznych Usług**: Zawsze mockuj zapytania do sieci (np. Gemini API, Odoo) w testach jednostkowych.
5. **Uruchomienie Lokalne**: Wykonaj `./run_tests.sh` w celu zbiorczej weryfikacji.
6. **Złożenie Handshake**: Po pomyślnym wykonaniu wygeneruj sygnatury poprawności.
