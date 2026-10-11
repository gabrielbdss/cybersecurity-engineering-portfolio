#!/usr/bin/env python3
"""Check local Markdown link targets without fetching network resources."""
from pathlib import Path
import re
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def check_links(root):
    """Return invalid (source, href) pairs for ordinary local Markdown links."""
    failures = []
    for source in sorted(root.rglob("*.md")):
        if ".git" in source.parts:
            continue
        in_fence = False
        for line in source.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK.finditer(line):
                href = match.group(1).strip().split(" \"", 1)[0]
                parsed = urlparse(href)
                if not parsed.path or parsed.scheme or parsed.netloc:
                    continue
                if parsed.path.startswith("/"):
                    continue  # Host-relative web paths are not local files.
                target = (source.parent / unquote(parsed.path)).resolve()
                try:
                    target.relative_to(root.resolve())
                except ValueError:
                    failures.append((source.relative_to(root), href))
                    continue
                if not target.exists():
                    failures.append((source.relative_to(root), href))
    return failures


def main():
    failures = check_links(ROOT)
    for source, href in failures:
        print(f"BROKEN: {source} -> {href}")
    print(f"Markdown local link validation: {len(failures)} issue(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
