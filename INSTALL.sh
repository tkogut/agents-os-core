#!/bin/bash
# ==============================================================================
# AGENTS-OS v4.0 SWARM EDITION - UNIVERSAL INSTALLER
# Architekt: Antigravity Orchestrator & User tkogut
# ==============================================================================

set -e

echo "🚀 Rozpoczynam instalację AGENTS-OS v4.0 Swarm Edition..."

# 1. Zależności systemu
if ! command -v snap &> /dev/null; then
  echo "📦 Inicjalizacja snapd..."
  # Pomijamy apt-get update jeśli nie mamy sudo bez hasła, ale informujemy użytkownika
  if sudo -n apt update &>/dev/null; then
      sudo apt install -y snapd
  else
      echo "⚠️ Pomijam instalację snapd (brak bezhasłowego sudo). Upewnij się, że snap jest obecny."
  fi
fi

if command -v agy &> /dev/null; then
    echo "Antigravity CLI (agy) jest już zainstalowane. Pomijam pobieranie."
else
    echo "Pobieranie i instalacja Antigravity CLI (Go Binary)..."
    curl -fL -o antigravity.tar.gz "https://antigravity.google/download/linux-x64.tar.gz"
    tar -xzf antigravity.tar.gz
    if sudo -n mv agy /usr/local/bin/ 2>/dev/null; then
        echo "✓ agy zainstalowany w /usr/local/bin"
    else
        mkdir -p "$HOME/.local/bin"
        mv agy "$HOME/.local/bin/"
        echo "✓ agy zainstalowany w $HOME/.local/bin"
    fi
    rm -f antigravity.tar.gz
fi

if ! command -v gh &> /dev/null; then
  echo "📦 Instalacja github-cli (gh)..."
  if sudo -n snap install gh --classic &>/dev/null; then
      echo "✓ gh zainstalowany"
  else
      echo "⚠️ Nie udało się zainstalować gh. Zainstaluj ręcznie."
  fi
fi

echo "📦 Instalacja zależności Python (GitPython, PyGithub)..."
pip3 install GitPython PyGithub --break-system-packages || pip3 install GitPython PyGithub || echo "UWAGA: Problemy z instalacją pip, użyj środowiska wirtualnego jeśli wymagane."

# 2. Integracja z modułem kompresji tożsamości (Caveman)
echo "🛡️ Integracja z modułem kompresji tożsamości (Caveman)..."
# Pomijamy interaktywne pobieranie z agy jeśli nie jesteśmy zalogowani, nie wieszamy skryptu
if command -v agy &>/dev/null && agy auth status &>/dev/null; then
    timeout 5 agy extensions install https://github.com/JuliusBrussee/caveman || echo "UWAGA: Wtyczka caveman mogła być już zainstalowana."
else
    echo "⚠️ Pomijam agy extensions install (brak autoryzacji). Zostanie uruchomione po zalogowaniu."
fi

# 3. Kopiowanie The Vault
AGY_DIR="$HOME/.antigravity"
VAULT_DIR="$AGY_DIR/templates/v4.0-swarm"

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
npx -y antigravity-awesome-skills --path .agents/skills --risk safe,none

echo "⚙️ Rejestracja globalnego skrótu CLI (os-init)..."
if [ -f "./os-init" ]; then
    if sudo -n cp ./os-init /usr/local/bin/os-init 2>/dev/null; then
        sudo -n chmod +x /usr/local/bin/os-init
        echo "✓ Skrót zarejestrowany w /usr/local/bin/os-init"
    else
        echo "⚠️ Brak uprawnień sudo. Rejestracja w ~/.local/bin/os-init..."
        mkdir -p "$HOME/.local/bin"
        cp ./os-init "$HOME/.local/bin/os-init"
        chmod +x "$HOME/.local/bin/os-init"
        echo "✓ Skrót zarejestrowany w $HOME/.local/bin/os-init"
    fi
else
    echo "⚠️ Nie odnaleziono pliku os-init w repozytorium!"
fi

echo "===================================================================="
echo "✅ DEPLOY ZAKOŃCZONY SUKCESEM: SYSTEM AGENTS-OS GOTOWY."
echo "Uruchom komendę: 'os-init nazwa-mojego-projektu' aby wystartować."
echo "===================================================================="
