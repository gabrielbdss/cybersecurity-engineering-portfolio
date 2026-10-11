# Project Lumen — Executed Application Security Assessment (Sanitized Public Edition)

**Author:** Gabriel Barbosa · Cybersecurity Engineer  
**Classification:** Public, anonymized case study  
**Evidence source:** An application security assessment **actually performed** against a privately held codebase. Primary evidence is confidential; there are no raw private artifacts in this repository.

> **Important:** “Project Lumen” is an invented public codename. It is not the name, architecture or release of the actual assessed application. The detailed report and scanner evidence are not public. Conceptual diagrams in the PDF are newly drawn illustrations, not depictions of the private system.

## Public report

[**Project Lumen — Application Security Assessment (14-page PDF)**](Projeto_Lumen_AppSec_Assessment_Real_Sanitizado.pdf)

The PDF is the full formatted portfolio deliverable. This Markdown summary explains the evidence boundary and makes the engineering methods accessible to code reviewers. **The sanitized 14-page PDF is included alongside this summary in the public case-study folder.**

## 1. Scope and work actually performed

The underlying real assessment included:

| Workstream | Performed activity | Public claim / limitation |
|---|---|---|
| SAST | Semgrep runs using general, security-focused and secrets-oriented rule sets | Alerts were reviewed against actual source; no proprietary code or scanner output is released |
| SCA | Trivy scan of dependency inventory and advisories | Dependencies requiring attention were identified; installed version does **not** alone prove reachability or exploitation |
| Authentication and authorization | Directed inspection of session/auth flows and configuration-sensitive behavior | A configuration-dependent concern was identified in source; actual production configuration was **not** established by this assessment |
| Multi-tenancy | Inspection of identity propagation, tenant boundaries and relevant existing test evidence | Controls were observed in reviewed code/tests; no universal isolation claim |
| AI / agent security | Review of tool authorization, trust boundaries and high-impact approval controls | A credential/authority design question was documented; unauthorized privilege escalation was **not** demonstrated |
| CI/CD and supply chain | Review of workflow hardening and dependency governance | Hardening recommendations were documented, not represented as already remediated |
| Manual triage | Investigation of automated warnings and relevant controls | Scanner alerts were not automatically promoted into confirmed vulnerabilities |

**Operational boundary:** This was a directed, primarily code-focused security assessment. The full application test suite was not executed as part of this assessment, live production behavior was not exhaustively reproduced, and no destructive production exploitation is claimed.

## 2. Evidence-based distinctions

- **Source-observed**: an implementation or configuration-dependent path was identified in the code reviewed.
- **Tool-observed**: SAST/SCA produced alerts over the examined inputs; coverage depends on rules and files actually processed.
- **Contextually reviewed**: the analyst inspected controls and test examples to triage scanner findings.
- **Not established**: deployed-state applicability, active exploitation, compromise, full-path reachability or successful remediation where supporting tests were absent.

These distinctions prevent the misleading claim that every scanner alert is an exploitable production vulnerability.

## 3. Sanitized result categories

| Category | Defensible result | What is not claimed |
|---|---|---|
| Authentication | Configuration-dependent security concern in code | The production system was running in that state |
| Dependencies | Advisories detected; update and regression review recommended | A vulnerability was reachable or exploited |
| AI privilege boundaries | Trust and tool authorization design reviewed | Confirmed privilege escalation |
| Pipeline and supply chain | Hardening opportunities | Confirmed compromise |
| Existing security controls | Specific code/tests provided corroborating evidence | System-wide security assurance |

The exact weak conditions, identifiers, endpoints, source locations, dependency versions, evidence screenshots and counts have been omitted to avoid exposing proprietary system details or active remediation context.

## 4. Remediation strategy recorded

1. Ensure configuration-dependent protected paths fail closed.
2. Prioritize dependency updates by actual applicability, version compatibility and regressions.
3. Review token/workload privilege boundaries and policy-controlled tool execution.
4. Reduce CI permissions and strengthen source/third-party action and dependency governance.
5. Perform an authorized retest after fixes, including both positive and negative conditions.
6. Preserve an evidence manifest and document unresolved claims explicitly.

These are **recommendations made by the assessment**, not proof that private infrastructure was modified or remediated.

## 5. Privacy and provenance

This public summary follows the author's requested confidentiality boundary:

- No employer, product, customer, private repo name or proprietary architecture is disclosed here.
- No raw source, API endpoints, secrets, tokens, login or internal role design is disclosed.
- Illustrations are **generic**, but the **assessment activity was real**.
- Supporting raw evidence remains restricted, so outside reviewers cannot independently reproduce findings from this public document.
- There is no client, employer or third-party signature attached; no certification or approval of the original target's security is implied.

## 6. Related public demonstrations

- [AI security laboratory and trust-boundary model](README.md): wholly synthetic AI adversarial testing methodology.
- [Public branch protection validation](../03-devsecops-merge-gate/BRANCH_PROTECTION_VALIDATION.md): separately inspectable real test of this personal public repository.
- [Dependency vulnerability triage](../06-dependency-vulnerability-triage/README.md): vendor-neutral explanation of advisory and reachability analysis.

**Engineering lesson:** *The tools produce signals; a security assessment explains their context, evidence quality, limitations and a safe validation plan.*
