"""Security regression tests for a fictional private serverless API declaration."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from review_serverless import assess

HERE = Path(__file__).resolve().parent


class ServerlessBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.good = json.loads((HERE / "evidence" / "private-service.json").read_text())

    def mutate(self, field, value):
        doc = copy.deepcopy(self.good)
        doc[field] = value
        return doc

    def test_private_service_passes(self):
        self.assertEqual(assess(self.good)["decision"], "PASS")

    def test_public_ingress_fails(self):
        self.assertEqual(assess(self.mutate("ingress", "all"))["decision"], "FAIL")

    def test_missing_invoker_iam_check_fails(self):
        self.assertEqual(assess(self.mutate("invoker_iam_check_enabled", False))["decision"], "FAIL")

    def test_anonymous_invoker_fails(self):
        self.assertEqual(assess(self.mutate("invokers", ["allUsers"]))["decision"], "FAIL")

    def test_all_authenticated_invoker_fails(self):
        self.assertEqual(assess(self.mutate("invokers", ["allAuthenticatedUsers"]))["decision"], "FAIL")

    def test_default_identity_fails(self):
        self.assertEqual(assess(self.mutate("runtime_service_account", "123456789-compute@developer.gserviceaccount.com"))["decision"], "FAIL")

    def test_missing_field_fails_closed(self):
        doc = copy.deepcopy(self.good)
        del doc["ingress"]
        self.assertEqual(assess(doc)["decision"], "FAIL")

    def test_invalid_invokers_type_fails_closed(self):
        self.assertEqual(assess(self.mutate("invokers", "serviceAccount:anything"))["decision"], "FAIL")

    def test_unexpected_input_fails_closed(self):
        self.assertEqual(assess({**self.good, "admin_override": True})["decision"], "FAIL")

    def test_invalid_root_fails_closed(self):
        self.assertEqual(assess([])["decision"], "FAIL")

    def test_cli_exit_codes(self):
        script = HERE / "review_serverless.py"
        ok = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stderr)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text(json.dumps(self.mutate("ingress", "all")), encoding="utf-8")
            denied = subprocess.run([sys.executable, str(script), "--config", str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(denied.returncode, 1, denied.stderr)
            self.assertEqual(json.loads(denied.stdout)["decision"], "FAIL")


if __name__ == "__main__":
    unittest.main()
