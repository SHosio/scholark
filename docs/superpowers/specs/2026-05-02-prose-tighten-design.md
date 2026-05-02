# Design: prose-tighten skill

**Date:** 2026-05-02
**Status:** Draft, pending implementation
**Skill name:** `prose-tighten`
**Plugin:** Scholark

## Motivation

LLM-assisted academic writing tends to produce prose with sagging readability scores (long sentences, fluff phrases, nominalizations) — but optimizing directly for Flesch Reading Ease backfires in academic contexts because the metric punishes load-bearing technical vocabulary indiscriminately. Researchers iterating in Claude Code need a way to tighten their prose before it leaves for Overleaf, *without* losing field-specific terminology and *without* targeting a Flesch number.

The right model is: shorten sentences, cut fluff, fix nominalizations — and *protect* technical vocabulary, asking the user when uncertain. Flesch is reported as a diagnostic only, never as a target.

## Scope

**In scope (v1):**
- Sentence-level edits: split long sentences, remove fluff phrases, simplify wordy connectives.
- Verb/noun-level edits: nominalizations, passive→active, redundant qualifiers, hedging stacks.
- Terminology protection: ask the user about high-uncertainty terms before editing; flag medium-uncertainty terms in a post-edit report.
- Flesch / Flesch-Kincaid as before/after diagnostics with explicit "do not optimize for these" disclaimer.
- `.tex` only.
- Whole-paper or per-section invocation.
- Multi-file LaTeX projects (`\input` / `\include` / `\subfile` followed recursively).

**Out of scope (v1):**
- Replacing technical vocabulary with lay terms unless user-confirmed.
- Restructuring arguments, sections, or contributions (that is `paper-review`'s job).
- Citation reformatting.
- Paragraph-level cohesion rewrites (Williams-style old-info → new-info flow). Stretch goal for v2.
- `.md`, `.txt`, or `.pdf` input.
- Block-protection markers (e.g., `\begin{scholark_lock}...\end{scholark_lock}`) — deferred to v1.1 once the cross-skill convention is settled (see memory: `project_block_protection.md`).
- Persistent memory of terminology decisions across runs on the same paper — deferred until `.scholark/state/` is designed.

## Skill identity

**Name:** `prose-tighten`

**Frontmatter description (for SKILL.md):**

> Tighten academic prose without losing field-specific terminology. Splits long sentences, cuts fluff, fixes nominalizations. Asks before touching technical terms. `.tex` only. Use when the user says "tighten this", "tighten the intro", "shorten this section", "make this clearer", "check writing complexity in X", "prose pass on the methods", "this paragraph is too dense", or "fix the prose in section 3".

**Where it sits among Scholark skills:** sibling to `paper-review` and `literature-blind-spots`. Natural workflow pairing: `prose-tighten` → `paper-review` (tighten the prose, then have the structural review run on a clean version).

## Input handling

**Auto-discovery of the working paper.** Skill does not require an explicit file pointer. By default it locates the working paper in the project root by scanning for the `.tex` file containing `\documentclass{}` and `\begin{document}`. In single-paper projects (the common case) this is unambiguous. If the project has multiple candidate entry-point files, the skill lists them and asks the user to choose.

**Section reference.** Free-text from the user, mapped to LaTeX structure:
- "the intro" / "introduction" → `\section{Introduction}` or fuzzy match
- "section 3" → 3rd `\section{}` block by document order
- "methods and results" → multiple sections processed in order
- "the abstract" → `\begin{abstract}...\end{abstract}`
- No section reference, or "tighten the whole paper" → whole-paper mode (see Whole-paper handling)

When the section reference is ambiguous (e.g., "the part about RCA"), the skill lists the document's section structure and asks the user to pick.

**Multi-file projects.** The skill follows `\input{}`, `\include{}`, and `\subfile{}` recursively to build a virtual flat view. Section targeting works against the virtual view; edits go to the physical file that owns the prose.

## Never-touch zones

The skill must mask these zones from edit candidates:

- Citations: `\cite{}`, `\citep{}`, `\citet{}`, `\autocite{}`, `\textcite{}`, `\ref{}`, `\autoref{}`, `\label{}`
- Math: `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, and `equation` / `align` / `eqnarray` / `gather` environments
- Code/verbatim: `verbatim`, `lstlisting`, `minted` environments, `\verb||`
- Quoted speech: `` ``...'' ``
- Figure/table captions (`\caption{}` contents) — left alone in v1
- Comment lines (anything after unescaped `%`)
- User-defined custom commands — skill leaves `\customcmd{...}` whole rather than peeking inside
- Includes inside `\iffalse...\fi` or commented-out `\input{}` lines

**In-scope zones:** plain prose between paragraphs and *inside* formatting wrappers like `\emph{}`, `\textbf{}`, `\textit{}` (display, not semantics — words inside are fair game).

## Procedure

The skill executes these steps in order:

1. **Resolve target.** Auto-discover the working paper. Identify section(s) to process. Confirm with user only if ambiguous.
2. **Read prose.** Extract in-scope text, masking never-touch zones.
3. **Scan for candidates:**
   - Long sentences (>30 words OR >2 independent clauses — calibration heuristic, not a hard rule)
   - Fluff phrases (canonical list: "plays a central role in", "as a result", "in practice", "it is important to note that", "due to the fact that", and similar — list maintained inside the skill prompt)
   - Nominalizations ("performance of analysis" → "analyzing", "the determination of X" → "determining X")
   - Wordy connectives ("due to the fact that" → "because", "in order to" → "to")
   - Passive constructions where active reads better
   - Hedging stacks ("may potentially possibly")
   - Redundant qualifiers ("very unique", "completely eliminated")
   - **Terminology candidates** — words that *might* be lay-replaceable but *might* be load-bearing field terms
4. **Triage terminology candidates** (hybrid rule):
   - High uncertainty (no obvious lay synonym OR no nearby gloss/definition) → batch into one question to the user before any edits: *"Are these load-bearing terms? [list with yes/no]"*
   - Medium uncertainty (plausible synonym exists, looks safe) → make best guess, flag in the post-edit report
5. **Multi-file safety check.** If the pass will edit any file other than the auto-discovered entry-point file (because the targeted section's prose lives in an included file), the skill says once before any edits:
   > *"This pass will edit: rw.tex (included from main.tex). Proceed? [y/n]"*
   This applies to every mode — section-targeted or whole-paper. If only the entry-point file is touched, no question is asked.
6. **Apply edits in place.** Edit the `.tex` file(s) directly. Edits respect never-touch zones — sentences containing citations or math have prose tightened around them while the protected tokens pass through unchanged.
7. **Compute Flesch (diagnostic only).** Strip LaTeX commands, run Flesch Reading Ease + Flesch-Kincaid Grade Level on the resulting plain text, record before/after numbers. Output explicitly states these are diagnostics, not targets.
8. **Emit reports** (see Output bundle).
9. **Halt cases:**
   - No candidates found → report "nothing to tighten — prose is already tight" + Flesch numbers as confirmation. Encouraging, not a failure.
   - User answers "no, load-bearing" to every terminology question → proceed with non-terminology edits only, note in summary.

## Whole-paper handling

When the user invokes the skill on the whole paper (no section reference, or "tighten the whole paper"):

1. **Enumerate sections.** Skill identifies all `\section{}` blocks in document order across the virtual flat view (following `\input{}`/`\include{}`/`\subfile{}`). Treats `\section{}` as the processing unit; subsections are processed as part of their parent. The abstract is a separate unit.
2. **Volume check.** Skill scans all sections to count candidates first. If the total exceeds 150 (initial calibration — Simo will tune in practice), it warns:
   > *"Found 240 candidates across 8 sections. Whole-paper passes that big are hard to review in one diff. Suggest running section-by-section. Proceed with whole-paper anyway? [y/n]"*
   Below the threshold, no warning.
3. **Multi-file safety check.** Inherits from the general procedure (step 5) — if the whole-paper pass will edit multiple included files, the skill names them and asks once before editing.
4. **One unified terminology batch.** Skill collects high-uncertainty terminology candidates across all sections, deduplicates them (one decision per term covers every occurrence), and asks them in one batch question before any edits begin.
5. **Sequential edits.** Skill edits Section 1 → Section 2 → ... → Conclusion in order. **No chat updates between sections.**
6. **One rolled-up report.** Sidecar report has section-by-section breakdown but is one file. In-chat summary shows totals across the paper plus a one-line per-section row.
7. **Halt-on-error.** If the skill hits something unparseable mid-paper (e.g., a section block that can't be cleanly tokenized), it stops at that section, reports what was completed and where it halted. No partial-mess silent finish.

**Subsection targeting:** if the user names a subsection ("subsection 3.2", or its title), the skill targets that subsection specifically. Sub-section is a valid unit, just not the default for whole-paper mode.

**Resolution rules for includes:**
- `\input{rw}` resolves to `rw.tex` (default `.tex` extension)
- Relative paths resolve relative to the file doing the include
- `\subfile{}` (from the `subfiles` package) is followed the same way
- Includes inside `\iffalse...\fi` or commented-out `\input{}` lines are skipped
- Missing include files → skill skips with a warning ("rw.tex referenced but not found"), continues
- **Circular includes** → skill detects, bails with a clear error before editing anything
- **Absolute paths or paths outside project root** → skill refuses to edit and asks user to invoke directly on the file (v1 caution)
- Same prose included multiple times → skill processes the source file once; edits propagate to every include site

## Output bundle

The skill emits five things after a pass:

1. **In-place edits to the `.tex` file(s).** The diff is the primary review surface — user reviews via Overleaf / their editor / `git diff`.

2. **Brief in-chat summary.** Scannable response in the Claude Code conversation. Contains:
   - Sections processed (with line ranges)
   - Edit counts: N sentences split, M fluff phrases removed, X nominalizations fixed, Y wordy connectives, Z passive→active flips, W terminology terms touched
   - Flesch Reading Ease before → after, Flesch-Kincaid Grade Level before → after, with the disclaimer that these are **diagnostics only**, not optimization targets
   - One-line pointer to the sidecar report

3. **Sidecar markdown report.** Written to `.scholark/reports/prose-tighten/<paper-stem>-<timestamp>.md` in the project root. Contains:
   - **Section A — Change log:** every edit, organized by category, with line numbers and before/after snippets
   - **Section B — Terminology touched:** every term modified (whether user-confirmed or auto-decided), with original term, replacement, rationale, and confidence level — the audit trail for "did I lose anything load-bearing?"
   - **Section C — Uncertain calls:** non-terminology edits the skill wasn't fully confident about (ambiguous antecedents, sentences where a split might shift emphasis), each with a "verify this" line and line number
   - **Section D — Skipped candidates:** things the skill noticed but chose *not* to touch (terminology user said is load-bearing, long sentences whose structure was deemed essential)
   - Timestamp in the filename so multiple passes accumulate (audit trail) rather than overwrite

4. **Verify-nothing-lost prompt.** Last line of the in-chat summary, every time, no exceptions:
   > *Please review the diff and confirm no critical terminology or meaning was lost. If anything is wrong: `git checkout -- <file>` to revert all, or revert specific hunks in your editor.*

5. **Git status reminder.** If the `.tex` file was tracked but uncommitted before the run, skill notes this and suggests staging the prior state first (so the user has a clean revert point). If already clean, no reminder.

**`.scholark/` setup:** on first write to `.scholark/`, the skill checks if `.scholark/` is in the project's `.gitignore`. If not (and a `.gitignore` exists), it appends and notes in the chat output. If no `.gitignore` exists, it just creates the directory — does not generate a `.gitignore` for the user.

## Error handling

- **Wrong file type.** User points at `.md`, `.txt`, `.pdf`. Skill responds: *"prose-tighten is `.tex` only — for other formats, point me at the source `.tex` file."* No partial work.
- **No working paper found.** Project has no `.tex` file with `\documentclass{}`. Skill asks: *"I can't find a `.tex` paper in this project. Which file should I tighten?"*
- **Multiple candidate papers.** Skill lists the candidates and asks user to pick.
- **LaTeX parse failures.** Unbalanced braces, unclosed environments, malformed includes. Skill reports the failure with file + line, makes **no edits**, suggests user fix the syntax and retry.
- **User cancels mid-run.** If interrupted between terminology batch and edits, no edits made — skill exits cleanly. If interrupted mid-edit, last completed edit is on disk; user reverts via git or per-hunk in editor. Skill does not attempt self-rollback.
- **Not a git repo.** Skill still works. Drops git-specific parts of verify prompt and gitignore handling. Tells user: *"this directory isn't a git repo — review the diff in your editor; no automatic revert is available."*
- **Skill invoked twice on same file.** Each run produces a new timestamped report. v1 does not remember terminology decisions across runs — every invocation starts fresh.
- **Empty section** (header exists but body is just `\input{...}`). Skill recognizes the forwarding header, follows the include, processes the actual content there.

## Architecture

Single `SKILL.md` file at `skills/prose-tighten/SKILL.md`, following the structure of `paper-review/SKILL.md` and `literature-blind-spots/SKILL.md`. No code, no dependencies, no build — it is a markdown procedure that Claude executes when invoked.

The discipline (preserve terminology, ask when unsure, never touch citations/math/code/quotes/captions, never optimize for Flesch) lives entirely in the skill prompt where it can be reviewed in one place.

If discipline drift becomes a real problem in practice (e.g., the skill keeps replacing technical terms despite the rules), v2 can split into orchestrating skill + tightener sub-agent + verifier sub-agent (mirroring `research-brainstorm`'s pattern). v1 trusts the prompt.

## Cross-skill conventions established or honored

- **`.scholark/` artifact directory** (established by this skill): reports go to `.scholark/reports/prose-tighten/`. See memory `project_scholark_artifact_dir.md`. Future skills writing artifacts should use the same root.
- **Auto-discovery of the working paper**: skill does not demand an explicit file pointer. See memory `feedback_paper_inference.md`. Already the implicit convention used by existing Scholark skills.
- **Block protection** (deferred): when the Scholark-wide block-protection convention is settled (see memory `project_block_protection.md`), prose-tighten v1.1 picks up support — likely a single rule added to the SKILL.md prompt.

## Open questions for implementation

These are calibration decisions to defer until the skill is in use:

- The 30-word / 2-clause threshold for "long sentence" — initial guess; tune from real usage.
- The 150-candidate volume threshold for whole-paper mode — initial guess; tune from real usage.
- The fluff-phrase canonical list — start with a base set, expand as Simo flags more in practice.
- Which `\textbf{}` / `\emph{}` wrappers to consider semantic vs display (e.g., does Simo use `\emph{microservices}` to mark a defined term?). For v1, all formatting wrappers are display.

## Workflow integration

Pairing with `paper-review` (the canonical recommended workflow):
1. User runs `prose-tighten` on the draft → tighter prose, terminology preserved.
2. User reviews the diff, accepts or reverts.
3. User runs `paper-review` on the tightened draft → structural / argumentative review on cleaner prose.

This pairing is a candidate for the future Scholark lander "best workflows" gallery (see memory `project_workflow_gallery.md`).
