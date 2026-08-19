---
name: finding-original-cds
description: Use when the user wants to find and add an original (non-remastered, non-deluxe, non-club-edition) CD pressing of an album to their Discogs wantlist, or decide which Discogs CD release to buy — e.g. "find an original US CD of X", "add the original pressing to my wantlist", "which CD pressing should I get", or avoiding remaster/deluxe/anniversary/club editions. Discogs-specific.
---

# Finding original CDs on Discogs

## Overview

Pick the best **original or non-remastered** CD pressing of an album and add it to the wantlist, balancing how common a pressing is (haves), price, and US availability. **Core insight:** have/want counts live in the **public Discogs release API** (`WebFetch https://api.discogs.com/releases/<id>`, no auth) — the discogs MCP tools cannot return them — and **the live price lives in a second call, `/marketplace/stats/<id>`**. That's the step that gets re-derived every session; don't.

Default target is a **US CD** unless the user says otherwise.

## When to use

- "Find an original / non-remastered CD of [album]" · "add the original pressing to my wantlist"
- "Which [album] CD should I get / buy?" · comparing pressings · avoiding remaster/deluxe/anniversary editions

Not for: vinyl-specific hunts (same method, swap the format filter), buying/checkout, or non-Discogs catalogs.

## Tool reality — what returns what

| Need | Tool | Returns | Missing |
|------|------|---------|---------|
| List pressings | `search_discogs(type="release")` | format, label, year, ID | **country, have/want** |
| Pressing details | `get_release(<id>)` (MCP) | country, catalog #, format, tracklist | **have/want, price** |
| Have/want + stock | `WebFetch https://api.discogs.com/releases/<id>` | `community.have`/`want`, `num_for_sale`, country, year, catalog | **a trustworthy price** — see below |
| **The price you quote** | `curl "https://api.discogs.com/marketplace/stats/<id>?curr_abbr=USD"` | live `{num_for_sale, lowest_price, blocked_from_sale}` | — (the only current figure) |
| Which master is on the disc | same call → `identifiers[]` (`type == "Matrix / Runout"`) + `notes` | matrix runout, SID codes, pressing-plant IDs, manufacturing-window notes | — (the only hard evidence; see matrix section) |
| Cover/case photos | `curl api.discogs.com/releases/<id>` → `images[].uri`, then download + `Read` | public image URLs (no auth), then view the JPEGs | discogs.com **website** blocks `WebFetch` (403); the **API** doesn't |
| Add | `add_to_wantlist(release_id)` | confirmation | takes **release_id only** |

- **Quote price from `/marketplace/stats/<id>`, never from the release record.** The release object's `lowest_price` goes stale and gives no sign of it. Sampled across 10 releases on 2026-08-16, **3 disagreed with the live figure** — *Ziggy Stardust* `12217950` read **$0.20** on the release and **$31.38** on marketplace stats, a 157× error that put a $31 disc on the wantlist as if it were pocket change. The other two were off by ~$1 in both directions. `num_for_sale` matched in all 10, so the release record is fine for stock depth; it's the price field that lies. One extra call per finalist.
- **No marketplace tools exist.** `lowest_price` is the **global** low, not US-seller-only. You cannot filter by seller location — hand off `https://www.discogs.com/sell/release/<id>?ships_from=United States`.
- **The wantlist listing lags after writes.** A successful `add_to_wantlist` worked even if `get_wantlist` doesn't show it yet. To confirm a removal, re-issue the DELETE — a `404 "does not exist in the user's wantlist"` proves it's gone.
- **The `/versions` feed can hide a `Remastered` tag — never filter remasters on it alone.** Its `format` string is not a faithful flattening of the release's `formats[]`; it appears to carry only the *first* format object's descriptions, so a `Remastered` hanging off a second `All Media` entry vanishes. On *Ziggy Stardust* (master `1561`), release `1030082` reads `Album, Reissue` in the versions feed but `CD:Album/Reissue, CD:Compilation, All Media:Remastered` at release level — it's the 2002 30th Anniversary 2CD remaster, and it survived a keyword filter into the shortlist. Same trap on `9599077`. **Use `/versions` for cheap fan-out (country, catalog, have-counts), then confirm every finalist against `/releases/<id>` `formats[]` before ranking it.**
- **For a big catalogue title, go straight to the versions endpoint — `search_discogs` won't cope.** *Thriller* has 59 US CD versions and *Bad* 37, far past what a 50-result release search surfaces usefully. `curl "https://api.discogs.com/masters/<id>/versions?format=CD&country=US&per_page=100"` returns every pressing **with `stats.community.in_collection` inline**, so one call gives you the country filter and the have-counts together and you only fetch `/releases/<id>` for the handful of finalists. Get the master id from `database/search?type=master`.
- **Don't retry a 429 more than once, and never in a tight loop.** A `429`/`504` from the MCP means Discogs is throttling a shared egress IP, and repeated attempts extend the penalty (see [[corrections]] → Discogs API Rate Limits). One retry after a window reset is the limit; after that, hand Rian the `discogs.com/release/<id>` pages. Three manual retries are what tripped the circuit breaker on 2026-08-04.
- **MCP rate-limit fallback.** The discogs MCP has a circuit breaker that trips for ~10 min under load (`"Discogs rate-limit circuit tripped", retryAfterSecs: <n>`) — it takes down `search_discogs`, `get_release`, **and** the wantlist tools at once. The **public API needs no auth for reads**, so you can keep working: `curl "https://api.discogs.com/database/search?q=<Artist>+<Album>&type=master"` returns master IDs, and `/masters/<id>/versions?format=CD&country=US` + `/releases/<id>` already work unauthenticated. **Wantlist writes work over the PAT too** — so a tripped circuit blocks nothing. (Corrected 2026-08-05; this section previously claimed writes had no public-API substitute, which sent you to hand Rian links for no reason.)

```bash
curl -X PUT    -H "Authorization: Discogs token=$DISCOGS_TOKEN" -A "<UA>" \
  "https://api.discogs.com/users/elezea-records/wants/<release_id>"   # 201 = added
curl -X DELETE -H "Authorization: Discogs token=$DISCOGS_TOKEN" -A "<UA>" \
  "https://api.discogs.com/users/elezea-records/wants/<release_id>"   # 204 = removed
```

Re-issue the DELETE to confirm a removal — `404 "does not exist in the user's wantlist"` proves it. When the MCP 429s, do the whole add/remove flow over curl rather than stopping; still respect the one-retry rule on the MCP itself.

**Wantlist *reads* now have a substitute (as of 2026-08-05).** Rian's Discogs username is **`elezea-records`** (not `rianvdm` — that returns nulls), and a personal access token is stored as `DISCOGS_TOKEN` in `~/git/product-ai/.env` and `~/.config/ebay/credentials.env`. So a read works without the MCP at all:

```bash
curl -s -H "Authorization: Discogs token=$DISCOGS_TOKEN" -H "User-Agent: <UA>" \
  "https://api.discogs.com/users/elezea-records/wants?per_page=100"
```

A PAT also raises the rate limit to 60/min. Prefer it over burning retries on a throttled MCP.

## Steps

1. **List pressings:** `search_discogs(query="<Artist> <Album>", type="release", per_page=50)`. Note the `Format: CD` IDs. (`type="release"` = specific pressings, not the master.)
2. **Drop remaster/deluxe/club:** exclude anything whose format says `Remastered`, `Deluxe Edition`, `Box Set`, `Anniversary`, `Club Edition`, or is a much-later year. `Reissue` alone is fine. **Club-edition tell:** these aren't always tagged `Club Edition` — a catalog number starting with `D` (e.g. `D 110473`) instead of the label's standard catalog/barcode is a giveaway for a BMG/Columbia House club pressing. Avoid those too.
3. **Get stats (parallel):** for each surviving CD, `WebFetch https://api.discogs.com/releases/<id>` → `community.have`, `community.want`, `num_for_sale`, country. Keep **Country = US**. Then, for the finalists only, `curl "https://api.discogs.com/marketplace/stats/<id>?curr_abbr=USD"` for the live price — that's the number you report and rank on.
4. **Compare & pick** by the rubric below.
5. **Verify the master (conditional):** if a finalist's manufacturing window straddles a known remaster date, or its year is blank, check `identifiers[]` for the matrix runout before adding — see the matrix section for the trigger list.
6. **Add:** `add_to_wantlist(release_id=<winner>)`.
7. **Hand off** the `ships_from=United States` sell link.

## Pick by (in order)

0. **`num_for_sale: 0` disqualifies, no matter how common.** Check this before ranking — a pressing nobody is selling can't be bought, and a high `have` count actively disguises that. Michael Jackson *Thriller*'s 1983 US original (`3430475`) has 783 haves and **zero** copies for sale; three of the four *Bad* candidates were the same. Rank only the pressings with stock.
1. **Most common = highest `have`** — "the obvious one." Multiple US entries can share a catalog (e.g. `CD 5013`) but be separate pressings; the highest-have one is the common one, not necessarily the literal first press.
2. **Price sanity** — if the true first pressing carries a premium, take a cheaper common non-remastered reissue. If everything's cheap (typical for 80s/90s CDs), just take the most common.
3. **Availability = `num_for_sale`** — among pressings that have stock, more for sale = better odds of a US-shipping copy.

Originality preference: original-era (release year ≈ album year) > reissue/repress of the same master > **never** remaster/deluxe. **The hard line is _remastered_, not later-year:** a reissue or repress — even one with a blank or much-later year — is fine as long as the format doesn't say `Remastered`. Don't reject a pressing just because its year is later than the album or unknown; only the remaster tag disqualifies it.

## Original vs reissue vs remaster

- **Original** — year matches the album's first release; no "Reissue/Remastered" in the format. (Early CDs "Made in Japan for [US label]" are often the earliest US issues.)
- **Reissue / Repress** — format says `Reissue` or `Repress` (or just carries a later/blank year); *nominally* the same master, later run. **OK — this is the common, acceptable case; don't overthink it.** The tag is user-submitted, though, so it's a claim about the run, not a guarantee about the audio — see the matrix section for when to actually check.
- **Remaster / Deluxe / Anniversary** — format says `Remastered`, or a later year with extra tracks/discs; different sound. **Avoid.** **Catalog-number tell:** a remaster almost always gets a *new* catalog number while plain reissues keep the original's — so same catalog # as the first press is *strong evidence* of the same (non-remastered) master. E.g. SRV *Texas Flood* `EK 38734` (original + all its reissues) vs `EK 65870`/`88697830242` (remasters); Sade *Love Deluxe* `EK 53178` vs `EK 85243` remaster; every non-remaster Pink Floyd DSOTM shares `CDP 7 46001 2`. **It is evidence, not proof** — labels do keep printing the old catalog number on runs pressed after a remaster exists. When it matters, confirm with the matrix runout (next section).

  **Split catalog numbers before comparing them.** The `/masters/<id>/versions` endpoint packs several into one `catno` string — `"16029-2, 299 143"` — while `/releases/<id>` lists them separately under `labels[]`. Strip punctuation off both sides without splitting on the comma first and you compare `160292299143` against `160292`, which never matches, so a genuine same-catalog pressing silently reads as "different catalog." Split on `[,;/]`, normalise each part, then intersect the sets. This is what hid the fact that Rian's 1990 Phil Collins *Face Value* `16029-2` carries the same catalog as the 1985 and 1988 pressings, against the 2016 remaster's `R2 550171` (found 2026-08-05; fixing it moved 7 albums out of the "different catalog" bucket in the collection-wide audit).
- **Club Edition** — BMG/Columbia House mail-order pressing. Often tagged `Club Edition`, but the tell is a catalog # starting with `D` (e.g. `D 110473`) instead of a normal barcode. Different packaging/quality (and sometimes swaps a digipak for a jewel case, or vice versa). **Avoid.**

## "Should I replace a remaster I already own?" — check, don't assume

The rubric above says avoid remasters when *buying*. It does **not** follow that every remaster in the collection is a downgrade, and answering per-album takes about five minutes.

**Three sources carry the evidence, in this order:**

1. **`https://www.dyradb.com/?artist=<Artist+Name>`** — dynamic range per edition, matched by barcode. Fetches fine. Coverage is patchy (nothing at all for Dire Straits' *On The Night*, Deep Purple, or Black Sabbath's debut), so a miss here means "unmeasured", never "fine".
2. **`https://paoprod.com/projects/album-comparisons/<artist-album>/`** — A/B write-ups of specific pressing pairs with a verdict. Fetches fine, but the index page is JS-rendered, so **find the slug with a web search rather than curling the index**.
3. **magicvinyldigital.net** — per-edition DR tables. Fetches fine.

**Steve Hoffman forums, Home Theater Forum and loh-humm.com all block WebFetch (403).** Don't burn turns on them; a search summary of a forum thread is the most you'll get, and see the warning below about those.

**The answer is genuinely per-catalogue. Measured 2026-08-16:**

| Album | Owned | Verdict |
|---|---|---|
| Dire Straits *Brothers In Arms* | 1996 Ludwig/Gateway | **Replace.** 1985 John Dent original is DR16 vs DR12 |
| Dire Straits *On Every Street* | 2000 Warner SBM | **Replace.** 1991 original DR12 vs DR10 |
| Fleetwood Mac *Rumours* | 2004 Rhino (Inglot/Hersch) | **Replace.** PAO calls the 1984 CD the decisive winner |
| Bon Jovi ×4 | 1998–99 Mercury (Marino) | **Replace.** +7 dB and "boxed in" on *Slippery*; *Cross Road* measures DR8 |
| **Black Sabbath *Black Sabbath* / *Paranoid*** | 2004 Sanctuary (Ray Staff) | **KEEP.** The Staff/Black Box masters are the *recommended* ones; the 1986 Castle "originals" are the muddy discs |
| **Deep Purple *Machine Head*** | 2012 Jon Astley | **KEEP.** Beats the bass-heavy 1997; closest to the original vinyl |
| **Deep Purple *Made In Japan*** | 2014 (original 1972 mix) | **KEEP.** The 1998 EMI 25th is the one with the bad reputation |

**So lead with the catalogue's history, not the tag.** Where the first CD issue was a poor transfer — early-80s Castle, thin 80s licensee pressings — the remaster is usually the upgrade, and wantlisting "the original" makes the collection worse.

**Say which claims are measured and which are forum consensus.** And **fetch the page before quoting it**: on 2026-08-16 a search summary attributed a QuadraphonicQuad quote to *On Every Street* when the thread was discussing *Brothers In Arms*, which produced a confident and wrong "keep the remaster" recommendation that the DR table then reversed.

## Confirming the master from the matrix runout

The catalog number can lie; the **matrix runout** is the physical evidence. It's in the release API under `identifiers[]` where `type == "Matrix / Runout"` — free, unauthenticated, same `curl` you already made:

```bash
curl -s -A "<UA>" "https://api.discogs.com/releases/<id>" | python3 -c "
import sys,json; r=json.load(sys.stdin)
print((r.get('notes') or '')[:400])
[print(' ',i.get('type'),'|',i.get('description'),'|',i.get('value')) for i in r.get('identifiers',[])]"
```

**What to look for:** a matrix that embeds the **mastering catalog code** ties the disc to a known master. `2A EK38112 46 C2` carries `EK38112` — the original *Thriller* master — so every pressing showing `1A/2A EK 38112` is the original regardless of its Discogs year. A matrix with only a **manufacturing part number** and no mastering code (`DIDP-020022 28` — Sony's part ID) identifies the plant run, **not the master**, and proves nothing.

**When to bother.** Not every time — for a cheap 90s reissue with a clean catalog match, skip it. Run the check when:
- The pressing's manufacturing window **straddles a known remaster date** (Discogs `notes` often state the window, e.g. "manufactured between 1995 and 2003" vs the Oct 2001 Epic remasters). This is the trap.
- The year is blank *and* the release is a finalist you're about to add.
- Rian asks about sound quality, or pushes back on a "same master" claim.

**When the matrix can't confirm it, say so plainly** and pick a sibling that can. Don't upgrade "no contrary evidence" into "verified." On 2026-08-04 a *Thriller* repress (`4548499`, `DIDP-020022`, mfg 1995–2003) was recommended as a safe non-remaster on the catalog-number heuristic alone; the matrix carried no mastering code and the window ran past the 2001 Grundman remaster. Swapped for `10343315` (`2A/1A EK 38112`, in stock, same price).

## Verifying packaging from photos (jewel case vs digipak)

Discogs often leaves packaging blank, so when it matters (the user wants a jewel case, not a digipak, or vice versa) — confirm it by eye. The discogs.com **website** blocks `WebFetch` (403), but the **API returns image URLs unauthenticated**, and the `Read` tool renders images visually. So:

1. `curl -s -A "<descriptive UA + contact url>" "https://api.discogs.com/releases/<id>"` → read the `images[].uri` array (public CDN links on `i.discogs.com`; Discogs requires *some* User-Agent). The `images` key is present even with no auth token.
2. `curl` each `uri` to a scratchpad `.jpg`, then `Read` it to look.

**Reading the photos:**
- Discogs shots are usually flat **scans of the printed artwork** (front, booklet panels, discs, back inlay), *not* angled photos of the physical case. Infer the case from physical tells: **rounded corners + visible fold lines + a thick/stepped cardboard spine edge → digipak**; square corners + a flat tray-card back → jewel case.
- **Strongest jewel-case tell = the back inlay.** A jewel case's tray card is a flat rectangle with the spine text printed down **both** the left and right edges (the two fold-over spine flaps) — see it and it's a jewel case. A digipak has no tray card and folds the other way, so it never shows that dual-spine flat back.
- **Track count is a *regional* tell, not a digipak tell.** A bonus track / higher track count can just mark a regional issue — e.g. the US Matador *Music Has the Right to Children* jewel case has all 18 tracks (incl. "Happy Cycling"), same as the UK digipak. Don't reject a pressing on track count; verify the **case shape**.
- A standard **UPC barcode** on the back argues against a club edition; club pressings often drop the barcode and carry a `D`-prefixed catalog number (see above).
- If no image shows the actual case and the scans are ambiguous, **say so — don't guess.** Fall back to the seller's own marketplace listing photos, which usually show the physical item.

## Output

Report to the user, in this shape:
1. A candidates table — `ID · catalog/pressing · have · want · low price · # for sale` (US, non-club CDs only).
2. The pick + one line why (most common / price / availability).
3. The `add_to_wantlist` confirmation.
4. The US-seller link: `https://www.discogs.com/sell/release/<id>?ships_from=United States`.

## Common mistakes

- Trusting `search_discogs` for country or popularity — it has neither; you must `get_release` / hit the API.
- Picking the literal first pressing when the user asked for the *common* one — optimize for haves unless they say "first pressing."
- Promising "ships from US" — you can only confirm a US *pressing*; seller location needs the sell-link filter.
- Re-checking `get_wantlist` right after adding and panicking it's missing — that's listing lag, not a failure.
- Treating the catalog-number match as proof of the master. It's evidence. If the pressing run could postdate a remaster, read the matrix or say you can't confirm.
- Flagging "you already own this" because the master shows `✓ in your collection` — **don't.** The user knows. They're almost always filling a vinyl→CD format gap, and the master-level marker only means they own *some* pressing, not the CD. Add it without the caveat.

## Example — Bryan Adams, *Reckless* (US CD)

API stats across US CD candidates: `11044695` (920 have, $4, 17 for sale) ≫ `3918297` reissue (377, $2) > `4258827` earliest CD 5013 (310, $2.23, only 4 for sale). Picked **11044695** — most common, original 1984 pressing, cheap, best-stocked. Nothing was expensive, so no original-vs-price tradeoff.


**Once pressings are on the wantlist, `finding-cd-bundles` finds eBay sellers holding several of them at once** (it searches by each pressing's UPC, so it inherits the master judgement made here). Use it before buying — batching saves shipping.

**Going the other direction — "which of my CDs are remasters?" — is `auditing-cd-collection`,** which applies this rubric across the whole collection at once and writes a Google Sheet. That one produces the *candidate list*; deciding whether any given candidate is actually worth replacing is the "Should I replace a remaster I already own?" section above, because the answer turns on the album's own CD history rather than on the tag.
