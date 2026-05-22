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

if command -v agy &> /dev/null; then
    echo "Antigravity CLI (agy) jest już zainstalowane. Pomijam pobieranie."
else
    echo "Pobieranie i instalacja Antigravity CLI (Go Binary)..."
    curl -fL -o antigravity.tar.gz "https://antigravity.google/download/linux-x64.tar.gz"
    tar -xzf antigravity.tar.gz
    sudo mv agy /usr/local/bin/
    rm antigravity.tar.gz
fi

if ! command -v gh &> /dev/null; then
  echo "📦 Instalacja github-cli (gh)..."
  sudo snap install gh --classic
fi

echo "📦 Instalacja zależności Python (GitPython, PyGithub)..."
pip3 install GitPython PyGithub || echo "UWAGA: Problemy z instalacją pip, użyj środowiska wirtualnego jeśli wymagane."

# 2. Instalacja wtyczki Caveman (pominięta/zaktualizowana dla agy)
echo "🛡️ Integracja z modułem kompresji tożsamości (Caveman)..."
agy extensions install https://github.com/JuliusBrussee/caveman || echo "UWAGA: Wtyczka caveman mogła być już zainstalowana."

# 3. Kopiowanie The Vault
AGY_DIR="$HOME/.antigravity"
VAULT_DIR="$AGY_DIR/templates/v3.2-swarm"

echo "✨ Deploy: The Template Vault (Złoty Standard)..."
mkdir -p "$VAULT_DIR"
cp -ra ./vault/. "$VAULT_DIR/"

# 4. Globalne Umiejętności (Skille)
echo "🧠 Wdrażanie systemów automatyzacji (Swarm Bootstrapper)..."
mkdir -p "$AGY_DIR/skills/swarm-bootstrapper"
cp -ra ./global_skills/swarm-bootstrapper/. "$AGY_DIR/skills/swarm-bootstrapper/"

mkdir -p "$AGY_DIR/skills/browser-connectivity"
cp -ra ./global_skills/browser-connectivity/. "$AGY_DIR/skills/browser-connectivity/"

mkdir -p "$AGY_DIR/skills/github-orchestrator"
cp -ra ./global_skills/github-orchestrator/. "$AGY_DIR/skills/github-orchestrator/"

mkdir -p "$AGY_DIR/skills/logic-auditor"
cp -ra ./global_skills/logic-auditor/. "$AGY_DIR/skills/logic-auditor/"

mkdir -p "$AGY_DIR/skills/rebuild-skill"
cp -ra ./global_skills/rebuild-skill/. "$AGY_DIR/skills/rebuild-skill/"

echo "⚙️ Integracja Awesome Skills..."
npx antigravity-awesome-skills --path .agents/skills --risk safe,none

echo "⚙️ Rejestracja globalnego skrótu CLI (os-init)..."
if [ -f "./os-init" ]; then
    sudo cp ./os-init /usr/local/bin/os-init
    sudo chmod +x /usr/local/bin/os-init
else
    echo "⚠️ Nie odnaleziono pliku os-init w repozytorium!"
fi

echo "===================================================================="
echo "✅ DEPLOY ZAKOŃCZONY SUKCESEM: SYSTEM AGENTS-OS GOTOWY."
echo "Uruchom komendę: 'os-init nazwa-mojego-projektu' aby wystartować."
echo "===================================================================="