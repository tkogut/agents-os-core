---
tags: ["#NotebookLM", "#ExpertKnowledge", "#OpenMercato", "#CezarRuntime", "#SwarmTriad"]
date_synced: "2026-08-07"
version: "6.5-Swarm"
status: "STABLE"
---

# 🛸 Specyfikacja Architektoniczna: Integracja Open-Mercato Enterprise Skills & Cezar Runtime (v6.5-Swarm)

> **Źródło wiedzy eksperckiej:** [open-mercato/open-mercato](https://github.com/open-mercato/open-mercato) | [open-mercato/skills](https://github.com/open-mercato/skills)
> **Zastosowanie:** AGENTS-OS v6.5 Enterprise Swarm Platform
> **Status:** `#ExpertKnowledge` `#NotebookLM`

---

## 1. Architektura SDLC i Pipeline Automation (36 Skills Integration)

Inicjalizacja pipeline'u deweloperskiego w dowolnym projekcie odbywa się za pomocą zdarzenia `/om-setup-agent-pipeline`.

```
                  ┌────────────────────────────────────────┐
                  │      /om-setup-agent-pipeline          │
                  └──────────────────┬─────────────────────┘
                                     │
                        ┌────────────┴────────────┐
                        ▼                         ▼
            .ai/agentic.config.json            SDLC.md
             (Gate Commands & Validation)  (Source of Truth)
```

### 1.1 Artefakty Głównodowodzące
- **`.ai/agentic.config.json`**: Definiuje sekwencję komend walidacyjnych CI/CD (lint, typecheck, build, test) oraz limity zasobowe.
- **`SDLC.md`**: Wyznacza cykl życia kodu (Issue -> Branch -> Worktree -> Implementation -> Handshake -> QA Gate -> PR Merge).

### 1.2 Pełna Macierz 36 Skilli Open-Mercato
| Kategoria | Skille | Opis |
| :--- | :--- | :--- |
| **Pipeline Core** | `om-setup-agent-pipeline`, `om-pipeline-retro`, `om-prepare-issue`, `om-auto-manage-issues`, `om-close-fixed-issues` | Scaffolding i automatyczny triaż pipeline'u. |
| **Automatyzacja PR** | `om-auto-create-pr`, `om-auto-create-pr-loop`, `om-auto-continue-pr`, `om-auto-continue-pr-loop`, `om-open-pr`, `om-pr-autopilot` | Wielokrotne i pętlowe tworzenie/wznawianie PR. |
| **Implementacja & Fix** | `om-auto-implement-spec`, `om-auto-fix-issue`, `om-auto-fix-pr`, `om-fix`, `om-root-cause`, `om-apply-upgrade-notes` | Automatyczna zamiana wymagań w kod oraz naprawa błędów. |
| **Weryfikacja & QA** | `om-auto-qa-pr`, `om-auto-review-pr`, `om-code-review`, `om-review-prs`, `om-verify-in-repo`, `om-integration-tests` | Statyczna i dynamiczna kontrola jakości kodu. |
| **UX & Design** | `om-ux-shape`, `om-ux-setup`, `om-ux-review-pr` | Scaffolding i audyt interfejsów użytkownika. |
| **Governance & Merge** | `om-approve-merge-pr`, `om-merge-buddy`, `om-check-and-commit`, `om-auto-update-changelog`, `om-followup-issue-from-pr` | Kontrola scalania PR, commitowanie i Changelog. |
| **Planowanie & Wymagania** | `om-brainstorm`, `om-spec-writing`, `om-auto-write-spec`, `om-prepare-test-env`, `om-create-skill` | Tworzenie specyfikacji i nowych umiejętności. |

### 1.3 Protokół Pracy Buildera (Claude)
- **Wielostopniowy cykl:** Wymuszona sekwencja `[PLAN -> HANDOFF -> NOTIFY]`.
- **Atomic Commits:** Każdą zrealizowaną jednostkę operacyjną zamyka pojedynczy, czysty commit w Git Worktree.

---

## 2. Cezar Runtime & Fault Tolerance (Zero-Loss State Engine)

Cezar Runtime to wysokowydajnościowa warstwa wykonawcza dla agentów, dbająca o odporność na awarie i optymalizację pamięci.

```
┌────────────────────────────────────────────────────────────────────────┐
│                          CEZAR RUNTIME ENGINE                          │
├──────────────────────────┬──────────────────────────┬──────────────────┤
│ Queue & RAM Allocation   │ Heartbeat & State Dump   │ Auto Recovery    │
│ Max 10GB RAM / Instance  │ Cyclical HANDOFF.md Dump │ om-auto-continue │
└──────────────────────────┴──────────────────────────┴──────────────────┘
```

### 2.1 Zarządzanie Zasobami i Alokacja RAM
- **Twardy Limit Alokacji:** Maksymalnie **10GB RAM** per instancja agenta.
- **Menedżer Kolejek (Queue Manager):** Izolacja zasobowa zapobiegająca wyczerpaniu pamięci (OOM) przy równoległych sesjach subagentów.

### 2.2 Fault Tolerance (Bezstratne Wznawianie)
- **Heartbeat Protocol:** Co 30 sekund system rejestruje stan wątku w pamięci podręcznej.
- **`HANDOFF.md` State Dump:** Stan realizacji (ukończone pliki, pozostałe kroki, kontekst sesji) jest cyklicznie zrzucany do pliku `HANDOFF.md` w katalogu projektu/worktree.
- **Asynchroniczny Recovery:** W przypadku awarii węzła lub przekroczenia limitu czasu API, proces jest przywracany bez utraty danych za pomocą komend `om-auto-continue-pr` lub `om-auto-continue-pr-loop`.

---

## 3. Task Router i Izolacja Kontekstu (Anti-Context Bloat)

Dla zapobieżenia przepełnieniu okna kontekstowego LLM (Context Bloat), główny plik `AGENTS.md` pełni wyłącznie funkcję Dyspozytora (Router/Dispatcher).

```
                            ┌────────────────┐
                            │   AGENTS.md    │
                            │ (Task Router)  │
                            └───────┬────────┘
                                    │ Match Task Pattern
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
   agents-custom-fields.md      agents-ui.md          agents-api.md
```

### 3.1 Dyspozytornia Zadań (Task Router Matrix)
Przed rozpoczęciem analizy lub kodowania, Agent dopasowuje zadanie do poniższej macierzy i wczytuje wyłącznie pasujące moduły wiedzy:

| Kontekst Zadania | Wyznaczony Moduł Dokumentacji |
| :--- | :--- |
| **Architektura & Scaffolding** | `core` + `.ai/docs/module-development.md` |
| **Interfejs Użytkownika & Design System** | `agents-ui.md` + `packages/ui/AGENTS.md` |
| **Pola Niestandardowe & Modele Danych** | `agents-custom-fields.md` + `core` → Custom Fields |
| **API & Integracje Zewnętrzne** | `agents-api.md` + `core` → API Routes |
| **Testowanie & QA Gate** | `CODE_REVIEW.md` + `om-auto-qa-pr` |

---

## 4. Brama Jakości (QA Gate) & Visual Proof-of-Work

Każda zmiana w kodzie przechodzi przez dwustopniową bramę weryfikacyjną.

```
[Builder Commit] ──► [PR tagged 'needs-qa'] ──► [Visual PoW & Browser Screenshot] ──► [qa-approved tag] ──► [Merge]
```

### 4.1 Hard Lock Policy
- Pull Request automatycznie otrzymuje etykietę `needs-qa`.
- Automatyczny merge jest zablokowany (Hard Lock).
- Scalenie kodu do gałęzi `main`/`master` wymaga ręcznej lub audytorskiej weryfikacji i zdjęcia blokady flagą `qa-approved`.

### 4.2 Visual Proof-of-Work & Browser Verification
- **Generowanie Makiet:** Każda zmiana w interfejsie użytkownika (UI/Frontend) wymaga wygenerowania funkcjonalnej makiety w formacie HTML/React.
- **Automatyczny Screenshot:** System wywołuje integrację `browser-provider`, renderuje makietę w przeglądarce bezgłowej (headless CDP), wykonuje zrzuty ekranu i dołącza je bezpośrednio do opisu Pull Requesta jako niepodważalny dowód wdrożenia (Visual Proof-of-Work).

---

## 5. Moduł Ewaluatora (Cost Optimization & Model Down-Scaling)

Moduł Ewaluatora służy do ciągłej optymalizacji kosztów wywołań LLM oraz walidacji stabilności promptów.

### 5.1 System Benchmarkingowy (`evaluator.json`)
- Zestaw standaryzowanych przypadeków testowych (Use-Cases).
- Automatyczne wywoływanie promptów systemowych na zadaniach wzorcowych i pomiar wskaźników:
  - **Accuracy Pass Rate (%)**
  - **Token Consumption**
  - **Latency (ms)**

### 5.2 Strategia Down-Scaling
Gdy nowa funkcja uzyskuje stabilność na modelach klasy Flagship (np. Claude Sonnet / Gemini Pro), Ewaluator testuje i przesuwa wykonanie na tańsze i szybsze modele (np. Gemini Flash / Flash-Lite), zachowując 100% zgodności logiki biznesowej.

---

## 6. Swarm Triad (Restrykcyjny Podział Ról)

```
       ┌─────────────────────────────────────────────────────────┐
       │                     SWARM TRIAD                         │
       ├───────────────────┬───────────────────┬─────────────────┤
       │    COORDINATOR    │      BUILDER      │     AUDITOR     │
       │    (Gemini-High)  │     (Claude)      │  (Gemini-Low)   │
       │ Strategia i Plan  │ Kod w Worktree    │ Static QA & Logs│
       │ ZAKAZ KODOWANIA   │ Zero-Leak Policy  │ Brama QA Gate   │
       └───────────────────┴───────────────────┴─────────────────┘
```

1. **Coordinator (Gemini High):** Tworzy architekturę i zarządza `task.md`. Obowiązuje go **całkowity zakaz bezpośredniej modyfikacji kodu źródłowego**.
2. **Builder (Claude Sonnet/Thinking):** Wykonuje operacje w izolowanych Git Worktrees. Zabezpieczony regułą `R-SEC-01` (Zero-Leak Policy).
3. **Auditor (Gemini Low):** Weryfikuje logi `*_handshake.json`, uruchamia skrypty linterów (`brooks-lint`, `validate-handshakes.py`) i nakłada/zdejmuje etykiety bramki QA.

---

#NotebookLM #ExpertKnowledge