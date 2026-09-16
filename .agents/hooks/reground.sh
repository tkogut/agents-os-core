#!/usr/bin/env bash
# UserPromptSubmit hook - cheap swarm re-grounding.
#
# Fires ONCE per user turn (not per tool call) and prints a single compact line
# that Claude Code appends to context. Budget is deliberately ~1 line: the whole
# point of preferring this over a per-tool-call injector is that it must stay
# too cheap to argue about. Never blocks: always exits 0.
set -uo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
TASK="$ROOT/.agents/task.md"
[ -f "$TASK" ] || exit 0

BRANCH=$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')
DIRTY=$(git -C "$ROOT" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
TITLE=$(grep -m1 '^# ' "$TASK" 2>/dev/null | sed 's/^# //')
OPEN=$(grep -cE '^[[:space:]]*- \[ \]' "$TASK" 2>/dev/null || true)
DONE=$(grep -cE '^[[:space:]]*- \[x\]' "$TASK" 2>/dev/null || true)

printf '[SWARM] branch=%s dirty=%s | task: %s | checklist: %s done / %s open | SSOT: .agents/task.md + .agents/MEMORY.md\n' \
    "$BRANCH" "$DIRTY" "${TITLE:-<none>}" "${DONE:-0}" "${OPEN:-0}"
exit 0
