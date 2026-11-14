---
name: session-end
description: Write a session handoff note, promote learnings, then commit and push the session's files
---

# Session End

Write a handoff note to the appropriate session log so the next session can pick up where this one left off.

**Two session logs exist:**
- `01-context/session-log-work.md` — your job (teams, escalations, internal tools)
- `01-context/session-log-personal.md` — Personal/side projects (Discrobble, discogs-mcp, ListenToMore, tldl, blog posts, gaming)

## Your Task

$ARGUMENTS

## Instructions

### 1. Assess the Session

Review what happened in this conversation. Only write a handoff note if the session involved **substantive work** — decisions made, problems investigated, documents created, or significant context built up. Skip if the session was just a quick question or trivial task.

If the session wasn't substantive enough for a handoff note, say so. If it still edited product-ai files, go to step 7 to commit them; otherwise end.

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
3. Apply the edit directly — no pre-approval step. **Rewrite the paragraph that already covers the topic; do not append a dated paragraph beside it.** Keep the rule and the tell, drop the day's counts and names unless one of them is the tell. Appended paragraphs pile up into one rule stated several times, which later costs a cleanup pass.
4. If a learning is being promoted from `01-context/corrections.md` into an infrastructure file, **remove it from corrections** — it's been baked in and no longer needs the staging area.
5. **Auto-memory is not a promotion target for shared lessons.** It is Claude Code-only and machine-local, so OpenCode, Codex, and the other Mac never see it. A lesson that should change behaviour everywhere goes to a tracked file from the table above; keep auto-memory for facts about this machine or this harness.

**Judgment gate — ask before writing when:**
- The change touches a **skill, command, agent, or AGENTS.md** AND you're uncertain whether it belongs there (these files load into every future session, so a bad edit propagates). For clear-fit edits to those files — a new case in a lookup table, an obvious missing step in a command — apply directly.
- You're tempted to add a correction that might be general CSS/domain knowledge rather than an agent-specific behavioral fix.
- A change would restructure a file rather than amend it.

For stable-facts, session logs, project CONTEXTs, decisions.md, and corrections.md: always apply directly. These are low-blast-radius and easily reverted.

**If no infrastructure updates are needed**, say so explicitly: "No infrastructure updates needed from this session." Don't silently skip this step.

### 4. Update Stable Facts

Based on whether this session was work or personal, read and update the matching file:
- Work session → `01-context/stable-facts-work.md`
- Personal session → `01-context/stable-facts-personal.md`

If the session crossed both domains, update both.

**Measure, prune, then update.** Record the file's size with `wc -c <file>` before touching it. Then, before adding anything new, review every existing entry against these questions:

**Active Work — for each item, ask:**
1. **Still active?** Has this shipped, been abandoned, or become someone else's problem? If yes → remove.
2. **Stale?** Has this item had no session activity in 4+ weeks AND no open threads? If yes → propose removal.
3. **Redundant?** Is this captured better in a project CONTEXT.md or decision log? If yes → remove from stable-facts (it's duplicated context).
4. **Longer than the entry form?** Rewrite it to the form below.

**Entry form (every bullet in the file):** the current state, the next action, and a pointer to where the detail lives (a project CONTEXT, the repo's own instructions, a note, or the session log), in about 400 characters. Release histories, issue lists, commit hashes, and investigation notes belong at the pointer's target. If a detail exists nowhere else, move it to its home before cutting it here.

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
* **Set** the header line to `**Last updated:** YYYY-MM-DD`, with nothing after the date. The session log is the changelog.

Write new and updated entries in the entry form. Detail worth keeping from this session goes in the session-log entry from step 2, and stable facts gets the pointer.

**Size budget: 15,000 bytes per file.** Run `wc -c <file>` again after your edits. If it's over budget, rewrite or cut the longest entries first and re-measure until it's under. If Active Work grows beyond ~12 items, that's a signal that pruning isn't aggressive enough — force-rank and cut.

Apply prunes and updates directly. The final Confirm step lists what changed; user can spot-check or revert via git.

### 5. Write the Entry

Read the chosen session log file (`session-log-work.md` or `session-log-personal.md`), then **prepend** the new entry after the file header (after the pruning rule paragraph, before the first existing H2 entry). The file is in reverse chronological order — newest entries first. Do not modify existing entries.

Include a **Promoted:** field in the session log entry if any infrastructure files were updated:

```markdown
**Promoted:** [List of files updated and what changed, e.g., "Updated `.opencode/command/meeting.md` to include project context check step."]
```

### 6. Check File Size

After writing, count the number of H2 entries in the file. If there are more than 50, warn the user that it's time to archive older entries.

### 7. Commit and Push

Run this after every edit from this session is written, including steps 3–6. Running `/session-end` is the request to commit and push product-ai.

**Settle open offers first.** If this session or this run offered to change a file ("Want me to update X?") and the user hasn't answered, ask now. Make the changes they accept, drop the ones they decline, and only then commit.

1. **List the session's files.** That means every product-ai file this session created or edited: notes, CONTEXTs, the session log, stable-facts, corrections and system files. `git status` also shows other sessions' uncommitted work, so build the list from this session's edits rather than from the status output. Leave out gitignored files.
2. **Check each file's diff** (`git diff -- <path>`). Hunks this session didn't write, such as an earlier session's uncommitted edits to the same file, go into the commit without asking; name them in the report. Stop and ask only if another live session is still editing that file: `ListAgents` shows a peer in this repo and the file changed in the last few minutes.
3. **Stage by explicit path:** `git add -- <path> ...`. Confirm `git diff --cached --name-only` lists exactly the session's files. Never use `git add -A`, `git add .` or `git up` (it stages the whole worktree), and never `--amend`.
4. **Commit** with a subject that names the session's main outcome and a short body saying what changed and why. End with the commit attribution line the harness provides.
5. **Push** with a bare `git push`, unpiped. If the remote has moved on, run `git pull --rebase --autostash`, then push again. If the rebase or the autostash conflicts, stop and report; don't resolve it. If a permission rule blocks the push, give the user `! git push` to run themselves.
6. **Verify on the remote side:** `git status -sb` shows nothing ahead of `origin/main`, and `git log origin/main -1 --format=%h` matches the new commit.

Edits in other repos (shared skill repos, side projects) follow that repo's own branch and review process. List them in the report and leave them uncommitted.

### 8. Confirm

Report in this order so a bad change is easy to catch:

* **High-blast edits (flag prominently if present):** any edits to `.opencode/skills/`, `.opencode/command/`, `.opencode/agent/`, or `AGENTS.md`. These load into every future session — if the user disagrees, they'll want to revert immediately.
* **Stable-facts changes:** removed entries, updated entries, and each file's size before and after in bytes (flag any file still over the 15,000-byte budget).
* **Corrections:** entries added, entries retired (baked in elsewhere).
* **Project CONTEXT / decisions.md:** what was changed.
* **Session log:** which file got the entry, plus current H2 count (warn if >50).
* **Commit:** short SHA, file count, and whether the push landed. List files left uncommitted on purpose (other sessions' work, other repos).

Format the report so the user can scan it in <10 seconds and spot anything that looks wrong. Revert path: `git revert <sha>` for the session commit, or `git checkout <sha>^ -- <file>` for a single file.
