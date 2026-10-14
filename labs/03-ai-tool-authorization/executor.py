"""Independent PEP and isolated in-memory ticket mutation target.

Only cooperating threads sharing one TicketExecutor instance are protected.
This is NOT a distributed or crash-durable transaction system.
"""
from __future__ import annotations

import copy
import json
import re
import threading
from dataclasses import dataclass
from typing import Callable

from policy import PolicyDecision, PolicyUnavailable, TicketPolicy, TrustedContext

_ID = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
_RESOURCE = re.compile(r"[a-z0-9-]{1,64}/[a-z0-9-]{1,64}\Z")
_FIELDS = frozenset({"request_id", "action_id", "tool", "action", "resource", "arguments"})
_UNTRUSTED_AUTHORITY_FIELDS = frozenset({"principal_id", "tenant_id", "permissions", "override", "admin"})
_ACTIONS = frozenset({"ticket.comment", "ticket.delete"})
_MAX_JSON = 16_384


class BadProposal(ValueError):
    def __init__(self, reason_code: str):
        self.reason_code = reason_code
        super().__init__(reason_code)


@dataclass(frozen=True, slots=True)
class Action:
    """Immutable snapshot of untrusted proposal fields, after strict validation."""

    request_id: str
    action_id: str
    tool: str
    name: str
    resource: str
    comment: str | None


def _reject_duplicate_keys(items: list[tuple[str, object]]) -> dict:
    result = {}
    for name, value in items:
        if name in result:
            raise BadProposal("DUPLICATE_JSON_KEY")
        result[name] = value
    return result


def _reject_constant(value: str) -> None:
    raise BadProposal("INVALID_JSON_CONSTANT")


def parse_proposal(raw: dict | str) -> Action:
    """Reject ambiguous/privileged inputs; snapshot all effect-relevant values."""
    if isinstance(raw, str):
        if len(raw) > _MAX_JSON:
            raise BadProposal("JSON_TOO_LARGE")
        try:
            data = json.loads(
                raw,
                object_pairs_hook=_reject_duplicate_keys,
                parse_constant=_reject_constant,
            )
        except (json.JSONDecodeError, UnicodeError, RecursionError) as exc:
            raise BadProposal("INVALID_JSON") from exc
    else:
        data = raw
    if not isinstance(data, dict):
        raise BadProposal("INVALID_SHAPE")
    if _UNTRUSTED_AUTHORITY_FIELDS.intersection(data):
        raise BadProposal("UNTRUSTED_AUTHORITY_FIELD")
    if set(data) != _FIELDS:
        raise BadProposal("INVALID_FIELDS")
    if any(type(data[k]) is not str or not _ID.fullmatch(data[k]) for k in ("request_id", "action_id")):
        raise BadProposal("INVALID_IDENTIFIER")
    if type(data["tool"]) is not str or data["tool"] != "ticket_api":
        raise BadProposal("UNSUPPORTED_TOOL")
    if type(data["action"]) is not str or data["action"] not in _ACTIONS:
        raise BadProposal("UNSUPPORTED_OPERATION")
    if type(data["resource"]) is not str or not _RESOURCE.fullmatch(data["resource"]):
        raise BadProposal("INVALID_RESOURCE")
    arguments = data["arguments"]
    if type(arguments) is not dict:
        raise BadProposal("INVALID_ARGUMENTS")
    if data["action"] == "ticket.comment":
        if set(arguments) != {"comment"} or type(arguments["comment"]) is not str:
            raise BadProposal("INVALID_ARGUMENTS")
        if not (1 <= len(arguments["comment"]) <= 280) or not arguments["comment"].strip():
            raise BadProposal("INVALID_COMMENT")
        comment = arguments["comment"]
    else:
        if arguments:
            raise BadProposal("INVALID_ARGUMENTS")
        comment = None
    return Action(data["request_id"], data["action_id"], data["tool"],
                  data["action"], data["resource"], comment)


class TicketExecutor:
    """PEP: check, authorize, prevent replay, and commit while holding one lock.

    Under the lock we build fresh copies before publishing them. All mutable
    protected ticket state is owned by this instance. Audit entries are allowed
    even for DENY/ERROR; they are not mutations of protected ticket resources.
    """

    def __init__(self, tickets: dict, policy: TicketPolicy | None = None):
        self._lock = threading.RLock()
        self._tickets = copy.deepcopy(tickets)
        self._used_action_ids: frozenset[str] = frozenset()
        self._mutation_count = 0
        self._audit: list[dict] = []
        self._policy = policy if policy is not None else TicketPolicy()

    def snapshot(self) -> dict:
        """PRIVILEGED LOCAL HARNESS ONLY: full synthetic protected state.

        Never expose this accessor to an agent/client or unauthenticated API.
        """
        with self._lock:
            return copy.deepcopy(self._tickets)

    def mutation_count(self) -> int:
        with self._lock:
            return self._mutation_count

    def audit_events(self) -> list[dict]:
        """PRIVILEGED REVIEWER ACCESS ONLY: full, cross-tenant audit snapshots.

        The standalone lab has no real authentication layer. In production this
        method must be kept behind server-side reviewer access control.
        """
        with self._lock:
            return copy.deepcopy(self._audit)

    def run(
        self,
        proposal: dict | str,
        context: TrustedContext,
        *,
        _trusted_test_after_check: Callable[[], None] | None = None,
    ) -> dict:
        """Return only an agent-safe decision; retain full evidence internally.

        The optional hook belongs ONLY to trusted adversarial unit tests. It
        simulates a changed source proposal after PDP ALLOW, before any effect.
        It MUST NOT be exposed to the agent, a web endpoint, or plugin data.
        """
        with self._lock:
            before = copy.deepcopy(self._tickets)
            initial_count = self._mutation_count
            action: Action | None = None
            decision, reason, executed = "ERROR", "INVALID_PROPOSAL", False
            try:
                action = parse_proposal(proposal)
                if not isinstance(context, TrustedContext):
                    raise PolicyUnavailable("Trusted session required")
                if action.action_id in self._used_action_ids:
                    decision, reason = "DENY", "REPLAY_BLOCKED"
                else:
                    try:
                        verdict = self._policy.evaluate(
                            context, action.name, action.resource,
                            copy.deepcopy(self._tickets.get(action.resource)),
                        )
                    except Exception as exc:
                        raise PolicyUnavailable("PDP failed") from exc
                    if type(verdict) is not PolicyDecision or type(verdict.allowed) is not bool:
                        raise PolicyUnavailable("PDP returned invalid decision")
                    if not verdict.allowed:
                        decision, reason = "DENY", verdict.reason_code
                    else:
                        if _trusted_test_after_check is not None:
                            _trusted_test_after_check()
                        # Fail closed if the submitted operation has changed
                        # since its authorization. The effect uses 'action', never
                        # the untrusted dict, and cannot be redirected by mutation.
                        try:
                            current = parse_proposal(proposal)
                        except BadProposal:
                            current = None
                        if current != action:
                            decision, reason = "DENY", "OPERATION_CHANGED"
                        else:
                            candidate = copy.deepcopy(self._tickets)
                            if action.name == "ticket.comment":
                                candidate[action.resource]["comments"].append(action.comment)
                            elif action.name == "ticket.delete":
                                del candidate[action.resource]
                            else:
                                raise AssertionError("Unreachable validated action")
                            next_used = self._used_action_ids | {action.action_id}
                            # No external I/O and no callback during the commit.
                            # Cooperating threads cannot observe partial state.
                            self._tickets = candidate
                            self._used_action_ids = next_used
                            self._mutation_count += 1
                            decision, reason, executed = "ALLOW", "AUTHORIZED", True
            except BadProposal as exc:
                decision = "DENY" if exc.reason_code == "UNTRUSTED_AUTHORITY_FIELD" else "ERROR"
                reason = exc.reason_code
            except PolicyUnavailable:
                decision, reason = "ERROR", "POLICY_UNAVAILABLE"
            except Exception:
                # Unexpected faults must never fall back to an ALLOW result.
                decision, reason = "ERROR", "EXECUTION_ERROR"

            after = copy.deepcopy(self._tickets)
            # A safely shaped untrusted identifier may label a rejected request
            # for correlation, but never becomes proof of authority.
            safe_request_id = action.request_id if action else None
            safe_action_id = action.action_id if action else None
            if action is None and isinstance(proposal, dict):
                for label in ("request_id", "action_id"):
                    candidate_id = proposal.get(label)
                    if type(candidate_id) is str and _ID.fullmatch(candidate_id):
                        if label == "request_id":
                            safe_request_id = candidate_id
                        else:
                            safe_action_id = candidate_id
            event = {
                "request_id": safe_request_id,
                "action_id": safe_action_id,
                "trusted_principal_id": context.principal_id if isinstance(context, TrustedContext) else None,
                "trusted_tenant_id": context.tenant_id if isinstance(context, TrustedContext) else None,
                "decision": decision,
                "reason_code": reason,
                "executed": executed,
                "mutation_count_delta": self._mutation_count - initial_count,
                "target_before": before.get(action.resource) if action else None,
                "target_after": after.get(action.resource) if action else None,
                "state_before": before,
                "state_after": after,
            }
            # F-01 (2026-10-12): privileged evidence MUST NOT escape via the
            # agent-facing return path, even after an attempted cross-tenant
            # access. No ticket content or trusted identity leaves run().
            self._audit.append(copy.deepcopy(event))
            return {
                "request_id": safe_request_id,
                "action_id": safe_action_id,
                "decision": decision,
                "reason_code": reason,
                "executed": executed,
                "mutation_count_delta": event["mutation_count_delta"],
            }
