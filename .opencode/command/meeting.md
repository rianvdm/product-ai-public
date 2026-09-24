---
name: meeting
description: Transform a meeting transcript into structured, scannable meeting notes
---

# Meeting Summary

Turn a meeting transcript into scannable notes that surface themes, decisions, open questions and action items, with every claim traceable to what was said or to a cited source.

## Arguments

* `$INPUT` — the transcript text, a Google Doc URL, or a file path. Any trailing text is context from the user, such as the topic or where related docs live.

## Workflow

Work through these in order. The run is complete when every step is done, or skipped with the reason given in the report.

1. **Get the complete transcript** (§1). Never draft from a truncated tool result: it silently drops the end of the meeting.
2. **Gather the sources that settle it** (§2): the deck or document the meeting reviewed, the attendee list, and the related project brain.
3. **Resolve names, products and dates** (§3).
4. **Draft topic-grouped notes** (§4), then apply provenance markers in a separate pass (§5).
5. **Save** to the right `meetings/` folder using the template (§6).
6. **Update stakeholder memory** (§7).
7. **Offer to update the related project `CONTEXT.md`** with new decisions, status changes, open questions and next steps. Update it if the user confirms or asked for it up front.
8. **Report back briefly:** the file path; stakeholder changes and anyone not in memory; names or terms left unresolved; any post-meeting check that changes a decision; and the CONTEXT offer. Opening the file in Obsidian follows AGENTS.md.

## 1. Get the complete transcript

* **Pasted text:** use it. **File path:** read it.
* **Google Doc URL:** the document ID is the string between `/d/` and `/edit`. Read `01-context/agent-tooling.md` → *cf-portal codemode* first, then fetch with `codemode.google_workspace_mcp_docs_get({ documentId, format: "markdown" })`. If the tool fails, ask the user to paste the transcript.
* **Gemini meeting docs have three tabs:** Quick notes, Full notes and Transcript. A `?tab=` in the URL only names one of them. Markdown export concatenates all three, so the transcript follows both notes tabs. To read one tab alone, fetch `format: "raw"` with `includeTabsContent: true`, pick the tab from `doc.tabs[]` by `tabProperties.title`, and join `textRun.content` from `documentTab.body.content`. The Full notes tab carries the **Invited** list and a link to the calendar event. Those names are person chips, so read `person.personProperties.name` too or the line comes back empty (verified 2026-09-22).

**Long transcripts: slice inside the codemode sandbox.** `portal_codemode_execute` truncates its *return value* at roughly 6K–10K tokens, tightening as context fills, but the sandbox holds the whole document. Fetch once per call and return only a slice:

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

Then return `s.slice(1800, 14000)`, `s.slice(13700, 25500)` and so on until you've covered `length`. About 11–12K characters per slice is safe (verified 2026-08-06). Overlap each slice by a few hundred characters so nothing falls between them. Each slice is an independent call, so they can run in parallel.

**Dual-track transcripts.** Some recordings interleave two transcription passes of the same audio, usually a `Microphone` channel and a diarized `Speaker 1/2/3` channel, so nearly every sentence appears twice with different garbles. The user may call this "some duplication." Treat it as evidence: where the channels disagree, one is usually right (`office seaford` → Thomas Seifert). Check which channel handles a few known words better and prefer it. Don't deduplicate before reading.

**Merged diarization labels.** One `Speaker N` label can hold several people. **The tell is a label that answers its own questions:** if "Speaker 1" asks why X was decided and also supplies the design rationale, it isn't one person. Before writing "Speaker N is <name>", scan that label for lines only the presenter could have said. If you find one, say the label is merged and attribute nothing from it without independent confirmation. Third-party address is the strongest confirmation: when the presenter says "what Rian was saying" right after a line, that line is attributable and the rest of the bucket is not.

## 2. Gather the sources that settle it

### The deck or document under review

A deck, or the document the meeting reviewed, resolves transcription garbles faster than asking anyone. The presenter's own slide usually carries the product name, vendor, acronym or figure the transcriber mangled (`Ventronome` → Metronome, `basil` → Bazel). Fetch a deck with `codemode.google_workspace_mcp_slides_get({presentationId, format: "markdown"})` and slice it like a long doc; Slides is read-only over MCP, and the `building-google-slides` skill covers large-deck and multi-column extraction traps. Fetch a Google Doc with `docs_get` as in §1.

Read it for more than proper nouns:

* **Grades the room flattens.** A presenter will say two things as a pair that the slide scores differently. Look for modal verbs, priority labels and one-line principles. A deck that labels two mandates **must** and **should** while the talk presents them as equals has told you the most decision-relevant thing in the session.
* **Disagreements with the transcript.** Record both rather than reconciling them. A slide that lists three levers where the speaker said four tells you what was ad-libbed; collapsing them into one number destroys that.
* **Figures quoted from the document.** Check the unit and basis, because that is what slips. In a pricing review, a speaker compared ClickHouse at "0.34 cents" with R2 at "15 cents" per GB. The memo's 0.34¢ was a cost to serve per *million events*, 15¢ was ten times R2's public list price, and the memo itself called ClickHouse the more expensive backend. Gemini's summary repeated the comparison as fact.
* **What it doesn't cover.** If a section was spoken to a diagram with no text, say so in place, so readers don't assume the deck corroborates it. If the deck fails to resolve the open garbles, record that too.

#### Speaker notes are a separate fetch, and worth it

`slides_get` returns a PDF-flattened rendering with slide text but no speaker notes. Notes live on each page's `notesPage`: get the objectIds in order from `slides_get_pages`, then call `slides_get_page` per page and walk the JSON for `textRun.content`:

```javascript
const pg  = parse(await codemode.google_workspace_mcp_slides_get_pages({presentationId: P}));
const ids = (pg.slides || pg.pages || pg).map(x => x.objectId || x.pageId).filter(Boolean);
const walk = (o, acc) => { if (!o || typeof o !== 'object') return acc;
  if (o.textRun && typeof o.textRun.content === 'string') acc.push(o.textRun.content);
  for (const k of Object.keys(o)) walk(o[k], acc); return acc; };
// then per page: const notes = d?.slideProperties?.notesPage ?? d?.notesPage;
//                walk(notes, []).join('').replace(/\v/g, '\n').trim()
```

Batch four pages at a time (the upstream concurrency cap) inside one `portal_codemode_execute`, return only the trimmed text, and drop pages whose only "note" is the slide number, the default placeholder. Real notes can hold the presenter's own written caveats and live links (verified 2026-08-13). A slide showing only a title and page number has no text in either place, so the transcript is its only source.

### Attendance

The attendee list decides who gets credited and who gets a stakeholder update. Sources, best first: the calendar event's participants (find the event with `calendar_get_events` around the meeting time, then call `calendar_get_participants`), the Gemini **Invited** list, speaker labels, then names mentioned as present.

### The related project brain

Look for a matching brain in `work/projects/` using the meeting title, the user's message and the topics discussed, and read its `CONTEXT.md` before drafting. It gives you correct names and tells you what's new versus already known. With no match, proceed without one.

* **When the meeting is a factual dispute** ("did we already agree on X?"), check the brain's dated decision table before writing. A documented, dated decision and an unresolved one are different situations, and one side may simply be correct.
* **Before asserting that something is unowned, undecided or undesigned,** check the team hub (`06-work/cloudflare/product/<team>/CONTEXT.md`) and any onsite repo as well as the brain you're reading. Org-level assignments land there, so silence in one brain is not evidence. **The tell is a structural explanation that none of the participants gave:** if a root cause appears only in your parenthetical and in nobody's words, source it or drop it.

## 3. Resolve names, products and dates

Common mistranscriptions:

| Person (role) | Transcribed as |
|---|---|
| [Author] | Ryan, Rihanna, Rion, Ron |
| Ryan Skidmore (engineer, AI code reviewer) | "Ryan" when the topic is the AI reviewer, CI components or DevTools engineering |
| Nevi Shah (PM: WOBS, WAE, unified Observability) | Nebby, Navi, Navy, Nebi, Nav'i |
| Marc Selwan (Senior PM, R2 SQL and Pipelines) | Mark Selwin, Mark Sullivan |
| Micah Wylde (Principal Systems Engineer, Pipelines and R2 SQL) | Mike, Micha |
| Rifad Lafir (engineer, Security Observability) | Rafod, Rifat |
| Nick Piazza (SecOps) | Nick Piaza |
| Pranav Sekhar (Senior Growth Engineer, AEO) | Prenav, prenov |
| Aly Cabral (VP, Developer GTM) | Ally; the vault once carried "Ally Cabraw" |
| Carsten Holm (VP, Pricing) | Carson |
| Thomas Seifert (CFO) | office seaford |
| Matt TK (CF CLI and CF Wrangler) | One person: don't split him into "Matt" and "TK" or "correct" him to Matt Moen or Tim Kadlec |

Gemini also fuses a name to the next word (`Carstenalready`, `Nevilike`), so search stems.

**For a name not in the table,** verify against a system of record. The vault propagates its own errors, and a wrong spelling repeated in seven files reads as confirmation.

1. `cfi backstage get user:cloudflare-com/<username>` for title, team and manager.
2. The reviewer or stakeholder table on a relevant wiki page; RFCs and specs list full names.
3. The people directory: `GET https://people.cloudflare.dev/api/v1/employees?limit=100` with a `cf-access-token`, cursor-paginated (about 57 pages; `limit` above 100 errors, and the cursor must be URL-encoded). A zero-hit scan proves a transcription wrong. It works on a surname, or on a mangled first name via a `firstName` prefix scan, which is how "Ally" became Aly Cabral.

When you grep the vault, grep the stem (`Aly`, `Cabr`), not the transcribed spelling: `\bally\b` misses a correct "Aly Cabral" and reports that the vault doesn't know. Beware the plausible-seniority trap: a real exec whose name nearly fits will feel like a match (Allan Leinwand for "Ally"), and fitting seniority is not evidence. Never build a name from an email prefix or invent a surname; look it up or use what you have. If a name stays unresolved, flag it inline, and never let an unverified spelling into `stakeholders.json`.

**Use circumstance to rule candidates out.** When a transcript introduces someone by circumstance ("back from parental leave", "just joined", "leaving for India"), check it against what the vault shows a same-named candidate doing at the time. A transcript named "Drew" as the returning pricing owner. Andrew Depke was the obvious match but had been working the whole time, so the note said "Drew, not Andrew Depke", and a later calendar invite confirmed Drew Conklin.

**A correct spelling can still name nobody in the room.** Cross-check anyone credited with owning work against the attendee list. A summit transcript named a "Josh" who wasn't there, so the owner became `[TBD — name doesn't match anyone in the room]`.

**Products and acronyms get the same treatment,** because a plausible product exists for almost any mangled string. Check Amazon's product list with the Amazon docs search tool or docs.example.com: "cloud for sesses" is Amazon for SaaS, and SASE surviving a plausibility check is exactly the trap. Treat the Gemini auto-summary as another unreliable narrator; it once expanded AEO (answer engine optimization) as "Account Expansion." Flag what you can't resolve, and remove the flag once it's resolved.

**Resolve relative dates with `date -j -f %Y-%m-%d <date> +%A`,** not arithmetic. When a participant's recollection conflicts with a dated artifact, record both in a parenthetical and leave the artifact's date alone.

## 4. Draft the notes

Your job is structure and meaning, not polish; transcription tools already handle filler and grammar.

* **Light cleanup only:** fix misheard names and terms, drop leftover filler and repetition, and leave sentences alone unless they're unclear.
* **Group by topic** under descriptive H2 headers, in prose or bullets as fits.
* **Attribute** opinions, decisions and actions to speakers.
* **Preserve meaning exactly:** intent, technical terms, names and jargon. Questions stay questions. Handle sensitive or personal topics with discretion.
* **Speakers keep their words.** Don't answer the meeting's questions or correct speakers in their own voice. When a cited source contradicts or settles something said, keep what was said and add a clearly labelled post-meeting check that cites the source.

## 5. Provenance [CRITICAL]

When notes draw on a citable source (deck, doc, ticket) and a machine transcript, the reader needs to know which claim came from where. The failure is systematic. Draft from the transcript and consult the deck afterwards, and you'll mark what *sounds* conversational instead of what lacks a slide: hedges on figures printed in 30pt, bare assertions nobody can verify, and every breach running the same direction.

Avoid it one of three ways, in order of preference:

1. **Separate structurally.** Give each person or topic an *On the slide* block and an *In the room* block. There is nothing to misapply, and the split survives careless edits. Best when the notes are laid out per person or per topic.
2. **Let a citation be the marker.** Write `[slide 13]`, or `[memo: <section>]` for a document, where the source backs a claim. State the rule once in the header (*a bracketed citation means the source says it; anything uncited was spoken*) and apply it mechanically. Best when the source arrives after drafting: everything starts uncited, and a citation goes on only where you can point at a page. `grep -o '\[slide [0-9]*\]'` shows coverage.
3. **Derive markers mechanically.** Mark everything unverified, then unmark only what you can point to. Never mark by feel, and never in the drafting pass.

With any approach:

* **Default to unverified.** A missed marker should cost a hedge, not create a false citation.
* **State the marker's scope,** such as "from the marker to the end of the sentence."
* **Quotation marks mean the citable source.** If you quote transcript wording, say so in the header or inline.
* **Blank lines make blocks.** Consecutive lines collapse into one rendered paragraph, so a structural split without blank lines vanishes in the web view.

## 6. Save the notes

Save to a `meetings/` subfolder as `YYYY-MM-DD-[descriptive-name].md`:

* **Project meeting** (review, workshop, decision meeting): the project brain's `meetings/`.
* **1:1:** `06-work/cloudflare/team/<person>/meetings/`, even when it covered one project; the project links to it. If the user redirects a 1:1 to another person's folder (for example, prep for a related 1:1), honour that, add a reference stub (summary plus link) in the canonical person's `meetings/`, and add a one-line pointer to that person's `CONTEXT.md` 1:1 summary.
* **Cross-project or team-level meeting:** the brain that tracks the decision under discussion, linking the others from the header; otherwise `06-work/cloudflare/product/<team>/meetings/`.
* **Genuinely unclear:** ask before saving.

```markdown
# [Meeting title] - [YYYY-MM-DD]

> **Source:** [transcript link]
> **Participants:** [names; roles where they help; who left early]
> **Provenance:** [only when citing a deck or document: the marker rule from §5]

## Summary

[2-3 sentences on themes and outcomes, enough to decide whether to read on.]

## [Topic]

[What was discussed, decided or flagged, with attribution.]

## Personal

[Non-work discussion. Omit if none.]

## Decisions

* **[Decision]** — [context, and who made the call]

## Open Questions

* **[Question]** — [context, who raised it, who needs to answer]

## Action Items

* [ ] **[Owner]:** [action with enough context to act on, plus any deadline]
```

Title 1:1s as `# 1:1 with [Person] - [YYYY-MM-DD]`.

Section rules:

* **Summary:** always; 2–3 sentences on themes and outcomes, not a chronological recap.
* **Decisions:** always, writing "No decisions made." if none. Include anything agreed, approved or resolved, with enough context to stand alone.
* **Open Questions:** always, writing "No open questions." if none. Include anything raised but unresolved or left for follow-up, with who raised it and who answers.
* **Action Items:** always, writing "No action items identified." if none. Include implied commitments, name the owner or write `[TBD]`, give enough context to act without rereading the notes, use checkboxes, and include any deadline mentioned.

## 7. Update stakeholder memory

For each identified participant other than Rian, find their entry in `stakeholders.json` by email or case-insensitive name. The schema lives in the `stakeholder-memory` skill.

* **Found:** append a `meeting` interaction (`date`, `type`, a one-sentence `summary`, `source`) unless one with the same date and source already exists. Add topics they clearly advocated to `whatTheyCareAbout`, add commitments from the Action Items (`owner` is `me` or `them`, `status` is `open`), and set `lastUpdated`.
* **Not found:** skip them, and report how many participants aren't in memory. The exception is someone who authored material in the meeting, such as a slide or a doc they presented, and whose identity you verify with `cfi backstage get user:cloudflare-com/<username>`. Create their entry and say so in the report. Look up emails; never infer them from usernames.
* **Nobody identifiable** (no speaker labels, no attendee list): skip the step and say why.

## Quality bar

* Meaning is 100% preserved: you change how things are said, never what.
* Someone reading only the Summary, Decisions and Action Items gets the essential picture, and none of those items are buried in topic prose.
* Attributions are accurate, and merged speaker labels are flagged.
* No added formality, no "improved" ideas, no dropped content that carries meaning, and no over-cleaning of an already-clean transcript.
* The notes contain no commentary about your edits. Provenance markers and labelled post-meeting checks are content, not edit notes.
