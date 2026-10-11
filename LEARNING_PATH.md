# Guided Cybersecurity Engineering Learning Path

**Purpose:** Understand, run, challenge and explain the public portfolio artifacts. This is a study plan, not a claim of independent professional proficiency or an employer assessment.

## A repeatable study method

For each artifact: **observe → reproduce → explain → challenge → adapt → document**.
1. Define the threat, asset and trust boundary in plain language.
2. Reproduce the published output locally with synthetic evidence.
3. Explain each input, decision rule, state and error path.
4. Change one controlled fixture and predict the expected outcome before running.
5. Explain the limits: what this proves, what it does not prove, and what production evidence would be needed.
6. Document safe next steps; distinguish READ ONLY analysis from MUTATING or DESTRUCTIVE operations.

## Eight guided modules

| Session | Topic | Practical exercise | Interview objective |
|---|---|---|---|
| 01 | Incident response / HTTP | Run Lab 01; explain 403, request IDs and UTC; create a stale denial | Explain fact vs hypothesis |
| 02 | Python and JSONL | Read `triage.py`; implement a new test with guidance | Explain parsing, correlation windows and failure modes |
| 03 | IAM / least privilege | Run Lab 02; compare declared grant scope with declared need | Explain IAM inheritance and why this lab is not effective-access evaluation |
| 04 | CI and DevSecOps | Run Lab 04; inspect GitHub Actions and ruleset negative PR | Explain pipeline vs branch ruleset and fail-closed behavior |
| 05 | AppSec | Read Project Lumen; separate Semgrep/SAST, Trivy/SCA and manual review | Defend actual performed work without revealing private findings |
| 06 | AI security | Analyze tool authorization lab and boundary diagram | Explain why model output is not authorization |
| 07 | Incident playbook | Work through a synthetic incident tabletop, from detection to recovery | Explain authority, evidence custody, containment and rollback |
| 08 | Technical mock interview | Reproduce two labs and answer an adversarial review | Explain limits, debugging, validation and residual risk autonomously |

## Self-check questions

- What direct evidence supports this claim? Is it OBSERVED, VERIFIED, INFERRED or UNVERIFIED?
- Which source fields and timestamps must agree before we claim correlation?
- How could this test pass while the real system remains vulnerable?
- Which proposed action changes production state, and who has authority to approve it?
- If CI passes, what still needs to be enforced by branch protection?
- What would constitute a meaningful negative test?

## Read-only local commands

```bash
python3 labs/01-cloud-incident-triage/triage.py
python3 -m unittest discover -s labs/01-cloud-incident-triage -p "test_*.py" -v
python3 labs/02-cloud-least-privilege/review_access.py
python3 -m unittest discover -s labs/02-cloud-least-privilege -p "test_*.py" -v
python3 scripts/check_portfolio_links.py
```

These commands inspect and execute local synthetic evidence; they do not query the cloud or change employer resources.

## Completion criterion

The learner should be able to reproduce the output, interpret failures, write and explain one test, and answer what the artifact does **not** prove without consulting prepared talking points.
