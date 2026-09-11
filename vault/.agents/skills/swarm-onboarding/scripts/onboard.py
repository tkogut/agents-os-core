#!/usr/bin/env python3
"""
AGENTS-OS v6.5 Swarm Edition — Universal Agent Onboarding Engine
Scans git state, MEMORY.md, task.md, plans, and swarm handshakes to generate
an executive onboarding briefing for any incoming agent (Antigravity, Claude Code, Cursor).
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def find_project_root():
    curr = Path.cwd().resolve()
    while curr != curr.parent:
        if (curr / ".agents").exists() or (curr / ".git").exists():
            return curr
        curr = curr.parent
    return Path.cwd().resolve()

def run_cmd(cmd, cwd):
    try:
        res = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True, timeout=10)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), 1

def format_section(title, content):
    border = "=" * 70
    return f"\n{border}\n📌 {title}\n{border}\n{content}\n"

def main():
    root = find_project_root()
    print(f"🚀 [SWARM ONBOARDING] Inicjalizacja kontekstu projektu w: {root}")

    # 1. Git Status & Remote Sync
    git_branch, _, _ = run_cmd("git rev-parse --abbrev-ref HEAD", root)
    git_status, _, _ = run_cmd("git status --short", root)
    git_log, _, _ = run_cmd("git log -n 5 --oneline", root)
    git_remote, _, _ = run_cmd("git remote -v", root)

    git_summary = f"• Gałąź lokalna: {git_branch or 'Brak (nie repozytorium git)'}\n"
    if git_status:
        staged = len([l for l in git_status.splitlines() if l and l[0] in 'MADRC'])
        unstaged = len([l for l in git_status.splitlines() if l and l[1] in 'MD?'])
        git_summary += f"• Stan drzewa: ⚠️ Niezacommitowane zmiany (Staged: {staged}, Unstaged/Untracked: {unstaged})\n"
    else:
        git_summary += "• Stan drzewa: ✅ Czyste (working tree clean)\n"

    git_summary += f"• Ostatnie commity:\n"
    for line in (git_log.splitlines() if git_log else ["(brak commitów)"]):
        git_summary += f"    {line}\n"

    # 2. SSOT Memory Engine (.agents/MEMORY.md)
    memory_path = root / ".agents" / "MEMORY.md"
    memory_snippet = "⚠️ Plik .agents/MEMORY.md nie istnieje. Zainicjuj go za pomocą os-upgrade-project."
    if memory_path.exists():
        try:
            text = memory_path.read_text(encoding="utf-8")
            lines = text.splitlines()
            extracted = []
            for line in lines[:60]:
                if line.startswith("#") or line.strip().startswith("- **") or line.strip().startswith("• **"):
                    extracted.append(line)
            memory_snippet = "\n".join(extracted) if extracted else text[:1000]
        except Exception as e:
            memory_snippet = f"Błąd odczytu MEMORY.md: {e}"

    # 3. Active Tasks & Sprint (.agents/task.md or task.md)
    task_path = root / "task.md"
    if not task_path.exists():
        task_path = root / ".agents" / "task.md"
    
    task_snippet = "ℹ️ Brak aktywnego task.md. Sprawdź .agents/plans/ pod kątem planów wdrożeniowych."
    if task_path.exists():
        try:
            task_text = task_path.read_text(encoding="utf-8")
            t_lines = task_text.splitlines()
            header = t_lines[:20]
            bottom_lines = t_lines[-35:] if len(t_lines) > 35 else []
            
            task_snippet = "--- [NAGŁÓWEK / CEL SPRINTU] ---\n" + "\n".join(header)
            if bottom_lines:
                task_snippet += "\n\n--- [NAJNOWSZY STATUS / WNIOSKI Z KOŃCA TASK.MD] ---\n" + "\n".join(bottom_lines)
        except Exception as e:
            task_snippet = f"Błąd odczytu task.md: {e}"

    # 4. Architectural Plans (.agents/plans/)
    plans_dir = root / ".agents" / "plans"
    plans_summary = "Brak katalogu .agents/plans/"
    if plans_dir.is_dir():
        plans = sorted([p.name for p in plans_dir.glob("*.md") if p.name != "000-TEMPLATE.md"])
        if plans:
            plans_summary = f"Znaleziono {len(plans)} planów architektonicznych. Najnowsze:\n"
            for p in plans[-5:]:
                plans_summary += f"  • .agents/plans/{p}\n"
        else:
            plans_summary = "Brak planów wdrożeniowych w .agents/plans/"

    # 5. Worktrees & Swarm Handshakes
    worktrees_dir = root / "tmp" / "worktrees"
    wt_summary = "• Aktywne Git Worktrees: brak (izolacja czysta)\n"
    if worktrees_dir.is_dir():
        active_wts = [w.name for w in worktrees_dir.iterdir() if w.is_dir()]
        if active_wts:
            wt_summary = f"• Aktywne Git Worktrees w tmp/worktrees/: {', '.join(active_wts)}\n"

    # 6. Governance & Safety Directives
    rules_dir = root / ".agents" / "rules"
    safety_summary = (
        "1. TRIADA SWARM: Coordinator (plan & push) | Builder (kod w tmp/worktrees/) | Auditor (QA/Math)\n"
        "2. SSOT VERSION BUMP: Każdy commit/PR musi podnieść wersję SemVer we wszystkich wymaganych plikach.\n"
        "3. ZERO-LOSS / GUARDRAILS: Blokada maintenance przed testami/wdrożeniem (`scripts/maintenance.py`).\n"
        "4. BRANCH GUARD: Nigdy nie commituj/pushuj bezpośrednio do main/master — twórz gałąź funkcyjną i PR."
    )

    # Generate Full Briefing
    output = []
    output.append(format_section("1. STAN REPOZYTORIUM & SYNCHRONIZACJA GIT", git_summary + wt_summary))
    output.append(format_section("2. ARCHITEKTURA & PAMIĘĆ TRWAŁA (.agents/MEMORY.md)", memory_snippet))
    output.append(format_section("3. AKTUALNY SPRINT & ZAKAZANE ŚCIEŻKI (task.md)", task_snippet))
    output.append(format_section("4. PLANY WDROŻENIOWE (.agents/plans/)", plans_summary))
    output.append(format_section("5. BEZWZGLĘDNE REGUŁY BEZPIECZEŃSTWA (GOVERNANCE)", safety_summary))
    
    final_report = "\n".join(output)
    print(final_report)

    # Return structured instructions for agent
    print("\n" + "=" * 70)
    print("🎯 REKOMENDACJA DLA AGENTA PO ONBOARDINGU:")
    print("1. Jeśli gałąź lokalna jest w tyle za remote: wykonaj `git pull --rebase`.")
    print("2. Przed rozpoczęciem kodowania nowego zadania uruchom `/grill-me` (pre-flight wywiad).")
    print("3. Pracuj wyłącznie w gałęzi funkcyjnej lub worktree (`tmp/worktrees/`).")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
