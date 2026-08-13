#!/usr/bin/env python3
"""Verify the distributable Blog—FSE—V3.0.0 skill package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED = (
    "SKILL.md",
    "agents/openai.yaml",
    "assets/finest-sculpture.json",
    "references/content-contract.md",
    "references/computer-use-shopify.md",
    "references/security-and-handoff.md",
    "scripts/build_review_docx.py",
    "scripts/validate_publish_bundle.py",
)

SECRET_PATTERNS = (
    re.compile(r"shpat_[A-Za-z0-9]+"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"][^'\"]+"),
)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")

    profile_path = root / "assets/finest-sculpture.json"
    if profile_path.is_file():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid site profile JSON: {exc}")
        else:
            expected = {
                "schemaVersion": "3.0.0",
                "productionDomain": "finestsculpture.com",
                "shopifyStoreHandle": "c4055d-2",
                "targetBlog": "News",
                "minimumInternalLinks": 2,
                "imageCount": 6,
            }
            for key, value in expected.items():
                if profile.get(key) != value:
                    errors.append(f"profile {key} must be {value!r}")

    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix in {".pyc", ".png", ".jpg", ".jpeg", ".webp", ".docx"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible secret in {path.relative_to(root)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS: Blog—FSE—V3.0.0 package")
    print("Store: c4055d-2 / finestsculpture.com")
    print("Target blog: News")
    print("Secrets: none detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
