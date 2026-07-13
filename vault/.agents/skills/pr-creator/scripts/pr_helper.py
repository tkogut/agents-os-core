#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse

def get_current_branch():
    """Zwraca nazwę aktualnej gałęzi git."""
    res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    return res.stdout.strip()

def run_tests():
    """Wykrywa typ projektu i uruchamia odpowiednie testy."""
    print("🧪 [1/3] Uruchamianie testów sprawdzających jakość (Quality Gate)...")
    
    # 1. Node.js (package.json)
    if os.path.exists("package.json"):
        print("   Detected Node.js project. Running: npm test...")
        res = subprocess.run(["npm", "test"], capture_output=False)
        return res.returncode == 0
        
    # 2. Python (pytest)
    elif os.path.exists("pytest.ini") or os.path.exists("requirements.txt") or os.path.exists("pyproject.toml"):
        # Sprawdzamy czy pytest jest zainstalowany
        pytest_installed = subprocess.run(["pip", "show", "pytest"], capture_output=True).returncode == 0
        if pytest_installed:
            print("   Detected Python project. Running: pytest...")
            res = subprocess.run(["pytest"], capture_output=False)
            return res.returncode == 0
            
    print("   ⚠️  Nie wykryto znanego środowiska testowego (npm test / pytest). Pomijam ten krok.")
    return True

def generate_pr_metadata():
    """Generuje domyślny tytuł i opis PR na podstawie historii ostatnich commitów."""
    # Pobierz ostatnie 5 commitów na obecnej gałęzi, których nie ma na origin/master lub origin/main
    base_branch = "master"
    res_base = subprocess.run(["git", "show-ref", "--verify", "refs/remotes/origin/main"], capture_output=True)
    if res_base.returncode == 0:
        base_branch = "main"
        
    res_commits = subprocess.run(
        ["git", "log", f"origin/{base_branch}..HEAD", "--oneline"], 
        capture_output=True, 
        text=True
    )
    
    commits = res_commits.stdout.strip().split("\n")
    commits = [c for c in commits if c]  # Usuń puste linie
    
    if not commits:
        title = "feat: updates"
        body = "Opis zmian wdrożonych na gałęzi."
    else:
        # Tytuł na podstawie ostatniego commita
        last_commit_msg = " ".join(commits[0].split(" ")[1:])
        title = last_commit_msg
        
        # Opis na podstawie wszystkich commitów z tej gałęzi
        body = "### Opis zmian:\n"
        for c in commits:
            msg = " ".join(c.split(" ")[1:])
            body += f"- {msg}\n"
            
    return title, body

def create_pull_request(title, body):
    """Tworzy PR przy użyciu GitHub CLI."""
    print("🚀 [3/3] Tworzenie Pull Requesta na GitHubie...")
    pr_cmd = [
        "gh", "pr", "create",
        "--title", title,
        "--body", body
    ]
    
    # Uruchom interaktywnie
    res = subprocess.run(pr_cmd)
    if res.returncode == 0:
        print("✅ Pull Request został pomyślnie utworzony!")
    else:
        print("❌ Wystąpił błąd podczas tworzenia PR w GitHub CLI.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="AGENTS-OS GitHub PR Creator Helper")
    parser.add_argument("--skip-tests", action="store_true", help="Pomiń uruchamianie testów przed PR")
    parser.add_argument("--title", help="Tytuł Pull Requesta")
    parser.add_argument("--body", help="Opis Pull Requesta")
    
    args = parser.parse_args()
    
    # 1. Zabezpieczenie przed bezpośrednią pracą na main/master
    branch = get_current_branch()
    if branch in ["main", "master", ""]:
        print("❌ BŁĄD: Jesteś na chronionej gałęzi głównej. PR musi być tworzony z gałęzi roboczej (feature branch).")
        sys.exit(1)
        
    print(f"🌿 Rozpoczynam procedurę PR dla gałęzi: {branch}")
    
    # 2. Uruchomienie testów
    if not args.skip_tests:
        test_success = run_tests()
        if not test_success:
            print("❌ BŁĄD: Testy nie powiodły się! Popraw błędy przed utworzeniem Pull Requesta.")
            sys.exit(1)
        print("✅ Wszystkie testy przeszły pomyślnie.")
        
    # 3. Generowanie metadanych PR
    title = args.title
    body = args.body
    
    if not title or not body:
        print("🪐 [2/3] Generowanie automatycznego tytułu i opisu PR...")
        auto_title, auto_body = generate_pr_metadata()
        title = title or auto_title
        body = body or auto_body
        
    print(f"\nProponowany tytuł PR: {title}")
    print(f"Proponowany opis PR:\n{body}\n")
    
    # 4. Tworzenie PR
    create_pull_request(title, body)

if __name__ == "__main__":
    main()
