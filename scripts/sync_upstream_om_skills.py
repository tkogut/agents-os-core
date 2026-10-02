#!/usr/bin/env python3
"""
sync_upstream_om_skills.py — Synchronizes Open-Mercato skills from upstream repository.
Part of AGENTS-OS Swarm Harness.

Usage:
  python3 scripts/sync_upstream_om_skills.py [--check-only] [--output-summary <path>]

Actions:
  1. Clones or fetches https://github.com/open-mercato/skills (or custom upstream).
  2. Compares upstream skills with local global_skills/ and vault/.agents/skills/.
  3. Copies new and modified skills to:
     - global_skills/
     - .agents/skills/
     - vault/.agents/skills/
  4. Generates/updates Claude Code symlinks in:
     - .claude/skills/
     - vault/.claude/skills/
  5. Updates harness metrics in os-upgrade-project and docs/API.md if skill count changed.
  6. Emits a structured summary for CI / GitHub Actions PR creation.
"""

import argparse
import datetime
import os
import re
import shutil
import subprocess
import sys
import tempfile


def get_repo_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def extract_skill_description(skill_dir):
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return ""
    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    return ""


def compare_skill_dirs(src, dst):
    """Returns True if dst has any differences from src or if dst does not exist."""
    if not os.path.exists(dst):
        return True
    res = subprocess.run(["diff", "-rq", src, dst], capture_output=True, text=True)
    return res.returncode != 0


def update_harness_counts(repo_root, total_skills, total_om_skills):
    """Updates skills count in os-upgrade-project and docs/API.md if needed."""
    # 1. os-upgrade-project
    upgrade_script = os.path.join(repo_root, "os-upgrade-project")
    if os.path.isfile(upgrade_script):
        with open(upgrade_script, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace 7X+ skilli and 4X skilli Open-Mercato
        content = re.sub(r"\d+\+ skilli", f"{total_skills}+ skilli", content)
        content = re.sub(r"\d+ skilli om-\*", f"{total_om_skills} skilli om-*", content)
        content = re.sub(r"\d+ skilli Open-Mercato", f"{total_om_skills} skilli Open-Mercato", content)
        
        with open(upgrade_script, "w", encoding="utf-8") as f:
            f.write(content)

    # 2. docs/API.md
    api_doc = os.path.join(repo_root, "docs", "API.md")
    if os.path.isfile(api_doc):
        with open(api_doc, "r", encoding="utf-8") as f:
            content = f.read()
        
        content = re.sub(r"\d+\+ skilli, w tym \d+ skilli Open-Mercato",
                         f"{total_skills}+ skilli, w tym {total_om_skills} skilli Open-Mercato", content)
        
        with open(api_doc, "w", encoding="utf-8") as f:
            f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Sync Open-Mercato skills from upstream repository.")
    parser.add_argument("--upstream", default="https://github.com/open-mercato/skills.git",
                        help="Upstream git repository URL")
    parser.add_argument("--check-only", action="store_true",
                        help="Only check for changes without modifying local files")
    parser.add_argument("--output-summary", default=None,
                        help="File path to write markdown summary to")
    parser.add_argument("--github-output", default=None,
                        help="File path for GITHUB_OUTPUT environment file")
    args = parser.parse_args()

    repo_root = get_repo_root()
    global_dir = os.path.join(repo_root, "global_skills")
    vault_agent_dir = os.path.join(repo_root, "vault", ".agents", "skills")
    local_agent_dir = os.path.join(repo_root, ".agents", "skills")
    claude_dir = os.path.join(repo_root, ".claude", "skills")
    vault_claude_dir = os.path.join(repo_root, "vault", ".claude", "skills")

    print(f"🚀 Checking upstream skills repository: {args.upstream}...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        clone_cmd = ["git", "clone", "--depth", "1", args.upstream, tmp_dir]
        res = subprocess.run(clone_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ Failed to clone upstream repository: {res.stderr}", file=sys.stderr)
            sys.exit(1)

        upstream_skills_dir = os.path.join(tmp_dir, "skills")
        if not os.path.isdir(upstream_skills_dir):
            print(f"❌ Directory 'skills/' not found in upstream repository.", file=sys.stderr)
            sys.exit(1)

        upstream_skills = [
            d for d in os.listdir(upstream_skills_dir)
            if os.path.isdir(os.path.join(upstream_skills_dir, d))
        ]
        upstream_skills.sort()

        new_skills = []
        updated_skills = []

        for skill in upstream_skills:
            src = os.path.join(upstream_skills_dir, skill)
            dst_global = os.path.join(global_dir, skill)
            if not os.path.exists(dst_global):
                new_skills.append(skill)
            elif compare_skill_dirs(src, dst_global):
                updated_skills.append(skill)

        total_changes = len(new_skills) + len(updated_skills)
        print(f"🔍 Scan complete: {len(upstream_skills)} upstream skills found.")
        print(f"   • New skills: {len(new_skills)}")
        print(f"   • Modified skills: {len(updated_skills)}")

        if total_changes == 0:
            print("✅ All OM skills are already up-to-date with upstream.")
            if args.github_output:
                with open(args.github_output, "a", encoding="utf-8") as f:
                    f.write("has_changes=false\n")
            if args.output_summary:
                with open(args.output_summary, "w", encoding="utf-8") as f:
                    f.write("### 🟢 OM Skills Sync\nAll skills are up-to-date with upstream.\n")
            sys.exit(0)

        if args.check_only:
            print("⚠️ Changes detected (check-only mode active):")
            for s in new_skills:
                print(f"   + [NEW] {s}")
            for s in updated_skills:
                print(f"   ~ [MOD] {s}")
            if args.github_output:
                with open(args.github_output, "a", encoding="utf-8") as f:
                    f.write("has_changes=true\n")
            sys.exit(1)

        # Apply synchronization
        print("\n⚙️ Applying synchronization across harness directories...")
        target_dirs = [global_dir, vault_agent_dir, local_agent_dir]
        for s in new_skills + updated_skills:
            src = os.path.join(upstream_skills_dir, s)
            for t_dir in target_dirs:
                dst = os.path.join(t_dir, s)
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            
            # Symlinks
            for c_dir, rel_target in [(claude_dir, "../../.agents/skills"),
                                      (vault_claude_dir, "../../.agents/skills")]:
                os.makedirs(c_dir, exist_ok=True)
                link_path = os.path.join(c_dir, s)
                if os.path.islink(link_path) or os.path.exists(link_path):
                    os.remove(link_path)
                os.symlink(os.path.join(rel_target, s), link_path)

            print(f"   ✓ Synced {s}")

        # Update metrics & counts
        total_vault_skills = len([
            d for d in os.listdir(vault_agent_dir)
            if os.path.isdir(os.path.join(vault_agent_dir, d))
        ])
        total_om_skills = len([
            d for d in os.listdir(vault_agent_dir)
            if os.path.isdir(os.path.join(vault_agent_dir, d)) and d.startswith("om-")
        ])

        update_harness_counts(repo_root, total_vault_skills, total_om_skills)
        print(f"📊 Updated harness counts: {total_vault_skills} total skills ({total_om_skills} OM skills).")

        # Prepare summary
        today = datetime.date.today().isoformat()
        summary_lines = [
            f"## 🛸 Weekly Open-Mercato Skills Sync ({today})",
            "",
            f"Automated synchronization from upstream `{args.upstream}`:",
            f"- **New skills added**: {len(new_skills)}",
            f"- **Existing skills updated**: {len(updated_skills)}",
            f"- **Total repository skills**: {total_vault_skills} (w tym {total_om_skills} `om-*`)",
            "",
        ]

        if new_skills:
            summary_lines.append("### 🆕 New Skills:")
            for s in new_skills:
                desc = extract_skill_description(os.path.join(global_dir, s))
                summary_lines.append(f"- **`{s}`**: {desc}")
            summary_lines.append("")

        if updated_skills:
            summary_lines.append("### 🔄 Updated Skills:")
            for s in updated_skills:
                summary_lines.append(f"- `{s}`")
            summary_lines.append("")

        summary_text = "\n".join(summary_lines)

        if args.output_summary:
            with open(args.output_summary, "w", encoding="utf-8") as f:
                f.write(summary_text)

        if args.github_output:
            with open(args.github_output, "a", encoding="utf-8") as f:
                f.write("has_changes=true\n")
                f.write(f"new_count={len(new_skills)}\n")
                f.write(f"updated_count={len(updated_skills)}\n")
                f.write(f"total_skills={total_vault_skills}\n")

        print("✨ Sync completed successfully.")


if __name__ == "__main__":
    main()
