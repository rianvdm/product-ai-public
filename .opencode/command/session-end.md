---
description: Write a session handoff note before ending a substantive work session
---

# Session End

Write a handoff note to `01-context/session-log.md` so the next session can pick up where this one left off.

## Your Task

$ARGUMENTS

## Instructions

### 1. Assess the Session

Review what happened in this conversation. Only write a handoff note if the session involved **substantive work** — decisions made, problems investigated, documents created, or significant context built up. Skip if the session was just a quick question or trivial task.

If the session wasn't substantive enough for a handoff note, say so and end.

### 2. Draft the Entry

Write a new H2 entry to append to `01-context/session-log.md`. Use this exact format:

```markdown
## YYYY-MM-DD — [Brief topic description]

**What happened:** [1-3 sentences summarizing what was done. Be specific — mention file paths, ticket IDs, project names.]

**Decisions:** [Any decisions made during the session. Reference where they were documented if applicable.]

**Learned:** [Anything discovered that should persist — debugging insights, preferences expressed, corrections needed, approach that worked/didn't work. If nothing notable, omit this field.]

**Open threads:** [What's unfinished or needs follow-up. If nothing, omit this field.]
```

### 3. Check for Promotable Learnings

Before writing, check if any learnings from this session should be promoted to a more durable location:

* **Repeated correction?** → Add to `01-context/corrections.md`
* **Cross-cutting decision?** → Add to `decisions.md`
* **Project-specific update?** → Update the relevant project's context file
* **Skill gap?** → Note it in the session log for future skill updates

If you identify promotable learnings, write them to the appropriate files AND include them in the session log entry.

### 4. Write the Entry

Read `01-context/session-log.md`, then append the new entry at the end of the file (after the last existing entry). Do not modify existing entries.

### 5. Check File Size

After writing, count the number of H2 entries in the file. If there are more than 50, warn the user that it's time to archive older entries.

### 6. Confirm

Report what you wrote and where. Mention any promotable learnings that were written to other files.
