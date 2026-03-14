# Multi-Agent Investigation Command

*A generalized version of the multi-agent orchestration pattern used for customer escalation investigations. Adapt the agent roles, data sources, and domain skills to your own products and tools.*

This document describes the architecture of a slash command that dispatches multiple specialist agents in parallel to investigate a customer-reported issue, then synthesizes and validates their findings. The pattern works for any investigation that requires cross-referencing multiple data sources.

## How It Works

The command takes a ticket ID as input and runs through five phases:

### Phase 1: Understand the Issue

Read the ticket from your issue tracker. Extract:

* Summary and description
* Expected vs. actual behavior
* Priority and urgency signals
* Current status and owner
* Linked engineering tickets
* Customer identifiers (account ID, domain, job ID, etc.)

Classify the issue into a category that guides the investigation. Each category maps to specific code repositories, domain skills, and issue tracker projects to prioritize.

### Phase 2: Parallel Investigation

Dispatch three specialist agents simultaneously, each focused on a different data source:

**Agent 1 — Code investigator:** Searches your codebase for the relevant logic, recent changes, and related merge requests. Uses domain skills to know which repositories and services to prioritize.

**Agent 2 — Issue tracker investigator:** Searches beyond the linked tickets for related issues, prior incidents, duplicate reports, and patterns across projects.

**Agent 3 — Documentation and operations investigator:** Checks public docs, internal wiki, active incidents, and recent deploys. Identifies whether the reported behavior matches documented behavior.

All three agents return structured findings. Wait for all three before proceeding.

### Phase 2.5: Generate Verification Queries

A fourth agent receives the combined findings and generates database queries that can confirm or refute the working hypothesis. These might be SQL queries against your analytics database, log queries, or API calls.

### Phase 3: Synthesize

Combine all findings into a structured analysis:

* **Issue summary** — Copy-pasteable for chat or an engineering lead
* **Issue classification** — Bug, expected behavior, documentation gap, configuration error, or other. Supported by evidence from all phases.
* **Root cause** — Anchored in code where possible. If inferred, label it as such.
* **Customer impact** — Who is affected, severity, workarounds
* **Verification queries** — Database queries from Phase 2.5
* **Recommended next steps** — Concrete actions for engineering, PM, and support
* **Data collection status** — What was checked, what was unavailable, and how the analysis compensated

### Phase 4: Validate and Challenge

Two sequential validation steps:

**Step 1 — Blind source verification.** A validator agent independently re-fetches every source cited in the draft (tickets, code files, wiki pages, doc URLs, merge requests). For each source, it verifies the source exists and supports the claim made about it.

**Step 2 — Analysis challenge.** A challenger agent reviews the draft, the validator's report, and the raw research findings. It challenges the classification, proposes an alternative explanation, and produces a confidence assessment (High / Medium / Low).

Apply fixes based on validation results before writing the final output.

## Key Design Decisions

**Why parallel agents instead of a single long conversation?**
Each agent has a focused scope and specialized tools. The code investigator reads code deeply. The issue tracker investigator searches broadly across projects. Running them in parallel is faster and produces more thorough results than a single agent trying to do everything sequentially.

**Why blind validation?**
Agents make mistakes. They cite files that don't exist, mischaracterize what code does, or draw conclusions the evidence doesn't support. A separate validator that independently re-fetches sources catches most of these errors.

**Why classify the issue explicitly?**
"It's a bug" is an assumption many investigations start with. Forcing explicit classification — bug, expected behavior, documentation gap, configuration error — prevents premature conclusions and makes the analysis more useful to engineering.

**Why include a data collection status table?**
Not every data source is always available. Tool failures, access issues, or time constraints mean some sources go unchecked. Documenting what was and wasn't checked lets the reader calibrate trust in the analysis.

## Adapting This Pattern

To adapt this for your own products:

1. **Define your categories.** Map issue types to the code repositories, database tables, and documentation sources relevant to each.
2. **Build domain skills.** Encode institutional knowledge about your products: architecture, common failure modes, which services handle what, which repos to search first. This is what makes the agents useful rather than generic.
3. **Choose your agents.** The three-agent split (code, issues, docs/ops) works well for most product investigations. You might add or swap agents depending on your data sources.
4. **Add verification queries.** If you have a queryable data store (analytics DB, log aggregator, etc.), add a query generation phase. Including the queries in the output lets engineering verify claims independently.
5. **Always validate.** The blind validator and adversarial challenger are the most important parts of the system. Skip them and you'll ship analyses with broken source links and unsupported claims.

## Example Command Structure

```
.opencode/command/investigate.md     # The orchestration command
.opencode/agent/code-investigator.md  # Code search specialist
.opencode/agent/issue-investigator.md # Issue tracker specialist
.opencode/agent/context-investigator.md # Docs and operations specialist
.opencode/agent/query-generator.md    # Verification query generator
.opencode/agent/blind-validator.md    # Source verification (already in this repo)
```

The orchestration command dispatches the agents using the Task tool with `subagent_type` parameters. Each agent file defines the specialist's scope, tools, and output format.

## Related Files

* [`/session-end`](.opencode/command/session-end.md) — The promote-to-infrastructure step means investigation insights get baked into domain skills for future investigations
* [`blind-validator`](.opencode/agent/blind-validator.md) — The source verification agent used in Phase 4
* [`cross-session-memory.md`](cross-session-memory.md) — How the system maintains context between investigation sessions
