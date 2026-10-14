"""Fetch the public RSS feeds of the Mon and Burmese editions of IMNA and Thanlwin Times.

Pilot scope only: the feeds expose the ten or so most recent posts per edition. The full
archives are not crawled until the outlets reply to the permission requests sent 2026-10-14.
Output: data/raw/<outlet>.<lang>.jsonl with one post per line (title, link, date, text).
Note: monnews.org sits behind a bot filter that returns 403 to scripts; its feeds are saved by
hand from a browser into data/raw/ when needed (see README).
"""
from __future__ import annotations

import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEEDS = {
    ("imna", "mnw"): "https://mon.monnews.org/feed/",
    ("imna", "my"): "https://burmese.monnews.org/feed/",
    ("thanlwin", "mnw"): "https://mon.thanlwintimes.com/?feed=rss2",
    ("thanlwin", "my"): "https://burmese.thanlwintimes.com/?feed=rss2",
}
NS = {"content": "http://purl.org/rss/1.0/modules/content/", "dc": "http://purl.org/dc/elements/1.1/"}
OUT = Path(__file__).resolve().parent / "data" / "raw"


def strip_html(s: str) -> str:
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>|</p>|</div>|</h\d>|</li>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t ]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36", "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for (outlet, lang), url in FEEDS.items():
        try:
            root = ET.fromstring(fetch(url))
        except Exception as e:  # noqa: BLE001
            print(f"{outlet}.{lang}: FAILED {e}")
            continue
        rows = []
        for item in root.iter("item"):
            title = strip_html(item.findtext("title") or "")
            link = (item.findtext("link") or "").strip()
            date = (item.findtext("pubDate") or "").strip()
            body = item.findtext("content:encoded", namespaces=NS) or item.findtext("description") or ""
            rows.append({"outlet": outlet, "lang": lang, "title": title, "link": link, "date": date, "text": strip_html(body)})
        path = OUT / f"{outlet}.{lang}.jsonl"
        path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
        full = sum(1 for r in rows if len(r["text"]) > 600)
        print(f"{outlet}.{lang}: {len(rows)} posts, {full} with full text, median chars {sorted(len(r['text']) for r in rows)[len(rows)//2] if rows else 0}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
