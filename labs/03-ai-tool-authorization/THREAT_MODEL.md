# Threat Model — AI Action Boundary (v1.0, synthetic)

## Mission and protected assets

Prevent any model-proposed ticket mutation unless an independent enforcement layer authorizes the precise actor, operation and current resource. Protected assets: ticket existence, status, comments, tenant isolation, policy authority, replay state, and correlatable execution records.

## Attacker / capabilities

An adversary may control untrusted text supplied to an agent, the proposed JSON body, its action/resource/arguments, a claimed `principal_id`, injected `override` instructions, reuse of an `action_id`, and timing of concurrent submissions. They may not modify server-owned session fixtures, policies or store internals directly and may not execute malicious Python in the process. This limitation is material.

## Trust boundaries

1. **Model-to-parser:** all JSON fields are untrusted; schema rejects unknown or invalid fields and explicit authority claims.
2. **Server-session-to-PEP:** only server-owned `TrustedContext` carries principal, tenant and capabilities; model output does not.
3. **PEP-to-PDP:** PDP reads server-side ticket ownership and returns typed ALLOW/DENY. Unexpected policy failures never authorize.
4. **PEP-to-store:** the protected mutation is reachable only through the authorized executor flow. Immutable action snapshot and lock bind decision to effect.
5. **Replay ledger/store:** single shared lock serializes all cooperating in-process threads; action ID reuse cannot produce another mutation.
6. **Evidence (F-01):** full snapshots and the authenticated identity are confined to the privileged *local reviewer harness* (`audit_events()` / `snapshot()`); `run()` only returns minimal decision metadata to agents. These are not real authenticated service endpoints. The `demo.py` output is an explicitly privileged evaluator artifact, never a response to an agent.
7. **Foreign-resource existence:** foreign-tenant ticket IDs return `CROSS_TENANT_ACCESS` regardless of whether the foreign ticket exists, preventing existence enumeration through public reason codes.

## Threat-to-control map

| ID | Abuse / failure | Defense | Verification |
| --- | --- | --- | --- |
| C01 | incorrectly applied authorized operation | check capability/tenant/resource; mutate exact target | one intended effect, other resources unchanged |
| C02 | insufficient delete privilege | `ticket.delete` capability required | DENY, zero mutating calls and unchanged full state |
| C03 | cross-tenant access | match authenticated tenant to stored ticket owner and resource tenant | DENY, zero effects |
| C04 | claim `admin` or `override` from model | strict contract + trusted-context-only identity | no privilege promotion; denial |
| C05 | change action/resource/args between decision and use | validated frozen action, recheck original source, critical-section execution | three adversarial mutation variants fail with no effects |
| C06 | same authorized ID replayed | shared consumed-ID registry under lock | second execution zero effect |
| C07 | unavailable/faulty PDP | typed decision and fail-closed handling | error classified; zero mutations |
| Additional | malformed payload / ambiguous duplicate JSON keys | exact schema and parser errors | controlled rejection |
| Additional | unrelated ticket modified accidentally | full snapshot comparison + isolation tests | unrelated resources unchanged |
| Concurrent | two threads use same ID together | common `RLock` across check/reserve/mutation | concurrency test: one allowed, others replay |

## Assumptions and invariants

- **INV-01:** `DENY` or `ERROR` implies no mutation of protected resources by that request; full before/after state equal and invocation delta zero.
- **INV-02:** no JSON assertion overrides server-authenticated identity, tenant or capabilities.
- **INV-03:** only the action/resource/arguments bound to the authorization may reach the executor.
- **INV-04:** consumed `action_id` never effects a second mutation while the shared executor lives.
- **INV-05:** missing, malformed, timed-out or exception-producing policy evaluation cannot result in ALLOW.
- **INV-06:** successful authorized mutation affects only its permitted target.
- **INV-07:** single-process concurrent duplicate submissions still produce at most one mutation.
- **INV-08 (F-01):** every public `run()` result contains decision metadata only — never ticket content, trusted principal details or cross-tenant snapshots; separate privileged audit retains the full evidence. Foreign-tenant ticket existence cannot be distinguished from policy reason codes.

## Failure modes / residual risk

- The in-memory ledger is lost on restart and does not coordinate across processes/hosts. This lab does not claim durable or distributed exactly-once behavior.
- The server is a synthetic trusted harness, not a demonstration of real-world authentication or IAM enforcement.
- Python objects, fixtures and internal lock are not hardened against arbitrary in-process code execution; this threat is outside this lab's scope.
- Real remote service writes need durable transactions, idempotency keys and crash-recovery logic not modeled here.
- A global `action_id` namespace means an accepted completed ID remains unavailable even if a different principal later presents it; this is an intentionally conservative choice for the lab.
- Under denial or error, an audit record is written; the invariant concerns the protected ticket target and mutation counter, not absence of benign observability data.
- Full snapshots are easy for a tiny synthetic data set, but would require privileged reviewer authentication, data minimization, retention policies and careful redaction/scaling in production. The lab's `audit_events()` method does not itself authenticate its caller, and the local reviewer CLI output includes protected synthetic state. This is explicitly **outside** the untrusted-agent boundary.

**No employer architecture, secrets, private data, real system or production compliance is claimed.**
