#!/usr/bin/env python3
"""List and inspect vinyl pressings of a Discogs master, for finding-original-vinyl.

Python 3.9+, stdlib only. Needs DISCOGS_TOKEN in the environment
(source ~/.config/ebay/credentials.env). Paces requests at ~1.1 s to stay
under Discogs' 60/min authenticated budget and stops on the first 429.

Usage:
  python3 vinyl-pressings.py master "The Cure Disintegration"
  python3 vinyl-pressings.py versions 31755
  python3 vinyl-pressings.py detail 1681869 1353673 2323894
  python3 vinyl-pressings.py reviews 750080 520824
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.discogs.com"
UA = "FindingOriginalVinyl/1.0"
PACE_SECONDS = 1.1

# Format descriptions that take a pressing out of the running before any
# per-release check. Promos stay in: same cut, they just cost more.
EXCLUDED = ("Unofficial Release", "Club Edition", "Picture Disc", "Test Pressing", "White Label")

# Club pressings are sometimes marked only in free text or notes, not in
# descriptions (German "Club-Sonderauflage", Columbia House/BMG licence lines).
CLUB_TEXT = re.compile(r"club|columbia house|bmg direct|record of the month", re.I)

# Credit roles that identify who mastered or cut the lacquer.
CUT_ROLES = ("Master", "Lacquer", "Cut", "Remaster", "Mix")

_last_call = 0.0


def get(path):
    """GET an API path with pacing; exit on 429 rather than retry."""
    global _last_call
    token = os.environ.get("DISCOGS_TOKEN")
    if not token:
        sys.exit("DISCOGS_TOKEN is not set: source ~/.config/ebay/credentials.env first")
    wait = PACE_SECONDS - (time.time() - _last_call)
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(
        API + path, headers={"User-Agent": UA, "Authorization": f"Discogs token={token}"}
    )
    _last_call = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        if err.code == 429:
            sys.exit("429 from Discogs: stop here, wait a minute, and do not loop on retries")
        if err.code == 404:
            return None
        raise


def cmd_master(query):
    q = urllib.parse.quote_plus(query)
    for r in get(f"/database/search?q={q}&type=master&per_page=8")["results"]:
        print(f"{r['id']}\t{r['title']}\t{r.get('year', '')}")


def cmd_versions(master_id):
    rows, page = [], 1
    while True:
        d = get(f"/masters/{master_id}/versions?format=Vinyl&per_page=100&page={page}")
        rows += d["versions"]
        if page >= d["pagination"]["pages"]:
            break
        page += 1
    kept = [r for r in rows if not any(x in r["format"] for x in EXCLUDED)]
    print(f"{len(rows)} vinyl versions; {len(rows) - len(kept)} excluded ({', '.join(EXCLUDED)})")
    unofficial = [str(r["id"]) for r in rows if "Unofficial Release" in r["format"]]
    if unofficial:
        print(f"unofficial (check runouts for replicas of a pick): {' '.join(unofficial)}")
    print("id\tcountry\tyear\tlabel\tcatno\tformat\thave\twant")
    for r in sorted(kept, key=lambda r: -r["stats"]["community"]["in_collection"]):
        c = r["stats"]["community"]
        print(
            f"{r['id']}\t{r['country']}\t{r.get('released', '')}\t{r['label']}\t{r['catno']}"
            f"\t{r['format']}\t{c['in_collection']}\t{c['in_wantlist']}"
        )


def side_lengths(tracklist):
    """Sum track durations per side letter (A1, B2, ...). Empty if durations are missing."""
    sides = {}
    for t in tracklist:
        m = re.match(r"([A-Z])", t.get("position", ""))
        dur = re.fullmatch(r"(\d+):(\d\d)", t.get("duration", ""))
        if t.get("type_") == "track" and m and dur:
            sides[m.group(1)] = sides.get(m.group(1), 0) + int(dur.group(1)) * 60 + int(dur.group(2))
    return " ".join(f"{k}={v // 60}:{v % 60:02d}" for k, v in sorted(sides.items()))


def print_reviews(rid):
    rv = (get(f"/releases/{rid}/reviews?per_page=100") or {}).get("results", [])
    print(f"   reviews: {len(rv)}")
    for x in rv:
        print(f"    - [{x['date_added'][:10]}] {x['review_plaintext'].replace(chr(10), ' ')[:1500]}")


def cmd_reviews(ids):
    for rid in ids:
        print(f"\n## {rid}")
        print_reviews(rid)


def cmd_detail(ids, reviews):
    for rid in ids:
        r = get(f"/releases/{rid}")
        if r is None:
            print(f"\n## {rid}: not found")
            continue
        s = get(f"/marketplace/stats/{rid}?curr_abbr=USD") or {}
        p = get(f"/marketplace/price_suggestions/{rid}") or {}
        fmt = "; ".join(
            f"{f['qty']}x{f['name']}:{'/'.join(f.get('descriptions', []))}"
            + (f" [{f['text']}]" if f.get("text") else "")
            for f in r["formats"]
        )
        c = r["community"]
        low = (s.get("lowest_price") or {}).get("value")
        sugg = {k.split("(")[-1].rstrip(")"): round(v["value"]) for k, v in p.items()}
        tracks = [t for t in r["tracklist"] if t.get("type_") == "track"]
        print(f"\n## {rid} {r.get('country')} {r.get('year')} | {fmt}")
        print(f"   catno: {', '.join(l['catno'] for l in r['labels'])}")
        print(f"   have {c['have']} want {c['want']} | rating {c['rating']['average']} ({c['rating']['count']})")
        print(
            f"   for sale {s.get('num_for_sale')} | floor ${low} | blocked {s.get('blocked_from_sale')}"
            f" | VG+ ${sugg.get('VG+')} NM ${sugg.get('NM or M-')}"
        )
        print(f"   tracks {len(tracks)} | sides {side_lengths(tracks) or 'durations missing'}")
        credits = [f"{e['role']}: {e['name']}" for e in r.get("extraartists", []) if any(x in e["role"] for x in CUT_ROLES)]
        print(f"   credits: {'; '.join(credits) or 'none'}")
        runouts = [i.get("value") for i in r.get("identifiers", []) if i["type"] == "Matrix / Runout"]
        print(f"   runouts: {' | '.join(runouts[:4]) or 'none'}")
        notes = (r.get("notes") or "").replace("\n", " ")
        phono = sorted(set(re.findall(r"℗\s*(?:&\s*©\s*)?((?:19|20)\d\d)", notes)))
        print(f"   ℗ years in notes: {', '.join(phono) or 'none'}")
        print(f"   notes: {notes[:300]}")
        free_text = " ".join(f.get("text", "") for f in r["formats"]) + " " + notes
        if CLUB_TEXT.search(free_text):
            print(f"   CLUB? free text or notes mention: {CLUB_TEXT.search(free_text).group(0)}")
        if reviews:
            print_reviews(rid)


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd, args = argv[1], argv[2:]
    if cmd == "master" and args:
        cmd_master(" ".join(args))
    elif cmd == "versions" and len(args) == 1:
        cmd_versions(args[0])
    elif cmd == "reviews" and args:
        cmd_reviews(args)
    elif cmd == "detail" and args:
        reviews = "--reviews" in args
        cmd_detail([a for a in args if a != "--reviews"], reviews)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
