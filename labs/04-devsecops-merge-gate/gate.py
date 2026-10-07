#!/usr/bin/env python3
import json
import sys

ACCEPTABLE = {"PASS", "N/A"}
KNOWN = {"PASS", "FAIL", "N/A", "PENDING", "UNKNOWN"}

def evaluate(document):
    lanes = document.get("lanes", {})
    if not lanes:
        return False, "no lanes supplied"
    for name, state in lanes.items():
        if state not in KNOWN:
            return False, f"{name}: unrecognized state"
        if state not in ACCEPTABLE:
            return False, f"{name}: {state}"
    return True, "all applicable lanes acceptable"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: gate.py <state.json>")
        raise SystemExit(2)
    with open(sys.argv[1], encoding="utf-8") as fh:
        doc = json.load(fh)
    passed, reason = evaluate(doc)
    print(json.dumps({"decision": "PASS" if passed else "FAIL", "reason": reason}))
    raise SystemExit(0 if passed else 1)
