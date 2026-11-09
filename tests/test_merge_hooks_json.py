import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, SCRIPTS)
import merge_hooks_json as m  # noqa: E402

TEMPLATE = {
    "guard-confidential-gemini": {"PreToolUse": [{"matcher": ".*", "hooks": [{"type": "command", "command": "python3 scripts/guard_confidential_gemini.py"}]}]},
    "distributed-sync": {"SessionStart": [{"type": "command", "command": "git pull"}]},
}


class TestMergeHooksJson(unittest.TestCase):
    def path(self, content=None):
        d = tempfile.mkdtemp()
        p = os.path.join(d, ".gemini", "hooks.json")
        if content is not None:
            os.makedirs(os.path.dirname(p))
            open(p, "w", encoding="utf-8").write(content)
        return p

    def load(self, p):
        return json.load(open(p, encoding="utf-8"))

    def run_process(self, p, refresh=False):
        out = []
        r = m.process(p, TEMPLATE, refresh, out.append)
        return r, out

    def test_missing_file_created_from_template(self):
        p = self.path()
        r, _ = self.run_process(p)
        self.assertEqual(r, "created")
        self.assertEqual(self.load(p), TEMPLATE)

    def test_custom_keys_preserved_and_missing_added(self):
        custom = {"my-hook": {"Stop": [{"type": "command", "command": "echo hi"}]}}
        p = self.path(json.dumps(custom))
        r, _ = self.run_process(p)
        self.assertEqual(r, "merged")
        cfg = self.load(p)
        self.assertEqual(cfg["my-hook"], custom["my-hook"])
        for k in TEMPLATE:
            self.assertEqual(cfg[k], TEMPLATE[k])

    def test_differing_managed_key_kept_without_refresh(self):
        mine = {"distributed-sync": {"SessionStart": [{"type": "command", "command": "custom"}]}}
        p = self.path(json.dumps(mine))
        r, out = self.run_process(p)
        cfg = self.load(p)
        self.assertEqual(cfg["distributed-sync"], mine["distributed-sync"])
        self.assertIn("guard-confidential-gemini", cfg)
        self.assertTrue(any("różni się od szablonu" in line for line in out))
        self.assertFalse(os.path.exists(p + ".bak"))

    def test_refresh_replaces_only_managed_keys_with_backup(self):
        mine = {"distributed-sync": {"old": 1}, "my-hook": {"keep": True}}
        p = self.path(json.dumps(mine))
        r, _ = self.run_process(p, refresh=True)
        cfg = self.load(p)
        self.assertEqual(cfg["distributed-sync"], TEMPLATE["distributed-sync"])
        self.assertEqual(cfg["my-hook"], {"keep": True})
        self.assertEqual(json.load(open(p + ".bak")), mine)

    def test_invalid_json_untouched(self):
        p = self.path("{ not json")
        r, _ = self.run_process(p)
        self.assertEqual(r, "invalid")
        self.assertEqual(open(p).read(), "{ not json")

    def test_non_object_json_untouched(self):
        p = self.path("[1, 2]")
        r, _ = self.run_process(p)
        self.assertEqual(r, "invalid")
        self.assertEqual(open(p).read(), "[1, 2]")

    def test_idempotent_second_run_does_not_rewrite(self):
        p = self.path(json.dumps({"x": 1}))
        self.run_process(p)
        before = (open(p).read(), os.stat(p).st_mtime_ns)
        r, _ = self.run_process(p)
        self.assertEqual(r, "unchanged")
        self.assertEqual((open(p).read(), os.stat(p).st_mtime_ns), before)

    def test_indent_preserved(self):
        p = self.path('{\n    "my-hook": {}\n}\n')
        self.run_process(p)
        self.assertIn('\n    "my-hook"', open(p).read())

    def test_cli_template_stdin_and_exit_codes(self):
        p = self.path(json.dumps({"x": 1}))
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "merge_hooks_json.py"), p, "--template-stdin"],
                           input=json.dumps(TEMPLATE), capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("guard-confidential-gemini", self.load(p))
        bad = subprocess.run([sys.executable, os.path.join(SCRIPTS, "merge_hooks_json.py"), p, "--template-stdin"],
                             input="not json", capture_output=True, text=True)
        self.assertEqual(bad.returncode, 2)
        self.assertEqual(self.load(p).get("x"), 1)


if __name__ == "__main__":
    unittest.main()
