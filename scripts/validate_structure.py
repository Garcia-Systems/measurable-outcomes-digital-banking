#!/usr/bin/env python3
"""Validate the textbook's chapter, Part, contents, and local-link structure."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_RE = re.compile(r"chapter-(\d{2})-")
CONTENTS_RE = re.compile(r"^\d+\. \[Chapter (\d+):[^]]+\]\(([^)]+)\)$", re.MULTILINE)
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parts = sorted((ROOT / "chapters").glob("part-*"))
    if len(parts) != 8:
        fail(f"expected 8 Parts, found {len(parts)}")

    chapters = sorted((ROOT / "chapters").glob("part-*/chapter-*.md"))
    numbers = []
    for chapter in chapters:
        match = CHAPTER_RE.match(chapter.name)
        if not match:
            fail(f"invalid chapter filename: {chapter.relative_to(ROOT)}")
        numbers.append(int(match.group(1)))
    if numbers != list(range(40)):
        fail(f"chapter numbers must be exactly 0–39 once each; found {numbers}")

    contents = (ROOT / "CONTENTS.md").read_text(encoding="utf-8")
    entries = [(int(number), target) for number, target in CONTENTS_RE.findall(contents)]
    if [number for number, _ in entries] != list(range(40)):
        fail("CONTENTS must list Chapters 0–39 exactly once and in order")
    expected = {path.relative_to(ROOT).as_posix() for path in chapters}
    actual = {target for _, target in entries}
    if actual != expected:
        fail(f"CONTENTS chapter targets differ: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")

    checked = 0
    for source in ROOT.rglob("*.md"):
        if ".git" in source.parts:
            continue
        for target in LINK_RE.findall(source.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            local = target.split("#", 1)[0]
            if local and not (source.parent / local).resolve().exists():
                fail(f"broken link: {source.relative_to(ROOT)} -> {target}")
            checked += 1
    print(f"PASS: 8 Parts, 40 unique Chapters (0–39), 40 CONTENTS entries, {checked} local links")


if __name__ == "__main__":
    main()
