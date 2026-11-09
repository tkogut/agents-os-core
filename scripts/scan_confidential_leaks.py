#!/usr/bin/env python3
"""
scan_confidential_leaks.py — scans committed harness files for leaks of confidential
vault content (canary phrases) and secret patterns (vault AGENTS.md pkt 10).

Targets (relative to --root, default: repo root):
  .agents/MEMORY.md, .agents/task.md, .agents/swarm/*_handshake.json
  plus any --file PATH / --stdin (e.g. a PR description piped from `gh pr view`).

Output: only "<file>: <RULE>" lines. NEVER prints the matched value or its context.
Exit codes: 0 clean, 1 findings, 2 usage/read error (fail-closed: unreadable target = error).
"""
import argparse
import glob
import os
import re
import sys

RULES = [
    # canary phrases planted in confidential vault pages (step 5 of the second-brain plan)
    ("CANARY", re.compile(r"CANARY-SB-[A-Za-z0-9]{6,}")),
    ("API_KEY_SK", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("AWS_ACCESS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GITHUB_TOKEN", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}")),
    ("PRIVATE_KEY", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
    ("CONNECTION_STRING", re.compile(r"://[^\s/:@]+:[^\s/@]{3,}@[^\s/]+")),
    ("CREDENTIAL_PAIR", re.compile(
        r"(?i)\b(password|passwd|secret|token|api[_-]?key)\b\s*[:=]\s*[\"']?[A-Za-z0-9/+_.\-]{12,}")),
]

DEFAULT_TARGETS = [".agents/MEMORY.md", ".agents/task.md"]
DEFAULT_GLOBS = [".agents/swarm/*_handshake.json"]


def scan_text(text):
    """Return sorted list of rule names matched in text (values are never returned)."""
    return sorted({name for name, rx in RULES if rx.search(text)})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--file", action="append", default=[], help="extra file to scan")
    ap.add_argument("--stdin", action="store_true", help="also scan stdin (label: <stdin>)")
    args = ap.parse_args(argv)

    targets = [os.path.join(args.root, t) for t in DEFAULT_TARGETS]
    for g in DEFAULT_GLOBS:
        targets += sorted(glob.glob(os.path.join(args.root, g)))
    targets += args.file

    findings, errors = [], []
    for path in targets:
        if not os.path.exists(path):
            continue  # optional target absent in this repo
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                rules = scan_text(fh.read())
        except OSError as e:
            errors.append(f"{os.path.relpath(path, args.root)}: READ_ERROR ({e.__class__.__name__})")
            continue
        for r in rules:
            findings.append(f"{os.path.relpath(path, args.root)}: {r}")

    if args.stdin:
        for r in scan_text(sys.stdin.read()):
            findings.append(f"<stdin>: {r}")

    for line in findings + errors:
        print(line)
    if errors:
        return 2
    if findings:
        print(f"WYNIK: NIE ZDANY ({len(findings)} trafień; wartości nie są wypisywane)")
        return 1
    print("WYNIK: ZDANY (brak fraz kontrolnych i wzorców sekretów)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
