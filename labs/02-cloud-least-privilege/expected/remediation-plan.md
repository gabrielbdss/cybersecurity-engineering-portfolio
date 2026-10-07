# Reference Remediation Plan

## LP-01 — Audit delete capability has no demonstrated requirement
**Evidence state:** VERIFIED within the synthetic dataset.

The effective-access evidence grants `data.audit.delete`; the workload requirements do not identify a delete operation.

**Recommendation:** remove the delete capability in the laboratory target policy.

**Validation:** confirm append behavior still succeeds and deletion remains denied.

**Rollback:** restore the prior laboratory policy if required application behavior fails.

## LP-02 — Cryptographic signing scope is broader than demonstrated need
**Evidence state:** VERIFIED within the synthetic dataset.

The workload requires signing with one synthetic key, while the grant is project-scoped.

**Recommendation:** constrain signing authority to the required key when the platform policy model permits it.

**Validation:** required signing succeeds; signing against an unrelated synthetic key is denied.

**Rollback:** restore the previous laboratory binding if the expected signing path fails.

## LP-03 — Key listing is not demonstrated as necessary
Treat it as a removal candidate, but validate whether the application discovers keys dynamically before changing policy.

## Limitation
This exercise demonstrates an access-review method. It does not establish that any comparable permission exists or is exploitable in a real environment.
