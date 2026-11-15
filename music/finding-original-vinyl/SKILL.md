---
name: finding-original-vinyl
description: Use when the user wants a non-remastered vinyl LP of an album added to their Discogs wantlist, asks which vinyl pressing to buy, or compares original pressings, reissues, and remasters on vinyl. For CDs use finding-original-cds.
---

# Finding original vinyl on Discogs

## Overview

On vinyl the unit that matters is the **cut**: the lacquer an engineer cut, which every stamper and every pressing plant downstream copies. Label, country, and the `Reissue`/`Remastered` tags are evidence about the cut, not the cut itself. So group pressings by cut, price each group, read what owners say, and pick down a fixed ladder.

The user is in the US. A US original is the default target; anything else is a step down the ladder, not a different goal.

**Before the first Discogs call, read [discogs-api.md](../finding-original-cds/discogs-api.md)**: endpoints, the price-suggestion and reviews calls, auth, rate limits, and wantlist writes.

## The ladder

Take the highest rung that has stock and a price that makes sense:

1. **US original:** first-era US pressing of the original cut.
2. **Same cut, other country:** a pressing whose runout carries the US original's matrix (Canadian *Disintegration* `1681869`: `STE-60855 A … MASTERDISK-HW` DMM, the US cut at a third of the price; Mexican *Violator* `948760`: the US `1-26081-A-SR1`), or a later repress from the original stampers (UK 1986 *Pornography* `9804267` shares `FIXD 7 A //3 ▽420` with the 1982 first press).
3. **Other original-era pressing:** a different cut from the original tapes in the release era (German, Dutch, UK).
4. **Non-remaster reissue:** a later pressing with no new mastering. A reissue can be a **new cut** of the old master (1986 Elektra *Pornography*, cut by Dennis King); that's still a reissue, not a remaster.
5. **Remaster:** only when nothing above exists or has stock.

**Reviews can move a reissue up.** When owners who compared directly say a rung-4 reissue beats the original, and it costs less, it outranks rungs 1 to 3. The 1986 Elektra *Pornography* beat the A&M original this way.

**"A US reissue that isn't a remaster"** in the user's words is rung 4. When rung 4 is empty, the answer comes from rungs 2 and 3, and rung 5 stays last.

## Steps

Every step applies to every album. The helper does the fetching: `set -a; . ~/.config/ebay/credentials.env; set +a`, then `python3 vinyl-pressings.py <master|versions|detail|reviews> …` from this skill's folder.

1. **Fan out.** `master "<Artist> <Album>"`, then `versions <master_id>`. The helper drops unofficial releases, club editions, picture discs, test pressings, and white labels, and lists the unofficial IDs separately. Also set aside colored or numbered limited editions from after the original era; they're almost always remasters.
2. **Detail the candidates.** `detail <ids…>` for every original-era pressing with stock, every reissue that isn't tagged `Remastered`, and the two or three most common remasters (for the price comparison). It prints formats, catalog numbers, stock, floor, VG+/NM suggestions, side lengths, cutting credits, runouts, and ℗ years. A `CLUB?` line means the club marker sits in free text (German `Club-Sonderauflage`, a Columbia House or BMG licence line): treat it as a club edition.
3. **Classify each pressing** into a ladder rung, using these tests:
   - **Remaster** if any of: `Remastered` in release-level `formats[]`; a `Remastered By` credit; a `Mastered By` or `Lacquer Cut By` credit from the reissue era, naming someone other than the original engineer; a ℗ year in the notes that matches a known remaster; a runout shared with a tagged remaster; or a new mix ("new stereo mix" in notes or hype sticker). The 2020 *Seeds of Love* `16026538` says only `Reissue` but credits Tim de Paravicini mastering and a Paul Stubblebine cut: a remaster.
   - **Same cut** only when the runouts carry the same matrix number (`1-26081-A-SR1`, `ST-E-60855`, `FIXD 7 A //3`). The same engineer's mark on a different matrix is a separate cut: Canadian *Violator* reads `92-60811 … K-DISC BH`, Bobby Hata again, but not the US cut. Plant variants of one release (US 1982 A&M *Pornography*: Indianapolis, Electrosound, Monarch) share the matrix and are one cut; price them as a group and take the cheapest. When variants in a group are within about 15% on VG+, take the one with the most copies for sale and the most comparison reviews: *Big Chair*'s Hauppauge `2106689` ($32, 57 listed, 27 comments) over the Allied `14292010` ($29, 6 listed, 1 comment). One "US original" can hold several cuts, so check each plant variant's runout: *Big Chair*'s Allied `6579663` is Howie Weinberg's cut, not Calbi's.
   - **Unverified** when a reissue has no credits and no runouts. Say so; don't promote it above rung 4.
4. **Check content against the CD.** Compare the track count with the CD release. Flag a single LP with sides over about 25 minutes: long sides are cut quieter. The 1989 *Disintegration* LP drops two tracks and runs 30 minutes a side, and owners of the European pressing call it "very quiet."
5. **Price.** Rank on the **VG+ suggestion**; show NM, the live floor, and `num_for_sale` beside it. When the VG+ suggestion is more than twice the floor and at least 5 copies are listed, the suggestion is probably inflated: quote the floor-to-VG+ range and rank on its midpoint. A pressing with nothing for sale is out, however common.
6. **Read the reviews** for each finalist on rungs 1 to 4 and the main remaster: `reviews <ids…>`. A comment that compares two pressings directly ("played them side by side", "I have both") outweighs general praise. Album praise ("best Cure record") says nothing about the pressing. Note how many comments a verdict rests on; three is thin. When a review or note mentions fakes or counterfeits, find the replica among the unofficial IDs from step 1, compare its runout with the pick's, and tell the user what tells them apart.
7. **Decide.** Walk the ladder from rung 1. Add the pick **without asking** when it's on the highest rung with stock and its VG+ suggestion is at most 2× the cheapest remaster's VG+. Otherwise present the table and a recommendation, and ask. Asking costs one message; a wrong $200 add costs more.
8. **Add and hand off.** PUT the release to the wantlist, then give the US-shipping link `https://www.discogs.com/sell/release/<id>?ships_from=United%20States`. A pick from outside the US usually ships internationally: mention the shipping cost and possible customs or brokerage fees. For an original over $50, suggest asking the seller for runout photos before buying.

## Output

Report in this order:

1. **Two-sentence verdict:** the pick and the ladder rung it came from, and why the rungs above it lost (no such pressing, price, stock, or reviews).
2. **Pricing table**, remasters included:

   | Pressing | ID | Cut | VG+ | NM | Floor | For sale |
   |---|---|---|---|---|---|---|

   IDs link to `https://www.discogs.com/release/<id>`. Mark the pick in bold.
3. **Relative pricing:** the pick as a multiple of the remaster's VG+, and the US original as a multiple of the pick.
4. **Reviews:** the direct comparisons quoted, with the comment count behind each verdict.
5. **Content flags:** missing tracks or long sides, if any.
6. **Action:** "Added `<id>` (201)" with the sell link, or the single question when step 7 says to ask.

## Calibration

| Album | Outcome | What decided it |
|---|---|---|
| The Cure, *Disintegration* | Rung 2: Canada 1989 `1681869`, VG+ $82 | US original $226; Canadian runout shows the same Masterdisk/Howie Weinberg DMM cut |
| Tears For Fears, *The Seeds Of Love* | Rung 1: US 1989 `1800734`, VG+ $46 | Cheap original; every later reissue is a new master or mix despite the tags |
| The Cure, *Pornography* | Rung 4 promoted: US 1986 Elektra `750080`, VG+ $58 | Cheaper than the A&M original ($78), and a direct comparison calls it better |
| Tears For Fears, *Songs From The Big Chair* | Rung 1: US 1985 Hauppauge `2106689`, VG+ $32 | Original costs the same as the 2014 reissue, which is a new master despite the "Reissue" tag; tie-break on stock within the Calbi cut |
| Depeche Mode, *Violator* | Asked: US 1990 Sire `426350`, VG+ $162, or German `524566`, VG+ $58 | No non-remaster reissue exists (2014 Rhino is an untagged remaster); US original is 6× the remaster; a German counterfeit copies the runout |

## Common mistakes

| Mistake | What to do instead |
|---|---|
| Ranking on the floor price | The floor is one copy in unknown condition. Rank on the VG+ suggestion |
| Treating a missing `Remastered` tag as proof | Read the credits and runouts (step 3) |
| Treating countries as separate products | Group by cut; a foreign pressing of the US cut is rung 2 |
| Quoting Discogs ratings | They score the album: every pressing of the five albums above rated 4.2 to 4.8 |
| Adding an expensive pick without asking | Step 7's 2× rule decides; above it, ask |

Once the user buys one, remove it from the wantlist and record the order in their purchases-in-flight log, marked as vinyl.
