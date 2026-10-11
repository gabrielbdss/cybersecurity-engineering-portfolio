import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
SCRIPT = ROOT / "triage.py"
EVIDENCE = ROOT / "evidence"
NAMES = ("requests.jsonl", "application.jsonl", "audit.jsonl")


class TriageTests(unittest.TestCase):
    def run_tool(self, directory):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--evidence-dir", str(directory)],
            text=True, capture_output=True, check=False
        )
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def copy_data(self, directory):
        for name in NAMES:
            (directory / name).write_text(
                (EVIDENCE / name).read_text(encoding="utf-8"), encoding="utf-8"
            )

    def test_synthetic_fixture_reports_denial_without_claiming_compromise(self):
        code, report = self.run_tool(EVIDENCE)
        self.assertEqual(code, 0)
        self.assertEqual(report["data_type"], "synthetic_laboratory")
        self.assertEqual(report["request_count"], 2)
        self.assertEqual(len(report["denied_requests"]), 1)
        self.assertEqual(report["denied_requests"][0]["http_status"], 403)
        self.assertTrue(report["denied_requests"][0]["application_denial_correlated"])
        self.assertTrue(all(
            state == "UNVERIFIED" for state in report["hypotheses_not_established"].values()
        ))

    def test_sorted_timeline_has_all_events(self):
        code, report = self.run_tool(EVIDENCE)
        self.assertEqual(code, 0)
        self.assertEqual(len(report["timeline"]), 7)
        self.assertEqual(
            [item["timestamp"] for item in report["timeline"]],
            sorted(item["timestamp"] for item in report["timeline"])
        )

    def test_http_denial_without_app_event_is_not_claimed_correlated(self):
        with tempfile.TemporaryDirectory() as td:
            directory = pathlib.Path(td)
            self.copy_data(directory)
            (directory / "application.jsonl").write_text("", encoding="utf-8")
            code, report = self.run_tool(directory)
            self.assertEqual(code, 0)
            self.assertFalse(report["denied_requests"][0]["application_denial_correlated"])

    def test_absent_evidence_fails(self):
        with tempfile.TemporaryDirectory() as td:
            code, report = self.run_tool(pathlib.Path(td))
            self.assertEqual(code, 2)
            self.assertIn("error", report)

    def test_malformed_json_fails(self):
        with tempfile.TemporaryDirectory() as td:
            directory = pathlib.Path(td)
            self.copy_data(directory)
            (directory / "requests.jsonl").write_text("{invalid", encoding="utf-8")
            code, report = self.run_tool(directory)
            self.assertEqual(code, 2)
            self.assertIn("invalid JSON", report["error"])

    def test_timestamp_missing_timezone_fails(self):
        with tempfile.TemporaryDirectory() as td:
            directory = pathlib.Path(td)
            self.copy_data(directory)
            request = json.loads((directory / "requests.jsonl").read_text().splitlines()[0])
            request["timestamp"] = "2030-01-15T14:02:11"
            (directory / "requests.jsonl").write_text(
                json.dumps(request) + "\n", encoding="utf-8"
            )
            code, report = self.run_tool(directory)
            self.assertEqual(code, 2)
            self.assertIn("UTC offset", report["error"])

    def test_unusual_200_request_does_not_become_denial(self):
        with tempfile.TemporaryDirectory() as td:
            directory = pathlib.Path(td)
            self.copy_data(directory)
            request = json.loads((directory / "requests.jsonl").read_text().splitlines()[0])
            request["status"] = 200
            (directory / "requests.jsonl").write_text(
                json.dumps(request) + "\n", encoding="utf-8"
            )
            code, report = self.run_tool(directory)
            self.assertEqual(code, 0)
            self.assertEqual(report["denied_requests"], [])


    def test_stale_denial_is_not_correlated(self):
        with tempfile.TemporaryDirectory() as td:
            directory = pathlib.Path(td)
            self.copy_data(directory)
            path = directory / "application.jsonl"
            records = [json.loads(row) for row in path.read_text().splitlines()]
            records[0]["timestamp"] = "2030-01-15T14:08:00Z"
            path.write_text("\n".join(json.dumps(row) for row in records) + "\n")
            code, report = self.run_tool(directory)
            self.assertEqual(code, 0)
            self.assertFalse(report["denied_requests"][0]["application_denial_correlated"])

    def test_early_denial_is_not_correlated(self):
        with tempfile.TemporaryDirectory() as td:
            directory = pathlib.Path(td)
            self.copy_data(directory)
            path = directory / "application.jsonl"
            records = [json.loads(row) for row in path.read_text().splitlines()]
            records[0]["timestamp"] = "2030-01-15T13:59:00Z"
            path.write_text("\n".join(json.dumps(row) for row in records) + "\n")
            code, report = self.run_tool(directory)
            self.assertEqual(code, 0)
            self.assertFalse(report["denied_requests"][0]["application_denial_correlated"])

    def test_duplicate_request_id_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            directory = pathlib.Path(td)
            self.copy_data(directory)
            path = directory / "requests.jsonl"
            original = path.read_text()
            path.write_text(original + original.splitlines()[0] + "\n")
            code, report = self.run_tool(directory)
            self.assertEqual(code, 2)
            self.assertIn("duplicate request_id", report["error"])

    def test_invalid_status_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            directory = pathlib.Path(td)
            self.copy_data(directory)
            path = directory / "requests.jsonl"
            records = [json.loads(row) for row in path.read_text().splitlines()]
            records[0]["status"] = 999
            path.write_text("\n".join(json.dumps(row) for row in records) + "\n")
            code, report = self.run_tool(directory)
            self.assertEqual(code, 2)
            self.assertIn("valid HTTP integer", report["error"])

    def test_orphan_application_event_is_not_misattributed(self):
        with tempfile.TemporaryDirectory() as td:
            directory = pathlib.Path(td)
            self.copy_data(directory)
            path = directory / "application.jsonl"
            extra = {"timestamp": "2030-01-15T14:09:00Z",
                     "request_id": "orphan-0001", "event": "AUTHORIZATION_DENIED"}
            path.write_text(path.read_text() + json.dumps(extra) + "\n")
            code, report = self.run_tool(directory)
            self.assertEqual(code, 0)
            self.assertEqual(report["orphan_application_request_ids"], ["orphan-0001"])

    def test_audit_causal_linkage_remains_unestablished(self):
        code, report = self.run_tool(EVIDENCE)
        self.assertEqual(code, 0)
        self.assertEqual(report["audit_request_correlation"], "NOT_ESTABLISHED")
        self.assertEqual(report["correlation_window_seconds"], 120)
        self.assertEqual(report["source_counts"],
                         {"request": 2, "application": 3, "audit": 2})

    def test_offset_normalizes_and_correlates(self):
        with tempfile.TemporaryDirectory() as td:
            directory = pathlib.Path(td)
            self.copy_data(directory)
            path = directory / "requests.jsonl"
            records = [json.loads(row) for row in path.read_text().splitlines()]
            records[0]["timestamp"] = "2030-01-15T11:02:11-03:00"
            path.write_text("\n".join(json.dumps(row) for row in records) + "\n")
            code, report = self.run_tool(directory)
            self.assertEqual(code, 0)
            self.assertTrue(report["denied_requests"][0]["application_denial_correlated"])
            self.assertEqual(report["denied_requests"][0]["timestamp"],
                             "2030-01-15T14:02:11Z")

if __name__ == "__main__":
    unittest.main()
