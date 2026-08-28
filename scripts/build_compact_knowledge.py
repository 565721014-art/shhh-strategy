#!/usr/bin/env python3
"""Build a token-efficient, text-first derivative of the SHHH knowledge archive.

The source archive is never modified.  The compact derivative keeps the
structured problem/paper cards and strategy records needed for automatic
retrieval, while leaving raw PDFs, spreadsheets, page images, full OCR and
executables in the user's external archive.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


TEXT_EXTENSIONS = {".md", ".json", ".txt"}
ROOT_FILES = {
    "data_structure.md",
    "国一赛题分析思考手册.md",
}
INDEX_FILES = {
    "corpus_manifest.json",
    "logic_index.json",
    "quality_report.md",
    "navigation_quality_report.md",
}
PROBLEM_FILES = {
    "data_structure.md",
    "logic_map.json",
    "problem_card.md",
    "problem_manifest.json",
}
PAPER_FILES = {"paper_card.md", "problem_analysis_excerpt.txt", "page_index.json"}


def copy_one(source: Path, destination: Path, selected: list[Path]) -> None:
    if not source.is_file():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    selected.append(destination)


def copy_text_tree(
    source: Path,
    destination: Path,
    selected: list[Path],
    excluded_dirs: set[str] | None = None,
) -> None:
    if not source.is_dir():
        return
    excluded_dirs = excluded_dirs or set()
    for path in sorted(source.rglob("*")):
        relative_parts = set(path.relative_to(source).parts)
        if relative_parts & excluded_dirs:
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            copy_one(path, destination / path.relative_to(source), selected)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def sanitize_json_value(value: object) -> object:
    """Remove workstation-specific absolute paths from copied JSON records."""
    if isinstance(value, dict):
        return {key: sanitize_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_json_value(item) for item in value]
    if isinstance(value, str) and re.match(r"^[A-Za-z]:[\\/]", value):
        portable_name = value.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1]
        return f"EXTERNAL_FULL_ARCHIVE/{portable_name}"
    return value


def sanitize_copied_json(selected: list[Path]) -> None:
    for path in selected:
        if path.suffix.lower() != ".json":
            continue
        try:
            value = load_json(path)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        write_json(path, sanitize_json_value(value))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(source: Path, destination: Path) -> dict[str, object]:
    source = source.resolve()
    destination = destination.resolve()
    if not source.is_dir():
        raise FileNotFoundError(f"source archive not found: {source}")
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(
            f"destination must be new or empty; refusing to overwrite: {destination}"
        )
    destination.mkdir(parents=True, exist_ok=True)

    selected: list[Path] = []
    # Prefer the package's explanatory README so regenerated derivatives keep
    # the same compact/external-archive contract.
    template_readme = Path(__file__).resolve().parents[1] / "knowledge" / "README.md"
    copy_one(
        template_readme if template_readme.is_file() else source / "README.md",
        destination / "README.md",
        selected,
    )
    for name in sorted(ROOT_FILES):
        copy_one(source / name, destination / name, selected)

    for dirname in ["新题迁移分析引擎", "AI时代读题训练", "model_versions", "国一论文成品教材"]:
        copy_text_tree(source / dirname, destination / dirname, selected)

    copy_text_tree(source / "迭代训练", destination / "迭代训练", selected)
    copy_text_tree(
        source / "heldout_evaluation",
        destination / "heldout_evaluation",
        selected,
        excluded_dirs={"papers_unlocked", "papers_locked"},
    )

    for name in sorted(INDEX_FILES):
        copy_one(source / "index" / name, destination / "index" / name, selected)

    problems_source = source / "problems"
    for problem_dir in sorted(path for path in problems_source.iterdir() if path.is_dir()):
        problem_dest = destination / "problems" / problem_dir.name
        for name in sorted(PROBLEM_FILES):
            copy_one(problem_dir / name, problem_dest / name, selected)
        copy_one(
            problem_dir / "original" / "statement.txt",
            problem_dest / "original" / "statement.txt",
            selected,
        )
        papers_source = problem_dir / "papers"
        if papers_source.is_dir():
            for paper_dir in sorted(path for path in papers_source.iterdir() if path.is_dir()):
                paper_dest = problem_dest / "papers" / paper_dir.name
                for name in sorted(PAPER_FILES):
                    copy_one(paper_dir / name, paper_dest / name, selected)

    # The corpus manifest is useful for retrieval, but its absolute source root
    # would leak a workstation path into a portable package.
    corpus_path = destination / "index" / "corpus_manifest.json"
    if corpus_path.is_file():
        corpus = load_json(corpus_path)
        if isinstance(corpus, dict):
            corpus["root"] = "."
            corpus["knowledge_mode"] = "compact"
            corpus["raw_evidence_external"] = True
            write_json(corpus_path, corpus)

    sanitize_copied_json(selected)

    suffixes = Counter(path.suffix.lower() or "[no extension]" for path in selected)
    relative_files = [str(path.relative_to(destination)).replace("\\", "/") for path in selected]
    manifest = {
        "format": "shhh-strategy-compact-knowledge",
        "format_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "knowledge_mode": "compact",
        "purpose": "text-first automatic retrieval with external raw evidence on demand",
        "source_archive": {
            "files": sum(1 for _ in source.rglob("*" ) if _.is_file()),
            "bytes": sum(path.stat().st_size for path in source.rglob("*") if path.is_file()),
            "path_is_intentionally_omitted": True,
        },
        "included": {
            "files": len(selected),
            "bytes": sum(path.stat().st_size for path in selected),
            "suffix_counts": dict(sorted(suffixes.items())),
            "sha256": {
                relative: sha256(destination / relative)
                for relative in sorted(relative_files)
            },
        },
        "excluded_by_design": [
            "raw problem and paper PDFs",
            "spreadsheets and CSV data attachments",
            "page-level PNG/JPG images and HTML galleries",
            "full OCR dumps and page_text directories",
            "complete held-out solution/paper text files",
            "SQLite corpus binary index (JSON/Markdown indexes are retained)",
            "executables, caches and temporary rendering artifacts",
        ],
        "external_archive_env": "SHHH_STRATEGY_KNOWLEDGE_ROOT",
        "retrieval_contract": {
            "required_files": [
                "index/corpus_manifest.json",
                "国一论文成品教材/textbook_manifest.json",
                "迭代训练/iteration_manifest.json",
            ],
            "visual_or_exact_formula_check": "set SHHH_STRATEGY_KNOWLEDGE_ROOT to the original archive",
        },
    }
    write_json(destination / "compact_manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="full knowledge archive")
    parser.add_argument("--destination", type=Path, required=True, help="new compact archive")
    args = parser.parse_args()
    manifest = build(args.source, args.destination)
    print(
        json.dumps(
            {
                "destination": str(args.destination.resolve()),
                "files": manifest["included"]["files"],
                "bytes": manifest["included"]["bytes"],
                "mode": manifest["knowledge_mode"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
