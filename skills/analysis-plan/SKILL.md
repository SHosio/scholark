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
  - **Two+ IVs, mixed:** Mixed-design ANOVA (or aligned rank transform)
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
- **t-tests:** Cohen's d (small=0.2, medium=0.5, large=0.8)
- **ANOVA:** Partial eta-squared (small=0.01, medium=0.06, large=0.14) or generalized eta-squared
- **Chi-square:** Cramér's V
- **Regression:** R², adjusted R²
- Always report confidence intervals for effect sizes when possible

### Multiple Comparisons
- If testing multiple DVs: how to handle family-wise error rate
- Bonferroni correction across DVs vs. treating each DV as independent analysis
- Pre-registered vs. exploratory distinction

## Qualitative Analysis

If the study includes qualitative data (interviews, open-ended responses, think-aloud protocols):

### Coding Approach
- **Thematic analysis** (Braun & Clarke) — inductive or deductive? Semantic or latent?
- **Grounded theory** — constant comparison, theoretical sampling, saturation
- **Content analysis** — frequency-based, category development
- **Affinity diagramming** — for design-oriented research

### Rigor
- **Inter-rater reliability:** Cohen's kappa or Krippendorff's alpha. How many raters? What threshold? (kappa > 0.7 typically acceptable)
- **Codebook development:** Initial codes → pilot coding → discussion → refined codebook
- **Saturation:** How will you determine when to stop? Data-driven saturation assessment
- **Member checking / triangulation** if applicable

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
