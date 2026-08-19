---
name: playlist-cover
description: Use when the user wants cover art for a Spotify playlist — they give a playlist link, usually with the name they want on it, and want an image made and put on the playlist. Triggers e.g. "make a cover for this playlist", "playlist cover for <link>", "I need artwork for this playlist", "redo this playlist's cover", "generate a Spotify cover", "cover art for <playlist name>". Designs the art and attaches it, not playlist curation — for what to put *in* a playlist this is the wrong skill.
---

# Playlist covers

## Overview

Read what a playlist actually contains, design three covers from it, look at them, and hand over the one that survives.

**The core insight:** the playlist name is the weakest signal available. Spotify hangs genre tags off every artist, so a playlist resolves to `shoegaze ×198, slowcore ×111, dream pop ×89, 1990–2025 median 2021, mean popularity 24` — an era, a scene, and a sense of how underground it is. A playlist called "Guitars" tells you none of that. Fetch the brief before designing anything.

**The second insight:** image models misspell titles, and nothing in the API flags it — the request succeeds, the file writes, the path prints. The only way to catch it is to open the image. See *The verification gate*.

## The house style

On 2026-08-17 Rian named three of his own covers as the target: *Guitars* (a burning Stratocaster on flat red), *Calm* (a hazy amber sunrise over a lake, title in spaced caps inside a thin square rule) and *Dark Ambient* (a near-black storm sky over a barren plain, title tiny and low-contrast). They look nothing alike and they are built the same way. Four rules, all four in every variant:

| Rule | What it means | The failure it replaces |
|---|---|---|
| **One idea, fully committed** | A single subject doing a single thing. Nothing added to fill space. | Collages and "and also a…" compositions, which read as clip art no matter how well rendered |
| **Photographic realism** | Rendered or shot, with real light and real material. | Flat vector and painterly illustration, which read as cheap |
| **Near-monochrome** | One hue family across a *full* range from near-white to near-black. *Guitars* is red/orange/black; *Calm* runs cream sky to amber water to shadowed ridges; *Dark Ambient* is grey-blue from pale cloud to black land. | The four-colour palettes this skill kept specifying, which dilute the image |
| **Title as a designed lockup** | The type is a graphic element with its own treatment — a face borrowed from the genre's visual culture, a considered size, sometimes a rule or frame around it. Small: roughly a third of the frame width, never a headline. | "Put the title in the empty area", which produces a caption rather than a cover |

The fourth is the one that gets skipped, because placement feels like design and isn't. Decide the lockup — face, size, colour, and any framing device — as deliberately as the subject.

**Cheesy is allowed; AI-looking is not.** Rian's steer on the 90s rave playlist was "still kind of cheesy like the time and music require, but less AI-like — more photorealistic." Genres with a loud visual culture (rave, synthwave, hair metal) *should* get their clichés; what makes a cover read as generated is never the cliché, it's the rendering — everything-at-once compositions, four or five hues, and CGI surfaces instead of photographed ones. The cover being replaced had four mirrorballs, lasers, a crowd and a DJ booth in one frame. Commit to the cheesy idea and shoot it, don't render it.

**Match the mood of the music, and break any of the four rules that fight it.** Each reference matches its own register: *Guitars* is aggressive, *Calm* serene, *Dark Ambient* bleak. Following the rules while missing the mood produces something correct and wrong — the first *South African Jams* retry was a flag in muted folds, tasteful and faintly funereal, for a playlist of Jeremy Loops and amapiano. Rian's words: "this needs to be a happy thing." Read the genres for feeling before reaching for a subject, and say the feeling in the prompt.

The rule this breaks most often is the palette, because **near-monochrome does not mean muted** — *Guitars* is a brilliant saturated red. A joyful playlist wants a flat marigold or turquoise ground under hard bright sunlight: still one hue, still no environment, just loud instead of quiet.

**Scale the title to how loud the music is.** The three references land on a clean gradient, and mean popularity tracks it closely enough to use as the dial:

| Playlist | Genre, popularity | Title treatment |
|---|---|---|
| *Guitars* | hard rock, 43 | Heavy condensed display, angular terminals, top corner, about a third of frame width |
| *Calm* | ambient/neoclassical, 27 | Light letter-spaced capitals centred inside a thin hairline square rule, about a quarter of frame width |
| *Dark Ambient* | drone/dark ambient, 15 | Very small light-weight sans, low-contrast grey against dark, set off-centre and low, about a fifth of frame width |

Under ~20 popularity the type should feel almost too quiet to notice — that restraint is the genre signal.

**Small type needs a full-quality render — the draft tier physically cannot do it.** `gpt-image-1-mini` at `low` has a floor on glyph size and ignores every instruction that tries to go below it: "one fifth", "one tenth", "a small discreet caption" and "vast empty space around the text" all came back at about a third. The same prompt on `chatgpt-image-latest` at `high` landed at one fifth, correctly spelled, first try. Four things follow:

* **Drafts overstate title size, so never redesign a layout over it** — and never judge a quiet-genre treatment at draft tier at all. The model also stacks lines by itself to cope with the floor, so a two-line draft title does not predict a two-line final.
* **This is also why small type breaks.** Nearly every spelling failure lands on small text at draft tier, where the mini is straining against its own floor. At full quality the same tiny titles render cleanly.
* **Draft the short lockup and add the extra line at full quality.** Two elements is what the draft tier can hold. *The Midnight Essentials* broke four rounds running, even with the letters spelled out individually; shortening to *The Midnight* cleared it on the next render, and the full three-element lockup then came back perfect at full quality.
* **Numerals fail worse than letters, and the palette can contaminate them.** A *1990-2005* subtitle returned *1820 2009*, *1990-200S* and *1960-2005* in one batch — and the *1960* came from the one variant graded warm sepia, where the model read the grade as an era and dated the cover to match. Cut digits first when a lockup is fighting you; if they must stay, make the palette era-correct.

**A framing device does most of the work on a quiet cover.** Rendering *Calm* with a square rule, with a taller rectangle, and with none, Rian rated both framed versions good and the unframed one was a stock sunset with a word on it — same photograph, same type. When a quiet cover feels generic, add the rule rather than a second subject. Hairline rules and letter-spaced caps render reliably even at draft tier, and having a rule matters more than its proportions.

**When Rian names a cover he likes, go and look at it before designing.** `fetch-playlist.mjs` prints the playlist's `current cover` URL — `curl` it and Read the image. Describe what is actually there: subject, ground, palette count, type treatment, how much of the frame the title occupies. Designing from a remembered impression of a cover you were shown is how the recipe gets lost.

**The concept in an existing cover is probably his, so treat it as a brief rather than calling it tired** — keep the subject and fix the craft, or ask which he wants. "Better and more stylish" is a different request from "something else". Told to keep *Faith*'s cross I kept the cross and rendered three muted material directions that all threw away what he actually valued, which was a luminous cross floating in darkness — **the concept is usually the treatment, not the subject.** Repeat the *look* back before rendering: a cover you can describe only by what is in frame is one you have half understood.

## The run

1. **Get the brief.**

   ```bash
   node ~/git/product-ai/.opencode/skills/playlist-cover/fetch-playlist.mjs "<url>"
   ```

   Add `--json` for the structured version, `--max-tracks N` to widen the sample (default 200, spread evenly across long playlists rather than taken off the top).

2. **Decide the title.** Whatever Rian says the playlist is called wins, including its capitalisation. Only fall back to the Spotify name if he didn't give one. If he wants no text at all, set `"title": null` in the spec.

3. **Pick three directions** — one each from three *different* rows of the archetype table below. Three treatments of one idea is not a choice, it's a rendering artifact.

4. **Write the spec** to the scratchpad and render drafts:

   ```bash
   node ~/git/product-ai/.opencode/skills/playlist-cover/generate-cover.mjs --spec <scratchpad>/spec.json
   ```

   Defaults are `gpt-image-1-mini` at `low` — the draft tier. The hard constraints (no logos, watermarks, fake UI, duplicated titles) are appended by the script, so leave them out of the prompt.

5. **Open every draft with the Read tool.** See the verification gate below. Re-render anything that fails before Rian sees it.

6. **Open the survivors in Preview, then present them** — `open -a Preview <file> …` with every draft in one command, in the same order you describe them. Rian compares them at full size in Preview, not in the transcript, and expects them to be on screen when he reads your summary. Then one line each on what the direction is doing. Not a paragraph.

7. **Promote his pick to full quality — render it both ways and let him choose.** The edit preserves the composition he picked; the re-render rebuilds the subject and is usually the better *picture*. Neither wins reliably, and both together cost about 12k tokens, so stop guessing:

   ```bash
   # a) edit — keeps the exact composition he approved
   node ~/git/product-ai/.opencode/skills/playlist-cover/generate-cover.mjs --spec <scratchpad>/final.json \
     --edit <scratchpad>/drafts/<slug>-<label>.png --model chatgpt-image-latest --quality high \
     --only final --name <slug>-edit --out <scratchpad>/finals

   # b) re-render — same prompt, full quality, fresh composition
   node ~/git/product-ai/.opencode/skills/playlist-cover/generate-cover.mjs --spec <scratchpad>/spec.json \
     --only <label> --model chatgpt-image-latest --quality high \
     --name <slug>-rerender --out <scratchpad>/finals
   ```

   The edit prompt asks to reproduce the draft at higher fidelity — crisper edges, finer texture, cleaner letterforms — and says explicitly that nothing may move, resize or shift hue.

   **Why both.** The edit keeps the composition and recovers detail the draft never had, but it cannot re-expose a scene — it came back flat and waxy where the re-render had hard sunlight and real cast shadows. The re-render rebuilds the subject properly, and its cost is drift: on *Faith* it lost the approved composition, and the *Guitars* re-render was a different guitar in a different pose.

   **Route by what is changing: adding something inside the existing exposure goes to the edit, changing the exposure itself goes to the re-render.** The edit can add a medium into darkness that is already there and can lift a black point locally; asked instead for more haze on *Shimmery Guitars* it left the figure a hard silhouette sitting on top of the fog, where the re-render lifted the whole key and dissolved the figure into it. But an atmospheric win that shifts the mood is a loss — *Faith*'s re-render delivered every requested change and lifted the *whole frame*, turning a dark cover into a warm radiant one, so the edit took it.

   **Check saturation first on both, because that is the axis neither respects.** "Nothing else may move, resize or shift hue" holds for geometry and composition and not for grade: the *Trance Classics* edit was asked only to reset a typeface and sharpen metal and pulled the icy cyan out to near-neutral steel, while *The Midnight* re-render drifted warm the other way. A lost grade is recoverable with a second edit that touches nothing else. Running tally: the edit has won four of six promotions.

8. **Verify the final too**, including the 300px check. Then give him the path.

9. **Attach it to the playlist.**

   ```bash
   node ~/git/product-ai/.opencode/skills/playlist-cover/set-cover.mjs "<playlist url or id>" <cover>.png
   ```

   It re-encodes to JPEG under Spotify's 256 KB base64 ceiling, uploads, then reads the playlist back and prints whether a custom cover is actually live. A `202 Accepted` alone does not mean the image took, which is why the script checks rather than trusting the status code.

   The upload is destructive — see Limits. Read the playlist's current image first and ask before overwriting anything that isn't a `mosaic.scdn.co` URL.

Drafts and both finals stay in the scratchpad; only the cover he picks lands in `05-personal/music/playlist-covers/`.

## Changing one thing about a cover he already likes

Re-rendering rolls fresh artwork and throws away the composition he approved. `--edit` doesn't: it sends the existing image to the edits endpoint, and anything the prompt doesn't mention survives.

```bash
node ~/git/product-ai/.opencode/skills/playlist-cover/generate-cover.mjs --spec <scratchpad>/tweak.json \
  --edit <path-to-existing-cover>.png
```

Write the prompt as *only the change*, and close it by naming what must not move — "leave the guitar shape, the glare, the composition and the colours exactly as they are." Without that sentence the model drifts.

Two rules:

- **Copy the cover to the scratchpad and edit from the copy** when the output path is the cover itself. Editing a file onto itself works, but a bad result then has nothing to fall back to.
- **Draft tier is nearly free here** (~270 tokens an edit, versus several thousand for a full high-quality render), so try four typefaces rather than guessing one. It softens fine detail though, so apply the winner to the original at `chatgpt-image-latest --quality high`.

## The verification gate

**Never show Rian a cover you have not opened.** Read every generated file before it appears in a response, drafts and finals alike.

Check four things:

| Check | How |
|---|---|
| Title spelled exactly right | Read the letters one at a time. `mosz`/`most` survives a glance. |
| Title legible small | `sips -Z 300 <file> --out <file>-300.png`, then Read *that*. Full size lies. |
| No stray marks | Signatures, watermarks, fake player UI, a second copy of the title in a corner, and **small blocks of garbled pseudo-lettering** — usually just under the real title. |
| Matches the brief | Right era, right mood, and 1:1 with nothing letterboxed. |

A draft that fails any of these gets re-rendered, not explained away. Text failures usually clear on a straight retry; if the same word breaks twice, shorten what you asked for or move the title somewhere with less texture under it, and name the specific letter that broke — *"the second word is AFRICAN, beginning with the letter F, not a P"* fixed it first try.

**This bites several times a session**, always in the lettering and never in the artwork, and most of them are invisible at page scale — *AfrIcan* with a capital I, *Dork Amblent*, *APRICAN*, a circumflex hook on the t of *Ambient*, a line of garbled pseudo-lettering under *Jams*. Nothing about the API call hints at any of it. Magnify the title every time.

**Magnify anything suspicious rather than squinting at it.** A 30px smear of fake text is invisible at page scale and obvious at 3×. Crop and upscale before deciding it's nothing:

```bash
sips -c <h> <w> --cropOffset <top> <left> <file> --out c.png && sips -z <3h> <3w> c.png --out zoom.png
```

(`sips` is the tool available here — there is no ImageMagick and no PIL on this Mac.)

**Red flags — you are about to ship something broken:**

- "The prompt specified the title, so the title is right"
- "It rendered with no API error, so it worked"
- "Two of them were fine, the third probably is"
- "Rian can see the image himself and will spot it"
- "It's only a draft"
- Writing a response that references an image file you have not Read

## Reading the brief

Match on the genre tags and the era, not the playlist name. The archetype decides *what is in frame*; the house style above still decides how it is rendered, coloured and lettered.

| Archetype | Reach for it when | Looks like |
|---|---|---|
| **Symbolic object on a flat field** | Tags name a loud, physical scene — punk, metal, garage, hard rock. Concrete one-word names. | One object doing something dramatic — burning, shattering, submerged — on a saturated single-colour ground with no environment at all, corner-set display lettering. This is the *Guitars* recipe and it is the strongest of the five |
| **Atmospheric photograph** | Ambient, slowcore, dream pop, folk, quiet electronica. Low mean popularity. | Landscape or weather carrying the mood, one hue family, framed caps or a small clean sans, lots of air. This is the *Calm* recipe |
| **Illustrated scene with a figure** | Singer-songwriter, indie, emo, country, soul — anything about people. Names that are phrases or lyrics. | One figure in a mood-lit scene, photographic rather than painterly, two anchor colours, warmer type clear of the focal point |
| **Neon / retro graphic** | Synthwave, italo disco, city pop, new wave. Era clustered 1979–1991, or deliberately retro-modern. | Chrome, grids, dusk cityscape, one dominant hue against near-black, retro script or heavy geometric type |
| **Abstract texture** | Tags scatter across many genres, or lean experimental, techno, drone, jazz fusion. | Gradient, grain, fluid form, no literal subject, one hue plus white, widely tracked geometric sans |

**A subject in an environment reads as stock photography.** The object-on-a-flat-field row wins ties for a reason: a guitar against flat red is a cover, a guitar on a beach at sunset is a photograph with words on it. When an archetype calls for a real setting, keep the setting near-empty and let one thing carry it.

Era shifts the treatment inside the archetype: a 1985-median playlist wants grain, halation and slight print misregistration; a 2023-median one wants cleaner edges and a flatter palette. Popularity sets the type — see the title-scale table above.

## Writing a variant prompt

Six parts, in this order. Each is a phrase or two, not a paragraph.

1. **Medium and treatment** — photographic or rendered with real light and material, per the house style. Reach for painterly or flat-vector only when Rian asks for it by name.
2. **Subject** — what is in frame and what it is doing.
3. **Composition** — where the focal element sits *and where the empty space is*. The title needs somewhere quiet to live, so decide that here rather than hoping.
4. **Light and texture** — direction of light, grain, bloom, brush, halation.
5. **Palette** — one hue family plus black or white, named. Two or three colours, not four. Named colours beat mood words, and a tight palette is what separates *Guitars* from a stock photo.
6. **Title treatment** — typeface character, colour, scale, placement into the empty space from part 3.

What testing rather than taste has established:

- **Buy legibility with weight, not size.** A title that reads comfortably at 1024px can go marginal at 300, but the answer is a heavier face, more contrast against its ground, or a framing rule — *not* a bigger title. A headline-sized title is the single clearest tell of a generated cover.
- **"Hazy" comes back saturated.** Recreating *Calm*, asking for heavy atmospheric haze produced a uniform orange field where the reference is washed toward cream. Haze describes the light, not the colour — ask for desaturated, washed out, or bleached toward white by name, and name the pale end of the range as well as the deep end.
- **Lift the black point, or the subject sits on top of the fog rather than inside it.** Name the dark end by colour (*smoky teal-grey*) and close the **palette** line — not the light line — with **"no true black anywhere"**. It is the single phrase that separates atmosphere from a cutout. Pair it with the edges that must survive — hair strands, the outline of a head, the edge of a guitar neck — because lifting the blacks otherwise takes the subject's definition with it.
- **Put the title where the texture is calm.** Type over busy detail is what pushes the model into misspelling it: on *Shimmery Guitars* the word "Guitars" broke three times out of three where the title crossed a dark guitar silhouette and zero times out of two where it sat on a smooth gradient. Name the thing to keep clear of — *"positioned low on the left in the empty fog and clear of the guitar neck"* — which can buy more than a nudged title, since the re-render answered it by flipping the neck to the opposite diagonal and freeing the whole left third.
- **Never write "very widely letter-spaced" unless you want capitals.** That phrase reliably drags the model into all-caps whatever case you asked for. "Moderate letter spacing, mixed case with only the first letter of each word capitalised" holds; so does "entirely in lowercase with no capital letters anywhere".
- **Name the typeface by its anatomy, not its vibe.** "High-contrast Didone serif, hairline horizontals against thick vertical stems, sharp unbracketed serifs" lands. "Interesting" or "monospaced" does not — a request for monospace came back as a soft rounded face near Comic Sans.
- **Glowing things need a medium, or you get an airbrush.** *Faith*'s original cover was a radiant cross that read as a worship-slide background, because the light had no physical cause — the fix is to name what the light is happening *in*. Asked for "a cross of light in dark air", the model returned the same soft gradient; asked for light blooming through condensation on a cold window, and for a seam of live embers, it rendered actual optics and actual material. Dust, fog, breath, condensation, smoke, water and glass all work. Light with nothing to pass through is a gradient, and a gradient is what "ethereal" degrades into.

- **Two things manufacture fake text, and the appended constraints stop neither** — they forbid captions and watermarks, not an object's own labelling or an artefact you asked for. **Subjects that plausibly carry text:** a boombox came back with a tuner dial of garbled pseudo-lettering, because real dials have writing on them; radios, books, signs, jerseys, album sleeves and shop fronts all carry this risk, so either avoid text surfaces or say the object's dials, labels and markings are blank and unlettered. **Requested degradation:** "VHS tape noise", "tracking glitches" and heavy grain resolve into smeared lettering, so exclude the side effect by name — "no smeared artefacts resembling letters, words or corrupted text anywhere."
- **Ask for sharpness or you may not get it.** A "shot close, shallow depth of field" crowd of hands came back soft, and Rian noticed before I did. When detail matters, name it: sharp focus front to back, deep depth of field, no blur anywhere, and the specific things that must resolve — individual beads, skin texture, fingernails.
- **Small objects at distance dissolve.** Anything that has to stay identifiable — a flag, an instrument, a face — must be large in frame or cropped close. A South African flag on a distant pole came back as a green-and-red smear with a yellow blob, and the composition couldn't be rescued without moving the flag closer, which made it a different picture.

## Matching a real logo or typeface

When Rian asks for a band's actual lettering, three things are true and worth saying plainly:

1. **You cannot load a font file.** The image model renders type from description only, so the output is *evocative of* the logo, never a match. Say so rather than implying otherwise.
2. **Go and look at it first.** Don't design from memory or from a font-identification forum — those are usually guesses. The Spotify credentials already in `.env` will fetch official artwork: search `/v1/search?type=artist`, then `/v1/artists/<id>/albums`, `curl` a cover URL, and Read the image. Describe what you actually see.
3. **Describe the treatment, not the font.** The Midnight's wordmark reads as their logo because it is a *neon sign* — one continuous tube of uniform stroke width, connected cursive, cream core with a magenta halo — far more than because of any particular letterforms. Get the treatment right and the letterforms matter much less.

If an exact match genuinely matters, the only honest route is to render the artwork with `"title": null` and let Rian set real type over it in a design tool. Offer that instead of iterating toward a match you can't reach.

## Limits

**Private playlists 404 the fetch.** `fetch-playlist.mjs` authenticates as an app with zero scopes, so it reads public playlists only, and Spotify returns the same 404 for private, deleted, and mistyped. `scripts/spotify.mjs` authenticates as Rian and does see private playlists — `node scripts/spotify.mjs GET "/playlists/<id>/tracks?limit=100" --all` gets the tracks, and you build the brief from those by hand.

**Upload replaces, never merges.** `set-cover.mjs` works (verified Aug 2026 on *Melodic Dance*), but `PUT /playlists/{id}/images` overwrites whatever is there and Spotify keeps no history. A `mosaic.scdn.co` URL in the playlist's `images` is the auto-generated grid of album art, so replacing it costs nothing; any other URL is a cover Rian uploaded, and that one is gone the moment you overwrite it. Read the current image URL before uploading, and ask when it isn't a mosaic.

**Cost.** Measured Aug 2026: three mini/low drafts ≈ 816 image output tokens total, one `gpt-image-2` high ≈ 7,000, one `chatgpt-image-latest` high ≈ 4,600. Order of a few cents for the drafts, order of a quarter for the finals. Don't render six drafts because three felt thin — render three good ones.

## Models and quality

| Model | Use |
|---|---|
| `gpt-image-1-mini` | Drafts and cheap type experiments. The default in the script. |
| `chatgpt-image-latest` | **Finals.** On the *Guitars* test it produced a more convincingly photographic subject than `gpt-image-2` — correct pickguard, three single coils, tremolo, jack socket — for a third fewer tokens. One prompt, one render each, so keep watching rather than treating it as settled. |
| `gpt-image-2` | The prior default for finals; still good, leans more illustrative than photographic. |

`quality` accepts **low, medium, high, auto** and nothing else — `high` is the ceiling on every image model this account can reach, verified against the API on 2026-08-17. There is no tier above it, so don't go looking for one. `1024x1024` is the right size: Spotify serves 640px at most, so rendering larger buys nothing.

**Drafts are honest about composition, palette, subject and type placement, and dishonest about quality and title size** (the mini at `low` renders subjects soft and plasticky; the glyph floor is covered under the house style). When Rian judges a draft as looking cheap or its type as too large, say the tier is doing it and offer a full-quality render of that variant, rather than redesigning.

## Quick reference

| Command | Does |
|---|---|
| `fetch-playlist.mjs "<url>"` | Brief: name, era, genre tags, top artists, sample tracks |
| `fetch-playlist.mjs "<url>" --json` | Same, structured |
| `generate-cover.mjs --spec s.json` | Render every variant at draft quality |
| `... --only <label> --model chatgpt-image-latest --quality high` | Re-render one variant at full quality — better subject detail, but the composition drifts |
| `... --out <dir> --name <slug>` | Where it lands and what it's called (`--name` needs `--only`) |
| `... --edit <existing>.png` | Change one thing, keep the rest of the artwork |
| `sips -Z 300 <f> --out <f>-300.png` | The legibility check that actually matters |
| `open -a Preview <f> <f> <f>` | Put the drafts on screen before describing them |
| `set-cover.mjs "<url>" <f>.png` | Attach the finished cover to the playlist (destructive — read Limits) |

Spec fields: `slug`, `title` (`null` for a wordless cover), `outDir`, `model`, `quality`, `size`, `edit` (same as `--edit`), `variants[{label, prompt}]`.

Credentials, all in `product-ai/.env`: `OPENAI_API_KEY` renders; `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` fetch the brief; `SPOTIFY_REFRESH_TOKEN` is what `set-cover.mjs` needs for the upload. On `invalid_grant`, re-run `node scripts/spotify-auth.mjs` — see `managing-spotify-playlists`.
