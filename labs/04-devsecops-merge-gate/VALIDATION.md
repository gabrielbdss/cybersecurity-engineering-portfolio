# Lab 04 — Validation Record

**Policy:** `lab-v2`
**Scope:** local synthetic evaluator, not a production CI/CD protection claim.

## Regression coverage

| Scenario | Expected |
|---|---|
| Required lanes all PASS | PASS |
| Security lane FAIL | FAIL |
| Explicit deploy N/A for documentation-only changes | PASS |
| UNKNOWN state | FAIL |
| Unresolved PENDING snapshot | FAIL |
| Missing security lane | FAIL |
| Only build lane supplied | FAIL |
| Unexpected extra lane | FAIL |
| Unsupported policy version | FAIL |
| Deploy N/A for code change | FAIL |
| Security N/A even for documentation changes | FAIL |
| Missing changed-files metadata | FAIL |
| Path traversal | FAIL |
| Invalid state type | FAIL |
| Non-object input | FAIL |
| Malformed JSON | FAIL |
| Missing input file | FAIL |

## Reproduce

```bash
cd labs/04-devsecops-merge-gate
python3 -m unittest -v test_gate.py
```

The suite should run **17 tests**. The repository workflow executes the suite on pushes and pull requests, as well as the four named fixture decisions.

The evaluator accepts only the narrow, explicitly coded documentation exception. Its `changed_files` field is synthetic test input; it is **not cryptographically or independently verified** and must not be trusted for authorization in a live merge decision. This lab does not implement polling, GitHub rulesets or branch protection.
