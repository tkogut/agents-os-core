# Task Backlog: Hook Branch Safety & Main/Master Protection (AGENTS-OS v6.5.3 Swarm)
Branch: `fix/hook-branch-protection`
Worktree: `tmp/worktrees/fix/hook-branch-protection`

---

## 📋 Ticket Overview & Implementation Roadmap

- [x] **H1: Protected Branch Guard in Lifecycle Hooks**
  - **Description**: Zabezpieczenie hooków SessionEnd / Stop przed automatycznym pushem i commitem na gałęziach `main`/`master`.
  - **Target**: `vault/.agents/hooks.json`, `.agents/hooks.json`, `os-upgrade-project`, `docs/API.md`, `CHANGELOG.md`
  - **Status**: COMPLETE

- [x] **H2: E2E Test Suite & Handshake Verification**
  - **Description**: Uruchomienie `execution/test_bootstrap.sh`, wygenerowanie i walidacja Builder Handshake.
  - **Status**: COMPLETE
