#!/usr/bin/env python3
"""Validate the installed skill and its mapped local knowledge archive."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1] / "knowledge"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    skill_dir = Path(__file__).resolve().parents[1]
    version_path = skill_dir / "references" / "version.json"
    version = load_json(version_path)
    configured_root = os.environ.get("SHHH_STRATEGY_KNOWLEDGE_ROOT")
    if configured_root:
        root = Path(configured_root).expanduser().resolve()
    else:
        default_root = Path(version["knowledge_root_default"])
        root = (
            (skill_dir / default_root).resolve()
            if not default_root.is_absolute()
            else default_root.resolve()
        )

    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    required_skill_files = [
        "SKILL.md",
        "agents/openai.yaml",
        "references/core-protocol.md",
        "references/structural-gates.md",
        "references/gates/task-semantics.md",
        "references/gates/identification-dynamics.md",
        "references/gates/data-claims.md",
        "references/gates/policy-global.md",
        "references/gates/validation-uncertainty.md",
        "references/input-visual-integrity.md",
        "references/state-ledger.md",
        "references/analysis-state.schema.json",
        "references/behavior-regression.md",
        "references/regression-observation.schema.json",
        "references/complexity-stop-gates.md",
        "references/historical-transfer-index.md",
        "references/output-modes.md",
        "references/paper-comparison.md",
        "references/post-route-stress-reread.md",
        "references/knowledge-source-map.md",
        "references/version.json",
        "references/completeness-audit.json",
        "scripts/freeze_analysis.py",
        "scripts/analysis_state.py",
        "scripts/inventory_problem.py",
        "scripts/evaluate_regression.py",
        "scripts/stability_self_test.py",
        "scripts/query_knowledge.py",
        "scripts/build_compact_knowledge.py",
        "scripts/refresh_compact_manifest.py",
        "scripts/validate_skill.py",
    ]
    for relative in required_skill_files:
        if not (skill_dir / relative).is_file():
            errors.append(f"missing skill file: {relative}")

    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    if "TODO" in skill_text:
        errors.append("SKILL.md still contains TODO")
    if "name: shhh-strategy" not in skill_text:
        errors.append("SKILL.md name mismatch")
    if version.get("engine_version") != "v27.2_stability_guarded":
        errors.append("engine version is not v27.2_stability_guarded")

    markdown_files = [skill_dir / "SKILL.md"] + sorted((skill_dir / "references").rglob("*.md"))
    for markdown_path in markdown_files:
        markdown_text = markdown_path.read_text(encoding="utf-8")
        for match in re.finditer(r"\]\(([^)#]+)(?:#[^)]*)?\)", markdown_text):
            target = match.group(1)
            if "://" in target:
                continue
            base = skill_dir if markdown_path == skill_dir / "SKILL.md" else markdown_path.parent
            if not (base / target).exists():
                errors.append(
                    f"broken markdown link in {markdown_path.relative_to(skill_dir)}: {target}"
                )

    gate_numbers = []
    for gate_path in sorted((skill_dir / "references" / "gates").glob("*.md")):
        gate_numbers.extend(
            int(value)
            for value in re.findall(
                r"^## (\d+)\.", gate_path.read_text(encoding="utf-8"), re.M
            )
        )
    if sorted(gate_numbers) != list(range(1, 19)):
        errors.append(f"structural gate coverage mismatch: {sorted(gate_numbers)}")

    for schema_name in ["analysis-state.schema.json", "regression-observation.schema.json"]:
        schema = load_json(skill_dir / "references" / schema_name)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"schema draft mismatch: {schema_name}")

    audit_path = skill_dir / "references" / "completeness-audit.json"
    if audit_path.is_file():
        audit = load_json(audit_path)
        packaging = audit.get("packaging", {})
        actual_reference_files = sum(
            1 for path in (skill_dir / "references").rglob("*") if path.is_file()
        )
        actual_script_files = sum(
            1
            for path in (skill_dir / "scripts").iterdir()
            if path.is_file() and path.suffix == ".py"
        )
        if packaging.get("reference_files") != actual_reference_files:
            errors.append(
                "completeness audit reference count mismatch: "
                f"{packaging.get('reference_files')} != {actual_reference_files}"
            )
        if packaging.get("script_files") != actual_script_files:
            errors.append(
                "completeness audit script count mismatch: "
                f"{packaging.get('script_files')} != {actual_script_files}"
            )
        for relative, expected_hash in audit.get("internal_sha256", {}).items():
            path = skill_dir / relative
            if not path.is_file():
                errors.append(f"completeness audit missing hashed file: {relative}")
            elif sha256(path) != str(expected_hash).upper():
                errors.append(f"completeness audit hash mismatch: {relative}")

    history_index = (
        skill_dir / "references" / "historical-transfer-index.md"
    ).read_text(encoding="utf-8")
    expected_case_ids = {
        "2016A",
        "2016B",
        "2017A",
        "2017B",
        "2017C",
        "2018B",
        "2020A",
        "2020B",
        "2020C",
        "2021A",
        "2021B",
        "2021C",
        "2021D",
        "2021E",
        "2022A",
        "2022B",
        "2022C",
        "2022D",
        "2022E",
        "2023A",
        "2023B",
        "2023C",
        "2023D",
        "2023E",
        "2024A",
        "2024B",
        "2024C",
        "2024D",
        "2024E",
        "2025A",
        "2025B",
        "2025C",
        "2025D",
        "2025E",
    }
    indexed_case_ids = set(re.findall(r"\| (20\d{2}[A-E]) ", history_index))
    if indexed_case_ids != expected_case_ids:
        missing = sorted(expected_case_ids - indexed_case_ids)
        extra = sorted(indexed_case_ids - expected_case_ids)
        errors.append(f"historical index mismatch; missing={missing}, extra={extra}")

    compact_manifest_path = root / "compact_manifest.json"
    compact_mode = compact_manifest_path.is_file()
    if not root.exists():
        warnings.append(
            f"optional knowledge root missing: {root}; core strategy files are still validated"
        )
    else:
        textbook_path = root / "国一论文成品教材" / "textbook_manifest.json"
        iteration_path = root / "迭代训练" / "iteration_manifest.json"
        corpus_path = root / "index" / "corpus_manifest.json"
        matrix_path = (
            root
            / "model_versions"
            / "v27_1_complexity_guarded"
            / "往届34题防误删训练.md"
        )
        archive_required = [textbook_path, iteration_path, corpus_path]
        if not compact_mode:
            archive_required.append(matrix_path)
        for path in archive_required:
            if not path.is_file():
                errors.append(f"missing archive file: {path}")

        if not errors:
            textbook = load_json(textbook_path)
            iteration = load_json(iteration_path)
            corpus = load_json(corpus_path)
            if textbook.get("problems") != 23 or textbook.get("papers") != 58:
                errors.append("textbook manifest is not 23 problems / 58 papers")
            if iteration.get("counts", {}).get("problems_completed") != 23:
                errors.append("iteration manifest does not show 23 completed problems")
            if iteration.get("counts", {}).get("papers_compared") != 58:
                errors.append("iteration manifest does not show 58 compared papers")
            corpus_counts = corpus.get("counts", {})
            expected_counts = version["coverage"]
            for key in [
                "problems",
                "papers",
                "paper_pages",
                "statement_pages",
                "attachments",
                "visual_hint_pages",
            ]:
                expected_key = {
                    "problems": "primary_training_problems",
                    "papers": "paper_records",
                }.get(key, key)
                if corpus_counts.get(key) != expected_counts.get(expected_key):
                    errors.append(
                        f"corpus count mismatch {key}: {corpus_counts.get(key)} != {expected_counts.get(expected_key)}"
                    )

            for chapter in textbook.get("chapters", []):
                path = root / "国一论文成品教材" / chapter["chapter"]
                if not path.is_file():
                    errors.append(f"missing chapter: {path}")
            for paper in corpus.get("papers", []):
                paper_keys = ["card_path"]
                if not compact_mode:
                    paper_keys.append("gallery_path")
                for key in paper_keys:
                    path = root / paper[key]
                    if not path.exists():
                        errors.append(f"missing paper {key}: {path}")

            if compact_mode:
                compact = load_json(compact_manifest_path)
                if compact.get("format") != "shhh-strategy-compact-knowledge":
                    errors.append("compact manifest format mismatch")
                if compact.get("knowledge_mode") != "compact":
                    errors.append("compact manifest knowledge_mode mismatch")
                included = compact.get("included", {})
                actual_files = sorted(
                    path
                    for path in root.rglob("*")
                    if path.is_file() and path != compact_manifest_path
                )
                actual_relative = [
                    str(path.relative_to(root)).replace("\\", "/")
                    for path in actual_files
                ]
                expected_hashes = included.get("sha256", {})
                expected_names = set(expected_hashes)
                actual_names = set(actual_relative)
                if expected_names != actual_names:
                    errors.append(
                        "compact manifest file list mismatch; "
                        f"missing={sorted(expected_names - actual_names)}, "
                        f"extra={sorted(actual_names - expected_names)}"
                    )
                if included.get("files") != len(actual_files):
                    errors.append(
                        f"compact manifest file count mismatch: {included.get('files')} != {len(actual_files)}"
                    )
                actual_bytes = sum(path.stat().st_size for path in actual_files)
                if included.get("bytes") != actual_bytes:
                    errors.append(
                        f"compact manifest byte count mismatch: {included.get('bytes')} != {actual_bytes}"
                    )
                actual_suffixes = dict(
                    sorted(
                        Counter(
                            path.suffix.lower() or "[no extension]"
                            for path in actual_files
                        ).items()
                    )
                )
                if included.get("suffix_counts") != actual_suffixes:
                    errors.append("compact manifest suffix counts mismatch")
                for relative in sorted(expected_names & actual_names):
                    actual_hash = sha256(root / relative).lower()
                    if actual_hash != str(expected_hashes[relative]).lower():
                        errors.append(f"compact manifest hash mismatch: {relative}")
                notes.append(
                    "compact knowledge mode: raw PDFs, spreadsheets, images and full OCR remain external"
                )
            else:
                matrix_text = matrix_path.read_text(encoding="utf-8")
                rows = re.findall(r"^\| 20(?:16|17|18|20|21|22|23|24|25)[A-E] ", matrix_text, re.M)
                if len(rows) != 34:
                    errors.append(f"historical matrix row count is {len(rows)}, expected 34")

                source_paths = {
                    "v27_1_engine_manifest": root
                    / "model_versions"
                    / "v27_1_complexity_guarded"
                    / "engine_manifest.json",
                    "v27_1_complexity_gate": root
                    / "model_versions"
                    / "v27_1_complexity_guarded"
                    / "复杂度_证据_停止门.md",
                    "v27_1_historical_34_matrix": matrix_path,
                    "v26_engine_manifest": root
                    / "model_versions"
                    / "v26_post_23_iteration_frozen"
                    / "engine_manifest.json",
                    "textbook_manifest": textbook_path,
                    "iteration_manifest": iteration_path,
                    "corpus_manifest": corpus_path,
                }
                for key, expected_hash in version["source_hashes"].items():
                    path = source_paths[key]
                    if sha256(path) != expected_hash:
                        errors.append(f"source hash mismatch: {key}")

    if errors:
        status = "FAIL"
    elif warnings:
        status = "WARN"
    else:
        status = "PASS"
    result = {
        "status": status,
        "skill_dir": str(skill_dir),
        "knowledge_root": str(root),
        "errors": errors,
        "warnings": warnings,
        "notes": notes,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
