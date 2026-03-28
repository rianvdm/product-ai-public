---
description: Review changes with parallel @code-review subagents
agent: plan
---

Review uncommitted changes by default. If no uncommitted changes, review the last commit. If the user provides a PR/MR number or link, fetch it with CLI tools first.

Guidance: $ARGUMENTS

Launch FOUR (4) @code-review subagents in parallel. Give each a different focus area. If the user guidance specifies areas, use those (still include the Codex reviewer). Otherwise default to: (1) correctness, (2) security & resilience, (3) complexity & maintainability, (4) Codex compliance. Include the focus area in each subagent's prompt.

For the Codex reviewer (#4): instruct it to load the `codex` skill, identify the language(s) in the diff, read the relevant Codex reference files (e.g., `references/typescript/README.md` for TypeScript), and check the code against each applicable rule. For each violation, cite the specific Codex rule and reference path. Classify findings as either "deviation from Codex" (the code violates a rule) or "codebase-wide gap" (the entire codebase deviates, not just this change). Only flag deviations introduced by this change as actionable; codebase-wide gaps are informational only.

After all four complete, deduplicate their findings — keep the version with better evidence, use the higher severity when they disagree, and drop anything without a `file:line` reference. Run the project's lint/test commands to catch anything the reviewers missed.

Then launch ONE (1) final @code-review subagent to validate. Pass it the compiled findings, the user guidance, and this instruction: "For each finding, read the code at the referenced file:line. Classify as **Confirmed** (provably real), **Disputed** (not supported by the code), or **Acknowledged** (real but not worth fixing). Return only Confirmed findings."

Present only Confirmed findings to the user, ranked by severity. If nothing survived validation, say so.
