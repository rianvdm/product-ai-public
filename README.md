# Product AI Public

Curated prompts, commands, and agents for AI-assisted product management. A subset of my personal "second brain" repo, published for others to adapt.

## What's here

This is a curated subset of my personal AI-assisted product management toolkit. These prompts, context files, and commands work with Claude, ChatGPT, OpenCode, Cursor, or any LLM-based coding/writing assistant.

### OpenCode Commands & Agents

* [`.opencode/agent/blind-validator.md`](.opencode/agent/blind-validator.md) -- Independently re-fetches all sources cited in a draft (Jira tickets, GitLab files, wiki pages, doc URLs, MRs) and verifies that each exists and supports the claims made. Returns a structured verification report. Use as a validation step in any command that produces source-backed analysis.
* [`.opencode/agent/code-review.md`](.opencode/agent/code-review.md) -- Reviews code for bugs, security, and maintainability with tool-assisted validation
* [`.opencode/command/code-review.md`](.opencode/command/code-review.md) -- Review changes with parallel @code-review subagents
* [`.opencode/command/doc-review.md`](.opencode/command/doc-review.md) -- Review generated files for accuracy, completeness, and style using multi-agent validation
* [`.opencode/command/new-project.md`](.opencode/command/new-project.md) -- Scaffold a new project brain folder
* [`.opencode/command/session-end.md`](.opencode/command/session-end.md) -- Write a session handoff note before ending a substantive work session
* [`.opencode/command/session-start.md`](.opencode/command/session-start.md) -- Load recent session context and corrections at the start of a work session
* [`.opencode/skills/interactive-explainer/SKILL.md`](.opencode/skills/interactive-explainer/SKILL.md) -- Builds a self-contained interactive HTML visualisation that makes a process, algorithm, decision logic, or system visually and experientially understandable. Primary input is a linear walkthrough, but works directly from code, documents, or concept descriptions too — and can invoke the linear-walkthrough skill as an intermediate step if the source material lacks sufficient clarity or structure. Use when the user wants to "see how this works", wants an interactive version of a walkthrough, wants to explain a process visually to an audience, or asks to "visualise", "animate", or "build an interactive explanation" of anything. Richer and more interactive is always preferred, as long as it makes the logic clearer rather than decorating it.
* [`.opencode/skills/linear-walkthrough/SKILL.md`](.opencode/skills/linear-walkthrough/SKILL.md) -- Generates a linear, narrative walkthrough of source material — code, documents, architecture diagrams, meeting notes, Jira tickets, or any combination. Produces a step-by-step guide that explains logic, purpose, and connections between components in a readable sequence. Use when the user wants to understand how something works, wants to explain a system to others, asks to "walk through" or "explain" code or docs, or needs to document a system's logic for learning or onboarding. Also trigger when the user provides files or code and asks "how does this work?" or "take me through this.
* [`.opencode/skills/pm-thinking/SKILL.md`](.opencode/skills/pm-thinking/SKILL.md) -- Apply Rian's product management philosophy to all product-related tasks.

### Context Files

* [`01-context/avoid-ai-patterns.md`](01-context/avoid-ai-patterns.md) -- To keep writing natural and human, avoid these telltale AI patterns:
* [`01-context/product-philosophy.md`](01-context/product-philosophy.md) -- In this document I try to articulate something that can be notoriously hard to pin down: how I think about product work.
* [`01-context/project-template.md`](01-context/project-template.md) -- Use this template to create a dedicated "project brain" folder for major initiatives.

### Prompts

* [`02-prompts/dev/brainstorming-planning.md`](02-prompts/dev/brainstorming-planning.md) -- Build ideas from scratch through guided discovery, then produce developer-ready specs and implementation prompts.
* [`02-prompts/pm/debate-product-idea.md`](02-prompts/pm/debate-product-idea.md) -- You are a simulator for a high-stakes product strategy debate.
* [`02-prompts/pm/draft-review-prd.md`](02-prompts/pm/draft-review-prd.md) -- These instructions enable LLMs to help users create clear, outcome-focused Product Requirements Documents (PRDs) for ...
* [`02-prompts/pm/review-okrs.md`](02-prompts/pm/review-okrs.md) -- These instructions enable LLMs to help users create clear, outcome-focused OKRs for product and platform teams (DevTo...
* [`02-prompts/pm/review-spec.md`](02-prompts/pm/review-spec.md) -- Review engineering specification documents (SPECs/FSPECs) to ensure they faithfully translate product requirements in...

### 04-Docs

* [`04-docs/cross-session-memory.md`](04-docs/cross-session-memory.md) -- This system gives the agent continuity between sessions without requiring automated extraction tools, vector database...

## How to use these

Most of these files are **system prompts** or **prompt templates** you can paste into any LLM conversation. Some are designed for specific tools:

* **`01-context/`** files work well as persistent context (system prompts, custom instructions, or project knowledge files)
* **`02-prompts/`** files are task-specific prompts you paste when needed
* **`.opencode/command/`** files are [OpenCode](https://opencode.ai) slash commands (but the prompt content works anywhere)

## Adapting to your context

These prompts reference a few personal conventions you'll want to adapt:

* References to `01-context/*.md` files point to personal context documents (writing style, philosophy, etc.). Create your own equivalents.
* Some prompts mention MCP servers or tool integrations. Replace with whatever tools you use.
* The writing style and product philosophy reflect my preferences. Adjust to match yours.

## About

I'm [Rian van der Merwe](https://elezea.com), a product manager who uses AI tools extensively in my daily work. This repo contains the prompts and context files I've found most useful, published so others can adapt them.

For more on my approach to product management and AI, see [`01-context/product-philosophy.md`](01-context/product-philosophy.md).

## License

MIT. Use these however you like.
