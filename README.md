# Scholark

A Claude Code plugin for HCI researchers. Skills and agents that support the research workflow from ideation through manuscript finalization.

For full-powered academic literature search, pair with [Scholark-1](https://github.com/SHosio/scholark-1) — the MCP server that searches Semantic Scholar, OpenAlex, Crossref, and Europe PMC in parallel.

## What's Included

### Agents
- **research-ideator** — Creative, web-augmented agent that generates divergent research ideas from current trends, adjacent fields, and unconventional angles
- **research-critic** — Rigorous adversarial reviewer grounded in published literature and HCI methodology conventions

### Skills
- `/scholark:research-brainstorm` — Explore a research question from multiple angles using both agents, then converge on the 2-3 strongest options
- `/scholark:study-design` — Formalize a study design: variables, conditions, counterbalancing, participants, procedure
- `/scholark:analysis-plan` — Pre-specify statistical and qualitative analysis with assumption checks and violation handling
- `/scholark:study-validator` — Completeness checklist that flags missing elements reviewers would catch
- `/scholark:paper-review` — Pre-submission review against common rejection patterns at top HCI venues
- `/scholark:literature-blind-spots` — Analyze a draft paper for citation gaps and find real papers to fill them

### What works without Scholark-1

The **study-design**, **analysis-plan**, and **study-validator** skills work fully on their own — no MCP needed.

The **research-brainstorm** and **paper-review** skills work partially: brainstorm's critic agent loses its ability to ground critiques in published work, and paper-review can't verify claims against literature.

The **literature-blind-spots** skill requires Scholark-1 — it cannot run without it.

## Install

### 1. Install the plugin

```bash
git clone https://github.com/SHosio/scholark.git
claude plugin add ./scholark
```

This installs the plugin for your user (available in all projects). To install it for a single project only, run from that project's directory:

```bash
claude plugin add ./scholark --scope project
```

### 2. Install Scholark-1 (recommended)

To unleash the full power of brainstorming, critique, and literature blind spot analysis, install the [Scholark-1](https://github.com/SHosio/scholark-1) MCP server in your research project:

```bash
git clone https://github.com/SHosio/scholark-1.git
cd scholark-1
cp .env.example .env
# Edit .env with your API keys (optional — most tools work without them)
```

Then add it to your research project's `.mcp.json`:

```json
{
  "mcpServers": {
    "scholark-1": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/scholark-1", "scholark-1"]
    }
  }
}
```

### 3. Configure API keys (optional)

In your Scholark-1 `.env` file:

- `SEMANTIC_SCHOLAR_API_KEY` — Higher rate limits (free key from [semanticscholar.org](https://www.semanticscholar.org/product/api))
- `OPENALEX_EMAIL` — Polite pool priority (just your email, no signup)
- `UNPAYWALL_EMAIL` — Required only for open access PDF lookup (just your email)

## Workflow

A typical session flows through the skills in order:

1. **Brainstorm** — Start with an idea, get divergent perspectives, narrow to 2-3 options
2. **Design** — Formalize the chosen option into a complete study design
3. **Analysis** — Pre-specify the analysis plan for each dependent variable
4. **Validate** — Run a completeness check before piloting

The literature blind spots skill works independently — point it at a draft paper anytime.

## Requirements

- [Claude Code](https://claude.ai/code) with plugin support
- [Scholark-1](https://github.com/SHosio/scholark-1) for literature search features (recommended, not required)

## Philosophy

The skills in this plugin are grounded in established HCI methodology — contribution type frameworks (Wobbrock & Kientz, 2016), current CHI reviewing standards, reflexive thematic analysis (Braun & Clarke), estimation-based statistical reporting, and open science practices. On top of that foundation, the current version reflects the personal opinions and reviewing experience of [Dr. Simo Hosio](https://github.com/SHosio). It is opinionated by design.

**You should adapt it.** Fork the repo, use the skills on your own work, and when something doesn't fit your field or your perspective — tell Claude to change it. The skills are markdown files. Every disagreement is a chance to encode your own expertise. Over time, the plugin becomes a living reflection of your methodology standards.

## Workshops

Dr. Simo Hosio is available for hire to give workshops on Claude Code for academic work — from installing and using these tools to forking and customizing them for your own field. [Get in touch.](https://github.com/SHosio)

## License

MIT
