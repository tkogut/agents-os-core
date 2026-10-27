#!/usr/bin/env python3
"""
guard_confidential_gemini.py — PreToolUse Guard for Gemini Confidentiality Policy
Part of AGENTS-OS Swarm Governance & Data Protection (v7.0).

Policy & Governance:
- Gemini agents running under consumer plans (no DPA) MUST NEVER access files
  marked 'confidential: true', their raw source copies (raw_path), or their
  human-zone originals (e.g. in Firma/).
- Fail-Closed: if model is empty, unknown, or contains 'gemini' -> strict block.
- Zero Full-Disk Probing: vault path is strictly resolved via config / env / default fallback
  (C:\\Users\\tkogut\\Documents\\sejf_tk -> /mnt/c/Users/tkogut/Documents/sejf_tk). Never walks external drives.
- Fast-Bypass (<0.1ms): immediately allows non-vault file and command operations.
- Dynamic TTL Cache (60s): caches vault frontmatter index in /tmp to prevent WSL 9p timeouts.
- Refusals redirect to Claude Code.
"""

import sys
import json
import os
import re
import time

VAULT_DEFAULT_PATH = "/mnt/c/Users/tkogut/Documents/sejf_tk"
CACHE_FILE = "/tmp/guard_sejf_tk_cache.json"
CACHE_TTL = 60.0  # seconds

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

def load_agentic_config() -> dict:
    """Locates and loads .ai/agentic.config.json if present."""
    base_dirs = [
        os.getcwd(),
        os.path.dirname(os.path.abspath(__file__)),
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    ]
    for b in base_dirs:
        cfg_path = os.path.join(b, ".ai", "agentic.config.json")
        if os.path.isfile(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as fp:
                    return json.load(fp)
            except Exception:
                pass
    return {}

def resolve_vault_path(env_path: str = None) -> str:
    """
    Resolves vault path strictly using hierarchy:
    1. env_path (if passed explicitly)
    2. .ai/agentic.config.json (context.second_brain.local_path)
    3. os.environ['OBSIDIAN_VAULT_PATH']
    4. VAULT_DEFAULT_PATH (/mnt/c/Users/tkogut/Documents/sejf_tk)
    Zero recursive disk scanning.
    """
    if env_path:
        return normalize_path(env_path)

    cfg = load_agentic_config()
    cfg_path = (cfg.get("context", {}).get("second_brain", {}).get("local_path") or
                cfg.get("context", {}).get("second_brain", {}).get("windows_default_path"))
    if cfg_path:
        norm_cfg = normalize_path(cfg_path)
        if os.path.isdir(norm_cfg):
            return norm_cfg

    env_val = os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_val:
        norm_env = normalize_path(env_val)
        if os.path.isdir(norm_env):
            return norm_env

    return normalize_path(VAULT_DEFAULT_PATH)

def get_confidential_paths_dynamic(vault_dir: str):
    """
    Returns (confidential_rels, confidential_dirs, confidential_basenames) using 60s TTL cache.
    Scans frontmatter:
    1. confidential: true
    2. raw_path: <path>
    3. Oryginał (strefa człowieka): [[<title>]] -> resolves to vault file
    """
    now = time.time()
    if os.path.isfile(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            if (now - data.get("timestamp", 0) < CACHE_TTL and
                data.get("vault_dir") == vault_dir):
                return (set(data.get("confidential_rels", [])),
                        set(data.get("confidential_dirs", [])),
                        set(data.get("confidential_basenames", [])))
        except Exception:
            pass

    confidential_rels = set()
    confidential_dirs = set()
    confidential_basenames = set()
    
    if not os.path.isdir(vault_dir):
        return confidential_rels, confidential_dirs, confidential_basenames

    md_by_basename = {}
    all_md_files = []

    for root, dirs, files in os.walk(vault_dir):
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

    for full, rel in all_md_files:
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read(16384)

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

                m_raw = re.search(r"^\s*raw_path:\s*[\"']?([^\"'\n\r]+)[\"']?", content, re.MULTILINE | re.IGNORECASE)
                if m_raw:
                    raw_val = m_raw.group(1).strip().replace("\\", "/").lower()
                    confidential_rels.add(raw_val)
                    confidential_basenames.add(os.path.basename(raw_val))
                    d = os.path.dirname(raw_val)
                    while d and d != ".":
                        confidential_dirs.add(d)
                        d = os.path.dirname(d)

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

    # Save cache atomically
    try:
        cache_data = {
            "timestamp": now,
            "vault_dir": vault_dir,
            "confidential_rels": list(confidential_rels),
            "confidential_dirs": list(confidential_dirs),
            "confidential_basenames": list(confidential_basenames),
        }
        tmp_cache = f"{CACHE_FILE}.tmp.{os.getpid()}"
        with open(tmp_cache, "w", encoding="utf-8") as fp:
            json.dump(cache_data, fp)
        os.replace(tmp_cache, CACHE_FILE)
    except Exception:
        pass

    return confidential_rels, confidential_dirs, confidential_basenames

def evaluate_hook(payload: dict) -> dict:
    # 1. Check Model Identification & Provider DPA Status
    model_name = payload.get("modelName", "") or ""
    model_name_low = model_name.lower()

    # If explicitly Claude and does not mention gemini, allow
    if "claude" in model_name_low and "gemini" not in model_name_low:
        return {"decision": "allow"}

    # Check if Gemini Enterprise DPA is signed in configuration
    cfg = load_agentic_config()
    dpa_signed = cfg.get("data_protection", {}).get("gemini", {}).get("dpa_signed", False)
    if dpa_signed:
        return {"decision": "allow"}

    # Fail-closed: consumer Gemini or unknown model
    tool_call = payload.get("toolCall", {})
    tool_name = (tool_call.get("name") or "").lower()
    args = tool_call.get("args") or {}

    vault_dir = resolve_vault_path()

    file_path = args.get("Path") or args.get("AbsolutePath") or args.get("file_path") or args.get("path") or ""
    target_dir = args.get("Directory") or args.get("dir") or args.get("folder") or ""
    cmd_line = args.get("CommandLine") or args.get("command") or ""

    # --- FAST-BYPASS (<0.1ms) ---
    # If operation clearly does NOT touch vault or keywords, exit immediately
    touches_vault = False
    norm_file = normalize_path(file_path) if file_path else ""
    norm_dir = normalize_path(target_dir) if target_dir else ""
    cmd_norm = cmd_line.replace("\\", "/").lower() if cmd_line else ""

    if norm_file and (norm_file.startswith(vault_dir) or "sejf_tk" in norm_file or "sejf-tk" in norm_file):
        touches_vault = True
    elif norm_dir and (norm_dir.startswith(vault_dir) or "sejf_tk" in norm_dir or "sejf-tk" in norm_dir):
        touches_vault = True
    elif cmd_norm:
        if any(k in cmd_norm for k in ["sejf_tk", "sejf-tk", "wiki", "firma", "raw/notes", "raw/", "umowa", "vaga"]):
            touches_vault = True

    if not touches_vault:
        return {"decision": "allow"}

    # If touches vault, evaluate against confidential index
    conf_rels, conf_dirs, conf_basenames = get_confidential_paths_dynamic(vault_dir)

    # 2. Check direct file access
    if norm_file and norm_file.startswith(vault_dir):
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

    # 3. Check search directory tools
    if norm_dir and norm_dir.startswith(vault_dir):
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
    if tool_name in ["run_command", "bash", "execute_command"] and cmd_norm:
        # 4a. Check direct reference to confidential file
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

        # 4b. Check recursive search over confidential dirs
        has_search_cmd = bool(re.search(r'\b(grep|egrep|fgrep|rg|ripgrep|ag|find)\b', cmd_norm))
        has_recursive_flag = bool(re.search(r'(-[a-z]*r|--recursive|-exec\b)', cmd_norm))
        
        if has_search_cmd and has_recursive_flag:
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
        sys.stderr.write(f"[guard_confidential_gemini.py Error] {e}\n")
        json.dump({
            "decision": "deny",
            "reason": f"Błąd wewnętrzny hooka ochrony poufności (Fail-Closed): {e}"
        }, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")

if __name__ == "__main__":
    main()
