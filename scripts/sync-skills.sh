#!/bin/bash
# ==============================================================================
# AGENTS-OS v5.0 — Skills Synchronizer
# Synchronizuje skille między global_skills/ a vault/.agents/skills/
# w celu uniknięcia rozbieżności wersji w szablonie instalacyjnym.
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

GLOBAL_DIR="$REPO_DIR/global_skills"
VAULT_SKILLS_DIR="$REPO_DIR/vault/.agents/skills"

# Lista skilli do synchronizacji z global_skills/ do vault/.agents/skills/
# (Skille, które deweloperzy edytują w global_skills i powinny trafić do szablonu startowego)
SHARED_SKILLS=(
    "vps-ops"
    "n8n-ops"
    "skill-rebuild"
)

echo "🔄 Rozpoczynam synchronizację skilli Agents-OS..."

for skill in "${SHARED_SKILLS[@]}"; do
    src="$GLOBAL_DIR/$skill"
    dst="$VAULT_SKILLS_DIR/$skill"

    if [ -d "$src" ]; then
        echo "   -> Synchronizuję: $skill"
        # Usuń starą wersję w vault, jeśli istnieje
        if [ -d "$dst" ]; then
            rm -rf "$dst"
        fi
        # Skopiuj na świeżo
        cp -ra "$src" "$dst"
        echo "      ✓ Skopiowano do vault"
    else
        echo "   ⚠️ Ostrzeżenie: Skill '$skill' nie istnieje w global_skills/ ($src)"
    fi
done

echo "✅ Synchronizacja zakończona pomyślnie."
