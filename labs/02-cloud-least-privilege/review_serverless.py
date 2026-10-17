#!/usr/bin/env python3
"""Assess a fictional private Cloud Run service declaration; no cloud API calls."""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = frozenset({
    "service", "runtime_service_account", "ingress", "invokers",
    "invoker_iam_check_enabled",
})
SA_PATTERN = re.compile(r"^[a-z][a-z0-9-]*@[a-z][a-z0-9-]*\.iam\.gserviceaccount\.com$")
DEFAULT_COMPUTE_SA = re.compile(r"^[0-9]+-compute@developer\.gserviceaccount\.com$")


def assess(document):
    """Return a conservative verdict for this lab's *declared* private API policy."""
    if not isinstance(document, dict):
        return {"decision": "FAIL", "findings": ["expected a JSON object"]}
    if set(document) != FIELDS:
        return {"decision": "FAIL", "findings": ["missing or unexpected declaration fields"]}

    findings = []
    if not isinstance(document["service"], str) or not document["service"].strip():
        findings.append("service name missing or invalid")

    identity = document["runtime_service_account"]
    if not isinstance(identity, str) or not SA_PATTERN.fullmatch(identity):
        findings.append("runtime identity is not a declared user-managed service account")
    elif DEFAULT_COMPUTE_SA.fullmatch(identity):
        findings.append("default compute service account not permitted")

    if document["ingress"] != "internal":
        findings.append("private API policy requires internal ingress")

    if document["invoker_iam_check_enabled"] is not True:
        findings.append("invoker IAM authorization must be enabled")

    invokers = document["invokers"]
    if (not isinstance(invokers, list) or not invokers
            or not all(isinstance(m, str) for m in invokers)):
        findings.append("invoker declaration missing or invalid")
    elif len(set(invokers)) != len(invokers):
        findings.append("duplicate invoker declaration")
    elif any(not member.startswith("serviceAccount:")
             or not SA_PATTERN.fullmatch(member.removeprefix("serviceAccount:"))
             for member in invokers):
        findings.append("only named service-account invokers are permitted")

    return {"decision": "FAIL" if findings else "PASS", "findings": findings,
            "scope": "synthetic declaration only; not deployed IAM or runtime behavior"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path,
                        default=HERE / "evidence" / "private-service.json")
    args = parser.parse_args()
    try:
        with args.config.open(encoding="utf-8") as stream:
            document = json.load(stream)
        result = assess(document)
    except (OSError, UnicodeError, ValueError, TypeError):
        result = {"decision": "FAIL", "findings": ["invalid or unavailable JSON declaration"]}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
