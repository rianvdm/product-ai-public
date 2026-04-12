---
description: Write a session handoff note before ending a substantive work session
---

# Session End

Write a handoff note to the appropriate session log so the next session can pick up where this one left off.

**Two session logs exist:**
- `01-context/session-log-work.md` — Amazon work (Data Platform, DevTools, escalations, Exponent, internal tools)
- `01-context/session-log-personal.md` — Personal/side projects (Discrobble, discogs-mcp, ListenToMore, tldl, blog posts, gaming)

## Your Task

$ARGUMENTS

## Instructions

### 1. Assess the Session

Review what happened in this conversation. Only write a handoff note if the session involved **substantive work** — decisions made, problems investigated, documents created, or significant context built up. Skip if the session was just a quick question or trivial task.

If the session wasn't substantive enough for a handoff note, say so and end.

**Admission quality check:** For each piece of information you'd include in the handoff note, ask:
* **Novel?** Does this extend or contradict something already in the system (skills, commands, stable-facts)? If it's already baked in, don't re-store it.
* **Actionable?** Can a future session use this? Debugging dead-ends and one-off lookups usually aren't worth recording.
* **Durable?** Will this matter in 2 weeks? Open threads and decisions yes; transient investigation details usually no.

Use judgment — these are quality filters, not hard gates. The goal is to keep the session log high-signal.

### 2. Draft the Entry

Determine which session log this entry belongs in based on the session topic:
- **Work** → `01-context/session-log-work.md`
- **Personal** → `01-context/session-log-personal.md`

Write a new H2 entry to prepend to the chosen file (newest first). Use this exact format:

```markdown
## YYYY-MM-DD — [Brief topic description]

**What happened:** [1-3 sentences summarizing what was done. Be specific — mention file paths, ticket IDs, project names.]

**Decisions:** [Any decisions made during the session. Reference where they were documented if applicable.]

**Learned:** [Anything discovered that should persist — debugging insights, preferences expressed, corrections needed, approach that worked/didn't work. If nothing notable, omit this field.]

**Open threads:** [What's unfinished or needs follow-up. If nothing, omit this field.]
```

### 3. Promote Learnings to Infrastructure

This is the most important step. Session logs capture *what happened*, but institutional knowledge only persists if it gets baked into the files the agent actually loads. Review the session and check whether any learnings, workflow improvements, or behavioral fixes should be promoted to infrastructure files.

**Promotion targets (check each one):**

| Target | When to promote | File(s) |
|--------|----------------|---------|
| **Command** | A command workflow was improved, a missing step was discovered, or a default should change | `.opencode/command/*.md` |
| **Skill** | Domain knowledge was gained, a decision tree needs a new branch, or a lookup table needs updating | `.opencode/skills/*/SKILL.md` |
| **Agent** | An agent needs new instructions, a better prompt, or a new agent would be useful | `.opencode/agent/*.md` |
| **AGENTS.md** | A system-level convention changed, a new trigger was identified, or structural changes are needed | `AGENTS.md` |
| **Project CONTEXT** | Project-specific status, decisions, or context changed | `work/projects/*/CONTEXT.md` |
| **Decisions** | A cross-cutting decision was made that should be recorded for future reference | `decisions.md` |
| **Corrections** | A behavioral fix has no better home yet — use as a staging area, not a permanent destination | `01-context/corrections.md` |

**How to promote:**

1. For each learning, identify the best target. Prefer infrastructure files (commands, skills, agents, AGENTS.md) over corrections. Corrections is the staging area for things that don't fit anywhere else *yet*.
2. Read the target file first to understand its current state.
3. Draft the specific edit — what to add or change, and where in the file.
4. Present **all** proposed edits to the user in a single summary before writing anything. Format:
   ```
   **Proposed infrastructure updates:**
   * `[file path]` — [what would change and why]
   * `[file path]` — [what would change and why]
   ```
5. Wait for the user to approve, reject, or modify before writing.
6. If a learning is being promoted from `01-context/corrections.md` into an infrastructure file, **remove it from corrections** — it's been baked in and no longer needs the staging area.

**If no infrastructure updates are needed**, say so explicitly: "No infrastructure updates needed from this session." Don't silently skip this step.

### 4. Update Stable Facts

Read `01-context/stable-facts.md` and update it based on this session.

**Prune first, then update.** Before adding anything new, review every existing entry against these questions:

**Active Work — for each item, ask:**
1. **Still active?** Has this shipped, been abandoned, or become someone else's problem? If yes → remove.
2. **Stale?** Has this item had no session activity in 4+ weeks AND no open threads? If yes → propose removal.
3. **Redundant?** Is this captured better in a project CONTEXT.md or decision log? If yes → remove from stable-facts (it's duplicated context).
4. **Too detailed?** Does the entry contain investigation details, file paths, or implementation notes that were useful at the time but aren't needed for orientation anymore? If yes → trim to 1-2 sentences or remove.

**Recent Decisions — for each item, ask:**
- Is this older than 6 weeks? If yes → remove (it's baked in or no longer relevant).

**Blockers — for each item, ask:**
- Is this resolved? If yes → remove.

**Environment — for each item, ask:**
- Is this still true? Has the tool/access/config changed? If stale → update or remove.

**After pruning, then:**
* **Add/update** any active work items that changed status or direction
* **Add** recent decisions worth tracking
* **Add/remove** blockers
* **Update** environment facts if tools, access, or setup changed
* **Update** the "Last updated" date

Keep the file compact (<60 lines). If Active Work grows beyond ~12 items, that's a signal that pruning isn't aggressive enough — force-rank and cut.

Present all proposed removals and updates together in the "Proposed infrastructure updates" summary shown to the user for approval (same as Step 3 promotions). Group them as **Removals** and **Updates** so the user can see what's being cut.

### 5. Write the Entry

Read the chosen session log file (`session-log-work.md` or `session-log-personal.md`), then **prepend** the new entry after the file header (after the pruning rule paragraph, before the first existing H2 entry). The file is in reverse chronological order — newest entries first. Do not modify existing entries.

Include a **Promoted:** field in the session log entry if any infrastructure files were updated:

```markdown
**Promoted:** [List of files updated and what changed, e.g., "Updated `.opencode/command/meeting.md` to include project context check step."]
```

### 6. Check File Size

After writing, count the number of H2 entries in the file. If there are more than 50, warn the user that it's time to archive older entries.

### 7. Confirm

Report:
* What was written to the session log
* Which infrastructure files were updated (if any)
* Whether any corrections were retired (removed because they were baked into infrastructure)
