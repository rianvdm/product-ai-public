---
name: building-exec-resumes
description: Use when writing or reviewing a resume tailored to one senior product leadership posting (VP Product, SVP, CPO, Head of Product), setting up a career fact base for resumes, or rendering a resume from Markdown to a two-page PDF. Covers fact selection, positioning, bullet craft, stage tailoring, AI-tell checks, and the tailoring workflow. Not for cover letters, exec bios, or LinkedIn rewrites.
---

# Building exec resumes

A framework for writing a VP+ product resume tailored to one posting. Two files hold the candidate's material. The **fact base** holds every claim: titles, dates, scope, achievements, each with a status tag. The rules in this file decide which facts go on the page and how they're written. Nothing reaches a resume that isn't in the fact base.


The evidence behind each rule is in `research/`: `exec-resume-norms.md`, `product-exec-signals.md`, and `ai-tells-resumes.md`. Rules that rest on reasoning alone are marked "(inference)". Rules that rest on resume-vendor material are marked "(vendor)".

## Setup

Create a resume folder for the candidate with:

| Path | Contents |
|---|---|
| `career-fact-base.md` | Copy `reference/fact-base-template.md` and fill it in. |
| `tailored/` | One `YYYY-MM-DD-company-role.md` per application, plus its `.posting.md` and rendered `.pdf`. |
| `public-profile-fixes.md` | A running checklist of LinkedIn or personal-site text that contradicts the fact base: where, current text, canonical text, why. |

Populate the fact base before drafting anything. Pre-fill it from LinkedIn, the candidate's site, and published posts, mark every gap `needs-check`, then close the gaps in one interview with the candidate. It's done when the candidate has reviewed every `needs-check` entry.

Rendering needs Python 3.9+, `pip install markdown pypdf`, and Google Chrome. The renderer lives in `scripts/`.

## How a VP+ resume gets used

At VP level, most doors open through referrals and backchannel references. Korn Ferry's CEO says most unsolicited resumes go unopened ([Burnison, 2019](https://www.kornferry.com/insights/this-week-in-leadership/best-resume-in-20-years)), and a former Daversa recruiter says some clients won't take a first call without one or two backdoor references ([Gupta, 2024](https://www.news.aakashg.com/p/product-leadership-job-search)). Ashby's data puts referral applications at a 40% interview rate against 3% for inbound ([Ashby](https://www.ashbyhq.com/talent-trends-report/reports/referrals)).

So picture the reader as someone who already has the candidate's name. They're skeptical, they'll open LinkedIn in the next tab, they may call a former colleague, and in the interview they'll pick a bullet and ask "tell me about that." Spencer Stuart verifies education and runs deep background checks on its finalists ([Spencer Stuart, 2023](https://www.spencerstuart.com/research-and-insight/your-experience-as-a-candidate)). Employment and education verification are where those checks most often find discrepancies ([HireRight, 2025](https://www.hireright.com/company/newsroom/identity-fraud-and-candidate-discrepancies-remain-key-concerns-for-employers)).

A claim that can't survive LinkedIn, a reference call, and a follow-up question stays off the page.

## Positioning

Open with a name, a contact line, and two or three sentences of positioning. Skip the objective statement ([Ask a Manager](https://www.askamanager.org/2020/02/my-step-by-step-guide-to-writing-a-resume.html)) and the "core competencies" grid. The case for a keyword block comes mostly from vendors, and keyword stuffing hurt resumes in TheLadders' eye-tracking work ([Ladders 2018](https://www.prnewswire.com/news-releases/ladders-updates-popular-recruiter-eye-tracking-study-with-new-key-insights-on-how-job-seekers-can-improve-their-resumes-300744217.html)). Put the posting's keywords inside the positioning and the bullets.

The positioning says what kind of product leader the candidate is for *this* company. It contains:

- the domain, in the posting's own nouns where they're true
- the strongest scope fact for this role (a team built, a business run, a scale handled)
- one point of view, taken from the fact base's "Points of view" section

The point of view is the sentence most likely to come out generic, so it never gets written fresh. If no entry in "Points of view" fits the posting, ask the candidate for one and add it to the fact base first.

Then apply the test: could this paragraph sit on another VP of Product's resume without edits? If yes, rewrite it with named products, real scale, and a sharper point of view. Recruiters describe generic, interchangeable text as the thing they now read as AI ([Chamberlin, LHH](https://www.huffpost.com/entry/recruiters-job-application-chatgpt_l_6723b4e1e4b0871068fe81ad); [Chait, Greenhouse](https://fortune.com/2025/11/18/hiring-job-seekers-recruiters-talent-acquisition-ai-doom-loop-application-technology/)).

## Structure and format

**Length.** Two pages at most. TheLadders recommends two, Korn Ferry notes most systems accept two, and the case for three pages comes only from resume-writing vendors ([Korn Ferry, 2025](https://www.kornferry.com/insights/this-week-in-leadership/5-resume-resolutions-for-2025)). One page works for a sharply scoped application (inference).

**How far back.** Show roughly the last 10 to 15 years in full (vendor consensus; Korn Ferry says to prioritize the last decade). Everything older goes in one "Earlier" line with titles and companies, so the career arc stays visible without taking space.

**Age signals.** Leave graduation years off. A 40,000-application field experiment showed graduation year works as an age signal ([Neumark et al., 2019](https://www.nber.org/papers/w21669)). It tested lower-skill jobs, so the size of the effect at VP level is uncertain, but dropping the year costs nothing. The two most common age stereotypes in AARP's 2025 survey are "less tech-savvy" and "resistant to change" ([AARP, 2025](https://www.aarp.org/pri/topics/work-finances-retirement/employers-workforce/age-discrimination-workplace/)). Recent hands-on work answers both without saying so. Also leave years off books and older talks.

**Consistency with LinkedIn.** The reader has LinkedIn open. The resume may leave details out but never contradict it. Record in the fact base whether the candidate trims LinkedIn to match or keeps it complete, and log every mismatch in `public-profile-fixes.md`.

**Per role**, in this order:

1. Company name, with "(acquired by X, year)" where it applies.
2. One italic line on what the company does and its size or stage at the time. Burnison recommends this for lesser-known employers ([Korn Ferry, 2020](https://www.kornferry.com/insights/this-week-in-leadership/three-best-resumes)).
3. Title and dates, one line per title, using the exact HR titles from the fact base. Stack promotions under one company header, newest first.
4. One italic scope line: reporting line, who reports to the candidate, products owned, and the revenue relationship.
5. Bullets.

**File format.** Markdown source, rendered to a single-column, text-based PDF with `scripts/render_resume.py`. Single column and standard section names are what TheLadders found easiest to scan, and they parse in Greenhouse, Ashby, and Lever (vendor). If a search firm asks for Word, convert the Markdown with pandoc.

**Pronouns.** Write bullets with an implied subject ("Set up...", "Moved..."). Use "my team" where credit is shared. Never "I" at the start of a bullet (inference; this is the common convention).

### Skeleton

`scripts/resume.css` styles exactly these heading levels. Values in angle brackets come from the fact base.

```markdown
---
company: <company>
role: <posting title>
posting: <URL>
date: <YYYY-MM-DD>
---

# <Name>

<City, region> · [<email>](mailto:<email>) · [<linkedin.com/in/handle>](https://www.linkedin.com/in/<handle>) · [<site>](https://<site>)

<Two or three sentences of positioning.>

## Experience

### <Current company>

*<Company line from the fact base.>*

#### <HR title> · <dates>

*<Scope line.>*

- <Bullet.>

#### <Earlier HR title at the same company> · <dates>

- <Bullet.>

### <Previous company> (acquired by <X>, <year>)

...

## Earlier

<Titles and companies before the cutoff, one line.>

## Education

<Degrees from the fact base, no years.>

## Writing and speaking

<One or two lines of public proof, as Markdown links, with no years for items older than five years.>
```

Education usually goes last for experienced leaders. Move it up only when the degree is directly relevant to the posting (inference).

## The career story

Read the sequence of titles the way a screener will. A GM who became a Director, or a Head of Product at a 20-person startup who became a Director at a big company, reads to some screeners as a step down. Handle it on the page with scope: the company line and the products owned show the size of the job. Then prepare an answer for each transition a screener will ask about, especially short stints and title changes after acquisitions. An acquisition note explains a title change; it doesn't explain a departure.

## Bullets

**How many.** Three or four for the current and most recent roles, one or two for older ones ([Biddle, 2021](https://askgib.substack.com/p/what-are-your-top-tips-for-a-pm-resumecv)). Older roles also read plainer and shorter.

**What the resume must show.** Across the resume, at least one bullet per company about building or developing the team, and at least one commercial bullet per company where a commercial fact exists. Cagan calls developing the team the VP Product's most important job ([SVPG](https://www.svpg.com/the-vp-product-role/)). a16z's talent team wants leaders who drove the roadmap themselves and can talk pricing, packaging, and revenue ([a16z, 2023](https://a16z.com/hiring-a-chief-product-officer/)). Place each fact under the title it belongs to, using the achievement's title field in the fact base.

**Attribution.** Most bullets should make the candidate's own decision visible, because a16z's talent team discounts "supporting players at larger companies" ([a16z, 2023](https://a16z.com/hiring-a-chief-product-officer/)). The attribution verb on the resume can never be stronger than the one in the fact base. Where the fact base says "facilitated", "supported", or "helped", name the specific decision the candidate made, or credit "my team". "Facilitated" is also on the flagged-word list, so describe what the facilitation was: "ran the process that produced the strategy", "worked with the team to write". A list of shipped features reads as a feature factory ([Abramson, via Gupta](https://www.news.aakashg.com/p/product-leadership-job-search)), so write what changed because of the work.

**Headcount.** Count only people who reported to the candidate. Partner teams are written as partners: "partnered with about 45 engineers across two platform teams." Claim managing managers only where the fact base records it.

**Vary the bullet type.** "Verb, task, resulting in N%" is Laszlo Bock's 2014 formula ([Bock](https://www.linkedin.com/pulse/20140929001534-24454816-my-personal-formula-for-a-better-resume)). Used on every bullet, it reads as generated ([Gem, 2026](https://www.gem.com/blog/detect-ai-generated-resumes)). Across the whole resume, mix these types:

- a decision and what followed
- a scope statement ("Took over a team with no product function...")
- a fact that stands on its own ("The product had over 20,000 paying customers by 2023.")
- a trade-off, or something deliberately stopped

Some bullets won't have a number. Exec readers expect a few bullets about judgment calls (inference).

**Numbers.** Every number comes from the fact base with a `sourced` or `estimate` tag. `estimate` figures get approximate wording ("about", "roughly"). Use exact figures the candidate can defend in a reference call. Mansfield wants exact numbers ([Bespoke, 2025](https://www.bespokepartners.com/a-pretty-resume-wont-cut-it-using-smart-criteria-to-showcase-true-value-creation/)), and Burnison warns that unrealistic metrics sink credibility ([Korn Ferry, 2026](https://www.kornferry.com/insights/special-edition/a-resume-redux)).

**Scope without P&L.** Platform and internal-product roles often don't own a P&L, and no source covers how to show that. Use the number of products, customer reach, data scale, and cost outcomes. Where revenue comes into it, label the relationship as the fact base does: "revenue influenced", "used by N customers" (inference).

**Proper nouns.** Each company names at least one product, system, customer type, or partner a reader could check. A model can't invent these without the facts, and they give the interviewer something to ask about (inference, from [Chamberlin](https://www.huffpost.com/entry/recruiters-job-application-chatgpt_l_6723b4e1e4b0871068fe81ad)).

**Rewrites.** Each stronger version uses only the fact base's wording and attribution. These examples are illustrative:

| Weak | Stronger |
|---|---|
| Accountable for revenue and product growth as part of the Executive Leadership Team. | Helped grow the product from $2M ARR in 2016 to over $10M by 2023, with over 20,000 paying customers. |
| Led the project to transition from credits-based pricing to monthly plans. | Moved the product from prepaid credits to monthly plans and tiers, a more profitable model. |
| Built the strategy, OKRs, and roadmap with Engineering counterparts. | Set up the first product function for the internal developer tooling team, and wrote its strategy, OKRs, and roadmap with the engineering leads. |

## Tailoring by company stage and domain

Hire for the next 12 to 18 months, says Elad Gil ([High Growth Handbook](https://growth.eladgil.com/book/chapter-4-building-the-executive-team/hiring-executives/)). Read the posting for which kind of leader it wants, then lead with the matching facts.

| Stage | What they're hiring for | Lead with | Play down | Objection to pre-empt |
|---|---|---|---|---|
| Series B–D, under 500 people | A hands-on leader who builds the product org and partners with the founder ([Riviera, 2019](https://www.rivierapartners.com/insights/questions-to-answer-before-hiring-a-vp-product-and-mistakes-to-avoid/)) | First-PM and GM roles, pricing changes, startup roles reporting to the CEO, recent hands-on work | Operating inside a large matrix | Horowitz's rhythm and skill-set mismatches for big-company execs ([Horowitz](https://a16z.com/why-is-it-hard-to-bring-big-company-execs-into-little-companies/)). Answer with bullets that show pace and personal ownership. |
| Later stage, 500–2,000 people | A leader who runs a portfolio and plans across teams | Portfolio breadth, strategy the candidate wrote and got approved, reorgs and planning across teams, GM roles for commercial depth | Individual shipping details | "Can they run a multi-team org?" Answer with the role where managers reported to the candidate. Claim manager-of-managers only where the fact base records it. |
| Big-tech VP | Scale, cross-org influence, platform thinking | Company scale, system scale, cross-team work, M&A integration | Scrappiness for its own sake | "Has this person led at our scale?" Answer with scope, stated exactly. |

Then check the domain. Lead with the facts from the posting's domain (observability, data, devtools, security, AI infrastructure) and move the rest down.

### VP-level shape

For VP, SVP, and CPO postings, the page has to read as someone who runs a business and an org, not a strong individual contributor. A screener reads down the list and anchors on the smallest item. Lead with the evidence that is honestly VP-shaped:

- Positioning: the biggest business the candidate ran or helped grow, then the largest scale. Hands-on work gets one clause at the end.
- Current role: revenue ownership, the launch portfolio, and strategy approved above the candidate. Leave out intern projects and personal tooling.
- Scope line: "leads a team of PMs" without a peak count if the count is small; the count is for interviews.
- A long tenure with promotions: one block with the titles stacked and three or four bullets across the whole tenure, with the largest org first.

Postings that hire on hands-on impact (Principal PM, AI-lab product roles) use the opposite emphasis: tooling and shipped work lead, and headcount stays in the scope line.

Two framings help when classifying a posting: Shreyas Doshi's Operator, Craftsperson, and Visionary types ([Doshi](https://x.com/shreyas/status/1375491623308550144)), and Casey Winters's four kinds of product work, one of which is tech and process scaling ([Winters, 2021](https://www.caseyaccidental.com/p/why-product-leaders-fail)).

GM experience counts for a lot in B2B CPO roles, especially where pricing is in scope ([Russell Reynolds, 2020](https://www.russellreynolds.com/en/insights/reports-surveys/the-customer-first-organization-the-rise-of-the-chief-product-officer--full-2021-edition); [Insight Partners, 2026](https://www.insightpartners.com/ideas/ai-hiring-product-eng-leaders/)). Pair it with org-building evidence, or it reads as "business person, not product leader."

## AI experience

Two kinds of AI experience go in different places.

AI product and domain work goes under the role, like any other bullet, with no cap. For AI-infrastructure postings this is lead material.

Personal AI fluency gets one line, and it states who uses the work: tools other people rely on, internal training, open-source workflows. Insight Partners names personal AI experimentation as the signal they look for ([Insight, 2026](https://www.insightpartners.com/ideas/ai-hiring-product-eng-leaders/)), and Bessemer expects product leaders to engage with model quality directly ([Bessemer](https://www.bvp.com/atlas/talent-trends-for-the-ai-native-c-suite)).

Leave out "AI strategy", "AI-first mindset", tool lists, and any AI line with no user or outcome. Fortune reports hiring leaders are suspicious of AI-polished resumes and push hard in interviews on specific project steps ([Fortune, 2026](https://fortune.com/2026/08/10/resume-perfect-match-ai-hiring-hr-leaders-interview-matters-most/)). Don't lead with personal coding projects: readers will take it for an engineer's resume and ask who was running the org (inference).

## AI-tells checks

Run every check on every draft. Run checks 1, 10, 12, and 13 again after the candidate's edits and after any cuts made to fit two pages. In a 1,072-person test, recruiters picked the human-written resume 49.3% of the time ([Tegze, 2026](https://newsletter.jobsearch.guide/p/recruiters-cant-spot-ai-resumes)), so authorship itself is hard to spot. The research suggests readers react to generic text, bullets that all look alike, and numbers that don't hold up (inference; see §1 of `research/ai-tells-resumes.md`).

1. **Traceable numbers.** Every number matches a fact-base entry tagged `sourced` or `estimate`, including in the positioning.
2. **Metric template.** The "verb ... resulting in N%" pattern covers no more than half the bullets ([Gem](https://www.gem.com/blog/detect-ai-generated-resumes)).
3. **Opening verbs.** No verb opens more than two bullets. If several fact-base entries start with "Led", rewrite from the fact itself and not its wording.
4. **Metric density.** No more than about two thirds of the bullets carry a percentage (inference).
5. **Baselines.** Every percentage has a baseline, a timeframe, or an absolute number.
6. **Posting overlap.** No phrase of four or more words copied from the posting, and the posting's requirements aren't mirrored in order (vendor: Gem, Enhancv). Use its nouns so a recruiter's search hits.
7. **Someone-else test.** The positioning fails if it could describe another VP of Product.
8. **Voice across time.** Older roles are shorter and plainer than recent ones ([Gem](https://www.gem.com/blog/detect-ai-generated-resumes)).
9. **Proper nouns.** Each company names at least one checkable product, system, customer type, or partner.
10. **Em dashes.** Zero. Claude uses them more than human writers do. En dashes appear only in date ranges.
11. **Flagged words.** Any word family from the lists below appearing more than once per page gets rewritten (threshold from `research/ai-tells-resumes.md`).
12. **Artifacts.** No square brackets, angle brackets, "X%", placeholder text, arrows, or curly quotes in the rendered text. Markdown link syntax is fine, since it renders as a link.
13. **Canonical facts.** Every title, company, date, and attribution verb matches the fact base exactly.
14. **Interview test.** For each bullet, the candidate confirms at review (workflow step 7) that they can tell the story and answer one follow-up. Bullets they can't back up get cut.
15. **Acting abstractions.** No bullet makes an idea, plan, event, or tool do the acting: "two bets carry it", "updates that bring", "an onsite that gave", "the command gets". Rewrite with a person or team as the subject. Editor passes tend to miss this one, so read for it directly.
16. **Colon reveals and stacked clauses.** No colon inside a bullet to set up a payoff, and no more than one "that" or "which" clause per sentence. Break long bullets into short sentences.

**Pre-ChatGPT resume clichés.** These predate ChatGPT. They're on the list because they say nothing. Hiring managers disliked them in 2014 ([CareerBuilder](https://www.careerbuilder.com/share/aboutus/pressreleasesdetail.aspx?ed=03/13/2014&id=pr809&sd=3/13/2014)), and LinkedIn listed them as overused in 2017 ([LinkedIn](https://www.linkedin.com/blog/member/career/better-than-buzzwords-2017-is-the-year-to-start-showing-it-linkedin)):

> results-driven, proven track record, detail-oriented, team player, go-getter, go-to person, think outside the box, best of breed, synergy, thought leadership, value add, bottom-line, passionate, motivated, creative, strategic (as a self-description), specialized, experienced, expert, successful, excellent communicator, thrive in fast-paced environments

**LLM-flavoured resume words.** These showed up in ChatGPT resumes at high rates in one vendor experiment ([FreeCV](https://freecv.org/blog/words-that-make-resume-look-ai-written)) and in recruiter reports ([HuffPost, 2024](https://www.huffpost.com/entry/recruiters-job-application-chatgpt_l_6723b4e1e4b0871068fe81ad)). The evidence is weak, and the fix is the same either way: replace the word with what actually happened.

> spearheaded, orchestrated, championed, pioneered, leveraged, utilized, facilitated, fostered, streamlined, comprehensive, seamless, dynamic, robust, cutting-edge, innovative, adept, tech-savvy, proficient in, cross-functional synergy, strategic alignment, drive alignment, stakeholder alignment

"Delve" and "tapestry" didn't show up in resumes in that experiment, so they aren't worth checking for here.

**The AI-ranker tension.** LLM screeners score text written by the same model higher, by 23% to 60% in simulation ([Xu et al., 2025](https://arxiv.org/abs/2509.00462)), and wording-only changes flip 30% to 41% of LLM screening decisions ([Chen and Xiao, 2026](https://arxiv.org/abs/2609.16517)). There's no reliable way to game that without making the page worse for the person reading it. At VP level a person makes the call, so write for the person and use exact-match nouns for search (inference).

## Tailoring workflow

For each posting:

1. **Save the posting.** Copy the full text into `tailored/YYYY-MM-DD-company-role.posting.md`, with the URL at the top. Postings disappear.
2. **Classify it.** Pick the stage row and the domain. Note the three or four things the posting cares about most, in its own nouns.
3. **Select facts.** Pull entries from the fact base by theme, stage, and domain. Only `sourced` and `estimate` entries qualify; `needs-check` entries never do. Prefer entries with a story marked `yes` or a public write-up. Anything drafted from a `to confirm at review` entry needs the candidate's story at step 7, or it gets cut. If the posting needs a fact or a point of view the fact base doesn't have, ask the candidate and add it to the fact base first.
4. **Draft** `tailored/YYYY-MM-DD-company-role.md` from the skeleton, with the posting details in the frontmatter.
5. **Run all 16 checks** and fix every failure.
6. **Get an independent edit.** Dispatch a style-editing agent (or a fresh session) on the draft and apply the findings you agree with.
7. **Candidate review.** The candidate edits and confirms the interview test for each bullet. Unedited AI letters underperformed in the Freelancer.com data, and time spent editing correlated with getting hired ([Cui et al., 2025](https://arxiv.org/abs/2509.25054)).
8. **Render** with `python scripts/render_resume.py <file.md>`. It warns past two pages; cut until it doesn't. Then check where page 1 ends. A company may split across the page break as long as its heading, company line, first title, and at least the first full bullet sit on page 1. If less than that fits, add `{: .new-page }` to the company heading so the whole company starts page 2. Don't cut content just to fit a company on page 1.
9. **Re-run checks 1, 10, 12, and 13** on the final version.
10. **Check public profiles.** Before sending, confirm the title and date items in `public-profile-fixes.md` are done. Until they are, LinkedIn contradicts the resume.
11. **Update the fact base** with any new or corrected fact from the candidate, and `public-profile-fixes.md` with any new mismatch.

The resume is done when all 16 checks pass on the rendered version, the PDF is two pages or fewer, and the candidate has confirmed the interview test for every bullet.

## Sources

- [Spencer Stuart, "Your Experience as a Candidate"](https://www.spencerstuart.com/research-and-insight/your-experience-as-a-candidate) (2023): retained-search process, background and education checks.
- [Gary Burnison, "A Résumé Redux"](https://www.kornferry.com/insights/special-edition/a-resume-redux) (Korn Ferry, July 2026): accomplishments over activity, metric credibility.
- [Aakash Gupta and Colin Lernell, "The Product Leadership Job Search"](https://www.news.aakashg.com/p/product-leadership-job-search) (April 2024): named tech-search recruiters from Riviera, Daversa, and True Search.
- [Marty Cagan, "The VP Product Role"](https://www.svpg.com/the-vp-product-role/) (SVPG): team development as the top job.
- [a16z, "Hiring a Chief Product Officer"](https://a16z.com/hiring-a-chief-product-officer/) (June 2023): roadmap ownership, revenue mindset.
- [Ben Horowitz, "Why is it hard to bring big company execs into little companies?"](https://a16z.com/why-is-it-hard-to-bring-big-company-execs-into-little-companies/) (2010): the rhythm and skill-set mismatches.
- [Russell Reynolds, "The Rise of the Chief Product Officer"](https://www.russellreynolds.com/en/insights/reports-surveys/the-customer-first-organization-the-rise-of-the-chief-product-officer--full-2021-edition) (2020): breadth over title, the Digital GM.
- [Insight Partners, AI-ready product and engineering leaders](https://www.insightpartners.com/ideas/ai-hiring-product-eng-leaders/) (July 2026): personal AI experimentation, pricing.
- [Cui, Dias, and Ye, "Signaling in the Age of AI"](https://arxiv.org/abs/2509.25054) (2025): tailoring loses signal value; editing time correlates with hiring.
- [Xu, Li, and Jiang, "AI Self-preferencing in Algorithmic Hiring"](https://arxiv.org/abs/2509.00462) (2025): LLM screeners prefer LLM text.
- [Neumark, Burn, and Button, age discrimination field experiment](https://www.nber.org/papers/w21669) (2019): graduation year as an age signal.
- [HireRight 2025 Global Benchmark](https://www.hireright.com/company/newsroom/identity-fraud-and-candidate-discrepancies-remain-key-concerns-for-employers): employment and education discrepancies.
- [Ashby referrals report](https://www.ashbyhq.com/talent-trends-report/reports/referrals): referral vs inbound conversion.
- [Jan Tegze, "Recruiters can't spot AI resumes"](https://newsletter.jobsearch.guide/p/recruiters-cant-spot-ai-resumes) (May 2026): detection at coin-flip accuracy.

Everything else, including which claims were checked and discarded, is in `research/`.
