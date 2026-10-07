# Lab 01 — Evidence-Driven Cloud Incident Triage

**Type:** Synthetic laboratory  
**Safety:** Local/read-only analysis only  
**Goal:** Turn raw telemetry into defensible security conclusions without assuming that an unusual event is an attack.

## Scenario

A fictional serverless API emits an unusual request followed by an authorization failure and an application error. The analyst must correlate three synthetic evidence sources:

- request telemetry;
- application events;
- control-plane audit events.

No production system is contacted and no real organization is represented.

## Files

```text
lab/
├── evidence/
│   ├── requests.jsonl
│   ├── application.jsonl
│   └── audit.jsonl
├── expected/
│   └── analyst-notes.md
└── README.md
```

## Investigation questions

1. What event initiated the investigation?
2. Which facts are directly observed?
3. Is unauthorized access demonstrated?
4. Is credential compromise demonstrated?
5. Is privilege escalation demonstrated in the supplied window?
6. What additional evidence would be required before containment?

## Procedure

The exercise can be completed manually with any JSON-capable editor or command-line tooling.

Example local inspection:

```bash
cat evidence/requests.jsonl
cat evidence/application.jsonl
cat evidence/audit.jsonl
```

These commands operate only on the synthetic files in this repository.

Build a timeline using `timestamp`, then correlate records using `request_id`. Do not treat a shared identifier as proof of malicious intent; it establishes event correlation only.

## Expected reasoning standard

For every conclusion, record:

```text
Claim:
Evidence:
State: OBSERVED | VERIFIED | INFERRED | UNVERIFIED
Limitation:
Next safe action:
```

Compare your result with [expected/analyst-notes.md](expected/analyst-notes.md) only after completing the exercise.

## Success criteria

The lab is successful when the analyst can distinguish:

- an unusual request from a confirmed attack;
- an authorization failure from successful unauthorized access;
- absence of evidence in a bounded window from proof that an event never occurred;
- a containment hypothesis from an authorized containment decision.

## Safety note

All identities, IP addresses, resource names, timestamps and events in this lab are fictional or documentation-reserved examples.
