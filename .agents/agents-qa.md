# QA Domain Module

> Loaded by Task Router for quality assurance operations.

## QA Gate Policy
- **Hard Lock**: PR tagged `needs-qa` cannot auto-merge
- **Approval Required**: Manual `qa-approved` label
- **Visual Proof**: UI changes require screenshot evidence

## Gate Sequence
```
lint → typecheck → test → visual-proof → human-review
```

## Commands
| Gate | Command | Required |
|---|---|---|
| Lint | `shellcheck scripts/*.sh` | Yes |
| Typecheck | `python3 -m py_compile scripts/*.py` | No |
| Test | `python3 scripts/validate-handshakes.py` | Yes |
| Visual | Browser screenshot → PR comment | For UI only |

## Auditor Rules
1. Auditor role = `gemini-low` (cost-optimized)
2. Can BLOCK any merge via handshake rejection
3. Checks: lint results, test pass, handshake validity
4. Anomaly detection: flag unusual file patterns

## Skills Reference
| Skill | Description |
|---|---|
| `om-auto-qa-pr` | Full QA pass on PR |
| `om-code-review` | Deep code review |
| `om-integration-tests` | Run integration test suite |
| `om-verify-in-repo` | Verify changes match spec |
