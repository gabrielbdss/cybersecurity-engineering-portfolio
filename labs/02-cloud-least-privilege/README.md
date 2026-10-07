# Lab 02 — Cloud Least-Privilege Review

**Type:** Synthetic laboratory  
**Safety:** Local analysis only  
**Goal:** Review effective workload permissions and propose the smallest defensible access reduction without breaking required behavior.

## Scenario

A fictional serverless workload uses a runtime identity to read application data, append audit records and invoke a cryptographic signing operation. The supplied policy intentionally grants broader scope than the documented workload requirements.

All resources, identities and permissions are synthetic.

## Evidence

- `evidence/effective-access.json` — synthetic effective permissions.
- `evidence/workload-requirements.json` — operations the fictional workload is expected to perform.
- `expected/remediation-plan.md` — reference analysis.

## Questions

1. Which granted capabilities have a demonstrated workload requirement?
2. Which capabilities exceed that requirement?
3. Is broad scope alone sufficient to call something exploitable?
4. What should be reduced first?
5. What must be tested before an authorized change?

## Method

Compare **effective capability** with **demonstrated need**. Do not infer necessity from a role name and do not infer exploitability merely from excess permission.

A defensible recommendation contains:

```text
Current capability:
Demonstrated requirement:
Gap:
Risk:
Target capability:
Validation:
Rollback:
Evidence state:
```

## Success criteria

The analyst should identify the synthetic delete capability and project-wide cryptographic scope as reduction candidates while preserving required read, append and signing behavior.

The lab ends with a **remediation plan**, not a production mutation.
