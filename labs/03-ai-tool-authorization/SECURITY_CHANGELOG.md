# Security Change Log — AI Action Boundary

## 2026-10-12 — F-01: Minimize agent-facing responses and keep privileged evidence separate

**Origin:** Independent-style adversarial review simulation, Round 2 (same authoring assistant, not independent third-party approval). The initial source returned full cross-tenant snapshots from `TicketExecutor.run()` even on an unauthorized request.

**Risk:** If an integrating developer forwarded the raw return value to an agent, a DENY decision could reveal other tenants' ticket contents. Separately, `RESOURCE_NOT_FOUND` versus `CROSS_TENANT_ACCESS` permitted distinguishing nonexistent vs existing guessed foreign resources.

**Before (confirmed):** `run()` returned an `event` dictionary with `state_before`, `state_after`, `target_before`, `target_after`, `trusted_principal_id`, and `trusted_tenant_id`, across all protected tickets. A negative confidentiality probe failed on the original ZIP.

**After (implemented):**

1. `executor.py`: `run()` now returns **only** `request_id`, `action_id`, `decision`, `reason_code`, `executed`, `mutation_count_delta`. No snapshots or trusted principal/tenant fields are returned.
2. `executor.py`: full per-action audit event is retained internally; `audit_events()` returns defensive copies exclusively for the **trusted local reviewer harness**. `snapshot()` is also a privileged harness API. No network-facing authorization layer is implemented for these methods.
3. `policy.py`: foreign-tenant resource checks precede existence checks, so existing and nonexistent foreign IDs both get `CROSS_TENANT_ACCESS`.
4. `demo.py`: preserves `records` with full before/after state from **privileged** `audit_events()` and includes new `public_responses` demonstrating minimized action responses. CLI output is deliberately privileged and must not be sent to an agent.
5. `test_authorization.py`: existing assertions now read privileged audit events for snapshot comparisons. Added five F-01 tests (DENY, ALLOW, malformed/spoofing responses, defensive copying, non-enumeration).
6. `review/`: migrated 9 + 20 previously authored adversarial regression tests to the new public/audit split. The tests remain a simulated adversarial review, **not independent approval**.
7. `README.md`, `ARCHITECTURE.md`, `THREAT_MODEL.md`, evidence notes: now explicitly identify the confidentiality boundary, limitations and evidence paths. Clarified `--scenario ALL` uses `overall_verdict`.

**Compatibility note:** The return schema of `TicketExecutor.run()` changed intentionally. Callers that previously relied on raw snapshots from `run()` must be migrated to the privileged reviewer harness; this is a deliberate breaking API change. Existing C01–C07 security semantics and their privileged evidence remain intact.

**Scope and residual risk:** This is a **synthetic single-process Python lab**, without an actual authenticated server. A caller with arbitrary Python access to the executor object could still invoke the privileged `audit_events()` / `snapshot()` methods; a real service must protect those APIs at its boundary. CLI `demo.py` intentionally writes privileged synthetic evidence. No real tenant/customer information or cloud resource is involved. Replay ledger remains in-memory and concurrency is only within one shared instance.

**Validation:** See `evidence/F01_VERIFICATION.md` for actual tests and environment. No Python 3.12 GitHub Actions results, independent external review or official evaluation are claimed.
