---
name: managing-spotify-playlists
description: Use when the user wants to change or inspect one of their Spotify playlists — create one, rename it, add or remove tracks, reorder, change visibility, or attach cover art — or asks what a playlist currently contains. Triggers e.g. "add these to <playlist>", "make me a playlist of X", "clean up <playlist>", "dedupe this", "reorder these", "what's in my <playlist>", "set the cover on <playlist>". Playlist contents and metadata; for designing the cover image itself use playlist-cover.
---

# Managing Spotify playlists

## Overview

Rian's Spotify account (`rianvdm`) is writable from this repo. Every call goes through `scripts/spotify.mjs`, which refreshes a user token, backs off on 429, and follows pagination.

```bash
node scripts/spotify.mjs GET "/me/playlists?limit=50" --all
node scripts/spotify.mjs POST /users/rianvdm/playlists '{"name":"X","public":false}'
```

Importable too: `import { api, apiAll } from './scripts/spotify.mjs'` — reach for this the moment a task needs more than two calls, because loops and dedupe belong in one script, not fifteen Bash invocations.

**The core principle: Spotify has no undo, so capture state before you write.** Dump the current track list to the scratchpad before any destructive operation. That single step converts an irreversible mistake into a restorable one, and it costs one API call.

```bash
node scripts/spotify.mjs GET "/playlists/<id>/tracks?limit=100" --all > <scratchpad>/before-<slug>.json
```

## Two credentials live in .env — only one can write

`SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` alone are the client-credentials flow: app-level, **zero scopes**, public catalog reads only. It cannot see private playlists and cannot write anything. `.opencode/skills/playlist-cover/fetch-playlist.mjs` uses that flow, which is why it only reads.

Writes need `SPOTIFY_REFRESH_TOKEN`, also in `.env`, carrying `playlist-read-private`, `playlist-read-collaborative`, `playlist-modify-private`, `playlist-modify-public`, `ugc-image-upload`.

If a call fails with `invalid_grant` the token was revoked — re-run `node scripts/spotify-auth.mjs`. That needs `http://127.0.0.1:8888/callback` registered as a Redirect URI on the Spotify app's client ID. Spotify rejects `localhost` for loopback and matches the string exactly, so a trailing slash or `https` fails with `INVALID_CLIENT`.

## Reversibility — check this before every write

| Operation | Call | Recoverable? |
|---|---|---|
| Add tracks | `POST /playlists/{id}/tracks` | Yes — remove them again |
| Create playlist | `POST /users/{uid}/playlists` | Yes — unfollow it |
| Rename, re-describe, change visibility | `PUT /playlists/{id}` | Only if you captured the old values first |
| Reorder | `PUT /playlists/{id}/tracks` + `range_start` | Only from a saved copy of the original order |
| **Remove tracks** | `DELETE /playlists/{id}/tracks` | **No** |
| **Replace all** (`uris` on `PUT`) | `PUT /playlists/{id}/tracks` | **No — silently wipes the playlist** |
| **Upload cover** | `PUT /playlists/{id}/images` | **No — the previous image is gone** |
| "Delete" playlist | `DELETE /playlists/{id}/followers` | Unfollows rather than destroying; restorable from Rian's Spotify account page |

`uris` on `PUT /playlists/{id}/tracks` is the trap worth naming twice: it reads like an update and behaves like a truncate. Reordering and replacing are mutually exclusive in one request.

## Get confirmation before anything in bold above

Rian asked for this rule directly. Before firing a bold-row operation, show him:

1. The playlist name and its current track count.
2. The exact tracks affected — title and artist, not URIs — capped at 20 with a count of the remainder.
3. The resulting track count.
4. Where the before-state snapshot is saved.

Then stop and wait for a yes. A plan he approved earlier in the conversation is not a yes to the specific write; the diff he approves must be the diff you send.

Adding tracks, creating playlists, and renaming don't need this gate — do them and report what happened.

| Rationalization | Reality |
|---|---|
| "He asked me to clean it up, so removal is implied" | He authorized the goal, not a specific track list. Show the list. |
| "It's only a few tracks" | The count isn't what makes it irreversible. |
| "He can see the playlist and will notice" | Noticing afterwards is not the same as choosing beforehand. |
| "I already listed them earlier in the conversation" | Listed ≠ approved. Ask for the yes. |
| "Replacing is cleaner than diffing" | Replace wipes anything added since you last read the playlist. Diff. |
| "He said go ahead" (about a different playlist) | Approval doesn't travel between playlists or between runs. |
| "Re-reading to snapshot wastes a call" | One call against an unrecoverable loss. |

**Red flags — stop:** you're composing a `DELETE` or a `uris`-bearing `PUT` and there is no `before-*.json` in the scratchpad; you're about to say "done" for a removal Rian never saw itemised; you're uploading a cover without having checked whether one already exists.

**When a metadata field says a large batch of tracks is broken, verify one by playing it before proposing a fix.** A field that reports 17 beloved songs as unplayable is more likely to be the wrong field than to be 17 broken songs — and the "fix" it justifies is a destructive edit. Rian caught this one himself with "I tested and they work for me." Ask what the field actually means, and find the call that answers the question directly, before writing a proposal built on it.

## Resolving track names

When Rian gives song titles rather than URIs, search resolves each one and **the resolved list goes to him before the add**, formatted as `query → matched title / artist / album / year`. Spotify's top hit is routinely a karaoke cover, a live version, a remaster, or a sped-up edit, and none of that is visible in a URI.

Flag any row where the matched artist differs from the requested one, the title carries `Live`/`Remaster`/`Karaoke`/`Sped Up`, or search returned nothing. Those are the rows he needs to look at; the clean ones he can skim.

**The same rule applies to tracks *you* propose, and there it matters more.** A recommendation list written from memory is a list of existence claims, and the resolver is cheap — search each one, print `artist / title / album / year / popularity / duration`, and read the result before it reaches him. Resolving 20 shoegaze picks on 2026-08-17 caught four separate failures that all look identical in a chat message: three titles that returned nothing at all, and a Fleshwater pick whose duration gave it away as a **77-second interlude**. Also print the artist search separately when the band's name is a common word — searching `julie` returns Julien Baker, not the band, so a name-equality match on the artist endpoint can fail while a `artist:… track:…` track query succeeds.

**`release_date` is not the original release year on catalogue-heavy genres.** Resolving 90s dance picks returned *Café Del Mar* dated 2005 and *Castles in the Sky* dated 2015 — both the original recordings, sitting on later compilations, because that is the only copy Spotify carries. So a date outside the playlist's own bracket is not evidence of a re-recording, and a date inside it is not evidence you got the right mix. Say which it is rather than letting the year imply it, and where a track has a famous later remix (*For An Angel* '98, Delerium's *Silence* via Tiësto), search for that mix by name — the bare `artist:… track:…` query returns the album original, which can be a completely different record.

**Report a missing catalogue as missing rather than substituting.** Hotline TNT resolved only to Audiotree live sessions, no studio album — the honest output is to drop the pick and say why, not to quietly hand over a live version.

## API notes that bite

| Thing | Detail |
|---|---|
| Batch ceiling | 100 URIs per add or remove request. Chunk longer lists. |
| Pagination | Playlist tracks page at 100. Use `--all` or `apiAll` — a playlist of 257 needs three calls. |
| Null tracks | `items[].track` can be `null` for unavailable or local files. Filter before mapping `.uri`. |
| Duplicates | Spotify permits the same track twice. Dedupe on `track.id`, not name. |
| **`positions` on DELETE is ignored** | **A remove deletes EVERY occurrence of the URI, not the one you targeted.** The `positions` array is from an older API version; the current endpoint accepts it without complaint, returns 200, and removes them all. Removing one copy of a track that appears twice took *Faith* 131 → 129 on 2026-08-18. To de-duplicate, delete the URI and then re-add one copy with an explicit `position` — and verify the count, because nothing in the response tells you how many it took. |
| **Empty `available_markets` does NOT mean unplayable** | It usually means **track relinking**: the ID in the playlist is a market-specific stub Spotify resolves to a playable equivalent at play time, so it is licensed nowhere *directly* and reads as dead. 17 tracks on *I'll Do My Crying In The Rain* looked unplayable everywhere and all 17 play fine. **Ask with `market=US` and read `is_playable`** — that is the field that answers the question — and treat a `linked_from` on the result as proof relinking is doing its job. Reading the wrong field here nearly swapped 17 working tracks out of Rian's most-prized playlist. |
| `snapshot_id` | Pass it on removes to make the write conditional on the version you read. |
| Cover upload | `PUT /playlists/{id}/images`, raw base64 JPEG as the body, `Content-Type: image/jpeg`, **256 KB max payload** — that's the base64 size, so the JPEG must be meaningfully smaller. Not JSON, so `spotify.mjs`'s JSON path doesn't apply. |
| Position | `position` on add is zero-based; omit it to append. |
| Owner | Only playlists owned by `rianvdm` are writable. Check `owner.id` before promising an edit on a followed playlist. |
| Signatures | `api(method, path, body)` takes the method; **`apiAll(path)` does not** — it is GET-only. `apiAll('GET', p)` silently fetches the path `"GET"`. |
| `BASE` already ends in `/v1` | So paths start `/search`, `/playlists/…`, `/artists/…`. Writing `/v1/search` doubles it. |
| A malformed path returns **410**, not 404 | Both mistakes above surface as `410 GET GET` or `410 GET /v1/search…` with an empty message, which reads like a deprecated or withdrawn endpoint rather than a path you built wrong. Check the path shape before believing the API changed. |

### Reordering

`uris` on `PUT` truncates, so a reorder is a sequence of single-item moves. Selection-sort against the target list, updating a local copy of the order after each call so the next index is right:

```js
for (let i = 0; i < TARGET.length; i++) {
  const j = cur.indexOf(TARGET[i], i);
  if (j === i) continue;
  await api('PUT', `/playlists/${ID}/tracks`, { range_start: j, insert_before: i, range_length: 1 });
  cur.splice(i, 0, cur.splice(j, 1)[0]);
}
```

Read the playlist back afterwards and assert the result equals the target, rather than trusting that N calls returned 200. An 18-track reorder took 13 moves; a 130-track one took 123.

**At album length, sequence by hand; past that, sequence to constraints and say so.** *Faith* is 130 tracks and nearly 13 hours, and a hand-built running order across that is theatre — nobody hears position 70 as following 69. What is actually broken at that length is measurable: 14 places where the same artist played twice in a row, and energy jumps like 0.28 → 0.86. So hand-pick an opening run of about a dozen (the part that actually gets heard) and a closing run of about eight, then generate the middle to hard constraints — no same-artist adjacency, bounded energy step — and report the numbers rather than describing a mood. **Round-robin the middle over an energy-sorted list into ~7 waves and arc each one**; a greedy nearest-energy walk instead collapses into one monotonic ramp, which is a sort, not a running order.

**Group artists into families for the adjacency rule.** Spotify's credits split acts that a listener hears as one: Crowder and David Crowder Band are the same man, Hillsong Worship and Hillsong UNITED are the same house. Fold them before checking adjacency or the constraint passes while the playlist still sounds repetitive.

Express the target as track URIs and resolve names to URIs once, up front. Building the target as `artist — title` strings and matching those against the playlist breaks on typography — Deserta's *I'm So Tired* is a straight apostrophe in the API and a curly one everywhere a human types it, which failed a whole run. Whatever the target is keyed on, assert the mapping is complete **before** the first move, so a mismatch aborts instead of half-reordering the playlist.

**Re-read the live playlist inside the write script, and abort if it no longer matches the plan you proposed.** Rian edits playlists in the Spotify client while a session is running, and it happens often enough to design for: on 2026-08-18 *Trance Classics* went 20 → 19 between the reorder and the next turn (he removed a duplicate I had flagged), and 24 → 25 midway through a sequencing analysis (he added a track). Both were caught only because the script compared the live order against the snapshot before its first `PUT`. Don't hardcode a track count from an earlier turn either — assert against what you just read, and make the mismatch a thrown error rather than a warning.

### Sequencing data

Energy, valence, danceability, tempo and key come from `scripts/audio-features.mjs`, which serves them from ReccoBeats. Spotify's own `/audio-features`, `/audio-analysis` and `/recommendations` are dead for this app — 403/403/404, closed to apps without pre-November-2024 access.

```bash
node scripts/audio-features.mjs "<playlist url or id>"   # table, plus a coverage line
```

**Coverage is partial and the gap lands exactly where it hurts.** ReccoBeats thins out on small-label and recent releases — 16 of 19 on Shimmery Guitars, and the three misses were its three most obscure tracks. Read the coverage line before leaning on the numbers, and sequence the uncovered tracks on artist separation, duration and era, the way you would with no data at all.

Then say which basis you used, per track group rather than for the playlist as a whole: *"sequenced on energy and key where ReccoBeats had data, on artist spacing and length for the three it didn't."* Describing a whole running order as tuned to energy when a fifth of it was judgement is inventing a measurement.

## Cover art

Designing the image *and* attaching it is `playlist-cover`, which ships the upload:

```bash
node .opencode/skills/playlist-cover/set-cover.mjs "<playlist url or id>" <cover>.png
```

It handles the JPEG re-encode under the 256 KB base64 ceiling and reads the playlist back to confirm the image took, because `202 Accepted` is returned whether or not it did. The rule that matters here is the one this skill enforces: the upload overwrites, Spotify keeps no history, so check the current `images[0].url` first. A `mosaic.scdn.co` URL is the auto-generated grid and costs nothing to replace; anything else is a cover Rian chose, and that needs a yes before you overwrite it.
