# Review Engineering SPECs

Review engineering specification documents (SPECs/FSPECs) to ensure they faithfully translate product requirements into technical design, surface gaps, and provide actionable feedback.

---

## When to Use

- Reviewing a SPEC before signing off as PM reviewer
- Checking alignment between a PRD and its corresponding SPEC
- Preparing feedback for engineering leads on technical proposals
- Validating that product requirements haven't been lost in translation

---

## Context Files to Read

| File | When to Load |
|------|--------------|
| `01-context/product-philosophy.md` | Always — grounds review in outcome-focused thinking |
| `01-context/writing-style-work.md` | When drafting written feedback |
| The corresponding PRD | Always — this is your source of truth for requirements |
| Project CONTEXT.md | If available — captures decisions, open questions, and constraints |

---

## Using MCP Servers

Use these proactively during review:

| Server | When to Use |
|--------|-------------|
| **wiki** | Fetch the SPEC if given a URL; find related technical decisions or prior art |
| **backstage** | Look up referenced systems, services, or team ownership |
| **gitlab** | Verify technical claims about existing infrastructure |
| **jira** | Check linked tickets for additional context |

---

## The Review Process

### Step 1: Gather Context

Before reviewing the SPEC, ensure you have:

1. **The SPEC document** — fetch via wiki MCP if given a URL
2. **The corresponding PRD** — this is your alignment baseline
3. **Any project context** — CONTEXT.md, research docs, decision logs
4. **Open questions from PRD** — these should be answered in the SPEC

### Step 2: Check Alignment

Compare the SPEC against the PRD on these dimensions:

| Dimension | What to Check |
|-----------|---------------|
| **Requirements coverage** | Are all must-have requirements addressed? Any missing? |
| **Success metrics** | Does the design support measuring the PRD's success criteria? |
| **User flows** | Do the technical flows match the intended user experience? |
| **Scope boundaries** | Are PRD non-goals respected? Any scope creep? |
| **Decisions** | Are prior decisions (from PRD or CONTEXT) honored? Any undocumented pivots? |
| **Open questions** | Does the SPEC resolve open questions from the PRD, or acknowledge them? |
| **Parallel tracks** | If the SPEC shares a SHIP/Epic with another SPEC or RFC, is the composition story documented *in this SPEC*, or only elsewhere? A reader who lands on this SPEC alone should understand where it fits in the program. |

### Step 3: Evaluate Technical Design

Review the SPEC on its own merits:

| Area | Questions to Ask |
|------|------------------|
| **Architecture** | Is the system design clear? Are components well-defined? |
| **Data model** | Does the schema support the requirements? Any gaps? |
| **Performance** | Are performance targets stated and achievable? |
| **Dependencies** | Are external dependencies identified with owners and timelines? |
| **Release plan** | Is there a phased approach? What ships in V1 vs later? |
| **Risks** | Are technical risks identified with mitigations? |
| **Testing** | Is the test plan adequate for the requirements? |

### Step 4: Identify Gaps and Questions

Look for:

- **Missing sections** — requirements without technical solutions
- **Unstated assumptions** — decisions made without rationale
- **Ambiguity** — areas that need clarification before implementation
- **Blocking issues** — problems that must be resolved before work begins

---

## Output Format

Structure your review as follows:

```markdown
# SPEC Review: [Document Title]

*Reviewer: [Your name]*
*Date: [Date]*
*SPEC URL: [Link]*

---

## Overall Assessment

[2-3 sentences: Is the SPEC ready for approval? What's the main recommendation?]

**Recommendation:** [Approve / Approve with minor changes / Revise and re-review]

---

## Alignment with PRD

| Area | PRD Says | SPEC Says | Assessment |
|------|----------|-----------|------------|
| [Requirement 1] | [PRD text] | [SPEC approach] | [Aligned / Gap / Needs clarification] |
| [Requirement 2] | [PRD text] | [SPEC approach] | [Aligned / Gap / Needs clarification] |

[Add narrative if needed to explain significant gaps]

---

## Questions for Engineering

[Numbered list of specific questions that need answers before approval]

1. **[Topic]:** [Specific question]
2. **[Topic]:** [Specific question]

---

## Missing from SPEC

| Missing Element | Why It Matters |
|-----------------|----------------|
| [Element 1] | [Impact on requirements or implementation] |
| [Element 2] | [Impact on requirements or implementation] |

---

## What's Working Well

[Brief acknowledgment of strengths — don't over-praise, but recognize good work]

* [Strength 1]
* [Strength 2]

---

## Technical Observations

### Strengths
* [Technical strength 1]
* [Technical strength 2]

### Concerns
* [Technical concern 1]
* [Technical concern 2]

---

## Recommendations

[Numbered list of specific, actionable recommendations]

1. **[Action]:** [What to do and why]
2. **[Action]:** [What to do and why]

---

## Next Steps

* [What needs to happen before approval]
* [Who needs to be involved]
* [Timeline considerations]

---

## Related Documents

* **PRD:** [Link]
* **SPEC:** [Link]
* [Other relevant docs]
```

---

## Quality Criteria

A good SPEC review:

- **Grounds feedback in the PRD** — every concern traces back to a requirement or decision
- **Distinguishes blocking from non-blocking** — clear on what must be fixed vs. what's a suggestion
- **Asks specific questions** — not vague concerns, but answerable questions
- **Acknowledges constraints** — understands engineering tradeoffs, doesn't demand perfection
- **Provides actionable recommendations** — concrete next steps, not just criticism
- **Respects the SPEC author's expertise** — questions technical choices, doesn't dictate them

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's a Problem |
|--------------|-------------------|
| **Reviewing without the PRD** | You have no baseline for alignment |
| **Nitpicking implementation details** | PMs review requirements and outcomes, not code |
| **Vague concerns** | "This seems risky" helps no one — be specific |
| **Missing the forest for trees** | Don't miss major gaps while fixating on minor issues |
| **Assuming malice** | If something seems wrong, ask — there may be context you lack |
| **Blocking on non-blocking issues** | Distinguish "must fix" from "would be nice" |
| **Ignoring undocumented decisions** | If SPEC pivots from PRD, ask why and document |

---

## Review Tone Guidelines

- **Be direct but collaborative** — assume good intent
- **Prioritize feedback** — blocking issues first, then suggestions
- **Explain why** — don't just flag issues, explain the impact
- **Ask, don't demand** — "Can you clarify..." not "You need to..."
- **Acknowledge good work briefly** — don't over-praise, but recognize strengths

---

## Example Review Snippets

### Good alignment assessment:
> The SPEC proposes using shipboard3 infrastructure instead of Workers (as stated in the PRD). This is likely a pragmatic choice given shipboard3's existing JIRA sync infrastructure, but the decision should be formally documented in CONTEXT.md.

### Good question:
> **Objective/KR linkage:** The data model has `okr_measures` with a `parent_id` self-reference, but doesn't address where Objectives come from. The PRD notes this is pending Roger Tam's response on SHIP→Epic migration. How should we proceed if that migration isn't feasible?

### Good recommendation:
> **Document the tech stack decision.** Update CONTEXT.md to record the pivot from Workers to shipboard3 with rationale (reusing existing JIRA sync infrastructure). This ensures future readers understand why the SPEC differs from the PRD.

### Bad (too vague):
> The data model seems incomplete.

### Bad (too prescriptive):
> You need to use PostgreSQL instead of D1 for this.
