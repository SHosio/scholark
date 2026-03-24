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

3. **Top 2-3 Options** — Converge on the strongest study design options. For each:
   - What you'd study (research question)
   - How you'd study it (brief method sketch)
   - Why it's strong (what makes this compelling)
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
