# Supplemental adversarial review scripts

These are **author-side simulations**, not independent third-party review. Both scripts were ported from the earlier reported review rounds to the F-01 public-response vs privileged-audit split. Run using Python standard library only:

```bash
python3 labs/03-ai-tool-authorization/review/adversarial_round1.py labs/03-ai-tool-authorization
python3 labs/03-ai-tool-authorization/review/adversarial_round2.py labs/03-ai-tool-authorization
```

- Round 1: 9 tests, including 20 x 32-thread same-action-ID contention (640 attempted calls).
- Round 2: 20 tests, including 15 x 48-thread contention (720 attempted calls).
- These scripts use `TicketExecutor.run()` for **minimal decision metadata**; assertions requiring protected full state call the privileged local `audit_events()`/`snapshot()` API.
- They do **not** test multiple processes, durable persistence, production access control or crash consistency.

History: the two source suites previously ran on the original ZIP; they were amended only where callers depended on the deliberately removed `run()` snapshot fields, not to bypass or weaken a denial invariant. Test sources can be inspected and modified by an independent reviewer.
