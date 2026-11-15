# Discogs API reference for pressing hunts

Shared by `finding-original-cds` and `finding-original-vinyl`. Format-specific judgement (what counts as an original, club tells, cut identity) lives in each skill; this file covers what each endpoint returns, the auth and rate-limit rules, and wantlist writes.

## What returns what

| Need | Call | Returns | Missing |
|------|------|---------|---------|
| Master ID | `GET /database/search?q=<Artist>+<Album>&type=master` | master IDs | — |
| Every pressing, cheaply | `GET /masters/<id>/versions?format=<CD\|Vinyl>&country=US&per_page=100` | ID, country, label, `catno`, a flattened `format` string, `stats.community.in_collection`/`in_wantlist` | a faithful `Remastered` tag (see below); price |
| Pressing details | `GET /releases/<id>` | `formats[]`, `labels[]`, `community.have`/`want`/`rating`, `tracklist` with durations, `extraartists` (mastering and cutting credits), `identifiers[]` (runouts, barcodes), `notes`, `images[]` | a trustworthy price |
| **Live floor price and stock** | `GET /marketplace/stats/<id>?curr_abbr=USD` | `num_for_sale`, `lowest_price`, `blocked_from_sale` | condition of the floor copy |
| **Price by condition** | `GET /marketplace/price_suggestions/<id>` (token required) | suggested price per grade, Mint through Poor, in USD | — |
| **What owners say about a pressing** | `GET /releases/<id>/reviews?per_page=100` (undocumented, works with the token) | `results[].review_plaintext`, `date_added` | — |
| A seller's stock | `GET /users/<seller>/inventory?per_page=100&sort=artist&sort_order=asc` | listings with release ID, condition, price, `ships_from`, comments | pages past 100 (see below) |
| Photos | `images[].uri` from the release record, downloaded and opened with `Read` | public JPEGs | — |

The discogs MCP's `search_discogs` and `get_release` return neither have/want counts nor prices. Use the REST calls above for anything you rank on.

## Prices

- **Quote the floor from `/marketplace/stats/<id>`, never from the release record.** The release object's `lowest_price` goes stale without warning. In a 10-release sample on 2026-08-16, three disagreed with the live figure; *Ziggy Stardust* `12217950` read $0.20 on the release and $31.38 live. `num_for_sale` matched in all ten, so the release record is fine for stock depth.
- **The floor is condition-blind.** A $6 floor under a $40 VG+ suggestion is usually a worn copy. Compare pressings on the VG+ suggestion; report the floor alongside it.
- **The condition grades are one number scaled by fixed ratios.** Across every release checked on 2026-11-14, NM was 0.89× Mint and VG+ 0.68× Mint, so the grades aren't independent measurements. When a suggestion sits far above a deep floor (UK *Violator* `46905`: VG+ $262 with 30 copies listed from $50), say the suggestion looks inflated rather than quoting it as the market price.
- **`lowest_price` is the global floor.** No API call filters by seller location. Hand off `https://www.discogs.com/sell/release/<id>?ships_from=United%20States`.
- **Sold history (last sold, median) is only on the release web page**, which blocks `WebFetch` and `curl` with a 403. The API has no equivalent.

## The versions feed hides tags

The `/versions` `format` string carries only the first format object's descriptions, so a `Remastered` attached to a second `All Media` entry disappears. *Ziggy Stardust* `1030082` reads `Album, Reissue` in the feed but `All Media:Remastered` at release level. **Use `/versions` for fan-out, then confirm every finalist's `formats[]` and credits on `/releases/<id>`.** It also packs several catalog numbers into one `catno` string (`"16029-2, 299 143"`); split on `[,;/]` before comparing.

## Runouts

Runouts sit in `identifiers[]` where `type == "Matrix / Runout"`, next to the free-text `notes` that often record the pressing plant and manufacturing window:

```bash
curl -s -A "<UA>" "https://api.discogs.com/releases/<id>" | python3 -c "
import sys,json; r=json.load(sys.stdin)
print((r.get('notes') or '')[:400])
[print(' ',i.get('type'),'|',i.get('description'),'|',i.get('value')) for i in r.get('identifiers',[])]"
```

What a runout proves differs by format; each skill says how to read it.

## Seller inventories

`/users/<seller>/inventory` stops at page 100 (10,000 listings) for anyone else's inventory: `"Pagination above 100 disabled for inventories besides your own"`. For a bigger seller, fetch `sort=artist&sort_order=asc` and `sort_order=desc`, up to 100 pages each, and dedupe on listing ID. That covered all 19,258 FrequencesDisquaire listings on 2026-11-14.

## Auth, rate limits, and the MCP

- **The wantlist account's username is `elezea-records`**, not `rianvdm`.
- **`DISCOGS_TOKEN` lives in `~/.config/ebay/credentials.env` and `~/git/product-ai/.env`.** Source the ebay file (`set -a; . ~/.config/ebay/credentials.env; set +a`) for wantlist writes; the product-ai token has returned 403 on add/remove.
- **The token raises the budget from 25 to 60 requests a minute per IP.** Pace at about one call a second.
- **Stop at the first 429.** A 429 or 504 from the MCP means Discogs is throttling a shared egress IP, and retries extend the penalty (see [[corrections]] → Discogs API Rate Limits). One retry after the window resets is the limit; three manual retries tripped the MCP circuit breaker on 2026-08-04.
- **The MCP's circuit breaker** (`"Discogs rate-limit circuit tripped", retryAfterSecs: <n>`) takes down search, release, and wantlist tools together for about ten minutes. Everything in this file works over curl with the token, so carry on there.

## Wantlist reads and writes

```bash
set -a; . ~/.config/ebay/credentials.env; set +a
UA="DiscogsPressingHelper/1.0"
curl -s -o /dev/null -w "%{http_code}\n" -X PUT    -H "Authorization: Discogs token=$DISCOGS_TOKEN" -A "$UA" \
  "https://api.discogs.com/users/elezea-records/wants/<release_id>"   # 201 = added
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE -H "Authorization: Discogs token=$DISCOGS_TOKEN" -A "$UA" \
  "https://api.discogs.com/users/elezea-records/wants/<release_id>"   # 204 = removed; repeat it: 404 proves it's gone
curl -s -H "Authorization: Discogs token=$DISCOGS_TOKEN" -A "$UA" \
  "https://api.discogs.com/users/elezea-records/wants?per_page=100"   # read
```

`GET /wants` lags after a write, so a fresh add can be missing from the listing. Trust the 201, and prove a removal with a second DELETE returning 404.

When the user buys a wantlisted pressing, remove it from the wantlist and record the order in their purchases-in-flight log.
