🛸 KONSTYTUCJA AGENTS-OS v7.1 Swarm Edition — Instrukcja obsługi
Wersja: 7.1.0-swarm (źródło prawdy: plik VERSION) | Status: STABLE | Architekt: Antigravity Orchestrator & GEM (Gemini Evolution Manager)
Poprzednie wydanie tego dokumentu: 6.5-AG. Zmiany względem 6.5 opisuje CHANGELOG.md; sekcje 9–11 są nowe.

🛠️ 1. ARCHITEKTURA ORKIESTRACJI (THE SWARM TRIAD)
System operuje w trybie asynchronicznego roju (Swarm) z wykorzystaniem natywnych, równoległych Subagentów Antigravity oraz Claude Code. Każda rola posiada twarde ramy odpowiedzialności. Aktualne modele wskazuje CLAUDE.md i agents.yaml (przykładowo: Coordinator Gemini 4 Argon / Gemini 3.8 Flash Medium; Builder Gemini 3.1 Pro, Claude 3.7 lub Claude Opus 5.5; Auditor Gemini 3.8 Flash Medium lub subagent Auditor):

Coordinator:
- Rola: Główny Zarządca i Architekt Kontekstu.
- Zadania: Planowanie strategiczne (.agents/plans/), orkiestracja zadań, zarządzanie backlogiem (task.md), zrzut stanu pamięci (.agents/MEMORY.md, .agents/task.md).
- Zasada: Zakaz bezpośredniego pisania kodu w głównym drzewie projektu. Wymusza to hook guard-coordinator (decyzja force_ask: wyjątek tylko za zgodą człowieka w oknie Antigravity).

The Builder:
- Rola: Inżynier Zmian.
- Zadania: Pisanie kodu, testy, lokalne walidacje, atomowe commity (SWARM_ROLE=builder).
- Zasada: Pracuje wyłącznie w izolowanych obszarach roboczych (Git Worktrees w tmp/worktrees/feature/<nazwa>). Zmiany w skryptach instalatora i scripts/* wymagają autoryzacji koordynatora.

The Auditor:
- Rola: Strażnik Jakości i Infrastruktury.
- Zadania: Linting, audyt bezpieczeństwa, weryfikacja logów, sprawdzanie matematyczne (math_check), akceptacja PR.

The Orchestrator (Użytkownik - tkogut):
- Rola: Ostateczna Instancja Decyzyjna (Sygnał: EXECUTE).

📁 2. TOPOLOGIA SYSTEMOWA
Struktura repozytorium źródłowego agents-os-core (projekty potomne dostają jej podzbiór z szablonu vault/):
.
├── VERSION                 # Wersja systemu (źródło prawdy, np. 7.1.0-swarm)
├── agents.yaml             # Rejestr ról i modeli
├── CLAUDE.md, AGENTS.md    # Manifesty sesji (Claude Code builder / opis frameworka)
├── SDLC.md, CHANGELOG.md   # Cykl wytwórczy i historia zmian
├── INSTALL.sh              # Instalator; os-init, os-init-claude, os-add-skill,
│                           #   os-upgrade-project, os-run-builder, os-publish-knowledge  # CLI
├── .agents/
│   ├── hooks.json          # Hooki Antigravity/Gemini (lustra: .gemini/, .antigravity/)
│   ├── hooks/              # Skrypty hooków Claude Code (podpięte w .claude/settings.json)
│   ├── scripts/            # Fizyczne kopie strażników (identyczne z scripts/)
│   ├── mcp-servers/        # Lokalne węzły MCP (antigravity-docs)
│   ├── rules/, plans/      # Reguły zachowania i plany operacyjne
│   ├── specs/              # Specyfikacje, graph.json, knowledge/ (notatki z NotebookLM)
│   ├── eval/               # Moduł ewaluacji promptów
│   ├── swarm/              # Handshake'e subagentów
│   └── MEMORY.md, task.md  # Stan i backlog (SSOT)
├── .claude/                # settings.json (hooki), commands/, skills/ (dowiązania)
├── .ai/                    # agentic.config.json, trackers/, browsers/, specs/
├── .github/workflows/      # mcp-docs-updater.yml, om-skills-sync.yml
├── global_skills/          # Skille systemowe (57 katalogów)
├── scripts/                # Strażniki, skaner wycieków, publikacja do vaulta, handshake
├── tests/                  # pytest: strażnicy, skaner, scalanie hooków, spójność wersji
└── vault/                  # Szablon projektu potomnego (m.in. 70 skilli)

🧠 3. GITOPS & BAZA WIEDZY (MCP PROTOCOL)
Od wydania 6.5 system zapobiega halucynacjom modeli LLM (Anti-Hallucination Matrix):
- Węzeł Dokumentacji (MCP Node): Baza wiedzy o środowisku Antigravity jest mapowana do IDE przez węzeł Node.js w .agents/mcp-servers/antigravity-docs/. Model otrzymuje narzędzia: search_docs, read_doc, list_document_names.
- Izolacja Pamięci: ZAKAZ uruchamiania serwera MCP globalnie. Serwer musi być definiowany w .gemini/mcp_config.json z użyciem ścieżek bezwzględnych.
- Autonomiczna Aktualizacja (CI/CD): Potok .github/workflows/mcp-docs-updater.yml (Cron Job) indeksuje oficjalną dokumentację (Python + Playwright) i wypycha zmiany tylko przy wykryciu rzeczywistych modyfikacji (Dirty-Check); commity mają postać chore(mcp): auto-refresh Antigravity docs.

🪨 4. PROTOKÓŁ CAVEMAN ULTRA+ (TOKEN OPTIMIZATION)
Maksymalna kompresja kontekstu i oszczędność tokenów (od 2026-11-02 jako trzy rodzeństwa skilli: caveman, ultracave, megacave):
- Logic-First Speech: Zakaz form grzecznościowych. Komunikacja startuje od akcji lub wyniku.
- Prompt Compaction: Instrukcje w skróconych formach symbolicznych.
- Active Graph Evolution: Zamiast pełnego skanowania kodu, agenci odpytują .agents/specs/graph.json w celu identyfikacji ścieżek krytycznych.
- Ultra-Review: Auditor komunikuje się kodami błędów i wskaźnikami linii (np. ERR: L45 @ auth.rs -> null pointer).

🚨 5. DEFENSYWNE OBEJŚCIA BŁĘDÓW (CRITICAL ANTI-BUG)
Z uwagi na niestabilność silnika Antigravity system stosuje obejścia:
- Blokada File Edit Hang (+0 -0): wbudowany edytor wizualny Antigravity potrafi zawiesić się w pętli, generując pusty diff. Reguła 3 w .agents/rules/core-rule.md nakazuje edycję plików przez terminal (cat/heredoc/sed) w agentach Antigravity. Claude Code używa własnych natywnych narzędzi edycji.
- Stale Worktree Crash: osierocone gałęzie worktree mogą powodować zawieszenie modeli. Hook before_model_call z `git worktree prune` NIE jest już zainstalowany w żadnym hooks.json (obecnie hooks.json zawiera strażników i synchronizację rozproszoną). Sprzątanie jest ręczne: `git worktree prune`, a worktree usuwa się po merge.

🚀 6. KOMENDY NATYWNE (SLASH COMMANDS) & ASYNCHRONICZNOŚĆ
- /goal – Wymusza autonomiczny tryb pracy ("Vibe Coding").
- /grill-me – Aktywne planowanie: rygorystyczny wywiad przed dotknięciem kodu; ustalenia trafiają do .agents/MEMORY.md.
- /schedule – Cykliczne zadania w tle (Scheduled Tasks) dla Auditora.
- /browser – Mostek CDP (WSL2-Bridge), tylko po bezpośrednim wywołaniu.
- Claude Code (.claude/commands/): /worktree-init, /handshake, /qa-gate, /commit oraz pętle Open Mercato (om-*), opisane w CLAUDE.md.

🛠️ 7. EKOSYSTEM UMIEJĘTNOŚCI (AWESOME SKILLS)
- Zakaz manualnej modyfikacji: zakaz ręcznego kopiowania plików skilli w .agents/skills/.
- Natywny Instalator: ./os-add-skill <nazwa-skilla> (zabezpieczony przed Path Traversal): najpierw lokalny szablon ~/.antigravity/templates/v7.1-swarm (offline), potem źródła zdalne; albo oficjalne CLI Antigravity.
- Rygor Bezpieczeństwa: instalacja ze zdalnych źródeł z filtrem ryzyka: `npx antigravity-awesome-skills --path .agents/skills --risk safe,none`.

🔒 8. ŚRODKI BEZPIECZEŃSTWA & GIT WORKTREE AUTOMATION
- Secrets Sanitization (R-SEC-01): zakaz odczytu plików .env i tabel konfiguracyjnych bez maskowania wyjścia (grep -v, sed, awk).
- Role Enforcement (Git Hook): scripts/install-git-hooks.sh instaluje pre-commit uruchamiający scripts/check_coordinator_role.sh: blokuje commit kodu (src/, api/, ui_dashboard/, lib/, app/, components/) na main/master i wymaga ważnego handshake'u Buildera. Commity Buildera oznaczamy SWARM_ROLE=builder.
- Hooki Claude Code (.claude/settings.json): PreToolUse (Edit|Write|NotebookEdit) → .agents/hooks/claude-pre-tool-guard.sh blokuje zapis kodu na main/master; SessionStart wykonuje git pull --rebase, UserPromptSubmit wypisuje linię re-groundingu (branch, zadanie, SSOT), PreCompact robi zrzut przed kompaktowaniem, Stop i SessionEnd zrzucają stan (MEMORY.md, task.md) poza main/master.
- Git Worktree Isolation: Builder pracuje w ./tmp/worktrees/ (./os-run-builder <gałąź> lub /worktree-init).
- Protokół Handshake (.agents/swarm/): Builder i Auditor zapisują <conversation_id>_<role>_handshake.json (raport z weryfikacją i listą zmian); walidacja: scripts/validate-handshakes.py.
- Cleanup Orchestration: @brooks-lint oraz @finishing-a-development-branch.

🧠 9. SECOND BRAIN & POUFNOŚĆ (NOWE W 7.x, ISO 27001)
Vault sejf_tk (Obsidian LLM Wiki) jest zasobem zewnętrznym; dostęp agentów reguluje polityka z CLAUDE.md i skill second-brain:
- Gemini w planie konsumenckim (brak DPA) czyta wyłącznie index-public.md i strony bez flagi poufności. Strażnik scripts/guard_confidential_gemini.py (PreToolUse; rejestracja w .gemini/, .antigravity/, .agents/hooks.json) odmawia odczytu stron poufnych, index.md i wiki/overview.md oraz rekurencyjnego wyszukiwania (grep -r, rg, ag, ack, git grep). Zakaz zapisu w vaulcie dla Gemini jest polityką bez blokady technicznej.
- Claude Code i Claude Desktop (konto MIW Group, DPA) mają stałą zgodę na czytanie stron poufnych, ale nie kopiują ich treści do repozytoriów, MEMORY.md, task.md, handshake'ów ani opisów commitów/PR. Skaner scripts/scan_confidential_leaks.py (frazy kontrolne, wzorce sekretów) jest częścią QA gate.
- Publikacja notatek: scripts/publish_knowledge_to_vault.py / /os-publish-knowledge (skan PII i sekretów, dry-run domyślnie, bez --ingest).
- Szczegóły i decyzje: .agents/specs/second-brain-integration-plan.md, .agents/specs/second-brain-propagation-report.md.

🏷️ 10. WERSJONOWANIE I TESTY
- Wersję systemu określa plik VERSION; nagłówek wydania w CHANGELOG.md, katalog szablonu ~/.antigravity/templates/v<MAJOR.MINOR>-swarm oraz napisy w żywych plikach muszą z nim zgadzać się (Rule 4 w core-rule.md, wymusza tests/test_version_consistency.py).
- QA gate przed PR: shellcheck, py_compile, validate-handshakes, scan_confidential_leaks, pytest tests (CLAUDE.md sekcja 5).
- os-upgrade-project scala hooks.json (scripts/merge_hooks_json.py) zamiast go nadpisywać; --refresh-hooks podmienia tylko wpisy zarządzane.

⚠️ 11. ZNANE OGRANICZENIA (stan 2026-11-09)
- .agents/hooks/claude-pre-tool-guard.sh kończy się kodem 1, który w Claude Code nie blokuje wywołania (blokuje kod 2). Ochrona main/master po stronie Claude'a jest więc zasadą, nie blokadą techniczną; decyzja właściciela: bez zmian.
- Strażnik poufności nie pilnuje Claude'a (rozpoznaje modele po modelName).
- Dla narzędzi bez hooków (Cursor, Codex, aider) zakazy dostępu do vaulta są polityką.

Podpisano: Antigravity Orchestrator & GEM
