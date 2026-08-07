# HANDOFF — Agent State Transfer Document

> Template for Cezar Runtime fault-tolerance.

## Session Info
- **Conversation ID**: `<auto-fill>`
- **Role**: `<coordinator|builder|auditor>`
- **Timestamp**: `<ISO-8601>`
- **Status**: `<in-progress|completed|failed|timeout>`

## Current Task
- **Issue**: `#<number>`
- **Branch**: `<branch-name>`
- **Worktree**: `tmp/worktrees/<branch-name>`

## Progress
- [ ] Phase 1: Issue Triage
- [ ] Phase 2: Branch & Worktree
- [ ] Phase 3: Implementation
- [ ] Phase 4: Handshake
- [ ] Phase 5: QA Gate
- [ ] Phase 6: PR Merge

## State Snapshot
### Files Modified
- `<path>`: `<description>`

### Pending Actions
1. `<next action>`

### Blockers
- `<none | description>`

## Recovery Instructions
If this session was interrupted, resume with:
```bash
om-auto-continue-pr <branch-name>
```
