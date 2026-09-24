# Traps

Every one of these was hit building the first explainer. They share a shape: the page
renders and looks finished, so nothing draws attention to them. Measure rather than
eyeball — most were found with `getBoundingClientRect()` in the browser console, not
by looking.

## The page renders but will not scroll

`overflow-x: hidden` on `body`. Per spec, when one axis is not `visible` the other
computes to `auto`, so `body` becomes a scroll container — and since its scrollHeight
equals its clientHeight, nothing scrolls anywhere. The wheel just does nothing.

```js
getComputedStyle(document.body).overflowY   // "auto" is the tell
window.scrollY                              // pinned at 0 while scrollHeight is huge
```

Fix: `html { overflow-x: clip; }`. `clip` does not create a scroll container.

## A full-bleed block silently stays inside the column

```css
.bleed  { margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw); }
.ladder { margin: 4rem 0 0; }   /* later in the sheet, same specificity */
```

The `margin` shorthand resets left and right to `0` and wins on source order, so the
breakout quietly does nothing. Use `margin-top` on anything that also carries `.bleed`.

Leave `width` auto and let the negative margins resolve it. Hardcoding `100vw`
overshoots by the scrollbar width, which is what tempts you into the `overflow-x`
trap above.

## An animated SVG dot sits in the top-left corner

A `<circle>` with no `cx`/`cy` is at the origin, and `animateMotion` does not move it
until its `begin` time. Staggered dots therefore pile up at (0,0) first.

```html
<circle class="pulse-dot" r="7" opacity="0">
  <set attributeName="opacity" to="1" begin="1.4s" fill="freeze"/>
  <animateMotion dur="4.2s" repeatCount="indefinite" begin="1.4s">
    <mpath href="#upflow"/>
  </animateMotion>
</circle>
```

The same trap with `<animate attributeName="cx">`: a circle whose only `cx` comes from
the animation has `cx="0"` until the timeline is running. On screen it is a flash at
most, but the 414px iframe overflow check (below) measures the frame after `onload`,
before SMIL has started, and reported an 83px circle at `left: -16` on TIST's split
figure. Give every animated circle a static `cx`/`cy` equal to its first keyframe —
it also fixes what reduced-motion users see when the timeline is paused.

Related: CSS `transform-origin` on an SVG element needs `transform-box: fill-box` to
mean what you expect. And keep `<text>` inside the `viewBox` — relying on
`overflow: visible` to rescue a stray label is fragile.

## A numbered list has a ragged left margin

Digits are tabular by default in most sans faces: every digit gets the same advance
width, so "1" is centred in a full-width slot and its ink starts right of "4". Fix
with `font-variant-numeric: proportional-nums`.

## The headings beside those numbers are also ragged

If each row is its own grid container, `grid-template-columns: auto 1fr` sizes the
column **per row** — four rows, four different column widths. Give the numeral a
font-relative floor instead, so every row computes the same:

```css
.r .num { min-width: 1.15ch; }   /* ch = advance of "0" in this same font */
```

Check the headroom rather than trusting it. Measure the widest digit against `ch`
with a hidden probe span; anything at or above `1.0` will break the alignment.

## A big numeral floats at the top of its row

`align-items: baseline` pins it to the heading and strands it above the description,
with all the empty space below. `align-items: center` centres it against the whole
block. Verify by comparing the numeral's ink centre to the text block's centre —
box centre is not ink centre when `line-height` is below 1.

## Verifying, without fooling yourself

**Byte-compare against `https://therapy-words.com/<slug>/` directly.** The zone has no
bot rules, so curl gets the real page (verified on the 2026-09-04 move: all six pages,
`sitemap.xml` and `robots.txt` matched the repo byte for byte). This was not true while
the site lived on `therapywords.elezea.com`: the `elezea.com` zone's bot rules return a
403 challenge page to curl for any HTML path, and only the workers.dev host could be
compared. If the site ever moves back onto an `elezea.com` subdomain, that trap returns.

**Byte-compare live against the repo.** Command substitution strips trailing newlines,
so `diff <(printf '%s' "$BODY") file` always reports a difference that is not real:

```bash
curl -sS "$URL/<slug>/" -o /tmp/live.html
diff /tmp/live.html public/<slug>/index.html && echo IDENTICAL
```

**A byte-compare straight after a deploy can report the old page, and the deploy was
fine.** Cloudflare serves these assets `max-age=0, must-revalidate`, but an edge node
can still hand you a stale entry for a little while. Read the header before concluding
anything, and re-fetch past the cache:

```bash
curl -sS -D- -o /dev/null "$URL/<slug>/" | grep -i cf-cache-status   # HIT means maybe stale
curl -sS -H 'Cache-Control: no-cache' "$URL/<slug>/?cb=$$" -o /tmp/live.html
```

If the cache-busted copy matches and the plain one does not, the deploy succeeded and
the edge has not caught up. Say that, rather than reporting a failed deploy.

**Fetch the directory URL, not the file.** `/<slug>/index.html` and `/index.html` both
307 to the trailing-slash form under default `html_handling`, and `curl` without `-L`
saves the empty redirect body. On 2026-08-26 that produced "DIFFERS" for two pages that
were byte-identical. Compare `$URL/<slug>/` against `public/<slug>/index.html`, and check
the live byte count is non-zero before believing either verdict.

**Verify every DOI and citation URL you write.** Publishers bot-block `curl` — MDPI and
ScienceDirect both return 403 — so a non-200 proves nothing, and the temptation is to
type a plausible-looking DOI instead. Resolve it through Crossref, which also returns
the title and authors so you can confirm it is the paper you meant:

```bash
curl -sS "https://api.crossref.org/works/10.3390/ijerph19031142" \
  | python3 -c "import json,sys; m=json.load(sys.stdin)['message']; print(m['title'][0])"
```

Searching Crossref by title (`?query.bibliographic=...`) is also how you find the rest
of an exchange — a critique, its published comment, and the reply — which is a fairer
account of a contested method than the critique alone.

**`resize_window` in the Chrome tools reports success before it applies**, and against a
maximised window it never applies at all — it returns "Successfully resized" while
`window.innerWidth` stays put. Read the width back before trusting it. When it will not
move, test responsive layout in an iframe instead, which gets real media-query
evaluation at whatever width you set:

```js
const f = document.createElement('iframe');
f.style.cssText = 'position:fixed;top:0;left:0;width:414px;height:820px;border:0;z-index:99999';
f.src = '/<slug>/';
document.body.appendChild(f);
await new Promise(r => f.onload = r);
const d = f.contentDocument, w = f.contentWindow;
[...d.querySelectorAll('body *')].filter(e => {
  const b = e.getBoundingClientRect();
  return b.width > 0 && (b.right > w.innerWidth + 1 || b.left < -1);
}).length;      // 0 = nothing overflows at 414px
```

Remove the iframe when you are done, and report the width you actually measured.

**Previewing locally:** `wrangler dev` refuses to start when the repo's wrangler is
older than the `compatibility_date` ("newest date supported by this server binary").
The site is static files, so skip it: `cd public && python3 -m http.server 8799`, then
open `http://localhost:8799/<slug>/`. Kill it when done. Deploy with
`npx wrangler@latest deploy` if the pinned wrangler fails the same way.

**Probe layouts in the browser before editing the sheet.** When the question is "which
width or size makes this fit", inject a `<style>` with each candidate rule set and measure
after each one — hero height against `innerHeight`, `h1` line count (box height ÷
`lineHeight`), the next section's `top`, and the left edge of the hero text against the
left edge of the section below it. One JS call answers all the candidates; editing the
CSS and reloading answers one per round trip, and the landing-page hero took three of
those before the probe settled it. Remove the probe style when done.

**Deploying:** assets-only Worker, so `wrangler.jsonc` has no `main` and therefore no
`assets.binding` — the binding is only valid alongside a script. `/slug` 307-redirects
to `/slug/`, which is `html_handling: auto-trailing-slash` doing its job.
