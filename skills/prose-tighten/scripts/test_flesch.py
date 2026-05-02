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


# --- strip_latex: math, environments, comments ---

def test_strip_inline_math_dollar():
    text = "The value $x = 5$ is interesting."
    assert flesch.strip_latex(text) == "The value is interesting."


def test_strip_display_math_dollar():
    text = "Then $$y = mx + b$$ holds."
    assert flesch.strip_latex(text) == "Then holds."


def test_strip_display_math_bracket():
    text = "Then \\[y = mx + b\\] holds."
    assert flesch.strip_latex(text) == "Then holds."


def test_strip_inline_math_paren():
    text = "Note \\(x = 5\\) clearly."
    assert flesch.strip_latex(text) == "Note clearly."


def test_strip_equation_environment():
    text = "Result: \\begin{equation} a^2 + b^2 = c^2 \\end{equation} thus."
    assert flesch.strip_latex(text) == "Result: thus."


def test_strip_align_environment():
    text = "We have \\begin{align} x &= 1 \\\\ y &= 2 \\end{align} as expected."
    assert flesch.strip_latex(text) == "We have as expected."


def test_strip_verbatim_environment():
    text = 'Code:\n\\begin{verbatim}\nprint("hi")\n\\end{verbatim}\nDone.'
    assert flesch.strip_latex(text) == "Code: Done."


def test_strip_lstlisting_environment():
    text = "Code:\n\\begin{lstlisting}\nx = 1\n\\end{lstlisting}\nDone."
    assert flesch.strip_latex(text) == "Code: Done."


def test_strip_minted_environment():
    text = "Code:\n\\begin{minted}{python}\nx = 1\n\\end{minted}\nDone."
    assert flesch.strip_latex(text) == "Code: Done."


def test_strip_verb_inline():
    text = "Run \\verb|grep foo| to search."
    assert flesch.strip_latex(text) == "Run to search."


def test_strip_comments():
    text = "Real text. % this is a comment\nMore text."
    assert flesch.strip_latex(text) == "Real text. More text."


def test_preserve_escaped_percent():
    text = "Growth was 50\\% last year."
    result = flesch.strip_latex(text)
    assert "Growth was 50" in result
    assert "last year" in result


def test_strip_caption():
    text = "See figure. \\caption{A nice plot of results.} The plot shows facts."
    assert flesch.strip_latex(text) == "See figure. The plot shows facts."
