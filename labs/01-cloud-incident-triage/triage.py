#!/usr/bin/env python3
"""Correlate fictional security telemetry locally; never contact a cloud API."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def timestamp_utc(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid ISO-8601 timestamp") from exc
    if stamp.utcoffset() is None:
        raise ValueError("timestamp must include UTC offset")
    return stamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def load_jsonl(path):
    records = []
    with path.open(encoding="utf-8") as stream:
        for lineno, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name}:{lineno}: invalid JSON") from exc
            if not isinstance(item, dict):
                raise ValueError(f"{path.name}:{lineno}: expected JSON object")
            item = dict(item)
            try:
                item["timestamp"] = timestamp_utc(item.get("timestamp"))
            except ValueError as exc:
                raise ValueError(f"{path.name}:{lineno}: {exc}") from exc
            records.append(item)
    return records


def analyze(directory):
    sources = {
        "request": load_jsonl(directory / "requests.jsonl"),
        "application": load_jsonl(directory / "application.jsonl"),
        "audit": load_jsonl(directory / "audit.jsonl"),
    }
    if not sources["request"]:
        raise ValueError("request evidence is empty")

    by_request = defaultdict(list)
    timeline = []
    for source, records in sources.items():
        for record in records:
            request_id = record.get("request_id")
            if source != "audit" and (not isinstance(request_id, str) or not request_id):
                raise ValueError(f"{source}: request_id is required")
            if source == "application":
                if not isinstance(record.get("event"), str):
                    raise ValueError("application: event must be a string")
                by_request[request_id].append(record)
            if source == "request":
                status = record.get("status")
                if isinstance(status, bool) or not isinstance(status, int):
                    raise ValueError("request: status must be an integer")
                description = f"HTTP {status}"
            elif source == "application":
                description = record["event"]
            else:
                description = record.get("action")
                if not isinstance(description, str):
                    raise ValueError("audit: action must be a string")
            timeline.append({
                "timestamp": record["timestamp"],
                "source": source,
                "request_id": request_id if source != "audit" else None,
                "event": description,
            })

    timeline.sort(key=lambda item: (item["timestamp"], item["source"], item["event"]))
    denied = []
    for request in sources["request"]:
        if request["status"] == 403:
            matching = any(
                item["event"] == "AUTHORIZATION_DENIED"
                for item in by_request[request["request_id"]]
            )
            denied.append({
                "request_id": request["request_id"],
                "timestamp": request["timestamp"],
                "http_status": 403,
                "application_denial_correlated": matching,
                "classification": "OBSERVED",
            })

    return {
        "data_type": "synthetic_laboratory",
        "request_count": len(sources["request"]),
        "denied_requests": denied,
        "audit_actions_in_sample": sorted({
            item["action"] for item in sources["audit"]
        }),
        "hypotheses_not_established": {
            "credential_compromise": "UNVERIFIED",
            "privilege_escalation": "UNVERIFIED",
            "data_exfiltration": "UNVERIFIED",
        },
        "limitation": (
            "Observed status codes and application events do not prove attacker "
            "intent, credential compromise, absence of side effects, or safety "
            "outside the supplied synthetic time window."
        ),
        "timeline": timeline,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--evidence-dir", type=Path, default=ROOT / "evidence",
        help="Directory containing the three local JSONL fixtures"
    )
    args = parser.parse_args()
    try:
        report = analyze(args.evidence_dir)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
