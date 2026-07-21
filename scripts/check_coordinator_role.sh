#!/usr/bin/env bash
# check_coordinator_role.sh — Safety Gate v6.1 (R-ROLE-01)
# Weryfikuje obecność poprawnego Builder handshake przed commitem zmian w src/

SWARM_DIR="$(git rev-parse --show-toplevel 2>/dev/null)/.agents/swarm"
CONVERSATION_ID="${1:-${COORDINATOR_SESSION_ID:-}}"

SRC_CHANGES=$(git diff --cached --name-only 2>/dev/null | grep -E '^src/|^api/' || true)
if [ -z "$SRC_CHANGES" ]; then
    exit 0
fi

echo "🔍 [Safety Gate R-ROLE-01] Wykryto zmiany w src/:"
echo "$SRC_CHANGES"

if [ -z "$CONVERSATION_ID" ]; then
    echo "⚠️  COORDINATOR_SESSION_ID nieustawiony — Safety Gate pominięty (tryb developerski)."
    exit 0
fi

BUILDER_HS=$(find "$SWARM_DIR" -name "*_builder_handshake.json" 2>/dev/null | while read f; do
    python3 -c "
import json, sys
with open('$f') as fp:
    d = json.load(fp)
conv = d.get('conversation_id', '')
role = d.get('role', '').lower()
status = d.get('status', '')
if 'builder' in role and status == 'SUCCESS' and conv != '$CONVERSATION_ID':
    print(conv)
" 2>/dev/null
done | head -1)

if [ -z "$BUILDER_HS" ]; then
    echo "🚨 [R-ROLE-01] COMMIT ZABLOKOWANY: Brak ważnego Builder handshake od subagenta!"
    echo "   Zmiany w src/ wymagają delegacji do subagenta Builder (invoke_subagent)."
    exit 1
fi

echo "✅ [Safety Gate R-ROLE-01] Builder handshake z subagenta wykryty ($BUILDER_HS). Commit dozwolony."
exit 0
