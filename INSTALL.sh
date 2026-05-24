#!/bin/bash
# ==============================================================================
# AGENTS-OS v4.1 SWARM EDITION - UNIVERSAL INSTALLER
# Architekt: Antigravity Orchestrator & User tkogut
# ==============================================================================

set -e

echo "🚀 Rozpoczynam instalację AGENTS-OS v4.1 Swarm Edition..."

# 1. Zależności systemu
if ! command -v snap &> /dev/null; then
  echo "📦 Inicjalizacja snapd..."
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
  echo "📦 Instalacja github-cli (gh) przez APT..."
  if sudo -n true 2>/dev/null; then
      sudo apt-get update -y &>/dev/null
      sudo apt-get install -y curl gpg &>/dev/null
      sudo mkdir -p /etc/apt/keyrings
      sudo chmod 0755 /etc/apt/keyrings
      curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null
      sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
      echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
      sudo apt-get update -y &>/dev/null
      sudo apt-get install -y gh &>/dev/null
      echo "✓ gh zainstalowany przez APT"
  else
      echo "⚠️ Brak bezhasłowego sudo. Próba instalacji interaktywnej gh..."
      if sudo apt-get update && sudo apt-get install -y curl gpg && \
         sudo mkdir -p /etc/apt/keyrings && sudo chmod 0755 /etc/apt/keyrings && \
         curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
         sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg && \
         echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
         sudo apt-get update && sudo apt-get install -y gh; then
          echo "✓ gh zainstalowany przez APT"
      else
          echo "⚠️ Nie udało się zainstalować gh. Zainstaluj ręcznie."
      fi
  fi
fi

echo "📦 Konfiguracja izolowanego środowiska Python (venv)..."
if python3 -m venv "$HOME/.antigravity/venv" 2>/dev/null; then
    "$HOME/.antigravity/venv/bin/pip" install --upgrade pip &>/dev/null || true
    echo "📦 Instalacja zależności Python (GitPython, PyGithub) w venv..."
    "$HOME/.antigravity/venv/bin/pip" install GitPython PyGithub
else
    echo "⚠️ Nie udało się utworzyć venv. Próba instalacji python3-venv..."
    if sudo -n true 2>/dev/null; then
        sudo apt-get update -y &>/dev/null
        sudo apt-get install -y python3-venv &>/dev/null
    else
        sudo apt-get update && sudo apt-get install -y python3-venv
    fi
    
    if python3 -m venv "$HOME/.antigravity/venv" 2>/dev/null; then
        "$HOME/.antigravity/venv/bin/pip" install --upgrade pip &>/dev/null || true
        echo "📦 Instalacja zależności Python (GitPython, PyGithub) w venv..."
        "$HOME/.antigravity/venv/bin/pip" install GitPython PyGithub
    else
        echo "⚠️ Nie można utworzyć venv. Instalacja globalna bibliotek Python..."
        pip3 install GitPython PyGithub --break-system-packages || pip3 install GitPython PyGithub || echo "⚠️ Nie udało się zainstalować zależności Pythona."
    fi
fi

# 2. Integracja z modułem kompresji tożsamości (Caveman)
echo "🛡️ Integracja z modułem kompresji tożsamości (Caveman)..."

# 3. Kopiowanie The Vault
AGY_DIR="$HOME/.antigravity"
VAULT_DIR="$AGY_DIR/templates/v4.1-swarm"

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

echo "⚙️ Rejestracja skryptu os-init-run (wykonywalny backend)..."
if [ -f "./os-init" ]; then
    if sudo -n cp ./os-init /usr/local/bin/os-init-run 2>/dev/null; then
        sudo -n chmod +x /usr/local/bin/os-init-run
        echo "✓ Backend zarejestrowany w /usr/local/bin/os-init-run"
    else
        echo "⚠️ Brak uprawnień sudo. Rejestracja w ~/.local/bin/os-init-run..."
        mkdir -p "$HOME/.local/bin"
        cp ./os-init "$HOME/.local/bin/os-init-run"
        chmod +x "$HOME/.local/bin/os-init-run"
        echo "✓ Backend zarejestrowany w $HOME/.local/bin/os-init-run"
    fi
else
    echo "⚠️ Nie odnaleziono pliku os-init w repozytorium!"
fi

echo "⚙️ Rejestracja shell function os-init w ~/.bashrc.d/antigravity..."
SHELL_RC="$HOME/.bashrc.d/antigravity"
if ! grep -q 'os-init()' "$SHELL_RC" 2>/dev/null; then
    echo "⚠️ Shell function os-init nie znaleziona. Dodaj ją ręcznie lub uruchom skrypt ponownie."
else
    echo "✓ Shell function os-init() jest zarejestrowana w $SHELL_RC"
fi

echo ""
echo "ℹ️  Aby aktywować os-init w bieżącym terminalu:"
echo "   source ~/.bashrc.d/antigravity"

# 5. Autoryzacja i logowanie do usług CLI (tylko w trybie interaktywnym)
if [ -t 0 ]; then
    echo "🔑 Wykryto terminal interaktywny. Konfiguracja autoryzacji CLI..."
    
    # Logowanie GitHub CLI
    if command -v gh &> /dev/null; then
        if ! gh auth status &>/dev/null; then
            echo "🐙 Logowanie do GitHub CLI (wymagane do synchronizacji repozytoriów):"
            gh auth login || echo "⚠️ Pominięto autoryzację GitHub."
        else
            echo "✓ GitHub CLI jest już zalogowany."
        fi
    fi
    
    # Logowanie Antigravity CLI
    if command -v agy &> /dev/null; then
        echo "🪐 Uruchamianie logowania do Antigravity CLI..."
        # Wywołanie agy bez parametrów lub wymuszające logowanie
        # (Większość wersji agy automatycznie wyzwala flow logowania przy pierwszym użyciu)
        agy --version &>/dev/null || echo "⚠️ Nie udało się sprawdzić statusu logowania agy."
        
        echo "🛡️ Instalacja wtyczki Caveman w agy..."
        agy plugin install caveman || echo "⚠️ Nie udało się zainstalować wtyczki Caveman (zaloguj się i zainstaluj ręcznie: agy plugin install caveman)."
    fi
else
    echo "🖥️ Środowisko nieinteraktywne. Pomijam autoryzację CLI (wykonaj ręcznie po instalacji)."
fi

echo "===================================================================="
echo "✅ DEPLOY ZAKOŃCZONY SUKCESEM: SYSTEM AGENTS-OS GOTOWY."
echo ""
echo "Następne kroki:"
echo "  1. Załaduj shell config:  source ~/.bashrc.d/antigravity"
echo "  2. Utwórz projekt:         os-init nazwa-projektu"
echo ""
echo "  Komenda os-init automatycznie:"
echo "    ✓ Tworzy strukturę folderów (Złoty Standard)"
echo "    ✓ Tworzy repo na GitHubie (tkogut/nazwa-projektu)"
echo "    ✓ Robi initial commit i push"
echo "    ✓ Otwiera Antigravity IDE w folderze projektu"
echo "    ✓ Przechodzi do folderu projektu w terminalu (cd)"
echo "===================================================================="
