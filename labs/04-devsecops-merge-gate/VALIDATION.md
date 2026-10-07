# Lab 04 — Validation Record

The evaluator is designed for local deterministic testing.

| Fixture | Expected decision | Security property |
|---|---|---|
| `positive.json` | PASS | all required lanes acceptable |
| `negative.json` | FAIL | downstream failure closes gate |
| `not-applicable.json` | PASS | N/A must be explicit policy state |
| `unknown.json` | FAIL | unexpected state is not silently accepted |

## Reproduce

```bash
python3 gate.py evidence/positive.json
echo $?

python3 gate.py evidence/negative.json
echo $?

python3 gate.py evidence/not-applicable.json
echo $?

python3 gate.py evidence/unknown.json
echo $?
```

Expected exit codes: `0, 1, 0, 1`.

This validation record describes the intended deterministic behavior of the included local evaluator. It does not represent a production CI/CD control.
