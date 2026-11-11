# Product AI Public

Prompts, commands, skills, and agents for AI-assisted product management, plus the developer and hobby skills that grew up alongside them. They're a subset of my personal "second brain" repo, published for others to adapt. See [How I AI](https://elezea.com/ai/) for a series of posts on how this system works in practice.

## Start here

1. Read [`product-philosophy.md`](01-context/product-philosophy.md), then try the [`pm-thinking`](.opencode/skills/pm-thinking/SKILL.md) skill, which applies it. Both work as published.
2. Use [`avoid-ai-patterns.md`](01-context/avoid-ai-patterns.md) as persistent context for anything you draft with an LLM, and run [`generate-writing-style.md`](02-prompts/meta/generate-writing-style.md) on your own writing samples to produce the style guide several other files expect.
3. Read [`cross-session-memory.md`](04-docs/cross-session-memory.md) to see how the session commands, stable facts, and corrections fit together before copying any of them.

The prompts and context files work in any LLM assistant. The commands, agents, and skills assume an agentic harness with a shell and subagents; they are written for [OpenCode](https://opencode.ai) and adapt to Claude Code and similar tools. Several of them call tools from my own setup, listed under [What needs your own tools](#what-needs-your-own-tools).

## Product work

### Context files

* [`product-philosophy.md`](01-context/product-philosophy.md) -- How I think about product work: problem-first, outcomes over outputs, empowered teams
* [`avoid-ai-patterns.md`](01-context/avoid-ai-patterns.md) -- Words, phrases, and structural patterns that make AI writing obvious, with dated notes on which tells current models still show
* [`avoid-ai-visual-patterns.md`](01-context/avoid-ai-visual-patterns.md) -- The visual counterpart to `avoid-ai-patterns.md`: layout and motion habits that make AI-built HTML explainers look generated
* [`project-template.md`](01-context/project-template.md) -- Template for creating a dedicated "project brain" folder for major initiatives
* [`stable-facts-template.md`](01-context/stable-facts-template.md) -- Template for the stable facts file used by cross-session memory. The session commands read `stable-facts-work.md` and `stable-facts-personal.md`, so copy it to those names

### Prompts

**Product management**

* [`draft-review-prd.md`](02-prompts/pm/draft-review-prd.md) -- Draft or review PRDs using a structured Product Opportunity Assessment framework. Asks for Confluence wiki markup output
* [`review-okrs.md`](02-prompts/pm/review-okrs.md) -- Draft or review OKRs with outcome-over-output discipline, good and bad examples for each part, and a review template. Asks for Confluence wiki markup output
* [`debate-product-idea.md`](02-prompts/pm/debate-product-idea.md) -- Simulate a high-stakes product strategy debate with multiple perspectives
* [`review-spec.md`](02-prompts/pm/review-spec.md) -- Review engineering specs to ensure they faithfully translate product requirements

**Development**

* [`brainstorming-planning.md`](02-prompts/dev/brainstorming-planning.md) -- Build ideas through guided discovery, then produce developer-ready specs

**Meta**

* [`generate-writing-style.md`](02-prompts/meta/generate-writing-style.md) -- Analyze writing samples and produce a reusable system prompt for style emulation

### Skills

* [`pm-thinking`](.opencode/skills/pm-thinking/SKILL.md) -- Apply problem-first, outcome-focused product thinking to any product task
* [`linear-walkthrough`](.opencode/skills/linear-walkthrough/SKILL.md) -- Generate narrative walkthroughs of code, documents, or systems for learning and onboarding
* [`check-skill`](.opencode/skills/check-skill/SKILL.md) -- Audit any SKILL.md against best practices: 5 skill killers, anatomy completeness, scoping, and context binding
* [`system-file-guardrails`](.opencode/skills/system-file-guardrails/SKILL.md) -- Safety checks for editing AI system files (skills, commands, agents): pre-edit reference checks, post-edit validation, post-session coherence. Describes my own sync setup, so read it as a pattern

### Agents

* [`code-review`](.opencode/agent/code-review.md) -- Evidence-based code review with tool-assisted validation and provability classification
* [`blind-validator`](.opencode/agent/blind-validator.md) -- Re-fetch each source cited in a draft and check every claim against it. Checks caller-supplied raw output where it cannot fetch, and flags references that are not pinned links
* [`challenger`](.opencode/agent/challenger.md) -- Adversarial reasoning reviewer that finds logic errors, weak explanations, unsupported claims, and gaps that mechanical checklists miss
* [`fix-assessor`](.opencode/agent/fix-assessor.md) -- Read code, map change surface area, check CI/tests, and score feasibility criteria for a proposed fix
* [`research`](.opencode/agent/research.md) -- Deep research across docs, a wiki, Jira, GitLab, and a service catalog, returning sourced findings. Used by `/assess-fix` and `/doc-review`; point its source table at your own tools
* [`editor`](.opencode/agent/editor.md) -- Ruthless style editor that runs ten scoped passes over a document to catch AI patterns, overused words, banned sentence structures, and style-guide violations

### Commands

* [`/assess-fix`](.opencode/command/assess-fix.md) -- Assess whether a Jira ticket's fix can be implemented by a technical PM and LLM coding agent, with a Go/No-Go verdict and implementation brief
* [`/code-review`](.opencode/command/code-review.md) -- Review changes with four parallel code-review agents, then confirm the findings with a fifth. The fourth reviewer checks against a `codex` engineering-standards skill you supply
* [`/meeting`](.opencode/command/meeting.md) -- Transform a meeting transcript into structured notes with decisions and action items. The most environment-specific command here; read it as a worked example
* [`/doc-review`](.opencode/command/doc-review.md) -- Review generated files for accuracy, completeness, and style
* [`/new-project`](.opencode/command/new-project.md) -- Scaffold a new project brain folder
* [`/session-start`](.opencode/command/session-start.md) -- Load recent session context and corrections at the start of a work session
* [`/session-end`](.opencode/command/session-end.md) -- Write a session handoff note before ending a work session

### Docs

* [`cross-session-memory.md`](04-docs/cross-session-memory.md) -- A four-layer memory system that gives AI agents continuity between sessions
* [`multi-agent-investigation.md`](04-docs/multi-agent-investigation.md) -- Architecture for multi-agent customer escalation investigations with parallel dispatch and blind validation

## Beyond PM work

These have nothing to do with product management. They're here because I've revised them more than any other skills I have, and most of each one is field notes on where an API lied or a mistake cost real money.

### Explainers

* [`interactive-explainer`](.opencode/skills/interactive-explainer/SKILL.md) -- Build interactive HTML visualizations of processes, algorithms, or systems. The single-file mode works as published; the deployed-site mode relies on files that are not included
* [`visual-eli5`](.opencode/skills/visual-eli5/SKILL.md) -- Build picture-led HTML explainers with page checks, browser rendering, and share cards. Includes three Python helpers; adapt the site URLs, local repo path, and author byline before use. Python 3.10+ and Chrome/Chromium are needed for rendering
* [`building-psych-explainers`](.opencode/skills/building-psych-explainers/SKILL.md) -- Build one-page psychology explainers for [therapy-words.com](https://therapy-words.com): sourcing from the originator's own words, a beat structure, and five checks (brevity, newbie, pattern, cadence, voice). Includes `css-traps.md` and a Python 3 brevity/pattern checker with no dependencies

### Developer

* [`workers-vitest-pool`](.opencode/skills/workers-vitest-pool/SKILL.md) -- Set up or upgrade vitest tests for Cloudflare Workers: a known-good stack (vitest 4, pool-workers 0.22, workers-types 5, an exact wrangler pin, Node 22), the v2-to-v4 migration recipe that fixes the `.sqlite-shm` isolation bug, and the package's rename to `@cloudflare/vitest-plugin`
* [`discord-bot`](.opencode/skills/discord-bot/SKILL.md) -- Discord bot development guide: Developer Portal setup, Gateway vs Interactions architecture, Cloudflare Workers integration, common gotchas, and verification checklist
* [`diagnosing-mac-performance`](.opencode/skills/diagnosing-mac-performance/SKILL.md) -- Triage a slow Mac: snapshot CPU/memory/swap, identify runaway processes and memory pressure, and recommend fixes ordered by disruption

### Music

Five skills covering a CD collection and a Spotify library. The scripts they call are not included; [`music/README.md`](music/README.md) specifies them and the credentials they need.

* [`finding-original-cds`](music/finding-original-cds/SKILL.md) -- Pick the best original (non-remaster) CD pressing on Discogs, and work around MCP rate limits by hitting the public API directly
* [`finding-cd-bundles`](music/finding-cd-bundles/SKILL.md) -- Price a Discogs wantlist against live eBay listings by barcode, find sellers worth bundling, and cross-check both against the Discogs marketplace floor
* [`auditing-cd-collection`](music/auditing-cd-collection/SKILL.md) -- Classify a whole collection as remaster/original/unverified across ~1,800 cached API calls, and the four matching traps that each produced wrong answers first
* [`managing-spotify-playlists`](music/managing-spotify-playlists/SKILL.md) -- Read and write Spotify playlists safely: which operations are irreversible, how to sequence a long playlist to constraints, and the API fields that mean the opposite of what they look like
* [`playlist-cover`](music/playlist-cover/SKILL.md) -- Generate playlist artwork from what the playlist actually contains, and the verification gate that catches image models misspelling the title

### Personal

* [`books/CLAUDE.md`](05-personal/books/CLAUDE.md) -- Agent instructions for a per-book reading-notes folder: progress-aware, spoiler-safe, web-search-first for factual claims
* [`books/the-will-of-the-many.md`](05-personal/books/the-will-of-the-many.md) -- Example book notes file following the pattern (characters, magic system, worldbuilding, plot threads)
* [`antiphon/CONTEXT.md`](05-personal/antiphon/CONTEXT.md) -- Operating instructions for a personal Last.fm music recommender: live listening data via MCP, Spotify search links, mood buckets, and signal-cited picks
* [`antiphon/templates/`](05-personal/antiphon/templates/) -- Empty starter files for the recommender pattern: user config, the three-state mood library, and an anti-rec list
* [`02-prompts/meta/therapy-session-summary.md`](02-prompts/meta/therapy-session-summary.md) -- Summarize therapy session transcripts into structured notes with IFS (Internal Family Systems) support

## How to use these

* **`01-context/`** files work well as persistent context (system prompts, custom instructions, or project knowledge files). The two templates are starting points to copy
* **`02-prompts/`** files are task-specific prompts you paste when needed
* **`04-docs/`** files explain how the larger patterns fit together. Read them; there is nothing to install
* **`05-personal/`** files are examples of the same approach applied outside work
* **`.opencode/command/`** files are OpenCode slash commands. They need a harness with a shell and subagents; in Claude Code they go in `.claude/commands/`
* **`.opencode/skills/`** and **`music/`** files are on-demand skills that get loaded when specific topics come up. Each is a folder with a `SKILL.md`; drop the folder into your own skills directory to use it (`.claude/skills/` in Claude Code)
* **`.opencode/agent/`** files define specialized subagents. Their frontmatter (`mode`, the pinned `model`, and on most of them a `tools` map) is OpenCode's, so adjust it for another harness

## What needs your own tools

This is a slice of a working setup, so some files point at things that are not published. Each gap is listed below with what to swap in.

* **Personal context files.** Commands and agents read `01-context/writing-style-work.md`, `writing-style-personal.md`, `corrections.md`, split `stable-facts-*` and `session-log-*` files, and a root `AGENTS.md`. `/meeting` also reads `agent-tooling.md` and `corrections/cloudflare-tooling.md`. Create your own; the templates and `generate-writing-style.md` cover most of them.
* **Internal tools.** [`/assess-fix`](.opencode/command/assess-fix.md), [`/meeting`](.opencode/command/meeting.md), [`/new-project`](.opencode/command/new-project.md), and [`blind-validator`](.opencode/agent/blind-validator.md) reach Jira, GitLab, a wiki, and Google Docs through a CLI and an MCP portal from my workplace (`cfi`, cf-portal). [`/doc-review`](.opencode/command/doc-review.md) and [`fix-assessor`](.opencode/agent/fix-assessor.md) expect the same access without naming a tool. Swap in whatever gives your agent that access.
* **Unpublished skills.** Some files load skills that aren't in this repo. Supply your own or remove the step.
  * `/code-review`: `codex`
  * The PM prompts and `/assess-fix`: `company-context`, `team-context`
  * `/assess-fix` and `/new-project`: `cfi`
  * `/assess-fix`: `systematic-debugging`, from the [superpowers](https://github.com/obra/superpowers) plugin
  * `/meeting`: `stakeholder-memory`, `building-google-slides`
  * `interactive-explainer` (deployed mode): `internal-workers-deployment`
* **A missing reference file.** The PRD and OKR prompts point to `03-reference/confluence-wiki-markup-syntax.md` for their output format. Drop that requirement if you do not write to Confluence.

## Versions

Files are synced from a private repo and change in place, without a changelog per file. [Releases](https://github.com/rianvdm/product-ai-public/releases) mark points worth linking to and summarize what changed since the last one.

## About

I'm [Rian van der Merwe](https://elezea.com). I lead product teams and use these files in my own work every day.

## License

MIT; see [LICENSE](LICENSE). Use these however you like.
