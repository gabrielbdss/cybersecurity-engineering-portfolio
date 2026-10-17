# Tabletop — Suspicious API request and authorization denial

**Type:** fictional, discussion-based incident-response exercise. **Execution status:** scenario and facilitator prompts prepared; no live incident, team drill, cloud containment or recovery test performed.

## Scenario

A fictional internal API emits one HTTP 403, a corresponding application authorization-denied event, and an unrelated audit event. An alert fires. The analyst must avoid confusing a blocked attempt with a confirmed compromise.

## Facilitation sequence

| Stage | Prompt | Expected analyst artifact |
| --- | --- | --- |
| Detect | What triggered the alert, and what system is in scope? | One-sentence incident intake |
| Preserve | Which logs must be retained before any changes? | Read-only preservation plan |
| Triage | Do HTTP and application events share a request ID and plausible time? | UTC timeline and correlated/unrelated event distinction |
| Hypotheses | Does the evidence show stolen credentials or exfiltration? | Evidence-for/evidence-against matrix; **UNVERIFIED** where absent |
| Decide | Is immediate containment justified? Who authorizes it? | Decision owner and proportional containment rationale |
| Recover | What must be verified before declaring recovery? | Functional regression, auth-denial and telemetry checks |
| Learn | Which uncertainty needs a new alert, test or logging field? | One prioritized improvement and residual risk |

## Reproduce the technical evidence

From the repository root:

```bash
python3 labs/01-cloud-incident-triage/triage.py
python3 -m unittest discover -s labs/01-cloud-incident-triage -p 'test_*.py' -v
```

**Expected interpretation:** A correlated HTTP 403 and application denial can be supported by synthetic evidence. Malicious intent, compromise, data exfiltration and operational recovery are **not** established.

**Completion requirement for a future exercise:** Capture facilitator, date, decisions, outcome and improvement owner only after a real tabletop session actually occurs. Do not mark the tabletop as executed based on this document.
