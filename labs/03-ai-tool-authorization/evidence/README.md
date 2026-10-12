# Evidence — reproducible, not self-attesting

`test-vector.json` is the **historical static sample** from the earlier portfolio lab, not a record of a security test execution. Do not call that fixture a CI PASS.

`generated-C01.json` through `generated-C07.json` and `generated-CONCURRENT.json` are generated **by executing** `demo.py` on the isolated build environment. These are *privileged offline-review artifacts*; they contain full store before/after snapshots and `mutation_count_delta` generated from the simulated executor. They also carry the **separate minimized `public_responses`** that would be returned to an agent. Do not make the CLI artifact itself an agent response. Validate them again locally and on GitHub Actions; these files alone do not prove the absence of other vulnerabilities.

From repo root, regenerate independent evidence:

```bash
python3 -m unittest discover -s labs/03-ai-tool-authorization -p 'test_*.py' -v
python3 labs/03-ai-tool-authorization/demo.py --scenario C01 > labs/03-ai-tool-authorization/evidence/generated-C01.json
python3 labs/03-ai-tool-authorization/demo.py --scenario C03 > labs/03-ai-tool-authorization/evidence/generated-C03.json
python3 labs/03-ai-tool-authorization/demo.py --scenario C06 > labs/03-ai-tool-authorization/evidence/generated-C06.json
python3 labs/03-ai-tool-authorization/demo.py --scenario C07 > labs/03-ai-tool-authorization/evidence/generated-C07.json
python3 labs/03-ai-tool-authorization/demo.py --scenario CONCURRENT > labs/03-ai-tool-authorization/evidence/generated-CONCURRENT.json
```

To regenerate the other C02/C04/C05 records replace `--scenario` appropriately. Every demo starts with a *fresh* store. A `PASS` in output is based on programmatic assertions; inspect `state_before`, `state_after`, `mutation_count_delta`, and `reason_code`. The independent reviewer should add their own unexpected cases.

`local-test-results.txt` is captured local unittest output. `LOCAL_VERIFICATION.md` documents the actual local environment, scope and clear remaining CI/review gaps. Run metadata is synthetic-lab evidence, not a production report.


## F-01 evidence generated after confidentiality hardening

Read [F01_VERIFICATION.md](F01_VERIFICATION.md). `f01-tests-console.log`, `f01-adversarial-round1.log`, `f01-adversarial-round2.log` and `f01-confidentiality-probe.log` are captured test outputs for this corrected source. The historical `local-test-results.txt` belongs to the original 26-test build and is **not** evidence of the fix.
