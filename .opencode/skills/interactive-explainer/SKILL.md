---
name: interactive-explainer
description: Builds a self-contained interactive HTML visualisation that makes a process, algorithm, decision logic, or system visually and experientially understandable. Primary input is a linear walkthrough, but works directly from code, documents, or concept descriptions too — and can invoke the linear-walkthrough skill as an intermediate step if the source material lacks sufficient clarity or structure. Use when the user wants to "see how this works", wants an interactive version of a walkthrough, wants to explain a process visually to an audience, or asks to "visualise", "animate", or "build an interactive explanation" of anything. Richer and more interactive is always preferred, as long as it makes the logic clearer rather than decorating it.
---

# Interactive Explainer

You build interactive HTML visualisations that make abstract processes, algorithms, and decision logic _experiential_ — something the reader can manipulate and explore, not just read. The goal is to eliminate cognitive debt: after using the visualisation, the reader should feel like they _understand_ the logic, not just that they've seen it described.

## Source Material

Preferred input is a **linear walkthrough** (from the `linear-walkthrough` skill), because walkthroughs are already structured as a logical narrative with clear sections and identified connections. If none exists:

- Work directly from source material (code, document, concept description)
- If the source material is dense, ambiguous, or poorly structured, **invoke the `linear-walkthrough` skill first** to extract a clear narrative, then use that as input. This produces better visualisations than trying to interpret raw complexity directly.

## Before You Build

Identify two things:

### 1. What is the core thing to make understandable?

Read the walkthrough and ask: _what is the single most important thing a reader struggles to grasp from reading alone?_ This is usually one of:

- A **decision algorithm** — branching logic that leads to different outcomes based on inputs
- A **sequential process** — stages that execute in order, each transforming something
- A **system with interacting parts** — components that affect each other
- A **concept with a key mechanism** — an abstract idea that becomes clear when you can "turn the dial"

The visualisation should be built around _that one thing_, not an exhaustive diagram of everything.

### 2. What visualisation type fits?

| Core content                         | Visualisation type                                                                                   |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Decision algorithm / flowchart       | **Interactive decision tree** — live inputs that traverse the logic and highlight the resulting path |
| Sequential pipeline / process stages | **Animated step-through** — stages that activate in sequence with explanations at each step          |
| System with interacting components   | **Clickable component diagram** — click to explore each part; relationships animate on hover/click   |
| Parameter-driven concept             | **Live explorer** — sliders/inputs that change the output in real time, showing cause and effect     |
| Comparative options                  | **Side-by-side toggle** — switch between options and see what changes                                |

If the content is complex enough to merit it, combine types — e.g. a decision tree that also shows parameter effects as sliders. Richer is better _if it adds clarity_. Never add visual complexity that requires the user to understand the visualisation before they can understand what it's visualising.

**Propose the approach briefly before building.** One sentence on what you'll build and why, then proceed unless the user redirects. Don't wait for approval — describe and build.

## Two Output Modes

### Mode A: Deployed Worker site (preferred for durable explainers)

For explainers that will be shared with colleagues, maintained over time, and deployed behind Access, use the **deployed Worker framework**. This is a battle-tested shared CSS/JS engine extracted from two production sites.

**When to use:** The user wants a deployed internal site, mentions "deploy", wants something colleagues can bookmark, or the subject is complex enough to warrant multiple guided modes.

**Deployment:** Follows the standard `internal-workers-deployment` skill (Data Lab account, `cf-*` naming, wildcard Access).

**Implementation reference:** Read `reference/deployed-worker-framework.md` in this skill's directory for the explainer-specific guide covering:
- Shared CSS/JS framework (copied verbatim from existing sites)
- `window.pageConfig` data model
- Page-specific CSS patterns (domain colors, highlights, dark mode)
- Diagram HTML components (nodes, arrows, forks)
- Mobile responsive breakpoints
- Freshness checks
- Common mistakes to avoid

**Existing sites using this framework:**

| Site | Repo | URL | Shared JS? | Pages |
|------|------|-----|------------|-------|
| Worker → Logpush Fields | `cf-workers-logpush-api` | `cf-workers-logpush-api.datalab.cfdata.org` | No (single-page) | `/` (PRD companion comparing 4 options) |

**Linking from `cfrian` home page:** When deploying a new explainer, also add a `<ToolCard>` to `/Users/rian/Documents/GitHub/cfrian/src/pages/Home.tsx` (the "All Tools" hub at `cf-rian.datalab.cfdata.org`). Each new explainer's nav header should link back with `← All Tools` pointing at `cf-rian.datalab.cfdata.org`. Build with `pnpm build` and deploy with `npx wrangler deploy` after editing.



### Mode B: Single-file HTML (for quick explorations)

For one-off visualisations, quick explorations, or content that doesn't need deployment, produce a single self-contained `.html` file.

**When to use:** The user says "quick", wants to explore an idea, or the subject is simple enough for a single page without guided modes.

**Output requirements:**
- Single self-contained `.html` file — all CSS and JavaScript inline, no external file dependencies
- CDN libraries are permitted when they meaningfully improve the output (D3.js for complex graphs, Chart.js for data, anime.js for animation). Note any CDN dependencies so the user knows an internet connection is needed.
- Vanilla JS is preferred for simple interactions — don't pull a library for something you can do cleanly in 30 lines

## Design Principles (both modes)

**Clarity before richness.** Every visual element should earn its place by making the logic clearer. If removing something makes the visualisation easier to understand, remove it.

**Interactive, not passive.** The user should be able to change something and see the logic respond. A static diagram is documentation; an interactive one is understanding.

**Self-orienting.** The visualisation should include:

- A clear title
- A one-line description of what it shows
- Brief labels or tooltips on interactive controls so the user knows what they're manipulating

**Smooth and intentional.** Transitions should be smooth (200–400ms CSS transitions for most things). Animation should have a purpose — use it to show _movement through logic_ (a path being highlighted, a stage activating), not decoration.

### Visual style

Use a clean, modern design based on a clean design system. The palette uses **semantic CSS custom properties** with automatic dark mode support.

For deployed Worker sites, the tokens are defined in `shared.css`. For single-file HTML, include this token block in the `<style>`:

```css
:root {
  color-scheme: light dark;

  /* --- Surfaces (layered hierarchy) --- */
  --base: #ffffff;          /* page background */
  --elevated: #fafafa;      /* cards, panels raised above base */
  --recessed: #e6e6e6;      /* inset areas, code blocks */
  --overlay: #f5f5f5;       /* tooltips, popovers */

  /* --- Text --- */
  --text-default: #1a1a1a;
  --text-strong: #525252;   /* secondary headings, labels */
  --text-subtle: #737373;   /* descriptions, captions */
  --text-inactive: #a3a3a3; /* disabled, placeholder */

  /* --- Brand & accent --- */
  --brand: #f6821f;         /* brand orange — use sparingly for identity */
  --accent: #1a5dab;        /* dashboard blue — primary interactive */
  --accent-hover: #174e91;
  --accent-light: #e8f0fe;  /* highlight backgrounds */

  /* --- Semantic --- */
  --success: #059669;
  --success-light: #d1fae5;
  --warning: #d97706;
  --warning-light: #fef3c7;
  --danger: #dc2626;
  --danger-light: #fee2e2;
  --info: #2563eb;
  --info-light: #dbeafe;

  /* --- Chrome --- */
  --border: rgba(0, 0, 0, 0.1);
  --ring: #a3a3a3;          /* focus rings */
  --muted: #d4d4d4;         /* inactive borders, dividers */

  /* --- Typography --- */
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

@media (prefers-color-scheme: dark) {
  :root {
    --base: #0a0a0a;
    --elevated: #171717;
    --recessed: #262626;
    --overlay: #262626;

    --text-default: #f5f5f5;
    --text-strong: #a3a3a3;
    --text-subtle: #737373;
    --text-inactive: #525252;

    --brand: #f6821f;
    --accent: #5b9cef;
    --accent-hover: #7db3f5;
    --accent-light: #1a2a44;

    --success: #34d399;
    --success-light: #064e3b;
    --warning: #fbbf24;
    --warning-light: #451a03;
    --danger: #f87171;
    --danger-light: #450a0a;
    --info: #60a5fa;
    --info-light: #172554;

    --border: rgba(255, 255, 255, 0.1);
    --ring: #525252;
    --muted: #404040;
  }
}
```

**Usage rules:**

* **Surfaces** follow a hierarchy: `base` (page) < `elevated` (cards) < `recessed` (inset). Never skip levels.
* **`--brand`** (brand orange) is for identity accents only — a logo mark, a thin top border, a highlight badge. Never use it as a primary button or large fill.
* **`--accent`** (dashboard blue) is the primary interactive color — buttons, selected states, active nodes, links.
* Always set `background: var(--base); color: var(--text-default)` on `body` so dark mode works end to end.

For node/flowchart diagrams:

* Active/selected nodes: `accent` fill, white text
* Inactive nodes: `elevated` fill, `border` stroke, `text-strong` text
* The _current path_ through a decision tree should be clearly highlighted vs the greyed-out unchosen branches
* Consider a thin `brand` top-border on the page or title area for brand identity

### Patterns for common visualisation types

#### Interactive decision tree

Structure: inputs on the left or top; the tree in the centre; result panel at the bottom or right.

- Inputs should be the actual decision parameters (sliders, dropdowns, toggles)
- As inputs change, the active path through the tree updates in real time — highlight the traversed nodes and dim the unchosen branches
- The result card shows the outcome with a brief explanation of _why_ this path was taken
- Avoid drawing the entire tree if it's large — show the active path prominently and collapse or dim unused branches

#### Animated step-through

Structure: a linear sequence of stages across the top or side; a detail panel that shows what's happening at the current stage.

- Each stage is a card or node; the active one is highlighted
- Prev/Next controls (and optionally auto-play with speed control)
- The detail panel explains the stage in plain language — this is not just a label, it's the "tour guide" commentary
- Animate transitions between stages (content fades, progress bar advances)

**For deployed Worker sites**, the shared.js engine handles all of this automatically via the `pageConfig.modes` step definitions.

#### Live explorer

Structure: controls (sliders, inputs) in a sidebar; the main area shows the output updating in real time.

- Label every control clearly with its name and current value
- Show cause-and-effect — when a parameter changes, the thing that changes in the output should be visually obvious (highlight it briefly, animate it)
- Include axis labels, legends, or annotations as needed

## Saving and opening

### Deployed Worker sites

Deploy with `npx wrangler deploy` from the repo. See `reference/deployed-worker-framework.md` for the full deployment and Access setup process.

### Single-file HTML

Save to:

```
/Users/rian/git/product-ai/output/<name>.html
```

Name it after the source walkthrough or subject matter — e.g. `Interactive - Data Pipeline Systems.html`.

After saving, you MUST open it in the default browser immediately — do not ask the user to do this:

```bash
open "/Users/rian/git/product-ai/output/<name>.html"
```

Run this command yourself before finishing. Then tell the user where the file was saved and confirm it's open.
