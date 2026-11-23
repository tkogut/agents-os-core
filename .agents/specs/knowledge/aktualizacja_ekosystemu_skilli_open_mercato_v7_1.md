---
tags: ["#NotebookLM", "#ExpertKnowledge", "#OpenMercato", "#CezarRuntime", "#SwarmTriad", "#GraphRAG", "#AgentsOS"]
date_synced: "2026-11-23"
version: "7.1.0-swarm"
status: "STABLE"
title: "Aktualizacja Ekosystemu Skilli Open-Mercato v7.1 (Nowe Moduły SDLC i Multi-Model Harness)"
---

# 🧠 BAZA WIEDZY DLA NOTEBOOK.LM: AKTUALIZACJA EKOSYSTEMU SKILLI OPEN-MERCATO (v7.1)
> **Dokument źródłowy:** AGENTS-OS Platform v7.1 Swarm & Open-Mercato Upstream
> **Zastosowanie:** Uzupełnienie bazy wiedzy Sejfu Obsidian (`sejf_tk`) o 38 nowych i rozszerzonych modułów SDLC.
> **Łączna liczba modułów w ekosystemie:** 74 skille `om-*` (oraz 28 systemowych, łącznie 102 skille w Vault).

---

## 🌐 1. EWOLUCJA ARCHITEKTONICZNA: OD MONOLITU DO MULTI-MODEL HARNESS

Wersja 7.1 frameworka AGENTS-OS wprowadza fundamentalne rozszerzenie możliwości autonomicznego wytwarzania oprogramowania. Dotychczasowy rdzeń 36 skilli skupiał się na standardowym potoku: triage -> fix -> worktree -> validation -> review loop.

Nowa fala 38 skilli wprowadza 4 nowe paradygmaty:
1. **Multi-Model Staged Harness (`om-implement-feature-*`, `om-fix-issue-*`):**
   - Delegowanie wąskich pakietów wdrożeniowych (Implementation Packets) do tańszych/szybszych modeli roboczych (np. Flash/Sonnet), przy zachowaniu nadrzędnej orkiestracji i walidacji przez model wiodący.
2. **Product Discovery & Synthetic Personas (`om-discover`, `om-synthetic-users`, `om-mockup-prototype`):**
   - Faza przedimplementacyjna: od weryfikacji pomysłu biznesowego, przez symulację decyzji syntetycznych użytkowników pod presją, aż po generowanie klikalnych makiet low-fi.
3. **Paranoid Security & Dependency Auditing (`om-auto-sec-report*`, `om-auto-audit-dependencies`):**
   - Dedykowane moduły bezpieczeństwa klasy OWASP, mapy podatności lockfile oraz generowanie zanonimizowanych raportów bezpieczeństwa dla PR-ów i wydań.
4. **Smart Testing & Autonomous Merge Queues (`om-smart-test`, `om-auto-merge-buddy`, `om-auto-merge-triage`):**
   - Redukcja kosztów CI/CD: uruchamianie wyłącznie testów dotkniętych zmianami w kodzie oraz bezobsługowa kolejka PR dociągająca kod do merge'a.

---

## 🗺️ 2. PRZEGLĄD 38 NOWYCH I ROZSZERZONYCH SKILLI WG DOMEN

### 📁 Grupa A: Zarządzanie Kontekstem, Higiena i Ewolucja Repozytorium
* **`om-ai-context-maintenance`**: Automatyczna rotacja i archiwizacja starych katalogów uruchomieniowych `.ai/runs` i planów do skompresowanych archiwów `.tgz`. Domyślnie utrzymuje ostatnie 14 dni w stanie rozpakowanym, zapobiegając rozrostowi repozytorium.
* **`om-create-agents-md`**: Generowanie i aktualizacja reguł `AGENTS.md` (zarówno dla roota, jak i podmodułów) na bazie faktycznego kodu źródłowego, komend testowych i wzorców projektowych.
* **`om-share-this-session`**: Bezpieczne udostępnianie zanonimizowanych sesji agenta i artefaktów. Przeprowadza pełną sanityzację prywatności i weryfikację zgody przed wygenerowaniem paczki ZIP.
* **`om-evolve-harness`**: Analiza i samoczynna ewolucja konfiguracji harnessu w oparciu o zebrane metryki wydajności i błędy sesji.
* **`om-eject-and-customize`**: Bezpieczny mechanizm "eject" dla modułów i zależności zewnętrznych z zachowaniem historii proweniencji do przyszłych diffów upgrade'owych.
* **`om-framework-context`**: Dostarczanie ustrukturyzowanej wiedzy kontekstowej o architekturze frameworka do promptów agentów.
* **`om-help`**: Globalny katalog komend i routing intencji dla wszystkich skilli ekosystemu OM.

### 📁 Grupa B: Inżynieria Wymagań, Odkrywanie Produktu i UX
* **`om-discover`**: Prowadzenie ustrukturyzowanego wywiadu produktowego i generowanie `product-brief.md` (problem, dowody, zakres, decyzje, ryzyka).
* **`om-setup-discovery-pipeline`**: Konfiguracja bramki Discovery w SDLC, integracja ról produktowych i reguł Definition of Ready w `SDLC.md`.
* **`om-app-spec-writing`**: Opracowywanie biznesowych specyfikacji aplikacji (App Spec) zawierających model domenowy, analizę ROI przepływów i mapowanie luk platformowych.
* **`om-backlog`**: Automatyczna dekompozycja briefu produktowego lub faz specyfikacji na epiki, historyjki użytkownika (z kryteriami akceptacji) oraz atomowe zadania.
* **`om-synthetic-users`**: Budowa paneli syntetycznych person badawczych i symulacja ścieżek użytkownika pod presją decyzyjną (analiza tarć, weryfikacja założeń UX).
* **`om-mockup-prototype`**: Budowa klikalnych prototypów low-fi w przeglądarce przed przejściem do szczegółowego designu i implementacji.
* **`om-ux-design`**: Projektowanie szczegółowych ekranów i powiązanych prototypów w oparciu o tokeny i system komponentów projektu.
* **`om-figma-design-with-ds`**: Generowanie i mapowanie komponentów interfejsu z Design Systemem w środowisku Figma.

### 📁 Grupa C: Audyt Jakości, Bezpieczeństwo i Przygotowanie Implementacji
* **`om-pre-implement-spec`**: Rygorystyczny audyt specyfikacji przed implementacją (bramka gotowości, audyt kompatybilności wstecznej `BACKWARD_COMPATIBILITY.md`, analiza luk).
* **`om-gap-analysis`**: Identyfikacja brakujących elementów, niespójności API i długów technicznych w kodzie względem wymagań.
* **`om-auto-sec-report-pr`**: Paranoidalny audyt bezpieczeństwa klasy OWASP dla pojedynczego PR/diffa (wykrywanie nieoczywistych wektorów ataku, raport ze zredagowanymi payloadami).
* **`om-auto-sec-report`**: Agregacja analiz bezpieczeństwa w oknie czasowym (np. ostatnie 7 dni wydań) z mapą cieplną ryzyka.
* **`om-auto-audit-dependencies`**: Automatyczny audyt zależności w plikach lockfile względem baz podatności (OSV, CVE) z automatycznym tworzeniem dedykowanych issue.

### 📁 Grupa D: Kolejki Zgłoszeń i Autonomiczny Automerge
* **`om-auto-issue-triage`**: Inteligentny ranking otwartych zgłoszeń bug/feature kwalifikujących się do automatycznej naprawy (z nadaniem etykiety `cez-autofix` po akceptacji człowieka).
* **`om-auto-merge-triage`**: Analiza otwartych PR-ów pod kątem dojrzałości do scalenia (podział na tiery kwalifikacji, ocena dowodów testowych i screenshotów).
* **`om-auto-merge-buddy`**: Autonomiczny proces roboczy obsługujący kolejkę PR (lokalna naprawa CI, dociąganie review, weryfikacja bramek i squash-merge).

### 📁 Grupa E: Wielomodelowe i Zoptymalizowane Łańcuchy Wytwórcze
* **`om-setup-agent-harness`**: Konfiguracja macierzy modeli, puli workerów implementacyjnych, niezależnych doradców audytowych i polityk pakietów high-assurance.
* **`om-harness`**: Narzędzie operacyjne do zarządzania stanem i parametrami środowiska harnessu.
* **`om-implement-feature`**: Wdrażanie dużych funkcjonalności w ustrukturyzowanych etapach z checkpointami testowymi.
* **`om-implement-feature-optimized`**: Zoptymalizowana wersja delegująca zadania do dedykowanych modeli roboczych w celu redukcji kosztów tokenów.
* **`om-implement-feature-multi`**: Implementacja równoległa z wykorzystaniem wielu wątków i workerów.
* **`om-implement-feature-multi-optimized`**: Najbardziej zaawansowany wariant łączący tanią pulę workerów z niezależnym komitetem modeli doradczych (Model Council).
* **`om-fix-issue`**: Kompleksowy łańcuch naprawy zgłoszenia: od triage, przez reprodukcję, minimalny patch w worktree, po PR.
* **`om-fix-issue-optimized`**: Odchudzony wariant naprawy zgłoszenia przez zoptymalizowanych workerów.
* **`om-fix-issue-multi`**: Wielowątkowa diagnostyka i naprawa złożonych błędów.
* **`om-fix-issue-multi-optimized`**: Zoptymalizowana wielomodelowa naprawa błędów pod nadzorem komitetu audytorów.

### 📁 Grupa F: Inteligentne Testy, Diagnostyka i Ewaluacja (Eval)
* **`om-smart-test`**: Inteligentne mapowanie zmienionego kodu na jednostki testowe. Uruchamia tylko te testy, na które diff miał faktyczny wpływ, skracając pętlę zwrotną.
* **`om-qa-buddy`**: Interaktywny runbook dla testera manualnego, synchronizowany na bieżąco z werdyktami modeli AI i wykrytymi usterkami.
* **`om-auto-qa-scenarios`**: Ekstrakcja scenariuszy testowych (P0/P1/P2) ze scalonych PR-ów do czytelnych raportów Markdown/HTML dla zespołu QA.
* **`om-troubleshooter`**: Zaawansowany moduł diagnostyczny: od symptomu błędu, przez routing w `AGENTS.md`, izolację przyczyny źródłowej, po minimalny patch z testem regresyjnym.
* **`om-judge-agent-session`**: Wzorzec LLM-as-a-judge: ewaluacja przebiegu sesji programistycznej agenta, weryfikacja atestów kontrolera, bramek projektowych i kontraktu stylów.

---

## 🔗 3. INTEGRACJA Z ARCHITEKTURĄ SEJFU OBSIDIAN (KARPATHY LLM WIKI)

Wszystkie nowe umiejętności są zmapowane w relacjach grafowych Sejfu Wiedzy (`sejf_tk`):
- **Węzły źródłowe (`wiki/sources/`)**: Publikacja tego kompendium tworzy stronę `src-aktualizacja-ekosystemu-skilli-open-mercato-v7-1.md`.
- **Węzły pojęciowe (`wiki/concepts/`)**:
  - `[[Multi-Model Harness]]`: orkiestracja zadań pomiędzy wyspecjalizowanymi modelami AI.
  - `[[Synthetic Users]]`: panele syntetycznych person do eksploracji UX i testów decyzyjnych.
  - `[[Smart Testing]]`: ukierunkowane testowanie oparte na mapowaniu diffów.
  - `[[Autonomous Automerge]]`: bezobsługowe kolejkowanie i scalanie PR-ów.
- **Indeks i Dziennik**: Automatyczna rejestracja w `index.md` (sekcja Źródeł) oraz wpis w `log.md`.
