---
name: auditing-cd-collection
description: Use when the user wants to audit their whole CD collection — for remasters ("which of my CDs are remasters", "audit my collection", "re-run the CD audit") or for packaging ("list every digipak", "which of my CDs are not jewel cases", "digipak vs jewel case"). Collection-wide and produces a Google Sheet. For picking the right pressing of ONE album use finding-original-cds; for pricing a wantlist use finding-cd-bundles; for which owned CDs are not ripped yet use ripping-cds.
---

# Auditing the CD collection for remasters

## Overview

Classifies every CD in Rian's Discogs collection as remaster / original / unverified, finds a non-remastered pressing to replace each remaster with, and writes it all to a Google Sheet he can work through. **Core insight:** the whole thing runs off two Discogs endpoints plus one versions lookup, and the expensive part (~1,800 API calls) is fully cached on disk — so a re-run after a wantlist change costs one script, not the whole pipeline.

Last full run: **2026-08-23** — 792 CDs, 164 flagged, 61 on the review list after exclusions. Output: [CD Collection — Remaster Audit](https://docs.google.com/spreadsheets/d/1nTfjYqsPbMXRjtmPND0VegwjVxwMU5n_CZMvxiXD2Mk/edit). Human-readable writeup: `05-personal/music/cd-remaster-audit.md`.

## When to use

- "Which of my CDs are remasters?" · "audit my collection" · "re-run the CD audit"
- After adding replacements to the wantlist and wanting the review list refreshed
- Not for: one album (`finding-original-cds`), pricing a wantlist (`finding-cd-bundles`), vinyl (the folder ID would need changing)

## Running it

Scripts live beside this file. They read and write a working directory set by `AUDIT_DIR` — **never let data land in the skill folder.** `DISCOGS_TOKEN` is in `~/git/product-ai/.env` (also `~/.config/ebay/credentials.env`).

```bash
export AUDIT_DIR=~/.cache/cd-audit          # durable, NOT a session scratchpad
set -a; . ~/git/product-ai/.env; set +a       # DISCOGS_TOKEN
S=~/git/product-ai/.opencode/skills/auditing-cd-collection

python3 $S/fetch_collection.py    # ~10s   collection + wantlist
python3 $S/fetch_details.py       # ~25min 792 releases + 740 masters  (RESUMABLE, but see Rate limits)
python3 $S/fetch_slow.py          # ~35min same work, single-threaded, never gives up
python3 $S/classify.py            # instant, local only
python3 $S/enrich.py              # ~8min  versions lookup for ~250 masters (RESUMABLE)
python3 $S/build_sheet.py         # ~1min  creates the spreadsheet
python3 $S/format_sheet.py        # ~30s   reads sheet.json written by the previous step
```

**Order matters and the steps are not independent.** `classify.py` must run before `enrich.py` (enrich reads `classified.json` to decide which masters to look up), and `build_sheet.py` writes the `sheet.json` that `format_sheet.py` needs.

### Re-running cheaply

**Point `AUDIT_DIR` at `~/.cache/cd-audit`, not a session scratchpad.** The cache is the whole reason a re-run is cheap, and a scratchpad is deleted when the session ends — the 2026-08-23 re-run paid the full ~50 minutes again because the 08-05 cache had gone with its scratchpad. `~/.cache` survives, sits outside the repo, and never gets committed.

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

Authenticated Discogs allows 60 req/min. `fetch_details.py` and `enrich.py` use a token bucket at 50–55/min with 4 workers; in practice Discogs throttles to ~33/min anyway. **Don't raise the worker count** — latency isn't the bottleneck, the bucket is.

**Treat 60/min as the ceiling, not the sustainable rate.** Once Discogs has been throttling this egress, a fixed 46/min buys a 429 every ~25 requests, and with a 90s cooldown that delivers an effective **5.9/min** — measured 2026-08-23. Both `fetch_slow.py` and `enrich.py` now narrow their own rate on each 429 so they settle where they can actually run; the manual overrides are `DISCOGS_THROTTLE` (seconds between requests, default 1.3) and `DISCOGS_ENRICH_RATE` / `DISCOGS_ENRICH_WORKERS` (default 50/4). **After a busy session start at `DISCOGS_THROTTLE=2.2` and `DISCOGS_ENRICH_RATE=25`** — both finished with zero throttling at those settings where the defaults were collapsing.

**`fetch_details.py` gives up, and after a busy session it will.** It died at **117 of 788** on 2026-08-15 and at **763 of 792** on 2026-08-23, both with `RuntimeError: gave up on https://api.discogs.com/releases/...` — six retries with capped backoff isn't enough headroom once the same session has been hitting Discogs for something else. The cache means a re-run resumes, but it dies again at the next contended moment.

**If anything else has already hit Discogs this session, run `fetch_slow.py` from the start** and skip `fetch_details.py` entirely. One request at a time at ~46/min, 90s cooldown on a 429, never gives up — ~35 min for a full 792 + 740 against ~25 for the parallel one. It writes the same `_key`/`_missing`/`data` envelope to the same two jsonl files, so the two share a cache and either resumes the other's work. Ten extra minutes that finish beats twenty-five that don't.

(`05-personal/music/packaging-audit/fetch_releases_slow.py` is the ancestor of `fetch_slow.py` and covers releases only — the masters pass is half the run, so prefer the one in this folder.)

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

Rows leave the review list for four reasons, each stated per row on the `Excluded` tab:

1. **A non-remastered copy is already on the shelf** — matched on master ID (falling back to artist + title), in three tiers: an original-era copy, a copy carrying the original catalog number, or a copy with no remaster evidence but an unconfirmed year. Owning a remaster only matters if the original isn't already there.
2. **The replacement is already on the wantlist** — the decision is made.
3. **The replacement is already ordered** — see below.
4. **`KEEP_ARTISTS` in `build_sheet.py`** — a `{artist: reason}` dict, currently Genesis (Definitive Edition remasters by choice), Peter Gabriel and U2 (happy with the shelf copies). Add an entry to retire an artist; the reason lands verbatim on the `Excluded` tab.

### In-flight orders

**A bought-but-undelivered disc is invisible to both other exclusions** — the collection still holds the remaster, and the wantlist entry was deleted at purchase. Without this step every open order reads as outstanding work. On the 2026-08-23 run that was 27 line items.

`build_sheet.py` reads `in_flight.json` from `AUDIT_DIR` if it exists:

```json
[{"artist": "Pearl Jam", "album": "Ten", "note": "Replacement ordered 2026-08-22 (crescentmusicexchange, eBay) — in transit"}]
```

Transcribe it from `05-personal/music/cd-purchases-in-flight.md`, which is hand-kept because [the Discogs API only returns orders where you are the *seller*](https://www.discogs.com/developers). Artist must match exactly after normalising; album matches as a substring **either way**, so the order list can abbreviate (`The Rise And Fall Of Ziggy Stardust` finds `…And The Spiders From Mars`). Entries that match nothing are printed at the end of the run — treat that list as transcription drift to fix, not as a silent no-op.

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
