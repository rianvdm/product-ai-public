---
description: Scaffold a new project brain folder
---

# New Project Scaffolding

Read these files before proceeding:
- `01-context/project-template.md` - **REQUIRED: Project brain structure and templates**
- `01-context/product-philosophy.md` - My product beliefs

## Project Description

$ARGUMENTS

## Instructions

Create a new project brain folder based on the template in `01-context/project-template.md`.

### Steps

1. **Parse the project description** to determine:
   - A short, kebab-case folder name (e.g., `logpush-bigquery`, `developer-portal`)
   - The full project name for the CONTEXT.md title

2. **Create the folder structure** at `work/projects/[project-name]/`:
   ```
   [project-name]/
   ├── CONTEXT.md
   ├── artifacts/
   ├── decisions/
   ├── research/
   └── meetings/
   ```

3. **Generate CONTEXT.md** using the template from `01-context/project-template.md`:
   - Fill in the project name
   - Set Status to "Discovery"
   - Set PM to "[Author]"
   - Draft a problem statement based on the description provided
   - Leave other fields as placeholders for the user to fill in
   - Add any obvious open questions based on the description

4. **Create placeholder files** in subdirectories:
   - `artifacts/.gitkeep`
   - `decisions/.gitkeep`
   - `research/.gitkeep`
   - `meetings/.gitkeep`

5. **Report what was created** and suggest next steps:
   - Fill in the Quick Reference table (Eng Lead, Designer, Target Launch)
   - Define success metrics with baselines and targets
   - Identify key stakeholders
   - Search wiki for related prior work

### Before Creating

Search for any existing documentation or prior work related to this project. Mention relevant findings when reporting what was created.
