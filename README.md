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
- `/scholark:prose-tighten` — Tighten `.tex` prose without losing field-specific terminology. Splits long sentences, cuts fluff, fixes nominalizations. Asks before touching technical terms

### What works without Scholark-1

The **study-design**, **analysis-plan**, and **study-validator** skills work fully on their own — no MCP needed.

The **research-brainstorm** and **paper-review** skills work partially: brainstorm's critic agent loses its ability to ground critiques in published work, and paper-review can't verify claims against literature.

The **literature-blind-spots** skill requires Scholark-1 — it cannot run without it.

## Install

### 1. Install the plugin

Clone the repo and load it with the `--plugin-dir` flag:

```bash
git clone https://github.com/SHosio/scholark.git
claude --plugin-dir ./scholark
```

This loads the plugin for your session. Use an absolute path to load it from any directory:

```bash
claude --plugin-dir /path/to/scholark
```

Skills are namespaced under `scholark:` (e.g., `/scholark:research-brainstorm`).

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

## Writing Style

To set the register (formal vs. conversational, hedge level, audience), add a line to your project's `CLAUDE.md`:

```
Academic paper targeting CHI 2026. Formal but not stiff. Hedge claims appropriately.
```

If you ask Claude to read your draft, it will naturally calibrate to your voice. The `CLAUDE.md` line ensures the right register even in sessions where your paper isn't loaded.

For mechanical prose tightening — splitting long sentences, cutting fluff, fixing nominalizations — use the `prose-tighten` skill. It is `.tex` only and leaves field-specific terminology alone (asks you when uncertain).

Want more control? Edit `CLAUDE.md` with as much or as little style guidance as you like — or add another writing skill to the plugin yourself. That's the beauty of Claude Code: everything is a markdown file you own.

## Workflow

A typical session flows through the skills in order:

1. **Brainstorm** — Start with an idea, get divergent perspectives, narrow to 2-3 options
2. **Design** — Formalize the chosen option into a complete study design
3. **Analysis** — Pre-specify the analysis plan for each dependent variable
4. **Validate** — Run a completeness check before piloting
5. **Tighten** — When you have a draft, run `prose-tighten` on the `.tex` to clean up sentence-level prose without touching your terminology
6. **Review** — Run `paper-review` on the tightened draft to catch structural issues reviewers will flag
7. **You** — Read the output. Apply judgment. Decide what stays, what goes, and what needs rethinking. AI can generate options at scale — but taste, conviction, and knowing when something *feels wrong* are yours alone. That's not a limitation of the tool. That's the point.

The literature blind spots skill works independently — point it at a draft paper anytime.

## Citation Accuracy Warning

The citation and literature tools are designed to remove the grunt work — cleaning up BibTeX files, finding DOIs, tracking down missing references. They are not designed to replace reading the papers you cite. If you are doing your job as a researcher and actually engaging with the work you reference, you will catch most errors naturally.

That said: LLMs hallucinate references. A particularly insidious failure mode is Claude "recognizing" a famous researcher's name and substituting it for the actual author, then dismissing correct metadata as a database error. The skills now explicitly instruct Claude to verify online and flag discrepancies to you rather than silently guessing — but no safeguard is foolproof. Verify what you cite.

## Requirements

- [Claude Code](https://claude.ai/code) with plugin support
- [Scholark-1](https://github.com/SHosio/scholark-1) for literature search features (recommended, not required)

## Philosophy

The skills in this plugin are grounded in established HCI methodology — contribution type frameworks (Wobbrock & Kientz, 2016), current CHI reviewing standards, reflexive thematic analysis (Braun & Clarke), estimation-based statistical reporting, and open science practices. On top of that foundation, the current version reflects the personal opinions and reviewing experience of [Dr. Simo Hosio](https://github.com/SHosio). It is opinionated by design.

**You should adapt it.** Fork the repo, use the skills on your own work, and when something doesn't fit your field or your perspective — tell Claude to change it. The skills are markdown files. Every disagreement is a chance to encode your own expertise. Over time, the plugin becomes a living reflection of your methodology standards.

## A Note on Ethics and Integrity

This tool can write. It can draft paragraphs, formulate arguments, and produce text that reads like a competent academic paper. That is precisely what makes it dangerous if used thoughtlessly.

**The purpose of academic work is not to produce papers. It is to develop thinking.** The reasoning, the struggle with a messy literature, the slow refinement of an argument — that is the work. A paper is just the artifact that comes out the other end. If you outsource the thinking to an AI and rubber-stamp the output, you are not doing research. You are generating documents. The work will be hollow, and so will your development as a scholar.

AI-assisted science is genuinely exciting. Using these tools to pressure-test your ideas, explore methodological alternatives, catch blind spots, or accelerate tedious structural work is legitimate and powerful. But there is a bright line between *augmenting your thinking* and *replacing it*. You must stay on the right side of that line, and you must be honest with yourself about which side you are on.

**Before using Scholark's writing capabilities, know the rules:**

- **Your venue's policy.** ACM, IEEE, and other publishers have explicit and evolving policies on AI-generated content in submissions. Read them. They differ, and they change.
- **Your institution's policy.** Universities and research groups increasingly have their own guidelines on AI use in academic work. Follow them.
- **Your own ethical standards.** No policy can substitute for your own judgment. If you cannot defend how you used the tool to a colleague, to a reviewer, or to yourself — you should not have used it that way.

The future of AI in research is still being written. Be part of shaping it responsibly, not part of the cautionary tales.

The author assumes no responsibility for how these tools are used. You are solely accountable for the integrity and ethics of your own research.

## Workshops

Dr. Simo Hosio is available for hire to give workshops on Claude Code for academic work — from installing and using these tools to forking and customizing them for your own field. [Get in touch.](https://simohosio.com)

## License

MIT
