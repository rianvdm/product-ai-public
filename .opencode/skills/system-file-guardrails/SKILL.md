---
name: system-file-guardrails
description: Safety checks for editing system files — commands in .opencode/command/, skills in .opencode/skills/, agents in .opencode/agent/, or AGENTS.md itself. Load when creating or modifying any of these files.
---

# System File Edit Guardrails

Follow these checks when editing system files: commands (`.opencode/command/`), skills (`.opencode/skills/`), agents (`.opencode/agent/`), or `AGENTS.md` itself.

## Before Editing

| Check | What to verify |
|-------|---------------|
| **Inbound references** | Search for the file's name across `.opencode/command/`, `.opencode/skills/`, `.opencode/agent/`, and `AGENTS.md`. Note files whose assumptions could break if this file changes. |
| **Outbound references** | What skills, agents, or commands does this file reference? Verify each exists on disk. |

If broken outbound references are found, warn before proceeding (the edit might be fixing them).

## After Editing a Command

| Check | What to verify |
|-------|---------------|
| Frontmatter | `description` present |
| `$ARGUMENTS` | Parsed and handled (if command accepts arguments) |
| Skill loading | Lazy — no loading during research phases |
| Token efficiency | Compact tables over prose. Nothing duplicated from `AGENTS.md` |
| MCP tool references | Correct tool names, fallback behavior if tools are unavailable |

## After Editing a Skill or Agent

| Check | What to verify |
|-------|---------------|
| Frontmatter | `name`, `description` present. Agents: `mode`, `tools` also present |
| Description accuracy | Frontmatter `description` matches what the file actually does |
| Stale references | No references to commands, tools, files, or skills that don't exist |
| Agent quality checklist | Present and covers the agent's actual scope |

## Writing the Content

The checks above cover mechanics. For the *writing* — what earns its place in a file that loads into every session — two references, which agree more than they appear to:

* **`superpowers:writing-skills`** — TDD for documentation. Baseline-test first, and its **Match the Form to the Failure** table: prohibitions and rationalization tables work for *discipline* failures (agent knows the rule, skips it under pressure) and measurably backfire on *shaping* failures (output has the wrong form), where a positive recipe wins.
* **Matt Pocock's `writing-for-agents`** — the pruning lens. Read the real files, not the [overview page](https://www.aihero.dev/skills-writing-great-skills): `gh api repos/mattpocock/skills/contents/skills/productivity/writing-for-agents/SKILL.md --jq .content | base64 -d`, plus its sibling `SKILL-MECHANICS.md` for frontmatter and the model- vs user-invoked choice. Five levers: **context pointers** (the pointer's wording, not its target, decides reliability — one trigger per branch), **information hierarchy** (in-file step → in-file reference → disclosed reference; inline what every branch needs, push behind a pointer what only some branches reach), **completion criteria** (checkable *and* exhaustive — "every rule applied" drives legwork where "produce a list" does not), **leading words** (a pretrained concept repeated as a token, never as a sentence), and **pruning** (the **no-op test**: delete the line, did behaviour change? If not, delete the whole sentence, not some words).

Where they look opposed they aren't: Pocock calls negation a failure mode — "*Don't think of an elephant*, and the elephant is all there is" — which is the same finding as superpowers' shaping-vs-discipline split, reached from the other side. Default to the positive recipe unless the failure is genuinely one of discipline.

## Post-Session Coherence

When 2+ system files are modified in a session, offer a coherence check before wrapping up:

> "You modified N system files this session — running a quick coherence check."

| Check | What to verify |
|-------|---------------|
| Cross-references | Do modified files' references to other files still resolve? |
| Scope alignment | If a convention spans multiple files, do they use consistent language? |
| Displaced content | Were any existing sections accidentally removed or overwritten? |
