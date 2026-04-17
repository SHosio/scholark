# Citation Accuracy — Shared Policy

This is the authoritative policy on how skills and agents in scholark handle academic metadata (author names, titles, years, venues, DOIs). Any skill or agent that touches citations MUST follow these rules. Individual skill and agent files reference this document rather than duplicating the full text.

## Why this document exists

A production incident on 2026-04-17 produced fabricated author names ("Aaron Kim Peter Bach" invented from the database string "A. Bach") in a blind-spots HTML report. The failure mode was: a sub-agent returned initials, the main agent expanded them into full given names from "context," and the fabrication was not caught because the main agent did not re-verify against `fetch_paper_details`. The rules below close that class of error.

## The Absolute Rules

1. **Copy metadata verbatim from the tool response.** Author names, titles, years, venues — paste exactly what the tool returned. Do not reformat, do not "clean up," do not translate, do not re-case.

2. **NEVER expand initials into given names.** If the database returns `A. Bach`, write `A. Bach` — not `Aaron Bach`, not `Andreas Bach`, not `A. K. P. Bach`. Expanding `A.` into a full first name is fabrication, even if you are "pretty sure" who the author is. The `A.` is the authoritative output. Leave it alone.

3. **NEVER add middle initials, middle names, or honorifics** that the database did not return. Two initials is not three initials.

4. **NEVER abbreviate full names returned by the database** (the opposite direction). If the database returns `Mareike Augsburger`, do not abbreviate to `M. Augsburger` for visual consistency.

5. **NEVER reconcile conflicting name strings from different sources.** If Semantic Scholar says `A. Bach` and OpenAlex says `Aaron Kim Peter Bach`, do NOT merge, average, or pick. Present BOTH strings with their sources, and flag for manual inspection.

6. **NEVER trust a sub-agent's author strings without verifying via `fetch_paper_details`.** Sub-agents can hallucinate too. If a sub-agent returns author names, re-fetch the paper details directly before putting those names in the output.

7. **DOI metadata over gut feeling.** If DOI metadata says the author is Ruth Schmidt and you "know" it should be Albrecht Schmidt — the metadata is right and you are wrong. Never dismiss a metadata mismatch as a "database error."

8. **When in doubt, go online.** Fetch the actual paper page, the publisher landing page, the DOI resolver. Use every tool at your disposal to find the truth before inventing anything.

9. **Never silently resolve discrepancies.** Present what you found, what the sources say, and let the user make the final call.

10. **Never auto-correct author names, titles, or years.** Present both versions and ask.

## When the Metadata is Partial or Ambiguous — FLAG, DO NOT FILL

Any of these conditions require flagging for manual inspection rather than guessing:

- The database returned only initials (e.g., `A. Bach`, `N. van Berkel`) and you want to know a full name
- Two sources disagree on an author's name spelling or form
- The venue field is `"Not available"` or missing
- The year is missing or reported inconsistently across sources
- A sub-agent returned names that differ from what `fetch_paper_details` returns
- A field contains characters that look encoding-mangled (e.g., `cSerban` for `Šerban`)

**How to flag in HTML output:** use a visible marker like `⚠ MANUAL CHECK` next to the affected field, with a one-line note explaining what is ambiguous. Example:

```html
Authors: A. Bach, T. M. Nørgaard, J. Brok, N. van Berkel
<span class="flag">⚠ MANUAL CHECK — initials only; verify full names against publisher page before citing.</span>
```

**How to flag in plain-text output:** include the marker `[MANUAL CHECK: reason]` immediately after the ambiguous field.

It is always acceptable to return LESS information than the user wants (initials, partial author list, "year unknown"). It is NEVER acceptable to return FABRICATED information.

## Pre-Output Checklist

Before emitting any citation or metadata to the user, verify:

- [ ] Every author name appears exactly as in a `fetch_paper_details` response (or exactly as in the original `search_papers` response if no fetch was done).
- [ ] No given name has been expanded from an initial.
- [ ] No full name has been abbreviated to an initial.
- [ ] No author has been added, removed, or reordered.
- [ ] The title is a verbatim copy-paste (no corrections of capitalization, punctuation, or typos).
- [ ] The year, venue, and DOI match the tool response.
- [ ] Any ambiguity is marked with `⚠ MANUAL CHECK` or `[MANUAL CHECK: reason]` rather than silently resolved.
- [ ] If a sub-agent supplied citation data, its author strings have been re-verified via `fetch_paper_details`.

## The Underlying Principle

**The user is always the final authority on citation accuracy. Your job is to surface what the databases actually said, not to produce a polished final citation.** A verbatim-but-ugly citation is always better than a polished-but-fabricated one.
