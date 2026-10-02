#!/bin/bash
# ==============================================================================
# sync-knowledge.sh [sciezka | . | --all]
# Synchronizuje wiedzę ekspercką (.agents/specs/knowledge/) i skilla notebooklm-sync
# z bazy agents-os-core do wskazanego lub bieżącego katalogu.
# ==============================================================================

set -e

CORE_DIR="/home/tkogut/projects/agents-os-core"
KNOWLEDGE_SRC="$CORE_DIR/.agents/specs/knowledge"
GRAPH_SRC="$CORE_DIR/.agents/specs/graph.json"
SKILL_SRC="$CORE_DIR/.agents/skills/notebooklm-sync"

find_project_root() {
    local curr="$(pwd)"
    while [ "$curr" != "/" ]; do
        if [ -d "$curr/.agents" ]; then
            echo "$curr"
            return 0
        fi
        curr="$(dirname "$curr")"
    done
    echo "$(pwd)"
}

sync_to_project() {
    local TARGET_DIR="$1"
    
    if [ ! -d "$TARGET_DIR/.agents" ]; then
        echo "⚠️  W folderze $(basename "$TARGET_DIR") brak katalogu .agents/. Tworzę strukturę..."
        mkdir -p "$TARGET_DIR/.agents"
    fi
    
    echo "🔄 Synchronizacja bazy wiedzy do: $TARGET_DIR"
    
    # 1. Kopiowanie bazy wiedzy
    mkdir -p "$TARGET_DIR/.agents/specs/knowledge"
    cp -u "$KNOWLEDGE_SRC"/*.md "$TARGET_DIR/.agents/specs/knowledge/" 2>/dev/null || cp "$KNOWLEDGE_SRC"/*.md "$TARGET_DIR/.agents/specs/knowledge/"
    
    # 2. Kopiowanie grafu
    if [ -f "$GRAPH_SRC" ]; then
        mkdir -p "$TARGET_DIR/.agents/specs"
        cp "$GRAPH_SRC" "$TARGET_DIR/.agents/specs/graph.json"
    fi
    
    # 3. Kopiowanie skilla notebooklm-sync
    if [ -d "$SKILL_SRC" ]; then
        mkdir -p "$TARGET_DIR/.agents/skills/notebooklm-sync"
        cp -r "$SKILL_SRC"/* "$TARGET_DIR/.agents/skills/notebooklm-sync/"
    fi
    
    echo "✅ Zsynchronizowano pomyślnie bazy wiedzy i skill notebooklm-sync w: $TARGET_DIR"
}

if [ "$1" = "--all" ]; then
    echo "🌐 Masowa synchronizacja ze wszystkimi projektami w ~/projects..."
    for p in /home/tkogut/projects/*; do
        if [ -d "$p" ] && [ "$p" != "$CORE_DIR" ]; then
            sync_to_project "$p"
        fi
    done
    echo "🎉 Zakończono masową synchronizację."
elif [ -n "$1" ] && [ "$1" != "." ]; then
    TARGET="$(realpath "$1")"
    if [ ! -d "$TARGET" ]; then
        echo "❌ BŁĄD: Katalog nie istnieje: $TARGET"
        exit 1
    fi
    sync_to_project "$TARGET"
else
    # Domyślnie bieżący katalog roboczy (pwd)
    TARGET="$(find_project_root)"
    sync_to_project "$TARGET"
fi
