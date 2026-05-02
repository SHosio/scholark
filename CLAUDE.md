# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Scholark is a Claude Code plugin for HCI researchers. It provides research design skills and specialized agents. The plugin is independent of but designed to pair with [Scholark-1](https://github.com/SHosio/scholark-1), a separate MCP server for academic literature search.

**Platform**: Claude Code plugin. Mostly declarative — markdown skill definitions and JSON config. One skill (`prose-tighten`) ships a small Python helper for the Flesch diagnostic; that helper has its own pytest suite under `skills/prose-tighten/scripts/`.

## Architecture

### Two-Agent System
- **research-ideator** (`agents/research-ideator.md`): Creative idea generation using web search + academic search. Runs on Sonnet.
- **research-critic** (`agents/research-critic.md`): Adversarial reviewer using academic search only (web search deliberately disabled via `disallowedTools`). Runs on Sonnet.

The `research-brainstorm` skill dispatches both agents in parallel and synthesizes their outputs.

### Seven Skills
1. **research-brainstorm** — Coordinates both agents, produces ranked ideas with risk assessment
2. **study-design** — Conversational study design formalization (IVs, DVs, design type, sampling, procedure)
3. **analysis-plan** — Pre-registration-ready statistical analysis specification
4. **study-validator** — Completeness checklist with severity-rated gaps
5. **literature-blind-spots** — Accepts .tex/.md/.pdf drafts, searches for citation gaps, outputs HTML report
6. **paper-review** — Pre-submission review against common rejection patterns at top HCI venues (CHI, CSCW, UIST, DIS, TOCHI, IJHCS)
7. **prose-tighten** — Tightens academic prose in `.tex` (split long sentences, cut fluff, fix nominalizations) without losing field-specific terminology. Reports a real Flesch diagnostic via `textstat`; never hallucinates scores.

### Scholark-1 Dependency
Scholark-1 MCP is a separate install configured per-project. Skills that need it (literature-blind-spots, research-brainstorm) check for its availability and guide the user to install it if missing. Skills that don't need it (study-design, analysis-plan, study-validator) work fully standalone.

### Sister project: Scholark-1

[Scholark-1](https://github.com/SHosio/scholark-1) lives at `/Users/simohosio/Code/personal/scholark-1` on this machine. It is an MCP server (Python, FastMCP) that searches Semantic Scholar, OpenAlex, Crossref, Europe PMC, and PubMed in parallel and returns deduplicated paper metadata. Scholark (this plugin) and Scholark-1 are designed to work together but install separately. Important file to know: `scholark-1/server.py` defines the MCP tools and their `instructions` block — it is the canonical place where Scholark-1's behavioural rules live (citation integrity, session logging, etc.).

### Session log convention (reproducibility)

Both Scholark-1 and this plugin maintain a per-project session log. Scholark-1 writes to `.scholark-1/session-log.md`; this plugin writes to `.scholark/session-log.md`. The two folders are separate by design — each tool owns its own folder.

For this plugin, every skill appends one line per invocation to `.scholark/session-log.md` in the project root, format:
```
YYYY-MM-DD HH:MM:SS | <skill-name> | one-sentence summary
```
The convention is encoded in each `SKILL.md` so end-user installations of the plugin honour it without depending on a CLAUDE.md file in the user's project. On first write, the skill creates `.scholark/` and adds it to the project's `.gitignore` (if one exists). Skips logging if there is no clear project root or the user has opted out.

`.scholark/` also holds skill-specific reports (e.g., `prose-tighten` writes `.scholark/reports/prose-tighten/<paper-stem>-<timestamp>.md`). Reports are detailed; the session log is a one-line timeline across all skill calls.
