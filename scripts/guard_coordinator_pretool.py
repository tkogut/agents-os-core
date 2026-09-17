#!/usr/bin/env python3
"""
guard_coordinator_pretool.py — Antigravity / Gemini PreToolUse Hook (R-ROLE-01 / Worktree Enforce)
Part of AGENTS-OS v6.5 Swarm Governance.

Ensures that the Coordinator (main thread) cannot directly modify production
source code in the root workspace. Modifying production code requires:
  1. An isolated Git Worktree (tmp/worktrees/feature/<name>).
  2. Delegation to a Builder subagent (invoke_subagent).

This hook receives a JSON payload on stdin and prints a JSON decision on stdout:
  {"decision": "allow"} OR
  {"decision": "deny", "reason": "..."}
"""

import json
import os
import sys

ALLOWED_PATH_PATTERNS = [
    "/tmp/worktrees/",
    "/.worktrees/",
    "/brain/",
    "/scratch/",
    ".gemini/antigravity",
    ".gemini/antigravity-cli",
]

ALLOWED_DIRS = {
    ".agents",
    "plans",
    "docs",
    "vault",
    ".claude",
    ".ai",
    ".git",
}

ALLOWED_EXTENSIONS = {
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".txt",
    ".csv",
    ".lock",
}

ALLOWED_BASENAMES = {
    ".gitattributes",
    ".gitignore",
    ".dockerignore",
    "LICENSE",
    "VERSION",
}

CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte",
    ".html", ".css", ".scss", ".sass", ".less",
    ".go", ".rs", ".c", ".cpp", ".cc", ".h", ".hpp",
    ".java", ".kt", ".rb", ".php", ".sh", ".bash", ".zsh",
    ".sql", ".graphql", ".proto"
}

PROTECTED_DIRS = {
    "src", "ui_dashboard", "api", "lib", "app",
    "backend", "frontend", "components", "pkg", "cmd"
}


def evaluate_tool_call(payload: dict) -> dict:
    tool_call = payload.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})
    target_file = args.get("TargetFile", "")

    if not target_file:
        return {"decision": "allow"}

    norm_path = os.path.normpath(target_file)

    # 1. Check Artifact Directory if specified in payload
    artifact_dir = payload.get("artifactDirectoryPath", "")
    if artifact_dir and norm_path.startswith(os.path.normpath(artifact_dir)):
        return {"decision": "allow"}

    # 2. Check Allowed Substrings (Worktrees, Brain, Scratch)
    for pattern in ALLOWED_PATH_PATTERNS:
        if pattern in norm_path:
            return {"decision": "allow"}

    # 3. Check Base Name / Exact Allowed Files
    base_name = os.path.basename(norm_path)
    if base_name in ALLOWED_BASENAMES:
        return {"decision": "allow"}

    # 4. Check Allowed Directories
    path_parts = norm_path.split(os.sep)
    for allowed_dir in ALLOWED_DIRS:
        if allowed_dir in path_parts:
            return {"decision": "allow"}

    # 5. Check Allowed Metadata Extensions (Markdown, JSON, YAML)
    _, ext = os.path.splitext(norm_path)
    if ext.lower() in ALLOWED_EXTENSIONS:
        return {"decision": "allow"}

    # 6. Check if file is in a protected source directory or has code extension
    is_code_file = ext.lower() in CODE_EXTENSIONS
    is_in_protected_dir = any(p_dir in path_parts for p_dir in PROTECTED_DIRS)

    if is_code_file or is_in_protected_dir:
        return {
            "decision": "force_ask",
            "reason": (
                f"⚠️ [Swarm Governance Alert] Koordynator próbuje zmodyfikować kod produkcyjny ({norm_path}) "
                f"bezpośrednio w głównym drzewie projektu poza worktree.\n"
                f"• Jeśli to SZYBKI HOTFIX (np. 1 linijka, literówka, debug) -> Kliknij ZEZWÓL (Allow).\n"
                f"• Jeśli to NOWY FICZER / refaktor -> Kliknij ODRZUĆ (Deny), aby agent utworzył worktree i oddelegował do subagenta Buildera."
            )
        }

    # Default: allow unrecognized non-code files
    return {"decision": "allow"}


def main():
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            json.dump({"decision": "allow"}, sys.stdout)
            sys.stdout.write("\n")
            return

        payload = json.loads(raw_input)
        result = evaluate_tool_call(payload)
        json.dump(result, sys.stdout)
        sys.stdout.write("\n")
    except Exception as e:
        # Failsafe: log error to stderr, don't crash
        sys.stderr.write(f"[guard_coordinator_pretool.py] Error: {e}\n")
        json.dump({"decision": "allow"}, sys.stdout)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
