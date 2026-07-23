#!/usr/bin/env python3
"""Audit Draw.io sources for structural, MathJax, and vector-asset problems."""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
import urllib.parse
import zlib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


MATH_SPAN_RE = re.compile(r"\\\((?:.|\n)*?\\\)|\\\[(?:.|\n)*?\\\]")
TAG_RE = re.compile(r"<[^>]+>")
RASTER_DATA_RE = re.compile(
    r"data:image/(?:png|jpe?g|webp|gif)", re.IGNORECASE
)
RASTER_PATH_RE = re.compile(
    r"(?:file:/+|https?://|image=)[^;\"'<>\s]*\.(?:png|jpe?g|webp|gif)"
    r"(?:[?#][^;\"'<>\s]*)?",
    re.IGNORECASE,
)
SVG_DATA_RE = re.compile(
    r"data:image/svg\+xml(?:;base64)?,([^;\"'<>\s]+)",
    re.IGNORECASE,
)
SVG_RASTER_HREF_RE = re.compile(
    r"(?:href|xlink:href)\s*=\s*[\"'][^\"']*\.(?:png|jpe?g|webp|gif)"
    r"(?:[?#][^\"']*)?[\"']",
    re.IGNORECASE,
)
FAKE_MATH_RULES = (
    ("HTML subscript/superscript", re.compile(r"<\s*/?\s*(?:sub|sup)\b", re.I)),
    (
        "plain Unicode math operator",
        re.compile(
            r"[\u00b1\u00d7\u03a3\u2208\u2209\u2211\u222b\u221a"
            r"\u2264\u2265\u2286\u21d2\u21a6]"
        ),
    ),
    ("plain dimension", re.compile(r"\b\d+\s*(?:x|X|\u00d7)\s*\d+\b")),
)


@dataclass(frozen=True)
class Issue:
    severity: str
    page: str
    cell: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "page": self.page,
            "cell": self.cell,
            "message": self.message,
        }


def decode_diagram(diagram: ET.Element) -> ET.Element:
    """Return the mxGraphModel for compressed or uncompressed Draw.io pages."""
    for child in diagram:
        if child.tag.endswith("mxGraphModel"):
            return child

    payload = (diagram.text or "").strip()
    if not payload:
        raise ValueError("diagram page contains no mxGraphModel or compressed payload")

    try:
        compressed = base64.b64decode(payload)
        inflated = zlib.decompress(compressed, -15).decode("utf-8")
        xml_text = urllib.parse.unquote(inflated)
        model = ET.fromstring(xml_text)
    except Exception as exc:  # pragma: no cover - exact codec error is platform-specific
        raise ValueError(f"cannot decode compressed Draw.io page: {exc}") from exc

    if not model.tag.endswith("mxGraphModel"):
        raise ValueError(f"decoded page root is {model.tag}, not mxGraphModel")
    return model


def load_pages(path: Path) -> list[tuple[str, ET.Element]]:
    tree = ET.parse(path)
    root = tree.getroot()

    if root.tag.endswith("mxGraphModel"):
        return [(path.stem, root)]
    if not root.tag.endswith("mxfile"):
        raise ValueError(f"root element is {root.tag}, expected mxfile or mxGraphModel")

    pages: list[tuple[str, ET.Element]] = []
    diagrams = [child for child in root if child.tag.endswith("diagram")]
    for index, diagram in enumerate(diagrams, start=1):
        page_name = diagram.get("name") or f"page-{index}"
        pages.append((page_name, decode_diagram(diagram)))
    if not pages:
        raise ValueError("mxfile contains no diagram pages")
    return pages


def remove_math_spans(value: str) -> str:
    return MATH_SPAN_RE.sub("", value)


def visible_text(value: str) -> str:
    return TAG_RE.sub(" ", html.unescape(value))


def raster_in_svg_data(text: str) -> bool:
    decoded = urllib.parse.unquote(html.unescape(text))
    if RASTER_DATA_RE.search(decoded) or RASTER_PATH_RE.search(decoded):
        return True

    for match in SVG_DATA_RE.finditer(decoded):
        payload = urllib.parse.unquote(match.group(1))
        if payload.lstrip().startswith("<"):
            svg_text = payload
        else:
            try:
                svg_text = base64.b64decode(payload, validate=True).decode(
                    "utf-8", errors="ignore"
                )
            except Exception:
                continue
        if RASTER_DATA_RE.search(svg_text) or SVG_RASTER_HREF_RE.search(svg_text):
            return True
    return False


def geometry_has_point(cell: ET.Element, side: str) -> bool:
    point_name = f"{side}Point"
    for node in cell.iter():
        if node.tag.endswith("mxPoint") and node.get("as") == point_name:
            return True
    return False


def audit_page(
    page_name: str,
    model: ET.Element,
    require_math: bool,
) -> list[Issue]:
    issues: list[Issue] = []
    cells = [node for node in model.iter() if node.tag.endswith("mxCell")]
    ids = [cell.get("id") for cell in cells if cell.get("id")]
    id_set = set(ids)

    duplicates = sorted(
        cell_id for cell_id, count in Counter(ids).items() if count > 1
    )
    for duplicate in duplicates:
        issues.append(Issue("error", page_name, duplicate, "duplicate mxCell id"))

    if require_math and model.get("math") != "1":
        issues.append(
            Issue("error", page_name, "-", 'mxGraphModel must set math="1"')
        )

    for cell in cells:
        cell_id = cell.get("id") or "(missing-id)"
        parent = cell.get("parent")
        source = cell.get("source")
        target = cell.get("target")
        value = cell.get("value") or ""
        style = cell.get("style") or ""

        if not cell.get("id"):
            issues.append(Issue("error", page_name, cell_id, "mxCell is missing an id"))

        if parent and parent not in id_set:
            issues.append(
                Issue("error", page_name, cell_id, f"missing parent reference: {parent}")
            )
        for endpoint_name, endpoint in (("source", source), ("target", target)):
            if endpoint and endpoint not in id_set:
                issues.append(
                    Issue(
                        "error",
                        page_name,
                        cell_id,
                        f"missing {endpoint_name} reference: {endpoint}",
                    )
                )

        if cell.get("edge") == "1":
            has_source = bool(source) or geometry_has_point(cell, "source")
            has_target = bool(target) or geometry_has_point(cell, "target")
            if not has_source or not has_target:
                missing = "source" if not has_source else "target"
                issues.append(
                    Issue(
                        "warning",
                        page_name,
                        cell_id,
                        f"edge has no attached or fixed {missing} endpoint",
                    )
                )

        contains_math = bool(MATH_SPAN_RE.search(value))
        if contains_math and model.get("math") != "1":
            issues.append(
                Issue(
                    "error",
                    page_name,
                    cell_id,
                    'MathJax label exists but mxGraphModel math is not "1"',
                )
            )

        non_math = remove_math_spans(value)
        for label, pattern in FAKE_MATH_RULES:
            if pattern.search(non_math):
                snippet = visible_text(non_math).strip().replace("\n", " ")[:80]
                issues.append(
                    Issue(
                        "warning",
                        page_name,
                        cell_id,
                        f"{label} outside MathJax: {snippet!r}",
                    )
                )

        if raster_in_svg_data(value) or raster_in_svg_data(style):
            issues.append(
                Issue(
                    "error",
                    page_name,
                    cell_id,
                    "embedded raster image found; use Draw.io primitives or vector SVG",
                )
            )

    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit a .drawio file for graph integrity, true MathJax, and vector-only assets."
    )
    parser.add_argument("drawio", type=Path, help="path to the .drawio source")
    parser.add_argument(
        "--require-math",
        action="store_true",
        help='require math="1" even when no MathJax label is detected',
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return failure when warnings are present",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print machine-readable JSON",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.drawio.is_file():
        print(f"error: file not found: {args.drawio}", file=sys.stderr)
        return 2

    try:
        pages = load_pages(args.drawio)
    except (ET.ParseError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    issues: list[Issue] = []
    for page_name, model in pages:
        issues.extend(audit_page(page_name, model, args.require_math))

    errors = sum(issue.severity == "error" for issue in issues)
    warnings = sum(issue.severity == "warning" for issue in issues)

    if args.json:
        print(
            json.dumps(
                {
                    "file": str(args.drawio),
                    "pages": len(pages),
                    "errors": errors,
                    "warnings": warnings,
                    "issues": [issue.as_dict() for issue in issues],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    else:
        for issue in issues:
            print(
                f"{issue.severity.upper()}: "
                f"[{issue.page}] cell={issue.cell}: {issue.message}"
            )
        print(
            f"Audited {len(pages)} page(s): {errors} error(s), {warnings} warning(s)."
        )

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
