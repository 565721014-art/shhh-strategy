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
    "solved_unvalidated",
    "solved_and_validated",
]


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
        "source_inventory",
        "subquestions",
        "activated_gates",
        "ambiguities",
        "locks",
        "routes",
        "validation_items",
        "claim_boundaries",
        "results",
        "events",
    }
    missing = sorted(required - set(document))
    if missing:
        errors.append(f"missing top-level fields: {missing}")
        return errors
    extra = sorted(set(document) - required)
    if extra:
        errors.append(f"unexpected top-level fields: {extra}")
    if document.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
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
        "events",
    ]
    for field in list_fields:
        if not isinstance(document.get(field), list):
            errors.append(f"{field} must be an array")
    if errors:
        return errors

    subquestion_ids = unique_ids(document["subquestions"], "subquestion", errors)
    ambiguity_ids = unique_ids(document["ambiguities"], "ambiguity", errors)
    lock_ids = unique_ids(document["locks"], "lock", errors)
    validation_ids = unique_ids(document["validation_items"], "validation", errors)
    claim_ids = unique_ids(document["claim_boundaries"], "claim", errors)
    result_ids = unique_ids(document["results"], "result", errors)
    del ambiguity_ids, lock_ids, validation_ids, claim_ids, result_ids

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
        "relations",
        "constraints",
        "algorithm_exit",
        "output_schema",
        "validation",
        "rejection_condition",
    }
    for item in route_items:
        if isinstance(item, dict):
            require_fields(item, route_required, f"route {item.get('id')}", errors)
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
                "relations",
                "constraints",
                "algorithm_exit",
                "output_schema",
                "validation",
            ]:
                if not route.get(field):
                    errors.append(f"selected route {route_id} has empty {field}")

    if QUALITY_STATES.index(target) >= QUALITY_STATES.index("solved_unvalidated"):
        if not document["results"]:
            errors.append("no computed or constructive results are recorded")

    if target == "solved_and_validated":
        if not document["validation_items"]:
            errors.append("no validation items are recorded")
        failed = [
            item.get("id", "unnamed")
            for item in document["validation_items"]
            if item.get("blocking", True) and item.get("status") not in {"pass", "not_applicable"}
        ]
        if failed:
            errors.append(f"blocking validation has not passed: {failed}")
    return errors


def new_document(case_id: str, inventory_path: Path | None) -> dict:
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
        "schema_version": "1.0",
        "case_id": case_id,
        "created_utc": now,
        "updated_utc": now,
        "quality_state": "draft",
        "source_inventory": inventory,
        "subquestions": [],
        "activated_gates": [],
        "ambiguities": [],
        "locks": [],
        "routes": {"baseline_id": None, "selected_ids": [], "items": []},
        "validation_items": [],
        "claim_boundaries": [],
        "results": [],
        "events": [],
    }
    append_event(document, "init", "analysis ledger created")
    return document


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

    args = parser.parse_args()
    if args.command == "init":
        if args.inventory is not None and not args.inventory.is_file():
            raise FileNotFoundError(args.inventory)
        document = new_document(args.case_id, args.inventory)
        atomic_write(args.output, document)
        print_result("PASS", args.output)
        return 0

    state_path = args.state.resolve()
    document = load_json(state_path)

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
        "events": len(document.get("events", [])),
        "errors": errors,
    }
    print(json.dumps(summary_payload, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
