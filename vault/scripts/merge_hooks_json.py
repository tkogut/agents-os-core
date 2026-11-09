#!/usr/bin/env python3
"""
merge_hooks_json.py — scala zarządzane wpisy hooków AGENTS-OS do istniejącego hooks.json
BEZ nadpisywania pliku (używane przez os-upgrade-project).

Użycie:
    merge_hooks_json.py TARGET (--template-stdin | --template FILE) [--refresh]

Zasady:
  * brak pliku / pusty plik  -> zapis szablonu,
  * klucz z szablonu, którego nie ma w pliku -> dodany,
  * klucz własny projektu (spoza szablonu)    -> zawsze zachowany,
  * klucz z szablonu, który już jest i RÓŻNI SIĘ od szablonu -> zachowany (ostrzeżenie);
    tylko z --refresh podmieniany na wersję z szablonu (po kopii zapasowej *.bak),
  * nieprawidłowy JSON / nie-obiekt -> plik NIETKNIĘTY (ostrzeżenie), kod wyjścia 0,
  * nic do zmiany -> plik nie jest zapisywany (idempotencja).
Zapis atomowy (plik tymczasowy + os.replace).
"""
import argparse
import json
import os
import shutil
import sys
import time


def merge(existing, template, refresh=False):
    """Return (merged, added, kept_differing, refreshed). Pure function."""
    merged = dict(existing)
    added, kept, refreshed = [], [], []
    for key, value in template.items():
        if key not in merged:
            merged[key] = value
            added.append(key)
        elif merged[key] != value:
            if refresh:
                merged[key] = value
                refreshed.append(key)
            else:
                kept.append(key)
    return merged, added, kept, refreshed


def detect_indent(raw):
    return 4 if raw.startswith('{\n    "') else 2


def atomic_write(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = f"{path}.tmp-{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


def process(path, template, refresh=False, out=print):
    raw = None
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
    if raw is None or not raw.strip():
        atomic_write(path, json.dumps(template, ensure_ascii=False, indent=2) + "\n")
        out(f"   ✓ {path}: utworzono z szablonu")
        return "created"
    try:
        existing = json.loads(raw)
    except json.JSONDecodeError as e:
        out(f"   ⚠ {path}: nieprawidłowy JSON ({e.msg}), plik pozostawiony bez zmian")
        return "invalid"
    if not isinstance(existing, dict):
        out(f"   ⚠ {path}: oczekiwano obiektu JSON, plik pozostawiony bez zmian")
        return "invalid"
    merged, added, kept, refreshed = merge(existing, template, refresh)
    for k in kept:
        out(f"   ⚠ {path}: wpis '{k}' różni się od szablonu, zachowano wersję projektu (--refresh-hooks podmieni)")
    if not added and not refreshed:
        out(f"   ✓ {path}: bez zmian")
        return "unchanged"
    if refreshed:
        bak = path + ".bak"
        if os.path.exists(bak):
            bak = f"{path}.bak-{time.strftime('%Y%m%d%H%M%S')}"
        shutil.copyfile(path, bak)
        out(f"   ℹ {path}: kopia zapasowa -> {os.path.basename(bak)}")
    atomic_write(path, json.dumps(merged, ensure_ascii=False, indent=detect_indent(raw)) + "\n")
    parts = []
    if added:
        parts.append("dodano: " + ", ".join(added))
    if refreshed:
        parts.append("odświeżono: " + ", ".join(refreshed))
    out(f"   ✓ {path}: " + "; ".join(parts))
    return "merged"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("target")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--template-stdin", action="store_true")
    g.add_argument("--template")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args(argv)
    try:
        raw = sys.stdin.read() if args.template_stdin else open(args.template, encoding="utf-8").read()
        template = json.loads(raw)
        assert isinstance(template, dict)
    except Exception as e:
        print(f"   ✗ nieprawidłowy szablon hooków: {e.__class__.__name__}", file=sys.stderr)
        return 2
    process(args.target, template, args.refresh)
    return 0


if __name__ == "__main__":
    sys.exit(main())
