# Specyfikacja Integracji Architektury Open-Mercato z Swarm Triad

**Wersja:** 1.0.0  
**Projekt:** mms4tk + Hermes Agent Swarm  
**Status:** Zatwierdzona Specyfikacja Architektoniczna  

---

## 1. Wstęp i Cel Architektoniczny

Dokument ten opisuje wzorzec integracji architektury klasy Enterprise (Open-Mercato) z natywnym triadycznym modelem agentowym (Swarm Triad: Coordinator, Builder, Auditor).

Celem jest zapewnienie:
1. **Pełnej separacji ról**: Rozdzielenie planowania i devops (Coordinator), implementacji (Builder) oraz audytu bezpieczeństwa i jakości (Auditor).
2. **Niezawodności w pętli handlowej**: Bezpośrednie połączenie taktycznego silnika M15 z ze strategiczną inteligencją Hermes Agent (H4/D1).
3. **Persystencji i Fault-Tolerance**: Odporność na restarty kontenerów dzięki persystencji SQLite (`logs.db`, `kanban.db`) oraz wolumenom Docker.

---

## 2. Podział Odpowiedzialności (Swarm Triad)

| Rola | Uprawnienia | Dostęp do plików | Zadania |
| :--- | :--- | :--- | :--- |
| **Coordinator** | DevOps, Git Push, Plan Management | `.agents/plans/`, `.env` | Orkiestracja zadań, merge branchy, push produkcyjny |
| **Builder** | Kodowanie w odizolowanym Worktree | `src/`, `tests/`, `scripts/` | Atomowa implementacja funkcji, pisanie testów |
| **Auditor** | Read-Only Audit & QA Gate | Całe repozytorium (odczyt) | Weryfikacja R-SEC-01, linter, testy `52/52 PASSED` |

---

## 3. Integracja dwupoziomowa (Tactical vs Strategic)

### Taktyczna Warstwa Wykonawcza (M15)
- Działa w kontenerze `antigravity_core`.
- Odczytuje zamknięte świece M15 (`candles[:-1]`).
- Wylicza wstęgi TMA i ATR.
- Zarządza dźwignią (`BASE_MODE` x1.0 vs `SCOUT_MODE` x0.1).

### Strategiczna Warstwa Nadzorcza (Hermes H4/D1)
- Działa w kontenerze `hermes-agent`.
- Odczytuje wyższe interwały i ustawia `StrategyProfile` (`directional_bias`).
- Obsługuje zadania Cron (`mms4tk_event_dispatcher`, `mms4tk_h4_analysis`, `mms4tk_d1_atr_check`).
- Przekazuje trudne oceny świec do interfejsu **Human-in-the-Loop (HITL)**.
