# Lab 02 — Cloud Least-Privilege Review

**Type:** Synthetic laboratory
**Safety:** Local/read-only analysis; never modifies IAM
**Goal:** Compare fictional grant declarations with workload requirements.

## Inputs

- \`evidence/effective-access.json\` — **synthetic declared grant inventory**, not an actual effective IAM computation
- \`evidence/workload-requirements.json\` — fictional required capabilities and target resources

## Reproduce

From the repository root:

\`\`\`bash
python3 labs/02-cloud-least-privilege/review_access.py
python3 -m unittest discover -s labs/02-cloud-least-privilege -p "test_*.py" -v
\`\`\`

The script outputs a JSON report and returns exit code \`0\` for successfully assessed fixtures or \`2\` for malformed or missing evidence. There are no external packages or cloud API requests.

## Classification

| State | Meaning |
|---|---|
| \`MATCHED_DECLARED_SCOPE\` | A matching capability and identical scope string appears in the declared needs |
| \`SCOPE_REVIEW_REQUIRED\` | Capability is required, but grant scope does not match any declared target exactly |
| \`NO_DEMONSTRATED_NEED\` | A granted capability has no matching declared requirement |

A separate list describes required capabilities with no supplied grant. The synthetic fixture is expected to find **1 scope match**, **2 scope-review candidates** and **2 grants with no demonstrated requirement**.

**Important:** Scope-string differences are not a calculation of actual cloud permissions or evidence of exploitability. A real assessment would evaluate resource ancestry, binding scope, conditional and deny policies, identity context and verified workload behavior. Do not change IAM based on this exercise.

Seven automated tests cover the expected classifications, missing grants, duplicate grants, malformed input and incomplete requirements.

See [expected/remediation-plan.md](expected/remediation-plan.md) for reference recommendations and rollback considerations.
