# Public Portfolio Security Assurance

**Status:** Portfolio CI and Publication Gate validated on PR; CodeQL is already active through GitHub Default Setup; Dependency Review is prepared but **not enabled** until Dependency graph is activated. Evidence must come from completed runs, not YAML alone.  
**Scope:** This repository's public source, controlled labs and publication safety. **Not** a claim about employer systems, CTF challenge correctness or production security.

## Security workflow matrix

| Workflow | Trigger | Scope and expected behavior | Principal limitation |
| --- | --- | --- | --- |
| [Portfolio CI](../.github/workflows/portfolio-ci.yml) | PR / main / manual | Existing Gitleaks secret scanning, regression tests, link checking **plus Publication Gate** in the existing merge-gate validation job | Patterns cannot guarantee absence of sensitive information |
| **CodeQL (GitHub Default Setup — existing)** | GitHub-managed | Existing CodeQL deployment, discovered when GitHub rejected a duplicate custom SARIF upload | Configuration and exact coverage governed by GitHub Default Setup; do not run advanced CodeQL simultaneously |
| [Security - Publication Gate](../.github/workflows/security-publication-gate.yml) | PR / main / manual | Independently validates sensitive file conventions, conservative secret markers and the embargoed CTF folder's file allowlist; positive/negative tests | Existing file contents allowed by name still need a human spoiler review |
| **[Dependency Review — template prepared](workflow-templates/security-dependency-review.yml)** | **NOT ACTIVE** | PR dependency-delta check is ready to place in workflows after Dependency graph is enabled | GitHub rejected the test with: **Dependency review is not supported on this repository. Please ensure that Dependency graph is enabled** |
| [Security - Weekly Assurance Summary](../.github/workflows/security-weekly-review.yml) | Mondays / manual | Generates a read-only aggregate of visible Code Scanning, Dependabot and Secret Scanning open alerts in the Actions run summary | Unsupported or unauthorized APIs report **UNKNOWN** rather than falsely claiming zero |
| [Operation Cymbal Disclosure Reminder](../.github/workflows/operation-cymbal-disclosure-reminder.yml) | One-time 2026-11-02 UTC-guarded schedule / manual | Requests explicit publication review by opening a generic issue | No automatic disclosure, report upload, visibility or branch changes |

## Release policy

- A successful automated check means its specific condition passed; it is **not** evidence of comprehensive security.
- Keep the existing GitHub-managed CodeQL, Gitleaks and Publication Gate under review. Move the Dependency Review template into `.github/workflows` **only after enabling Dependency graph** and verifying a successful PR check. Never claim it is active while blocked.
- **Repository owner action needed:** Settings → Security → Code security → enable **Dependency graph**. This connector does not offer a compatible settings-write action, so the control cannot be enabled from this session.
- Automated publication restrictions are a backstop. **Human review remains mandatory** for real assessment material, active competitions, third-party content and employer-related information.
- The only detailed Operation Cymbal forensic report is personal and remains outside this public repository.
- GitHub's default scheduled workflows execute only after the workflow is present on the default branch, and may start late.

## Negative-test record and review criteria

**Synthetic test cases** (no real secrets): allow a clean CTF overview; reject new unapproved CTF files, nested CTF paths, sensitive key-file extensions, `.env` and a synthetic private-key delimiter; skip `.git` metadata. The tests execute in isolated temporary directories.

**Acceptable merge evidence:** completed Publication Gate and Portfolio CI checks on the PR. Existing CodeQL Default Setup can be reviewed separately in Security → Code scanning. Dependency Review is currently not active and has **no PASS assertion**. Follow up after enabling the dependency graph.

No process changes, production deployment, external publication or authentication secrets are required to run these validators.
