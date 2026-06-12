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

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_dir = os.path.join(project_root, "vault", ".agents", "skills")
    
    if not os.path.exists(skills_dir):
        print(f"⚠️  Katalog skilli nie istnieje w: {skills_dir}")
        return

    plugin_dir = os.path.expanduser("~/.gemini/config/plugins/agents-os-local")
    commands_dir = os.path.join(plugin_dir, "commands")
    os.makedirs(commands_dir, exist_ok=True)
    
    # Usuwamy stare komendy żeby uniknąć osieroconych plików
    for f in os.listdir(commands_dir):
        if f.endswith(".toml"):
            os.remove(os.path.join(commands_dir, f))
            
    print("⚙️ Generowanie komend ukośnika (Plugins/Commands)...")
    
    count = 0
    for skill_name in os.listdir(skills_dir):
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
        description = metadata.get("description", f"Uruchom skill {name}")
        trigger = metadata.get("trigger", metadata.get("trigger_words", f"@{name}"))
        
        # Oczyszczenie napisów do zapisu w TOML
        description_clean = description.replace('"', '\\"').replace('\n', ' ')
        
        toml_path = os.path.join(commands_dir, f"{name}.toml")
        
        # Tworzymy treść TOML
        toml_content = f'description = "{description_clean}"\n'
        toml_content += f'prompt = "Użyj skilla {name}. Trigger: {trigger}."\n'
        
        try:
            with open(toml_path, "w", encoding="utf-8") as f:
                f.write(toml_content)
            print(f"   ✔ Zarejestrowano komendę: /{name}")
            count += 1
        except Exception as e:
            print(f"   ❌ Błąd zapisu komendy /{name}: {e}")
            
    print(f"✅ Wygenerowano {count} komend ukośnika w {commands_dir}.")

if __name__ == "__main__":
    main()
