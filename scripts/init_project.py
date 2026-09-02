#!/usr/bin/env python3
"""Create or confirm one shhh-strategy case workspace on the user's Desktop."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


LAYOUT = {
    "sources": "00_sources",
    "audit": "01_audit",
    "strategy": "02_strategy",
    "code": "03_code",
    "results": "04_results",
    "figures": "05_figures",
    "paper": "06_paper",
    "logs": "99_logs",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def desktop_path() -> Path:
    if sys.platform == "win32":
        try:
            import winreg

            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                value, _ = winreg.QueryValueEx(key, "Desktop")
            return Path(os.path.expandvars(value)).expanduser().resolve()
        except (OSError, ImportError):
            pass
    return (Path.home() / "Desktop").resolve()


def safe_slug(case_id: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "-", case_id.strip())
    value = re.sub(r"\s+", " ", value).strip(" .-")
    if not value:
        raise ValueError("case ID does not contain a usable folder name")
    return value[:80].rstrip(" .")


def atomic_write(path: Path, document: dict) -> None:
    content = json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def ensure_project(
    case_id: str,
    project_dir: Path | None = None,
    desktop: Path | None = None,
    source_paths: list[Path] | None = None,
) -> dict:
    case_id = case_id.strip()
    if not case_id:
        raise ValueError("case ID must be non-empty")
    slug = safe_slug(case_id)
    desktop = (desktop or desktop_path()).expanduser().resolve()
    root = (
        project_dir.expanduser().resolve()
        if project_dir is not None
        else desktop / "数学建模项目" / slug
    )
    root.mkdir(parents=True, exist_ok=True)
    for relative in LAYOUT.values():
        (root / relative).mkdir(exist_ok=True)

    manifest_path = root / "project.json"
    normalized_sources = sorted(
        {str(path.expanduser().resolve()) for path in (source_paths or [])}
    )
    now = utc_now()
    status = "created"
    if manifest_path.exists():
        document = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        if document.get("format") != "shhh-strategy-project":
            raise ValueError(f"existing manifest has an unexpected format: {manifest_path}")
        if document.get("case_id") != case_id:
            raise ValueError(
                f"existing project belongs to case {document.get('case_id')!r}, not {case_id!r}"
            )
        document["source_paths"] = sorted(
            set(document.get("source_paths", [])) | set(normalized_sources)
        )
        document["last_confirmed_utc"] = now
        document["root"] = str(root)
        document["directories"] = LAYOUT
        status = "confirmed"
    else:
        document = {
            "format": "shhh-strategy-project",
            "schema_version": "1.0",
            "case_id": case_id,
            "folder_slug": slug,
            "root": str(root),
            "created_utc": now,
            "last_confirmed_utc": now,
            "directories": LAYOUT,
            "source_paths": normalized_sources,
        }
    atomic_write(manifest_path, document)
    return {
        "status": status,
        "case_id": case_id,
        "project_root": str(root),
        "manifest": str(manifest_path),
        "directories": {name: str(root / relative) for name, relative in LAYOUT.items()},
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--project-dir", type=Path)
    parser.add_argument("--desktop", type=Path)
    parser.add_argument("--source", action="append", type=Path, default=[])
    args = parser.parse_args()
    try:
        result = ensure_project(
            args.case_id,
            project_dir=args.project_dir,
            desktop=args.desktop,
            source_paths=args.source,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
