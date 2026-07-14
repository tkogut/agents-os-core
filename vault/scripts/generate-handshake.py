#!/usr/bin/env python3
"""
generate-handshake.py — Protokół uścisku dłoni (Handshake) dla Swarm Triad.
Generuje plik potwierdzający zakończenie pracy przez Builder lub Auditor.

Użycie:
    python3 scripts/generate-handshake.py \
        --role builder \
        --conversation-id <uuid> \
        --status SUCCESS \
        --files "src/main.py,src/static/app.js" \
        --math-check PASSED \
        [--notes "Opcjonalne notatki"]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone


SWARM_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".agents", "swarm")
ALLOWED_ROLES = ["builder", "auditor", "coordinator"]
ALLOWED_STATUSES = ["SUCCESS", "FAILURE", "PARTIAL"]
ALLOWED_CHECKS = ["PASSED", "FAILED", "SKIPPED", "N/A"]


def parse_args():
    p = argparse.ArgumentParser(description="Generate Swarm Triad handshake JSON file.")
    p.add_argument("--role", required=True, choices=ALLOWED_ROLES,
                   help="Rola agenta (builder/auditor/coordinator)")
    p.add_argument("--conversation-id", required=True,
                   help="UUID sesji konwersacji (conversation ID)")
    p.add_argument("--status", required=True, choices=ALLOWED_STATUSES,
                   help="Status zakończenia zadania")
    p.add_argument("--files", default="",
                   help="Przecinkami rozdzielona lista zmodyfikowanych plików")
    p.add_argument("--math-check", default="PASSED", choices=ALLOWED_CHECKS,
                   help="Wynik Math-Consistency check (Auditor)")
    p.add_argument("--notes", default="",
                   help="Opcjonalne notatki / opis")
    return p.parse_args()


def main():
    args = parse_args()

    os.makedirs(SWARM_DIR, exist_ok=True)

    files_modified = [f.strip() for f in args.files.split(",") if f.strip()]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    payload = {
        "conversation_id": args.conversation_id,
        "role": args.role.capitalize() + " Agent",
        "status": args.status,
        "files_modified": files_modified,
        "math_consistency_check": args.math_check,
        "timestamp": timestamp,
        "notes": args.notes
    }

    filename = f"{args.conversation_id}_{args.role}_handshake.json"
    filepath = os.path.join(SWARM_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"✅ Handshake saved → {filepath}")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
