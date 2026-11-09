# Raport: rozprowadzenie second-brain na projekty swarm (2026-11-09)

Zakres: strażnik poufności (`scripts/guard_confidential_gemini.py` + rejestracja hooka), skill `second-brain`, skaner wycieków (`scripts/scan_confidential_leaks.py`) oraz krótka sekcja „Second Brain” w `CLAUDE.md`. Źródło: `agents-os-core` po PR #44-#51. Wszystko w osobnych PR-ach, **żaden niezmergowany**: do merge nic się w projektach nie zmienia.

## Metoda
- Celowo **nie** użyto `os-upgrade-project`: skrypt nadpisuje `hooks.json` (`echo "$HOOKS_CONTENT" > …`), ustawia parametry gita i dowiązuje 65+ skilli, czyli znacznie więcej niż second-brain, i mógłby skasować własne wpisy projektu.
- Skrypt ukierunkowany: osobny worktree na gałęzi `chore/second-brain-guard` z `origin/<gałąź bazowa>`, scalanie wpisu strażnika do istniejących `hooks.json` (zachowuje inne klucze), brak ruchu w katalogach roboczych projektów (wiele ma niezacommitowane zmiany).
- Weryfikacja w każdym worktree przed commitem: `py_compile`, poprawny JSON hooków, wywołanie CLI strażnika przez stdin (zwykły odczyt = allow, odczyt `index.md` vaulta = deny), skaner = ZDANY, kopie strażnika identyczne.

## Wynik

| Projekt | PR | Zakres |
|---|---|---|
| mms4tk | tkogut/mms4tk#146 | strażnik zaktualizowany (2 kopie), skill zaktualizowany, skaner, sekcja CLAUDE.md |
| agents-os-agy-starter-kit | tkogut/agents-os-agy-starter-kit#2 | strażnik, skaner, `hooks.json` x3; skill pominięty (`.agents/skills/` w `.gitignore`); brak CLAUDE.md |
| like-n8n | tkogut/like-n8n#1 | strażnik, skaner, skill, `hooks.json` x3 (nowe); brak CLAUDE.md |
| linkedin-tracker | tkogut/linkedin-tracker#33 | strażnik, skaner, skill + dowiązanie, `hooks.json` x3 (scalone), sekcja CLAUDE.md; `.agents/scripts` to dowiązanie do `scripts/` |
| my-budda | tkogut/my-budda#1 | jak like-n8n |
| n8n_leads | tkogut/n8n_leads#1 | jak like-n8n |
| ogrodnik-4-0 | tkogut/ogrodnik-4-0#1 | jak like-n8n |
| osint-lead-tracker | tkogut/osint-lead-tracker#7 | strażnik, skaner, skill + dowiązanie, `hooks.json` x3 (scalone z `distributed-sync`) |
| portfolio-sentinel | tkogut/portfolio-sentinel#3 | strażnik, skaner, skill + dowiązanie, `hooks.json` x3 (scalone); gałąź bazowa `master` |
| python-udemy | tkogut/python-udemy#1 | jak like-n8n |
| my-budget | **brak PR** | commit lokalny gotowy; repozytorium `tkogut/my-budget` nie istnieje na GitHubie (push: „repository not found”) |

## Pominięte świadomie
- `budzet-app`: remote `pkogut05/budzet-domowy` (inne konto); wymaga decyzji właściciela.
- `linkedin-monitoring`: brak remote.
- `agents-os-test-bootstrap-*`, `test-proj-local`: kopie testowe (detached HEAD, 71 zmian).
- `BI_assistant`, `agents-odoo-harness`: nie są projektami swarm.
- `mark-vinicius-cherry-tycoon`: inna architektura; ma własny proces digestów (PR gry #16).
- `agents-os-core`: źródło.

## Ustalenia
1. W 8 z 11 projektów nie było żadnego `hooks.json`; w 2 (`linkedin-tracker`, `osint-lead-tracker`) brakowało strażnika poufności; tylko mms4tk miał go (starszy). Dla Gemini te projekty działały bez blokady technicznej.
2. `guard-coordinator` (R-ROLE-01 dla Gemini) jest w mms4tk i `linkedin-tracker`; w pozostałych go nie ma. Nie był w zakresie, więc nie dodany.
3. Brak `CLAUDE.md` w 8 projektach: sekcja „Second Brain” dodana tylko w mms4tk i `linkedin-tracker`. W pozostałych wiedzę niesie skill (o ile aktywowany frazami).
4. `os-upgrade-project` nie rozprowadza skanera ani skilla w sposób ukierunkowany i nadpisuje `hooks.json`; do poprawy (scalanie zamiast nadpisywania, dystrybucja skanera).
5. W `linkedin-tracker` `.agents/scripts` jest śledzonym dowiązaniem; hook używa `scripts/…`, więc działa.

## Ograniczenia i ryzyka
- Do merge PR-ów projekty pozostają bez zmian. Wykonanie hooka w żywym Antigravity potwierdzono tylko w `agents-os-core`.
- Strażnik nie pilnuje Claude Code (rozpoznaje modele po `modelName`); ochrona po stronie Claude'a to skill i zasady.
- `claude-pre-tool-guard.sh` kończy się kodem 1 (nieblokującym w Claude Code); decyzja właściciela z 2026-11-09: bez zmian.
- Strażnik wymaga vaulta pod `/mnt/c/Users/tkogut/Documents/sejf_tk` lub `OBSIDIAN_VAULT_PATH`; na innej maszynie fail-closed dla operacji dotykających vaulta.
- Testy jednostkowe strażnika zależą od żywego vaulta, dlatego nie kopiowano ich do projektów.
- Skaner nie jest wpięty w CI projektów.

## Następne kroki (decyzje właściciela)
1. Przejrzeć i zmergować 10 PR-ów (kolejność dowolna).
2. `my-budget`: utworzyć/wskazać poprawny remote albo pominąć.
3. `budzet-app`: zdecydować, czy objąć (inne konto).
4. Zdecydować o `guard-coordinator` w projektach bez niego i o `CLAUDE.md` tam, gdzie go brak.
5. mms4tk: rozstrzygnąć poufność wiedzy, potem opublikować 11 oczekujących notatek (`os-publish-knowledge`).
6. Zaktualizować `os-upgrade-project` (scalanie hooków, dystrybucja skanera i skilla).
7. Sprzątanie po merge: worktree w katalogu roboczym sesji (scratchpad) i gałęzie `chore/second-brain-guard`.
