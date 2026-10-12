# Lab 03 — AI Action Boundary: Independent Tool Authorization

**Synthetic, standalone security engineering lab.** No real LLM, cloud, network API, production service, secrets, or third-party dependencies are needed.

## The security question

> A model can *propose* a ticket operation; it must not *grant itself authority* to execute it.

This lab applies **AI-02**: untrusted model output must not bypass authorization at the tool execution boundary. The target is a disposable in-memory ticket store containing separate fictional tenants. All executions use fresh synthetic data.

## Run locally (Python 3.12+)

From the **repository root**:

```bash
python3 --version
python3 -m unittest discover -s labs/03-ai-tool-authorization -p 'test_*.py' -v
python3 labs/03-ai-tool-authorization/demo.py --scenario C01
python3 labs/03-ai-tool-authorization/demo.py --scenario C03
python3 labs/03-ai-tool-authorization/demo.py --scenario C06
python3 labs/03-ai-tool-authorization/demo.py --scenario C07
python3 labs/03-ai-tool-authorization/demo.py --scenario CONCURRENT
python3 labs/03-ai-tool-authorization/demo.py --scenario ALL
```

Exit status `0` with test `OK` or a single-scenario demo `"verdict": "PASS"` indicates passing **for the tested synthetic implementation**, not a production or independent-review attestation. With `--scenario ALL`, inspect **`"overall_verdict": "PASS"`** and the `results` array. The demo exits nonzero if its built-in oracles fail. To reproduce stored evidence, see [evidence/README.md](evidence/README.md).

## Architecture

```text
Untrusted ticket text or model -> untrusted action JSON
                                      |
                                      v
                              strict schema parser
                                      |
Server-owned TrustedContext --------> PEP / TicketExecutor
                                      |
                      replay check + lock + independent PDP
                                      |
                            frozen authorized operation
                                      |
                           in-memory protected commit
                                      |
                        structured audit event + snapshots
```

- `policy.py`: `TrustedContext` and independent `TicketPolicy` / PDP authorization decision.
- `executor.py`: strict input validation, immutable `Action` snapshot, single-process lock, effect enforcement, replay ledger, **minimal agent-facing `run()` result**, and **full before/after state available only via the privileged local audit harness** (`audit_events()`).
- `lab_data.py`: server-owned synthetic fixture loader; **not** an authentication service.
- `demo.py`: CLI scenarios C01–C07 plus `CONCURRENT`, each with a clean starting state and explicit verdict checks.
- `test_authorization.py`: independent unit and adversarial checks, including error injection and effect isolation.
- `fixtures/`: synthetic tickets and server-owned session fixture data.
- `THREAT_MODEL.md`: assets, attacker capabilities, trust boundaries, assumptions, threat table, residual risks.
- `ARCHITECTURE.md`: data contract, binding strategy, concurrency and failure analysis.

## Trust / authorization boundaries

The **only** principal and tenant identity used for authorization comes from a `TrustedContext` created by the local **server harness**. It is never accepted from agent JSON. Unsupported authority fields (`principal_id`, `tenant_id`, `permissions`, `override`, `admin`) are rejected. The policy also checks **actual ticket ownership in the server-side ticket store**; a resource string from the model is not proof of ownership.

Permission is checked before any mutation. If the evaluator errors, times out, or returns an invalid decision type, the PEP fails closed. No agent-provided hash, role, prompt instruction, or claim is accepted as authorization.

## Security change F-01 — 12 October 2026

**Finding (before):** `TicketExecutor.run()` returned complete multi-tenant `state_before` and `state_after` snapshots, including foreign tenant data even on `DENY`. The previous policy also gave different reason codes for existing and missing foreign-tenant IDs.

**Correction (after):** `run()` returns only request/action correlation IDs, decision, reason, executed boolean, and per-request mutation delta — **no ticket content, user identity or tenant snapshots**. Full `target_before`/`target_after`, `state_before`/`state_after` and trusted principal details are retained in `audit_events()` **for a privileged LOCAL reviewer harness only**. The local `demo.py` explicitly calls this privileged accessor to create the evaluator's evidence; `records` and `initial_state` / `final_state` in that CLI output MUST NOT be forwarded to untrusted actors. `public_responses` demonstrates the safe contract. Foreign-tenant ticket IDs return the same `CROSS_TENANT_ACCESS` whether the ticket exists or not.

**Tests:** F-01 response minimization (DENY, ALLOW and malformed inputs); defensive-copy audit evidence; foreign ticket existence non-enumeration. Full details, limits and actual results are in [SECURITY_CHANGELOG.md](SECURITY_CHANGELOG.md) and [evidence/F01_VERIFICATION.md](evidence/F01_VERIFICATION.md).

**Important limit:** the lab provides **no real reviewer authentication**. `snapshot()` and `audit_events()` are trusted local Python APIs; a production integration must restrict these behind server-side access control. The demo is a *privileged offline review CLI*, not a user-facing API. No confidentiality claim is made if an attacker can call arbitrary Python methods on the `TicketExecutor` object.

## Scenario / oracle matrix

| Scenario | Purpose | Required test oracle |
| --- | --- | --- |
| C01 | same-tenant authorized comment | `ALLOW`, exactly one target mutation, other targets unchanged |
| C02 | missing delete permission | `DENY`, full protected state equal before/after, zero mutations |
| C03 | cross-tenant comment | `DENY`, full state unchanged, zero mutations |
| C04 | `principal_id=admin` / override | identity not elevated, no mutation |
| C05 | mutate action/resource/args after policy | changed operation denied, no mutation |
| C06 | reuse consumed `action_id` | first `ALLOW` +1; second denied +0, same final state |
| C07 | policy timeout/invalid decision | `ERROR` / fail closed, full state unchanged, zero mutations |
| Extra | malformed JSON, fields, IDs, types | controlled rejection, zero mutations |
| Extra | effect isolation | only authorized target changes |
| Extra | concurrent replay | exactly one `ALLOW` among simultaneous thread requests |

All denied/error executions compare **entire protected state**, not just the requested target, and require `mutation_count_delta == 0`. Audit logging for denials is intentionally *not* counted as a protected target mutation.

## Design limits (do not overclaim)

1. **No production security claim:** this is an educational in-memory simulation. It proves behavior only in the exercised cases.
2. **Single process / threads:** one `TicketExecutor` shared across cooperating threads uses an `RLock`. No claim for multiprocess, distributed nodes, persistent databases, host crashes or process restarts.
3. **At-most-once under tested conditions, not durable exactly-once:** consumed action IDs live in memory. After restart they are forgotten. There is no transactional outbox, persistent ledger, external effects or crash-recovery proof.
4. **Trusted server assumption:** authentication is simulated by fixture selection. Attackers are not assumed able to execute arbitrary Python in-process or mutate the private ticket store / trusted fixture source directly.
5. **TOCTOU scope:** effects use an immutable, validated `Action` snapshot while policy and mutation run under one lock. Tests can change the original source proposal after authorization and show rejection. No external mutable resource or remote authorization server is involved.
6. **No cryptographic claims:** snapshots and audit events are inspectable, not signed or tamper-evident. CI success must be checked from actual GitHub job execution after publication.
7. **Error handling:** fail-closed on policy errors, with no deliberate simulated crash between internal commit operations. This lab does not prove durability or atomicity against process termination at arbitrary CPU instructions.

## Independent reviewer checklist

1. Clone this repository on a clean machine (Python 3.12+).
2. Run all tests, demo C01..C07 and `CONCURRENT` without secrets or network.
3. Change the synthetic fixture *locally* and rerun: ensure policy uses the current stored tenant.
4. Inject `principal_id: "admin-a"`, malformed inputs, modified arguments and invalid PDP output.
5. In privileged local CLI/reviewer evidence only, inspect `records[].target_before/target_after`, `state_before/state_after` and `mutation_count_delta`. Confirm `public_responses` has no snapshots; do not accept an unverified printed `PASS`.
6. Inspect actual GitHub Actions job steps and HEAD SHA before claiming CI PASS.
7. Keep the PR unmerged until an independent reviewer gives a documented disposition.

**Publication note:** verify authorship, applicable license and disclosure approval before putting any review materials online. This repository contains only fictional resources and self-contained source code; it does not use employer materials.
