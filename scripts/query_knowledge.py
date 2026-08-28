#!/usr/bin/env python3
"""Retrieve a small structural slice from the local 23-problem/58-paper archive."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1] / "knowledge"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def score_text(text: str, terms: list[str]) -> tuple[int, list[str]]:
    lowered = text.lower()
    matched = []
    score = 0
    for term in terms:
        key = term.lower()
        count = lowered.count(key)
        if count:
            matched.append(term)
            score += 1 + min(count, 4)
    return score, matched


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Search historical cases by mechanism terms without loading all papers."
    )
    parser.add_argument("terms", nargs="+", help="mechanism terms, not a past problem title")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    env_root = os.environ.get("SHHH_STRATEGY_KNOWLEDGE_ROOT")
    root = (args.root or (Path(env_root) if env_root else DEFAULT_ROOT)).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(
            f"optional knowledge root not found: {root}; set SHHH_STRATEGY_KNOWLEDGE_ROOT to a compatible archive"
        )

    corpus = load_json(root / "index" / "corpus_manifest.json")
    textbook = load_json(root / "国一论文成品教材" / "textbook_manifest.json")
    iterations = load_json(root / "迭代训练" / "iteration_manifest.json")

    chapters = {item["source_problem_id"]: item for item in textbook["chapters"]}
    curated_paper_titles = {}
    for chapter_item in textbook["chapters"]:
        for paper_id, paper_title in zip(
            chapter_item.get("paper_ids", []), chapter_item.get("paper_titles", [])
        ):
            curated_paper_titles[str(paper_id)] = paper_title
    iteration_by_id = {item["id"]: item for item in iterations["order"]}
    papers_by_problem: dict[str, list[dict]] = {}
    for paper in corpus.get("papers", []):
        papers_by_problem.setdefault(paper.get("problem", ""), []).append(paper)

    results = []
    for problem in corpus.get("problems", []):
        pid = problem.get("problem", "")
        searchable = " ".join(
            [
                pid,
                problem.get("title", ""),
                problem.get("category", ""),
                problem.get("mother", ""),
                problem.get("chain", ""),
                " ".join(problem.get("risks", [])),
            ]
        )
        score, matched = score_text(searchable, args.terms)
        if not score:
            continue
        chapter = chapters.get(pid, {})
        paper_cards = []
        for paper in papers_by_problem.get(pid, []):
            card = root / paper.get("card_path", "")
            item = {
                "paper_id": paper.get("paper_id"),
                "title": curated_paper_titles.get(
                    str(paper.get("paper_id")), paper.get("title")
                ),
                "card": str(card),
                "card_available": card.is_file(),
            }
            # Gallery pages are intentionally omitted from the compact package.
            # Expose them only when the selected archive actually contains them.
            gallery_value = paper.get("gallery_path")
            if gallery_value:
                gallery = root / gallery_value
                item["gallery_available"] = gallery.is_file()
                if gallery.is_file():
                    item["gallery"] = str(gallery)
            paper_cards.append(item)
        iteration = iteration_by_id.get(pid)
        iteration_record = None
        if iteration:
            prefix = f"{int(iteration['n']):02d}_"
            matches = sorted((root / "迭代训练" / "records").glob(prefix + "*.json"))
            if matches:
                iteration_record = str(matches[0])
        results.append(
            {
                "score": score,
                "matched_terms": matched,
                "problem": pid,
                "title": problem.get("title"),
                "category": problem.get("category"),
                "mother": problem.get("mother"),
                "chain": problem.get("chain"),
                "risks": problem.get("risks", []),
                "problem_card": str(root / "problems" / pid / "problem_card.md"),
                "logic_map": str(root / "problems" / pid / "logic_map.json"),
                "iteration_record": iteration_record,
                "chapter": str(root / "国一论文成品教材" / chapter.get("chapter", "")),
                "paper_cards": paper_cards,
            }
        )

    results.sort(key=lambda item: (-item["score"], item["problem"]))
    print(
        json.dumps(
            {
                "query_terms": args.terms,
                "knowledge_root": str(root),
                "matches": results[: max(args.limit, 1)],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
