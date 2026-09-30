#!/usr/bin/env python3
"""Render a tailored resume from Markdown to a print-ready PDF via headless Chrome.

Python 3.9+. Needs `pip install markdown pypdf` and Google Chrome (or Chromium).

Usage:
    python render_resume.py tailored/2026-10-01-acme-vp-product.md
    python render_resume.py resume.md -o out.pdf --chrome /usr/bin/chromium
"""
import argparse
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

import markdown
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
CSS_PATH = HERE / "resume.css"
DEFAULT_CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
MAX_PAGES = 2

_FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


class RenderError(Exception):
    """A failure the user can act on; the CLI prints it without a traceback."""


def strip_frontmatter(md_text: str) -> str:
    """Drop a leading YAML block (tailored resumes keep posting metadata there)."""
    return _FRONTMATTER.sub("", md_text, count=1)


def build_html(md_text: str, title: str) -> str:
    body = markdown.markdown(md_text, extensions=["extra", "sane_lists"])
    # The HTML is written to a temp dir, so point relative URLs (e.g. a fonts/ folder) back here.
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<base href="{HERE.as_uri()}/">'
        f"<title>{html.escape(title)}</title>"
        f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>"
        f"</head><body>{body}</body></html>"
    )


def render_pdf(
    md_path: Path,
    pdf_path: Optional[Path] = None,
    chrome: Path = DEFAULT_CHROME,
    timeout: float = 60,
) -> Path:
    md_path = Path(md_path)
    if not md_path.is_file():
        raise RenderError(f"Input file not found: {md_path}")
    if not chrome.exists():
        raise RenderError(f"Chrome not found at {chrome}")
    pdf_path = Path(pdf_path) if pdf_path else md_path.with_suffix(".pdf")
    # Remove any previous render so a silent Chrome failure can't pass off the old PDF as new.
    if pdf_path.exists():
        pdf_path.unlink()

    md_text = strip_frontmatter(md_path.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        html_file = Path(tmp) / "resume.html"
        html_file.write_text(build_html(md_text, md_path.stem), encoding="utf-8")
        try:
            result = subprocess.run(
                [
                    str(chrome), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", html_file.as_uri(),
                ],
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            raise RenderError(f"Chrome timed out after {timeout:g}s rendering {md_path}") from None
        except OSError as err:
            raise RenderError(f"Could not run Chrome at {chrome}: {err.strerror}") from None
    if result.returncode != 0 or not pdf_path.is_file():
        raise RenderError(f"Chrome failed to write {pdf_path}: {result.stderr.strip()[-500:]}")
    return pdf_path


def page_count(pdf_path: Path) -> int:
    return len(PdfReader(str(pdf_path)).pages)


def _page_fonts(pdf_path: Path):
    for page in PdfReader(str(pdf_path)).pages:
        resources = page.get("/Resources")
        fonts = resources.get_object().get("/Font") if resources else None
        for font in (fonts.get_object().values() if fonts else []):
            yield font.get_object()


def embedded_fonts(pdf_path: Path) -> set:
    """Font family names embedded in the PDF (subset prefixes like ABCDEF+ removed)."""
    names = set()
    for font in _page_fonts(pdf_path):
        descriptor = font.get("/FontDescriptor")
        family = descriptor.get_object().get("/FontFamily") if descriptor else None
        name = str(family or font.get("/BaseFont", "")).lstrip("/")
        names.add(name.split("+", 1)[-1])
    return names


def link_targets(pdf_path: Path) -> set:
    """URIs of clickable link annotations in the PDF."""
    targets = set()
    for page in PdfReader(str(pdf_path)).pages:
        for annot in page.get("/Annots") or []:
            action = annot.get_object().get("/A")
            uri = action.get_object().get("/URI") if action else None
            if uri:
                targets.add(str(uri))
    return targets


def font_subtypes(pdf_path: Path) -> set:
    return {str(font.get("/Subtype")) for font in _page_fonts(pdf_path)}


def extract_text(pdf_path: Path) -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("markdown_file", type=Path)
    parser.add_argument("-o", "--output", type=Path, help="PDF path (default: next to the source)")
    parser.add_argument("--chrome", type=Path, default=DEFAULT_CHROME, help=f"Chrome binary (default: {DEFAULT_CHROME})")
    args = parser.parse_args(argv)
    try:
        pdf = render_pdf(args.markdown_file, args.output, chrome=args.chrome)
    except RenderError as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    pages = page_count(pdf)
    print(f"Wrote {pdf} ({pages} page{'s' if pages != 1 else ''})")
    if pages > MAX_PAGES:
        print(f"WARNING: {pages} pages; the guidelines cap resumes at {MAX_PAGES}.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
