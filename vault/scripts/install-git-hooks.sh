#!/usr/bin/env bash
# install-git-hooks.sh — Installs pre-commit hook enforcing R-ROLE-01 Swarm Governance
set -e

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"

if [ ! -d "$HOOKS_DIR" ]; then
    echo "⚠️  .git/hooks nie istnieje w $REPO_ROOT. Pomijam instalację."
    exit 0
fi

PRE_COMMIT="$HOOKS_DIR/pre-commit"

cat << 'EOF' > "$PRE_COMMIT"
#!/usr/bin/env bash
# AGENTS-OS Swarm Governance Pre-Commit Gate
SCRIPT_PATH="$(git rev-parse --show-toplevel 2>/dev/null)/scripts/check_coordinator_role.sh"
if [ -f "$SCRIPT_PATH" ]; then
    bash "$SCRIPT_PATH"
fi
EOF

chmod +x "$PRE_COMMIT"
echo "✅ Zainstalowano pre-commit hook Swarm Governance w $PRE_COMMIT"
