# ⚙️ Domain Module: SDLC & Pipeline Workflow

**Reference:** Integrates with [SDLC.md](../../SDLC.md)

### Rules & Workflow:
1. **Worktree Isolation**: Every implementation must run in `tmp/worktrees/task_<name>/`.
2. **Role Commit Enforcement**: Commit messages must specify `SWARM_ROLE=builder` for functional changes.
3. **No Direct Pushes**: Only the Coordinator role may push merged `main` to `origin/main`.
4. **State-Dump Obligation**: Coordinator must ensure `.agents/MEMORY.md` and `.agents/task.md` state-dump is pushed before concluding sessions.
