#!/usr/bin/env python3
"""
AGENTS-OS v5.0 SWARM - Project Bootstrapper
Kolejność: folder → vault → .gitignore → git init → commit → gh repo create → push
Wypisuje __PROJECT_DIR__:<ścieżka> jako ostatnią linię (używana przez os-init do cd).
Używa natywnych bibliotek GitPython i PyGithub zamiast surowych wywołań subprocess.
"""
import os
import sys
import shutil

import git
import github
from github import Github, GithubException

VAULT_DIR = os.path.expanduser("~/.antigravity/templates/v5.0-swarm")
if not os.path.exists(VAULT_DIR):
    # Domyślnie fallback do lokalnego folderu jeśli brak globalnej instalacji
    local_vault = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "vault")
    if os.path.exists(local_vault):
        VAULT_DIR = local_vault

# --------------------------------------------------------------------------- #
# Argument handling
# --------------------------------------------------------------------------- #
if len(sys.argv) > 1:
    arg1 = sys.argv[1]
    if os.path.isabs(arg1):
        TARGET_DIR = os.path.abspath(arg1)
        project_name = os.path.basename(TARGET_DIR)
    elif "/" in arg1 or "\\" in arg1:
        # Posiada separator ścieżki -> traktuj jako ścieżkę względną
        TARGET_DIR = os.path.abspath(arg1)
        project_name = os.path.basename(TARGET_DIR)
    else:
        project_name = arg1
        PROJECTS_ROOT = os.path.expanduser("~/projects")
        TARGET_DIR = os.path.join(PROJECTS_ROOT, project_name)
else:
    project_name = os.path.basename(os.getcwd())
    TARGET_DIR = os.getcwd()

# SAFETY GUARDRAIL
if os.path.abspath(TARGET_DIR) == os.path.expanduser("~"):
    print("❌ ERROR: Inicjalizacja w katalogu domowym ($HOME) jest ZABRONIONA.")
    sys.exit(1)

# --------------------------------------------------------------------------- #
# 1. Tworzenie folderu projektu
# --------------------------------------------------------------------------- #
if not os.path.exists(TARGET_DIR):
    print(f"📦 Tworzenie projektu: {TARGET_DIR}")
    os.makedirs(TARGET_DIR)

print(f"🚀 INICJACJA AGENTS-OS v5.0 SWARM W: {TARGET_DIR}")

# --------------------------------------------------------------------------- #
# 2. Kopiowanie Vault (Złoty Standard)
# --------------------------------------------------------------------------- #
if os.path.exists(VAULT_DIR):
    print("🛡️  Transfer tożsamości (Kopiowanie Złotego Standardu)...")
    for item in os.listdir(VAULT_DIR):
        src = os.path.join(VAULT_DIR, item)
        dst = os.path.join(TARGET_DIR, item)
        if os.path.isdir(src):
            if not os.path.exists(dst):
                shutil.copytree(src, dst)
        else:
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
else:
    print(f"⚠️  Vault nie znaleziony w {VAULT_DIR}. Tworzę minimalną strukturę...")
    for d in [".agents/plans", ".agents/skills", "execution", "tmp"]:
        os.makedirs(os.path.join(TARGET_DIR, d), exist_ok=True)

# --------------------------------------------------------------------------- #
# 3. Tworzenie .gitignore jeśli brak
# --------------------------------------------------------------------------- #
gitignore_path = os.path.join(TARGET_DIR, ".gitignore")
if not os.path.exists(gitignore_path):
    print("📝 Tworzenie .gitignore...")
    with open(gitignore_path, "w") as f:
        f.write("# AGENTS-OS v5.0\ntmp/\n*.log\n__pycache__/\n.DS_Store\nnode_modules/\n.env\n")

# Tworzymy README.md jeśli brak (potrzebny do commita)
readme_path = os.path.join(TARGET_DIR, "README.md")
if not os.path.exists(readme_path):
    with open(readme_path, "w") as f:
        f.write(f"# {project_name}\n\nAGENTS-OS v5.0 Swarm Edition\n")

# --------------------------------------------------------------------------- #
# 4. Pozyskanie tokena GitHub i określenie użytkownika
# --------------------------------------------------------------------------- #
token = os.environ.get("GITHUB_TOKEN")
if not token:
    # Używamy natywnego odczytu z pliku hosts.yml aby uniknąć wywołania subprocess
    gh_hosts_path = os.path.expanduser("~/.config/gh/hosts.yml")
    if os.path.exists(gh_hosts_path):
        try:
            with open(gh_hosts_path, "r") as f:
                content = f.read()
                # Proste wyciągnięcie tokena (zakładając strukturę hosts.yml)
                if "oauth_token: " in content:
                    token = content.split("oauth_token: ")[1].split("\n")[0].strip()
        except Exception:
            pass

gh_user = None
if token:
    try:
        g = Github(auth=github.Auth.Token(token))
        gh_user = g.get_user().login
    except Exception as e:
        print(f"⚠️  PyGithub auth failed: {e}. Używam konfiguracji gita.")

if not gh_user:
    try:
        config = git.GitConfigParser(os.path.expanduser("~/.gitconfig"), read_only=True)
        gh_user = config.get_value("github", "user", default="") or config.get_value("user", "name", default="").replace(" ", "")
    except Exception:
        pass

if not gh_user:
    gh_user = "twoj-github-username"

# --------------------------------------------------------------------------- #
# 5. Git init (Natywnie przez GitPython)
# --------------------------------------------------------------------------- #
git_path = os.path.join(TARGET_DIR, ".git")
try:
    if not os.path.exists(git_path):
        print("📦 Inicjalizacja lokalnego repo git...")
        repo = git.Repo.init(TARGET_DIR)
        with repo.config_writer() as writer:
            writer.set_value("init", "defaultBranch", "main")
    else:
        repo = git.Repo(TARGET_DIR)

    # Upewnij się, że branch to main
    try:
        repo.git.checkout("-b", "main")
    except Exception:
        try:
            repo.git.branch("-M", "main")
        except Exception:
            pass
except Exception as e:
    print(f"❌ Error during git init: {e}")
    sys.exit(1)

# Upewnij się, że tożsamość git jest skonfigurowana przed commitowaniem
try:
    with repo.config_reader() as reader:
        has_name = reader.has_option("user", "name")
        has_email = reader.has_option("user", "email")
    if not has_name or not has_email:
        print(f"   ⚙️  Brak tożsamości Git. Ustawiam lokalnie: {gh_user}")
        with repo.config_writer() as writer:
            writer.set_value("user", "name", gh_user)
            writer.set_value("user", "email", f"{gh_user}@users.noreply.github.com")
except Exception as e:
    print(f"⚠️  Nie udało się skonfigurować tożsamości git: {e}")

# --------------------------------------------------------------------------- #
# 6. Initial commit (Natywnie przez GitPython)
# --------------------------------------------------------------------------- #
if repo.is_dirty(untracked_files=True):
    print("📝 Initial commit...")
    try:
        repo.git.add(A=True)
        repo.index.commit("init: agents-os v5.0 swarm bootstrap")
        print("   ✅ Commit gotowy.")
    except Exception as e:
        print(f"❌ Commit failed: {e}")
        sys.exit(1)
else:
    print("   ℹ️  Brak zmian do commita (repo już zainicjalizowane).")

# --------------------------------------------------------------------------- #
# 7. GitHub repo — utwórz jeśli nie istnieje (Natywnie przez PyGithub)
# --------------------------------------------------------------------------- #
print(f"🐙 Sprawdzanie repo na GitHubie dla użytkownika {gh_user}...")
repo_exists = False
if token:
    try:
        g = Github(auth=github.Auth.Token(token))
        g.get_repo(f"{gh_user}/{project_name}")
        repo_exists = True
        print(f"   ✅ Repo już istnieje: {gh_user}/{project_name}")
    except GithubException as e:
        if e.status == 404:
            repo_exists = False
        else:
            print(f"⚠️  GitHub API returned status {e.status}: {e.data}")
    except Exception as e:
        print(f"⚠️  GitHub API error: {e}")

if not repo_exists and token:
    try:
        print(f"🐙 Tworzenie publicznego repo: {gh_user}/{project_name}...")
        g = Github(auth=github.Auth.Token(token))
        user = g.get_user()
        gh_repo = user.create_repo(
            name=project_name,
            private=False,
            description=f"AGENTS-OS v5.0 — {project_name}"
        )
        print(f"   ✅ Repo utworzone: {gh_repo.html_url}")
    except Exception as e:
        print(f"   ⚠️  Nie udało się utworzyć repozytorium przez API: {e}")

# Ustawienie origin remote
try:
    origin = repo.remote("origin")
    origin.set_url(f"https://github.com/{gh_user}/{project_name}.git")
except ValueError:
    origin = repo.create_remote("origin", f"https://github.com/{gh_user}/{project_name}.git")
    print(f"   🔗 Remote origin ustawiony: https://github.com/{gh_user}/{project_name}.git")
except Exception as e:
    print(f"⚠️  Nie udało się skonfigurować remote origin: {e}")

# --------------------------------------------------------------------------- #
# 8. Push (Natywnie przez GitPython)
# --------------------------------------------------------------------------- #
print("🚀 Push na GitHub...")
try:
    # Pobierz aktualną nazwę gałęzi
    current_branch = repo.active_branch.name
    origin.push(refspec=f"{current_branch}:{current_branch}", set_upstream=True)
    print(f"   ✅ Push zakończony ({current_branch} → origin).")
except Exception as e:
    print(f"   ⚠️  Push failed: {e}")
    print(f"      Możesz pushować ręcznie: git push -u origin {repo.active_branch.name}")

print(f"\n✨ AGENTS-OS v5.0 Swarm — projekt GOTOWY.")
print(f"   GitHub: https://github.com/{gh_user}/{project_name}")

# WAŻNE: ostatnia linia = sygnał dla os-init (shell function) do cd
print(f"__PROJECT_DIR__:{TARGET_DIR}")
