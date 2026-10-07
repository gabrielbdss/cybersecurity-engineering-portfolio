# Lab 04 — Deterministic DevSecOps Merge Gate

**Type:** Synthetic CI/CD security laboratory  
**Safety:** No production repository or deployment  
**Goal:** Demonstrate a deterministic, fail-closed merge decision across multiple CI lanes.

## Scenario

A fictional repository has four validation lanes: build, security, deployment validation and quality. Some lanes may be explicitly non-applicable to a change. The merge gate must normalize their states and produce one predictable decision.

## Policy

Accepted terminal states:

- `PASS` — required lane completed successfully.
- `N/A` — policy explicitly determines that the lane does not apply.

Rejected states:

- `FAIL` — required lane failed.
- `UNKNOWN` — unexpected or unrecognized terminal state.
- `PENDING` after the bounded wait expires.

## Decision invariant

> A pull request cannot receive a successful merge-gate decision unless every applicable required lane reaches an explicitly acceptable terminal state.

## Test matrix

| Test | Build | Security | Deploy | Quality | Expected |
|---|---|---|---|---|---|
| Positive | PASS | PASS | PASS | PASS | PASS |
| Negative | PASS | FAIL | PASS | PASS | FAIL |
| Explicit N/A | PASS | PASS | N/A | PASS | PASS |
| Unknown | PASS | UNKNOWN | PASS | PASS | FAIL |
| Timeout | PASS | PENDING | PASS | PASS | FAIL |

## Local evaluator

The included Python script reads a synthetic JSON state file and exits with:

- `0` when the merge decision is PASS;
- `1` when the gate fails closed.

Run locally:

```bash
python3 gate.py evidence/positive.json
python3 gate.py evidence/negative.json
```

No network access, repository mutation or deployment occurs.

## Evidence objective

The useful evidence is not merely a green check. It is the combination of:

1. policy version;
2. normalized input states;
3. deterministic decision;
4. negative test proving failure behavior;
5. explicit handling of N/A and unknown states.

## Engineering lesson

A CI gate is a security control only when its applicability, terminal states and failure behavior are deterministic and testable.
