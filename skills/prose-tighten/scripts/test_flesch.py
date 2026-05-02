"""Tests for flesch.py — LaTeX stripping and metric computation."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flesch

SCRIPT = os.path.join(HERE, 'flesch.py')


# --- strip_latex: basic ---

def test_strip_plain_text():
    assert flesch.strip_latex("Hello world.") == "Hello world."


def test_strip_section_header():
    text = "\\section{Introduction} The body text follows."
    assert flesch.strip_latex(text) == "The body text follows."


def test_strip_subsection_header():
    text = "\\subsection*{Methods} We did things."
    assert flesch.strip_latex(text) == "We did things."


def test_strip_citation():
    text = "Prior work \\cite{smith2020} showed this."
    assert flesch.strip_latex(text) == "Prior work showed this."


def test_strip_multiple_citation_styles():
    text = "Per \\citet{a} and \\citep{b} and \\autocite{c}, things matter."
    result = flesch.strip_latex(text)
    assert "things matter" in result
    assert "smith2020" not in result
    assert "{" not in result and "}" not in result


def test_emph_keeps_content():
    text = "This is \\emph{important} for our argument."
    assert flesch.strip_latex(text) == "This is important for our argument."


def test_textbf_keeps_content():
    text = "We define \\textbf{microservices} carefully."
    assert flesch.strip_latex(text) == "We define microservices carefully."


def test_strip_unknown_command_with_arg():
    text = "Use \\customcmd{xyz} now."
    assert flesch.strip_latex(text) == "Use now."


def test_collapse_whitespace():
    text = "Lots\n\nof\t  white   space."
    assert flesch.strip_latex(text) == "Lots of white space."
