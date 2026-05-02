"""Flesch readability diagnostic for prose-tighten skill.

Strips LaTeX commands and never-touch zones (citations, math, code, comments,
captions), then computes Flesch Reading Ease and Flesch-Kincaid Grade Level
using textstat. Outputs JSON.

Usage: python3 flesch.py <path-to-tex>
Exit codes: 0 success, 1 usage/IO error, 2 textstat not installed.
"""

import json
import re
import sys


def strip_latex(text):
    """Strip LaTeX commands and never-touch zones, return plain prose."""
    return text


def compute(latex_path):
    """Read a .tex file, strip it, compute Flesch metrics."""
    pass


def main(argv):
    pass


if __name__ == '__main__':
    sys.exit(main(sys.argv))
