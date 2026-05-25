#!/usr/bin/env bash
# ==============================================================================
# AGENTS-OS E2E Integration Test Suite — Project Bootstrap Verification
# ==============================================================================

set -o errexit
set -o pipefail
set -o nounset

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECTS_ROOT="$(dirname "$REPO_ROOT")"
TEST_PROJECT="agents-os-test-bootstrap-$(date +%s)"
TEST_DIR="$PROJECTS_ROOT/$TEST_PROJECT"

echo "🧪 [TEST] Rozpoczynam test integracyjny E2E dla os-init/bootstrap.py..."

# 1. Czyszczenie przedtestowe
if [ -d "$TEST_DIR" ]; then
    echo "🧹 [TEST] Usuwanie pozostałości po poprzednim teście..."
    rm -rf "$TEST_DIR"
fi

# Wykryj użytkownika GitHub
GH_USER="twoj-github-username"
if command -v gh &>/dev/null; then
    GH_USER=$(gh api user -q .login 2>/dev/null || echo "twoj-github-username")
fi
if [ "$GH_USER" = "twoj-github-username" ]; then
    GH_USER=$(git config github.user 2>/dev/null || git config user.name 2>/dev/null | tr -d ' ' || echo "twoj-github-username")
fi

echo "🐙 [TEST] Zdiagnozowany użytkownik GitHub: $GH_USER"

# Usuń zdalne repozytorium na GitHubie, jeśli istnieje
if command -v gh &>/dev/null; then
    echo "🧹 [TEST] Upewnianie się, że repozytorium na GitHubie nie istnieje..."
    gh repo delete "$GH_USER/$TEST_PROJECT" --yes &>/dev/null || true
fi

# 2. Uruchom os-init-run (backend)
echo "🚀 [TEST] Uruchamianie os-init dla projektu '$TEST_PROJECT'..."
export OS_INIT_TEST=true
if command -v os-init-run &>/dev/null; then
    os-init-run "$TEST_PROJECT"
elif [ -f "$REPO_ROOT/os-init" ]; then
    bash "$REPO_ROOT/os-init" "$TEST_PROJECT"
else
    echo "❌ [TEST] Nie znaleziono skryptu os-init!"
    exit 1
fi

# 3. Weryfikacja katalogu lokalnego
echo "🔍 [TEST] Weryfikacja katalogu lokalnego..."
if [ ! -d "$TEST_DIR" ]; then
    echo "❌ [TEST] BŁĄD: Katalog $TEST_DIR nie został utworzony!"
    exit 1
fi

# Weryfikacja struktury szablonu (Złoty Standard)
expected_files=(
    "$TEST_DIR/agents.yaml"
    "$TEST_DIR/task.md"
    "$TEST_DIR/design-tokens.md"
    "$TEST_DIR/execution"
    "$TEST_DIR/.agents/rules/GOVERNANCE.md"
    "$TEST_DIR/.agents/specs/AGENTS-OS.md"
)

for file in "${expected_files[@]}"; do
    if [ ! -e "$file" ]; then
        echo "❌ [TEST] BŁĄD: Brak oczekiwanego elementu szablonu: $file"
        exit 1
    fi
done
echo "   ✅ Struktura katalogów i plików szablonu jest poprawna."

# 4. Weryfikacja Gita
echo "🔍 [TEST] Weryfikacja repozytorium Git..."
if [ ! -d "$TEST_DIR/.git" ]; then
    echo "❌ [TEST] BŁĄD: Git nie został zainicjalizowany!"
    exit 1
fi

cd "$TEST_DIR"

# Sprawdź czy jest commit
commit_count=$(git rev-list --count HEAD 2>/dev/null || echo "0")
if [ "$commit_count" -eq 0 ]; then
    echo "❌ [TEST] BŁĄD: Brak początkowego commita w repozytorium!"
    exit 1
fi
echo "   ✅ Początkowy commit istnieje (liczba commitów: $commit_count)."

# Sprawdź remote origin
remote_url=$(git remote get-url origin 2>/dev/null || echo "")
expected_url="https://github.com/$GH_USER/$TEST_PROJECT.git"
if [ "$remote_url" != "$expected_url" ]; then
    echo "❌ [TEST] BŁĄD: Niepoprawny adres remote origin! Otrzymano: '$remote_url', Oczekiwano: '$expected_url'"
    exit 1
fi
echo "   ✅ Adres remote origin jest poprawny: $remote_url"

# 5. Weryfikacja dynamicznego dociągania skilli (os-add-skill)
echo "🔍 [TEST] Weryfikacja dynamicznego dociągania skilli (os-add-skill)..."
if command -v os-add-skill-run &>/dev/null; then
    os-add-skill-run "postgresql-optimization"
elif [ -f "$REPO_ROOT/os-add-skill" ]; then
    python3 "$REPO_ROOT/os-add-skill" "postgresql-optimization"
else
    echo "❌ [TEST] Nie znaleziono skryptu os-add-skill!"
    exit 1
fi

if [ ! -f "$TEST_DIR/.agents/skills/postgresql-optimization/SKILL.md" ]; then
    echo "❌ [TEST] BŁĄD: Skill 'postgresql-optimization' nie został pobrany!"
    exit 1
fi
echo "   ✅ Skill 'postgresql-optimization' pobrany pomyślnie."

# 6. Sprzątanie po teście
echo "🧹 [TEST] Rozpoczynam sprzątanie po zakończonym teście..."

# Powrót do katalogu głównego
cd - &>/dev/null

# Usuń zdalne repozytorium na GitHubie
if command -v gh &>/dev/null; then
    echo "   🧹 Usuwanie repozytorium na GitHubie ($GH_USER/$TEST_PROJECT)..."
    gh repo delete "$GH_USER/$TEST_PROJECT" --yes || {
        echo "   ⚠️  [TEST] OSTRZEŻENIE: Nie udało się usunąć repo na GitHub (brak uprawnienia 'delete_repo'). Usuń je ręcznie: https://github.com/$GH_USER/$TEST_PROJECT"
    }
fi

# Usuń katalog lokalny
echo "   🧹 Usuwanie katalogu lokalnego ($TEST_DIR)..."
rm -rf "$TEST_DIR"

echo "🎉 [TEST] TEST ZAKOŃCZONY SUKCESEM. Wszystkie asercje poprawne."
