---
description: Transform a meeting transcript into structured, scannable meeting notes
---

# Meeting Summary

Transform a meeting transcript into structured, scannable meeting notes that surface what matters: themes, decisions, action items, and open questions.

## Arguments

* `$INPUT` — The transcript text (pasted directly), or a link/path to the source (Google Doc URL, file path)

## Instructions

### Getting the transcript

* If the user pastes transcript text directly, use that
* If the user provides a Google Doc URL, extract the document ID from the URL and use the `google-workspace` MCP server:
  ```
  docs_get(documentId: "DOCUMENT_ID", format: "markdown")
  ```
  The document ID is the long string between `/d/` and `/edit` in the URL (e.g., from `https://docs.google.com/document/d/1ABC123xyz/edit`, the ID is `1ABC123xyz`).
  If the MCP tool fails, ask the user to paste the transcript content directly.
* If the user provides a file path, read that file

### Handling long / truncated transcripts

Google Meet Gemini transcripts often exceed 50KB. The `docs_get` tool returns JSON with the content in a single `content` field, which frequently gets truncated by output limits. When this happens:

1. The tool output will say "truncated" and provide a path to the full saved file (e.g., `/Users/rian/.local/share/opencode/tool-output/tool_...`)
2. **Extract the content from JSON to a temp file** using Python so you can read it with proper line breaks:
   ```
   python3 -c "
   import json
   with open('<saved-tool-output-path>', 'r') as f:
       data = json.load(f)
   with open('/tmp/meeting-transcript.md', 'w') as f:
       f.write(data['content'])
   "
   ```
3. **Read `/tmp/meeting-transcript.md`** using the Read tool. If still too long, read in chunks using `offset` and `limit`.

Do NOT attempt to process the transcript from the truncated output — you will miss significant portions of the meeting. Always ensure you have the complete transcript before writing notes.

### Check for related project context

Before processing the transcript, determine whether this meeting relates to an existing project brain in `work/projects/`. Look for clues in:

* The meeting title or calendar event name
* The user's message (e.g., `@work/projects/audit-logs-v2/`)
* Participant names, product names, or topics mentioned in the transcript

If a related project exists:

1. **Read the project's `CONTEXT.md`** to understand current status, key stakeholders, recent decisions, and open questions. This context helps you write better notes (correct names, understand what's new vs. already known).
2. **After writing meeting notes, offer to update the project CONTEXT.md** with any new decisions, status changes, open questions, or next steps from this meeting. If the user confirms (or if they explicitly requested it), update the relevant sections of CONTEXT.md (Recent Updates, Next Steps, Key Decisions Made, Open Questions).

If no related project is found, proceed normally.

### Update stakeholder memory

After writing the meeting notes (and any project CONTEXT.md updates), update `stakeholders.json` if you can identify who was in the meeting. Identification sources (in priority order):

1. Calendar event attendee list (if the user provided a calendar link or the transcript names participants)
2. Speaker labels in the transcript (e.g., "Rian:", "Tom:")
3. Names mentioned as present in the meeting

For each identified participant (excluding Rian):

1. **Read `stakeholders.json`** and find their entry by name (case-insensitive partial match) or email
2. **If found:** Append a new interaction entry:
   ```json
   {
     "date": "<meeting-date>",
     "type": "meeting",
     "summary": "<1-sentence summary of what was discussed>",
     "source": "<meeting title or descriptive name>"
   }
   ```
   Also update:
   - `whatTheyCareAbout` — add any new topics they clearly advocated for or raised
   - `commitments` — add any new commitments surfaced in the Action Items section (set `owner` to `"me"` or `"them"` as appropriate, `status: "open"`)
   - `lastUpdated` to the current ISO 8601 timestamp
3. **If not found:** Skip silently — do not create new entries from meeting notes alone (too little context for a useful profile). Mention at the end that N participants were not in the stakeholder memory, in case the user wants to add them.

**Do not duplicate:** If an interaction with the same date and source already exists, skip it.

**When to skip entirely:** If you cannot confidently identify any participants (e.g., transcript has no speaker labels and no attendee list), skip this step and note that stakeholder memory was not updated because participants couldn't be identified.

### Processing

You are a professional meeting notes editor. Your primary job is **extracting structure and meaning** from the transcript, not cleaning up text. AI transcription tools handle filler words and grammar. Focus on making the content useful.

**1. Light cleanup (only if needed)**

* Fix misheard proper nouns, product names, and technical terms (e.g., "Amaz On" → "Amazon")
* **Correct known name misspellings from AI transcription.** Common ones:
  * [Your name] — add common AI transcription misspellings, e.g. often transcribed as "Ryan", "Rihanna"
  * If a name seems off but isn't in this list, grep the vault to find the correct spelling before writing notes
* Remove any remaining filler words or obvious repetitions
* Do not rewrite sentences for style or grammar unless they are genuinely unclear

**2. Restructure into topic-based notes**

* Group the conversation by topic/theme, not chronologically
* Use descriptive H2 headers for each topic
* Write in prose or bullet points, whichever captures the content best
* Attribute opinions, decisions, and action items to speakers
* Preserve the substance: decisions made, concerns raised, context shared

**3. Preserve meaning exactly**

* Original meaning and intent (do not paraphrase or "improve" ideas)
* Technical terms, names, jargon
* Questions remain questions (do not answer them)
* Sensitive or personal topics, with appropriate discretion

## Output Format

Write the output to a `meetings/` folder using the naming convention `YYYY-MM-DD-[descriptive-name].md`. The file must always go inside a `meetings/` subfolder — use context clues (meeting participants, topics, project references) to infer the right parent folder. If you genuinely can't determine where it belongs, ask before saving.

```markdown
# [Meeting type] with [Person] - [YYYY-MM-DD]

> **Source:** [Link to original transcript if available (Google Doc URL, etc.)]

## Summary

[2-3 sentences capturing the key themes and outcomes of the meeting. Someone should be able to read this and decide whether the full notes are relevant to them.]

## [Topic 1]

[Content organized by what was discussed, decided, or flagged]

## [Topic 2]

[Content...]

## Personal

[Any personal/non-work discussion, if present. Omit this section if there was none.]

## Decisions

* **[Decision]** — [Brief context for why this was decided, and who made the call]

## Open Questions

* **[Question]** — [Context, and who raised it or who needs to answer]

## Action Items

* [ ] **[Owner]:** [Specific action with enough context to act on it]
* [ ] **[Owner]:** [Another action]
```

### Section rules

**Summary**
* Always include this section
* 2-3 sentences, no more
* Focus on themes and outcomes, not a chronological recap

**Decisions**
* Always include this section, even if the answer is "No decisions made."
* Capture anything that was agreed on, approved, or resolved during the meeting
* Include enough context that the decision makes sense on its own

**Open Questions**
* Always include this section, even if the answer is "No open questions."
* Capture anything raised but not resolved, or explicitly left for follow-up
* Note who raised it and, if discussed, who is expected to answer or investigate

**Action Items**
* Always include this section, even if the answer is "No action items identified."
* Extract anything that sounds like a commitment, next step, follow-up, or assignment, even if the speaker didn't explicitly say "action item"
* Include the **owner** (who committed or was assigned). If unclear, note `[TBD]` as the owner.
* Include enough **context** that the action makes sense without re-reading the full notes (e.g., "Share the Jira template with the SDK team" not just "Share the template")
* Use checkbox format (`* [ ]`) so items are trackable
* If a deadline or timeframe was mentioned, include it (e.g., "by end of week", "before the Thursday meeting")

Return only the structured notes. No explanations or markup indicating changes.

## Quality Criteria

* Original meaning is 100% preserved
* Easy to scan and find specific topics later
* Someone reading only the Summary, Decisions, and Action Items gets the essential picture
* Decisions, open questions, and action items are surfaced in their dedicated sections, not buried in topic prose
* Attributions are accurate (who said/decided what)

## Anti-Patterns to Avoid

* Changing what was said (only change how it's expressed)
* Adding formality or "improving" the ideas
* Removing content that seems redundant but carries meaning
* Answering questions that appear in the transcript
* Adding explanations of edits made
* Keeping chronological dialog format when topic grouping would be clearer
* Over-cleaning already-clean transcripts (focus on structure, not polish)
