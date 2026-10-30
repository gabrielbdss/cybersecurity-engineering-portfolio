# Public Portfolio Security Assurance

**Status:** Portfolio CI and Publication Gate previously validated on PR; CodeQL remains active through GitHub Default Setup. Following the repository owner's enabling of Dependency graph, Dependency Review has been moved to an executable workflow. Its operational result must be verified against a completed PR run, not inferred from YAML alone.  
**Scope:** This repository's public source, controlled labs and publication safety. **Not** a claim about employer systems, CTF challenge correctness or production security.

## Security workflow matrix

| Workflow | Trigger | Scope and expected behavior | Principal limitation |
| --- | --- | --- | --- |
| [Portfolio CI](../.github/workflows/portfolio-ci.yml) | PR / main / manual | Existing Gitleaks secret scanning, regression tests, link checking **plus Publication Gate** in the existing merge-gate validation job | Patterns cannot guarantee absence of sensitive information |
| **CodeQL (GitHub Default Setup — existing)** | GitHub-managed | Existing CodeQL deployment, discovered when GitHub rejected a duplicate custom SARIF upload | Configuration and exact coverage governed by GitHub Default Setup; do not run advanced CodeQL simultaneously |
| [Security - Publication Gate](../.github/workflows/security-publication-gate.yml) | PR / main / manual | Independently validates sensitive file conventions, conservative secret markers and the embargoed CTF folder's file allowlist; positive/negative tests | Existing file contents allowed by name still need a human spoiler review |
| [Security - Dependency Review](../.github/workflows/security-dependency-review.yml) | PR to main | Uses the GitHub dependency graph to examine new dependency changes and fail on reported HIGH or CRITICAL advisories | Not a comprehensive historical scan; requires a valid dependency graph, declared manifests and an independently observed PASS |
| [Security - Weekly Assurance Summary](../.github/workflows/security-weekly-review.yml) | Mondays / manual | Generates a read-only aggregate of visible Code Scanning, Dependabot and Secret Scanning open alerts in the Actions run summary | Unsupported or unauthorized APIs report **UNKNOWN** rather than falsely claiming zero |
| [Operation Cymbal Disclosure Reminder](../.github/workflows/operation-cymbal-disclosure-reminder.yml) | One-time 2026-11-02 UTC-guarded schedule / manual | Requests explicit publication review by opening a generic issue | No automatic disclosure, report upload, visibility or branch changes |

## Release policy

- A successful automated check means its specific condition passed; it is **not** evidence of comprehensive security.
- Keep the existing GitHub-managed CodeQL, Gitleaks and Publication Gate under review. Dependency Review is now present in `.github/workflows`, following reported activation of Dependency graph. Validate successful PR results before describing the control as operational; use repository rules to require its stable job name only after a PASS.
- **Owner-reported setting change:** Dependency graph was enabled on October 30, 2026. GitHub Actions checks determine whether the workflow can use it; the connector's repository metadata does not independently expose the setting.
- Automated publication restrictions are a backstop. **Human review remains mandatory** for real assessment material, active competitions, third-party content and employer-related information.
- The only detailed Operation Cymbal forensic report is personal and remains outside this public repository.
- GitHub's default scheduled workflows execute only after the workflow is present on the default branch, and may start late.

## Negative-test record and review criteria

**Synthetic test cases** (no real secrets): allow a clean CTF overview; reject new unapproved CTF files, nested CTF paths, sensitive key-file extensions, `.env` and a synthetic private-key delimiter; skip `.git` metadata. The tests execute in isolated temporary directories.

**Acceptable merge evidence:** completed Dependency Review, Publication Gate and Portfolio CI checks on this activation PR. Existing CodeQL Default Setup remains separate in Security → Code scanning. A successful PR result validates the dependency delta checked, not an exhaustive dependency inventory.

No process changes, production deployment, external publication or authentication secrets are required to run these validators.
