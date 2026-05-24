#!/usr/bin/env python3
"""
AGENTS-OS v4.2 SWARM - Project Bootstrapper
Kolejność: folder → vault → .gitignore → git init → commit → gh repo create → push
Wypisuje __PROJECT_DIR__:<ścieżka> jako ostatnią linię (używana przez os-init do cd).
"""
import os
import shutil
import sys
import subprocess

VAULT_DIR = os.path.expanduser("~/.antigravity/templates/v4.2-swarm")

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

print(f"🚀 INICJACJA AGENTS-OS v4.2 SWARM W: {TARGET_DIR}")

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
        f.write("# AGENTS-OS v4.2\ntmp/\n*.log\n__pycache__/\n.DS_Store\nnode_modules/\n.env\n")

# Tworzymy README.md jeśli brak (potrzebny do commita)
readme_path = os.path.join(TARGET_DIR, "README.md")
if not os.path.exists(readme_path):
    with open(readme_path, "w") as f:
        f.write(f"# {project_name}\n\nAGENTS-OS v4.2 Swarm Edition\n")

# --------------------------------------------------------------------------- #
# 4. Git init (ZAWSZE przed gh repo create)
# --------------------------------------------------------------------------- #
git_path = os.path.join(TARGET_DIR, ".git")
if not os.path.exists(git_path):
    print("📦 Inicjalizacja lokalnego repo git...")
    subprocess.run(["git", "init"], cwd=TARGET_DIR, check=True, capture_output=True)
    # Ustaw branch na main
    subprocess.run(["git", "branch", "-M", "main"], cwd=TARGET_DIR, check=True, capture_output=True)
else:
    # Sprawdź czy jesteśmy na main lub master
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=TARGET_DIR, capture_output=True, text=True
    ).stdout.strip()
    if not branch:
        subprocess.run(["git", "branch", "-M", "main"], cwd=TARGET_DIR, capture_output=True)

# --------------------------------------------------------------------------- #
# 5. Initial commit (PRZED gh repo create — gh --push wymaga commitów)
# --------------------------------------------------------------------------- #
status = subprocess.run(
    ["git", "status", "--porcelain"],
    cwd=TARGET_DIR, capture_output=True, text=True
)
if status.stdout.strip():
    print("📝 Initial commit...")
    subprocess.run(["git", "add", "-A"], cwd=TARGET_DIR, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init: agents-os v4.2 swarm bootstrap"],
        cwd=TARGET_DIR, check=True, capture_output=True
    )
    print("   ✅ Commit gotowy.")
else:
    print("   ℹ️  Brak zmian do commita (repo już zainicjalizowane).")

# --------------------------------------------------------------------------- #
# 6. GitHub repo — utwórz jeśli nie istnieje, ustaw remote
# --------------------------------------------------------------------------- #
# Ustal dynamicznie użytkownika GitHub
gh_user = "twoj-github-username"
try:
    gh_user_proc = subprocess.run(
        ["gh", "api", "user", "-q", ".login"],
        capture_output=True, text=True, check=True
    )
    gh_user = gh_user_proc.stdout.strip()
except Exception:
    # Fallback do git config github.user lub user.name
    git_user_proc = subprocess.run(
        ["git", "config", "github.user"],
        capture_output=True, text=True
    )
    if git_user_proc.returncode == 0 and git_user_proc.stdout.strip():
        gh_user = git_user_proc.stdout.strip()
    else:
        git_user_name_proc = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True, text=True
        )
        if git_user_name_proc.returncode == 0 and git_user_name_proc.stdout.strip():
            gh_user = git_user_name_proc.stdout.strip().replace(" ", "")

print(f"🐙 Sprawdzanie repo na GitHubie dla użytkownika {gh_user}...")
gh_check = subprocess.run(
    ["gh", "repo", "view", f"{gh_user}/{project_name}"],
    cwd=TARGET_DIR, capture_output=True
)

if gh_check.returncode != 0:
    # Repo nie istnieje — utwórz BEZ --push (commitujemy sami w kroku 5 i 7)
    print(f"🐙 Tworzenie publicznego repo: {gh_user}/{project_name}...")
    result = subprocess.run(
        ["gh", "repo", "create", project_name,
         "--public",
         "--description", f"AGENTS-OS v4.2 — {project_name}",
         "--source", TARGET_DIR,
         "--remote", "origin"],
        cwd=TARGET_DIR, capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"   ✅ Repo utworzone: https://github.com/{gh_user}/{project_name}")
    else:
        print(f"   ⚠️  gh repo create failed: {result.stderr.strip()}")
        # Fallback: ustaw remote ręcznie
        remote_url = f"https://github.com/{gh_user}/{project_name}.git"
        subprocess.run(
            ["git", "remote", "add", "origin", remote_url],
            cwd=TARGET_DIR, capture_output=True
        )
        print(f"   🔗 Remote origin ustawiony ręcznie: {remote_url}")
else:
    print(f"   ✅ Repo już istnieje: {gh_user}/{project_name}")
    # Upewnij się że remote origin jest ustawiony
    remote_check = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=TARGET_DIR, capture_output=True, text=True
    )
    if remote_check.returncode != 0:
        remote_url = f"https://github.com/{gh_user}/{project_name}.git"
        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=TARGET_DIR, capture_output=True)

# --------------------------------------------------------------------------- #
# 7. Push
# --------------------------------------------------------------------------- #
print("🚀 Push na GitHub...")
# Wykryj aktualną gałąź
current_branch = subprocess.run(
    ["git", "branch", "--show-current"],
    cwd=TARGET_DIR, capture_output=True, text=True
).stdout.strip() or "main"

push_result = subprocess.run(
    ["git", "push", "-u", "origin", current_branch],
    cwd=TARGET_DIR, capture_output=True, text=True
)
if push_result.returncode == 0:
    print(f"   ✅ Push zakończony ({current_branch} → origin).")
else:
    # Jeśli branch nie istnieje na remote, wymuś
    push_result2 = subprocess.run(
        ["git", "push", "--set-upstream", "origin", f"HEAD:{current_branch}"],
        cwd=TARGET_DIR, capture_output=True, text=True
    )
    if push_result2.returncode == 0:
        print(f"   ✅ Push zakończony ({current_branch}).")
    else:
        print(f"   ⚠️  Push failed: {push_result.stderr.strip()}")
        print(f"      Możesz pushować ręcznie: git push -u origin {current_branch}")

print(f"\n✨ AGENTS-OS v4.2 Swarm — projekt GOTOWY.")
print(f"   GitHub: https://github.com/{gh_user}/{project_name}")

# WAŻNE: ostatnia linia = sygnał dla os-init (shell function) do cd
print(f"__PROJECT_DIR__:{TARGET_DIR}")
