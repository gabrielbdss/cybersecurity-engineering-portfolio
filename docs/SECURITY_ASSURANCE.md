# Public Portfolio Security Assurance

**Status:** Implemented through GitHub Actions; evidence must come from completed runs, not merely YAML configuration.  
**Scope:** This repository's public source, controlled labs and publication safety. **Not** a claim about employer systems, CTF challenge correctness or production security.

## Security workflow matrix

| Workflow | Trigger | Scope and expected behavior | Principal limitation |
| --- | --- | --- | --- |
| [Portfolio CI](../.github/workflows/portfolio-ci.yml) | PR / main / manual | Existing Gitleaks secret scanning, regression tests, link checking **plus Publication Gate** in the existing merge-gate validation job | Patterns cannot guarantee absence of sensitive information |
| [Security - CodeQL Python](../.github/workflows/security-codeql.yml) | PR / main / Tuesdays | Python CodeQL with `security-extended` queries; results in Code Scanning if GitHub permissions allow | Only supported Python code paths and query coverage |
| [Security - Publication Gate](../.github/workflows/security-publication-gate.yml) | PR / main / manual | Independently validates sensitive file conventions, conservative secret markers and the embargoed CTF folder's file allowlist; positive/negative tests | Existing file contents allowed by name still need a human spoiler review |
| [Security - Dependency Review](../.github/workflows/security-dependency-review.yml) | PR to main | Blocks introduction of dependencies reported with high/critical known vulnerabilities | This is a PR delta check; not an inventory of all existing dependencies |
| [Security - Weekly Assurance Summary](../.github/workflows/security-weekly-review.yml) | Mondays / manual | Generates a read-only aggregate of visible Code Scanning, Dependabot and Secret Scanning open alerts in the Actions run summary | Unsupported or unauthorized APIs report **UNKNOWN** rather than falsely claiming zero |
| [Operation Cymbal Disclosure Reminder](../.github/workflows/operation-cymbal-disclosure-reminder.yml) | One-time 2026-11-02 UTC-guarded schedule / manual | Requests explicit publication review by opening a generic issue | No automatic disclosure, report upload, visibility or branch changes |

## Release policy

- A successful automated check means its specific condition passed; it is **not** evidence of comprehensive security.
- Keep CodeQL, dependency review, Gitleaks and the Publication Gate visible in PR checks; use repository rules to require checks **only after their job names and green execution are confirmed**.
- Automated publication restrictions are a backstop. **Human review remains mandatory** for real assessment material, active competitions, third-party content and employer-related information.
- The only detailed Operation Cymbal forensic report is personal and remains outside this public repository.
- GitHub's default scheduled workflows execute only after the workflow is present on the default branch, and may start late.

## Negative-test record and review criteria

**Synthetic test cases** (no real secrets): allow a clean CTF overview; reject new unapproved CTF files, nested CTF paths, sensitive key-file extensions, `.env` and a synthetic private-key delimiter; skip `.git` metadata. The tests execute in isolated temporary directories.

**Acceptable merge evidence:** completed PR checks for all new workflows, plus the existing Portfolio CI; review the full CodeQL SARIF result in the Security UI and the dependency-review summary for actual findings and limits.

No process changes, production deployment, external publication or authentication secrets are required to run these validators.
