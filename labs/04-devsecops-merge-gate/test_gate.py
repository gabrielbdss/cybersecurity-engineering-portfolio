import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
GATE = ROOT / "gate.py"
EVIDENCE = ROOT / "evidence"

class MergeGateTests(unittest.TestCase):
    def run_fixture(self, name):
        proc = subprocess.run(
            [sys.executable, str(GATE), str(EVIDENCE / name)],
            text=True,
            capture_output=True,
            check=False,
        )
        payload = json.loads(proc.stdout)
        return proc.returncode, payload

    def test_positive_passes(self):
        code, payload = self.run_fixture("positive.json")
        self.assertEqual(code, 0)
        self.assertEqual(payload["decision"], "PASS")

    def test_negative_fails_closed(self):
        code, payload = self.run_fixture("negative.json")
        self.assertEqual(code, 1)
        self.assertEqual(payload["decision"], "FAIL")

    def test_explicit_na_passes(self):
        code, payload = self.run_fixture("not-applicable.json")
        self.assertEqual(code, 0)
        self.assertEqual(payload["decision"], "PASS")

    def test_unknown_fails_closed(self):
        code, payload = self.run_fixture("unknown.json")
        self.assertEqual(code, 1)
        self.assertEqual(payload["decision"], "FAIL")

if __name__ == "__main__":
    unittest.main()
