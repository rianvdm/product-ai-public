---
name: session-start
description: Load recent session context and corrections at the start of a work session
---

# Session Start

Load cross-session memory to establish continuity from previous work sessions.

## Your Task

$ARGUMENTS

## Instructions

### 1. Load Corrections

Read `01-context/corrections.md` in full. Apply these corrections for the rest of the conversation. Do not summarize them back to the user unless asked — just internalize them.

### 2. Load Stable Facts

Two stable-facts files exist:
- `01-context/stable-facts-work.md` — work state, blockers, environment
- `01-context/stable-facts-personal.md` — Personal/side-project state, decisions, environment

**If the user's arguments indicate a topic area** (e.g., "the pricing project" → work, "Discrobble work" → personal), read only the relevant file. **Otherwise**, read both.

This gives you the current state of all active work, recent decisions, blockers, and environment constraints. Use this as your primary orientation — it's more current and compact than the session log.

### 3. Load Recent Session Logs

Two session logs exist:
- `01-context/session-log-work.md` — work
- `01-context/session-log-personal.md` — Personal/side projects (Discrobble, discogs-mcp, ListenToMore, tldl)

**If the user's arguments indicate a topic area** (e.g., "the pricing project" → work, "Discrobble work" → personal), use only the relevant log. **Otherwise**, use both.

List the entry headings first with `grep -n '^## ' <log>`. Each entry is an H2 with its date and topic, newest first, and it runs from its heading's line to the line before the next heading, or to the end of the file for the last entry.

Choose **3 entries** from whichever log(s) you're using, then read only those line ranges:

- **The arguments name a topic** (a project, product, ticket, or person): the 3 newest entries whose heading matches it. Match loosely, so "Discrobble" also matches `cf-discrobble-api`. If fewer than 3 headings match, fill the remaining slots with the newest entries.
- **No topic:** the 3 newest entries.

When reviewing open threads from the session log, cross-reference against stable-facts. Don't list items that are already captured as active work or blockers — only surface threads that stable-facts doesn't cover.

### 4. Check for Open Threads

From the recent entries and stable-facts, identify what might be relevant to today's work. Present briefly:

```
**Current state** (from stable-facts):
* [2-3 most relevant active work items based on recency or user's arguments]

**Recent sessions:**
* [Date] — [Topic]: [One-line summary]
* [Date] — [Topic]: [One-line summary]
* [Date] — [Topic]: [One-line summary]

**Open threads not in stable-facts:**
* [Thread from session log entry, if any that aren't already tracked]
```

If the user provided arguments (e.g., "resuming the migration work"), also load the relevant project CONTEXT.md for that topic.

### 5. Offer Context Loading

If the recent sessions suggest a particular area of work (e.g., multiple escalation sessions, ongoing project work), offer to load the relevant skill or project context:

> "Your recent sessions have been focused on [topic]. Want me to load [skill/project context]?"

Only offer this if there's a clear pattern. Don't offer if sessions were varied.

### 6. Ready Check

End with a brief confirmation that context is loaded and you're ready to work. Keep it to one line — don't repeat everything you just loaded.
