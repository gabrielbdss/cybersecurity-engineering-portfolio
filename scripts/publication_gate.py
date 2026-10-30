#!/usr/bin/env python3
"""Conservative public-portfolio disclosure guard.

No network calls, no access to secrets, and no printing of matching values.
This gate supplements (does not replace) manual review and Gitleaks.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

CTF_ROOT = Path("case-studies/08-operation-cymbal-cold-room")
CTF_ALLOWED = {"README.md", "README.pt-BR.md", "methodology.md", "DISCLOSURE.md"}
FORBIDDEN_BASENAMES = {".env", "credentials.json", "token.json", "id_rsa", "id_ed25519"}
FORBIDDEN_SUFFIXES = {".pem", ".p12", ".pfx", ".key", ".evtx", ".pcap", ".pcapng", ".har", ".sqlite", ".sqlite3"}
TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".xml", ".html", ".js", ".ts", ".ps1"}
SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", ".venv", "node_modules"}
MAX_BYTES = 2_000_000
SENSITIVE_MARKERS = [
    ("private-key-block", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("github-classic-token", re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}")),
    ("google-api-key", re.compile(r"AIza[A-Za-z0-9_-]{35}")),
    ("slack-token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}")),
]


def inspect(root: Path) -> list[tuple[str, str]]:
    """Return only file paths and issue categories, never captured secret values."""
    root = root.resolve()
    findings: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.is_symlink():
            findings.append((rel.as_posix(), "symlink-needs-manual-review"))
            continue
        if not path.is_file():
            continue

        rel_str = rel.as_posix()
        try:
            within_ctf = rel.is_relative_to(CTF_ROOT)
        except AttributeError:
            within_ctf = rel == CTF_ROOT or CTF_ROOT in rel.parents

        # Full allowlist: adding new material to the active/embargoed CTF case fails closed.
        if within_ctf and rel.name not in CTF_ALLOWED:
            findings.append((rel_str, "ctf-unapproved-file"))
            continue
        if within_ctf and rel.parent != CTF_ROOT:
            findings.append((rel_str, "ctf-unapproved-nested-file"))
            continue

        if path.name.lower() in FORBIDDEN_BASENAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append((rel_str, "restricted-file-type"))
            continue

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            if path.stat().st_size > MAX_BYTES:
                findings.append((rel_str, "large-text-file-needs-review"))
                continue
            data = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            findings.append((rel_str, "unreadable-text-file"))
            continue
        for rule, expression in SENSITIVE_MARKERS:
            if expression.search(data):
                findings.append((rel_str, rule))
    return findings


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print("Publication Gate: invalid repository root")
        return 2
    findings = inspect(root)
    if findings:
        print("Publication Gate: FAIL (only path/category shown; no secret values)")
        for path, rule in findings:
            print(f"  {path}: {rule}")
        return 1
    print("Publication Gate: PASS (automated patterns only; human review still required)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
