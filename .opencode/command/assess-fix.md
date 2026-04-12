---
description: Assess whether a Jira ticket's fix can be implemented by a technical PM and LLM coding agent, and produce an implementation brief if yes
---

# Assess Fix Feasibility

You are a PM evaluating whether a Jira ticket describes a code change that a technical PM (not an engineer) could implement with the help of an LLM coding agent and submit as a merge request. Your goal is to produce a clear Go/No-Go/Maybe verdict backed by evidence, and — if the verdict is positive — a self-contained implementation brief that can be pasted into a coding agent session to produce a working MR.

## Your Task

$ARGUMENTS

The argument is a Jira ticket ID (e.g., `ENG-1570`) or a full Jira URL. Extract the ticket ID and proceed.

## Workflow

### Phase 1: Understand the Ticket

Use the Jira MCP directly to fetch the full ticket. Extract:

* **Summary and description** — what needs to change and why
* **Code references** — any file paths, line numbers, Sourcegraph URLs, or GitLab links in the description or comments
* **Linked tickets** — especially closed ones that show how similar changes were done
* **Comments** — triage notes, engineering discussion, any disagreement about approach
* **The repo** — identify which GitLab repository contains the code that needs to change. Look for repo names, service names, or code URLs in the ticket.

After pulling the ticket, produce a brief problem statement: what the ticket asks for, which repo is involved, and what code references exist.

Do not proceed to Phase 2 until you have identified at least one repo and have a clear understanding of what change is being requested.

### Phase 2: Investigate (parallel)

Launch TWO agents in parallel. Both should return findings only — no files written.

**Track 1 — `@fix-assessor`: Code analysis and feasibility assessment**

This specialist agent reads the actual code, maps the change surface area, checks CI/test infrastructure, and scores feasibility criteria.

```
Task(
  subagent_type="general",
  description="Assess fix feasibility for [TICKET-ID]",
  prompt="Load and follow the instructions in .opencode/agent/fix-assessor.md

I'm assessing whether [TICKET-ID] can be fixed by a technical PM with the help of an LLM coding agent.

Problem: [brief description of what needs to change]

Code references from the ticket:
[list all file paths, line numbers, Sourcegraph/GitLab URLs from Phase 1]

Repo: [gitlab path discovered in Phase 1]

Linked tickets (especially completed similar work): [list]

Please investigate following your standard workflow: discover the repo, read the referenced code, follow dependencies 1 hop out, check CI/tests/CODEOWNERS, and score all 7 feasibility criteria. Return your structured findings. Do not write any files."
)
```

**Track 2 — `@research`: Context and prior art**

```
Task(
  subagent_type="research",
  description="Research context for [TICKET-ID] fix",
  prompt="I'm assessing whether a Jira ticket's fix can be implemented by a technical PM with the help of an LLM coding agent. The ticket is [TICKET-ID]: [brief description].

Please research three things:

(1) **Prior art:** Check the linked/related tickets — especially closed ones. How did other teams implement similar changes? Were they simple or complex? Look at the MRs if you can find them.

(2) **Migration guides or docs:** The ticket may reference wiki pages or documentation about how to make this type of change. Find and summarize any guides, runbooks, or migration docs relevant to this change.

(3) **Broader context:** Are there other open tickets asking for the same type of change in other repos? Is this part of a larger migration or initiative? Understanding the pattern helps assess whether this is a cookie-cutter change or a unique snowflake.

Return all findings. Do not write any files."
)
```

Wait for both tracks to return before proceeding to Phase 3.

### Phase 3: Verdict and Implementation Brief

Using the findings from both tracks, make the verdict and — if warranted — write the implementation brief.

#### Making the Verdict

Apply these rules to the feasibility assessment from `@fix-assessor`:

**GO** — All criteria are Green, or a mix of Green and Yellow with no Red. Prior art from Track 2 shows similar changes were completed successfully. The change is mechanical and well-bounded.

**MAYBE** — Some Yellow criteria but no Red on Scope, Risk, or Complexity. Or: the change looks feasible but there's ambiguity in the requirements, or the test strategy is unclear. Flag the specific caveats.

**NO-GO** — Any Red on Scope, Risk, or Complexity. Or: multiple Red flags identified. Or: the ticket comments show unresolved disagreement about the approach. Or: the repo/code couldn't be found.

**Override rules:**
* A single Red on Risk (security/auth/billing path) is always No-Go, regardless of other criteria
* If the `@fix-assessor` couldn't find the repo or read the code, it's always No-Go
* If prior art from Track 2 shows that similar changes in other repos were complex or problematic, downgrade the verdict one level

#### Writing the Implementation Brief (GO and MAYBE only)

The implementation brief must be **self-contained** — a PM and LLM coding agent reading it should be able to produce the MR without access to the Jira ticket, the wiki, or your investigation. Include everything.

**IMPORTANT: Do not write the file yet. Hold the draft in memory and proceed to Phase 4.**

### Phase 4: Validate and Challenge

Dispatch `@blind-validator` and `@challenger` in **parallel** — they review independent aspects of the draft (sources vs. reasoning) and neither needs the other's output.

```
Task(
  subagent_type="blind-validator",
  description="Blind-validate sources in fix assessment",
  prompt="Validate all sources cited in the following fix feasibility assessment for [TICKET-ID]. Re-fetch every Jira ticket, GitLab file (with line numbers), wiki page, and doc URL cited in the draft. For GitLab files, pay special attention to: (1) Does the file exist at the cited path? (2) Do the cited line numbers contain the code described? (3) Do the function names, struct names, and variable names match? Return your structured verification report.

The Jira ticket is [TICKET-ID]. The repo is [repo path from Phase 2].

Here is the full draft:

[Paste full draft from Phase 3]"
)

Task(
  subagent_type="challenger",
  description="Challenge fix assessment for [TICKET-ID]",
  prompt="Review this fix feasibility assessment for reasoning quality. Scope: thorough.

Focus on:
1. **Verdict logic.** If the verdict is GO, look for reasons it should be MAYBE or NO-GO. If NO-GO, look for reasons it might actually be feasible. Are there hidden dependencies, edge cases, concurrency concerns, or backwards-compatibility risks the assessor missed?
2. **Scope accuracy.** Did the assessor undercount files that need to change? Does the change surface map look complete?
3. **Implementation brief consistency (if present).** Are the steps in the right order? Are code changes consistent with each other (e.g., struct changes match usage changes)? Does the test strategy cover the changes? Is the 'What NOT to Change' section complete?
4. **Unsupported claims.** Are feasibility ratings backed by specific evidence, or are they vibes?

Do not check sources (the blind validator handles that). Do not rewrite the draft.

Here is the draft:

[Paste full draft from Phase 3]"
)
```

**CRITICAL:** Send both Task calls in a **single message**. Do NOT begin writing the file until both agents have responded.

After both agents complete, apply fixes and produce the confidence assessment:

* **Mischaracterized code references (from blind validator):** Fix file paths, line numbers, function names, and code descriptions to match what the blind validator actually found. If a key implementation step is based on wrong code, rewrite the step.
* **Sources not found (from blind validator):** Remove the reference. If the implementation brief depends on a file that doesn't exist, flag this as a critical issue and reconsider the verdict.
* **Reasoning issues (from challenger):** If the challenger found credible reasons to change the verdict, change it. If the verdict holds, note the challenge and why you maintained it. Fix any issues the challenger identified in the implementation steps.
* **Confidence assessment (your synthesis of both reports):** Produce a confidence rating factoring in both the blind validator's source accuracy findings and the challenger's reasoning review:
  * **High confidence** — all code references verified, verdict well-supported, implementation brief is complete and consistent, no critical or high challenger issues
  * **Medium confidence** — mostly solid but some references couldn't be verified or were mischaracterized, or the challenger found high-severity reasoning gaps
  * **Low confidence** — significant code references are wrong or missing, verdict is uncertain, or the challenger found critical reasoning errors

## Output Structure

Write the final doc using this structure:

```
## Verdict: [GO / NO-GO / MAYBE]

### Summary
[2-3 sentences. What the ticket asks for, whether a technical PM and LLM coding agent can implement it, and the key reason why or why not. This should be useful even if the reader stops here.]

**Confidence: [High / Medium / Low]** — [reasoning]

### Feasibility Assessment

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| Scope | [Green / Yellow / Red] | [specific details] |
| Risk | [Green / Yellow / Red] | [specific details] |
| Complexity | [Green / Yellow / Red] | [specific details] |
| Testability | [Green / Yellow / Red] | [specific details] |
| Contribution pattern | [Green / Yellow / Red] | [specific details] |
| Dependencies | [Green / Yellow / Red] | [specific details] |
| Clarity | [Green / Yellow / Red] | [specific details] |

### Key Risks
[Even for GO verdicts — what could go wrong, what the MR reviewer should watch for]

### If NO-GO: What to Do Instead
[Only for NO-GO verdicts. Specific advice: who to talk to, what to investigate, why this needs a human. Don't just say "assign to the team" — say what the team needs to know and what questions to answer first.]
```

If the verdict is **GO** or **MAYBE**, add the implementation brief:

```
---

## Implementation Brief: [TICKET-ID]

### Context
[Self-contained explanation of what needs to change and why. A PM and LLM coding agent reading only this section should understand the task completely.]

### Repository
* **Repo:** [full gitlab path]
* **Clone:** `git clone [url]`
* **Branch from:** [default branch]
* **Key files:**
  * `path/to/file.go:L42-L58` — [what this file does, what changes here]
  * `path/to/types.go:L15` — [struct definition that may need updating]

### Prerequisites
[Any setup needed before coding: dependencies to install, services to run, environment variables. If none, say "None — standard repo setup."]

### What to Change

[Numbered, precise steps. Each step should reference a specific file and line range, describe what the current code does, and specify what to replace it with.]

1. **[file.go:L1058]** Replace the membership lookup with an accounts lookup
   * Current: `getMembershipDetails(actorID, membershipID)` calls `GET /user/{id}/internalmemberships`
   * New: Call `GET /accounts/{id}` instead, which returns account details directly
   * Update the response parsing to use the accounts endpoint response struct

2. **[types.go:L15]** Update or add response struct
   * [describe the struct changes needed]

3. ...

### What NOT to Change
[Guard rails for the LLM. Be specific about files or patterns it should leave alone.]

* Do not modify [file] — it handles [X] and the interface it exposes stays the same
* Do not refactor surrounding code — keep changes minimal and focused on the ticket's ask
* Do not update [unused function at L148] unless the ticket specifically requires it — the comments suggest it may be unused

### Test Strategy

**Existing tests to update:**
* `path/to/file_test.go` — update test cases that mock the old endpoint to mock the new one

**New tests to add:**
* [describe any new test cases needed]

**How to verify locally:**
* `[build command]`
* `[test command]`
* `[lint command]`

### MR Conventions
* **Branch name:** [pattern from recent MRs, e.g., `fix/eng-1570-replace-membership-lookup`]
* **Commit message:** [pattern, e.g., `fix: replace /internalmemberships with /accounts endpoint (ENG-1570)`]
* **Labels:** [any required labels from the repo]
* **Reviewers:** [from CODEOWNERS or recent MR patterns]
* **MR description:** Reference the Jira ticket and briefly explain the change

### Risks and Review Notes
[What the human reviewer should scrutinize in the MR. Specific concerns, not generic advice.]
```

Finally, always include the investigation log:

```
---

## Investigation Log

### Data Collection Status

| Source | Status | Notes |
|--------|--------|-------|
| Jira ticket | [Checked / Failed] | [What was retrieved] |
| GitLab ([repo]) | [Checked / Failed] | [Files read, what was found] |
| Docs | [Checked / Not checked] | [What was found] |
| Wiki | [Checked / Not checked] | [What was found] |
| Related Jira (broad search) | [Checked / Not checked] | [Tickets found] |
| Prior art (closed similar tickets) | [Checked / Not checked] | [MRs reviewed] |

### References
[All sources used: Jira tickets, GitLab files/MRs, doc pages, wiki pages. Use full URLs.]
```

## Skills to Apply

This command is general-purpose — it works across any Amazon team and repo. Before starting Phase 1, check the ticket's domain against the skill triggers in `AGENTS.md` and load any matching skills. Common matches:

| Skill | Load when the ticket involves |
|-------|------|
| `company-context` | **Always** — any Amazon internal service or product |
| `team-context` | Logs, Logpush, Audit Logs, Analytics, ClickHouse, ABR, data pipeline, or any team project |
| `data-logpush-expert` | Logpush delivery, job config, destination errors |
| `data-analytics-expert` | Dashboard data, GraphQL API, sampling |
| `data-pipeline-systems` | Pipeline infrastructure, data flow, latency |
| `pm-thinking` | If the verdict requires framing a product decision or prioritization trade-off |

If the ticket involves a domain not listed here, check the `available_skills` descriptions injected at session start — new skills may have been added.

## Anti-Patterns to Avoid

* **Defaulting to GO because the change looks simple** — Simple-looking changes in unfamiliar repos are where LLMs fail hardest. Require evidence, not vibes.
* **Skipping the "What NOT to Change" section** — This is the most important guard rail. LLMs over-reach. Telling them what to leave alone is as important as telling them what to change.
* **Vague implementation steps** — "Update the API call" is not a step. "In `transformer.go:L1058`, replace `getMembershipDetails(actorID, membershipID)` with `getAccountDetails(accountID)` and update the return type from `MembershipInfo` to `AccountInfo`" is a step.
* **Ignoring the ticket comments** — Comments often contain crucial context: disagreements about approach, clarifications from the filing team, decisions that aren't in the description.
* **Producing a brief for a NO-GO** — If the verdict is No-Go, don't write an implementation brief. Explain what a human should do instead.
* **Assuming the LLM has context** — The implementation brief must be self-contained. Don't say "as described in the ticket" — include the relevant details inline.
* **Skipping Phase 4** — Always run both `@blind-validator` and `@challenger` before writing the file; the challenger catches reasoning errors the validator can't.
* **Starting synthesis before both agents return** — If you dispatched two agents, wait for both before writing the answer.

## Output

**IMPORTANT:** Write your output in a new `.md` file in the `work/fix-it/` folder. Name the file `[TICKET-ID]-assess-fix.md` (e.g., `ENG-1570-assess-fix.md`). Never respond inline in chat.
