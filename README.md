# 🛸 AGENTS-OS v6.5 Swarm Edition — Instrukcja Obsługi

> **Dla kogo jest ten dokument?**  
> Dla każdego programisty i operatora — wyjaśniamy krok po kroku architekturę asynchronicznego roju agentów AI, bezkonfliktową synchronizację rozproszoną oraz zestaw narzędzi CLI.

---

## 📑 Spis treści

1. [Czym jest AGENTS-OS?](#1-czym-jest-agents-os)
2. [Wymagania wstępne](#2-wymagania-wstępne)
3. [Instalacja — jednorazowa konfiguracja](#3-instalacja)
4. [Tworzenie projektu pod Antigravity IDE — `os-init`](#4-os-init)
5. [Tworzenie projektu pod Claude Code (VS Code) — `os-init-claude`](#5-os-init-claude)
6. [Modernizacja istniejącego projektu — `os-upgrade-project`](#6-os-upgrade-project)
7. [Dynamiczne pobieranie umiejętności — `os-add-skill`](#7-os-add-skill)
8. [Protokół rygoru architektonicznego — `/grill-me`](#8-grill-me)
9. [Struktura projektu i bezkonfliktowy Auto-Sync](#9-struktura-projektu-i-bezkonfliktowy-auto-sync)
10. [The Swarm Triad i codzienna praca](#10-the-swarm-triad-i-codzienna-praca)
11. [Najczęstsze problemy i rozwiązania](#11-najczęstsze-problemy)
12. [Dokumentacja techniczna i API](#12-dokumentacja-techniczna-i-api)
13. [English version](#english)

---

## 1. Czym jest AGENTS-OS?

**AGENTS-OS** to zaawansowany framework koordynacji i konteneryzacji pracy agentów sztucznej inteligencji (Antigravity IDE, Claude Code, Cursor, Zed). Zapewnia rygor architektoniczny, pracę w modelu asynchronicznej triady (**Swarm Triad**), bezkonfliktową synchronizację rozproszoną na wielu maszynach (Laptop WSL, VPS, Desktop) oraz dynamiczną integrację z biblioteką 1400+ skilli.

### Kluczowe Komponenty Systemu:

| Narzędzie / Komponent | Typ | Przeznaczenie |
|---|---|---|
| **`INSTALL.sh`** | Instalator | Jednorazowa konfiguracja środowiska, szablonów, zależności Pythona i komend powłoki |
| **`os-init`** | CLI / Shell | Tworzy nowe repozytorium z szablonu Vault i otwiera Antigravity IDE |
| **`os-init-claude`** | CLI / Shell | Tworzy nowe repozytorium zoptymalizowane pod VS Code i Claude Code |
| **`os-upgrade-project`** | CLI | Migruje dowolny projekt do standardu v6.5 Swarm (auto-sync, union-merge, hooki, symlinki) |
| **`os-add-skill`** | CLI | Dynamicznie pobiera i linkuje skille z rejestrów RAG oraz bazy `sickn33/awesome-skills` |
| **`os-run-builder`** | CLI | Automatyzuje izolację środowiska roboczego w Git Worktree (`tmp/worktrees/`) |
| **`/grill-me`** | CLI / Skill | Pre-flight interview weryfikujący topologię maszyn, bazy fail-closed i odporność na awarie |
| **Vault (Złoty Standard)** | Szablon | Wzorcowa struktura repozytorium kopiowana do każdego projektu |

---

## 2. Wymagania Wstępne

Zanim zaczniesz, upewnij się że masz zainstalowane:

| Narzędzie | Jak sprawdzić | Gdzie pobrać |
|---|---|---|
| **WSL2 + Ubuntu** (Windows) | `wsl --version` w PowerShell | [docs.microsoft.com](https://docs.microsoft.com/pl-pl/windows/wsl/install) |
| **Antigravity IDE** | Czy masz ikonę w Menu Start | Oficjalny instalator |
| **VS Code** *(opcjonalne — tryb Claude Code)* | `code --version` | [code.visualstudio.com](https://code.visualstudio.com/) |
| **Claude Code extension** *(opcjonalne)* | Rozszerzenie w VS Code Marketplace | `claude.ai/code` |
| **Python 3** | `python3 --version` w terminalu WSL | Preinstalowany w Ubuntu (`>= 3.10`) |
| **Git** | `git --version` | `sudo apt install git` |
| **GitHub CLI** | `gh --version` | Instaluje się automatycznie przez `INSTALL.sh` |

---

## 3. Instalacja

> ⚠️ **Wykonujesz to tylko raz** — przy pierwszym uruchomieniu środowiska.

```bash
# 1. Otwórz terminal WSL (Ubuntu)

# 2. Sklonuj repozytorium rdzenia
mkdir -p ~/projects
git clone https://github.com/tkogut/agents-os-core.git ~/projects/agents-os-core
cd ~/projects/agents-os-core

# 3. Uruchom instalator
bash INSTALL.sh

# 4. Zaloguj się do GitHub CLI (jeśli nie jesteś zalogowany)
gh auth login

# 5. Załaduj konfigurację do bieżącego terminala
source ~/.bashrc.d/antigravity
```

---

## 4. `os-init` — Tworzenie projektu (Antigravity IDE)

Jedno polecenie wykonuje pełny bootstrap produkcyjnego projektu:

```bash
os-init nazwa-projektu
```

### Co dzieje się automatycznie:
1. 📦 Tworzy katalog: `~/projects/nazwa-projektu`
2. 🛡️ Kopiuje strukturę **Vault (Złoty Standard)** wraz z 70+ skillami.
3. 📝 Konfiguruje `.gitattributes` (`merge=union` dla plików pamięci i zadań).
4. ⚙️ Ustawia lokalne parametry Git: `pull.rebase=true` oraz `merge.conflictstyle=diff3`.
5. 🔀 Inicjalizuje lokalne repozytorium Git i tworzy initial commit.
6. 🐙 Tworzy publiczne repozytorium na GitHubie (`github.com/<user>/nazwa-projektu`).
7. 🚀 Wysyła kod (`git push origin main`).
8. 🔗 Mapuje symlinki `.claude/skills/*` dla kompatybilności krzyżowej IDE.
9. 🖥️ Otwiera **Antigravity IDE** w środowisku WSL:Ubuntu.
10. 🔀 Przechodzi (`cd`) do katalogu w bieżącym terminalu.

---

## 5. `os-init-claude` — Tworzenie projektu (Claude Code / VS Code)

Dla programistów preferujących edytor VS Code z rozszerzeniem Claude Code:

```bash
os-init-claude nazwa-projektu
```

Dodatkowo:
- Generuje manifest [`CLAUDE.md`](file:///home/tkogut/projects/agents-os-core/CLAUDE.md).
- Konfiguruje natywne slash commands w `.claude/commands/` (`/grill-me`, `/worktree-init`, `/handshake`, `/qa-gate`, `/commit`).
- Ustawia rolę Builder jako `claude-code` w `agents.yaml`.
- Otwiera projekt poleceniem `code .`.

---

## 6. `os-upgrade-project` — Modernizacja Istniejących Projektów

Jeśli masz starszy projekt i chcesz wdrożyć natywny silnik asynchronicznej pracy wielomaszynowej AGENTS-OS v6.5 Swarm:

```bash
# Wewnątrz katalogu projektu:
os-upgrade-project

# Lub podając ścieżkę:
os-upgrade-project ~/projects/stary-projekt
```

Skrypt automatycznie:
- Wdraża reguły `.gitattributes` (`merge=union` dla `MEMORY.md` i `task.md`).
- Ustawia parametry `pull.rebase=true` i `merge.conflictstyle=diff3`.
- Wdraża natywne hooki cyklu życia (`SessionStart` pull / `SessionEnd` auto state-dump).
- Tworzy dowiązania symboliczne do 70+ skilli w `.claude/skills/`.
- Inicjalizuje standard pamięci maszynowej `.agents/MEMORY.md` (v0.42.1).

---

## 7. `os-add-skill` — Dynamiczne Pobieranie Umiejętności

Potrzebujesz specjalistycznej wiedzy (np. optymalizacji PostgreSQL, bezpieczeństwa sieciowego, testów Playwright)?

```bash
os-add-skill postgresql-optimization
os-add-skill n8n-ops
```

Skrypt przeszukuje lokalny rejestr, repozytorium główne oraz bazę **1400+ skilli `sickn33/antigravity-awesome-skills`**, pobiera pliki do `.agents/skills/` i natychmiast tworzy dowiązanie w `.claude/skills/`.

---

## 8. `/grill-me` — Protokół Rygoru Architektonicznego

Przed przystąpieniem do kodowania nietrywialnych funkcji, uruchom protokół wywiadu architektonicznego:

```bash
# W oknie czatu asystenta:
/grill-me

# Lub bezpośrednio z terminala:
node .agents/skills/grill-me.js
```

Asystent zweryfikuje:
1. **Topologię maszyn** (który węzeł ma wyłączność na wdrożenie).
2. **Auto-Sync** (rebase strategy i union merge).
3. **Bazy danych i fallbacki** (Defensive Hybrid, Factory Defaults, 501 Fail-Closed).
4. **Edge cases** (limity API, split-brain, Circuit Breakers).
5. **Mandat zrzutu stanu** (State-Dump R-SYNC-01 do `.agents/MEMORY.md`).

---

## 9. Struktura Projektu i Bezkonfliktowy Auto-Sync

```
moja-aplikacja/
│
├── .gitattributes           ← Reguły bezkonfliktowego łączenia (merge=union)
├── agents.yaml              ← Konfiguracja ról i uprawnień Swarm Triad
├── design-tokens.md         ← Standard UI i tokeny wizualne
├── task.md                  ← 📋 Główny backlog zadań (append-only)
├── CLAUDE.md                ← Konfiguracja Buildera dla Claude Code
│
├── .ai/
│   └── agentic.config.json  ← Centralna konfiguracja pipeline'u i bramek QA
│
├── .antigravity/            ← Hooki cyklu życia sesji (SessionStart/End)
│   └── hooks.json
├── .claude/
│   ├── commands/            ← Slash commands (/grill-me, /commit, itd.)
│   └── skills/              ← Automatyczne symlinki do .agents/skills/*
│
├── execution/               ← Skrypty testowe i weryfikacyjne
├── tmp/
│   └── worktrees/           ← Odizolowane środowiska pracy subagentów Builder
│
└── .agents/                 ← Rdzeń pamięci i inteligencji agenta
    ├── MEMORY.md            ← Pamięć rozproszona v0.42.1 (rejestr węzłów i sesji)
    ├── swarm/               ← Podpisy i pliki handshake (*_handshake.json)
    ├── skills/              ← Fizyczne implementacje skilli
    ├── specs/               ← Specyfikacje architektoniczne i RAG
    └── rules/               ← Żelazne reguły bezpieczeństwa (GOVERNANCE.md)
```

---

## 10. The Swarm Triad i Codzienna Praca

System wymusza podział odpowiedzialności na trzy niezależne role:

```
[COORDINATOR]  → Planuje w task.md, izoluje gałąź przez os-run-builder. ZAKAZ edycji src/.
       ↓
  [BUILDER]    → Implementuje kod w tmp/worktrees/, uruchamia testy, podpisuje _handshake.json.
       ↓
  [AUDITOR]    → Weryfikuje testy bramki QA, sprawdza spójność logiki, dopuszcza do PR.
```

### Codzienna Praca:
```bash
# 1. Otwórz projekt
cd ~/projects/moja-aplikacja
antigravity .   # lub: code .

# 2. Dopisuj zadania w task.md i wykonaj wywiad /grill-me

# 3. Zapisz i zsynchronizuj stan
git push
```

---

## 11. Najczęstsze Problemy

| Problem | Przyczyna | Rozwiązanie |
|---|---|---|
| `Permission denied` przy `~/.bashrc.d/antigravity` | Próba uruchomienia zamiast ładowania (`source`) | Użyj `source ~/.bashrc.d/antigravity` |
| `os-init: command not found` | Brak załadowanej konfiguracji shella | Uruchom `source ~/.bashrc.d/antigravity` |
| Błędy merge w `MEMORY.md` | Brak reguły union w `.gitattributes` | Uruchom `os-upgrade-project` |
| Claude Code nie widzi skilli | Brak dowiązań w `.claude/skills/` | Uruchom `os-upgrade-project` lub `bash INSTALL.sh` |
| Explorer zawiesza się przy `\\wsl.localhost` | Znany błąd sieciowy WSL2 | W PowerShell uruchom `wsl --shutdown` |

---

## 12. Dokumentacja Techniczna i API

Szczegółowa specyfikacja interfejsów, formatów JSON, schematów pamięci i protokołów bezpieczeństwa znajduje się w dedykowanych dokumentach:
- 📖 [**Dokumentacja Techniczna API & CLI** (`docs/API.md`)](file:///home/tkogut/projects/agents-os-core/docs/API.md)
- 🛡️ [**Standard Cyklu Życia SDLC** (`SDLC.md`)](file:///home/tkogut/projects/agents-os-core/SDLC.md)
- 📜 [**Changelog i Historia Wdrożeń** (`CHANGELOG.md`)](file:///home/tkogut/projects/agents-os-core/CHANGELOG.md)

---

<br><hr><br>

<a name="english"></a>
# [EN] AGENTS-OS v6.5 Swarm Edition — User Guide

> **Enterprise-grade asynchronous multi-agent framework for Antigravity IDE and Claude Code.**

---

## What is AGENTS-OS?

**AGENTS-OS** provides orchestration, architectural rigor, and distributed multi-machine synchronization for AI coding agents. It enforces the **Swarm Triad** pattern (Coordinator / Builder / Auditor) with Git Worktree isolation and conflict-free memory merging.

### Core Tooling Suite:

| Tool | Type | Purpose |
|---|---|---|
| **`INSTALL.sh`** | Installer | Single-command system setup, Python venv, templates, and shell integration |
| **`os-init`** | CLI | Creates a new Golden Standard repository and launches Antigravity IDE |
| **`os-init-claude`** | CLI | Creates a new repository tailored for VS Code and Claude Code |
| **`os-upgrade-project`** | CLI | Modernizes existing repositories to v6.5 Swarm (auto-sync, union-merge, hooks) |
| **`os-add-skill`** | CLI | Dynamically fetches skills from RAG registries and 1,400+ community skills |
| **`os-run-builder`** | CLI | Automates Git Worktree workspace isolation under `tmp/worktrees/` |
| **`/grill-me`** | CLI / Skill | Pre-flight architectural interview ensuring fail-closed resilience and state dumps |

---

## Quick Start

```bash
# 1. Clone & Install
mkdir -p ~/projects
git clone https://github.com/tkogut/agents-os-core.git ~/projects/agents-os-core
cd ~/projects/agents-os-core
bash INSTALL.sh

# 2. Source environment
source ~/.bashrc.d/antigravity

# 3. Create a project
os-init my-new-app
```

---

## Technical Reference

For technical schemas (`MEMORY.md` v0.42.1, `*_handshake.json`, `.ai/agentic.config.json`, lifecycle hooks, and CLI API specifications), refer to [**`docs/API.md`**](file:///home/tkogut/projects/agents-os-core/docs/API.md).
