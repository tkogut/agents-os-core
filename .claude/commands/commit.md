# /commit — Caveman-style Atomic Commit
#
# Usage: /commit
# Creates a Conventional Commit ≤50 chars with SWARM_ROLE=builder.

Generate and execute an atomic caveman-style commit.

Steps:
1. Show staged changes:
   ```bash
   git diff --cached --stat
   ```
2. If nothing staged, ask: "Stage all changes? (git add -A)" — if yes, run it.
3. Suggest a commit message based on staged changes (Conventional Commits format):
   - `feat: <description>` — new feature
   - `fix: <description>` — bugfix
   - `chore: <description>` — maintenance/config
   - `refactor: <description>` — refactoring
   - `docs: <description>` — documentation
   - Rule: ≤50 chars total.
4. Ask me to confirm or adjust the message.
5. Execute:
   ```bash
   SWARM_ROLE=builder git commit -m "<confirmed message>"
   ```
6. Show the commit hash and summary.

Rules:
- Never use `git commit -m "wip"` or generic messages.
- No commits with unstaged test files or debug artifacts.
- Pre-commit hook will enforce SWARM_ROLE=builder automatically.
