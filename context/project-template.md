# Project Brain Template

Use this template to create a dedicated "project brain" folder for major initiatives. Each project folder becomes a self-contained context that Claude can reference for full project understanding.

---

## Folder Structure

```
work/projects/[project-name]/
├── CONTEXT.md           # This file - project overview and key info
├── decisions/           # Decision logs
│   └── YYYY-MM-DD-decision-title.md
├── research/            # Customer feedback, data analysis, competitive intel
│   ├── customer-interviews/
│   ├── data-analysis/
│   └── competitive/
├── artifacts/           # PRDs, specs, designs, one-pagers
│   ├── prd.md
│   ├── one-pager.md
│   └── designs/
└── meetings/            # Meeting notes, 1:1s related to this project
    └── YYYY-MM-DD-meeting-title.md
```

---

## CONTEXT.md Template

Copy this into your project's `CONTEXT.md` file:

```markdown
# [Project Name]

## Quick Reference

| Field | Value |
|-------|-------|
| Status | [Discovery / In Progress / Launched / On Hold] |
| PM | [Name] |
| Eng Lead | [Name] |
| Designer | [Name] |
| Target Launch | [Quarter/Date] |
| Confluence | [Link to PRD/wiki page] |

## Problem Statement

[2-3 sentences describing the user/customer pain this project addresses. Be specific about who is affected and what the impact is.]

## Target Users

[Who specifically is this for? Include roles, segments, or personas.]

## Success Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| [Primary metric] | [Current value] | [Goal] |
| [Secondary metric] | [Current value] | [Goal] |

## Key Stakeholders

| Person | Role | Interest/Concern |
|--------|------|------------------|
| [Name] | [Title] | [What they care about] |

## Current Status

[Brief update on where the project stands. Update this regularly.]

### Recent Updates
- [Date]: [What happened]
- [Date]: [What happened]

### Next Steps
- [ ] [Action item]
- [ ] [Action item]

## Key Decisions Made

| Date | Decision | Rationale | Alternatives Considered |
|------|----------|-----------|------------------------|
| [Date] | [What was decided] | [Why] | [What else we considered] |

See `decisions/` folder for detailed decision logs.

## Open Questions

- [ ] [Question that needs to be resolved]
- [ ] [Question that needs to be resolved]

## Links

- PRD: [Link]
- Design: [Link]
- Eng spec: [Link]
- Gchat channel: [Link]
- Dashboard: [Link]
```

---

## Decision Log Template

Save in `decisions/YYYY-MM-DD-decision-title.md`:

```markdown
# Decision: [Title]

**Date:** [YYYY-MM-DD]
**Decision Maker:** [Name]
**Status:** [Proposed / Decided / Revisited]

## Context

[What situation or question prompted this decision?]

## Options Considered

### Option A: [Name]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Effort:** [Low/Medium/High]

### Option B: [Name]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Effort:** [Low/Medium/High]

## Decision

[What did we decide and why?]

## Implications

[What does this mean for the project? Any follow-up actions?]

## Revisit Criteria

[Under what circumstances would we reconsider this decision?]
```

---

## Meeting Notes Template

Save in `meetings/YYYY-MM-DD-meeting-title.md`:

```markdown
# [Meeting Title]

**Date:** [YYYY-MM-DD]
**Attendees:** [Names]
**Type:** [Standup / Review / Decision / Brainstorm]

## Agenda

1. [Topic]
2. [Topic]

## Notes

### [Topic 1]
[Discussion notes]

### [Topic 2]
[Discussion notes]

## Decisions Made

- [Decision and rationale]

## Action Items

- [ ] [Action] - @[Owner] - Due: [Date]
- [ ] [Action] - @[Owner] - Due: [Date]

## Next Meeting

[Date and focus]
```

---

## How to Use with Claude

When working on a project, point Claude to the project folder:

> "Read the files in `work/projects/[project-name]/` to understand the context, then help me [task]."

Or for specific tasks:

> "Based on the CONTEXT.md in the [project-name] project folder, help me draft an update for stakeholders."

The more complete your project brain, the better Claude can assist with context-aware help.
