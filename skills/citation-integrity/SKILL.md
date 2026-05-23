---
name: citation-integrity
description: Verify every inline citation in an academic paper by spawning one verifier agent per cited source that reads the full paper before judging the claim. Use whenever the user asks for a citation audit, citation integrity check, citation accuracy review, pre-submission citation pass, or anything that involves checking whether the wording around a `\cite{}` actually matches what the cited paper says. Triggers on phrases like "audit my citations", "verify references", "check that my citations are accurate", "make sure I haven't misrepresented any cited work", "citation pre-submission review", "are my citations correct?", "find misleading citations", "find wrong citations", "citation integrity check". The skill expects every cited paper to be available as a markdown file in a context folder, one `.md` per bibtex citekey. If any cited paper is missing the skill stops and warns the user, encouraging them to obtain the source by their own means (institutional access, preprints, contacting authors) or to convert provided PDFs via the bundled `marker_single` wrapper; only with the user's explicit confirmation does it proceed and report those citations as "Not audited (source missing)". The skill never independently fetches sources from the web or scholarly databases. Produces a structured audit report with Verified / Partial / Misleading / Wrong / Unverifiable / Not audited verdicts per claim plus suggested fixes, and a per-paper publication context map as an optional byproduct.
---

# Citation Integrity

Rigorously verify every inline citation in an academic manuscript. The skill reads each cited paper in full (from local markdown the user has prepared) and checks whether the manuscript's wording matches what the source actually says. Designed for the moment before submission, when soft errors in citation accuracy are most costly to leave in.

> **Offline by design.** Unlike `/scholark:literature-blind-spots` and `/scholark:paper-review`, this skill never fetches anything from the web or scholarly databases. The audit is grounded in the source markdown the user has prepared. If a cited paper is not in the context folder, the skill stops and asks the user how to proceed.

This skill is the active enforcer for the policy stated in `../../CITATION-ACCURACY.md`: every claim is grounded in text actually seen in the source paper. Citation-integrity verifies what manuscripts already cite; `literature-blind-spots` finds what they should also cite; `paper-review` flags structural issues. Run all three before submission.

## What the skill produces

Two artifacts:

1. **Audit report** written to `.scholark/reports/citation-integrity/<paper-stem>-<YYYY-MM-DD-HHMM>.md` in the project root. Severity-sorted entries (Wrong → Misleading → Partial → Verified → Unverifiable → Not audited), each with the manuscript line, the exact claim sentence, a source-grounded justification, and a suggested fix. Headline counts at the top.

2. **Publication context map** (optional) at `<context-folder>/publications-context-map.md`. One entry per cited paper summarising what the paper is, why it is cited here, and adjacent angles the manuscript could draw on. Generated as a byproduct of the full-paper reads. The map is a user artifact; future audit runs ignore it and re-read the source each time.

## Step 1: Find the working paper and context

The skill needs three things from the project. Auto-discover where possible; ask one tight clarifying question when ambiguous.

**Manuscript.** Auto-discover the `.tex` file using the same pattern as `prose-tighten`: look for a file containing both `\documentclass{}` and `\begin{document}` in the project root or its immediate subdirectories. If multiple candidates exist, list them and ask. Pandoc Markdown (`.md`) is accepted as a fallback for manuscripts that are not in LaTeX. If neither is found, ask the user.

**Context folder.** A directory containing one `<citekey>.md` per cited paper. Try in order: `context/`, `paper/context/`, then a sibling directory containing many `.md` files named after citekeys. If none of these exist, ask the user where the source markdowns live (or whether they need to be created from PDFs in Step 3).

**Bibtex file (optional but recommended).** Try `references.bib`, `bibliography.bib`, or the first `.bib` file in the manuscript's directory. Used to surface paper titles when the coverage gate fires and when dispatching the verifier agents. If no `.bib` is found, the skill still runs; titles just appear as the citekey instead.

If anything is unclear, ask one question. Do not guess at file paths.

## Step 2: Extract citations from the manuscript

Run the citation extractor:

```bash
python3 <SKILL_BASE_DIR>/scripts/extract_citations.py <manuscript-path>
```

(Use the `--format markdown` flag for Pandoc Markdown manuscripts.)

The script returns a JSON inventory, one record per (citekey, occurrence) pair, with fields `{citekey, file, line, claim_sentence}`. It handles the LaTeX `\cite`, `\citep`, `\citet`, `\citeauthor`, `\citeyear`, `\autocite` families with their starred and optional-argument variants, expands multi-citekey commands like `\cite{A, B, C}` into three rows, and skips commented-out lines.

Group the inventory by citekey in memory. The next step queries against that grouping.

## Step 3: Coverage gate

Run the coverage checker:

```bash
python3 <SKILL_BASE_DIR>/scripts/check_coverage.py <citation-inventory.json> <context-folder> [--bib <references.bib>]
```

The script reports which citekeys have a corresponding `<citekey>.md` in the context folder and which do not. With `--bib`, it also surfaces the bibtex title for each missing entry so the user can identify them.

**The gate is critical.** The audit is most useful when every cited paper has a local markdown. If any markdowns are missing, do not silently proceed and do not attempt any independent lookup (no WebFetch, no DOI resolution, no MCP call). Surface the missing list prominently with bibtex titles and present three options:

1. **Provide PDFs and convert (strongly recommended).** The user supplies PDFs in a directory plus a mapping JSON of the form `[{"pdf": "wherearewenow.pdf", "citekey": "Riegel2021"}, ...]`. Run:
   ```bash
   bash <SKILL_BASE_DIR>/scripts/convert_pdfs.sh <pdf-dir> <mapping.json> <context-folder>
   ```
   The script wraps `marker_single` (from `pip install marker-pdf`), writes each PDF as `<citekey>.md` with YAML frontmatter (`source_pdf`, `converted_date`, `num_images`), and deletes the source PDFs unless `--keep-pdfs` is passed. After conversion, re-run Step 3. If `marker_single` or `jq` are missing, the script exits with install instructions; surface them to the user and do not attempt an alternative converter silently.

2. **Find the sources first by their own means.** Suggest this explicitly: institutional access, preprint servers, contacting authors. The skill stays out of this loop on purpose; the user has access channels the skill does not.

3. **Proceed without those sources (requires explicit confirmation).** The audit runs on the citekeys that do have markdowns. The missing citekeys' claims appear in the final report under a dedicated `Not audited (source missing)` section with occurrence count and bibtex title. The default disposition is to push back toward options 1 or 2; option 3 is the fallback for the genuine "I cannot get this paper" case.

## Step 4: Dispatch citation-verifier agents in parallel

Once every citekey either has a local markdown or the user has explicitly accepted option 3, dispatch verifiers.

In plain terms: spawn one `citation-verifier` agent per cited paper, all in parallel, in a single message containing one Agent tool call per citekey. Each agent reads the full markdown of its assigned paper and judges every claim where the manuscript cites it. The agent has only the `Read` tool, so it cannot search the web or query any database; the verdict is grounded purely in the source text the user already trusts.

**Agent prompt for each citekey.** Include:

- Citekey, full title, venue (short form), and year (from bibtex if available; otherwise leave blank fields explicit).
- Absolute path to `<context-folder>/<citekey>.md`.
- Numbered list of occurrences, each with manuscript line number, the verbatim claim sentence, and a note when the citation is co-cited with other papers.
- Reference to the verdict definitions in `../../references/citation-integrity/verdict-rubric.md` (the agent's own prompt body already embeds the core definitions, so the rubric is a deepening reference for borderline cases).

**Optional: include a context-map block.** If the user wants the publication context map byproduct, add a separate instruction block in the agent prompt asking for the per-paper context-map entry in the format of `../../references/citation-integrity/context-map-template.md`. Without that block, the agent returns verdicts only.

**Skip dispatch for citekeys without a markdown.** Those entries appear in the final report under `Not audited (source missing)`. Do not spawn an agent for them.

**If a verifier returns malformed output**, re-prompt once with a tighter format constraint. If still malformed, record the affected claims as `Unverifiable` with a "verifier error" note.

## Step 5: Synthesize the audit report

Consolidate all verifier verdicts into a single audit report at:

```
.scholark/reports/citation-integrity/<paper-stem>-<YYYY-MM-DD-HHMM>.md
```

Use the structure in `../../references/citation-integrity/audit-report-template.md`. Key elements:

- **Headline counts** at the top (Wrong / Misleading / Partial / Verified / Unverifiable / Not audited), plus a style-notes line if em-dashes or "not X, but Y" antithesis appeared in the manuscript prose during verification.
- **Entries grouped by severity**, not by paper. Authors fix top-down by impact.
- **Per entry**: manuscript line, exact citation text, source-grounded justification with a short quoted phrase, suggested fix.
- **Cross-cutting observations** at the end: patterns that recur across multiple citations (e.g. "in N citations we attribute our own synthesis to a source that does not itself make that claim"). These are often the highest-yield findings because fixing one root cause resolves several flagged claims at once.

After writing the file, summarise the headline counts inline to the user and offer to apply suggested fixes interactively.

**`.scholark/` setup.** On first write to `.scholark/`, create the folder. If a `.gitignore` exists at the project root and does not already contain `.scholark/`, append the entry with a short comment noting it was added by Scholark. If no `.gitignore` exists, just create the folder; do not generate a `.gitignore`.

## Step 6: Optional apply-fixes pass

If the user accepts, walk through each non-Verified entry one at a time. For each:

1. Show the manuscript line and the suggested replacement.
2. Wait for user confirmation (`y` / `n` / edit-then-apply).
3. Apply the change with the `Edit` tool.

Group Wrong and Misleading verdicts first; Partial verdicts last. Skip Verified entries (no change needed) and Unverifiable entries (no source to ground a fix in). For Not audited entries, the suggested fix is to obtain the source and re-run; no in-place edit is offered.

## Rules

These rules apply on every invocation. They are constraints, not heuristics.

1. **No independent web fetching.** The skill never calls WebFetch, WebSearch, or any scholarly MCP server. If a source is missing, the user provides it via PDF conversion or by other means. This is the boundary that keeps the audit honest.

2. **Hard coverage gate.** Never silently proceed when sources are missing. Surface the missing list with bibtex titles and require explicit user confirmation if the user chooses to proceed without those sources.

3. **Full re-reads of sources.** Every verdict is grounded in text the verifier agent actually read in the source markdown. If a context map already exists from a prior run, the audit ignores it for verification and only consults it for navigation.

4. **One verifier per citekey, in parallel.** A paper cited four times is read once; the same agent judges all four occurrences. Co-cited claims (e.g. `\cite{A, B}` for one sentence) appear in both agents' prompts, and each agent independently judges whether its paper supports the claim.

5. **No new citations.** The skill does not propose papers the manuscript should cite. That is `/scholark:literature-blind-spots`. Suggested fixes either rephrase the claim to match the source or recommend dropping the citation.

6. **Verdicts before fixes.** Phase 6 (apply-fixes) is opt-in and asks per-edit. The skill does not batch-edit the manuscript without per-claim confirmation.

7. **Prose conventions.** The audit report, the context map, and all suggested-fix wording follow the same two rules: no em-dashes (`—`), no "not X, but Y" antithesis. Use periods, commas, parentheses, or rewrites instead. These rules apply only to text the skill writes; the manuscript itself is not silently rewritten, but the skill flags such violations in a small "Style notes" section in the audit report when it spots them in passing.

## Bundled resources

- `scripts/extract_citations.py`: parses LaTeX and Pandoc Markdown manuscripts for citation occurrences with surrounding claim sentences.
- `scripts/check_coverage.py`: cross-checks citekeys against the context folder; surfaces bibtex titles for missing sources.
- `scripts/convert_pdfs.sh`: wraps `marker_single` to convert PDFs to `<citekey>.md` with YAML frontmatter.
- `../../agents/citation-verifier.md`: the dedicated read-only agent dispatched in Step 4. Self-contained: verdict definitions and per-claim format are embedded in the agent body.
- `../../references/citation-integrity/verdict-rubric.md`: full rubric with calibration examples. Use for borderline cases the agent surfaces, and as a reference document for the user.
- `../../references/citation-integrity/audit-report-template.md`: layout for the synthesis report.
- `../../references/citation-integrity/context-map-template.md`: layout for the optional publication context map byproduct.

## Dependencies

- **`marker_single`** (from the `marker-pdf` Python package). Required only when PDFs need to be converted. Install with `pip install marker-pdf`. If missing when needed, the conversion script exits with the install instruction; surface it and do not attempt an alternative.
- **`jq`** (used inside `convert_pdfs.sh`). Install via the system package manager.
- **Python 3.8+** for the bundled scripts.
- A sub-agent-capable environment (Claude Code) for the parallel verifier dispatch.

## Edge cases

- **Wrong manuscript type.** User points at `.pdf`, `.docx`, etc. Respond: "citation-integrity needs the source `.tex` (or Pandoc Markdown `.md`). Please point me at the source file." No partial work.
- **No working paper found.** Ask: "I can't find a manuscript in this project. Which file should I audit?"
- **Multiple candidate papers.** List them and ask the user to pick.
- **Context folder missing entirely.** Ask the user where source markdowns live, or whether they want to start by converting PDFs via Step 3 option 1.
- **Citekey case mismatch or typo in context folder.** The coverage check surfaces this. The user fixes the filename and re-runs Step 3.
- **Manuscript uses an unusual citation syntax.** The extractor covers LaTeX `\cite*` family and Pandoc `[@key]`. Extend `scripts/extract_citations.py` if needed; flag the limitation to the user before extending.
- **Cited paper genuinely unavailable.** The user takes option 3 in Step 3 and accepts that those citations will be reported as `Not audited (source missing)` rather than verified.
- **Verifier returns malformed output.** Re-prompt once with a tighter format constraint; if still malformed, mark affected claims as `Unverifiable` with a "verifier error" note.
- **Skill invoked twice on the same manuscript.** Each run writes a new timestamped report. The audit does not remember verdicts across runs; every invocation re-reads every source.
- **Not a git repo.** Skill still works. Drop git-specific parts of the `.gitignore` handling; the report still writes to `.scholark/reports/citation-integrity/`.

## Workflow integration

Recommended pre-submission ordering, paired with sibling skills:

1. `/scholark:literature-blind-spots` to find papers the manuscript should cite but does not.
2. `/scholark:paper-review` for structural and argumentative review.
3. `/scholark:prose-tighten` for sentence-level cleanup.
4. `/scholark:citation-integrity` (this skill) as the last pass before submission, when the citation set is stable.

Running this skill earlier is fine, but the audit is most useful once the citation set has stopped churning.

## Citation Accuracy

The full policy is in `../../CITATION-ACCURACY.md` at the scholark plugin root. This skill is the active enforcer of the policy's underlying principle: every claim about a cited paper must be grounded in text actually seen in that paper. The pre-output checklist in `CITATION-ACCURACY.md` applies whenever the audit report or context map names an author, title, year, or venue (which come from bibtex and the source markdown's own metadata, copied verbatim). Do not expand initials, do not reconcile conflicting strings across sources, and flag rather than fill when fields are partial or ambiguous.

## Session log (reproducibility artefact)

After completing a run, append one line to `.scholark/session-log.md` at the project root.

**Format** (one line per invocation):
```
YYYY-MM-DD HH:MM:SS | citation-integrity | one-sentence summary of what ran and what came out
```

Use ISO-style local date and time with seconds (e.g. `2026-05-02 14:31:07`). Always include the date; log lines from previous sessions must remain readable later.

**On first write to `.scholark/`:** create the folder and append `.scholark/` to the project's `.gitignore` with a short comment noting it was added by Scholark (only if `.gitignore` exists and the entry is not already there).

**Skip logging** if there is no clear project root (e.g., the user is at `$HOME`), no obvious work artefact (paper, study materials, draft) in the directory, or if the user has explicitly said they don't want session tracking.

The log is for the user's own reproducibility and reflection: what was run, on what, what came out.
