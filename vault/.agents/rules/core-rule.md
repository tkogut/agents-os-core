# Core Rule: Installer Repository Management

## Rule 1: Git Worktrees Enforce
- All future updates, features, or branch-based testing in `agents-os-core` MUST use **Git Worktrees** instead of dirty index switching or branch checkouts in the main working directory.
- This ensures clean separation and avoids snapshot contamination in WSL sandbox environments.

## Rule 2: Asynchronous Execution Mode
- Heavy build scripts, sync tasks, or deployment testing must run in **asynchronous mode** (e.g. background tasks or schedule timers).
- Avoid blocking the coordinator flow or interactive shell during active development loops.

## Rule 3: File Editing Restrictions
- Due to known issues with native File Edit Tools (such as infinite +0 -0 loops), file edits or creations in this repository must use raw terminal commands (`cat << 'EOF'`, `sed`, etc.) until fixed.

## Rule 4: System Version Consistency (v6.5+)
- Whenever any system improvements, bug fixes, or new features are introduced to `agents-os-core`, the system version number (e.g. `v6.5`) must be updated across all files of the project, including:
  1. Bootstrapper scripts (`bootstrap.py`) and initializers (`os-init`).
  2. Installation scripts (`INSTALL.sh`) and default template directory names (e.g. `v6.5-swarm`).
  3. All project documentation (`README.md`, `CHANGELOG.md`, etc.).
  4. Core configuration templates in the Vault (`vault/` directory).
- Under no circumstances should mismatched or stale version strings remain in the code or config.

## Rule 5: Secrets Sanitization and Masking (R-SEC-01)
- Kategoryczny zakaz odpytywania, czytania lub wyświetlania plików `.env`, zmiennych środowiskowych i baz danych konfiguracyjnych w surowej postaci do czatu dewelopera lub logów sesji.
- Wszystkie odczyty z konsoli (np. `cat .env`, zapytania SQLite do tabeli `settings`) MUSZĄ być maskowane lub filtrowane za pomocą komend bash (np. `grep -v`, `sed`, `awk` lub SQL `REPLACE`) w celu ukrycia wartości kluczy (API keys, passwords, tokens).
- Ujawnienie surowych wartości poświadczeń w logach lub czacie stanowi błąd krytyczny i wymaga natychmiastowej rotacji kluczy u dewelopera.

## Rule 6: Coordinator Source Code Edit Prohibition (R-ROLE-01) ⛔ KRITYCZNY

**Status: MANDATORY | Priority: CRITICAL | Version: v6.2+**

Główny wątek agenta (Coordinator) ma **kategoryczny zakaz** bezpośredniego wywoływania narzędzi modyfikujących kod produkcyjny (`replace_file_content`, `write_to_file`, `multi_replace_file_content`) dla plików w katalogach `/src`, `/api`, `src/`, `api/`.

**Jedyna dopuszczalna ścieżka modyfikacji kodu:** delegowanie przez `invoke_subagent` do roli `cavecrew-builder` lub `swarm_builder`.

**Safety Gate:**
- Skrypt `scripts/validate-handshakes.py` sprawdza, czy `conversation_id` w `*_builder_handshake.json` jest różny od `COORDINATOR_SESSION_ID`.
- Jeśli conversation_id Buildera = ID Coordinatora → błąd `DIRECT_COORDINATOR_EDIT_FORBIDDEN`, exit code 2.
- Hook `scripts/check_coordinator_role.sh` blokuje commit zmian w `src/` bez ważnego Builder handshake od subagenta.

**Naruszenie:** Commit blokowany. Sesja oznaczana jako `GOVERNANCE_VIOLATION`.

## Rule 7: LLM Cost & Swarm Optimization (v6.2+)
- **Caveman Prompts**: Wszystkie prompty i instrukcje do subagentów muszą być pisane w skróconym formacie Caveman (bez uprzejmości, czysty techniczny styl), co eliminuje narzut tokenów.
- **Direct Git Actions**: Coordinator wykonuje operacje Git (stage, commit, push, deploy) bezpośrednio z głównego terminala za pomocą `smart_commit.sh`, bez powoływania dedykowanego, kosztownego subagenta.