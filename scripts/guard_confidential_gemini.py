#!/usr/bin/env bash
#!/usr/bin/env python3
"""
guard_confidential_gemini.py — PreToolUse Guard for Gemini Confidentiality Policy
Part of AGENTS-OS Swarm Governance & Data Protection.

Policy:
- Gemini agents running under consumer plans (no DPA) MUST NEVER access files
  marked 'confidential: true', their raw source copies (raw_path), or their
  human-zone originals (e.g. in Firma/).
- Fail-Closed: if model is empty, missing, or contains 'gemini' -> strict block.
- Dynamic discovery: builds the confidential file set from frontmatter at runtime.
- Directory searches: blocks recursive content searches (grep -r, find -exec, etc.)
  over vault directories containing confidential files.
- Refusals redirect to Claude Code.
"""

import sys
import json
import os
import re

VAULT_DEFAULT_PATH = "/mnt/c/Users/tkogut/Documents/sejf_tk"

def normalize_path(path_str: str) -> str:
    """Normalizes Windows, WSL, relative, and case variations into a canonical unix-like path."""
    if not path_str:
        return ""
    p = path_str.strip().strip("'\"")
    p = p.replace("\\", "/")
    # Match Windows drive letter: C:/... -> /mnt/c/...
    m_win = re.match(r'^([a-zA-Z]):/(.*)', p)
    if m_win:
        drive = m_win.group(1).lower()
        rest = m_win.group(2)
        p = f"/mnt/{drive}/{rest}"
    p = os.path.normpath(p)
    return p.lower()

def resolve_vault_path(env_path: str = None) -> str:
    candidate = env_path or os.environ.get("OBSIDIAN_VAULT_PATH") or VAULT_DEFAULT_PATH
    norm = normalize_path(candidate)
    if os.path.isdir(norm):
        return norm
    # Check if alternative exists
    if os.path.isdir(VAULT_DEFAULT_PATH):
        return VAULT_DEFAULT_PATH
    return norm

def get_confidential_paths_dynamic(vault_dir: str):
    """
    Dynamically scans the vault for confidential files:
    1. Frontmatter: confidential: true
    2. raw_path: <path>
    3. Oryginał (strefa człowieka): [[<title>]] -> resolves to vault file
    Returns:
      confidential_rels: set of lowercase relative paths
      confidential_dirs: set of lowercase directory paths containing confidential files
      confidential_basenames: set of lowercase file basenames
    """
    confidential_rels = set()
    confidential_dirs = set()
    confidential_basenames = set()
    
    if not os.path.isdir(vault_dir):
        return confidential_rels, confidential_dirs, confidential_basenames

    # Index all markdown files in vault for link resolution
    md_by_basename = {} # lowercase basename -> list of relative paths
    all_md_files = []

    for root, dirs, files in os.walk(vault_dir):
        # Ignore .git and .obsidian internals
        root_norm = root.replace("\\", "/")
        if "/.git" in root_norm or "/.obsidian" in root_norm:
            continue
        for f in files:
            if f.endswith(".md"):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, vault_dir).replace("\\", "/")
                all_md_files.append((full, rel))
                base = os.path.splitext(f)[0].lower()
                md_by_basename.setdefault(base, []).append(rel)

    # Inspect frontmatter and links
    for full, rel in all_md_files:
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read(16384) # read first 16KB

            is_confidential = False
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 2:
                    fm = parts[1]
                    if re.search(r"^\s*confidential:\s*true\b", fm, re.IGNORECASE | re.MULTILINE):
                        is_confidential = True
            
            if not is_confidential and re.search(r"confidential:\s*true\b", content[:2000], re.IGNORECASE):
                is_confidential = True

            if is_confidential:
                rel_low = rel.lower()
                confidential_rels.add(rel_low)
                confidential_basenames.add(os.path.basename(rel_low))
                d = os.path.dirname(rel_low)
                while d and d != ".":
                    confidential_dirs.add(d)
                    d = os.path.dirname(d)

                # Check raw_path
                m_raw = re.search(r"^\s*raw_path:\s*[\"']?([^\"'\n\r]+)[\"']?", content, re.MULTILINE | re.IGNORECASE)
                if m_raw:
                    raw_val = m_raw.group(1).strip().replace("\\", "/").lower()
                    confidential_rels.add(raw_val)
                    confidential_basenames.add(os.path.basename(raw_val))
                    d = os.path.dirname(raw_val)
                    while d and d != ".":
                        confidential_dirs.add(d)
                        d = os.path.dirname(d)

                # Check Oryginał (strefa człowieka): [[Title]]
                for m_orig in re.finditer(r"Orygina[łl](?:y)?\s*\([^)]*\)\s*:\s*(.+)", content, re.IGNORECASE):
                    links = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", m_orig.group(1))
                    for link in links:
                        link_base = link.strip().lower()
                        matches = md_by_basename.get(link_base, [])
                        for match in matches:
                            m_low = match.lower()
                            confidential_rels.add(m_low)
                            confidential_basenames.add(os.path.basename(m_low))
                            d = os.path.dirname(m_low)
                            while d and d != ".":
                                confidential_dirs.add(d)
                                d = os.path.dirname(d)
        except Exception:
            pass

    return confidential_rels, confidential_dirs, confidential_basenames

def evaluate_hook(payload: dict) -> dict:
    # 1. Fail-closed model identification
    model_name = payload.get("modelName", "") or ""
    model_name_low = model_name.lower()

    # If explicitly Claude and does NOT mention gemini, allow
    if "claude" in model_name_low and "gemini" not in model_name_low:
        return {"decision": "allow"}

    # Fail-closed: empty, unknown, or gemini -> enforce Gemini confidentiality policy
    tool_call = payload.get("toolCall", {})
    tool_name = (tool_call.get("name") or "").lower()
    args = tool_call.get("args") or {}

    vault_dir = resolve_vault_path()
    conf_rels, conf_dirs, conf_basenames = get_confidential_paths_dynamic(vault_dir)

    # 2. Check direct file access tools
    # Tools: read_file, view_file, open_file, read_file_range, etc.
    file_path = args.get("Path") or args.get("AbsolutePath") or args.get("file_path") or args.get("path") or ""
    if file_path:
        norm_file = normalize_path(file_path)
        # Check if inside vault
        if norm_file.startswith(vault_dir):
            rel = os.path.relpath(norm_file, vault_dir).replace("\\", "/").lower()
            if rel in conf_rels or os.path.basename(rel) in conf_basenames:
                return {
                    "decision": "deny",
                    "reason": (
                        "🛑 [POLITYKA POUFNOŚCI GEMINI — BRAK DPA] ODRZUCONO:\n"
                        f"Plik '{rel}' jest oznaczony jako 'confidential: true' (lub stanowi powiązany oryginał/kopię surową).\n"
                        "Z powodu braku umowy powierzenia (DPA) w konsumenckim planie Google AI Pro, modele Gemini "
                        "mają bezwzględny zakaz odczytu i przetwarzania tego dokumentu, nawet po zatwierdzeniu przez użytkownika.\n"
                        "➡️ Skieruj zadanie do agenta Claude Code."
                    )
                }

    # 3. Check search tools (search_files, grep_search, file_search, find_files)
    target_dir = args.get("Directory") or args.get("dir") or args.get("folder") or args.get("path") or ""
    if target_dir:
        norm_dir = normalize_path(target_dir)
        if norm_dir.startswith(vault_dir):
            rel_dir = os.path.relpath(norm_dir, vault_dir).replace("\\", "/").lower()
            if rel_dir == "." or rel_dir in conf_dirs:
                return {
                    "decision": "deny",
                    "reason": (
                        "🛑 [POLITYKA POUFNOŚCI GEMINI — BRAK DPA] ODRZUCONO:\n"
                        f"Próba przeszukania katalogu '{rel_dir}' zawierającego pliki poufne.\n"
                        "Wyniki przeszukiwania nie mogą zostać przefiltrowane po fakcie i trafiłyby do kontekstu Gemini.\n"
                        "➡️ Wyklucz pliki poufne lub wykonaj operację przez agenta Claude Code."
                    )
                }

    # 4. Check run_command (Bash)
    if tool_name in ["run_command", "bash", "execute_command"]:
        cmd_line = args.get("CommandLine") or args.get("command") or ""
        cmd_norm = cmd_line.replace("\\", "/").lower()

        # 4a. Check if command references any confidential file directly
        for rel in conf_rels:
            base = os.path.basename(rel)
            if rel in cmd_norm or (len(base) > 5 and base in cmd_norm):
                return {
                    "decision": "deny",
                    "reason": (
                        f"🛑 [POLITYKA POUFNOŚCI GEMINI — BRAK DPA] ODRZUCONO (Bash):\n"
                        f"Polecenie odwołuje się bezpośrednio do pliku poufnego '{base}'.\n"
                        "Odczyt zablokowany dla agentów Gemini. Użyj agenta Claude Code."
                    )
                }

        # 4b. Check for directory-wide / recursive searches over confidential folders
        # Patterns: grep -r, grep -R, rg, find with exec, etc.
        has_search_cmd = bool(re.search(r'\b(grep|egrep|fgrep|rg|ripgrep|ag|find)\b', cmd_norm))
        has_recursive_flag = bool(re.search(r'(-[a-z]*r|--recursive|-exec\b)', cmd_norm))
        
        if has_search_cmd and has_recursive_flag:
            # Check if command targets vault or any confidential directory
            targets_confidential_dir = False
            if "sejf_tk" in cmd_norm or "sejf-tk" in cmd_norm:
                targets_confidential_dir = True
            for d in ["wiki", "firma", "raw/notes", "raw", "inwestycje"]:
                if f"/{d}" in cmd_norm or f" {d}" in cmd_norm or f"\"{d}" in cmd_norm or f"'{d}" in cmd_norm:
                    targets_confidential_dir = True
                    break

            if targets_confidential_dir:
                return {
                    "decision": "deny",
                    "reason": (
                        "🛑 [POLITYKA POUFNOŚCI GEMINI — BRAK DPA] ODRZUCONO (Bash Search):\n"
                        "Wykryto rekurencyjne przeszukiwanie katalogu zawierającego pliki poufne (grep -r/find po vaulcie/wiki/Firma/raw).\n"
                        "Zgodnie z polityką bezpieczeństwa Gemini wyniki nie mogą trafić do modelu, gdyż nie można ich przefiltrować po fakcie.\n"
                        "➡️ Użyj agenta Claude Code lub wyklucz pliki poufne."
                    )
                }

    # Default allow for non-confidential operations
    return {"decision": "allow"}

def main():
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            json.dump({"decision": "allow"}, sys.stdout)
            sys.stdout.write("\n")
            return

        payload = json.loads(raw_input)
        result = evaluate_hook(payload)
        json.dump(result, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    except Exception as e:
        # Fail-closed on error for safety
        sys.stderr.write(f"[guard_confidential_gemini.py Error] {e}\n")
        json.dump({
            "decision": "deny",
            "reason": f"Błąd wewnętrzny hooka ochrony poufności (Fail-Closed): {e}"
        }, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")

if __name__ == "__main__":
    main()
