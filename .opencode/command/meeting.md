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
* If the user provides a Google Doc URL, extract the document ID from the URL and read it via cf-portal codemode (see AGENTS.md → MCP Servers):
  ```
  codemode.google_workspace_mcp_docs_get({ documentId: "DOCUMENT_ID", format: "markdown" })
  ```
  The document ID is the long string between `/d/` and `/edit` in the URL (e.g., from `https://docs.google.com/document/d/1ABC123xyz/edit`, the ID is `1ABC123xyz`).
  If the MCP tool fails, ask the user to paste the transcript content directly.
* If the user provides a file path, read that file

### Handling long / truncated transcripts

Google Meet Gemini transcripts often exceed 50KB and get truncated in the tool output.

**Preferred approach — slice inside the codemode sandbox.** `portal_codemode_execute` truncates its *return value* (~6K–10K tokens, tightening as context fills), but the sandbox itself holds the whole document. So fetch once, return only a byte range, and repeat — no truncation, no temp files, no dependence on where the harness saves tool output:

```javascript
async () => {
  const parse = (r) => { const t = r?.[0]?.text ?? r?.content?.[0]?.text ?? JSON.stringify(r);
                         try { return JSON.parse(t); } catch { return { raw: String(t) }; } };
  const r = await codemode.google_workspace_mcp_docs_get({ documentId: "DOC_ID", format: "markdown" });
  const d = parse(r);
  const s = typeof d === 'string' ? d : (d.content ?? d.raw ?? JSON.stringify(d));
  return { length: s.length, head: s.slice(0, 2000) };   // first call: get the length
}
```

Then re-call with `return s.slice(1800, 14000)`, `s.slice(14000, 25500)`, … until you've covered `length`. **~11–12K chars per slice is a safe window.** Overlap each slice slightly (start a few hundred chars before the previous end) so nothing falls between the seams. A 36KB transcript takes one length probe plus three slices. Verified 2026-08-06.

**Fallback — the saved tool-output file** (opencode-specific paths; may not exist in other harnesses). When the output says "truncated" it provides a path to the full saved file (e.g. `/Users/rian/.local/share/opencode/tool-output/tool_...`).

**Step 1: Check the saved file format.** Run `head -c 500 <saved-tool-output-path>` to see if it's plain markdown or JSON-wrapped. Recent observation (2026-04-20): the saved output is often already plain markdown with no JSON envelope.

**Step 2a (plain markdown):** Copy directly to a temp file:
```
cp <saved-tool-output-path> /tmp/meeting-transcript.md
```

**Step 2b (JSON-wrapped):** Extract the content field using Python:
```
python3 -c "
import json
with open('<saved-tool-output-path>', 'r') as f:
    data = json.load(f)
with open('/tmp/meeting-transcript.md', 'w') as f:
    f.write(data['content'])
"
```

**Step 3: Read `/tmp/meeting-transcript.md`** using the Read tool. If still too long, read in chunks using `offset` and `limit`.

Do NOT attempt to process the transcript from the truncated tool output — you will miss significant portions of the meeting. Always ensure you have the complete transcript before writing notes.

### Dual-track transcripts, and merged diarization labels

**Some recordings produce two transcription passes of the same audio, interleaved.** A `Microphone` channel and a diarized `Speaker 1/2/3` channel, so nearly every sentence appears **twice** with different garbles. The user may describe this only as "some duplication." Two things follow:

* **The duplication is a gift, not noise.** Where the two channels disagree, one of them is usually right, which resolves garbles with no deck and nobody to ask. On the 2026-08-13 DRA session this settled ~16 corrections on its own (`customer metadata library` → Customer Metadata Boundary, `edge rights` → edge writes, `office seaford` → Thomas Seifert, and so on). In that recording the `Speaker N` rendering was consistently the closer of the two — check which channel is better on a few known words, then prefer it.
* **Feed it to `add-transcript.py` as-is.** The reflow is whitespace-only and word-for-word verified, so the interleaving survives and the raw file stays honestly raw. Don't pre-clean it.

**A `Speaker N` label can hold more than one person, and this is the more dangerous half.** Diarization merges voices, so a single label routinely carries both the questions *and* the presenter's own answers. On 2026-08-13 `Speaker 1` contained at least three people: Rian, Oliver Roup, and Tom Lianza's replies. **The tell is a label that answers its own questions** — if "Speaker 1" both asks "why did we decide X?" and supplies the design rationale, it is not one person.

So before writing "Speaker N is <name>": scan that label's lines for any that only the presenter could have said. If you find one, say the label is merged and attribute nothing from it except lines with independent confirmation. **Third-party address inside the transcript is the strongest confirmation available** — when the presenter says "what Rian was saying" or "regional services, what Oliver just said" immediately after a line, that line is attributable and the rest of the bucket is not.

### If the session had slides, fetch them before you start

**A deck resolves transcription garbles faster and more reliably than asking anyone.** The presenter's own slide usually contains the product name, vendor, acronym or figure the transcriber mangled. On 2026-08-11 a single pass over a summit deck resolved seven open garbles that had been sitting in an "ask the speaker" list — `Ventronome` → Metronome, `sports steel` → SupportSeal, `big gigs` → Big Digs, `basil` → Bazel, `right dot` → WriteGuard, and the internal sense of a pillar name.

Fetch with `codemode.google_workspace_mcp_slides_get({presentationId, format: "markdown"})`, slicing the return value the same way as a long doc. Slides is **read-only** over MCP, so this is a fetch, never an edit.

**Garbles are the cheap win; the expensive win is a claim the deck grades and the room flattens.** A presenter walking a slide will say two things as a pair that the slide scores differently, and the spoken version loses the score. On 2026-08-13 the deck labelled its two mandates **must** and **should** while the talk presented them as a dual mandate on parallel tracks, and that single word was the most decision-relevant thing in the deck. The same slide-only layer produced the principle behind an entire program ("big, painful, risky data migrations must not block a product from having a regionalized offering") and a claim of latitude the speaker never made aloud ("we reserve the right to keep this where we please"). **So read the deck for modal verbs, priority labels, and one-line principles, not only for proper nouns.**

**Read the deck for disagreements with the transcript too, and record both rather than reconciling them.** The same session's levers slide listed three where he said four aloud, and the deck said "230 services immediately behind api.cloudflare.com" where he said hostnames upstream of a gateway. Those gaps are information about what was ad-libbed; collapsing them into one number destroys that.

**Also note what the deck does *not* cover.** If a whole section of the notes was spoken to a diagram with no text on it, say so in place. Otherwise a reader assumes the deck corroborated it. And if the deck fails to resolve the open garbles, record *that* — it converts "we should check the deck" from an open loop into a closed one.

#### Speaker notes are a separate fetch, and worth it

`slides_get` returns a **PDF-flattened** rendering, which carries slide body text but **not** speaker notes. Notes live on a per-page `notesPage` and need `slides_get_pages` (for the objectIds, in order) then `slides_get_page` per page, walking the JSON for `textRun.content`:

```javascript
const pg  = parse(await codemode.google_workspace_mcp_slides_get_pages({presentationId: P}));
const ids = (pg.slides || pg.pages || pg).map(x => x.objectId || x.pageId).filter(Boolean);
const walk = (o, acc) => { if (!o || typeof o !== 'object') return acc;
  if (o.textRun && typeof o.textRun.content === 'string') acc.push(o.textRun.content);
  for (const k of Object.keys(o)) walk(o[k], acc); return acc; };
// then per page: const notes = d?.slideProperties?.notesPage ?? d?.notesPage;
//                walk(notes, []).join('').replace(/\v/g, '\n').trim()
```

Batch 4 at a time (the upstream concurrency cap) inside one `portal_codemode_execute`, return only the trimmed note text, and **filter out pages whose only "note" is the slide number** — that is the default placeholder and it will otherwise look like every slide has notes. Verified 2026-08-13: 5 of 17 slides had real notes, and they included the presenter's own written admission corroborating something he said aloud, plus a live wiki URL that a project brain had recorded under a stale path.

A pure-diagram slide has no text in either place. If `slides_get` shows only a title and a page number for a slide, there is nothing more to extract and the transcript is your only source for it.

### Provenance in a multi-source synthesis [CRITICAL]

When a write-up draws on both a citable source (deck, doc, ticket) and an uncitable one (machine transcript), the reader needs to know which claim came from where. **The failure mode is systematic, not occasional:** if you draft from the transcript and consult the deck afterwards, you will mark the passages that *sound* conversational rather than the ones that actually lack a slide. That produces hedges on figures printed in 30pt type and bare assertions on things nobody can verify — the exact inverse of what the marker is for. Measured on 2026-08-11: ~25 breaches in one document, every one in the same direction.

Three ways to avoid it, in order of preference:

1. **Separate structurally.** Give each person or topic an *On the slide* block and an *In the room* block. No marker to misapply, and the split survives a careless edit. This is the better choice whenever the document has a per-person or per-topic layout.
2. **Let a page citation be the marker.** Write `[slide 13]` inline where the deck backs a claim, state the rule once at the top — *a bracketed slide citation means the deck or its notes say it; anything uncited was spoken only* — and say that it was applied mechanically. This is the best option when the deck arrives **after** the notes are drafted, because it converts the whole retrofit into one auditable pass: everything starts uncited, and a citation goes on only where you can point at a page. It is also self-checking, since `grep -o '\[slide [0-9]*\]'` tells you the coverage. Used 2026-08-13 for the DRA write-up: 21 citations across 16 of 17 slides.
3. **Derive markers mechanically.** Mark *everything* as unverified first, then unmark only what you can point to on a specific page. Never mark by feel, and never in the same pass as drafting.

Three rules that go with any of these approaches:

* **Default to unverified.** If an omission errs toward "unverified" rather than toward "the deck says so", a missed marker is a small cost instead of a false citation.
* **State the marker's scope.** "Applies from the marker to the end of the sentence" — otherwise a mid-sentence marker is ambiguous about which half it governs.
* **Quotation marks mean the citable source.** If a phrase is too good to paraphrase but only exists on tape, say so inline. Never let transcript wording sit in quotes unflagged.

**Markdown trap:** a structural split only exists if the blocks are separated by **blank lines**. Consecutive lines collapse into one rendered paragraph, so the distinction you built disappears in the web view while looking correct in the source.

### Check for related project context

Before processing the transcript, determine whether this meeting relates to an existing project brain in `work/projects/`. Look for clues in:

* The meeting title or calendar event name
* The user's message (e.g., `@work/projects/audit-logs-v2/`)
* Participant names, product names, or topics mentioned in the transcript

If a related project exists:

1. **Read the project's `CONTEXT.md`** to understand current status, key stakeholders, recent decisions, and open questions. This context helps you write better notes (correct names, understand what's new vs. already known).
2. **After writing meeting notes, offer to update the project CONTEXT.md** with any new decisions, status changes, open questions, or next steps from this meeting. If the user confirms (or if they explicitly requested it), update the relevant sections of CONTEXT.md (Recent Updates, Next Steps, Key Decisions Made, Open Questions).

If no related project is found, proceed normally.

**When the meeting itself is a factual dispute between two stakeholders ("did we already agree on X?", "was that ever confirmed?"), check the related project's decision log before writing the notes — don't just record both accounts and let them sit unreconciled.** Project `CONTEXT.md` "Key Decisions Made" tables carry dates and rationale that can independently settle who's right, which changes how you frame the disagreement (a documented, dated decision vs. an unresolved one are different situations, not just different opinions). Verified 2026-08-12: Sahidya's claim that a Logpush pricing decision was "already confirmed" checked out against `projects/logpush-paygo/CONTEXT.md`'s decision table (dated 2026-08-04, before the disputing chat thread) — corroborating one side's account with a primary source rather than defaulting to "it's a communication-styles issue" when one side is simply factually correct.

**Before adding a `*(Project-brain note: …)*` that explains the meeting structurally — above all one asserting something is unowned, undecided or undesigned — verify that claim against the team hub, not just the project brain you're already reading.** Org-level assignments (who owns what, which projects came out of an onsite) get recorded in `06-work/cloudflare/product/<team>/CONTEXT.md` and in the onsite's own repo, *not* in the project brain of whoever is affected by them — so "this brain records no resolution" is not evidence that none exists. Verified 2026-08-13: a note explaining a Nevi/Sahidya conflict as caused by "undesigned Unified UI ownership, open since 2026-05-13" rested on one 1:1's *"to be designed at NYC onsite, not settled before"* plus the absence of a follow-up entry in the WOBS brain, while `product/observability/CONTEXT.md` held a table of the five projects taken off that onsite with named owners (Single Log Surface → Nevi + Nick Downie), and three later meeting notes named the same pair. The invented framing also misread the participant's grievance — she was in the room when the assignment was made, and her complaint was reciprocity, not ambiguity. **The tell is a structural explanation that none of the participants gave:** if the "root cause" appears only in your parenthetical and in nobody's words, source it or drop it.

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

   **Exception — you have more than meeting notes.** If the person authored their own material in the meeting (a slide they wrote, a doc they presented) *and* you can verify their identity at source (`cfi backstage get user:cloudflare-com/<username>` for title, email and manager), that is a legitimate basis for a new entry: their own stated priorities plus a verified identity. Create it, and say in the report that you did and on what basis so the user can revert. Never invent an email from a username pattern — look it up. Applied 2026-08-11 for seven summit attendees whose reflection slides gave a better `whatTheyCareAbout` than most calendar bootstraps.

**Do not duplicate:** If an interaction with the same date and source already exists, skip it.

**When to skip entirely:** If you cannot confidently identify any participants (e.g., transcript has no speaker labels and no attendee list), skip this step and note that stakeholder memory was not updated because participants couldn't be identified.

### Processing

You are a professional meeting notes editor. Your primary job is **extracting structure and meaning** from the transcript, not cleaning up text. AI transcription tools handle filler words and grammar. Focus on making the content useful.

**1. Light cleanup (only if needed)**

* Fix misheard proper nouns, product names, and technical terms (e.g., "Amaz On" → "Amazon")
* **Correct known name misspellings from AI transcription.** Common ones:
  * [Your name] — add common AI transcription misspellings, e.g. often transcribed as "Ryan", "Rihanna", "Rion"
  * Marc Selwan (Senior PM, Developer Platform — R2 SQL, Pipelines) — often transcribed as "Mark Selwin", "Mark Sullivan"
  * Micah Wylde (Principal Systems Engineer, Pipelines / R2 SQL) — often transcribed as "Mike", "Micha"
  * Nevi Shah (PM, WOBS) — often transcribed as "Nebby", "Navi", "Navy", "Nebi", "Nav'i"
  * Rifad Lafir (engineer, Security Observability) — often transcribed as "Rafod", "Rifat"
  * Nick Piazza (SecOps) — often transcribed as "Nick Piaza"
  * Pranav Sekhar (Senior Growth Engineer, AEO — Fatima Yusuf's team) — often transcribed as "Prenav", "prenov"
  * Aly Cabral (VP, Developer GTM — Fatima Yusuf's manager) — often transcribed as "Ally"; the vault also carried "Ally Cabraw" for months
* **Resolving a name that isn't in the list above.** Do *not* stop at grepping the vault — the vault propagates its own errors (a wrong spelling repeated across seven files reads as confirmation). Verify against a system of record:
  1. `cfi backstage get user:cloudflare-com/<username>` — gives job title, team, cost centre, and manager
  2. The reviewer/stakeholder table on a relevant wiki page (RFCs and specs list full names, and this is often the fastest hit for engineers who aren't in the vault yet)
  3. The people directory — `GET https://people.cloudflare.dev/api/v1/employees?limit=100` with a `cf-access-token`, cursor-paginated (~5,700 records, 57 pages; `limit` above 100 errors, and the cursor must be URL-encoded). Slow but definitive: a zero-hit scan *proves* the transcription is wrong rather than leaving it a guess. Works on a **surname** when you have one, and on a **mangled first name** via a `firstName` prefix scan when you don't — that's how "Ally" resolved to Aly Cabral.

  **When you do grep the vault, grep the stem, not the transcribed spelling.** A garbled name and the correct one usually differ by exactly the characters you'd anchor on: `\bally\b` misses "Aly Cabral" sitting correctly in `decisions.md`, so the scan reports "not in the vault" when the answer was already there. Try dropped/doubled letters and a surname fragment (`Ally`, `Aly`, `Cabr`) before concluding the vault doesn't know.

  Beware the plausible-seniority trap: for an exec-sounding first name, a real exec whose name *nearly* fits will surface and feel like a match (Allan Leinwand, Chief Engineering Officer, for "Ally"). Seniority fitting the context is not evidence.

  If a name still can't be resolved, write it with an explicit uncertainty flag rather than silently guessing — and never let an unverified spelling into `stakeholders.json`.
* **The vault's own activity record can *disqualify* a name-match — this is the cheapest tool you have and it isn't an identity lookup.** When a transcript introduces someone by circumstance ("returning from parental leave after six months", "just joined", "he's leaving for India"), that circumstance is a discriminator. Check it against what the vault shows a same-first-named person doing in that window: if the record has them actively working the whole time, they are a different person, and you know it without resolving who the new person is. Verified 2026-08-17 — a transcript named **"Drew"** as the pricing owner taking over Logpush-Paygo, back from six months' parental leave. The obvious candidate was **Andrew Depke**, who is already in that project's stakeholder table. He was the wrong answer, and the proof was in the same brain: he'd driven the FSPEC to v12 and closed review findings through July, so he cannot have been on leave. The outcome was a correct, useful negative — *"Drew is unresolved, and specifically not Andrew Depke"* — which is a far better note than either a guess or a bare "couldn't resolve it."
* **Resolve relative dates with `date`, not arithmetic — and when a participant's recollection conflicts with a dated artifact, record both and don't re-date the artifact.** Transcripts are full of "last Tuesday", "this morning", "it happened Monday", and those land in project brains as specific dates that other sessions then reason from. One `date -j -f %Y-%m-%d <date> +%A` per anchor settles it. The second half matters more: on 2026-08-17 Rian placed a conversation on Thursday that the vault's own notes date Wednesday 08-12. The notes are the better record (they were written from that call), so the fix is a parenthetical saying he recalled it as Thursday and *don't re-date the existing notes off a recollection* — the alternative silently corrupts a dated artifact to match a passing remark.
* **A clean, correctly-spelled name in the transcript can still refer to nobody real.** This is a different failure than a misheard name — the transcription is fine, but the name doesn't map to anyone in the room. Cross-check any named individual against the meeting's actual attendee/participant list before writing them into an output artifact (an Actions-table owner, a stakeholder update) as a confirmed person, especially when they're credited with owning work. Discovered 2026-08-12: a Lisbon summit transcript addressed someone as "Josh" and credited him with owning ticket-automation work; no Josh was on the summit's attendee list. Confirmed with Rian ("There is no Josh in the room") rather than guessed at — the owner became an explicit `[TBD — name doesn't match anyone in the room]` instead of a name.
* **Garbled *product* and acronym names get the same treatment as people's names — and are easier to get wrong**, because a plausible-sounding product exists for almost any mangled string. Check against Amazon's actual product list (`mcp__cloudflare__docs`, or docs.example.com) before committing to a reading. Worked example (2026-08-06): "cloud for first sess" / "cloud for sesses" is **Amazon for SaaS**, not Amazon SASE — SASE is a real Amazon product, which is exactly why the wrong guess survived a plausibility check. Likewise, don't trust the **Gemini auto-summary at the top of the transcript doc** to expand an acronym: on that same transcript it rendered **AEO** (answer engine optimization — Fatima Yusuf's growth channel for AI-agent/answer-engine discoverability) as "Account Expansion/Enterprise." Treat the auto-summary as another unreliable narrator, not a key.

  If you can't resolve a product name or acronym, flag it inline rather than picking the likeliest option silently — and if you *do* resolve it after the user corrects you, remove the uncertainty flag rather than leaving a stale hedge.
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

**1:1 meeting notes belong in the person's folder, not the project folder.** If this is a 1:1 (two-person recurring conversation), save it to `06-work/cloudflare/team/<person>/meetings/` even if the 1:1 covered a specific project. The project gets a wikilink reference to the 1:1 note instead. Rationale: 1:1s accumulate as a durable record of that relationship and often cover multiple projects; duplicating or moving them into project folders breaks that thread. Project-specific meetings (reviews, workshops, decision meetings with multiple attendees) go in the project's `meetings/` folder as normal.

**Exception — the user explicitly redirects a 1:1's notes to a different person's folder.** This happens when a 1:1 is direct prep for, or about, a related 1:1 with someone else (e.g., a Nevi 1:1 processed as prep for a same-day Sahidya 1:1 on the same conflict). Honor the redirect, but don't let the redirected-from person's own history go missing: write the full notes at the requested location, add a short **reference stub** (summary + link, no duplicated content) in the canonical `<person>/meetings/` folder, and add a one-line entry to that person's `CONTEXT.md` "1:1 Notes Summary" section pointing at the full notes. Applied 2026-08-12 for the Nevi 1:1 filed in Sahidya's folder.

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
