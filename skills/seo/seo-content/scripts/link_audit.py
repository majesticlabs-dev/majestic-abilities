#!/usr/bin/env python3
"""Audit markdown links for seo-content drafts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def classify(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return "external"
    if url.startswith("/") or parsed.scheme == "":
        return "internal"
    return "other"


def check_url(url: str, timeout: int = 8) -> tuple[bool, str]:
    try:
        req = Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=timeout) as resp:
            return resp.status < 400, str(resp.status)
    except Exception as exc:
        return False, exc.__class__.__name__


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit markdown internal and external links.")
    parser.add_argument("path", help="Markdown draft path")
    parser.add_argument("--check-external", action="store_true", help="Make network HEAD requests for external links")
    parser.add_argument("--min-internal", type=int, default=2)
    parser.add_argument("--min-external", type=int, default=1)
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print(f"FAIL missing file: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    links = [(anchor.strip(), url.strip()) for anchor, url in LINK_RE.findall(text)]
    internal = [(a, u) for a, u in links if classify(u) == "internal"]
    external = [(a, u) for a, u in links if classify(u) == "external"]
    empty_anchors = [(a, u) for a, u in links if not a or a.lower() in {"click here", "here", "link"}]

    broken = []
    if args.check_external:
        for anchor, url in external:
            ok, detail = check_url(url)
            if not ok:
                broken.append((anchor, url, detail))

    ok = len(internal) >= args.min_internal and len(external) >= args.min_external and not empty_anchors and not broken

    print(f"links_total={len(links)} internal={len(internal)} external={len(external)}")
    print(f"empty_or_weak_anchors={len(empty_anchors)}")
    if args.check_external:
        print(f"broken_external={len(broken)}")
        for anchor, url, detail in broken:
            print(f"BROKEN {detail} {anchor}: {url}")
    print("PASS links" if ok else "FAIL links")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
