# Architecture, contract and concurrency model

## Untrusted action JSON contract

Exactly these top-level fields, with no extra fields:

```json
{
  "request_id": "req-demo-1",
  "action_id": "demo-1",
  "tool": "ticket_api",
  "action": "ticket.comment",
  "resource": "tenant-a/ticket-101",
  "arguments": {"comment": "Synthetic comment"}
}
```

- `request_id`, `action_id`: ASCII letters, digits, underscore and dash, length 1–64.
- `tool`: literal `ticket_api` only.
- `action`: `ticket.comment` or `ticket.delete`.
- `resource`: `lowercase-tenant-id/lowercase-ticket-id`, each segment length 1–64 and characters `[a-z0-9-]`.
- `arguments`: for comment, exactly `{"comment": <non-blank string of length 1..280>}`; for delete, `{}`.
- Entire JSON string capped at 16,384 characters. Parser rejects duplicate JSON object keys, non-finite JSON numeric constants, unexpected types, unknown fields, missing fields and authority-like fields.
- Fields such as `principal_id`, `tenant_id`, `permissions`, `override` or `admin` in agent-proposed JSON are **rejected**, not trusted or used for authorization.

This is a deliberately narrow contract. A new operation type requires explicit schema and policy changes.

## Trusted context and stored truth

`TrustedContext(principal_id, tenant_id, permissions)` is a frozen dataclass constructed from local server-owned fixture data. In the CLI, choosing a fixture simulates authentication; it does not authenticate actual network users. The PDP checks the ticket's **stored** `tenant_id`, not only the string given in `resource`.

## PEP/PDP/executor separation

- The parser returns an immutable `Action` with only the mutation-relevant fields.
- The **PEP** (`TicketExecutor.run`) owns the lock, replay ledger, snapshots, policy dispatch, change detection and effect execution.
- The **PDP** (`TicketPolicy.evaluate`) returns a typed `PolicyDecision` based on capability and stored ownership. Any exception or malformed result fails closed.
- The executor modifies an isolated candidate copy of the store and swaps it into the instance's protected state under the lock; the `action_id` is consumed after a successful effect.
- The mutation counter is incremented only on the authorized mutating execution path. **F-01 response boundary:** `run()` returns only `request_id`, `action_id`, `decision`, `reason_code`, `executed`, `mutation_count_delta`. No `target_before`, `state_before`, tenant IDs or ticket content escapes in this agent-facing result. **Privileged local reviewer only:** `audit_events()` provides the complete server-trusted identity and target/full-store snapshots needed for verifiable evidence; `snapshot()` is similarly privileged.
- The isolated `demo.py` is explicitly a reviewer CLI and emits the privileged `records`, `initial_state`, `final_state` to local stdout; do not expose its output to the agent or an untrusted client. It also records separate `public_responses` for inspecting the contract. This lab does not authenticate reviewers; access to these privileged Python APIs must be controlled by a real deployment.

## TOCTOU and adversarial hook

`_trusted_test_after_check` is a **test-only instrumentation point**, invoked after PDP ALLOW but before the effect while holding the engine lock. Tests modify the original input proposal's action, resource or arguments. The PEP reparses the source and rejects the changed proposal (`OPERATION_CHANGED`) without mutating. The effect would only use the immutable validated `Action`, never mutable attacker-supplied data.

No untrusted input can set or inject this callback through JSON. The hook must never be exposed to a real API. We do not assert that reparsing untrusted input solves general distributed TOCTOU. For this simulation, all stored ticket state is protected by the same lock.

## Replay / concurrency

A single `RLock` serializes all supported operations through one shared `TicketExecutor`. It covers permission evaluation, replay lookup, source-change check, candidate-state computation and commit. A global in-memory set records consumed `action_id` values. Simultaneously submitted duplicate IDs are serialized, so only one reaches a successful effect. `test_concurrent_replay_single_process_no_double_execution` launches 16 threads behind a barrier and checks one ALLOW and 15 replay denials with one total mutation.

This supports **at-most-one observed mutating effect in a live single executor instance** under the tested conditions. No persistent exactly-once or distributed idempotency guarantee is claimed. The in-memory commit is not designed for abrupt process termination at an arbitrary instruction. A real service would need durable atomic mutation/idempotency coordination.

## Failure and error behavior

- Missing permission, tenant mismatch, replay and changed source: `DENY`, protected state identical, zero target mutations. A guessed foreign-tenant resource receives the same `CROSS_TENANT_ACCESS` error whether it exists or not; this avoids exposing foreign-ticket existence by reason-code differences.
- Invalid schema: `ERROR` with stable reason code (spoofed identity specifically `DENY`), no target mutation.
- Policy exception, timeout, or untyped decision: `ERROR` / `POLICY_UNAVAILABLE`, no target mutation.
- Unexpected executor exception before commit: `ERROR` / `EXECUTION_ERROR`, no intentional target mutation.
- When strict validation rejects a parsed Python dictionary, a syntactically safe `request_id` and `action_id` may still be echoed as **untrusted correlation labels**. They are never authority. Completely unparsable JSON has null IDs because there is no safe parsed structure.
- Audit records, unlike ticket-state writes, are allowed for denied/error requests.

## Reviewer trade-offs

The global lock is simple and robust for a small demo but serializes all tenants and operations, reducing throughput. An optimized system might use per-key locks plus a robust transactional ledger, but complexity and proof obligations increase. Full snapshots provide transparent **privileged reviewer** evidence for tiny fixtures; they are not suitable for user-visible responses or unchanged use with large sensitive real-world data sets. See SECURITY_CHANGELOG.md (F-01).
