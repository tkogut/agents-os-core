#!/usr/bin/env python3
"""
publish_knowledge_to_vault.py — Secure Publication of Knowledge Notes to Obsidian Vault
Part of AGENTS-OS Swarm Knowledge Integration (v7.0 ISO 27001 Rigor).

Specifications:
- Copies markdown notes from .agents/specs/knowledge to <vault>/raw/notes.
- Default mode: DRY-RUN. File writes require '--apply'.
- Secret & PII Scanning (ISO 27001):
  - API keys, tokens, passwords, JWT, private keys, connection strings, emails outside miw.group, PESEL, IBAN.
  - Blocked files report ONLY pattern name, NEVER secret/PII values.
- Overwrite Protection:
  - Never overwrites: identical sha256 = SKIPPED, different content = CONFLICT.
- Path Hygiene:
  - Skips symlinks, non-.md files, and path traversals.
- Frontmatter Enrichment:
  - Adds source: agents-os-core, source_path, sha256, published: YYYY-MM-DD, status: new.
- Vault Git Mandate:
  - ZERO git commit or push operations in vault.
- Exit Codes:
  - 0: All files published or skipped without issues.
  - 2: One or more files blocked by security scanner or encountered a conflict.
"""

import sys
import os
import argparse
import re
import hashlib
import json
from datetime import date

VAULT_DEFAULT_PATH = "/mnt/c/Users/tkogut/Documents/sejf_tk"

# ==============================================================================
# 1. PII and Secret Scanners (ISO 27001)
# ==============================================================================

def validate_pesel(pesel: str) -> bool:
    """Validates 11-digit PESEL using checksum algorithm."""
    if len(pesel) != 11 or not pesel.isdigit():
        return False
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    total = sum(int(pesel[i]) * weights[i] for i in range(10))
    checksum = (10 - (total % 10)) % 10
    if checksum != int(pesel[10]):
        return False
    # Validate month range (01-12, 21-32, 41-52, 61-72, 81-92)
    month = int(pesel[2:4])
    day = int(pesel[4:6])
    if day < 1 or day > 31:
        return False
    base_month = month % 20
    if base_month < 1 or base_month > 12:
        return False
    return True

def validate_iban(iban: str) -> bool:
    """Validates Polish and international IBANs using standard mod-97 check."""
    cleaned = iban.replace(" ", "").upper()
    if len(cleaned) < 15 or len(cleaned) > 34:
        return False
    if not re.match(r'^[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}$', cleaned):
        return False
    # Move first 4 chars to end
    rearranged = cleaned[4:] + cleaned[:4]
    # Replace letters with digits: A=10 ... Z=35
    num_str = ""
    for ch in rearranged:
        if ch.isdigit():
            num_str += ch
        elif ch.isalpha():
            num_str += str(ord(ch) - ord('A') + 10)
        else:
            return False
    try:
        return int(num_str) % 97 == 1
    except Exception:
        return False

SECRET_PATTERNS = [
    ("API_KEY_SK", re.compile(r'\bsk-[A-Za-z0-9_-]{20,}\b')),
    ("AWS_ACCESS_KEY", re.compile(r'\bAKIA[0-9A-Z]{16}\b')),
    ("GITHUB_TOKEN", re.compile(r'\b(ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{50,})\b')),
    ("JWT_TOKEN", re.compile(r'\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b')),
    ("PRIVATE_KEY", re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),
    ("CONNECTION_STRING_PASSWORD", re.compile(r'[a-zA-Z0-9+.-]+://[^:/ \t\n\r]+:[^@/ \t\n\r]+@')),
    ("SECRET_CREDENTIAL", re.compile(r'(?i)\b(password|has[lł]o|token|secret|api[_-]?key)\s*[:=]\s*["\']?([^\s"\'\n\r]{6,})["\']?')),
    ("PII_EXTERNAL_EMAIL", re.compile(r'\b[A-Za-z0-9._%+-]+@(?!(?:[a-zA-Z0-9-]+\.)*miw\.group\b|(?:[a-zA-Z0-9-]+\.)*miw-group\.com\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', re.IGNORECASE)),
]

def scan_content_for_secrets(content: str) -> list:
    """
    Scans text for secrets and PII.
    Returns list of matched pattern names (NEVER secret values).
    """
    findings = set()
    for name, pattern in SECRET_PATTERNS:
        if pattern.search(content):
            findings.add(name)

    # Check for PESEL candidates
    for m in re.finditer(r'\b[0-9]{11}\b', content):
        if validate_pesel(m.group(0)):
            findings.add("PII_PESEL")

    # Check for IBAN candidates (PL followed by 26 digits or international)
    for m in re.finditer(r'\b[A-Z]{2}[0-9]{2}[0-9A-Za-z]{11,30}\b', content):
        if validate_iban(m.group(0)):
            findings.add("PII_IBAN")

    return sorted(list(findings))

# ==============================================================================
# 2. Frontmatter Parsing and Enrichment
# ==============================================================================

def split_frontmatter(content: str) -> tuple:
    """Splits markdown into (raw_frontmatter_str or None, body_content)."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return None, content

def enrich_frontmatter(content: str, rel_path: str, sha256_hash: str, pub_date: str) -> str:
    """
    Enriches markdown content with standard frontmatter metadata.
    Preserves all existing keys and appends/updates metadata.
    """
    fm_str, body = split_frontmatter(content)
    lines = []
    if fm_str:
        # Keep existing lines, skipping keys we intend to override
        skip_keys = {"source", "source_path", "sha256", "published", "status"}
        for line in fm_str.strip().splitlines():
            k_match = re.match(r'^([a-zA-Z0-9_-]+):', line)
            if k_match and k_match.group(1).lower() in skip_keys:
                continue
            lines.append(line)

    lines.append(f"source: agents-os-core")
    lines.append(f"source_path: {rel_path}")
    lines.append(f"sha256: {sha256_hash}")
    lines.append(f"published: {pub_date}")
    lines.append(f"status: new")

    new_fm = "---\n" + "\n".join(lines) + "\n---\n"
    # Ensure clean separation with body
    clean_body = body.lstrip("\r\n")
    return new_fm + clean_body

def compute_body_hash(content: str) -> str:
    """Computes SHA-256 of the markdown content body (ignoring publish metadata)."""
    _, body = split_frontmatter(content)
    clean = re.sub(r'\s+', ' ', body.strip())
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()

# ==============================================================================
# 3. Publisher Engine & INGEST Scaffolder
# ==============================================================================

def to_kebab_slug(name: str) -> str:
    """Converts a filename or title into a kebab-case ascii slug without polish chars."""
    if name.lower().endswith(".md"):
        name = name[:-3]
    pol_map = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'a', 'Ć': 'c', 'Ę': 'e', 'Ł': 'l', 'Ń': 'n', 'Ó': 'o', 'Ś': 's', 'Ź': 'z', 'Ż': 'z'
    }
    for k, v in pol_map.items():
        name = name.replace(k, v)
    name = re.sub(r'[^a-zA-Z0-9]+', '-', name)
    name = name.strip('-').lower()
    return name or "notatka"

def detect_vault_root(dest_dir: str) -> str:
    """Detects the vault root from dest_dir (usually <vault>/raw/notes)."""
    norm = os.path.normpath(dest_dir)
    parent = os.path.dirname(norm)
    grandparent = os.path.dirname(parent)
    if os.path.exists(os.path.join(grandparent, "index.md")):
        return grandparent
    if os.path.exists(os.path.join(parent, "index.md")):
        return parent
    if os.path.basename(parent) == "raw":
        return grandparent
    env_vault = os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_vault and os.path.isdir(env_vault):
        return env_vault
    if os.path.isdir(VAULT_DEFAULT_PATH):
        return VAULT_DEFAULT_PATH
    return grandparent

def mark_raw_note_processed(raw_note_path: str, today_str: str):
    """Marks a raw note in raw/notes as processed in YAML frontmatter."""
    try:
        with open(raw_note_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "status: processed" in content:
            return
        if "status: new" in content:
            content = re.sub(r'status:\s*new', f'status: processed\nprocessed: {today_str}', content, count=1)
        else:
            fm, body = split_frontmatter(content)
            if fm:
                lines = fm.splitlines()
                lines.insert(-1, f"status: processed\nprocessed: {today_str}")
                content = "\n".join(lines) + "\n" + body
            else:
                content = f"---\nstatus: processed\nprocessed: {today_str}\n---\n" + content
        with open(raw_note_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception:
        pass

def scaffold_ingest_source(vault_root: str, target_file_name: str, note_content: str, today_str: str, apply: bool = False) -> dict:
    """
    Scaffolds wiki/sources/src-<slug>.md, updates index.md and log.md.
    Returns status dict.
    """
    slug = to_kebab_slug(target_file_name)
    if not slug.startswith("src-"):
        src_filename = f"src-{slug}.md"
    else:
        src_filename = f"{slug}.md"

    # Extract title
    m_h1 = re.search(r'^#\s+(.+)$', note_content, re.MULTILINE)
    if m_h1:
        title = m_h1.group(1).strip()
    else:
        m_title = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', note_content, re.MULTILINE)
        title = m_title.group(1).strip() if m_title else os.path.splitext(target_file_name)[0]
    clean_title = re.sub(r'[*_`]', '', title).strip()

    # Extract tags
    m_tags = re.search(r'^tags:\s*\[(.*?)\]', note_content, re.MULTILINE)
    tags = []
    if m_tags:
        raw_tags = m_tags.group(1).split(",")
        tags = [t.strip().strip("'\"# ") for t in raw_tags if t.strip().strip("'\"# ")]
    if not tags:
        tags = ["źródło", "agents-os"]

    # Extract lead summary
    body = re.sub(r'^---\s*[\s\S]*?---\s*', '', note_content).strip()
    lead_lines = []
    capturing = False
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            if capturing:
                break
            continue
        if stripped.startswith("#") or stripped.startswith(">") or stripped.startswith("---"):
            continue
        capturing = True
        lead_lines.append(stripped)
    lead_summary = " ".join(lead_lines) if lead_lines else f"Notatka wiedzy inżynieryjnej przetransferowana z projektu agents-os: {clean_title}."

    # Extract H2 sections
    h2_matches = re.findall(r'^##\s+(.+)$', body, re.MULTILINE)
    if h2_matches:
        details_bullets = "\n".join(f"- **{re.sub(r'[*_`]', '', h).strip()}**" for h in h2_matches[:10])
    else:
        details_bullets = f"- Szczegółowa treść w załączonym pliku źródłowym `raw/notes/{target_file_name}`."

    src_page_content = f"""---
title: "Źródło: {clean_title}"
type: source
domain: programowanie
tags: [{", ".join(tags)}]
sources: ["raw/notes/{target_file_name}"]
created: {today_str}
updated: {today_str}
status: draft
created_by: os-publish-knowledge
raw_path: raw/notes/{target_file_name}
---

## Podsumowanie

{lead_summary}

## Szczegóły

{details_bullets}

## Sprzeczności / otwarte pytania

- Wstępny scaffolding wygenerowany automatycznie przez narzędzie `os-publish-knowledge`. Wymaga dekompozycji pojęciowej i semantycznej przez agenta LLM lub człowieka.

## Powiązania

- [[overview]]
- [[index]]

## Źródła

- Oryginał: `raw/notes/{target_file_name}`
"""

    if not apply:
        return {
            "raw_note": target_file_name,
            "source_page": src_filename,
            "slug": slug,
            "title": clean_title,
            "status": "DRY-RUN (ready to scaffold)"
        }

    sources_dir = os.path.join(vault_root, "wiki", "sources")
    os.makedirs(sources_dir, exist_ok=True)
    src_page_path = os.path.join(sources_dir, src_filename)

    status = "SCAFFOLDED"
    if os.path.exists(src_page_path):
        status = "EXISTS_KEPT"
    else:
        try:
            with open(src_page_path, "w", encoding="utf-8") as f:
                f.write(src_page_content)
        except Exception as e:
            return {
                "raw_note": target_file_name,
                "source_page": src_filename,
                "slug": slug,
                "title": clean_title,
                "status": f"ERROR_WRITE_SOURCE ({e})"
            }

    # Update index.md
    index_path = os.path.join(vault_root, "index.md")
    if os.path.exists(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                idx_content = f.read()
            wiki_link = f"[[{os.path.splitext(src_filename)[0]}]]"
            if wiki_link not in idx_content:
                entry_line = f"- {wiki_link} – {clean_title}\n"
                if "## Źródła (sources)\n" in idx_content:
                    idx_content = idx_content.replace("## Źródła (sources)\n", f"## Źródła (sources)\n{entry_line}")
                elif "## Źródła\n" in idx_content:
                    idx_content = idx_content.replace("## Źródła\n", f"## Źródła\n{entry_line}")
                else:
                    idx_content += f"\n## Źródła (sources)\n{entry_line}"
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(idx_content)
        except Exception:
            pass

    # Update log.md
    log_path = os.path.join(vault_root, "log.md")
    if os.path.exists(log_path):
        try:
            log_entry = f"\n\n## [{today_str}] ingest | {clean_title}\nAutomatyczny scaffolding INGEST dla notatki `raw/notes/{target_file_name}` (os-publish-knowledge).\nZmienione pliki: wiki/sources/{src_filename}, index.md, raw/notes/{target_file_name}, log.md."
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception:
            pass

    return {
        "raw_note": target_file_name,
        "source_page": src_filename,
        "slug": slug,
        "title": clean_title,
        "status": status
    }

def resolve_default_dest() -> str:
    env_vault = os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_vault:
        return os.path.join(env_vault, "raw", "notes")
    return os.path.join(VAULT_DEFAULT_PATH, "raw", "notes")

def publish_notes(source_dir: str, dest_dir: str, apply: bool = False, ingest: bool = False) -> dict:
    """
    Main publish workflow with optional INGEST scaffolding.
    Returns result summary dict.
    """
    summary = {
        "source_dir": source_dir,
        "dest_dir": dest_dir,
        "mode": "APPLY" if apply else "DRY-RUN",
        "published": [],
        "ingested": [],
        "skipped": [],
        "blocked": [],
        "conflicts": [],
        "errors": []
    }

    if not os.path.isdir(source_dir):
        summary["errors"].append(f"Katalog źródłowy nie istnieje: {source_dir}")
        return summary

    if apply and not os.path.isdir(dest_dir):
        try:
            os.makedirs(dest_dir, exist_ok=True)
        except Exception as e:
            summary["errors"].append(f"Nie można utworzyć katalogu docelowego '{dest_dir}': {e}")
            return summary

    today_str = date.today().isoformat()
    vault_root = detect_vault_root(dest_dir)

    # Walk source directory
    for root, dirs, files in os.walk(source_dir):
        for f in sorted(files):
            full_src = os.path.join(root, f)
            rel_src = os.path.relpath(full_src, source_dir).replace("\\", "/")

            # Rule: Skip symlinks
            if os.path.islink(full_src):
                summary["skipped"].append({"file": rel_src, "reason": "SYMLINK_IGNORED"})
                continue

            # Rule: Only .md files
            if not f.lower().endswith(".md"):
                summary["skipped"].append({"file": rel_src, "reason": "NOT_MARKDOWN"})
                continue

            # Rule: Prevent path traversal
            norm_rel = os.path.normpath(rel_src)
            if norm_rel.startswith("..") or os.path.isabs(norm_rel):
                summary["skipped"].append({"file": rel_src, "reason": "PATH_TRAVERSAL_IGNORED"})
                continue

            # Read source content
            try:
                with open(full_src, "r", encoding="utf-8", errors="ignore") as fp:
                    src_content = fp.read()
            except Exception as e:
                summary["errors"].append(f"Błąd odczytu '{rel_src}': {e}")
                continue

            # Security and PII scan
            findings = scan_content_for_secrets(src_content)
            if findings:
                summary["blocked"].append({
                    "file": rel_src,
                    "patterns": findings
                })
                continue

            # Check target destination
            target_file_name = os.path.basename(rel_src)
            target_path = os.path.join(dest_dir, target_file_name)

            src_body_hash = compute_body_hash(src_content)
            src_sha256 = hashlib.sha256(src_content.encode("utf-8")).hexdigest()

            if os.path.exists(target_path):
                try:
                    with open(target_path, "r", encoding="utf-8", errors="ignore") as tfp:
                        target_content = tfp.read()
                    target_body_hash = compute_body_hash(target_content)

                    if src_body_hash == target_body_hash:
                        summary["skipped"].append({
                            "file": rel_src,
                            "target": target_file_name,
                            "reason": "IDENTICAL_CONTENT"
                        })
                        if ingest:
                            if "status: processed" not in target_content:
                                ing_res = scaffold_ingest_source(vault_root, target_file_name, target_content, today_str, apply=apply)
                                if apply and ing_res["status"] in ("SCAFFOLDED", "EXISTS_KEPT"):
                                    mark_raw_note_processed(target_path, today_str)
                                summary["ingested"].append(ing_res)
                        continue
                    else:
                        summary["conflicts"].append({
                            "file": rel_src,
                            "target": target_file_name,
                            "reason": "TARGET_EXISTS_WITH_DIFFERENT_CONTENT"
                        })
                        continue
                except Exception as e:
                    summary["conflicts"].append({
                        "file": rel_src,
                        "target": target_file_name,
                        "reason": f"TARGET_READ_ERROR: {e}"
                    })
                    continue

            # If no conflict, prepare enriched output
            enriched_content = enrich_frontmatter(src_content, rel_src, src_sha256, today_str)

            if apply:
                try:
                    with open(target_path, "w", encoding="utf-8") as out_fp:
                        out_fp.write(enriched_content)
                    summary["published"].append({
                        "file": rel_src,
                        "target": target_file_name,
                        "sha256": src_sha256
                    })
                    if ingest:
                        ing_res = scaffold_ingest_source(vault_root, target_file_name, enriched_content, today_str, apply=True)
                        if ing_res["status"] in ("SCAFFOLDED", "EXISTS_KEPT"):
                            mark_raw_note_processed(target_path, today_str)
                        summary["ingested"].append(ing_res)
                except Exception as e:
                    summary["errors"].append(f"Błąd zapisu '{target_path}': {e}")
            else:
                summary["published"].append({
                    "file": rel_src,
                    "target": target_file_name,
                    "sha256": src_sha256,
                    "note": "DRY-RUN (ready to write)"
                })
                if ingest:
                    ing_res = scaffold_ingest_source(vault_root, target_file_name, enriched_content, today_str, apply=False)
                    summary["ingested"].append(ing_res)

    return summary

def main():
    parser = argparse.ArgumentParser(description="Publikacja notatek wiedzy do Obsidian Vault (raw/notes).")
    parser.add_argument("--source", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".agents", "specs", "knowledge"),
                        help="Katalog źródłowy z notatkami (.agents/specs/knowledge)")
    parser.add_argument("--dest", default=resolve_default_dest(),
                        help="Katalog docelowy w vaulcie (<vault>/raw/notes)")
    parser.add_argument("--apply", action="store_true", help="Wykonaj faktyczny zapis (domyślnie dry-run)")
    parser.add_argument("--ingest", action="store_true",
                        help="Wykonaj automatyczny scaffolding INGEST (wiki/sources/src-*, index.md, log.md)")
    parser.add_argument("--json", action="store_true", help="Wyświetl raport w formacie JSON")

    args = parser.parse_args()

    source_dir = os.path.abspath(args.source)
    dest_dir = os.path.abspath(args.dest)

    res = publish_notes(source_dir, dest_dir, apply=args.apply, ingest=args.ingest)

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"==================================================")
        print(f"📦 RAPORT PUBLIKACJI WIEDZY DO VAULTA ({res['mode']})")
        print(f"Źródło: {res['source_dir']}")
        print(f"Cel   : {res['dest_dir']}")
        print(f"==================================================")
        print(f"✅ Do publikacji / opublikowano : {len(res['published'])}")
        for item in res["published"]:
            print(f"   • {item['file']} -> {item['target']}")
        if res.get("ingested"):
            print(f"📄 Scaffolding INGEST (wiki/)  : {len(res['ingested'])}")
            for item in res["ingested"]:
                print(f"   • {item['raw_note']} -> wiki/sources/{item['source_page']} [{item['status']}]")
        print(f"⏭️  Pominięto                    : {len(res['skipped'])}")
        for item in res["skipped"]:
            print(f"   • {item['file']} ({item['reason']})")
        print(f"🛑 Zablokowano (bezpieczeństwo) : {len(res['blocked'])}")
        for item in res["blocked"]:
            print(f"   • {item['file']} [WZORCE: {', '.join(item['patterns'])}]")
        print(f"⚠️  Konflikty                    : {len(res['conflicts'])}")
        for item in res["conflicts"]:
            print(f"   • {item['file']} -> {item['target']} ({item['reason']})")
        if res["errors"]:
            print(f"❌ Błędy I/O                    : {len(res['errors'])}")
            for err in res["errors"]:
                print(f"   • {err}")
        print(f"==================================================")

    # Return exit code 2 if any blocked or conflicts
    if res["blocked"] or res["conflicts"] or res["errors"]:
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
