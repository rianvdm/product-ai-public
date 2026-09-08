---
name: visual-eli5
description: Use when the user asks for a temporary or one-off visual HTML page that explains an unfamiliar topic from scratch with big pictures and few words. Do not use for prose-only explanations, reader-controlled interactive visualizations, or pages for the therapy explainer site.
---

# Visual ELI5

## Boundaries

The outcome is that a novice can say the one or two important things in plain language after seeing the page. Route the request before building:

- Therapy-site work goes to `building-psych-explainers`.
- Reader-controlled or durable internal explainers go to `interactive-explainer`.
- An editable whiteboard goes to `building-tldraw-diagrams`.
- Prose only uses a normal response or `linear-walkthrough`.

An explicit `$visual-eli5` controls this temporary explanatory build. One-off pages publish to **whatevenis.elezea.com** only when the user requests publication. The repo is `~/git/whatevenis` (Worker name `whateven`), an assets-only Worker with a home page and one directory per subject.

### Publish an approved page

Treat routine publication as a self-contained continuation of this workflow. Use the repo's local instructions, configuration, and installed CLI help; web research belongs to subject verification during authoring. Retrieve deployment documentation only when an unfamiliar command, changed configuration, or unresolved error requires it.

1. Read the destination repo's instructions and check its Git state. Copy the approved page and `og.png` into `public/<slug>/`, and the share-card source into `og/<slug>.html`.
2. Add the home-page link and README table entry. Confirm the canonical, `og:url`, and `og:image` URLs use the same slug. Rerun this skill's checks against the destination page.
3. Check the newest Worker version's `metadata.source` before deploying; reconcile any API-only changes. Run `npx wrangler deploy --dry-run`, then `npx wrangler deploy` from the repo root.
4. Confirm the new version is active through the deployments list. Verify the page and home link in a browser wider than the page column. Bot Fight Mode on elezea.com can return 403 to shell requests; use the browser for live-page inspection.

For another destination or hosting changes, use that destination's deployment workflow.

## Output contract

Set `page_dir="$(mktemp -d)"` and create exactly one self-contained `"$page_dir/index.html"`, plus the share card pair `"$page_dir/og-card.html"` and `"$page_dir/og.png"`; keep all review evidence in `"$page_dir/review"`. Never create a repository or edit/deploy a destination without a separate request and destination workflow. Open the local page for inspection, and do not deploy it. The page uses its subject's objects, relationships, scale, or sequence as the composition; every picture earns its place by demonstrating a claim.

## Build workflow

1. Verify authoritative sources and record them in the page. When the subject serves more than one audience or use (a drug with two indications, a tool with two jobs), pick one, name it in the first scene, and say so in the reply; ask first only when the choice would change every scene. Write one or two outcomes, choose an accurate familiar anchor and write out what happens in it in two sentences (a comb: each tooth flicks the nail, and the flicks come so fast you hear a buzz), because a comparison that is only named works for the reader who has already made it, and draft each scene internally in this order: `Claim`, `Picture`, `Coverage`, `Motion`, before writing HTML.
2. Choose a visual language from the subject before drafting any HTML. Name the real surface the subject lives on (a record sleeve and its centre label, a blister pack and its folded leaflet, a tide table pinned up in a harbour office) and take three decisions from it, each with its origin written down: a palette of ground, ink, and one or two accents pulled from that surface; a type feel picked from the system stacks (grotesque, geometric, humanist, serif, slab, or monospace) that the surface would use; and a layout that fits the composition (single column, figure-first with prose alongside, a dark ground, full-bleed figures, a two-column ledger). Put the three decisions and their origins in an HTML comment at the top of the `<style>` block, give every figure colour a CSS variable so the language lives in that one block rather than in hex scattered through the SVGs, and carry the same palette into the share card. The house default is a warm off-white ground, a 760px single column, a heavy tight-tracked system sans headline, a small-caps eyebrow, and one near-black object with one orange accent; that is what gets drawn unprompted, so a page lands there only when the subject's own surface looks like that, and the comment says so. Run `python3 "$skill_dir/scripts/compare-language.py" "$page_dir/index.html" ~/git/whatevenis/public/*/index.html`; it prints ground, headline face class, accent, and column width for each page, and the new page passes when at least two of the four differ from every page already on the site.
3. Start with the purpose or question and define terms in prose before using them; a scene that leans on a claim comes after the scene that makes it. Words that name drawn things count as terms (a slip, a row, a cell), a caption is a label and not a definition, one thing keeps the name its figure prints, and one word never names two things (a grading rule and a ruler). The last scene carries the outcome or evidence that answers the question, with a figure the reader has not seen; the shortest accurate answer is one closing sentence in that scene, an `h3` after the figure, and a recap scene that reuses an earlier figure is cut. Use complete novice-readable sentences rather than topic labels, questions, fragments, or contradiction-first slogans.
4. Use one semantic section per scene: `section[data-scene]` with a nonempty unique `id`; the first scene has one `h1[data-claim]`, later scenes one `h2[data-claim]`; explanatory copy is `p[data-prose]`; each scene has a named, visible `data-visual`. A `figcaption` names what the marks are ("The plugs are naltrexone.") in one or two short sentences; every explanatory sentence goes in `p[data-prose]`, where the density checker counts it.
5. Keep the page local and self-contained. A source hyperlink is documentation; remote scripts, styles, fonts, images, media, frames, and runtime assets are not.
6. Give the page a share card, the way the therapy-words pages carry one. The head block after `<title>` holds a `<meta name="description">` under 160 characters, the canonical link, `og:type` article, `og:site_name` "What even is", `og:url`, `og:title` (the h1 claim), `og:description` (one sentence naming the objects in the chain), `og:image` at `https://whatevenis.elezea.com/<slug>/og.png` with `og:image:width` 1200, `og:image:height` 630 and `og:image:alt`, and `twitter:card` summary_large_image. Write `"$page_dir/og-card.html"` as a self-contained 1200×630 page in the palette chosen in step 2: a ground from that palette, an eyebrow with the host, the h1 claim as the title, the `og:description` sentence as the sub, and on the right a monochrome SVG glyph of the first scene's figure with the page's one accent colour, redrawn rather than copied so it reads at card size. Render it with `python3 "$skill_dir/scripts/build-og.py" "$page_dir"` and look at the PNG; the glyph is caught in its finished state, so a card that depends on motion has nothing to show.

### Scene gate

Before a scene advances, fill and inspect all four draft slots in order: `Claim`, `Picture`, `Coverage`, `Motion`.

- `Claim` is the single subject-and-verb claim and becomes the scene heading. It has one finite clause, or multiple clauses joined by a connector that names one visible relation: `[effect] because [cause]`, `[cause], so [effect]`, `[state A] while/but [contrasting state B]`, or `[earlier], then [later]`. `while`/`but` must express an actual visible contrast, such as stable-versus-changing or misconception-versus-reality; simultaneity alone is two scenes. A comma-plus-`and`, semicolon, colon, or dash does not name that relation and must be split; compound subjects such as `sunlight and orbit` remain one clause.
- `Picture` follows Claim and names drawable cues—objects, positions, paths/arrows, boundaries, scales, timelines, or side-by-side states—that visibly encode each relationship. Every relationship cue contains both named actors or endpoints plus the visible link between them; for `A around B`, Picture names A, B, and the encircling path or positions, because a path or arrow alone is incomplete. Labels may name an object, unfamiliar term, quantity, or duration, but a label or sentence that merely restates Claim or says “the diagram shows that…” is not evidence. Keep reader-facing headings and captions as complete novice-readable sentences; tiny diagram labels may be fragments.
- `Coverage` has one line per mapping, exactly `"[claim phrase]" → "[exact contiguous excerpt from Picture]"`. Every line has two quoted spans and an arrow; the right span must be a contiguous substring of Picture naming a concrete drawable cue, not a repeated claim sentence. For a relationship, that excerpt contains both named actors or endpoints and the visible link; use multiple exact mappings when the complete evidence is non-contiguous. If no Picture substring exists, revise Picture first. Order or repetition is not elapsed time; a duration needs a clock, calendar, or timeline label. A missing mapping forces revision.
- `Motion` matches one subject-filled form exactly:

  ```text
  None — [named visible cues/states] show [named claim relationship] together
  Animate — [named visible change] reveals [named claim relationship]; reduced motion shows [named static cues] preserving that relationship
  ```

When the user requests only a plan or outline, return `Claim`, `Picture`, `Coverage`, and `Motion` for every scene so the gate is inspectable. Coverage is planning evidence only and is omitted from a built reader-facing page. This is a subject-shaped planning contract, not a visual or HTML template.

For a plan or outline request, immediately before replying, re-read every scene and complete only when every scene passes all four Scene-gate slots; any failed `Claim`, `Picture`, `Coverage`, or `Motion` slot—including missing actor–link–endpoint evidence—returns that scene to drafting.

## Page contract

Start each page with a visible `What even is` site-title link to `https://whatevenis.elezea.com/`. Use the absolute URL so it also works in the local preview; keep the subject label outside the link.

Choose subject-appropriate system fonts, but avoid Verdana. Apply the chosen type family consistently to prose, figure labels, and the share card.

Use the checker constants exactly: `MAX_AVERAGE_SENTENCE_WORDS = 12`, `MAX_PARAGRAPH_WORDS = 40`, `MAX_SCENE_PARAGRAPH_WORDS = 65`, `MAX_CAPTION_WORDS = 20`, and `MIN_RENDERED_TEXT_PX = 9`. A visual demonstrates its claim; every scene passes “When you ___, ___” using words already introduced.

Animate the one or two scenes whose claim is a sequence (a molecule dropping into a slot, a bounce, a signal spreading) and keep the rest static. Build each animated element in its finished state, let keyframes deviate from it briefly and hold the finished picture for most of the loop, and set `animation: none` under `@media (prefers-reduced-motion: reduce)`, so the reduced-motion frame is the finished picture with no extra work. One mark gets one animated element, since two on separate loops drift out of phase and leave the mark half drawn. Motion explains change, direction, sequence, timing, or cause and effect and never gates content. The prose of an animated scene names the motion the reader sees: say what does not move and what does (the record slides past; the needle only moves across the groove), because a sentence like "the needle stays put" beside a dot that visibly moves reads as a contradiction.

Close the page with a footer byline reading `Made by <a href="https://elezea.com">[Author]</a>`, placed after the source list, so every page on the site is attributed.

Draw figures in a 720-wide `viewBox` with `width: 100%`. SVG text at 13 to 15 px renders near 7 px on a phone, so scale the label classes to about 1.4x under 480 px; at that size a label takes about 12 viewBox units per character, so a column 170 units wide holds 14 characters, and a longer label goes onto a second line or against the far edge with `text-anchor`. Keep labels under about 25 characters and plan for one render pass of collisions at phone width, which is where they appear. The 1.4x bump is what makes a label outgrow the `viewBox`, so a label centred at x with the figure 720 wide can only be about twice the smaller of x and 720 - x: shorten it, split it onto a second line, or, for a dense relationship diagram whose labels cannot shrink, mark the figure `class="wide"` so it keeps the small sizes and scrolls. Nudging a label sideways to fit is the one move to avoid, because it detaches the label from the mark it names. Draw one `<path>` per arrow; a path with several subpaths gets a single arrowhead. Keep content visible on arrival and make desktop and phone layouts readable without horizontal clipping.

The following compact example is a content sketch, not the four-slot plan/outline contract:

```text
Claim: Every conversation gets its own durable room.
Picture: A front door routes one message into one labeled room with a SQLite shelf.
Motion: None. The routing arrow already shows direction.
```

## Checks

Set `skill_dir` to the directory containing `SKILL.md`. Resolve `../../../01-context/avoid-ai-patterns.md` and `../../../01-context/avoid-ai-visual-patterns.md` relative to `skill_dir`; read both completely. Then run:

```sh
python3 "$skill_dir/scripts/check-page.py" "$page_dir/index.html"
python3 "$skill_dir/scripts/check-page.py" --prose "$page_dir/index.html"
python3 "$skill_dir/scripts/check-page.py" --render "$page_dir/review" "$page_dir/index.html"
```

Review desktop and phone captures, plus reduced-motion captures when motion exists. `REVIEW` lines are findings to resolve or justify in the review table: `prose.caption-explains` means a caption is carrying explanation, and `render.small-text` names phone text that renders below the minimum size. `render.viewbox-clipping` is an error, not a review: it names SVG text whose box runs past its own `viewBox`, which an SVG root silently cuts off. It is the failure the phone label bump causes, it is invisible in a desktop capture and in the viewport-clipping check, and it is caught only by measuring `getBBox` against the `viewBox`. Write `"$page_dir/review/scene-review.md"` beginning with this literal Markdown header:

```markdown
# scene-review.md

| Scope | Claim | What the visual demonstrates | Undefined terms | Source evidence | Prose findings | Visual findings | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Use one row for `page` and one row for every `data-scene`. In each scene row, include a source URL or file locator and supporting fact, a term check, prose findings, visual findings, and a `keep`/`fix` decision. Record the `Motion` decision and its evidence in the relevant `Visual findings` and `Decision` cells. Scope every finding to `page` or scene IDs and resolve every fix before completion.

## Completion

Completion requires all sixteen acceptance behaviors: a subject-derived visual language recorded in the style comment and passing `compare-language.py` against the site; scene count; one claim per scene; heading/picture pairing; complete novice-readable prose; subject-shaped composition; no remote dependencies; content visible on arrival; a reasoned motion decision; reduced-motion behavior; terms defined before use; auditable source evidence; a footer byline; desktop and phone viewport evidence; a share card (`og:*` head block plus an inspected 1200×630 `og.png`); and temporary/open behavior. Record the exit status from `open "$page_dir/index.html"`, return the absolute `"$page_dir/index.html"` path, resolve every checker error and every review finding, and finish only with zero unresolved findings.
