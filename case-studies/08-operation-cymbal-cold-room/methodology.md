# Investigation Methodology — No-Spoiler Learning Notes

**Environment:** Authorized, simulated CTF. **Publication:** Method only; no answers or challenge-specific indicators.

## Phase 1 — Scope

Read the scenario's authorized boundaries. Note the central investigative question, available source systems and date range. Avoid changes to remote systems: the lab work in this case consisted of read-only telemetry interpretation and submission to the competition platform.

## Phase 2 — Intelligence to hypothesis

Use threat reports and detections to define observable behaviors. A threat-actor name or technique tag is a starting hypothesis, **not attribution proof**. Ask what independent record would support or falsify it.

## Phase 3 — Normalized and raw evidence

Review normalized SIEM event labels for discovery, then inspect raw source fields when the answer depends on exact identities, file actions or command lines. Retain source application, event type, clock basis and source/target semantics.

## Phase 4 — Build bounded timelines

Establish temporal order before proposing cause and effect. When UI display timestamps differ from source UTC timestamps, preserve both and explicitly identify the clock basis. Seek independent record types to confirm a sequence.

## Phase 5 — Confidence grading

| Classification | Meaning |
| --- | --- |
| OBSERVED | A source record directly states the event or value |
| CORROBORATED | A separate source independently supports the claim |
| INFERRED | Evidence is suggestive, but one or more links remain unproven |
| UNKNOWN | Available evidence is insufficient |

A process launch can support that a command ran without proving the intended effect; a file-write event does not automatically prove the prior content or persistence success; a successful HTTP response does not prove full receiver-side validation.

## Phase 6 — Cross-incident correlation

Compare generic factors (technique, identity abuse, staging, cloud-facing activity) separately from distinctive identifiers. Do **not** equate a common detection category with one common operator. A shared-actor claim would require specific bridging evidence and consideration of competing explanations.

## Phase 7 — Communicate and learn

For each technical hypothesis, capture privately: **question → query purpose → source → observed fact → confidence → alternative explanation → defensive implication**. Share only generalized lessons while disclosure restrictions are active.

## Safe analytical practice

This portfolio does not contain or execute real attack scripts, the challenge's query strings, flags, tokens, secrets, exfiltration destinations, or confidential telemetry. All detailed personal learning artifacts are maintained outside this public repository.

[Back to case study](README.md) · [Disclosure policy](DISCLOSURE.md)
