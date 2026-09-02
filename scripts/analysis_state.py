#!/usr/bin/env python3
"""Create, seal, validate, and transition a shhh-strategy analysis ledger."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


QUALITY_STATES = [
    "draft",
    "understanding_locked",
    "audit_complete",
    "route_executable",
]

DECISION_KINDS = {
    "interpretation",
    "objective",
    "preference",
    "route",
    "complexity",
    "validation",
    "claim_boundary",
}

STRESS_CATEGORIES = {
    "counterexample",
    "boundary",
    "data_quality",
    "leakage",
    "duplicate_unit",
    "identifiability",
    "feasibility",
    "robustness",
    "simplification",
    "abnormal_execution",
}
READINESS_DIMENSIONS = {
    "source_and_deliverable_closure",
    "mechanism_state_information_fidelity",
    "mathematical_identifiability_closure",
    "necessary_complexity_and_proof_roles",
    "data_algorithm_operationality",
    "falsification_validation_and_independence",
    "dependency_uncertainty_and_error_propagation",
    "output_reproducibility_and_claim_consistency",
    "contest_narrative_and_resource_feasibility",
}
EXPERIENCE_CHECKS = {
    "mechanism_before_model_name",
    "information_clock_and_nonanticipativity",
    "ideal_realizable_true_evaluator",
    "candidate_bound_corroboration_roles",
    "global_objective_and_coupling",
    "minimum_from_smallest_case",
    "solver_complexity_separate_from_model_complexity",
    "evidence_ceiling_and_no_old_answer_transfer",
}
EXCELLENCE_DIMENSIONS = {
    "interpretation_precision",
    "mechanism_fidelity",
    "mathematical_rigor",
    "computational_reliability",
    "validation_and_falsification",
    "uncertainty_and_decision_value",
    "reproducibility_and_communication",
}
ADVANCE_CATEGORIES = {
    "correctness",
    "validation",
    "decision_value",
    "robustness",
    "efficiency",
    "reproducibility",
    "interpretability",
}
LOOP_PHASES = {"concretize", "operationalize", "attack", "repair", "regress"}
REQUIRED_LOOP_PHASES = {"concretize", "operationalize", "attack", "regress"}
GENERIC_PLACEHOLDERS = {
    "done",
    "pass",
    "passed",
    "complete",
    "completed",
    "n/a",
    "na",
    "not applicable",
    "完成",
    "通过",
    "无",
    "暂无",
}


def specific_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value.strip().lower() not in GENERIC_PLACEHOLDERS


def specific_evidence(values: object) -> bool:
    return isinstance(values, list) and bool(values) and all(specific_text(item) for item in values)


def empty_competition_readiness() -> dict:
    return {
        "status": "pending",
        "audit_passes": 0,
        "pass_records": [],
        "dimensions": [
            {"id": item, "status": "pending", "method": "", "evidence": []}
            for item in sorted(READINESS_DIMENSIONS)
        ],
        "experience_checks": [
            {"id": item, "status": "pending", "evidence": []}
            for item in sorted(EXPERIENCE_CHECKS)
        ],
        "stop_certificate": {
            "retained_route_roles": [],
            "covered_outputs": [],
            "unresolved_limits": [],
            "no_further_complexity_reason": "",
            "conclusion_ceiling": "",
            "handoff_artifacts": [],
        },
    }


def empty_excellence_assurance() -> dict:
    return {
        "status": "pending",
        "benchmark_basis": "generalized_historical_process",
        "claim_scope": "generalized_process_standard",
        "award_guarantee": False,
        "dimensions": [
            {
                "id": item,
                "reference_bar": "",
                "route_evidence": [],
                "delta": "",
                "method": "",
                "status": "pending",
            }
            for item in sorted(EXCELLENCE_DIMENSIONS)
        ],
        "advances": [],
        "external_evidence": [],
    }


def strategy_only_scope() -> dict:
    return {
        "mode": "strategy_only",
        "program_execution": False,
        "numerical_solving": False,
        "completion_state": "route_executable",
    }


def empty_human_review() -> dict:
    return {
        "status": "pending",
        "decision_points": [],
        "final_route_review": {
            "status": "pending",
            "reviewed_artifact": None,
            "recommendation": "",
            "evidence": [],
        },
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("analysis state must be a JSON object")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


def semantic_state_hash(document: dict) -> str:
    payload = copy.deepcopy(document)
    payload.pop("events", None)
    return canonical_hash(payload)


def event_hash(event: dict) -> str:
    payload = dict(event)
    payload.pop("sha256", None)
    return canonical_hash(payload)


def append_event(document: dict, action: str, reason: str) -> None:
    now = utc_now()
    document["updated_utc"] = now
    events = document.setdefault("events", [])
    previous = events[-1]["sha256"] if events else None
    event = {
        "seq": len(events) + 1,
        "utc": now,
        "action": action,
        "reason": reason,
        "state_sha256": semantic_state_hash(document),
        "previous_sha256": previous,
    }
    event["sha256"] = event_hash(event)
    events.append(event)


def atomic_write(path: Path, document: dict) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def unique_ids(items: list, label: str, errors: list[str]) -> set[str]:
    ids: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            errors.append(f"{label}[{index}] has no non-empty id")
        else:
            ids.append(item["id"])
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    if duplicates:
        errors.append(f"duplicate {label} ids: {duplicates}")
    return set(ids)


def require_fields(item: dict, required: set[str], label: str, errors: list[str]) -> None:
    absent = sorted(required - set(item))
    if absent:
        errors.append(f"{label} missing fields: {absent}")
    unexpected = sorted(set(item) - required)
    if unexpected:
        errors.append(f"{label} has unexpected fields: {unexpected}")


def validate_structure(document: dict, require_current_event: bool = True) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "case_id",
        "created_utc",
        "updated_utc",
        "quality_state",
        "project_workspace",
        "scope_contract",
        "instruction_sources",
        "human_review",
        "final_gate_rescan",
        "competition_readiness",
        "excellence_assurance",
        "source_inventory",
        "subquestions",
        "activated_gates",
        "ambiguities",
        "locks",
        "routes",
        "validation_items",
        "claim_boundaries",
        "results",
        "iterations",
        "events",
    }
    missing = sorted(required - set(document))
    if missing:
        errors.append(f"missing top-level fields: {missing}")
        return errors
    extra = sorted(set(document) - required)
    if extra:
        errors.append(f"unexpected top-level fields: {extra}")
    if document.get("schema_version") != "1.4":
        errors.append("schema_version must be 1.4; run the upgrade command for older ledgers")
    if not isinstance(document.get("case_id"), str) or not document["case_id"].strip():
        errors.append("case_id must be non-empty")
    if document.get("quality_state") not in QUALITY_STATES:
        errors.append(f"invalid quality_state: {document.get('quality_state')}")

    list_fields = [
        "subquestions",
        "activated_gates",
        "ambiguities",
        "locks",
        "validation_items",
        "claim_boundaries",
        "results",
        "iterations",
        "events",
    ]
    for field in list_fields:
        if not isinstance(document.get(field), list):
            errors.append(f"{field} must be an array")
    if errors:
        return errors

    scope = document.get("scope_contract")
    scope_required = {"mode", "program_execution", "numerical_solving", "completion_state"}
    if not isinstance(scope, dict):
        errors.append("scope_contract must be an object")
    else:
        require_fields(scope, scope_required, "scope_contract", errors)
        if scope != strategy_only_scope():
            errors.append("scope_contract must preserve the strategy-only boundary")

    human_review = document.get("human_review")
    human_required = {"status", "decision_points", "final_route_review"}
    if not isinstance(human_review, dict):
        errors.append("human_review must be an object")
    else:
        require_fields(human_review, human_required, "human_review", errors)
        if human_review.get("status") not in {"pending", "approved", "blocked"}:
            errors.append("human_review status is invalid")
        decision_points = human_review.get("decision_points")
        if not isinstance(decision_points, list):
            errors.append("human_review decision_points must be an array")
        else:
            decision_required = {
                "id",
                "kind",
                "summary",
                "options",
                "recommendation",
                "consequences",
                "evidence",
                "dependencies",
                "status",
                "resolution",
            }
            decision_ids: list[str] = []
            for item in decision_points:
                if not isinstance(item, dict):
                    errors.append("human_review has a non-object decision point")
                    continue
                require_fields(item, decision_required, f"decision point {item.get('id')}", errors)
                decision_ids.append(item.get("id"))
                if item.get("kind") not in DECISION_KINDS:
                    errors.append(f"decision point {item.get('id')} has invalid kind")
                if item.get("status") not in {
                    "pending",
                    "user_confirmed",
                    "reopened",
                    "superseded",
                }:
                    errors.append(f"decision point {item.get('id')} has invalid status")
                for field in ["options", "consequences", "evidence", "dependencies"]:
                    if not isinstance(item.get(field), list):
                        errors.append(f"decision point {item.get('id')} {field} must be an array")
                if isinstance(item.get("options"), list) and len(item.get("options")) < 2:
                    errors.append(f"decision point {item.get('id')} must expose at least two live options")
                if item.get("status") == "user_confirmed" and not specific_text(item.get("resolution")):
                    errors.append(f"confirmed decision point {item.get('id')} lacks resolution")
                if item.get("status") in {"pending", "reopened"} and item.get("resolution") is not None:
                    errors.append(f"unresolved decision point {item.get('id')} already has a resolution")
            if len(decision_ids) != len(set(decision_ids)):
                errors.append("human_review decision point ids are duplicated")
        final_review = human_review.get("final_route_review")
        final_required = {"status", "reviewed_artifact", "recommendation", "evidence"}
        if not isinstance(final_review, dict):
            errors.append("human_review final_route_review must be an object")
        else:
            require_fields(final_review, final_required, "final_route_review", errors)
            if final_review.get("status") not in {"pending", "user_approved", "revision_requested"}:
                errors.append("final_route_review status is invalid")
            if final_review.get("reviewed_artifact") is not None and not isinstance(
                final_review.get("reviewed_artifact"), str
            ):
                errors.append("final_route_review reviewed_artifact must be a string or null")
            if not isinstance(final_review.get("recommendation"), str):
                errors.append("final_route_review recommendation must be a string")
            if not isinstance(final_review.get("evidence"), list):
                errors.append("final_route_review evidence must be an array")

    subquestion_ids = unique_ids(document["subquestions"], "subquestion", errors)
    ambiguity_ids = unique_ids(document["ambiguities"], "ambiguity", errors)
    lock_ids = unique_ids(document["locks"], "lock", errors)
    validation_ids = unique_ids(document["validation_items"], "validation", errors)
    claim_ids = unique_ids(document["claim_boundaries"], "claim", errors)
    result_ids = unique_ids(document["results"], "result", errors)
    iteration_ids = unique_ids(document["iterations"], "iteration", errors)
    del ambiguity_ids, lock_ids, validation_ids, claim_ids, result_ids, iteration_ids

    workspace = document.get("project_workspace")
    workspace_required = {"root", "manifest", "status"}
    if not isinstance(workspace, dict):
        errors.append("project_workspace must be an object")
    else:
        require_fields(workspace, workspace_required, "project_workspace", errors)
        if workspace.get("status") not in {"uninitialized", "confirmed", "blocked"}:
            errors.append("project_workspace status is invalid")
        if workspace.get("status") == "confirmed":
            if not workspace.get("root") or not workspace.get("manifest"):
                errors.append("confirmed project_workspace lacks root or manifest")
            else:
                manifest_path = Path(workspace["manifest"])
                if not manifest_path.is_file():
                    errors.append("linked project manifest is missing")
                else:
                    try:
                        manifest = load_json(manifest_path)
                        if manifest.get("format") != "shhh-strategy-project":
                            errors.append("linked project manifest format is invalid")
                        if manifest.get("case_id") != document.get("case_id"):
                            errors.append("linked project manifest case_id mismatch")
                        if Path(manifest.get("root", "")).resolve() != Path(workspace["root"]).resolve():
                            errors.append("linked project manifest root mismatch")
                    except (OSError, ValueError, json.JSONDecodeError) as error:
                        errors.append(f"linked project manifest cannot be read: {error}")

    instruction_sources = document.get("instruction_sources")
    instruction_required = {
        "user_directives",
        "statement_requirements",
        "attachment_requirements",
        "embedded_commands",
        "conflicts",
    }
    if not isinstance(instruction_sources, dict):
        errors.append("instruction_sources must be an object")
    else:
        require_fields(instruction_sources, instruction_required, "instruction_sources", errors)
        for field in instruction_required:
            if not isinstance(instruction_sources.get(field), list):
                errors.append(f"instruction_sources {field} must be an array")

    final_gate_rescan = document.get("final_gate_rescan")
    if not isinstance(final_gate_rescan, dict):
        errors.append("final_gate_rescan must be an object")
    else:
        require_fields(final_gate_rescan, {"status", "evidence"}, "final_gate_rescan", errors)
        if final_gate_rescan.get("status") not in {"pending", "complete", "blocked"}:
            errors.append("final_gate_rescan status is invalid")
        if not isinstance(final_gate_rescan.get("evidence"), list):
            errors.append("final_gate_rescan evidence must be an array")

    readiness = document.get("competition_readiness")
    readiness_required = {
        "status",
        "audit_passes",
        "pass_records",
        "dimensions",
        "experience_checks",
        "stop_certificate",
    }
    if not isinstance(readiness, dict):
        errors.append("competition_readiness must be an object")
    else:
        require_fields(readiness, readiness_required, "competition_readiness", errors)
        if readiness.get("status") not in {"pending", "ready", "blocked"}:
            errors.append("competition_readiness status is invalid")
        if not isinstance(readiness.get("audit_passes"), int) or readiness.get("audit_passes", -1) < 0:
            errors.append("competition_readiness audit_passes must be a nonnegative integer")
        pass_records = readiness.get("pass_records")
        if not isinstance(pass_records, list):
            errors.append("competition_readiness pass_records must be an array")
        else:
            pass_required = {"id", "kind", "status", "scope", "evidence"}
            pass_ids: list[str] = []
            for item in pass_records:
                if not isinstance(item, dict):
                    errors.append("competition readiness has a non-object pass record")
                    continue
                require_fields(item, pass_required, f"competition pass {item.get('id')}", errors)
                pass_ids.append(item.get("id"))
                if item.get("kind") not in {
                    "source_falsification",
                    "competition_readiness",
                    "repair_regression",
                }:
                    errors.append(f"competition pass {item.get('id')} has invalid kind")
                if item.get("status") not in {"complete", "blocked"}:
                    errors.append(f"competition pass {item.get('id')} has invalid status")
                if not isinstance(item.get("scope"), str) or not isinstance(item.get("evidence"), list):
                    errors.append(f"competition pass {item.get('id')} has invalid scope or evidence")
            if len(pass_ids) != len(set(pass_ids)):
                errors.append("competition pass record ids are duplicated")
        dimensions = readiness.get("dimensions")
        if not isinstance(dimensions, list):
            errors.append("competition_readiness dimensions must be an array")
        else:
            dimension_required = {"id", "status", "method", "evidence"}
            dimension_ids: list[str] = []
            for item in dimensions:
                if not isinstance(item, dict):
                    errors.append("competition readiness has a non-object dimension")
                    continue
                require_fields(
                    item,
                    dimension_required,
                    f"competition dimension {item.get('id')}",
                    errors,
                )
                dimension_ids.append(item.get("id"))
                if item.get("status") not in {"pending", "pass", "blocked"}:
                    errors.append(f"competition dimension {item.get('id')} has invalid status")
                if not isinstance(item.get("method"), str) or not isinstance(item.get("evidence"), list):
                    errors.append(f"competition dimension {item.get('id')} has invalid method or evidence")
            if set(dimension_ids) != READINESS_DIMENSIONS or len(dimension_ids) != len(READINESS_DIMENSIONS):
                errors.append("competition readiness dimensions are incomplete or duplicated")
        checks = readiness.get("experience_checks")
        if not isinstance(checks, list):
            errors.append("competition_readiness experience_checks must be an array")
        else:
            check_required = {"id", "status", "evidence"}
            check_ids: list[str] = []
            for item in checks:
                if not isinstance(item, dict):
                    errors.append("competition readiness has a non-object experience check")
                    continue
                require_fields(
                    item,
                    check_required,
                    f"experience check {item.get('id')}",
                    errors,
                )
                check_ids.append(item.get("id"))
                if item.get("status") not in {"pending", "pass", "blocked", "not_applicable"}:
                    errors.append(f"experience check {item.get('id')} has invalid status")
                if not isinstance(item.get("evidence"), list):
                    errors.append(f"experience check {item.get('id')} evidence must be an array")
            if set(check_ids) != EXPERIENCE_CHECKS or len(check_ids) != len(EXPERIENCE_CHECKS):
                errors.append("competition experience checks are incomplete or duplicated")
        stop_certificate = readiness.get("stop_certificate")
        stop_required = {
            "retained_route_roles",
            "covered_outputs",
            "unresolved_limits",
            "no_further_complexity_reason",
            "conclusion_ceiling",
            "handoff_artifacts",
        }
        if not isinstance(stop_certificate, dict):
            errors.append("competition_readiness stop_certificate must be an object")
        else:
            require_fields(stop_certificate, stop_required, "competition stop_certificate", errors)
            for field in ["retained_route_roles", "covered_outputs", "unresolved_limits", "handoff_artifacts"]:
                if not isinstance(stop_certificate.get(field), list):
                    errors.append(f"competition stop_certificate {field} must be an array")
            retained_required = {"route_id", "responsibility"}
            for item in stop_certificate.get("retained_route_roles", []):
                if not isinstance(item, dict):
                    errors.append("competition stop_certificate has a non-object retained route role")
                    continue
                require_fields(item, retained_required, "competition retained route role", errors)
            output_required = {"subquestion_id", "output", "producer_route_id"}
            for item in stop_certificate.get("covered_outputs", []):
                if not isinstance(item, dict):
                    errors.append("competition stop_certificate has a non-object covered output")
                    continue
                require_fields(item, output_required, "competition covered output", errors)
            for field in ["no_further_complexity_reason", "conclusion_ceiling"]:
                if not isinstance(stop_certificate.get(field), str):
                    errors.append(f"competition stop_certificate {field} must be a string")

    excellence = document.get("excellence_assurance")
    excellence_required = {
        "status",
        "benchmark_basis",
        "claim_scope",
        "award_guarantee",
        "dimensions",
        "advances",
        "external_evidence",
    }
    if not isinstance(excellence, dict):
        errors.append("excellence_assurance must be an object")
    else:
        require_fields(excellence, excellence_required, "excellence_assurance", errors)
        if excellence.get("status") not in {"pending", "ready", "blocked"}:
            errors.append("excellence_assurance status is invalid")
        if excellence.get("benchmark_basis") not in {
            "generalized_historical_process",
            "same_problem_opt_in",
            "blind_external_evaluation",
        }:
            errors.append("excellence_assurance benchmark_basis is invalid")
        if excellence.get("claim_scope") not in {
            "generalized_process_standard",
            "same_problem_comparative",
            "blind_external_validated",
        }:
            errors.append("excellence_assurance claim_scope is invalid")
        if excellence.get("award_guarantee") is not False:
            errors.append("excellence_assurance award_guarantee must remain false")
        excellence_dimensions = excellence.get("dimensions")
        if not isinstance(excellence_dimensions, list):
            errors.append("excellence_assurance dimensions must be an array")
        else:
            dimension_required = {
                "id",
                "reference_bar",
                "route_evidence",
                "delta",
                "method",
                "status",
            }
            excellence_ids: list[str] = []
            for item in excellence_dimensions:
                if not isinstance(item, dict):
                    errors.append("excellence assurance has a non-object dimension")
                    continue
                require_fields(
                    item,
                    dimension_required,
                    f"excellence dimension {item.get('id')}",
                    errors,
                )
                excellence_ids.append(item.get("id"))
                if item.get("status") not in {
                    "pending",
                    "meets_reference",
                    "exceeds_reference",
                    "below_reference",
                    "not_comparable",
                }:
                    errors.append(f"excellence dimension {item.get('id')} has invalid status")
                for field in ["reference_bar", "delta", "method"]:
                    if not isinstance(item.get(field), str):
                        errors.append(f"excellence dimension {item.get('id')} has invalid {field}")
                if not isinstance(item.get("route_evidence"), list):
                    errors.append(f"excellence dimension {item.get('id')} route_evidence must be an array")
            if set(excellence_ids) != EXCELLENCE_DIMENSIONS or len(excellence_ids) != len(
                EXCELLENCE_DIMENSIONS
            ):
                errors.append("excellence dimensions are incomplete or duplicated")
        advances = excellence.get("advances")
        if not isinstance(advances, list):
            errors.append("excellence_assurance advances must be an array")
        else:
            advance_required = {
                "id",
                "dimension_id",
                "category",
                "trigger",
                "reference_limit",
                "improvement",
                "ablation",
                "verification",
                "evidence",
                "cost",
                "status",
            }
            advance_ids: list[str] = []
            for item in advances:
                if not isinstance(item, dict):
                    errors.append("excellence assurance has a non-object advance")
                    continue
                require_fields(item, advance_required, f"excellence advance {item.get('id')}", errors)
                advance_ids.append(item.get("id"))
                if item.get("dimension_id") not in EXCELLENCE_DIMENSIONS:
                    errors.append(f"excellence advance {item.get('id')} has invalid dimension")
                if item.get("category") not in ADVANCE_CATEGORIES:
                    errors.append(f"excellence advance {item.get('id')} has invalid category")
                if item.get("status") not in {"planned", "verified", "failed", "blocked"}:
                    errors.append(f"excellence advance {item.get('id')} has invalid status")
                for field in [
                    "trigger",
                    "reference_limit",
                    "improvement",
                    "ablation",
                    "verification",
                    "cost",
                ]:
                    if not isinstance(item.get(field), str):
                        errors.append(f"excellence advance {item.get('id')} has invalid {field}")
                if not isinstance(item.get("evidence"), list):
                    errors.append(f"excellence advance {item.get('id')} evidence must be an array")
            if len(advance_ids) != len(set(advance_ids)):
                errors.append("excellence advance ids are duplicated")
        if not isinstance(excellence.get("external_evidence"), list):
            errors.append("excellence_assurance external_evidence must be an array")

    sub_required = {
        "id",
        "lock_status",
        "object",
        "inputs",
        "information_time",
        "state",
        "decision",
        "hard_constraints",
        "objective",
        "outputs",
        "dependencies",
        "validation",
    }
    sub_allowed = sub_required | {"notes"}
    for item in document["subquestions"]:
        if isinstance(item, dict):
            absent = sorted(sub_required - set(item))
            if absent:
                errors.append(f"subquestion {item.get('id')} missing fields: {absent}")
            unexpected = sorted(set(item) - sub_allowed)
            if unexpected:
                errors.append(
                    f"subquestion {item.get('id')} has unexpected fields: {unexpected}"
                )
            for dependency in item.get("dependencies", []):
                if dependency not in subquestion_ids:
                    errors.append(
                        f"subquestion {item.get('id')} references unknown dependency {dependency}"
                    )

    ambiguity_required = {
        "id",
        "summary",
        "evidence",
        "options",
        "recommended",
        "affects",
        "blocking",
        "status",
        "resolution",
    }
    for item in document["ambiguities"]:
        if isinstance(item, dict):
            require_fields(item, ambiguity_required, f"ambiguity {item.get('id')}", errors)
            if item.get("status") == "resolved" and not item.get("resolution"):
                errors.append(f"resolved ambiguity {item.get('id')} has no resolution")
            if item.get("status") == "open" and item.get("resolution"):
                errors.append(f"open ambiguity {item.get('id')} already has a resolution")

    lock_required = {
        "id",
        "kind",
        "statement",
        "evidence",
        "confirmation",
        "dependencies",
        "supersedes",
    }
    for item in document["locks"]:
        if isinstance(item, dict):
            require_fields(item, lock_required, f"lock {item.get('id')}", errors)
            if not item.get("statement") or not item.get("evidence"):
                errors.append(f"lock {item.get('id')} lacks statement or evidence")
            if item.get("confirmation") not in {
                "source_fixed",
                "user_confirmed",
                "agent_default",
                "provisional",
                "reopened",
            }:
                errors.append(f"lock {item.get('id')} has invalid confirmation")

    seen_gates: set[int] = set()
    for index, gate in enumerate(document["activated_gates"]):
        if not isinstance(gate, dict):
            errors.append(f"activated_gates[{index}] must be an object")
            continue
        number = gate.get("gate")
        if not isinstance(number, int) or not 1 <= number <= 18:
            errors.append(f"activated_gates[{index}] has invalid gate number")
        elif number in seen_gates:
            errors.append(f"gate {number} is activated more than once")
        else:
            seen_gates.add(number)
        if not gate.get("trigger") or not gate.get("evidence"):
            errors.append(f"gate {number} lacks trigger or evidence")

    routes = document.get("routes")
    if not isinstance(routes, dict):
        errors.append("routes must be an object")
        route_items = []
    else:
        for field in ["baseline_id", "selected_ids", "items"]:
            if field not in routes:
                errors.append(f"routes missing {field}")
        route_items = routes.get("items", []) if isinstance(routes.get("items"), list) else []
    route_ids = unique_ids(route_items, "route", errors)
    route_required = {
        "id",
        "role",
        "status",
        "trigger",
        "baseline_defect_or_distinct_role",
        "variables",
        "assumptions",
        "relations",
        "constraints",
        "data_pipeline",
        "algorithm_steps",
        "algorithm_exit",
        "stress_tests",
        "output_schema",
        "validation",
        "failure_handling",
        "stopping_conditions",
        "rejection_condition",
    }
    for item in route_items:
        if isinstance(item, dict):
            require_fields(item, route_required, f"route {item.get('id')}", errors)
            stress_tests = item.get("stress_tests")
            if not isinstance(stress_tests, list):
                errors.append(f"route {item.get('id')} stress_tests must be an array")
            else:
                seen_categories: set[str] = set()
                stress_required = {"category", "status", "method", "evidence"}
                for test in stress_tests:
                    if not isinstance(test, dict):
                        errors.append(f"route {item.get('id')} has a non-object stress test")
                        continue
                    require_fields(
                        test,
                        stress_required,
                        f"route {item.get('id')} stress test {test.get('category')}",
                        errors,
                    )
                    category = test.get("category")
                    if category not in STRESS_CATEGORIES:
                        errors.append(f"route {item.get('id')} has invalid stress category {category}")
                    elif category in seen_categories:
                        errors.append(f"route {item.get('id')} duplicates stress category {category}")
                    else:
                        seen_categories.add(category)
                    if test.get("status") not in {"pass", "fail", "blocked", "not_applicable"}:
                        errors.append(f"route {item.get('id')} stress test {category} has invalid status")
                    if not test.get("method") or not test.get("evidence"):
                        errors.append(f"route {item.get('id')} stress test {category} lacks method or evidence")
    if routes and routes.get("baseline_id") is not None and routes.get("baseline_id") not in route_ids:
        errors.append("baseline_id does not reference a route")
    for route_id in routes.get("selected_ids", []) if isinstance(routes, dict) else []:
        if route_id not in route_ids:
            errors.append(f"selected route does not exist: {route_id}")

    validation_required = {"id", "blocking", "status", "method", "evidence"}
    for item in document["validation_items"]:
        if isinstance(item, dict):
            require_fields(item, validation_required, f"validation {item.get('id')}", errors)
            if item.get("status") not in {"planned", "pass", "fail", "blocked", "not_applicable"}:
                errors.append(f"validation {item.get('id')} has invalid status")

    claim_required = {"id", "statement", "level", "evidence", "prohibited_upgrades"}
    claim_levels = {"descriptive", "predictive", "mechanism", "causal", "scenario", "candidate", "proven"}
    for item in document["claim_boundaries"]:
        if isinstance(item, dict):
            require_fields(item, claim_required, f"claim {item.get('id')}", errors)
            if item.get("level") not in claim_levels:
                errors.append(f"claim {item.get('id')} has invalid level")

    result_required = {"id", "subquestion_id", "producer_route_id", "status", "evidence"}
    for item in document["results"]:
        if isinstance(item, dict):
            require_fields(item, result_required, f"result {item.get('id')}", errors)
            if item.get("subquestion_id") not in subquestion_ids:
                errors.append(f"result {item.get('id')} references unknown subquestion")
            if item.get("producer_route_id") not in route_ids:
                errors.append(f"result {item.get('id')} references unknown route")
            if item.get("status") not in {"computed", "reproduced", "validated"}:
                errors.append(f"result {item.get('id')} has invalid status")

    iteration_required = {"id", "cycle", "phases", "test", "finding", "change", "evidence", "status"}
    seen_cycles: set[int] = set()
    for item in document["iterations"]:
        if isinstance(item, dict):
            require_fields(item, iteration_required, f"iteration {item.get('id')}", errors)
            cycle = item.get("cycle")
            if not isinstance(cycle, int) or cycle < 1:
                errors.append(f"iteration {item.get('id')} has invalid cycle")
            elif cycle in seen_cycles:
                errors.append(f"iteration cycle is duplicated: {cycle}")
            else:
                seen_cycles.add(cycle)
            if item.get("status") not in {"confirmed", "corrected", "blocked"}:
                errors.append(f"iteration {item.get('id')} has invalid status")
            phases = item.get("phases")
            if not isinstance(phases, list) or not phases:
                errors.append(f"iteration {item.get('id')} has no phases")
            elif len(phases) != len(set(phases)) or any(phase not in LOOP_PHASES for phase in phases):
                errors.append(f"iteration {item.get('id')} has invalid or duplicate phases")
            if item.get("status") == "corrected" and "repair" not in (phases or []):
                errors.append(f"corrected iteration {item.get('id')} does not include repair phase")
            if not item.get("test") or not item.get("finding") or not item.get("evidence"):
                errors.append(f"iteration {item.get('id')} lacks test, finding, or evidence")

    inventory = document.get("source_inventory")
    if not isinstance(inventory, dict):
        errors.append("source_inventory must be an object")
    else:
        if inventory.get("status") not in {"missing", "inventoried", "complete", "blocked"}:
            errors.append("source_inventory status is invalid")
        digest = inventory.get("sha256")
        if digest is not None and (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(ch not in "0123456789abcdefABCDEF" for ch in digest)
        ):
            errors.append("source_inventory sha256 is invalid")
        inventory_path = inventory.get("path")
        if inventory_path is not None:
            linked_path = Path(inventory_path)
            if not linked_path.is_file():
                errors.append("linked source inventory file is missing")
            elif digest != sha256_file(linked_path):
                errors.append("linked source inventory hash has changed")

    previous = None
    for index, event in enumerate(document["events"], start=1):
        if not isinstance(event, dict):
            errors.append(f"events[{index - 1}] must be an object")
            continue
        if event.get("seq") != index:
            errors.append(f"event sequence mismatch at {index}")
        if event.get("previous_sha256") != previous:
            errors.append(f"event previous hash mismatch at {index}")
        if event.get("sha256") != event_hash(event):
            errors.append(f"event hash mismatch at {index}")
        previous = event.get("sha256")
    if require_current_event:
        if not document["events"]:
            errors.append("state has no provenance event")
        elif document["events"][-1].get("state_sha256") != semantic_state_hash(document):
            errors.append("semantic state changed after the last sealed event")
    if not errors and document.get("quality_state") in QUALITY_STATES:
        errors.extend(transition_errors(document, document["quality_state"]))
    return errors


def transition_errors(document: dict, target: str) -> list[str]:
    errors: list[str] = []
    inventory_status = document["source_inventory"].get("status")
    open_blocking = [
        item.get("id")
        for item in document["ambiguities"]
        if item.get("blocking") and item.get("status") == "open"
    ]
    subquestions = document["subquestions"]
    route_items = {item.get("id"): item for item in document["routes"].get("items", [])}

    if QUALITY_STATES.index(target) >= QUALITY_STATES.index("understanding_locked"):
        workspace = document.get("project_workspace", {})
        if workspace.get("status") != "confirmed":
            errors.append("project workspace is not confirmed")
        instruction_sources = document.get("instruction_sources", {})
        if not instruction_sources.get("user_directives"):
            errors.append("user directives are not recorded separately")
        if not instruction_sources.get("statement_requirements"):
            errors.append("statement requirements are not recorded separately")
        if inventory_status not in {"inventoried", "complete"}:
            errors.append("source inventory is not inventoried or complete")
        if not subquestions:
            errors.append("no subquestions are recorded")
        for item in subquestions:
            if item.get("lock_status") != "locked":
                errors.append(f"subquestion {item.get('id')} is not locked")
            for field in ["object", "information_time", "objective"]:
                if not item.get(field):
                    errors.append(f"subquestion {item.get('id')} has empty {field}")
            for field in ["inputs", "outputs", "validation"]:
                if not item.get(field):
                    errors.append(f"subquestion {item.get('id')} has empty {field}")
        if open_blocking:
            errors.append(f"blocking ambiguities remain open: {open_blocking}")

    if QUALITY_STATES.index(target) >= QUALITY_STATES.index("audit_complete"):
        baseline_id = document["routes"].get("baseline_id")
        if not baseline_id or baseline_id not in route_items:
            errors.append("a credible baseline route is not recorded")
        if not route_items:
            errors.append("no route candidates are recorded")

    if QUALITY_STATES.index(target) >= QUALITY_STATES.index("route_executable"):
        if inventory_status != "complete":
            errors.append("source inventory is not semantically complete")
        selected_ids = document["routes"].get("selected_ids", [])
        if not selected_ids:
            errors.append("no selected route is recorded")
        for route_id in selected_ids:
            route = route_items.get(route_id, {})
            if route.get("status") != "selected":
                errors.append(f"selected route {route_id} does not have selected status")
            for field in [
                "trigger",
                "variables",
                "assumptions",
                "relations",
                "constraints",
                "data_pipeline",
                "algorithm_steps",
                "algorithm_exit",
                "stress_tests",
                "output_schema",
                "validation",
                "failure_handling",
                "stopping_conditions",
            ]:
                if not route.get(field):
                    errors.append(f"selected route {route_id} has empty {field}")
            tests = route.get("stress_tests", [])
            categories = {
                test.get("category")
                for test in tests
                if isinstance(test, dict) and test.get("category") in STRESS_CATEGORIES
            }
            missing_categories = sorted(STRESS_CATEGORIES - categories)
            if missing_categories:
                errors.append(
                    f"selected route {route_id} lacks stress categories: {missing_categories}"
                )
            failed_tests = [
                test.get("category", "unnamed")
                for test in tests
                if isinstance(test, dict) and test.get("status") in {"fail", "blocked"}
            ]
            if failed_tests:
                errors.append(
                    f"selected route {route_id} has unresolved stress tests: {failed_tests}"
                )
        if not document.get("iterations"):
            errors.append("no autonomous route stress/repair iteration is recorded")
        completed_phases = {
            phase
            for item in document.get("iterations", [])
            for phase in item.get("phases", [])
            if phase in LOOP_PHASES
        }
        missing_phases = sorted(REQUIRED_LOOP_PHASES - completed_phases)
        if missing_phases:
            errors.append(f"autonomous loop phases are incomplete: {missing_phases}")
        blocked_iterations = [
            item.get("id", "unnamed")
            for item in document.get("iterations", [])
            if item.get("status") == "blocked"
        ]
        if blocked_iterations:
            errors.append(f"route iterations remain blocked: {blocked_iterations}")
        final_scan = document.get("final_gate_rescan", {})
        if final_scan.get("status") != "complete" or not final_scan.get("evidence"):
            errors.append("final 18-gate rescan is not complete with evidence")
        readiness = document.get("competition_readiness", {})
        if readiness.get("status") != "ready":
            errors.append("competition readiness is not ready")
        if readiness.get("audit_passes", 0) < 2:
            errors.append("competition readiness requires at least two complete audit passes")
        pass_records = readiness.get("pass_records", [])
        completed_records = [
            item for item in pass_records if isinstance(item, dict) and item.get("status") == "complete"
        ]
        if readiness.get("audit_passes") != len(completed_records):
            errors.append("competition audit_passes does not match completed pass records")
        completed_kinds = {item.get("kind") for item in completed_records}
        for kind in ["source_falsification", "competition_readiness"]:
            if kind not in completed_kinds:
                errors.append(f"competition readiness lacks completed {kind} pass")
        for item in pass_records:
            if not isinstance(item, dict):
                continue
            if item.get("status") == "blocked":
                errors.append(f"competition pass {item.get('id')} remains blocked")
            if not specific_text(item.get("scope")) or not specific_evidence(item.get("evidence")):
                errors.append(f"competition pass {item.get('id')} lacks specific scope or evidence")
        for item in readiness.get("dimensions", []):
            if (
                item.get("status") != "pass"
                or not specific_text(item.get("method"))
                or not specific_evidence(item.get("evidence"))
            ):
                errors.append(f"competition dimension {item.get('id')} has not passed with evidence")
        for item in readiness.get("experience_checks", []):
            if (
                item.get("status") not in {"pass", "not_applicable"}
                or not specific_evidence(item.get("evidence"))
            ):
                errors.append(f"experience check {item.get('id')} is unresolved or unjustified")
        certificate = readiness.get("stop_certificate", {})
        for field in ["retained_route_roles", "covered_outputs", "handoff_artifacts"]:
            if not certificate.get(field):
                errors.append(f"competition stop certificate has empty {field}")
        for field in ["no_further_complexity_reason", "conclusion_ceiling"]:
            value = certificate.get(field)
            if not specific_text(value):
                errors.append(f"competition stop certificate has empty {field}")
        retained_roles = certificate.get("retained_route_roles", [])
        retained_ids = [
            item.get("route_id") for item in retained_roles if isinstance(item, dict)
        ]
        if set(retained_ids) != set(selected_ids) or len(retained_ids) != len(selected_ids):
            errors.append("competition stop certificate does not map every selected route exactly once")
        for item in retained_roles:
            if isinstance(item, dict) and not specific_text(item.get("responsibility")):
                errors.append(f"competition retained route {item.get('route_id')} lacks a specific responsibility")
        expected_outputs = {
            (item.get("id"), output)
            for item in subquestions
            for output in item.get("outputs", [])
        }
        covered_outputs = certificate.get("covered_outputs", [])
        covered_pairs = [
            (item.get("subquestion_id"), item.get("output"))
            for item in covered_outputs
            if isinstance(item, dict)
        ]
        if set(covered_pairs) != expected_outputs or len(covered_pairs) != len(expected_outputs):
            errors.append("competition stop certificate does not map every official output exactly once")
        for item in covered_outputs:
            if not isinstance(item, dict):
                continue
            if item.get("producer_route_id") not in selected_ids:
                errors.append(
                    f"competition output {item.get('subquestion_id')}:{item.get('output')} uses an unselected producer"
                )
        excellence = document.get("excellence_assurance", {})
        if excellence.get("status") != "ready":
            errors.append("excellence assurance is not ready")
        dimensions = excellence.get("dimensions", [])
        for item in dimensions:
            if not isinstance(item, dict):
                continue
            if item.get("status") not in {"meets_reference", "exceeds_reference"}:
                errors.append(f"excellence dimension {item.get('id')} does not meet the reference bar")
            if not all(
                [
                    specific_text(item.get("reference_bar")),
                    specific_evidence(item.get("route_evidence")),
                    specific_text(item.get("delta")),
                    specific_text(item.get("method")),
                ]
            ):
                errors.append(f"excellence dimension {item.get('id')} lacks specific evidence or method")
        exceeded = {
            item.get("id")
            for item in dimensions
            if isinstance(item, dict) and item.get("status") == "exceeds_reference"
        }
        if len(exceeded) < 2:
            errors.append("excellence assurance requires at least two exceeded dimensions")
        if not exceeded.intersection({"mathematical_rigor", "validation_and_falsification"}):
            errors.append("excellence assurance lacks a rigor or falsification advance")
        advances = excellence.get("advances", [])
        verified_advances = [
            item for item in advances if isinstance(item, dict) and item.get("status") == "verified"
        ]
        if len(verified_advances) < 2:
            errors.append("excellence assurance requires at least two verified advances")
        categories = {item.get("category") for item in verified_advances}
        if len(categories) < 2:
            errors.append("verified excellence advances must cover at least two categories")
        if not categories.intersection({"correctness", "validation"}):
            errors.append("verified excellence advances lack correctness or validation")
        for item in advances:
            if not isinstance(item, dict):
                continue
            if item.get("status") != "verified":
                errors.append(f"excellence advance {item.get('id')} is not verified")
            if item.get("dimension_id") not in exceeded:
                errors.append(f"excellence advance {item.get('id')} does not map to an exceeded dimension")
            if not all(
                specific_text(item.get(field))
                for field in [
                    "trigger",
                    "reference_limit",
                    "improvement",
                    "ablation",
                    "verification",
                    "cost",
                ]
            ) or not specific_evidence(item.get("evidence")):
                errors.append(f"excellence advance {item.get('id')} lacks a specific ablation or evidence chain")
        basis = excellence.get("benchmark_basis")
        scope = excellence.get("claim_scope")
        expected_scope = {
            "generalized_historical_process": "generalized_process_standard",
            "same_problem_opt_in": "same_problem_comparative",
            "blind_external_evaluation": "blind_external_validated",
        }.get(basis)
        if scope != expected_scope:
            errors.append("excellence benchmark basis and claim scope disagree")
        if basis in {"same_problem_opt_in", "blind_external_evaluation"} and not specific_evidence(
            excellence.get("external_evidence")
        ):
            errors.append("comparative or blind excellence claim lacks external evidence")
        if excellence.get("award_guarantee") is not False:
            errors.append("award guarantee must remain false")
        human_review = document.get("human_review", {})
        if human_review.get("status") != "approved":
            errors.append("human review is not approved")
        unresolved_decisions = [
            item.get("id", "unnamed")
            for item in human_review.get("decision_points", [])
            if isinstance(item, dict) and item.get("status") in {"pending", "reopened"}
        ]
        if unresolved_decisions:
            errors.append(f"human review decisions remain unresolved: {unresolved_decisions}")
        for item in human_review.get("decision_points", []):
            if not isinstance(item, dict) or item.get("status") == "superseded":
                continue
            if (
                item.get("status") != "user_confirmed"
                or not specific_text(item.get("summary"))
                or not specific_text(item.get("recommendation"))
                or not specific_evidence(item.get("evidence"))
                or not isinstance(item.get("options"), list)
                or len(item.get("options")) < 2
                or not isinstance(item.get("consequences"), list)
                or len(item.get("consequences")) != len(item.get("options"))
                or not all(specific_text(value) for value in item.get("options", []))
                or not all(specific_text(value) for value in item.get("consequences", []))
                or not specific_text(item.get("resolution"))
            ):
                errors.append(
                    f"human review decision {item.get('id')} lacks a complete recommendation-backed approval record"
                )
            matching_locks = [
                lock
                for lock in document.get("locks", [])
                if isinstance(lock, dict)
                and lock.get("confirmation") == "user_confirmed"
                and item.get("id") in lock.get("dependencies", [])
            ]
            if not matching_locks:
                errors.append(
                    f"human review decision {item.get('id')} is not preserved by a user-confirmed lock"
                )
        final_review = human_review.get("final_route_review", {})
        if final_review.get("status") != "user_approved":
            errors.append("final route review is not user-approved")
        if not specific_text(final_review.get("reviewed_artifact")):
            errors.append("final route review lacks the exact reviewed artifact")
        if not specific_text(final_review.get("recommendation")):
            errors.append("final route review lacks a specific recommendation")
        if not specific_evidence(final_review.get("evidence")):
            errors.append("final route review lacks specific approval evidence")
    return errors


def project_workspace(project_manifest: Path | None, case_id: str) -> dict:
    if project_manifest is None:
        return {"root": None, "manifest": None, "status": "uninitialized"}
    manifest_path = project_manifest.resolve()
    manifest = load_json(manifest_path)
    if manifest.get("format") != "shhh-strategy-project":
        raise ValueError("project manifest format is invalid")
    if manifest.get("case_id") != case_id:
        raise ValueError("project manifest case_id does not match ledger case_id")
    root = Path(manifest.get("root", "")).resolve()
    if not root.is_dir():
        raise ValueError("project root recorded in manifest does not exist")
    return {"root": str(root), "manifest": str(manifest_path), "status": "confirmed"}


def new_document(
    case_id: str, inventory_path: Path | None, project_manifest: Path | None = None
) -> dict:
    now = utc_now()
    inventory = {"path": None, "sha256": None, "status": "missing"}
    if inventory_path is not None:
        inventory_doc = load_json(inventory_path)
        inventory = {
            "path": str(inventory_path.resolve()),
            "sha256": sha256_file(inventory_path),
            "status": "complete"
            if inventory_doc.get("overall_status") == "complete"
            else "blocked"
            if inventory_doc.get("overall_status") == "blocked"
            else "inventoried",
        }
    document = {
        "schema_version": "1.4",
        "case_id": case_id,
        "created_utc": now,
        "updated_utc": now,
        "quality_state": "draft",
        "project_workspace": project_workspace(project_manifest, case_id),
        "scope_contract": strategy_only_scope(),
        "instruction_sources": {
            "user_directives": [],
            "statement_requirements": [],
            "attachment_requirements": [],
            "embedded_commands": [],
            "conflicts": [],
        },
        "human_review": empty_human_review(),
        "final_gate_rescan": {"status": "pending", "evidence": []},
        "competition_readiness": empty_competition_readiness(),
        "excellence_assurance": empty_excellence_assurance(),
        "source_inventory": inventory,
        "subquestions": [],
        "activated_gates": [],
        "ambiguities": [],
        "locks": [],
        "routes": {"baseline_id": None, "selected_ids": [], "items": []},
        "validation_items": [],
        "claim_boundaries": [],
        "results": [],
        "iterations": [],
        "events": [],
    }
    append_event(document, "init", "analysis ledger created")
    return document


def upgrade_document(document: dict) -> bool:
    version = document.get("schema_version")
    if version not in {"1.0", "1.1", "1.2", "1.3", "1.4"}:
        raise ValueError(f"unsupported schema version: {version}")
    changed = False
    if version == "1.0":
        document["schema_version"] = "1.1"
        document.setdefault(
            "project_workspace", {"root": None, "manifest": None, "status": "uninitialized"}
        )
        document.setdefault(
            "instruction_sources",
            {
                "user_directives": [],
                "statement_requirements": [],
                "attachment_requirements": [],
                "embedded_commands": [],
                "conflicts": [],
            },
        )
        document.setdefault("iterations", [])
        document.setdefault("final_gate_rescan", {"status": "pending", "evidence": []})
        for route in document.get("routes", {}).get("items", []):
            route.setdefault("assumptions", [])
            route.setdefault("data_pipeline", [])
            route.setdefault("algorithm_steps", [])
            route.setdefault("stress_tests", [])
            route.setdefault("failure_handling", [])
            route.setdefault("stopping_conditions", [])
        append_event(document, "upgrade:1.0->1.1", "V27.3 execution fields added; populate before promotion")
        version = "1.1"
        changed = True
    if version == "1.1":
        document["schema_version"] = "1.2"
        document.setdefault("competition_readiness", empty_competition_readiness())
        append_event(
            document,
            "upgrade:1.1->1.2",
            "V27.4 competition-readiness fields added; complete them before route_executable promotion",
        )
        changed = True
        version = "1.2"
    if version == "1.2":
        document["schema_version"] = "1.3"
        document.setdefault("excellence_assurance", empty_excellence_assurance())
        append_event(
            document,
            "upgrade:1.2->1.3",
            "V27.5 excellence-assurance fields added; verify deltas before route_executable promotion",
        )
        changed = True
        version = "1.3"
    if version == "1.3":
        document["schema_version"] = "1.4"
        document.setdefault("scope_contract", strategy_only_scope())
        document.setdefault("human_review", empty_human_review())
        if document.get("quality_state") in {"solved_unvalidated", "solved_and_validated"}:
            document["quality_state"] = "route_executable"
        append_event(
            document,
            "upgrade:1.3->1.4",
            "V27.6 strategy-only scope and recommendation-backed human review added; prior solve states collapse to route_executable while historical result records are preserved",
        )
        changed = True
    return changed


def print_result(status: str, path: Path, errors: list[str] | None = None) -> None:
    print(
        json.dumps(
            {"status": status, "path": str(path.resolve()), "errors": errors or []},
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init")
    init.add_argument("--case-id", required=True)
    init.add_argument("--output", type=Path, required=True)
    init.add_argument("--inventory", type=Path)
    init.add_argument("--project-manifest", type=Path)

    validate = subparsers.add_parser("validate")
    validate.add_argument("state", type=Path)

    seal = subparsers.add_parser("seal")
    seal.add_argument("state", type=Path)
    seal.add_argument("--reason", required=True)

    transition = subparsers.add_parser("transition")
    transition.add_argument("state", type=Path)
    transition.add_argument("--to", choices=QUALITY_STATES, required=True)
    transition.add_argument("--reason", required=True)

    set_inventory = subparsers.add_parser("set-inventory")
    set_inventory.add_argument("state", type=Path)
    set_inventory.add_argument("inventory", type=Path)

    summary = subparsers.add_parser("summary")
    summary.add_argument("state", type=Path)

    upgrade = subparsers.add_parser("upgrade")
    upgrade.add_argument("state", type=Path)

    args = parser.parse_args()
    if args.command == "init":
        if args.inventory is not None and not args.inventory.is_file():
            raise FileNotFoundError(args.inventory)
        if args.project_manifest is not None and not args.project_manifest.is_file():
            raise FileNotFoundError(args.project_manifest)
        document = new_document(args.case_id, args.inventory, args.project_manifest)
        atomic_write(args.output, document)
        print_result("PASS", args.output)
        return 0

    state_path = args.state.resolve()
    document = load_json(state_path)

    if args.command == "upgrade":
        try:
            changed = upgrade_document(document)
        except ValueError as error:
            print_result("FAIL", state_path, [str(error)])
            return 1
        if changed:
            atomic_write(state_path, document)
        errors = validate_structure(document, require_current_event=True)
        print_result("PASS" if not errors else "FAIL", state_path, errors)
        return 1 if errors else 0

    if args.command == "validate":
        errors = validate_structure(document, require_current_event=True)
        print_result("PASS" if not errors else "FAIL", state_path, errors)
        return 1 if errors else 0

    if args.command == "seal":
        errors = validate_structure(document, require_current_event=False)
        if errors:
            print_result("FAIL", state_path, errors)
            return 1
        append_event(document, "seal", args.reason)
        atomic_write(state_path, document)
        print_result("PASS", state_path)
        return 0

    if args.command == "set-inventory":
        current_errors = validate_structure(document, require_current_event=True)
        if current_errors:
            print_result("FAIL", state_path, current_errors)
            return 1
        inventory_path = args.inventory.resolve()
        inventory_doc = load_json(inventory_path)
        overall = inventory_doc.get("overall_status")
        document["source_inventory"] = {
            "path": str(inventory_path),
            "sha256": sha256_file(inventory_path),
            "status": "complete"
            if overall == "complete"
            else "blocked"
            if overall == "blocked"
            else "inventoried",
        }
        append_event(document, "set_inventory", f"source inventory linked: {inventory_path.name}")
        atomic_write(state_path, document)
        print_result("PASS", state_path)
        return 0

    if args.command == "transition":
        errors = validate_structure(document, require_current_event=False)
        errors.extend(transition_errors(document, args.to))
        if errors:
            print_result("FAIL", state_path, errors)
            return 1
        old_state = document["quality_state"]
        document["quality_state"] = args.to
        append_event(document, f"transition:{old_state}->{args.to}", args.reason)
        atomic_write(state_path, document)
        print_result("PASS", state_path)
        return 0

    errors = validate_structure(document, require_current_event=True)
    summary_payload = {
        "status": "PASS" if not errors else "FAIL",
        "case_id": document.get("case_id"),
        "quality_state": document.get("quality_state"),
        "inventory_status": document.get("source_inventory", {}).get("status"),
        "subquestions": len(document.get("subquestions", [])),
        "activated_gates": [item.get("gate") for item in document.get("activated_gates", [])],
        "open_blocking_ambiguities": [
            item.get("id")
            for item in document.get("ambiguities", [])
            if item.get("blocking") and item.get("status") == "open"
        ],
        "selected_routes": document.get("routes", {}).get("selected_ids", []),
        "project_root": document.get("project_workspace", {}).get("root"),
        "iterations": len(document.get("iterations", [])),
        "competition_readiness": document.get("competition_readiness", {}).get("status"),
        "competition_audit_passes": document.get("competition_readiness", {}).get("audit_passes"),
        "excellence_assurance": document.get("excellence_assurance", {}).get("status"),
        "excellence_claim_scope": document.get("excellence_assurance", {}).get("claim_scope"),
        "scope_mode": document.get("scope_contract", {}).get("mode"),
        "human_review": document.get("human_review", {}).get("status"),
        "pending_human_decisions": [
            item.get("id")
            for item in document.get("human_review", {}).get("decision_points", [])
            if item.get("status") in {"pending", "reopened"}
        ],
        "final_route_review": document.get("human_review", {})
        .get("final_route_review", {})
        .get("status"),
        "events": len(document.get("events", [])),
        "errors": errors,
    }
    print(json.dumps(summary_payload, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
