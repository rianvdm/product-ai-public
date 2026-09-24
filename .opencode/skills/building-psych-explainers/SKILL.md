---
name: building-psych-explainers
description: Use when the user wants to create, update, restyle, review, or publish a psychology or therapy explainer on What That Therapy Word Means, including polyvagal theory, brainspotting, IFS, attachment, EMDR, somatic work, or parts work.
---

# Building psych explainers

Each explainer is one page on a site that already exists.

**Site:** What that therapy word means
**Repo:** `~/git/what-that-therapy-word-means` (GitHub `rianvdm/what-that-therapy-word-means`)
**Live:** https://therapy-words.com (custom domain on its own zone since 2026-09-04; the
canonical host in every page's tags). https://befriending-your-nervous-system.<account>.workers.dev
still serves the same files — the Worker kept its original name when the repo was renamed —
and the previous home, `therapywords.elezea.com`, is a 301 redirect rule on the elezea.com zone

```
public/
  index.html            landing page; one <a class="shelf-slab"> per explainer
  assets/explainer.css  the entire design system, shared by every page
  <slug>/index.html     one explainer
wrangler.jsonc          assets-only Worker: no main, no assets.binding
```

Start by copying an existing page under `public/` as the skeleton. A new page adds
markup and inline SVG. It does not add styles — if you need a style that is not in
`explainer.css`, add it there so every page gets it.

## Order of work

1. **Source it.** Find where the originator explains the idea in their own words —
   a transcript, a talk, their own book or site — and fetch that page. Quote from it.
   The best source is often a PDF transcript, and a 27-page interview yields far more
   quotable wording than any summary of it. WebFetch cannot read a PDF — it saves the
   binary locally and tells you where. Extract it with the macOS PDFKit recipe in
   `.opencode/command/extract-pdf.md`, which needs no install and no network. **Do not
   go looking for `pdftotext`, `mutool`, `qpdf`, `gs`, `pypdf` or `Quartz`-for-system-
   python — none of them are on this machine**, and building a venv to get one is a
   detour around a tool that already works.
   **For an HTML transcript, curl the page and strip the tags yourself.** WebFetch runs
   a summariser that refuses to return long verbatim passages (on TIST it answered a
   request for the transcript with a note about a 125-character quote limit). The raw
   page was 8,000 words and read straight through in one go; that is where every spoken
   quote on the page came from.
   **When the originator's own words exist only behind a paywall** (EMDR: Shapiro's
   park story is in a journal PDF that serves an HTML block page), tell that part from
   their organisation's own page and quote them elsewhere. Do not quote via a blog
   that quotes them — the wording cannot be checked.
2. **Check the evidence.** Search for the state of the research and write down what
   you actually find. This goes in the footer whether it is flattering or not.
   Publisher pages (ScienceDirect, Taylor & Francis, Springer, PubMed) 403 or
   cookie-wall WebFetch. Get abstracts with numbers from Europe PMC instead:
   `curl -s "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:<doi>&format=json&resultType=core"`
   returns `abstractText`; Crossref confirms the DOI, title and authors. Guideline PDFs
   read through the PDFKit recipe once downloaded.
3. **Draft the arc** from the beats below.
4. **Build the page.**
5. **Run all five checks.** Fix what they surface. Brevity first, because every
   later check can be satisfied by adding words; the voice pass last, because cutting
   is what breaks the voice, and it is the one Rian reads for.
6. **Show Rian the prose before anything goes live** — the page is public writing.
7. **Add the index entry**, deploy, byte-compare live against the repo file.

## The beats

Follow the ones the concept actually has, in this order. Number the sections on
the page as you keep them.

| Beat | What goes in it |
|---|---|
| What it is for | In the hero sub, first sentence: who uses this and for what. "A therapy for trauma." "A way to understand why you feel calm, anxious or shut down." |
| The hook question | The single question the concept answers. Polyvagal: "am I safe?" |
| The mechanism | What is physically happening, with the anatomy figure |
| The model | The central picture the originator themselves uses |
| How it behaves | The rules of that model — what moves, in what order |
| The payoff | The one idea that changes how a reader sees their own week |
| The reframe | What the concept stops being the reader's fault |
| Other people | Where other humans come into it |
| The vocabulary | One or two coined words worth keeping |
| The practice | What the originator actually teaches people to do |
| The small actions | Concrete physical things, not insights |
| The short version | The whole page in two sentences |
| Sources | Real links, plus the required caveat |

**Drop beats the concept does not have. Never invent one to fill a slot.** Polyvagal
has a three-state model; brainspotting has a technique and no equivalent model. Forcing
a concept into a shape it does not have is the worst failure available here. A concept
with fewer beats gets a shorter page. The first brainspotting draft filled the missing
model with paragraphs instead: five vocabulary terms where the beat says one or two, a
section on the originator's training philosophy, a 108-word opener. Rian's verdict was
"a lot more wordy and difficult to understand," and the cut removed a section, three
terms and a third of the paragraph words without losing a beat.

## What a page is

- Flat colour fields with hard edges, dark type sitting on them, running full-bleed
  edge to edge for the central model
- Big bold sans for headings, serif for anything quoted or explanatory
- Hairline rules between list items, and whitespace doing the rest of the separating
- Hand-authored inline SVG figures, large and geometric
- Motion that runs by itself: SVG `animateMotion`, CSS keyframes, ambient loops
- Everything visible the moment it is on screen
- Nothing the reader can click except links

Few words per screen. When a section grows past a headline, a short paragraph or two
and a picture, cut an idea rather than shrink the type. The brevity check below holds
the ceilings: 500 paragraph
words on the page, 12 words a sentence, 40 in a paragraph, 65 in a section. Polyvagal
sits at 452 and 8.5 words a sentence; IFS shipped at 491 and 11.7. Both read right.
The ceilings are limits, not targets — see the voice below.

## The voice

One person, kindly and calmly, explaining the idea to someone who asked. Every lede is
a sentence that person would say out loud, in full, with a subject and a verb. Rian's
brief after reading the first IFS draft: *"I don't want people to feel like they are
studying. Someone is kindly, calmly, clearly explaining this topic to them."*

That draft passed every countable check at 387 paragraph words and 7.6 words a
sentence, and read like revision notes. The tells, all from that page:

- A line with no speaker: *"Ask a client how they feel toward their critic. I hate it."*
  Who said "I hate it"? → *"When Schwartz asked clients how they felt toward their
  critic, they mostly said they hated it."*
- A one-word caption doing a sentence's job: *"Blended."* → *"That is the part talking."*
- A list of nouns standing in for a claim: *"The critic, the binge, the collapse."*
  Rian's question was *"what does that mean?"* — naming things instead of saying what
  happens, in the hero of all places. The fix was to delete it.
- Instructions where an explanation was owed: *"Ask the guards. Wait for a yes."* →
  *"You talk to the protectors first, ask what they are afraid of, and wait until they
  say yes."*

The rewrite added a hundred words and four words a sentence, and stayed under every
ceiling. Brevity is spent on fewer ideas per screen, never on clipping the sentences
that carry the ideas that stay.

## Required on every page

A page missing any of these is not finished.

- `<a class="backlink" href="/">What that therapy word means</a>` at the top of the hero
- **The `h1` is the idea's one-sentence claim**, in words you could say across a table,
  with the therapy's name left to the eyebrow. The five on the shelf: "Your body decides
  before you do", "Where you look affects how you feel", "Some memories never turn into
  the past", "There are no bad parts", "The thing you do to cope is trying to help".
  Rian's rule after the fifth page, when the shelf carried three shapes (an instruction,
  a noun phrase naming the problem, and the claims): *"they need to be a unit… and a bit
  more descriptive."* A claim tells the reader what the page will argue; a noun phrase
  only names its subject. Set the `<br>`s by hand so it holds three lines at 1512px and
  414px; a nine-word claim needs a page-level `style="font-size: clamp(2.8rem, 9.5vw,
  6.8rem)"` on the `h1` to do that, and that is the only per-page style allowed. The
  `<title>` and the shelf `h3` carry the same sentence, and a section `h2` must not
  repeat it (EMDR's opener had to be rewritten when the title moved onto it).
- A `<p class="term">` between the eyebrow and the `h1`, carrying the word the reader
  came for as people say it ("EMDR", "Polyvagal theory", "TIST"), and the same line
  above the `h3` in the shelf slab. The eyebrow then names the originator on every page
  ("Deb Dana"), followed by the expansion when the term is an abbreviation the sub
  does not spell out ("Janina Fisher · Trauma-Informed Stabilization Treatment"); no
  "for beginners" suffix. The shelf's `.slab-pos` is the originator alone. Rian's note after five pages: the term was
  *"kind of hidden in that eyebrow"*.
- Hero: eyebrow, `.term`, `h1`, `.sub`, `.colourbar`, `.scrollcue`. **The `.sub` opens with what
  the thing is for, in plain words, before the idea or the name:** "A therapy for trauma:
  for when something terrible happened and it keeps coming back as if it were now."
  Rian's rule after reading the first EMDR draft, whose hero opened on the mechanism —
  and all three earlier heroes had the same gap. The landing page's `.shelf-sub` leads the
  same way, but vary the stem: with four blurbs side by side, three opening "A therapy
  for…" read as one template with the nouns swapped (the editor's finding on the landing
  page). "Trauma therapy, for when…" and "For trauma, and for…" still lead with the use.
- Three or more direct quotes from the originator, each attributed, with their role
  given at the first mention ("Deb Dana, trauma therapist") — **and no more than about
  six `.quote` blocks on the page.** The shipped pages carry six to eight. TIST's first
  draft had twelve, and Rian's note was *"too many quotes - that pushes the length
  longer than it needs to be."* The six cut were each restating a lede or a display
  element already on the page (the slide text behind a `.big-fact`, the paper's line
  behind the "I" / "a part of me" pair), and the page lost nothing. Count with
  `grep -c 'class="quote"'`; the script's "attributed quotes" figure counts every
  curly-quoted span, slab voices included, and reads high.
- A short-version section near the end
- A sources list of real, fetched links
- A `<p class="caveat">` at the foot of the sources section stating how well
  evidenced the concept is, and attributing any numbers that are not the
  originator's own words
- A matching `<a class="shelf-slab">` added to `public/index.html`, newest first: the
  colour class cycles `a`, `b`, `c` down the page (so re-letter the ones below it), and
  the slab carries a small monochrome `.glyph` of the page's central figure, drawn in
  `var(--on-field)` — the page's own figure would vanish on its colour field
- The head block every page carries after its meta description: canonical, `og:*`,
  `twitter:card` and the three icon links. Copy it from an existing page and change
  the slug in the three URLs, `og:title` (the h1 claim), `og:description` (the sub's
  first sentence) and `og:image:alt`. The host is `https://therapy-words.com`.
  Keep the meta description under 160 characters.
- `node scripts/build-og.mjs`, run after the slab is in: it renders `public/<slug>/og.png`
  from that slab with headless Chrome and rewrites `sitemap.xml`. Commit the PNG. Look
  at it — a glyph that animates is caught at its `data-reduced-motion-time` frame, so a
  glyph with no static positions or a bad frame value shows up here first.

## Check 1 — the brevity pass

```bash
python3 <skill-dir>/scripts/pattern-check.py public/<slug>/index.html
```

The first block it prints is brevity: paragraph words on the page, words per
sentence, the longest paragraph, paragraph words per section, and the caveat's
length, each against a budget taken from the polyvagal page. Run it on `public/index.html`
too after touching the landing page; only its three-quotes rule does not apply there.
Anything OVER gets cut,
and cut means one of three moves:

- Delete the sentence. Most of the time this is the one.
- Move the point into a display element — a slab, a numbered step, a `.big-fact`
  line, a list with hairline rules — where the reader scans it instead of reading it.
- Split the sentence. A subordinate clause is a second sentence, or nothing.

The one move that is not on the list is rewriting the paragraph so it says the same
thing in fewer words: it comes back longer on the next pass. Polyvagal's opener is
"Am I safe? It answers long before you notice you asked." The whole section is two
lines and a figure.

These moves are for lines the script marks OVER. Once it passes, stop cutting: a page
well under the ceilings has room to spend, and the voice pass will spend it.

## Check 2 — the newbie pass

```bash
python3 <skill-dir>/scripts/pattern-check.py --prose public/<slug>/index.html
```

That prints the visible prose in page order, figures marked, sources dropped. Read it
cold, as someone who has never heard of the concept. The hero sub and the figure
labels are part of it — the hero is where IFS failed this check.

The failure is almost never a bad explanation. It is a missing introduction. Look for:

- A term used before it is defined, including the name of the theory itself
- A person named without their role
- A word that exists only in a small eyebrow label, which body text then refers to
  ("Dana coined the word" — which word?)
- A metaphor pointing at a concept the page never introduced ("applies the brake")
- A pronoun in a quote with nothing on the page to point at. Schwartz's "it's the
  nature of the mind to have them" opened a section where "parts" had not yet been
  said. Put the referent in square brackets: "to have [parts]"

**Then complete the sentence for every section and every figure: "When you ___,
___."** Use only words the page has already given the reader. If the blank needs a
word from your own head, the section is naming its subject instead of saying what
happens. Brainspotting's section 02 drew a route from the eye to "the midbrain" and
Rian's response was *"what does it actually mean though. when we look, ......"* The
page could not finish it. The finished version — *your eyes are wired to the part of
the brain that feels, not the part that talks, so where you look can reach a feeling
that words cannot* — became the lede. The same pass found five more: a brainspot that
"matches" what you carry (it is where the feeling gets strongest), a session whose
0–10 rating was never mentioned again (it is meant to come down), "watch whatever
turns up" (feelings, pictures, memories), "tuned to you" (watches you closely), and
"rides in the tail" (follows). Each fix was a plain verb, and none added a sentence.

Figures fail this test in a specific way: they draw a path, a stack or a map, and
nothing on the page says what travels along it or why the shape matters. A figure
earns its place when the lede next to it states the claim the picture makes.

## Check 3 — the pattern pass

The same script, the blocks after brevity. It measures negation-contrast density
against budget, em dashes split by prose vs list separators, and punctuation variety,
and reports two things it will not fail you on: the spread of `h2` lengths and
plain-negation density. Fix anything it reports as OVER, then read
`01-context/avoid-ai-patterns.md` for the judgement calls it cannot count —
coaching-register lines, rule-of-three pile-ups, metaphors run into the ground.

Keep a negation-contrast only where it corrects a misreading the reader would
otherwise have. Curly quotes and em-dash characters stay: that rule is for spotting
machine-written text, and this is typeset display type.

## Check 4 — the cadence pass

**The script is blind to rhythm, and rhythm is what survives it.** Dispatch the
`editor` agent on the finished page. On brainspotting it found three tells the script
had passed clean, and IFS produced the same three plus a fourth. **Answer its findings
by cutting or by saying the thing plainly, never by joining sentences**, then run the
brevity check again. The editor's instinct is a blog post's: it fixes short uniform
sentences by hanging clauses off them, and on this site that is the regression — the
first brainspotting draft came out of its cadence pass at 17 words a sentence.

- **Headers all the same length.** Ten of eleven `h2`s sat in a 4–9 word aphoristic
  band. Polyvagal breaks its band twice, at "Down where?" and "Small, physical,
  unglamorous." A person writing ten headlines produces one that does not fit.
- **Plain-negation density.** A separate family from negation-contrast, which is why
  the script reports it without failing on it. Nineteen carriers in 1,142 words, with
  "nobody" five times, had the page describing its subject by what was absent.
- **One sentence shape repeating.** Seven sentences ending on a short clause hung off
  ", and". On IFS: three "…, and someone is there" endings, six "X. Then Y." pairs,
  six colon reveals.
- **Command voice.** Four IFS headings were imperatives ("Protectors first. Always.",
  "Get curious. Then wait.") and five of six exercise titles were verbs. Polyvagal's
  headings describe, and its exercise titles are nouns ("A sigh", "Your voice"). The
  page had turned into instructions, which is the same failure the voice pass catches
  from the other side.

Give the agent `context hint: personal` (its path table does not cover this repo) plus
four scoping rules, or it will report the page's own conventions as findings: quoted
material is the originator's wording and not the page's style; curly quotes and
em-dash characters are typeset display type; sources-list em dashes are separators;
SVG `<text>` labels are visible prose but SVG internals are not.

Weigh its rewrites rather than applying them. On brainspotting one overclaimed past
the evidence and one wanted invented dates in a label — both would have shipped a
factual error to fix a style one. **Its "number without a source" flags have been
wrong on all three pages** ("ten minutes" was Grand's own; "twenty to forty passes"
was the VA page in the sources list; "decades" was Schwartz's "30 years" in the
transcript) — check the sources before hedging a number, and if the pointer is real
but implicit, make the source description name it.

## Check 5 — the voice pass

Last, after the cadence cuts, with the prose dump from check 2. Read every lede,
caption, step and list item aloud as the person in **The voice** above. Anything you
would not say to someone across a table — a fragment with no speaker, a one-word
caption, a noun list where a claim should be, an order where an explanation was owed —
gets said in full. This pass is allowed to add words; the ceilings are the only limit,
and the script is run once more when it is done.

## Done means

- `pattern-check.py` reports nothing over budget, brevity block included, and it was
  run again after the cadence and voice passes
- Every beat you kept reads cold without assuming anything, and "When you ___, ___"
  completes for each section from the page's own words
- The `editor` agent has run and its cadence findings are answered
- Every lede reads as one person calmly explaining, in full sentences
- Every required item above is present
- Rian has seen the prose
- The live URL is byte-identical to the repo file

## Red flags

| Thought | Reality |
|---|---|
| "It reads fine, I can skip the passes" | All five passes found real problems on a page that read fine. Run them. |
| "The checker passes, so the page is done" | IFS passed at 7.6 words a sentence and Rian sent it back as "studying". The script holds ceilings; the voice pass holds the floor. |
| "The search summary covers it" | Summaries drop the quotable lines. Fetch the source. |
| "The transcript has a great story" | The story is the source, not the page. One line and the figure. A 27-page transcript put a 108-word narrative at the top of brainspotting. |
| "The editor wants this sentence longer" | It wants a clause hung off it. Say the thing plainly instead. Rhythm on this site comes from a two-word line next to a picture, not from a subordinate clause. |
| "The figure shows the mechanism" | A route with no stated claim is a diagram of nothing. Write the "when you ___, ___" sentence first; if the picture does not make that sentence easier to believe, redraw it. |
| Naming the anatomy ("the midbrain") | The reader has no picture of it. Say what it does — the part of the brain that feels — and let the sources carry the name. |
| "The evidence is probably solid" | Brainspotting's strongest trial is one therapist in her own practice. Look it up every time. |
| Typing a DOI or URL you did not fetch | You will guess a plausible one. Resolve every citation through `api.crossref.org/works/<doi>`, which returns title and authors so you can check it is the right paper. When the originator's paper has no Crossref record at all (Fisher's 2017 TIST paper is a PDF on her own site), link that PDF and say in the source description whose site it is. |
| "I'll add the index entry after" | The page is unreachable until you do. Do it before deploying. |
| Reaching for `border-radius` on a content block | Flat and hard-edged. Radius belongs to circles only. |
| Adding a scroll-reveal or fade-in | Content is visible on arrival. |
| "I verified that" (without having run it) | Byte-compare live against the repo. Say what you actually checked. |

## Traps

The CSS and SVG failures that cost real time are in `reference/css-traps.md`, along
with how to preview locally and how to verify a deploy. Read it before debugging a
layout that renders but behaves wrong.


