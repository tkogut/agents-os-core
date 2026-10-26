import unittest
import sys
import os
import json

# Add scripts directory to path
scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, os.path.abspath(scripts_dir))

import guard_confidential_gemini

VAULT_PATH = "/mnt/c/Users/tkogut/Documents/sejf_tk"

class TestGuardConfidentialGemini(unittest.TestCase):

    def setUp(self):
        self.vault_dir = guard_confidential_gemini.resolve_vault_path()

    def test_01_gemini_reading_confidential_wiki_source(self):
        payload = {
            "modelName": "gemini-3.8-flash",
            "toolCall": {
                "name": "read_file",
                "args": {
                    "Path": os.path.join(self.vault_dir, "wiki/sources/src-umowa-vaga-slowenia.md")
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "deny")
        self.assertIn("POLITYKA POUFNOŚCI GEMINI", res["reason"])
        self.assertIn("Claude Code", res["reason"])

    def test_02_gemini_reading_raw_notes_source_copy(self):
        payload = {
            "modelName": "gemini-3.1-pro",
            "toolCall": {
                "name": "view_file",
                "args": {
                    "AbsolutePath": os.path.join(self.vault_dir, "raw/notes/umowa-dystrybucyjna-vaga-slowenia.md")
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "deny")
        self.assertIn("POLITYKA POUFNOŚCI GEMINI", res["reason"])

    def test_03_gemini_reading_human_zone_original(self):
        payload = {
            "modelName": "gemini-3.8-flash",
            "toolCall": {
                "name": "read_file",
                "args": {
                    "Path": os.path.join(self.vault_dir, "Firma/Umowa Dystrybucyjna na Wyłączność (Słowenia) – VAGA D.O.O..md")
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "deny")
        self.assertIn("POLITYKA POUFNOŚCI GEMINI", res["reason"])

    def test_04_windows_path_normalization(self):
        win_path = r"C:\Users\tkogut\Documents\sejf_tk\wiki\sources\src-umowa-vaga-slowenia.md"
        payload = {
            "modelName": "gemini-3.8-flash",
            "toolCall": {
                "name": "read_file",
                "args": {
                    "Path": win_path
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "deny")

    def test_05_fail_closed_missing_model_name(self):
        payload = {
            "modelName": "",
            "toolCall": {
                "name": "read_file",
                "args": {
                    "Path": os.path.join(self.vault_dir, "wiki/entities/vaga-doo.md")
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "deny")

    def test_06_claude_allowed_through_this_hook(self):
        payload = {
            "modelName": "claude-sonnet-5",
            "toolCall": {
                "name": "read_file",
                "args": {
                    "Path": os.path.join(self.vault_dir, "wiki/sources/src-umowa-vaga-slowenia.md")
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "allow")

    def test_07_gemini_reading_non_confidential_file(self):
        # index.md is public
        payload = {
            "modelName": "gemini-3.8-flash",
            "toolCall": {
                "name": "read_file",
                "args": {
                    "Path": os.path.join(self.vault_dir, "index.md")
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "allow")

    def test_08_gemini_reading_agents_md(self):
        payload = {
            "modelName": "gemini-3.8-flash",
            "toolCall": {
                "name": "read_file",
                "args": {
                    "Path": os.path.join(self.vault_dir, "AGENTS.md")
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "allow")

    def test_09_bash_direct_reference_to_confidential_file(self):
        payload = {
            "modelName": "gemini-3.8-flash",
            "toolCall": {
                "name": "run_command",
                "args": {
                    "CommandLine": "cat /mnt/c/Users/tkogut/Documents/sejf_tk/raw/notes/umowa-dystrybucyjna-vaga-slowenia.md"
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "deny")
        self.assertIn("ODRZUCONO (Bash)", res["reason"])

    def test_10_bash_recursive_search_over_vault(self):
        payload = {
            "modelName": "gemini-3.8-flash",
            "toolCall": {
                "name": "run_command",
                "args": {
                    "CommandLine": "grep -rn 'VAGA' /mnt/c/Users/tkogut/Documents/sejf_tk"
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "deny")
        self.assertIn("ODRZUCONO (Bash Search)", res["reason"])

    def test_11_bash_recursive_search_over_confidential_subdir(self):
        payload = {
            "modelName": "gemini-3.8-flash",
            "toolCall": {
                "name": "run_command",
                "args": {
                    "CommandLine": "find wiki -name '*.md' -exec grep 'VAGA' {} +"
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "deny")

    def test_12_bash_non_vault_command_allowed(self):
        payload = {
            "modelName": "gemini-3.8-flash",
            "toolCall": {
                "name": "run_command",
                "args": {
                    "CommandLine": "python3 scripts/validate-handshakes.py"
                }
            }
        }
        res = guard_confidential_gemini.evaluate_hook(payload)
        self.assertEqual(res["decision"], "allow")

if __name__ == "__main__":
    unittest.main()
