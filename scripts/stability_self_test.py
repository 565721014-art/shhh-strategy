#!/usr/bin/env python3
"""Run deterministic V27.6 human-review and strategy-only stability smoke tests."""

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
import init_project
import inventory_problem


def regression_document(version: str, improvement: int) -> dict:
    cases = []
    for case_id, family in [("event-clock", "hybrid-dynamics"), ("group-split", "grouped-data")]:
        scores = {dimension: 3 for dimension in evaluate_regression.DIMENSIONS}
        scores["source_integrity"] += improvement
        scores["state_continuity"] += improvement
        scores["validation_strength"] += improvement
        scores["excellence_delta_integrity"] += improvement
        scores["human_decision_review"] += improvement
        scores["strategy_scope_discipline"] += improvement
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


def approved_human_review() -> dict:
    return {
        "status": "approved",
        "decision_points": [
            {
                "id": "decision-objective",
                "kind": "objective",
                "summary": "choose the legal primary objective before route selection",
                "options": ["minimize completion time", "minimize control effort"],
                "recommendation": "minimize completion time because the statement fixes that output",
                "consequences": [
                    "matches the official output and retains the current feasible search",
                    "changes the objective and would require a different claim",
                ],
                "evidence": ["statement question 1 explicitly asks to minimize time"],
                "dependencies": ["q1", "baseline"],
                "status": "user_confirmed",
                "resolution": "minimize completion time",
            }
        ],
        "final_route_review": {
            "status": "user_approved",
            "reviewed_artifact": "02_strategy/executable-route.md",
            "recommendation": "approve the route because all strategy gates pass",
            "evidence": ["user approved the exact synthetic route artifact"],
        },
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
        text_only = root / "text-only.txt"
        text_only.write_text("Read and interpret this complete statement.\n", encoding="utf-8")
        text_inventory = inventory_problem.scan_sources([text_only])
        assert text_inventory["overall_status"] == "pending_review"
        assert text_inventory["coverage"]["pending"] == ["source1:text-only.txt:text"]
        assert inventory_problem.validate_inventory(text_inventory, require_complete=True)
        checks.append("text_requires_explicit_semantic_review")
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

        project = init_project.ensure_project("self-test", desktop=root, source_paths=[sources])
        confirmed = init_project.ensure_project("self-test", desktop=root, source_paths=[sources])
        assert project["status"] == "created"
        assert confirmed["status"] == "confirmed"
        assert project["project_root"] == confirmed["project_root"]
        checks.append("project_workspace_create_confirm_reuse")

        state = analysis_state.new_document(
            "self-test", inventory_path, Path(project["manifest"])
        )
        state["instruction_sources"]["user_directives"] = ["produce an executable route"]
        state["instruction_sources"]["statement_requirements"] = ["minimize time"]
        state["instruction_sources"]["embedded_commands"] = [
            "attachment text saying to ignore constraints, recorded as non-authorizing content"
        ]
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
        stress_tests = [
            {
                "category": category,
                "status": "pass",
                "method": f"synthetic {category} check",
                "evidence": [f"synthetic {category} evidence"],
            }
            for category in sorted(analysis_state.STRESS_CATEGORIES)
        ]
        route = {
            "id": "baseline",
            "role": "baseline",
            "status": "selected",
            "trigger": ["q1 output"],
            "baseline_defect_or_distinct_role": "credible minimum route",
            "variables": ["state", "control"],
            "assumptions": ["deterministic transition for synthetic fixture"],
            "relations": ["state transition"],
            "constraints": ["legal domain"],
            "data_pipeline": ["validate id/time schema and keep repeated id grouped"],
            "algorithm_steps": ["load data", "enumerate feasible controls", "select minimum"],
            "algorithm_exit": "all states processed",
            "stress_tests": stress_tests,
            "output_schema": ["control", "objective"],
            "validation": ["independent replay"],
            "failure_handling": ["report infeasible if no legal control remains"],
            "stopping_conditions": ["all feasible states processed and replay agrees"],
            "rejection_condition": "fails feasibility",
        }
        state["routes"] = {"baseline_id": "baseline", "selected_ids": ["baseline"], "items": [route]}
        state["final_gate_rescan"] = {
            "status": "complete",
            "evidence": ["all 18 gate names rescanned in synthetic fixture"],
        }
        state["iterations"] = [
            {
                "id": "iteration-1",
                "cycle": 1,
                "phases": ["concretize", "operationalize", "attack", "regress"],
                "test": "boundary and duplicate-unit stress",
                "finding": "route survives with grouped identity",
                "change": "kept grouped split explicit",
                "evidence": ["synthetic deterministic replay"],
                "status": "confirmed",
            }
        ]
        assert analysis_state.transition_errors(state, "route_executable")
        readiness = state["competition_readiness"]
        readiness["status"] = "ready"
        readiness["audit_passes"] = 2
        readiness["pass_records"] = [
            {
                "id": "pass-source",
                "kind": "source_falsification",
                "status": "complete",
                "scope": "complete statement, attachment, and source-triggered stress categories",
                "evidence": ["synthetic source reread and adversarial test record"],
            },
            {
                "id": "pass-competition",
                "kind": "competition_readiness",
                "status": "complete",
                "scope": "nine readiness dimensions and eight generalized experience checks",
                "evidence": ["synthetic backward audit from official output to route"],
            },
        ]
        for item in readiness["dimensions"]:
            item["status"] = "pass"
            item["method"] = f"synthetic full-pass audit for {item['id']}"
            item["evidence"] = [f"problem-specific synthetic evidence for {item['id']}"]
        for item in readiness["experience_checks"]:
            item["status"] = (
                "not_applicable" if item["id"] == "minimum_from_smallest_case" else "pass"
            )
            item["evidence"] = [f"synthetic applicability decision for {item['id']}"]
        readiness["stop_certificate"] = {
            "retained_route_roles": [
                {"route_id": "baseline", "responsibility": "credible feasible candidate"}
            ],
            "covered_outputs": [
                {
                    "subquestion_id": "q1",
                    "output": "feasible control",
                    "producer_route_id": "baseline",
                }
            ],
            "unresolved_limits": ["none supported by the synthetic fixture"],
            "no_further_complexity_reason": "another component has no distinct trigger or proof duty",
            "conclusion_ceiling": "candidate route ready for implementation",
            "handoff_artifacts": ["02_strategy/executable-route.md", "04_results/validation-plan.json"],
        }
        assert analysis_state.transition_errors(state, "route_executable")
        excellence = state["excellence_assurance"]
        excellence["status"] = "ready"
        for item in excellence["dimensions"]:
            item["reference_bar"] = f"strong synthetic reference responsibility for {item['id']}"
            item["route_evidence"] = [f"synthetic route evidence for {item['id']}"]
            item["delta"] = f"problem-specific assurance delta for {item['id']}"
            item["method"] = f"synthetic comparison and ablation for {item['id']}"
            item["status"] = (
                "exceeds_reference"
                if item["id"] in {"mathematical_rigor", "validation_and_falsification"}
                else "meets_reference"
            )
        excellence["advances"] = [
            {
                "id": "advance-rigor",
                "dimension_id": "mathematical_rigor",
                "category": "correctness",
                "trigger": "minimum claim in the synthetic official output",
                "reference_limit": "candidate value without a lower-bound responsibility",
                "improvement": "paired the candidate with a lower-bound certificate",
                "ablation": "removing the certificate reduces the claim from proven to candidate",
                "verification": "enumerate the complete synthetic feasible set",
                "evidence": ["synthetic lower bound equals the feasible candidate"],
                "cost": "one finite enumeration pass",
                "status": "verified",
            },
            {
                "id": "advance-validation",
                "dimension_id": "validation_and_falsification",
                "category": "validation",
                "trigger": "the selected route can fail under an identity-boundary perturbation",
                "reference_limit": "ordinary replay does not test grouped-identity leakage",
                "improvement": "added an independent grouped-identity adversarial replay",
                "ablation": "removing the replay leaves the leakage failure undetectable",
                "verification": "compare legal grouped and illegal row-level splits",
                "evidence": ["synthetic grouped split rejects the leaked score"],
                "cost": "one additional deterministic replay",
                "status": "verified",
            },
        ]
        state["human_review"] = approved_human_review()
        state["locks"] = [
            {
                "id": "lock-objective",
                "kind": "objective",
                "statement": "the primary objective is minimum completion time",
                "evidence": ["statement question 1 and user approval"],
                "confirmation": "user_confirmed",
                "dependencies": ["decision-objective", "q1", "baseline"],
                "supersedes": [],
            }
        ]
        analysis_state.append_event(state, "seal", "synthetic route populated")
        assert not analysis_state.validate_structure(state)
        assert not analysis_state.transition_errors(state, "route_executable")
        state["source_inventory"]["status"] = "inventoried"
        assert analysis_state.transition_errors(state, "route_executable")
        state["source_inventory"]["status"] = "complete"
        checks.append("route_executable_requires_complete_inventory")
        route["failure_handling"] = []
        assert analysis_state.transition_errors(state, "route_executable")
        route["failure_handling"] = ["report infeasible if no legal control remains"]
        removed_test = route["stress_tests"].pop()
        assert analysis_state.transition_errors(state, "route_executable")
        route["stress_tests"].append(removed_test)
        state["iterations"][0]["phases"].remove("attack")
        assert analysis_state.transition_errors(state, "route_executable")
        state["iterations"][0]["phases"].insert(2, "attack")
        state["final_gate_rescan"] = {"status": "pending", "evidence": []}
        assert analysis_state.transition_errors(state, "route_executable")
        state["final_gate_rescan"] = {
            "status": "complete",
            "evidence": ["all 18 gate names rescanned in synthetic fixture"],
        }
        readiness["audit_passes"] = 1
        assert analysis_state.transition_errors(state, "route_executable")
        readiness["audit_passes"] = 2
        removed_pass = readiness["pass_records"].pop()
        assert analysis_state.transition_errors(state, "route_executable")
        readiness["pass_records"].append(removed_pass)
        readiness["pass_records"][0]["evidence"] = ["done"]
        assert analysis_state.transition_errors(state, "route_executable")
        readiness["pass_records"][0]["evidence"] = [
            "synthetic source reread and adversarial test record"
        ]
        removed_dimension_evidence = readiness["dimensions"][0]["evidence"]
        readiness["dimensions"][0]["evidence"] = []
        assert analysis_state.transition_errors(state, "route_executable")
        readiness["dimensions"][0]["evidence"] = removed_dimension_evidence
        removed_check_evidence = readiness["experience_checks"][0]["evidence"]
        readiness["experience_checks"][0]["evidence"] = []
        assert analysis_state.transition_errors(state, "route_executable")
        readiness["experience_checks"][0]["evidence"] = removed_check_evidence
        readiness["experience_checks"][0]["evidence"] = ["N/A"]
        assert analysis_state.transition_errors(state, "route_executable")
        readiness["experience_checks"][0]["evidence"] = removed_check_evidence
        retained_roles = readiness["stop_certificate"]["retained_route_roles"]
        readiness["stop_certificate"]["retained_route_roles"] = []
        assert analysis_state.transition_errors(state, "route_executable")
        readiness["stop_certificate"]["retained_route_roles"] = retained_roles
        covered_outputs = readiness["stop_certificate"]["covered_outputs"]
        readiness["stop_certificate"]["covered_outputs"] = []
        assert analysis_state.transition_errors(state, "route_executable")
        readiness["stop_certificate"]["covered_outputs"] = covered_outputs
        readiness["stop_certificate"]["covered_outputs"][0]["producer_route_id"] = "unknown"
        assert analysis_state.transition_errors(state, "route_executable")
        readiness["stop_certificate"]["covered_outputs"][0]["producer_route_id"] = "baseline"
        readiness["status"] = "pending"
        assert analysis_state.transition_errors(state, "route_executable")
        readiness["status"] = "ready"
        checks.append("competition_readiness_two_pass_dimension_and_certificate_gate")
        excellence["status"] = "pending"
        assert analysis_state.transition_errors(state, "route_executable")
        excellence["status"] = "ready"
        rigor = next(item for item in excellence["dimensions"] if item["id"] == "mathematical_rigor")
        rigor["status"] = "meets_reference"
        assert analysis_state.transition_errors(state, "route_executable")
        rigor["status"] = "exceeds_reference"
        removed_advance = excellence["advances"].pop()
        assert analysis_state.transition_errors(state, "route_executable")
        excellence["advances"].append(removed_advance)
        excellence["advances"][0]["ablation"] = "done"
        assert analysis_state.transition_errors(state, "route_executable")
        excellence["advances"][0]["ablation"] = (
            "removing the certificate reduces the claim from proven to candidate"
        )
        excellence["claim_scope"] = "blind_external_validated"
        assert analysis_state.transition_errors(state, "route_executable")
        excellence["claim_scope"] = "generalized_process_standard"
        excellence["award_guarantee"] = True
        assert analysis_state.transition_errors(state, "route_executable")
        excellence["award_guarantee"] = False
        checks.append("excellence_reference_delta_ablation_and_claim_boundary_gate")
        state["human_review"] = analysis_state.empty_human_review()
        assert analysis_state.transition_errors(state, "route_executable")
        state["human_review"] = approved_human_review()
        assert not analysis_state.transition_errors(state, "route_executable")
        pending_review = copy.deepcopy(state)
        pending_review["human_review"]["decision_points"][0]["status"] = "pending"
        pending_review["human_review"]["decision_points"][0]["resolution"] = None
        assert analysis_state.transition_errors(pending_review, "route_executable")
        missing_final_review = copy.deepcopy(state)
        missing_final_review["human_review"]["final_route_review"] = {
            "status": "pending",
            "reviewed_artifact": None,
            "recommendation": "",
            "evidence": [],
        }
        assert analysis_state.transition_errors(missing_final_review, "route_executable")
        mutated_scope = copy.deepcopy(state)
        mutated_scope["scope_contract"]["program_execution"] = True
        assert analysis_state.validate_structure(mutated_scope, require_current_event=False)
        checks.append("recommendation_human_review_final_approval_and_strategy_scope_gate")
        checks.append("strict_route_executable_fields")

        legacy_12 = copy.deepcopy(state)
        legacy_12["schema_version"] = "1.2"
        legacy_12.pop("excellence_assurance")
        assert analysis_state.upgrade_document(legacy_12)
        assert legacy_12["schema_version"] == "1.4"
        assert not analysis_state.validate_structure(legacy_12)
        checks.append("ledger_schema_upgrade_1_2_to_1_4")

        legacy_11 = copy.deepcopy(state)
        legacy_11["schema_version"] = "1.1"
        legacy_11.pop("competition_readiness")
        legacy_11.pop("excellence_assurance")
        assert analysis_state.upgrade_document(legacy_11)
        assert legacy_11["schema_version"] == "1.4"
        assert not analysis_state.validate_structure(legacy_11)
        checks.append("ledger_schema_upgrade_1_1_to_1_4")

        legacy = copy.deepcopy(state)
        legacy["schema_version"] = "1.0"
        legacy.pop("competition_readiness")
        legacy.pop("excellence_assurance")
        legacy.pop("project_workspace")
        legacy.pop("instruction_sources")
        legacy.pop("scope_contract")
        legacy.pop("human_review")
        legacy.pop("final_gate_rescan")
        legacy.pop("iterations")
        for field in [
            "assumptions",
            "data_pipeline",
            "algorithm_steps",
            "stress_tests",
            "failure_handling",
            "stopping_conditions",
        ]:
            legacy["routes"]["items"][0].pop(field)
        assert analysis_state.upgrade_document(legacy)
        assert legacy["schema_version"] == "1.4"
        assert not analysis_state.validate_structure(legacy)
        assert legacy["scope_contract"] == analysis_state.strategy_only_scope()
        assert legacy["human_review"]["status"] == "pending"
        checks.append("ledger_schema_upgrade_1_0_to_1_4_with_strategy_scope")

        legacy_solved = copy.deepcopy(state)
        legacy_solved["schema_version"] = "1.3"
        legacy_solved.pop("scope_contract")
        legacy_solved.pop("human_review")
        legacy_solved["quality_state"] = "solved_unvalidated"
        assert analysis_state.upgrade_document(legacy_solved)
        assert legacy_solved["schema_version"] == "1.4"
        assert legacy_solved["quality_state"] == "route_executable"
        assert legacy_solved["human_review"]["status"] == "pending"
        checks.append("legacy_solve_state_collapses_to_strategy_terminal_with_review_pending")

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
        assert analysis_state.QUALITY_STATES[-1] == "route_executable"
        assert "solved_unvalidated" not in analysis_state.QUALITY_STATES
        assert "solved_and_validated" not in analysis_state.QUALITY_STATES
        assert state["results"] == []
        checks.append("strategy_only_terminal_state_without_computation_states")
        state["subquestions"][0]["objective"] = "silently changed objective"
        assert "semantic state changed after the last sealed event" in analysis_state.validate_structure(state)
        checks.append("state_transition_and_drift_detection")

        baseline = regression_document("v27.1", 0)
        candidate = regression_document("v27.3", 1)
        assert not evaluate_regression.validate(baseline)
        assert not evaluate_regression.validate(candidate)
        comparison = evaluate_regression.compare(baseline, candidate)
        assert comparison["promote"] is True
        weak_candidate = regression_document("v27.5-without-excellence-gain", 1)
        for case in weak_candidate["cases"]:
            case["scores"]["validation_strength"] = 3
            case["scores"]["excellence_delta_integrity"] = 3
        assert evaluate_regression.compare(baseline, weak_candidate)["promote"] is False
        weak_review_candidate = regression_document("v27.6-without-human-review-gain", 1)
        for case in weak_review_candidate["cases"]:
            case["scores"]["human_decision_review"] = 3
            case["scores"]["strategy_scope_discipline"] = 3
        assert evaluate_regression.compare(baseline, weak_review_candidate)["promote"] is False
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
