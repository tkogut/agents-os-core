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

# 1. Synchronizacja skilli lokalnych z global_skills/
for skill in "${SHARED_SKILLS[@]}"; do
    src="$GLOBAL_DIR/$skill"
    dst="$VAULT_SKILLS_DIR/$skill"

    if [ -d "$src" ]; then
        echo "   [local] -> Synchronizuję: $skill"
        if [ -d "$dst" ]; then
            rm -rf "$dst"
        fi
        cp -ra "$src" "$dst"
    else
        echo "   ⚠️ Ostrzeżenie: Skill '$skill' nie istnieje w global_skills/ ($src)"
    fi
done

# 2. Synchronizacja skilli z wtyczki caveman
CAVEMAN_PLUGIN_DIR="$HOME/.gemini/config/plugins/caveman/skills"
if [ -d "$CAVEMAN_PLUGIN_DIR" ]; then
    echo "🔄 Synchronizacja skilli z wtyczki Caveman..."
    for skill_path in "$CAVEMAN_PLUGIN_DIR"/*; do
        if [ -d "$skill_path" ]; then
            skill_name=$(basename "$skill_path")
            dst="$VAULT_SKILLS_DIR/$skill_name"
            echo "   [caveman] -> Synchronizuję: $skill_name"
            if [ -d "$dst" ]; then
                rm -rf "$dst"
            fi
            cp -ra "$skill_path" "$dst"
        fi
    done
else
    echo "⚠️ Ostrzeżenie: Folder wtyczki Caveman ($CAVEMAN_PLUGIN_DIR) nie istnieje. Pomijam."
fi

echo "✅ Synchronizacja zakończona pomyślnie."
