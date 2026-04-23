#!/bin/bash
# ==============================================================================
# AGENTS-OS v3.2 SWARM EDITION - UNIVERSAL INSTALLER
# Architekt: Antigravity Orchestrator & User tkogut
# ==============================================================================

set -e

echo "🚀 Rozpoczynam instalację AGENTS-OS v3.2 Swarm Edition..."

# 1. Zależności systemu
if ! command -v snap &> /dev/null; then
  echo "📦 Instalacja snapd..."
  sudo apt update && sudo apt install -y snapd
fi

if ! command -v gemini &> /dev/null; then
  echo "📦 Instalacja gemini-cli..."
  sudo snap install gemini-cli
fi

# 2. Instalacja wtyczki Caveman
echo "🛡️ Integracja z modułem kompresji tożsamości (Caveman)..."
gemini extensions install https://github.com/JuliusBrussee/caveman || echo "UWAGA: Wtyczka caveman mogła być już zainstalowana."

# 3. Kopiowanie The Vault
GEMINI_DIR="$HOME/.gemini"
VAULT_DIR="$GEMINI_DIR/antigravity/templates/v3.2-swarm"

echo "✨ Deploy: The Template Vault (Złoty Standard)..."
mkdir -p "$VAULT_DIR"
cp -ra ./vault/. "$VAULT_DIR/"

# 4. Globalne Umiejętności (Skille)
echo "🧠 Wdrażanie systemów automatyzacji (Swarm Bootstrapper)..."
mkdir -p "$GEMINI_DIR/antigravity/skills/swarm-bootstrapper"
cp -ra ./global_skills/swarm-bootstrapper/. "$GEMINI_DIR/antigravity/skills/swarm-bootstrapper/"

# 5. CLI Shortcut (os-init)
echo "⚙️ Rejestracja globalnego skrótu CLI (os-init)..."
if [ -f "./os-init" ]; then
    sudo cp ./os-init /usr/local/bin/os-init
    sudo chmod +x /usr/local/bin/os-init
else
    echo "⚠️ Nie odnaleziono pliku os-init w repozytorium!"
fi

# 6. Naprawa izolacji (Snap Guard)
SNAP_GEMINI_DIR="$HOME/snap/gemini-cli/current/.gemini"
if [ -d "$HOME/snap/gemini-cli" ]; then
    echo "🔗 Aktywacja Snap Sandbox Guard..."
    mkdir -p "$(dirname "$SNAP_GEMINI_DIR")"
    ln -sfn "$GEMINI_DIR" "$SNAP_GEMINI_DIR"
fi

echo "===================================================================="
echo "✅ DEPLOY ZAKOŃCZONY SUKCESEM: SYSTEM AGENTS-OS GOTOWY."
echo "Uruchom komendę: 'os-init nazwa-mojego-projektu' aby wystartować."
echo "===================================================================="
