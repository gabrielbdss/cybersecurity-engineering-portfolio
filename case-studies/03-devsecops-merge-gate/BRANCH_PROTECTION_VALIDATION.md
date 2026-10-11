# Branch Protection & CI/CD Security Gate — Public Validation

**Security engineering evidence | 11 October 2026 | Personal public GitHub portfolio**

## Objective

Prevent unvalidated changes from reaching the protected `main` branch. A passing CI workflow alone is insufficient if branch governance does not require it.

## Scope and privacy

This case is based **only on the public portfolio repository** `gabrielbdss/cybersecurity-engineering-portfolio`. It does not describe or reproduce any FoundLab project, architecture, workflow, ticket, secret or internal security finding.

## Implemented controls

The repository's active ruleset `Main Branch Security Gate` targets the default branch and requires:

- Changes through a Pull Request before merging; zero required human approvals for this single-maintainer portfolio.
- Both GitHub Actions jobs, `Validate merge-gate lab` and `Validate synthetic cloud-security labs`, to pass.
- An up-to-date PR branch with respect to the latest base branch.
- Protection against branch deletion and non-fast-forward/force pushes.
- No configured bypass actors.

**Verification boundary:** The GitHub API reported `protected: true` and an active default-branch ruleset with these controls. This is a configuration observation, not proof against every possible administrative or platform-level bypass.

## Negative validation — PR #4

**Test strategy:** Create a separate branch with an intentionally failing Python unit test inside the existing lab test-discovery path. Open a PR to `main` without merging it. Inspect required CI jobs and the PR mergeability state.

**Public, reproducible evidence:**

| Evidence | Observation | Link |
|---|---|---|
| [Pull Request #4](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/pull/4) | Deliberately failing test; PR closed **without merge** | [PR #4](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/pull/4) |
| [GitHub Actions run 38149828330](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/actions/runs/38149828330) | Overall run **FAILURE** as intentionally designed | [CI evidence](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/actions/runs/38149828330) |
| Required job: `Validate synthetic cloud-security labs` | **FAILURE**; the incident-triage regression step contained the intentional failing test | [Job details](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/actions/runs/38149828330) |
| Required job: `Validate merge-gate lab` | **SUCCESS**; passing one required job was insufficient | [Run details](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/actions/runs/38149828330) |
| [Main branch](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/tree/main) | Remained at pre-test commit `b5108d46fd980d14729261c6866a0d5856f8ca39` during the negative test | [Source](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio) |

GitHub reported the test PR's mergeability state as **blocked** after the required job failed. The PR was later closed without merging, preserving `main`. **No attempt was made to bypass the rule or force a merge.**

## Positive control

Previously, both required jobs completed successfully on the production-independent public portfolio [main CI run 38135077892](https://github.com/gabrielbdss/cybersecurity-engineering-portfolio/actions/runs/38135077892). This demonstrates that the checks can pass on valid portfolio content. It is **not** a separate positive PR merge test under the newly enabled ruleset; that end-to-end test remains an optional next step.

## CI/CD concepts

- **CI (Continuous Integration):** Run automated tests for changes pushed or proposed through PRs.
- **CD (Continuous Delivery/Deployment):** Additional stages to prepare or deploy releases. This portfolio does **not** demonstrate an automated production deployment.
- **Pipeline:** Workflow-defined sequence of jobs and steps; here, GitHub Actions executes Python test suites and fixture smoke checks.
- **Required status checks:** GitHub branch governance evaluates named CI job results.
- **Ruleset / branch protection:** Repository-level enforcement that prevents merges when conditions are unsatisfied.
- **Fail-closed negative test:** Intentionally fail an obligatory job and demonstrate that an unsafe PR remains unmerged.

## Result and limits

**VERIFIED in public GitHub metadata:** active ruleset, required job configurations, one successful historical main run, one failed negative PR run, merge-blocked state, and closure without merge.

**NOT CLAIMED:** a comprehensive penetration test of GitHub, prevention of every administrative/platform bypass, a production application deployment, or testing of any employer system.

This is a public repository governance case study, complementary to the [synthetic Merge Gate evaluator](../../labs/04-devsecops-merge-gate/README.md), rather than a reproduction of an employer pipeline.
