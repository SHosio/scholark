---
name: literature-blind-spots
description: Analyze a draft paper for literature gaps and find real papers to fill them. Use when the user has a .tex, .md, or .pdf draft and wants to find missing references, blind spots in related work, or papers that could strengthen their argument. Also triggers on "find what's missing", "blind spots", "gaps in my references", or "what am I not citing".
---

# Literature Blind Spots

> **Works best with [Scholark-1](https://github.com/SHosio/scholark-1) MCP.** Before proceeding, check if scholark-1 tools are available in this session. If not, tell the user: "This skill works best with the Scholark-1 MCP server for academic literature search. Without it, I'll use web search to find papers via Google Scholar, ACM DL, and publisher sites — results may be less comprehensive. For full coverage, install Scholark-1 from https://github.com/SHosio/scholark-1." Then continue using WebSearch and WebFetch as the primary search method.

Analyze a draft paper to identify gaps in its literature coverage, then use the scholark-1 MCP tools to find real papers that could fill those gaps. Output an HTML file the user can read and act on.

**This skill works well as a background task.** If the user wants, they can say "run this in the background and let me know when done."

## Step 1: Read the Paper

Read the user's draft file (.tex, .md, or .pdf). Focus on:
- **Claims made** — What does the paper assert? What does it take for granted?
- **Related work coverage** — What fields, methods, and frameworks are cited?
- **Methods** — What methodological approach is used? Are there precedents not cited?
- **Discussion** — What implications are drawn? What limitations are acknowledged?
- **Theoretical framing** — What framework is used? Are alternatives acknowledged?

## Step 2: Identify Blind Spots

Categorize gaps into these types:

1. **Missing foundational work** — Seminal papers in the area that should be cited
2. **Adjacent field connections** — Work from related fields (psychology, sociology, design, education, etc.) that directly relates but isn't cited
3. **Methodological precedents** — Similar methods used in other contexts that validate or challenge the approach
4. **Competing/alternative frameworks** — Theoretical perspectives that offer different explanations
5. **Recent developments** — Papers from the last 2 years that the authors may have missed
6. **Replication & meta-analysis** — Review papers or replications that contextualize the work

## Step 3: Search for Papers

For each blind spot, use scholark-1 MCP tools:
- `search_papers` — broad keyword search across all 4 databases
- `search_by_topic` — topic-focused search with year filtering
- `fetch_paper_details` — get full metadata for promising results

Search strategically:
- Use different query formulations per gap
- Try both broad and narrow searches
- Look for review/survey papers in the area
- Check citation counts to prioritize influential work

### Handling Thin or Failed Results

Semantic Scholar is frequently rate-limited. If scholark-1 searches return fewer results than expected, empty results, or errors:

1. **Try reformulating queries** with different keywords, broader/narrower scope, or different scholark-1 tools.
2. **Fall back to web search.** Use WebSearch to search Google Scholar (`site:scholar.google.com`), ACM Digital Library (`site:dl.acm.org`), IEEE Xplore, or other academic sources. Use WebFetch to pull paper details from publisher landing pages or DOI resolvers.
3. **Note the source.** Papers found via web search fallback may have less structured metadata. Mark them clearly and advise the user to verify details.
4. **Don't give up on a blind spot** just because the API is throttled. A gap in the literature is still a gap even if the search tool is struggling.

## Step 4: Generate HTML Output

Write an HTML file to the current working directory named `blind-spots-[date].html`. The file should be self-contained (inline CSS, no external dependencies) and readable in any browser.

### HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>Literature Blind Spot Analysis — [Paper Title]</title>
    <style>
        /* Clean, readable styling */
        body { font-family: -apple-system, system-ui, sans-serif; max-width: 900px; margin: 0 auto; padding: 2rem; line-height: 1.6; color: #1a1a1a; }
        h1 { border-bottom: 2px solid #333; padding-bottom: 0.5rem; }
        .category { margin: 2rem 0; padding: 1.5rem; border-left: 4px solid #2563eb; background: #f8fafc; }
        .category h2 { margin-top: 0; color: #1e40af; }
        .paper { margin: 1rem 0; padding: 1rem; background: white; border: 1px solid #e2e8f0; border-radius: 4px; }
        .paper h3 { margin: 0 0 0.5rem 0; }
        .paper .doi { font-family: monospace; font-size: 0.85rem; }
        .paper .doi a { color: #2563eb; }
        .reasoning { color: #4a5568; font-style: italic; margin-top: 0.5rem; }
        .source-tag { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 0.75rem; background: #e2e8f0; }
        .meta { font-size: 0.85rem; color: #64748b; }
    </style>
</head>
<body>
    <h1>Literature Blind Spot Analysis</h1>
    <p class="meta">Paper: [title] | Analyzed: [date] | Gaps found: [N]</p>
    <p>[Brief summary of the paper's focus and scope]</p>

    <!-- For each category -->
    <div class="category">
        <h2>[Category Name]</h2>
        <p>[Why this gap matters for this specific paper]</p>

        <div class="paper">
            <h3>[Paper Title]</h3>
            <p class="doi">DOI: <a href="https://doi.org/[DOI]">[DOI]</a></p>
            <p><strong>Authors:</strong> [authors] | <strong>Year:</strong> [year] | <span class="source-tag">[Source: database]</span></p>
            <p>[Abstract or key finding]</p>
            <p class="reasoning"><strong>Why this paper matters:</strong> [How it could strengthen the draft — be specific about which section or claim it supports/challenges]</p>
        </div>
        <!-- More papers... -->
    </div>
    <!-- More categories... -->
</body>
</html>
```

## Step 5: Report to User

Tell the user:
- Where the file was saved
- How many blind spots were found across how many categories
- The 2-3 most important gaps (the ones that a reviewer would most likely flag)
- Suggest they review the HTML file and decide which papers to add

## Rules

- **Only include papers you actually found via scholark-1.** Never fabricate titles, DOIs, or authors.
- **Be specific about why each paper matters.** Not "this is related" — explain how it would strengthen a specific part of the draft.
- **Prioritize quality over quantity.** 3 highly relevant papers per gap are better than 10 tangentially related ones.
- **Note uncertainty.** If a search returned limited results for a gap, say so. The gap may still be real even if papers are hard to find.
- **Include the source database** for each paper (Semantic Scholar, OpenAlex, Crossref, Europe PMC) — this is how scholark-1 works.

## Citation Accuracy — CRITICAL

The full authoritative policy lives in `../../CITATION-ACCURACY.md` at the scholark plugin root. That document is the source of truth; the summary below restates it for discoverability, but if the two ever disagree, follow `CITATION-ACCURACY.md`.

**Never trust your own knowledge of authors, titles, or publication details.** Your training data contains associations (e.g., a well-known researcher in a subfield) that will cause you to "recognize" authors who are not on a paper. This is hallucination, and in academic work it corrupts citations.

### The Absolute Rules

1. **Copy metadata verbatim from the database response.** Author names, titles, years, venues — paste exactly what the tool returned. Do not reformat, do not "clean up," do not translate.
2. **NEVER expand initials into given names.** If the database returns `A. Bach`, write `A. Bach` — not `Aaron Bach`, not `Andreas Bach`, not `A. K. P. Bach`. Expanding `A.` into a full first name is fabrication, even if you're "pretty sure" who the author is. The `A.` is the authoritative output. Leave it alone.
3. **NEVER add middle initials, middle names, or honorifics** that the database did not return. Two initials is not three initials.
4. **NEVER reconcile conflicting name strings from different sources.** If Semantic Scholar says `A. Bach` and OpenAlex says `Aaron Kim Peter Bach`, do not merge, average, or pick — present BOTH strings with their sources, and flag for manual inspection.
5. **NEVER trust a subagent's author strings without verifying via `fetch_paper_details`.** Subagents can hallucinate too. If a subagent returns author names, re-fetch the paper details directly before putting those names in the output.
6. **DOI metadata over gut feeling.** If DOI metadata says the author is Ruth Schmidt and you "know" it should be Albrecht Schmidt — the metadata is right and you are wrong. Never dismiss a metadata mismatch as a "database error."
7. **When in doubt, go online.** Fetch the actual paper page, the publisher landing page, the DOI resolver. Use every tool at your disposal to find the truth.
8. **Never silently resolve discrepancies.** Present what you found, what the sources say, and let the user make the final call.
9. **Never auto-correct author names, titles, or years.** Present both versions and ask.

### When the Metadata is Partial or Ambiguous — FLAG, DO NOT FILL

Any of these conditions require flagging for manual inspection rather than guessing:

- The database returned only initials (e.g., `A. Bach`, `N. van Berkel`) and you want to know a full name
- Two sources disagree on an author's name spelling or form
- The venue field is `"Not available"` or missing
- The year is missing or reported inconsistently across sources
- A subagent returned names that differ from what `fetch_paper_details` returns

**How to flag in the HTML output:** use a visible marker like `⚠ MANUAL CHECK` next to the affected field, with a one-line note explaining what the disagreement is. Example:

```
Authors: A. Bach, T. M. Nørgaard, J. Brok, N. van Berkel ⚠ MANUAL CHECK — initials only; verify full names against the publisher page before citing.
```

It is always acceptable to return LESS information (initials, partial author list, "year unknown") than the user wants. It is NEVER acceptable to return FABRICATED information.

### Pre-Output Checklist

Before writing the HTML file, for every paper entry, verify:

- [ ] Every author name appears exactly as in a `fetch_paper_details` response (or exactly as in the original `search_papers` response if no fetch was done).
- [ ] No given name has been expanded from an initial.
- [ ] No author has been added, removed, or reordered.
- [ ] The title is a verbatim copy-paste (no corrections of capitalization, punctuation, or typos).
- [ ] The year, venue, and DOI match the database response.
- [ ] Any ambiguity is marked `⚠ MANUAL CHECK` rather than silently resolved.

**The user is always the final authority on citation accuracy. Your job is to surface what the databases actually said, not to produce a polished final citation.**
