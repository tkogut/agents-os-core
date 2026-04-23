# AGENTS-OS v3.2 Swarm Edition (Ultra+) - Master Manual

**Data Zbudowania Systemu**: Kwiecień 2026
**Architekt**: Antigravity Orchestrator & User tkogut
**Poziom Kompresji**: Caveman Ultra+

---

## 1. Czym jest AGENTS-OS v3.2 Swarm?
AGENTS-OS to rygorystyczny framework konfiguracyjny (Dotfiles) zaprojektowany specjalnie dla ekosystemu **Google Cloud Antigravity** oraz nakładki na terminal **Gemini CLI**. Zmusza modele AI udostępnione przez Google (Gemini, Claude) do pracy w trybie "Swarm" (Rozproszenie Ról) z wykorzystaniem agresywnej optymalizacji użycia tokenów "Caveman Ultra+".

Zapewnia to:
- Maksymalną efektywność kodu.
- Brak halucynacji związanych z przełączaniem kontekstów.
- Szybsze operacje na plikach i doskonałą integralność w terminalu (WSL).

## 2. Inicjalizacja Nowego Projektu (`os-init`)

Stworzyliśmy absolutnie samowystarczalny system. Nie musisz już ręcznie kopiować plików z poprzednich projektów.

### Instalacja systemu na nowym komputerze:
Aby zaaplikować cały ekosystem i stworzyć Złoty Standard od zera, wystarczy pobrać repozytorium i uruchomić skrypt instalacyjny:

```bash
git clone https://github.com/tkogut/agents-os-core.git
cd agents-os-core
bash INSTALL.sh
```

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

## 6. Globalne Umiejętności (Global Skills)
System jest wyposażony domyślnie w "Agentic Skills" dostarczane jako globalne rozszerzenia możliwości Agenta:
- **`swarm-bootstrapper` (os-init)**: Automatyzacja tworzenia środowisk deweloperskich. Agent czyta architekturę systemu, konfiguruje i loguje projekt w pamięci podręcznej.
- **`github-orchestrator`**: Operator Zdalnego Składowania. Możesz napisać: *"github init"* by utworzył chmurę, lub *"zapisz i pushnij"* by od razu skompresował Twoje intencje w commit i je wdrożył. Odpala i czyta także `github actions` bez wychodzenia na stronę WWW.
- **`caveman`**: Redukcja szumu języka naturalnego. Oszczędność tokenów wejściowych o ~75%.

---
Dokument wygenerowany przez Instancję Antigravity w dniu ostatecznej weryfikacji. Zakończono protokół.

<br><hr><br>

# [EN] AGENTS-OS v3.2 Swarm Edition (Ultra+) - Master Manual

**System Build Date**: April 2026
**Architect**: Antigravity Orchestrator & User tkogut
**Compression Level**: Caveman Ultra+

---

## 1. What is AGENTS-OS v3.2 Swarm?
AGENTS-OS is a rigorous configuration framework (Dotfiles) designed specifically for the **Google Cloud Antigravity Ecosystem** and the **Gemini CLI**. It forces Google-provided AI models (Gemini, Claude) to operate in "Swarm" mode (Role Distribution) utilizing aggressive token usage optimization known as "Caveman Ultra+".

This ensures:
- Maximum code efficiency.
- Zero hallucinations related to context switching.
- Faster file operations and pristine terminal integrity (WSL).

## 2. Initializing a New Project (`os-init`)

We have created an absolutely self-sufficient system. You no longer need to manually copy files from previous projects.

### System installation on a new machine:
To apply the entire ecosystem and create the Golden Standard from scratch, just clone the repository and run the installation script:

```bash
git clone https://github.com/tkogut/agents-os-core.git
cd agents-os-core
bash INSTALL.sh
```

### How to create a new project (The Bootstrapper):
Type in the OS terminal:
```bash
os-init my-new-project-name
```

**What will the AI do?**
1. The system will auto-create the directory `/home/tkogut/projects/my-new-project-name`.
2. It will copy the "Golden Standard", aka The Template Vault from `~/.gemini/antigravity/templates/v3.2-swarm/` into it.
3. Initializes an empty GiT repository.
4. Reports back in "ACTIVE" state with the corresponding "State Token".

*(Typing just `os-init` will initialize the architecture in your current working directory).*

---

## 3. The Template Vault (Golden Standard)
When you create a new project, an inviolable hierarchy (Topology) is copied into it. It contains a pristine, clean system state based on proven mechanisms.

**View of the starting folder for a new application:**
```plaintext
/my-new-project-name/
├── AGENTS-OS.md               <-- Supreme Law. Contains Agent operation rules.
├── agents.md                  <-- Roles Registry (Triad) and tasks to offload to Models.
├── task.md                    <-- State Token (You write here what AI should do).
├── design-tokens.md           <-- Empty scratchpad for UI guidelines.
├── execution/                 <-- Runtime files for The Builder.
├── tmp/                       <-- Logs (according to the Command Logging Protocol).
├── .github/                   <-- CI/CD configuration.
└── .agent/                    <-- Agent's Subconscious Memory
    ├── rules/
    │   ├── GOVERNANCE.md      <-- Local Law (Is it Python? Vue? Odoo?)
    │   └── GEMINI.md          <-- Context Guard for Snap.
    ├── plans/                 <-- Templates for long-term deployment plans.
    ├── specs/                 <-- External Knowledge & Graph RAG (graph.json).
    ├── workflows/             <-- Automated instructions for tools.
    └── skills/                <-- Skills (Caveman, NotebookLM Sync, etc.).
```

---

## 4. Models in the System (The Swarm Triad)
The Agent supports 3 operational roles. Depending on the task, it switches work modes:

1. **Coordinator (Management)**
   - Type: Gemini 3.1 Pro
   - Tools: `browser`, `task_boundary`.
   - Access Rule: Works on `plans/`, `tasks.md`. DOES NOT WRITE MAIN CODE IN `/src`. Serves as the construction manager.
2. **Builder (Change Engineering)**
   - Type: Claude 4.6 Thinking
   - Tools: `view_file`, `execution`, terminal.
   - Access Rule: Writes the "atomic armor" of code inside `src/` and `execution/`. Optimizes live.
3. **Auditor (Security & QA)**
   - Type: Gemini 3 Flash
   - Operations: Rapid verification. Z-index, linting, server error reports. Works in fractions of a second using the logging protocol (`/tmp/*.log`). Reports bugs in `caveman-review` mode (one liner).

## 5. Caveman Ultra+ Standard and Snap Sandbox Guard

- **Caveman Ultra+**: All instructions are heavily reduced. The Agent is forbidden from writing fluff ("I'm glad I could help", "Sure, I'd be happy to do that"). Communication with the agent looks like communicating with a military radio sniper. Short, vectorized, to the point.
- **Snap Sandbox Guard**: Your Google Antigravity CLI was installed via `snap`, which means terminal imprisonment. Our `global_antigravity_update.sh` script (and automatically the `GEMINI.md` in new projects) bypasses this via soft links ("Symlinks"). If the structure breaks, just call `Snap Audit` or run the `os-init` command in your IDE. 

## 6. Global Skills Overview
The system comes pre-equipped with "Agentic Skills" layered as global extensions of your Agent's capabilities:
- **`swarm-bootstrapper` (os-init)**: Developer environment setup automation. The Agent reads system architecture, configures paths, and primes the project into sub-memory.
- **`github-orchestrator`**: Remote Storage Operator. You can command: *"github init"* to auto-create the repository in the cloud, or *"auto commit"* to compress intents into conventional commits and push them. It can run and read `github actions` silently in the terminal.
- **`caveman`**: Heavy NLP reduction. Shrinks input token overhead by ~75%.

---
Document generated by the Antigravity Instance on the day of final verification. Protocol complete.
