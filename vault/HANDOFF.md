# 🛡️ Cezar Runtime HANDOFF Template (Fault-Tolerance & Session Resumption)

**System:** mms4tk + Hermes Agent Swarm  
**Purpose:** Fault-tolerance protocol for agent session crashes, server restarts, or context handoffs.

---

## 📌 Session Resumption Checklist

In the event of a system interrupt or context reset:

1. **State Recovery**:
   - Inspect `.agents/swarm/logs.db` for the last recorded daemon cycle and strategy state (`BASE_MODE` vs `SCOUT_MODE`).
   - Query `/api/v1/state` and `/api/v1/daemon/status`.

2. **Active Worktree Audit**:
   - Run `git worktree list` to detect open feature branches under `tmp/worktrees/`.
   - If an active worktree exists, read its latest commit message and `git status`.

3. **Pending Webhook & Kanban Queue**:
   - Query `kanban.db` tasks in `/docker/hermes-agent/data/kanban.db`.
   - Resolve any blocked HITL cards via `POST /api/v1/hermes/hitl_resolve`.

---

## 📑 Handoff Receipt Template

```markdown
### 📋 Session Handoff Receipt
- **Timestamp**: {{ TIMESTAMP_ISO }}
- **Active State**: {{ BASE_MODE | SCOUT_MODE }}
- **Current Leverage**: {{ LEVERAGE_MULTIPLIER }}
- **Trading Symbol**: {{ MMS4_SYMBOL }}
- **Pending Tasks**: {{ PENDING_KANBAN_TASKS }}
- **Last Clean Commit**: {{ GIT_COMMIT_SHA }}
```
