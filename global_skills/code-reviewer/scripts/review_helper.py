#!/usr/bin/env python3
import os
import sys
import subprocess
import re

# Wzorce sekretów do detekcji wycieków
SECRET_PATTERNS = [
    (r"(?i)api_key\s*=\s*['\"][a-zA-Z0-9_\-]{16,}['\"]", "API Key leak candidate"),
    (r"(?i)secret\s*=\s*['\"][a-zA-Z0-9_\-]{16,}['\"]", "Client Secret leak candidate"),
    (r"(?i)password\s*=\s*['\"][a-zA-Z0-9_\-]{8,}['\"]", "Password leak candidate"),
    (r"(?i)token\s*=\s*['\"][a-zA-Z0-9_\-]{20,}['\"]", "Token/Credential leak candidate"),
    (r"\"private_key\":\s*\"-----BEGIN PRIVATE KEY-----", "Private Key leak candidate")
]

# Wzorce debugerów
DEBUG_PATTERNS = [
    (r"console\.log\(", "js/ts console.log statement"),
    (r"print\(", "python print statement (ensure it's not a legacy debug print)"),
    (r"breakpoint\(", "python breakpoint() debugger statement"),
    (r"import\s+pdb;\s*pdb\.set_trace\(", "python pdb debugger statement")
]

def get_git_diff():
    """Zwraca listę zmodyfikowanych i dodanych linii w git diff (staged i unstaged)."""
    # Sprawdzamy zarówno staged, jak i unstaged zmiany
    diff_cmd = ["git", "diff", "HEAD", "--unified=0"]
    res = subprocess.run(diff_cmd, capture_output=True, text=True)
    return res.stdout

def parse_diff(diff_content):
    """Parsuje diff i grupuje dodane linie według plików."""
    files_changes = {}
    current_file = None
    
    for line in diff_content.split("\n"):
        if line.startswith("+++ b/"):
            current_file = line[6:]
            files_changes[current_file] = []
        elif line.startswith("+") and not line.startswith("+++"):
            added_content = line[1:]  # usuń znak '+'
            if current_file:
                files_changes[current_file].append(added_content)
                
    return files_changes

def analyze_changes(files_changes):
    """Analizuje dodany kod pod kątem wycieków i debugerów."""
    warnings = []
    
    for filepath, lines in files_changes.items():
        # Pomijaj pliki testowe i skrypty pomocnicze
        if "test" in filepath.lower() or filepath.endswith(".md"):
            continue
            
        for line_no, content in enumerate(lines):
            # 1. Sprawdzanie wycieków sekretów
            for pattern, desc in SECRET_PATTERNS:
                if re.search(pattern, content):
                    warnings.append({
                        "file": filepath,
                        "line_content": content.strip(),
                        "category": "CRITICAL / SECURITY",
                        "reason": f"Potencjalny wyciek klucza/hasła ({desc})"
                    })
            
            # 2. Sprawdzanie pozostawionych debugerów
            for pattern, desc in DEBUG_PATTERNS:
                if re.search(pattern, content):
                    # Pomijamy printy logów i strukturalne printy (np. logger)
                    if "print(" in content and ("logger" in content or "log." in content):
                        continue
                    warnings.append({
                        "file": filepath,
                        "line_content": content.strip(),
                        "category": "WARNING / CLEAN CODE",
                        "reason": f"Pozostawiona komenda diagnostyczna/debuger ({desc})"
                    })
                    
    return warnings

def check_tests_existence(files_changes):
    """Sprawdza, czy dla nowych/zmodyfikowanych plików logicznych istnieją odpowiadające im pliki testowe."""
    warnings = []
    for filepath in files_changes.keys():
        if filepath.endswith((".py", ".js", ".ts", ".go")):
            # Jeśli to plik testowy, ignorujemy
            if "test" in filepath.lower() or "spec" in filepath.lower():
                continue
                
            # Szukamy odpowiadającego pliku testowego
            base_name = os.path.basename(filepath)
            name_no_ext, ext = os.path.splitext(base_name)
            
            test_candidates = [
                f"test_{name_no_ext}{ext}",
                f"{name_no_ext}.test{ext}",
                f"{name_no_ext}.spec{ext}"
            ]
            
            found_test = False
            # Sprawdzamy cały projekt
            for root, dirs, files in os.walk("."):
                # Pomijamy venv, node_modules, .git
                if any(ignored in root for ignored in ["venv", "node_modules", ".git", ".agents"]):
                    continue
                for f in files:
                    if f in test_candidates:
                        found_test = True
                        break
                if found_test:
                    break
                    
            if not found_test:
                warnings.append({
                    "file": filepath,
                    "category": "IMPROVEMENT / QUALITY",
                    "reason": f"Brak powiązanego pliku testowego dla zmodyfikowanego kodu ({test_candidates[0]} / {test_candidates[1]})"
                })
                
    return warnings

def main():
    print("🔍 Uruchamianie lokalnego Asystenta Code Review...")
    
    diff_content = get_git_diff()
    if not diff_content.strip():
        print("✅ Brak lokalnych zmian do przeanalizowania (git diff HEAD jest pusty).")
        sys.exit(0)
        
    changes = parse_diff(diff_content)
    
    # 1. Analiza kodu pod kątem wycieków i debugerów
    warnings = analyze_changes(changes)
    
    # 2. Analiza pod kątem obecności testów jednostkowych
    test_warnings = check_tests_existence(changes)
    warnings.extend(test_warnings)
    
    # Prezentacja raportu
    if not warnings:
        print("\n🎉 WYNIK AUDYTU: ZMIANY POPRAWNE!")
        print("   Nie znaleziono wycieków sekretów ani pozostawionych debugerów.")
        sys.exit(0)
        
    print(f"\n⚠️  Znaleziono {len(warnings)} potencjalnych uwag:")
    print("=" * 80)
    
    criticals = [w for w in warnings if "CRITICAL" in w["category"]]
    non_criticals = [w for w in warnings if "CRITICAL" not in w["category"]]
    
    if criticals:
        print("\n🚨 KRYTYCZNE BŁĘDY / ZABEZPIECZENIA (Należy bezwzględnie poprawić!):")
        for w in criticals:
            print(f"   • Plik: {w['file']}")
            print(f"     Problem: {w['reason']}")
            print(f"     Kod:     {w['line_content']}")
            print("-" * 60)
            
    if non_criticals:
        print("\n💡 SUGESTIE / CZYSTY KOD / JAKOŚĆ:")
        for w in non_criticals:
            print(f"   • Plik: {w['file']}")
            print(f"     Problem: {w['reason']}")
            if "line_content" in w:
                print(f"     Kod:     {w['line_content']}")
            print("-" * 60)
            
    print("\n[Werdykt]: Zmiany wymagają weryfikacji i poprawek przed commitem.")
    sys.exit(1 if criticals else 0)

if __name__ == "__main__":
    main()
