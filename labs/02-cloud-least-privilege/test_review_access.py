import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
SCRIPT = ROOT / "review_access.py"
GRANTS = ROOT / "evidence" / "effective-access.json"
REQUIREMENTS = ROOT / "evidence" / "workload-requirements.json"


class AccessReviewTests(unittest.TestCase):
    def run_tool(self, grants, requirements):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--grants", str(grants),
             "--requirements", str(requirements)],
            text=True, capture_output=True, check=False
        )
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def test_reference_dataset(self):
        code, report = self.run_tool(GRANTS, REQUIREMENTS)
        self.assertEqual(code, 0)
        self.assertEqual(report["summary"], {
            "MATCHED_DECLARED_SCOPE": 1,
            "SCOPE_REVIEW_REQUIRED": 2,
            "NO_DEMONSTRATED_NEED": 2,
        })
        self.assertEqual(report["required_capabilities_without_grant"], [])
        excess = {
            item["capability"] for item in report["grants_review"]
            if item["classification"] == "NO_DEMONSTRATED_NEED"
        }
        self.assertEqual(excess, {"data.audit.delete", "crypto.keys.list"})

    def test_missing_grant_is_reported_without_automatic_change(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td) / "grants.json"
            data = json.loads(GRANTS.read_text())
            data["grants"] = [
                row for row in data["grants"] if row["capability"] != "crypto.sign"
            ]
            path.write_text(json.dumps(data), encoding="utf-8")
            code, report = self.run_tool(path, REQUIREMENTS)
            self.assertEqual(code, 0)
            self.assertIn(
                {"capability": "crypto.sign", "target": "key/audit-signing-key"},
                report["required_capabilities_without_grant"]
            )

    def test_duplicate_grant_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td) / "grants.json"
            data = json.loads(GRANTS.read_text())
            data["grants"].append(dict(data["grants"][0]))
            path.write_text(json.dumps(data), encoding="utf-8")
            code, report = self.run_tool(path, REQUIREMENTS)
            self.assertEqual(code, 2)
            self.assertIn("duplicate", report["error"])

    def test_incomplete_record_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td) / "requirements.json"
            data = json.loads(REQUIREMENTS.read_text())
            del data["required_operations"][0]["target"]
            path.write_text(json.dumps(data), encoding="utf-8")
            code, report = self.run_tool(GRANTS, path)
            self.assertEqual(code, 2)
            self.assertIn("invalid row", report["error"])

    def test_malformed_json_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td) / "grants.json"
            path.write_text("{invalid", encoding="utf-8")
            code, report = self.run_tool(path, REQUIREMENTS)
            self.assertEqual(code, 2)
            self.assertIn("error", report)

    def test_missing_file_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            code, report = self.run_tool(
                pathlib.Path(td) / "missing.json", REQUIREMENTS
            )
            self.assertEqual(code, 2)
            self.assertIn("error", report)

    def test_synthetic_scope_mismatch_not_called_effective_access(self):
        code, report = self.run_tool(GRANTS, REQUIREMENTS)
        self.assertEqual(code, 0)
        scoped = {
            item["capability"] for item in report["grants_review"]
            if item["classification"] == "SCOPE_REVIEW_REQUIRED"
        }
        self.assertEqual(scoped, {"data.audit.append", "crypto.sign"})
        self.assertIn("not proof", report["limitation"])


if __name__ == "__main__":
    unittest.main()
