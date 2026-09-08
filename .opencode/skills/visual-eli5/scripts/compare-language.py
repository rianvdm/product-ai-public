#!/usr/bin/env python3
"""Compare a visual-eli5 page's visual language with pages already on the site.

    python3 compare-language.py NEW.html EXISTING.html [EXISTING.html ...]

For each page it extracts four traits: the page ground (body background), the
headline face (h1 font-family, classed as grotesque, geometric, humanist, serif,
slab, or mono), the accent (the most-used saturated colour in CSS and SVG), and
the column width (main max-width). The new page passes when at least two of the
four differ from every existing page; otherwise it prints which page it matches
and exits 1. Standard library only.
"""

from __future__ import annotations

import colorsys
import re
import sys
from collections import Counter
from pathlib import Path

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b")
FACE_CLASSES = {
    "grotesque": ("-apple-system", "blinkmacsystemfont", "system-ui", "helvetica", "arial", "inter", "segoe", "roboto", "san francisco", "sf pro", "ui-sans-serif", "sans-serif"),
    "geometric": ("futura", "avenir", "gill sans", "century gothic", "montserrat", "poppins", "avant garde"),
    "humanist": ("verdana", "optima", "trebuchet", "tahoma", "lucida grande", "calibri", "source sans", "open sans", "seravek"),
    "serif": ("georgia", "times", "palatino", "iowan", "charter", "baskerville", "garamond", "didot", "bodoni", "hoefler", "cambria", "ui-serif", "serif", "new york"),
    "slab": ("rockwell", "courier prime", "clarendon", "zilla", "roboto slab"),
    "mono": ("menlo", "monaco", "courier", "sf mono", "consolas", "ui-monospace", "monospace", "jetbrains"),
}


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def normalise_hex(value: str) -> str:
    r, g, b = hex_to_rgb(value)
    return f"#{r:02x}{g:02x}{b:02x}"


def resolve_vars(value: str, variables: dict[str, str]) -> str:
    for _ in range(5):
        new = re.sub(r"var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)", lambda m: variables.get(m.group(1), m.group(0)), value)
        if new == value:
            break
        value = new
    return value


def css_variables(css: str) -> dict[str, str]:
    variables: dict[str, str] = {}
    for block in re.finditer(r":root\s*\{([^}]*)\}", css):
        for name, val in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", block.group(1)):
            variables.setdefault(name.strip(), val.strip())
    return variables


def declaration(css: str, selector_re: str, prop: str, variables: dict[str, str]) -> str | None:
    for match in re.finditer(r"([^{}]+)\{([^}]*)\}", css):
        selectors = [part.strip() for part in match.group(1).split(",")]
        if not any(re.fullmatch(selector_re, s) for s in selectors):
            continue
        found = re.search(rf"(?:^|;)\s*{re.escape(prop)}\s*:\s*([^;]+)", match.group(2))
        if found:
            return resolve_vars(found.group(1).strip(), variables)
    return None


def first_hex(value: str | None) -> str | None:
    if not value:
        return None
    match = HEX_RE.search(value)
    return normalise_hex(match.group(0)) if match else None


def face_class(font_family: str | None) -> str:
    if not font_family:
        return "unknown"
    families = [f.strip().strip("'\"").lower() for f in font_family.split(",")]
    for family in families:
        for cls, names in FACE_CLASSES.items():
            if any(family.startswith(name) or name == family for name in names):
                return cls
    return "unknown"


def saturation(hex_value: str) -> float:
    r, g, b = (c / 255 for c in hex_to_rgb(hex_value))
    return colorsys.rgb_to_hsv(r, g, b)[1]


def hue(hex_value: str) -> float:
    r, g, b = (c / 255 for c in hex_to_rgb(hex_value))
    return colorsys.rgb_to_hsv(r, g, b)[0] * 360


def accent(source: str, variables: dict[str, str]) -> str | None:
    text = resolve_vars(source, variables)
    counts: Counter[str] = Counter()
    for match in HEX_RE.finditer(text):
        value = normalise_hex(match.group(0))
        if saturation(value) >= 0.45:
            counts[value] += 1
    return counts.most_common(1)[0][0] if counts else None


def traits(path: Path) -> dict[str, str | None]:
    source = path.read_text(encoding="utf-8")
    css = "\n".join(m.group(1) for m in re.finditer(r"<style[^>]*>(.*?)</style>", source, flags=re.S))
    variables = css_variables(css)
    ground = first_hex(declaration(css, r"(?:html,\s*)?body|html", "background", variables)) or first_hex(
        declaration(css, r"(?:html,\s*)?body|html", "background-color", variables)
    )
    face = declaration(css, r"h1", "font-family", variables) or declaration(css, r"(?:html,\s*)?body|html", "font-family", variables)
    width = declaration(css, r"main|\.page|\.wrap|\.container", "max-width", variables)
    return {"ground": ground, "face": face_class(face), "accent": accent(source, variables), "width": width}


def same_colour(a: str | None, b: str | None, tolerance: int = 28) -> bool:
    if not a or not b:
        return a == b
    return max(abs(x - y) for x, y in zip(hex_to_rgb(a), hex_to_rgb(b))) <= tolerance


def same_accent(a: str | None, b: str | None) -> bool:
    if not a or not b:
        return a == b
    diff = abs(hue(a) - hue(b))
    return min(diff, 360 - diff) <= 20


def differences(new: dict[str, str | None], old: dict[str, str | None]) -> list[str]:
    diff = []
    if not same_colour(new["ground"], old["ground"]):
        diff.append("ground")
    if new["face"] != old["face"]:
        diff.append("face")
    if not same_accent(new["accent"], old["accent"]):
        diff.append("accent")
    if (new["width"] or "").replace(" ", "") != (old["width"] or "").replace(" ", ""):
        diff.append("width")
    return diff


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    pages = [Path(p) for p in argv[1:]]
    rows = [(page, traits(page)) for page in pages]
    print(f"{'page':40} {'ground':9} {'face':10} {'accent':9} width")
    for page, t in rows:
        print(f"{str(page)[-40:]:40} {t['ground'] or '-':9} {t['face']:10} {t['accent'] or '-':9} {t['width'] or '-'}")
    new_page, new = rows[0]
    status = 0
    for page, old in rows[1:]:
        if page.resolve() == new_page.resolve():
            continue
        diff = differences(new, old)
        verdict = "OK" if len(diff) >= 2 else "SAME HOUSE"
        if len(diff) < 2:
            status = 1
        print(f"{verdict}: vs {page} differs in {', '.join(diff) or 'nothing'}")
    return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
