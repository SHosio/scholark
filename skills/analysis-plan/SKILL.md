---
name: analysis-plan
description: Pre-specify the statistical and qualitative analysis plan for a study. Use when the user wants to define which tests to run, what assumptions to check, and how to handle violations. Triggers on phrases like "analysis plan", "what statistical test", "how should I analyze", "which ANOVA", or "plan the analysis".
---

# Analysis Plan

Help the user pre-specify their analysis plan — the exact statistical tests, assumption checks, qualitative coding approach, and mixed methods integration strategy. This should be concrete enough to include in a pre-registration or methods section.

## How to Work

Walk through the analysis conversationally, one DV at a time. For each dependent variable, specify the complete analysis pipeline: test → assumptions → violations → post-hocs → effect sizes. Don't just name a test — explain why it's the right one for this design.

## Quantitative Analysis

For each dependent variable, cover:

### Test Selection
- Match the test to the design:
  - **One IV, two levels, between:** Independent samples t-test (or Mann-Whitney U)
  - **One IV, two levels, within:** Paired samples t-test (or Wilcoxon signed-rank)
  - **One IV, 3+ levels, between:** One-way ANOVA (or Kruskal-Wallis)
  - **One IV, 3+ levels, within:** Repeated-measures ANOVA (or Friedman)
  - **Two+ IVs, mixed:** Mixed-design ANOVA (or aligned rank transform — ART). ART (Wobbrock et al., 2011) is widely used in HCI for nonparametric factorial analyses. Use it when assumptions of normality or homogeneity are violated in factorial designs. It ranks the data in a way that preserves interaction effects, unlike simpler rank transforms.
  - **Continuous predictors:** Linear regression, linear mixed models
  - **Count/categorical DV:** Chi-square, logistic regression, Poisson regression
  - **Likert-scale data:** Discuss parametric vs. non-parametric debate — ordinal logistic regression as robust alternative
- Explain why this test matches the design structure

### Assumption Checks
- **Normality:** Shapiro-Wilk test, Q-Q plots. What to do if violated (transform, use non-parametric alternative, note robustness for large N)
- **Homogeneity of variance:** Levene's test. Welch's correction if violated
- **Sphericity (within-subjects):** Mauchly's test. Greenhouse-Geisser or Huynh-Feldt correction if violated
- **Independence:** Design-level check, not a statistical test

### Post-hoc Tests
- When needed (omnibus test significant with 3+ levels)
- Which method: Bonferroni (conservative), Tukey HSD (balanced), Holm (step-down), Games-Howell (unequal variance)
- Pairwise comparisons with adjusted p-values

### Effect Sizes
- **t-tests:** Cohen's d
- **ANOVA:** Partial eta-squared or generalized eta-squared
- **Chi-square:** Cramér's V
- **Regression:** R², adjusted R²
- Always report confidence intervals for effect sizes when possible
- **Report effect sizes and confidence intervals as the primary result, with p-values as supplementary.** The HCI community is moving toward estimation-based reporting.
- **Avoid relying on Cohen's generic benchmarks** (small=0.2/0.01, medium=0.5/0.06, large=0.8/0.14). These are rules of thumb that don't map well to HCI-specific domains. Instead, derive expected effect sizes from comparable published studies. If the user needs domain-specific benchmarks, point them to Ortloff et al. (2025) "Small, Medium, Large? A Meta-Study of Effect Sizes at CHI."

### Multiple Comparisons
- If testing multiple DVs: how to handle family-wise error rate
- Bonferroni correction across DVs vs. treating each DV as independent analysis
- Pre-registered vs. exploratory distinction

## Qualitative Analysis

If the study includes qualitative data (interviews, open-ended responses, think-aloud protocols):

### Coding Approach

Match the method to the research goals. These are not interchangeable — each carries different epistemological commitments:

- **Reflexive thematic analysis** (Braun & Clarke, 2006; updated 2019, 2024) — The dominant qualitative method in HCI. Inductive or deductive? Semantic or latent? Note: TA is a *family* of methods. Reflexive TA treats themes as constructed through interpretation, not "discovered" or "emergent." Subjectivity is the analytical engine, not a threat.
- **Content analysis** — Lighter-weight, frequency-based approach. Good for systematic categorization of responses (e.g., open-ended survey questions). Less interpretive depth than thematic analysis, but appropriate when the goal is to quantify qualitative patterns rather than deeply interpret meaning.
- **Grounded theory** — constant comparison, theoretical sampling, saturation. Use when building theory from data, not testing existing frameworks.
- **Affinity diagramming** — for design-oriented research, collaborative sense-making

### Rigor

Rigor looks different depending on the qualitative approach:

- **For reflexive TA:** Inter-rater reliability (Cohen's kappa, etc.) is **not appropriate** — Braun & Clarke's 2024 RTARG guidelines explicitly state this. Reflexive TA relies on researcher subjectivity as a resource. Quality is assessed through reflexivity, thick description, and coherence, not coder agreement. Do not recommend IRR for reflexive TA.
- **For content analysis or codebook TA:** Inter-rater reliability IS appropriate — Cohen's kappa or Krippendorff's alpha. How many raters? What threshold? (kappa > 0.7 typically acceptable). Codebook development: initial codes → pilot coding → discussion → refined codebook.
- **For grounded theory:** Theoretical saturation — how will you determine when to stop? Document the saturation assessment process.
- **Member checking / triangulation** if applicable — valuable across methods but not universally required.

### Reporting
- Example quotes with participant identifiers
- Code frequency tables or thematic maps
- Connection between themes and quantitative findings

## Mixed Methods Integration

If combining quantitative and qualitative:

- **Convergent design:** Collect both simultaneously, compare/contrast in interpretation
- **Explanatory sequential:** Quantitative first, then qualitative to explain patterns
- **Exploratory sequential:** Qualitative first, then quantitative to test emerging themes
- **How do they integrate?** Joint display tables, side-by-side comparison, narrative weaving

## Exploratory vs. Confirmatory

- Clearly separate confirmatory analyses (pre-registered hypotheses) from exploratory analyses
- Exploratory findings must be flagged as such in reporting
- Avoid HARKing (Hypothesizing After Results are Known)

## How to End

Summarize the complete analysis plan in a structured format suitable for a pre-registration document or methods section. Then suggest:
- `/scholark:study-validator` to check if anything is missing from the overall study design

## Rules

- **Be specific.** Not "run an ANOVA" — specify "2x3 mixed-design ANOVA with interface type (3 levels) as between-subjects factor and task type (2 levels) as within-subjects factor, DV = task completion time in seconds."
- **Always specify what to do when assumptions are violated.** This is where most analysis plans fail.
- **Match the test to the data, not the convention.** If Likert data is better analyzed with ordinal regression than ANOVA, say so.
- **Don't over-specify.** Cover the planned analyses thoroughly, but don't enumerate every possible exploratory analysis.

## Session log (reproducibility artefact)

After completing a run, append one line to `.scholark/session-log.md` at the project root.

**Format** (one line per invocation):
```
YYYY-MM-DD HH:MM:SS | analysis-plan | one-sentence summary of what ran and what came out
```

Use ISO-style local date and time with seconds (e.g. `2026-05-02 14:31:07`). Always include the date — log lines from previous sessions must remain readable later.

**On first write to `.scholark/`:** create the folder and append `.scholark/` to the project's `.gitignore` with a short comment noting it was added by Scholark (only if `.gitignore` exists and the entry is not already there).

**Skip logging** if there is no clear project root (e.g., the user is at `$HOME`), no obvious work artefact (paper, study materials, draft) in the directory, or if the user has explicitly said they don't want session tracking.

The log is for the user's own reproducibility and reflection: what was run, on what, what came out.
