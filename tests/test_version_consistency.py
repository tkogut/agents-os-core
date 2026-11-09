"""Wymusza Rule 4 (.agents/rules/core-rule.md): VERSION jest źródłem prawdy, wszystkie żywe pliki mają tę samą wersję.

Skanuje WSZYSTKIE śledzone pliki tekstowe poza historycznymi (CHANGELOG, dokumenty źródłowe, specyfikacje z datą,
raporty, handshake'e, katalog zewnętrznego katalogu skilli). Dokumenty czekające na przegląd treści są jawnie
wymienione w PENDING_REVIEW i znikają stąd, gdy zostaną zaktualizowane.
"""
import json
import os
import re
import subprocess
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HISTORICAL = re.compile(
    r"^(tmp/|\.ai/specs/|\.agents/mcp-servers/|\.agents/specs/archive/)|knowledge/|CHANGELOG\.md$|_handshake\.json$|"
    r"swarm_audit_report|BACKWARD_COMPAT|antigravity-docs|awesome-skills-catalog"
)
# Dokumenty z treścią opisującą starsze wersje; do przeglądu w osobnym PR (usuń z listy po aktualizacji).
PENDING_REVIEW = {
    ".agents/specs/AGENTS-OS.md", ".agents/specs/architecture.md", ".agents/specs/graph.json",
    ".agents/eval/evaluator.md", ".agents/hooks/claude-pre-tool-guard.sh",
}
# Stan sesji i historia: tylko pierwsza linia (nagłówek) ma być aktualna.
STATE_FILES = {".agents/MEMORY.md", ".agents/task.md", "vault/.agents/MEMORY.md", "vault/.agents/task.md",
               "vault/HANDOFF.md"}
# Pliki, w których klucz `version:` oznacza wersję systemu (w innych, np. SKILL.md, to wersja skilla).
VERSION_KEY_FILES = {"agents.yaml", "vault/agents.yaml", "CLAUDE.md", "vault/CLAUDE.md", "vault/task.md"}
ALLOW_LINE = re.compile(r"old_tmpl|bumped from|Historia|from `?6\.5")
PATTERNS = [
    re.compile(r"AGENTS-OS (?:Platform )?v(\d+\.\d+)"),
    re.compile(r"\bv(\d+\.\d+)-swarm\b"),
    re.compile(r"(?:^|\s)(?:Version|Wersja):\s*(\d+\.\d+)-swarm"),
]
KEY_PATTERN = re.compile(r"^version:\s*(\d+\.\d+)(?:-swarm)?\s*$")


def read_version():
    with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as fh:
        return fh.read().strip()


def tracked_files():
    out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    return [f for f in out.split("\n") if f]


class TestVersionConsistency(unittest.TestCase):
    def setUp(self):
        self.version = read_version()
        m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)-swarm", self.version)
        self.assertIsNotNone(m, f"VERSION musi mieć postać MAJOR.MINOR.PATCH-swarm, jest: {self.version!r}")
        self.short = f"{m.group(1)}.{m.group(2)}"

    def scan(self, rel, only_first_line=False):
        problems = []
        try:
            with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                lines = fh.readlines()
        except (UnicodeDecodeError, OSError, IsADirectoryError):
            return problems
        for n, line in enumerate(lines[:1] if only_first_line else lines, 1):
            if ALLOW_LINE.search(line):
                continue
            pats = list(PATTERNS)
            found = [x for p in pats for x in p.findall(line)]
            if rel in VERSION_KEY_FILES:
                found += KEY_PATTERN.findall(line)
            for f in found:
                if f != self.short:
                    problems.append(f"{rel}:{n}: v{f} (oczekiwano v{self.short})")
        return problems

    def test_all_live_files_use_current_version(self):
        problems = []
        for rel in tracked_files():
            if HISTORICAL.search(rel) or rel in PENDING_REVIEW:
                continue
            problems += self.scan(rel, only_first_line=rel in STATE_FILES)
        self.assertEqual(problems, [], "Stare wersje w żywych plikach:\n" + "\n".join(problems))

    def test_pending_review_list_has_no_stale_entries(self):
        tracked = set(tracked_files())
        for rel in PENDING_REVIEW:
            self.assertIn(rel, tracked, f"PENDING_REVIEW wskazuje nieistniejący plik: {rel}")

    def test_agentic_config_versions(self):
        for rel in (".ai/agentic.config.json", "vault/.ai/agentic.config.json"):
            with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                self.assertEqual(json.load(fh).get("version"), f"{self.short}-swarm", rel)

    def test_install_template_dir_matches_version(self):
        with open(os.path.join(ROOT, "INSTALL.sh"), encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn(f'templates/v{self.short}-swarm"', text)

    def test_changelog_has_current_release_header(self):
        with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as fh:
            self.assertIn(f"## [{self.version}]", fh.read())


if __name__ == "__main__":
    unittest.main()
