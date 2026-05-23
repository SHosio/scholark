---
generated: {{ISO_DATE}}
manuscript: {{manuscript_path}}
paper_count: {{N_papers}}
---

# Publications Context Map ({{manuscript_filename}})

One entry per cited paper. The map is built from full-paper agent reads (the same reads that produced the citation audit). It does not replace the audit; future audit runs ignore the map and re-read the source each time.

Cluster ordering is suggestive, not enforced. Use H2 cluster dividers if the paper has more than roughly 10 cited works.

---

## {{Cluster label, optional}}

*One-line cluster intro framing the role these papers play in the manuscript.*

# `{{citekey}}`. {{Title}} ({{Year}})

## Summary
2-3 sentences faithfully describing what the paper is and does. Concrete numbers (sample size, F1 score, hierarchy depth, etc.) when they exist.

## Why cited here
2-4 sentences mapping the paper to the manuscript's argument. Tie to the manuscript's central framing (pillars, claims, design choices) where possible.

## Adjacent angles (optional)
1-2 sentences naming under-used aspects of the paper that the manuscript could draw on. Skip this section if no obvious unused angles surface.

---

(repeat per paper)

---

## Cross-cluster connections (optional appendix)

Threads worth following through the manuscript. Each thread names 2 to 4 papers using [[wikilink]] syntax (the citekey, without backticks) so the entries can be cross-navigated.

## What this manuscript deliberately does NOT claim (optional appendix)

Useful for keeping the discussion tight and pre-empting reviewer overreach. Examples:

- "We do not claim that BCTO is conformant with our merge/split. We claim BCTO supplies the principles we adapt."
- "We do not claim that Condition 3 improves wellbeing. We claim it changes the legibility of the practice description."
