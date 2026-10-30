# Case Study 08 — Operation Cymbal: Cold Room

**Evidence-driven Threat Hunting · Incident Response · AI Security**

**Event:** Google Cloud Security Community × Hack The Box (HTB CTF)  
**Event window:** October 29–November 1, 2026  
**Environment:** Authorized simulated CTF — **not a production or employer assessment**  
**Status:** **Spoiler-free public overview; challenge solutions withheld**  
**Participant:** Gabriel Barbosa · Cybersecurity Engineer

[Português (Brasil)](README.pt-BR.md) · [Methodology](methodology.md) · [Disclosure controls](DISCLOSURE.md) · [Portfolio](../../README.md)

## Platform-reported completion

| Metric | Recorded result |
| --- | ---: |
| Scenarios completed | **3 / 3** |
| Accepted flags | **18 / 18** |
| Completion | **100%** |
| Registered team members | **1** |
| Official ranking | **Not verified** |

The outcome above was observed in the HTB event interface. The event used dynamic scoring, so no fixed point total or final position is claimed. This is **not** a Google Cloud certification, a third-party endorsement, a professional penetration test, or evidence of employer production security. Competitive prize eligibility is determined by the organizers.

**Assistance transparency:** conversational AI assisted log interpretation, technical reasoning and documentation. Conclusions were checked against the challenge telemetry and platform feedback. One registered team member does not imply an unassisted solve. Organizer rules govern competition eligibility.

## Scope: what was investigated

The three challenge tracks supported practice in these fields without exposing their questions or answers:

| Track | Public skills demonstrated |
| --- | --- |
| **Investigation** | Windows and endpoint event triage, identity telemetry, bounded timeline reconstruction |
| **Threat Hunting** | Intelligence-led hypotheses, SIEM searches and cloud / SaaS / proxy-log correlation |
| **AI Misuse** | Development-tool provenance, process genealogy, cloud-identity and CI/CD threat analysis |

**Analytical tools and data sources:** Google Security Operations (SecOps), Google Threat Intelligence (GTI), Windows/Sysmon events, HTTP proxy records and SaaS audit telemetry, within the controlled competition environment.

## Evidence-first workflow

~~~mermaid
flowchart LR
    A["Authorize scope"] --> B["Form a hypothesis"]
    B --> C["Search source telemetry"]
    C --> D["Correlate timeline"]
    D --> E["Validate competing explanations"]
    E --> F["Report confidence and limits"]
~~~

Investigation notes distinguish **OBSERVED** (direct record), **CORROBORATED** (independent supporting records), **INFERRED** (plausible, not proven) and **UNKNOWN** (insufficient evidence). A matching timestamp alone does not demonstrate a common actor; an HTTP success code alone does not validate the integrity of transferred content.

## Transferable engineering lessons

- Use threat intelligence to generate testable hypotheses, not to override actual telemetry.
- Reconcile normalized SIEM fields with raw log provenance and UTC offsets.
- Correlate identity events, process relationships, network actions and file operations while separating correlation from causation.
- Review OAuth permissions, service-account privileges and evidence of abnormal access.
- Treat developer tooling, build scripts and CI/CD identities as security boundaries.
- Document uncertainty and define measurable validation criteria before prescribing a response.

## Publication restrictions

This repository intentionally **does not** contain challenge flags, answer strings, per-flag queries, raw logs, attacker indicators, affected identifiers, scripts, detailed challenge timelines, screenshots revealing solutions or the separate private forensic report.

**Ending the event does not automatically grant permission to publish a walkthrough.** Technical disclosure requires an explicit check of HTB and event-specific terms, and any necessary organizer authorization. See [DISCLOSURE.md](DISCLOSURE.md).

This is an independent participant portfolio case, not an official Google Cloud or Hack The Box report or endorsement. FoundLab is a professional affiliation only; this controlled CTF is not presented as employer work.
