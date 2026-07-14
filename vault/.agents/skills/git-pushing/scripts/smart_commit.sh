#!/bin/bash
set -e

# ── Swarm Triad Handshake Gate ──────────────────────────────────────────────
# Coordinator push is blocked unless a Builder handshake exists for the
# current conversation. Builder/Auditor pushes skip this check.
#
# Override (emergency only): SKIP_HANDSHAKE=1 bash smart_commit.sh "msg"
# ────────────────────────────────────────────────────────────────────────────

ROLE="${SWARM_ROLE:-coordinator}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
VALIDATE_SCRIPT="$PROJECT_ROOT/scripts/validate-handshakes.py"

if [ "$ROLE" = "coordinator" ] || [ "$ROLE" = "gem" ]; then
    if [ "${SKIP_HANDSHAKE:-0}" != "1" ]; then
        echo "🤝 [Handshake Gate] Weryfikacja protokołu uścisku dłoni..."

        if [ ! -f "$VALIDATE_SCRIPT" ]; then
            echo "❌ [Handshake Gate] Brak skryptu: $VALIDATE_SCRIPT"
            echo "   Uruchom: python3 scripts/generate-handshake.py --role builder ..."
            exit 1
        fi

        if ! python3 "$VALIDATE_SCRIPT" --require-roles builder > /tmp/handshake_check.log 2>&1; then
            echo "❌ [Handshake Gate] BRAK lub NIEPOPRAWNY handshake od Buildera!"
            echo "   Szczegóły:"
            cat /tmp/handshake_check.log | sed 's/^/   /'
            echo ""
            echo "   Rozwiązanie: Builder musi uruchomić:"
            echo "   python3 scripts/generate-handshake.py --role builder --conversation-id <UUID> --status SUCCESS ..."
            echo ""
            echo "   Pominięcie (awaryjnie): SKIP_HANDSHAKE=1 bash smart_commit.sh \"msg\""
            exit 1
        fi

        echo "✅ [Handshake Gate] Handshake zweryfikowany. Push dozwolony."
        cat /tmp/handshake_check.log | grep -E "✅|role|status|timestamp" | sed 's/^/   /'
        echo ""
    else
        echo "⚠️  [Handshake Gate] POMINIĘTO (SKIP_HANDSHAKE=1). Push bez weryfikacji."
    fi
fi

# Default commit message if none provided
MESSAGE="${1:-chore: update code}"

# Add all changes
git add .

# Commit with the provided message
git commit -m "$MESSAGE"

# Get current branch name
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Push to remote, setting upstream if needed
git push -u origin "$BRANCH"

echo "✅ Successfully pushed to $BRANCH"
