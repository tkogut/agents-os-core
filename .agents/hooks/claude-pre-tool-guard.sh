#!/usr/bin/env bash
# claude-pre-tool-guard.sh — Claude Code PreToolUse Safety Hook
# Part of AGENTS-OS v6.5 Swarm Governance (R-ROLE-01)
# Blocks direct code writes on main/master branches.

set -e

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

# If on a protected branch (main/master)
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    python3 -c "
import sys, json, os

ALLOWED_EXTENSIONS = {'.md', '.json', '.yaml', '.yml', '.txt', '.csv', '.lock'}
ALLOWED_DIRS = {'.agents', 'plans', 'docs', 'vault', '.claude', '.ai'}
ALLOWED_BASENAMES = {'.gitattributes', '.gitignore', '.dockerignore', 'LICENSE', 'VERSION'}

try:
    data = json.load(sys.stdin)
    tool_input = data.get('tool_input', {}) or data.get('input', {})
    file_path = tool_input.get('file_path', '') or tool_input.get('path', '')
    if not file_path:
        sys.exit(0)

    norm_path = os.path.normpath(file_path)
    base_name = os.path.basename(norm_path)
    _, ext = os.path.splitext(norm_path)

    if base_name in ALLOWED_BASENAMES or ext.lower() in ALLOWED_EXTENSIONS:
        sys.exit(0)

    path_parts = norm_path.split(os.sep)
    if any(d in path_parts for d in ALLOWED_DIRS):
        sys.exit(0)

    # Any code modification on main/master is rejected
    sys.stderr.write(
        f'\n🛑 [AGENTS-OS Swarm Guard] DIRECT WRITE FORBIDDEN ON {norm_path}!\n'
        f'   You are on branch \'\$BRANCH\'. Direct code modification on main/master is prohibited.\n'
        f'   Please initialize a worktree using /worktree-init or switch to a feature branch.\n\n'
    )
    sys.exit(1)
except Exception:
    sys.exit(0)
"
fi

exit 0
