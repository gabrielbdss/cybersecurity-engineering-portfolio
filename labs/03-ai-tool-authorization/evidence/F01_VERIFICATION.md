# F-01 — Verification, evidence and limitations

**Date:** 12 October 2026
**Codebase:** local `AI_Action_Boundary_F01_Fixed` working copy, derived from the original `AI_Action_Boundary_Challenge_Portfolio_Draft.zip`.
**Environment tested:** isolated Linux / Python 3.13.5, standard library; no cloud, credentials or production data.
**GitHub:** No commit, push, PR or CI execution made in this exercise.

## Observed before/after

| Requirement | Original ZIP | F-01 corrected package |
| --- | --- | --- |
| Cross-tenant denied request has zero ticket mutations | PASS | PASS |
| `TicketExecutor.run()` avoids returning foreign-tenant snapshots | **FAIL** — included `state_before` and `state_after` for both tenants | **PASS** — no target or state snapshots in returned dict |
| Agent-facing result excludes server-trusted principal and tenant IDs | **FAIL** — fields in returned dict | **PASS** — absent from result |
| Privileged audit still has complete before/after state for tests | PASS | PASS — `audit_events()` returns defensive copies |
| Existing vs nonexistent foreign resource indistinguishable by denial category | **FAIL** — could get `CROSS_TENANT_ACCESS` vs `RESOURCE_NOT_FOUND` | **PASS** — `CROSS_TENANT_ACCESS` for both |
| C01-C07 plus CONCURRENT demonstration | PASS on original in earlier test run | **PASS** after this change |

The before-case of foreign data exposure was identified by inspecting `run()` and by the negative probe `AI_Action_Boundary_Confidentiality_Probe.py` against the original ZIP in the prior review. The corrected build was retested by that probe, with 1/1 PASS (log: `f01-confidentiality-probe.log`). This is a *contract-level* test of the `run()` return; there was no real-world exposure or exfiltration.

## Test runs on corrected package

| Run | Actual observed result | Evidence file |
| --- | --- | --- |
| Main Lab03 regression suite, including 5 new F-01 tests | **31/31 PASS** | `f01-tests-console.log` |
| Supplemental adversarial round 1 (ported to F-01 split) | **9/9 PASS** | `f01-adversarial-round1.log` |
| Supplemental adversarial round 2 (ported to F-01 split) | **20/20 PASS** | `f01-adversarial-round2.log` |
| Standalone negative confidentiality probe, now a positive regression | **1/1 PASS** | `f01-confidentiality-probe.log` |
| Demo C01–C07 and CONCURRENT | **8/8 PASS** | `generated-C01.json` … `generated-CONCURRENT.json`, `generated-ALL.json` |

**Total across unittest runners:** 61/61 executions passed (31 + 9 + 20 + 1). The final probe overlaps a built-in confidentiality property; do not treat 61 as 61 unique security guarantees. The 8 demo verdicts were also checked by programmatic assertions against expected mutation counts and the separate `public_responses` schema.

## Reproduce (from repo root)

```bash
python3 -m unittest discover -s labs/03-ai-tool-authorization -p 'test_*.py' -v
python3 labs/03-ai-tool-authorization/review/adversarial_round1.py labs/03-ai-tool-authorization
python3 labs/03-ai-tool-authorization/review/adversarial_round2.py labs/03-ai-tool-authorization
python3 labs/03-ai-tool-authorization/demo.py --scenario ALL > /tmp/ai-boundary-all.json
python3 -c 'import json; d=json.load(open("/tmp/ai-boundary-all.json")); assert d["overall_verdict"] == "PASS"; print([(r["scenario"],r["verdict"]) for r in d["results"]])'
```

The `review/` tests are repeatable with no cloud/network. GitHub CI source in this ZIP is a **proposal only**; the updated source has **not** yet been exercised under GitHub Actions / Python 3.12, and must be integrated without overwriting existing workflow jobs.

## Response surfaces / residual risks

- **Untrusted/agent-facing:** Only the return from `TicketExecutor.run()` is intended to be forwarded; it contains minimal correlation/decision/mutation data, without snapshots, foreign resource identifiers or trusted session fields.
- **Privileged local reviewer:** `audit_events()` / `snapshot()` and `demo.py` stdout contain the full synthetic state across tenants, by design for the challenge's review evidence. This local lab does **not** enforce access control on those Python APIs. Never wire those privileged outputs directly to a model/agent or public endpoint.
- **Replay/concurrency:** Validated for cooperating threads sharing one in-memory executor. No persistent ledger, multi-process or crash-recovery guarantee.
- **Adversarial review independence:** All supplementary probes were authored or adapted in the same assistant-led project; they do **not** constitute external independent sign-off.
- **Scope:** No production system, real ticket, external LLM or business-specific implementation was accessed.

**Assessment:** F-01 closed **for the intended separation of public `run()` and privileged local reviewer output** in the synthetic lab, with the above limitations and pending external review/CI. Do not mark the overall challenge GO based only on local PASS reports.
