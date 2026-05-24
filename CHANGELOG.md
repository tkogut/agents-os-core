# 🛸 Historia Zmian / Changelog — AGENTS-OS v4.1 (Universal Swarm)

Wszystkie zmiany w tej wersji są bezpośrednią odpowiedzią na audyt przenaszalności systemu zawarty w [AGENTS-OS_Evaluation_Report.md](file:///home/tkogut/projects/agents-os-core/AGENTS-OS_Evaluation_Report.md).

---

## [4.1.1] - 2026-05-24

### 🚀 Poprawki i Automatyzacja (Portability & Automation)

* **Instalacja wtyczki Caveman przez URL**:
  * Zmieniono cel instalacji wtyczki `caveman` w [INSTALL.sh](file:///home/tkogut/projects/agents-os-core/INSTALL.sh) na bezpośredni link GitHub (`https://github.com/juliusbrussee/caveman`). Rozwiązuje to błąd instalacji lokalnej.
* **Automatyczne czyszczenie starych szablonów**:
  * Dodano moduł czyszczący w [INSTALL.sh](file:///home/tkogut/projects/agents-os-core/INSTALL.sh), usuwający stare wersje szablonów (np. `v4.0-swarm`) przed kopiowaniem nowych.
* **Automatyczny test E2E**:
  * Utworzono skrypt testowy [test_bootstrap.sh](file:///home/tkogut/projects/agents-os-core/execution/test_bootstrap.sh) weryfikujący tworzenie projektów, strukturę Złotego Standardu, repozytorium git i push na GitHub.

---

## [4.1.0] - 2026-05-24

### 🚀 Nowości i Ulepszenia Przenaszalności (Portability)

* **Dynamiczny odczyt nazwy użytkownika GitHub (Fix 3.1)**:
  * Zastąpiono zahardkodowaną nazwę użytkownika `tkogut` w skrypcie [bootstrap.py](file:///home/tkogut/projects/agents-os-core/global_skills/swarm-bootstrapper/scripts/bootstrap.py) oraz [os-init](file:///home/tkogut/projects/agents-os-core/os-init) dynamicznym odpytywaniem przez `gh api user -q .login`.
  * Wdrożono solidny mechanizm fallback do zmiennych konfiguracyjnych git (`git config github.user` / `git config user.name`) w przypadku braku zalogowania w CLI.

* **Dynamiczne mapowanie użytkownika Windows w WSL2 (Fix 3.2)**:
  * Zastąpiono zahardkodowany profil Windows `admin_tk` w ścieżce do IDE w [os-init](file:///home/tkogut/projects/agents-os-core/os-init) dynamicznym wywołaniem systemowym `cmd.exe /c "echo %USERNAME%"`.
  * Dzięki temu edytor Antigravity IDE uruchamia się poprawnie u każdego użytkownika WSL.

* **Instalacja GitHub CLI (gh) przez APT zamiast Snap (Fix 3.3)**:
  * Zmieniono metodę instalacji `gh` w [INSTALL.sh](file:///home/tkogut/projects/agents-os-core/INSTALL.sh) ze `snap` na oficjalne repozytorium APT Debiana/Ubuntu.
  * Rozwiązuje to błąd braku demona `snapd`/`systemd` na domyślnych dystrybucjach WSL2.

* **Izolacja zależności Python w Virtualenv (Fix 3.4)**:
  * Wprowadzono tworzenie dedykowanego środowiska wirtualnego w katalogu `~/.antigravity/venv` podczas instalacji w [INSTALL.sh](file:///home/tkogut/projects/agents-os-core/INSTALL.sh).
  * Przeniesiono instalację bibliotek `GitPython` oraz `PyGithub` do venv, eliminując potrzebę używania ryzykownej flagi `--break-system-packages`.
  * Zaktualizowano [os-init](file:///home/tkogut/projects/agents-os-core/os-init), aby automatycznie używał interpretera z venv przy wywoływaniu bootstrappera.

---

*Zarządzanie wersją i dokumentacją: Antigravity Agent & tkogut.*
