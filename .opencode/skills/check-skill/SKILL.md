---
name: checking-skill-quality
description: >
  Use when the user says "check this skill", "review this skill", "quality check skill",
  "audit this skill", "skill quality check", "does this skill follow best practices",
  or provides a path to a SKILL.md file for review. Also triggers on "check skill quality",
  "skill review", or "is this skill well-written". Audits a skill file against the AIDB
  Skills Masterclass best practices framework, checking for the 5 skill killers, proper
  anatomy, scoping, and context binding.
---

# Checking Skill Quality

## Context Required

Read the target SKILL.md file before running. If the skill has a folder with supporting
files (templates, examples, scenarios), read those too to assess context binding.

## Steps

1. Ask for the skill path if not provided
2. Read the full SKILL.md at that path — do not skim
3. If a skill folder exists, list its contents and read any supporting files
4. Check the frontmatter:
   - Name: lowercase, hyphens only, max 64 chars, gerund form (verb-ing)?
   - Description: starts with "Use when..."? Lists trigger phrases? Written in third person? Loud and specific?
5. Check for the 5 Skill Killers:
   - **Killer 1 — Vague/quiet description**: Is it specific, loud, third-person, with "Use when..." format and edge-case triggers?
   - **Killer 2 — Over-defined process**: Is freedom matched to task fragility? Tight for fragile ops, loose for creative?
   - **Killer 3 — Stating the obvious**: Does every paragraph add signal the model doesn't already know? Challenge each section.
   - **Killer 4 — Missing gotcha section**: Is there a dedicated Gotcha Section with documented failure patterns specific to this skill?
   - **Killer 5 — Monolithic blob**: Is the SKILL.md under 500 lines?
6. Check skill anatomy completeness and quality:
   - Steps: numbered list (not prose)?
   - Output: literal template/example shown (not just described)?
   - Gotcha Section: present and substantive — not empty, not generic?
   - Constraints: sharp and specific to this skill (not generic model behavior)?
   - Identity/role section: absent? Flag explicitly if present — "Act as a senior X" is always an anti-pattern
7. Check scoping:
   - Can you describe the skill's job in one sentence?
   - Does it have two distinct triggers suggesting it should be two skills?
   - Would two different people use different halves of it?
8. Check context binding:
   - Are files specific to this skill in the folder?
   - Are shared/org-level references pointed to externally (not duplicated)?
   - Is any context that should be external being embedded inline?
9. Classify the skill type:
   - **Capability Uplift**: new function the model can't do well alone — note it may become obsolete as models improve
   - **Encoded Preference**: your workflow for something the model can do — note it gets more valuable over time
10. Generate the audit report per the output format below

## Output

### Skill Quality Audit: `[skill-name]`

**Type:** Capability Uplift / Encoded Preference
**Overall verdict:** SOLID / NEEDS WORK / RED FLAG

---

**5 Skill Killers Check**

| # | Killer | Status | Notes |
|---|--------|--------|-------|
| 1 | Vague/quiet description | PASS / FAIL | [specifics] |
| 2 | Over-defined process | PASS / FAIL | [specifics] |
| 3 | Stating the obvious | PASS / FAIL | [specifics] |
| 4 | Missing gotcha section | PASS / FAIL | [specifics] |
| 5 | Monolithic blob | PASS / FAIL | [line count] |

---

**Anatomy Check**

| Section | Present | Quality | Notes |
|---------|---------|---------|-------|
| Name (gerund, hyphens, ≤64 chars) | Yes/No | Good/Weak/N/A | |
| Description (trigger, loud, 3rd person) | Yes/No | Good/Weak | |
| Context Required | Yes/No | Good/Weak/N/A | |
| Steps (numbered, not prose) | Yes/No | Good/Weak | |
| Output (literal template shown) | Yes/No | Good/Weak | |
| Gotcha Section (substantive) | Yes/No | Good/Weak | |
| Constraints | Yes/No | Good/Weak/N/A | |
| Identity/role section (should be ABSENT) | Absent/Present | — | Flag if present |

---

**Scoping**
- One clear job: [yes/no + one-sentence description of the job]
- Split candidate: [yes/no + reason if yes]

**Context Binding**
- In-folder files: [list, or "none"]
- External references: [list, or "none"]
- Misplaced context: [yes/no + specifics if yes]

---

**Top Recommended Improvements**
1. [Most impactful fix — be specific, not generic]
2. [Second fix]
3. [Third fix, if applicable]

**Litmus Test**
After this skill runs, can the output be used directly — or will it need editing and restructuring? [honest assessment based on how precise the steps and output format are]

---

## Gotcha Section

- Do not mark a skill SOLID just because all sections are present — check the QUALITY of each section, not just presence
- A description that lists trigger phrases but is vague about what the skill does still fails Killer 1
- The Gotcha Section is the highest-signal content in any skill — missing or generic gotcha content is always at least NEEDS WORK
- Do not flag prose in Steps as automatic fail if the prose is tight and directive — the problem is prose that hides ambiguity or gives the model too much latitude on fragile operations
- A Capability Uplift skill should be noted as potentially obsolete if a recent model improvement may have addressed the gap it fills
- The litmus test is not rhetorical — actually assess whether the output format and step precision would produce directly usable output
- If supporting files exist but are not referenced in the SKILL.md, flag the disconnect
- Do not skip the scoping check — skills that try to do two jobs are a common failure mode that the rest of the audit misses

## Constraints

- Read the entire skill file before issuing any verdict
- Overall verdict rules:
  - RED FLAG: any Killer scores FAIL and the fix is non-trivial, or an identity/role section is present
  - NEEDS WORK: one or more Killers fail but fixes are minor, or anatomy sections are weak
  - SOLID: all 5 Killers pass and anatomy is complete and high-quality
- Do not soften verdicts to be encouraging — the point is to surface real issues
- Flag identity/role sections ("Act as a...") explicitly every time — no exceptions
