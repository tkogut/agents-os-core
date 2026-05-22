import os
import shutil
import sys
import git
from github import Github, GithubException

VAULT_DIR = os.path.expanduser("~/.gemini/antigravity/templates/v4.0-swarm")
TARGET_DIR = os.getcwd()

# Argument handling
if len(sys.argv) > 1:
    project_name = sys.argv[1]
    # FORCE PROJECTS ROOT
    PROJECTS_ROOT = os.path.expanduser("~/projects")
    TARGET_DIR = os.path.join(PROJECTS_ROOT, project_name)
    if not os.path.exists(TARGET_DIR):
        print(f"📦 Tworzenie projektu w ROOT: {TARGET_DIR}")
        os.makedirs(TARGET_DIR)
else:
    TARGET_DIR = os.getcwd()

# SAFETY GUARDRAIL
if os.path.abspath(TARGET_DIR) == os.path.expanduser("~"):
    print("❌ ERROR: Inicjalizacja w katalogu domowym ($HOME) jest ZABRONIONA.")
    print("Wróć do planowania. Wybierz inny folder (np. ~/projects/...).")
    sys.exit(1)

print(f"🚀 INICJACJA AGENTS-OS v4.0 SWARM W: {TARGET_DIR}")

if not os.path.exists(VAULT_DIR):
    print(f"ERR: Złoty Standard nie istnieje w {VAULT_DIR}. Przerwanie.")
    sys.exit(1)

# Check context
os.chdir(TARGET_DIR)

# Init Git using GitPython
git_path = os.path.join(TARGET_DIR, ".git")
if not os.path.exists(git_path):
    print("📦 Git repo: BRAK. Inicjalizowanie...")
    git.Repo.init(TARGET_DIR)

# Check GitHub Auth using PyGithub
print("🔍 Sprawdzanie autoryzacji GitHub API...")
github_token = os.environ.get("GITHUB_TOKEN")
if github_token:
    g = Github(github_token)
    try:
        user = g.get_user()
        print(f"✅ GitHub API zalogowany jako: {user.login}")
    except GithubException:
        print("⚠️  Błąd autoryzacji tokenu GitHub.")
else:
    print("⚠️  Brak zmiennej GITHUB_TOKEN w środowisku. Autoryzacja ograniczona.")

# Copy Vault
print("🛡️ Transfer tożsamości (Kopiowanie Złotego Standardu)...")
for item in os.listdir(VAULT_DIR):
    src = os.path.join(VAULT_DIR, item)
    dst = os.path.join(TARGET_DIR, item)
    if os.path.isdir(src):
        if not os.path.exists(dst):
            shutil.copytree(src, dst)
    else:
        if not os.path.exists(dst):
            shutil.copy2(src, dst)

print("🧩 Aktywne rozszerzenia (Antigravity CLI):")
try:
    ext_dirs = [
        os.path.expanduser("~/.gemini/extensions"),
        os.path.expanduser("~/snap/gemini-cli/current/.gemini/extensions")
    ]
    found_exts = []
    for edir in ext_dirs:
        if os.path.exists(edir):
            for ext in os.listdir(edir):
                if os.path.isdir(os.path.join(edir, ext)):
                    found_exts.append(ext)
    
    found_exts = list(set(found_exts))
    
    if found_exts:
        for ext in found_exts:
            print(f"   ✓ {ext} (Zainstalowane)")
    else:
        print("   Brak zainstalowanych rozszerzeń lub środowisko zablokowane.")
except Exception as e:
    print(f"   [Błąd sprawdzania: {e}]")

# Create .gitignore if missing
gitignore_path = os.path.join(TARGET_DIR, ".gitignore")
if not os.path.exists(gitignore_path):
    print("📝 Tworzenie domyślonego .gitignore...")
    with open(gitignore_path, "w") as f:
        f.write("# AGENTS-OS v4.0 Default ignore\n")
        f.write("tmp/\n")
        f.write("*.log\n")
        f.write("__pycache__/\n")
        f.write(".DS_Store\n")
        f.write("node_modules/\n")
        f.write(".env\n")

print("✨ AGENTS-OS v4.0 Swarm Edition - ACTIVE.")
print(f"Handshake Verified. Gotowy w {TARGET_DIR}")

print("\n💡 Pamiętaj: Utwórz puste repozytorium na Github, a następnie przypnij je:")
if len(sys.argv) > 1:
    print(f"   git remote add origin https://github.com/[twoj-nick]/{project_name}.git")
else:
    print("   git remote add origin https://github.com/[twoj-nick]/[nazwa-projektu].git")
print("   git push -u origin master\n")