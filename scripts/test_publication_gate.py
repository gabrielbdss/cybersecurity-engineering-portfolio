#!/usr/bin/env python3
"""Regression tests using fictional fixture data in temporary directories."""
import tempfile
import unittest
from pathlib import Path
from publication_gate import inspect


class PublicationGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, rel, content):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_permitted_public_ctf_overview(self):
        self.write("case-studies/08-operation-cymbal-cold-room/README.md",
                   "18 / 18 accepted flags; no solution disclosed")
        self.assertEqual(inspect(self.root), [])

    def test_ctf_answer_document_blocked_by_allowlist(self):
        self.write("case-studies/08-operation-cymbal-cold-room/solutions.md",
                   "fictional test fixture")
        self.assertEqual(inspect(self.root)[0][1], "ctf-unapproved-file")

    def test_ctf_nested_file_blocked(self):
        self.write("case-studies/08-operation-cymbal-cold-room/extra/README.md", "test")
        self.assertTrue(inspect(self.root))

    def test_private_key_filename_blocked(self):
        self.write("keys/test.pem", "not a real credential")
        self.assertEqual(inspect(self.root)[0][1], "restricted-file-type")

    def test_env_filename_blocked(self):
        self.write(".env", "SYNTHETIC=true")
        self.assertEqual(inspect(self.root)[0][1], "restricted-file-type")

    def test_private_key_delimiter_blocked(self):
        header = "-----BEGIN " + "PRIVATE KEY-----"\n        self.write("notes.txt", header + "\\nplaceholder\\n")
        self.assertEqual(inspect(self.root)[0][1], "private-key-block")

    def test_git_dir_skipped(self):
        self.write(".git/example.pem", "not published")
        self.assertEqual(inspect(self.root), [])

    def test_benign_synthetic_workflow_is_accepted(self):
        self.write(".github/workflows/test.yml", "name: safe\non: push\n")
        self.assertEqual(inspect(self.root), [])


if __name__ == "__main__":
    unittest.main()
