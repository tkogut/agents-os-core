# Task Backlog: Native Grill-Me Skill Implementation (AGENTS-OS v6.5 Swarm)
Branch: `feature/native-grill-me-skill`
Worktree: `tmp/worktrees/feature/native-grill-me-skill`

---

## 📋 Ticket Overview & Implementation Roadmap

- [x] **G1: Worktree Environment Isolation**
  - **Description**: Utworzenie odizolowanego worktree `tmp/worktrees/feature/native-grill-me-skill` i inicjalizacja backlogu.
  - **Status**: COMPLETE

- [x] **G2: Executable Grill-Me Script Implementation**
  - **Description**: Utworzenie wykonywalnego skryptu `vault/.agents/skills/grill-me.js` oraz `grill_me.py` z profesjonalnym nagłówkiem, pytaniami architektonicznymi i instrukcją zapisu w `.agents/MEMORY.md`.
  - **Target**: `vault/.agents/skills/grill-me.js`, `vault/.agents/skills/grill-me/scripts/grill_me.py`, `global_skills/grill-me/scripts/grill_me.py`
  - **Status**: COMPLETE

- [x] **G3: Skill Manifest & Claude Slash Command Registration**
  - **Description**: Utworzenie `SKILL.md` oraz `.claude/commands/grill-me.md` dla pełnej integracji z systemem komend Claude Code i Antigravity.
  - **Target**: `vault/.agents/skills/grill-me/SKILL.md`, `global_skills/grill-me/SKILL.md`, `vault/.claude/commands/grill-me.md`
  - **Status**: COMPLETE

- [x] **G4: Symlink Mapping & Installer Integration**
  - **Description**: Rozszerzenie mapowania symlinków w `INSTALL.sh`, `os-init`, `os-init-claude`, `bootstrap.py`, `bootstrap-claude.py` i `os-upgrade-project`, aby `.claude/skills/grill-me` było automatycznie linkowane.
  - **Target**: `INSTALL.sh`, `os-init`, `os-init-claude`, `bootstrap.py`, `bootstrap-claude.py`, `os-upgrade-project`, `scripts/sync-skills.sh`
  - **Status**: COMPLETE

- [x] **G5: Integration Verification & Handshake**
  - **Description**: Uruchomienie `test_bootstrap.sh` z asercją obecności i działania skilla `grill-me`, wygenerowanie `_handshake.json` i zgłoszenie gotowości do PR.
  - **Target**: `execution/test_bootstrap.sh`, `.agents/swarm/*_builder_handshake.json`
  - **Status**: COMPLETE
