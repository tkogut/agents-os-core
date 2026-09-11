---
name: swarm-onboarding
description: Automatyczny protokół onboardingu i synchronizacji kontekstu dla agentów dołączających do projektu (Antigravity, Claude Code, Cursor itp.). Bada stan Gita, czyta SSOT MEMORY.md, task.md, reguły Triady, ostatnie PR-y i decyzje, generując zwięzły Executive Briefing.
trigger: /swarm-onboarding
---

# 🐝 Swarm Agent Onboarding Protocol (AGENTS-OS v6.5)

Uruchom ten skill za każdym razem, gdy nowy agent (lub nowa sesja agenta) dołącza do projektu lub zmienia rolę w Swarmie.

## 🚀 Szybkie Uruchomienie Silnika Onboardingu

Wykonaj skrypt onboardingu projektu w terminalu:

```bash
python3 .agents/skills/swarm-onboarding/scripts/onboard.py || python3 global_skills/swarm-onboarding/scripts/onboard.py
```

---

## 🧭 Protokół Krok po Kroku (Gdy uruchamiasz manualnie w czacie)

Jeśli jesteś modelem LLM i realizujesz onboarding wewnątrz czatu, wykonaj następujące 5 kroków weryfikacji:

1. **Synchronizacja Gita**:
   - Sprawdź bieżącą gałąź i status: `git status`, `git branch -a`.
   - Jeśli gałąź jest opóźniona względem `origin`: wykonaj `git pull --rebase`.
   - Przejrzyj 5 ostatnich commitów: `git log -n 5 --oneline`.

2. **Ingestia Pamięci Trwałej (SSOT)**:
   - Otwórz i przeczytaj `.agents/MEMORY.md`.
   - Zidentyfikuj: architekturę systemu, konfigurację środowiska/VPS, aktywne bezpieczniki oraz stan produkcji.

3. **Status Sprintu & Zakazy (task.md)**:
   - Przeczytaj `task.md` (lub `.agents/task.md`).
   - Zanotuj aktualny cel, zrealizowane tickety oraz sekcje **"Czego świadomie NIE robić" / odrzucone hipotezy**.

4. **Architektura & Plany (.agents/plans/)**:
   - Sprawdź ostatnie plany w `.agents/plans/` (np. `PLAN-010`, `PLAN-011`).

5. **Raport Executive Briefing dla Użytkownika**:
   - Przedstaw 4-punktowe podsumowanie:
     1. **Gdzie jesteśmy**: Gałąź, commity, gotowość Gita.
     2. **Co wiemy**: Stan produkcji i kluczowe ustalenia z MEMORY.md.
     3. **Czego NIE ruszamy**: Odrzucone ścieżki i twarde guardraile.
     4. **Co robimy teraz**: Najbliższe zaplanowane zadanie (oraz propozycja `/grill-me` przed kodowaniem).
