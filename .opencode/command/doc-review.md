---
description: Review generated files for accuracy, completeness, and style using multi-agent validation
---

# Review Generated File

Review a file produced by another command (e.g., `/ask-se`, `/prd`, `/okr`) using parallel subagents with independent focus areas, followed by a validation pass that filters out false positives.

## Input

$ARGUMENTS

The input should include a file path to review. Optionally, the user may append a `--focus` directive to add a custom lens (e.g., `--focus "verify all Jira links are real"`).

**Parse the arguments:**
* **File path** — everything before `--focus` (required)
* **Custom focus** — everything after `--focus` (optional, passed to all three subagents as additional guidance)

If no file path is provided, ask the user which file to review.

## Pre-Flight

1. **Read the target file** using the Read tool. If it doesn't exist, stop and tell the user.

2. **Detect the source command** from the file's location to determine which format spec to check against:

| File location | Source command | Format reference |
|---------------|---------------|------------------|
| `work/support/` | `/ask-se` | `.opencode/command/ask-se.md` (Summary → Structure → Sources → FAQ sections) |
| `*/prds/` | `/prd` | `02-prompts/pm/draft-review-prd.md` (Problem-first, POA, required sections) |
| `*/okrs/` | `/okr` | `02-prompts/pm/review-okrs.md` (Problem → End State → Objective → Key Results) |
| Other | Unknown | `01-context/writing-style-work.md` (general style check only) |

3. **Read the format reference file** so the style/structure agent has the spec.

4. **Read the writing style file** (`01-context/writing-style-work.md` for work files, `01-context/writing-style-personal.md` for personal files).

## Phase 1: Parallel Review (Three Subagents)

Launch THREE (3) subagents in parallel using the Task tool. Use `@research` agents for Subagents 1 and 2 (they need MCP access to verify facts and check coverage), and a `general` agent for Subagent 3 (style checking only needs local files).

Each subagent receives:
* The full content of the target file
* The file path
* The format reference content (from Pre-Flight step 2)
* The custom `--focus` directive, if provided
* Their specific focus area (below)

### Subagent 1: Factual Accuracy (`@research`)

> Focus: Are claims, explanations, and technical details correct?

**Agent type:** `research` — needs MCP access for verification.

**Primary sources:** Amazon docs (for official product behavior) and GitLab (for code references and implementation details). Use wiki and Jira as secondary sources when docs/GitLab don't have the answer.

**Read-only constraint:** Only use MCP tools for reading and searching. Do NOT create comments, notes, MRs, update tickets, or modify any resources.

Prompt the subagent to:
* Check every factual claim against Amazon docs first, then GitLab for implementation-level claims
* Flag hallucinated URLs, product names, feature descriptions, or behaviors
* Verify code examples and configuration snippets are syntactically valid
* Confirm referenced tickets, pages, or docs actually exist (use MCP tools to fetch them directly)
* Use `webfetch` to verify external URLs resolve when practical
* For each finding, include `file_path:line_number`, severity (Critical/Major/Minor), and evidence

### Subagent 2: Completeness & Gaps (`@research`)

> Focus: Does the document fully address its stated scope?

**Agent type:** `research` — needs MCP access to check what's missing against internal knowledge.

**Primary sources:** Wiki (for tribal knowledge, edge cases, historical decisions) and Jira (for known issues, roadmap items, related work the doc should reference). Use Amazon docs and GitLab as secondary sources when needed.

**Read-only constraint:** Only use MCP tools for reading and searching. Do NOT create comments, notes, MRs, update tickets, or modify any resources.

Prompt the subagent to:
* Identify questions the document claims to answer but doesn't
* Flag missing sections required by the format spec
* Search wiki for related context the document should reference but doesn't (known issues, gotchas, prior decisions)
* Search Jira for open bugs or planned work that affect the document's topic
* Check for logical gaps (conclusions without supporting arguments, recommendations without trade-offs)
* Note where "TODO", placeholder text, or thin sections suggest unfinished work
* Check that sources/references are actually cited, not just listed
* For each finding, include `file_path:line_number`, severity (Critical/Major/Minor), and what's missing

### Subagent 3: Style & Structure (`general`)

> Focus: Does the document follow the expected format and writing standards?

**Agent type:** `general` — no MCP access needed; works entirely against local style guides and format specs.

Prompt the subagent to:
* Compare section structure against the format reference from the source command
* Check adherence to writing style guide (lead with outcomes, no hype language, etc.)
* Flag anti-patterns per `01-context/avoid-ai-patterns.md`: overused words and phrases, banned sentence structures, structural patterns (uniform rhythm, faux balance, arguments that teleport), excessive em dashes, overwrought sincerity
* Verify link format correctness (wikilinks for internal, standard markdown for external)
* Check file naming conventions (kebab-case, date prefix where needed)
* For each finding, include `file_path:line_number`, severity (Critical/Major/Minor), and the specific violation

**Custom focus:** If a `--focus` directive was provided, append it to each subagent's prompt as additional guidance: "The reviewer also asks you to pay special attention to: [custom focus]"

## Phase 2: Deduplication

After all three subagents complete, compile their findings and deduplicate:

* **Same issue reported by multiple agents:** Keep the version with better evidence (more specific `file:line`, clearer explanation)
* **Severity disagreements:** Use the higher severity
* **Drop findings without a `file:line` reference** — vague observations don't survive this step

Produce a compiled findings list.

## Phase 3: Validation (`@blind-validator`)

Launch ONE (1) `blind-validator` subagent using the Task tool. Pass it:
* The full content of the target file (this is the "draft" the validator expects)
* The compiled findings from Phase 2, framed as claims to verify — each finding is a claim about what exists at a specific `file:line` location
* The custom `--focus` directive, if provided
* This instruction:

> "You are validating review findings against a document. Each finding is a claim that a specific issue exists at a specific location in the draft. Treat each finding as a source-backed claim and verify it independently:
>
> * **Read the content at the cited `file:line`** for every finding. Do not skip any.
> * **Classify each finding** using your standard framework:
>   - **Verified** → the issue provably exists at the cited location (maps to **Confirmed**)
>   - **Mischaracterized** → the cited content does not actually have the claimed issue (maps to **Disputed**)
>   - **Not found** → the cited location doesn't exist or can't be read (maps to **Disputed**)
>
> For findings that cite external sources (URLs, Jira tickets, wiki pages, GitLab files), use your full MCP-backed verification: re-fetch the source and confirm it supports the finding's claim.
>
> For findings that are purely about style or structure (no external source to verify), read the cited `file:line` and confirm the pattern the finding describes is actually present.
>
> Return your standard verification report. The calling command will use Verified findings as Confirmed and discard the rest."

## Output

Present only **Confirmed** findings to the user, grouped by severity:

```
## Review: [filename]

**Source command:** /ask-se (detected) | **Findings:** N confirmed

### Critical
* `file:line` — [description with evidence]

### Major
* `file:line` — [description with evidence]

### Minor
* `file:line` — [description with evidence]
```

If nothing survived validation, say:

> **Review complete.** All findings were either disputed or acknowledged. The document looks solid.

**Do NOT write the review output to a file** — display it inline in the conversation. This is a transient review, not a permanent artifact.
