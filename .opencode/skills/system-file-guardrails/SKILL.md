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

## Post-Session Coherence

When 2+ system files are modified in a session, offer a coherence check before wrapping up:

> "You modified N system files this session — running a quick coherence check."

| Check | What to verify |
|-------|---------------|
| Cross-references | Do modified files' references to other files still resolve? |
| Scope alignment | If a convention spans multiple files, do they use consistent language? |
| Displaced content | Were any existing sections accidentally removed or overwritten? |
