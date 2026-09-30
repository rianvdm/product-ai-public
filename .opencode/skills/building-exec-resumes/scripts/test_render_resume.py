"""Tests for render_resume. Run from this folder: python -m unittest test_render_resume.py"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_resume  # noqa: E402

SAMPLE = """---
company: Example Co
posting: https://example.com/jobs/1
---

# Test Person

Springfield · test@example.com

## Experience

### Example Co · VP Product (2024 – present)

- Grew ARR 7× at Example Co; kept NPS at 78 during the change.
- Worked with “quoted” partners in Kaapstad and Zürich.
"""

LONG = "# Long\n\n" + "\n".join(f"- Filler bullet number {i} with enough words to wrap across the page width." for i in range(400))


class StripFrontmatterTest(unittest.TestCase):
    def test_removes_leading_yaml_block(self):
        out = render_resume.strip_frontmatter(SAMPLE)
        self.assertNotIn("posting:", out)
        self.assertTrue(out.lstrip().startswith("# Test Person"))

    def test_leaves_text_without_frontmatter_alone(self):
        self.assertEqual(render_resume.strip_frontmatter("# Hi\n"), "# Hi\n")


class BuildHtmlTest(unittest.TestCase):
    def test_inlines_css_and_renders_headings(self):
        html = render_resume.build_html("# Name\n\n## Experience\n", "Name")
        self.assertIn("<style>", html)
        self.assertIn("<h1>Name</h1>", html)
        self.assertIn('<meta charset="utf-8">', html)


class RenderPdfTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="resume test "))  # space on purpose

    def test_renders_selectable_text_without_frontmatter(self):
        src = self.tmp / "sample.md"
        src.write_text(SAMPLE, encoding="utf-8")
        pdf = render_resume.render_pdf(src)
        self.assertEqual(pdf, self.tmp / "sample.pdf")
        text = render_resume.extract_text(pdf)
        self.assertIn("Test Person", text)
        self.assertIn("Zürich", text)
        self.assertIn("7×", text)
        self.assertNotIn("posting:", text)
        self.assertLessEqual(render_resume.page_count(pdf), 2)

    def test_cli_warns_when_over_two_pages(self):
        src = self.tmp / "long.md"
        src.write_text(LONG, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(Path(render_resume.__file__)), str(src)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertRegex(result.stderr, r"WARNING: \d+ pages")

    def test_cli_missing_input_exits_1_with_message(self):
        result = subprocess.run(
            [sys.executable, str(Path(render_resume.__file__)), str(self.tmp / "nope.md")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("not found", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_embeds_fonts(self):
        src = self.tmp / "sample.md"
        src.write_text(SAMPLE, encoding="utf-8")
        pdf = render_resume.render_pdf(src)
        self.assertTrue(render_resume.embedded_fonts(pdf))

    def test_markdown_links_become_clickable(self):
        src = self.tmp / "links.md"
        src.write_text("# Name\n\n[example.com](https://example.com) · [me@example.com](mailto:me@example.com)\n", encoding="utf-8")
        pdf = render_resume.render_pdf(src)
        self.assertEqual(render_resume.link_targets(pdf), {"https://example.com/", "mailto:me@example.com"})

    def test_new_page_marker_starts_heading_on_next_page(self):
        src = self.tmp / "break.md"
        src.write_text("# Name\n\nShort first page.\n\n### Second Company {: .new-page }\n\n- Bullet.\n", encoding="utf-8")
        pdf = render_resume.render_pdf(src)
        self.assertEqual(render_resume.page_count(pdf), 2)
        from pypdf import PdfReader
        page2 = PdfReader(str(pdf)).pages[1].extract_text()
        self.assertIn("Second Company", page2)
        self.assertNotIn("{:", page2)

    def test_fonts_are_not_type3(self):
        # Type3 glyph procedures parse badly in some applicant tracking systems.
        src = self.tmp / "sample.md"
        src.write_text(SAMPLE, encoding="utf-8")
        pdf = render_resume.render_pdf(src)
        self.assertNotIn("/Type3", render_resume.font_subtypes(pdf))

    def _fake_chrome(self, body: str) -> Path:
        script = self.tmp / "fake-chrome"
        script.write_text(f"#!/bin/sh\n{body}\n")
        script.chmod(0o755)
        return script

    def test_stale_pdf_is_not_reported_as_fresh(self):
        src = self.tmp / "sample.md"
        src.write_text(SAMPLE, encoding="utf-8")
        (self.tmp / "sample.pdf").write_bytes(b"old render")
        silent_chrome = self._fake_chrome("exit 0")  # succeeds but writes nothing
        with self.assertRaisesRegex(render_resume.RenderError, "failed to write"):
            render_resume.render_pdf(src, chrome=silent_chrome)

    def test_chrome_hang_raises_readable_error(self):
        src = self.tmp / "sample.md"
        src.write_text(SAMPLE, encoding="utf-8")
        hanging_chrome = self._fake_chrome("sleep 5")
        with self.assertRaisesRegex(render_resume.RenderError, "timed out"):
            render_resume.render_pdf(src, chrome=hanging_chrome, timeout=1)

    def test_unexecutable_chrome_raises_readable_error(self):
        src = self.tmp / "sample.md"
        src.write_text(SAMPLE, encoding="utf-8")
        not_executable = self.tmp / "chrome-noexec"
        not_executable.write_text("#!/bin/sh\nexit 0\n")
        with self.assertRaisesRegex(render_resume.RenderError, "Could not run Chrome"):
            render_resume.render_pdf(src, chrome=not_executable)

    def test_missing_chrome_raises_readable_error(self):
        src = self.tmp / "sample.md"
        src.write_text(SAMPLE, encoding="utf-8")
        with self.assertRaisesRegex(render_resume.RenderError, "Chrome not found"):
            render_resume.render_pdf(src, chrome=Path("/nonexistent/chrome"))


if __name__ == "__main__":
    unittest.main()
