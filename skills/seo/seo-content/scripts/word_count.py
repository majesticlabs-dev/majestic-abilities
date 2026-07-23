#!/usr/bin/env python3
"""Validate markdown word-count basics for seo-content drafts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TARGETS = {
    "guide": (3000, 8000),
    "how-to": (1500, 3500),
    "comparison": (2000, 4500),
    "listicle": (1500, 5000),
    "definition": (700, 1800),
    "data-study": (1500, 5000),
    "resource": (1200, 5000),
    "opinion": (900, 2500),
    "case-study": (900, 2500),
}


def strip_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[#>*_\-|]", " ", text)
    return text


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'’-]+\b", strip_markdown(text)))


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip() and not p.lstrip().startswith("#")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check markdown word count against content type targets.")
    parser.add_argument("path", help="Markdown draft path")
    parser.add_argument("--type", choices=sorted(TARGETS), default="guide", help="Content type")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print(f"FAIL missing file: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    words = count_words(text)
    low, high = TARGETS[args.type]
    para_lengths = [count_words(p) for p in paragraphs(text)]
    long_paragraphs = [n for n in para_lengths if n > 120]

    ok = low <= words <= high and not long_paragraphs
    print(f"word_count={words}")
    print(f"target_type={args.type} target_min={low} target_max={high}")
    print(f"paragraphs={len(para_lengths)} long_paragraphs_over_120_words={len(long_paragraphs)}")
    print("PASS word count" if ok else "FAIL word count")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
