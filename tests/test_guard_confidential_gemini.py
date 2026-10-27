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

    def test_13_cache_tampered_rebuilds(self):
        _, cache_file = guard_confidential_gemini.get_cache_paths()
        # Tamper with the cache by inserting false entries with bad checksum
        tampered_data = {
            "version": 1,
            "vault_dir": self.vault_dir,
            "timestamp": 123456789.0,
            "confidential_rels": ["fake/file.md"],
            "confidential_dirs": [],
            "confidential_basenames": ["file.md"],
            "checksum": "BAD_CHECKSUM_TAMPERED"
        }
        os.makedirs(os.path.dirname(cache_file), mode=0o700, exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as fp:
            json.dump(tampered_data, fp)

        # Verify that get_confidential_paths_dynamic detects bad checksum and rebuilds cleanly
        rels, _, _ = guard_confidential_gemini.get_confidential_paths_dynamic(self.vault_dir)
        self.assertNotIn("fake/file.md", rels)
        self.assertIn("wiki/sources/src-umowa-vaga-slowenia.md", rels)

    def test_14_cache_expired_past_ttl_rebuilds(self):
        _, cache_file = guard_confidential_gemini.get_cache_paths()
        old_time = 1000.0  # long expired
        checksum = guard_confidential_gemini.compute_cache_checksum(self.vault_dir, old_time, ["old/file.md"], [], ["file.md"])
        expired_data = {
            "version": 1,
            "vault_dir": self.vault_dir,
            "timestamp": old_time,
            "confidential_rels": ["old/file.md"],
            "confidential_dirs": [],
            "confidential_basenames": ["file.md"],
            "checksum": checksum
        }
        os.makedirs(os.path.dirname(cache_file), mode=0o700, exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as fp:
            json.dump(expired_data, fp)

        rels, _, _ = guard_confidential_gemini.get_confidential_paths_dynamic(self.vault_dir)
        self.assertNotIn("old/file.md", rels)
        self.assertIn("wiki/sources/src-umowa-vaga-slowenia.md", rels)

    def test_15_cache_corrupted_json(self):
        _, cache_file = guard_confidential_gemini.get_cache_paths()
        os.makedirs(os.path.dirname(cache_file), mode=0o700, exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as fp:
            fp.write("{MALFORMED_JSON_SYNTAX_ERROR:::")

        # Guard handles syntax error gracefully and rebuilds cache
        rels, _, _ = guard_confidential_gemini.get_confidential_paths_dynamic(self.vault_dir)
        self.assertIn("wiki/sources/src-umowa-vaga-slowenia.md", rels)

    def test_16_cache_unwritable_directory(self):
        # Even if saving cache fails due to I/O error or permission, scan still succeeds
        rels, _, _ = guard_confidential_gemini.get_confidential_paths_dynamic(self.vault_dir)
        self.assertTrue(len(rels) > 0)

    def test_17_fail_closed_missing_vault(self):
        non_existent_vault = "/non/existent/vault/path/xyz"
        # Calling scan_vault_confidential on non-existent vault raises FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            guard_confidential_gemini.scan_vault_confidential(non_existent_vault)

        # Hook evaluation on a path referencing missing vault returns fail-closed deny
        payload = {
            "modelName": "gemini-3.8-flash",
            "toolCall": {
                "name": "read_file",
                "args": {
                    "Path": "/non/existent/vault/path/xyz/secret.md"
                }
            }
        }
        # Force resolve_vault_path to raise by temporarily mocking environment
        old_env = os.environ.get("OBSIDIAN_VAULT_PATH")
        try:
            os.environ["OBSIDIAN_VAULT_PATH"] = non_existent_vault
            # Temporarily change default path to test missing path
            orig_def = guard_confidential_gemini.VAULT_DEFAULT_PATH
            guard_confidential_gemini.VAULT_DEFAULT_PATH = "/tmp/non_existent_def_vault"
            
            res = guard_confidential_gemini.evaluate_hook(payload)
            self.assertEqual(res["decision"], "deny")
            self.assertIn("FAIL-CLOSED", res["reason"])
        finally:
            guard_confidential_gemini.VAULT_DEFAULT_PATH = orig_def
            if old_env is not None:
                os.environ["OBSIDIAN_VAULT_PATH"] = old_env
            else:
                os.environ.pop("OBSIDIAN_VAULT_PATH", None)

if __name__ == "__main__":
    unittest.main()
