# prose-tighten Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `prose-tighten` skill in the Scholark plugin — a `.tex`-only academic prose tightener that splits long sentences, cuts fluff, and asks before touching technical terms. Reports a real Flesch diagnostic via `textstat`; never hallucinates scores.

**Architecture:** Single `SKILL.md` (markdown procedure) plus a small Python helper script (`flesch.py`) for the Flesch diagnostic. Test-driven for the script; manual smoke-tested for the skill prompt. All hard rules ship inside the `SKILL.md` so they are visible on any user's machine that installs the plugin.

**Tech Stack:** Markdown (skill), Python 3 (helper script), `textstat` (optional dependency for Flesch), pytest (for the script tests).

**Spec:** `docs/superpowers/specs/2026-05-02-prose-tighten-design.md` — read it before starting. The plan implements the spec; in case of conflict, the spec wins.

**Hard rules (from the spec — repeat in your head before each task):**
- Never have the LLM compute Flesch in-head. Real tool or no number.
- Never replace technical vocabulary without user confirmation.
- Never optimize for a Flesch target. Diagnostic only.
- All universal rules ship in the `SKILL.md` (and other repo files) — local memory is not a substitute.

---

## File Structure

**Create:**
- `skills/prose-tighten/SKILL.md` — the skill prompt (~250 lines, markdown)
- `skills/prose-tighten/scripts/flesch.py` — Python helper (~110 lines)
- `skills/prose-tighten/scripts/test_flesch.py` — pytest suite (~180 lines)

**Modify:**
- `CLAUDE.md` — bump skill count, add prose-tighten to the list
- `README.md` — add prose-tighten to skill list, update "Writing Style" section to acknowledge it, add to the workflow

**No build, no CI changes.** The plugin remains markdown-first; the only code is the optional helper script.

---

## Phase 1 — Helper script (TDD)

### Task 1: Bootstrap directory and first failing test

**Files:**
- Create: `skills/prose-tighten/scripts/test_flesch.py`
- Create: `skills/prose-tighten/scripts/flesch.py`

- [ ] **Step 1: Create directories**

```bash
mkdir -p skills/prose-tighten/scripts
```

- [ ] **Step 2: Write the first failing test**

Create `skills/prose-tighten/scripts/test_flesch.py`:

```python
"""Tests for flesch.py — LaTeX stripping and metric computation."""

import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flesch


def test_strip_plain_text():
    assert flesch.strip_latex("Hello world.") == "Hello world."
```

- [ ] **Step 3: Create stub `flesch.py`**

Create `skills/prose-tighten/scripts/flesch.py`:

```python
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
```

- [ ] **Step 4: Run pytest to confirm test passes**

Run from the repo root:
```bash
cd skills/prose-tighten/scripts && python3 -m pytest test_flesch.py -v
```

Expected: 1 passed.

- [ ] **Step 5: Commit**

```bash
git add skills/prose-tighten/scripts/flesch.py skills/prose-tighten/scripts/test_flesch.py
git commit -m "feat: scaffold prose-tighten flesch helper with first test"
```

---

### Task 2: LaTeX command stripping (sections, citations, formatting)

**Files:**
- Modify: `skills/prose-tighten/scripts/test_flesch.py`
- Modify: `skills/prose-tighten/scripts/flesch.py`

- [ ] **Step 1: Add failing tests for command stripping**

Append to `test_flesch.py`:

```python
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
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd skills/prose-tighten/scripts && python3 -m pytest test_flesch.py -v
```

Expected: 1 passed (from Task 1), 8 failed (the new ones).

- [ ] **Step 3: Implement command stripping**

Replace the stub `strip_latex` in `flesch.py` with:

```python
def strip_latex(text):
    """Strip LaTeX commands and never-touch zones, return plain prose."""
    # Remove citations and refs entirely
    text = re.sub(
        r'\\(cite|citep|citet|autocite|textcite|parencite|ref|autoref|label|cref|Cref)\*?\{[^}]*\}',
        '', text
    )
    # Keep content of formatting wrappers
    text = re.sub(
        r'\\(emph|textbf|textit|underline|textsc|textsf|texttt)\{([^}]*)\}',
        r'\2', text
    )
    # Remove section headers (we want body prose only)
    text = re.sub(
        r'\\(section|subsection|subsubsection|paragraph|subparagraph|chapter|part)\*?\{[^}]*\}',
        '', text
    )
    # Remove other single-arg commands we haven't handled
    text = re.sub(r'\\\w+\*?\{[^}]*\}', '', text)
    # Remove standalone commands like \\ or \newline
    text = re.sub(r'\\\w+\*?', '', text)
    # Remove leftover braces
    text = re.sub(r'[{}]', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

- [ ] **Step 4: Run tests to confirm all pass**

```bash
cd skills/prose-tighten/scripts && python3 -m pytest test_flesch.py -v
```

Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add skills/prose-tighten/scripts/flesch.py skills/prose-tighten/scripts/test_flesch.py
git commit -m "feat: strip LaTeX commands, citations, and formatting wrappers"
```

---

### Task 3: Math, code environments, and comment stripping

**Files:**
- Modify: `skills/prose-tighten/scripts/test_flesch.py`
- Modify: `skills/prose-tighten/scripts/flesch.py`

- [ ] **Step 1: Add failing tests for math, environments, and comments**

Append to `test_flesch.py`:

```python
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
```

- [ ] **Step 2: Run tests to confirm new ones fail**

```bash
cd skills/prose-tighten/scripts && python3 -m pytest test_flesch.py -v
```

Expected: 9 passed (prior), several failed (the new ones — exact count depends on coincidence).

- [ ] **Step 3: Update `strip_latex` to handle math, environments, comments**

Replace `strip_latex` in `flesch.py` with the full version:

```python
def strip_latex(text):
    """Strip LaTeX commands and never-touch zones, return plain prose."""
    # Remove line comments (% to end of line) but not escaped \%
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)
    # Remove display math
    text = re.sub(r'\$\$[\s\S]*?\$\$', '', text)
    text = re.sub(r'\\\[[\s\S]*?\\\]', '', text)
    # Remove inline math
    text = re.sub(r'\$[^$\n]*\$', '', text)
    text = re.sub(r'\\\([\s\S]*?\\\)', '', text)
    # Remove math/code/verbatim environments
    for env in ('equation', 'align', 'eqnarray', 'gather',
                'verbatim', 'lstlisting', 'minted'):
        text = re.sub(
            rf'\\begin\{{{env}\*?\}}[\s\S]*?\\end\{{{env}\*?\}}',
            '', text
        )
    # Remove \verb||
    text = re.sub(r'\\verb\|[^|]*\|', '', text)
    # Remove \caption{...} contents
    text = re.sub(r'\\caption\*?\{[^}]*\}', '', text)
    # Remove citations and refs entirely
    text = re.sub(
        r'\\(cite|citep|citet|autocite|textcite|parencite|ref|autoref|label|cref|Cref)\*?\{[^}]*\}',
        '', text
    )
    # Keep content of formatting wrappers
    text = re.sub(
        r'\\(emph|textbf|textit|underline|textsc|textsf|texttt)\{([^}]*)\}',
        r'\2', text
    )
    # Remove section headers (we want body prose)
    text = re.sub(
        r'\\(section|subsection|subsubsection|paragraph|subparagraph|chapter|part)\*?\{[^}]*\}',
        '', text
    )
    # Remove other \cmd{arg}
    text = re.sub(r'\\\w+\*?\{[^}]*\}', '', text)
    # Replace escaped percent with literal
    text = text.replace(r'\%', '%')
    # Remove standalone commands
    text = re.sub(r'\\\w+\*?', '', text)
    # Remove leftover braces
    text = re.sub(r'[{}]', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

- [ ] **Step 4: Run tests to confirm all pass**

```bash
cd skills/prose-tighten/scripts && python3 -m pytest test_flesch.py -v
```

Expected: all tests passed (count is the cumulative total — should be 22).

- [ ] **Step 5: Commit**

```bash
git add skills/prose-tighten/scripts/flesch.py skills/prose-tighten/scripts/test_flesch.py
git commit -m "feat: strip math, code environments, and comments"
```

---

### Task 4: `compute()` function with textstat

**Files:**
- Modify: `skills/prose-tighten/scripts/test_flesch.py`
- Modify: `skills/prose-tighten/scripts/flesch.py`

**Prerequisite:** Install textstat in the environment running tests:
```bash
python3 -m pip install textstat pytest
```

If pip refuses (PEP 668), use a venv:
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install textstat pytest
```

- [ ] **Step 1: Add failing tests for `compute()`**

Append to `test_flesch.py`:

```python
import tempfile


def test_compute_basic_prose():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
        f.write("This is a simple sentence. It has two parts. Three sentences total.")
        path = f.name
    try:
        result = flesch.compute(path)
        assert 'fre' in result
        assert 'fkgl' in result
        assert 'words' in result
        assert 'sentences' in result
        assert isinstance(result['fre'], (int, float))
        assert isinstance(result['fkgl'], (int, float))
        assert result['words'] > 0
        assert result['sentences'] >= 1
    finally:
        os.unlink(path)


def test_compute_strips_latex_before_scoring():
    """Flesch numbers should reflect prose only, not LaTeX commands."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
        f.write("\\section{Intro} The cat sat on the mat. It was a fine cat.")
        path = f.name
    try:
        result = flesch.compute(path)
        # 'Intro', 'section', 'cite' should not be counted as words
        assert result['words'] == 11  # "The cat sat on the mat. It was a fine cat."
        assert result['sentences'] == 2
    finally:
        os.unlink(path)


def test_compute_empty_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
        f.write("")
        path = f.name
    try:
        result = flesch.compute(path)
        assert result['words'] == 0
        assert result.get('fre') is None
        assert 'error' in result
    finally:
        os.unlink(path)


def test_compute_only_latex_no_prose():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
        f.write("\\documentclass{article}\n\\begin{document}\n\\end{document}")
        path = f.name
    try:
        result = flesch.compute(path)
        assert result['words'] == 0
        assert 'error' in result
    finally:
        os.unlink(path)
```

- [ ] **Step 2: Run tests to confirm failures**

```bash
cd skills/prose-tighten/scripts && python3 -m pytest test_flesch.py -v
```

Expected: prior tests pass; new tests fail with `AttributeError: module 'flesch' has no attribute 'compute'`.

- [ ] **Step 3: Implement `compute()`**

Append to `flesch.py` (after `strip_latex`):

```python
def compute(latex_path):
    """Read a .tex file, strip it, compute Flesch metrics."""
    with open(latex_path, 'r', encoding='utf-8') as f:
        latex = f.read()
    plain = strip_latex(latex)
    if not plain:
        return {
            'fre': None,
            'fkgl': None,
            'words': 0,
            'sentences': 0,
            'error': 'No prose found after LaTeX stripping',
        }
    import textstat
    return {
        'fre': round(textstat.flesch_reading_ease(plain), 2),
        'fkgl': round(textstat.flesch_kincaid_grade(plain), 2),
        'words': textstat.lexicon_count(plain),
        'sentences': textstat.sentence_count(plain),
    }
```

- [ ] **Step 4: Run tests**

```bash
cd skills/prose-tighten/scripts && python3 -m pytest test_flesch.py -v
```

Expected: all tests pass (cumulative ~26).

- [ ] **Step 5: Commit**

```bash
git add skills/prose-tighten/scripts/flesch.py skills/prose-tighten/scripts/test_flesch.py
git commit -m "feat: compute Flesch metrics via textstat"
```

---

### Task 5: CLI entry point with JSON output

**Files:**
- Modify: `skills/prose-tighten/scripts/test_flesch.py`
- Modify: `skills/prose-tighten/scripts/flesch.py`

- [ ] **Step 1: Add failing CLI tests**

Append to `test_flesch.py`:

```python
import json
import subprocess

SCRIPT = os.path.join(HERE, 'flesch.py')


def test_cli_no_args():
    proc = subprocess.run(
        [sys.executable, SCRIPT],
        capture_output=True, text=True
    )
    assert proc.returncode == 1
    out = json.loads(proc.stdout)
    assert 'error' in out
    assert 'usage' in out['error'].lower()


def test_cli_missing_file():
    proc = subprocess.run(
        [sys.executable, SCRIPT, '/nonexistent/path-that-does-not-exist.tex'],
        capture_output=True, text=True
    )
    assert proc.returncode == 1
    out = json.loads(proc.stdout)
    assert 'error' in out
    assert 'not found' in out['error'].lower()


def test_cli_valid_file_returns_json():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
        f.write("Quick brown fox jumps. Lazy dog runs fast.")
        path = f.name
    try:
        proc = subprocess.run(
            [sys.executable, SCRIPT, path],
            capture_output=True, text=True
        )
        assert proc.returncode == 0, f"stderr: {proc.stderr}, stdout: {proc.stdout}"
        out = json.loads(proc.stdout)
        assert 'fre' in out
        assert isinstance(out['fre'], (int, float))
        assert out['words'] > 0
    finally:
        os.unlink(path)
```

- [ ] **Step 2: Run tests to confirm failure**

```bash
cd skills/prose-tighten/scripts && python3 -m pytest test_flesch.py -v
```

Expected: previous tests pass; CLI tests fail (no main entry, prints nothing on direct invocation).

- [ ] **Step 3: Add `main()` and `__main__` guard**

Append to `flesch.py`:

```python
def main(argv):
    if len(argv) != 2:
        print(json.dumps({'error': 'usage: flesch.py <path-to-tex>'}))
        return 1
    try:
        result = compute(argv[1])
    except FileNotFoundError:
        print(json.dumps({'error': f'file not found: {argv[1]}'}))
        return 1
    except ImportError:
        print(json.dumps({'error': 'textstat not installed'}))
        return 2
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
```

- [ ] **Step 4: Run tests**

```bash
cd skills/prose-tighten/scripts && python3 -m pytest test_flesch.py -v
```

Expected: all tests pass (cumulative ~29).

- [ ] **Step 5: Sanity-check the CLI by hand**

```bash
echo "The quick brown fox jumps. The lazy dog rests." > /tmp/sample.tex
python3 skills/prose-tighten/scripts/flesch.py /tmp/sample.tex
rm /tmp/sample.tex
```

Expected: a JSON line printed, with `fre`, `fkgl`, `words`, `sentences` keys, all populated with real numbers.

- [ ] **Step 6: Commit**

```bash
git add skills/prose-tighten/scripts/flesch.py skills/prose-tighten/scripts/test_flesch.py
git commit -m "feat: add CLI entry point with JSON output"
```

---

## Phase 2 — Skill markdown

### Task 6: Create `SKILL.md` — frontmatter, identity, procedure

**Files:**
- Create: `skills/prose-tighten/SKILL.md`

- [ ] **Step 1: Write the SKILL.md file**

Create `skills/prose-tighten/SKILL.md` with the following content:

````markdown
---
name: prose-tighten
description: Tighten academic prose without losing field-specific terminology. Splits long sentences, cuts fluff, fixes nominalizations. Asks before touching technical terms. .tex only. Use when the user says "tighten this", "tighten the intro", "shorten this section", "make this clearer", "check writing complexity in X", "prose pass on the methods", "this paragraph is too dense", or "fix the prose in section 3".
---

# prose-tighten

Tighten academic prose in a `.tex` file without sacrificing field-specific terminology. Splits long sentences, removes fluff phrases, fixes nominalizations, and replaces wordy connectives with simpler ones. Asks the user before touching anything that might be load-bearing technical vocabulary. `.tex` only — for other formats, point at the source `.tex` file.

> **Pairs naturally with `paper-review`.** Run `prose-tighten` first to clean up sentence-level prose, then `paper-review` for structural and argumentative review on the cleaner text.

## Hard rules — non-negotiable

These rules apply on every invocation. They are not heuristics; they are constraints.

1. **Never hallucinate numerical scores.** Flesch numbers come from `flesch.py` (which calls `textstat`) or they are omitted with a note. Never approximate, never estimate, never reason about syllables in your head. If the tool isn't there, the diagnostic is skipped — that is fine.
2. **Never optimize for Flesch.** Flesch is reported as a diagnostic, before and after, with an explicit "diagnostic only — not a target" disclaimer. Do not chase a higher score. Do not "improve" the number by replacing precise terms with vaguer ones.
3. **Never replace technical vocabulary without user confirmation.** When uncertain whether a term is load-bearing, ask. Field-specific terms (e.g., "microservices", "anomalies", "reflexive thematic analysis") look like dense vocabulary to general-readability metrics, but they are precise and reviewers expect them. The skill's job is to remove *fluff*, not technical density.
4. **Never touch citations, math, code, comments, captions, or quoted speech.** See "Never-touch zones" below.

## Step 1: Find the working paper

Auto-discover the `.tex` file in the project. Look for a file containing both `\documentclass{}` and `\begin{document}` in the project root or its immediate subdirectories. In a single-paper project (the common case) this is unambiguous.

If the project has multiple candidate entry-point `.tex` files, list them and ask the user to pick.

If no `.tex` file is found, ask: "I can't find a `.tex` paper in this project. Which file should I tighten?"

The user's request is *what* to tighten ("the intro", "the methods", "the whole paper"); the file is your problem to solve, not theirs.

## Step 2: Identify the section(s) to process

Map the user's free-text reference to LaTeX structure:

- "the intro" / "introduction" → `\section{Introduction}` or fuzzy match
- "section 3" → 3rd `\section{}` block by document order
- "methods and results" → multiple sections, processed in order
- "the abstract" → `\begin{abstract}...\end{abstract}`
- "the whole paper" or no reference → whole-paper mode (Step 4 onward)

If the section reference is ambiguous (e.g., "the part about RCA"), list the document's section structure and ask the user to pick.

## Step 3: Resolve multi-file projects

If the entry-point file contains `\input{}`, `\include{}`, or `\subfile{}`, follow them recursively to build a virtual flat view of the document. Track line origins so each piece of prose maps back to its source file.

The targeted section's prose may live in a file other than the entry point (e.g., `\section{Related Work}` is in `main.tex` but its body is `\input{rw}` → the prose is in `rw.tex`).

**Resolution rules:**
- `\input{rw}` resolves to `rw.tex` (default `.tex` extension).
- Relative paths resolve relative to the file doing the include.
- `\subfile{}` (subfiles package) is followed the same way.
- Skip includes inside `\iffalse...\fi` or commented-out lines.
- Missing include file → warn ("rw.tex referenced but not found"), continue with the rest.
- Circular include → bail with a clear error before any edit.
- Path outside project root → refuse to edit; ask the user to invoke directly on that file.

## Step 4: Volume check (whole-paper mode only)

If the user invoked whole-paper mode, scan all sections first to count tightening candidates. If the total exceeds 150, warn:

> "Found N candidates across M sections. Whole-paper passes that big are hard to review in one diff. Suggest running section-by-section. Proceed with whole-paper anyway? [y/n]"

Below the threshold, no warning. The 150 number is a starting calibration — the user will tune in practice.

## Step 5: Multi-file safety check

If the pass will edit any file other than the auto-discovered entry-point file, ask once before any edits:

> "This pass will edit: rw.tex (included from main.tex). Proceed? [y/n]"

This applies to every mode — section-targeted or whole-paper. Single-file passes skip this question.

## Step 6: Scan for tightening candidates

Read the in-scope prose, masking the never-touch zones (see below). Identify candidates in these categories:

**Sentence-level (definitely in scope):**
- **Long sentences** — over 30 words, or with more than two independent clauses joined by conjunctions. Heuristic, not a hard rule; use judgment when the sentence's structure is essential.
- **Fluff phrases** — phrases that add length without meaning. Canonical examples (extend in practice):
  - "plays a central role in", "plays a significant role in"
  - "as a result", "as a consequence"
  - "in practice", "in reality", "in essence"
  - "it is important to note that", "it should be noted that"
  - "due to the fact that" → "because"
  - "in order to" → "to"
  - "the fact that" → often deletable
  - "a number of" → "several" / "many"
  - "for the most part", "by and large"
- **Wordy connectives** — replace with shorter forms when meaning is preserved.

**Verb/noun-level (judgment calls):**
- **Nominalizations** — turn nouns derived from verbs back into verbs. "the analysis of X" → "analyzing X". "performance of RCA" → "performing RCA". "the determination of Y" → "determining Y".
- **Passive → active** — flip when the active voice reads better and the agent is known. Do not flip when the patient is the topic of the sentence (legitimate use of passive).
- **Hedging stacks** — "may potentially possibly" → pick one.
- **Redundant qualifiers** — "very unique", "completely eliminated", "absolutely essential".

**Out of scope (do not touch):**
- Replacing technical vocabulary with lay terms (see Hard Rule 3).
- Restructuring arguments, sections, or contributions (`paper-review` does this).
- Citation reformatting.
- Paragraph-level cohesion rewrites (out of v1).

## Step 7: Triage terminology candidates

For each word the model considers replacing, classify uncertainty:

- **High uncertainty** — no obvious lay synonym OR no nearby gloss/definition in the surrounding prose. Examples: niche method names, domain-specific compound terms, acronyms without expansion. → Batch into one upfront question to the user before any edits:
  > "Are these load-bearing technical terms? Answer y/n for each:
  >   - microservices
  >   - anomalies
  >   - reflexive thematic analysis"
- **Medium uncertainty** — plausible lay synonym exists, term looks tightenable. → Make best guess, edit, flag in the post-edit report.

If the user answers "no, load-bearing" to every term, proceed with non-terminology edits only and note in the summary: "All terminology preserved per your input."

## Step 8: Apply edits in place

Edit the `.tex` file(s) directly. Edits respect never-touch zones — sentences containing citations or math have prose tightened around them while the protected tokens pass through unchanged.

For whole-paper mode: edit Section 1 → Section 2 → ... in order, no chat updates between sections.

If you hit something unparseable mid-paper (a section block that can't be tokenized cleanly), stop at that section. Report what was completed and where you halted. Do NOT silently finish with a partial mess.

## Step 9: Compute Flesch (diagnostic only)

Compute Flesch Reading Ease and Flesch-Kincaid Grade Level **before and after** the edits using the helper script. The script lives in this skill's own folder under `scripts/flesch.py`. Claude Code provides this skill's base directory when the skill is loaded — use it to construct the path:

```bash
python3 <SKILL_BASE_DIR>/scripts/flesch.py <path-to-tex>
```

For example, if the skill loaded from `/Users/jane/.claude/plugins/scholark/skills/prose-tighten/`, run:
```bash
python3 /Users/jane/.claude/plugins/scholark/skills/prose-tighten/scripts/flesch.py /Users/jane/papers/draft/main.tex
```

The script returns JSON: `{"fre": <float>, "fkgl": <float>, "words": <int>, "sentences": <int>}`.

**First-run dependency check.** Before computing, verify `textstat` is importable:

```bash
python3 -c "import textstat" 2>&1
```

If the import fails, ask the user:
> "prose-tighten uses the `textstat` Python package for the Flesch diagnostic. It's not installed. Install it now via `python3 -m pip install textstat`? [y / skip]"

- **y** → run `python3 -m pip install textstat`. On success, continue. On failure (PEP 668, no network), surface the error and suggest alternatives (`pipx install textstat`, `uv pip install textstat`, virtualenv) — then ask again whether to skip the diagnostic for this run.
- **skip** → omit the diagnostic, note "Flesch diagnostic skipped — `textstat` not available" in the summary, continue with everything else.

If `python3` is not on the path → omit the diagnostic with the same kind of note.

**Repeat from Hard Rule 1: never produce Flesch numbers by in-head reasoning. If the tool fails, the diagnostic is omitted. There is no fallback.**

## Step 10: Emit the output bundle

Five things, every run:

### A. In-place edits to the `.tex` file(s)
The diff is the primary review surface — user reviews via Overleaf, their editor, or `git diff`.

### B. Brief in-chat summary
Scannable response in the Claude Code conversation. Format:

```
prose-tighten complete

Sections: Introduction (lines 12–87), Related Work (lines 89–203)
Edits: 5 sentences split, 8 fluff phrases removed, 3 nominalizations fixed,
       2 wordy connectives, 1 passive→active, 4 terminology terms touched

Flesch (diagnostic only — not a target):
  Reading Ease:    32.1 → 38.4
  Grade Level:     14.9 → 13.7

Full report: .scholark/reports/prose-tighten/<paper-stem>-<timestamp>.md

Please review the diff and confirm no critical terminology or meaning was lost.
If anything is wrong: `git checkout -- <file>` to revert all, or revert
specific hunks in your editor.
```

If the diagnostic was skipped, omit the Flesch block and note the reason where the numbers would be.

### C. Sidecar markdown report
Write to `.scholark/reports/prose-tighten/<paper-stem>-<YYYY-MM-DD-HHMM>.md` in the project root. Sections:

- **Section A — Change log:** every edit, organized by category (sentence splits, fluff removals, nominalizations, etc.), with line numbers and before/after snippets.
- **Section B — Terminology touched:** every term modified (whether user-confirmed or auto-decided), with original term, replacement, rationale, and confidence level. The audit trail for "did I lose anything load-bearing?"
- **Section C — Uncertain calls:** non-terminology edits the skill wasn't fully confident about (ambiguous antecedents, splits that might shift emphasis), each with a "verify this" line.
- **Section D — Skipped candidates:** things the skill noticed but chose not to touch (terminology user said is load-bearing, long sentences whose structure was deemed essential).

The timestamp in the filename means multiple passes accumulate (audit trail) rather than overwrite.

**`.scholark/` setup.** On first write to `.scholark/`, check if `.scholark/` is in the project's `.gitignore`. If not (and a `.gitignore` exists), append it and tell the user. If no `.gitignore` exists, just create the directory — do not generate a `.gitignore`.

### D. Verify-nothing-lost prompt
Always the last line of the in-chat summary, no exceptions:
> "Please review the diff and confirm no critical terminology or meaning was lost. If anything is wrong: `git checkout -- <file>` to revert all, or revert specific hunks in your editor."

### E. Git status reminder
If the `.tex` file was tracked but uncommitted before the run, note it in the summary and suggest staging the prior state first (clean revert point). If already clean, no reminder.

## Never-touch zones

These are masked from edit candidates. The skill must never touch them:

- **Citations:** `\cite{}`, `\citep{}`, `\citet{}`, `\autocite{}`, `\textcite{}`, `\parencite{}`, `\ref{}`, `\autoref{}`, `\label{}`, `\cref{}`, `\Cref{}`
- **Math:** `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, and `equation` / `align` / `eqnarray` / `gather` environments
- **Code/verbatim:** `verbatim`, `lstlisting`, `minted` environments, `\verb||`
- **Quoted speech:** `` ``...'' ``
- **Figure/table captions:** `\caption{}` contents — left alone in v1
- **Comment lines:** anything after an unescaped `%`
- **User-defined custom commands:** leave `\customcmd{...}` whole — do not peek inside
- **Includes inside `\iffalse...\fi`** or commented-out `\input{}` lines

**In-scope:** plain prose between paragraphs and inside formatting wrappers like `\emph{}`, `\textbf{}`, `\textit{}` (display, not semantics — words inside are fair game).

## Edge cases

- **Wrong file type.** User points at `.md`, `.txt`, `.pdf`. Respond: "prose-tighten is `.tex` only — for other formats, point me at the source `.tex` file." No partial work.
- **No working paper found.** Project has no `.tex` file with `\documentclass{}`. Ask: "I can't find a `.tex` paper in this project. Which file should I tighten?"
- **Multiple candidate papers.** List the candidates and ask the user to pick.
- **LaTeX parse failures.** Unbalanced braces, unclosed environments, malformed includes. Report the failure with file + line, make NO edits, suggest the user fix the syntax and retry.
- **No candidates found.** Report "nothing to tighten — prose is already tight" plus Flesch numbers as confirmation. Encouraging, not a failure.
- **User cancels mid-run.** Between terminology batch and edits → no edits made, exit cleanly. Mid-edit → last completed edit on disk; user reverts via git or per-hunk in editor. Skill does not attempt self-rollback.
- **Not a git repo.** Skill still works. Drop git-specific parts of the verify prompt and gitignore handling. Tell the user: "this directory isn't a git repo — review the diff in your editor; no automatic revert is available."
- **Skill invoked twice on the same file.** Each run produces a new timestamped report. v1 does not remember terminology decisions across runs — every invocation starts fresh.
- **Empty section** (header exists but body is just `\input{...}`). Recognize the forwarding header, follow the include, process the actual content there.

## Workflow integration

Recommended pairing:
1. Run `prose-tighten` → tighter prose, terminology preserved.
2. Review the diff, accept or revert.
3. Run `paper-review` on the tightened draft → structural review on cleaner prose.
````

- [ ] **Step 2: Verify it parses correctly**

```bash
head -1 skills/prose-tighten/SKILL.md
```

Expected: the line is `---`.

```bash
grep -c "^##" skills/prose-tighten/SKILL.md
```

Expected: at least 12 (for the various ## section headings).

- [ ] **Step 3: Commit**

```bash
git add skills/prose-tighten/SKILL.md
git commit -m "feat: add prose-tighten SKILL.md"
```

---

## Phase 3 — Repo integration

### Task 7: Update CLAUDE.md and README.md

**Files:**
- Modify: `CLAUDE.md`
- Modify: `README.md`

- [ ] **Step 1: Read the current CLAUDE.md skill section**

```bash
grep -n "skills" CLAUDE.md
```

Find the "Five Skills" header and the list under it.

- [ ] **Step 2: Update CLAUDE.md**

Replace the line `### Five Skills (sequential workflow)` with:
```markdown
### Six Skills
```

Add a 6th item to the numbered list (after `literature-blind-spots`):
```markdown
6. **prose-tighten** — Tighten `.tex` prose (split long sentences, cut fluff, fix nominalizations) without losing field-specific terminology. Reports a real Flesch diagnostic via the `textstat` package; never hallucinates scores.
```

- [ ] **Step 3: Update README.md skill list**

In the `### Skills` section (around line 13), add:
```markdown
- `/scholark:prose-tighten` — Tighten `.tex` prose without losing field-specific terminology. Splits long sentences, cuts fluff, fixes nominalizations. Asks before touching technical terms.
```

- [ ] **Step 4: Update README.md "Writing Style" section**

The current section starts with: `Scholark doesn't have a writing style skill — it doesn't need one.` That sentence is now misleading. Replace the section with:

```markdown
## Writing Style

To set the register (formal vs. conversational, hedge level, audience), add a line to your project's `CLAUDE.md`:

```
Academic paper targeting CHI 2026. Formal but not stiff. Hedge claims appropriately.
```

If you ask Claude to read your draft, it will naturally calibrate to your voice. The `CLAUDE.md` line ensures the right register even in sessions where your paper isn't loaded.

For mechanical prose tightening — splitting long sentences, cutting fluff, fixing nominalizations — use the `prose-tighten` skill. It is *.tex* only and leaves field-specific terminology alone (asks you when uncertain).

Want more control? Edit `CLAUDE.md` with as much or as little style guidance as you like — or add another writing skill to the plugin. That's the beauty of Claude Code: everything is a markdown file you own.
```

- [ ] **Step 5: Update README.md Workflow section**

Add prose-tighten to the workflow. Find the `## Workflow` section and update the numbered list. Replace:

```markdown
1. **Brainstorm** — Start with an idea, get divergent perspectives, narrow to 2-3 options
2. **Design** — Formalize the chosen option into a complete study design
3. **Analysis** — Pre-specify the analysis plan for each dependent variable
4. **Validate** — Run a completeness check before piloting
5. **You** — Read the output. Apply judgment. ...
```

with:

```markdown
1. **Brainstorm** — Start with an idea, get divergent perspectives, narrow to 2-3 options
2. **Design** — Formalize the chosen option into a complete study design
3. **Analysis** — Pre-specify the analysis plan for each dependent variable
4. **Validate** — Run a completeness check before piloting
5. **Tighten** — When you have a draft, run `prose-tighten` on it before submission to clean up sentence-level prose without touching your terminology
6. **Review** — Run `paper-review` on the tightened draft to catch structural issues reviewers will flag
7. **You** — Read the output. Apply judgment. ...
```

- [ ] **Step 6: Verify the changes look right**

```bash
git diff CLAUDE.md README.md
```

Expected: clean, minimal diffs that only change the skill list, the workflow, and the writing-style section.

- [ ] **Step 7: Commit**

```bash
git add CLAUDE.md README.md
git commit -m "docs: register prose-tighten in CLAUDE.md, README, and workflow"
```

---

### Task 8: Smoke test on a sample `.tex`

**Files:**
- (Temporary, not committed) a sample `.tex` file in `/tmp/`

This task verifies the helper script works end-to-end on a realistic input. The skill itself (the markdown procedure) cannot be unit-tested — it runs inside Claude. Manual smoke is the v1 validation.

- [ ] **Step 1: Create a realistic sample**

```bash
cat > /tmp/prose-tighten-smoke.tex <<'EOF'
\documentclass{article}
\begin{document}
\section{Introduction}
Root cause analysis (RCA) plays a central role in microservice operations by enabling engineers to identify the underlying causes of anomalies and apply targeted actions to prevent future recurrence \cite{smith2020}. Without a clear understanding of why failures occur, similar anomalies are likely to reappear, repeatedly impacting both technical systems and the business processes built on top of them \cite{jones2021}. As a result, timely and effective RCA is essential not only for short-term incident recovery but also for long-term system reliability and continuous operational improvement.

\section{Methods}
We analyzed $N = 42$ traces using the algorithm \cite{algorithm}.
\begin{equation}
  E = mc^2
\end{equation}
The performance of analysis was measured by accuracy.

\section{Results}
% This is a comment that should be stripped
The system worked. We observed positive outcomes.
\end{document}
EOF
```

- [ ] **Step 2: Run the helper script directly**

```bash
python3 skills/prose-tighten/scripts/flesch.py /tmp/prose-tighten-smoke.tex
```

Expected output: a JSON object with all four fields populated, e.g.:
```json
{"fre": 28.5, "fkgl": 15.2, "words": 73, "sentences": 5}
```

The exact numbers will vary, but verify:
- `words` is reasonable (~70 — the sample has roughly that many prose words after stripping)
- `sentences` is plausible (4–6)
- `fre` and `fkgl` are real numbers (not None, not strings)
- No LaTeX commands like `cite` or `equation` show up as words (you can sanity-check by mentally counting prose words in the sample)

- [ ] **Step 3: Run with textstat removed to verify error path**

```bash
python3 -c "import textstat" && python3 -m pip uninstall -y textstat
python3 skills/prose-tighten/scripts/flesch.py /tmp/prose-tighten-smoke.tex; echo "exit: $?"
python3 -m pip install textstat
```

Expected: the middle command prints a JSON `{"error": "textstat not installed"}` and the exit code is `2`.

(If you're in a venv or shared environment, skip this step — uninstalling textstat may be disruptive. Instead, simulate the error by temporarily renaming the installed `textstat` directory in `site-packages` and running the script.)

- [ ] **Step 4: Run with a missing file to verify error path**

```bash
python3 skills/prose-tighten/scripts/flesch.py /tmp/does-not-exist.tex; echo "exit: $?"
```

Expected: JSON with `"error": "file not found: ..."` and exit code `1`.

- [ ] **Step 5: Clean up the sample**

```bash
rm /tmp/prose-tighten-smoke.tex
```

- [ ] **Step 6: No commit needed for this task** — smoke test is verification only.

---

### Task 9: Run the full test suite once more, then declare ship-ready

**Files:** none modified.

- [ ] **Step 1: Run all tests**

```bash
cd skills/prose-tighten/scripts && python3 -m pytest test_flesch.py -v
```

Expected: all tests pass (target ~29 total).

- [ ] **Step 2: Sanity check that the SKILL.md frontmatter parses**

```bash
head -10 skills/prose-tighten/SKILL.md
```

Expected: frontmatter starts with `---`, has `name:` and `description:` lines, and ends with `---`.

- [ ] **Step 3: Verify nothing in the skill prompt mentions hallucinating Flesch**

```bash
grep -i -E "estimat|approximat|ballpark" skills/prose-tighten/SKILL.md
```

Expected: only matches that explicitly *forbid* these (in the Hard rules section), not any that suggest doing them.

- [ ] **Step 4: Confirm the v1 ships without lock-block support**

```bash
grep -i "scholark_lock\|scholark:lock" skills/prose-tighten/SKILL.md
```

Expected: no matches. Lock support is v1.1 — the design memo lives in our brainstorm memory, not in the shipped skill.

- [ ] **Step 5: Final commit (if any housekeeping changes were made above)**

```bash
git status
```

If clean, no commit needed. If there are uncommitted changes from the verification pass, commit:

```bash
git add -A
git commit -m "chore: tidy prose-tighten before v1 ship"
```

---

## Self-review (already done; tasks above reflect this)

**Spec coverage check:** Every section of the spec maps to at least one task —
- Identity & invocation → Task 6 (frontmatter)
- Input handling, multi-file → Steps 1–3 of SKILL.md (Task 6)
- Procedure → Steps 4–8 of SKILL.md (Task 6)
- Whole-paper handling → Step 4–5–8 of SKILL.md (Task 6)
- Output bundle → Step 10 of SKILL.md (Task 6)
- Error handling → Edge cases section of SKILL.md (Task 6)
- Flesch hard rules → Hard rules section + Step 9 of SKILL.md (Task 6) + flesch.py (Tasks 1–5)
- `.scholark/` artifact dir → Step 10 of SKILL.md (Task 6)
- Auto-discovery of working paper → Step 1 of SKILL.md (Task 6)
- README/CLAUDE.md updates → Task 7

**Placeholder scan:** No "TBD", "implement later", "similar to Task N" — every code-emitting step shows the actual code.

**Type consistency:** `strip_latex` and `compute` and `main` keep their signatures across tasks. JSON keys are `fre`, `fkgl`, `words`, `sentences`, `error` — same in tests, helper, and skill prompt.

---

## Notes for the executing engineer

- **Do not skip the TDD cycle in Phase 1** — write the failing test first, see it fail, then implement. The LaTeX-stripping regex is fiddly; tests catch regressions cheaply.
- **`textstat` install can fail on PEP 668 systems** (newer macOS Python, system Linux). If the install command in Task 4's prerequisite errors, use a venv: `python3 -m venv .venv && source .venv/bin/activate && pip install textstat pytest`. Run pytest from inside the venv. The skill itself, when invoked at runtime, will face the same issue and is designed to ask the user — see Step 9 of `SKILL.md`.
- **Do not change the JSON contract** of `flesch.py` (`fre`, `fkgl`, `words`, `sentences`, `error`). The skill prompt parses these keys; renaming them silently breaks the skill at runtime.
- **Commit messages must stay under 3 sentences** (per Simo's global CLAUDE.md). Conventional commits format: `feat:`, `fix:`, `docs:`, `chore:`.
- **Do not implement block protection** (`\begin{scholark_lock}...\end{scholark_lock}`). It is explicitly out of scope for v1; the design is being thought through separately for the whole toolkit.
- **The `flesch.py` script has no dependencies beyond `textstat`** — keep it that way. No `pandoc`, no `beautifulsoup`, no `nltk`. The whole point is to stay easy to install on any researcher's laptop.
