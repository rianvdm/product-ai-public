# AI tells in resumes: what recruiters detect, and what reads as human

*Research gathered 2026-09-29 by Claude subagents for the resume framework. Evidence tiers are marked inline. Verify anything important before quoting it publicly.*

*Research date: 2026-09-29. Web research only. Complements `01-context/avoid-ai-patterns.md`; general prose tells from that file are not repeated here unless the resume evidence changes how they apply.*

## Summary

The evidence says recruiters penalize resumes that read as generic, and they can't reliably tell whether AI wrote them. Every survey that claims "X% reject AI resumes" is a resume-builder vendor poll on Pollfish. The best controlled test found recruiters at coin-flip accuracy. The academic work (Freelancer.com cover letters, Upwork resumes) shows AI polish erases the value of tailoring as a signal, which pushes employers toward work history, referrals and interviews. For a VP+ candidate the practical risk is sounding like everyone else, and a checker should target the specific failure modes below, not a list of forbidden words.

Five findings that change how to approach this:

1. Most "AI tells" in resumes are pre-ChatGPT resume clichés. "Results-driven", "synergy", "go-getter", "passionate", "strategic" and "specialized" were on hiring-manager hate lists in 2014 and LinkedIn's overused list in 2017. Avoiding them is about avoiding cliché. They don't prove authorship either way.
2. Human detection is poor. In one test with 1,072 participants, recruiters picked the human resume 49.3% of the time. Recruiters in vendor surveys *claim* they can spot AI quickly, and those claims shouldn't be taken at face value.
3. Keyword mirroring has lost its value as a signal. On Freelancer.com, an AI writing tool raised cover-letter alignment with the job post, and the link between alignment and callbacks fell 51%. Employers shifted weight to work history.
4. AI screeners may *prefer* LLM-written resumes. One study found that LLM evaluators favour resumes written by the same model (23% to 60% more likely to be shortlisted in simulation). So "sound less like AI" and "score well with an AI screener" can pull in opposite directions. Referrals and search firms avoid that conflict entirely.
5. For exec roles the resume is a smaller part of the decision than it is for inbound roles. Referral applicants convert to interview at roughly 13x the inbound rate (Ashby data). The resume's job is to survive a skeptical read by a person who will also check LinkedIn and ask about each bullet in an interview.

## Evidence grading used in this file

| Grade | Meaning |
|---|---|
| A (academic) | Peer-reviewed or working paper with published method and data |
| S (survey, independent) | Survey by a party without a resume product to sell |
| V (vendor survey) | Survey by a company that sells resume, ATS or hiring tools. Lower confidence: Pollfish-style online panels, self-reported, headline stats chosen by marketing |
| N (named anecdote) | A named recruiter or talent leader describing what they see |
| U (unattributed / blog) | SEO blog or unsourced claim. Lowest confidence |
| I (inference) | My reasoning, not sourced |

---

## 1. How recruiters detect AI resumes, and how often they say they penalize them

### Survey figures

| Claim | Source, date | Method | Grade |
|---|---|---|---|
| AI-generated content is the #2 resume red flag at 49%, behind job-hopping (65%); vague responsibility descriptions 42% | [Resume Genius Hiring Trends 2026](https://resumegenius.com/blog/job-hunting/hiring-trends-report-2026), June 2026 | 1,500 US hiring managers via Pollfish, June 4-6, 2026 | V |
| In 2024, 20% said suspected AI content would definitely stop them hiring | Same report (2024 wave, 625 managers) | Pollfish | V |
| 58% have received AI-generated resumes or cover letters; 86% expect authenticity verification problems | [Resume Genius, AI's Impact on Hiring 2026](https://resumegenius.com/blog/ai-impact-on-hiring-2026), June 2026 | 1,500 US hiring managers, Pollfish | V |
| 58% of hiring managers use AI to screen resumes (35% in 2025); 6% let AI reject with limited human review | Same | Same | V |
| 19.6% would reject a candidate with a fully AI-generated resume or cover letter; 33.5% say they can spot one in under 20 seconds; 52% accept AI for proofreading or drafting | [TopResume](https://topresume.com/career-advice/ai-in-hiring-survey), 2025 | 600 US hiring managers, Pollfish, May 15-16, 2025 | V |
| 49% "dismiss" AI-generated resumes; managers say they prefer an authentic flawed resume to a polished AI one | [Resume.io](https://resume.io/blog/resume-rejections), updated Jan 22, 2025 | 3,000 hiring managers; method not published on page | V |
| 29% of respondents say recruiters spot AI easily, 56% "sometimes"; HR respondents 44% "easy" | [Kickresume](https://www.kickresume.com/en/press/resume-trends-survey/), Dec 2025 | 1,004 global respondents, mixed job seekers and HR, anonymous online | V |
| 77% of hiring teams regularly see AI-generated or AI-assisted applications, up from 53% in early 2024 | [Willo Hiring Trends 2026](https://www.willo.video/the-hiring-trends-report-2026), Jan 2026 | 100+ hiring professionals | V (interview-software vendor) |
| 91% of recruiters have spotted candidate deception; 34% spend up to half their week filtering spam/junk applications; 74% more worried about misrepresented experience than a year ago | [Greenhouse AI in Hiring Report 2025](https://www.greenhouse.com/newsroom/an-ai-trust-crisis-70-of-hiring-managers-trust-ai-to-make-faster-and-better-hiring-decisions-only-8-of-job-seekers-call-it-fair), 2025 | 4,100+ job seekers, recruiters, hiring managers in US, UK, IE, DE | V (ATS vendor, but not a resume seller) |
| 39% of candidates used AI during the application; 6% admit interview fraud; Gartner predicts 1 in 4 candidate profiles fake by 2028 | [HR Dive on Gartner](https://www.hrdive.com/news/fake-job-candidates-ai/757126/), July 31, 2025; [Gartner press release](https://www.gartner.com/en/newsroom/press-releases/2025-07-31-gartner-survey-shows-just-26-percent-of-job-applicants-trust-ai-will-fairly-evaluate-them) | 3,290 candidates (4Q24) and 3,000 candidates | S |

### How reliable are the rejection numbers?

- The range runs from 19.6% (TopResume) to 49% (Resume.io, Resume Genius). The questions differ: "would reject a fully AI-generated resume" is not "sees AI content as a red flag". None of these measure actual rejections.
- All the resume-specific figures come from companies selling resume builders, several of which sell AI writing features. Pollfish recruits respondents through in-app offers; "hiring manager" is self-reported. Treat these as directional.
- The claim that a third can spot AI "in 20 seconds" is self-assessment. The one controlled test I found points the other way: Jan Tegze ran a test with 1,072 participants on eight AI-generated resumes, and recruiters scored 49.3% when guessing which was human, against 51.0% for job seekers ([Job Search Guide newsletter](https://newsletter.jobsearch.guide/p/recruiters-cant-spot-ai-resumes), May 24, 2026). Grade N/V: a practitioner's self-run test, not peer reviewed, self-selected sample, but it has a stated method.
- Broader detection research agrees. Perplexity-based AI detectors misclassified 61.3% of non-native English essays as AI on average ([Liang et al., Patterns 2023](https://arxiv.org/abs/2304.02819), grade A). Jobscan says no major ATS (Workday, Greenhouse, iCIMS, SuccessFactors, Lever, Taleo) natively detects AI authorship ([Jobscan](https://www.jobscan.co/blog/can-ats-detect-ai-resume/), May 12, 2026, V).
- A widely repeated claim that only 18% of hiring managers correctly identified three ChatGPT cover letters (ResumeBuilder, March 2023) I could not trace to a primary page. The ResumeBuilder page I found ([Feb 2023](https://www.resumebuilder.com/3-in-4-job-seekers-who-used-chatgpt-to-write-their-resume-got-an-interview/)) surveyed job seekers, not hiring managers. Don't cite the 18% figure.

Reading across all of it (I): recruiters react to *genericness* and label it AI. Whether a model wrote the text matters less than whether it reads like it could belong to anyone.

### Named recruiters and what they describe (grade N)

| Person | Role | What they see | Source |
|---|---|---|---|
| Bonnie Dilber | Recruiting manager, Zapier | "Easily 25% of apps" look AI-generated; identical answers to open questions (many applicants used the same "flower shop" example) | [HuffPost](https://www.huffpost.com/entry/recruiters-job-application-chatgpt_l_6723b4e1e4b0871068fe81ad), Oct/Nov 2024 |
| Gabrielle Woody | University recruiter, Intuit | Repeated "adept", "tech-savvy", "cutting-edge" | Same |
| Laurie Chamberlin | Head of LHH Recruitment Solutions North America | "absence of specificity, authenticity and personal touch" as the red flag | Same; also [Forbes Coaches Council](https://www.forbes.com/councils/forbescoachescouncil/2025/08/07/how-recruiters-can-tell-you-used-ai-on-your-resume-and-why-it-matters/), Aug 7, 2025 |
| Tejal Wagadia | Tech recruiter | Leftover placeholders like "add numbers here" | HuffPost, same |
| Kasandra Valle | Talent acquisition manager | "big uptick in the exact same format" from ChatGPT | [Enhancv](https://enhancv.com/blog/signs-of-ai-generated-resume/), updated Sep 24, 2026 (V) |
| Daniel Chait | CEO, Greenhouse | With AI-polished applications "you end up basically not being able to tell anyone apart" | [Fortune](https://fortune.com/2025/11/18/hiring-job-seekers-recruiters-talent-acquisition-ai-doom-loop-application-technology/), Nov 18, 2025 |
| Abby Konet, Shanon Castro, Krysha Abbott, Vicki Salemi | Talent acquisition leaders / Monster career expert | Signals that still count: scope, tangible outcomes, realistic progression, the candidate's ability to relate their experience to the role | [Monster](https://hiring.monster.com/resources/blog/ai-resumes-employer-hiring-signals), 2026 (V) |
| Katie Tanner | HR consultant | 1,200+ applications for one remote role; took the post down | NYT DealBook, June 21, 2025, via [Mayer Brown](https://www.mayerbrown.com/en/news/2025/06/employers-are-buried-in-ai-generated-resumes) and [Compono](https://www.compono.com/articles/the-r%C3%A9sum%C3%A9-is-dead-and-ai-buried-it-in-hiring-slop) summaries (NYT itself paywalled) |

---

## 2. Resume-specific tells, with the evidence behind each

No peer-reviewed study has measured word frequency in resumes before and after ChatGPT. The word lists circulating online come from recruiter anecdote, vendor blogs, or informal generation experiments. The strongest resume-adjacent frequency evidence is a single blog experiment (below) plus the academic "excess vocabulary" work on scientific abstracts.

### Vocabulary

| Tell | Evidence | Grade |
|---|---|---|
| "Proficient", "detail-oriented", "proven track record", "results-driven" each appeared in 40-44% of 500 ChatGPT-generated resumes; "foster" 38%, "utilize" 37%, "leverage" 36%, "comprehensive" 36%, "streamline" 30%, "stakeholder" 29%, "dynamic" 27%, "facilitate" 25%, "spearheaded" 15%, "seamless" 8%; "delve" and "tapestry" 0% | [FreeCV blog](https://freecv.org/blog/words-that-make-resume-look-ai-written), undated | U. Manual count, simple prompts, model and date not stated, vendor blog. Useful as a hypothesis list only |
| Kobak et al. excess-vocabulary words: delve, underscore, utilize, align, crucial, comprehensive, intricate, pivotal. "Delves" rose about 28x in PubMed abstracts | [Kobak et al., Science Advances 2025](https://www.science.org/doi/10.1126/sciadv.adt3813) | A, but for scientific abstracts. "Comprehensive" and "utilize" overlap with the resume list; "delve" does not transfer |
| "Adept", "tech-savvy", "cutting-edge" | Gabrielle Woody (Intuit), HuffPost 2024 | N |
| "Leveraged synergies to optimize outcomes", "results-driven", "detail-oriented", "innovative problem-solver" | [Gem](https://www.gem.com/blog/detect-ai-generated-resumes), Apr 21, 2026 | V (recruiting software) |
| Pre-AI clichés: "best of breed" 38%, "go-getter" 27%, "think outside the box" 26%, "synergy" 22%, "go-to person" 22%, "thought leadership" 16%, "value add" 16%, "results-driven" 16%, "team player" 15%, "bottom-line" 14% | [CareerBuilder / Harris Poll](https://www.careerbuilder.com/share/aboutus/pressreleasesdetail.aspx?ed=03/13/2014&id=pr809&sd=3/13/2014), Mar 2014, 2,201 hiring managers | S (pre-dates LLMs) |
| LinkedIn's most overused profile words: specialized, experienced, leadership, skilled, passionate, expert, motivated, creative, strategic, successful | [LinkedIn blog](https://www.linkedin.com/blog/member/career/better-than-buzzwords-2017-is-the-year-to-start-showing-it-linkedin), 2017 | S (platform data, pre-LLM) |

Implication (I): the resume "AI list" is mostly the old cliché list plus a handful of LLM-register words (leverage, foster, utilize, facilitate, comprehensive, seamless, streamline, spearheaded, orchestrated). Treat both families the same way: replace an adjective with the evidence behind it.

### Structure and formatting

| Tell | Evidence | Grade |
|---|---|---|
| Every bullet follows action verb + task + metric + outcome | Gem, Apr 2026 | V |
| All sections share identical tone and vocabulary, where a human's older roles read differently from recent ones | Gem, Apr 2026 | V |
| Round percentages (25%, 30%, 50%) versus measured-looking ones (23%, 41%) | [Sajjaad substack](https://sajjaad.substack.com/p/recruiters-can-tell-you-used-ai-on) (surfaced via search, not fetched) | U |
| Metrics with no baseline, timeframe or attribution ("improved efficiency by 35%") | Gem, Apr 2026 | V |
| Skills from the job description appear with identical phrasing or in the same order | Gem; Enhancv "perfect job ad-resume alignment", 2026 | V |
| Em dashes in 92% of 500 ChatGPT resumes, about 4 per resume | FreeCV blog | U. Model-dependent: per `avoid-ai-patterns.md`, current ChatGPT uses fewer em dashes and Claude uses more. For a Claude-assisted draft, this is a live risk |
| Em dashes and semicolons more frequent than normal professional writing | Gem | V |
| Leftover placeholders ("add numbers here", bracketed text) | Tejal Wagadia, HuffPost 2024; Forbes Coaches Council 2025 | N |
| Identical "why this company" answers built on the company's mission statement | Bonnie Dilber, HuffPost 2024 | N |
| No revision history in file metadata; created in one session | Gem | V. Probably overstated for PDFs; note only (I) |
| "Robotic bullet symmetry" and uniform bullet length | Enhancv, Hirelytica and other vendor blogs | V/U. No data found. Mark as inference-supported |
| Title Case overuse | No source found | Not supported. Don't treat as a resume-specific tell |

About the "Verb + X, resulting in Y%" pattern: this structure is Laszlo Bock's 2014 advice from Google ("Accomplished [X] as measured by [Y], by doing [Z]") ([LinkedIn, Sep 29, 2014](https://www.linkedin.com/pulse/20140929001534-24454816-my-personal-formula-for-a-better-resume)). LLMs learned it from a decade of career advice. The formula isn't the tell. Running every bullet through it with invented numbers is.

---

## 3. Academic evidence on LLMs in job applications

| Study | Data | Findings | Grade |
|---|---|---|---|
| Cui, Dias, Ye, "Signaling in the Age of AI: Evidence from Cover Letters" ([arXiv 2509.25054](https://arxiv.org/abs/2509.25054)), Sep 2025, rev. Nov 2025 | Freelancer.com, 5.5M bids, Jan-Sep 2023, around an AI "Bid Writer" launched Apr 19, 2023 | Tool access raised text alignment with the job post (0.22 SD, TF-IDF) and callbacks (about 6% over baseline). The correlation between alignment and callbacks fell 51%; with offers, 79%. Over 75% of AI letters were submitted within a minute with little editing; editing time correlated with hiring success. Employers shifted weight to prior work history | A (working paper) |
| Galdin and Silbert, "Making Talk Cheap" ([arXiv 2511.08785](https://arxiv.org/abs/2511.08785)), Nov 2025 | Freelancer.com Jan 2021-Jul 2024; about 960K pre-LLM and 1.7M post-LLM applications | Before LLMs, employers valued customized proposals highly (1 SD of signal worth about a $25.67 lower bid). After LLMs, they didn't. For AI-written proposals, effort and signal correlated negatively. Counterfactual without signaling: top-quintile workers hired 19% less, bottom quintile 14% more | A (working paper) |
| Wiles, Munyikwa, Horton, "Algorithmic Writing Assistance on Jobseekers' Resumes Increases Hires" ([NBER w30886](https://www.nber.org/papers/w30886); [Management Science 2025](https://pubsonline.informs.org/doi/10.1287/mnsc.2024.04528)) | Field experiment, about 480K jobseekers, online labor market; pre-ChatGPT grammar and style assistance | Treated jobseekers hired 8% more often, at 10% higher wages; employer satisfaction unchanged; biggest effect for non-native writers | A (peer reviewed) |
| Xu, Li, Jiang, "AI Self-preferencing in Algorithmic Hiring" ([arXiv 2509.00462](https://arxiv.org/abs/2509.00462)), Aug 2025, final Jun 2026 | 2,245 pre-ChatGPT human resumes (LiveCareer), rewritten by GPT-4o, DeepSeek-V3, Llama-3.3 and others; 24 occupations | LLM evaluators prefer their own output 67-82% of the time; same-model candidates 23-60% more likely to be shortlisted in simulation; biggest gaps in business roles (sales, accounting) | A (non-archival conference) |
| Chen and Xiao, "Competence-Preserving Resume Perturbations" ([arXiv 2609.16517](https://arxiv.org/abs/2609.16517)), Sep 15, 2026 | Controlled profiles re-rendered with different wording, structure, polish; six open LLMs | Screening decisions flipped 29.6-41.4% of the time on presentation-only changes | A (preprint, small open models) |
| Liang et al., "Widespread adoption of LLM-assisted writing across society" ([Patterns 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12745980/)) | 304M job *postings* plus complaints and press releases, 2022-2024 | LLM-assisted text in job postings near 10% for small firms; adoption plateaued in 2024 | A. Covers employers' postings, not applications |

What this means for a resume (I):
- Polish is now cheap, so polish alone earns little. Wiles et al. show clarity helped before LLMs; Cui et al. and Galdin and Silbert show that once everyone can generate a tailored, fluent document, employers stop paying for it.
- Employers substitute toward signals that are costly to fake: verifiable history, specific projects, referrals. That's the direction to write toward.
- Editing time predicts success in Cui et al. Heavy human editing is itself the useful behaviour, not just a way to hide AI use.

---

## 4. Mirroring the job description

| Question | Evidence |
|---|---|
| Does ATS filtering on keywords exist? | Yes, as recruiter search filters: 76.4% of 384 surveyed recruiters filter by skills, 55.3% by job title ([Jobscan State of the Job Search 2025](https://www.jobscan.co/state-of-the-job-search), V). Filtering is mostly a recruiter running a search, not automatic rejection: in a small Enhancv survey, about 92% of 25 recruiters don't configure auto-reject on content (reported via [Interview Guys](https://blog.theinterviewguys.com/ats-resume-rejection-myth/), U) |
| The "75% of resumes rejected by ATS" statistic | Traced to a 2012 sales pitch by Preptel, which closed in 2013; no methodology ever published ([JobCannon](https://jobcannon.io/research/stats/ats-myth-preptel), [HiringThing](https://blog.hiringthing.com/applicant-tracking-system-myths)). Don't optimize against it |
| Do modern screeners match exact phrases? | Jobscan (which sells keyword tools) says modern ATS assess semantic alignment rather than exact phrases (May 2026, V). LLM screeners are sensitive to presentation (Chen and Xiao 2026, A) |
| Does alignment still help with employers? | It raises callbacks a little but predicts much less than it used to (Cui et al., A: 51% drop). Employers stopped paying for customization after LLMs (Galdin and Silbert, A) |
| Recruiter perception of heavy mirroring | JD skills in identical wording and order are a stated tell (Gem, Enhancv, V). Dilber's identical mission-statement answers (N) |

Practical line (I, informed by the above): use the posting's *nouns* where they truly describe your work (the product area, the title, the named skills a recruiter would type into a search), so a search hits. Don't mirror its *sentences*, its order, or its adjectives. One or two exact-match terms per requirement is enough for search; beyond that, alignment adds little and becomes a visible pattern.

---

## 5. What reads as human-written (positive guidance)

| Signal | Source | Grade |
|---|---|---|
| Career progression, scope, tangible outcomes, realistic trajectory | Abby Konet, Shanon Castro (TA leaders) via [Monster](https://hiring.monster.com/resources/blog/ai-resumes-employer-hiring-signals), 2026 | N/V |
| Specific real-life examples behind claims | Laurie Chamberlin, LHH, HuffPost 2024 | N |
| Show results instead of claiming to be results-driven; plain verbs ("achieved", "improved", "trained", "mentored") | CareerBuilder 2014 | S |
| Replace adjectives with evidence | [LinkedIn 2017](https://www.linkedin.com/blog/member/career/better-than-buzzwords-2017-is-the-year-to-start-showing-it-linkedin) | S |
| A numeric baseline for each measured claim, plus how you did it | Bock 2014 | N (Google's head of people ops) |
| Unedited AI output underperforms; editing time predicts hiring | Cui et al. 2025 | A |
| Minor imperfections read as authentic to some managers | Resume.io 2025 | V |
| Prior work history carries more weight once written signals weaken | Cui et al. 2025 | A |
| Consistency across resume, LinkedIn and interview | "Interview mismatch" as a tell (Gem, V). The widely quoted "71% check LinkedIn / 42% disqualify on mismatch" figures had no traceable primary source, so they are not cited here | V / unsourced |

Inferences for a VP+ product resume (I), each tied to the evidence above:
- Proper nouns carry the most weight: named products, named customers where public, named systems, named partners, the org you reported into. A model can't invent them without the facts, and a reader can check them. This is the resume version of the "name real people" rule in `avoid-ai-patterns.md`.
- Honest scale beats big round numbers: "about 40 engineers across 5 teams", "revenue in the low hundreds of millions". Only give specific numbers that you could defend with a source in an interview.
- Vary bullet structure. Some bullets are a decision and its consequence, some are a scope statement, some a single fact. Not every bullet needs a metric; exec readers expect some bullets to be about calls you made.
- Put one or two idiosyncratic details in the doc: an unusual constraint, a thing you killed, a trade-off. These are the "loose ends" `avoid-ai-patterns.md` says machine prose lacks, and they give an interviewer something to ask about.
- Every bullet should map to a story you can tell for three minutes. Recruiters describe interview mismatch as the moment AI suspicion becomes a trust problem.

---

## 6. The 2025-2026 context and what it means for exec candidates

| Fact | Source | Grade |
|---|---|---|
| LinkedIn: about 11,000 applications per minute, up 45% year over year | NYT, Jun 21, 2025, via [Fortune](https://fortune.com/2025/11/18/hiring-job-seekers-recruiters-talent-acquisition-ai-doom-loop-application-technology/) and [eWeek](https://www.eweek.com/news/ai-job-applications-linkedin/) | S (platform figure via press) |
| Applications per hire tripled since 2021 and stayed above 300 through 2025; candidates about 50% less likely to reach interview than five years ago | Ashby, 100M+ applications, 200K jobs, via [HR Dive](https://www.hrdive.com/news/recruiters-see-job-applications-triple-to-more-than-300-per-role/820096/), May 7, 2026 | V (ATS vendor, large behavioural dataset) |
| Referral application-to-interview 40% vs inbound 3%; interview-to-offer 16% vs 6%; referrals only 1% of applications | [Ashby referrals report](https://www.ashbyhq.com/talent-trends-report/reports/referrals), 38M applications, 2021-2024 | V (behavioural data) |
| 75% of job seekers use AI to polish applications; 41% admit trying prompt injections; 8% think AI screening is fairer | Greenhouse, via Fortune, Nov 2025 | V |
| HBR: AI has made resumes and interviews poor signals; companies adding in-person steps | [HBR, Sunil and Saraf](https://hbr.org/2026/06/ai-has-broken-hiring-heres-how-to-fix-it), Jun 8, 2026. Authors co-founded an interview-screening company | N (commercial interest) |
| Auto-apply tools: Wonsulting shut its bulk auto-apply feature in Aug 2025 after about 1 interview per 50 applications | [Interview Guys](https://blog.theinterviewguys.com/the-20-interviews-from-5-000-applications-math-auto-apply-doesn-t/) | U |

Implications for exec candidates (I):
- At VP+ most hires come through referrals, retained search and direct outreach, where the resume gets read by a person who already has a reason to take the candidate seriously. That reader is looking for evidence of judgment and scope, and is primed by vendor messaging to suspect polish.
- Recruiters are more skeptical of misrepresentation (Greenhouse 74%; Gartner fraud predictions). Every number and claim should survive a reference check.
- If the application also goes through an inbound ATS with an LLM ranker, the self-preference and presentation-sensitivity findings mean small wording changes can move a score. There's no reliable way to game that without making the doc worse for the human reader. Prioritize the human reader and use exact-match nouns for search.

---

## Resume-specific flagged list

Use density, not presence, as in `avoid-ai-patterns.md`. Flag when a word family appears more than once per resume page or in the summary.

**Flag and rewrite with evidence** (words vendor blogs and recruiters associate with AI resumes):
- spearheaded, orchestrated, championed, pioneered (as generic leadership verbs) [Gem, FreeCV, Enhancv; V/U]
- leveraged, utilized, facilitated, fostered, streamlined [FreeCV U; Kobak A for utilize]
- comprehensive, seamless, dynamic, robust, cutting-edge, innovative [FreeCV U; Woody N]
- results-driven, detail-oriented, proven track record, proficient in [FreeCV U; CareerBuilder S for results-driven]
- adept, tech-savvy [Woody N]
- cross-functional synergy, strategic alignment, drive alignment, stakeholder alignment [vendor blogs V; synergy CareerBuilder S]
- "passionate about", "thrive in fast-paced", "excellent communicator", "team player" [LinkedIn 2017 S; CareerBuilder S]

**Pre-AI clichés** (flag for the same reason, not as authorship tells): best of breed, go-getter, think outside the box, go-to person, thought leadership, value add, bottom-line, specialized, experienced, expert, motivated, creative, strategic, successful [CareerBuilder 2014, LinkedIn 2017; S]

**Not worth flagging in a resume:** delve, tapestry (0% in the resume experiment, FreeCV U). Title Case (no evidence found).

**Keep:** "drove" and "led" are normal exec verbs. Flag them only when every bullet opens with them (I).

## Structural checks for a draft

Each check is tagged with its source or marked (I).

1. **Unmeasured numbers.** Every number traces to a source you could name in an interview. Strip or hedge the rest. [avoid-ai-patterns.md; Gem V "unverifiable metrics"; Kickresume V on exaggeration; Greenhouse V on misrepresentation]
2. **Metric density.** If more than about two thirds of bullets carry a percentage, flag it. [I, from Gem's "every entry" pattern]
3. **Round-number share.** If most percentages end in 0 or 5, check each is real. [U; I]
4. **Baselines.** Every percentage has a baseline, timeframe or absolute number next to it. [Bock 2014; Gem V]
5. **Bullet template uniformity.** Count bullets matching "Verb ... , resulting in / driving / leading to ... N%". Flag if one template covers more than half. [Gem V; Bock for origin]
6. **Opening-verb variety.** Flag repeated first verbs and any "spearheaded/orchestrated/championed" cluster. [Gem, FreeCV; I for threshold]
7. **Bullet length spread.** Compute word-count spread per role. Near-identical lengths across 5+ bullets is a flag. [Vendor blogs only; I]
8. **Proper-noun density.** Each role should name at least one product, system, customer type or partner a reader could verify. [Chamberlin N; Konet N; I]
9. **JD overlap.** Diff the draft against the posting. Flag copied phrases of 4+ words and skills listed in the posting's order. Keep exact-match nouns for titles and skills. [Gem V; Enhancv V; Cui et al. A for why it adds little]
10. **Summary genericness.** Could the summary belong to another VP of Product? If yes, rewrite with named domains, scale and one specific bet. [Dilber N; Chait N]
11. **Voice drift across time.** Older roles can be shorter and plainer. Identical tone and density from the first job to the latest is a flag. [Gem V]
12. **Em dashes.** For Claude-assisted drafts, target zero or one. [FreeCV U; avoid-ai-patterns.md on Claude specifically]
13. **Placeholders and artifacts.** Search for brackets, "X%", "[company]", "add", curly quotes, arrows. [Wagadia N; avoid-ai-patterns.md]
14. **LinkedIn parity.** Titles, dates, team sizes and headline numbers match LinkedIn exactly. [Gem V "interview mismatch"; I]
15. **Interview test.** For each bullet, one sentence of the backstory is known and one follow-up question has an answer. Cut bullets that fail. [Cui et al. A on editing effort; Gem V]
16. **Skills section symmetry.** A tidy, evenly sized skills grid mirroring the JD is a flag. Exec resumes often drop the skills grid entirely. [I]

## Gaps and things I couldn't verify

- No peer-reviewed word-frequency study of resumes before and after ChatGPT exists that I could find. The resume word list rests on one vendor blog experiment, recruiter anecdote, and transfer from academic-abstract studies.
- The NYT June 2025 article is paywalled; its figures come via secondary coverage.
- The CNBC "Goodbye AI resumes" piece (Sep 23, 2026) returned 403; not used.
- Unverified and not cited as fact: ResumeBuilder "18% identified AI cover letters", "71% check LinkedIn / 42% disqualify", ExecuNet "26 seconds on a C-suite resume", HBR "6,380 screening sessions" (appears only in a secondary blog).
- The Resume Now "62% reject AI resumes without personalization" page timed out; method unverified.
- Title-case overuse as an AI tell: no source found.
