#!/usr/bin/env python3
"""Run deterministic V27.2 stability smoke tests without external data."""

from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import analysis_state
import evaluate_regression
import inventory_problem


def regression_document(version: str, improvement: int) -> dict:
    cases = []
    for case_id, family in [("event-clock", "hybrid-dynamics"), ("group-split", "grouped-data")]:
        scores = {dimension: 3 for dimension in evaluate_regression.DIMENSIONS}
        scores["source_integrity"] += improvement
        scores["state_continuity"] += improvement
        cases.append(
            {
                "case_id": case_id,
                "mechanism_family": family,
                "scores": scores,
                "critical_failures": [],
                "evidence": ["synthetic deterministic self-test fixture"],
            }
        )
    return {
        "format": "shhh-strategy-regression-observation",
        "version": version,
        "evaluation_status": "development",
        "cases": cases,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    skill_dir = Path(__file__).resolve().parents[1]
    checks: list[str] = []

    with tempfile.TemporaryDirectory(prefix="shhh-v27-2-") as temporary:
        root = Path(temporary)
        sources = root / "problem"
        sources.mkdir()
        (sources / "statement.txt").write_text("Question 1: minimize time.\n", encoding="utf-8")
        (sources / "data.csv").write_text("id,time\n1,0\n1,1\n", encoding="utf-8")
        (sources / "figure.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"></svg>\n',
            encoding="utf-8",
        )

        inventory = inventory_problem.scan_sources([sources])
        assert len(inventory["files"]) == 3
        assert inventory["overall_status"] == "pending_review"
        for record in inventory["files"]:
            for inspection in record["inspections"].values():
                if inspection["required"]:
                    inspection["status"] = "complete"
                    inspection["note"] = "synthetic self-test review"
        inventory_problem.refresh_status(inventory)
        assert inventory["overall_status"] == "complete"
        inventory_path = root / "source-inventory.json"
        inventory_problem.atomic_write(inventory_path, inventory)
        assert not inventory_problem.validate_inventory(inventory, require_complete=True)
        checks.append("inventory_scan_mark_hash_validate")

        state = analysis_state.new_document("self-test", inventory_path)
        state["subquestions"] = [
            {
                "id": "q1",
                "lock_status": "locked",
                "object": "one controlled process",
                "inputs": ["time table"],
                "information_time": "before the decision",
                "state": ["process state"],
                "decision": ["control"],
                "hard_constraints": ["legal domain"],
                "objective": "minimize completion time",
                "outputs": ["feasible control"],
                "dependencies": [],
                "validation": ["independent replay"],
                "notes": [],
            }
        ]
        state["activated_gates"] = [
            {"gate": 1, "trigger": "minimum deliverable", "evidence": ["statement:q1"], "status": "active"}
        ]
        route = {
            "id": "baseline",
            "role": "baseline",
            "status": "selected",
            "trigger": ["q1 output"],
            "baseline_defect_or_distinct_role": "credible minimum route",
            "variables": ["state", "control"],
            "relations": ["state transition"],
            "constraints": ["legal domain"],
            "algorithm_exit": "all states processed",
            "output_schema": ["control", "objective"],
            "validation": ["independent replay"],
            "rejection_condition": "fails feasibility",
        }
        state["routes"] = {"baseline_id": "baseline", "selected_ids": ["baseline"], "items": [route]}
        analysis_state.append_event(state, "seal", "synthetic route populated")
        assert not analysis_state.validate_structure(state)
        assert not analysis_state.transition_errors(state, "route_executable")
        state["quality_state"] = "route_executable"
        analysis_state.append_event(state, "transition:draft->route_executable", "all executable fields present")
        assert not analysis_state.validate_structure(state)
        state_path = root / "analysis-state.json"
        analysis_state.atomic_write(state_path, state)
        analysis_path = root / "analysis.md"
        analysis_path.write_text("Executable synthetic route.\n", encoding="utf-8")
        freeze_dir = root / "freezes"
        completed = subprocess.run(
            [
                sys.executable,
                str(skill_dir / "scripts" / "freeze_analysis.py"),
                "--case-id",
                "self-test",
                "--analysis",
                str(analysis_path),
                "--source",
                str(sources),
                "--ledger",
                str(state_path),
                "--state",
                "route_executable",
                "--output-dir",
                str(freeze_dir),
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert completed.returncode == 0, completed.stderr
        freeze = json.loads((freeze_dir / "self-test_freeze.json").read_text(encoding="utf-8"))
        assert freeze["analysis_ledger"]["sha256"] == analysis_state.sha256_file(state_path)
        checks.append("ledger_aware_freeze")
        solved_state = copy.deepcopy(state)
        solved_state["results"] = [
            {
                "id": "result-q1",
                "subquestion_id": "q1",
                "producer_route_id": "baseline",
                "status": "computed",
                "evidence": ["synthetic output artifact"],
            }
        ]
        solved_state["validation_items"] = [
            {
                "id": "replay-q1",
                "blocking": True,
                "status": "planned",
                "method": "independent replay",
                "evidence": [],
            }
        ]
        solved_state["claim_boundaries"] = [
            {
                "id": "claim-q1",
                "statement": "synthetic candidate only",
                "level": "candidate",
                "evidence": ["computed output"],
                "prohibited_upgrades": ["proven optimal"],
            }
        ]
        analysis_state.append_event(solved_state, "seal", "synthetic result recorded")
        assert not analysis_state.transition_errors(solved_state, "solved_unvalidated")
        assert analysis_state.transition_errors(solved_state, "solved_and_validated")
        solved_state["validation_items"][0]["status"] = "pass"
        solved_state["validation_items"][0]["evidence"] = ["replay matched"]
        solved_state["results"][0]["status"] = "validated"
        analysis_state.append_event(solved_state, "seal", "blocking validation passed")
        assert not analysis_state.transition_errors(solved_state, "solved_and_validated")
        checks.append("audit_result_and_validation_state_separation")
        state["subquestions"][0]["objective"] = "silently changed objective"
        assert "semantic state changed after the last sealed event" in analysis_state.validate_structure(state)
        checks.append("state_transition_and_drift_detection")

        baseline = regression_document("v27.1", 0)
        candidate = regression_document("v27.2", 1)
        assert not evaluate_regression.validate(baseline)
        assert not evaluate_regression.validate(candidate)
        comparison = evaluate_regression.compare(baseline, candidate)
        assert comparison["promote"] is True
        checks.append("behavior_observation_validation_and_promotion_gate")

    gate_numbers = []
    for path in sorted((skill_dir / "references" / "gates").glob("*.md")):
        gate_numbers.extend(int(value) for value in re.findall(r"^## (\d+)\.", path.read_text(encoding="utf-8"), re.M))
    assert sorted(gate_numbers) == list(range(1, 19))
    checks.append("all_18_structural_gates_preserved_once")

    print(json.dumps({"status": "PASS", "checks": checks}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
