# Engineering Evidence Map

**Scope:** public, independently inspectable portfolio artifacts. This index describes what the source and public CI demonstrate; it is not a claim about private infrastructure.

| Engineering focus | Executable evidence | What it establishes | Material limit |
| --- | --- | --- | --- |
| Cloud Security | [Least-privilege review](../labs/02-cloud-least-privilege/README.md), [private serverless declaration validator](../labs/02-cloud-least-privilege/review_serverless.py) and [negative tests](../labs/02-cloud-least-privilege/test_review_serverless.py) | Deterministic review of fictional permissions and a declared internal-only API policy | Not effective GCP IAM, Workload Identity Federation or a deployed Cloud Run evaluation |
| Incident Response | [Event correlation CLI](../labs/01-cloud-incident-triage/README.md) and [regression suite](../labs/01-cloud-incident-triage/test_triage.py) | Correlates fictional request and application events with a bounded window | Does not prove compromise or recovery in a live incident |
| DevSecOps | [Fail-closed merge evaluator](../labs/04-devsecops-merge-gate/README.md), [branch-protection experiment](../case-studies/03-devsecops-merge-gate/BRANCH_PROTECTION_VALIDATION.md), and [portfolio CI](../.github/workflows/portfolio-ci.yml) | Local decision tests and an independently visible intentionally blocked PR | Local gate is not a production GitHub rules engine; Gitleaks custom canary regression proves detection, not every real-world secret pattern |
| AI Security | [AI Action Boundary lab](../labs/03-ai-tool-authorization/README.md), [threat model](../labs/03-ai-tool-authorization/THREAT_MODEL.md), [F-01 verification](../labs/03-ai-tool-authorization/evidence/F01_VERIFICATION.md) | In-memory tool authorization boundary, denial, replay and concurrency under specified tests | No real model integration, identity provider, multi-process durability or external independent sign-off |
| Security Governance | [Evidence-first method](../methodology/evidence-first-production-safe.md), [publication policy](../SECURITY.md), [incident response tabletop](../case-studies/05-incident-response-playbook/TABLETOP_EXERCISE.md) | Scope, decision authority, limits and synthetic response decisions are documented | Documentation alone does not prove operational readiness |

## Reviewer checklist

1. Choose the artifact and reproduce its local test command.
2. Confirm the exact workflow run, job result and commit.
3. Inspect one negative result and one positive result.
4. Differentiate **verified behavior** from **documented design**.
5. Inspect stated assumptions, residual risks and confidentiality limits.

## Hosted CI evidence

- **Positive (feature PR):** [PR #11](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/pull/11), [CI run 39048976337](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/actions/runs/39048976337): three jobs pass, including Gitleaks; test counts are recorded in the run logs.
- **Negative (throwaway PR):** [PR #12](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/pull/12), [CI run 39050826675](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/actions/runs/39050826675): a **custom Gitleaks rule** detects an entirely fictional test marker and the required `Validate merge-gate lab` job fails; both other jobs pass. The PR was closed **without merging**.
- **Scope:** No real credential was inserted into the test. The experiment proves scanner execution, controlled synthetic marker detection and required-check failure, but **does not establish coverage for every secret pattern or independently prove mergeability of a non-draft PR**.

**Publication status:** These claims refer to the linked PRs and run IDs; no production application, live cloud IAM or private security environment was modified by this laboratory.
