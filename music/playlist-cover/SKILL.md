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

**People: no generated photorealistic humans.** Rian finds them cheesy and recognisably AI-generated (September 16, 2026). This includes celebrity likenesses, anonymous crowds, and rear-view figures; hiding a face does not solve it. For people, use an explicitly illustrated treatment or a real sourced photograph. Photographic generation remains suitable for objects, places and natural textures. Choose the emotional moment before styling it: a live playlist needs the connection of a performance, not merely a polished instrument. For a human-centred cover, establish the illustrated or real-photo direction with Rian before rendering.

On 2026-08-17 Rian named three of his own covers as the target: *Guitars* (a burning Stratocaster on flat red), *Calm* (a hazy amber sunrise over a lake, title in spaced caps inside a thin square rule) and *Dark Ambient* (a near-black storm sky over a barren plain, title tiny and low-contrast). They look nothing alike and they are built the same way. These four principles guide the composition; use the agreed medium for human subjects:

| Rule | What it means | The failure it replaces |
|---|---|---|
| **One idea, fully committed** | A single subject doing a single thing. Nothing added to fill space. | Collages and "and also a…" compositions, which read as clip art no matter how well rendered |
| **Photographic realism for non-human subjects** | Rendered or shot, with real light and real material. Human subjects use illustration or real photography, as above. | Generic clip art and synthetic photographic people |
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

**Historical typography observations (August 2026, mini/low).** These findings describe the old models; Flare and Sunburst have not yet been tested on these covers. In those tests, `gpt-image-1-mini` at `low` appeared to have a floor on glyph size and ignored instructions that tried to go below it: "one fifth", "one tenth", "a small discreet caption" and "vast empty space around the text" all came back at about a third. The same prompt on `chatgpt-image-latest` at `high` landed at one fifth, correctly spelled, first try. The following workarounds helped in those tests:

* **Mini/low drafts overstated title size.** If Flare misses the requested size, compare that variant at a higher quality before changing the layout. Mini/low also stacked lines in the old tests, so its two-line draft title did not predict a two-line final.
* **This is also why small type breaks.** Nearly every spelling failure lands on small text at draft tier, where the mini is straining against its own floor. At full quality the same tiny titles render cleanly.
* **Draft the short lockup and add the extra line at full quality.** Two elements is what the draft tier can hold. *The Midnight Essentials* broke four rounds running, even with the letters spelled out individually; shortening to *The Midnight* cleared it on the next render, and the full three-element lockup then came back perfect at full quality.
* **Numerals fail worse than letters, and the palette can contaminate them.** A *1990-2005* subtitle returned *1820 2009*, *1990-200S* and *1960-2005* in one batch — and the *1960* came from the one variant graded warm sepia, where the model read the grade as an era and dated the cover to match. Cut digits first when a lockup is fighting you; if they must stay, make the palette era-correct.

**A framing device does most of the work on a quiet cover.** Rendering *Calm* with a square rule, with a taller rectangle, and with none, Rian rated both framed versions good and the unframed one was a stock sunset with a word on it — same photograph, same type. When a quiet cover feels generic, add the rule rather than a second subject. Hairline rules and letter-spaced caps rendered reliably in the August draft tests, and Rian preferred having a rule over either particular proportion.

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

   Defaults are `gpt-image-2.5-flare` at `low`. If lettering or subject detail fails, retry the affected variant at `medium` before changing its design. The hard constraints (no logos, watermarks, fake UI, duplicated titles) are appended by the script, so leave them out of the prompt.

5. **Open every draft with the Read tool.** See the verification gate below. Re-render anything that fails before Rian sees it.

6. **Open the survivors in Preview, then present them** — `open -a Preview <file> …` with every draft in one command, in the same order you describe them. Rian compares them at full size in Preview, not in the transcript, and expects them to be on screen when he reads your summary. Then one line each on what the direction is doing. Not a paragraph.

7. **Promote his pick to full quality — render it both ways and let him choose.** Use `gpt-image-2.5-sunburst` at `xhigh` for both. Compare an edit intended to preserve the approved composition with a fresh render of the same prompt. Keep this comparison while gathering evidence on the new model; cost and timing are recorded in each usage sidecar:

   ```bash
   # a) edit — use the approved composition as the reference
   node ~/git/product-ai/.opencode/skills/playlist-cover/generate-cover.mjs --spec <scratchpad>/final.json \
     --edit <scratchpad>/drafts/<slug>-<label>.png --model gpt-image-2.5-sunburst --quality xhigh \
     --only final --name <slug>-edit --out <scratchpad>/finals

   # b) re-render — same prompt, full quality, fresh composition
   node ~/git/product-ai/.opencode/skills/playlist-cover/generate-cover.mjs --spec <scratchpad>/spec.json \
     --only <label> --model gpt-image-2.5-sunburst --quality xhigh \
     --name <slug>-rerender --out <scratchpad>/finals
   ```

   The edit prompt asks to reproduce the draft at higher fidelity — crisper edges, finer texture, cleaner letterforms — and says explicitly that nothing may move, resize or shift hue.

   **Why both (August 2026 observations with the previous models).** The edit kept the composition and recovered detail the draft never had, but struggled to re-expose a scene — it came back flat and waxy where the re-render had hard sunlight and real cast shadows. The re-render rebuilds the subject properly, and its cost is drift: on *Faith* it lost the approved composition, and the *Guitars* re-render was a different guitar in a different pose.

   **Route by what is changing: adding something inside the existing exposure goes to the edit, changing the exposure itself goes to the re-render.** The edit can add a medium into darkness that is already there and can lift a black point locally; asked instead for more haze on *Shimmery Guitars* it left the figure a hard silhouette sitting on top of the fog, where the re-render lifted the whole key and dissolved the figure into it. But an atmospheric win that shifts the mood is a loss — *Faith*'s re-render delivered every requested change and lifted the *whole frame*, turning a dark cover into a warm radiant one, so the edit took it.

   **Check saturation first on both, because that is the axis neither respects.** "Nothing else may move, resize or shift hue" holds for geometry and composition and not for grade: the *Trance Classics* edit was asked only to reset a typeface and sharpen metal and pulled the icy cyan out to near-neutral steel, while *The Midnight* re-render drifted warm the other way. For a lost grade, make a second edit that changes only the colour, explicitly passing `--model gpt-image-2.5-sunburst --quality xhigh`. August 2026 tally with the previous models: the edit won four of six promotions. Re-check these tendencies on Sunburst.

8. **Verify the final too**, including the 300px check. Then give him the path.

9. **Attach it to the playlist.**

   ```bash
   node ~/git/product-ai/.opencode/skills/playlist-cover/set-cover.mjs "<playlist url or id>" <cover>.png
   ```

   It re-encodes to JPEG under Spotify's 256 KB base64 ceiling, uploads, then reads the playlist back and prints whether a custom cover is actually live. A `202 Accepted` alone does not mean the image took, which is why the script checks rather than trusting the status code.

   The upload is destructive — see Limits. Read the playlist's current image first and ask before overwriting anything that isn't a `mosaic.scdn.co` URL.

Drafts and both finals stay in the scratchpad; only the cover he picks lands in `05-personal/music/playlist-covers/`.

## Changing one thing about a cover he already likes

Re-rendering generates fresh artwork. `--edit` sends the approved image as a reference so the model can preserve its composition. Verify that unchanged details survive, especially colour and lettering.

```bash
node ~/git/product-ai/.opencode/skills/playlist-cover/generate-cover.mjs --spec <scratchpad>/tweak.json \
  --edit <path-to-existing-cover>.png --model gpt-image-2.5-sunburst --quality xhigh
```

Write the prompt as *only the change*, and close it by naming what must not move — "leave the guitar shape, the glare, the composition and the colours exactly as they are." Without that sentence the model drifts.

Two rules:

- **Copy the cover to the scratchpad and edit from the copy** when the output path is the cover itself. Editing a file onto itself works, but a bad result then has nothing to fall back to.
- **Edits default to Sunburst/xhigh.** For an inexpensive type experiment, explicitly select `--model gpt-image-2.5-flare --quality low` and inspect its usage before expanding the batch. Apply the chosen treatment to the original with Sunburst/xhigh. Explicit CLI flags override spec values; spec values override defaults, so pass the final flags when reusing a draft spec.

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
| **Illustrated scene with people** | Singer-songwriter, indie, emo, country, soul, or live music where human connection is central. | Expressive illustration with a specific human moment; establish the treatment with Rian. Use real photography if a photographic human scene is wanted. |
| **Neon / retro graphic** | Synthwave, italo disco, city pop, new wave. Era clustered 1979–1991, or deliberately retro-modern. | Chrome, grids, dusk cityscape, one dominant hue against near-black, retro script or heavy geometric type |
| **Abstract texture** | Tags scatter across many genres, or lean experimental, techno, drone, jazz fusion. | Gradient, grain, fluid form, no literal subject, one hue plus white, widely tracked geometric sans |

**A subject in an environment reads as stock photography.** The object-on-a-flat-field row wins ties for a reason: a guitar against flat red is a cover, a guitar on a beach at sunset is a photograph with words on it. When an archetype calls for a real setting, keep the setting near-empty and let one thing carry it.

Era shifts the treatment inside the archetype: a 1985-median playlist wants grain, halation and slight print misregistration; a 2023-median one wants cleaner edges and a flatter palette. Popularity sets the type — see the title-scale table above.

## Writing a variant prompt

Six parts, in this order. Each is a phrase or two, not a paragraph.

1. **Medium and treatment** — photographic or rendered with real light and material for non-human subjects. For people, use the illustrated treatment agreed with Rian or a real sourced photograph.
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

**Cost.** Each render saves `<name>.usage.json` beside its PNG with the requested model, quality, size, operation, elapsed milliseconds, and full API `usage`. Use this to measure the new models on actual cover prompts. Both 2.5 models charge $30 per million image output tokens plus input charges; equal token rates do not imply equal per-image costs. [Pricing and usage guidance](https://developers.openai.com/api/docs/guides/image-generation#cost-and-latency)

Historical measurements from August 2026: three mini/low drafts used about 816 image output tokens total; one `gpt-image-2` high used about 7,000; one `chatgpt-image-latest` high used about 4,600. These are previous-model observations, not estimates for Flare or Sunburst.

## Models and quality

Defaults updated September 16, 2026. Flare drafts and Sunburst edits were tested on Goeie Ou Dae. Rian preferred the `xhigh` final over `high` and chose it as the final-quality default. Keep drafts at `low`; explicit spec and CLI settings still override defaults.

| Operation | Model and quality |
|---|---|
| Draft generation | `gpt-image-2.5-flare`, `low`; try `medium` if lettering or detail fails. Script default for generation. |
| Final generation | `gpt-image-2.5-sunburst`, `xhigh`; pass both flags explicitly. |
| Targeted edit | `gpt-image-2.5-sunburst`, `xhigh`. Script default for edits when the spec/CLI does not override it. |
| Difficult lettering or material detail | Try `max` on the affected variant if a visible problem persists at `xhigh`. |

Both 2.5 models support `low`, `medium`, `high`, `xhigh`, `max`, and `auto`. Keep quality explicit for predictable comparisons. Start at `1024x1024` and retain the 300px legibility check. [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)

OpenAI positions Sunburst for precise edits and Flare for fast everyday generation. Both were released September 8, 2026. [Release notes](https://developers.openai.com/api/docs/changelog)

The old mini draft and `chatgpt-image-latest` final models are scheduled to shut down December 1, 2026. Keep their names only in historical observations. The previous preference for `chatgpt-image-latest` over `gpt-image-2` came from one Guitars comparison; it establishes no ranking against the new models. [Deprecations](https://developers.openai.com/api/docs/deprecations)

On Goeie Ou Dae, Sunburst/high used 1,756 image output tokens in 39.1 seconds; xhigh used 3,122 in 58.2 seconds. Both used the same draft and prompt. Rian found xhigh clearly better even though the assistant judged the difference subtle. His visual preference determines the default; these measurements describe one comparison.

Judge each draft's composition, palette, subject, and type placement directly. If low-quality output looks cheap or its type is too large, compare at higher quality before redesigning. The old mini's glyph floor has not been established for Flare. Keep the full-size and 300px visual checks for every model.

## Quick reference

| Command | Does |
|---|---|
| `fetch-playlist.mjs "<url>"` | Brief: name, era, genre tags, top artists, sample tracks |
| `fetch-playlist.mjs "<url>" --json` | Same, structured |
| `generate-cover.mjs --spec s.json` | Render every variant at draft quality |
| `... --only <label> --model gpt-image-2.5-sunburst --quality xhigh` | Re-render one variant at full quality — better subject detail, but the composition drifts |
| `... --out <dir> --name <slug>` | Where it lands and what it's called (`--name` needs `--only`) |
| `... --edit <existing>.png` | Change one thing, keep the rest of the artwork |
| `sips -Z 300 <f> --out <f>-300.png` | The legibility check that actually matters |
| `open -a Preview <f> <f> <f>` | Put the drafts on screen before describing them |
| `set-cover.mjs "<url>" <f>.png` | Attach the finished cover to the playlist (destructive — read Limits) |

Spec fields: `slug`, `title` (`null` for a wordless cover), `outDir`, `model`, `quality`, `size`, `edit` (same as `--edit`), `variants[{label, prompt}]`.

Credentials, all in `product-ai/.env`: `OPENAI_API_KEY` renders; `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` fetch the brief; `SPOTIFY_REFRESH_TOKEN` is what `set-cover.mjs` needs for the upload. On `invalid_grant`, re-run `node scripts/spotify-auth.mjs` — see `managing-spotify-playlists`.
