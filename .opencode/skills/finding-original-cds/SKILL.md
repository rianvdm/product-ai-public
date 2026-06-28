---
name: finding-original-cds
description: Use when the user wants to find and add an original (non-remastered, non-deluxe, non-club-edition) CD pressing of an album to their Discogs wantlist, or decide which Discogs CD release to buy — e.g. "find an original US CD of X", "add the original pressing to my wantlist", "which CD pressing should I get", or avoiding remaster/deluxe/anniversary/club editions. Discogs-specific.
---

# Finding original CDs on Discogs

## Overview

Pick the best **original or non-remastered** CD pressing of an album and add it to the wantlist, balancing how common a pressing is (haves), price, and US availability. **Core insight:** have/want counts and price live in the **public Discogs release API** (`WebFetch https://api.discogs.com/releases/<id>`, no auth) — the discogs MCP tools cannot return them. That's the step that gets re-derived every session; don't.

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
| Have/want + price | `WebFetch https://api.discogs.com/releases/<id>` | `community.have`/`want`, `lowest_price`, `num_for_sale`, country, year, catalog | — (the key source) |
| Cover/case photos | `curl api.discogs.com/releases/<id>` → `images[].uri`, then download + `Read` | public image URLs (no auth), then view the JPEGs | discogs.com **website** blocks `WebFetch` (403); the **API** doesn't |
| Add | `add_to_wantlist(release_id)` | confirmation | takes **release_id only** |

- **No marketplace tools exist.** `lowest_price` is the **global** low, not US-seller-only. You cannot filter by seller location — hand off `https://www.discogs.com/sell/release/<id>?ships_from=United States`.
- **The wantlist listing lags after writes.** A successful `add_to_wantlist` worked even if `get_wantlist` doesn't show it yet. To confirm a removal, re-issue the DELETE — a `404 "does not exist in the user's wantlist"` proves it's gone.

## Steps

1. **List pressings:** `search_discogs(query="<Artist> <Album>", type="release", per_page=50)`. Note the `Format: CD` IDs. (`type="release"` = specific pressings, not the master.)
2. **Drop remaster/deluxe/club:** exclude anything whose format says `Remastered`, `Deluxe Edition`, `Box Set`, `Anniversary`, `Club Edition`, or is a much-later year. `Reissue` alone is fine. **Club-edition tell:** these aren't always tagged `Club Edition` — a catalog number starting with `D` (e.g. `D 110473`) instead of the label's standard catalog/barcode is a giveaway for a BMG/Columbia House club pressing. Avoid those too.
3. **Get stats (parallel):** for each surviving CD, `WebFetch https://api.discogs.com/releases/<id>` → `community.have`, `community.want`, `lowest_price`, `num_for_sale`, country. Keep **Country = US**.
4. **Compare & pick** by the rubric below.
5. **Add:** `add_to_wantlist(release_id=<winner>)`.
6. **Hand off** the `ships_from=United States` sell link.

## Pick by (in order)

1. **Most common = highest `have`** — "the obvious one." Multiple US entries can share a catalog (e.g. `CD 5013`) but be separate pressings; the highest-have one is the common one, not necessarily the literal first press.
2. **Price sanity** — if the true first pressing carries a premium, take a cheaper common non-remastered reissue. If everything's cheap (typical for 80s/90s CDs), just take the most common.
3. **Availability = `num_for_sale`** — more for sale = better odds of a US-shipping copy.

Originality preference: original-era (release year ≈ album year) > reissue > **never** remaster/deluxe.

## Original vs reissue vs remaster

- **Original** — year matches the album's first release; no "Reissue/Remastered" in the format. (Early CDs "Made in Japan for [US label]" are often the earliest US issues.)
- **Reissue** — format says `Reissue`; same master, later run. **OK.**
- **Remaster / Deluxe / Anniversary** — later year, extra tracks/discs, different sound. **Avoid.**
- **Club Edition** — BMG/Columbia House mail-order pressing. Often tagged `Club Edition`, but the tell is a catalog # starting with `D` (e.g. `D 110473`) instead of a normal barcode. Different packaging/quality (and sometimes swaps a digipak for a jewel case, or vice versa). **Avoid.**

## Verifying packaging from photos (jewel case vs digipak)

Discogs often leaves packaging blank, so when it matters (the user wants a jewel case, not a digipak, or vice versa) — confirm it by eye. The discogs.com **website** blocks `WebFetch` (403), but the **API returns image URLs unauthenticated**, and the `Read` tool renders images visually. So:

1. `curl -s -A "<descriptive UA + contact url>" "https://api.discogs.com/releases/<id>"` → read the `images[].uri` array (public CDN links on `i.discogs.com`; Discogs requires *some* User-Agent). The `images` key is present even with no auth token.
2. `curl` each `uri` to a scratchpad `.jpg`, then `Read` it to look.

**Reading the photos:**
- Discogs shots are usually flat **scans of the printed artwork** (front, booklet panels, discs, back inlay), *not* angled photos of the physical case. Infer the case from physical tells: **rounded corners + visible fold lines + a thick/stepped cardboard spine edge → digipak**; square corners + a flat tray-card back → jewel case.
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
- Flagging "you already own this" because the master shows `✓ in your collection` — **don't.** The user knows. They're almost always filling a vinyl→CD format gap, and the master-level marker only means they own *some* pressing, not the CD. Add it without the caveat.

## Example — Bryan Adams, *Reckless* (US CD)

API stats across US CD candidates: `11044695` (920 have, $4, 17 for sale) ≫ `3918297` reissue (377, $2) > `4258827` earliest CD 5013 (310, $2.23, only 4 for sale). Picked **11044695** — most common, original 1984 pressing, cheap, best-stocked. Nothing was expensive, so no original-vs-price tradeoff.

