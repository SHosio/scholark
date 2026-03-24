# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Scholark is a Claude Code plugin for HCI researchers. It provides research design skills and specialized agents. The plugin is independent of but designed to pair with [Scholark-1](https://github.com/SHosio/scholark-1), a separate MCP server for academic literature search.

**Platform**: Claude Code plugin (no build system, no tests, no compilation). The plugin is declarative — markdown definitions and JSON config.

## Architecture

### Two-Agent System
- **research-ideator** (`agents/research-ideator.md`): Creative idea generation using web search + academic search. Runs on Sonnet.
- **research-critic** (`agents/research-critic.md`): Adversarial reviewer using academic search only (web search deliberately disabled via `disallowedTools`). Runs on Sonnet.

The `research-brainstorm` skill dispatches both agents in parallel and synthesizes their outputs.

### Five Skills (sequential workflow)
1. **research-brainstorm** — Coordinates both agents, produces ranked ideas with risk assessment
2. **study-design** — Conversational study design formalization (IVs, DVs, design type, sampling, procedure)
3. **analysis-plan** — Pre-registration-ready statistical analysis specification
4. **study-validator** — Completeness checklist with severity-rated gaps
5. **literature-blind-spots** — Accepts .tex/.md/.pdf drafts, searches for citation gaps, outputs HTML report

### Scholark-1 Dependency
Scholark-1 MCP is a separate install configured per-project. Skills that need it (literature-blind-spots, research-brainstorm) check for its availability and guide the user to install it if missing. Skills that don't need it (study-design, analysis-plan, study-validator) work fully standalone.
