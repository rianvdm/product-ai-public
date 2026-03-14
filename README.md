# Product AI Public

Curated prompts, commands, skills, and agents for AI-assisted product management. A subset of my personal "second brain" repo, published for others to adapt.

## What's here

These prompts, context files, and commands work with Claude, ChatGPT, OpenCode, Cursor, or any LLM-based coding/writing assistant.

### Context files

* [`product-philosophy.md`](01-context/product-philosophy.md) -- How I think about product work: problem-first, outcomes over outputs, empowered teams
* [`avoid-ai-patterns.md`](01-context/avoid-ai-patterns.md) -- Words, phrases, and structural patterns that make AI writing obvious
* [`project-template.md`](01-context/project-template.md) -- Template for creating a dedicated "project brain" folder for major initiatives
* [`stable-facts-template.md`](01-context/stable-facts-template.md) -- Template for the stable facts file used by cross-session memory

### Prompts

**Product management**

* [`draft-review-prd.md`](02-prompts/pm/draft-review-prd.md) -- Draft or review PRDs using a structured Product Opportunity Assessment framework
* [`review-okrs.md`](02-prompts/pm/review-okrs.md) -- Draft or review OKRs with outcome-over-output discipline and scoring rubrics
* [`debate-product-idea.md`](02-prompts/pm/debate-product-idea.md) -- Simulate a high-stakes product strategy debate with multiple perspectives
* [`review-spec.md`](02-prompts/pm/review-spec.md) -- Review engineering specs to ensure they faithfully translate product requirements

**Development**

* [`brainstorming-planning.md`](02-prompts/dev/brainstorming-planning.md) -- Build ideas through guided discovery, then produce developer-ready specs

### Skills

* [`pm-thinking`](.opencode/skills/pm-thinking/SKILL.md) -- Apply problem-first, outcome-focused product thinking to any product task
* [`interactive-explainer`](.opencode/skills/interactive-explainer/SKILL.md) -- Build self-contained interactive HTML visualizations of processes, algorithms, or systems
* [`linear-walkthrough`](.opencode/skills/linear-walkthrough/SKILL.md) -- Generate narrative walkthroughs of code, documents, or systems for learning and onboarding

### Agents

* [`code-review`](.opencode/agent/code-review.md) -- Evidence-based code review with tool-assisted validation and provability classification
* [`blind-validator`](.opencode/agent/blind-validator.md) -- Independently re-fetch and verify every source cited in a draft document

### Commands

* [`/code-review`](.opencode/command/code-review.md) -- Review changes using three parallel code-review agents, then validate with a fourth
* [`/meeting`](.opencode/command/meeting.md) -- Transform a meeting transcript into structured notes with decisions and action items
* [`/doc-review`](.opencode/command/doc-review.md) -- Review generated files for accuracy, completeness, and style
* [`/new-project`](.opencode/command/new-project.md) -- Scaffold a new project brain folder
* [`/session-start`](.opencode/command/session-start.md) -- Load recent session context and corrections at the start of a work session
* [`/session-end`](.opencode/command/session-end.md) -- Write a session handoff note before ending a work session

### Docs

* [`cross-session-memory.md`](04-docs/cross-session-memory.md) -- A three-layer memory system that gives AI agents continuity between sessions
* [`multi-agent-investigation.md`](04-docs/multi-agent-investigation.md) -- Architecture for multi-agent customer escalation investigations with parallel dispatch and blind validation

## How to use these

Most of these files are **system prompts** or **prompt templates** you can paste into any LLM conversation. Some are designed for specific tools:

* **`01-context/`** files work well as persistent context (system prompts, custom instructions, or project knowledge files)
* **`02-prompts/`** files are task-specific prompts you paste when needed
* **`.opencode/command/`** files are [OpenCode](https://opencode.ai) slash commands (but the prompt content works anywhere)
* **`.opencode/skills/`** files are on-demand skills that get loaded when specific topics come up
* **`.opencode/agent/`** files define specialized subagents for specific tasks

## Adapting to your context

These prompts reference a few conventions you'll want to adapt:

* References to `01-context/*.md` files point to personal context documents (writing style, philosophy, etc.). Create your own equivalents.
* Some prompts mention MCP servers or tool integrations. Replace with whatever tools you use.
* The writing style and product philosophy reflect my preferences. Adjust to match yours.

## About

I'm [Rian van der Merwe](https://elezea.com), a product manager who uses AI tools extensively in my daily work. This repo contains the prompts and context files I've found most useful, published so others can adapt them.

For more on my approach to product management and AI, see [`product-philosophy.md`](01-context/product-philosophy.md).

## License

MIT. Use these however you like.
