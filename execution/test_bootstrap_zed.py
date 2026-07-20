import os
import sys
import shutil
import json
import subprocess
import unittest

class TestBootstrapZed(unittest.TestCase):
    def setUp(self):
        self.projects_dir = os.path.expanduser("~/projects")
        self.test_project = "test-zed-project-temp"
        self.project_path = os.path.join(self.projects_dir, self.test_project)
        # Ensure we start clean
        if os.path.exists(self.project_path):
            shutil.rmtree(self.project_path)

    def tearDown(self):
        # Clean up
        if os.path.exists(self.project_path):
            shutil.rmtree(self.project_path)

    def test_successful_bootstrap_zed(self):
        # Run bootstrap_zed.py
        script_path = os.path.join(os.path.dirname(__file__), "bootstrap_zed.py")

        # Override WSL_DISTRO_NAME and disable zed executable search or run it with safe path
        env = os.environ.copy()
        env["WSL_DISTRO_NAME"] = "TestDistro"

        # Run the script via subprocess
        # We pass a test project name
        res = subprocess.run([sys.executable, script_path, self.test_project], env=env, capture_output=True, text=True)

        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)

        # The script should complete successfully (exit code 0 or warning about zed executable not found, but overall status success)
        self.assertEqual(res.returncode, 0)

        # 1. Verify directory structure
        self.assertTrue(os.path.exists(os.path.join(self.project_path, ".agents")))
        self.assertTrue(os.path.exists(os.path.join(self.project_path, "src")))
        self.assertTrue(os.path.exists(os.path.join(self.project_path, ".zed")))

        # 2. Verify settings.json compliance
        settings_path = os.path.join(self.project_path, ".zed", "settings.json")
        self.assertTrue(os.path.exists(settings_path))

        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        self.assertEqual(settings.get("ai_privacy"), "high")
        self.assertIn("telemetry", settings)
        self.assertFalse(settings["telemetry"].get("diagnostics"))
        self.assertFalse(settings["telemetry"].get("metrics"))

        # 3. Verify git setup
        self.assertTrue(os.path.exists(os.path.join(self.project_path, ".git")))

        # Verify that root commit is created and there are commits in the repo
        res_git = subprocess.run(["git", "log", "--oneline"], cwd=self.project_path, capture_output=True, text=True)
        self.assertEqual(res_git.returncode, 0)
        self.assertIn("initial commit", res_git.stdout)

    def test_directory_traversal_protection(self):
        # Attempt to escape PROJECTS_DIR
        script_path = os.path.join(os.path.dirname(__file__), "bootstrap_zed.py")
        malicious_project = "../malicious-traversal"

        res = subprocess.run([sys.executable, script_path, malicious_project], capture_output=True, text=True)

        # The script must fail with exit code 1 due to safety boundary
        self.assertEqual(res.returncode, 1)
        self.assertIn("ERROR: Project path", res.stderr)

if __name__ == "__main__":
    unittest.main()
