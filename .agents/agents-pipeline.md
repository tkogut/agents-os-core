# Pipeline Domain Module

> Loaded by Task Router when handling SDLC operations.

## Workflow
1. Issue → `om-prepare-issue` → labeled & scoped
2. Branch → `os-run-builder <name>` → worktree created
3. Implement → `om-auto-implement-spec` → code written
4. Handshake → `validate-handshakes.py` → state verified
5. PR → `om-auto-create-pr` → PR opened with `needs-qa`
6. Review → `om-auto-review-pr` → feedback posted
7. Merge → `om-approve-merge-pr` → merged to main

## Fault Recovery
- Interrupted? → `om-auto-continue-pr <branch>`
- Loop needed? → `om-auto-continue-pr-loop`
- State file: `HANDOFF.md` in worktree root

## Skills Reference
| Skill | Phase | Description |
|---|---|---|
| `om-prepare-issue` | 1 | Triage and label issues |
| `om-auto-implement-spec` | 3 | Transform spec to code |
| `om-auto-create-pr` | 5 | Open PR with QA label |
| `om-auto-review-pr` | 6 | Automated code review |
| `om-approve-merge-pr` | 7 | Final merge approval |
