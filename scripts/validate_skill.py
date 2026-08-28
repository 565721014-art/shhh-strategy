#!/usr/bin/env python3
"""Validate the installed skill and its mapped local knowledge archive."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
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

    required_skill_files = [
        "SKILL.md",
        "agents/openai.yaml",
        "references/core-protocol.md",
        "references/structural-gates.md",
        "references/input-visual-integrity.md",
        "references/complexity-stop-gates.md",
        "references/historical-transfer-index.md",
        "references/output-modes.md",
        "references/paper-comparison.md",
        "references/knowledge-source-map.md",
        "references/version.json",
        "references/completeness-audit.json",
        "scripts/freeze_analysis.py",
        "scripts/query_knowledge.py",
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

    for match in re.finditer(r"\]\(([^)]+)\)", skill_text):
        target = match.group(1)
        if "://" not in target and not (skill_dir / target).exists():
            errors.append(f"broken SKILL.md link: {target}")

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
        for path in [textbook_path, iteration_path, corpus_path, matrix_path]:
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
                for key in ["card_path", "gallery_path"]:
                    path = root / paper[key]
                    if not path.exists():
                        errors.append(f"missing paper {key}: {path}")

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
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
