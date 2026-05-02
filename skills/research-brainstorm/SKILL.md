---
name: research-brainstorm
description: Brainstorm research ideas from multiple angles using divergent ideation and rigorous critique. Use when the user has a research question or idea they want to explore, wants research direction suggestions, or says things like "I'm thinking about studying...", "what could we research about...", or "brainstorm ideas for..."
---

# Research Brainstorm

> **Best with [Scholark-1](https://github.com/SHosio/scholark-1) MCP.** Before dispatching agents, check if scholark-1 tools are available in this session. If not, tell the user: "This skill works best with the Scholark-1 MCP server for academic literature search. The agents can still brainstorm using web search, but for grounded academic critique, install Scholark-1 from https://github.com/SHosio/scholark-1 and add it to your project's `.mcp.json`." Then continue — the skill still works, but the critic agent will be limited.

Help the user explore a research question from multiple angles by generating divergent ideas and subjecting them to rigorous critique, then converging on the 2-3 strongest options.

## Step 1: Understand the Research Question

Ask the user to describe:
- Their research idea or question
- Any constraints (timeline, available participants, equipment, target venue)
- What they already know or have tried
- Whether they're open to any direction or have a specific angle in mind

Keep this conversational — one or two questions, not an interrogation.

## Step 2: Dispatch Agents

Once you understand the research question, launch **both agents in parallel** using the Agent tool:

1. **research-ideator** — Give it the user's research question and constraints. Ask it to generate 5-7 diverse ideas from different angles (technological, societal, cross-disciplinary, contrarian, methodological), grounded in current trends and adjacent academic work.

2. **research-critic** — Give it the same research question. Ask it to evaluate the core idea for validity threats, existing competing work, and methodological pitfalls. Have it search for related published work that the user should know about.

Launch both in the same message so they run in parallel.

## Step 3: Synthesize

When both agents return, present their outputs to the user in a synthesized format:

1. **The Ideas** — Present the ideator's ideas, but annotated with any relevant critiques. If the critic found existing work that overlaps with an idea, note it. If a critique applies to a specific idea, pair them.

2. **The Challenges** — Present the critic's cross-cutting concerns that apply to the research area as a whole, not just individual ideas.

3. **Contribution Type Mapping** — For each promising direction, explain which HCI contribution type(s) it most naturally aligns with (empirical, artifact, methodological, theoretical, dataset, survey, opinion, replication — per Wobbrock & Kientz, 2016) and why. Be honest: if an idea doesn't map cleanly to established types, say so — that's useful for the user to know. If the idea combines types (e.g., artifact + empirical), explain how the parts fit together. The user ultimately decides how to frame their contribution, but your job is to make the options visible.

4. **Top 2-3 Options** — Converge on the strongest study design options. For each:
   - What you'd study (research question)
   - How you'd study it (brief method sketch)
   - Why it's strong (what makes this compelling)
   - Contribution framing (which contribution type(s) and how the method supports that framing)
   - Key risk (the biggest validity threat to address)
   - Your recommendation on which option is strongest and why

## Step 4: Iterate

Stay conversational. The user may want to:
- Drill deeper into one option
- Combine elements from different ideas
- Ask for more ideas in a specific direction
- Challenge your recommendation
- Move on to study design (suggest `/scholark:study-design` when they're ready)

## Rules

- Don't present agent outputs as raw dumps. Synthesize them into a coherent narrative.
- Be opinionated — recommend your top pick and explain why.
- If the user's original idea has a serious flaw, say so directly but constructively.
- When the user is ready to formalize their choice, suggest moving to `/scholark:study-design`.

## Session log (reproducibility artefact)

After completing a run, append one line to `.scholark/session-log.md` at the project root.

**Format** (one line per invocation):
```
YYYY-MM-DD HH:MM:SS | research-brainstorm | one-sentence summary of what ran and what came out
```

Use ISO-style local date and time with seconds (e.g. `2026-05-02 14:31:07`). Always include the date — log lines from previous sessions must remain readable later.

**On first write to `.scholark/`:** create the folder and append `.scholark/` to the project's `.gitignore` with a short comment noting it was added by Scholark (only if `.gitignore` exists and the entry is not already there).

**Skip logging** if there is no clear project root (e.g., the user is at `$HOME`), no obvious work artefact (paper, study materials, draft) in the directory, or if the user has explicitly said they don't want session tracking.

The log is for the user's own reproducibility and reflection: what was run, on what, what came out.
