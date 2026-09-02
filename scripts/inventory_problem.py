#!/usr/bin/env python3
"""Inventory problem files, preserve hashes, and track text/visual inspection coverage."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import mimetypes
import os
import re
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree


VISUAL_SUFFIXES = {".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".svg", ".webp"}
TEXT_SUFFIXES = {".txt", ".md", ".csv", ".tsv", ".json", ".yaml", ".yml"}
DATA_SUFFIXES = {".csv", ".tsv", ".xlsx", ".xls", ".json"}
OFFICE_SUFFIXES = {".docx", ".pptx", ".xlsx"}
ALLOWED_INSPECTION_STATUS = {"pending", "complete", "blocked", "not_applicable"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


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


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("inventory must be a JSON object")
    return value


def decode_text(path: Path) -> tuple[str | None, str | None]:
    raw = path.read_bytes()
    for encoding in ["utf-8-sig", "utf-8", "gb18030", "utf-16"]:
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return None, None


def inspect_delimited(path: Path, delimiter: str) -> dict:
    text, encoding = decode_text(path)
    if text is None:
        return {"parser": "csv", "status": "blocked", "reason": "text decoding failed"}
    rows = 0
    minimum = None
    maximum = 0
    sample_header: list[str] = []
    reader = csv.reader(text.splitlines(), delimiter=delimiter)
    for row in reader:
        if rows == 0:
            sample_header = row[:50]
        width = len(row)
        minimum = width if minimum is None else min(minimum, width)
        maximum = max(maximum, width)
        rows += 1
    return {
        "parser": "csv",
        "status": "indexed",
        "encoding": encoding,
        "rows": rows,
        "min_columns": minimum or 0,
        "max_columns": maximum,
        "header_preview": sample_header,
    }


def inspect_text(path: Path) -> dict:
    text, encoding = decode_text(path)
    if text is None:
        return {"parser": "text", "status": "blocked", "reason": "text decoding failed"}
    return {
        "parser": "text",
        "status": "indexed",
        "encoding": encoding,
        "lines": len(text.splitlines()),
        "characters": len(text),
    }


def xml_count(archive: zipfile.ZipFile, member: str, token: str) -> int | None:
    if member not in archive.namelist():
        return None
    return archive.read(member).count(token.encode("utf-8"))


def inspect_office(path: Path) -> dict:
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            result = {
                "parser": "openxml",
                "status": "indexed",
                "members": len(names),
                "embedded_media": len([name for name in names if "/media/" in name]),
                "charts": len([name for name in names if "/charts/" in name and name.endswith(".xml")]),
                "drawings": len([name for name in names if "/drawings/" in name and name.endswith(".xml")]),
                "external_links": len([name for name in names if "/externalLinks/" in name and name.endswith(".xml")]),
            }
            suffix = path.suffix.lower()
            if suffix == ".docx":
                result.update(
                    {
                        "tables": xml_count(archive, "word/document.xml", "<w:tbl"),
                        "math_elements": xml_count(archive, "word/document.xml", "<m:oMath"),
                        "footnotes_present": "word/footnotes.xml" in names,
                        "endnotes_present": "word/endnotes.xml" in names,
                    }
                )
                if "docProps/app.xml" in names:
                    try:
                        root = ElementTree.fromstring(archive.read("docProps/app.xml"))
                        pages = next((node.text for node in root.iter() if node.tag.endswith("}Pages")), None)
                        result["reported_pages"] = int(pages) if pages else None
                    except (ElementTree.ParseError, ValueError):
                        result["reported_pages"] = None
            elif suffix == ".pptx":
                slides = [name for name in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)]
                result["slides"] = len(slides)
                result["notes_slides"] = len([name for name in names if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", name)])
            elif suffix == ".xlsx":
                result["worksheets"] = len([name for name in names if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", name)])
                result["formula_cells"] = sum(
                    archive.read(name).count(b"<f")
                    for name in names
                    if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", name)
                )
                result["defined_names_present"] = (
                    "xl/workbook.xml" in names and b"<definedNames" in archive.read("xl/workbook.xml")
                )
            return result
    except (zipfile.BadZipFile, OSError) as exc:
        return {"parser": "openxml", "status": "blocked", "reason": str(exc)}


def inspect_pdf(path: Path) -> dict:
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        encrypted = bool(reader.is_encrypted)
        pages = None if encrypted else len(reader.pages)
        return {"parser": "pypdf", "status": "indexed", "pages": pages, "encrypted": encrypted}
    except ImportError:
        raw = path.read_bytes()
        page_markers = len(re.findall(rb"/Type\s*/Page\b", raw))
        return {
            "parser": "pdf-marker-fallback",
            "status": "provisional",
            "pages": page_markers or None,
            "warning": "install pypdf or render the PDF to verify page count",
        }
    except Exception as exc:  # corrupted or unsupported PDF
        return {"parser": "pypdf", "status": "blocked", "reason": str(exc)}


def inspect_image(path: Path) -> dict:
    try:
        from PIL import Image  # type: ignore

        with Image.open(path) as image:
            return {
                "parser": "pillow",
                "status": "indexed",
                "width": image.width,
                "height": image.height,
                "frames": getattr(image, "n_frames", 1),
                "mode": image.mode,
                "format": image.format,
            }
    except ImportError:
        return {"parser": "none", "status": "provisional", "warning": "Pillow unavailable; dimensions not indexed"}
    except Exception as exc:
        return {"parser": "pillow", "status": "blocked", "reason": str(exc)}


def machine_metadata(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return inspect_delimited(path, ",")
    if suffix == ".tsv":
        return inspect_delimited(path, "\t")
    if suffix in TEXT_SUFFIXES:
        return inspect_text(path)
    if suffix in OFFICE_SUFFIXES:
        return inspect_office(path)
    if suffix == ".pdf":
        return inspect_pdf(path)
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp"}:
        return inspect_image(path)
    if suffix == ".zip":
        try:
            with zipfile.ZipFile(path) as archive:
                return {"parser": "zip", "status": "indexed", "members": len(archive.namelist())}
        except zipfile.BadZipFile as exc:
            return {"parser": "zip", "status": "blocked", "reason": str(exc)}
    return {"parser": "hash-only", "status": "indexed"}


def inspection_template(path: Path, metadata: dict) -> dict:
    suffix = path.suffix.lower()
    inspections = {
        "text": {"required": suffix in TEXT_SUFFIXES or suffix in {".pdf", ".docx", ".pptx"}, "status": "pending", "note": ""},
        "visual": {"required": suffix in VISUAL_SUFFIXES, "status": "pending", "note": ""},
        "data": {"required": suffix in DATA_SUFFIXES, "status": "pending", "note": ""},
        "formula": {"required": suffix in {".pdf", ".docx", ".pptx", ".xlsx", ".xls"}, "status": "pending", "note": ""},
        "schema": {"required": suffix in {".csv", ".tsv", ".xlsx", ".xls", ".json"}, "status": "pending", "note": ""},
    }
    if suffix in {".txt", ".md", ".yaml", ".yml"} and metadata.get("status") == "indexed":
        inspections["text"] = {"required": True, "status": "pending", "note": "machine-readable text indexed; explicit semantic review is still required"}
    if suffix in {".csv", ".tsv"} and metadata.get("status") == "indexed":
        inspections["text"] = {"required": True, "status": "complete", "note": "delimited text decoded"}
    for value in inspections.values():
        if not value["required"]:
            value["status"] = "not_applicable"
    return inspections


def file_record(path: Path, root: Path, source_index: int) -> dict:
    relative = path.name if root.is_file() else str(path.relative_to(root)).replace("\\", "/")
    metadata = machine_metadata(path)
    return {
        "id": f"source{source_index}:{relative}",
        "source_index": source_index,
        "relative_path": relative,
        "absolute_path": str(path.resolve()),
        "suffix": path.suffix.lower(),
        "mime": mimetypes.guess_type(path.name)[0],
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "machine_metadata": metadata,
        "inspections": inspection_template(path, metadata),
    }


def refresh_status(document: dict) -> None:
    blocked = []
    pending = []
    for record in document.get("files", []):
        if record.get("machine_metadata", {}).get("status") == "blocked":
            blocked.append(f"{record.get('id')}:machine")
        for name, inspection in record.get("inspections", {}).items():
            if inspection.get("required") and inspection.get("status") == "blocked":
                blocked.append(f"{record.get('id')}:{name}")
            elif inspection.get("required") and inspection.get("status") != "complete":
                pending.append(f"{record.get('id')}:{name}")
    document["coverage"] = {"blocked": blocked, "pending": pending}
    document["overall_status"] = "blocked" if blocked else "pending_review" if pending else "complete"
    document["updated_utc"] = utc_now()


def scan_sources(sources: list[Path]) -> dict:
    roots = [path.resolve() for path in sources]
    missing = [str(path) for path in roots if not path.exists()]
    if missing:
        raise FileNotFoundError("missing source(s): " + "; ".join(missing))
    records = []
    for index, root in enumerate(roots, start=1):
        paths = [root] if root.is_file() else sorted(path for path in root.rglob("*") if path.is_file())
        for path in paths:
            records.append(file_record(path, root, index))
    now = utc_now()
    document = {
        "format": "shhh-problem-source-inventory",
        "schema_version": "1.0",
        "created_utc": now,
        "updated_utc": now,
        "sources": [{"index": index, "path": str(root), "type": "file" if root.is_file() else "directory"} for index, root in enumerate(roots, start=1)],
        "files": records,
        "coverage": {"blocked": [], "pending": []},
        "overall_status": "pending_review",
        "limitations": [
            "Hashes and machine metadata prove inventory integrity, not semantic understanding.",
            "PDF/Office/image content remains incomplete until required visual and formula inspections are marked complete.",
        ],
    }
    refresh_status(document)
    return document


def validate_inventory(document: dict, require_complete: bool) -> list[str]:
    errors: list[str] = []
    if document.get("format") != "shhh-problem-source-inventory":
        errors.append("inventory format mismatch")
    records = document.get("files")
    if not isinstance(records, list) or not records:
        errors.append("inventory has no files")
        return errors
    seen = set()
    for record in records:
        file_id = record.get("id")
        if not file_id or file_id in seen:
            errors.append(f"missing or duplicate file id: {file_id}")
        seen.add(file_id)
        path = Path(record.get("absolute_path", ""))
        if not path.is_file():
            errors.append(f"source file missing: {file_id}")
            continue
        if path.stat().st_size != record.get("bytes"):
            errors.append(f"size changed: {file_id}")
        if sha256_file(path) != record.get("sha256"):
            errors.append(f"hash changed: {file_id}")
        for name, inspection in record.get("inspections", {}).items():
            if inspection.get("status") not in ALLOWED_INSPECTION_STATUS:
                errors.append(f"invalid inspection status: {file_id}:{name}")
    test_document = json.loads(json.dumps(document))
    refresh_status(test_document)
    if test_document.get("overall_status") != document.get("overall_status"):
        errors.append("overall_status is stale; rescan or mark again")
    if require_complete and document.get("overall_status") != "complete":
        errors.append(f"inventory is not complete: {document.get('coverage')}")
    return errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan")
    scan.add_argument("--source", action="append", type=Path, required=True)
    scan.add_argument("--output", type=Path, required=True)

    mark = subparsers.add_parser("mark")
    mark.add_argument("inventory", type=Path)
    mark.add_argument("--file-id", required=True)
    mark.add_argument("--inspection", choices=["text", "visual", "data", "formula", "schema"], required=True)
    mark.add_argument("--status", choices=sorted(ALLOWED_INSPECTION_STATUS), required=True)
    mark.add_argument("--note", required=True)

    validate = subparsers.add_parser("validate")
    validate.add_argument("inventory", type=Path)
    validate.add_argument("--require-complete", action="store_true")

    summary = subparsers.add_parser("summary")
    summary.add_argument("inventory", type=Path)

    args = parser.parse_args()
    if args.command == "scan":
        document = scan_sources(args.source)
        atomic_write(args.output, document)
        print(json.dumps({"status": "PASS", "output": str(args.output.resolve()), "overall_status": document["overall_status"], "files": len(document["files"]), "coverage": document["coverage"]}, ensure_ascii=False, indent=2))
        return 0

    inventory_path = args.inventory.resolve()
    document = load_json(inventory_path)
    if args.command == "mark":
        matches = [record for record in document.get("files", []) if record.get("id") == args.file_id]
        if len(matches) != 1:
            raise ValueError(f"file id must match exactly once: {args.file_id}")
        inspection = matches[0].get("inspections", {}).get(args.inspection)
        if inspection is None:
            raise ValueError(f"inspection does not exist: {args.inspection}")
        if args.status == "not_applicable" and inspection.get("required"):
            raise ValueError("a required inspection cannot be marked not_applicable; explain a source-based exception by rescanning with a supported type")
        inspection["status"] = args.status
        inspection["note"] = args.note
        inspection["reviewed_utc"] = utc_now()
        refresh_status(document)
        atomic_write(inventory_path, document)
        print(json.dumps({"status": "PASS", "overall_status": document["overall_status"], "coverage": document["coverage"]}, ensure_ascii=False, indent=2))
        return 0
    if args.command == "validate":
        errors = validate_inventory(document, args.require_complete)
        print(json.dumps({"status": "PASS" if not errors else "FAIL", "inventory": str(inventory_path), "overall_status": document.get("overall_status"), "errors": errors}, ensure_ascii=False, indent=2))
        return 1 if errors else 0
    print(json.dumps({"inventory": str(inventory_path), "overall_status": document.get("overall_status"), "files": len(document.get("files", [])), "coverage": document.get("coverage", {}), "sources": document.get("sources", [])}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
