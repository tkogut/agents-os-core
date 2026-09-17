#!/usr/bin/env bash
# check_coordinator_role.sh — Safety Gate v6.5 (R-ROLE-01)
# Weryfikuje zakaz bezpośrednich commitów na main/master oraz obecność
# poprawnego Builder handshake przed commitem zmian w kodzie produkcyjnym.

set -e

SWARM_DIR="$(git rev-parse --show-toplevel 2>/dev/null)/.agents/swarm"
CONVERSATION_ID="${1:-${COORDINATOR_SESSION_ID:-}}"
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

SRC_CHANGES=$(git diff --cached --name-only 2>/dev/null | grep -E '^src/|^api/|^ui_dashboard/|^lib/|^app/|^components/' || true)
if [ -z "$SRC_CHANGES" ]; then
    exit 0
fi

echo "🔍 [Safety Gate R-ROLE-01] Wykryto zmiany w kodzie produkcyjnym:"
echo "$SRC_CHANGES"

# 1. Bezwzględny zakaz commitowania kodu na gałęzi main/master
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo "🚨 [R-ROLE-01] COMMIT ZABLOKOWANY NA GAŁĘZI $BRANCH!"
    echo "   Wykryto próbę bezpośredniego commitowania zmian w kodzie na chronionej gałęzi."
    echo "   Wszystkie zmiany w kodzie produkcyjnym MUSZĄ być dokonywane w dedykowanym worktree na gałęzi feature/*."
    exit 1
fi

# 2. Weryfikacja obecności poprawnego Builder handshake
if [ ! -d "$SWARM_DIR" ]; then
    echo "🚨 [R-ROLE-01] COMMIT ZABLOKOWANY: Katalog .agents/swarm/ nie istnieje!"
    echo "   Zmiany w kodzie wymagają delegacji do subagenta Builder i wygenerowania handshake."
    exit 1
fi

BUILDER_HS=$(find "$SWARM_DIR" -name "*_builder_handshake.json" 2>/dev/null | while read -r f; do
    python3 -c "
import json, sys
try:
    with open('$f') as fp:
        d = json.load(fp)
    conv = d.get('conversation_id', '')
    role = d.get('role', '').lower()
    status = d.get('status', '')
    coord_id = '$CONVERSATION_ID'
    if 'builder' in role and status == 'SUCCESS':
        if coord_id and conv == coord_id:
            # Sfałszowany handshake: conversation_id Buildera jest identyczny z Koordynatorem
            sys.exit(1)
        print(conv)
except Exception:
    pass
" 2>/dev/null
done | head -1)

if [ -z "$BUILDER_HS" ]; then
    echo "🚨 [R-ROLE-01] COMMIT ZABLOKOWANY: Brak ważnego Builder handshake w .agents/swarm/!"
    echo "   Wymagany handshake z rolą 'builder' i statusem 'SUCCESS' wygenerowany przez subagenta."
    echo "   Użyj scripts/generate-handshake.py przed commitem."
    exit 1
fi

echo "✅ [Safety Gate R-ROLE-01] Builder handshake zweryfikowany ($BUILDER_HS). Commit dozwolony."
exit 0
