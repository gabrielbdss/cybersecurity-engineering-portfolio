# Engineering Evidence Map

**Scope:** public, independently inspectable portfolio artifacts. This index describes what the source and public CI demonstrate; it is not a claim about private infrastructure.

| Engineering focus | Executable evidence | What it establishes | Material limit |
| --- | --- | --- | --- |
| Cloud Security | [Least-privilege review](../labs/02-cloud-least-privilege/README.md), [private serverless declaration validator](../labs/02-cloud-least-privilege/review_serverless.py) and [negative tests](../labs/02-cloud-least-privilege/test_review_serverless.py) | Deterministic review of fictional permissions and a declared internal-only API policy | Not effective GCP IAM, Workload Identity Federation or a deployed Cloud Run evaluation |
| Incident Response | [Event correlation CLI](../labs/01-cloud-incident-triage/README.md) and [regression suite](../labs/01-cloud-incident-triage/test_triage.py) | Correlates fictional request and application events with a bounded window | Does not prove compromise or recovery in a live incident |
| DevSecOps | [Fail-closed merge evaluator](../labs/04-devsecops-merge-gate/README.md), [branch-protection experiment](../case-studies/03-devsecops-merge-gate/BRANCH_PROTECTION_VALIDATION.md), and [portfolio CI](../.github/workflows/portfolio-ci.yml) | Local decision tests and an independently visible intentionally blocked PR | Local gate is not a production GitHub rules engine; secret-scanning effectiveness and CI behavior require separate run evidence |
| AI Security | [AI Action Boundary lab](../labs/03-ai-tool-authorization/README.md), [threat model](../labs/03-ai-tool-authorization/THREAT_MODEL.md), [F-01 verification](../labs/03-ai-tool-authorization/evidence/F01_VERIFICATION.md) | In-memory tool authorization boundary, denial, replay and concurrency under specified tests | No real model integration, identity provider, multi-process durability or external independent sign-off |
| Security Governance | [Evidence-first method](../methodology/evidence-first-production-safe.md), [publication policy](../SECURITY.md), [incident response tabletop](../case-studies/05-incident-response-playbook/TABLETOP_EXERCISE.md) | Scope, decision authority, limits and synthetic response decisions are documented | Documentation alone does not prove operational readiness |

## Reviewer checklist

1. Choose the artifact and reproduce its local test command.
2. Confirm the exact workflow run, job result and commit.
3. Inspect one negative result and one positive result.
4. Differentiate **verified behavior** from **documented design**.
5. Inspect stated assumptions, residual risks and confidentiality limits.

**Status note:** Newly proposed controls on a feature branch remain **PENDING HOSTED VALIDATION** until CI jobs execute and a reviewer verifies the results. Do not call this work merged or production-proven prematurely.
