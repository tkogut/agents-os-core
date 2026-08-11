# 🔀 Agents-OS Context Router & Task Entry-Point

**System:** AGENTS-OS v6.5 Swarm Edition  
**Context Budget Policy:** Lean entry-point router loading a maximum of 3 domain modules simultaneously.

---

## 🧭 Domain Routing Map

Select the appropriate domain module based on your current task objective:

1. **Pipeline & SDLC Workflow**:
   - Module: [agents-pipeline.md](domain/agents-pipeline.md)
   - Scope: 6-phase SDLC lifecycle, Git Worktree isolation, Swarm Triad roles.

2. **Quality Assurance & Verification**:
   - Module: [agents-qa.md](domain/agents-qa.md)
   - Scope: Validation gates (`pytest`, `flake8`, `mypy`), R-SEC-01 secret hygiene, security audit.

3. **UX & Proof-of-Work Evidence**:
   - Module: [agents-ux.md](domain/agents-ux.md)
   - Scope: Visual proof-of-work, Kanban Web UI state tracking, human-in-the-loop (HITL) resolution.

---

## ⚡ Context Budget Constraints
- **Rule**: Do not load more than 3 domain specification modules into active context at once.
- **Priority**: Primary focus must remain on source implementation files in `src/mms4tk/`.
