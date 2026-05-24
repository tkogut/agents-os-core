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
  - [x] Implement `os-add-skill` script (Python downloader with recursive API directory fetch)
  - [x] Update `INSTALL.sh` (remove global awesome-skills, deploy `os-add-skill`, auto-generate `~/.bashrc.d/antigravity` and update `~/.bashrc`)
  - [x] Update `os-init` (dynamic Windows user scanning & extract project name basename for GitHub URL)
  - [x] Update `bootstrap.py` (use `git branch -M main` and support relative/absolute paths)
  - [x] Update `test_bootstrap.sh` (verify dynamic `os-add-skill` functionality)


