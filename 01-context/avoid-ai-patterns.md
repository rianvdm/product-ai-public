# Avoid AI-Sounding Language

*Last updated: 2026-08-16*

To keep writing natural and human, avoid these telltale AI patterns. Any single instance might be fine. The problem is when multiple patterns appear together or when one is used repeatedly.

## How to use this list

These tells have a half-life. Models are trained on human feedback and drop the habits people flag publicly, so any entry here can go stale without warning. ChatGPT used an em dash in almost every sentence until recently; asked today whether AI overuses the dash, it now says they are "best used sparingly." Re-check anything here against current model behaviour before treating it as settled.

Two rules that keep this list from being applied badly:

* **Density decides.** A single match proves nothing. Claiming a text is AI-written because it says "delve" is like claiming one is by Jane Austen because it says "imprudence." Count how often a pattern repeats per thousand words, and count related patterns as one family.
* **Absence is a tell too.** Most of this file catalogues doing too much of something. Two of the strongest current signals are missing things: punctuation and short sentences. Editing only by subtraction can push a draft further into machine territory.

## Highest-signal checks right now

Run these first. The rest of the file is the long tail.

1. Any specific number that was not measured. See Fabricated metrics below -- this outranks every style concern in the file.
2. Negation-contrast density across the whole "not X but Y" family, including the softer carriers. More than about one per 600 words is a template.
3. Long Latinate words, nominalisations, and scientific register where a plain word would carry the sentence.
4. Punctuation starvation -- too few commas, semicolons, and parentheses. For anything Claude drafted, also check em dashes in the other direction.
5. Sentences that all run long at the same length, with nothing short breaking the run.
6. Templated repetition: rule of threes, bold-label bullets, the same construction in every parallel item.

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

* **Verbs:** delve, underscore, highlight, showcase, leverage, utilize, facilitate, foster, navigate, garner, craft, harness, boast, surpass
* **Adjectives:** intricate, meticulous, swift, adept, liminal, spectral, crucial, pivotal, robust, seamless, transformative, groundbreaking, cutting-edge, nuanced, multifaceted, sharp (as in "a sharp piece," "a sharp essay" -- AI's go-to flattering adjective for someone else's writing), load-bearing (any use -- "the load-bearing question," "the load-bearing assumption," "this detail is load-bearing," "the load-bearing part of the argument." A go-to AI move for dressing up any claim as structurally critical. Avoid the word entirely; say what actually depends on what)
* **Nouns:** tapestry, journey, echo, whisper, shadow, ghost(s), landscape (as catch-all: "competitive landscape," "digital landscape," etc.), realm, paradigm, ecosystem, synergy, seam(s) (metaphor for the gaps between systems or teams -- name the actual gap instead), throughline (as in "the throughline is," "the real throughline" -- AI's go-to word for naming a connecting thread; say what actually connects the things), shape (as in "the same shape," "a different shape," "shaped like," "the shape of the problem" -- vague geometric metaphor standing in for a concrete comparison; say what the actual similarity is, or drop the comparison)
* **Atmosphere words:** quiet, hum/humming, woven/weave -- note: "quiet" is an especially common AI crutch (quiet confidence, quiet rebellion, quietly growing). Also: "deeply," "fundamentally"
* **Filler adverbs:** remarkably, genuinely, truly, incredibly, arguably -- these pose as intensifiers but weaken the claim. "The output was useful" is stronger than "The output was genuinely useful"

## Pretentious diction

The clearest current marker of machine prose is word weight. LLMs reach for long words (eight letters or more), Latinate suffixes, and scientific register far more often than human journalists or novelists do. Gemini and Claude lean on it hardest.

* **Polysyllable inflation:** "significant", "increasingly", "consequences", "substantial", "considerable" doing work that "big", "more", or "results" would do better
* **Rare-word reaching:** "interdependence", "reindustrialisation", "proliferation" -- real words that nobody says out loud
* **Scientific register in non-scientific writing:** "parameter", "methodology", "framework", "mechanism" applied to things that aren't experiments
* **Nominalisations:** verbs turned into nouns -- "expansion" for "expand", "utilisation" for "use", "implementation" for "build". The sentence loses its verb and gains a noun that does no work

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
* "In conclusion" / "To sum up" / "In summary" -- competent writing doesn't need to announce it's concluding. The reader can feel it
* "the same question wearing different clothes" / "X in disguise" / "X dressed up as Y" -- a costume metaphor standing in for "these are the same thing." Say it plainly: "ask the same thing," "are the same question"

## Word-level substitution tics

* **The "serves as" dodge:** replacing "is" with "serves as," "stands as," "marks," or "represents." AI avoids simple copulas because its repetition penalty pushes it toward fancier constructions ("The building serves as a reminder" instead of "The building is a reminder"). Corollary: "boasts," "features," "offers," and "carries" as substitutes for "has" ("The gallery boasts 3,000 square feet" instead of "The gallery has 3,000 square feet"; "a bigger share of PMs than most orgs carry" instead of "than most orgs have"). Often the comparison works with no verb at all -- "a bigger share of PMs than any org I've worked in"
* **Synonym cycling (elegant variation):** swapping synonyms for the same noun across consecutive sentences to avoid repetition -- "The protagonist faces challenges. The main character must overcome obstacles. The central figure eventually triumphs." Just use the same word. Real writers repeat nouns; AI cycles through alternatives
* **Superficial "-ing" analysis:** tacking a present participle phrase onto a sentence to inject hollow significance -- "highlighting its importance," "reflecting broader trends," "underscoring its role as a dynamic hub"
* **Invented concept labels:** compounding abstract problem-nouns that sound analytical without being grounded -- "supervision paradox," "acceleration trap," "workload creep." These function as rhetorical shorthand: name a thing, skip the argument
* **Vague attributions:** "Experts argue..." / "Industry reports suggest..." / "Observers have cited..." -- invoking unnamed authorities instead of being specific. If you can't name the source, you don't have one. The positive corollary is worth stating: name and quote real people. LLM prose is thin on quotation because bots don't talk to sources, so a draft carrying no named voice reads machine-made even when every sentence is clean

## Sentence structures to avoid

* **"It's not X -- it's Y"** -- the classic AI rhetorical move. Also catches the two-sentence variant ("It isn't X. It's Y."), the causal variant ("not because X, but because Y"), and the em-dash dismissal ("X -- not Y"). **Count the quiet variants in the same set: "rather than", "instead of", "not only X but also Y", "less about X and more about Y".** They are the same negation-contrast wearing a softer word, and they are what survives after the loud ones are edited out -- on 2026-08-11 a doc went from 16 `, not` constructions to 1 across two editor passes while carrying 16 unnoticed `rather than`s doing identical work. A useful ratio: more than about one negation-contrast per 600 words is a template regardless of which word carries it. **Check parallel items as a set, not just individually.** In bullets, section headers, or list items, the same negation-contrast repeating across every item is the tell even when each one is individually defensible -- three bullets reading "ships outcomes *rather than* features," "measures impact, *not only* velocity," "owns the roadmap, *not just* the backlog" is a template, not three sentences. Keep the contrast in the one place it carries the claim; make the rest positive assertions. **The keeper test:** a negation earns its place when it corrects a misreading the reader would otherwise have (a mischaracterisation of a named person, a figure that is cumulative and not annual). If the positive form loses nothing, use the positive form
* **"No X. No Y. Just Z."** -- dramatic countdown that builds false tension by negating before revealing the point
* **"The X? A Y."** -- self-posed rhetorical question answered immediately ("The result? Devastating." "The worst part? Nobody saw it coming."). The model asks a question nobody was asking, then answers it for dramatic effect
* **Excessive rule of threes** -- triplets in every paragraph (e.g., "Products impress people; platforms empower them. Products solve problems; platforms create worlds."). ChatGPT and Claude lean on the rule of three, "not X but Y", and "not only but also" more heavily than other models or human writers do
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

## Structural patterns

* **Uniform sentence rhythm** -- every sentence hits the same beat, same length, same cadence. Human writing uses variety: short punches, then longer stretches. The specific failure to look for is a run of long, evenly sized sentences with nothing short interrupting it. Bots default long -- "and" is their single most overused word -- and they rarely break a paragraph with a five-word sentence
* **Short punchy fragments as standalone paragraphs** -- the opposite problem: breaking every thought into its own line for manufactured emphasis ("He published this. Openly. In a book. As a priest."). No real person writes first drafts this way. This is a separate failure from the one above and the two don't cancel out. A draft needs some short sentences. Giving every sentence its own paragraph is a different problem
* **Faux balance** -- acknowledging "both sides" or admitting a concern, then proceeding exactly as planned. Nothing is actually weighed or traded off. Includes the "Despite its challenges..." formula: acknowledge problems only to immediately dismiss them
* **Too-tidy internal references** -- perfect callback loops, paragraphs that weave back to the intro's framing. Human writers leave some threads hanging
* **Arguments that teleport** -- logic jumps mid-paragraph where a conclusion appears without showing how it was reached. Sounds fluent enough to slip past a quick read
* **Missing emotional spikes** -- maintaining a neutral temperature even when the topic demands a stance. Competent but flat
* **Metaphors that almost land** -- comparisons that sound clever but don't actually map to the subject. Also: latching onto a single metaphor and beating it into the ground across an entire piece instead of using it once and moving on
* **Excessive coherence** -- every detail serves the argument, every example fits perfectly. Real writing has loose ends, throwaway details, oddly specific but unimportant facts
* **Listicle in a trench coat** -- numbered points disguised as continuous prose ("The first takeaway is... The second takeaway is... The third takeaway is..."). Still a list, just wearing a paragraph costume
* **Inline-header bullet lists** -- bullet points where each item starts with a bolded label followed by a colon, then a sentence restating the label. "**Speed:** Output is fast. **Quality:** Results are high quality." Flatten into prose or drop the redundant headers
* **Fragmented headers** -- a heading followed by a one-sentence paragraph that just restates the heading before the real content begins. "## Performance\n\nSpeed matters.\n\nWhen users hit a slow page..." Cut the throat-clearing sentence and start with the actual point
* **Diff-anchored writing** -- describing something as a change ("This function was added to replace the previous approach...") when the document should describe the current state. Unless it's a changelog or migration guide, write about what the thing *is*, not what it replaced
* **One-point dilution** -- making a single argument and restating it 10 different ways across thousands of words. An 800-word argument becomes 4000 words of circular repetition
* **Fractal summaries** -- summarizing at every level of the document. Every subsection gets a summary, every section gets a summary, the document itself gets a summary. Also: "And so we return to where we began"
* **Historical analogy stacking** -- rapid-fire listing of companies or tech revolutions to build false authority ("Apple didn't build Uber. Facebook didn't build Spotify. Stripe didn't build Shopify.")
* **Repeated scaffolding across a series** -- reusing the same section structure from post to post (e.g., every entry ending with a "What I've Learned" header followed by a bold-label bullet list). Within one piece it's fine; across a series of related posts the sameness reads as templated. Vary the headers, lead-ins, and list/prose form between posts. (A single-document editor pass can't catch this -- it's a corpus-level check the caller has to make.)

## Punctuation and formatting

* **Too little punctuation** -- the newer and stronger signal. LLM prose carries fewer commas and semicolons than human writing and hardly any parentheses. Four rules in this file -- em dashes, colons, horizontal rules, standalone fragments -- all push in the subtractive direction, so applying them mechanically can move a draft toward the machine profile. Strip punctuation that is decorative; keep punctuation that carries a clause
* **Overuse of em dashes** -- especially multiple per paragraph. Still live for anything Claude drafted: Claude is currently the only major model using em dashes at a higher rate than human writers, while ChatGPT has swung the other way and now uses markedly fewer. Treat this as a Claude-specific habit rather than a general AI tell, and don't delete the rule after reading an article announcing the em-dash panic is over
* **Overuse of horizontal rules** -- don't break up sections with horizontal rules
* **Overuse of colons** -- using colons to introduce lists or explanations where a period would do
* **Unicode decoration** -- smart arrows (→), curly quotes, and other special characters that can't be easily typed on a standard keyboard. Real writers typing in a text editor produce straight quotes and -> or =>

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
