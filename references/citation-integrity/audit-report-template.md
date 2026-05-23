---
generated: {{ISO_DATE}}
auditor: one citation-verifier agent per citekey, each reading the full source paper before judging
manuscript: {{manuscript_path}}
context_folder: {{context_folder_path}}
citekeys_checked: {{N_citekeys}}
occurrence_pairs_checked: {{N_occurrences}}
verdict_scale: Verified | Partial | Misleading | Wrong | Unverifiable | Not audited (source missing)
---

# Inline citation audit ({{manuscript_filename}})

Headline counts: **{{N_wrong}} Wrong**, **{{N_misleading}} Misleading**, **{{N_partial}} Partial**, **{{N_verified}} Verified**, **{{N_unverifiable}} Unverifiable**, **{{N_not_audited}} Not audited (source missing)**.{{ + style notes line if any}}

Reading order below is by severity. Each entry quotes the manuscript line and gives the verifier's verdict, justification, and suggested fix.

## WRONG ({{N_wrong}}). The cited paper does not support the claim.

{{ for each wrong-verdict entry }}
### {{n}}. `{{citekey}}` at {{manuscript_basename}}:L{{line}}

> "{{exact_claim_sentence}}"

Justification: {{justification}}

**Fix:** "{{suggested_fix}}"

{{ /for }}

## MISLEADING ({{N_misleading}}). The framing distorts what the paper says.

{{ for each misleading-verdict entry }}
### {{n}}. `{{citekey}}` at {{manuscript_basename}}:L{{line}}

> "{{exact_claim_sentence}}"

Justification: {{justification}}

**Fix:** "{{suggested_fix}}"

{{ /for }}

## PARTIAL ({{N_partial}}). Gist is right but a detail is off.

{{ for each partial-verdict entry, in compact form (one block per entry) }}
### {{n}}. `{{citekey}}` at {{manuscript_basename}}:L{{line}}

> "{{exact_claim_sentence}}"

{{one-sentence justification}}. **Fix:** "{{suggested_fix}}"

{{ /for }}

## VERIFIED ({{N_verified}}). No correction needed.

{{ list as bullets, citekey + line + one-line description, no full entry blocks }}
- `{{citekey}}` L{{line}}: {{one-line description of what was verified}}
- ...

## UNVERIFIABLE ({{N_unverifiable}}). The claim is about something the paper cannot in principle answer.

{{ for each unverifiable entry }}
- `{{citekey}}` L{{line}}: {{reason, e.g. external citation count, meta-claim about citation impact}}.
{{ /for }}

## NOT AUDITED ({{N_not_audited}}). Source markdown was not available; the user chose to proceed without verification.

These citations were not checked against a source paper. They may be perfectly accurate; the audit makes no claim either way. The fix is to obtain the source and re-run the audit.

{{ for each not-audited entry }}
- `{{citekey}}` ({{N_occurrences}} occurrence(s), lines {{L1, L2, ...}}): {{bib_title}}.
{{ /for }}

## Cross-cutting observations

Patterns that recur across multiple citations and where one root-cause fix resolves several flagged claims at once. List 2 to 5 observations in order of impact. Examples of observation kinds:

- "Synthesis-as-source: in {{N}} citations we attribute our own decomposition/synthesis to the source rather than presenting it as ours."
- "Protocol-or-probe-as-finding: in {{N}} citations we describe protocol or probe papers as if they reported empirical results."
- "Co-cite contamination: in {{N}} citations a position paper is co-cited with an empirical paper for an empirical claim."
- "Title-quote-as-finding: a paper's title quote is described in body as a finding."

## Style notes (separate from citation accuracy)

{{ if any em-dashes or "not X, but Y" antithesis were observed in the manuscript prose during verification, list them here. Otherwise: "None observed during verification." }}

## Coverage

- Citekeys audited (had a local markdown in `<context-folder>/<citekey>.md`): {{N_covered}}.
- Citekeys not audited (source markdown was missing; user proceeded without): {{N_not_audited}}.
- Commented-out citations in the manuscript (excluded from extraction): {{N_commented}}.

## Next steps

Suggested fix order:

1. Fix Wrong first (load-bearing reviewer-spottable errors).
2. Fix Misleading next (same risk, slightly more interpretive).
3. Fix Partial last (low-risk wording polish).
4. Re-source or rephrase the Unverifiable claims.
5. Obtain sources for the Not audited entries and re-run, or drop those citations if not load-bearing.
