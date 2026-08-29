#!/usr/bin/env python3
"""Create an auditable pre-comparison freeze for one problem analysis."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from analysis_state import load_json as load_state_json
from analysis_state import validate_structure as validate_analysis_state


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def source_record(path: Path) -> dict:
    resolved = path.resolve()
    if resolved.is_file():
        return {
            "path": str(resolved),
            "type": "file",
            "size": resolved.stat().st_size,
            "sha256": sha256_file(resolved),
        }
    if resolved.is_dir():
        files = []
        for child in sorted(p for p in resolved.rglob("*") if p.is_file()):
            files.append(
                {
                    "relative_path": str(child.relative_to(resolved)),
                    "size": child.stat().st_size,
                    "sha256": sha256_file(child),
                }
            )
        directory_digest = hashlib.sha256(
            json.dumps(files, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest().upper()
        return {
            "path": str(resolved),
            "type": "directory",
            "files": files,
            "sha256": directory_digest,
        }
    raise FileNotFoundError(str(resolved))


def safe_case_id(value: str) -> str:
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    normalized = "".join(ch if ch in allowed else "_" for ch in value.strip())
    if not normalized:
        raise ValueError("case id cannot be empty")
    return normalized


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Hash the complete problem sources and independent analysis for an auditable freeze."
    )
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--analysis", required=True, type=Path)
    parser.add_argument("--source", action="append", required=True, type=Path)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path.cwd() / "shhh-freezes")
    parser.add_argument(
        "--state",
        choices=[
            "understanding_locked",
            "audit_complete",
            "route_executable",
            "solved_unvalidated",
            "solved_and_validated",
        ],
        default="route_executable",
    )
    args = parser.parse_args()

    analysis = args.analysis.resolve()
    if not analysis.is_file():
        raise FileNotFoundError(f"analysis file not found: {analysis}")

    source_paths = [path.resolve() for path in args.source]
    missing = [str(path) for path in source_paths if not path.exists()]
    if missing:
        raise FileNotFoundError("missing source(s): " + "; ".join(missing))

    ledger_record = None
    if args.ledger is not None:
        ledger_path = args.ledger.resolve()
        if not ledger_path.is_file():
            raise FileNotFoundError(f"ledger file not found: {ledger_path}")
        ledger = load_state_json(ledger_path)
        ledger_errors = validate_analysis_state(ledger, require_current_event=True)
        if ledger_errors:
            raise ValueError("invalid analysis ledger: " + "; ".join(ledger_errors))
        if ledger.get("quality_state") != args.state:
            raise ValueError(
                f"ledger quality state {ledger.get('quality_state')} != requested freeze state {args.state}"
            )
        ledger_record = source_record(ledger_path)

    case_id = safe_case_id(args.case_id)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{case_id}_freeze.json"

    payload = {
        "protocol": "v27.2_problem_sources_inventory_ledger_and_independent_analysis_before_same_problem_comparison",
        "case_id": args.case_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "quality_state": args.state,
        "analysis": source_record(analysis),
        "analysis_ledger": ledger_record,
        "sources": [source_record(path) for path in source_paths],
        "limitations": [
            "A freeze proves file integrity and ordering, not analytical correctness.",
            "Historical public problems may still exist in model pretraining data.",
        ],
    }
    payload_bytes = json.dumps(
        payload, ensure_ascii=False, indent=2, sort_keys=True
    ).encode("utf-8")
    payload["freeze_payload_sha256"] = hashlib.sha256(payload_bytes).hexdigest().upper()
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
