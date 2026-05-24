#!/usr/bin/env python3
"""
AGENTS-OS v4.0 SWARM - Project Bootstrapper
Tworzy projekt, repo GitHub, commit initial + push.
Wypisuje ścieżkę projektu na stdout jako ostatnią linię (używana przez os-init do cd).
"""
import os
import shutil
import sys
import subprocess

VAULT_DIR = os.path.expanduser("~/.antigravity/templates/v4.0-swarm")

# --------------------------------------------------------------------------- #
# Argument handling
# --------------------------------------------------------------------------- #
if len(sys.argv) > 1:
    project_name = sys.argv[1]
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

print(f"🚀 INICJACJA AGENTS-OS v4.0 SWARM W: {TARGET_DIR}")

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
        f.write("# AGENTS-OS v4.0\ntmp/\n*.log\n__pycache__/\n.DS_Store\nnode_modules/\n.env\n")

# --------------------------------------------------------------------------- #
# 4. Git init
# --------------------------------------------------------------------------- #
git_path = os.path.join(TARGET_DIR, ".git")
if not os.path.exists(git_path):
    print("📦 Inicjalizacja lokalnego repo git...")
    subprocess.run(["git", "init"], cwd=TARGET_DIR, check=True)
    subprocess.run(["git", "checkout", "-b", "main"], cwd=TARGET_DIR, check=True)

# --------------------------------------------------------------------------- #
# 5. Tworzenie repo na GitHubie (gh CLI)
# --------------------------------------------------------------------------- #
print("🐙 Sprawdzanie repo na GitHubie...")
gh_check = subprocess.run(
    ["gh", "repo", "view", f"tkogut/{project_name}"],
    cwd=TARGET_DIR, capture_output=True
)

if gh_check.returncode != 0:
    print(f"🐙 Tworzenie publicznego repo: tkogut/{project_name}...")
    result = subprocess.run(
        ["gh", "repo", "create", project_name,
         "--public",
         "--description", f"AGENTS-OS v4.0 — {project_name}",
         "--source", TARGET_DIR,
         "--remote", "origin",
         "--push"],
        cwd=TARGET_DIR, capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ Repo utworzone: https://github.com/tkogut/{project_name}")
        repo_created_by_gh = True
    else:
        print(f"⚠️  gh repo create failed: {result.stderr.strip()}")
        repo_created_by_gh = False
else:
    print(f"✅ Repo już istnieje: tkogut/{project_name}")
    repo_created_by_gh = False

# --------------------------------------------------------------------------- #
# 6. Sprawdź remote + initial commit + push (jeśli gh nie zrobiło tego sam)
# --------------------------------------------------------------------------- #
if not repo_created_by_gh:
    # Sprawdź czy remote origin już jest ustawiony
    remote_check = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=TARGET_DIR, capture_output=True, text=True
    )
    if remote_check.returncode != 0:
        remote_url = f"https://github.com/tkogut/{project_name}.git"
        print(f"🔗 Ustawianie remote origin: {remote_url}")
        subprocess.run(
            ["git", "remote", "add", "origin", remote_url],
            cwd=TARGET_DIR, check=True
        )

    # Commit jeśli są zmiany
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=TARGET_DIR, capture_output=True, text=True
    )
    if status.stdout.strip():
        print("📝 Initial commit...")
        subprocess.run(["git", "add", "-A"], cwd=TARGET_DIR, check=True)
        subprocess.run(
            ["git", "commit", "-m", "init: agents-os v4.0 swarm bootstrap"],
            cwd=TARGET_DIR, check=True
        )

    # Push
    print("🚀 Push na GitHub (main)...")
    push_result = subprocess.run(
        ["git", "push", "-u", "origin", "main"],
        cwd=TARGET_DIR, capture_output=True, text=True
    )
    if push_result.returncode == 0:
        print("✅ Push zakończony sukcesem.")
    else:
        # Spróbuj z master
        push_result2 = subprocess.run(
            ["git", "push", "-u", "origin", "HEAD"],
            cwd=TARGET_DIR, capture_output=True, text=True
        )
        if push_result2.returncode == 0:
            print("✅ Push zakończony sukcesem.")
        else:
            print(f"⚠️  Push failed: {push_result.stderr.strip()}")

# --------------------------------------------------------------------------- #
# 7. Rozszerzenia (info)
# --------------------------------------------------------------------------- #
print("\n🧩 Aktywne rozszerzenia (Antigravity CLI):")
ext_dirs = [
    os.path.expanduser("~/.antigravity/extensions"),
    os.path.expanduser("~/.gemini/extensions"),
]
found_exts = []
for edir in ext_dirs:
    if os.path.exists(edir):
        for ext in os.listdir(edir):
            if os.path.isdir(os.path.join(edir, ext)):
                found_exts.append(ext)
if found_exts:
    for ext in list(set(found_exts)):
        print(f"   ✓ {ext}")
else:
    print("   Brak zainstalowanych rozszerzeń.")

print(f"\n✨ AGENTS-OS v4.0 Swarm — projekt GOTOWY.")
print(f"   GitHub: https://github.com/tkogut/{project_name}")

# WAŻNE: ostatnia linia to ścieżka do projektu — używana przez os-init
print(f"__PROJECT_DIR__:{TARGET_DIR}")
