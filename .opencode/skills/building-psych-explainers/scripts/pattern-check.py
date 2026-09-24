#!/usr/bin/env python3
"""Measure an explainer page for brevity and against the countable rules in
avoid-ai-patterns.md.

Usage:  python3 pattern-check.py public/<slug>/index.html
        python3 pattern-check.py --prose public/<slug>/index.html

Brevity comes first because it is the brief: big pictures, few words. The budgets
are the polyvagal page's numbers with a little room. Then the pattern rules.

--prose prints the visible prose in page order instead -- headings, ledes, slabs,
steps, list items, SVG labels, quotes -- with figures marked and the sources section
dropped. It is the input to the newbie pass and the voice pass, which are reads, not
counts.

Counts only what can honestly be counted. The judgement calls -- coaching register,
metaphors run into the ground, rule-of-three pile-ups -- still need a human read of
01-context/avoid-ai-patterns.md.

Two deliberate scoping choices:

* Quoted material is excluded from the totals. The originator's own sentences are
  not the page author's style, and counting them punishes the page for quoting,
  which the pattern file explicitly rewards.
* Only unambiguously contrastive carriers count against the negation budget. A bare
  "is not" or "none of" is often a plain negation ("none of it is your fault"), and
  a check that cries wolf gets ignored. Those are listed for a human to judge.
"""

import html
import re
import sys
from pathlib import Path

EM = "—"
NEGATION_BUDGET_PER_WORDS = 600  # avoid-ai-patterns.md: >1 per 600 words is a template
MAX_PROSE_EM_DASHES = 3

# Carriers that are contrastive by construction -- these count.
CONTRASTIVE = [
    (r", not ", '", not"'),
    (r"\binstead of\b", '"instead of"'),
    (r"\brather than\b", '"rather than"'),
    (r"\bnot only\b", '"not only"'),
    (r"\bless about\b", '"less about"'),
    (r"\bnot because\b", '"not because"'),
]

# Plain negations. Contrastive ONLY when an affirmative restatement follows
# ("Shutting down is not a failure of will. It is the oldest protection you own").
# Too noisy to count; shown so a human can decide.
AMBIGUOUS = [
    (r"\b(?:is|are|was|were)\s+not\b", "is/are not"),
    (r"\bnone of\b", "none of"),
]

# A different family from negation-contrast, and never a pass/fail here -- some of
# these are the only honest way to say the thing. What matters is the rate: a page
# that keeps reaching for them describes its subject by what is absent. Measured on
# brainspotting, 1 per 60 words read as a tic and 1 per 79 read fine.
PLAIN_NEGATION = ["no", "not", "nobody", "never", "nothing", "none", "cannot", "rarely", "without"]
NEGATION_WORDS_PER_CARRIER = 70

# Ten of eleven headings inside a 4-9 word band was the strongest machine-cadence
# signal an editor pass found on a page this script had passed clean. Report the
# spread; a human decides whether the sameness is deliberate.
HEADING_BAND = 4

# Brevity. The brief is big pictures and few words, and this is the check that
# holds it. Budgets are taken from the polyvagal page, which is the reference: it
# passes every one of them with a little room, and the first brainspotting draft
# (616 paragraph words, 17 words a sentence, a 108-word opener, a 154-word caveat)
# fails four. "Paragraph" means <p class="lede"> and the hero's <p class="sub">;
# everything else the reader scans rather than reads -- slabs, lists, big facts.
# The share of prose in paragraphs is reported but not budgeted: it was 49% vs 55%
# on those two pages, too close to tell them apart.
MAX_PARAGRAPH_WORDS = 500          # polyvagal 452, brainspotting draft 617
MAX_WORDS_PER_SENTENCE = 12        # polyvagal 8.5, brainspotting draft 16.7
MAX_PARAGRAPH_LENGTH = 40          # polyvagal 36, brainspotting draft 59
MAX_SECTION_PARAGRAPH_WORDS = 65   # polyvagal 57, brainspotting draft 108
MAX_CAVEAT_WORDS = 80              # polyvagal 40, brainspotting draft 154


def paragraph_words(markup: str) -> list[int]:
    """Word count of each lede/sub paragraph in a chunk of markup."""
    paras = re.findall(r'<p class="(?:lede|sub)"[^>]*>(.*?)</p>', markup, flags=re.S)
    return [len(strip_to_prose(p).split()) for p in paras]


def sentence_count(markup: str) -> int:
    text = " ".join(strip_to_prose(p) for p in
                    re.findall(r'<p class="(?:lede|sub)"[^>]*>(.*?)</p>', markup, flags=re.S))
    return len(re.findall(r"[.!?](?:\s|$)", text))


def strip_to_prose(markup: str) -> str:
    markup = re.sub(r"<svg.*?</svg>", " ", markup, flags=re.S)
    markup = re.sub(r"<!--.*?-->", " ", markup, flags=re.S)
    markup = re.sub(r"<[^>]+>", " ", markup)
    return re.sub(r"\s+", " ", html.unescape(markup)).strip()


def context(text: str, match: re.Match, width: int = 46) -> str:
    lo = max(0, match.start() - width)
    hi = min(len(text), match.end() + width)
    return ("..." if lo else "") + text[lo:hi].strip() + ("..." if hi < len(text) else "")


def visible_prose(body: str) -> str:
    """The page as a cold reader meets it: one line per element, figures marked,
    SVG labels kept, sources dropped."""
    body = re.sub(r'<section[^>]*class="[^"]*sources[^"]*".*?</section>', "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)

    def figure(m: re.Match) -> str:
        labels = re.findall(r"<text[^>]*>(.*?)</text>", m.group(0), flags=re.S)
        labels = [html.unescape(re.sub(r"<[^>]+>", "", l)).strip() for l in labels]
        return "\n[figure: " + " / ".join(l for l in labels if l) + "]\n"

    body = re.sub(r"<svg.*?</svg>", figure, body, flags=re.S)
    body = re.sub(r"<br\s*/?>", " ", body)
    body = re.sub(r"</(?:p|h\d|li|strong|span)>", "\n", body)
    body = re.sub(r"<[^>]+>", "", body)
    lines = [re.sub(r"\s+", " ", html.unescape(l)).strip() for l in body.splitlines()]
    return "\n".join(l for l in lines if l)


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--prose"]
    want_prose = "--prose" in sys.argv
    if len(args) != 1:
        print(__doc__)
        return 2

    path = Path(args[0])
    if not path.is_file():
        print(f"error: no such file: {path}")
        return 2

    src = path.read_text(encoding="utf-8")
    if "<body>" not in src:
        print("error: no <body> found -- is this an explainer page?")
        return 2
    body = src.split("<body>", 1)[1].split("</body>")[0]

    if want_prose:
        print(visible_prose(body))
        return 0

    # The sources list uses an em dash as a separator in every item. That is list
    # formatting, not prose habit, so it is reported apart from the running text.
    sources = "".join(
        re.findall(r'<section[^>]*class="[^"]*sources[^"]*".*?</section>', body, flags=re.S)
    )
    running = body.replace(sources, " ") if sources else body

    all_prose = strip_to_prose(body)
    prose = strip_to_prose(running)

    quotes = re.findall(r"“[^”]*”", prose)
    own = prose
    for q in quotes:
        own = own.replace(q, " ")
    own = re.sub(r"\s+", " ", own).strip()

    words = len(own.split())
    budget = round(words / NEGATION_BUDGET_PER_WORDS)
    fails = []

    print(f"\n{path}")
    print(f"  own prose, quotes excluded ........ {words} words")
    print(f"  attributed quotes ................. {len(quotes)}")
    if len(quotes) < 3:
        fails.append("fewer than 3 attributed quotes -- named voices are required")

    # --- brevity -------------------------------------------------------------
    print("\n  brevity (big pictures, few words)")
    sections = re.findall(r"<section[^>]*>.*?</section>", running, flags=re.S)
    per_section = []
    for sec in sections:
        eyebrow = re.search(r'class="eyebrow">(.*?)</p>', sec, flags=re.S)
        label = strip_to_prose(eyebrow.group(1)) if eyebrow else "hero"
        label = re.sub(r"^\d+\s*/\s*", "", label)
        per_section.append((label, sum(paragraph_words(sec))))
    para_lengths = paragraph_words(running)
    para_total = sum(para_lengths)
    share = para_total / words if words else 0
    sentences = sentence_count(running)
    wps = para_total / sentences if sentences else 0
    longest = max(para_lengths) if para_lengths else 0
    caveat = re.search(r'<p class="caveat">(.*?)</p>', sources, flags=re.S)
    caveat_words = len(strip_to_prose(caveat.group(1)).split()) if caveat else 0

    print(f"      paragraph words ............ {para_total} of {words} own "
          f"(budget {MAX_PARAGRAPH_WORDS}; {share:.0%} in paragraphs, reported only)")
    print(f"      words per sentence ......... {wps:.1f} (budget {MAX_WORDS_PER_SENTENCE})")
    print(f"      longest paragraph .......... {longest} words (budget {MAX_PARAGRAPH_LENGTH})")
    print(f"      caveat ..................... {caveat_words} words (budget {MAX_CAVEAT_WORDS})")
    heavy = [(l, n) for l, n in per_section if n > MAX_SECTION_PARAGRAPH_WORDS]
    print(f"      paragraph words by section . "
          + ", ".join(f"{l} {n}" for l, n in per_section))
    if para_total > MAX_PARAGRAPH_WORDS:
        fails.append(f"{para_total} paragraph words against a budget of {MAX_PARAGRAPH_WORDS} -- cut, "
                     "or move the point into a slab, list or big fact")
    if wps > MAX_WORDS_PER_SENTENCE:
        fails.append(f"{wps:.1f} words a sentence against a budget of {MAX_WORDS_PER_SENTENCE} -- "
                     "split them; a subordinate clause is a second sentence")
    if longest > MAX_PARAGRAPH_LENGTH:
        fails.append(f"a {longest}-word paragraph against a budget of {MAX_PARAGRAPH_LENGTH}")
    for label, n in heavy:
        fails.append(f"section '{label}' carries {n} paragraph words against a budget of "
                     f"{MAX_SECTION_PARAGRAPH_WORDS} -- a headline and two short lines, then a picture")
    if caveat_words > MAX_CAVEAT_WORDS:
        fails.append(f"a {caveat_words}-word caveat against a budget of {MAX_CAVEAT_WORDS} -- "
                     "name the strongest study and the strongest objection, link the rest")

    print(f"\n  negation-contrast (budget {budget})")
    counted = 0
    for pattern, label in CONTRASTIVE:
        for m in re.finditer(pattern, own, flags=re.I):
            counted += 1
            print(f"      {label:14} {context(own, m)}")
    if not counted:
        print("      none")
    print(f"      counted {counted} against budget of {budget}")
    if counted > budget:
        fails.append(
            f"{counted} negation-contrasts against a budget of {budget} -- keep only the "
            "ones correcting a misreading, make the rest positive"
        )

    amb = [(lbl, m) for pat, lbl in AMBIGUOUS for m in re.finditer(pat, own, flags=re.I)]
    if amb:
        print(f"\n  plain negations -- contrastive only if an affirmative follows")
        for label, m in amb:
            print(f"      {label:14} {context(own, m)}")

    # Reported, never failed. Rate is the signal, not any single word.
    tally = {w: len(re.findall(rf"\b{w}\b", own, flags=re.I)) for w in PLAIN_NEGATION}
    carriers = sum(tally.values())
    print("\n  plain-negation rate (reported, not a budget)")
    print("      " + "  ".join(f"{w} {n}" for w, n in tally.items() if n) or "      none")
    if carriers:
        rate = words // carriers
        note = "dense -- the page may be describing itself by what is absent" \
            if rate < NEGATION_WORDS_PER_CARRIER else "fine"
        print(f"      {carriers} carriers, 1 per {rate} words ({note})")

    heads = [
        html.unescape(re.sub(r"<[^>]+>", "", h)).split()
        for h in re.findall(r"<h2[^>]*>(.*?)</h2>", body, flags=re.S)
    ]
    lengths = [len(h) for h in heads]
    print("\n  h2 lengths (reported, not a budget)")
    if lengths:
        print(f"      {lengths}")
        band = [n for n in lengths if HEADING_BAND <= n <= HEADING_BAND + 5]
        if len(lengths) > 4 and len(lengths) - len(band) <= 1:
            print(f"      {len(band)} of {len(lengths)} in a {HEADING_BAND}-{HEADING_BAND + 5} word band")
            print("      -- a person writing this many headlines produces one that does not fit")
    else:
        print("      none")

    prose_em = own.count(EM)
    print(f"\n  em dashes in running prose ........ {prose_em}")
    print(f"  em dashes in the sources list ..... {all_prose.count(EM) - prose_em} (separators, fine)")
    if prose_em > MAX_PROSE_EM_DASHES:
        fails.append(
            f"{prose_em} em dashes in prose -- a live Claude tell; vary with commas, "
            "colons, parentheses"
        )

    print("\n  punctuation variety")
    for ch, name in ((",", "commas"), (";", "semicolons"), (":", "colons"), ("(", "parens")):
        print(f"      {name:12} {own.count(ch)}")
    if own.count("(") == 0 and own.count(";") == 0:
        fails.append("no parentheses and no semicolons -- punctuation starvation is its own tell")

    print()
    if fails:
        for f in fails:
            print(f"  OVER: {f}")
    else:
        print("  PASS on everything countable.")
    print("  Now read 01-context/avoid-ai-patterns.md for what cannot be counted.\n")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
