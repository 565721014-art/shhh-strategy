#!/usr/bin/env python3
"""Refresh hashes and byte counts after editing a compact knowledge layer."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="compact knowledge directory")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = root / "compact_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = sorted(
        path for path in root.rglob("*") if path.is_file() and path != manifest_path
    )
    relative = [str(path.relative_to(root)).replace("\\", "/") for path in files]
    manifest.setdefault("included", {})["files"] = len(files)
    manifest["included"]["bytes"] = sum(path.stat().st_size for path in files)
    manifest["included"]["suffix_counts"] = dict(
        sorted(Counter(path.suffix.lower() or "[no extension]" for path in files).items())
    )
    manifest["included"]["sha256"] = {
        name: sha256(root / name) for name in relative
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "root": str(root),
                "files": len(files),
                "bytes": manifest["included"]["bytes"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
