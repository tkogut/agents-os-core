# Core Rule: Installer Repository Management

## Rule 1: Git Worktrees Enforce
- All future updates, features, or branch-based testing in `agents-os-core` MUST use **Git Worktrees** instead of dirty index switching or branch checkouts in the main working directory.
- This ensures clean separation and avoids snapshot contamination in WSL sandbox environments.

## Rule 2: Asynchronous Execution Mode
- Heavy build scripts, sync tasks, or deployment testing must run in **asynchronous mode** (e.g. background tasks or schedule timers).
- Avoid blocking the coordinator flow or interactive shell during active development loops.

## Rule 3: File Editing Restrictions
- Due to known issues with native File Edit Tools (such as infinite +0 -0 loops), file edits or creations in this repository must use raw terminal commands (`cat << 'EOF'`, `sed`, etc.) until fixed.

## Rule 4: System Version Consistency
- Jedynym źródłem prawdy o wersji systemu jest plik `VERSION` w katalogu głównym (np. `7.1.0-swarm`; w dokumentach i nazwach katalogów szablonów skrót `v7.1` / `v7.1-swarm`).
- Przy zmianie wersji zaktualizuj `VERSION`, a następnie wszystkie żywe pliki: skrypty (`os-*`, `INSTALL.sh`, bootstrapery), nazwy katalogów szablonów (`v<MAJOR.MINOR>-swarm`), dokumentację (`README.md`, `docs/`, `SDLC.md`, `CLAUDE.md`), `agents.yaml` i szablony w `vault/`. Wpisy historyczne (`CHANGELOG.md` dla wydanych wersji, cytowane dokumenty źródłowe) zostają bez zmian.
- Spójność wymusza `tests/test_version_consistency.py` (część `pytest tests`): pozostawienie starego ciągu wersji w żywym pliku jest błędem testu.

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

## Rule 8: Distributed State-Dump & Cloud Consistency (R-SYNC-01)
- **Iron Rule**: Przed ostatecznym raportem dla użytkownika, rola Coordinator MUSI upewnić się, że stan prac w `.agents/MEMORY.md` oraz `.agents/task.md` został zrzucony (state-dump via git push), co zapewnia spójność chmury przy przełączaniu maszyn roboczych (laptop, desktop, VPS).
- Automatyczne hooki cyklu życia (`SessionStart` i `SessionEnd` / `PreInvocation` i `Stop`) synchronizują pamięć przed rozpoczęciem i po zakończeniu sesji.