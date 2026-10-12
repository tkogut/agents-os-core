#!/usr/bin/env python3
import os
import re

def parse_frontmatter(content):
    metadata = {}
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return metadata
    
    yaml_lines = match.group(1).splitlines()
    current_key = None
    for line in yaml_lines:
        if not line.strip():
            continue
        m = re.match(r'^([a-zA-Z0-9_\-]+)\s*:\s*(.*)$', line)
        if m:
            current_key = m.group(1)
            metadata[current_key] = m.group(2).strip().strip('"').strip("'")
        elif current_key and line.startswith(' '):
            metadata[current_key] += ' ' + line.strip().strip('"').strip("'")
    return metadata

def generate_claude_commands(skills, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    count = 0
    for skill in skills:
        name = skill["name"]
        description = skill["description"]
        trigger = skill["trigger"]
        cmd_path = os.path.join(target_dir, f"{name}.md")
        
        # Don't overwrite existing specialized manual commands
        CORE_MANUAL_COMMANDS = {"commit", "grill-me", "handshake", "qa-gate", "worktree-init"}
        if name in CORE_MANUAL_COMMANDS and os.path.exists(cmd_path):
            continue
        if os.path.exists(cmd_path):
            with open(cmd_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "<!-- manual-command -->" in content:
                continue

        cmd_content = f"""---
description: {description}
---

Przeczytaj instrukcje ze skilla `{name}` z pliku `.claude/skills/{name}/SKILL.md` (lub `.agents/skills/{name}/SKILL.md`) i wykonaj zadanie zgodnie z jego procedurą.
Trigger context: {trigger}

Dodatkowe argumenty/kontekst od użytkownika:
$ARGUMENTS
"""
        try:
            with open(cmd_path, "w", encoding="utf-8") as f:
                f.write(cmd_content)
            count += 1
        except Exception as e:
            print(f"   ❌ Błąd zapisu komendy Claude /{name}: {e}")
    return count

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_dir = os.path.join(project_root, "vault", ".agents", "skills")
    
    if not os.path.exists(skills_dir):
        print(f"⚠️  Katalog skilli nie istnieje w: {skills_dir}")
        return

    # 1. Zbieranie metadanych wszystkich skilli
    skills = []
    for skill_name in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, skill_name)
        if not os.path.isdir(skill_path):
            continue
            
        skill_md_path = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(skill_md_path):
            continue
            
        try:
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"   ❌ Błąd odczytu {skill_name}/SKILL.md: {e}")
            continue
            
        metadata = parse_frontmatter(content)
        name = metadata.get("name", skill_name)
        description = metadata.get("description", f"Uruchom skill {name}").replace('"', '\\"').replace('\n', ' ')
        trigger = metadata.get("trigger", metadata.get("trigger_words", f"@{name}"))
        skills.append({
            "name": name,
            "description": description,
            "trigger": trigger
        })

    # 2. Generowanie komend TOML dla Gemini CLI
    gemini_plugin_dir = os.path.expanduser("~/.gemini/config/plugins/agents-os-local")
    gemini_commands_dir = os.path.join(gemini_plugin_dir, "commands")
    if os.path.exists(os.path.dirname(gemini_plugin_dir)):
        os.makedirs(gemini_commands_dir, exist_ok=True)
        for f in os.listdir(gemini_commands_dir):
            if f.endswith(".toml"):
                os.remove(os.path.join(gemini_commands_dir, f))
        gemini_count = 0
        for skill in skills:
            toml_path = os.path.join(gemini_commands_dir, f"{skill['name']}.toml")
            toml_content = f'description = "{skill["description"]}"\n'
            toml_content += f'prompt = "Użyj skilla {skill["name"]}. Trigger: {skill["trigger"]}."\n'
            try:
                with open(toml_path, "w", encoding="utf-8") as f:
                    f.write(toml_content)
                gemini_count += 1
            except Exception as e:
                print(f"   ❌ Błąd zapisu komendy Gemini /{skill['name']}: {e}")
        print(f"✅ Gemini: Wygenerowano {gemini_count} komend w {gemini_commands_dir}")

    # 3. Generowanie komend Markdown dla Claude Code (GLOBALNIE w ~/.claude/commands/)
    user_claude_commands = os.path.expanduser("~/.claude/commands")
    claude_user_count = generate_claude_commands(skills, user_claude_commands)
    print(f"✅ Claude (Global): Wygenerowano {claude_user_count} komend w {user_claude_commands}")

    # 4. Generowanie komend Markdown dla repozytorium vault/.claude/commands/ oraz .claude/commands/
    vault_claude_commands = os.path.join(project_root, "vault", ".claude", "commands")
    vault_count = generate_claude_commands(skills, vault_claude_commands)
    print(f"✅ Claude (Vault): Wygenerowano {vault_count} komend w {vault_claude_commands}")

    repo_claude_commands = os.path.join(project_root, ".claude", "commands")
    if os.path.exists(repo_claude_commands):
        repo_count = generate_claude_commands(skills, repo_claude_commands)
        print(f"✅ Claude (Repo): Wygenerowano {repo_count} komend w {repo_claude_commands}")

if __name__ == "__main__":
    main()
