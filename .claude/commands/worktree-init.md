# /worktree-init — Initialize Git Worktree for current task
#
# Usage: /worktree-init
# Claude Code will ask for branch name and create an isolated worktree.

Create a git worktree for the current task following SDLC Phase 2.

Steps:
1. Ask me: "What is the branch name for this task? (e.g. fix-login-bug, feat-user-profile)"
2. Run:
   ```bash
   BRANCH_NAME="feature/<answer>"
   git worktree add tmp/worktrees/$BRANCH_NAME -b $BRANCH_NAME
   echo "✅ Worktree created at: tmp/worktrees/$BRANCH_NAME"
   echo "📁 Switch to: cd tmp/worktrees/$BRANCH_NAME"
   ```
3. Confirm worktree is created and tell me the path.
4. Remind me: all implementation must happen inside this worktree directory.

Rules:
- Branch name must use kebab-case.
- Prefix: `feature/` for new features, `fix/` for bugfixes, `chore/` for maintenance.
- NEVER work on master/main directly.
