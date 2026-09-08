# Task Backlog: Distributed Multi-Agent Sync Core (AGENTS-OS v6.5 Swarm)
Branch: `feature/distributed-sync-core`
Worktree: `tmp/worktrees/feature/distributed-sync-core`

---

## 📋 Ticket Overview & Implementation Roadmap

- [x] **P1: Worktree Mandate & Environment Isolation**
  - **Description**: Utworzenie odizolowanego środowiska roboczego `tmp/worktrees/feature/distributed-sync-core` dla bezpiecznej modyfikacji rdzenia bez ingerencji w `master`.
  - **Status**: COMPLETE

- [x] **P2: Conflict-Free Merge Configuration (.gitattributes)**
  - **Description**: Dodanie `.gitattributes` do `vault/` oraz głównego repozytorium z regułą `merge=union` dla `.agents/MEMORY.md` oraz `.agents/task.md`.
  - **Target**: `vault/.gitattributes`, `.gitattributes`
  - **Status**: COMPLETE

- [x] **P3: Native Lifecycle Sync Hooks (.antigravity/hooks.json & .gemini/hooks.json)**
  - **Description**: Implementacja automatycznych hooków zdarzeń dla Antigravity/Gemini (`SessionStart` / `PreInvocation` -> auto rebase pull, `SessionEnd` / `Stop` -> auto commit & push pamięci i stanu).
  - **Target**: `vault/.antigravity/hooks.json`, `vault/.gemini/hooks.json`, `vault/.agents/hooks.json`, `.agents/hooks.json`
  - **Status**: COMPLETE

- [x] **P4: Global & Local Git Settings Automation (INSTALL.sh & os-init)**
  - **Description**: Rejestracja `pull.rebase true` oraz `merge.conflictstyle diff3` w instalatorze `INSTALL.sh`, wrapperach `os-init`, `os-init-claude` oraz skryptach `bootstrap.py` / `bootstrap-claude.py`.
  - **Target**: `INSTALL.sh`, `os-init`, `os-init-claude`, `global_skills/swarm-bootstrapper/scripts/bootstrap.py`, `global_skills/swarm-bootstrapper/scripts/bootstrap-claude.py`
  - **Status**: COMPLETE

- [x] **P5: Architectural Governance & Coordinator Mandate Update**
  - **Description**: Wpisanie żelaznej zasady zrzutu pamięci (state-dump) przed finalnym raportem do dokumentów ról (`vault/CLAUDE.md`, `vault/.agents/rules/GOVERNANCE.md`, `vault/.agents/rules/core-rule.md`, `vault/.agents/agents.md`, `vault/SDLC.md`, `CLAUDE.md`, `SDLC.md`).
  - **Target**: `vault/CLAUDE.md`, `vault/.agents/rules/GOVERNANCE.md`, `vault/.agents/rules/core-rule.md`, `vault/.agents/agents.md`, `vault/SDLC.md`, `CLAUDE.md`, `SDLC.md`
  - **Status**: COMPLETE

- [x] **P6: Starter Memory & Task Schemas (v0.42.1)**
  - **Description**: Utworzenie szablonu `.agents/MEMORY.md` w standardzie v0.42.1 oraz `.agents/task.md` w szablonie `vault/`.
  - **Target**: `vault/.agents/MEMORY.md`, `vault/.agents/task.md`, `.agents/MEMORY.md`, `.agents/task.md`
  - **Status**: COMPLETE

- [x] **P7: E2E Test Suite & Distributed Sync Assertions**
  - **Description**: Rozszerzenie skryptu `execution/test_bootstrap.sh` o weryfikację `.gitattributes`, `hooks.json`, ustawień `pull.rebase` i `merge.conflictstyle` oraz plików pamięci; uruchomienie testów lokalnych.
  - **Target**: `execution/test_bootstrap.sh`
  - **Status**: COMPLETE

- [x] **P8: Swarm Triad Handshake Generation & Validation**
  - **Description**: Wygenerowanie `<conversation_id>_builder_handshake.json` i walidacja za pomocą `scripts/validate-handshakes.py`.
  - **Target**: `.agents/swarm/<conv_id>_builder_handshake.json`
  - **Status**: COMPLETE

- [x] **P9: PR Readiness & Release Notes Delivery**
  - **Description**: Przegląd diffa, przygotowanie `CHANGELOG.md`, weryfikacja czystości drzewa git i zgłoszenie gotowości do wdrożenia poprzez PR.
  - **Target**: `CHANGELOG.md`, git commit
  - **Status**: READY_FOR_PR
