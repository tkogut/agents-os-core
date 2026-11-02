#!/usr/bin/env python3
"""
guard_confidential_gemini.py — PreToolUse Guard for Gemini Confidentiality Policy
Part of AGENTS-OS Swarm Governance & Data Protection (v7.0 ISO 27001 Rigor).

Governance & ISO 27001 Security Specifications:
1. Zero Full-Disk Probing:
   - Vault path is strictly resolved: .ai/agentic.config.json -> OBSIDIAN_VAULT_PATH -> default fallback (C:\\Users\\tkogut\\Documents\\sejf_tk -> /mnt/c/Users/tkogut/Documents/sejf_tk).
   - If path is missing or non-existent, the guard raises a clear error and fails closed (DENY). Never traverses disks.
2. Fast-Bypass (<0.1ms):
   - Non-vault operations are immediately allowed without loading cache or accessing the vault filesystem.
3. Secure User Cache (~/.cache/agents-os-core/):
   - Cache resides in the user's private directory (0700 directory, 0600 file), never in shared /tmp.
   - Cache stores ONLY the list of protected files with timestamps and integrity checksum (SHA-256).
   - NEVER stores a precomputed allow/deny decision.
   - Tampered, corrupted, or expired (>60s) cache is rebuilt. If rebuilding fails, access is denied (FAIL-CLOSED).
4. Fail-Closed Mandate:
   - Missing vault, read errors, parsing errors, or unrebuildable cache result in a hard DENY.
   - Clean security error messages with ZERO secret leakage.
5. Gemini vs Claude Policy:
   - Consumer Gemini plans (no DPA) are strictly blocked from 'confidential: true', raw sources, and Firma/ originals.
   - Recursive searches (grep -r, find -exec) over confidential directories are blocked.
   - Redirects to Claude Code.
"""

import sys
import json
import os
import re
import time
import hashlib

VAULT_DEFAULT_PATH = "/mnt/c/Users/tkogut/Documents/sejf_tk"
CACHE_DIR_DEFAULT = os.path.expanduser("~/.cache/agents-os-core")
CACHE_FILE_NAME = "vault_confidential_cache.json"
CACHE_TTL = 60.0  # seconds

def normalize_path(path_str: str) -> str:
    """Normalizes Windows, WSL, relative, and case variations into a canonical unix-like path."""
    if not path_str:
        return ""
    p = path_str.strip().strip("'\"")
    p = p.replace("\\", "/")
    m_win = re.match(r'^([a-zA-Z]):/(.*)', p)
    if m_win:
        drive = m_win.group(1).lower()
        rest = m_win.group(2)
        p = f"/mnt/{drive}/{rest}"
    p = os.path.normpath(p)
    return p.lower()

def get_cache_paths() -> tuple:
    """Returns (cache_dir, cache_file) ensuring secure directory permissions (0700)."""
    base_cache = os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")
    cache_dir = os.path.join(base_cache, "agents-os-core")
    try:
        os.makedirs(cache_dir, mode=0o700, exist_ok=True)
        # Enforce 0700 in case it existed with loose permissions
        os.chmod(cache_dir, 0o700)
    except Exception:
        pass
    cache_file = os.path.join(cache_dir, CACHE_FILE_NAME)
    return cache_dir, cache_file

def compute_cache_checksum(vault_dir: str, timestamp: float, rels: list, dirs: list, basenames: list) -> str:
    """Computes SHA-256 integrity checksum over stored cache metadata."""
    sorted_rels = sorted(list(rels))
    sorted_dirs = sorted(list(dirs))
    sorted_basenames = sorted(list(basenames))
    raw = f"{vault_dir}:{timestamp:.4f}:{','.join(sorted_rels)}:{','.join(sorted_dirs)}:{','.join(sorted_basenames)}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

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
    2. os.environ['OBSIDIAN_VAULT_PATH']
    3. .ai/agentic.config.json (context.second_brain.local_path / windows_default_path)
    4. VAULT_DEFAULT_PATH (/mnt/c/Users/tkogut/Documents/sejf_tk)
    Zero Full-Disk Probing: if a specified/default path does not exist, raises FileNotFoundError.
    """
    if env_path:
        norm = normalize_path(env_path)
        if os.path.isdir(norm):
            return norm
        raise FileNotFoundError(f"Wskazany katalog vaulta '{env_path}' nie istnieje.")

    env_val = os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_val:
        norm_env = normalize_path(env_val)
        if os.path.isdir(norm_env):
            return norm_env
        raise FileNotFoundError(f"Katalog vaulta ze zmiennej OBSIDIAN_VAULT_PATH ('{env_val}') nie istnieje.")

    cfg = load_agentic_config()
    cfg_path = (cfg.get("context", {}).get("second_brain", {}).get("local_path") or
                cfg.get("context", {}).get("second_brain", {}).get("windows_default_path"))
    if cfg_path:
        norm_cfg = normalize_path(cfg_path)
        if os.path.isdir(norm_cfg):
            return norm_cfg
        raise FileNotFoundError(f"Katalog vaulta z konfiguracji .ai/agentic.config.json ('{cfg_path}') nie istnieje.")

    norm_def = normalize_path(VAULT_DEFAULT_PATH)
    if os.path.isdir(norm_def):
        return norm_def

    raise FileNotFoundError(
        f"Katalog vaulta nie został odnaleziony w konfiguracji (.ai/agentic.config.json), "
        f"zmiennej OBSIDIAN_VAULT_PATH ani pod domyślną ścieżką '{VAULT_DEFAULT_PATH}'. "
        f"Zasada Zero Full-Disk Probing: skanowanie dysku jest zabronione (Fail-Closed)."
    )

def scan_vault_confidential(vault_dir: str) -> tuple:
    """
    Scans the vault directory for confidential entries:
    - Frontmatter 'confidential: true'
    - 'raw_path'
    - 'Oryginał (strefa człowieka): [[...]]'
    Raises exception on I/O or directory error (fail-closed).
    """
    if not os.path.isdir(vault_dir):
        raise FileNotFoundError(f"Katalog vaulta nie istnieje: {vault_dir}")

    confidential_rels = set()
    confidential_dirs = set()
    confidential_basenames = set()

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
        except Exception as e:
            raise IOError(f"Błąd odczytu pliku vaulta '{rel}': {e}")

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

    return confidential_rels, confidential_dirs, confidential_basenames

def save_cache_atomic(cache_file: str, vault_dir: str, timestamp: float, rels: set, dirs: set, basenames: set) -> None:
    """Atomically writes cache file with mode 0600."""
    cache_dir = os.path.dirname(cache_file)
    os.makedirs(cache_dir, mode=0o700, exist_ok=True)
    try:
        os.chmod(cache_dir, 0o700)
    except Exception:
        pass

    rels_list = sorted(list(rels))
    dirs_list = sorted(list(dirs))
    base_list = sorted(list(basenames))
    checksum = compute_cache_checksum(vault_dir, timestamp, rels_list, dirs_list, base_list)

    payload = {
        "version": 1,
        "vault_dir": vault_dir,
        "timestamp": timestamp,
        "confidential_rels": rels_list,
        "confidential_dirs": dirs_list,
        "confidential_basenames": base_list,
        "checksum": checksum
    }

    tmp_file = f"{cache_file}.tmp.{os.getpid()}_{int(time.time()*1000)}"
    # Open with mode 0600
    fd = os.open(tmp_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with open(fd, "w", encoding="utf-8") as fp:
            json.dump(payload, fp)
        os.replace(tmp_file, cache_file)
        os.chmod(cache_file, 0o600)
    except Exception:
        if os.path.exists(tmp_file):
            try:
                os.remove(tmp_file)
            except Exception:
                pass
        raise

def get_confidential_paths_dynamic(vault_dir: str) -> tuple:
    """
    Returns (confidential_rels, confidential_dirs, confidential_basenames).
    Validates cache integrity and TTL (60s).
    If cache is invalid or missing, rebuilds it.
    If rebuilding fails, raises exception (fail-closed).
    """
    _, cache_file = get_cache_paths()
    now = time.time()
    cache_valid = False

    if os.path.isfile(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as fp:
                data = json.load(fp)

            c_vault = data.get("vault_dir")
            c_ts = data.get("timestamp", 0)
            c_rels = data.get("confidential_rels", [])
            c_dirs = data.get("confidential_dirs", [])
            c_base = data.get("confidential_basenames", [])
            c_chk = data.get("checksum", "")

            # Integrity check: verify checksum
            computed_chk = compute_cache_checksum(c_vault, c_ts, c_rels, c_dirs, c_base)
            if computed_chk == c_chk and c_vault == vault_dir and (now - c_ts < CACHE_TTL):
                return set(c_rels), set(c_dirs), set(c_base)
        except Exception:
            # Corrupted, unreadable, or tampered cache -> proceed to rebuild
            pass

    # Rebuild cache
    rels, dirs, basenames = scan_vault_confidential(vault_dir)
    try:
        save_cache_atomic(cache_file, vault_dir, now, rels, dirs, basenames)
    except Exception as e:
        # If cache cannot be written due to permissions, log warning but return valid scan results
        sys.stderr.write(f"[guard_confidential_gemini] Cache write warning: {e}\n")

    return rels, dirs, basenames

def evaluate_hook(payload: dict) -> dict:
    """
    Evaluates a tool call payload.
    Fail-closed on any error or missing vault.
    """
    try:
        # 1. Model Identification & Provider DPA Status
        model_name = payload.get("modelName", "") or ""
        model_name_low = model_name.lower()

        # Claude is allowed through this gate (governed by separate user confirmation)
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

        # 2. Resolve Vault Path (Zero Full-Disk Probing)
        try:
            vault_dir = resolve_vault_path()
        except FileNotFoundError as fnf_err:
            # If the tool call touches vault keywords but vault is not configured, DENY
            return {
                "decision": "deny",
                "reason": f"🛑 [POLITYKA POUFNOŚCI GEMINI — FAIL-CLOSED] Błąd konfiguracji vaulta:\n{fnf_err}"
            }

        file_path = args.get("Path") or args.get("AbsolutePath") or args.get("file_path") or args.get("path") or ""
        target_dir = args.get("Directory") or args.get("dir") or args.get("folder") or ""
        cmd_line = args.get("CommandLine") or args.get("command") or ""

        # --- FAST-BYPASS (<0.1ms) ---
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

        # 3. Dynamic Confidential Paths with Integrity Cache
        try:
            conf_rels, conf_dirs, conf_basenames = get_confidential_paths_dynamic(vault_dir)
        except Exception as scan_err:
            return {
                "decision": "deny",
                "reason": (
                    "🛑 [POLITYKA POUFNOŚCI GEMINI — FAIL-CLOSED] Odmowa dostępu:\n"
                    f"Nie można zweryfikować statusu poufności dokumentów w vaulcie: {scan_err}\n"
                    "Z powodu braku DPA dostęp zablokowano. Skieruj zadanie do Claude Code."
                )
            }

        # 4. Direct file access check
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

        # 5. Directory search tool check
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

        # 6. Run command (Bash) check
        if tool_name in ["run_command", "bash", "execute_command"] and cmd_norm:
            # 6a. Direct reference to confidential file
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

            # 6b. Recursive search over confidential dirs
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

    except Exception as unhandled_err:
        return {
            "decision": "deny",
            "reason": f"🛑 [POLITYKA POUFNOŚCI GEMINI — FAIL-CLOSED] Błąd wewnętrzny strażnika: {unhandled_err}"
        }

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
            "reason": f"Błąd krytyczny hooka ochrony poufności (Fail-Closed): {e}"
        }, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        sys.exit(2)

if __name__ == "__main__":
    main()
