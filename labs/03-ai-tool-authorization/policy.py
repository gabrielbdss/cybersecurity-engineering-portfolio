"""Independent authorization rules for a 100% synthetic ticket system."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrustedContext:
    """Constructed only by the trusted lab harness; never parsed from AI JSON."""

    principal_id: str
    tenant_id: str
    permissions: frozenset[str]


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reason_code: str


class PolicyUnavailable(RuntimeError):
    """Policy evaluator failed to return a valid authorization decision."""


class TicketPolicy:
    """The PDP: check capability, requested resource and stored ownership."""

    def evaluate(
        self,
        context: TrustedContext,
        action: str,
        requested_resource: str,
        ticket: dict | None,
    ) -> PolicyDecision:
        if not isinstance(context, TrustedContext):
            raise PolicyUnavailable("Missing trusted context")
        resource_tenant = requested_resource.split("/", 1)[0]
        # F-01: hide whether foreign-tenant ticket IDs actually exist.
        # Return the same reason for existing and nonexistent foreign IDs.
        if resource_tenant != context.tenant_id:
            return PolicyDecision(False, "CROSS_TENANT_ACCESS")
        if ticket is None:
            return PolicyDecision(False, "RESOURCE_NOT_FOUND")
        actual_tenant = ticket.get("tenant_id")
        if actual_tenant != context.tenant_id:
            return PolicyDecision(False, "CROSS_TENANT_ACCESS")
        if action not in context.permissions:
            return PolicyDecision(False, "MISSING_PERMISSION")
        return PolicyDecision(True, "AUTHORIZED")
