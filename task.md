# Backlog - AGENTS-OS Core Inception

- [x] Create directory topology (`.agents/skills`, `.agents/rules`, `.agents/specs`, `.agents/plans`, `.agents/swarm`)
- [x] Create core files: `agents.yaml` (with GEM role), `task.md`, `design-tokens.md`
- [x] Implement Graph RAG in `.agents/specs/graph.json` mapping `INSTALL.sh`, `os-init`, and `vault/`
- [x] Implement Self-Rule in `.agents/rules/core-rule.md` forcing Git Worktrees and asynchronous execution
- [x] Verify core configuration structure and validate Graph RAG node integrity
- [x] Migrate Constitution and knowledge base to native structure in `.agents/specs/` and update `graph.json`
- [x] Patch all working files to replace old v3.2 references with native AGENTS-OS v4.2

- [x] Portability & Automation updates (v4.2.0)
  - [x] Update Caveman plugin installation in `INSTALL.sh` to use github URL
  - [x] Implement old template clean-up in `INSTALL.sh`
  - [x] Create automated E2E script `execution/test_bootstrap.sh`

- [x] Dynamic Skill Loading & CLI enhancements (v4.2.0)
  - [x] Update Caveman plugin installation in `INSTALL.sh` to use github URL
  - [x] Implement old template clean-up in `INSTALL.sh`
  - [x] Create automated E2E script `execution/test_bootstrap.sh`
  - [x] Update `os-add-skill` script
  - [x] Update `INSTALL.sh`
  - [x] Update `os-init`
  - [x] Update `bootstrap.py`
  - [x] Update `test_bootstrap.sh`

- [x] Systemic Version Bump & Documentation Upgrade (v6.0)
  - [x] **TSK-016**: Stworzenie izolowanego środowiska Git Worktree pod gałąź `feature/v6-upgrade`.
  - [x] **TSK-017**: Aktualizacja Konstytucji `AGENTS-OS.md` do wersji v6.0 (wdrożenie rygorów Swarm Triad i automatyzacji sprzątania).
  - [x] **TSK-018**: Kompleksowa aktualizacja `README.md` i `CHANGELOG.md` dla v6.0 ("Enterprise Swarm Edition").
  - [x] **TSK-019**: Przeskanowanie i zmiana zmiennych wersji w `INSTALL.sh`, `os-init`, `os-add-skill`, `agents.yaml`, `vault/agents.yaml`, `bootstrap.py`.
  - [x] **TSK-020**: Usunięcie przestarzałych plików dokumentacji (`walkthrough.md`, `implementation_plan.md`, `refactor_decision.md`).
  - [x] **TSK-021**: Uruchomienie testu integracyjnego `test_bootstrap.sh` w celu walidacji poprawności działania instalacji v6.0.




