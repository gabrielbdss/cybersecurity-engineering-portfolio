# LOCAL_VERIFICATION — preparation environment

**Generated (UTC):** 2026-10-12T12:16:57Z
**Python:** 3.13.5
**Environment:** isolated container, Linux; **not** the user's Mac and **not** GitHub Actions.
**Unit and adversarial tests:** 26/26 PASS, no failures, no errors, exit code 0.
**Demo (`--scenario ALL`):** PASS, exit code 0.
**Individual scenario results:** C01=PASS, C02=PASS, C03=PASS, C04=PASS, C05=PASS, C06=PASS, C07=PASS, CONCURRENT=PASS.

**Real observed target effects:** C01 = 1 mutation; C02/C03/C04/C05/C07 = 0; C06 first = 1 and second = 0; CONCURRENT = 1 total mutation for 12 attempted concurrent calls. The unit test additionally exercises 16 simultaneous calls behind a thread barrier. Consult generated JSONs for complete before/after state, decisions, correlation IDs and mutation deltas. This is local synthetic validation only.

## Source SHA-256 (captured for this run)

- `policy.py`: `b584a7670df3fc957eccf7148b270a5cff5119bb452b4303f1dac68fcd9e53e9`
- `executor.py`: `b1a3c95b2b31bd32cecb92d4751dd173bf0fc7bbb073cc6e4c10814b3d029dee`
- `lab_data.py`: `d61191a849d3a776146f2a0b1bd390b65bc2450a68a6f3c81147bd01be7a0bc8`
- `demo.py`: `2fecbeeb7b2262729d40d3cab2240e335b64dd78f2589690868d6c2195c5ed3f`
- `test_authorization.py`: `e5970356aa9e0375cc7b971120b64050e5f019b798a7a9db753e1f07dd47bb6d`

## Remaining gates / limitations

- On-user-mac Python 3.13.7 execution of this generated code: **NOT_RUN**.
- GitHub Actions Python 3.12 execution and stable required-check enforcement: **NOT_RUN / NOT_VERIFIED**.
- Separate PR, independent adversarial review and author's technical defense: **NOT_RUN**.
- Formal GO / CONDITIONAL GO / HOLD score: **NOT_EVALUATED**.
- Production or institutional security: **NOT CLAIMED**.
- Concurrency guarantee: **single Python process / shared executor instance only**; not crash-durable, multi-process or distributed.

A successful local test suite does not guarantee the absence of vulnerabilities under unseen adversarial cases.


## Additional F-01 security remediation validation — 12/10/2026

This earlier verification note refers to the **pre-F-01** version. The corrected source was executed separately on Python 3.13.5, with main suite 31/31, migrated reviewer simulations 9/9 and 20/20, standalone confidentiality probe 1/1, and all eight CLI demos PASS. Full new logs and limits are in [F01_VERIFICATION.md](F01_VERIFICATION.md). Python 3.12 remote CI remains NOT_RUN. The original `local-test-results.txt` is retained as **historical old-build output** and must not be cited as current F-01 verification.
