---
name: auditing-cd-collection
description: Use when the user wants to audit their whole CD collection — for remasters ("which of my CDs are remasters", "audit my collection", "re-run the CD audit") or for packaging ("list every digipak", "which of my CDs are not jewel cases", "digipak vs jewel case"). Collection-wide and produces a Google Sheet. For picking the right pressing of ONE album use finding-original-cds; for pricing a wantlist use finding-cd-bundles.
---

# Auditing the CD collection for remasters

## Overview

Classifies every CD in Rian's Discogs collection as remaster / original / unverified, finds a non-remastered pressing to replace each remaster with, and writes it all to a Google Sheet he can work through. **Core insight:** the whole thing runs off two Discogs endpoints plus one versions lookup, and the expensive part (~1,800 API calls) is fully cached on disk — so a re-run after a wantlist change costs one script, not the whole pipeline.

Last full run: **2026-08-05** — 780 CDs, 171 flagged, 135 on the review list after exclusions. Output: a Google Sheet, plus a human-readable writeup alongside it.

## When to use

- "Which of my CDs are remasters?" · "audit my collection" · "re-run the CD audit"
- After adding replacements to the wantlist and wanting the review list refreshed
- Not for: one album (`finding-original-cds`), pricing a wantlist (`finding-cd-bundles`), vinyl (the folder ID would need changing)

## Running it

Scripts live beside this file. They read and write a working directory set by `AUDIT_DIR` — **never let data land in the skill folder.** `DISCOGS_TOKEN` is in `~/git/product-ai/.env` (also `~/.config/ebay/credentials.env`).

```bash
export AUDIT_DIR=/path/to/scratchpad
set -a; . ~/git/product-ai/.env; set +a       # DISCOGS_TOKEN
S=~/git/product-ai/.opencode/skills/auditing-cd-collection

python3 $S/fetch_collection.py    # ~10s   collection + wantlist
python3 $S/fetch_details.py       # ~35min 780 releases + 737 masters  (RESUMABLE)
python3 $S/classify.py            # instant, local only
python3 $S/enrich.py              # ~8min  versions lookup for ~250 masters (RESUMABLE)
python3 $S/build_sheet.py         # ~1min  creates the spreadsheet
python3 $S/format_sheet.py        # ~30s   reads sheet.json written by the previous step
```

**Order matters and the steps are not independent.** `classify.py` must run before `enrich.py` (enrich reads `classified.json` to decide which masters to look up), and `build_sheet.py` writes the `sheet.json` that `format_sheet.py` needs.

### Re-running cheaply

The two slow steps append to `releases.jsonl` / `masters.jsonl` / `enrich.jsonl` and skip anything already cached. So:

| What changed | What to re-run |
|---|---|
| Wantlist only | `fetch_collection.py` → `build_sheet.py` → `format_sheet.py` (~2 min) |
| Classification logic | `classify.py` → `enrich.py` → `build_sheet.py` → `format_sheet.py` |
| Sheet layout only | `build_sheet.py` → `format_sheet.py` |
| New CDs added to the collection | all of it — but cached releases are skipped, so only the new ones are fetched |

**`build_sheet.py` always creates a NEW spreadsheet.** Trash the old one first or Drive fills with drafts:

```bash
gws drive files update --params '{"fileId":"<OLD_ID>"}' --json '{"trashed":true}'
```

### Rate limits

Authenticated Discogs allows 60 req/min. Both fetchers use a shared token bucket at 50–55/min with 4 workers; in practice Discogs throttles to ~33/min anyway. **Don't raise the worker count** — latency isn't the bottleneck, the bucket is. A sequential version took 50 min for what now takes 35.

**`fetch_details.py` gives up, and after a busy session it will.** On 2026-08-15 it died at **117 of 788** with `RuntimeError: gave up on https://api.discogs.com/releases/...` — six retries with capped backoff wasn't enough headroom because the same session had already been running seller scans against the same egress. The cache means a re-run resumes, but it can die again at the next contended moment.

**If Discogs has already been hit hard this session, use the single-threaded fetcher instead:** `05-personal/music/packaging-audit/fetch_releases_slow.py`. One request at a time at ~46/min, cools down 90s on a 429, and never gives up — ~17 min for 788 against ~8 for the parallel one. It appends to the same `releases.jsonl` in the same shape, so the two are interchangeable and share a cache. Seventeen minutes that finishes beats eight that doesn't.

### Check `gws auth` before a long fetch, not after

`gws` tokens expire silently (`401 invalid_grant: Token has been expired or revoked`) and re-authing needs an **interactive browser login Claude cannot drive** — Rian has to run `gws auth login` himself. Discovered on 2026-08-15 with 20 minutes of fetching already committed. `gws drive files list --params '{"pageSize":2}'` is a one-second read that catches it. Run it first.

## The classification rubric

Evidence, strongest first. All of it lands in the sheet's `Why flagged` column so a wrong call stays visible.

| Verdict | Trigger |
|---|---|
| **Remaster** | Format tag `Remastered`, or the notes say so |
| **Audiophile edition** | A reissue-only line (MFSL, SHM-CD, XRCD, gold disc), or an encoding pressed 3+ years after the album |
| **Deluxe/expanded** | Tag `Deluxe Edition` / `Anniversary Edition` / `Expanded Edition` |
| **Likely remaster** | Bit-depth or remix talk on a disc pressed 3+ years later |
| **Undated pressing** | Album year known, pressing year blank — judge on catalog number instead |
| **Later press, unverified** | 5+ years after the CD debut, no remaster evidence |
| **Original-era** | Within ~4 years of the album's CD debut, no remaster evidence |

### Four traps this handles, all of which produced wrong answers first

1. **Encodings are not remasters.** HDCD, SACD, multichannel and Sony SBM shipped on plenty of *original* releases — DC Talk *Supernatural* and Lifehouse *No Name Face* are HDCD originals. They only count as evidence when the disc also postdates the album by 3+ years. Without this gate ~19 originals get flagged.
2. **Pre-1983 albums must be measured from the CD era.** The first CD of a 1971 album necessarily arrives a decade late and is still the original CD master. The rubric compares against `max(album_year, 1983)`. Without it the whole classic-rock shelf looks suspect.
3. **`\bre-?master` needs the word boundary.** Without it the regex matches "P|re-Master|ing" — the WCI Record Group credit printed on genuinely original 80s pressings. Cost two false positives (Phil Collins *Face Value*, Prince *Purple Rain*).
4. **Catalog numbers must be split before comparing.** Discogs packs several into one field (`"16029-2, 299 143"`) while a release's own labels list them separately. Normalising both sides to one blob makes every partial match fail silently. Splitting on the comma first moved 7 albums out of the "differs from the earliest CD" bucket. See [[finding-original-cds]], which carries the same gotcha.

## Two replacement columns, and why

`build_sheet.py` offers both, because they disagree exactly where it matters:

- **Most common non-remastered** — ranked by owner count per the `finding-original-cds` rubric. Right for an 80s/90s album.
- **Earliest CD pressing** — right for anything predating the CD era. The most-owned *Kind Of Blue* is a **2009** run; the original CD is **1984 `CK 08163`**. Same for *Somethin' Else* (2008 vs 1986 `CDP 7 46338 2`).

Discogs tags don't catch every modern reissue, so for jazz and classic rock read the earliest column.

## Exclusions

Rows leave the review list for three reasons, each stated per row on the `Excluded` tab:

1. **A non-remastered copy is already on the shelf** — matched on master ID (falling back to artist + title), in three tiers: an original-era copy, a copy carrying the original catalog number, or a copy with no remaster evidence but an unconfirmed year. Owning a remaster only matters if the original isn't already there.
2. **The replacement is already on the wantlist** — the decision is made.
3. **`KEEP_ARTISTS` in `build_sheet.py`** — currently `{"Genesis"}`, because Rian wants the Definitive Edition Remasters. Edit that set to add more.

**Nothing is deleted.** Excluded rows move to their own tab with the reason, so every call is auditable and reversible.

## Gotchas

- **The wantlist read needs the PAT**, not the MCP — `elezea-records`, not `rianvdm`. See [[finding-original-cds]] for the auth details and the listing-lag warning.
- **`gws` takes the request body on the command line**, and macOS caps that at 1 MB. `build_sheet.py` chunks values at 110 rows and `format_sheet.py` batches requests at 22 for this reason. Don't raise them.
- **Catalog numbers must be written as text.** `USER_ENTERED` turns `0602567565659` into a number and eats the leading zero; the `cell(force_text=…)` path prefixes an apostrophe.
- **Bound the checkbox data-validation range.** An unbounded range paints checkboxes onto the spare grid rows, so `values.get` reports more rows than exist.
- **What this never proves:** Discogs tags are user-submitted, so a missing `Remastered` tag is the absence of a claim, not evidence of an original master. No matrix runouts are read — that is the only real proof, and it is a per-disc lookup. For an album actually about to be bought, run [[finding-original-cds]].
- **`/versions` can hide a `Remastered` tag, and `enrich.py` reads exactly that field** (`parse()` → `v.get("format")`). The versions feed appears to carry only the *first* format object's descriptions, so a `Remastered` hanging off a second `All Media` entry vanishes — release `1030082` (Bowie *Ziggy Stardust*) reads `Album, Reissue` there but `All Media:Remastered` at release level. **Consequence: a suggested replacement can itself be a remaster.** Confirmed 2026-08-05. Not yet fixed here — the fix is a `/releases/<id>` confirmation per candidate, which is a real cost across ~250 masters. Until then, treat suggested replacements as candidates and confirm the finalist with [[finding-original-cds]] before buying.

## The packaging audit — same collection, different question

"Which of my CDs are digipaks / not jewel cases?" runs the same pipeline with a different classifier. Scripts: `05-personal/music/packaging-audit/`, writeup `05-personal/music/cd-packaging-audit.md`. Last run **2026-08-15**: 788 CDs → **165 confirmed non-jewel, 144 jewel, 19 ambiguous, 460 unknown**.

Three things that transfer:

1. **Discogs has no packaging field.** It appears only when a contributor typed it into `formats[].text` or mentioned it in `notes`, and **58% of the collection has neither**. Any "list every X" request against packaging has to ship the coverage gap as a visible tab, not a silent omission.
2. **Notes carry ~3× the packaging signal of the format field** (33 vs 10 across the first 229 releases), which is the entire justification for the per-release fetch. The **collection summary and the full release record carry identical `formats[].text`** — so if notes aren't needed, skip the fetch entirely.
3. **A packaging word near a disc is not a claim about the disc's packaging.** `gatefold` matched jewel cases holding gatefold *booklets*, and matched the phrase "the album wallets **are not** gatefold". Strong terms (digipak, digisleeve, digibook, card sleeve) are positive statements; weak ones (gatefold) lose to an explicit jewel-case mention in the same text. A slipcase usually wraps a jewel case and is **ambiguous, not a digipak**.

## Related

- [[finding-original-cds]] — picking the right pressing for one album
- [[finding-cd-bundles]] — pricing the wantlist against eBay and Discogs
- `05-personal/music/cd-remaster-audit.md` — the human-readable writeup of the last run
- `05-personal/music/cd-packaging-audit.md` — the digipak-vs-jewel-case run
