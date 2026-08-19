# Music skills

Five skills for buying CDs and running a Spotify library. They're a hobby, and I've published them because they're the most heavily-iterated skills I have. A CD purchase either arrives as the right pressing or it doesn't, and a Spotify write either wrecked the playlist or it didn't. That feedback is fast and unambiguous, so these files have been corrected far more often than anything in my work folders.

Most of what's in them is field notes: where an API returned something true but misleading, and what believing it cost. If you're writing skills of your own, that's the part worth stealing.

## The CD ones

These three form a loop.

* **[`auditing-cd-collection`](auditing-cd-collection/SKILL.md)** runs across the whole collection and classifies every disc as remaster, original, or unverified. Roughly 1,800 API calls, fully cached, output to a Google Sheet. The interesting section is the four traps: encodings that look like remasters and aren't, pre-1983 albums that have to be dated from the CD era, and a regex that matched a credit line printed on original 80s pressings.
* **[`finding-original-cds`](finding-original-cds/SKILL.md)** takes one album and picks which pressing to want.
* **[`finding-cd-bundles`](finding-cd-bundles/SKILL.md)** prices the resulting wantlist against live eBay listings and the Discogs marketplace, and finds sellers holding enough of it to be worth one order. The core trick is that a remaster has its own barcode, so searching eBay by the barcode of the exact wanted pressing filters remasters for free.

The audit finds a remaster on the shelf, `finding-original-cds` decides what should replace it, that goes on the wantlist, and `finding-cd-bundles` works out where to buy it. Each one is useful alone, but the bundle finder inherits the wantlist's mistakes: it will faithfully find you remasters if a remaster got wantlisted by mistake.

## The Spotify ones

* **[`managing-spotify-playlists`](managing-spotify-playlists/SKILL.md)** covers reading and writing playlists. Most of it is about the fact that Spotify has no undo: which calls are irreversible, what to snapshot before firing one, and the confirmation gate that has to happen first. It also documents two API fields that don't do what they look like. One of them nearly swapped 17 perfectly good tracks out of a playlist I care about.
* **[`playlist-cover`](playlist-cover/SKILL.md)** generates artwork from what the playlist contains: genre tags, era, and how obscure the artists are all shape the design. The section that gets used most is the verification gate, because image models misspell the title constantly and nothing in the API response hints at it.

## What's not here

**Only the `SKILL.md` files are published.** Every skill in this folder is backed by Node or Python that talks to Discogs, eBay, Spotify and the OpenAI image API, and those are wired into my machine's credentials and paths. The skill docs describe what the scripts do and where they go wrong. That's the part you can reuse.

A few references also point at files outside this repo, `[[wikilink]]` style notes that live in my private vault. I left them in. Seeing what a skill leans on is part of understanding how it's put together.

## Setting this up yourself

The skills describe the scripts but don't ship them, so standing this up means rebuilding them. That's a reasonable job to hand to a coding agent, but point it at **this whole folder**, not just this file. The `SKILL.md` documents cover the behaviour (what the output should say, which heuristics are wrong, where each API lies); this section covers the interfaces, endpoints and auth shapes. Neither half is enough alone.

Everything is Node 22+ or Python 3 with no third-party packages: stdlib and `fetch` only. Expect to iterate. The specification below is complete enough to get working scripts. Yours will end up different from mine.

### Credentials

The scripts read a `.env` at the repo root directly, so a shell export won't do.

| Key | Needed by | Where it comes from |
|---|---|---|
| `DISCOGS_TOKEN` | all three CD skills | Discogs -> Settings -> Developers -> personal access token. Does wantlist **writes** as well as reads |
| `DISCOGS_USER` | all three CD skills | Your Discogs username. Note this can differ from your login name, and the wrong one returns nulls with no error |
| `EBAY_APP_ID`, `EBAY_CERT_ID` | `finding-cd-bundles` | eBay developer program, production keyset, Browse API scope. A new keyset stays inactive, and auth returns `invalid_client`, until you set Notifications -> Marketplace Account Deletion -> "Not persisting eBay data" |
| `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` | both Spotify skills | Spotify developer dashboard. On their own these are the client-credentials flow: **zero scopes, public catalog reads only** |
| `SPOTIFY_REFRESH_TOKEN` | playlist writes, cover upload | Minted by the auth script below. Scopes: `playlist-read-private`, `playlist-read-collaborative`, `playlist-modify-private`, `playlist-modify-public`, `ugc-image-upload` |
| `OPENAI_API_KEY` | `playlist-cover` | Image generation |

The collection audit also needs a Google Sheets and Drive client. I use a CLI wrapper; anything that can create a spreadsheet, write value ranges, and apply formatting requests will do.

### Build only the group you want

The two groups share nothing. The Spotify pair runs on Spotify and OpenAI credentials alone; the CD three run on Discogs and eBay. Within the CD group, `finding-original-cds` ships no scripts at all. It's a judgement rubric that runs on the public Discogs API and an agent's own reasoning, so it's the cheapest place to start, and it tells you whether the API is behaving before you build anything.

### Layout

Only one thing here will break if you move it. `set-cover.mjs` and `audio-features.mjs` both import from a single shared `spotify.mjs`, so it lives outside the skill folders and the relative paths have to resolve.

```
.
├── .env
├── scripts/
│   ├── spotify.mjs
│   ├── spotify-auth.mjs
│   └── audio-features.mjs        imports { apiAll } from './spotify.mjs'
└── skills/
    ├── finding-original-cds/     SKILL.md only, no scripts
    ├── finding-cd-bundles/       + find-bundles.mjs, seller-scan.mjs, seller-discover.mjs
    ├── auditing-cd-collection/   + the six .py steps
    ├── managing-spotify-playlists/  SKILL.md only, drives scripts/spotify.mjs
    └── playlist-cover/           + fetch-playlist.mjs, generate-cover.mjs, set-cover.mjs
                                    set-cover.mjs imports { token } from scripts/spotify.mjs
```

Each skill folder is a drop-in `SKILL.md` with YAML frontmatter. Put them wherever your harness looks for skills.

### Wire details agents get wrong

These are the ones an agent will invent plausibly and wrongly, producing scripts that 401 or 403 with nothing useful in the message.

**Discogs.** Base is `https://api.discogs.com`. The auth header is `Authorization: Discogs token=<DISCOGS_TOKEN>`, *not* `Bearer`. It also requires a descriptive `User-Agent` of your own (`YourTool/1.0 +https://example.com`); a default or generic one gets rejected. Authenticated rate ceiling is 60 requests/minute, and in practice it throttles harder than that under load.

**Spotify.** API base is `https://api.spotify.com/v1`. Refresh with `POST https://accounts.spotify.com/api/token`, `grant_type=refresh_token`, and `Authorization: Basic <base64(client_id:client_secret)>`. The same Basic header with `grant_type=client_credentials` gets you the zero-scope app token that `fetch-playlist.mjs` uses.

**eBay.** Token from `POST https://api.ebay.com/identity/v1/oauth2/token`, `Authorization: Basic <base64(EBAY_APP_ID:EBAY_CERT_ID)>`, `grant_type=client_credentials`, `scope=https://api.ebay.com/oauth/api_scope`. Search is `GET https://api.ebay.com/buy/browse/v1/item_summary/search?gtin=<upc>`, and `gtin` accepts UPC/EAN only. A catalog number silently returns nothing useful.

**ReccoBeats.** Base is `https://api.reccobeats.com/v1`, no auth, takes Spotify track IDs directly.

### Check it works before building on it

Four one-call smoke tests, in the order that saves the most time:

1. `GET https://api.discogs.com/users/<you>/wants` with the token header returns your wantlist. Confirms both the auth shape and the User-Agent.
2. `GET /me/playlists?limit=1` through `spotify.mjs` returns a private playlist. Confirms the refresh token has the scopes, which the client-credentials token doesn't.
3. An eBay `item_summary/search?gtin=` on a barcode you can read off a disc in your hand returns listings. Confirms the keyset is activated.
4. `set-cover.mjs` against a throwaway playlist, then read the playlist back and check `images[0].url` changed. The upload returns `202 Accepted` whether or not it worked, so this is the only test that means anything.

### Spotify scripts

* **`spotify.mjs`** is the client everything else goes through. CLI `node spotify.mjs <METHOD> <path> [jsonBody] [--all]`, plus importable `{ api, apiAll, token }`. It refreshes an access token from `SPOTIFY_REFRESH_TOKEN`, backs off on 429, and `--all` / `apiAll` follow `next` and merge the `items` arrays. Two interface details the skills rely on: the base URL already ends in `/v1`, so paths start `/playlists/...`; and `apiAll(path)` is GET-only, taking no method argument.
* **`spotify-auth.mjs`** is the one-time authorization-code flow. Opens a browser, catches the redirect on a loopback server, exchanges the code, writes the refresh token back into `.env`. Register `http://127.0.0.1:8888/callback` as the Redirect URI. Spotify rejects `localhost` for loopback and string-matches exactly, so a trailing slash or `https` fails.
* **`audio-features.mjs <playlist url|id> [--json]`**, importable as `audioFeatures(trackIds)`. Energy, valence, danceability, tempo and key come from **ReccoBeats**, which is free, unauthenticated, and takes Spotify track IDs directly. Spotify's own `/audio-features`, `/audio-analysis` and `/recommendations` were closed in November 2024 to apps that didn't already have access and now return 403/403/404. Print a coverage count: ReccoBeats thins out on small-label and recent releases, which is exactly where you'd want it.

### playlist-cover scripts

* **`fetch-playlist.mjs <url|uri|id> [--json] [--max-tracks N]`** builds the design brief. Name, description, era, top artists, sample tracks, current cover URL, and the genre tags Spotify hangs off each artist. Those tags do most of the work. Client-credentials auth, so public playlists only; private, deleted and mistyped all return an identical 404. Sample tracks are spread evenly across the whole playlist.
* **`generate-cover.mjs --spec <spec.json>`**, with `--only <label>`, `--model`, `--quality`, `--out <dir>`, `--name <slug>`, and `--edit <existing.png>` to route the request through the edits endpoint. Spec shape: `{slug, title, outDir, model, quality, size, edit, variants: [{label, prompt}]}`, where `title: null` means a wordless cover. The script appends the hard constraints (no logos, watermarks, fake player UI, duplicated titles) so prompts don't repeat them.
* **`set-cover.mjs <playlistUrlOrId> <cover.png>`**. `PUT /playlists/{id}/images` wants a **raw base64 JPEG body, not JSON**, so this bypasses the client's JSON path and reuses only its `token()` helper. The 256 KB ceiling applies to the base64 payload, so re-encode and step quality down until it fits; don't error out. Read the playlist back afterwards to confirm the image took, since a `202 Accepted` comes back either way.

### finding-cd-bundles scripts

* **`find-bundles.mjs`** with `--cheapest`, `--min N`, `--html`, `--zip NNNNN`, `--country XX|ANY`, `--json`, `--refresh`. The pipeline is wantlist -> each release's barcode from `identifiers[]` -> eBay Browse `item_summary/search?gtin=<upc>` -> group by `seller.username`. Every album also gets `GET /marketplace/stats/<id>?curr_abbr=USD` for the Discogs floor. Cache barcodes forever and prices for 12 hours; a Discogs failure should be swallowed and deliberately *not* cached, so the next run retries.
* **`seller-scan.mjs <seller> [seller2 ...]`** searches a named seller's stock via the **undocumented `q=` parameter** on `GET /users/{seller}/inventory`. Full enumeration isn't available: page > 100 returns 403 for anyone's inventory but your own, a 10,000-item ceiling that `sort` doesn't move. Inventory listings come back with `release.master_id: null` and `q=` matches loosely, so confirm every candidate against `/releases/<id>`.
* **`seller-discover.mjs [probes]`** finds big sellers without knowing their names. Marketplace listing IDs are sequential integers, and `/marketplace/listings/<id>` returns `seller.username`, `ships_from`, `condition` and the format. Sampling random IDs samples the marketplace weighted by listing count, so big sellers turn up on their own. Around a 3% hit rate; resolve each name against `/users/<name>` for its true size.

### auditing-cd-collection scripts

Six Python steps sharing a working directory set by `AUDIT_DIR`, run in order. The two slow ones append to a cache and skip what's already there, so a re-run picks up where it stopped.

```
fetch_collection.py  ->  cd_collection_raw.json, wantlist.json
fetch_details.py     ->  releases.jsonl, masters.jsonl        (slow, resumable)
classify.py          ->  classified.json                      (local only)
enrich.py            ->  enrich.jsonl                         (slow, resumable)
build_sheet.py       ->  a new Google Sheet + sheet.json
format_sheet.py      ->  reads sheet.json, applies formatting
```

The steps aren't independent: `classify.py` decides which masters `enrich.py` looks up, and `build_sheet.py` writes the file `format_sheet.py` needs. The collection lives in a numbered Discogs folder, so find yours via `/collection/folders`. Both fetchers should share one token bucket at 50-55 requests/min against Discogs' authenticated ceiling of 60; adding workers doesn't help, because the bucket is the constraint. Worth building a single-threaded fallback fetcher too, appending to the same `releases.jsonl`. The parallel one gives up under contention, and seventeen minutes that finishes beats eight that doesn't.

### What you'll have to change

Discogs username, the collection folder ID, your shipping ZIP, the seller registry, and the `KEEP_ARTISTS` exclusion set in `build_sheet.py`. Also the house style section of `playlist-cover`, a written description of three covers I happen to like. Replace it with your own reference images.
