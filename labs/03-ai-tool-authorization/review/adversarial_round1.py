#!/usr/bin/env python3
"""Supplementary adversarial review for the synthetic AI Action Boundary lab.

Standalone and standard-library-only. Run outside the Git repository to avoid
changing source until its findings and methodology have been reviewed.

Usage:
  python3 AI_Action_Boundary_Adversarial_Review.py /path/to/labs/03-ai-tool-authorization

This is a supplemental adversarial simulation, NOT an independent third-party
security approval, formal proof, or distributed/concurrent durability guarantee.
"""
from __future__ import annotations

import copy
import json
import sys
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 AI_Action_Boundary_Adversarial_Review.py PATH_TO_LAB03")
LAB = Path(sys.argv[1]).expanduser().resolve()
if not (LAB / "executor.py").is_file() or not (LAB / "lab_data.py").is_file():
    raise SystemExit("Lab path must contain executor.py and lab_data.py")
sys.path.insert(0, str(LAB))

from executor import TicketExecutor  # noqa: E402
from lab_data import new_tickets, proposal, trusted_session  # noqa: E402
from policy import TicketPolicy  # noqa: E402


class AdversarialReview(unittest.TestCase):
    """Checks designed separately from test_authorization.py, using public lab APIs."""

    def setUp(self):
        self.analyst = trusted_session("analyst-a")
        self.engine = TicketExecutor(new_tickets())

    def test_01_concurrent_same_id_32_workers_repeated_20_rounds(self):
        workers, rounds = 32, 20
        for iteration in range(rounds):
            engine = TicketExecutor(new_tickets())
            barrier = threading.Barrier(workers)
            payload = proposal(f"burst-{iteration}")
            before = engine.snapshot()

            def attack(_):
                barrier.wait(timeout=15)
                return engine.run(copy.deepcopy(payload), self.analyst)

            with ThreadPoolExecutor(max_workers=workers) as pool:
                results = list(pool.map(attack, range(workers)))
            self.assertEqual(sum(r["decision"] == "ALLOW" for r in results), 1)
            self.assertEqual(sum(r["reason_code"] == "REPLAY_BLOCKED" for r in results), workers - 1)
            self.assertEqual(sum(r["mutation_count_delta"] for r in results), 1)
            self.assertEqual(engine.mutation_count(), 1)
            expected = copy.deepcopy(before)
            expected["tenant-a/ticket-101"]["comments"].append("Synthetic review")
            self.assertEqual(engine.snapshot(), expected)
            self.assertEqual(len(engine.audit_events()), workers)

    def test_02_same_id_mixed_arguments_never_double_executes(self):
        workers = 24
        engine = TicketExecutor(new_tickets())
        baseline = engine.snapshot()
        barrier = threading.Barrier(workers)

        def attack(index):
            barrier.wait(timeout=15)
            return engine.run(proposal("shared-mixed", comment=f"candidate-{index}"), self.analyst)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(attack, range(workers)))
        self.assertEqual(sum(r["decision"] == "ALLOW" for r in results), 1)
        self.assertEqual(sum(r["mutation_count_delta"] for r in results), 1)
        self.assertEqual(engine.mutation_count(), 1)
        final = engine.snapshot()
        self.assertEqual(len(final["tenant-a/ticket-101"]["comments"]),
                         len(baseline["tenant-a/ticket-101"]["comments"]) + 1)
        self.assertTrue(final["tenant-a/ticket-101"]["comments"][-1].startswith("candidate-"))
        self.assertEqual(final["tenant-b/ticket-202"], baseline["tenant-b/ticket-202"])

    def test_03_concurrent_distinct_ids_each_executes_once(self):
        workers = 24
        barrier = threading.Barrier(workers)
        baseline = self.engine.snapshot()

        def action(index):
            barrier.wait(timeout=15)
            return self.engine.run(proposal(f"independent-{index}", comment=f"unique-{index}"), self.analyst)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(action, range(workers)))
        self.assertEqual(sum(r["decision"] == "ALLOW" for r in results), workers)
        self.assertEqual(self.engine.mutation_count(), workers)
        final = self.engine.snapshot()
        new_comments = final["tenant-a/ticket-101"]["comments"][len(baseline["tenant-a/ticket-101"]["comments"]):]
        self.assertEqual(set(new_comments), {f"unique-{i}" for i in range(workers)})
        self.assertEqual(final["tenant-b/ticket-202"], baseline["tenant-b/ticket-202"])

    def test_04_cross_tenant_flood_never_touches_other_tenant(self):
        workers = 24
        barrier = threading.Barrier(workers)
        baseline = self.engine.snapshot()

        def attack(index):
            barrier.wait(timeout=15)
            resource = "tenant-b/ticket-202" if index % 2 else "tenant-a/ticket-101"
            return self.engine.run(proposal(f"mixed-tenant-{index}", resource=resource,
                                            comment=f"operation-{index}"), self.analyst)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(attack, range(workers)))
        self.assertEqual(sum(r["decision"] == "ALLOW" for r in results), workers // 2)
        self.assertEqual(sum(r["reason_code"] == "CROSS_TENANT_ACCESS" for r in results), workers // 2)
        self.assertEqual(self.engine.mutation_count(), workers // 2)
        self.assertEqual(self.engine.snapshot()["tenant-b/ticket-202"], baseline["tenant-b/ticket-202"])
        for r in results:
            if r["decision"] != "ALLOW":
                self.assertEqual(r["mutation_count_delta"], 0)
                self.assertNotIn("state_before", r)
        for event in self.engine.audit_events():
            if event["decision"] != "ALLOW":
                self.assertEqual(event["state_before"], event["state_after"])

    def test_05_duplicate_nested_json_fields_fail_closed(self):
        baseline = self.engine.snapshot()
        attack = ('{"request_id":"req-nested","action_id":"nested",'
                  '"tool":"ticket_api","action":"ticket.comment",'
                  '"resource":"tenant-a/ticket-101",'
                  '"arguments":{"comment":"safe","comment":"malicious"}}')
        r = self.engine.run(attack, self.analyst)
        self.assertNotEqual(r["decision"], "ALLOW")
        self.assertEqual(r["reason_code"], "DUPLICATE_JSON_KEY")
        self.assertEqual(self.engine.snapshot(), baseline)
        self.assertEqual(self.engine.mutation_count(), 0)

    def test_06_json_nan_fail_closed(self):
        baseline = self.engine.snapshot()
        attack = ('{"request_id":"req-nan","action_id":"nan",'
                  '"tool":"ticket_api","action":"ticket.comment",'
                  '"resource":"tenant-a/ticket-101","arguments":{"comment":NaN}}')
        r = self.engine.run(attack, self.analyst)
        self.assertNotEqual(r["decision"], "ALLOW")
        self.assertEqual(r["reason_code"], "INVALID_JSON_CONSTANT")
        self.assertEqual(self.engine.snapshot(), baseline)
        self.assertEqual(self.engine.mutation_count(), 0)

    def test_07_corrupt_stored_owner_must_fail_closed(self):
        fixtures = new_tickets()
        fixtures["tenant-a/ticket-101"]["tenant_id"] = "tenant-b"
        engine = TicketExecutor(fixtures)
        before = engine.snapshot()
        r = engine.run(proposal("mismatched-owner"), self.analyst)
        self.assertEqual((r["decision"], r["reason_code"]), ("DENY", "CROSS_TENANT_ACCESS"))
        self.assertEqual(engine.mutation_count(), 0)
        self.assertEqual(engine.snapshot(), before)

    def test_08_commit_exception_never_publishes_partial_state(self):
        fixtures = new_tickets()
        fixtures["tenant-a/ticket-101"]["comments"] = None
        engine = TicketExecutor(fixtures)
        before = engine.snapshot()
        r = engine.run(proposal("broken-store"), self.analyst)
        self.assertEqual((r["decision"], r["reason_code"]), ("ERROR", "EXECUTION_ERROR"))
        self.assertEqual(r["mutation_count_delta"], 0)
        self.assertEqual(engine.mutation_count(), 0)
        self.assertEqual(engine.snapshot(), before)

    def test_09_policy_returns_non_boolean_denied(self):
        class WrongPolicy(TicketPolicy):
            def evaluate(self, *args, **kwargs):
                from policy import PolicyDecision
                return PolicyDecision("yes", "AUTHORIZED")

        engine = TicketExecutor(new_tickets(), policy=WrongPolicy())
        before = engine.snapshot()
        r = engine.run(proposal("non-bool"), self.analyst)
        self.assertEqual(r["decision"], "ERROR")
        self.assertEqual(r["reason_code"], "POLICY_UNAVAILABLE")
        self.assertEqual(engine.snapshot(), before)
        self.assertEqual(engine.mutation_count(), 0)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]], verbosity=2)
