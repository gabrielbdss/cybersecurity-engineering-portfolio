#!/usr/bin/env python3
"""Compare fictional declared grants with workload needs, without changing IAM."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_object(path):
    with path.open(encoding="utf-8") as stream:
        document = json.load(stream)
    if not isinstance(document, dict):
        raise ValueError(f"{path.name}: expected JSON object")
    return document


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def validate_rows(rows, fields, label):
    if not isinstance(rows, list):
        raise ValueError(f"{label}: expected list")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or any(
            not nonblank(row.get(field)) for field in fields
        ):
            raise ValueError(f"{label}: missing or invalid row fields")
        key = (row["capability"], row[fields[1]])
        if key in seen:
            raise ValueError(f"{label}: duplicate capability and scope/target")
        seen.add(key)


def assess(grants_doc, requirements_doc):
    if not nonblank(grants_doc.get("identity")):
        raise ValueError("identity is required")
    if not nonblank(requirements_doc.get("workload")):
        raise ValueError("workload is required")
    grants = grants_doc.get("grants")
    required = requirements_doc.get("required_operations")
    validate_rows(grants, ("capability", "scope"), "grants")
    validate_rows(required, ("capability", "target", "reason"), "required_operations")

    by_capability = {}
    for entry in required:
        by_capability.setdefault(entry["capability"], set()).add(entry["target"])

    findings = []
    for entry in sorted(grants, key=lambda row: (row["capability"], row["scope"])):
        targets = by_capability.get(entry["capability"])
        if not targets:
            classification = "NO_DEMONSTRATED_NEED"
        elif entry["scope"] not in targets:
            classification = "SCOPE_REVIEW_REQUIRED"
        else:
            classification = "MATCHED_DECLARED_SCOPE"
        findings.append({
            "capability": entry["capability"],
            "granted_scope": entry["scope"],
            "required_targets": sorted(targets or ()),
            "classification": classification,
        })

    granted_caps = {entry["capability"] for entry in grants}
    missing = [
        {"capability": entry["capability"], "target": entry["target"]}
        for entry in required if entry["capability"] not in granted_caps
    ]
    counts = {
        classification: sum(
            finding["classification"] == classification for finding in findings
        )
        for classification in (
            "MATCHED_DECLARED_SCOPE",
            "SCOPE_REVIEW_REQUIRED",
            "NO_DEMONSTRATED_NEED",
        )
    }
    return {
        "data_type": "synthetic_laboratory",
        "identity": grants_doc["identity"],
        "workload": requirements_doc["workload"],
        "summary": counts,
        "grants_review": findings,
        "required_capabilities_without_grant": missing,
        "limitation": (
            "Declared scope string mismatch is a review candidate, not proof "
            "of an effective privilege or valid permission inheritance. "
            "This is not a cloud IAM evaluation and changes no policies."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--grants", type=Path, default=ROOT / "evidence" / "effective-access.json"
    )
    parser.add_argument(
        "--requirements", type=Path,
        default=ROOT / "evidence" / "workload-requirements.json"
    )
    args = parser.parse_args()
    try:
        report = assess(load_object(args.grants), load_object(args.requirements))
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
