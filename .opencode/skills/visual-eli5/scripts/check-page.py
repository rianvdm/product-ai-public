#!/usr/bin/env python3
"""Static semantic checks for a visual-eli5 HTML page.

The checker deliberately uses only the Python standard library.  Later review
stages can build on the small DOM and report model here without needing a
browser or an HTML parsing dependency.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol, Sequence, TextIO


MAX_AVERAGE_SENTENCE_WORDS = 12
MAX_PARAGRAPH_WORDS = 40
MAX_SCENE_PARAGRAPH_WORDS = 65
MAX_CAPTION_WORDS = 20
MAX_CAPTION_SENTENCES = 2
MIN_RENDERED_TEXT_PX = 9.0
WORD_RE = re.compile(r"\b[\w]+(?:['’\-][\w]+)*\b", re.UNICODE)

_VOID_ELEMENTS = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)
_PROSE_TAGS = frozenset(
    {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "dt", "dd", "figcaption", "blockquote", "label", "button", "summary"}
)
_REMOTE_URL_RE = re.compile(r"^(?:https?:)?//", re.IGNORECASE)
_CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)([^'\")\s]+)\1\s*\)", re.IGNORECASE)
_LINK_DEPENDENCY_RELS = frozenset(
    {
        "apple-touch-icon",
        "apple-touch-icon-precomposed",
        "icon",
        "manifest",
        "mask-icon",
        "modulepreload",
        "prefetch",
        "prerender",
        "stylesheet",
    }
)


@dataclass
class TextNode:
    text: str


@dataclass
class DomNode:
    tag: str
    attrs: dict[str, str]
    children: list["DomNode | TextNode"]
    parent: "DomNode | None" = None


@dataclass
class Document:
    source: str
    root: DomNode
    has_doctype: bool


@dataclass
class Finding:
    code: str
    message: str
    severity: str  # error or report
    scope: str = "page"


@dataclass
class SceneMetrics:
    scene_id: str
    claim: str
    paragraph_words: int
    sentence_count: int
    average_sentence_words: float
    longest_paragraph_words: int


@dataclass
class ProseLine:
    text: str
    tag: str
    scene_id: str | None
    kind: str
    source_order: int


@dataclass
class MotionUse:
    kind: str
    source: str
    requires_reduced_motion: bool
    needs_reduced_capture: bool = True


@dataclass
class MotionInventory:
    uses: list[MotionUse]
    has_css_reduced_rule: bool
    has_script_reduced_query: bool
    initial_hidden: list[str]
    scroll_observer_present: bool
    reveal_pattern: bool
    reduced_motion_gaps: list[str] = field(default_factory=list)


@dataclass
class CssRule:
    selector: str
    declarations: dict[str, str]
    context: str = ""


@dataclass
class VisualProxy:
    kind: str
    count: int
    samples: list[str]
    scene_ids: list[str]
    message: str


@dataclass
class StaticReport:
    path: str | None
    errors: list[Finding]
    reports: list[Finding]
    scenes: list[SceneMetrics]
    authored_prose: list[ProseLine]
    motion: MotionInventory
    visual_proxies: list[VisualProxy]


@dataclass(frozen=True)
class Viewport:
    name: str
    width: int
    height: int


DESKTOP = Viewport("desktop", 1440, 1100)
PHONE = Viewport("phone", 390, 844)


@dataclass
class ViewportReport:
    viewport: Viewport
    reduced_motion: bool
    client_width: int
    scroll_width: int
    scene_bounds: list[dict[str, object]]
    horizontally_clipped_text: list[dict[str, object]]
    hidden_before_scroll: list[dict[str, object]]
    reduced_motion_matched: bool
    running_animations: list[dict[str, object]]
    screenshots: list[str]
    small_text: list[dict[str, object]] = field(default_factory=list)
    view_box_clipped_text: list[dict[str, object]] = field(default_factory=list)


@dataclass
class RenderReport:
    output_dir: str
    browser: str
    viewports: list[ViewportReport]
    errors: list[Finding]
    reports: list[Finding] = field(default_factory=list)


class RenderUnavailable(RuntimeError):
    """Raised when a local Chrome instance cannot be started."""


class CdpSession(Protocol):
    def call(self, method: str, params: dict[str, object] | None = None) -> dict[str, object]: ...

    def evaluate(self, expression: str, *, await_promise: bool = False) -> object: ...

    def wait_event(self, method: str, timeout: float) -> dict[str, object]: ...

    def close(self) -> None: ...


class _TreeParser(HTMLParser):
    """Build a forgiving element tree while retaining decoded text nodes."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.root = DomNode("#document", {}, [])
        self.stack: list[DomNode] = [self.root]
        self.has_doctype = False

    def _append_text(self, value: str) -> None:
        if value:
            self.stack[-1].children.append(TextNode(value))

    def handle_data(self, data: str) -> None:
        self._append_text(data)

    def handle_entityref(self, name: str) -> None:
        self._append_text(html.unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self._append_text(html.unescape(f"&#{name};"))

    def handle_decl(self, decl: str) -> None:
        if decl.strip().lower().startswith("doctype"):
            self.has_doctype = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized: dict[str, str] = {}
        for name, value in attrs:
            normalized[name.lower()] = "" if value is None else value
        node = DomNode(tag.lower(), normalized, [], self.stack[-1])
        self.stack[-1].children.append(node)
        if node.tag not in _VOID_ELEMENTS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if self.stack[-1].tag == tag.lower() and tag.lower() not in _VOID_ELEMENTS:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        target = tag.lower()
        # HTMLParser is intentionally forgiving, but an end tag should close
        # the matching open element and any malformed descendants above it.
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == target:
                del self.stack[index:]
                return


def parse_html(source: str) -> Document:
    parser = _TreeParser()
    parser.feed(source)
    parser.close()
    return Document(source, parser.root, parser.has_doctype)


def _element_children(node: DomNode) -> list[DomNode]:
    return [child for child in node.children if isinstance(child, DomNode)]


def _walk(node: DomNode) -> list[DomNode]:
    result: list[DomNode] = []
    for child in node.children:
        if isinstance(child, DomNode):
            result.append(child)
            result.extend(_walk(child))
    return result


def _text(node: DomNode | TextNode) -> str:
    if isinstance(node, TextNode):
        return node.text
    return "".join(_text(child) for child in node.children)


def _clean_text(node: DomNode | TextNode) -> str:
    return re.sub(r"\s+", " ", _text(node)).strip()


def _has_attr(node: DomNode, name: str) -> bool:
    return name.lower() in node.attrs


def _descendants(node: DomNode, tag: str | None = None) -> list[DomNode]:
    descendants = _walk(node)
    if tag is None:
        return descendants
    expected = tag.lower()
    return [item for item in descendants if item.tag == expected]


def _ancestor_chain(node: DomNode) -> list[DomNode]:
    result: list[DomNode] = []
    current = node.parent
    while current is not None:
        result.append(current)
        current = current.parent
    return result


def _scene_ancestors(node: DomNode, scenes: list[DomNode]) -> list[DomNode]:
    scene_set = {id(scene): scene for scene in scenes}
    return [ancestor for ancestor in _ancestor_chain(node) if id(ancestor) in scene_set]


def _word_count(value: str) -> int:
    return len(WORD_RE.findall(value))


def _sentence_count(value: str) -> int:
    value = value.strip()
    if not value:
        return 0
    pieces = re.split(r"[.!?]+", value)
    count = sum(1 for piece in pieces if piece.strip())
    return max(count, 1)


def _finding(errors: list[Finding], code: str, message: str, scope: str = "page") -> None:
    errors.append(Finding(code, message, "error", scope))


def _is_remote(value: str) -> bool:
    return bool(_REMOTE_URL_RE.match(value.strip()))


def _is_self_contained_reference(value: str) -> bool:
    normalized = value.strip().lower()
    return not normalized or normalized.startswith(("data:", "#"))


def _srcset_candidates(value: str) -> list[str]:
    """Extract candidate URLs without splitting commas inside data URLs."""

    return [
        match.group(0).strip().split(None, 1)[0]
        for match in re.finditer(r"(?:data:[^\s]+|[^,\s]+)(?:\s+[^,\s]+)?", value, flags=re.I)
    ]


def _external_dependencies(document: Document) -> list[str]:
    dependencies: list[str] = []
    for node in _walk(document.root):
        if node.tag == "a":
            continue
        if node.tag == "link":
            rel = {token.lower() for token in node.attrs.get("rel", "").split()}
            if (
                (rel & _LINK_DEPENDENCY_RELS or "preload" in rel)
                and not _is_self_contained_reference(node.attrs.get("href", ""))
            ):
                dependencies.append(node.attrs["href"])
        for attr in ("src", "data"):
            if (
                attr in node.attrs
                and node.tag in {"script", "img", "video", "audio", "source", "track", "iframe", "embed", "object"}
                and not _is_self_contained_reference(node.attrs[attr])
            ):
                dependencies.append(node.attrs[attr])
        if "srcset" in node.attrs:
            for candidate_url in _srcset_candidates(node.attrs["srcset"]):
                if candidate_url and not _is_self_contained_reference(candidate_url):
                    dependencies.append(candidate_url)
        if node.tag in {"image", "use"}:
            for attr in ("href", "xlink:href"):
                if attr in node.attrs and not _is_self_contained_reference(node.attrs[attr]):
                    dependencies.append(node.attrs[attr])
        if node.tag == "video" and "poster" in node.attrs and not _is_self_contained_reference(node.attrs["poster"]):
            dependencies.append(node.attrs["poster"])
        if node.tag == "input" and node.attrs.get("type", "").strip().lower() == "image":
            if "src" in node.attrs and not _is_self_contained_reference(node.attrs["src"]):
                dependencies.append(node.attrs["src"])
        if "style" in node.attrs:
            dependencies.extend(url for url in _css_dependencies(node.attrs["style"]))
        if node.tag == "style":
            dependencies.extend(url for url in _css_dependencies(_text(node)))
    return dependencies


def _css_dependencies(value: str) -> list[str]:
    urls: list[str] = []
    imports = re.findall(r"@import\s+(?:url\(\s*)?['\"]?([^'\"\s;)]+)", value, re.IGNORECASE)
    for candidate in imports:
        if not _is_self_contained_reference(candidate):
            urls.append(candidate)
    for match in _CSS_URL_RE.finditer(value):
        candidate = match.group(2)
        if not _is_self_contained_reference(candidate):
            urls.append(candidate)
    return urls


def _remote_dependencies(document: Document) -> list[str]:
    """Return dependency findings under the stable dependency.remote code."""

    return _external_dependencies(document)


def _accessible_name(visual: DomNode, ids: dict[str, DomNode]) -> tuple[str, bool]:
    labelledby = visual.attrs.get("aria-labelledby", "").split()
    if labelledby:
        labels: list[str] = []
        for referenced in labelledby:
            target = ids.get(referenced)
            if target is None or not _clean_text(target):
                return "", False
            labels.append(_clean_text(target))
        return " ".join(labels), bool(labels)
    aria_label = visual.attrs.get("aria-label", "").strip()
    if aria_label:
        return aria_label, True
    if visual.tag == "svg":
        titles = [item for item in _descendants(visual, "title") if _clean_text(item)]
        if titles:
            return _clean_text(titles[0]), True
    if visual.tag == "figure" and "data-visual" in visual.attrs:
        captions = [item for item in _descendants(visual, "figcaption") if _clean_text(item)]
        if captions:
            return _clean_text(captions[0]), True
    if visual.tag == "img" and visual.attrs.get("alt", "").strip():
        return visual.attrs["alt"].strip(), True
    return "", False


def _is_aria_hidden(node: DomNode) -> bool:
    return node.attrs.get("aria-hidden", "").strip().lower() == "true" or any(
        ancestor.attrs.get("aria-hidden", "").strip().lower() == "true"
        for ancestor in _ancestor_chain(node)
    )


def _is_svg_text(node: DomNode) -> bool:
    return node.tag == "text" and any(ancestor.tag == "svg" for ancestor in _ancestor_chain(node))


def _scene_for(node: DomNode, scenes: list[DomNode]) -> DomNode | None:
    if node in scenes:
        return node
    owners = _scene_ancestors(node, scenes)
    return owners[0] if owners else None


def _visual_child_labels(visual: DomNode) -> list[str]:
    """Return authored labels inside a visual in source order, once each."""

    labels: list[str] = []
    seen: set[str] = set()

    def append(value: str) -> None:
        cleaned = re.sub(r"\s+", " ", value).strip()
        if cleaned and cleaned not in seen:
            labels.append(cleaned)
            seen.add(cleaned)

    def visit(node: DomNode | TextNode) -> None:
        if isinstance(node, TextNode):
            append(node.text)
            return
        if _is_aria_hidden(node) or node.tag in {"script", "style", "template"}:
            return
        if node is not visual and _has_attr(node, "data-visual"):
            return
        if node is not visual and (node.tag in _PROSE_TAGS or node.tag == "span" or _is_svg_text(node)):
            if any(_has_attr(descendant, "data-visual") for descendant in _descendants(node)):
                for child in node.children:
                    visit(child)
                return
            append(_text(node))
            return
        for child in node.children:
            visit(child)

    for child in visual.children:
        visit(child)
    return labels


def extract_authored_prose(document: Document) -> list[ProseLine]:
    """Extract authored lines in DOM order, including scene and visual markers."""

    elements = _walk(document.root)
    scenes = [node for node in elements if node.tag == "section" and _has_attr(node, "data-scene")]
    scene_numbers = {id(scene): index for index, scene in enumerate(scenes, 1)}
    lines: list[ProseLine] = []
    seen_scenes: set[str] = set()

    def emit(text: str, tag: str, scene: DomNode | None, kind: str) -> None:
        value = re.sub(r"\s+", " ", text).strip()
        if not value:
            return
        scene_id = _scene_id(scene, scene_numbers[id(scene)]) if scene is not None else None
        if scene_id is not None and scene_id not in seen_scenes:
            seen_scenes.add(scene_id)
            lines.append(ProseLine(f"[scene: {scene_id}]", "section", scene_id, "scene", len(lines)))
        lines.append(ProseLine(value, tag, scene_id, kind, len(lines)))

    def visit(node: DomNode) -> None:
        if node.tag in {"script", "style", "template"} or _is_aria_hidden(node):
            return
        scene = _scene_for(node, scenes)
        if _has_attr(node, "data-visual"):
            name, named = _accessible_name(node, ids)
            parts = [name] if named and name else []
            for label in _visual_child_labels(node):
                if label not in parts:
                    parts.append(label)
            emit(f"[visual: {' / '.join(parts) or 'unnamed visual'}]", node.tag, scene, "visual")
            return
        if node.tag in _PROSE_TAGS or _is_svg_text(node):
            emit(_clean_text(node), node.tag, scene, "authored")
        for child in node.children:
            if isinstance(child, DomNode):
                visit(child)

    ids: dict[str, DomNode] = {}
    for node in elements:
        node_id = node.attrs.get("id", "")
        if node_id and node_id not in ids:
            ids[node_id] = node
    for child in document.root.children:
        if isinstance(child, DomNode):
            visit(child)
    return lines


def format_authored_prose(lines: list[ProseLine]) -> str:
    return "\n".join(line.text for line in lines)


def _strip_css_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _mask_css_comments_and_strings(css: str) -> str:
    masked: list[str] = []
    index = 0
    quote: str | None = None
    while index < len(css):
        if quote:
            if css[index] == "\\" and index + 1 < len(css):
                masked.extend((" ", " "))
                index += 2
            elif css[index] == quote:
                masked.append(" ")
                quote = None
                index += 1
            else:
                masked.append(" ")
                index += 1
        elif css.startswith("/*", index):
            end = css.find("*/", index + 2)
            masked.extend(" " for _ in css[index : len(css) if end < 0 else end + 2])
            index = len(css) if end < 0 else end + 2
        elif css[index] in "'\"":
            masked.append(" ")
            quote = css[index]
            index += 1
        else:
            masked.append(css[index])
            index += 1
    return "".join(masked)


def _strip_js_comments(source: str) -> str:
    cleaned: list[str] = []
    index = 0
    quote: str | None = None
    while index < len(source):
        if quote:
            char = source[index]
            cleaned.append(char)
            if char == "\\" and index + 1 < len(source):
                cleaned.append(source[index + 1])
                index += 2
            elif char == quote:
                quote = None
                index += 1
            else:
                index += 1
        elif source.startswith("/*", index):
            end = source.find("*/", index + 2)
            if end < 0:
                break
            cleaned.extend(" " for _ in source[index : end + 2])
            index = end + 2
        elif source.startswith("//", index):
            end = source.find("\n", index + 2)
            if end < 0:
                break
            cleaned.extend(" " for _ in source[index:end])
            index = end
        elif source[index] in "'\"" or source[index] == chr(96):
            quote = source[index]
            cleaned.append(source[index])
            index += 1
        else:
            cleaned.append(source[index])
            index += 1
    return "".join(cleaned)


def _has_css_reduced_motion_rule(css: str) -> bool:
    for match in re.finditer(r"@media\b([^{}]*)\{", _mask_css_comments_and_strings(css), flags=re.I):
        if re.search(r"prefers-reduced-motion\s*:\s*reduce\b", match.group(1), flags=re.I):
            return True
    return False


def _has_script_reduced_motion_query(source: str) -> bool:
    cleaned = _strip_js_comments(source)
    index = 0
    while index < len(cleaned):
        if cleaned[index] in "'\"" or cleaned[index] == chr(96):
            quote = cleaned[index]
            index += 1
            while index < len(cleaned):
                if cleaned[index] == "\\":
                    index += 2
                elif cleaned[index] == quote:
                    index += 1
                    break
                else:
                    index += 1
            continue
        match = re.match(r"(?<![\w$])matchMedia\s*\(", cleaned[index:], flags=re.I)
        if match:
            cursor = index + match.end()
            while cursor < len(cleaned) and cleaned[cursor].isspace():
                cursor += 1
            if cursor < len(cleaned) and (cleaned[cursor] in "'\"" or cleaned[cursor] == chr(96)):
                quote = cleaned[cursor]
                cursor += 1
                query: list[str] = []
                while cursor < len(cleaned):
                    if cleaned[cursor] == "\\" and cursor + 1 < len(cleaned):
                        query.append(cleaned[cursor + 1])
                        cursor += 2
                    elif cleaned[cursor] == quote:
                        break
                    else:
                        query.append(cleaned[cursor])
                        cursor += 1
                if re.search(r"prefers-reduced-motion\s*:\s*reduce\b", "".join(query), flags=re.I):
                    return True
        index += 1
    return False


def _find_closing_brace(value: str, opening: int) -> int:
    depth = 1
    quote: str | None = None
    escaped = False
    index = opening + 1
    while index < len(value):
        char = value[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return len(value) - 1


def _split_css_declarations(body: str) -> dict[str, str]:
    declarations: dict[str, str] = {}
    start = 0
    depth = 0
    quote: str | None = None
    for index, char in enumerate(body + ";"):
        if quote:
            if char == quote and (index == 0 or body[index - 1] != "\\"):
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif char == ";" and depth == 0:
            piece = body[start:index].strip()
            start = index + 1
            if ":" not in piece:
                continue
            name, value = piece.split(":", 1)
            if name.strip():
                declarations[name.strip().lower()] = value.strip()
    return declarations


def parse_css_rules(css: str) -> list[CssRule]:
    """Parse ordinary CSS rules while preserving nested @media context."""

    cleaned = _strip_css_comments(css)
    rules: list[CssRule] = []

    def scan(start: int, end: int, context: str = "") -> None:
        index = start
        while index < end:
            while index < end and cleaned[index].isspace():
                index += 1
            if index >= end:
                break
            opening = cleaned.find("{", index, end)
            if opening < 0:
                break
            header = cleaned[index:opening].strip()
            closing = _find_closing_brace(cleaned[:end], opening)
            if closing < opening:
                break
            body = cleaned[opening + 1 : closing]
            nested = "@" in body and "{" in body
            if header.lower().startswith(("@media", "@supports", "@layer", "@container", "@scope")):
                nested_context = f"{context}{header} "
                scan(opening + 1, closing, nested_context)
            elif header.lower().startswith(("@keyframes", "@-webkit-keyframes")):
                # Keyframe frames are animation steps, not page selectors.
                # Do not let from/to opacity or transforms look like initial
                # hidden states for reveal analysis.
                pass
            elif nested:
                scan(opening + 1, closing, f"{context}{header} ")
                declarations = _split_css_declarations(body.split("{", 1)[0])
                if declarations:
                    rules.append(CssRule(f"{context}{header}", declarations, context))
            else:
                rules.append(CssRule(f"{context}{header}".strip(), _split_css_declarations(body), context))
            index = closing + 1

    scan(0, len(cleaned))
    return [rule for rule in rules if rule.selector and rule.declarations]


def _style_sources(document: Document) -> tuple[str, str]:
    css_parts: list[str] = []
    script_parts: list[str] = []
    for node in _walk(document.root):
        if node.tag == "style":
            css_parts.append(_text(node))
        elif node.tag == "script":
            script_parts.append(_text(node))
        if "style" in node.attrs:
            css_parts.append(f"inline:{node.tag} {{{node.attrs['style']}}}")
        for name, value in node.attrs.items():
            if name.startswith("on"):
                script_parts.append(value)
    return "\n".join(css_parts), "\n".join(script_parts)


def _duration_seconds(value: str) -> float:
    durations = []
    for match in re.finditer(r"(?<![\w.])(\d*\.?\d+)\s*(ms|s)\b", value, flags=re.I):
        amount = float(match.group(1))
        durations.append(amount / 1000 if match.group(2).lower() == "ms" else amount)
    return max(durations, default=0.0)


def _transition_properties(value: str) -> list[str]:
    properties: list[str] = []
    for item in value.split(","):
        tokens = item.strip().split()
        if tokens:
            properties.append(tokens[0].lower())
    return properties


def _short_colour_transition(selector: str, declarations: dict[str, str]) -> bool:
    if not re.search(r":(?:hover|focus)(?:\b|:)", selector, flags=re.I):
        return False
    transition = declarations.get("transition", "")
    if not transition:
        properties = declarations.get("transition-property", "")
        duration = declarations.get("transition-duration", "")
        transition = f"{properties} {duration}"
    allowed = {"color", "background", "background-color", "border", "border-color", "fill", "stroke"}
    return bool(transition) and _duration_seconds(transition) <= 0.2 and all(
        prop in allowed or (prop == "all" and False) for prop in _transition_properties(transition)
    )


def _is_reduced_motion_context(context: str) -> bool:
    return bool(
        re.search(
            r"@media\b[^{}]*prefers-reduced-motion\s*:\s*reduce\b",
            context,
            flags=re.I,
        )
    )


def _css_selector_list(selector: str) -> list[str]:
    return [part.strip() for part in selector.split(",") if part.strip()]


def _rule_selector_list(rule: CssRule) -> list[str]:
    selector = rule.selector
    if rule.context and selector.startswith(rule.context):
        selector = selector[len(rule.context) :].strip()
    return _css_selector_list(selector)


def _selectors_overlap(first: CssRule, second: CssRule) -> bool:
    return any(
        _selector_is_covered(left, right) or _selector_is_covered(right, left)
        for left in _rule_selector_list(first)
        for right in _rule_selector_list(second)
    )


def _selector_is_covered(base_selector: str, reduced_selector: str) -> bool:
    """Conservatively match reduced selectors to transition selectors."""

    reduced = reduced_selector.strip()
    return reduced == "*" or reduced == base_selector.strip()


def _transition_properties_for_rule(declarations: dict[str, str]) -> set[str]:
    transition = declarations.get("transition", "").strip()
    if transition and transition.lower().startswith("none"):
        return {"*"}
    if not transition and "transition-duration" in declarations and "transition-property" not in declarations:
        return {"*"}
    if transition and _transition_shorthand_is_propertyless(transition):
        return {"*"}
    value = transition or declarations.get("transition-property", "")
    if value.strip().lower() == "none":
        return {"*"}
    properties = set(_transition_properties(value))
    return {"*"} if "all" in properties else properties


def _transition_shorthand_is_propertyless(value: str) -> bool:
    normalized = re.sub(r"(?:cubic-bezier|steps|linear)\([^)]*\)", "timing", value, flags=re.I)
    timing_keywords = {"ease", "ease-in", "ease-out", "ease-in-out", "linear", "step-start", "step-end", "timing"}
    tokens = [token for item in normalized.split(",") for token in item.strip().split()]
    return bool(tokens) and all(
        re.fullmatch(r"\d*\.?\d+(?:ms|s)", token, flags=re.I) or token.lower() in timing_keywords
        for token in tokens
    )


def _transition_is_effectively_zero(declarations: dict[str, str]) -> bool:
    transition = declarations.get("transition", "").strip()
    if transition and transition.lower().startswith("none"):
        return True
    if declarations.get("transition-property", "").strip().lower() == "none":
        return True

    durations = declarations.get("transition-duration", "")
    if durations:
        values = re.findall(r"(?<![\w.])(\d*\.?\d+)\s*(ms|s)\b", durations, flags=re.I)
        if not values:
            return False
        return all(
            (float(amount) / 1000 if unit.lower() == "ms" else float(amount)) == 0
            for amount, unit in values
        )
    if not transition:
        return False

    items = [item.strip() for item in transition.split(",") if item.strip()]
    for item in items:
        if re.search(r"\b(?:var|calc|min|max|clamp)\s*\(", item, flags=re.I):
            return False
        values = re.findall(r"(?<![\w.])(\d*\.?\d+)\s*(ms|s)\b", item, flags=re.I)
        if any(
            (float(amount) / 1000 if unit.lower() == "ms" else float(amount)) > 0
            for amount, unit in values
        ):
            return False
    return True


def _transition_rule_is_protected(rule: CssRule, reduced_rules: list[CssRule]) -> bool:
    base_properties = _transition_properties_for_rule(rule.declarations)
    if not base_properties:
        return False
    for base_selector in _rule_selector_list(rule):
        for property_name in base_properties:
            if not any(
                _transition_is_effectively_zero(reduced.declarations)
                and any(
                    _selector_is_covered(base_selector, reduced_selector)
                    for reduced_selector in _rule_selector_list(reduced)
                )
                and (
                    "*" in _transition_properties_for_rule(reduced.declarations)
                    or property_name in _transition_properties_for_rule(reduced.declarations)
                )
                for reduced in reduced_rules
            ):
                return False
    return True


def _has_nonzero_translate(transform: str) -> bool:
    for match in re.finditer(r"\btranslate(?:x|y|z|3d)?\s*\(([^)]*)\)", transform, flags=re.I):
        arguments = match.group(1)
        if re.search(r"\b(?:var|calc)\s*\(", arguments, flags=re.I):
            return True
        values = re.findall(r"[-+]?\d*\.?\d+", arguments)
        if not values or any(float(value) != 0 for value in values):
            return True
    return False


def _initial_state(selector: str, declarations: dict[str, str]) -> bool:
    opacity = declarations.get("opacity", "").strip()
    if opacity:
        try:
            if float(opacity) <= 0:
                return True
        except ValueError:
            pass
    if declarations.get("visibility", "").strip().lower() in {"hidden", "collapse"}:
        return True
    if declarations.get("display", "").strip().lower() == "none":
        return True
    return _has_nonzero_translate(declarations.get("transform", ""))


def inventory_motion(document: Document, source: str) -> MotionInventory:
    css, scripts = _style_sources(document)
    rules = parse_css_rules(css)
    uses: list[MotionUse] = []
    transition_uses: list[tuple[MotionUse, CssRule]] = []
    initial_hidden: list[str] = []
    initial_state_rules: list[CssRule] = []
    has_css_reduced_rule = _has_css_reduced_motion_rule(css)
    has_script_reduced_query = _has_script_reduced_motion_query(scripts)
    script_code = _strip_js_comments(scripts)

    if re.search(r"@(?:-webkit-)?keyframes\b", css, flags=re.I):
        uses.append(MotionUse("css-keyframes", "@keyframes", True))
    for rule in rules:
        declarations = rule.declarations
        selector = rule.selector
        if "animation" in declarations or "animation-name" in declarations:
            value = declarations.get("animation", declarations.get("animation-name", ""))
            if value.strip().lower() not in {"", "none"}:
                uses.append(MotionUse("css-animation", f"{selector}: {value}", True))
        transition = declarations.get("transition", "")
        if transition.strip().lower() == "none":
            transition = ""
        if (transition or "transition-property" in declarations) and not _is_reduced_motion_context(rule.context):
            exempt = _short_colour_transition(selector, declarations)
            use = MotionUse(
                "css-transition-exempt" if exempt else "css-transition",
                f"{selector}: {transition or declarations.get('transition-property', '')}",
                not exempt,
                not exempt,
            )
            uses.append(use)
            if not exempt:
                transition_uses.append((use, rule))
        if _initial_state(selector, declarations):
            initial_hidden.append(selector)
            initial_state_rules.append(rule)

    reduced_rules = [
        rule
        for rule in rules
        if _is_reduced_motion_context(rule.context) and _transition_is_effectively_zero(rule.declarations)
    ]
    reduced_motion_gaps: list[str] = []
    for use, rule in transition_uses:
        if not _transition_rule_is_protected(rule, reduced_rules):
            reduced_motion_gaps.append(use.source)
            use.requires_reduced_motion = True
        else:
            use.requires_reduced_motion = False

    all_elements = _walk(document.root)
    initial_state_nodes: list[DomNode] = []
    for node in all_elements:
        if node.tag in {"animate", "animatemotion", "animatetransform", "set"}:
            uses.append(MotionUse("smil", node.tag, True))
        if "style" in node.attrs:
            inline = _split_css_declarations(node.attrs["style"])
            if _initial_state(f"inline:{node.tag}", inline):
                initial_hidden.append(f"inline:{node.tag}")
                initial_state_nodes.append(node)
    if re.search(r"\.animate\s*\(", script_code, flags=re.I):
        uses.append(MotionUse("web-animation", ".animate(", True))
    if re.search(r"requestAnimationFrame\s*\(", script_code, flags=re.I):
        uses.append(MotionUse("raf", "requestAnimationFrame", True))
    scroll_observer_present = bool(
        re.search(
            r"(?:\bIntersectionObserver\b|\baddEventListener\s*\(\s*['\"]scroll['\"]\s*(?:,|\))|\bonscroll\b)",
            script_code,
            flags=re.I,
        )
    )
    initial_state_rules = [rule for rule in initial_state_rules if not _is_reduced_motion_context(rule.context)]
    transition_rules = [rule for use, rule in transition_uses if use.kind == "css-transition"]
    associated_initial_state = any(
        _selectors_overlap(transition, initial)
        for transition in transition_rules
        for initial in initial_state_rules
    ) or any(
        any(_selector_matches(node, selector) for selector in _rule_selector_list(transition))
        for transition in transition_rules
        for node in initial_state_nodes
    )
    reveal_pattern = bool(transition_rules and (associated_initial_state or scroll_observer_present))
    return MotionInventory(
        uses,
        has_css_reduced_rule,
        has_script_reduced_query,
        list(dict.fromkeys(initial_hidden)),
        scroll_observer_present,
        reveal_pattern,
        list(dict.fromkeys(reduced_motion_gaps)),
    )


def _selector_matches(node: DomNode, selector: str) -> bool:
    selector = re.sub(r"^@[^ ]+\s+", "", selector).strip()
    selector = selector.split(",", 1)[0].strip()
    token = re.split(r"\s+|>", selector)[-1]
    token = re.sub(r"::?[\w-]+(?:\([^)]*\))?", "", token)
    attrs = re.findall(r"\[([\w:-]+)(?:\s*=\s*['\"]?([^\]'\"]+)['\"]?)?\]", token)
    for name, value in attrs:
        if name not in node.attrs:
            return False
        if value and node.attrs.get(name) != value:
            return False
    token = re.sub(r"\[[^]]+\]", "", token)
    id_match = re.search(r"#([\w-]+)", token)
    if id_match and node.attrs.get("id") != id_match.group(1):
        return False
    classes = re.findall(r"\.([\w-]+)", token)
    class_set = set(node.attrs.get("class", "").split())
    if any(class_name not in class_set for class_name in classes):
        return False
    tag = re.match(r"^[a-zA-Z][\w-]*|^\*", token)
    return not tag or tag.group(0) == "*" or node.tag == tag.group(0).lower()


def _scene_id_for_node(node: DomNode, scenes: list[DomNode]) -> str | None:
    scene = _scene_for(node, scenes)
    if scene is None:
        return None
    ordinal = scenes.index(scene) + 1
    return _scene_id(scene, ordinal)


def detect_visual_proxies(document: Document, source: str, motion: MotionInventory) -> list[VisualProxy]:
    css, _ = _style_sources(document)
    rules = parse_css_rules(css)
    elements = _walk(document.root)
    scenes = [node for node in elements if node.tag == "section" and _has_attr(node, "data-scene")]
    proxies: list[VisualProxy] = []

    for rule in rules:
        declarations = rule.declarations
        selectors = [part.strip() for part in rule.selector.split(",") if part.strip()]
        matched = [node for node in elements if any(_selector_matches(node, selector) for selector in selectors)]
        if "border-radius" in declarations:
            radius = declarations["border-radius"]
            if len(matched) >= 3:
                proxies.append(VisualProxy("visual.rounded-repeat", len(matched), selectors[:3], list(dict.fromkeys(filter(None, (_scene_id_for_node(node, scenes) for node in matched)))), f"rounded container selector {rule.selector!r} repeats across {len(matched)} elements"))
            if re.search(r"(?:9999?px|100%|50%)", radius, flags=re.I):
                proxies.append(VisualProxy("visual.pill", len(matched), selectors[:3], [], f"pill-like radius {radius!r} on {rule.selector!r}"))
        if "box-shadow" in declarations:
            proxies.append(VisualProxy("visual.shadow", len(matched), selectors[:3], [], f"box-shadow on {rule.selector!r}"))
        if any("gradient(" in value.lower() for value in declarations.values()):
            proxies.append(VisualProxy("visual.gradient", len(matched), selectors[:3], [], f"gradient on {rule.selector!r}"))

    if motion.initial_hidden:
        proxies.append(VisualProxy("visual.initial-hidden", len(motion.initial_hidden), motion.initial_hidden[:3], [], "initial hidden or translated states are present"))
    if motion.scroll_observer_present:
        proxies.append(VisualProxy("visual.scroll-trigger", 1, ["IntersectionObserver/scroll"], [], "scroll-triggered behavior is present"))

    signatures: dict[tuple[tuple[str, str], ...], list[str]] = {}
    for ordinal, scene in enumerate(scenes, 1):
        signature = tuple(
            (node.tag, node.attrs.get("class", ""))
            for node in _element_children(scene)
            if node.tag not in {"script", "style"}
        )
        signatures.setdefault(signature, []).append(_scene_id(scene, ordinal))
    for signature, scene_ids in signatures.items():
        if len(scene_ids) >= 2 and signature:
            proxies.append(VisualProxy("visual.scene-repeat", len(scene_ids), [tag for tag, _ in signature[:3]], scene_ids, f"scene composition repeats across {len(scene_ids)} scenes"))
    return proxies


def scan_prose_patterns(text: str) -> dict[str, object]:
    contrastive_patterns = [
        r", not ",
        r"\binstead of\b",
        r"\brather than\b",
        r"\bnot only\b",
        r"\bless about\b",
        r"\bnot because\b",
    ]
    contrastive = sum(len(re.findall(pattern, text, flags=re.I)) for pattern in contrastive_patterns)
    plain_words = ("no", "not", "nobody", "never", "nothing", "none", "cannot", "rarely", "without")
    tally = {word: len(re.findall(rf"\b{re.escape(word)}\b", text, flags=re.I)) for word in plain_words}
    heading_lengths: list[int] = []
    for line in text.splitlines():
        if line.startswith("[heading: ") and line.endswith("]"):
            heading_lengths.append(_word_count(line[10:-1]))
    for match in re.finditer(r"<h[1-6]\b[^>]*>(.*?)</h[1-6]\s*>", text, flags=re.I | re.S):
        heading_lengths.append(_word_count(re.sub(r"<[^>]+>", " ", html.unescape(match.group(1)))))
    punctuation = {name: text.count(char) for char, name in ((",", "commas"), (";", "semicolons"), (":", "colons"), ("(", "parens"))}
    words = _word_count(text)
    return {
        "words": words,
        "negation_contrasts": contrastive,
        "plain_negations": tally,
        "plain_negation_carriers": sum(tally.values()),
        "heading_lengths": heading_lengths,
        "em_dashes": text.count("—"),
        "punctuation": punctuation,
    }


def _scene_id(scene: DomNode, ordinal: int) -> str:
    value = scene.attrs.get("id", "").strip()
    return value or f"scene-{ordinal}"


def analyze_html(source: str, path: Path | None = None) -> StaticReport:
    document = parse_html(source)
    errors: list[Finding] = []
    reports: list[Finding] = []
    all_elements = _walk(document.root)
    mains = [node for node in all_elements if node.tag == "main"]
    if len(mains) != 1:
        _finding(errors, "document.main-count", f"expected one main element, found {len(mains)}")
    if not any(node.tag == "meta" and node.attrs.get("name", "").lower() == "viewport" for node in all_elements):
        _finding(errors, "document.viewport", "missing viewport metadata")

    scenes = [node for node in all_elements if node.tag == "section" and _has_attr(node, "data-scene")]
    if not scenes:
        _finding(errors, "scene.none", "page must contain at least one section[data-scene]")

    page_h1s = [node for node in all_elements if node.tag == "h1"]
    if len(page_h1s) != 1:
        _finding(errors, "document.h1-count", f"page must contain exactly one h1, found {len(page_h1s)}")

    scene_ids: list[str] = []
    explicit_scene_ids: set[str] = set()
    for ordinal, scene in enumerate(scenes, 1):
        raw_id = scene.attrs.get("id", "").strip()
        scene_ids.append(_scene_id(scene, ordinal))
        if not raw_id:
            _finding(errors, "scene.id", f"scene {ordinal} must have a nonempty id")
        elif raw_id in explicit_scene_ids:
            _finding(errors, "scene.duplicate-id", f"scene id {raw_id!r} is not unique")
        else:
            explicit_scene_ids.add(raw_id)

    ids: dict[str, DomNode] = {}
    for node in all_elements:
        node_id = node.attrs.get("id", "")
        if node_id and node_id not in ids:
            ids[node_id] = node

    scene_metrics: list[SceneMetrics] = []
    prose_nodes: list[tuple[DomNode, list[DomNode]]] = []
    for node in all_elements:
        if not _has_attr(node, "data-prose"):
            continue
        owners = _scene_ancestors(node, scenes)
        if node.tag != "p" or len(owners) != 1:
            _finding(errors, "prose.location", "data-prose must be a p element inside exactly one scene")
        else:
            prose_nodes.append((node, owners))

    for ordinal, scene in enumerate(scenes, 1):
        scene_id = scene_ids[ordinal - 1]
        claim_tag = "h1" if ordinal == 1 else "h2"
        claim_markers = [node for node in _descendants(scene) if _has_attr(node, "data-claim")]
        valid_claims = [node for node in claim_markers if node.tag == claim_tag and _clean_text(node)]
        if len(claim_markers) != 1 or len(valid_claims) != 1:
            code = "scene.first-claim" if ordinal == 1 else "scene.claim"
            _finding(errors, code, f"scene {scene_id!r} must have exactly one nonempty {claim_tag}[data-claim]", scene_id)
        claim = _clean_text(valid_claims[0]) if valid_claims else ""
        scene_paragraph_words = 0
        scene_sentence_count = 0
        longest_paragraph = 0
        for paragraph, owners in prose_nodes:
            if owners and owners[0] is scene:
                text = _clean_text(paragraph)
                words = _word_count(text)
                sentences = _sentence_count(text)
                scene_paragraph_words += words
                scene_sentence_count += sentences
                longest_paragraph = max(longest_paragraph, words)
                if words > MAX_PARAGRAPH_WORDS:
                    _finding(errors, "density.paragraph", f"paragraph has {words} words (maximum {MAX_PARAGRAPH_WORDS})", scene_id)
        if scene_paragraph_words > MAX_SCENE_PARAGRAPH_WORDS:
            _finding(errors, "density.scene", f"scene has {scene_paragraph_words} paragraph words (maximum {MAX_SCENE_PARAGRAPH_WORDS})", scene_id)
        average = scene_paragraph_words / scene_sentence_count if scene_sentence_count else 0.0
        scene_metrics.append(SceneMetrics(scene_id, claim, scene_paragraph_words, scene_sentence_count, average, longest_paragraph))

        visuals = ([scene] if _has_attr(scene, "data-visual") else []) + [
            node for node in _descendants(scene) if _has_attr(node, "data-visual")
        ]
        if not visuals:
            _finding(errors, "visual.missing", f"scene {scene_id!r} must contain a data-visual", scene_id)
        for visual in visuals:
            hidden = visual.attrs.get("aria-hidden", "").lower() == "true" or any(
                ancestor.attrs.get("aria-hidden", "").lower() == "true" for ancestor in _ancestor_chain(visual)
            )
            if hidden:
                _finding(errors, "visual.hidden", "data-visual is aria-hidden or inside an aria-hidden ancestor", scene_id)
            _, named = _accessible_name(visual, ids)
            if not named:
                _finding(errors, "visual.name", "data-visual must have an accessible name", scene_id)

    total_words = sum(metric.paragraph_words for metric in scene_metrics)
    total_sentences = sum(metric.sentence_count for metric in scene_metrics)
    if total_sentences:
        average_words = total_words / total_sentences
        if average_words > MAX_AVERAGE_SENTENCE_WORDS:
            _finding(errors, "density.average-sentence", f"average explanatory sentence has {average_words:.2f} words (maximum {MAX_AVERAGE_SENTENCE_WORDS})")

    remote = _remote_dependencies(document)
    if remote:
        _finding(errors, "dependency.remote", f"remote runtime or asset dependencies: {', '.join(dict.fromkeys(remote))}")

    authored_prose = extract_authored_prose(document)
    motion = inventory_motion(document, source)
    css_motion_kinds = {"css-keyframes", "css-animation"}
    script_motion_kinds = {"web-animation", "raf"}
    if (
        any(use.kind in css_motion_kinds and use.requires_reduced_motion for use in motion.uses)
        and not motion.has_css_reduced_rule
    ) or any(use.kind == "css-transition" and use.requires_reduced_motion for use in motion.uses):
        _finding(errors, "motion.reduced", "CSS motion requires @media (prefers-reduced-motion: reduce)")
    if any(use.kind in {"smil"} and use.requires_reduced_motion for use in motion.uses) and not motion.has_script_reduced_query:
        _finding(errors, "motion.reduced", "SVG SMIL motion requires a script prefers-reduced-motion query")
    if any(use.kind in script_motion_kinds and use.requires_reduced_motion for use in motion.uses) and not motion.has_script_reduced_query:
        _finding(errors, "motion.reduced", "JavaScript motion requires a script prefers-reduced-motion query")
    if motion.reveal_pattern:
        _finding(errors, "motion.reveal", "transition combines with initial hidden/translated state or a scroll trigger")

    visual_proxies = detect_visual_proxies(document, source, motion)
    for proxy in visual_proxies:
        reports.append(Finding(proxy.kind, proxy.message, "report", proxy.scene_ids[0] if proxy.scene_ids else "page"))

    authored_text = format_authored_prose(authored_prose)
    pattern_text = "\n".join(
        f"[heading: {line.text}]" if line.tag in {"h1", "h2", "h3", "h4", "h5", "h6"} else line.text
        for line in authored_prose
    )
    prose_patterns = scan_prose_patterns(pattern_text)
    word_count = int(prose_patterns["words"])
    contrastive = int(prose_patterns["negation_contrasts"])
    if contrastive > round(word_count / 600):
        reports.append(Finding("prose.negation-contrast", f"{contrastive} contrastive negations in {word_count} authored words", "report"))
    if int(prose_patterns["em_dashes"]) > 3:
        reports.append(Finding("prose.em-dash", f"{prose_patterns['em_dashes']} em dashes in authored prose", "report"))
    heading_lengths = prose_patterns["heading_lengths"]
    if len(heading_lengths) > 4:
        band = [length for length in heading_lengths if 4 <= length <= 9]
        if len(heading_lengths) - len(band) <= 1:
            reports.append(Finding("prose.heading-cadence", f"{len(band)} of {len(heading_lengths)} headings fall in the same 4-9 word band", "report"))
    punctuation = prose_patterns["punctuation"]
    if int(punctuation["parens"]) == 0 and int(punctuation["semicolons"]) == 0:
        reports.append(Finding("prose.punctuation", "no parentheses or semicolons in authored prose", "report"))
    for caption in all_elements:
        if caption.tag != "figcaption":
            continue
        caption_text = _clean_text(caption)
        caption_words = _word_count(caption_text)
        caption_sentences = _sentence_count(caption_text)
        if caption_words > MAX_CAPTION_WORDS or caption_sentences > MAX_CAPTION_SENTENCES:
            owners = _scene_ancestors(caption, scenes)
            scope = _scene_id(owners[0], scenes.index(owners[0]) + 1) if owners else "page"
            reports.append(
                Finding(
                    "prose.caption-explains",
                    f"figcaption has {caption_words} words in {caption_sentences} sentences; captions name the marks, explanation belongs in p[data-prose]",
                    "report",
                    scope,
                )
            )
    return StaticReport(str(path) if path is not None else None, errors, reports, scene_metrics, authored_prose, motion, visual_proxies)


def check_html_file(path: Path) -> StaticReport:
    source = path.read_text(encoding="utf-8")
    return analyze_html(source, path)


_STANDARD_CHROME_PATHS = (
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium.app/Contents/MacOS/Chromium"),
    Path("/usr/bin/google-chrome"),
    Path("/usr/bin/google-chrome-stable"),
    Path("/usr/bin/chromium"),
    Path("/usr/bin/chromium-browser"),
)
_CHROME_PATH_NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")


def find_chrome(env: Mapping[str, str] | None = None) -> Path | None:
    """Find the local Chrome binary without invoking a shell."""

    values = os.environ if env is None else env
    configured = values.get("CHROME_BIN", "").strip()
    if configured:
        return Path(configured).expanduser()
    for candidate in _STANDARD_CHROME_PATHS:
        if candidate.is_file():
            return candidate
    for name in _CHROME_PATH_NAMES:
        resolved = shutil.which(name)
        if resolved:
            return Path(resolved)
    return None


def _read_exact(sock: socket.socket, length: int) -> bytes:
    chunks: list[bytes] = []
    remaining = length
    while remaining:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError("WebSocket closed while reading a frame")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def encode_websocket_frame(payload: bytes, mask: bytes) -> bytes:
    """Encode one masked client text frame, including large payload lengths."""

    if len(mask) != 4:
        raise ValueError("WebSocket masks must contain exactly four bytes")
    length = len(payload)
    if length < 126:
        header = bytes((0x81, 0x80 | length))
    elif length < 2**16:
        header = bytes((0x81, 0x80 | 126)) + length.to_bytes(2, "big")
    else:
        header = bytes((0x81, 0x80 | 127)) + length.to_bytes(8, "big")
    masked = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
    return header + mask + masked


def _read_raw_websocket_frame(sock: socket.socket) -> tuple[bool, int, bytes]:
    first, second = _read_exact(sock, 2)
    final = bool(first & 0x80)
    opcode = first & 0x0F
    masked = bool(second & 0x80)
    length = second & 0x7F
    if length == 126:
        length = int.from_bytes(_read_exact(sock, 2), "big")
    elif length == 127:
        length = int.from_bytes(_read_exact(sock, 8), "big")
    mask = _read_exact(sock, 4) if masked else b""
    payload = _read_exact(sock, length)
    if mask:
        payload = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
    return final, opcode, payload


def read_websocket_frame(sock: socket.socket) -> bytes:
    """Read and reassemble one WebSocket data message.

    Chrome sends JSON as text frames, but CDP screenshot responses can be split
    across continuation frames. Ping frames are answered inline as required by
    RFC 6455 so callers only see complete application messages.
    """

    fragments: list[bytes] = []
    opcode: int | None = None
    while True:
        final, current_opcode, payload = _read_raw_websocket_frame(sock)
        if current_opcode == 0x9:  # ping
            sock.sendall(encode_websocket_frame(payload, os.urandom(4)).replace(b"\x81", b"\x8A", 1))
            continue
        if current_opcode == 0xA:  # pong
            continue
        if current_opcode == 0x8:  # close
            return b""
        if opcode is None:
            if current_opcode not in (0x1, 0x2):
                raise ValueError(f"unexpected WebSocket opcode {current_opcode}")
            opcode = current_opcode
        elif current_opcode != 0:
            raise ValueError(f"expected continuation frame, got opcode {current_opcode}")
        fragments.append(payload)
        if final:
            return b"".join(fragments)


class CdpClient:
    """The small standard-library WebSocket/CDP subset used by the renderer."""

    def __init__(self, sock: socket.socket):
        self._socket = sock
        self._next_id = 1
        self._events: list[dict[str, object]] = []
        self._responses: dict[int, dict[str, object]] = {}
        self._process: subprocess.Popen[bytes] | None = None
        self._profile: Path | None = None

    def _send(self, message: dict[str, object]) -> None:
        payload = json.dumps(message, separators=(",", ":")).encode("utf-8")
        self._socket.sendall(encode_websocket_frame(payload, os.urandom(4)))

    def _read_message(self) -> dict[str, object]:
        raw = read_websocket_frame(self._socket)
        if not raw:
            raise ConnectionError("Chrome closed the DevTools WebSocket")
        value = json.loads(raw.decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError("CDP message was not a JSON object")
        return value

    def call(self, method: str, params: dict[str, object] | None = None) -> dict[str, object]:
        request_id = self._next_id
        self._next_id += 1
        message: dict[str, object] = {"id": request_id, "method": method}
        if params is not None:
            message["params"] = params
        self._send(message)
        if request_id in self._responses:
            response = self._responses.pop(request_id)
        else:
            while True:
                response = self._read_message()
                incoming_id = response.get("id")
                if isinstance(incoming_id, int) and incoming_id == request_id:
                    break
                if isinstance(response.get("method"), str):
                    self._events.append(response)
                elif isinstance(incoming_id, int):
                    self._responses[incoming_id] = response
        if "error" in response:
            raise RuntimeError(f"CDP {method} failed: {response['error']}")
        result = response.get("result", {})
        return result if isinstance(result, dict) else {}

    def evaluate(self, expression: str, *, await_promise: bool = False) -> object:
        result = self.call(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True, "awaitPromise": await_promise},
        )
        exception = result.get("exceptionDetails")
        if exception:
            raise RuntimeError(f"Runtime.evaluate failed: {exception}")
        value = result.get("result", {})
        if isinstance(value, dict):
            if "value" in value:
                return value["value"]
            if "unserializableValue" in value:
                return value["unserializableValue"]
        return value

    def wait_event(self, method: str, timeout: float) -> dict[str, object]:
        deadline = time.monotonic() + timeout
        while True:
            for index, event in enumerate(self._events):
                if event.get("method") == method:
                    return self._events.pop(index)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"timed out waiting for CDP event {method}")
            self._socket.settimeout(remaining)
            try:
                event = self._read_message()
            except socket.timeout as exc:
                raise TimeoutError(f"timed out waiting for CDP event {method}") from exc
            finally:
                self._socket.settimeout(None)
            if event.get("method") == method:
                return event
            if isinstance(event.get("method"), str):
                self._events.append(event)
            elif isinstance(event.get("id"), int):
                self._responses[int(event["id"])] = event

    def close(self) -> None:
        try:
            self._socket.close()
        finally:
            if self._process is not None:
                _stop_process(self._process)
            if self._profile is not None:
                shutil.rmtree(self._profile, ignore_errors=True)
                self._profile = None


def _connect_websocket(url: str) -> socket.socket:
    from urllib.parse import urlsplit

    parsed = urlsplit(url)
    if parsed.scheme != "ws" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise RenderUnavailable(f"Chrome returned a non-loopback WebSocket URL: {url}")
    port = parsed.port
    if port is None:
        raise RenderUnavailable(f"Chrome WebSocket URL has no port: {url}")
    sock = socket.create_connection((parsed.hostname, port), timeout=5)
    key = base64.b64encode(os.urandom(16)).decode("ascii")
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query
    request = (
        f"GET {path} HTTP/1.1\r\nHost: {parsed.hostname}:{port}\r\n"
        "Upgrade: websocket\r\nConnection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
    ).encode("ascii")
    try:
        sock.sendall(request)
        response = b""
        while b"\r\n\r\n" not in response:
            chunk = sock.recv(4096)
            if not chunk:
                raise ConnectionError("WebSocket upgrade closed before headers")
            response += chunk
            if len(response) > 64 * 1024:
                raise ValueError("WebSocket upgrade response is too large")
        if not response.startswith(b"HTTP/1.1 101"):
            raise ConnectionError(f"WebSocket upgrade failed: {response.splitlines()[0]!r}")
    except Exception:
        sock.close()
        raise
    return sock


def _stop_process(process: subprocess.Popen[bytes]) -> bytes:
    """Terminate a Chrome child, escalate if needed, and close stderr once."""

    try:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=1)
            except (OSError, subprocess.TimeoutExpired):
                pass
            if process.poll() is None:
                process.kill()
                try:
                    process.wait(timeout=1)
                except (OSError, subprocess.TimeoutExpired):
                    pass
        stderr_value = process.stderr.read() if process.stderr is not None and not process.stderr.closed else b""
        if isinstance(stderr_value, str):
            return stderr_value.encode("utf-8", errors="replace")
        return stderr_value if isinstance(stderr_value, bytes) else b""
    except (OSError, ValueError):
        return b""
    finally:
        if process.stderr is not None:
            process.stderr.close()


def _bounded_process_error(process: subprocess.Popen[bytes], prefix: str) -> RenderUnavailable:
    stderr = _stop_process(process)
    excerpt = stderr.decode("utf-8", errors="replace")[:2000].strip()
    suffix = f": {excerpt}" if excerpt else ""
    return RenderUnavailable(f"{prefix}{suffix}")


def _page_target(port: int) -> str:
    request = urllib.request.Request(f"http://127.0.0.1:{port}/json", headers={"Cache-Control": "no-cache"})
    with urllib.request.urlopen(request, timeout=2) as response:
        targets = json.loads(response.read().decode("utf-8"))
    for target in targets:
        if target.get("type") == "page" and target.get("webSocketDebuggerUrl"):
            return str(target["webSocketDebuggerUrl"])
    raise RenderUnavailable("Chrome DevTools did not expose a page target")


def launch_cdp(chrome_bin: Path, *, force_reduced_motion: bool) -> CdpSession:
    profile = Path(tempfile.mkdtemp(prefix="visual-eli5-chrome-"))
    command = [
        str(chrome_bin),
        "about:blank",
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        "--remote-debugging-port=0",
        f"--user-data-dir={profile}",
    ]
    if force_reduced_motion:
        command.append("--force-prefers-reduced-motion")
    try:
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except OSError as exc:
        shutil.rmtree(profile, ignore_errors=True)
        raise RenderUnavailable(f"cannot launch Chrome: {exc}") from exc

    active_port = profile / "DevToolsActivePort"
    deadline = time.monotonic() + 5.0
    try:
        port: int | None = None
        while port is None:
            if active_port.exists():
                lines = active_port.read_text(encoding="utf-8").splitlines()
                if len(lines) >= 2 and lines[0].strip().isdigit() and lines[1].strip():
                    port = int(lines[0].strip())
                    break
            if process.poll() is not None:
                raise _bounded_process_error(process, "Chrome exited before DevToolsActivePort appeared")
            if time.monotonic() >= deadline:
                raise _bounded_process_error(process, "Chrome did not expose DevToolsActivePort within 5 seconds")
            time.sleep(0.05)
        target = _page_target(port)
        session = CdpClient(_connect_websocket(target))
        session._process = process
        session._profile = profile
        return session
    except RenderUnavailable:
        _stop_process(process)
        shutil.rmtree(profile, ignore_errors=True)
        raise
    except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError, ConnectionError) as exc:
        _stop_process(process)
        shutil.rmtree(profile, ignore_errors=True)
        raise RenderUnavailable(f"cannot connect to Chrome DevTools: {exc}") from exc


def build_probe_script() -> str:
    """Return the browser-side measurement promise installed before page scripts."""

    return r"""
(function () {
  function nextFrames() {
    return new Promise(function (resolve) {
      requestAnimationFrame(function () {
        requestAnimationFrame(resolve);
      });
    });
  }
  function rectFor(element) {
    var rect = element.getBoundingClientRect();
    return {
      left: rect.left + window.scrollX,
      top: rect.top + window.scrollY,
      right: rect.right + window.scrollX,
      bottom: rect.bottom + window.scrollY,
      width: rect.width,
      height: rect.height
    };
  }
  function sceneCandidates() {
    var marked = Array.prototype.slice.call(document.querySelectorAll('[data-scene]'));
    if (marked.length) return marked;
    var direct = Array.prototype.slice.call(document.querySelectorAll('main > section'));
    if (direct.length) return direct;
    var mains = Array.prototype.slice.call(document.querySelectorAll('main'));
    if (mains.length) return mains;
    var bodySections = Array.prototype.slice.call(document.querySelectorAll('body > section'));
    if (bodySections.length) return bodySections;
    return document.body ? [document.body] : [];
  }
  window.__visualEli5Ready = (async function () {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    await nextFrames();
    var root = document.documentElement;
    var clientWidth = root.clientWidth;
    var scrollWidth = root.scrollWidth;
    var scenes = sceneCandidates().map(function (element, index) {
      var bounds = rectFor(element);
      return Object.assign(bounds, {
        id: element.id || '', ordinal: index + 1
      });
    });
    var clipped = [];
    Array.prototype.slice.call(document.querySelectorAll('body *')).forEach(function (element) {
      if (/^(SCRIPT|STYLE|TEMPLATE)$/.test(element.tagName)) return;
      var text = (element.innerText || element.textContent || '').replace(/\s+/g, ' ').trim();
      if (!text || element.children.length) return;
      var rect = element.getBoundingClientRect();
      if (rect.left < -1 || rect.right > clientWidth + 1) {
        clipped.push({text: text, left: rect.left, right: rect.right, top: rect.top + window.scrollY, bottom: rect.bottom + window.scrollY});
      }
    });
    var viewBoxClipped = [];
    Array.prototype.slice.call(document.querySelectorAll('svg[viewBox] text')).forEach(function (element) {
      var svgRoot = element.ownerSVGElement;
      if (!svgRoot || !svgRoot.viewBox || !svgRoot.viewBox.baseVal) return;
      var vb = svgRoot.viewBox.baseVal;
      if (!vb.width) return;
      var box;
      try { box = element.getBBox(); } catch (err) { return; }
      if (!box || !box.width) return;
      var right = box.x + box.width;
      if (right > vb.width + 0.5 || box.x < -0.5) {
        viewBoxClipped.push({
          text: (element.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60),
          x: Math.round(box.x * 10) / 10,
          right: Math.round(right * 10) / 10,
          viewBoxWidth: vb.width
        });
      }
    });
    var smallText = [];
    Array.prototype.slice.call(document.querySelectorAll('body *')).forEach(function (element) {
      if (/^(SCRIPT|STYLE|TEMPLATE|TITLE|DESC)$/.test(element.tagName)) return;
      var text = (element.innerText || element.textContent || '').replace(/\s+/g, ' ').trim();
      if (!text || element.children.length) return;
      var rect = element.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      var declared = parseFloat(getComputedStyle(element).fontSize) || 0;
      if (!declared) return;
      var rendered = declared;
      var svgRoot = element.ownerSVGElement || null;
      if (svgRoot && svgRoot.viewBox && svgRoot.viewBox.baseVal && svgRoot.viewBox.baseVal.width) {
        rendered = declared * (svgRoot.getBoundingClientRect().width / svgRoot.viewBox.baseVal.width);
      }
      if (rendered < MIN_TEXT_PX) {
        smallText.push({text: text.slice(0, 60), renderedPx: Math.round(rendered * 10) / 10, declaredPx: declared, top: rect.top + window.scrollY});
      }
    });
    var hidden = [];
    Array.prototype.slice.call(document.querySelectorAll('body *')).forEach(function (element) {
      if (/^(SCRIPT|STYLE|TEMPLATE)$/.test(element.tagName)) return;
      var style = getComputedStyle(element);
      if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
        hidden.push({tag: element.tagName.toLowerCase(), id: element.id || '', className: element.className || '', display: style.display, visibility: style.visibility, opacity: style.opacity});
      }
    });
    var animations = (document.getAnimations ? document.getAnimations() : []).filter(function (animation) {
      return animation.playState === 'running';
    }).map(function (animation) {
      return {playState: animation.playState, currentTime: animation.currentTime, type: animation.constructor && animation.constructor.name || 'Animation'};
    });
    var body = document.body;
    var bodyRect = body ? body.getBoundingClientRect() : {right: 0, bottom: 0};
    var width = Math.max(root.scrollWidth, root.clientWidth, bodyRect.right + window.scrollX);
    var height = Math.max(root.scrollHeight, root.clientHeight, bodyRect.bottom + window.scrollY);
    return {
      clientWidth: clientWidth,
      scrollWidth: scrollWidth,
      scrollY: window.scrollY,
      reducedMotionMatched: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      documentBounds: {left: 0, top: 0, right: width, bottom: height, width: width, height: height},
      scenes: scenes,
      horizontallyClippedText: clipped,
      viewBoxClippedText: viewBoxClipped,
      smallText: smallText,
      hiddenBeforeScroll: hidden,
      runningAnimations: animations
    };
  })();
})();
""".strip().replace("MIN_TEXT_PX", str(MIN_RENDERED_TEXT_PX))


def instrument_page(source: str) -> str:
    script = f"<script>{build_probe_script()}</script>"
    head = re.search(r"<head\b[^>]*>", source, flags=re.IGNORECASE)
    if head:
        return source[: head.end()] + script + source[head.end() :]
    return script + source


def safe_scene_filename(scene_id: str, ordinal: int) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", scene_id)
    value = value.lstrip(".") or "scene"
    return f"{ordinal:03d}-{value}"


_SCROLL_COUNTER_SCRIPT = """
(function () {
  window.__visualEli5ScrollY = window.scrollY || 0;
  window.addEventListener('scroll', function () {
    window.__visualEli5ScrollY = window.scrollY || 0;
  }, {passive: true});
})();
""".strip()
_FREEZE_MOTION_SCRIPT = """
(function () {
  var style = document.createElement('style');
  style.setAttribute('data-visual-eli5-freeze', '');
  style.textContent = '* { animation-play-state: paused !important; transition: none !important; }';
  (document.head || document.documentElement).appendChild(style);
  if (document.getAnimations) document.getAnimations().forEach(function (animation) { try { animation.pause(); } catch (_) {} });
  return true;
})();
""".strip()


def _object_value(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        return value
    return {}


def _capture_bytes(value: object) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return base64.b64decode(value)
    if isinstance(value, dict):
        data = value.get("data")
        if isinstance(data, str):
            return base64.b64decode(data)
    raise ValueError("Chrome returned no PNG data")


def _capture_png(session: CdpSession, path: Path, params: dict[str, object]) -> None:
    result = session.call("Page.captureScreenshot", params)
    path.write_bytes(_capture_bytes(result))


def _finding_from_render(code: str, message: str, scope: str) -> Finding:
    return Finding(code, message, "error", scope)


def _report_dict(report: RenderReport) -> dict[str, object]:
    return {
        "output_dir": report.output_dir,
        "browser": report.browser,
        "errors": [
            {"code": item.code, "message": item.message, "severity": item.severity, "scope": item.scope}
            for item in report.errors
        ],
        "viewports": [
            {
                "viewport": {
                    "name": item.viewport.name,
                    "width": item.viewport.width,
                    "height": item.viewport.height,
                },
                "reduced_motion": item.reduced_motion,
                "client_width": item.client_width,
                "scroll_width": item.scroll_width,
                "scene_bounds": item.scene_bounds,
                "horizontally_clipped_text": item.horizontally_clipped_text,
                "small_text": item.small_text,
                "hidden_before_scroll": item.hidden_before_scroll,
                "reduced_motion_matched": item.reduced_motion_matched,
                "running_animations": item.running_animations,
                "screenshots": item.screenshots,
            }
            for item in report.viewports
        ],
    }


def _render_one_viewport(
    session: CdpSession,
    page_url: str,
    output_dir: Path,
    viewport: Viewport,
    *,
    reduced_motion: bool,
    errors: list[Finding],
    capture_overview: bool,
    reports: list[Finding] | None = None,
) -> ViewportReport:
    session.call(
        "Emulation.setDeviceMetricsOverride",
        {
            "width": viewport.width,
            "height": viewport.height,
            "deviceScaleFactor": 1,
            "mobile": viewport.width == PHONE.width,
        },
    )
    session.call("Page.enable")
    session.call("Runtime.enable")
    session.call("Page.addScriptToEvaluateOnNewDocument", {"source": _SCROLL_COUNTER_SCRIPT})
    session.call("Page.navigate", {"url": page_url})
    session.wait_event("Page.loadEventFired", 10)
    session.call("Page.reload", {"ignoreCache": True})
    session.wait_event("Page.loadEventFired", 10)
    measurement = _object_value(session.evaluate("window.__visualEli5Ready", await_promise=True))
    client_width = int(measurement.get("clientWidth", viewport.width) or viewport.width)
    scroll_width = int(measurement.get("scrollWidth", client_width) or client_width)
    if int(measurement.get("scrollY", 0) or 0) != 0:
        errors.append(_finding_from_render("render.scroll-position", "page was measured after scrolling", viewport.name))
    if scroll_width > client_width + 1:
        errors.append(
            _finding_from_render(
                "render.horizontal-overflow",
                f"{viewport.name} scrollWidth {scroll_width} exceeds clientWidth {client_width}",
                viewport.name,
            )
        )
    small_text = [item for item in measurement.get("smallText", []) if isinstance(item, dict)]
    if small_text and not reduced_motion and reports is not None:
        sample = "; ".join(f"{item.get('text', '')!r} at {item.get('renderedPx', '?')}px" for item in small_text[:3])
        reports.append(
            Finding(
                "render.small-text",
                f"{viewport.name} renders {len(small_text)} text node(s) below {MIN_RENDERED_TEXT_PX:g}px: {sample}",
                "report",
                viewport.name,
            )
        )
    clipped = [item for item in measurement.get("horizontallyClippedText", []) if isinstance(item, dict)]
    if clipped:
        errors.append(
            _finding_from_render(
                "render.horizontal-clipping",
                f"{viewport.name} has {len(clipped)} text node(s) outside the viewport",
                viewport.name,
            )
        )
    view_box_clipped = [item for item in measurement.get("viewBoxClippedText", []) if isinstance(item, dict)]
    if view_box_clipped:
        sample = "; ".join(
            f"{item.get('text', '')!r} runs to {item.get('right', '?')} of {item.get('viewBoxWidth', '?')}"
            for item in view_box_clipped[:3]
        )
        errors.append(
            _finding_from_render(
                "render.viewbox-clipping",
                f"{viewport.name} has {len(view_box_clipped)} svg text node(s) cut off by their own viewBox: {sample}",
                viewport.name,
            )
        )
    scenes_raw = [item for item in measurement.get("scenes", []) if isinstance(item, dict)]
    scene_bounds: list[dict[str, object]] = []
    for ordinal, scene in enumerate(scenes_raw, 1):
        original_id = str(scene.get("id", ""))
        scene_id = original_id or f"scene-{ordinal}"
        scene_copy = dict(scene)
        scene_copy["id"] = scene_id
        scene_copy["original_id"] = original_id
        scene_copy["ordinal"] = ordinal
        scene_bounds.append(scene_copy)
    hidden = [item for item in measurement.get("hiddenBeforeScroll", []) if isinstance(item, dict)]
    running = [item for item in measurement.get("runningAnimations", []) if isinstance(item, dict)]
    reduced_match = bool(measurement.get("reducedMotionMatched", False))
    if reduced_motion and (not reduced_match or running):
        errors.append(
            _finding_from_render(
                "render.reduced-motion",
                f"{viewport.name} reduced render requires media match and no running animations",
                viewport.name,
            )
        )
    # Measure first, then freeze motion so every capture in this viewport is
    # deterministic without hiding an initial-state problem from the probe.
    session.evaluate(_FREEZE_MOTION_SCRIPT)
    layout = _object_value(session.call("Page.getLayoutMetrics"))
    content = _object_value(layout.get("contentSize"))
    document_bounds = _object_value(measurement.get("documentBounds"))
    content_width = float(content.get("width", document_bounds.get("width", viewport.width)) or viewport.width)
    content_height = float(content.get("height", document_bounds.get("height", viewport.height)) or viewport.height)
    screenshots: list[str] = []
    if capture_overview:
        overview_name = f"{('reduced-' if reduced_motion else '')}{viewport.name}-overview.png"
        _capture_png(
            session,
            output_dir / overview_name,
            {
                "format": "png",
                "captureBeyondViewport": True,
                "clip": {"x": 0, "y": 0, "width": max(content_width, 1), "height": max(content_height, 1), "scale": 1},
            },
        )
        screenshots.append(overview_name)
    for ordinal, scene in enumerate(scene_bounds, 1):
        width = float(scene.get("width", 0) or 0)
        height = float(scene.get("height", 0) or 0)
        if width <= 0 or height <= 0:
            errors.append(_finding_from_render("render.scene-bounds", f"scene {scene['id']!r} has no captureable bounds", str(scene["id"])))
            continue
        scene_name = safe_scene_filename(str(scene["id"]), ordinal)
        prefix = "reduced-" if reduced_motion else ""
        filename = f"{prefix}{viewport.name}-scene-{scene_name}.png"
        _capture_png(
            session,
            output_dir / filename,
            {
                "format": "png",
                "captureBeyondViewport": True,
                "clip": {
                    "x": float(scene.get("left", 0) or 0),
                    "y": float(scene.get("top", 0) or 0),
                    "width": width,
                    "height": height,
                    "scale": 1,
                },
            },
        )
        screenshots.append(filename)
    return ViewportReport(
        viewport,
        reduced_motion,
        client_width,
        scroll_width,
        scene_bounds,
        clipped,
        hidden,
        reduced_match,
        running,
        screenshots,
        small_text,
    )


def render_page(
    page: Path,
    output_dir: Path,
    chrome_bin: Path | None = None,
    cdp_factory: Callable[..., CdpSession] = launch_cdp,
) -> RenderReport:
    """Run static checks and capture deterministic desktop/phone evidence."""

    source = page.read_text(encoding="utf-8")
    static = check_html_file(page)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "authored-prose.txt").write_text(format_authored_prose(static.authored_prose), encoding="utf-8")
    chosen = chrome_bin or find_chrome()
    if chosen is None:
        raise RenderUnavailable("Chrome was not found; set CHROME_BIN or install Chrome")
    errors = list(static.errors)
    reports = list(static.reports)
    viewports: list[ViewportReport] = []
    reduced_needed = any(use.needs_reduced_capture for use in static.motion.uses)
    with tempfile.TemporaryDirectory(prefix="visual-eli5-render-") as raw:
        instrumented = Path(raw) / "index.html"
        instrumented.write_text(instrument_page(source), encoding="utf-8")
        page_url = instrumented.resolve().as_uri()
        normal_session = cdp_factory(chosen, force_reduced_motion=False)
        try:
            for viewport in (DESKTOP, PHONE):
                viewports.append(
                    _render_one_viewport(
                        normal_session,
                        page_url,
                        output_dir,
                        viewport,
                        reduced_motion=False,
                        errors=errors,
                        capture_overview=True,
                        reports=reports,
                    )
                )
        finally:
            normal_session.close()
        if reduced_needed:
            reduced_session = cdp_factory(chosen, force_reduced_motion=True)
            try:
                for viewport in (DESKTOP, PHONE):
                    viewports.append(
                        _render_one_viewport(
                            reduced_session,
                            page_url,
                            output_dir,
                            viewport,
                            reduced_motion=True,
                            errors=errors,
                            capture_overview=False,
                        )
                    )
            finally:
                reduced_session.close()
    report = RenderReport(str(output_dir), str(chosen), viewports, errors, reports)
    (output_dir / "render-report.json").write_text(json.dumps(_report_dict(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def print_static_report(report: StaticReport, stream: TextIO) -> None:
    for finding in report.errors:
        stream.write(f"OVER {finding.code}: {finding.message}\n")
    for finding in report.reports:
        stream.write(f"REVIEW {finding.code}: {finding.message}\n")
    for scene in report.scenes:
        stream.write(
            f"scene {scene.scene_id}: paragraph_words={scene.paragraph_words} "
            f"sentence_count={scene.sentence_count} "
            f"average_sentence_words={scene.average_sentence_words:.2f} "
            f"longest_paragraph_words={scene.longest_paragraph_words}\n"
        )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check a visual-eli5 HTML page. Exit 0 means no errors (reports may exist), "
            "exit 1 means semantic or density errors, and exit 2 means usage or unreadable input."
        )
    )
    parser.add_argument("--metrics", action="store_true", help="print scene metrics (the default report includes them)")
    parser.add_argument("--prose", action="store_true", help="print authored prose and visual markers in source order")
    parser.add_argument("--render", type=Path, metavar="OUTPUT_DIRECTORY", help="render deterministic Chrome screenshots")
    parser.add_argument("--chrome-bin", type=Path, help="Chrome executable used by --render")
    parser.add_argument("page", type=Path, help="HTML file to check")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # Keep the public entry point usable by callers that invoke main()
        # directly while preserving argparse's normal CLI output.
        return int(exc.code)
    try:
        if args.render is not None:
            output_dir = args.render
            render_report = render_page(args.page, output_dir, args.chrome_bin)
            for finding in render_report.errors:
                print(f"OVER {finding.code}: {finding.message}", file=sys.stdout)
            render_reviews = render_report.reports if isinstance(getattr(render_report, "reports", None), list) else []
            for finding in render_reviews:
                print(f"REVIEW {finding.code}: {finding.message}", file=sys.stdout)
            print(f"render-report: {output_dir / 'render-report.json'}")
            return 1 if render_report.errors else 0
        report = check_html_file(args.page)
    except RenderUnavailable as exc:
        print(f"check-page: render unavailable: {exc}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError) as exc:
        print(f"check-page: cannot read input: {exc}", file=sys.stderr)
        return 2
    if args.prose:
        print(format_authored_prose(report.authored_prose))
    else:
        print_static_report(report, sys.stdout)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
