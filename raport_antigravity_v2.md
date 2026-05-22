# Raport z analizy kodu aplikacji setupu środowiska Antigravity

## 1. Analiza obecnej architektury instalacyjnej (AGENTS-OS v3.2 Swarm)

Aplikacja składa się z trzech głównych komponentów odpowiedzialnych za inicjalizację i instalację systemu Antigravity:

1. **Skrypt `INSTALL.sh` (Uniwersalny Instalator)**:
   - Zarządza instalacją pakietów zewnętrznych takich jak `snapd`, `gemini-cli` i `gh` za pomocą menedżera `snap`.
   - Zajmuje się integracją wtyczki Caveman (`https://github.com/JuliusBrussee/caveman`).
   - Dokonuje deploymentu "Złotego Standardu" (The Template Vault) oraz globalnych umiejętności (skilli) do docelowych ścieżek instalacji `~/.gemini/antigravity/`.
   - Posiada zaimplementowany mechanizm "Snap Sandbox Guard", naprawiający izolację poprzez dowiązania symboliczne.

2. **Skrypt inicjalizujący `os-init`**:
   - Stanowi prosty Bash-owy wrapper wykonujący główny skrypt napisany w języku Python (`bootstrap.py`), zlokalizowany w katalogu umiejętności `swarm-bootstrapper`.

3. **Skrypt `bootstrap.py` (Silnik Bootstrappera)**:
   - Główny punkt startowy dla tworzenia nowych projektów z możliwością specyfikacji niestandardowych katalogów (wymusza ścieżkę w katalogu `~/projects/`).
   - Wbudowane mechanizmy bezpieczeństwa: blokowanie inicjalizacji bezpośrednio w katalogu domowym usera.
   - Automatyzuje procesy poboczne: autoryzację `gh cli`, inicjalizację i konfigurację nowej instancji Git wraz z wygenerowaniem pliku `.gitignore`.
   - Sprawdza istnienie wtyczek frameworka z katalogów uwięzionego Snap.

### Kontekst nowej wersji:
Kod wykazuje rygorystyczne trzymanie się zasad zadeklarowanych w manifestach (np. The Swarm Triad, Caveman Ultra+). Niemniej instalator opiera się mocno na dystrybucji `snap`, co ogranicza ewentualny port środowiska Antigravity 2.0 na inne systemy, takie jak macOS. System "Role Distribution" i "Command Logging Protocol" jest oparty o sztywne szablony, więc ewentualna ewolucja z "AGENTS-OS v3.2" do wymogów "Antigravity 2.0" wymagałaby zwiększenia dynamizmu tych procesów.

## 2. Ocena potencjalnych modyfikacji (Rekomendacje)

- **Wsparcie Multi-Platform**: Skrypt `INSTALL.sh` używa wywołań specyficznych dla systemów Linux (szczególnie Debian/Ubuntu: `apt`). Do migracji należy rozważyć paczkowanie do kontenera z obsługą menedżera `brew` na macOS lub implementację instalatora w całości poprzez Python.
- **Dynamiczny Bootstrapping**: `bootstrap.py` wykorzystuje polecenia systemowe (`subprocess.run`). Lepszym sposobem byłaby implementacja SDK Git i GitHub za pomocą natywnych rozwiązań Python API (np. `PyGithub`, `GitPython`), ułatwiająca obsługę błędów.
- **Konfiguracja Środowiska Agenta**: Przejście z czystego Markdown do sformalizowanych, lżejszych plików typu YAML do mapowania ról w `.agent/agents.md`.

---

## 3. Prompt Modyfikujący dla Asystenta Antigravity

Poniżej przygotowany jest prompt operacyjny zgodny z kompresją "Caveman Ultra+" i protokołami opisanymi w dokumentacji `AGENTS-OS.md`, przeznaczony dla roli **Coordinator**:

```text
[INIT-TOKEN]
ROLE: Coordinator
MODE: Caveman Ultra+
TRACK: Alpha

ACTION: Modify antigravity setup logic for version 2.0.

TASKS:
1. UPDATE `INSTALL.sh`:
   - Replace strict `apt/snap` dependencies with dynamic OS detection (Linux/macOS).
   - Add Homebrew fallback logic.
   - Refactor Snap Sandbox Guard for v2.0 flexibility.

2. UPDATE `bootstrap.py`:
   - Implement `GitPython` and `PyGithub` instead of shell `subprocess`.
   - Inject v2.0 Graph RAG topology generation to `.agent/specs/graph.json`.
   - Update state token template to `AG-V2.0-TOKEN`.

EXECUTION:
- Delegate implementation to Builder.
- Generate unified Z-Index/Path reports.
- Wait for Auditor check: "Math-Consistency checked".
```
