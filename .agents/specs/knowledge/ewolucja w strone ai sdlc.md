---
tags: ["#NotebookLM", "#ExpertKnowledge", "#OpenMercato", "#CezarRuntime", "#SwarmTriad", "#AISDLC"]
date_synced: "2026-09-19"
version: "6.5-Swarm"
status: "STABLE"
---

# 🛸 Raport Techniczny: Ewolucja w stronę AI SDLC, Ekosystem Open Mercato i Orkiestrator Cezar (v6.5-Swarm)

> **Źródło wiedzy eksperckiej:** NotebookLM — [.agents/row_notes/ewolucja w stronę AI SDLC.md](file:///home/tkogut/projects/agents-os-core/.agents/row_notes/ewolucja%20w%20stron%C4%99%20AI%20SDLC.md)
> **Zastosowanie:** AGENTS-OS v6.5 Enterprise Swarm Platform
> **Status:** `#ExpertKnowledge` `#NotebookLM`

---

## 1. Wprowadzenie: Ewolucja w stronę AI SDLC

Współczesna inżynieria oprogramowania przechodzi paradygmatyczne przesunięcie: od tradycyjnego modelu SDLC, gdzie postęp blokowany jest przez ludzkich „gatekeeperów”, ku **AI SDLC** (*Autonomous Agentic Software Development Life Cycle*).

W tym nowym modelu pełny kontekst techniczny i biznesowy rezyduje bezpośrednio w repozytorium, eliminując wąskie gardła decyzyjne.

```
                      ┌─────────────────────────────────┐
                      │    Task-Driven Context Routing  │
                      └────────────────┬────────────────┘
                                       │
                 ┌─────────────────────┴─────────────────────┐
                 ▼                                           ▼
       Akumulacja Wiedzy w Repo                     Izolacja Zadań
     (Compounding Effect — Zero Loss)            (Anti-Hallucination & Slop)
```

### 1.1 Kluczowe Mechanizmy Architektoniczne
- **Task-Driven Context Routing**: Inteligentne filtrowanie wiedzy tak, by agenci nie ulegali „halucynacjom nadmiaru” w dużych systemach.
- **Efekt procentu składanego (*Compounding Effect*)**: Wiedza akumulowana w repozytorium nie ulatuje wraz z końcem sesji, lecz zasila każdą kolejną iterację, drastycznie skracając czas dowożenia funkcjonalności.
- **Context Engineering jako Firewall**: Jedyna skuteczna zapora przed degradacją jakości kodu (*AI slop*) przy długofalowej pracy agentycznej.

### 1.2 Triada Pojedynczego Źródła Prawdy (SSOT)
Fundamenty porządku repozytorium definiują trzy kluczowe pliki:

| Plik | Rola w Ekosystemie | Funkcja Strategiczna |
| :--- | :--- | :--- |
| **`AGENTS.md`** | Task Routing | Mapa aktywnych standardów i routingu zadań; zapobiega przeciążeniu kontekstu. |
| **`SDLC.md`** | Governance | Definicja procesów, bram kontrolnych QA i reguł Definition of Ready (DoR). |
| **`.ai/agentic.config.json`** | Pipeline Config | Parametry techniczne: stack technologiczny, komendy walidacyjne i taksonomia labelek. |

---

## 2. Ekosystem Open Mercato Skills: Modularna Inteligencja Agentów

Ekosystem Open Mercato to zestaw ponad **41 bazowych narzędzi**, rozszerzalny o ponad **1400 skilli społecznościowych** (rejestr `sickn33/awesome-skills`). System automatyzuje pełny cykl życia Pull Requesta, zapewniając spójność nawet w repozytoriach przekraczających 1.2 mln linii kodu. Skille są całkowicie niezależne od tech-stacku dzięki parametryzacji w `.ai/agentic.config.json`.

### 2.1 Konwencje Nazewnictwa i Strategia Pracy
Architektura wymusza rygorystyczny podział na dwie kategorie:

- **`om-auto-*` (Skille autonomiczne i nieinteraktywne)**:
  - Pracują wyłącznie w izolowanych Git Worktrees (`tmp/worktrees/`).
  - Podejmują samodzielnie najbardziej odwracalne decyzje.
  - Wykorzystują mechanizm blokad (etykiety `in-progress`), aby równolegle działające agenty nie kolidowały ze sobą.
- **`om-*` (Skille interaktywne)**:
  - Przykłady: `/om-brainstorm`, `/om-spec-writing`.
  - Wymagają dialogu i decyzji człowieka w punktach krytycznych dla wizji produktu.
- **Klasyfikacja Ryzyka Operacyjnego**:
  - Skille operujące na przeglądarce (np. `/om-auto-qa-pr`) są klasyfikowane jako *Medium/High Risk*. Wymagają bezpiecznych, efemerycznych środowisk uruchomieniowych.

### 2.2 Mapowanie Faz Pipeline'u

```
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│ Discovery & Spec        │ ──> │ Implementation & Repair │ ──> │ Review, QA & Release    │
├─────────────────────────┤     ├─────────────────────────┤     ├─────────────────────────┤
│ • om-discover           │     │ • om-auto-create-pr     │     │ • om-auto-review-pr     │
│ • om-synthetic-users    │     │ • om-auto-implement-spec│     │ • om-auto-fix-pr (CI)   │
│ • om-backlog            │     │ • om-root-cause / fix   │     │ • om-approve-merge-pr   │
└─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘
```

### 2.3 Mechanizmy Rozszerzalności
- **Repo-local override (`.ai/skills/`)**: Lokalne instrukcje nadpisują zachowania globalne bez konieczności forkowania biblioteki.
- **Abstrakcja Providerów**:
  - Deskryptory trackerów (`.ai/trackers/`): GitHub, Linear, Jira.
  - Deskryptory przeglądarek (`.ai/browsers/`): Agent-Browser, Playwright.

---

## 3. Harness i Orkiestrator Cezar: Zarządzanie Równoległą Flotą Agentów

Orkiestrator Cezar to silnik zmieniający interakcję z agentami z synchronicznej na w pełni asynchroniczną (**„Fire and forget”**). Deweloper zleca zadanie i może zamknąć środowisko robocze, podczas gdy Cezar na serwerze (np. VPS) przetwarza zadania 24/7 przy użyciu modeli Claude, Codex czy OpenCode.

### 3.1 Architektura „No Database” i Funkcja „Variants”
- **Brak Bazy Danych**: Cały stan, logi wykonania i kolejki są zapisywane jako zwykłe pliki w `.ai/cezar/`, co gwarantuje pełną audytowalność, zerową podatność i bezproblemowy backup w Gicie.
- **Mechanizm Variants**: Pozwala na jednoczesne, równoległe uruchomienie tego samego zadania ($x2$ lub $x3$) na różnych modelach LLM. Umożliwia deweloperowi wybór najbardziej optymalnego diffu przed scaleniem.

### 3.2 Automatyzacja Workflow (YAML)
Przepływy w `.ai/cezar/workflows/` umożliwiają sekwencyjne łączenie skilli z rygorystycznymi pętlami samonaprawy:

```yaml
steps:
  - id: implementation
    skill: om-auto-create-pr
  - id: validation
    command: "npm test"
    onFail:
      retry: implementation
      max: 3 # Zabezpieczenie przed pętlą i spalaniem tokenów
```

### 3.3 Zarządzanie Zasobami i Runtime
- **Środowisko**: Wymaga Node.js 20+, może być nadzorowane przez proces systemd.
- **Cockpit UI**: Umożliwia monitorowanie limitów zasobów (limit wątków, cap 10 GB RAM per instancja) oraz śledzenie kosztów tokenów w czasie rzeczywistym.

---

## 4. Integracja z Architekturą AGENTS-OS (v6.5 Swarm Edition)

W ekosystemie AGENTS-OS v6.5 pełni rolę **„Systemu Operacyjnego dla agentów”**, podczas gdy Open Mercato dostarcza modularnych **„aplikacji/skilli”** w przestrzeni użytkownika.

### 4.1 Role w Architekturze Swarm Triad (Fail-Closed)
- **COORDINATOR**: Zarządza backlogiem `task.md`, inicjuje `/grill-me`, planuje routing zadań i context window.
- **BUILDER**: Operuje wyłącznie w izolacji `tmp/worktrees/`, realizując zmiany kodu i komitując przez `om-auto-create-pr`.
- **AUDITOR**: Weryfikuje bramki QA/Validation Gate, sprawdza kontrakty i podpisuje `.agents/swarm/*_handshake.json`.

> Plik `task.md` jest prowadzony w reżimie **append-only**, co jest kluczowe dla zachowania spójności w rozproszonym roju maszyn bez mechanizmów blokowania plików (*lock-free*).

### 4.2 Synchronizacja Rozproszona i Protokół Pamięci
- **Konfiguracja Gita**: `merge=union` w `.gitattributes` dedykowany dla plików czysto append-only (`.agents/MEMORY.md`).
- **Model Dwuwarstwowy Skilli**: Fizyczne skille w `.agents/skills/` linkowane symbolicznie do `.claude/skills/` (lub odpowiedników w innych IDE).
- **Protokół `/grill-me`**: Pełni rolę *Pre-Flight Architectural Interview*. Wymusza mechanizm **State-Dump** (zrzut i synchronizację pamięci do `MEMORY.md`) przed i po każdej sesji pracy agenta.

---

## 5. Playbook Wdrożeniowy: Instrukcja Krok po Kroku

Poniższy standard operacyjny umożliwia wdrożenie systemu w modelach *Green Field* oraz *Brown Field*:

### 5.1 Inicjalizacja i Aktualizacja
1. **Instalacja**: `npx skills add open-mercato/skills`
2. **Konfiguracja**: `/om-setup-agent-pipeline` — automatyczna inspekcja repozytorium, konfiguracja `.ai/agentic.config.json` oraz wygenerowanie DoR w `SDLC.md`.
3. **Migracja i Konsolidacja**: Po każdej aktualizacji biblioteki skilli bezwzględnie uruchom `/om-apply-upgrade-notes`. Jest to krytyczny krok, bez którego migracje konfiguracyjne i deskryptory nie zostaną zaktualizowane.

### 5.2 Kluczowy Łańcuch Operacyjny (Production Loop)
1. `/grill-me` — pre-flight review, weryfikacja architektury i synchronizacja stanu (`MEMORY.md`).
2. `/om-auto-fix-issue` — triaż, wyszukanie przyczyny źródłowej (`om-root-cause`) oraz minimalna implementacja (`om-fix`).
3. `/om-pr-autopilot` — pełna stabilizacja CI, auto-review loop, QA gate i dociągnięcie PR do stanu *Merge-Ready*.
4. `/om-apply-upgrade-notes` — utrzymanie higieny repozytorium i pipeline'u po zmianach.

---

## 6. Podsumowanie Architektoniczne

Wdrożenie AI SDLC z AGENTS-OS i Open Mercato transformuje rolę programisty: **z twórcy pojedynczych linii kodu staje się on architektem, operatorem i audytorem procesów agentowych**, zarządzającym autonomiczną fabryką oprogramowania o najwyższym rygorze technicznym i matematycznej weryfikowalności handshakes.
