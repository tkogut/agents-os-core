# 🛸 Raport Oceny i Audytu Kodu: AGENTS-OS v4.1.1 (Universal Swarm)

**Status projektu:** STABLE / PRODUCTION READY (Wysoki poziom dojrzałości)  
**Wersja:** 4.1.1 (Antigravity 2.0 Native)  
**Data audytu:** 2026-05-24  
**Audytor:** Asystent AI Antigravity (GEM Expert)  

---

## 1. Podsumowanie Wykonawcze (Executive Summary)

Wersja **v4.1.1** stanowi olbrzymi krok naprzód w porównaniu do poprzedniego wydania. Zmiany wprowadzone w odpowiedzi na pierwszy audyt zlikwidowały główne blokady przenaszalności kodu:
*   Wdrożono dynamiczny odczyt nazwy użytkownika GitHub z wielopoziomowym fallbackiem.
*   Ścieżka profilu Windows dla IDE jest mapowana dynamicznie na podstawie zmiennej środowiskowej powłoki Windows.
*   Zastąpiono niestabilny system `snap` oficjalną instalacją przez menedżer pakietów `apt` dla GitHub CLI.
*   Wszystkie zależności Pythona zostały poprawnie odizolowane w dedykowanym środowisku wirtualnym (`venv`), co eliminuje ryzyko uszkodzenia pakietów systemowych.
*   Wprowadzono pełny test integracyjny E2E `test_bootstrap.sh` do weryfikacji poprawności działania całego systemu.

Podczas dogłębnej analizy kodu (Deep Code Review) wersji **v4.1.1** zidentyfikowano jednak **dwa nowe niedociągnięcia funkcjonalne oraz jedną optymalizację**, które wpływają na bezobsługowość instalacji i kompletność szablonów.

---

## 2. Nowo Zidentyfikowane Niedociągnięcia (Gaps & Bugs in v4.1.1)

### 🚨 2.1. Błąd Ścieżki Pobierania Awesome Skills (Puste Skille w Szablonach)
*   **Plik:** [INSTALL.sh](file:///home/tkogut/projects/agents-os-core/INSTALL.sh#L78) (linia 78).
*   **Kod:** `npx -y antigravity-awesome-skills --path .agents/skills --risk safe,none`
*   **Problem:** Polecenie pobiera skille do katalogu `.agents/skills` w **katalogu instalatora** (np. `~/projects/agents-os-core/.agents/skills`). Dzieje się to już *po* skopiowaniu szablonów `vault` do katalogu globalnego `~/.antigravity/templates/v4.1-swarm`.
*   **Skutki:** Nowe projekty tworzone przez `os-init` otrzymują **pusty katalog `.agents/skills`**. Pobrane oficjalne skille pozostają w folderze instalatora i nie są dystrybuowane do nowo utworzonych projektów.
*   **Rozwiązanie:** Skieruj pobieranie bezpośrednio do katalogu szablonu (Vault) przed jego kopiowaniem, lub bezpośrednio do folderu docelowego szablonu:
    ```bash
    # Pobranie skilli bezpośrednio do globalnego szablonu (Vault)
    npx -y antigravity-awesome-skills --path "$VAULT_DIR/.agents/skills" --risk safe,none
    ```

### 🚨 2.2. Luka Rejestracji w `INSTALL.sh` — Brak Zapisu `~/.bashrc.d/antigravity`
*   **Plik:** [INSTALL.sh](file:///home/tkogut/projects/agents-os-core/INSTALL.sh#L143-L149).
*   **Problem:** Skrypt sprawdza czy funkcja `os-init()` jest zarejestrowana w `~/.bashrc.d/antigravity`, ale **nigdy jej tam nie zapisuje ani nie tworzy tego pliku**. Jeśli plik nie istnieje lub nie ma w nim funkcji, instalator wyświetla ostrzeżenie i kończy pracę, zmuszając użytkownika do ręcznego konfigurowania powłoki.
*   **Skutki:** Brak automatyzacji przy pierwszym wdrożeniu. Nowy użytkownik nie otrzyma skrótów `agy`, `antigravity` ani funkcji `os-init` bez ręcznej edycji plików powłoki.
*   **Rozwiązanie:** Instalator powinien sam generować ten plik oraz dodawać jego import do głównego `~/.bashrc`:
    ```bash
    # W INSTALL.sh - automatyczna rejestracja:
    mkdir -p "$HOME/.bashrc.d"
    cat << 'EOF' > "$HOME/.bashrc.d/antigravity"
    # Antigravity launch function for IDE
    antigravity() {
        # ... definicja funkcji ...
    }
    alias antigravity-ide='"/mnt/c/Users/admin_tk/AppData/Local/Programs/Antigravity IDE/bin/antigravity-ide"'
    # ... definicja os-init() ...
    EOF

    # Dodanie do ~/.bashrc
    if ! grep -q "source ~/.bashrc.d/antigravity" "$HOME/.bashrc" 2>/dev/null; then
        echo "source ~/.bashrc.d/antigravity" >> "$HOME/.bashrc"
    fi
    ```

### ⚠️ 2.3. Ograniczenie Pobierania Profilu Windows (Brak Interop w WSL)
*   **Plik:** [os-init](file:///home/tkogut/projects/agents-os-core/os-init#L53).
*   **Kod:** `WIN_USER=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r')`
*   **Problem:** Jeśli w WSL2 wyłączona jest integracja z systemem Windows (brak możliwości uruchamiania plików `.exe` z poziomu Linuxa), wywołanie `cmd.exe` zwróci błąd, a zmienna `WIN_USER` będzie pusta. Skrypt powróci do domyślnej wartości `admin_tk`.
*   **Rozwiązanie (Dynamiczne skanowanie profili):** Zamiast odpytywać `cmd.exe`, przeszukaj bezpośrednio katalogi montowania Windows pod kątem instalacji Antigravity IDE. Jest to metoda w 100% niezależna od integracji i interop:
    ```bash
    # Wyszukiwanie ścieżki instalacji w profilach użytkowników Windows
    IDE_BIN=""
    for user_dir in /mnt/c/Users/*; do
        if [ -f "${user_dir}/AppData/Local/Programs/Antigravity IDE/bin/antigravity-ide" ]; then
            IDE_BIN="${user_dir}/AppData/Local/Programs/Antigravity IDE/bin/antigravity-ide"
            break
        fi
    done
    
    if [ -z "$IDE_BIN" ]; then
        # Fallback do standardowej ścieżki
        IDE_BIN="/mnt/c/Users/admin_tk/AppData/Local/Programs/Antigravity IDE/bin/antigravity-ide"
    fi
    ```

### ⚙️ 2.4. Optymalizacja Zmiany Nazwy Gałęzi w Git (`bootstrap.py`)
*   **Plik:** [bootstrap.py](file:///home/tkogut/projects/agents-os-core/global_skills/swarm-bootstrapper/scripts/bootstrap.py#L89) (linia 89).
*   **Kod:** `subprocess.run(["git", "checkout", "-b", "main"], cwd=TARGET_DIR, capture_output=True)`
*   **Opis:** Użycie `-b main` na nowo zainicjalizowanym repozytorium może w niektórych wersjach gita powodować błędy, jeśli domyślna konfiguracja użytkownika ustawia początkową gałąź jako `main`.
*   **Rozwiązanie:** Bezpieczniejszym i standardowym podejściem jest użycie polecenia wymuszenia zmiany nazwy bieżącej gałęzi:
    ```python
    subprocess.run(["git", "branch", "-M", "main"], cwd=TARGET_DIR, capture_output=True)
    ```

---

## 3. Rekomendacja Wdrożeniowa

Wdrożenie poprawek dla punktów **2.1 (ścieżka awesome-skills)** oraz **2.2 (zapis bashrc.d)** pozwoli na oznaczenie wersji jako **v4.2.0 (Zero-Click Production)**, gwarantując pełną automatyzację instalacji od pierwszego uruchomienia bez jakichkolwiek manualnych kroków po stronie użytkownika.
