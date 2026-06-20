#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request


def fetch(url: str, timeout: int) -> tuple[int, dict[str, str], bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Codex-Aliyun-Static-Site-Deploy/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read(2_000_000)
        final_url = resp.geturl()
        return resp.status, dict(resp.headers.items()), body, final_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a public static site URL.")
    parser.add_argument("url")
    parser.add_argument("--contains", help="Required text expected in the HTML body.")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    try:
        status, headers, body, final_url = fetch(args.url, args.timeout)
    except urllib.error.HTTPError as exc:
        print(f"ERROR: HTTP {exc.code} for {args.url}")
        print(exc.read(1000).decode("utf-8", "replace"))
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    content_type = headers.get("Content-Type", "")
    disposition = headers.get("Content-Disposition", "")
    text = body.decode("utf-8", "replace")
    title_match = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
    title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""

    errors: list[str] = []
    if status >= 400:
        errors.append(f"bad status: {status}")
    if "<Error>" in text[:1000] or "<Code>" in text[:1000]:
        errors.append("response looks like an Aliyun XML error")
    if "<html" not in text.lower()[:20000]:
        errors.append("response does not look like HTML")
    if "attachment" in disposition.lower():
        errors.append("Content-Disposition is attachment; browser may download the page")
    if content_type and all(token not in content_type.lower() for token in ["text/html", "application/xhtml"]):
        errors.append(f"Content-Type is not HTML: {content_type}")
    if args.contains and args.contains not in text:
        errors.append(f"missing required text: {args.contains}")

    print(f"URL: {args.url}")
    print(f"Final URL: {final_url}")
    print(f"Status: {status}")
    print(f"Content-Type: {content_type or '(missing)'}")
    print(f"Content-Disposition: {disposition or '(missing)'}")
    print(f"Title: {title or '(missing)'}")
    print(f"Bytes checked: {len(body)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("OK: public URL is serving an HTML page")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
