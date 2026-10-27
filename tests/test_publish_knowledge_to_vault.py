import unittest
import sys
import os
import shutil
import tempfile

# Add scripts directory to path
scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, os.path.abspath(scripts_dir))

import publish_knowledge_to_vault

class TestPublishKnowledgeToVault(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_pub_vault_")
        self.source_dir = os.path.join(self.test_dir, "source")
        self.dest_dir = os.path.join(self.test_dir, "raw", "notes")
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.dest_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_01_clean_file_dry_run_and_apply(self):
        clean_note = os.path.join(self.source_dir, "architektura-systemu.md")
        with open(clean_note, "w", encoding="utf-8") as fp:
            fp.write("---\ntitle: Architektura\n---\n# Architektura\nOpis architektury AGENTS-OS.")

        # 1. Dry run
        res_dry = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=False)
        self.assertEqual(len(res_dry["published"]), 1)
        self.assertEqual(len(res_dry["blocked"]), 0)
        self.assertEqual(len(res_dry["conflicts"]), 0)
        # Verify file NOT written yet
        target_path = os.path.join(self.dest_dir, "architektura-systemu.md")
        self.assertFalse(os.path.exists(target_path))

        # 2. Apply
        res_apply = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=True)
        self.assertEqual(len(res_apply["published"]), 1)
        self.assertTrue(os.path.exists(target_path))

        # Verify enriched frontmatter
        with open(target_path, "r", encoding="utf-8") as fp:
            content = fp.read()
        self.assertIn("source: agents-os-core", content)
        self.assertIn("status: new", content)
        self.assertIn("title: Architektura", content)
        self.assertIn("published: ", content)

    def test_02_secrets_and_pii_blocked(self):
        # Create files with various secret patterns
        bad_files = {
            "key_sk.md": "API key: " + "sk-" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
            "aws.md": "Config: " + "AKIA" + "IOSFODNN7EXAMPLE",
            "jwt.md": "Token: " + "ey" + "JhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." + "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0." + "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
            "private_key.md": "-----BEGIN " + "RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA...\n-----END RSA PRIVATE KEY-----",
            "email_ext.md": "Contact author at john.doe@external-corp.com for info.",
            "pesel.md": "Klient PESEL: 44051401359 weryfikacja tożsamości.",
            "password.md": "Database password: secretPassword123! in connection"
        }

        for filename, content in bad_files.items():
            f_path = os.path.join(self.source_dir, filename)
            with open(f_path, "w", encoding="utf-8") as fp:
                fp.write(content)

        res = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=True)
        self.assertEqual(len(res["blocked"]), len(bad_files))
        self.assertEqual(len(res["published"]), 0)

        # Verify that output reports pattern names, never secret values
        for blocked_item in res["blocked"]:
            for pattern in blocked_item["patterns"]:
                self.assertIn(pattern, [
                    "API_KEY_SK", "AWS_ACCESS_KEY", "JWT_TOKEN", "PRIVATE_KEY",
                    "PII_EXTERNAL_EMAIL", "PII_PESEL", "SECRET_CREDENTIAL"
                ])
                # Ensure no secrets leaked into pattern string
                self.assertNotIn("sk-", pattern)
                self.assertNotIn("AKIA", pattern)

    def test_03_repeated_run_idempotent_skip(self):
        note_path = os.path.join(self.source_dir, "kompendium.md")
        with open(note_path, "w", encoding="utf-8") as fp:
            fp.write("# Kompendium\nTreść kompendium.")

        # First run: published
        res1 = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=True)
        self.assertEqual(len(res1["published"]), 1)

        # Second run: identical content skipped
        res2 = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=True)
        self.assertEqual(len(res2["published"]), 0)
        self.assertEqual(len(res2["skipped"]), 1)
        self.assertEqual(res2["skipped"][0]["reason"], "IDENTICAL_CONTENT")

    def test_04_conflict_when_target_has_different_content(self):
        note_name = "specyfikacja.md"
        src_path = os.path.join(self.source_dir, note_name)
        with open(src_path, "w", encoding="utf-8") as fp:
            fp.write("# Nowa Wersja Specyfikacji\nZaktualizowana treść.")

        # Target file already exists with different content
        target_path = os.path.join(self.dest_dir, note_name)
        with open(target_path, "w", encoding="utf-8") as fp:
            fp.write("# Stara Wersja Specyfikacji\nZupełnie inna treść istniejąca w vaulcie.")

        res = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=True)
        self.assertEqual(len(res["conflicts"]), 1)
        self.assertEqual(len(res["published"]), 0)
        self.assertEqual(res["conflicts"][0]["reason"], "TARGET_EXISTS_WITH_DIFFERENT_CONTENT")

        # Verify target file was NOT overwritten
        with open(target_path, "r", encoding="utf-8") as fp:
            content = fp.read()
        self.assertIn("Stara Wersja Specyfikacji", content)

    def test_05_symlink_ignored(self):
        real_file = os.path.join(self.test_dir, "real.md")
        with open(real_file, "w", encoding="utf-8") as fp:
            fp.write("# Prawdziwy plik")

        symlink_path = os.path.join(self.source_dir, "symlink_note.md")
        os.symlink(real_file, symlink_path)

        res = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=True)
        self.assertEqual(len(res["published"]), 0)
        self.assertEqual(len(res["skipped"]), 1)
        self.assertEqual(res["skipped"][0]["reason"], "SYMLINK_IGNORED")

    def test_06_missing_source_directory_handled(self):
        res = publish_knowledge_to_vault.publish_notes("/non/existent/source/dir", self.dest_dir, apply=True)
        self.assertEqual(len(res["errors"]), 1)
        self.assertIn("Katalog źródłowy nie istnieje", res["errors"][0])

    def test_07_ingest_scaffolding_dry_run_and_apply(self):
        # Create vault structure
        index_path = os.path.join(self.test_dir, "index.md")
        with open(index_path, "w", encoding="utf-8") as fp:
            fp.write("# Centralny Indeks\n\n## Źródła (sources)\n- [[src-istniejace]] – Istniejące źródło\n")

        log_path = os.path.join(self.test_dir, "log.md")
        with open(log_path, "w", encoding="utf-8") as fp:
            fp.write("# Log\n\n## [2026-10-26] init | Start\n")

        # Create source note
        note_name = "nowa_architektura.md"
        src_note = os.path.join(self.source_dir, note_name)
        with open(src_note, "w", encoding="utf-8") as fp:
            fp.write("---\ntags: [ai-sdlc, open-mercato]\n---\n# Nowa Architektura Roju\nTo jest akapit wprowadzający opisujący architekturę roju.\n\n## Główne Składowe\n- Opis modułów.")

        # 1. Dry run with ingest
        res_dry = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=False, ingest=True)
        self.assertEqual(len(res_dry["published"]), 1)
        self.assertEqual(len(res_dry["ingested"]), 1)
        self.assertEqual(res_dry["ingested"][0]["status"], "DRY-RUN (ready to scaffold)")
        # Verify source page not created yet
        expected_src_page = os.path.join(self.test_dir, "wiki", "sources", "src-nowa-architektura.md")
        self.assertFalse(os.path.exists(expected_src_page))

        # 2. Apply with ingest
        res_apply = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=True, ingest=True)
        self.assertEqual(len(res_apply["published"]), 1)
        self.assertEqual(len(res_apply["ingested"]), 1)
        self.assertEqual(res_apply["ingested"][0]["status"], "SCAFFOLDED")

        # Verify source page created with correct structure
        self.assertTrue(os.path.exists(expected_src_page))
        with open(expected_src_page, "r", encoding="utf-8") as fp:
            src_content = fp.read()
        self.assertIn('title: "Źródło: Nowa Architektura Roju"', src_content)
        self.assertIn("type: source", src_content)
        self.assertIn("## Podsumowanie", src_content)
        self.assertIn("To jest akapit wprowadzający opisujący architekturę roju.", src_content)
        self.assertIn("## Szczegóły", src_content)
        self.assertIn("**Główne Składowe**", src_content)
        self.assertIn("## Powiązania", src_content)
        self.assertIn("[[overview]]", src_content)
        self.assertIn("[[index]]", src_content)

        # Verify index.md updated
        with open(index_path, "r", encoding="utf-8") as fp:
            idx_content = fp.read()
        self.assertIn("[[src-nowa-architektura]] – Nowa Architektura Roju", idx_content)

        # Verify log.md updated
        with open(log_path, "r", encoding="utf-8") as fp:
            log_content = fp.read()
        self.assertIn("ingest | Nowa Architektura Roju", log_content)

        # Verify raw note marked processed
        raw_note_path = os.path.join(self.dest_dir, note_name)
        with open(raw_note_path, "r", encoding="utf-8") as fp:
            raw_content = fp.read()
        self.assertIn("status: processed", raw_content)
        self.assertIn("processed: ", raw_content)

    def test_08_ingest_skips_existing_source_page_without_overwriting(self):
        # Create existing source page
        sources_dir = os.path.join(self.test_dir, "wiki", "sources")
        os.makedirs(sources_dir, exist_ok=True)
        existing_src_page = os.path.join(sources_dir, "src-istniejaca-notatka.md")
        with open(existing_src_page, "w", encoding="utf-8") as fp:
            fp.write("# Ręcznie napisana strona źródłowa — NIE NADPISYWAĆ!")

        # Create note
        note_name = "istniejaca_notatka.md"
        src_note = os.path.join(self.source_dir, note_name)
        with open(src_note, "w", encoding="utf-8") as fp:
            fp.write("# Istniejąca Notatka\nNowa treść.")

        res = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=True, ingest=True)
        self.assertEqual(len(res["published"]), 1)
        self.assertEqual(len(res["ingested"]), 1)
        self.assertEqual(res["ingested"][0]["status"], "EXISTS_KEPT")

        # Verify existing file preserved
        with open(existing_src_page, "r", encoding="utf-8") as fp:
            content = fp.read()
        self.assertIn("NIE NADPISYWAĆ!", content)

    def test_09_ingest_on_already_published_raw_note(self):
        # Note already published in raw/notes with status: new
        note_name = "publikacja_wczesniejsza.md"
        target_path = os.path.join(self.dest_dir, note_name)
        with open(target_path, "w", encoding="utf-8") as fp:
            fp.write("---\nsource: agents-os-core\nstatus: new\n---\n# Wcześniejsza Publikacja\nTreść notatki.")

        # Note also in source dir
        src_note = os.path.join(self.source_dir, note_name)
        with open(src_note, "w", encoding="utf-8") as fp:
            fp.write("# Wcześniejsza Publikacja\nTreść notatki.")

        # Running with ingest=True should detect raw note and perform ingest
        res = publish_knowledge_to_vault.publish_notes(self.source_dir, self.dest_dir, apply=True, ingest=True)
        self.assertEqual(len(res["skipped"]), 1)
        self.assertEqual(res["skipped"][0]["reason"], "IDENTICAL_CONTENT")
        self.assertEqual(len(res["ingested"]), 1)
        self.assertEqual(res["ingested"][0]["status"], "SCAFFOLDED")

        # Verify raw note now marked processed
        with open(target_path, "r", encoding="utf-8") as fp:
            content = fp.read()
        self.assertIn("status: processed", content)

if __name__ == "__main__":
    unittest.main()
