import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
GATE = ROOT / "gate.py"
EVIDENCE = ROOT / "evidence"


class MergeGateTests(unittest.TestCase):
    def run_path(self, path):
        proc = subprocess.run(
            [sys.executable, str(GATE), str(path)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertFalse(proc.stderr, proc.stderr)
        return proc.returncode, json.loads(proc.stdout)

    def assert_decision(self, document, expected):
        with tempfile.TemporaryDirectory() as tempdir:
            path = pathlib.Path(tempdir) / "input.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            code, payload = self.run_path(path)
        self.assertEqual(code, 0 if expected == "PASS" else 1)
        self.assertEqual(payload["decision"], expected)

    def fixture(self, name):
        return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))

    def test_positive_passes(self):
        self.assert_decision(self.fixture("positive.json"), "PASS")

    def test_negative_fails_closed(self):
        self.assert_decision(self.fixture("negative.json"), "FAIL")

    def test_explicit_documentation_exception_passes(self):
        self.assert_decision(self.fixture("not-applicable.json"), "PASS")

    def test_unknown_fails_closed(self):
        self.assert_decision(self.fixture("unknown.json"), "FAIL")

    def test_pending_final_snapshot_fails_closed(self):
        document = self.fixture("positive.json")
        document["lanes"]["security"] = "PENDING"
        self.assert_decision(document, "FAIL")

    def test_missing_security_lane_fails_closed(self):
        document = self.fixture("positive.json")
        del document["lanes"]["security"]
        self.assert_decision(document, "FAIL")

    def test_only_build_lane_fails_closed(self):
        document = self.fixture("positive.json")
        document["lanes"] = {"build": "PASS"}
        self.assert_decision(document, "FAIL")

    def test_unexpected_lane_fails_closed(self):
        document = self.fixture("positive.json")
        document["lanes"]["extra"] = "PASS"
        self.assert_decision(document, "FAIL")

    def test_unsupported_policy_version_fails_closed(self):
        document = self.fixture("positive.json")
        document["policy_version"] = "lab-v1"
        self.assert_decision(document, "FAIL")

    def test_na_for_code_change_fails_closed(self):
        document = self.fixture("not-applicable.json")
        document["changed_files"] = ["src/service.py"]
        self.assert_decision(document, "FAIL")

    def test_security_na_even_for_docs_fails_closed(self):
        document = self.fixture("not-applicable.json")
        document["lanes"]["security"] = "N/A"
        self.assert_decision(document, "FAIL")

    def test_missing_changed_files_fails_closed(self):
        document = self.fixture("positive.json")
        del document["changed_files"]
        self.assert_decision(document, "FAIL")

    def test_traversal_path_fails_closed(self):
        document = self.fixture("not-applicable.json")
        document["changed_files"] = ["docs/../src/app.py"]
        self.assert_decision(document, "FAIL")

    def test_invalid_state_type_fails_closed(self):
        document = self.fixture("positive.json")
        document["lanes"]["security"] = ["PASS"]
        self.assert_decision(document, "FAIL")

    def test_non_object_document_fails_closed(self):
        self.assert_decision([], "FAIL")

    def test_malformed_json_fails_closed(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = pathlib.Path(tempdir) / "broken.json"
            path.write_text("{not-valid", encoding="utf-8")
            code, payload = self.run_path(path)
        self.assertEqual(code, 1)
        self.assertEqual(payload["decision"], "FAIL")

    def test_missing_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as tempdir:
            code, payload = self.run_path(pathlib.Path(tempdir) / "absent.json")
        self.assertEqual(code, 1)
        self.assertEqual(payload["decision"], "FAIL")


if __name__ == "__main__":
    unittest.main()
