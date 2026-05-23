#!/usr/bin/env python3
"""
Cross-check that every citekey in a citation inventory has a corresponding
`<citekey>.md` in the context folder.

Usage:
    python3 check_coverage.py <citation-inventory.json> <context-folder> [--bib references.bib]

Output: JSON on stdout with two lists:
    {
      "covered":   [{"citekey": "...", "occurrences": N, "md_path": "..."}, ...],
      "missing":   [{"citekey": "...", "occurrences": N, "bib_title": "..." | null}, ...]
    }

Exit code: 0 if no missing, 1 if any missing. Useful for shell gating.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


BIB_ENTRY_RE = re.compile(
    r"^@[A-Za-z]+\{\s*([^,\s]+)\s*,",
    re.MULTILINE,
)
BIB_TITLE_RE = re.compile(
    r"title\s*=\s*[{\"]([^{}\"]*(?:\{[^{}]*\}[^{}\"]*)*)[}\"]",
    re.IGNORECASE,
)


def load_bib_titles(bib_path: Path) -> dict[str, str]:
    """Return a {citekey: title} map. Best effort parser; survives nested braces in title."""
    titles: dict[str, str] = {}
    text = bib_path.read_text(encoding="utf-8", errors="replace")
    # Split on @entry boundaries, then for each chunk pull citekey + title.
    chunks = re.split(r"(?=^@[A-Za-z]+\{)", text, flags=re.MULTILINE)
    for chunk in chunks:
        key_match = BIB_ENTRY_RE.match(chunk)
        if not key_match:
            continue
        citekey = key_match.group(1)
        title_match = BIB_TITLE_RE.search(chunk)
        title = title_match.group(1).strip() if title_match else ""
        titles[citekey] = re.sub(r"\s+", " ", title)
    return titles


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inventory", type=Path, help="JSON from extract_citations.py")
    ap.add_argument("context_folder", type=Path, help="Directory of <citekey>.md files")
    ap.add_argument("--bib", type=Path, default=None, help="Optional bibtex file for titles")
    args = ap.parse_args()

    if not args.inventory.exists():
        print(f"inventory not found: {args.inventory}", file=sys.stderr)
        return 2
    if not args.context_folder.is_dir():
        print(f"context folder not a directory: {args.context_folder}", file=sys.stderr)
        return 2

    records = json.loads(args.inventory.read_text(encoding="utf-8"))
    counts = Counter(r["citekey"] for r in records)

    bib_titles = load_bib_titles(args.bib) if args.bib and args.bib.exists() else {}

    md_set = {p.stem for p in args.context_folder.glob("*.md")}

    covered: list[dict] = []
    missing: list[dict] = []
    for citekey, n in sorted(counts.items()):
        if citekey in md_set:
            covered.append({
                "citekey": citekey,
                "occurrences": n,
                "md_path": str(args.context_folder / f"{citekey}.md"),
            })
        else:
            missing.append({
                "citekey": citekey,
                "occurrences": n,
                "bib_title": bib_titles.get(citekey),
            })

    json.dump({"covered": covered, "missing": missing}, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
