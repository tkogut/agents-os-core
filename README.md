# AGENTS-OS v4.1 Swarm Edition — Instrukcja obsługi

> **Dla kogo jest ten dokument?**
> Dla każdego — nawet jeśli nie programujesz na co dzień.
> Wyjaśniamy krok po kroku co robić i dlaczego.

---

## Spis treści

1. [Czym jest AGENTS-OS?](#1-czym-jest-agents-os)
2. [Co potrzebujesz zanim zaczniesz](#2-wymagania)
3. [Instalacja — jednorazowa konfiguracja](#3-instalacja)
4. [Tworzenie nowego projektu — komenda `os-init`](#4-os-init)
5. [Struktura nowego projektu](#5-struktura-projektu)
6. [Codzienna praca — jak otwierać projekty](#6-codzienna-praca)
7. [Najczęstsze problemy i rozwiązania](#7-najczestsze-problemy)
8. [Jak działa system od środka](#8-jak-dziala-od-srodka)
9. [English version](#english)

---

## 1. Czym jest AGENTS-OS?

**AGENTS-OS** to zestaw narzędzi i konfiguracji, który sprawia że asystent AI (Antigravity) działa jak doświadczony programista — zamiast pisać długie elaboraty, dostaje konkretne zadanie i je wykonuje.

System składa się z trzech elementów:

| Element | Co to jest | Do czego służy |
|---|---|---|
| **INSTALL.sh** | Skrypt instalacyjny | Jednorazowe ustawienie wszystkiego na komputerze |
| **os-init** | Komenda startowa | Tworzenie nowego projektu jedną komendą |
| **Vault (Złoty Standard)** | Szablon folderów | Gotowa struktura, która kopiuje się do każdego projektu |

---

## 2. Wymagania

Zanim zaczniesz, upewnij się że masz zainstalowane:

| Narzędzie | Jak sprawdzić | Gdzie pobrać |
|---|---|---|
| **WSL2 + Ubuntu** (Windows) | `wsl --version` w PowerShell | [docs.microsoft.com](https://docs.microsoft.com/pl-pl/windows/wsl/install) |
| **Antigravity IDE** | Czy masz ikonę w Menu Start | Zainstaluj przez oficjalny instalator |
| **Antigravity (okno czatu)** | Czy działa aplikacja asystenta | Jak wyżej |
| **Python 3** | `python3 --version` w terminalu WSL | Preinstalowany w Ubuntu |
| **Git** | `git --version` | `sudo apt install git` |
| **GitHub CLI** | `gh --version` | Instaluje się automatycznie przez INSTALL.sh |

> **Skąd wziąć terminal WSL?**
> W Windows naciśnij `Win + R`, wpisz `wsl` i Enter. Otworzy się czarny terminal Ubuntu.

---

## 3. Instalacja

> ⚠️ **Wykonujesz to tylko raz** — przy pierwszym ustawieniu systemu na komputerze.

### Krok 1 — Otwórz terminal WSL (Ubuntu)

W Windows: `Win + R` → wpisz `wsl` → Enter

### Krok 2 — Pobierz repozytorium

```bash
mkdir -p ~/projects
git clone https://github.com/tkogut/agents-os-core.git ~/projects/agents-os-core
cd ~/projects/agents-os-core
```

### Krok 3 — Uruchom instalator

```bash
bash INSTALL.sh
```

Instalator automatycznie:
- Instaluje GitHub CLI (`gh`) przez repozytorium APT
- Tworzy izolowane środowisko wirtualne Python (`~/.antigravity/venv`) z zależnościami (`GitPython`, `PyGithub`)
- Kopiuje szablony projektów do `~/.antigravity/templates/`
- Rejestruje komendę `os-init` w systemie
- Dodaje konfigurację do `~/.bashrc.d/antigravity`

### Krok 4 — Zaloguj się do GitHub

```bash
gh auth login
```

Wybierz: `GitHub.com` → `HTTPS` → `Login with a web browser` → wklej kod na stronie GitHub.

### Krok 5 — Załaduj konfigurację shella

```bash
source ~/.bashrc.d/antigravity
```

> **Co to robi?**
> Ładuje skróty i funkcje (w tym `os-init`) do Twojego terminala.
> **Nowe terminale** ładują to automatycznie. Przy pierwszym razie musisz to zrobić ręcznie.

---

## 4. `os-init` — Tworzenie nowego projektu

> 💡 **Jedna komenda robi wszystko.**

### Jak używać

W terminalu WSL wpisz:

```bash
os-init nazwa-twojego-projektu
```

**Przykład:**

```bash
os-init moja-aplikacja
```

### Co się dzieje automatycznie

```
1. 📦  Tworzy folder: ~/projects/moja-aplikacja
2. 🛡️  Kopiuje do niego Złoty Standard (szablony plików i folderów)
3. 📝  Tworzy .gitignore i README.md
4. 🔀  Inicjalizuje lokalne repozytorium Git
5. 📝  Robi pierwszy commit ("init: agents-os v4.1 swarm bootstrap")
6. 🐙  Tworzy publiczne repozytorium na GitHubie: github.com/<twój-użytkownik-git>/moja-aplikacja
7. 🚀  Wysyła (push) kod na GitHub
8. 🖥️  Otwiera Antigravity IDE w środowisku WSL:Ubuntu w folderze projektu
9. 🔀  Przechodzi do folderu projektu w Twoim terminalu (cd)
```

### Po zakończeniu

Twój terminal automatycznie przejdzie do nowego folderu:

```bash
📁 Jesteś w: /home/<użytkownik-linux>/projects/moja-aplikacja
```

A na GitHub pojawi się nowe repozytorium:
```
https://github.com/<twój-użytkownik-git>/moja-aplikacja
```

---

## 5. Struktura projektu

Każdy projekt tworzony przez `os-init` ma identyczną, gotową strukturę:

```
moja-aplikacja/
│
├── README.md                ← Opis projektu (tu możesz pisać co to za projekt)
├── .gitignore               ← Lista plików ignorowanych przez Git
├── agents.yaml              ← Konfiguracja ról asystenta AI
├── design-tokens.md         ← Wytyczne wizualne (kolory, fonty, itp.)
├── task.md                  ← 📋 TU PISZESZ CO AI MA ZROBIĆ
│
├── execution/               ← Skrypty uruchomieniowe
├── tmp/                     ← Logi tymczasowe (ignorowane przez Git)
│
├── .github/                 ← Konfiguracja automatyzacji GitHub Actions
│   └── workflows/
│
└── .agents/                 ← Pamięć i konfiguracja asystenta AI
    ├── plans/               ← Długoterminowe plany projektu
    ├── skills/              ← Umiejętności asystenta (pobierane automatycznie)
    ├── specs/               ← Dokumentacja techniczna i wiedza RAG
    └── workflows/           ← Zautomatyzowane instrukcje
```

### Najważniejszy plik: `task.md`

To tutaj piszesz asystentowi co ma zrobić. Przykład:

```markdown
## Zadanie
Stwórz stronę główną aplikacji w HTML i CSS.
Użyj kolorów: niebieski (#2563EB), biały (#FFFFFF).
Dodaj nagłówek, sekcję hero i stopkę.
```

---

## 6. Codzienna praca

### Otwieranie istniejącego projektu w IDE

Masz dwie opcje:

**Opcja A — z terminala WSL:**
```bash
source ~/.bashrc.d/antigravity   # tylko jeśli nowy terminal
cd ~/projects/nazwa-projektu
antigravity .
```

**Opcja B — z Menu Start Windows:**
1. Uruchom **Antigravity IDE**
2. `File` → `Open Folder`
3. W pasku adresu Eksploratora wpisz: `\\wsl.localhost\Ubuntu\home\<użytkownik-linux>\projects\`
4. Wybierz folder projektu

> ⚠️ **Uwaga:** Jeśli Eksplorator Windows się zawiesza przy otwieraniu folderu WSL, wykonaj reset:
> ```powershell
> # W PowerShell (Windows):
> wsl --shutdown
> ```
> Następnie uruchom ponownie terminal WSL.

### Wysyłanie zmian na GitHub

```bash
git add -A
git commit -m "opis: co zrobiłem"
git push
```

Lub powiedz asystentowi: *„zapisz i wyślij na GitHub"* — zrobi to za Ciebie.

---

## 7. Najczęstsze problemy

### ❌ `Permission denied` przy `~/.bashrc.d/antigravity`

**Problem:** Próbujesz uruchomić plik zamiast go załadować.

**Rozwiązanie:**
```bash
# ❌ ŹLE — uruchamia jako osobny proces
~/.bashrc.d/antigravity

# ✅ DOBRZE — ładuje do bieżącego terminala
source ~/.bashrc.d/antigravity
```

---

### ❌ `os-init: command not found`

**Problem:** Konfiguracja shella nie jest załadowana.

**Rozwiązanie:**
```bash
source ~/.bashrc.d/antigravity
```

Jeśli nadal nie działa, sprawdź instalację:
```bash
ls ~/.local/bin/os-init-run   # powinien istnieć
```

Jeśli pliku nie ma — uruchom ponownie `bash INSTALL.sh`.

---

### ❌ IDE otwiera się bez WSL:Ubuntu (projekt lokalny Windows)

**Problem:** IDE otwiera pliki w trybie Windows, nie WSL — brak dostępu do narzędzi Linux.

**Rozwiązanie:** Otwieraj IDE zawsze przez terminal WSL:
```bash
antigravity .
```

Lub używaj `os-init` — otwiera IDE automatycznie z flagą `--remote wsl+Ubuntu`.

---

### ❌ `gh repo create failed: --push enabled but no commits found`

**Problem:** Stara wersja skryptu — naprawiona w wersji `05a271f`.

**Rozwiązanie:** Pobierz najnowszą wersję i zainstaluj ponownie:
```bash
cd ~/projects/agents-os-core
git pull origin master
bash INSTALL.sh
```

---

### ❌ Eksplorator Windows zawiesza się przy `\\wsl.localhost`

**Problem:** Błąd integracji WSL2 z systemem plików Windows (znany bug WSL).

**Rozwiązanie:**
```powershell
# W PowerShell Windows:
wsl --shutdown
```
Następnie uruchom ponownie terminal WSL. Reset trwa ~5 sekund.

---

### ❌ `antigravity` otwiera okno czatu zamiast edytora kodu

**Problem:** Konflikt między aplikacją Antigravity (czat) a Antigravity IDE (edytor).

**Rozwiązanie:** Używaj konkretnych komend:
```bash
antigravity .          # otwiera IDE (edytor kodu) w bieżącym folderze
agy                    # uruchamia CLI asystenta (czat w terminalu)
```

---

## 8. Jak działa system od środka

> Ta sekcja jest dla ciekawskich — nie musisz tego czytać żeby używać systemu.

### Dlaczego `os-init` jest funkcją shella, a nie skryptem?

W systemie Linux, skrypt uruchomiony jako osobny proces **nie może zmienić katalogu** (`cd`) w terminalu rodzica. To fundamentalne ograniczenie systemu.

Dlatego `os-init` jest **funkcją shella** zdefiniowaną w `~/.bashrc.d/antigravity`:
1. Wywołuje `os-init-run` (właściwy skrypt)
2. Skrypt wypisuje na końcu `__PROJECT_DIR__:/ścieżka/do/projektu`
3. Funkcja przechwytuje tę linię i wykonuje `cd` — **w bieżącym terminalu**

### Kolejność operacji w `bootstrap.py`

```
git init  →  vault copy  →  .gitignore  →  README.md  →  git commit  →  gh repo create  →  git push
```

> Kolejność **musi** być taka — `gh repo create` wymaga żeby commit istniał zanim się go wywoła.

### The Swarm Triad — 3 role asystenta

System przypisuje asystentowi 3 tryby pracy:

| Rola | Kiedy aktywna | Co robi |
|---|---|---|
| **Coordinator** | Planowanie | Czyta `task.md`, tworzy plan, NIE pisze kodu |
| **Builder** | Implementacja | Pisze kod, edytuje pliki, uruchamia komendy |
| **Auditor** | Weryfikacja | Sprawdza błędy, logi, jakość kodu |

---

<br><hr><br>

<a name="english"></a>
# [EN] AGENTS-OS v4.1 Swarm Edition — User Guide

> **Who is this for?**
> Everyone — even if you don't code every day.
> Step-by-step instructions explaining what to do and why.

---

## Table of Contents

1. [What is AGENTS-OS?](#what-is-agents-os)
2. [Requirements](#requirements)
3. [Installation — one-time setup](#installation)
4. [Creating a new project — `os-init`](#os-init)
5. [Project structure](#project-structure)
6. [Daily workflow](#daily-workflow)
7. [Common issues & fixes](#common-issues)

---

## What is AGENTS-OS?

**AGENTS-OS** is a toolkit and configuration framework that makes the Antigravity AI assistant work like an experienced developer — instead of lengthy explanations, it receives a concrete task and executes it.

| Component | What it is | Purpose |
|---|---|---|
| **INSTALL.sh** | Installation script | One-time setup on your machine |
| **os-init** | Startup command | Create a new project with one command |
| **Vault (Golden Standard)** | Folder template | Ready-made structure copied into every project |

---

## Requirements

| Tool | How to check | Where to get |
|---|---|---|
| **WSL2 + Ubuntu** (Windows) | `wsl --version` in PowerShell | [docs.microsoft.com](https://docs.microsoft.com/en-us/windows/wsl/install) |
| **Antigravity IDE** | Icon in Start Menu | Official installer |
| **Antigravity (chat window)** | Does the assistant app work | Same as above |
| **Python 3** | `python3 --version` in WSL | Pre-installed in Ubuntu |
| **Git** | `git --version` | `sudo apt install git` |
| **GitHub CLI** | `gh --version` | Auto-installed by INSTALL.sh |

---

## Installation

> ⚠️ **Run this only once** — when setting up the system for the first time.

```bash
# 1. Open WSL terminal (Windows: Win+R → type "wsl" → Enter)

# 2. Clone the repository
mkdir -p ~/projects
git clone https://github.com/tkogut/agents-os-core.git ~/projects/agents-os-core
cd ~/projects/agents-os-core

# 3. Run the installer
bash INSTALL.sh

# 4. Log in to GitHub
gh auth login

# 5. Load shell configuration
source ~/.bashrc.d/antigravity
```

---

## `os-init` — Creating a new project

```bash
os-init my-project-name
```

**What happens automatically:**

```
1. 📦  Creates folder: ~/projects/my-project-name
2. 🛡️  Copies Golden Standard (file/folder templates)
3. 📝  Creates .gitignore and README.md
4. 🔀  Initializes local Git repository
5. 📝  Makes first commit
6. 🐙  Creates public GitHub repo: github.com/<your-github-username>/my-project-name
7. 🚀  Pushes code to GitHub
8. 🖥️  Opens Antigravity IDE in WSL:Ubuntu environment
9. 🔀  Changes terminal directory to the new project (cd)
```

---

## Project structure

```
my-project-name/
│
├── README.md                ← Project description
├── .gitignore               ← Files ignored by Git
├── agents.yaml              ← AI assistant role config
├── task.md                  ← 📋 WRITE AI TASKS HERE
│
├── execution/               ← Runtime scripts
├── tmp/                     ← Temporary logs (Git-ignored)
├── .github/                 ← GitHub Actions automation
│
└── .agents/                 ← AI assistant memory & config
    ├── plans/
    ├── skills/
    ├── specs/
    └── workflows/
```

---

## Daily workflow

```bash
# Open existing project in IDE (from WSL terminal)
cd ~/projects/my-project
antigravity .

# Push changes to GitHub
git add -A
git commit -m "describe: what you did"
git push
```

---

## Common issues

| Error | Cause | Fix |
|---|---|---|
| `Permission denied` on `~/.bashrc.d/antigravity` | Running instead of sourcing | Use `source ~/.bashrc.d/antigravity` |
| `os-init: command not found` | Shell config not loaded | Run `source ~/.bashrc.d/antigravity` |
| IDE opens without WSL:Ubuntu | Opening via .exe directly | Use `antigravity .` from WSL terminal |
| Explorer freezes at `\\wsl.localhost` | Known WSL2 network bug | Run `wsl --shutdown` in PowerShell, then restart WSL |
| `gh repo create failed: no commits` | Old script version | Run `git pull && bash INSTALL.sh` |

---

*Document maintained by Antigravity Agent & tkogut. Last updated: May 2026.*
