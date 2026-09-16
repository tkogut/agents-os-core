#!/usr/bin/env bash
# PreCompact hook - persist swarm state to disk BEFORE context is compacted.
#
# Compaction summarises the transcript; anything not written down is lost.
# This writes a single rolling snapshot file (not a growing pile) so a
# post-compaction session can re-read exact state instead of guessing.
# Never blocks: always exits 0.
set -uo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
OUT="$ROOT/.agents/swarm/precompact-snapshot.md"
mkdir -p "$(dirname "$OUT")" 2>/dev/null || exit 0

{
    echo "# PreCompact Snapshot (auto-generated, not committed)"
    echo
    echo "- generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "- branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null)"
    echo "- head: $(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null)"
    echo
    echo '## git status --short'
    echo '```'
    git -C "$ROOT" status --short 2>/dev/null
    echo '```'
    echo
    echo '## .agents/task.md'
    echo '```markdown'
    cat "$ROOT/.agents/task.md" 2>/dev/null
    echo '```'
    echo
    echo '## .agents/MEMORY.md (last 30 lines)'
    echo '```markdown'
    tail -30 "$ROOT/.agents/MEMORY.md" 2>/dev/null
    echo '```'
} > "$OUT" 2>/dev/null

echo "[SWARM] PreCompact snapshot written: .agents/swarm/precompact-snapshot.md"
exit 0
