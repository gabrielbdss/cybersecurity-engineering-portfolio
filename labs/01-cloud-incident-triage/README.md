# Lab 01 — Evidence-Driven Cloud Incident Triage

**Type:** Synthetic laboratory
**Safety:** Local/read-only analysis only
**Goal:** Correlate request, application and audit telemetry without assuming an attack.

## Inputs

The fictional serverless API evidence is held in the existing local files:

- `evidence/requests.jsonl` — synthetic HTTP request telemetry
- `evidence/application.jsonl` — synthetic application events
- `evidence/audit.jsonl` — synthetic control-plane read events

All identities, timestamps, addresses and resource labels are fictional or documentation examples; no real project is queried. **No employer production architecture is represented.**

## Reproduce

From the repository root:

```bash
python3 labs/01-cloud-incident-triage/triage.py
python3 -m unittest discover -s labs/01-cloud-incident-triage -p "test_*.py" -v
```

The script prints a machine-readable JSON report and returns exit code `0` on valid evidence and `2` on malformed, missing or invalid evidence. It uses only Python's standard library.

## Observed and unverified claims

The report constructs a timestamp-sorted timeline, correlates HTTP 403 with an application authorization-denial event only when the same request ID exists and the event is within the synthetic time window, and enumerates sampled audit action names.

The presence of an HTTP 403 and a correlated denial is **observed**. Compromised credentials, privilege escalation and data exfiltration remain **UNVERIFIED**. The tool does not infer malicious intent or absence of activity outside the narrow supplied dataset.

The 14 regression tests cover fixture correlation, chronology, non-correlated and time-shifted authorization denials, malformed JSON, timezone validation, duplicate IDs, invalid HTTP statuses, orphan application events and explicit non-correlation of audit events. Correlation in this synthetic lab requires a shared request ID and an event within 120 seconds after the HTTP 403; this does not prove causality in a live environment.

Review [expected/analyst-notes.md](expected/analyst-notes.md) for a human analyst's interpretation.
