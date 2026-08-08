1. Architektura Orkiestracji i Skala Enterprise (Open Mercato Context)
Wymiary projektu: Analiza skali systemu (~800 tys. linii kodu ERP, zero linii kodu napisanych ręcznie, ponad 1700 zmergowanych PR-ów, tygodniowy cykl wydań)
.
Przejście na AI-SDLC: Ewolucja od chaotycznego programowania ("Yolo Mode") do ustrukturyzowanej inżynierii oprogramowania sterowanej przez agentów
.
2. Budowa i Anatomia AGENTS.md oraz Wzorzec "Task Router" 🌟 (Główny punkt raportu)
Problem przeładowania kontekstu (Context Congestion): Dlaczego standardowy, pojedynczy plik instrukcji dla agentów przestaje działać w projektach o skali enterprise i powoduje dryfowanie oraz halucynacje modeli przy długich sesjach
.
Mechanizm Task Routera: Jak starter AGENTS.md (generowany przez setup pipeline)
 wykorzystuje uproszczoną tabelę przekierowań Markdown do dynamicznego dzielenia instrukcji
.
Routing dziedzinowy: Analiza podziału na wyspecjalizowane pliki (np. dedykowany plik dla pól niestandardowych agents-custom-fields.md), co drastycznie oszczędza okno kontekstowe LLM, podnosi precyzję wykonywania zadań i redukuje zużycie tokenów
.
3. Ekosystem Skills – Narzędzia Autonomiczne vs Interaktywne
Inicjalizacja i konfiguracja: Rola pliku .ai/agentic.config.json oraz generatora SDLC.md jako dokumentacji przepływu zadań
.
Autonomiczne potoki deweloperskie (om-auto-*):
Triaż błędów i automatyczna naprawa (om-auto-fix-issue)
.
Wdrażanie kodu faza po fazie w izolowanych Git Worktrees z checkpointami (om-auto-create-pr, om-auto-create-pr-loop z mechanizmem PLAN/HANDOFF/NOTIFY)
.
Automatyczne wznawianie przerwanych prac (om-auto-continue-pr i om-auto-continue-pr-loop)
.
Narzędzia interaktywne i rozszerzalność: Dostosowywanie procesów lokalnych bez modyfikacji rdzenia platformy poprzez nadpisywanie plików .ai/skills/<skill-name>/SKILL.md
.
4. Środowisko Uruchomieniowe Cezar – Wielowątkowość i Odporność
Równoległa egzekucja zadań: Zarządzanie wieloma wątkami agentów deweloperskich jednocześnie z poziomu interfejsu Cezara
.
Kolejkowanie i limity zasobów: Zabezpieczenie przed wyciekami i nadmiernym zużyciem pamięci RAM (np. żonglowanie limitami rzędu 10 GB RAM)
.
Odporność na awarie (Fault Tolerance): Wykorzystanie cyklicznego zapisu stanu w pliku HANDOFF.md do bezproblemowego wznawiania sesji po restartach serwera lub zamknięciu laptopa
.
5. Strategia Zapewnienia Jakości (QA Gate) i Wizualna Pętla Zwrotna
Bezwzględna bramka jakościowa: Zasada, zgodnie z którą PR oznaczony etykietą needs-qa nie może zostać scalony do gałęzi głównej bez manualnego zatwierdzenia przez człowieka (qa-approved)
.
Automatyzacja QA i Mockupy:
Jak skille automatycznie uruchamiają aplikację w przeglądarce i generują raporty z testów (om-auto-qa-pr, om-prepare-test-env)
.
Automatyczne generowanie klikalnych makiet w React/HTML oraz dołączanie zrzutów ekranu "przed/po" jako dowodu w Pull Requestach
.
Siatka bezpieczeństwa CI: Integracja tysięcy testów jednostkowych i integracyjnych jako twardy warunek dopuszczenia kodu wygenerowanego przez AI
.
6. Optymalizacja Kosztów i Suwerenność Cyfrowa
Ewaluator promptów: System testowania bazy instrukcji (harness) na zestawie ponad 200 przypadków użycia w celu optymalizacji zachowania promptów pod tańsze, słabsze modele (optymalizacja "w dół", np. pod Claude 3.5 Sonnet zamiast Opusa)
.
Zarządzanie modelami i bezpieczeństwem danych: Wykorzystanie hostów typu Open Router z polityką Zero Data Retention (ZDR) do bezpiecznej pracy z kodem enterprise
.
7. Środowisko Deweloperskie: Sandboxy
Bypass barier IT: Maszyny wirtualne dostarczane w chmurze z pełnym zestawem narzędzi (Cezar, terminal, edytor), eliminujące miesięczne procesy akceptacji bezpieczeństwa w korporacjach