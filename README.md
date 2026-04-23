# AGENTS-OS v3.2 Swarm Edition (Ultra+) - Master Manual

**Data Zbudowania Systemu**: Kwiecień 2026
**Architekt**: Antigravity Orchestrator & User tkogut
**Poziom Kompresji**: Caveman Ultra+

---

## 1. Czym jest AGENTS-OS v3.2 Swarm?
AGENTS-OS to rygorystyczny framework konfiguracyjny zmuszający modele AI udostępnione przez Google (Gemini, Claude) do pracy w trybie "Swarm" (Rozproszenie Ról) z wykorzystaniem agresywnej optymalizacji użycia tokenów "Caveman Ultra+".

Zapewnia to:
- Maksymalną efektywność kodu.
- Brak halucynacji związanych z przełączaniem kontekstów.
- Szybsze operacje na plikach i doskonałą integralność w terminalu (WSL).

## 2. Inicjalizacja Nowego Projektu (`os-init`)

Stworzyliśmy absolutnie samowystarczalny system. Nie musisz już ręcznie kopiować plików z poprzednich projektów.

### Jak utworzyć nowy projekt (The Bootstrapper):
Wpisz w terminalu OS:
```bash
os-init nazwa-mojego-projektu
```

**Co zrobi sztuczna inteligencja?**
1. System sam utworzy folder `/home/tkogut/projects/nazwa-mojego-projektu`.
2. Skopiuje do niego "Złoty Standard" tzw. The Template Vault z rezerwuaru `~/.gemini/antigravity/templates/v3.2-swarm/`.
3. Zainicjalizuje puste repozytorium GiT.
4. Zgłosi się w trybie "ACTIVE" z odpowiednim "State Token".

*(Jeśli wpiszesz samo `os-init`, zainicjuje to architekturę w folderze, w którym obecnie jesteś).*

---

## 3. The Template Vault (Złoty Standard)
Kiedy tworzysz nowy projekt, kopiowana jest do niego nienaruszalna hierarchia (Topologia).
Zawiera ona pusty, czysty stan systemu oparty o sprawdzone mechanizmy.

**Widok folderu startowego nowej aplikacji:**
```plaintext
/nazwa-mojego-projektu/
├── AGENTS-OS.md               <-- Prawo Nadrzędne. Zawiera zasady działania Agenta.
├── agents.md                  <-- Rejestr Ról (Triad) i zadania do przekazania Modelom.
├── task.md                    <-- State Token (Tutaj zapisujesz co AI ma zrobić).
├── design-tokens.md           <-- Pusty brudnopis dla wytycznych UI.
├── execution/                 <-- Pliki uruchomieniowe The Buildera.
├── tmp/                       <-- Logi (zgodnie z protokołem Command Logging Protocol).
├── .github/                   <-- Konfiguracja CI/CD.
└── .agent/                    <-- Pamięć Podświadoma Agenta
    ├── rules/
    │   ├── GOVERNANCE.md      <-- Prawo Lokalne (Czy to Python? Czy Vue? Odoo?)
    │   └── GEMINI.md          <-- Context Guard dla Snapa.
    ├── plans/                 <-- Szablony długoterminowych planów wdrożen.
    ├── specs/                 <-- Wiedza Zewnętrzna i Graph RAG (grapg.json).
    ├── workflows/             <-- Zautomatyzowane instrukcje dla narzędzi.
    └── skills/                <-- Umiejętności (Caveman, NotebookLM Sync, itp.).
```

---

## 4. Modele w Systemie (The Swarm Triad)
Agent obsługuje 3 role operacyjne. W zależności od zadania, zmienia tryb pracy:

1. **Coordinator (Zarządzanie)**
   - Typ: Gemini 3.1 Pro
   - Narzędzia: `browser`, `task_boundary`.
   - Zasada dostępu: Pracuje na `plans/`, `tasks.md`. NIE PISZE KODU GŁÓWNEGO W `/src`. Jest kierownikiem budowy.
2. **Builder (Inżynieria Zmian)**
   - Typ: Claude 4.6 Thinking
   - Narzędzia: `view_file`, `execution`, terminal.
   - Zasada dostępu: Pisze "atomiowy pancerz" kodu wewnątrz `src/` oraz `execution/`. Optymalizuje na żywo.
3. **Auditor (Zabezpieczenie & QA)**
   - Typ: Gemini 3 Flash
   - Operacje: Szybka weryfikacja. Z-index, linting, raporty z błędów serwera. Pracuje w ułamkach sekund przez protokół logowania (`/tmp/*.log`). Zgłasza błędy w trybie `caveman-review` (jedna linijka).

## 5. Standard Caveman Ultra+ i Snap Sandbox Guard

- **Caveman Ultra+**: Wszystkie instrukcje są zredukowane. Agent ma zakaz pisania bzdur ("Cieszę się, że mogłem pomóc", "Jasne, chętnie to zrobię"). Komunikacja z agentem wygląda jak komunikacja z wojskowym snajperem radiowym. Krótko, wektor, na temat.
- **Snap Sandbox Guard**: Twoje CLI Google Antigravity zostało zainstalowane przez `snap`, a to oznacza uwięzienie terminala. Stworzony przez nas skrypt `global_antigravity_update.sh` (oraz z automatu w nowym projekcie `GEMINI.md`) radzi sobie z tym przez miękkie dowiązania ("Symlinks"). Jeśli struktura się stłucze, wystarczy wezwać `Aduyt Snapa` albo uruchomić w IDE komendę `os-init`. 

---
Dokument wygenerowany przez Instancję Antigravity w dniu ostatecznej weryfikacji. Zakończono protokół.
