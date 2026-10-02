#!/usr/bin/env python3
"""Bring the week's log in line with GitHub.

For every account in config.json, find the pull requests it authored that merged, closed or
were open and active this week, then:

* add a bullet for any that the log does not mention,
* correct the status word of any bullet whose pull request has since changed state,
* start a new week's file when none exists, carrying the last week's Next, Blocked and In review
  bullets, so open work stays visible until it merges or closes.

Hand-written wording is never rewritten; only the status word before the colon changes.

    python3 sync.py            # sync and print what changed
    python3 sync.py --hook     # for a SessionStart hook: rate-limited, silent when nothing changed
    python3 sync.py --remind   # no network: print the Thursday reminder if the update is unsent
    python3 sync.py --sent     # mark this week's update as sent
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = json.loads((HERE / "config.json").read_text())
LOG_DIR = Path(CONFIG["log_dir"]).expanduser()
STAMP = LOG_DIR / ".last-sync"
HOOK_INTERVAL_SECONDS = 30 * 60
SENT_MARKER = "<!-- sent -->"

# Order of bullets inside a project section.
RANK = ["Next", "Blocked", "In review", "Merged", "Shipped", "Closed", "Decided", "Found"]
PR_STATUSES = {"In review", "Merged", "Closed"}
BULLET = re.compile(r"^- ([A-Z][a-z]+(?: [a-z]+)?): ")
PR_LINK = re.compile(r"https://github\.com/([^/\s]+/[^/\s]+)/pull/(\d+)")


def week_bounds(today: dt.date) -> tuple[dt.date, dt.date]:
    """The Friday that starts this week and the Thursday that ends it."""
    start = today - dt.timedelta(days=(today.weekday() - 4) % 7)
    return start, start + dt.timedelta(days=6)


def log_path(thursday: dt.date) -> Path:
    return LOG_DIR / f"{thursday.isoformat()}.md"


def gh_search(account: str, *qualifiers: str) -> list[dict]:
    token = subprocess.run(
        ["gh", "auth", "token", "--user", account], capture_output=True, text=True
    ).stdout.strip()
    if not token:
        raise RuntimeError(f"gh has no token for {account}; run: gh auth login")
    env = {**os.environ, "GH_TOKEN": token}
    result = subprocess.run(
        ["gh", "search", "prs", "--author", "@me", *qualifiers, "--limit", "100",
         "--json", "repository,number,title,url,state,closedAt,isDraft"],
        capture_output=True, text=True, env=env, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh search failed for {account}: {result.stderr.strip()}")
    return json.loads(result.stdout or "[]")


def local_date(timestamp: str | None) -> dt.date | None:
    if not timestamp:
        return None
    return dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone().date()


def this_weeks_pull_requests(start: dt.date, end: dt.date) -> dict[tuple[str, int], dict]:
    """Every pull request the log should mention, keyed by (repo, number), with its status."""
    since = (start - dt.timedelta(days=1)).isoformat()  # one day of slack for time zones
    found: dict[tuple[str, int], dict] = {}
    for account in CONFIG["accounts"]:
        for pr in gh_search(account, "--state", "open", "--updated", f">={since}"):
            found[(pr["repository"]["nameWithOwner"], pr["number"])] = {**pr, "status": "In review"}
        for pr in gh_search(account, "--state", "closed", "--closed", f">={since}"):
            closed = local_date(pr["closedAt"])
            if closed is None or not start <= closed <= end:
                continue
            status = "Merged" if pr["state"] == "merged" else "Closed"
            found[(pr["repository"]["nameWithOwner"], pr["number"])] = {**pr, "status": status}
    return found


def project_name(repo: str) -> str:
    return CONFIG["projects"].get(repo, repo.split("/")[-1])


def short_title(title: str) -> str:
    """Drop bracketed prefixes like "[sample-project]" and lower the first word unless it is an acronym."""
    title = re.sub(r"^(\[[^\]]*\]\s*)+", "", title).strip().rstrip(".")
    first = title.split(" ", 1)[0]
    if first[:1].isupper() and first[1:2].islower():
        title = title[0].lower() + title[1:]
    return title


class Log:
    """The week's file as a title, an ordered list of sections, and a tail of other lines."""

    def __init__(self, text: str):
        self.head: list[str] = []
        self.sections: dict[str, list[str]] = {}
        current = None
        for line in text.splitlines():
            if line.startswith("## "):
                current = line[3:].strip()
                self.sections.setdefault(current, [])
            elif current is None:
                self.head.append(line)
            elif line.strip():
                bullets = self.sections[current]
                if line.startswith("  ") and bullets:
                    bullets[-1] += " " + line.strip()  # rejoin a wrapped bullet
                else:
                    bullets.append(line)

    def render(self) -> str:
        out = [line for line in self.head]
        while out and not out[-1].strip():
            out.pop()
        for name, bullets in self.sections.items():
            ordered = sorted(bullets, key=lambda b: RANK.index(status_of(b)) if status_of(b) in RANK else len(RANK))
            out += ["", f"## {name}", ""] + ordered
        return "\n".join(out) + "\n"

    def find(self, repo: str, number: int) -> tuple[str, int] | None:
        for name, bullets in self.sections.items():
            for i, bullet in enumerate(bullets):
                for match in PR_LINK.finditer(bullet):
                    if match.group(1) == repo and int(match.group(2)) == number:
                        return name, i
        return None


def status_of(bullet: str) -> str | None:
    match = BULLET.match(bullet)
    return match.group(1) if match else None


def new_week(thursday: dt.date) -> str:
    """Header, plus the open bullets carried from the latest earlier week."""
    text = f"# Week Ending {thursday.isoformat()}\n"
    earlier = sorted(p for p in LOG_DIR.glob("????-??-??.md") if p.stem < thursday.isoformat())
    if not earlier:
        return text
    previous = Log(earlier[-1].read_text())
    carried = Log(text)
    for name, bullets in previous.sections.items():
        kept = [b for b in bullets if status_of(b) in {"Next", "Blocked", "In review"}]
        if kept:
            carried.sections[name] = kept
    return carried.render()


def sync(today: dt.date) -> list[str]:
    start, thursday = week_bounds(today)
    path = log_path(thursday)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    changes: list[str] = []
    if not path.exists():
        path.write_text(new_week(thursday))
        changes.append(f"started {path.name}")
    log = Log(path.read_text())
    for (repo, number), pr in sorted(this_weeks_pull_requests(start, thursday).items()):
        where = log.find(repo, number)
        if where:
            name, i = where
            bullet = log.sections[name][i]
            current = status_of(bullet)
            if current in PR_STATUSES and current != pr["status"]:
                log.sections[name][i] = f"- {pr['status']}: " + bullet[len(f"- {current}: "):]
                changes.append(f"#{number} {current} -> {pr['status']}")
            continue
        project = project_name(repo)
        log.sections.setdefault(project, []).append(
            f"- {pr['status']}: {short_title(pr['title'])} ([#{number}]({pr['url']}))."
        )
        changes.append(f"added #{number} ({pr['status']}, {project})")
    path.write_text(log.render())
    return changes


def main(argv: list[str]) -> int:
    today = dt.date.today()
    _, thursday = week_bounds(today)
    path = log_path(thursday)
    if "--sent" in argv:
        path.write_text(path.read_text().rstrip("\n") + f"\n\n{SENT_MARKER}\n")
        print(f"Marked {path.name} as sent.")
        return 0
    if "--remind" in argv:
        if today == thursday and not (path.exists() and SENT_MARKER in path.read_text()):
            print("It is Thursday and this week's update has not been sent. Use the weekly-log skill.")
        return 0
    hook = "--hook" in argv
    if hook and STAMP.exists() and time.time() - STAMP.stat().st_mtime < HOOK_INTERVAL_SECONDS:
        return 0
    try:
        changes = sync(today)
    except Exception as error:  # a hook must never block a session
        print(f"Weekly log sync failed: {error}", file=sys.stderr)
        return 0 if hook else 1
    STAMP.touch()
    if changes:
        print(f"Weekly log {path}: " + "; ".join(changes) + ".")
    elif not hook:
        print(f"Weekly log {path}: up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
