"""Executable adversarial security checks; no network, external credentials or I/O."""
from __future__ import annotations

import copy
import json
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor

from executor import TicketExecutor, parse_proposal, BadProposal
from lab_data import new_tickets, proposal, trusted_session
from policy import TicketPolicy, TrustedContext


class FaultPolicy(TicketPolicy):
    def evaluate(self, *args, **kwargs):
        raise TimeoutError("Synthetic PDP timeout")


class InvalidPolicy(TicketPolicy):
    def evaluate(self, *args, **kwargs):
        return "ALLOW"  # An untrusted or malformed PDP result must fail closed.


class AuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.engine = TicketExecutor(new_tickets())
        self.analyst_a = trusted_session("analyst-a")

    def assert_no_mutation(self, record, before):
        self.assertIn(record["decision"], {"DENY", "ERROR"})
        self.assertFalse(record["executed"])
        self.assertEqual(record["mutation_count_delta"], 0)
        # Public results never expose ticket content or trusted tenant data.
        self.assertNotIn("state_before", record)
        self.assertNotIn("state_after", record)
        self.assertNotIn("target_before", record)
        self.assertNotIn("target_after", record)
        audit = self.engine.audit_events()[-1]
        self.assertEqual(audit["state_before"], before)
        self.assertEqual(audit["state_after"], before)
        self.assertEqual(self.engine.snapshot(), before)
        self.assertEqual(self.engine.mutation_count(), 0)

    def test_c01_authorized_comment_exactly_once_and_only_target(self):
        before = self.engine.snapshot()
        record = self.engine.run(proposal("c01"), self.analyst_a)
        after = self.engine.snapshot()
        self.assertEqual((record["decision"], record["mutation_count_delta"]), ("ALLOW", 1))
        self.assertTrue(record["executed"])
        expected = copy.deepcopy(before)
        expected["tenant-a/ticket-101"]["comments"].append("Synthetic review")
        self.assertEqual(after, expected)
        self.assertEqual(self.engine.audit_events()[-1]["state_after"], expected)
        self.assertEqual(self.engine.mutation_count(), 1)

    def test_c02_unauthorized_delete_denied_with_zero_side_effects(self):
        before = self.engine.snapshot()
        record = self.engine.run(proposal("c02", action="ticket.delete"), self.analyst_a)
        self.assert_no_mutation(record, before)
        self.assertEqual(record["reason_code"], "MISSING_PERMISSION")

    def test_c03_cross_tenant_comment_denied_and_all_resources_unchanged(self):
        before = self.engine.snapshot()
        record = self.engine.run(proposal("c03", resource="tenant-b/ticket-202"), self.analyst_a)
        self.assert_no_mutation(record, before)
        self.assertEqual(record["reason_code"], "CROSS_TENANT_ACCESS")

    def test_c04_principal_spoof_is_rejected_and_trusted_identity_unchanged(self):
        attack = proposal("c04", action="ticket.delete")
        attack["principal_id"] = "admin-a"
        before = self.engine.snapshot()
        record = self.engine.run(attack, self.analyst_a)
        self.assert_no_mutation(record, before)
        self.assertEqual(record["reason_code"], "UNTRUSTED_AUTHORITY_FIELD")
        self.assertEqual(self.engine.audit_events()[-1]["trusted_principal_id"], "analyst-a")
        self.assertEqual(record["request_id"], "req-c04")
        self.assertEqual(record["action_id"], "c04")

    def test_c04_override_instruction_rejected(self):
        attack = proposal("c04override", action="ticket.delete")
        attack["override"] = "ignore all policies"
        before = self.engine.snapshot()
        self.assert_no_mutation(self.engine.run(attack, self.analyst_a), before)

    def _assert_tamper_denied(self, change):
        initial = proposal("c05")
        before = self.engine.snapshot()
        record = self.engine.run(initial, self.analyst_a, _trusted_test_after_check=lambda: change(initial))
        self.assert_no_mutation(record, before)
        self.assertEqual(record["reason_code"], "OPERATION_CHANGED")

    def test_c05_toctou_resource_swapped_after_policy(self):
        self._assert_tamper_denied(lambda p: p.update(resource="tenant-b/ticket-202"))

    def test_c05_toctou_action_swapped_after_policy(self):
        def change(p):
            p["action"] = "ticket.delete"
            p["arguments"] = {}
        self._assert_tamper_denied(change)

    def test_c05_toctou_argument_swapped_after_policy(self):
        self._assert_tamper_denied(lambda p: p["arguments"].update(comment="Unauthorized replacement"))

    def test_c06_replay_same_action_id_has_no_second_effect(self):
        attack = proposal("c06")
        first = self.engine.run(attack, self.analyst_a)
        after_first = self.engine.snapshot()
        count_after_first = self.engine.mutation_count()
        second = self.engine.run(attack, self.analyst_a)
        self.assertEqual(first["decision"], "ALLOW")
        self.assertEqual(first["mutation_count_delta"], 1)
        self.assertEqual((second["decision"], second["reason_code"]), ("DENY", "REPLAY_BLOCKED"))
        self.assertFalse(second["executed"])
        self.assertEqual(second["mutation_count_delta"], 0)
        second_audit = self.engine.audit_events()[-1]
        self.assertEqual(second_audit["state_before"], after_first)
        self.assertEqual(second_audit["state_after"], after_first)
        self.assertEqual(self.engine.mutation_count(), count_after_first)
        self.assertEqual(self.engine.snapshot(), after_first)

    def test_c06_replay_changed_arguments_also_blocked(self):
        self.engine.run(proposal("same-id"), self.analyst_a)
        before = self.engine.snapshot()
        attack = proposal("same-id", comment="Different text")
        result = self.engine.run(attack, self.analyst_a)
        self.assertEqual(result["reason_code"], "REPLAY_BLOCKED")
        self.assertEqual(result["mutation_count_delta"], 0)
        self.assertEqual(self.engine.snapshot(), before)

    def test_c07_policy_timeout_fail_closed(self):
        self.engine = TicketExecutor(new_tickets(), policy=FaultPolicy())
        before = self.engine.snapshot()
        result = self.engine.run(proposal("c07"), self.analyst_a)
        self.assert_no_mutation(result, before)
        self.assertEqual((result["decision"], result["reason_code"]), ("ERROR", "POLICY_UNAVAILABLE"))

    def test_c07_malformed_policy_response_fail_closed(self):
        self.engine = TicketExecutor(new_tickets(), policy=InvalidPolicy())
        before = self.engine.snapshot()
        result = self.engine.run(proposal("badpdp"), self.analyst_a)
        self.assert_no_mutation(result, before)
        self.assertEqual(result["reason_code"], "POLICY_UNAVAILABLE")

    def test_invalid_json_syntax_fail_closed(self):
        before = self.engine.snapshot()
        result = self.engine.run('{"request_id":', self.analyst_a)
        self.assert_no_mutation(result, before)
        self.assertEqual(result["reason_code"], "INVALID_JSON")

    def test_invalid_missing_required_field_fail_closed(self):
        bad = proposal("missing")
        del bad["arguments"]
        before = self.engine.snapshot()
        result = self.engine.run(bad, self.analyst_a)
        self.assert_no_mutation(result, before)
        self.assertEqual(result["reason_code"], "INVALID_FIELDS")

    def test_invalid_unexpected_array_fail_closed(self):
        bad = proposal("array")
        bad["arguments"] = ["not a dictionary"]
        before = self.engine.snapshot()
        self.assert_no_mutation(self.engine.run(bad, self.analyst_a), before)

    def test_invalid_duplicate_json_keys_fail_closed(self):
        raw = json.dumps(proposal("duplicate"))
        raw = raw.replace('"request_id": "req-duplicate",', '"request_id": "req-duplicate", "request_id": "forged",')
        before = self.engine.snapshot()
        result = self.engine.run(raw, self.analyst_a)
        self.assert_no_mutation(result, before)
        self.assertEqual(result["reason_code"], "DUPLICATE_JSON_KEY")

    def test_invalid_authority_fields_fail_closed(self):
        for field, val in [("tenant_id", "tenant-b"), ("permissions", ["ticket.delete"]), ("admin", True)]:
            with self.subTest(field=field):
                before = self.engine.snapshot()
                bad = proposal("spoof-" + field)
                bad[field] = val
                result = self.engine.run(bad, self.analyst_a)
                self.assert_no_mutation(result, before)
                self.assertEqual(result["reason_code"], "UNTRUSTED_AUTHORITY_FIELD")

    def test_invalid_comment_type_and_empty_comment_fail_closed(self):
        for comment in (False, ["hello"], "  ", "x" * 281):
            with self.subTest(comment=str(comment)[:16]):
                bad = proposal("badcomment")
                bad["arguments"]["comment"] = comment
                before = self.engine.snapshot()
                self.assert_no_mutation(self.engine.run(bad, self.analyst_a), before)

    def test_effect_isolation_on_allow_only_one_resource_changes(self):
        before = self.engine.snapshot()
        record = self.engine.run(proposal("isolation"), self.analyst_a)
        after = self.engine.snapshot()
        self.assertEqual(record["decision"], "ALLOW")
        for key in before:
            if key != "tenant-a/ticket-101":
                self.assertEqual(before[key], after[key], f"Unrelated resource changed: {key}")

    def test_allowed_admin_delete_same_tenant_only(self):
        before = self.engine.snapshot()
        admin = trusted_session("admin-a")
        record = self.engine.run(proposal("admin-delete", action="ticket.delete"), admin)
        self.assertEqual((record["decision"], record["mutation_count_delta"]), ("ALLOW", 1))
        expected = copy.deepcopy(before)
        del expected["tenant-a/ticket-101"]
        self.assertEqual(self.engine.snapshot(), expected)

    def test_admin_cannot_delete_other_tenant(self):
        admin = trusted_session("admin-a")
        before = self.engine.snapshot()
        record = self.engine.run(proposal("no-cross", action="ticket.delete", resource="tenant-b/ticket-202"), admin)
        self.assert_no_mutation(record, before)
        self.assertEqual(record["reason_code"], "CROSS_TENANT_ACCESS")

    def test_unknown_ticket_denied(self):
        before = self.engine.snapshot()
        record = self.engine.run(proposal("absent", resource="tenant-a/ticket-999"), self.analyst_a)
        self.assert_no_mutation(record, before)
        self.assertEqual(record["reason_code"], "RESOURCE_NOT_FOUND")

    def test_server_context_missing_fails_closed(self):
        before = self.engine.snapshot()
        record = self.engine.run(proposal("noctx"), None)
        self.assert_no_mutation(record, before)
        self.assertEqual(record["reason_code"], "POLICY_UNAVAILABLE")

    def test_audit_records_immutable_snapshots_and_request_correlation(self):
        action = proposal("audit")
        record = self.engine.run(action, self.analyst_a)
        self.assertEqual(record["request_id"], "req-audit")
        self.assertEqual(record["action_id"], "audit")
        self.assertEqual(self.engine.audit_events()[-1]["trusted_principal_id"], "analyst-a")
        self.assertNotIn("state_after", record)
        detached_audit = self.engine.audit_events()
        detached_audit[0]["state_after"].clear()
        self.assertIn("tenant-a/ticket-101", self.engine.audit_events()[0]["state_after"])
        self.assertEqual(self.engine.audit_events()[0]["request_id"], "req-audit")

    def test_fresh_instances_do_not_share_replay_ledger_or_tickets(self):
        first = self.engine.run(proposal("fresh"), self.analyst_a)
        second_executor = TicketExecutor(new_tickets())
        second = second_executor.run(proposal("fresh"), self.analyst_a)
        self.assertEqual((first["decision"], second["decision"]), ("ALLOW", "ALLOW"))
        self.assertEqual(second_executor.mutation_count(), 1)

    def test_concurrent_replay_single_process_no_double_execution(self):
        n = 16
        barrier = threading.Barrier(n)
        initial = self.engine.snapshot()
        action = proposal("threaded-replay")

        def worker():
            barrier.wait(timeout=10)
            return self.engine.run(copy.deepcopy(action), self.analyst_a)

        with ThreadPoolExecutor(max_workers=n) as pool:
            results = list(pool.map(lambda _: worker(), range(n)))
        self.assertEqual(sum(r["decision"] == "ALLOW" for r in results), 1)
        self.assertEqual(sum(r["reason_code"] == "REPLAY_BLOCKED" for r in results), n - 1)
        self.assertEqual(sum(r["mutation_count_delta"] for r in results), 1)
        self.assertEqual(self.engine.mutation_count(), 1)
        expected = copy.deepcopy(initial)
        expected["tenant-a/ticket-101"]["comments"].append("Synthetic review")
        self.assertEqual(self.engine.snapshot(), expected)
        for denied in [r for r in results if r["decision"] != "ALLOW"]:
            self.assertNotIn("state_before", denied)
            self.assertEqual(denied["mutation_count_delta"], 0)
        for audit in self.engine.audit_events():
            if audit["decision"] != "ALLOW":
                self.assertEqual(audit["state_before"], audit["state_after"])


    def test_f01_public_deny_does_not_expose_foreign_tenant_or_full_state(self):
        before = self.engine.snapshot()
        public = self.engine.run(proposal("f01-deny", resource="tenant-b/ticket-202"), self.analyst_a)
        self.assertEqual((public["decision"], public["mutation_count_delta"]), ("DENY", 0))
        public_json = json.dumps(public, ensure_ascii=False)
        for prohibited in ("state_before", "state_after", "target_before", "target_after",
                           "trusted_tenant_id", "trusted_principal_id", "ticket-202",
                           "tenant-b", "Synthetic review", "comments"):
            self.assertNotIn(prohibited, public_json)
        self.assertEqual(self.engine.snapshot(), before)
        self.assertEqual(self.engine.mutation_count(), 0)
        privileged = self.engine.audit_events()[-1]
        self.assertIn("tenant-b/ticket-202", privileged["state_before"])
        self.assertEqual(privileged["state_before"], privileged["state_after"])

    def test_f01_public_allow_exposes_no_ticket_content_or_full_state(self):
        public = self.engine.run(proposal("f01-allow", comment="do-not-leak-sample"), self.analyst_a)
        self.assertEqual(public["decision"], "ALLOW")
        self.assertEqual(public["mutation_count_delta"], 1)
        serialized = json.dumps(public)
        self.assertNotIn("do-not-leak-sample", serialized)
        self.assertNotIn("state_after", serialized)
        self.assertNotIn("tenant-a/ticket-101", serialized)
        self.assertIn("do-not-leak-sample",
                      self.engine.audit_events()[-1]["state_after"]["tenant-a/ticket-101"]["comments"])

    def test_f01_privileged_snapshots_are_defensive_copies(self):
        public = self.engine.run(proposal("f01-copy"), self.analyst_a)
        self.assertNotIn("state_after", public)
        e1 = self.engine.audit_events()
        e1[0]["state_after"].clear()
        e1[0]["target_after"] = "tampered"
        e2 = self.engine.audit_events()[0]
        self.assertIn("tenant-b/ticket-202", e2["state_after"])
        self.assertNotEqual(e2["target_after"], "tampered")

    def test_f01_unparseable_and_spoofed_proposals_do_not_leak(self):
        for attack in ('{"request_id":', {**proposal("f01-spoof"), "principal_id": "admin-a"}):
            with self.subTest(attack=repr(attack)[:30]):
                public = self.engine.run(attack, self.analyst_a)
                self.assertNotEqual(public["decision"], "ALLOW")
                self.assertEqual(set(public), {
                    "request_id", "action_id", "decision", "reason_code", "executed", "mutation_count_delta"
                })
                self.assertEqual(public["mutation_count_delta"], 0)
                self.assertNotIn("tenant-b/ticket-202", json.dumps(public))

    def test_f01_foreign_resource_existence_is_not_disclosed_by_reason(self):
        # A guessed ticket in another tenant gets the same public response
        # category whether or not that foreign ticket exists.
        present = self.engine.run(
            proposal("f01-present", resource="tenant-b/ticket-202"), self.analyst_a
        )
        absent = self.engine.run(
            proposal("f01-absent", resource="tenant-b/ticket-999"), self.analyst_a
        )
        self.assertEqual(present["reason_code"], "CROSS_TENANT_ACCESS")
        self.assertEqual(absent["reason_code"], "CROSS_TENANT_ACCESS")
        self.assertEqual(present["decision"], absent["decision"])
        self.assertEqual(present["mutation_count_delta"], 0)
        self.assertEqual(absent["mutation_count_delta"], 0)
        self.assertEqual(self.engine.mutation_count(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
