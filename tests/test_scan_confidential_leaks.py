import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, SCRIPTS)
import scan_confidential_leaks as scan  # noqa: E402

# Synthetic values assembled at runtime so no real-looking secret sits in this file.
FAKE_CANARY = "CANARY-SB-" + "TESTFAKE01"
FAKE_JWT = ".".join(["eyJ" + "a" * 10, "b" * 10, "c" * 10])
FAKE_AWS = "AKIA" + "A" * 16


def run(root, *extra, stdin=None):
    buf = io.StringIO()
    old = sys.stdin
    if stdin is not None:
        sys.stdin = io.StringIO(stdin)
    try:
        with redirect_stdout(buf):
            code = scan.main(["--root", root, *extra])
    finally:
        sys.stdin = old
    return code, buf.getvalue()


class TestScanConfidentialLeaks(unittest.TestCase):
    def mkroot(self, memory="", task="", handshake=None):
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, ".agents", "swarm"))
        open(os.path.join(d, ".agents", "MEMORY.md"), "w").write(memory)
        open(os.path.join(d, ".agents", "task.md"), "w").write(task)
        if handshake is not None:
            open(os.path.join(d, ".agents", "swarm", "x_builder_handshake.json"), "w").write(handshake)
        return d

    def test_clean_repo_passes(self):
        code, out = run(self.mkroot("Decyzje: plan second-brain, prefiks CANARY-SB- bez wartosci.", "- [ ] task"))
        self.assertEqual(code, 0)
        self.assertIn("ZDANY", out)

    def test_canary_in_memory_detected_without_printing_value(self):
        code, out = run(self.mkroot(f"notatka {FAKE_CANARY} koniec"))
        self.assertEqual(code, 1)
        self.assertIn(".agents/MEMORY.md: CANARY", out)
        self.assertNotIn(FAKE_CANARY, out)
        self.assertNotIn("TESTFAKE01", out)

    def test_canary_in_handshake_detected(self):
        code, out = run(self.mkroot(handshake='{"notes": "%s"}' % FAKE_CANARY))
        self.assertEqual(code, 1)
        self.assertIn("_handshake.json: CANARY", out)

    def test_secret_patterns_detected_rule_names_only(self):
        text = f"jwt {FAKE_JWT}\naws {FAKE_AWS}\npassword = Abcdefgh12345678\nurl https://user:hunter2x@host/db"
        code, out = run(self.mkroot(task=text))
        self.assertEqual(code, 1)
        for rule in ("JWT", "AWS_ACCESS_KEY", "CREDENTIAL_PAIR", "CONNECTION_STRING"):
            self.assertIn(f".agents/task.md: {rule}", out)
        for value in (FAKE_JWT, FAKE_AWS, "Abcdefgh12345678", "hunter2x"):
            self.assertNotIn(value, out)

    def test_stdin_pr_description_scanned(self):
        code, out = run(self.mkroot("ok"), "--stdin", stdin=f"opis PR {FAKE_CANARY}")
        self.assertEqual(code, 1)
        self.assertIn("<stdin>: CANARY", out)
        self.assertNotIn(FAKE_CANARY, out)

    def test_extra_file_and_unreadable_target_fail_closed(self):
        root = self.mkroot("ok")
        extra = os.path.join(root, "pr.md")
        open(extra, "w").write(FAKE_CANARY)
        code, out = run(root, "--file", extra)
        self.assertEqual(code, 1)
        os.chmod(extra, 0)
        if os.access(extra, os.R_OK):  # running as root: cannot simulate
            self.skipTest("cannot make file unreadable")
        code, out = run(root, "--file", extra)
        self.assertEqual(code, 2)
        self.assertIn("READ_ERROR", out)

    def test_placeholder_prefix_not_a_hit(self):
        self.assertEqual(scan.scan_text("CANARY-SB-<losowy> oraz CANARY-SB-"), [])

    def test_cli_exit_code(self):
        root = self.mkroot(FAKE_CANARY)
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "scan_confidential_leaks.py"), "--root", root],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertNotIn(FAKE_CANARY, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
