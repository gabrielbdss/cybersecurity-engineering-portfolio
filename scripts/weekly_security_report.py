#!/usr/bin/env python3
"""Read-only weekly GitHub security overview.

Only aggregate counts/statuses are printed. An API permission error is UNKNOWN,
not a fabricated zero. The job summary is private to the workflow run UI and
no issue, commit or remote write is performed.
"""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ENDPOINTS = [
    ("Code scanning", "code-scanning/alerts?state=open&per_page=100"),
    ("Dependabot", "dependabot/alerts?state=open&per_page=100"),
    ("Secret scanning", "secret-scanning/alerts?state=open&per_page=100"),
]


def fetch_count(repo, token, endpoint):
    if not repo or not token:
        return "UNAVAILABLE (missing authentication)"
    request = Request(
        f"https://api.github.com/repos/{repo}/{endpoint}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "portfolio-weekly-security-report",
        },
    )
    try:
        with urlopen(request, timeout=15) as response:
            data = json.load(response)
        if not isinstance(data, list):
            return "UNKNOWN (unexpected API response)"
        return f">=100 open (API page limit)" if len(data) == 100 else f"{len(data)} open"
    except HTTPError as error:
        return f"UNKNOWN (API HTTP {error.code}; permissions/availability)"
    except (URLError, TimeoutError, ValueError):
        return "UNKNOWN (network or parse failure)"


def main():
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GH_TOKEN", "")
    print("# Weekly Security Assurance — read-only snapshot\n")
    print("Data comes from current GitHub APIs and can be partial due to access limits.\n")
    print("| Data source | Observed status |\n| --- | --- |")
    for label, endpoint in ENDPOINTS:
        print(f"| {label} | {fetch_count(repo, token, endpoint)} |")
    print("\n**Interpretation:** zero open alerts means zero *visible via that API*, not absence of vulnerabilities.")
    print("UNKNOWN is a monitoring gap, **never** a PASS. Review CodeQL, dependency review, the publication guard and Gitleaks job logs individually.")
    print("\nThis workflow does not publish files, create issues, change settings or mutate the repository.")


if __name__ == "__main__":
    main()
