---
name: study-validator
description: Run a completeness check on a study design. Flags missing elements that reviewers would catch. Use when the user says "check my study design", "is anything missing", "validate this", "review my design", or "what would a reviewer say".
---

# Study Validator

Run a systematic completeness check on the user's study design. Flag what's missing, explain why it matters, and suggest how to address each gap.

## How to Work

Review the conversation history (or a provided document) for the current study design. Check each item below. For each gap found:

1. **Name the gap** — what's missing
2. **Explain why it matters** — what goes wrong without it (reviewer rejection, unreliable results, wasted time)
3. **Suggest how to fix it** — concrete, actionable steps

## Checklist

### Core Design
- [ ] **Research question(s)** — Is there a clear, specific RQ? Not just a topic area, but a testable question.
- [ ] **Hypotheses** — Are predictions stated? Directional or non-directional? If exploratory, is that stated?
- [ ] **IV specification** — All independent variables named with levels clearly defined.
- [ ] **DV specification** — All dependent variables named with exact measurement method.
- [ ] **Design type** — Between/within/mixed stated with rationale for the choice.

### Rigor
- [ ] **Counterbalancing** — For within-subjects: scheme specified (Latin square, full, randomized). N compatible with scheme.
- [ ] **Control/baseline condition** — What are participants compared against? Is it the right comparison?
- [ ] **Sample size justification** — Power analysis or other rationale. Expected effect size source cited.
- [ ] **Participant criteria** — Inclusion/exclusion criteria. Demographics to collect.
- [ ] **Task design** — Are tasks representative? Enough tasks to avoid ceiling/floor? Practice trials?

### Procedure
- [ ] **Session walkthrough** — Step-by-step procedure a research assistant could follow.
- [ ] **Training phase** — How are participants introduced to conditions? Equal training across conditions?
- [ ] **Data collection timing** — When are questionnaires administered? Pre/post/during?
- [ ] **Session duration** — Realistic? Fatigue a concern?

### Analysis
- [ ] **Analysis plan per DV** — Specific test named for each dependent variable.
- [ ] **Assumption checks** — What to check and what to do if violated.
- [ ] **Post-hoc strategy** — If using 3+ levels, which post-hoc correction?
- [ ] **Effect size measures** — Which ones and why.
- [ ] **Qualitative method** — If mixed methods: coding approach, inter-rater plan, saturation criteria.
- [ ] **Exploratory vs. confirmatory** — Clear distinction between pre-registered and exploratory analyses.

### Ethics & Reporting
- [ ] **Informed consent** — Procedure described.
- [ ] **Deception & debriefing** — If applicable, debriefing plan specified.
- [ ] **Data handling** — Anonymization, storage, retention policy.
- [ ] **Compensation** — Participant payment or credit.
- [ ] **Limitations** — Known threats to validity acknowledged.
- [ ] **Pilot study** — Plan for piloting before full data collection.

## Output Format

Present results in three sections:

### What's Solid
Briefly acknowledge the strong elements. Don't skip this — it helps the user know what NOT to change.

### Gaps Found
For each gap, use:
```
**[Gap name]** (severity: critical / important / minor)
Why it matters: [1-2 sentences]
How to fix: [Concrete suggestion]
```

Order by severity — critical first.

### Summary
- Total items checked: X
- Passed: X
- Gaps found: X (Y critical, Z important, W minor)
- Overall readiness: [Ready for piloting / Needs work on N areas / Major gaps to address]

## Rules

- **Check everything.** Don't skip items because they seem obvious.
- **Severity matters.** A missing pilot plan is minor. A confounded IV is critical. Rate accurately.
- **Don't invent problems.** If the design is solid on a dimension, say so and move on.
- **Be constructive.** Every gap gets a concrete suggestion, not just a flag.
- **Suggest next steps.** If gaps are found, point to which skill can help (e.g., "Use `/scholark:analysis-plan` to specify the missing analysis details").
