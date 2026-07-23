#!/usr/bin/env python3
"""Run deterministic technical SEO checks on a markdown draft."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def words(text: str) -> list[str]:
    return re.findall(r"\b[\w'’-]+\b", text.lower())


def headings(text: str) -> list[tuple[int, str]]:
    found = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            found.append((len(match.group(1)), match.group(2).strip()))
    return found


def meta_description(text: str) -> str | None:
    for line in text.splitlines():
        match = re.match(r"^meta description:\s*(.+)$", line.strip(), flags=re.I)
        if match:
            return match.group(1).strip()
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit title, meta, headings, and keyword placement.")
    parser.add_argument("path", help="Markdown draft path")
    parser.add_argument("--keyword", required=True, help="Primary keyword or query")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print(f"FAIL missing file: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    hs = headings(text)
    h1s = [title for level, title in hs if level == 1]
    h2s = [title for level, title in hs if level == 2]
    title = h1s[0] if h1s else ""
    meta = meta_description(text) or ""
    keyword = args.keyword.lower()
    first_100 = " ".join(words(text)[:100])

    checks = []
    checks.append(("exactly_one_h1", len(h1s) == 1, str(len(h1s))))
    checks.append(("title_60_chars_or_less", bool(title) and len(title) <= 60, str(len(title))))
    checks.append(("meta_120_to_160_chars", 120 <= len(meta) <= 160, str(len(meta))))
    checks.append(("keyword_in_first_100_words", keyword in first_100, args.keyword))
    checks.append(("has_h2s", len(h2s) >= 2, str(len(h2s))))
    checks.append(("keyword_in_heading", any(keyword in h.lower() for _, h in hs), args.keyword))

    bad_jumps = []
    previous = 0
    for level, title_text in hs:
        if previous and level > previous + 1:
            bad_jumps.append(title_text)
        previous = level
    checks.append(("no_heading_level_jumps", not bad_jumps, str(len(bad_jumps))))

    failed = [name for name, ok, _ in checks if not ok]
    for name, ok, detail in checks:
        print(f"{name}={'PASS' if ok else 'FAIL'} detail={detail}")
    print("PASS technical SEO" if not failed else "FAIL technical SEO")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
