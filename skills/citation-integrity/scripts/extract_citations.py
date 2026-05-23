#!/usr/bin/env python3
"""
Extract every active inline citation from a LaTeX or Pandoc-Markdown manuscript.

For each citation occurrence, returns the citekey, the file line number,
and the surrounding claim sentence.

Usage:
    python3 extract_citations.py <manuscript.tex>
    python3 extract_citations.py <manuscript.md> --format markdown

Output: JSON list on stdout. One record per (citekey, occurrence) pair.
Multi-citekey commands like \\cite{A, B, C} become three rows.
Commented-out citations in LaTeX (lines whose first non-whitespace char is %) are skipped.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# LaTeX cite commands. Covers \cite, \citep, \citet, \citeauthor, \citeyear,
# \autocite (biblatex), starred forms, and optional [prenote][postnote] arguments.
LATEX_CITE_RE = re.compile(
    r"\\(?:cite[a-zA-Z]*|autocite[a-zA-Z]*)\*?"  # command name
    r"(?:\s*\[[^\]]*\]){0,2}"                    # optional [pre][post]
    r"\s*\{([^}]+)\}"                            # the {citekeys} group
)

# Pandoc-Markdown citation forms: [@key], [@key1; @key2], [-@key], [@key, p. 5]
PANDOC_CITE_RE = re.compile(r"\[(-?@[^\]]+)\]")


def split_into_sentences(text: str) -> list[str]:
    """Cheap sentence splitter. Good enough for picking out the sentence
    containing a citation. Splits on '. ', '! ', '? ' that follow a non-digit."""
    parts = re.split(r"(?<=[^\d])(?<=[.!?])\s+(?=[A-Z\\])", text)
    return [p.strip() for p in parts if p.strip()]


def claim_sentence_around(line_text: str, match_start: int) -> str:
    """Return the sentence containing the citation, given the full line text
    and the character offset where the cite command starts within that line."""
    sentences = split_into_sentences(line_text)
    if len(sentences) == 1:
        return sentences[0]

    # Reconstruct character offsets per sentence to find the one containing match_start.
    offset = 0
    for sent in sentences:
        idx = line_text.find(sent, offset)
        if idx == -1:
            continue
        end = idx + len(sent)
        if idx <= match_start < end + 2:  # +2 for the splitting whitespace
            return sent
        offset = end
    return sentences[-1]  # fallback


def parse_latex(path: Path) -> list[dict]:
    """Walk a LaTeX file. Skip lines whose first non-whitespace char is `%`.
    Multi-line citations are not currently supported (rare in practice)."""
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            stripped = raw.lstrip()
            if stripped.startswith("%"):
                continue

            # Find all cite commands on this line.
            for m in LATEX_CITE_RE.finditer(raw):
                citekey_group = m.group(1)
                claim = claim_sentence_around(raw.rstrip("\n"), m.start())
                for raw_key in citekey_group.split(","):
                    key = raw_key.strip()
                    if not key:
                        continue
                    records.append({
                        "citekey": key,
                        "file": str(path),
                        "line": line_no,
                        "claim_sentence": claim,
                    })
    return records


def parse_pandoc_markdown(path: Path) -> list[dict]:
    """Walk a Pandoc-Markdown file. Citations look like [@key] or [@k1; @k2]."""
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            for m in PANDOC_CITE_RE.finditer(raw):
                inner = m.group(1)  # e.g. "@key1; @key2, p. 5"
                # Extract every @citekey token (strip locator tail after first comma).
                key_tokens = re.findall(r"-?@([A-Za-z0-9_:\-]+)", inner)
                if not key_tokens:
                    continue
                claim = claim_sentence_around(raw.rstrip("\n"), m.start())
                for key in key_tokens:
                    records.append({
                        "citekey": key,
                        "file": str(path),
                        "line": line_no,
                        "claim_sentence": claim,
                    })
    return records


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manuscript", type=Path, help="Path to .tex or .md manuscript")
    ap.add_argument(
        "--format",
        choices=("auto", "latex", "markdown"),
        default="auto",
        help="Manuscript format. Default: auto from extension.",
    )
    args = ap.parse_args()

    if not args.manuscript.exists():
        print(f"manuscript not found: {args.manuscript}", file=sys.stderr)
        return 2

    fmt = args.format
    if fmt == "auto":
        suffix = args.manuscript.suffix.lower()
        fmt = "latex" if suffix in {".tex", ".ltx"} else "markdown"

    records = parse_latex(args.manuscript) if fmt == "latex" else parse_pandoc_markdown(args.manuscript)
    json.dump(records, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
