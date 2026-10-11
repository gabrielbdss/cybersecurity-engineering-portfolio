#!/usr/bin/env python3
"""Synthetic, local-only merge decision evaluator (not a GitHub merge policy)."""
import json
import sys
from pathlib import Path

POLICY_VERSION = "lab-v2"
REQUIRED_LANES = ("build", "security", "deploy", "quality")
VALID_STATES = frozenset({"PASS", "FAIL", "N/A", "PENDING", "UNKNOWN"})


def _valid_path(value):
    if not isinstance(value, str) or not value or value.startswith("/") or "\\" in value:
        return False
    return all(part not in ("", ".", "..") for part in value.split("/"))


def _docs_only(changed_files):
    return all(
        path in ("README.md", "README.pt-BR.md") or path.startswith("docs/")
        for path in changed_files
    )


def evaluate(document):
    """Return (accepted, reason); unknown or incomplete evidence always fails."""
    if not isinstance(document, dict):
        return False, "input must be a JSON object"
    if document.get("policy_version") != POLICY_VERSION:
        return False, "missing or unsupported policy_version"

    changed_files = document.get("changed_files")
    if (not isinstance(changed_files, list) or not changed_files
            or not all(_valid_path(path) for path in changed_files)):
        return False, "changed_files must contain valid relative paths"

    lanes = document.get("lanes")
    if not isinstance(lanes, dict):
        return False, "lanes must be a JSON object"

    expected = set(REQUIRED_LANES)
    actual = set(lanes)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing:
        return False, f"missing required lanes: {', '.join(missing)}"
    if unexpected:
        return False, f"unexpected lanes: {', '.join(unexpected)}"

    for name in REQUIRED_LANES:
        state = lanes[name]
        if not isinstance(state, str) or state not in VALID_STATES:
            return False, f"{name}: unrecognized state"
        if state == "N/A":
            # This is a narrow lab-only exception, not a proof of actual PR scope.
            if name != "deploy" or not _docs_only(changed_files):
                return False, f"{name}: N/A not allowed by lab policy"
        elif state != "PASS":
            # PENDING represents an unresolved final snapshot, not real polling.
            return False, f"{name}: {state}"
    return True, "every required lane has an acceptable policy state"


def main(argv):
    if len(argv) != 2:
        result = (False, "usage: gate.py <state.json>")
    else:
        try:
            with Path(argv[1]).open(encoding="utf-8") as stream:
                document = json.load(stream)
            result = evaluate(document)
        except (OSError, UnicodeError, json.JSONDecodeError):
            result = (False, "cannot read valid JSON input")

    accepted, reason = result
    print(json.dumps({"decision": "PASS" if accepted else "FAIL", "reason": reason}))
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
