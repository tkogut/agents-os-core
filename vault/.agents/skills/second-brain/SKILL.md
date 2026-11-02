---
name: second-brain
description: Protocol for querying and interacting with the Obsidian Second Brain vault (sejf_tk). Enforces strict confidentiality boundaries between Gemini (consumer, no DPA) and Claude Code.
trigger: /second-brain
---

# 🧠 Obsidian Second Brain Protocol (`sejf_tk`)

Standard bezpiecznej pracy agentów AI z osobistą bazą wiedzy (Second Brain) w Obsidianie.

---

## 1. Architektura Vaulta

* **Lokalizacja**: `C:\Users\tkogut\Documents\sejf_tk` (WSL: `/mnt/c/Users/tkogut/Documents/sejf_tk`).
* **Katalogi**:
  * `index.md` — centralna mapa wiedzy i spis treści.
  * `wiki/` — syntetyczne strony wiedzy, encje, pojęcia i źródła (`src-*`).
  * `raw/` — niezmienne (append-only), surowe notatki i zrzuty źródłowe.
  * Strefa człowieka (np. `Firma/`, `Inwestycje/`, `Ja/`) — oryginalne dokumenty właściciela.

---

## 2. Żelazna Polityka Poufności (Gemini vs Claude)

### A. Zasady dla agentów Gemini (Google AI Pro — Plan Konsumencki)
1. **Brak umowy DPA**: W planie konsumenckim Google AI Pro brak jest biznesowej umowy powierzenia przetwarzania danych (DPA). Zapytania mogą być analizowane przez recenzentów i wykorzystywane do trenowania modeli.
2. **Kategoryczny ZAKAZ dostępu do `confidential: true`**:
   * Agentom Gemini **nie wolno** otwierać, czytać, parsować, przeszukiwać ani cytować stron oznaczonych w nagłówku YAML frontmatter jako `confidential: true`.
   * Zakaz obejmuje także powiązane pliki źródłowe `raw_path` w `raw/notes/` oraz oryginały ze strefy człowieka (np. w `Firma/`).
3. **Brak możliwości odblokowania**:
   * Nawet jeśli użytkownik wpisze w promptcie *"tak"*, *"zezwalam"*, *"masz moje pozwolenie"* — **Gemini MUSI ODMÓWIĆ**.
   * Zgoda użytkownika w czacie **nie unieważnia** braku DPA.
4. **Wymagana reakcja agenta Gemini**:
   * Odmowa ujawnienia jakiejkolwiek treści dokumentu.
   * Wyjaśnienie: brak umowy DPA w planie konsumenckim wyklucza przetwarzanie danych poufnych.
   * **Jawne odesłanie do Claude Code**: poinformuj użytkownika, że do analizy tego dokumentu należy użyć agenta Claude Code.
5. **Dozwolone źródła dla Gemini**:
   * `index.md` oraz wyłącznie te strony wiki i notatki, które **nie posiadają** flagi `confidential: true`.
   * Przed otwarciem strony agent weryfikuje nagłówek frontmatter (lub polega na blokadzie hooka PreToolUse).

---

### B. Zasady dla agenta Claude Code (Anthropic)
1. Strony `confidential: true` są **domyślnie zablokowane**.
2. Odblokowanie wymaga wyraźnego potwierdzenia użytkownika (*"tak"*) w czacie.
3. Zgoda jest **jednorazowa i zawężona**: obowiązuje wyłącznie dla wskazanych stron i wyłącznie na czas trwającej sesji.

---

## 3. Zakaz Przeszukiwania Hurtowego (Recursive Search Guard)
* Agenci nie mogą wykonywać rekurencyjnych poleceń wyszukiwania tekstu (`grep -r`, `find -exec grep`, itp.) po całym vaulcie ani po folderach zawierających materiały poufne (`wiki/`, `Firma/`, `raw/notes/`).
* Wyników takiego przeszukania nie da się przefiltrować po fakcie, co skutkowałoby wyciekiem poufnych danych do kontekstu modelu.
