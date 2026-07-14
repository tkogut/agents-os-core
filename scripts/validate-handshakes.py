#!/usr/bin/env python3
"""
validate-handshakes.py — Walidator protokołu uścisku dłoni (Handshake) Swarm Triad.
Weryfikuje, czy pliki handshake istnieją i mają poprawną strukturę.

Użycie:
    python3 scripts/validate-handshakes.py [--conversation-id <uuid>] [--require-roles builder,auditor]
    
    Bez argumentów: sprawdza ALL pliki w .agents/swarm/
    Z --conversation-id: sprawdza tylko pliki dla danej sesji
    Z --require-roles: weryfikuje, że wszystkie wymagane role złożyły handshake
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone


SWARM_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".agents", "swarm")
REQUIRED_FIELDS = ["conversation_id", "role", "status", "files_modified", "math_consistency_check", "timestamp"]


def load_handshakes(conversation_id=None):
    """Load all handshake files, optionally filtered by conversation_id."""
    if not os.path.isdir(SWARM_DIR):
        return []

    results = []
    for fname in os.listdir(SWARM_DIR):
        if not fname.endswith("_handshake.json"):
            continue
        if conversation_id and not fname.startswith(conversation_id):
            continue
        fpath = os.path.join(SWARM_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            results.append({"file": fname, "data": data, "valid": True, "errors": []})
        except (json.JSONDecodeError, IOError) as e:
            results.append({"file": fname, "data": None, "valid": False, "errors": [str(e)]})
    return results


def validate_handshake(entry):
    """Validate a single handshake entry for required fields."""
    if not entry["valid"]:
        return False
    data = entry["data"]
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing field: '{field}'")

    if "status" in data and data["status"] not in ("SUCCESS", "FAILURE", "PARTIAL"):
        errors.append(f"Invalid status value: '{data['status']}'")

    if "math_consistency_check" in data and data["math_consistency_check"] not in ("PASSED", "FAILED", "SKIPPED", "N/A"):
        errors.append(f"Invalid math_consistency_check: '{data['math_consistency_check']}'")

    entry["errors"] = errors
    entry["valid"] = len(errors) == 0
    return entry["valid"]


def main():
    p = argparse.ArgumentParser(description="Validate Swarm Triad handshake files.")
    p.add_argument("--conversation-id", default=None,
                   help="Filtruj po conversation_id (UUID sesji)")
    p.add_argument("--require-roles", default=None,
                   help="Przecinkami rozdzielone role, które MUSZĄ mieć handshake (np. builder,auditor)")
    args = p.parse_args()

    print(f"📂 Swarm dir: {SWARM_DIR}")
    entries = load_handshakes(args.conversation_id)

    if not entries:
        filter_info = f" dla conversation_id={args.conversation_id}" if args.conversation_id else ""
        print(f"⚠️  BRAK plików handshake{filter_info} w {SWARM_DIR}")
        sys.exit(1)

    print(f"🔍 Znaleziono {len(entries)} plik(ów) handshake:\n")

    all_valid = True
    found_roles = set()

    for entry in entries:
        is_valid = validate_handshake(entry)
        icon = "✅" if is_valid else "❌"
        print(f"  {icon} {entry['file']}")
        if entry["data"]:
            d = entry["data"]
            role_raw = d.get("role", "unknown").lower()
            found_roles.add(role_raw.replace(" agent", "").strip())
            print(f"     • role      : {d.get('role', '—')}")
            print(f"     • status    : {d.get('status', '—')}")
            print(f"     • math_check: {d.get('math_consistency_check', '—')}")
            print(f"     • timestamp : {d.get('timestamp', '—')}")
            files = d.get("files_modified", [])
            print(f"     • files     : {len(files)} plik(ów)")
            if d.get("notes"):
                print(f"     • notes     : {d['notes']}")
        if entry["errors"]:
            for err in entry["errors"]:
                print(f"     ⚠ {err}")
            all_valid = False
        print()

    # Role requirement check
    if args.require_roles:
        required = set(r.strip().lower() for r in args.require_roles.split(","))
        missing = required - found_roles
        if missing:
            print(f"❌ Brakujące handshake dla ról: {', '.join(missing)}")
            all_valid = False
        else:
            print(f"✅ Wszystkie wymagane role złożyły handshake: {', '.join(required)}")

    if all_valid:
        print("\n✅ WALIDACJA ZAKOŃCZONA: Wszystkie pliki handshake są poprawne.")
        sys.exit(0)
    else:
        print("\n❌ WALIDACJA NIEUDANA: Wykryto błędy w plikach handshake.")
        sys.exit(1)


if __name__ == "__main__":
    main()
