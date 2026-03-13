# Cross-Session Memory System

*Created 2026-03-06. Updated 2026-03-08.*

This system gives the agent continuity between sessions without requiring automated extraction tools, vector databases, or external infrastructure. It extends the existing file-based context patterns with three layers, two commands, and an active promotion pathway that turns session learnings into institutional knowledge.

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

**Maintenance:** When the file exceeds ~50 entries, archive everything older than 30 days to `01-context/_archive/session-log/`. Learnings should already be promoted to infrastructure files via `/session-end` — archiving is just cleanup, not a last-chance review.

### 2. Corrections (`01-context/corrections.md`)

**Problem it solves:** "The agent keeps making the same mistake."

A **staging area** for behavioral fixes that don't yet have a permanent home in a command, skill, agent, or AGENTS.md. This file should shrink over time as corrections get baked into infrastructure files via the `/session-end` promotion step.

**When to add entries:**
* The agent makes the same mistake more than twice
* Something is counterintuitive enough that the agent is likely to get it wrong (e.g., Confluence uses XHTML, not markdown)
* A behavioral fix doesn't have a natural home in any infrastructure file yet

**When to remove entries:**
* The correction has been baked into an infrastructure file (command, skill, agent, or AGENTS.md)
* The underlying issue is fixed
* The correction is no longer relevant

**How it loads:** Referenced by skills (company-context, pm-thinking, data-logpush-expert, data-analytics-expert) so it loads automatically when those skills trigger. Also loaded by `/session-start`.

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
3. **Actively promotes learnings to infrastructure** — proposes specific edits to commands, skills, agents, AGENTS.md, project CONTEXT files, and decisions. Presents all proposed edits for your approval before writing. If a correction gets baked into an infrastructure file, it's removed from `corrections.md`.
4. Appends the entry to `01-context/session-log.md`
5. Warns if the file has grown past 50 entries

You don't need to run this for quick questions or trivial tasks. The command will tell you if it thinks the session wasn't substantial enough.

**This is the primary mechanism for turning session learnings into institutional knowledge.** Without it, learnings sit in the session log and eventually get archived without being acted on.

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
  |── On-Demand Command Loading → session-start, session-end triggers
  └── On-Demand Skills → each skill references corrections.md

/session-start command (beginning of session)
  ├── Reads corrections.md (internalized)
  ├── Reads last 3 session-log.md entries
  └── Offers to load relevant context

/session-end command (end of session)
  ├── Appends work state to session-log.md
  ├── PROMOTES learnings to infrastructure:
  │   ├── Commands (.opencode/command/*.md)
  │   ├── Skills (.opencode/skills/*/SKILL.md)
  │   ├── Agents (.opencode/agent/*.md)
  │   ├── AGENTS.md
  │   ├── Project CONTEXT.md files
  │   └── Decisions log (decisions.md)
  ├── Falls back to corrections.md for fixes with no better home
  ├── Retires corrections that were baked into infrastructure
  └── Warns on file growth

Skills (loaded on demand)
  └── Reference corrections.md for fixes not yet baked in
```

The system is **pull-based** — context is read on demand, never injected automatically. The one active write path is `/session-end`, which promotes learnings to the files the agent actually loads in future sessions. This is what turns session-specific discoveries into institutional knowledge.

## What This System Does NOT Do

* **No auto-extraction.** The agent doesn't silently record things during a session. You decide when to write a handoff note via `/session-end`.
* **No vector search.** The repo is navigable enough with skills and CONTEXT.md files that brute-force loading works.
* **No external dependencies.** Everything is plain markdown in git. No databases, no API keys, no running services.
* **No per-turn memory.** Memory writes happen at session boundaries, not after every agent response.


## Tips for Getting the Most Out of It

* **Run `/session-end` when you're done with substantive work.** It takes 10 seconds and makes the next session significantly more productive. This is also when institutional knowledge gets promoted.
* **Approve infrastructure updates during `/session-end`.** The agent will propose specific edits to commands, skills, agents, and AGENTS.md. Reviewing and approving these is the highest-leverage thing you can do for future sessions.
* **Corrections should shrink over time.** If the corrections file keeps growing, that means learnings aren't being baked into infrastructure. Look for opportunities to promote corrections into the files they belong in.
* **Use the session log for "what" and infrastructure files for "how."** The session log tracks work state. Commands, skills, agents, and AGENTS.md define how the agent behaves.
* **Don't over-engineer.** The whole point of this system is that it's lightweight. If you find yourself spending more time maintaining the memory system than it saves, simplify.
