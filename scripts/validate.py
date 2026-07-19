#!/usr/bin/env python3
"""Static validation for the Corpus Balear portal — standard library only.

Run locally with `python3 scripts/validate.py`; CI runs the same script.
Checks structural/SEO invariants that are cheap to verify without a browser:
html sanity, JSON-LD validity, internal-anchor resolution, relative-asset
existence, and consistency between the project cards and the JSON-LD graph.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

WEB = Path(__file__).resolve().parent.parent / "web"
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


class Portal(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.srcs: list[str] = []
        self.card_links: list[str] = []
        self.h1 = 0
        self.lang: str | None = None
        self.has_title = False
        self.has_canonical = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = {k: (v or "") for k, v in attrs}
        if "id" in d:
            self.ids.add(d["id"])
        if tag == "html":
            self.lang = d.get("lang")
        if tag == "title":
            self.has_title = True
        if tag == "h1":
            self.h1 += 1
        if tag == "link" and d.get("rel") == "canonical":
            self.has_canonical = True
        if "href" in d:
            self.hrefs.append(d["href"])
            if tag == "a" and ({"card", "featured"} & set(d.get("class", "").split())):
                self.card_links.append(d["href"])
        if "src" in d:
            self.srcs.append(d["src"])


def is_relative(url: str) -> bool:
    return not re.match(r"^(https?:|data:|mailto:|tel:|#|//)", url)


def main() -> int:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    p = Portal()
    p.feed(html)

    if p.lang != "ca":
        err(f"<html lang> should be 'ca', got {p.lang!r}")
    if p.h1 != 1:
        err(f"expected exactly one <h1>, found {p.h1}")
    if not p.has_title:
        err("missing <title>")
    if not p.has_canonical:
        err("missing <link rel=canonical>")

    # JSON-LD parses
    data = None
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if not m:
        err("missing JSON-LD block")
    else:
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            err(f"JSON-LD does not parse: {e}")

    # Internal anchors resolve
    for h in p.hrefs:
        if h.startswith("#") and h[1:] and h[1:] not in p.ids:
            err(f"internal anchor {h} has no matching id")

    # Relative assets exist on disk
    for url in [*p.hrefs, *p.srcs]:
        if is_relative(url):
            target = WEB / url.split("?")[0].split("#")[0]
            if not target.exists():
                err(f"referenced asset not found: {url}")

    # Cards and JSON-LD hasPart list the same project URLs
    if data:
        parts: list[str] = []
        for node in data.get("@graph", []):
            for hp in node.get("hasPart", []) or []:
                if "url" in hp:
                    parts.append(hp["url"])
        cards, jsonld = set(p.card_links), set(parts)
        for missing in sorted(cards - jsonld):
            err(f"card link missing from JSON-LD hasPart: {missing}")
        for missing in sorted(jsonld - cards):
            err(f"JSON-LD hasPart URL has no matching card: {missing}")

    # sitemap.xml is well-formed; robots.txt points to it
    try:
        ET.parse(WEB / "sitemap.xml")
    except ET.ParseError as e:
        err(f"sitemap.xml is not valid XML: {e}")
    if "Sitemap:" not in (WEB / "robots.txt").read_text(encoding="utf-8"):
        err("robots.txt has no 'Sitemap:' line")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        return 1

    print("Portal validation passed")
    print(f"  ids={len(p.ids)}  hrefs={len(p.hrefs)}  cards={len(p.card_links)}  hasPart matches cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
