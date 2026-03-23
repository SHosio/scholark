# Scholark

A Claude Code plugin for HCI researchers. Bundles the [Scholark-1](https://github.com/SHosio/scholark-1) literature search MCP with research design skills and specialized agents.

## What's Included

### MCP Server (via Scholark-1)
- Search 4 academic databases in parallel (Semantic Scholar, OpenAlex, Crossref, Europe PMC)
- Fetch paper details, BibTeX, open access PDFs, citation context
- All results deduplicated by DOI with explicit source attribution

### Agents
- **research-ideator** — Creative, web-augmented agent that generates divergent research ideas from current trends, adjacent fields, and unconventional angles
- **research-critic** — Rigorous adversarial reviewer grounded in published literature and HCI methodology conventions

### Skills
- `/scholark:research-brainstorm` — Explore a research question from multiple angles using both agents, then converge on the 2-3 strongest options
- `/scholark:study-design` — Formalize a study design: variables, conditions, counterbalancing, participants, procedure
- `/scholark:analysis-plan` — Pre-specify statistical and qualitative analysis with assumption checks and violation handling
- `/scholark:study-validator` — Completeness checklist that flags missing elements reviewers would catch
- `/scholark:literature-blind-spots` — Analyze a draft paper for citation gaps and find real papers to fill them

## Install

```bash
# In Claude Code
/plugin install scholark
```

## Workflow

A typical session flows through the skills in order:

1. **Brainstorm** — Start with an idea, get divergent perspectives, narrow to 2-3 options
2. **Design** — Formalize the chosen option into a complete study design
3. **Analysis** — Pre-specify the analysis plan for each dependent variable
4. **Validate** — Run a completeness check before piloting

The literature blind spots skill works independently — point it at a draft paper anytime.

## Requirements

- [Claude Code](https://claude.ai/code) with plugin support
- [Scholark-1](https://github.com/SHosio/scholark-1) is installed automatically via the plugin's MCP configuration

## License

MIT
