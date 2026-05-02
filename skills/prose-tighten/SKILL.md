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

**Whole-paper mode:** collect terminology candidates across *all* sections first, deduplicate so each term appears once, and ask the single batch question before any section is edited. One decision per term covers every occurrence.

## Step 8: Apply edits in place

Edit the `.tex` file(s) directly. Edits respect never-touch zones — sentences containing citations or math have prose tightened around them while the protected tokens pass through unchanged.

For whole-paper mode: edit Section 1 → Section 2 → ... in order, no chat updates between sections.

If you hit something unparseable mid-paper (a section block that can't be tokenized cleanly), stop at that section. Report what was completed and where you halted. Do NOT silently finish with a partial mess.

## Step 9: Compute Flesch (diagnostic only)

Compute Flesch Reading Ease and Flesch-Kincaid Grade Level **before and after** the edits using the helper script. The script lives in this skill's own folder under `scripts/flesch.py`. Claude Code provides this skill's base directory when the skill is loaded — use it to construct the path:

```bash
python3 <SKILL_BASE_DIR>/scripts/flesch.py <path-to-tex>
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
The closing line of the in-chat summary (shown above in section B) is mandatory, every run, no exceptions.

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

## Session log (reproducibility artefact)

After completing a run, append one line to `.scholark/session-log.md` at the project root.

**Format** (one line per invocation):
```
YYYY-MM-DD HH:MM:SS | prose-tighten | one-sentence summary of what ran and what came out
```

Use ISO-style local date and time with seconds (e.g. `2026-05-02 14:31:07`). Always include the date — log lines from previous sessions must remain readable later.

**On first write to `.scholark/`:** create the folder and append `.scholark/` to the project's `.gitignore` with a short comment noting it was added by Scholark (only if `.gitignore` exists and the entry is not already there).

**Skip logging** if there is no clear project root (e.g., the user is at `$HOME`), no obvious work artefact (paper, study materials, draft) in the directory, or if the user has explicitly said they don't want session tracking.

The log is for the user's own reproducibility and reflection: what was run, on what, what came out.
