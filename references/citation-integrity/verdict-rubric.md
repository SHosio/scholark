# Verdict rubric

Six categories the `citation-integrity` audit uses for every claim-occurrence. Five are returned by the `citation-verifier` agent (Verified / Partial / Misleading / Wrong / Unverifiable). The sixth (Not audited) is assigned by the orchestrator when the user has chosen to proceed without a local source markdown for a given citekey.

Calibrated against failure modes observed across real HCI manuscripts. When the agent is torn between two verdicts, it should prefer the more severe one. Flagging a false positive is recoverable; silently letting a misleading citation through is not.

## Verified

The source paper directly supports the manuscript's claim. The wording either paraphrases or accurately summarises something the paper says or shows. Numbers, labels, and scope qualifiers all match.

**Example.** Manuscript: "Li et al. introduced the stage-based model of personal informatics systems." Source paper opens with: "we derived a stage-based model of personal informatics systems composed of five stages (preparation, collection, integration, reflection, and action)." Verdict: Verified.

## Partial

The gist is right but a detail is off. Most common detail-level slips:

- A rounded number is rounded the wrong way ("$120 billion" when the paper says $119.0 billion is fine; "$130 billion" is partial).
- A label is mis-named ("item 8: dose, frequency" when item 8 is actually "when and how much").
- The scope is broader or narrower than the paper's ("ML extraction of BCTs" when the paper extracted 70 entity types of which BCTs were one).
- A scare-quoted phrase is the manuscript's paraphrase rather than the paper's words.

Authors can usually fix Partial verdicts with a tight rewording. Flag them, but rank them below Misleading and Wrong.

## Misleading

The citation distorts what the paper actually says, even when no individual fact is technically wrong. The reader is led to believe the cited source supports a claim it does not actually make. Common patterns:

- Citing a **protocol paper** as if it reported empirical results. Example: citing Michie 2017 (a 2017 HBCP protocol) for "applied AI to extract BCTs at scale", when the application is described in future tense.
- Citing a **probe study** as if it demonstrated efficacy. Example: citing Bhattacharjee 2024 (a qualitative tech probe) with "demonstrating that targeted AI follow-up questions can help people refine plans".
- Attributing the manuscript's **own synthesis** to a source that does not make that claim. Example: "TIDieR converges on three core axes" when TIDieR has 12 items and never privileges these three.
- **Co-citing a position paper** alongside an empirical paper for an empirical claim. Example: citing Yang 2020 (a synthesis paper) alongside Dhillon 2024 for "scaffolding drives co-writing effect", when Yang 2020 has no co-writing data.
- Using a paper's **title quote** as if it were a body finding. Example: "Hwang found that people want output to be '80% me, 20% AI'" when the phrase appears only in the title and is not a quantified body claim.

Misleading verdicts are the highest-yield to fix because they survive reviewer scrutiny much less well than Partial ones.

## Wrong

The source paper does not support the claim at all. Either:

- The paper makes the opposite claim (e.g. manuscript: "BCTO uses mechanism of action as the merge/split basis"; paper: "BCTs were not generally defined in terms of their potential mechanisms of action").
- The author confused this citation with a different one and the cited paper has nothing to do with the topic.

Wrong is rare but always load-bearing. Reviewers who know the cited paper will spot Wrong instantly. Fix first.

## Unverifiable

The claim is about something the source paper cannot in principle answer. The canonical case is an external citation count ("cited over 8,000 times"); the paper itself does not know how many times it has been cited, so no amount of reading can confirm the claim. The audit notes this as Unverifiable-from-paper and suggests the author either drop the meta-claim or footnote it with a date-stamped lookup.

Unverifiable differs from "we could not open the source". The source-missing case has its own label (`Not audited`) so the two outcomes have distinct fixes: drop or footnote the meta-claim, versus obtain the source and re-run.

Do not collapse Unverifiable into Wrong. The fixes are different.

## Not audited (source missing)

Assigned only when the user, in the coverage gate, has explicitly chosen to proceed without a local markdown for one or more cited papers. The orchestrator (not the verifier agent) assigns this label after the audit, with the citekey, occurrence count, and bibtex title.

This label is a structural acknowledgement that the audit's central contract did not hold for the entry. The label says nothing about whether the citation is correct; the citation may be perfectly fine. The fix is to obtain the source (institutional access, preprint, contact the authors) and re-run, or to drop the citation if it is not load-bearing.

In the audit report, Not audited entries appear in their own dedicated section after Verified, so the headline counts at the top distinguish them clearly from the audited categories.

## Calibration tips

- If the claim is "X et al. showed that P" and the paper *partly* shows P, prefer Partial.
- If the claim is "X et al. showed that P" and the paper *does not* show P, prefer Misleading or Wrong depending on whether the paper at least addresses P.
- If the claim uses a scare-quoted phrase, the phrase must appear verbatim in the paper for Verified. If it does not appear, the verdict is at least Partial.
- If the claim is empirically narrow (a number, a study size, a metric) and the paper's value is materially different, it is at least Partial. If the manuscript's number does not appear at all in the paper, it is Misleading.
- If the cited paper is a protocol or position piece and the claim is in past tense or describes an empirical result, default to Misleading and check whether a sibling paper (often by the same authors) is the proper citation.
