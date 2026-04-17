---
name: paper-review
description: Review an HCI paper draft for common rejection patterns before submission. Accepts .tex, .md, or .pdf files. Use when the user says "review my paper", "what would reviewers say", "check my draft", "is this ready to submit", or "pre-submission review".
---

# Paper Review

Review an HCI paper draft against the most common reasons papers get rejected from top venues (CHI, CSCW, UIST, DIS, TOCHI, IJHCS). This is not copyediting — it is a structural and argumentative review focused on the issues that sink papers in peer review.

> **Works best with [Scholark-1](https://github.com/SHosio/scholark-1) MCP.** If scholark-1 tools are available, the review can verify claims against published literature. If not, the review focuses on structural and argumentative issues. Check for scholark-1 availability and inform the user either way.

## Step 1: Read the Paper

Read the user's draft file (.tex, .md, or .pdf). Read it fully before making any judgments. Map the paper's structure: introduction, related work, methods, results, discussion, conclusion.

## Step 2: Review Against Common Rejection Patterns

Check each of the following. For every issue found, be specific — quote the problematic passage or point to the exact section. Don't flag issues that aren't there.

### Contribution Clarity

- **Is the contribution stated sharply in the introduction?** Not buried, not vague, not just "we present a study of X." Can you state the contribution in one sentence after reading the intro? If you can't, a reviewer can't.
- **What type of contribution is this?** (empirical, artifact, methodological, theoretical, dataset, survey, opinion, replication). Is the paper clear about this? Papers that don't know what they are get rejected.
- **Is the contribution proportional to the paper length?** A thin contribution stretched across many pages is a top rejection reason (CHI ADR-Contribution).
- **Why now?** Does the introduction establish timeliness — why this research matters at this moment? If missing, reviewers assume the work repeats what's known.

### Delta to Prior Art

- **Is the gap between this work and prior art explicitly stated?** Not implied, not left for the reader to infer. The paper should say clearly: "Prior work has done X, but not Y. We do Y."
- **Is the related work engaged with critically, or just listed?** A related work section that merely summarizes prior papers without analyzing how they relate to, contrast with, or build upon each other is a red flag.
- **Does the paper cite its own prior work transparently?** Failing to position one's own closely related publications is a desk rejection criterion.

### Research Questions and Answers

- **Are research questions clearly stated?** Where in the paper?
- **Are the research questions actually answered?** Go through each RQ and check whether the results and discussion explicitly address it. This is one of the most common reviewer complaints — RQs set up in the introduction that are never clearly resolved.
- **Do the answers match the RQs?** If RQ1 asks "how do users perceive X?" but the results only report task completion times, there's a mismatch.

### Claims-Evidence Alignment

- **Do claims match what was actually measured?** If the paper claims the system "improved learning" but only measured engagement or preference, that's overclaiming. Claims must be precisely calibrated to what the evaluation measured.
- **Are qualitative findings generalized beyond their scope?** E.g., treating 12 interviews as representative of a population.
- **Are there internal contradictions?** Results that conflict with each other within the paper, or interpretations that don't logically follow from the data.

### Methodology Transparency

- **Could another researcher replicate the study from this description?** Check for: counterbalancing details, recruitment procedures, exact measures used, analysis steps, task descriptions.
- **Are design rationale choices explained?** Not just what was designed, but why. Why these conditions? Why this measure? Why this population?
- **For qualitative work:** Is the analytical approach clearly described? 40% of thematic analyses at CHI don't describe theme generation at all. Is the method used consistently with its epistemological commitments? (E.g., don't claim reflexive TA and then report inter-rater reliability.)

### Discussion and Implications

- **Is the discussion substantive or formulaic?** A thin discussion that merely restates results is a rejection signal.
- **Are implications grounded in the paper's own findings?** This is critical — design implications that are not traceable to the empirical findings of this specific paper are a common and serious reviewer complaint. For each implication, check: does the data in this paper actually support this?
- **Are limitations genuine or checkbox?** Shallow limitations sections written to satisfy a perceived requirement rather than genuinely engaging with what the work cannot claim.
- **Does the paper address both technical and human/social dimensions?** Papers that solve only a technical problem without considering the human context get flagged in HCI.

### Literature Contextualization

- **Is the problem sufficiently contextualized?** Insufficient literature review is the #1 desk rejection reason at CHI (ADR-Context).
- **Are there obvious blind spots?** If scholark-1 is available, run targeted searches for key claims that seem under-cited. If not, flag areas where the literature coverage seems thin based on the claims being made.
- **Suggest `/scholark:literature-blind-spots` for a deep literature gap analysis** if issues are found here.

### Presentation

- **Are figures informative?** Figures with captions like "A screenshot" without explaining significance. Missing confidence intervals or error bars in quantitative figures. Missing axis labels or units.
- **Is the writing accessible to an international audience?** Regional colloquialisms, jargon, or overly complex sentence structures that exclude non-native English speakers.
- **First impressions:** Missing references, formatting issues, inconsistent terminology. These signal carelessness and color the entire review.

## Step 3: Report

Present the review in this structure:

### Strengths
What the paper does well. Be specific — this helps the user know what NOT to change. Reviewers note strengths too.

### Issues Found
For each issue:
```
**[Issue name]** (severity: likely reject / major revision / minor revision)
Where: [Section or page where the issue appears]
What: [Specific description of the problem — quote the paper if possible]
Why it matters: [What a reviewer would say about this]
How to fix: [Concrete, actionable suggestion]
```

Order by severity — likely reject issues first.

### Verdict
- Issues found: X (Y likely reject, Z major revision, W minor revision)
- **Overall assessment:** [Strong submission / Needs revision on N areas / Significant structural issues to address]
- **Biggest risk:** [The single issue most likely to cause rejection]

### Suggested Next Steps
Point to relevant skills:
- `/scholark:literature-blind-spots` if literature gaps were found
- `/scholark:study-validator` if methodology gaps were found
- `/scholark:analysis-plan` if analysis issues were found

## Rules

- **Read the whole paper before judging.** Don't flag something in the introduction that gets resolved later.
- **Be a constructive Reviewer 2.** Direct and honest, but every critique gets a concrete fix. The goal is to strengthen the paper, not tear it down.
- **Don't invent problems.** If a section is solid, say so and move on. Not every paper has every issue.
- **Quote the paper.** When flagging an issue, point to the specific passage. "The discussion is weak" is not useful. "The discussion restates that 'participants preferred condition A' but doesn't explain why or what this means for design" is useful.
- **Distinguish fixable from fatal.** A missing positionality statement is fixable. A fundamental confound in the study design is potentially fatal. Rate accordingly.
- **Don't flag style preferences.** This is not about your preferred writing style. Focus on issues that would cause rejection.
- **Ground your review in what top HCI venues actually expect.** Not generic academic writing advice.

## Citation Accuracy — CRITICAL

If the review touches references, author names, DOIs, or publication metadata, you MUST follow the scholark Citation Accuracy policy in full: see `../../CITATION-ACCURACY.md` (at the scholark plugin root).

Key rules that apply every time metadata is produced:

- **Copy metadata verbatim.** Never expand initials into given names. Never abbreviate full names into initials. Never merge conflicting strings from different sources.
- **Never trust your own knowledge of authors or titles.** Your training data will cause you to "recognize" famous researchers where they don't belong. This is hallucination.
- **DOI metadata over gut feeling.** If metadata contradicts your expectation, the metadata is right.
- **Flag, do not fill.** If a field is ambiguous, partial, or only returned as initials, mark it `⚠ MANUAL CHECK` with a one-line reason. Returning less information is always acceptable; fabricating information is never acceptable.
- **Re-verify any citation data supplied by a sub-agent** via `fetch_paper_details` before passing it through to the user.

Run the pre-output checklist in `CITATION-ACCURACY.md` before emitting the review.

**The user is always the final authority on citation accuracy.**
