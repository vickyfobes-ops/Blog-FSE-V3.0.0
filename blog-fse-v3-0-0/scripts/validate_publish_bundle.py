#!/usr/bin/env python3
"""Validate the lightweight Codex-to-Shopify article bundle."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


FORBIDDEN_TAGS = {"script", "style", "iframe", "form", "object", "embed"}
ALLOWED_TAGS = {
    "h2", "h3", "p", "ul", "ol", "li", "strong", "em", "a", "figure",
    "img", "figcaption", "blockquote", "table", "thead", "tbody", "tr",
    "th", "td", "br", "hr",
}


class BodyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[str] = []
        self.links: list[dict[str, str]] = []
        self.images: list[tuple[str, str]] = []
        self.unsafe: list[str] = []
        self._current_link: dict[str, str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self.tags.append(tag)
        attr_map = {key.lower(): (value or "") for key, value in attrs}
        if tag in FORBIDDEN_TAGS or tag not in ALLOWED_TAGS:
            self.unsafe.append(f"unsupported tag <{tag}>")
        for key, value in attr_map.items():
            if key.startswith("on"):
                self.unsafe.append(f"inline event handler {key}")
            if key in {"href", "src"} and value.strip().lower().startswith("javascript:"):
                self.unsafe.append(f"javascript URL in {key}")
        if tag == "a":
            self._current_link = {
                "href": attr_map.get("href", ""),
                "title": attr_map.get("title", ""),
                "style": attr_map.get("style", ""),
                "text": "",
            }
        if tag == "img":
            self.images.append((attr_map.get("src", ""), attr_map.get("alt", "")))

    def handle_data(self, data: str) -> None:
        if self._current_link is not None:
            self._current_link["text"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._current_link is not None:
            self.links.append(self._current_link)
            self._current_link = None


def word_count(markdown: str) -> int:
    text = re.sub(r"<!--.*?-->", "", markdown, flags=re.S)
    text = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.M)
    text = re.sub(r"!\[[^\]]*\]\([^\)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    return len(re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*", text))


def internal_url(url: str, domain: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower().removeprefix("www.")
    target = domain.lower().removeprefix("www.")
    return parsed.scheme in {"http", "https"} and host == target


def product_url(url: str, domain: str) -> bool:
    if not internal_url(url, domain):
        return False
    path = urlparse(url).path.rstrip("/")
    return path.startswith("/products/") and len(path.split("/")) == 3


def black_underlined(style: str) -> bool:
    normalized = re.sub(r"\s+", "", style.lower())
    return "color:#111111" in normalized and "text-decoration:underline" in normalized


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, type=Path)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--domain", required=True)
    args = parser.parse_args()

    root = args.dir.expanduser().resolve()
    required = {
        "English Markdown": root / f"{args.slug}.md",
        "Chinese Markdown": root / f"{args.slug}.zh-CN.md",
        "Chinese Word review": root / f"{args.slug}.zh-CN.review.docx",
        "Shopify HTML": root / f"{args.slug}.shopify.html",
        "Metadata": root / f"{args.slug}.meta.json",
        "Review": root / f"{args.slug}.review.md",
    }
    errors: list[str] = []
    warnings: list[str] = []
    for label, path in required.items():
        if not path.is_file():
            errors.append(f"missing {label}: {path}")
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1

    english = required["English Markdown"].read_text(encoding="utf-8")
    html = required["Shopify HTML"].read_text(encoding="utf-8")
    try:
        meta = json.loads(required["Metadata"].read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"ERROR: invalid metadata JSON: {exc}")
        return 1

    if meta.get("siteId") != "finest-sculpture":
        errors.append("metadata siteId must be finest-sculpture")
    shopify = meta.get("shopify", {})
    if not isinstance(shopify, dict) or shopify.get("targetBlog") != "News":
        errors.append("metadata shopify.targetBlog must be News")

    words = word_count(english)
    target = int(meta.get("targetWords", 1200))
    minimum = max(900, int(target * 0.9))
    maximum = max(minimum, int(target * 1.35))
    if words < minimum:
        errors.append(f"English body has {words} words; minimum is {minimum}")
    if words > maximum:
        warnings.append(f"English body has {words} words; target is {target}")

    h1_count = len(re.findall(r"^#\s+", english, flags=re.M))
    h2s = re.findall(r"^##\s+(.+?)\s*$", english, flags=re.M)
    if h1_count != 1:
        errors.append(f"expected exactly one H1, found {h1_count}")
    if len(h2s) < 2 or h2s[-2] != "Sources and Technical References":
        errors.append("Sources and Technical References must immediately precede FAQ")
    if not h2s or h2s[-1] != "Frequently Asked Questions":
        errors.append("Frequently Asked Questions must be the final H2")
    faq_start = english.rfind("## Frequently Asked Questions")
    faq_count = len(re.findall(r"^###\s+", english[faq_start:], flags=re.M)) if faq_start >= 0 else 0
    if faq_count != 5:
        errors.append(f"FAQ must contain exactly five H3 questions, found {faq_count}")

    body = BodyParser()
    body.feed(html)
    errors.extend(body.unsafe)
    internal_link_items = [item for item in body.links if internal_url(item["href"], args.domain)]
    internal_links = sorted({item["href"] for item in internal_link_items})
    product_links = sorted({item["href"] for item in internal_link_items if product_url(item["href"], args.domain)})
    non_product_links = sorted(set(internal_links) - set(product_links))
    if non_product_links:
        errors.append("selected-site internal links must be direct product pages: " + ", ".join(non_product_links))
    if len(product_links) < 2:
        errors.append(f"expected at least two distinct product links, found {len(product_links)}")
    for item in internal_link_items:
        if product_url(item["href"], args.domain):
            anchor = item["text"].strip()
            if not anchor or anchor.lower() in {"click here", "learn more", "view product"} or anchor.startswith("http"):
                errors.append(f"product link must use descriptive anchor text: {item['href']}")
            if not black_underlined(item["style"]):
                errors.append(f"product link must be black and underlined: {item['href']}")
    if len(body.images) != 6:
        errors.append(f"expected exactly six HTML images, found {len(body.images)}")
    for index, (src, alt) in enumerate(body.images, start=1):
        if not src:
            errors.append(f"image {index} has no src")
        if not alt.strip():
            errors.append(f"image {index} has no alt text")

    image_dir = root / "images"
    local_images = [
        path for path in image_dir.glob("*")
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ] if image_dir.is_dir() else []
    if len(local_images) != 6:
        errors.append(f"expected exactly six local image files, found {len(local_images)}")

    seo = meta.get("seo", {})
    seo_title = str(seo.get("title", ""))
    meta_description = str(seo.get("metaDescription", ""))
    if not 45 <= len(seo_title) <= 60:
        errors.append(f"SEO title length must be 45-60, found {len(seo_title)}")
    if not 140 <= len(meta_description) <= 160:
        errors.append(f"meta description length must be 140-160, found {len(meta_description)}")

    sources = meta.get("researchSources", [])
    if not isinstance(sources, list) or len(sources) < 3:
        errors.append("metadata must contain at least three research sources")
    links = meta.get("internalLinks", [])
    verified_meta_links = {
        str(item.get("url", "")) for item in links
        if isinstance(item, dict)
        and item.get("verified") is True
        and item.get("type") == "commercial"
        and product_url(str(item.get("url", "")), args.domain)
    } if isinstance(links, list) else set()
    if len(verified_meta_links) < 2:
        errors.append("metadata must contain at least two verified commercial product links")
    if not verified_meta_links.issubset(set(product_links)):
        errors.append("every verified metadata product link must appear in Shopify HTML")

    review = meta.get("review", {})
    if not isinstance(review, dict) or review.get("status") != "approved":
        errors.append("metadata review.status must be approved before upload")

    image_plan = meta.get("imagePlan", [])
    if not isinstance(image_plan, list) or len(image_plan) != 6:
        errors.append("metadata imagePlan must contain exactly six entries")

    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARNING: {item}")
        return 1

    print(f"PASS: {args.slug}")
    print(f"English words: {words}")
    print(f"Product links: {len(product_links)}")
    print(f"Images: {len(body.images)}")
    print(f"Sources: {len(sources)}")
    for item in warnings:
        print(f"WARNING: {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
