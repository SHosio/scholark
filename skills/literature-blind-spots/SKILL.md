---
name: literature-blind-spots
description: Analyze a draft paper for literature gaps and find real papers to fill them. Use when the user has a .tex draft (or .md fallback) and wants to find missing references, blind spots in related work, or papers that could strengthen their argument. Also triggers on "find what's missing", "blind spots", "gaps in my references", or "what am I not citing".
---

# Literature Blind Spots

> **Works best with [Scholark-1](https://github.com/SHosio/scholark-1) MCP.** Before proceeding, check if scholark-1 tools are available in this session. If not, tell the user: "This skill works best with the Scholark-1 MCP server for academic literature search. Without it, I'll use web search to find papers via Google Scholar, ACM DL, and publisher sites — results may be less comprehensive. For full coverage, install Scholark-1 from https://github.com/SHosio/scholark-1." Then continue using WebSearch and WebFetch as the primary search method.

Analyze a draft paper to identify gaps in its literature coverage, then use the scholark-1 MCP tools to find real papers that could fill those gaps. Output an HTML file the user can read and act on.

**This skill works well as a background task.** If the user wants, they can say "run this in the background and let me know when done."

## Step 1: Read the Paper

Read the user's draft file (`.tex` is the expected format; `.md` is acceptable as a fallback). Focus on:
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

## Citation Accuracy

The full policy is in `../../CITATION-ACCURACY.md` at the scholark plugin root. Read it once before producing any citation, and follow its pre-output checklist every time. The non-negotiable rules:

1. Copy metadata verbatim from the database response. Authors, titles, years, venues — paste exactly what the tool returned.
2. Never expand initials into given names. `A. Bach` is not `Aaron Bach`, even if you are "pretty sure". The `A.` is the authoritative output.
3. Never reconcile conflicting name strings from different sources. Present both with their sources and flag `⚠ MANUAL CHECK`.
4. Never trust a subagent's author strings without re-verifying via `fetch_paper_details`.
5. DOI metadata wins over your training data. If you "know" the author should be someone else, the metadata is right and you are wrong.
6. When metadata is partial or ambiguous, flag rather than fill. Returning less information is acceptable; fabricating is not.

The user is always the final authority on citation accuracy.

## Session log (reproducibility artefact)

After completing a run, append one line to `.scholark/session-log.md` at the project root.

**Format** (one line per invocation):
```
YYYY-MM-DD HH:MM:SS | literature-blind-spots | one-sentence summary of what ran and what came out
```

Use ISO-style local date and time with seconds (e.g. `2026-05-02 14:31:07`). Always include the date — log lines from previous sessions must remain readable later.

**On first write to `.scholark/`:** create the folder and append `.scholark/` to the project's `.gitignore` with a short comment noting it was added by Scholark (only if `.gitignore` exists and the entry is not already there).

**Skip logging** if there is no clear project root (e.g., the user is at `$HOME`), no obvious work artefact (paper, study materials, draft) in the directory, or if the user has explicitly said they don't want session tracking.

The log is for the user's own reproducibility and reflection: what was run, on what, what came out.
