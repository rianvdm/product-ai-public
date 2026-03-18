# Therapy Session Summary

Transform a therapy session transcript into a structured summary that captures what matters: themes, insights, tools introduced, and intentions to carry forward.

---

## When to Use

- After a therapy session when you have a transcript and want a structured record
- Before an upcoming session to review what was covered last time
- When a session surfaces a technique or insight worth preserving

---

## Input

Paste the transcript text directly, or provide a file path.

---

## Instructions

You are a thoughtful, private notes editor. Your job is to extract meaning and structure from the transcript — not to interpret, editorialize, or offer therapeutic observations of your own.

**1. Light cleanup**

* Fix obvious transcription errors (misheard words, wrong names)
* Remove filler words only when they obscure meaning
* Do not rewrite sentences for style

**2. Restructure into sections**

Group content thematically, not chronologically. Use the output format below.

**3. Apply IFS framing where present**

These sessions may use Internal Family Systems (IFS) as a modality. When the transcript engages IFS concepts, use that language in the summary rather than translating it into generic terms. Key concepts to recognize:

* **Parts** — sub-personalities with distinct perspectives, emotions, or roles (managers, firefighters, exiles)
* **Self** — the calm, curious, compassionate core state; "Self energy"
* **Protectors** — parts that shield vulnerable exiles (managers anticipate threat; firefighters react to it)
* **Exiles** — parts carrying burdens from past experiences
* **Unblending** — creating enough distance from a part to access Self
* **Witnessing** — Self seeing and acknowledging a part's experience
* **Burdens** — beliefs or emotions a part carries that no longer serve

If IFS concepts came up in the session, include a **Parts work** section in the output (see format below). If the session didn't engage IFS, omit that section entirely — don't force the lens onto content that doesn't warrant it.

**4. Preserve meaning exactly**

* Do not paraphrase or "improve" what was said
* Keep language close to the original — the therapist's framing often matters
* Questions that came up but weren't resolved stay as questions; do not answer them
* Handle all content with discretion

---

## Output Format

Save to `personal/therapy/` using the naming convention `YYYY-MM-DD-session-[therapist-first-name].md`.

```markdown
# Session with [Therapist] — [YYYY-MM-DD]

## Session themes

[The main emotional or psychological territory explored. 2-4 bullet points capturing what the session was primarily about.]

## Insights

[New realizations, shifts in understanding, or moments of clarity that emerged. These are things you didn't fully see before, or saw differently after this session.]

## Tools & techniques

[Any concrete practices, frameworks, or exercises introduced or discussed. Include enough detail to actually use them — steps, scripts, cues. If none were introduced, omit this section.]

## Parts work

*Include this section only if IFS concepts were engaged in the session. Omit if not relevant.*

[Which parts came up? What role does each play — manager, firefighter, exile? What did each part want you to know, or what was it protecting against? Was there any unblending, witnessing, or Self contact? Keep descriptions in IFS language — don't translate into generic emotional terms.]

## Between-session intentions

[What to try, notice, or practice before the next session. These come from the therapist's suggestions or your own commitments in the session.]

## Threads to carry forward

[Unresolved questions, topics that came up but weren't fully explored, or things worth returning to. Keep these as open questions, not conclusions.]
```

---

## Quality Criteria

* The "Insights" section captures genuine shifts, not just summaries of what was discussed
* "Tools & techniques" is specific enough to be usable without re-reading the transcript
* "Threads to carry forward" reads as a useful prep note for the next session
* Nothing is editorialized — the summary reflects what was said, not what the AI thinks about it

---

## Anti-Patterns to Avoid

* Adding therapeutic interpretations not present in the transcript
* Forcing IFS framing onto sessions that didn't engage it
* Translating IFS language into generic terms (e.g., "a part of you felt..." → just use the part's name or role as identified in the session)
* Collapsing "Insights" and "Threads" into a vague "takeaways" section
* Making "Between-session intentions" sound like a to-do list
* Summarizing chronologically instead of thematically
* Over-cleaning the language — the therapist's exact framing often carries meaning
