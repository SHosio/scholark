#!/usr/bin/env bash
# Convert PDFs to <citekey>.md in a context folder, using `marker_single`.
#
# Usage:
#   convert_pdfs.sh <pdf-dir> <mapping.json> <context-folder>
#
# mapping.json shape (one of):
#   [{"pdf": "wherearewenow.pdf", "citekey": "Riegel2021"}, ...]
#
# Behaviour per pair:
#   1. Run `marker_single` on the PDF (output to a tmp scratch dir).
#   2. Read the generated .md, count images.
#   3. Write `<context-folder>/<citekey>.md` with YAML frontmatter:
#         source_pdf, converted_date, num_images
#   4. Place a bibkey-named copy of the PDF at `<context-folder>/<citekey>.pdf`.
#
# The source PDF is NEVER deleted. Both the markdown and the PDF end up in the
# context folder, both named after the bibtex citekey. The original PDF in the
# source directory is left untouched.
#
# Requires: marker_single (pip install marker-pdf), jq, python3.

set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <pdf-dir> <mapping.json> <context-folder>" >&2
  exit 2
fi

PDF_DIR="$1"
MAPPING="$2"
CONTEXT_DIR="$3"

if ! command -v marker_single >/dev/null 2>&1; then
  echo "marker_single not found on PATH. Install with: pip install marker-pdf" >&2
  exit 3
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "jq not found. Install with your package manager (brew install jq, apt install jq, ...)." >&2
  exit 3
fi
[[ -d "$PDF_DIR" ]] || { echo "PDF dir not found: $PDF_DIR" >&2; exit 2; }
[[ -f "$MAPPING" ]] || { echo "Mapping file not found: $MAPPING" >&2; exit 2; }
mkdir -p "$CONTEXT_DIR"

SCRATCH=$(mktemp -d)
trap 'rm -rf "$SCRATCH"' EXIT

DATE_STR=$(date +%Y-%m-%d)

count=$(jq 'length' "$MAPPING")
for i in $(seq 0 $((count - 1))); do
  PDF_NAME=$(jq -r ".[${i}].pdf" "$MAPPING")
  CITEKEY=$(jq -r ".[${i}].citekey" "$MAPPING")
  PDF_PATH="$PDF_DIR/$PDF_NAME"
  OUT_MD="$CONTEXT_DIR/$CITEKEY.md"

  if [[ ! -f "$PDF_PATH" ]]; then
    echo "[SKIP] PDF not found: $PDF_PATH"
    continue
  fi
  if [[ -f "$OUT_MD" ]]; then
    echo "[SKIP] Already exists: $OUT_MD"
    continue
  fi

  echo "[CONVERT] $PDF_NAME -> $CITEKEY.md"
  marker_single "$PDF_PATH" --output_dir "$SCRATCH" --disable_tqdm 2>&1 | tail -1

  BASENAME="${PDF_NAME%.pdf}"
  GEN_MD="$SCRATCH/$BASENAME/$BASENAME.md"
  if [[ ! -f "$GEN_MD" ]]; then
    echo "[ERROR] marker produced no markdown for $PDF_NAME"
    continue
  fi

  NUM_IMG=$(find "$SCRATCH/$BASENAME" -maxdepth 1 -type f \
            \( -iname '*.jpeg' -o -iname '*.jpg' -o -iname '*.png' \) | wc -l | tr -d ' ')

  {
    echo "---"
    echo "source_pdf: $PDF_NAME"
    echo "converted_date: $DATE_STR"
    echo "num_images: $NUM_IMG"
    echo "---"
    echo ""
    cat "$GEN_MD"
  } > "$OUT_MD"

  # Keep the PDF: place a bibkey-named copy in the context folder alongside the
  # markdown. Never delete the original source PDF.
  OUT_PDF="$CONTEXT_DIR/$CITEKEY.pdf"
  if [[ "$PDF_PATH" -ef "$OUT_PDF" ]]; then
    :  # source already is the bibkey-named PDF in the context folder
  elif [[ -f "$OUT_PDF" ]]; then
    echo "[KEEP] $CITEKEY.pdf already present in context folder"
  else
    cp "$PDF_PATH" "$OUT_PDF"
  fi
  echo "[DONE] $CITEKEY.md + $CITEKEY.pdf ($NUM_IMG images); source PDF preserved"
done
