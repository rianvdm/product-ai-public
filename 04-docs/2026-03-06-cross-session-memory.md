# Cross-Session Memory System

*Created 2026-03-06*

This system gives the agent continuity between sessions without requiring automated extraction tools, vector databases, or external infrastructure. It extends the existing file-based context patterns with three new mechanisms and two commands.

## How It Works

The system has three layers, each solving a different problem:

### 1. Session Log (`01-context/session-log.md`)

**Problem it solves:** "What was I working on yesterday? What's unfinished?"

A single rolling markdown file with dated entries. Each entry captures what happened, decisions made, things learned, and open threads. Written by the `/session-end` command at the end of substantive work sessions. Read by `/session-start` at the beginning of new sessions (loads the last 3 entries).

**Entry format:**
```markdown
## 2026-03-06 — Brief topic description

**What happened:** 1-3 sentences with specifics (file paths, ticket IDs, project names).

**Decisions:** Decisions made during the session, with references to where they were documented.

**Learned:** (optional) Anything discovered worth persisting — debugging insights, approaches that worked/didn't.

**Open threads:** (optional) What's unfinished or needs follow-up.
```

**Maintenance:** When the file exceeds ~50 entries, archive everything older than 30 days to `01-context/_archive/session-log/`. Before archiving, promote any durable learnings to the appropriate CONTEXT.md, skill, or corrections file.

### 2. Corrections (`01-context/corrections.md`)

**Problem it solves:** "The agent keeps making the same mistake."

A small, curated file of things the agent gets wrong repeatedly or that are counterintuitive. Currently seeded with corrections for Confluence wiki markup syntax, skill loading behavior, and command execution follow-through.

**When to add entries:**
* The agent makes the same mistake more than twice
* Something is counterintuitive enough that the agent is likely to get it wrong (e.g., Confluence uses XHTML, not markdown)
* A correction from a session log entry keeps being relevant

**When to remove entries:**
* The underlying issue is fixed (e.g., a skill was updated to handle the case)
* The correction has been baked into a command or skill file
* The correction is no longer relevant

**How it loads:** Referenced by skills (cloudflare-context, pm-thinking, data-logpush-expert, data-analytics-expert) so it loads automatically when those skills trigger. Also loaded by `/session-start`.

### 3. Decisions Log (`decisions.md`)

**Problem it solves:** "Didn't we already decide this? What was the reasoning?"

A cross-cutting decision log for decisions that don't belong to a specific project brain. Project-scoped decisions still go in the project's `decisions/` directory.

**Entry format:**
```markdown
## 2026-03-06 — Decision title

**Context:** Why this came up.

**Decision:** What was decided.

**Rationale:** Why this was chosen over alternatives.

**Status:** Active / Superseded / Revisit
```

## The Two Commands

### `/session-end`

Run this at the end of any substantive work session. It:

1. Reviews the conversation to assess whether it was substantive enough for a handoff note
2. Drafts an entry in the session log format
3. Checks if any learnings should be promoted to corrections, decisions, or a project CONTEXT.md
4. Appends the entry to `01-context/session-log.md`
5. Warns if the file has grown past 50 entries

You don't need to run this for quick questions or trivial tasks. The command will tell you if it thinks the session wasn't substantial enough.

### `/session-start`

Run this at the beginning of work sessions, or when resuming prior work. It:

1. Reads `01-context/corrections.md` (internalizes it silently)
2. Reads the last 3 entries from `01-context/session-log.md`
3. Presents a brief summary of recent sessions and any open threads
4. Offers to load relevant skills or project context if there's a clear pattern
5. Confirms it's ready to work

You can pass arguments: `/session-start resuming Town Lake work` — and it will also load the relevant project CONTEXT.md.

## How It Connects to the Existing System

```
AGENTS.md (always loaded)
  ├── Core Context Files section → references corrections.md, session-log.md, decisions.md
  ├── On-Demand Command Loading → session-start, session-end triggers
  └── On-Demand Skills → each skill references corrections.md

/session-start command
  ├── Reads corrections.md (internalized)
  ├── Reads last 3 session-log.md entries
  └── Offers to load relevant context

/session-end command
  ├── Appends to session-log.md
  ├── Promotes learnings to corrections.md / decisions.md / CONTEXT.md
  ��── Warns on file growth

Skills (loaded on demand)
  └── Reference corrections.md for known mistakes
```

The system is entirely **pull-based** — context is read on demand, never injected automatically. This keeps token usage predictable and avoids loading irrelevant context.

## What This System Does NOT Do

* **No auto-extraction.** The agent doesn't silently record things during a session. You decide when to write a handoff note via `/session-end`.
* **No vector search.** The repo is navigable enough with skills and CONTEXT.md files that brute-force loading works.
* **No external dependencies.** Everything is plain markdown in git. No databases, no API keys, no running services.
* **No per-turn memory.** Memory writes happen at session boundaries, not after every agent response.


## Tips for Getting the Most Out of It

* **Run `/session-end` when you're done with substantive work.** It takes 10 seconds and makes the next session significantly more productive.
* **Add corrections proactively.** When the agent makes a mistake, tell it to add an entry to corrections.md. This is the highest-signal memory you can build.
* **Keep the corrections file small.** If it grows past ~30 entries, some corrections should be baked into skills/commands instead.
* **Use the session log for "what" and corrections for "how."** The session log tracks work state. Corrections track behavioral fixes.
* **Don't over-engineer.** The whole point of this system is that it's lightweight. If you find yourself spending more time maintaining the memory system than it saves, simplify.
