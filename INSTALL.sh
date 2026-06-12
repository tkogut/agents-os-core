#!/bin/bash
# ==============================================================================
# AGENTS-OS v5.0 SWARM EDITION - UNIVERSAL INSTALLER
# Architekt: Antigravity Orchestrator & User tkogut
# ==============================================================================

set -e

echo "🚀 Rozpoczynam instalację AGENTS-OS v5.0 Swarm Edition..."

# 1. Zależności systemu

if command -v agy &> /dev/null || [ -f "/usr/local/bin/agy" ] || [ -f "$HOME/.local/bin/agy" ]; then
    echo "Antigravity CLI (agy) jest już zainstalowane. Pomijam pobieranie."
else
    echo "Pobieranie i instalacja Antigravity CLI (Go Binary)..."
    # Dynamiczne pobranie adresu URL z oficjalnego manifestu wydań dla linux_amd64
    CLI_URL=$(curl -fsSL "https://antigravity-cli-auto-updater-974169037036.us-central1.run.app/manifests/linux_amd64.json" | grep -o '"url": *"[^"]*"' | sed 's/"url": *//;s/"//g')
    if [ -z "$CLI_URL" ]; then
        # Fallback w przypadku problemów z manifestem
        CLI_URL="https://storage.googleapis.com/antigravity-public/antigravity-cli/1.0.2-6109799369277440/linux-x64/cli_linux_x64.tar.gz"
    fi
    curl -fL -o antigravity.tar.gz "$CLI_URL"
    tar -xzf antigravity.tar.gz
    mv antigravity agy
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
VAULT_DIR="$AGY_DIR/templates/v5.0-swarm"

# Czyszczenie starych wersji szablonów w celu zachowania czystości systemu
echo "🧹 Czyszczenie starych szablonów..."
if [ -d "$AGY_DIR/templates/v4.2-swarm" ]; then
    rm -rf "$AGY_DIR/templates/v4.2-swarm"
    echo "   ✓ Usunięto przestarzały szablon v4.2-swarm"
fi

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

mkdir -p "$AGY_DIR/skills/skill-rebuild"
cp -ra ./global_skills/skill-rebuild/. "$AGY_DIR/skills/skill-rebuild/"

echo "⚙️ Pobieranie katalogu skilli RAG..."
mkdir -p "$VAULT_DIR/.agents/specs"
curl -fsSL -o "$VAULT_DIR/.agents/specs/awesome-skills-catalog.md" "https://raw.githubusercontent.com/sickn33/antigravity-awesome-skills/main/CATALOG.md" || echo "⚠️  Nie udało się pobrać katalogu skilli."

echo "⚙️ Rejestracja narzędzi systemowych (backend)..."
if [ -f "./os-init" ]; then
    if sudo -n cp ./os-init /usr/local/bin/os-init-run 2>/dev/null; then
        sudo -n chmod +x /usr/local/bin/os-init-run
        echo "✓ os-init-run zarejestrowany w /usr/local/bin/os-init-run"
    else
        mkdir -p "$HOME/.local/bin"
        cp ./os-init "$HOME/.local/bin/os-init-run"
        chmod +x "$HOME/.local/bin/os-init-run"
        echo "✓ os-init-run zarejestrowany w $HOME/.local/bin/os-init-run"
    fi
fi

if [ -f "./os-add-skill" ]; then
    # Sprzątanie: usuń stary plik os-add-skill-run z v4.1.x jeśli istnieje
    sudo -n rm -f /usr/local/bin/os-add-skill-run 2>/dev/null || rm -f "$HOME/.local/bin/os-add-skill-run" 2>/dev/null || true

    if sudo -n cp ./os-add-skill /usr/local/bin/os-add-skill 2>/dev/null; then
        sudo -n chmod +x /usr/local/bin/os-add-skill
        echo "✓ os-add-skill zainstalowany w /usr/local/bin/os-add-skill"
    else
        mkdir -p "$HOME/.local/bin"
        cp ./os-add-skill "$HOME/.local/bin/os-add-skill"
        chmod +x "$HOME/.local/bin/os-add-skill"
        echo "✓ os-add-skill zainstalowany w $HOME/.local/bin/os-add-skill"
    fi
fi

echo "⚙️ Automatyczna generacja skrótów komend ukośnika (/) dla skilli..."
python3 ./scripts/generate_commands.py

echo "⚙️ Generowanie i rejestracja konfiguracji powłoki w ~/.bashrc.d/antigravity..."
mkdir -p "$HOME/.bashrc.d"
cat << 'EOF' > "$HOME/.bashrc.d/antigravity"
# Antigravity launch function for IDE
antigravity() {
    local win_user
    win_user=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r')
    if [ -z "$win_user" ]; then
        local user_dir
        for user_dir in /mnt/c/Users/*; do
            if [ -f "${user_dir}/AppData/Local/Programs/Antigravity IDE/bin/antigravity-ide" ]; then
                win_user=$(basename "$user_dir")
                break
            fi
        done
    fi
    if [ -z "$win_user" ]; then
        win_user="admin_tk"
    fi
    "/mnt/c/Users/${win_user}/AppData/Local/Programs/Antigravity IDE/bin/antigravity-ide" --remote wsl+Ubuntu "$(pwd)"
}
alias antigravity-ide='antigravity'

# ==============================================================================
# os-init <nazwa-projektu>
# Shell function wrapper — umożliwia cd do nowego projektu po jego utworzeniu.
# Wywołuje właściwy skrypt os-init-run, a następnie wchodzi do nowego katalogu.
# ==============================================================================
os-init() {
    local script
    # Szukaj zainstalowanego skryptu
    if command -v os-init-run &>/dev/null; then
        script="os-init-run"
    elif [ -f "$HOME/.local/bin/os-init-run" ]; then
        script="$HOME/.local/bin/os-init-run"
    elif [ -f "/usr/local/bin/os-init-run" ]; then
        script="/usr/local/bin/os-init-run"
    else
        echo "❌ os-init: skrypt nie znaleziony. Uruchom INSTALL.sh."
        return 1
    fi

    # Uruchom skrypt i przechwytuj ścieżkę projektu
    local output
    output=$(bash "$script" "$@")
    local exit_code=$?

    # Wyświetl cały output
    echo "$output"

    if [ $exit_code -ne 0 ]; then
        return $exit_code
    fi

    # Wyciągnij ścieżkę i wejdź do folderu projektu
    local project_dir
    project_dir=$(echo "$output" | grep "^__PROJECT_DIR__:" | sed 's/^__PROJECT_DIR__://')
    if [ -n "$project_dir" ] && [ -d "$project_dir" ]; then
        echo ""
        echo "🔀 Przechodzę do katalogu projektu..."
        cd "$project_dir" && echo "📁 Jesteś w: $(pwd)"
    fi
}

# Skrót do wklejania obrazów ze schowka Windows (WSL)
alias clip2img="powershell.exe -Command \"Add-Type -AssemblyName System.Windows.Forms; \$img = [System.Windows.Forms.Clipboard]::GetImage(); if (\$img -ne \$null) { [System.IO.Directory]::CreateDirectory('tmp') | Out-Null; \$img.Save('tmp/clip.png', [System.Drawing.Imaging.ImageFormat]::Png); echo '✓ Zapisano w tmp/clip.png' } else { echo '❌ Brak obrazu w schowku' }\""

EOF
chmod +x "$HOME/.bashrc.d/antigravity"
echo "✓ Plik ~/.bashrc.d/antigravity został zapisany."

# Dodaj do ~/.bashrc
if ! grep -q "source ~/.bashrc.d/antigravity" "$HOME/.bashrc" 2>/dev/null; then
    echo "" >> "$HOME/.bashrc"
    echo "# Import Antigravity environment settings" >> "$HOME/.bashrc"
    echo "source ~/.bashrc.d/antigravity" >> "$HOME/.bashrc"
    echo "✓ Dodano import do ~/.bashrc"
fi

# 5. Instalacja rozszerzenia WSL dla Antigravity IDE
echo "🔌 Konfiguracja integracji WSL dla Antigravity IDE..."
IDE_BIN=""
for user_dir in /mnt/c/Users/*; do
    if [ -f "${user_dir}/AppData/Local/Programs/Antigravity IDE/bin/antigravity-ide" ]; then
        IDE_BIN="${user_dir}/AppData/Local/Programs/Antigravity IDE/bin/antigravity-ide"
        break
    fi
done

if [ -z "$IDE_BIN" ]; then
    WIN_USER=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r')
    if [ -n "$WIN_USER" ] && [ -f "/mnt/c/Users/${WIN_USER}/AppData/Local/Programs/Antigravity IDE/bin/antigravity-ide" ]; then
        IDE_BIN="/mnt/c/Users/${WIN_USER}/AppData/Local/Programs/Antigravity IDE/bin/antigravity-ide"
    fi
fi

if [ -n "$IDE_BIN" ]; then
    echo "   📦 Instalacja rozszerzenia Remote - WSL..."
    if "$IDE_BIN" --install-extension ms-vscode-remote.remote-wsl &>/dev/null; then
        echo "   ✓ Rozszerzenie Remote - WSL zainstalowane pomyślnie."
    else
        echo "   ⚠️  Nie udało się automatycznie zainstalować rozszerzenia Remote - WSL."
        echo "      Zainstaluj je ręcznie w IDE lub uruchom:"
        echo "      \"$IDE_BIN\" --install-extension ms-vscode-remote.remote-wsl"
    fi
else
    echo "   ⚠️  Nie odnaleziono instalacji Antigravity IDE w systemie Windows."
fi

echo ""
echo "ℹ️  Aby aktywować os-init i os-add-skill w bieżącym terminalu:"
echo "   source ~/.bashrc.d/antigravity"

# 6. Autoryzacja i logowanie do usług CLI (tylko w trybie interaktywnym)
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
        agy plugin install https://github.com/juliusbrussee/caveman || echo "⚠️ Nie udało się zainstalować wtyczki Caveman (zaloguj się i zainstaluj ręcznie: agy plugin install https://github.com/juliusbrussee/caveman)."
    fi
else
    echo "🖥️ Środowisko nieinteraktywne. Pomijam autoryzację CLI (wykonaj ręcznie po instalacji)."
fi

echo "===================================================================="
echo "✅ DEPLOY ZAKOŃCZONY SUKCESEM: SYSTEM AGENTS-OS v5.0 GOTOWY."
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
