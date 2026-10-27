---
name: os-publish-knowledge
description: Publish engineering knowledge notes from .agents/specs/knowledge to Obsidian Second Brain (raw/notes) with ISO 27001 secret scan and automatic INGEST scaffolding into wiki/sources/, index.md, and log.md.
trigger: /os-publish-knowledge
trigger_words: ["publish knowledge", "os-publish-knowledge", "ingest knowledge", "publikuj wiedze", "zrob ingest", "ingest sejf"]
---

# 📦 Skill: `os-publish-knowledge` (ISO 27001 & INGEST Scaffolding)

Skill odpowiedzialny za bezpieczną publikację notatek wiedzy inżynieryjnej (`.md`) z katalogu `.agents/specs/knowledge/` projektu do osobistego Sejfu Obsidian (`sejf_tk`), wraz z automatycznym scaffoldingiem procedury **INGEST** (zgodnie ze wzorcem Karpathy LLM Wiki).

---

## 🛡️ Zasady Bezpieczeństwa (ISO 27001)

1. **Skaner Sekretów i PII**:
   - Blokuje transfer plików zawierających: klucze API (`sk-`, `AKIA`), tokeny JWT, klucze prywatne, hasła, adresy e-mail spoza domen MIW Group, numery PESEL i IBAN.
   - W przypadku wykrycia wrażliwych danych raport podaje **tylko nazwę reguły**, nigdy wartość sekretu.
2. **Ochrona przed Nadpisaniem**:
   - Identyczny plik (SHA-256): pomijany (`IDENTICAL_CONTENT`).
   - Różna treść przy istniejącej nazwie: zgłasza konflikt (`TARGET_EXISTS_WITH_DIFFERENT_CONTENT`), brak nadpisania.
3. **Fail-Closed & Zero Full-Disk Probing**:
   - Ścieżka docelowa vaulta pochodzi z: parametru CLI `--dest`, zmiennej `OBSIDIAN_VAULT_PATH` lub domyślnej `/mnt/c/Users/tkogut/Documents/sejf_tk/raw/notes`.
   - Brak skanowania całego dysku.

---

## 🚀 Użycie z Terminala (CLI)

W katalogu dowolnego projektu:

### 1. Podgląd bezpieczny (Dry-Run)
```bash
os-publish-knowledge
```
Sprawdza sekrety, porównuje sumy kontrolne i wyświetla raport bez modyfikowania plików.

### 2. Publikacja do `raw/notes` (Zapis)
```bash
os-publish-knowledge --apply
```
Kopiuje notatki do `<vault>/raw/notes/` ze statusem `status: new`.

### 3. Pełny cykl: Publikacja + Automatyczny Scaffolding INGEST
```bash
os-publish-knowledge --apply --ingest
```
Wykonuje publikację oraz natychmiastowy scaffolding INGEST w vaulcie:
- Tworzy stronę źródłową `wiki/sources/src-<slug>.md` (ze strukturą: Podsumowanie, Szczegóły, Sprzeczności, Powiązania, Źródła),
- Rejestruje źródło w `index.md` pod sekcją `## Źródła (sources)`,
- Dopisuje wpis do dziennika `log.md` (`## [YYYY-MM-DD] ingest | <Tytuł>`),
- Oznacza notatkę w `raw/notes/` jako `status: processed`.

---

## 🤖 Instrukcja dla Agenta AI (Claude / Antigravity / Gemini)

Gdy użytkownik prosi o:
- „Opublikuj notatki wiedzy z projektu”,
- „Wykonaj transfer wiedzy do sejfu”,
- „Zrób ingest wiedzy”,

Wykonaj następujące kroki:

1. **Uruchom weryfikację Dry-Run**:
   ```bash
   os-publish-knowledge --ingest
   ```
2. **Sprawdź raport**:
   - Jeśli `🛑 Zablokowano: > 0` lub `⚠️ Konflikty: > 0` – **ZATRZYMAJ SIĘ**. Zgłoś użytkownikowi pliki do oczyszczenia (podaj tylko typ reguły, zero sekretów).
3. **Zastosuj zmiany (`--apply --ingest`)**:
   ```bash
   os-publish-knowledge --apply --ingest
   ```
4. **Dekompozycja pojęciowa (Opcjonalny krok semantyczny LLM)**:
   - Po scaffoldingu przejrzyj utworzoną stronę `wiki/sources/src-<slug>.md`.
   - Jeśli notatka definiuje nowe kluczowe pojęcia biznesowe lub techniczne, utwórz dedykowane strony w `wiki/concepts/<pojęcie>.md` (min. 2 powiązania, wikilinki) i zaktualizuj `index.md`.
