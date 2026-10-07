# Lab 05 — Dependency Finding Reconciliation

**Type:** Synthetic local-analysis laboratory  
**Goal:** Reconcile scanner severity with evidence of package presence, advisory applicability and reachability.

## Inputs

The lab supplies a fictional scanner result and application usage record.

## Decision exercise

Classify these separately:

- **Presence** — is the affected version resolved?
- **Applicability** — does the advisory cover it?
- **Reachability** — is the affected behavior demonstrated as reachable?
- **Exploitation** — is there evidence that exploitation occurred?

Do not collapse these into one claim.

## Expected result

The synthetic evidence demonstrates **presence and advisory applicability**, while direct vulnerable-path reachability and exploitation remain **UNVERIFIED**.

This is still actionable: upgrade planning can be justified by exposure and risk without overstating what has been proven.

See [expected/analysis.md](expected/analysis.md) after completing your own assessment.
