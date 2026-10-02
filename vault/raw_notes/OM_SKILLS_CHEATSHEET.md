# 🛸 Kompendium i Ściąga: Umiejętności Open-Mercato (OM Skills)
> **Ekosystem:** AGENTS-OS Enterprise Swarm Platform (v6.5)  
> **Liczba modułów:** 36 skilli automatyzacji SDLC  
> **Konfiguracja bazowa:** `.ai/agentic.config.json` | `SDLC.md`

---

## 📑 Spis Treści
1. [Przegląd Architektury i Przepływu SDLC](#1-przegląd-architektury-i-przepływu-sdlc)
2. [Szybka Macierz Skilli (Tabela Referencyjna)](#2-szybka-macierz-skilli-tabela-referencyjna)
3. [Szczegółowy Opis Wszystkich 36 Skilli](#3-szczegółowy-opis-wszystkich-36-skilli)
   - [Kategoria 1: Pipeline Core & Konfiguracja Repozytorium](#kategoria-1-pipeline-core--konfiguracja-repozytorium)
   - [Kategoria 2: Planowanie, Wymagania & Zarządzanie Zgłoszeniami (Issues)](#kategoria-2-planowanie-wymagania--zarządzanie-zgłoszeniami-issues)
   - [Kategoria 3: UX, Design System & Badanie Interfejsów](#kategoria-3-ux-design-system--badanie-interfejsów)
   - [Kategoria 4: Autonomiczna Implementacja, Naprawa Błędów & Pętle Zadań](#kategoria-4-autonomiczna-implementacja-naprawa-błędów--pętle-zadań)
   - [Kategoria 5: Testy, Weryfikacja & Code Review (Bramki Jakości)](#kategoria-5-testy-weryfikacja--code-review-bramki-jakości)
   - [Kategoria 6: Zarządzanie Git, Scalanie & Wydania (Release & Governance)](#kategoria-6-zarządzanie-git-scalanie--wydania-release--governance)
4. [Typowe Łańcuchy Wywołań (Pipelines)](#4-typowe-łańcuchy-wywołań-pipelines)

---

## 1. Przegląd Architektury i Przepływu SDLC

Skille **Open-Mercato (OM)** stanowią standard autonomicznego cyklu wytwórczego oprogramowania (Agentic SDLC). Działają w oparciu o:
- **Pojedyncze Źródło Prawdy (SSOT):** Plik `.ai/agentic.config.json` definiuje komendy walidacyjne, gałęzie bazowe oraz taksonomię etykiet.
- **Bezstratny Stan (Cezar Runtime / Handshake):** Praca na izolowanych gałęziach Git Worktree ze zrzutem stanu do `HANDOFF.md`.
- **Bramki Jakości (Quality Gates):** Weryfikacja lintera, testów jednostkowych, typów i przeglądu kodu przed każdym scaleniem.

```
[Idea / Brainstorm] ➔ [Spec / Issue] ➔ [Worktree / Implementation] ➔ [QA & Review] ➔ [Merge & Release]
       │                      │                       │                    │                 │
  om-brainstorm        om-spec-writing        om-auto-implement    om-auto-qa-pr     om-approve-merge-pr
                       om-prepare-issue       om-auto-fix-issue    om-code-review    om-auto-update-changelog
```

---

## 2. Szybka Macierz Skilli (Tabela Referencyjna)

| Skill OM | Kategoria | Główne Przeznaczenie |
| :--- | :--- | :--- |
| `om-setup-agent-pipeline` | Core / Setup | Inicjalizacja i konfiguracja pipeline'u `.ai/agentic.config.json` |
| `om-pipeline-retro` | Core / Analityka | Analiza wydajności i kosztu poprawek w przebiegach pipeline'u |
| `om-create-skill` | Core / Tworzenie | Tworzenie nowych skilli OM lub podział istniejących według reguł |
| `om-apply-upgrade-notes` | Core / Utrzymanie | Wdrażanie migracji i instrukcji z `UPGRADE_NOTES.md` po aktualizacji |
| `om-brainstorm` | Wymagania | Faza dywergentna: ustrukturyzowana burza mózgów przed kodem/specem |
| `om-spec-writing` | Wymagania | Opracowanie technicznej specyfikacji w standardzie Staff Engineer |
| `om-auto-write-spec` | Wymagania | Autonomiczne wygenerowanie specyfikacji z issue/briefu i otwarcie PR |
| `om-prepare-issue` | Issues | Przygotowanie precyzyjnego zgłoszenia w trackerze (z deduplikacją) |
| `om-auto-manage-issues` | Issues | Triaż, standaryzacja i uzupełnianie etykiet/kontekstu istniejących issues |
| `om-followup-issue-from-pr` | Issues | Tworzenie issues na zadania dodatkowe wyciągnięte z dyskusji w PR |
| `om-close-fixed-issues` | Issues | Automatyczne zamykanie naprawionych issues po scaleniu PR |
| `om-ux-setup` | UX / Design | Ekstrakcja tokenów i komponentów repozytorium do `.uxproof/` |
| `om-ux-shape` | UX / Design | Kształtowanie cech produktu, interfejsu i zachowania AI przed kodowaniem |
| `om-ux-review-pr` | UX / Design | Audyt UX/UI zmian w PR przez inspekcję w żywej przeglądarce |
| `om-verify-in-repo` | Implementacja | Szybka brama tylko do odczytu: sprawdzenie czy błąd faktycznie istnieje |
| `om-root-cause` | Implementacja | Diagnoza przyczyny źródłowej (RCA) i wyznaczenie minimalnego zakresu zmian |
| `om-fix` | Implementacja | Wprowadzenie minimalnej poprawki z testami regresyjnymi w kodzie |
| `om-auto-fix-issue` | Implementacja | Kompletny łańcuch naprawy zgłoszenia od ID issue do gotowego PR |
| `om-auto-implement-spec` | Implementacja | Faza po fazie: wdrożenie całej specyfikacji i wystawienie PR |
| `om-auto-create-pr` | Implementacja | Autonomiczne wykonanie dowolnego zadania programistycznego od A do Z |
| `om-auto-create-pr-loop` | Implementacja | Długodystansowa pętla realizująca duże specyfikacje krok po kroku |
| `om-auto-continue-pr` | Implementacja | Wznowienie pracy nad otwartym PR po przerwaniu lub awarii sesji |
| `om-auto-continue-pr-loop` | Implementacja | Pętla wznawiania wieloetapowego PR aż do pełnego ukończenia |
| `om-auto-fix-pr` | Implementacja | Doprowadzenie istniejącego PR do stanu gotowości do scalenia (merge-ready) |
| `om-pr-autopilot` | Implementacja | Inteligentny pilot: diagnoza stanu PR i automatyczne dokończenie |
| `om-prepare-test-env` | Testy & QA | Przygotowanie środowiska uruchomieniowego i przeglądarek do testów lokalnych |
| `om-integration-tests` | Testy & QA | Tworzenie i uruchamianie testów integracyjnych / E2E w przeglądarce |
| `om-auto-qa-pr` | Testy & QA | Dynamiczne testy QA interfejsu w przeglądarce ze zrzutami ekranu |
| `om-code-review` | Code Review | Silnik przeglądu kodu pod kątem bezpieczeństwa, regresji i standardów |
| `om-auto-review-pr` | Code Review | Autonomiczne review pojedynczego PR w dedykowanym Git Worktree |
| `om-review-prs` | Code Review | Hurtowy przegląd wszystkich oczekujących PR-ów w repozytorium |
| `om-check-and-commit` | Git & Release | Walidacja brancha (lint, testy), auto-poprawki, commit i push |
| `om-open-pr` | Git & Release | Standaryzowane wystawienie/aktualizacja PR z szablonem i etykietami |
| `om-merge-buddy` | Git & Release | Skanowanie i raportowanie gotowości PR-ów do scalenia |
| `om-approve-merge-pr` | Git & Release | Oficjalna aprobata w review i scalenie PR metodą squash-merge |
| `om-auto-update-changelog` | Git & Release | Aktualizacja wpisów w `CHANGELOG.md` na bazie zmergowanych zmian |

---

## 3. Szczegółowy Opis Wszystkich 36 Skilli

### Kategoria 1: Pipeline Core & Konfiguracja Repozytorium

#### 1. `om-setup-agent-pipeline`
- **Rola:** Główny instalator i konfigurator procesów AI w projekcie.
- **Kiedy używać:** Przy pierwszym wdrożeniu AGENTS-OS w repozytorium lub przy zmianie narzędzi/etykiet.
- **Działanie:** Analizuje strukturę repozytorium, wykrywa skrypty walidacyjne (lint, build, test), tworzy plik `.ai/agentic.config.json` oraz generuje bazowe dokumenty SDLC (`SDLC.md`, `CODE_REVIEW.md`, `AGENTS.md`).

#### 2. `om-pipeline-retro`
- **Rola:** Narzędzie retrospektywy i analityki pipeline'u.
- **Kiedy używać:** Gdy chcemy zdiagnozować, dlaczego procesy agentowe trwają zbyt długo lub generują zbędne poprawki.
- **Działanie:** Skanuje historię wykonania zadań w trackerze, kategoryzuje przebiegi (czyste przejście, odzyskiwanie po awarii, pętle) i oblicza koszt poprawek w roboczogodzinach.

#### 3. `om-create-skill`
- **Rola:** Fabryka i architekt nowych umiejętności.
- **Kiedy używać:** Do generowania nowego modułu skilla zgodnego ze standardem OM lub do dekompozycji zbyt dużego pliku `SKILL.md`.
- **Działanie:** Tworzy kompletną strukturę skilla (YAML frontmatter, reguły, brama lintera), zachowując warstwową architekturę i kontrakty między-skillowe.

#### 4. `om-apply-upgrade-notes`
- **Rola:** Automatyczny wykonawca aktualizacji biblioteki skilli.
- **Kiedy używać:** Po pobraniu nowej wersji paczki skilli OM do repozytorium.
- **Działanie:** Czyta plik `UPGRADE_NOTES.md`, identyfikuje wymagane zmiany konfiguracyjne lub refaktoryzacje i bezpiecznie aplikuje je w projekcie.

---

### Kategoria 2: Planowanie, Wymagania & Zarządzanie Zgłoszeniami (Issues)

#### 5. `om-brainstorm`
- **Rola:** Moderator etapu koncepcyjnego przed podjęciem decyzji o kodowaniu.
- **Kiedy używać:** Gdy pomysł jest mglisty, użytkownik pyta „czy warto to budować” lub „przemyślmy to”.
- **Działanie:** Zadaje pytania otwierające (jedno na raz), analizuje alternatywy (w tym brak zmian), wyznacza rekomendowaną ścieżkę i przygotowuje brief dla kolejnego skilla.

#### 6. `om-spec-writing`
- **Rola:** Architekt dokumentacji technicznej i specyfikacji funkcjonalnych.
- **Kiedy używać:** Do tworzenia rzetelnego RFC/design-doca dla nowej funkcji lub modułu.
- **Działanie:** Działa w roli Staff Engineera. Tworzy szkielet specyfikacji, wymusza bramkę pytań otwartych (Open Questions gate), bada wzorce rynkowe i dzieli wdrożenie na fazy i kroki.

#### 7. `om-auto-write-spec`
- **Rola:** W pełni autonomiczny generator specyfikacji.
- **Kiedy używać:** Do szybkiej zamiany zgłoszenia (issue) lub briefu w gotowy Pull Request ze specyfikacją.
- **Działanie:** Uruchamia `om-spec-writing` w trybie autonomicznym, generuje makiety i zrzuty ekranu jako dowody PR oraz dodaje metadane umożliwiające natychmiastowe przekazanie do `om-auto-implement-spec`.

#### 8. `om-prepare-issue`
- **Rola:** Precyzyjny twórca zgłoszeń w trackerze zadań (GitHub Issues).
- **Kiedy używać:** Gdy chcemy opisać zadanie / zarejestrować pomysł bez natychmiastowego kodowania.
- **Działanie:** Sprawdza duplikaty wśród istniejących issues/PR, linkuje powiązane specyfikacje, dołącza dowody (np. zrzuty ekranu), definiuje jasne kryteria akceptacji i nadaje etykiety SDLC.

#### 9. `om-auto-manage-issues`
- **Rola:** Menedżer i higienista tablicy zgłoszeń.
- **Kiedy używać:** Do uporządkowania chaotycznych, niedostatecznie opisanych zgłoszeń w trackerze.
- **Działanie:** Wzbogaca issues o brakujące etykiety, sprawdza spójność ze specyfikacjami i formatuje zgłoszenia pod kątem gotowości do autonomicznego wdrożenia przez agenta.

#### 10. `om-followup-issue-from-pr`
- **Rola:** Ekstraktor zadań odroczonych (Follow-up generator).
- **Kiedy używać:** Po dyskusji w review PR, gdy pewne usprawnienia zostają odłożone na później.
- **Działanie:** Parsuje link do PR lub konkretnego komentarza, wyciąga z niego kontekst i otwiera nowe issue przypisane do odpowiedniego autora lub recenzenta.

#### 11. `om-close-fixed-issues`
- **Rola:** Automat porządkujący zamknięte zgłoszenia.
- **Kiedy używać:** Po zmergowaniu PR-ów do gałęzi głównej w ramach procesu release.
- **Działanie:** Zamyka issues powiązane słowami kluczowymi (`fixes`, `closes`, `resolves`), dodaje informacyjne podsumowania i zdejmuje blokady (claim locks).

---

### Kategoria 3: UX, Design System & Badanie Interfejsów

#### 12. `om-ux-setup`
- **Rola:** Ekstraktor reguł wzornictwa do formatu maszynowego.
- **Kiedy używać:** Jednorazowo w projekcie posiadającym UI lub po modyfikacji tokenów designu.
- **Działanie:** Skanuje repozytorium pod kątem tokenów CSS/Tailwind, rejestru komponentów i archetypów ekranów, zapisując wyekstrahowany kontrakt do `.uxproof/`.

#### 13. `om-ux-shape`
- **Rola:** Projektant logiki interakcji i użyteczności funkcji (Product & UX Shaping).
- **Kiedy używać:** Przed implementacją ekranów – do uproszczenia złożonych przepływów lub zdefiniowania zachowania komponentów AI.
- **Działanie:** Łączy wartość biznesową, ergonomię interfejsu, stany ekranów (loading, empty, error) oraz ograniczenia techniczne w spójną decyzję projektową.

#### 14. `om-ux-review-pr`
- **Rola:** Doświadczony audytor UX badający Pull Requesty.
- **Kiedy używać:** Do weryfikacji zmian wizualnych i interfejsowych w otwartym PR.
- **Działanie:** Uruchamia aplikację w przeglądarce, przechodzi ścieżki użytkownika i generuje 4-elementowy raport: **Dowód (Evidence)**, **Wzorzec (Pattern)**, **Kompromis (Trade-off)** i **Kryterium Akceptacji**.

---

### Kategoria 4: Autonomiczna Implementacja, Naprawa Błędów & Pętle Zadań

#### 15. `om-verify-in-repo`
- **Rola:** Szybka, bezpieczna brama weryfikacyjna triage (Read-Only).
- **Kiedy używać:** Jako pierwszy krok łańcucha naprawy błędu.
- **Działanie:** Działa w trybie tylko do odczytu. Sprawdza, czy raportowany błąd rzeczywiście występuje na obecnym branchu, czy ktoś już nad nim nie pracuje lub czy nie został już naprawiony.

#### 16. `om-root-cause`
- **Rola:** Analityk przyczyn źródłowych (Root Cause Analysis).
- **Kiedy używać:** Po potwierdzeniu błędu, przed przystąpieniem do pisania kodu.
- **Działanie:** Lokalizuje dokładne miejsce w kodzie wywołujące defekt i definiuje minimalną powierzchnię zmian niezbędną do usunięcia usterki.

#### 17. `om-fix`
- **Rola:** Precyzyjny mechanik usuwający usterkę.
- **Kiedy używać:** Mając gotową analizę z `om-root-cause`.
- **Działanie:** Blokuje zadanie w trackerze (claim issue), wprowadza minimalną wymaganą zmianę w kodzie, dopisuje testy regresyjne i uruchamia bramkę walidacyjną. Nie commituje samoczynnie kodu.

#### 18. `om-auto-fix-issue`
- **Rola:** Kompleksowy, autonomiczny naprawiacz błędów.
- **Kiedy używać:** Gdy podajemy tylko numer zgłoszenia (np. `om-auto-fix-issue 123`) i oczekujemy gotowego PR.
- **Działanie:** Wykonuje pełną sekwencję: `om-verify-in-repo` ➔ `om-root-cause` ➔ `om-fix` ➔ `om-open-pr` ➔ `om-auto-review-pr`.

#### 19. `om-auto-implement-spec`
- **Rola:** Autonomiczny wykonawca specyfikacji technicznych.
- **Kiedy używać:** Do wdrożenia zaakceptowanego dokumentu specyfikacji w kodzie.
- **Działanie:** Czyta plan wdrożenia ze specyfikacji, implementuje zadania krok po kroku, odpala testy po każdym etapie i publikuje kompletny Pull Request.

#### 20. `om-auto-create-pr`
- **Rola:** Uniwersalny realizator zadań autonomicznych.
- **Kiedy używać:** Do zrealizowania dowolnego zwięzłego zadania od briefu tekstowego po gotowy, zweryfikowany PR.
- **Działanie:** Tworzy izolowane środowisko, planuje kroki, pisze kod, weryfikuje bramkami testowymi i otwiera PR z pełną dokumentacją.

#### 21. `om-auto-create-pr-loop`
- **Rola:** Długodystansowy wykonawca wieloetapowych projektów.
- **Kiedy używać:** Przy bardzo dużych zadaniach, które przekraczają pojedyncze okno kontekstowe agenta.
- **Działanie:** Działa w pętli z cyklicznym zrzutem punktów kontrolnych (checkpoints) i wznawianiem stanu z `HANDOFF.md`.

#### 22. `om-auto-continue-pr`
- **Rola:** Operator wznawiania przerwanych prac.
- **Kiedy używać:** Gdy sesja budowania PR została przerwana przez timeout, błąd sieci lub wyczerpanie limitu tokenów.
- **Działanie:** Odczytuje stan gałęzi PR, ładuje ostatni zrzut z `HANDOFF.md` i kontynuuje realizację kolejnych kroków z planu.

#### 23. `om-auto-continue-pr-loop`
- **Rola:** Pętla wznawiająca dla procesów wsadowych.
- **Kiedy używać:** Do automatycznego dociągania skomplikowanych PR-ów w trybie nienadzorowanym.
- **Działanie:** Wielokrotnie wywołuje logikę kontynuacji aż do momentu, gdy wszystkie kroki ze specyfikacji zostaną odznaczone jako ukończone.

#### 24. `om-auto-fix-pr`
- **Rola:** Ratownik zablokowanych lub odrzuconych Pull Requestów.
- **Kiedy używać:** Gdy PR ma czerwone CI, konflikty z bazą lub uwagi w review.
- **Działanie:** Pobiera uwagi recenzentów i błędy z testów CI, poprawia kod, aktualizuje testy i dopycha zmiany na gałąź PR.

#### 25. `om-pr-autopilot`
- **Rola:** Diagnosta i pilot prowadzący PR do scalenia.
- **Kiedy używać:** Gdy chcemy powiedzieć: „dokończ PR #123 i doprowadź go do merge'a”.
- **Działanie:** Diagnozuje aktualny stan PR (brakujące review, nierozwiązane wątki, brak testów QA), dobiera właściwe skille OM i wykonuje je sekwencyjnie.

---

### Kategoria 5: Testy, Weryfikacja & Code Review (Bramki Jakości)

#### 26. `om-prepare-test-env`
- **Rola:** Inżynier lokalnego środowiska testowego.
- **Kiedy używać:** Przed uruchomieniem testów integracyjnych i badań w przeglądarce.
- **Działanie:** Buduje skrypty startowe dla aplikacji, uruchamia bazę danych/mocki, konfiguruje sterowniki przeglądarek i generuje deskryptor środowiska testowego.

#### 27. `om-integration-tests`
- **Rola:** Twórca i wykonawca testów integracyjnych / End-to-End.
- **Kiedy używać:** Do weryfikacji przepływów biznesowych na żywym organizmie aplikacji.
- **Działanie:** Steruje przeglądarką, eksploruje interfejs, tworzy powtarzalne scenariusze testowe i zapisuje artefakty z diagnozy błędów.

#### 28. `om-auto-qa-pr`
- **Rola:** Automatyczny tester jakości interfejsu w PR.
- **Kiedy używać:** Do weryfikacji UI w otwartym PR przed zatwierdzeniem przez zespół.
- **Działanie:** Uruchamia branch PR w przeglądarce, wykonuje scenariusze testowe użytkownika, rejestruje błędy konsoli i dołącza zrzuty ekranu do raportu w PR.

#### 29. `om-code-review`
- **Rola:** Główny silnik analizy statycznej i audytu kodu.
- **Kiedy używać:** Do oceny dowolnego diffa, brancha lub PR pod kątem zgodności ze standardami.
- **Działanie:** Sprawdza bezpieczeństwo, poprawność logiczną, kompatybilność wsteczną, reguły architektury i generuje werdykt (Approve / Request Changes) wraz z wagami błędów (Critical, Major, Minor).

#### 30. `om-auto-review-pr`
- **Rola:** Autonomiczny recenzent pojedynczego PR.
- **Kiedy używać:** Do pełnego zrecenzowania konkretnego PR w izolowanym środowisku.
- **Działanie:** Pobiera PR do odrębnego worktree, odpala walidacje, wykonuje `om-code-review` i publikuje oficjalny komentarz z review na GitHubie/trackerze.

#### 31. `om-review-prs`
- **Rola:** Dyspozytor hurtowego przeglądu kodu.
- **Kiedy używać:** Do masowego sprawdzenia wszystkich oczekujących PR-ów w kolejce.
- **Działanie:** Iteruje po nieprzejrzanych pull requestach (od najnowszego), rezerwuje blokady (locks) i deleguje zadania do `om-auto-review-pr`.

---

### Kategoria 6: Zarządzanie Git, Scalanie & Wydania (Release & Governance)

#### 32. `om-check-and-commit`
- **Rola:** Strażnik czystości gałęzi lokalnej.
- **Kiedy używać:** Przed wypchnięciem zmian (push) na zdalne repozytorium.
- **Działanie:** Uruchamia po kolei wszystkie skonfigurowane polecenia weryfikacyjne (linter, testy, typy, spójność tłumaczeń i18n), a po ich sukcesie tworzy zwięzły commit i wykonuje push.

#### 33. `om-open-pr`
- **Rola:** Standaryzowany otwieracz i aktualizator Pull Requestów.
- **Kiedy używać:** Po zakończeniu prac implementacyjnych na gałęzi roboczej.
- **Działanie:** Commituje stan roboczy, wypycha gałąź, tworzy lub aktualizuje PR z jednolitym szablonem opisu, aplikuje etykiety SDLC i zwalnia blokady zadań.

#### 34. `om-merge-buddy`
- **Rola:** Asystent i monitor kolejki scalania.
- **Kiedy używać:** Aby sprawdzić, które PR-y są gotowe do połączenia z główną gałęzią.
- **Działanie:** Skanuje otwarte PR, analizuje statusy CI, zatwierdzenia recenzentów oraz brak konfliktów, po czym generuje raport o gotowości do scalenia.

#### 35. `om-approve-merge-pr`
- **Rola:** Autoryzowany wykonawca scalenia (Squash-Merge).
- **Kiedy używać:** Do ostatecznego zatwierdzenia i wdrożenia przetestowanego PR do gałęzi bazowej.
- **Działanie:** Wystawia oficjalną akceptację w review, scala PR metodą squash-merge, usuwa gałąź roboczą i zamyka powiązane blokady.

#### 36. `om-auto-update-changelog`
- **Rola:** Redaktor i kronikarz wydań (`CHANGELOG.md`).
- **Kiedy używać:** Podczas przygotowywania nowego wydania (Release) po serii zmergowanych PR-ów.
- **Działanie:** Analizuje zmiany od ostatniego taga, grupuje je według czytelnych kategorii z emoji (✨ Features, 🐛 Fixes, 🔒 Security, ⚡ Performance) i dopisuje sekcję do `CHANGELOG.md`.

---

## 4. Typowe Łańcuchy Wywołań (Pipelines)

### 🐛 Łańcuch Autonomicznej Naprawy Błędu (Autofix Chain)
```
om-verify-in-repo ➔ om-root-cause ➔ om-fix ➔ om-open-pr ➔ om-auto-review-pr
```
*Szybka ścieżka:* `om-auto-fix-issue {issueId}`

### 🚀 Łańcuch Wdrożenia Nowej Funkcjonalności (Feature Flow)
```
om-brainstorm ➔ om-auto-write-spec ➔ om-auto-implement-spec ➔ om-auto-qa-pr ➔ om-approve-merge-pr
```

### 🛡️ Łańcuch Publikacji Wydania (Release Flow)
```
om-merge-buddy ➔ om-approve-merge-pr ➔ om-close-fixed-issues ➔ om-auto-update-changelog
```

---
*Dokument wygenerowany dla platformy AGENTS-OS.*
