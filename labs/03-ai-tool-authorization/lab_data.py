"""Trusted synthetic fixture loader. This is a test harness, not login code."""
from __future__ import annotations

import json
from pathlib import Path

from policy import TrustedContext

_ROOT = Path(__file__).resolve().parent / "fixtures"


def new_tickets() -> dict:
    """A fresh independent store on every call; no shared mutable fixtures."""
    return json.loads((_ROOT / "tickets.json").read_text(encoding="utf-8"))


def trusted_session(name: str) -> TrustedContext:
    """Choose identities ONLY from server-owned lab fixtures.

    CLI selection of a fixture is an explicitly simulated authenticated session.
    This is not a real authentication mechanism.
    """
    sessions = json.loads((_ROOT / "server_sessions.json").read_text(encoding="utf-8"))
    data = sessions[name]
    return TrustedContext(name, data["tenant_id"], frozenset(data["permissions"]))


def proposal(action_id: str, *, action: str = "ticket.comment",
             resource: str = "tenant-a/ticket-101", comment: str = "Synthetic review") -> dict:
    return {
        "request_id": "req-" + action_id,
        "action_id": action_id,
        "tool": "ticket_api",
        "action": action,
        "resource": resource,
        "arguments": {"comment": comment} if action == "ticket.comment" else {},
    }
