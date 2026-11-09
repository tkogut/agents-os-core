"""Wymusza Rule 4 (.agents/rules/core-rule.md): VERSION jest źródłem prawdy, żywe pliki mają tę samą wersję.

Pliki historyczne (CHANGELOG dla wydanych wersji, cytowane dokumenty źródłowe, specyfikacje z datą)
celowo nie są sprawdzane.
"""
import glob
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LIVE_FILES = [
    "README.md", "CLAUDE.md", "SDLC.md", "agents.yaml", ".gitignore", ".gitattributes",
    "docs/API.md", "docs/SKILLS_ARCHITECTURE.md", "OM_SKILLS_NOTEBOOKLM_KNOWLEDGE_BASE.md",
    "vault/CLAUDE.md", "vault/SDLC.md", "vault/agents.yaml", "vault/.gitattributes",
    "vault/task.md", "vault/os-run-builder",
    "os-upgrade-project", "os-add-skill", "INSTALL.sh",
]
LIVE_GLOBS = ["global_skills/swarm-bootstrapper/scripts/*.py"]
# Linie, które legalnie wymieniają stare wersje (sprzątanie starych szablonów, opis zmiany historycznej).
ALLOW_LINE = re.compile(r"old_tmpl|bumped from")
PATTERNS = [
    re.compile(r"AGENTS-OS (?:Platform )?v(\d+\.\d+)"),
    re.compile(r"\bv(\d+\.\d+)-swarm\b"),
    re.compile(r"^version:\s*(\d+\.\d+)(?:-swarm)?\s*$"),
    re.compile(r"^# Wersja:\s*(\d+\.\d+)-swarm"),
]


def read_version():
    with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as fh:
        return fh.read().strip()


class TestVersionConsistency(unittest.TestCase):
    def setUp(self):
        self.version = read_version()
        m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)-swarm", self.version)
        self.assertIsNotNone(m, f"VERSION musi mieć postać MAJOR.MINOR.PATCH-swarm, jest: {self.version!r}")
        self.short = f"{m.group(1)}.{m.group(2)}"

    def live_paths(self):
        paths = [os.path.join(ROOT, f) for f in LIVE_FILES]
        for g in LIVE_GLOBS:
            paths += glob.glob(os.path.join(ROOT, g))
        return paths

    def test_live_files_use_current_version(self):
        problems = []
        for path in self.live_paths():
            self.assertTrue(os.path.exists(path), f"brak pliku z listy żywych: {path}")
            with open(path, encoding="utf-8") as fh:
                for n, line in enumerate(fh, 1):
                    if ALLOW_LINE.search(line):
                        continue
                    for pat in PATTERNS:
                        for found in pat.findall(line):
                            if found != self.short:
                                problems.append(f"{os.path.relpath(path, ROOT)}:{n}: v{found} (oczekiwano v{self.short})")
        self.assertEqual(problems, [], "Stare wersje w żywych plikach:\n" + "\n".join(problems))

    def test_first_lines_of_state_files(self):
        for rel in (".agents/MEMORY.md", ".agents/task.md"):
            with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                head = fh.readline()
            for pat in PATTERNS[:1]:
                for found in pat.findall(head):
                    self.assertEqual(found, self.short, f"{rel}: nagłówek ma v{found}")

    def test_agentic_config_version(self):
        with open(os.path.join(ROOT, ".ai", "agentic.config.json"), encoding="utf-8") as fh:
            cfg = json.load(fh)
        self.assertEqual(cfg.get("version"), f"{self.short}-swarm")

    def test_install_template_dir_matches_version(self):
        with open(os.path.join(ROOT, "INSTALL.sh"), encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn(f'templates/v{self.short}-swarm"', text)

    def test_changelog_has_current_release_header(self):
        with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as fh:
            self.assertIn(f"## [{self.version}]", fh.read())


if __name__ == "__main__":
    unittest.main()
