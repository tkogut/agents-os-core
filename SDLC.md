# SDLC — Software Development Lifecycle (AGENTS-OS v6.5)

> Source of Truth for agent-driven development workflows.

## Lifecycle Phases

```
Issue → Branch → Worktree → Implementation → Handshake → QA Gate → PR Merge
```

### Phase 1: Issue Triage
- **Trigger**: New issue or `/om-prepare-issue`
- **Agent**: Coordinator (Gemini)
- **Output**: Labeled, prioritized issue with acceptance criteria
- **Skills**: `om-auto-manage-issues`, `om-prepare-issue`

### Phase 2: Branch & Worktree
- **Trigger**: Issue assigned to Builder
- **Agent**: Builder (Claude Opus / Claude Code VS Code)
- **Output**: Isolated git worktree at `tmp/worktrees/<branch-name>`
- **Script**: `os-run-builder <branch-name>`
- **Claude Code**: Use `/worktree-init` slash command or run manually:
  ```bash
  git worktree add tmp/worktrees/feature/<branch> -b feature/<branch>
  ```

### Phase 3: Implementation
- **Trigger**: Worktree ready
- **Agent**: Builder (Claude)
- **Protocol**: `[PLAN → HANDOFF → NOTIFY]`
- **Commit Policy**: Atomic (1 commit per unit of work)
- **Skills**: `om-auto-implement-spec`, `om-auto-fix-issue`, `om-fix`

### Phase 4: Handshake
- **Trigger**: Implementation complete
- **Agent**: Builder → Auditor
- **Output**: `<conversation_id>_<role>_handshake.json` in `.agents/swarm/`
- **Validation**: `python3 scripts/validate-handshakes.py`

### Phase 5: QA Gate
- **Trigger**: PR created with `needs-qa` label
- **Agent**: Auditor (Gemini-Low)
- **Gates**: lint → typecheck → test → visual proof
- **Policy**: NO auto-merge. Requires `qa-approved` flag.
- **Skills**: `om-auto-qa-pr`, `om-auto-review-pr`, `om-code-review`

### Phase 6: PR Merge
- **Trigger**: `qa-approved` label set
- **Agent**: Coordinator (approval) + Builder (merge)
- **Skills**: `om-approve-merge-pr`, `om-merge-buddy`
- **Post-merge**: `om-auto-update-changelog`, `om-followup-issue-from-pr`

## Hard Rules
1. Coordinator NEVER writes code.
2. Builder ALWAYS operates in worktrees.
3. Auditor can BLOCK any merge.
4. Every PR requires visual proof for UI changes.
5. HANDOFF.md must exist before phase transition.
