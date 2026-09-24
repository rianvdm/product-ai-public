---
name: finding-cd-bundles
description: Use when the user wants to buy CDs from their Discogs wantlist — the cheapest listing for each album, whether any eBay seller has several worth bundling, whether eBay or the Discogs marketplace is cheaper, or what a NAMED Discogs seller has from the wantlist. Triggers e.g. "what do my wantlist CDs cost", "cheapest place to buy these", "who has more than one of my wantlist CDs", "find CD bundles on eBay", "is eBay or Discogs cheaper", "what can I buy in one order", "check <seller> for my wantlist", "scan philadelphiamusic", "what does <seller> have". Sourcing and price, not which-pressing judgement — for choosing the right pressing use finding-original-cds.
---

# Buying wantlist CDs on eBay

## Overview

Price Rian's Discogs wantlist against live eBay listings — cheapest copy of each album, and whether any seller holds enough of them to be worth bundling.

**Core insight:** a CD remaster carries **its own UPC** — *Thriller* is `074643811224` original, `074646607329` for the 2001 Special Edition, `888750438621` for the 2014 reissue. So searching eBay by the barcode of the *exact wantlist pressing* returns that master and skips the remasters automatically. The barcode does the same job `finding-original-cds` does by hand. That's the whole trick; don't re-derive it.

**Corollary that matters:** this tool inherits its master judgement entirely from the wantlist. If a remaster got wantlisted by mistake, this faithfully finds remasters. The wantlist is the filter — curate it with `finding-original-cds` first.

**The barcode filters remasters. It does NOT filter club editions, and it does not filter packaging.** Found 2026-08-21 on The Cure *Disintegration*: eBay's `gtin` search returned 3 US listings and the cheapest, at $15.95, had **"MANUFACTURED BY COLUMBIA HOUSE UNDER LICENSE"** printed on the tray. A BMG copy (`D 101109` + "BMG Direct Marketing, Inc. under License") sat one row below it, advertised in the title as `9 60855-2`. Club pressings share the original's master and are indexed on eBay under the original's UPC, so **every filter this tool has passes them through.** Discogs doesn't have this problem — it catalogues club editions as separate releases, so a Discogs sell page for the wantlisted release is club-free by construction. On eBay you have to look. See *Reading an eBay listing* below.

**And check the other marketplace.** Every album is also priced against the Discogs marketplace floor, because eBay loses that comparison more often than not — see *The Discogs cross-check* below. Never report an eBay price without it.

## Buy the subset, and message the seller

Two things about bundles that are easy to get wrong, both learned the hard way on 2026-08-05:

**1. Never buy a whole bundle — buy the subset that wins.** A seller's price is competitive on some of their stock and bad on the rest. `resellingroly` held 5 wantlist albums; four of them beat the market but their *Nevermind* was $21.99 against $13.20 elsewhere. Buy those four, get *Nevermind* somewhere else. Evaluating bundles all-or-nothing made every one of 51 look like a loss — the script now computes the optimal subset (include an item whenever the seller's **price** undercuts the cheapest **landed** price elsewhere; shipping is paid once, which is what creates the room).

**2. The combined-shipping discount is negotiable, not a fixed property of the seller.** eBay exposes no combined-shipping rule through the API, and plenty of sellers have none configured — `resellingroly` charged 4 × per-item shipping to the cent, $18.98 on $24.23 of CDs. **Rian messaged them and they refunded the excess — ~$13.88, money confirmed received 2026-08-20.** So the "if they combine" figure isn't hypothetical; it's what you get by asking, asking worked first try, and it now has a closed loop rather than just a promise. That purchase saved ~$8.66 over buying the same four separately.

Scale expectations: US CD shipping is a near-flat **~$4.39 Media Mail** (median of 152 listings; 17% ship free), so savings are real but modest — roughly **4 of 50** bundles clear $1, topping out around **$6.50**. `--cheapest` is still the right default for "what does my wantlist cost"; the bundle view is for "is there a message worth sending."

```bash
# what it costs to buy the wantlist, cheapest listing per album
node ~/git/product-ai/.opencode/skills/finding-cd-bundles/find-bundles.mjs --cheapest

# bundle view — every seller now carries a verdict vs buying separately
node ~/git/product-ai/.opencode/skills/finding-cd-bundles/find-bundles.mjs --min 3
```

| Flag | Effect |
|------|--------|
| `--cheapest` | **Start here.** Cheapest landed listing per wantlist album + a total |
| `--min N` | Bundle view: only sellers with N+ albums. **Leave it at the default 2** unless the wantlist is large — see below |
| `--html` | Write + open a review page: photos, condition, landed price, per seller. **Use this when Rian wants to actually pick things** |
| `--zip NNNNN` | Quote shipping to this ZIP (no default — set your own). Without it, ~half the listings report only "CALCULATED" |
| `--country XX` \| `ANY` | Seller location (default `US`) |
| `--json` | Machine-readable, for further filtering |
| `--refresh` | Ignore the release cache — barcodes *and* Discogs prices (`~/.cache/cd-bundles/`) |

The Discogs cross-check has no flag. It runs in every mode.

## The Discogs cross-check

Added 2026-08-05 after Rian asked the obvious question nobody had asked: *is eBay even the cheaper venue?* Mostly it isn't. On the run that prompted it, **9 of 19 albums were cheaper on Discogs**, $151.25 of eBay listings against $26.91 of Discogs floors.

Every album gets `GET /marketplace/stats/<release_id>?curr_abbr=USD`, printed under its eBay row as `Discogs: N for sale from $X + shipping` with a `/sell/release/<id>` link. **Always on — there's no flag and no reason to want the worse picture.**

**The ⚠ marks rows where eBay's landed price exceeds the Discogs floor by more than $10** (`DISCOGS_SHIP_GUESS` in the script). That margin is a deliberate hedge, not a measurement — see the three blind spots below. Read the marker as "worth opening the tab", never as "definitely cheaper".

### Three things the floor does not tell you

The Discogs figure is **not** comparable to an eBay landed price, in three specific ways. Say so whenever you quote it:

1. **No shipping.** eBay's numbers here are landed to the configured ZIP; the Discogs floor is item-only.
2. **No seller country.** The stats endpoint takes no location filter, so the global floor skews toward Europe and Japan — exactly the sellers whose shipping erases the gap. This is why the margin is $10 and not $5.
3. **No condition.** Every eBay row carries a grade; the floor carries none. A $0.50 *Sonicpraise* could be anything.

This is the *only* marketplace data the API exposes — Discogs closed per-release listing enumeration years ago, so there's no way to see the actual listings, their conditions, or their shipping. Don't go looking for a better endpoint; there isn't one.

### It flags, it never filters

Nothing is dropped or hidden on the strength of a Discogs price. A floor that's really a Japanese seller quoting $22 shipping would silently delete a perfectly good US listing, and you'd never know. Show both numbers; let Rian judge.

**Bundle math stays eBay-internal.** The `✓`/`✗` subset logic still compares against the cheapest *eBay* alternative, which is what its verdict claims. Flagged items just carry a ⚠ so a "winning" bundle item that's still worse than Discogs is visible.

### The coverage gaps are where it pays off most

Albums eBay can't see used to be a dead end. Now they carry a price and a link — and they're often the cheapest things on the list:

```
No US eBay listings found for:
  Massive Attack - Mezzanine  —  Discogs: 25 for sale from $2.30 + shipping
  The Postal Service - Give Up  —  Discogs: 25 for sale from $4.01 + shipping
No barcode on the Discogs release (invisible to eBay's gtin search):
  Delta Blue - Turn  —  Discogs: 1 for sale from $39.53 + shipping
```

**Read this section out loud in any summary.** It's the part that changes what Rian actually buys.

### Caching

Barcodes cache forever (they never change); **prices cache for 12 hours** and live under a `stats` key in the same `~/.cache/cd-bundles/releases.json`. First run of the day adds ~25 Discogs calls at the existing 1.1s throttle (~28s); re-runs add none. `--refresh` clears both. A Discogs failure is swallowed and deliberately not cached — the cross-check is an enrichment, so a hiccup can't sink an otherwise good eBay run, and the next run retries instead of going 12h blind.

## When to use

- "Who has several of my wantlist CDs?" · "find me a bundle" · "what can I buy together"
- "Is eBay or Discogs cheaper for these?"
- Before placing an order, to check whether waiting to batch is worth it

Not for: choosing which pressing to want (→ `finding-original-cds`), vinyl, or actually placing the order — see *Reviewing and buying* below.

## Tool reality — what returns what

| Need | How | Notes |
|------|-----|-------|
| Wantlist | Discogs `GET /users/elezea-records/wants` with a PAT | Username is **`elezea-records`**, not `rianvdm` |
| Barcode for a release | `GET /releases/<id>` → `identifiers[]` where `type == "Barcode"` | Strip non-digits; eBay wants bare digits. Some releases have none |
| eBay listings | Browse `item_summary/search?gtin=<upc>` | `gtin` takes **UPC/EAN only**, never a catalog number |
| Seller | `.seller.username` on each item summary | The field the whole grouping hangs on |
| Seller location | `.itemLocation.country` | Filter on it — see below |
| Discogs price floor | `GET /marketplace/stats/<id>?curr_abbr=USD` | `{num_for_sale, lowest_price, blocked_from_sale}`. Item price only, any country, no condition |
| Discogs listings | **Does not exist** | Per-release enumeration was closed years ago. The aggregate above is all there is |
| Cart / checkout | **Does not exist** | No third-party cart API; Order API checkout is Limited Release |
| Your own *buyer* orders | **Does not exist** | `/marketplace/orders` returns orders where you're the **seller** only. Outstanding purchases have to be transcribed by hand — see [[cd-purchases-in-flight]] |
| A seller's shipping policy | **Does not exist** | Only the cart shows it. `shipping_price` on a listing is not it — see below |

**Credentials** live in `~/git/product-ai/.env` (and mirrored in `~/.config/ebay/credentials.env`): `EBAY_APP_ID`, `EBAY_CERT_ID`, `DISCOGS_TOKEN`. The script reads only those keys and never prints them.

⚠ **The two `DISCOGS_TOKEN` values are not interchangeable.** Reads work from either, but the one in `~/git/product-ai/.env` returns **403 on every write** — wantlist add/remove included (verified 2026-08-22). For any write, source `~/.config/ebay/credentials.env` and nothing else. A 403 here is the wrong token, not an account permission problem.

**If eBay auth returns `invalid_client`,** the production keyset has been deactivated. Fix at Application Keys → **Notifications** → **Marketplace Account Deletion** → toggle **"Not persisting eBay data"** → Confirm. That gate — not a human approval queue — is what holds up new keysets, and it activates the key immediately.

## Steps

1. **Run `--cheapest`** unless the question is specifically about one seller or one parcel. It handles wantlist → barcodes → searches → Discogs floors, and caches both so repeat runs make almost no Discogs calls.
2. **Lead with the ⚠ summary line, not the eBay total.** `$244.33 for 19 albums` on its own is misleading when 9 of them are cheaper on Discogs. Quote both numbers and the three caveats (no shipping, any country, no condition).
3. **Read the coverage gaps it prints at the end.** These are the albums eBay can't see — and they now carry Discogs prices, which is often where the best buys are. Never imply full eBay coverage.
4. **Run the bundle view at the default `--min 2`** and **quote the verdict line**, not the album count. It names the subset to buy (`✓`/`✗` per item, with where to get the `✗` ones instead) and what the message is worth. Expect ~4 in 50 to clear $1. Only raise `--min` if the output is genuinely too long to read — see *Don't raise `--min` on a short wantlist*.
5. **If Rian is picking rather than browsing, re-run with `--html`** and hand him the page — condition and cover art are what he'll actually decide on.
6. **Hand off the listing links.** Order placement is his; see *Reviewing and buying*.

## Don't raise `--min` on a short wantlist

Learned the expensive way on 2026-08-05: the bundle view was run at `--min 3`, reported three sellers and no bundle worth messaging — and Rian then bought **two CDs from `boris32` in one order**, a seller holding exactly 2 wantlist albums that the threshold had filtered out entirely.

The arithmetic is unforgiving. A 25-album wantlist simply doesn't produce many 3+ sellers; that run had three, all of them duds. **The number of qualifying sellers falls off a cliff as the wantlist shrinks**, so a threshold that was reasonable at 50 albums hides most of the real overlap at 25.

**Use the default `--min 2`.** Raise it only when the output is too long to read, and if you do, say which threshold you used so a missed 2-album pair is attributable rather than invisible. The earlier "3 is the useful floor" guidance was written when the wantlist was larger and is now wrong.

## Filter the seller's location, always

The default `--country US` exists because without it the top result is misleading. On 2026-08-05 the biggest apparent bundle was `dahub_australia` holding **9** wantlist albums — shipping from AU erases the saving that makes a bundle worth assembling. `koreadisco` had the same problem. Only drop to `--country ANY` if Rian asks, and if you do, say where the sellers are.

## Output

Per seller, best first:

| Field | Why it's there |
|-------|----------------|
| Album count + seller feedback % (score) | Whether the bundle is worth it, and whether the seller is trustworthy |
| `landed $X–$Y if combined · separately $Z` + a **verdict line** | The economic case. $X assumes no combining (common), $Y assumes one box at their top rate, $Z is the same albums bought from whoever's cheapest. Read the verdict, not the album count |
| Per listing: price + shipping, **condition**, album, item URL | Used CDs range Acceptable→Like New at similar prices; condition is the real differentiator |
| The seller's own listing title | Often names the pressing outright (`"Nirvana NEVERMIND CD ORIGINAL 1991 Geffen DGCD24425"`) — free confirmation you're getting the right master |
| `offer` / `AUCTION` / `LOT` tags | `offer` = Best Offer accepted (negotiation lever). `AUCTION` = **has a bidding option, which does not mean it lacks a Buy It Now** — see below. `LOT` = multi-disc lot, price not comparable |

**An `AUCTION` tag does not mean "can't buy it now."** `buyingOptions` is an array, and a listing carrying **both** `FIXED_PRICE` and `AUCTION` is a buy-it-now *with* bidding — `price` is the BIN price and `currentBidPrice` is the live bid. On 2026-08-05 an ad-hoc *OK Computer* search that filtered out everything tagged `AUCTION` reported the best US copy as **$28.24** when a dual-format listing was sitting at **$16.90** BIN — a 67% overstatement. Only exclude a listing when `buyingOptions` is `AUCTION` *alone*. The main script gets this right (it tags but never drops); ad-hoc searches are where the mistake happens.
| `Discogs: N for sale from $X + shipping` | The other venue's floor, with a ⚠ when eBay loses by >$10. Advisory — see *The Discogs cross-check* |
| Coverage gaps at the end | Which albums eBay returned nothing for, **now with Discogs prices** — always report these |

`--html` renders the same data as a contact sheet with cover thumbnails, with the Discogs floor as a clickable badge under each card. That's the one to use when the next step is choosing, not scanning.

**Ordering:** `--cheapest` lists albums **alphabetically**, so ⚠ rows fall wherever the album name lands. Only the bundle view ranks by economics (sellers by net saving, best first). Don't describe the cheapest list as prioritized.

## Reviewing and buying — the actual workflow

There is **no third-party cart API** on eBay, and Order API guest/member checkout is Limited Release requiring Developer Technical Support (checked against live docs 2026-08-04). So the tool ends at links. The flow from there:

1. **Open the ⚠ items on Discogs first.** That's where the sell page shows what the API won't: the actual listings, their conditions, and each seller's country. A $2.00 floor from Portland is a buy; the same floor from Osaka usually isn't. Do this before building an eBay cart, not after.
2. **Review the rest with `--html`.** Photos, condition, and the seller's title in one page. Discard anything where the title contradicts the wantlist pressing, or the condition is worse than you'd accept.
3. **Add each item to the eBay cart** from its listing page. The cart holds items from multiple sellers, but **combined shipping only ever applies within a single seller.**
4. **Check the cart's shipping line, and if it's charging per item, ask.** eBay doesn't expose combined-shipping rules through the API, and many sellers have none configured — the cart will happily quote 4 × Media Mail. **Message them; it works.** On 2026-08-05 `resellingroly` quoted $18.98 shipping on $24.23 of CDs and refunded the excess when asked. That single message is worth more than any of the automated savings this tool finds.
5. **Buy the `✓` items only.** The `✗` ones are cheaper elsewhere and the script prints where. Adding them "since I'm already ordering" is how a winning bundle turns into a losing one.
6. **Check `buyingOptions` before skipping an `AUCTION` item.** Auction-only listings can't be bundled into a straightforward checkout, but a listing that is `FIXED_PRICE` *and* `AUCTION` has a Buy It Now and is bundleable like any other — and is often the cheapest copy on the page.

## Calibration — what a healthy run looks like

Measured 2026-08-05 against a 32-item wantlist (US, used):

- **26 of 32** albums returned at least one UPC-matched listing; 1 had no barcode on Discogs; 4 had no US listings at all.
- `--cheapest` totalled **$282.32 for 23 albums**, ~$12.30 each landed.
- **~50 sellers with 2+**, 13 with 3+ — of which **4 are worth messaging**, saving $1.58–$6.46 on the optimal subset. Judged all-or-nothing instead, zero would have looked worth it.
- **Precision is excellent** — zero remasters/deluxe/anniversary editions across 50 hits for *No Jacket Required*; the barcode filter genuinely works.
- Title-mismatch drops run ~3%, and inspecting them showed only true junk (a Blind Melon CD mis-tagged with Phil Collins' UPC, two "you pick" lot listings).
- Shipping: median **$4.39**, 17% free, max $24.

Re-measured 2026-08-05 on the 28-entry wantlist (25 unique albums) after the `resellingroly` purchase:

- **19 of 25** priced on eBay, totalling **$244.33**; 4 had no US listings, 1 no barcode.
- **Only 3 sellers with 3+ albums, and none worth messaging** — every one came back "only 1 item here beats buying elsewhere". But a 2-album seller Rian did buy from was hidden by that threshold; see *Don't raise `--min`*.
- **9 of 19 flagged cheaper on Discogs** — $151.25 of eBay listings against $26.91 of floors. If a run flags almost nothing, suspect the stats call is failing silently rather than eBay suddenly being competitive.
- All 5 coverage-gap albums had Discogs stock, 4 of them under $5.

If a run comes back dramatically worse than this, suspect the wantlist changed or the location filter, not the approach.

## Reading an eBay listing before buying it

The script's output is a shortlist, not a verdict. Three checks close the gaps the API can't see, and on 2026-08-21 they eliminated **the three cheapest US copies** of an album in a row.

1. **Read the tray photo for a club marker.** "MANUFACTURED BY COLUMBIA HOUSE UNDER LICENSE" or "BMG Direct Marketing, Inc. under License" plus a `D`-prefixed catalog number (`D 101109`). Both are printed on the back tray card and are invisible in the title, the barcode and the item specifics. **A listing with no back-tray photo cannot be cleared** — either message the seller or move on.
2. **Read `Case Type` in the item specifics.** `Paper Sleeve` means a bare disc with no jewel case and no booklet, and the price looks like a bargain right up until you notice. One of the three 2026-08-21 rejects was this.
3. **Ignore the disc-face plant credit.** It does not identify the pressing — see the *Common mistakes* entry below.

**Run a keyword search alongside the barcode search when the answer matters for one album.** `gtin` recall on individual listings is poor: the same album returned **3 listings by barcode and 22 by keyword**, and every genuinely buyable copy was in the keyword set. Filter the keyword results on `/disintegration/i`-style title matching plus a negative-keyword list (`remaster|deluxe|anniversar|expanded|box set|\d\s*cd|vinyl|lot|you pick|import`). The barcode is the precision instrument; the keyword search is the recall instrument. **The main script deliberately uses only the former** — it is scanning 30+ albums, where precision matters more — so this is a one-album manual step, not a change to the tool.

## A 2xCD album could vanish from every list — fixed 2026-09-10

`LOT_RE` carried `\d+\s*cd'?s?\b` to catch "12 CD lot". It also matched **"2CD"**, which is how sellers correctly describe a legitimate 2-disc album — so the only US listing for *Across A Wire* (a 2xCD) was classed as a lot.

The classification alone would have been survivable. The damage came from the accounting: `kept` counted every title-plausible listing, but the priced list is built from `bestLanded`, which additionally requires `!isLot && ship != null`. So the album satisfied `kept > 0` — keeping it out of `noListings` — while never entering `bestLanded`. **It appeared in the priced list, in neither gap list, and in no total.** It was not mispriced; it was invisible, and the run's "21 albums" looked complete.

Two fixes, and the second matters more:

1. `isDiscCountLot(title, qty)` compares the number in the title against the wanted release's disc count, which is now stored on each want. "2CD" on a 2xCD want is a match; "12 CD" is a lot.
2. The gap test is now `kept === 0 || !bestLanded.has(album)`, so **an album that produces no comparable price is always reported**. This also catches the other silent-drop path — every listing quoting CALCULATED shipping, which `--zip` reduces but does not eliminate.

**Reconcile the counts on any run you're going to act on:** priced + both gap lists should equal the distinct wantlist albums. That arithmetic is the only thing that catches a vanish, and it is cheap. This is the same regex family as the `\bCD\b` / `2xCD` format-filter bug in `seller-scan.mjs` — a pattern that cannot tell a disc *count* from a lot *size*.

## Non-US sellers quote their own currency

`seller-scan.mjs` captured `l.price.currency` but printed a hardcoded `$`. Every registry seller was American, so it never showed until Gavin-B-And-G (London) — where **£16.00 shipping printed as "$16"**, understating it by about a third. It now prints the real symbol via `CUR_SYMBOL`.

**A foreign seller changes the arithmetic twice over**: the item prices convert, and the shipping tiers are quoted in the seller's currency too. Convert before comparing anything against the $6.00 local-shop benchmark or a Discogs floor in USD. Discogs' own listing page shows an "about $X" line — use it to sanity-check the rate rather than assuming one.

## Common mistakes

- **Reporting recall as a percentage of keyword-search hits.** Tried on 2026-08-05 and it's the wrong metric — Nevermind's UPC matches "only 10.5% of keyword hits" but that's **75 real listings**, which is abundant. What matters is absolute listings per album and whether sellers overlap. The percentage makes a working tool look broken.
- **Passing a catalog number to `gtin`.** It accepts UPC/EAN only. Catalog numbers are for the human eyeball step in `finding-original-cds`.
- **Trusting the raw hit list without a title check.** eBay's gtin index carries some mis-tagged listings; the script requires a shared distinctive token with artist or title. If a result looks wrong, it probably is.
- **Treating a UPC match as proof it isn't a club edition.** It isn't. Club pressings share the original's master and turn up in the `gtin` results under the original's barcode — see the *Core insight* caveat. The tray card is the only tell.
- **Reading the gtin result set as the listing set.** `gtin` returned **3** US listings where a keyword search returned **22** for the same album. The per-album coverage figures in *Calibration* say how often an album gets **at least one** hit; they say nothing about seeing most listings *within* an album. Never quote a gtin cheapest as "the cheapest on eBay" for a single-album question.
- **Reading the plant credit off the disc face.** "MADE IN U.S.A. BY WEA MANUFACTURING INC." is printed on the disc of pressings from *several* plants — the wantlisted 2026-08-21 *Disintegration* (`178726`) carries that text while being an SRC pressing, with `SRC` appearing only in the matrix runout. Nearly rejected a good listing on this. **Plant identity lives in the matrix, never in the printed credit.**
- **Implying full wantlist coverage.** Roughly one album in six returns nothing. Name them.
- **Trusting the run's album count without reconciling it.** Priced + both gap lists must equal the distinct wantlist albums, or something vanished — see the 2xCD section above.
- **Trusting a `0 raw` on an artist with an `&` in the name.** The inventory search returns empty on a literal `&`. Probe it by hand.
- **Recommending a bundle on album count.** The largest bundle is routinely the worst buy — `randrcollectables` had 6 albums at a flat $21.95 each. Quote the verdict line, which is computed on the optimal subset.
- **Raising `--min` to shorten the output.** A 2-album seller is a real bundle, and on a short wantlist most of them are. `--min 3` hid the order Rian actually placed on 2026-08-05.
- **Judging a bundle all-or-nothing.** One overpriced item shouldn't sink four good ones; it should just be bought elsewhere. This mistake made the tool report "no bundle is ever worth it," which was flatly wrong — Rian bought 4 of 5 from `resellingroly` the same day and saved ~$8.66.
- **Treating combined shipping as a fixed property of the seller.** It's negotiable. Ask before concluding a bundle doesn't pay.
- **Letting a "you choose / combine" listing win a price comparison.** These pick-from-a-list listings match a barcode and quote a headline price that isn't the price of that disc. They're filtered now; if a suspiciously cheap result appears, read the title.
- **Quoting the Discogs floor as if it were a landed price.** It has no shipping, no seller country, and no condition. "Cheaper on Discogs" is a lead to follow, not a conclusion — always attach the caveats.
- **Reporting the eBay total without the ⚠ count.** `$244.33 for 19 albums` reads as the answer when half the list is cheaper elsewhere. The two numbers belong in the same sentence.
- **Forgetting the coverage gaps now have prices.** They used to be a shrug; they're now often the best buys on the list (Mezzanine at $2.30 against no US eBay listing at all).

## Scanning a named Discogs seller — `seller-scan.mjs`

Everything above prices the wantlist against **eBay**, with Discogs present only as an aggregate floor. This section is the Discogs-side counterpart: **name a seller, get their actual listings** — condition, shipping origin, seller comments and all.

```bash
node ~/git/product-ai/.opencode/skills/finding-cd-bundles/seller-scan.mjs philadelphiamusic [seller2 ...]
```

**Keep the seller list and their shipping policies in [[seller-registry]].** Shipping policy is the whole strategy — see below.

### Why this exists, and why it looks the way it does

Discogs closed *release → sellers* years ago and the sell pages sit behind a Cloudflare challenge, so `finding-cd-bundles` can only ever show `num_for_sale` + `lowest_price`. But **seller → listings is open**, so naming sellers inverts the dead end. Three facts, all found by probing on 2026-08-05, none documented:

1. **`GET /users/{seller}/inventory?q=<free text>` filters that seller's stock.** Undocumented, and the only reason this is feasible — `q=annie lennox medusa` cut philadelphiamusic's 99,068 listings to 7.
2. **Pagination is capped at 100 pages for anyone else's inventory** — `403 {"message":"Pagination above 100 disabled for inventories besides your own"}`. A 10,000-item ceiling that **`sort`/`sort_order` do not move**, so you cannot partition past it. Enumeration is out; `q=` is the only route.
3. **Inventory listings return `release.master_id: null`**, and `q=` matches loosely (`michael jackson thriller` returns Aretha Franklin and David Sanborn). So every candidate is resolved against `/releases/<id>` — which also supplies the authoritative `formats[]` for the remaster check.

### It matches the master, not the release

Unlike the eBay path — which searches the **barcode of the exact wantlisted pressing** — this matches on `master_id`, so **any** pressing of a wantlist album counts, then filters remasters out afterward. That's usually what Rian wants from a big seller ("do they have a non-remastered copy of this at all"), but it means the two halves of this skill answer subtly different questions. Say which one you ran.

**When the wantlist entry was chosen for its *packaging*, master-level matching actively misleads.** On 2026-08-16 the fixed filter surfaced *Across A Wire* at five sellers from $3.00 — every copy the US `DGCD2-25222`, which is a **4-panel digipak**, when the wantlisted release is the EU `GED 25226` **jewel case** picked deliberately for that reason. None carried `[exact wantlist pressing]`, which is the only signal separating them.

**So read that marker before quoting a price**, and say plainly when a hit is a different pressing than the one wantlisted. A cheap hit on the wrong packaging is not a find.

**But a negative marker is not a skip verdict either — compare catalog numbers before ruling a hit out.** On 2026-08-23 two Pink Floyd hits at The-Music-Fix were called "wrong pressing, skip" because their release IDs differed from the wantlisted ones — yet both carried the **same catalog number** (`CK 33453`, `CK 40599`): sibling pressing runs of the same edition, differing only in matrix/plant, which is materially what the wantlist wants unless the entry is packaging- or matrix-driven (*Across A Wire* is; most aren't). Rian caught it. The ladder is: same release ID → exact; same catno → sibling run, normally fine; different catno → the real different-edition case that deserves the skip scrutiny.

### Shipping policy is the strategy

Record it in the registry for every seller, and read the results through it:

- **Flat rate + unlimited combining** (philadelphiamusic: **$5.00 flat**, cart states "add up to 997 more discs/tapes at no additional shipping cost"): only the first item carries shipping. Judge each album on its **item price** against another venue's **landed** price, and batch aggressively — re-scan whenever the wantlist grows, because anything they stock is worth adding at item cost alone. This flipped the Cranberries from "skip, $10 landed vs $9.98 on eBay" to "buy, $5 marginal".
- **Per-item shipping:** treat albums independently, and ask about combining before checkout — it's negotiable and asking has worked.
- **Unknown:** assume per-item. The API never exposes shipping rules; **only the cart does**, so confirm there before concluding.

⚠ **`shipping_price` on a listing can be the *incremental* rate, not the first-item rate.** Found on `AndrewRocco` 2026-08-22: 95 of 100 sampled listings quoted `$1.00`, which reads like the cheapest shipping anywhere in the registry. The real policy is **$6.00 for the first item, then $1.00 each** — the API was reporting the additional-item tier. This is a third distinct failure mode alongside the `$0.00` weight-calculator bug (ddsdiscsva, babshigh), and it's the dangerous one, because `$1.00` looks like a plausible real number where `$0.00` obviously doesn't.

**So never write a shipping figure into [[seller-registry]] from `shipping_price`.** Ask Rian to put one item in a cart and read the quote back — he did exactly that for AndrewRocco and it took one message. A uniform suspiciously-low quote means a tiered seller, not a bargain.

### Calibration

philadelphiamusic, 2026-08-05, 32-item wantlist: 4 albums matched across 9 listings. Cart of 3 came to $16.00 + $5.00 shipping against $40.63 for the same three on eBay — **$19.63 cheaper**, with sealed NM where eBay had VG and Good. (Cart built, not placed — the saving is quoted, not realised.) The standout was *The Police — Greatest Hits* at $7.00 sealed against $22.00 on eBay, on an album with only 3 US eBay listings.

### Known gap

The remaster filter reads the resolved `formats[]`, but **`Special Edition` is not tagged `Remastered` and will pass** — a 2009 *Nevermind* Special Edition came through at $69.73. Obvious at that price; a cheap one could slip past. For anything expensive, confirm the master with the matrix runout per `finding-original-cds`.

### `raw > 0 -> 0 cand` is the signature of a format-filter bug

Fixed 2026-08-15: `DESC_CD` was `/\bCD\b/i`, which **does not match `"HDCD"`** — there is no word boundary between the `D` and the `C`. HDCD is an ordinary CD that plays in any player, so every HDCD listing was fetched from the seller's inventory and thrown away one step *before* the master check. It cost an exact-pressing hit at $1.88 against $6.00 landed on eBay, and Rian found it by eye. Now `/\b(?:HD)?CD\b/i`; SACD, CDr, DVD and vinyl stay excluded via `DESC_OTHER`.

**The scan line is the tell.** `1 raw -> 0 cand -> 0 confirmed` means the seller *has* something matching the query that the format filter rejected — which is indistinguishable from an honest loose-match rejection unless you look. A true miss reads `0 raw`. **When Rian can see stock the scan can't, check the `raw > 0 -> 0 cand` rows first**, and print the offending `release.description` before assuming the search is fine.

**It happened again on 2026-08-16, wider: `\b(?:HD)?CD\b` also fails on `2xCD`.** Same cause — the `x` is a word character. **Every multi-disc release had been invisible to every seller scan ever run.** The fix is `/\b\d*x?(?:HD)?CD\b/i`, and re-scanning eight sellers raised the hit count at **six** of them: *Across A Wire* appeared at five sellers and *The Wall* at three, those being the only two 2xCD albums on the wantlist. SACD, CDr and `2xLP` stay correctly excluded.

**The lesson is the regex family, not the two instances.** `\bCD\b` fails against anything that prefixes CD without a separator — `HDCD`, `2xCD`, `3xCD`, `SHM-CD` is fine but `SHMCD` would not be. When adding a format token, test it against a list, and treat any `raw > 0 -> 0 cand` row as a bug report until proven otherwise.

### When the wantlisted release is ITSELF a remaster, an unconditional remaster filter guarantees a wrong answer

Fixed 2026-08-27. `DESC_BAD` rejected any CD description carrying `RM`, and `FMT_BAD` did the same against the resolved `formats[]`. But **some albums have no non-remastered edition, because the remaster IS the first release** — Sting's *Fields Of Gold* (1994) was newly mastered by Bob Ludwig at Gateway for that compilation, so nearly every pressing is tagged `Remastered`. On those, the filter could only ever return the sibling that happened to *lack* the tag, and silently dropped the exact wantlisted release.

ShinylVinyl held **four** US *Fields Of Gold* pressings. The scan reported one — `4465306`, the only untagged one — and dropped the exact wantlisted `4450033` **and** the NM `20804659` that turned out to be the right buy. The scan line read `4 raw -> 1 cand -> 1 confirmed`, which looks like an ordinary loose-match rejection.

**The fix is to make the remaster clause conditional, never to drop it.** `loadWantlist()` now computes `selfRemastered` per want from `basic_information.formats`, and:

```js
const descBad = (d, w) => DESC_BAD_ALWAYS.test(d) || (!w.selfRemastered && DESC_BAD_RM.test(d))
const fmtBad  = (f, w) => FMT_BAD_ALWAYS.test(f) || (!w.selfRemastered && FMT_BAD_RM.test(f))
```

`Club`, `Dlx`, `Anniversary`, `Promo`, `Test Pressing` and `Unofficial` stay unconditional — the Club Edition among those four *Fields Of Gold* copies is still correctly rejected.

**The general principle: the wantlist is the master filter.** The *Core insight* at the top of this file says so — this tool inherits its master judgement entirely from the wantlist, which is curated by `finding-original-cds`. A second filter that overrides the wantlist defeats the point, and it fails silently and specifically on the exact pressing. **Compilations and live albums are where this recurs**, since a comp is its own first release and often carries the tag.

### Cross-check a new seller against their Discogs wantlist page

This bug was caught because Rian opened ShinylVinyl's own **"in your wantlist"** seller page and saw four albums where the scan had marked three as exact. That page matches on the **exact release ID**; this scan matches on **`master_id`**. They answer different questions and neither subsumes the other:

* The Discogs page **misses same-catalog siblings** — it never showed their *Brothers In Arms*, *London Calling* or *Stay On These Roads*, all legitimate hits.
* The scan **can silently under-report** through a filter bug, as above.

**So open that page on every newly-added seller.** It costs one click, needs no API budget, and it is the only external check on this tool's recall that exists. Any album it lists that the scan didn't mark `[exact wantlist pressing]` is a bug report.

### An `&` in the query silently returns zero — fixed 2026-09-10

`q=Mumford & Sons Babel` returns **0** against a seller holding four copies. `q=Mumford Sons Babel` returns **4**. The `&` is correctly percent-encoded as `%26` by `URL.searchParams` — Discogs' inventory search simply dies on it, and reports the death as an empty result set rather than an error.

That makes it the worst possible failure shape: it is indistinguishable from the seller not stocking the album, so it reads as a legitimate `0 raw` and **the section below said to trust it**. Every seller scan ever run before this date silently omitted every artist with an ampersand in the name.

Reproduced on two sellers and isolated by elimination: `*`, `-`, `'`, `:`, `,` and the `(2)` same-name-artist suffix all match fine. Only `&` breaks. `cleanQuery()` in `seller-scan.mjs` now strips it before the request.

**The general rule: a wantlist entry whose artist or title contains punctuation deserves one manual `q=` probe before you trust a zero for it.** Found because Rian opened the seller's own wantlist page and saw two Mumford & Sons albums the scan had reported as absent — which is exactly the cross-check two sections below, doing the job it exists for.

### A zero is otherwise trustworthy — verified 2026-08-06

`q=` does a loose full-text match, so a one-word query looks alarmingly broken: `q=the cure` returned 29 listings containing no Cure release, `q=queen` returned 249 with no Queen. Tempting to read as a failing search. It isn't.

The script queries **artist + title together**, and that form has good recall — tested against six albums confirmed present in a seller's stock (*Jagged Little Pill Acoustic*, *Hours...*, *Boys For Pele*, Tin Machine's *Live: Oy Vey Baby*, Echobelly's *Lustra*) it found **6 of 6**, usually as the only hit. Trailing punctuation didn't matter.

So a reported 0 means the seller genuinely doesn't stock it — **unless the query contained an `&`**, per the section above. Sanity-check the inventory's format mix before writing off a whole scan, but **don't assume the search is broken just because single-word queries look noisy** — and check the `raw > 0 -> 0 cand` rows above before concluding anything.

### Hit count is not buy count

The most forgettable rule here. A 6-album hit looks like a 6-album order and was a 3-album order.

Scanning answers *"who has my wantlist albums"*. It does not answer *"who should I buy them from"* — for that, every hit still has to clear both alternatives:

1. **The eBay landed price** for that album, from `--cheapest`.
2. **The Discogs floor for the exact release the seller is listing** — not the wantlisted release ID, which is usually a different pressing with a different floor. `GET /marketplace/stats/<release_id>?curr_abbr=USD`.

Read the floor's **depth**, not just its price: 84 copies from $0.01 is real and reachable; 5 copies from $6.00 may be a foreign seller whose shipping erases the gap.

**A seller can hold six of your albums and deserve three of them. Report the split, not the hit count.**

⚠ **But once an order at a flat-rate seller is going out, stop comparing against the floor.** Marginal shipping is $0, so an extra disc must be judged on **item price against another venue's *landed* price** — the rule in *Shipping policy is the strategy* above. Comparing item price to a bare floor double-counts shipping and skips albums that were the cheapest way to get them.

Got this wrong on 2026-08-27: four ShinylVinyl albums were skipped as "5× the floor" when their shipping was already paid by a *Dark Side* order. *Brothers In Arms* at $6.04 marginal-free beat **every** registry alternative — dailybookstore $7.88 solo, CD_WAREHOUSE_817 $11.25 solo — and adding it killed a second order that existed only to carry it. Rian caught it by asking why the other matches weren't in the cart.

**"It's 5× the floor" is not a reason to skip an album whose shipping is already paid.** The floor still earns a skip on **depth** — 58 copies means you can genuinely do better — but that is a different argument, and say which one you're making.

### Sealed listings need a catalog-number check

A big seller clearing retail stock (`CD_WAREHOUSE_817`) lists mostly *"Brand New, Factory Sealed"* — and one listing said outright *"Cannot confirm matrix/pressing, as it is sealed."* Two of its sealed Mint hits carried **later catalog numbers than the wantlisted originals** (`88875043862` for *Thriller* instead of `EK 38112`; `B0015887-02` for *Nevermind* instead of `DGCD-24425`) and passed the remaster filter only because neither was *tagged* `Remastered`.

**Sealed + later catalog + unreadable matrix is the worst combination in this whole system** — it looks like the best listing on the page and can't be verified. Compare the catalog number against the wantlisted release on every sealed hit.

## Scanning a named eBay seller

The Discogs half of this skill can take a seller name and list their wantlist stock. The eBay half could not, until 2026-09-10. It can now, and the route matters because the two obvious approaches both fail.

Browse search accepts **`filter=sellers:{username}`**, but only alongside a `q`, `category_ids`, `gtin` or `epid` — a sellers filter on its own returns an error. That leaves two shapes:

* **Enumerate the seller's inventory** with `category_ids=176984` (Music > CDs) and page through. **Don't.** Deep offset paging is lossy: grebur-7102 reported `total: 5743` and returned **5,107 unique itemIds across 29 pages**, silently dropping the very listing that prompted the scan — which was in that category. Results reshuffle between pages, so items fall through the gaps. Enumeration looks authoritative and isn't.
* **Query per wantlist album with the ARTIST ONLY**, plus the sellers filter, and match titles locally. ~35 shallow calls, no pagination depth, and it found every listing enumeration found plus the ones enumeration lost. **This is the way.**

**Do not put the album title in `q`.** eBay ANDs every term, so a wantlist title more verbose than the seller's returns **zero**:

```
Counting Crows Across A Wire Live In New York City   -> 0
Counting Crows Across A Wire Live                    -> 1
Counting Crows                                       -> 4
```

The seller's title said "Live **From** New York" with no "City". The first version of `ebay-seller-scan.mjs` queried artist + title and **silently missed the exact listing this whole scan existed to find** — while still returning eight other hits, so it looked like it worked. Query broad, filter locally, and let the local matcher supply precision.

**Scope the search to `category_ids=176984` (Music > CDs).** Without it the scan returns vinyl, DVDs and box sets, and it is not a rounding error: it inflated rarewaves from 66 CD hits to 125, and their apparent best price for *Live At Wembley* was a **12" vinyl box set**. Roughly **40% of raw hits at the big new-media sellers were not CDs.** Guard the title as well (`vinyl|LP|12"|cassette|DVD|blu-ray|SACD`), because sellers miscategorise — but never reject on "box set" alone, since CD box sets are legitimate.

**Matching needs a coverage threshold, not a token hit.** Requiring one artist token plus *one* title token fails quietly by returning a real listing for the **wrong album**, which is worse than returning nothing:

| Wantlist album | Wrongly matched |
|---|---|
| *Jesus Freak* | "Welcome to the Freak Show: DC Talk Live in Concert" |
| *Live At Wembley '86* | "Queen Live Magic", "Return of the Champions" |
| *Rage Against The Machine* | "The Battle Of Los Angeles", "Maximum Rage" |

Requiring *every* title token overcorrects — the genuine *Across A Wire* listing omits "City". **60% of the title's distinctive tokens separates all of them**, and that threshold is what `ebay-seller-scan.mjs` uses.

**Self-titled albums need their own rule.** When the album title *is* the artist name, coverage is 100% for every record they ever made, so the threshold cannot help. Position discriminates instead: a listing for the self-titled record **leads** with the name, while one for another album leads with that album's. Without this, boris32's *Battle Of Los Angeles* and *Maximum Rage* both scored as the wantlisted debut.

These false positives are not cosmetic — they produced a "5 of 7 albums beat the market" verdict for boris32 that was really 4 of 6, and would have written fiction into the registry.

```bash
node ~/git/product-ai/.opencode/skills/finding-cd-bundles/ebay-seller-scan.mjs grebur-7102
```

It splits output into **complete** and **incomplete (disc only / no booklet)**, reading the description body for the latter — see below for why that matters.

### The gtin search misses stock the seller demonstrably has

`--cheapest` reported **no US eBay listings** for *Babel*. grebur-7102 had one, at $5.94. The barcode index simply doesn't carry every listing, which is the recall gap the *Common mistakes* entry warns about — stated there as "never quote a gtin cheapest as the cheapest on eBay for a single-album question", and here is the case that proves it. **A "no US eBay listings" line means the barcode search found nothing, not that eBay has nothing.**

### The description body outranks the item specifics — and bulk-template sellers are where they disagree

Written first as "read `Case Type` and `Edition` on every candidate", which caught some traps and **passed a disc-only CD straight through to a buy recommendation.** Rian caught it by opening the page.

grebur-7102's *Love Deluxe* at $6.03 reports **`Case Type = Jewel Case Standard`** in the item specifics. The first line of its description body reads **"NO BOOKLET   DISC ONLY"**. Both statements are on the same listing, and the item specifics are the wrong one. Their second *Love Deluxe* says the same in the description while carrying no `Case Type` at all, and two more listings put `***DISC ONLY***` in the title while the aspect still claimed a jewel case.

**How far this generalises, measured rather than assumed:** all four contradictions were that one seller's. Checking six listings across five other sellers (7946shantel, high5resaleshoppe, dad-at-home, charlie17766, spellbinder610, chbride71) found **zero** — every `Case Type` either agreed with its description or the description said nothing. Two of them positively declared `Cardboard Sleeve` on digipaks they were honest about.

So the honest rule is narrower than "the aspects lie": **item specifics are seller-entered, and a bulk lister working from a template will leave them at a flattering default while disclosing the truth in the description.** Read the description body first on every candidate — it costs one call and it is authoritative when they disagree — and treat a seller who contradicts themselves once as one who will do it again. **Precedence is description body, then title, then item specifics.** Fetch `/buy/browse/v1/item/{id}`, strip the tags from `description`, and read the first ~200 characters. Sellers who bulk-list from a template put the real disclosure there and let the structured fields default to something flattering.

What the item specifics are still good for, when nothing contradicts them:

* `UPC` — matched the *Across A Wire* listing to the wantlisted `GED 25226` family.
* `Edition` — `Greatest Hits` on a listing titled *Every Breath You Take* exposed a different 1995 compilation than the wantlisted 1992 `540 030-2`.
* A **track count in the description** is a cheap edition check: "13 soul-stirring tracks" matched Kari Jobe's standard `B002014102` against the Deluxe `B002014300`.

Also check `buyingOptions` for `BEST_OFFER`. All four candidates here had it, which is the same negotiation lever as asking about combined shipping.

## Discovering new sellers — `seller-discover.mjs`

`seller-scan.mjs` needs a name. When Rian asks for *new* big sellers, there is no endpoint that lists them and every HTML route is Cloudflare-walled (marketplace sell pages, Discogs forums, Steve Hoffman — all 403 to a fetcher).

**Don't guess usernames.** Tried on 2026-08-06: 146 guessed names yielded 25 live sellers, almost all record stores already known, and **nothing new above 30k listings**. Guessing can only surface sellers you can already name.

```bash
node ~/git/product-ai/.opencode/skills/finding-cd-bundles/seller-discover.mjs [probes]   # default 1800
```

Marketplace listing IDs are sequential integers (currently to ~4.35e9), and `/marketplace/listings/<id>` returns `seller.username`, `ships_from`, `condition` and `release.description`. Sampling random IDs samples the marketplace **weighted by listing count**, so big sellers surface by construction. Hit rate is ~3%; 1,800 probes nets ~55 live listings and ~54 distinct sellers in ~35 min. **Run it in the background and touch nothing else on the Discogs API meanwhile** — the throttle already sits near the 60 req/min cap.

It's a candidate *generator*, not a ranking — the biggest sellers appear once or twice at that sample size, so the script resolves every name against `/users/<name>` for the true inventory size. This is how `LIVINGISEASYNJ` (146k listings, third-largest US seller) was found after guessing missed it.

**Most of the marketplace is not US.** Of 54 sellers sampled, only **8 shipped from the US** — against UK 16, Germany 6, Spain 5, Japan 4, Netherlands 2, Sweden 2, France 2, Canada 2, and one each from Denmark, Ireland, Italy, Greece, Brazil, Portugal, Ukraine. **A random Discogs listing is only ~15% likely to be US**, which is why `--country US` matters on the eBay side and why the `/marketplace/stats` floor skews cheap-but-foreign.

The largest CD sellers are European and therefore out of scope for shipping: **recordsale-de** (Berlin, **1,338,208** listings) is 5.4× the biggest US seller. Also large: KUPIKU-COM (Japan, 474k), Lot.Of.Music (Netherlands, 321k), RecordCityDubStoreUK (204k), echogrove (Japan, 173k), www.hhv.de (154k). Worth knowing when something is unobtainable domestically.

### Does size predict hits?

Loosely, and only within the right inventory shape: 250k listings → 6 albums, 146k → 2, 99k → 4, 46k → 6, 15k of the wrong kind → 0. But **`devman242` at 1% CD held the best copy of a gap album on two consecutive scans**, and `CD_WAREHOUSE_817` at ~19% CD tied the best hit rate in the registry.

**And `Abandon_Ark` breaks the pattern outright: 2,017 listings → 5 albums** on a 35-entry wantlist (2026-08-21). That is a hit rate per listing about 100× bordentownrecords' at 1/124th the size. The inventory is 71% CD and entirely mainstream catalogue — no vinyl business, no deep backstock. **Size is close to worthless as a predictor once shape is right**, so never skip a small seller on listing count alone.

So size and shape predict hit *rate*, never whether a specific album is present. **A big wantlist gap justifies scanning a seller the screen would otherwise skip.**

### Ask Rian who he's already bought from — it beats both scripts

`dailybookstore` (32,281 listings, 100% across 11,959 ratings, 59% CD, US, and **$5.00 for 1–5 CDs then +$0.25**) was missed by 146 guessed names *and* by marketplace sampling. It surfaced on 2026-08-15 only because Rian mentioned he'd ordered there before.

Order history is a pre-filtered candidate list — a seller he's bought from has already cleared shipping, condition accuracy and communication, none of which any API field reports. **Ask before probing**, then confirm size and rating with one `GET /users/{name}` call.

### Screening a candidate before a full scan

- **Read `ships_from` off sampled listings, never the profile `location` field** — it's free text and often blank or wrong. `BagelRecords` shows a blank location and ships from the Netherlands.
- **CD share screens out vinyl shops.** Under ~15% CD means a vinyl business listing a few discs: MUSICMKT 12%, academyrecords 13%, mightyvinyl 3%, audiophileusa 0%. All scored zero wantlist hits.
- **Never reject on control-album queries.** Querying a handful of specific mainstream albums and rejecting sellers that lack them **would have rejected `bordentownrecords`**, the best seller in the registry, because its 6 hits were six other albums. That test also scored `LIVINGISEASYNJ` as "skip" and `devman242` as "marginal" — both then produced real hits on a full scan, including the best *Nevermind* found anywhere. Any control set cheap enough to run is too narrow to reject on.

Screen on format mix and origin, then **run the full scan** — it's ~35 calls and it's the only decisive test. And note that `devman242`, at 1% CD, held the best copy of a gap album: shape predicts hit *rate*, not whether a specific album is present.

## New-retail as a third venue — narrow, but real

eBay and Discogs are both **used** markets. A new-CD retailer is a different shape, and it wins in exactly one case: **a recent album whose current pressing is the only pressing.**

Tested 2026-08-16 on `deepdiscount.com` (Alliance Entertainment): Slowdive *Everything Is Alive* at **$13.65 new, in stock**, against a $24.53 Discogs floor and no US eBay listing at all. Free shipping over $25.

**A full 29-album sweep on 2026-08-16 found 6 worth buying, 5 of them on the exact wantlisted barcode.** Full per-album results: [[deepdiscount]].

**The UPC is the last path segment of the product URL** — `deepdiscount.com/<slug>/<upc>` — so it is readable straight off the search results page with no product-page visit. Compare it against the wantlisted release's barcode, which is already cached in `~/.cache/cd-bundles/releases.json` because the eBay half of this skill searches by barcode. A match means it *is* the wanted pressing, by the same logic `--cheapest` already relies on.

**"Reissue" does not mean "remastered", and a different UPC is not a remaster.** An earlier version of this section claimed new retail was structurally wrong for a used-market wantlist; Rian pushed back and the barcode data disproved it. The hard line is the `Remastered` tag (see `finding-original-cds`), and 3 of the differing-UPC hits carried no such tag on **any** release sharing the barcode. Check, don't assume.

**When resolving a UPC on Discogs, read every release sharing that barcode, not `results[0]`.** The top hit for *Dummy*'s barcode is a Russian unofficial pressing and for *Nevermind* a Brazilian one — judging on the first result would have been badly wrong in both directions.

Still true: a catalogue title whose catalog number *differs* from the wantlisted original deserves scepticism even with no remaster tag, because Discogs tags are user-submitted and a new catalog number is the classic remaster tell. Absence of a tag is the absence of a claim.

### It needs a browser, not a fetcher

`deepdiscount.com` is behind **Cloudflare Bot Management** — every path including the homepage returns `403` with a 12-byte body and sets `__cf_bm`. Both curl-with-a-browser-UA and WebFetch get the same 403. **The `claude-in-chrome` skill works**, because it drives a real Chrome session.

- Search URL is `https://www.deepdiscount.com/search?q=<query>&mod=AP`. **Not** `/catalogsearch/result/?q=` — that's the Magento default and it 404s here.
- Search results show title, format and price but **no catalog number or UPC**, so pressing identity needs the product page — which is the whole question for this wantlist.
- **Filter to CD rows** (`/\bCD (List )?Price:/`). Without it, t-shirts, jigsaws and socks flood the result and truncate the useful rows.
- Don't wire this into the scan pipeline. Driving a browser across 30+ albums is slow and breaks on markup changes; use it for one-off checks on recent albums.

## Related

- Skill `finding-original-cds` — which pressing to want in the first place, and the matrix-runout check for confirming a master. This skill assumes that one has already run.
- [[seller-registry]] — **who to scan and what shipping costs.** Durable reference, rewritten in place. Read it before scanning; update it when a seller's policy or standing changes.
- [[discogs-scan-results]] — **current hits, baskets and what to buy.** Living document, *overwritten* each run, never appended. Write results here, not into the registry.

  **Every seller name in that file must be a link**, and every buy row must carry its listing link — the file exists to be acted on, and an unlinked username means opening Discogs and typing it in. `seller-scan.mjs` already prints `https://www.discogs.com/sell/item/<id>` per listing; the seller profile is `https://www.discogs.com/seller/<name>/profile`. Link once per seller (the heading), not three times on the same page.
- [[discogs-original-cd-finder]] — the human-readable version of the pressing playbook, for when Rian wants to eyeball the rules himself.

**Keep those two files apart.** They were one file until 2026-08-16 and it rotted: seller notes became append-only logs where durable facts (who a seller is, what shipping costs) were interleaved with dated state (this cart, that basket), so a single seller took five stacked paragraphs across three dates to read, and nothing stale ever got deleted — it just got another paragraph underneath. **Durable facts go in the registry and get rewritten; dated state goes in scan-results and gets overwritten; mechanics go here.**
