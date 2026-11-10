# Avoid AI-Sounding Language

*Last updated: 2026-11-10*

To keep writing natural and human, avoid these telltale AI patterns. Any single instance might be fine. The problem is when multiple patterns appear together or when one is used repeatedly.

## How to use this list

These tells have a half-life. Models are trained on human feedback and drop the habits people flag publicly, so any entry here can go stale without warning. Em dashes are the clearest case. ChatGPT leaned on them heavily and then dropped them; Claude kept the habit through Opus 5 and nearly stopped with Opus 5.5 in September 2026; Wikipedia's "Signs of AI writing" page now files em-dash overuse under historical indicators. Re-check anything here against current model behaviour before treating it as settled.

Claims below that name a model carry a date. The punctuation, word-length, and sentence-length findings come mostly from one test published in July 2026 (it did not say which model versions it used), and newer models already diverge from it. Tells now differ by model version more than by vendor, so know which model drafted a text before applying a check that only fits some of them.

Two rules that keep this list from being applied badly:

* **Density decides.** A single match proves nothing. Claiming a text is AI-written because it says "delve" is like claiming one is by Jane Austen because it says "imprudence." Count how often a pattern repeats per thousand words, and count related patterns as one family.
* **Absence is a tell too.** Most of this file catalogues doing too much of something. Two of the strongest current signals are missing things: parenthetical asides and variety in sentence length. Editing only by subtraction can push a draft further into machine territory.

## Highest-signal checks right now

Run these first. The rest of the file is the long tail.

1. Any specific number that was not measured. See Fabricated metrics below -- this outranks every style concern in the file.
2. Negation-contrast density across the whole "not X but Y" family, including the softer carriers. More than about one per 600 words (a house rule of thumb) means each one needs to pass the keeper test.
3. Salience flags and mannered metaphor: "this matters", "matters because", "earns its keep". These are the most-measured tics of current Claude models.
4. Long Latinate words, nominalisations, and scientific register where a plain word would carry the sentence.
5. Punctuation starvation -- few parenthetical asides and, in text from older models, too few commas and semicolons. A draft with no em dashes proves nothing in either direction now.
6. Sentences that all run the same length, long or short, with nothing breaking the run.
7. Templated repetition: rule of threes, bold-label bullets, the same construction in every parallel item.

## Fabricated metrics [CRITICAL]

NEVER quote a specific number as fact unless it comes from verifiable data. Time savings, cost savings, productivity gains, and percentages must be either (a) measured or (b) explicitly framed as estimates.

| Fabricated precision | Honest framing |
|---|---|
| "Reduced triage time from 60 minutes to 5 minutes" | "Triage takes a fraction of the time it used to" |
| "Saved 80% of revision time" | "Each revision cycle got noticeably shorter" |
| "10x faster than manual process" | "Meaningfully faster -- the difference is obvious" |
| "Producing pages in minutes that previously took hours" | "What used to take most of an afternoon now takes one session" |

If a number is an estimate, say so: "roughly half the time", "a fraction of what it took before", "cut the cycle from hours to minutes." Vague-but-honest beats precise-but-fabricated. "Significantly faster" is better than "12x faster" when you have not measured it.

This applies to all output: docs, emails, blog posts, summaries. The temptation is strongest when describing productivity gains from tools or process changes.

## Overused words

This list mixes eras. Delve, tapestry, garner, intricate, pivotal, and underscore are 2023-24 tells that current models rarely produce (Wikipedia files them under GPT-4-era vocabulary). Keep avoiding them, but finding none says nothing about a draft: a November 2026 count of this vault found 46 of the 56 words below absent from three weeks of recent prose. Treat the list as a regression check and spend the attention on constructions.

* **Verbs:** delve, underscore, highlight, showcase, leverage, utilize, facilitate, foster, navigate, garner, craft, harness, boast, surpass
* **Adjectives:** intricate, meticulous, swift, adept, liminal, spectral, crucial, pivotal, robust, seamless, transformative, groundbreaking, cutting-edge, nuanced, multifaceted, sharp (as in "a sharp piece," "a sharp essay" -- AI's go-to flattering adjective for someone else's writing), load-bearing (any use -- "the load-bearing question," "the load-bearing assumption," "this detail is load-bearing," "the load-bearing part of the argument." A go-to AI move for dressing up any claim as structurally critical. Avoid the word entirely; say what actually depends on what)
* **Nouns:** tapestry, journey, echo, whisper, shadow, ghost(s), landscape (as catch-all: "competitive landscape," "digital landscape," etc.), realm, paradigm, ecosystem, synergy, seam(s) (metaphor for the gaps between systems or teams -- name the actual gap instead), throughline (as in "the throughline is," "the real throughline" -- AI's go-to word for naming a connecting thread; say what actually connects the things), shape (as in "the same shape," "a different shape," "shaped like," "the shape of the problem" -- vague geometric metaphor standing in for a concrete comparison; say what the actual similarity is, or drop the comparison)
* **Atmosphere words:** quiet, hum/humming, woven/weave -- note: "quiet" is an especially common AI crutch (quiet confidence, quiet rebellion, quietly growing). Also: "deeply," "fundamentally"
* **Filler adverbs:** remarkably, genuinely, truly, incredibly, arguably -- these pose as intensifiers but weaken the claim. "The output was useful" is stronger than "The output was genuinely useful"

## Pretentious diction

One of the clearest markers of machine prose is word weight. LLMs reach for long words (eight letters or more), Latinate suffixes, and scientific register far more often than human journalists or novelists do. In the July 2026 test behind this section Gemini and Claude leaned on it hardest; nobody has published a word-weight ranking for the current model versions.

* **Polysyllable inflation:** "significant", "increasingly", "consequences", "substantial", "considerable" doing work that "big", "more", or "results" would do better
* **Rare-word reaching:** "interdependence", "reindustrialisation", "proliferation" -- real words that nobody says out loud
* **Scientific register in non-scientific writing:** "parameter", "methodology", "framework", "mechanism" applied to things that aren't experiments
* **Nominalisations:** verbs turned into nouns -- "expansion" for "expand", "utilisation" for "use", "implementation" for "build". The sentence loses its verb and gains a noun that does no work
* **Mannered metaphor:** a flourish standing in for a literal phrase -- "this point earns its keep" for "this point still matters", "a dial worth turning" for "a parameter worth varying", "earns its place". This is where the habit shows in current Claude models: Anthropic's Fable 5.1 prompting guide names it as the pattern to suppress, and "earns its place" still turned up in Opus 5.5 output after the September 2026 style fixes (Arize). The metaphor brings connotations the sentence did not choose. When a literal phrase is available, use it

Orwell called this "pretentious diction": dressing up simple statements with complicated words and jargon to sound clever, on the belief that "Latin or Greek words are grander than Saxon ones."

**Scoping for work writing.** "Parameter", "methodology", and "mechanism" are sometimes the correct words in technical infrastructure docs, and swapping them for folksier ones makes the writing worse. The test is whether a shorter word carries the same meaning, and how many heavy words stack up in one paragraph.

## Overused phrases

* "It's worth noting that..." / "It bears mentioning" / "Notably" / "Interestingly" / "Importantly" -- filler transitions that signal nothing
* "In today's [fast-paced/ever-evolving/digital] [world/landscape/age]..."
* "Cannot be overstated"
* "A testament to..."
* "Paving the way"
* "Unlock the potential of..."
* "As mentioned above/earlier"
* "At the end of the day"
* "What stood out to me..." / "jumped out at me" / "caught my attention" / "what I keep coming back to" / "I keep thinking about" -- recycled reaction framing that becomes a tic across posts
* "In conclusion" / "To sum up" / "In summary" / "In short" -- competent writing doesn't need to announce it's concluding. The reader can feel it. "In short" is the live one: Opus 5.5 used it about eleven times as often as Opus 5 across 1,000 responses (Pangram, Sept 2026)
* "This matters" / "matters because" / "why X matters" / "the distinction matters" -- salience flags that assert importance instead of showing the consequence. Graphite measured "matters because" at 132 times the human rate for Opus 5 and 357 times for GPT-6 Astra (Sept 2026); Arize counted salience flags at 1.67 per 1,000 words in Opus 5 output and 0.93 in Opus 5.5, so the fix halved them and left them common. Say what breaks, changes, or costs money
* "the same question wearing different clothes" / "X in disguise" / "X dressed up as Y" -- a costume metaphor standing in for "these are the same thing." Say it plainly: "ask the same thing," "are the same question"

## Word-level substitution tics

* **The "serves as" dodge:** replacing "is" with "serves as," "stands as," "marks," or "represents." LLM prose underuses the plain copula ("The building serves as a reminder" instead of "The building is a reminder"). Corollary: "boasts," "features," "offers," and "carries" as substitutes for "has" ("The gallery boasts 3,000 square feet" instead of "The gallery has 3,000 square feet"; "a bigger share of PMs than most orgs carry" instead of "than most orgs have"). Often the comparison works with no verb at all -- "a bigger share of PMs than any org I've worked in"
* **Abstractions that travel, carry, or come along:** "two rules travel with it," "a caveat comes with the territory," "the risk rides along" -- personifying a rule, risk, or condition so it moves on its own. Cousin of the "carries" dodge above. Say what the reader must do: "check two things first"
* **Synonym cycling (elegant variation):** swapping synonyms for the same noun across consecutive sentences to avoid repetition -- "The protagonist faces challenges. The main character must overcome obstacles. The central figure eventually triumphs." Just use the same word. Real writers repeat nouns; AI cycles through alternatives. Mostly an older-model habit now (Wikipedia lists it as a historical indicator), so it is a low-priority check
* **Superficial "-ing" analysis:** tacking a present participle phrase onto a sentence to inject hollow significance -- "highlighting its importance," "reflecting broader trends," "underscoring its role as a dynamic hub"
* **Invented concept labels:** compounding abstract problem-nouns that sound analytical without being grounded -- "supervision paradox," "acceleration trap," "workload creep." These function as rhetorical shorthand: name a thing, skip the argument
* **Vague attributions:** "Experts argue..." / "Industry reports suggest..." / "Observers have cited..." -- invoking unnamed authorities instead of being specific. If you can't name the source, you don't have one. The positive corollary is worth stating: name and quote real people. LLM prose is thin on quotation because bots don't talk to sources, so a draft carrying no named voice reads machine-made even when every sentence is clean

## Sentence structures to avoid

* **"It's not X -- it's Y"** -- the classic AI rhetorical move. Also catches the two-sentence variant ("It isn't X. It's Y."), the causal variant ("not because X, but because Y"), and the em-dash dismissal ("X -- not Y"). **Count the quiet variants in the same set: "rather than" (and "rather than merely", "rather than simply"), "instead of", "not simply", "not only X but also Y", "less about X and more about Y", "less like X and more like Y".** They are the same negation-contrast wearing a softer word, and they are what survives after the loud ones are edited out -- on 2026-08-11 a doc went from 16 `, not` constructions to 1 across two editor passes while carrying 16 unnoticed `rather than`s doing identical work. A useful ratio: more than about one negation-contrast per 600 words is a template regardless of which word carries it. That figure is a house rule of thumb with no outside measurement behind it, so use it to trigger a pass over each instance and let the keeper test decide. The family is still live in every current model: Graphite (Sept 2026) measured "rather than merely" at 160 times the human rate for Opus 5 and found GPT-6 Astra talking about what things aren't about 12 times as often as human writers. **Check parallel items as a set, not just individually.** In bullets, section headers, or list items, the same negation-contrast repeating across every item is the tell even when each one is individually defensible -- three bullets reading "ships outcomes *rather than* features," "measures impact, *not only* velocity," "owns the roadmap, *not just* the backlog" is a template, not three sentences. Keep the contrast in the one place it carries the claim; make the rest positive assertions. **The keeper test:** a negation earns its place when it corrects a misreading the reader would otherwise have (a mischaracterisation of a named person, a figure that is cumulative and not annual). If the positive form loses nothing, use the positive form
* **"No X. No Y. Just Z."** -- dramatic countdown that builds false tension by negating before revealing the point
* **"The X? A Y."** -- self-posed rhetorical question answered immediately ("The result? Devastating." "The worst part? Nobody saw it coming."). The model asks a question nobody was asking, then answers it for dramatic effect
* **Excessive rule of threes** -- triplets in every paragraph (e.g., "Products impress people; platforms empower them. Products solve problems; platforms create worlds."). In a July 2026 test ChatGPT and Claude leaned on the rule of three, "not X but Y", and "not only but also" more heavily than other models or human writers. Since then Opus 5.5 cut its contrast reframes by about half while its three-part lists rose by about a third (Arize, Sept 2026), so in a Claude draft check triplets at least as hard as contrasts
* **Benefit without a cost:** "X without requiring Y", "without losing", "without sacrificing" -- a promised gain that skips the trade-off. GPT-6 Astra uses "without requiring" at 70 times the human rate, and Claude and Gemini share the milder forms (Graphite, Sept 2026). If there is a trade-off, name it; if there isn't, drop the clause
* **Anaphora abuse** -- repeating the same sentence opening multiple times in quick succession ("They could expose... They could offer... They could provide... They could create...")
* **"Honestly?" as punctuation** -- mid-sentence ("And honestly? That's amazing.") or as an opener ("Honestly? Most people don't follow up."). Drops a false beat of candor before something completely unremarkable
* **Dismissive formula:** "an X with Y and Z" (e.g., "a Reddit troll with Wi-Fi and billions")
* **Synesthesia abuse:** giving abstract concepts sensory qualities (grief that "tastes of metal," ideas that "smell of")
* **False ranges:** "from X to Y" where X and Y aren't on any real scale ("from innovation to cultural transformation" -- what's in between? Nothing)
* **Announcing the punchline:** "Here's the kicker." "But here's the thing." "The best part?" -- promises a payoff that rarely arrives
* **"Here's the move":** "Here's the move." "The move is X." "The play here is..." "The smart move is..." -- packaging a recommendation as a slick reveal instead of just stating it. Say what to do and why
* **Setup without delivery:** "I'm going to state this as clearly as possible" / "Here's the part most people miss" -- real directness doesn't announce itself
* **Soft announcing:** "Here's something I've been thinking about:" / "I think about it like this:" / "My advice is this:" / "The idea is simple:" -- quieter variants of announcing the punchline. Just say the thing
* **Coaching/therapy mode:** "You're not imagining it." "You're not alone." "You're not broken." -- unsolicited validation that nobody asked for
* **"Sit with it":** "Something to sit with." "That's worth sitting with." "Let that sit." "Do you want to sit with that for a while?" -- false-profundity framing that asks the reader to dwell on a point instead of earning the weight. Just make the point
* **Safe truths that teach nothing:** "Consistency is important." "Building relationships takes time." -- accurate, non-controversial, impossible to disagree with, zero information
* **Narrating the effort:** "Building X takes time." "Each one required reading through Y and Z to extract the patterns." -- describing how hard something was to build instead of just showing the result. Skip the labor and get to the payoff
* **Vague evolution openers:** "The system keeps evolving." "Things continue to develop." "The landscape is shifting." -- detached, impersonal throat-clearing. Be specific about what changed, or use first person
* **Abstract verdict sentences:** a concept noun as the subject, a verdict verb, and a vague object -- "Attach to the paid plan decides whether the portfolio grows." "Recovering the revenue depends on new usage." "New usage needs its own measure." "X is the biggest lever." They sound like a topic sentence but state no finding; the reader has to read the paragraph to learn what is happening. Common as bold paragraph leads in analysis docs. Say the finding with its actor and number ("Fewer paid-plan accounts buy the add-on than a year ago"), or the conclusion the paragraph reaches
* **Provenance clutter in decision documents:** research-note habits carried into prose written for a decision-maker. Four carriers: inline attribution with a date ("Dana said on Sept 22 that…", "Sam wrote on Sept 23…"); a caveat about the evidence placed beside its own figure ("That is a model result; we haven't checked it against renewals", "That is an expectation, not a measured effect"); an alternate-basis parenthetical after a number ("($1.2M on the alternate growth basis used in §4)"); and more than one § or Appendix pointer in a paragraph. Each is correct and each makes the sentence harder to read than the claim deserves. State the finding; put who said it, the method caveat and the second basis in a sources or method appendix, and keep the uncertainty for one risks section. Briefings have their own version: a selection trailer ("Selected because you own this product.", "Selected as an ownership change.") tacked onto an item that already shows why it is there. Leave the selection reasoning out of the reader's copy

## Structural patterns

* **Uniform sentence rhythm** -- every sentence hits the same beat, same length, same cadence. Human writing uses variety: short punches, then longer stretches. The specific failure to look for is a run of evenly sized sentences with nothing interrupting it. Which way it runs depends on the model. The models in a July 2026 test ran long ("and" was their single most overused word), and Fable 5.1 still runs long and dense by Anthropic's own account. Opus 5.5 runs short and even: about 12.5 words a sentence, with less variation than Opus 5 (Pangram, Sept 2026). GPT-6-era output is described the same way. Sameness is the tell in both cases, and chopping long sentences to a uniform short length only swaps one profile for the other
* **Short punchy fragments as standalone paragraphs** -- the opposite problem: breaking every thought into its own line for manufactured emphasis ("He published this. Openly. In a book. As a priest."). No real person writes first drafts this way. This is a separate failure from the one above and the two don't cancel out. A draft needs some short sentences. Giving every sentence its own paragraph is a different problem
* **Faux balance** -- acknowledging "both sides" or admitting a concern, then proceeding exactly as planned. Nothing is actually weighed or traded off. Includes the "Despite its challenges..." formula: acknowledge problems only to immediately dismiss them
* **Too-tidy internal references** -- perfect callback loops, paragraphs that weave back to the intro's framing. Human writers leave some threads hanging
* **Arguments that teleport** -- logic jumps mid-paragraph where a conclusion appears without showing how it was reached. Sounds fluent enough to slip past a quick read
* **Missing emotional spikes** -- maintaining a neutral temperature even when the topic demands a stance. Competent but flat
* **Metaphors that almost land** -- comparisons that sound clever but don't actually map to the subject. Also: latching onto a single metaphor and beating it into the ground across an entire piece instead of using it once and moving on
* **Excessive coherence** -- every detail serves the argument, every example fits perfectly. Real writing has loose ends, throwaway details, oddly specific but unimportant facts
* **Listicle in a trench coat** -- numbered points disguised as continuous prose ("The first takeaway is... The second takeaway is... The third takeaway is..."). Still a list, just wearing a paragraph costume
* **Inline-header bullet lists** -- bullet points where each item starts with a bolded label followed by a colon, then a sentence restating the label. "**Speed:** Output is fast. **Quality:** Results are high quality." Flatten into prose or drop the redundant headers. Expect more of these from Claude, not fewer: Opus 5.5 nearly doubled its bullet rate against Opus 5 (Pangram, Sept 2026) and used about 2.5 times as many bold lead-ins (Arize). A label that helps a reader scan a recurring report is fine; one that restates its own sentence is the problem
* **Semicolon ledgers** -- one line carrying three or more unrelated updates joined by semicolons ("A to answer on priority; B to send the one-pager; owner for the export destination still open"). Common in session logs and handoff notes, where it makes the note read as assembled from slots. Split unrelated updates into sentences or a real list, and keep the semicolons that join related clauses
* **Fragmented headers** -- a heading followed by a one-sentence paragraph that just restates the heading before the real content begins. "## Performance\n\nSpeed matters.\n\nWhen users hit a slow page..." Cut the throat-clearing sentence and start with the actual point
* **Diff-anchored writing** -- describing something as a change ("This function was added to replace the previous approach...") when the document should describe the current state. Unless it's a changelog or migration guide, write about what the thing *is*, not what it replaced
* **One-point dilution** -- making a single argument and restating it 10 different ways across thousands of words. An 800-word argument becomes 4000 words of circular repetition
* **Fractal summaries** -- summarizing at every level of the document. Every subsection gets a summary, every section gets a summary, the document itself gets a summary. Also: "And so we return to where we began"
* **Historical analogy stacking** -- rapid-fire listing of companies or tech revolutions to build false authority ("Apple didn't build Uber. Facebook didn't build Spotify. Stripe didn't build Shopify.")
* **Repeated scaffolding across a series** -- reusing the same section structure from post to post (e.g., every entry ending with a "What I've Learned" header followed by a bold-label bullet list). Within one piece it's fine; across a series of related posts the sameness reads as templated. Vary the headers, lead-ins, and list/prose form between posts. (A single-document editor pass can't catch this -- it's a corpus-level check the caller has to make.)

## Punctuation and formatting

* **Too little punctuation** -- in a July 2026 test LLM prose carried fewer commas and semicolons than human writing and hardly any parentheses. The parenthesis gap is the part that has held up: Graphite's September 2026 study found human writers use parenthetical asides far more often than every current model. The comma finding no longer generalises, since GPT-6-era output is described as heavy on commas and periods. Four rules in this file -- em dashes, colons, horizontal rules, standalone fragments -- all push in the subtractive direction, so applying them mechanically can move a draft toward the machine profile. A November 2026 count of this vault showed that drift (cause untested): against May to August prose, parentheses fell by a third, sentences of five words or fewer fell from 17% of the total to 11%, and "and" rose by more than half. Strip punctuation that is decorative; keep punctuation that carries a clause
* **Em dashes** -- no longer a reliable tell in either direction. ChatGPT dropped them first. Claude kept the habit longer: measurements of Opus 5 ranged from about the human rate (Graphite) to 12.9 per 1,000 words (Arize), and the same Arize test put Opus 5.5 at 0.05. Rates now vary by model version (Pangram, Nov 2026: GPT-6.1 Sol 1.32 per 1,000 words, Gemini 4 Argon 0.85, Haiku 5.5 under 0.01), and nobody has published a figure for Fable. Several per paragraph is still a fault. Zero is not a target: a dash that carries a real interruption is fine, a draft with none proves nothing, and swapping each one for a comma or an "and" only moves the tell
* **Overuse of horizontal rules** -- don't break up sections with horizontal rules
* **Overuse of colons** -- using colons to introduce lists or explanations where a period would do
* **Unicode decoration** -- smart arrows (→), curly quotes, and other special characters that can't be easily typed on a standard keyboard. Real writers typing in a text editor produce straight quotes and -> or =>. Curly quotes on their own are a weak signal: GPT-6.1 Sol put curly apostrophes in 74% of its answers against 0% for Haiku 5.5 (Pangram, Nov 2026), and Word and macOS autocorrect produce them for human writers too

## Tonal pitfalls

* **Overwrought sincerity** -- "woven into your daily rhythm," false warmth that reads as manufactured
* **Overeager enthusiasm** -- wide-eyed excitement about things that don't warrant it
* **Gesturing at depth** -- piling metaphors that collapse into nonsense instead of making a specific point
* **Atmosphere cosplay** -- describing everything as ghostly, echoing, or quiet when it isn't. Borrowed mood that doesn't match the subject
* **Corporate-inspirational filler** -- says everything and nothing ("revolutionize the way," "breakthrough advancement," "will define the next era of computing")
* **Performative empathy** -- unsolicited validation in contexts that don't call for it
* **Patronizing analogy** -- "Think of it as..." / "Think of it like a highway system for data." Defaults to teacher mode and assumes the reader needs a metaphor
* **Futurism invitation** -- "Imagine a world where..." followed by a list of wonderful things that will happen if the reader agrees with the premise
* **Pedagogical hand-holding** -- "Let's break this down." "Let's unpack this." "Let's explore this idea further." Assumes a teacher-student dynamic even for expert audiences
* **Asserting clarity instead of demonstrating it** -- "The truth is simple." "The reality is straightforward." "History is unambiguous on this point." If you have to tell the reader your point is clear, it probably isn't
* **False vulnerability** -- simulated self-awareness that reads as performative ("And yes, I'm openly in love with the platform model"). Real vulnerability is specific and uncomfortable; AI vulnerability is polished and risk-free
* **Stakes inflation** -- everything is the most important thing ever. A blog post about API pricing becomes a meditation on the fate of civilization
