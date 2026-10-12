"""CLI demonstrations. Each scenario runs on newly loaded synthetic fixtures."""
from __future__ import annotations

import argparse
import copy
import json
import threading
from concurrent.futures import ThreadPoolExecutor

from executor import TicketExecutor
from lab_data import new_tickets, proposal, trusted_session
from policy import TicketPolicy


class TimeoutPolicy(TicketPolicy):
    def evaluate(self, *args, **kwargs):
        raise TimeoutError("Simulated PDP unavailable")


def run_scenario(scenario: str) -> dict:
    engine = TicketExecutor(new_tickets(), policy=TimeoutPolicy() if scenario == "C07" else None)
    analyst = trusted_session("analyst-a")
    baseline = engine.snapshot()
    records = []
    if scenario == "C01":
        records = [engine.run(proposal("c01"), analyst)]
    elif scenario == "C02":
        records = [engine.run(proposal("c02", action="ticket.delete"), analyst)]
    elif scenario == "C03":
        records = [engine.run(proposal("c03", resource="tenant-b/ticket-202"), analyst)]
    elif scenario == "C04":
        attack = proposal("c04", action="ticket.delete")
        attack["principal_id"] = "admin-a"
        records = [engine.run(attack, analyst)]
    elif scenario == "C05":
        attack = proposal("c05")
        records = [engine.run(attack, analyst,
                              _trusted_test_after_check=lambda: attack.update(resource="tenant-b/ticket-202"))]
    elif scenario == "C06":
        request = proposal("c06")
        records = [engine.run(request, analyst), engine.run(request, analyst)]
    elif scenario == "C07":
        records = [engine.run(proposal("c07"), analyst)]
    elif scenario == "CONCURRENT":
        n = 12
        barrier = threading.Barrier(n)
        request = proposal("concurrent")

        def worker(_):
            barrier.wait(timeout=10)
            return engine.run(copy.deepcopy(request), analyst)
        with ThreadPoolExecutor(max_workers=n) as pool:
            records = list(pool.map(worker, range(n)))
    else:
        raise ValueError("Unsupported scenario: " + scenario)

    # The CLI runs in an explicitly privileged, local reviewer harness.
    # run() returns agent-safe metadata only; full records are fetched solely
    # from the reviewer-only audit_events() accessor for C01-C07 oracles.
    public_responses = records
    records = engine.audit_events()
    final = engine.snapshot()
    expected = copy.deepcopy(baseline)
    expected["tenant-a/ticket-101"]["comments"].append("Synthetic review")
    negative = lambda r: (r["decision"] in ("DENY", "ERROR") and not r["executed"]
                          and r["mutation_count_delta"] == 0
                          and r["state_before"] == r["state_after"])
    if scenario == "C01":
        passed = (len(records) == 1 and records[0]["decision"] == "ALLOW"
                  and records[0]["mutation_count_delta"] == 1 and final == expected)
    elif scenario == "C06":
        passed = (records[0]["decision"] == "ALLOW"
                  and records[0]["mutation_count_delta"] == 1
                  and records[1]["reason_code"] == "REPLAY_BLOCKED"
                  and negative(records[1]) and final == expected)
    elif scenario == "CONCURRENT":
        passed = (sum(r["decision"] == "ALLOW" for r in records) == 1
                  and sum(r["reason_code"] == "REPLAY_BLOCKED" for r in records) == 11
                  and sum(r["mutation_count_delta"] for r in records) == 1
                  and all(negative(r) for r in records if r["decision"] != "ALLOW")
                  and final == expected)
    else:
        reasons = {"C02": "MISSING_PERMISSION", "C03": "CROSS_TENANT_ACCESS",
                   "C04": "UNTRUSTED_AUTHORITY_FIELD", "C05": "OPERATION_CHANGED",
                   "C07": "POLICY_UNAVAILABLE"}
        passed = (len(records) == 1 and negative(records[0])
                  and records[0]["reason_code"] == reasons[scenario]
                  and final == baseline and engine.mutation_count() == 0)
    return {
        "scenario": scenario,
        "verdict": "PASS" if passed else "FAIL",
        "model": "single-process shared-lock synthetic target",
        "initial_state": baseline,
        "records": records,  # PRIVILEGED evaluator evidence; never send to agent
        "public_responses": public_responses,
        "final_state": final,
        "total_mutations": engine.mutation_count(),
    }


def main():
    parser = argparse.ArgumentParser(description="Synthetic action-boundary security demonstrations")
    parser.add_argument("--scenario", choices=["C01", "C02", "C03", "C04", "C05", "C06", "C07", "CONCURRENT", "ALL"], required=True)
    args = parser.parse_args()
    names = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "CONCURRENT"] if args.scenario == "ALL" else [args.scenario]
    outputs = [run_scenario(name) for name in names]
    output = {"overall_verdict": "PASS" if all(v["verdict"] == "PASS" for v in outputs) else "FAIL",
              "results": outputs} if args.scenario == "ALL" else outputs[0]
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    if any(x["verdict"] != "PASS" for x in outputs):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
