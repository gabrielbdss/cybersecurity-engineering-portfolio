# Lab 04 — Deterministic DevSecOps Merge Gate

**Type:** Synthetic CI/CD security laboratory
**Safety:** Local-only evaluation; no repository mutation or production deployment
**Goal:** Demonstrate a strict, fail-closed decision across required validation lanes.

## Policy `lab-v2`

The local evaluator requires an explicit `policy_version` of `lab-v2`, a non-empty `changed_files` list of valid relative paths, and **exactly four lanes**: `build`, `security`, `deploy` and `quality`.

Every required lane must be present. Missing, unknown, unexpected, malformed or unresolved lanes result in **FAIL**.

| State | Meaning | Decision |
|---|---|---|
| `PASS` | Required check succeeded | Accepted |
| `FAIL` | Required check failed | Rejected |
| `UNKNOWN` | Unrecognized/unknown state | Rejected |
| `PENDING` | Incomplete final snapshot | Rejected |
| `N/A` | Explicit synthetic policy exception | Only allowed for `deploy` on documentation-only changes |

Documentation-only means that every declared changed path is `README.md`, `README.pt-BR.md`, or under `docs/`. The `build`, `security` and `quality` lanes cannot be exempted by this laboratory policy. Paths containing traversal components are rejected.

## Reproduce

Run commands from this lab directory:

```bash
python3 gate.py evidence/positive.json           # PASS, exit 0
python3 gate.py evidence/negative.json           # FAIL, exit 1
python3 gate.py evidence/not-applicable.json     # PASS, exit 0
python3 gate.py evidence/unknown.json            # FAIL, exit 1
python3 -m unittest -v test_gate.py
```

The suite contains **17 tests**, including malformed input, incomplete lane sets, invalid exceptions, unsupported policy versions and unresolved states.

## Scope and limitations

This program is a **local deterministic evaluator**, not an end-to-end GitHub branch protection implementation. It does not fetch trusted PR changes, verify hosted job identities, authorize an exemption based on trusted GitHub metadata, or implement bounded polling. `PENDING` is rejected as an unresolved final snapshot. A real integration would need trusted workflow data, branch rules requiring the check, and end-to-end negative merge tests.

See [VALIDATION.md](VALIDATION.md) for the regression matrix and the repository workflow for hosted test evidence.
