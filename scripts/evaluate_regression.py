#!/usr/bin/env python3
"""Validate behavioral observations and compare a candidate with a baseline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DIMENSIONS = [
    "source_integrity",
    "problem_lock",
    "trigger_fidelity",
    "route_executability",
    "complexity_discipline",
    "validation_strength",
    "excellence_delta_integrity",
    "claim_boundary",
    "confirmation_discipline",
    "human_decision_review",
    "strategy_scope_discipline",
    "state_continuity",
]
NON_REGRESSION_DIMENSIONS = {
    "source_integrity",
    "problem_lock",
    "trigger_fidelity",
    "claim_boundary",
    "confirmation_discipline",
    "human_decision_review",
    "strategy_scope_discipline",
}
TARGETED_STABILITY_DIMENSIONS = {
    "validation_strength",
    "excellence_delta_integrity",
    "human_decision_review",
    "strategy_scope_discipline",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"observation must be an object: {path}")
    return value


def validate(document: dict) -> list[str]:
    errors: list[str] = []
    if document.get("format") != "shhh-strategy-regression-observation":
        errors.append("format mismatch")
    if not document.get("version"):
        errors.append("version is missing")
    if document.get("evaluation_status") not in {"development", "blind", "contaminated"}:
        errors.append("evaluation_status is invalid")
    cases = document.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty array")
        return errors
    seen = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"case {index} is not an object")
            continue
        case_id = case.get("case_id")
        if not case_id or case_id in seen:
            errors.append(f"case {index} has missing or duplicate case_id")
        seen.add(case_id)
        if not case.get("mechanism_family"):
            errors.append(f"case {case_id} has no mechanism_family")
        scores = case.get("scores")
        if not isinstance(scores, dict):
            errors.append(f"case {case_id} has no scores object")
            continue
        if set(scores) != set(DIMENSIONS):
            errors.append(f"case {case_id} score dimensions mismatch")
        for dimension, score in scores.items():
            if not isinstance(score, int) or not 0 <= score <= 4:
                errors.append(f"case {case_id} has invalid {dimension} score")
        if not isinstance(case.get("critical_failures"), list):
            errors.append(f"case {case_id} critical_failures must be an array")
        if not isinstance(case.get("evidence"), list) or not case.get("evidence"):
            errors.append(f"case {case_id} needs evidence")
    return errors


def by_id(document: dict) -> dict[str, dict]:
    return {case["case_id"]: case for case in document["cases"]}


def total_score(document: dict) -> int:
    return sum(sum(case["scores"].values()) for case in document["cases"])


def compare(baseline: dict, candidate: dict) -> dict:
    baseline_cases = by_id(baseline)
    candidate_cases = by_id(candidate)
    errors: list[str] = []
    if set(baseline_cases) != set(candidate_cases):
        errors.append(
            f"case sets differ; missing={sorted(set(baseline_cases) - set(candidate_cases))}, extra={sorted(set(candidate_cases) - set(baseline_cases))}"
        )
        return {"status": "FAIL", "promote": False, "errors": errors}

    critical_failures = {
        case_id: case["critical_failures"]
        for case_id, case in candidate_cases.items()
        if case["critical_failures"]
    }
    if critical_failures:
        errors.append(f"candidate has critical failures: {critical_failures}")

    regressions = []
    improved_families_by_dimension = {
        dimension: set() for dimension in TARGETED_STABILITY_DIMENSIONS
    }
    details = []
    for case_id in sorted(baseline_cases):
        base = baseline_cases[case_id]
        cand = candidate_cases[case_id]
        delta = {dimension: cand["scores"][dimension] - base["scores"][dimension] for dimension in DIMENSIONS}
        for dimension in NON_REGRESSION_DIMENSIONS:
            if delta[dimension] < 0:
                regressions.append(f"{case_id}:{dimension}:{delta[dimension]}")
        for dimension in TARGETED_STABILITY_DIMENSIONS:
            if delta[dimension] > 0:
                improved_families_by_dimension[dimension].add(cand["mechanism_family"])
        details.append({"case_id": case_id, "mechanism_family": cand["mechanism_family"], "delta": delta})
    if regressions:
        errors.append(f"critical-dimension regressions: {regressions}")

    baseline_total = total_score(baseline)
    candidate_total = total_score(candidate)
    if candidate_total < baseline_total:
        errors.append(f"total score regressed: {candidate_total} < {baseline_total}")
    for dimension, families in improved_families_by_dimension.items():
        if len(families) < 2:
            errors.append(
                f"{dimension} improvement was not demonstrated on two structurally different mechanism families"
            )
    if baseline.get("evaluation_status") != candidate.get("evaluation_status"):
        errors.append("baseline and candidate evaluation_status differ")
    if candidate.get("evaluation_status") == "contaminated":
        errors.append("contaminated observations cannot support promotion")

    return {
        "status": "PASS" if not errors else "FAIL",
        "promote": not errors,
        "baseline_version": baseline.get("version"),
        "candidate_version": candidate.get("version"),
        "evaluation_status": candidate.get("evaluation_status"),
        "baseline_total": baseline_total,
        "candidate_total": candidate_total,
        "improved_mechanism_families": {
            dimension: sorted(families)
            for dimension, families in sorted(improved_families_by_dimension.items())
        },
        "details": details,
        "errors": errors,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()

    candidate = load(args.candidate)
    errors = validate(candidate)
    if args.baseline is None:
        result = {"status": "PASS" if not errors else "FAIL", "version": candidate.get("version"), "errors": errors}
    else:
        baseline = load(args.baseline)
        baseline_errors = validate(baseline)
        if errors or baseline_errors:
            result = {"status": "FAIL", "promote": False, "errors": [f"candidate: {item}" for item in errors] + [f"baseline: {item}" for item in baseline_errors]}
        else:
            result = compare(baseline, candidate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
