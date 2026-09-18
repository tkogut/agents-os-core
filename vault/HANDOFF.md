# 🛡️ Cezar Runtime HANDOFF Template (Fault-Tolerance & Session Resumption)

**System:** AGENTS-OS v6.5 Swarm Edition  
**Purpose:** Fault-tolerance protocol for agent session crashes, environment resets, or context handoffs.

---

## 📌 Session Resumption Checklist

In the event of a system interrupt or context reset:

1. **State Recovery**:
   - Inspect `.agents/MEMORY.md` and `.agents/task.md` for active session context and last completed steps.
   - Verify uncommitted changes and current branch state.

2. **Active Worktree Audit**:
   - Run `git worktree list` to detect open feature branches under `tmp/worktrees/`.
   - If an active worktree exists, read its latest commit message and `git status`.

3. **Pending Tasks & Review Queue**:
   - Check open PRs or issues via tracker (`gh pr list`, `gh issue list`).
   - Resolve any blocked tasks or human confirmation checkpoints.

---

## 📑 Handoff Receipt Template

```markdown
### 📋 Session Handoff Receipt
- **Timestamp**: {{ TIMESTAMP_ISO }}
- **Active Role**: {{ COORDINATOR | BUILDER | AUDITOR }}
- **Active Worktree**: {{ WORKTREE_PATH }}
- **Branch**: {{ GIT_BRANCH }}
- **Pending Tasks**: {{ PENDING_TASKS }}
- **Last Clean Commit**: {{ GIT_COMMIT_SHA }}
```
