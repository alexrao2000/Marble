#!/usr/bin/env python3
"""Bring each project's weekly log in line with GitHub.

A week closes on Friday at the time `config.json` sets (local time) and the next one opens at
that instant. Each project keeps its own file per week, `<log_dir>/<project slug>/<closing
Friday>.md`. For every account in config.json, find the pull requests it authored that merged,
closed or were open and active this week, then:

* add a bullet for any that its project's file does not mention,
* correct the status word of any bullet whose pull request has since changed state,
* move a bullet whose pull request closed in a different week into that week's file,
* start a project's file for the new week, carrying its Next, Blocked and In review bullets,
  so open work stays visible until it merges or closes.

Hand-written wording is never rewritten; only the status word before the colon changes.

    python3 sync.py                    # sync this week and print what changed
    python3 sync.py --week 2026-10-02  # sync the week that closes on that Friday
    python3 sync.py --hook             # SessionStart: rate-limited, silent when nothing changed
    python3 sync.py --remind           # no network: say which projects' updates are due and unsent
    python3 sync.py --sent [slug ...]  # mark the due week's update as sent, for all or some projects
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
CLOSE_HOUR, CLOSE_MINUTE = (int(part) for part in CONFIG["closes_friday_at"].split(":"))
STAMP = LOG_DIR / ".last-sync"
HOOK_INTERVAL_SECONDS = 30 * 60
REMIND_BEFORE = dt.timedelta(hours=34)  # from Thursday 00:00 when the week closes Friday 10:00
REMIND_AFTER = dt.timedelta(hours=24)  # keep reminding for a day if the deadline slipped
SENT_MARKER = "<!-- sent -->"

# Order of bullets in a file.
RANK = ["Next", "Blocked", "In review", "Merged", "Shipped", "Closed", "Decided", "Found"]
PR_STATUSES = {"In review", "Merged", "Closed"}
CARRIED = {"Next", "Blocked", "In review"}
BULLET = re.compile(r"^- ([A-Z][a-z]+(?: [a-z]+)?): ")
PR_LINK = re.compile(r"https://github\.com/([^/\s]+/[^/\s]+)/pull/(\d+)")


# ---------------------------------------------------------------- weeks


def week_end(moment: dt.datetime) -> dt.datetime:
    """The Friday close strictly after `moment`: the end of the week `moment` falls in."""
    friday = moment.date() + dt.timedelta(days=(4 - moment.weekday()) % 7)
    close = dt.datetime.combine(friday, dt.time(CLOSE_HOUR, CLOSE_MINUTE)).astimezone()
    return close if close > moment else close + dt.timedelta(days=7)


def week_end_on(friday: dt.date) -> dt.datetime:
    return dt.datetime.combine(friday, dt.time(CLOSE_HOUR, CLOSE_MINUTE)).astimezone()


def now() -> dt.datetime:
    return dt.datetime.now().astimezone()


# ---------------------------------------------------------------- projects and files


def project_name(repo: str) -> str:
    return CONFIG["projects"].get(repo, repo.split("/")[-1])


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def log_path(project: str, end: dt.datetime) -> Path:
    return LOG_DIR / slug(project) / f"{end.date().isoformat()}.md"


def project_dirs() -> list[Path]:
    return sorted(p for p in LOG_DIR.iterdir() if p.is_dir() and not p.name.startswith("."))


def status_of(bullet: str) -> str | None:
    match = BULLET.match(bullet)
    return match.group(1) if match else None


def pr_key(bullet: str) -> tuple[str, int] | None:
    match = PR_LINK.search(bullet)
    return (match.group(1), int(match.group(2))) if match else None


class Log:
    """One project's week: a title, its bullets, and whether the update has been sent."""

    def __init__(self, path: Path, project: str, end: dt.datetime):
        self.path = path
        self.title = f"# {project}, Week Ending {end.date().isoformat()}"
        self.bullets: list[str] = []
        self.sent = False
        self.existed = path.exists()
        if not self.existed:
            return
        for line in path.read_text().splitlines():
            if line.startswith("# "):
                self.title = line
            elif line.strip() == SENT_MARKER:
                self.sent = True
            elif line.startswith("  ") and self.bullets:
                self.bullets[-1] += " " + line.strip()  # rejoin a wrapped bullet
            elif line.startswith("- "):
                self.bullets.append(line)

    def find(self, key: tuple[str, int]) -> int | None:
        for i, bullet in enumerate(self.bullets):
            if pr_key(bullet) == key:
                return i
        return None

    def save(self) -> None:
        if not self.bullets and not self.existed:
            return
        ordered = sorted(
            self.bullets, key=lambda b: RANK.index(status_of(b)) if status_of(b) in RANK else len(RANK)
        )
        text = "\n".join([self.title, "", *ordered]) + "\n"
        if self.sent:
            text += f"\n{SENT_MARKER}\n"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(text)


def open_log(project: str, end: dt.datetime, changes: list[str]) -> Log:
    """This project's file for the week, started from the previous week's open bullets if new."""
    path = log_path(project, end)
    log = Log(path, project, end)
    if log.existed:
        return log
    earlier = sorted(p for p in path.parent.glob("????-??-??.md") if p.stem < path.stem)
    if earlier:
        previous = Log(earlier[-1], project, end)
        log.bullets = [b for b in previous.bullets if status_of(b) in CARRIED]
        if log.bullets:
            changes.append(f"started {slug(project)}/{path.name}")
    return log


# ---------------------------------------------------------------- GitHub


def gh_search(account: str, *qualifiers: str) -> list[dict]:
    token = subprocess.run(
        ["gh", "auth", "token", "--user", account], capture_output=True, text=True
    ).stdout.strip()
    if not token:
        raise RuntimeError(f"gh has no token for {account}; run: gh auth login")
    env = {**os.environ, "GH_TOKEN": token}
    result = subprocess.run(
        ["gh", "search", "prs", "--author", "@me", *qualifiers, "--limit", "100",
         "--json", "repository,number,title,url,state,closedAt"],
        capture_output=True, text=True, env=env, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh search failed for {account}: {result.stderr.strip()}")
    return json.loads(result.stdout or "[]")


def moment(timestamp: str) -> dt.datetime:
    return dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone()


def pull_requests(start: dt.datetime) -> dict[tuple[str, int], dict]:
    """PRs open and active since `start`, or closed since `start`, keyed by (repo, number)."""
    since = (start - dt.timedelta(days=1)).date().isoformat()  # a day of slack for time zones
    found: dict[tuple[str, int], dict] = {}
    for account in CONFIG["accounts"]:
        for pr in gh_search(account, "--state", "open", "--updated", f">={since}"):
            found[(pr["repository"]["nameWithOwner"], pr["number"])] = {**pr, "status": "In review"}
        for pr in gh_search(account, "--state", "closed", "--closed", f">={since}"):
            status = "Merged" if pr["state"] == "merged" else "Closed"
            found[(pr["repository"]["nameWithOwner"], pr["number"])] = {
                **pr, "status": status, "closed": moment(pr["closedAt"])
            }
    return found


def short_title(title: str) -> str:
    """Drop bracketed prefixes like "[sample-project]" and lower the first word unless it is an acronym."""
    title = re.sub(r"^(\[[^\]]*\]\s*)+", "", title).strip().rstrip(".")
    first = title.split(" ", 1)[0]
    if first[:1].isupper() and first[1:2].islower():
        title = title[0].lower() + title[1:]
    return title


# ---------------------------------------------------------------- sync


def sync(end: dt.datetime) -> list[str]:
    start = end - dt.timedelta(days=7)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    changes: list[str] = []
    logs: dict[Path, Log] = {}

    def log_for(project: str, week: dt.datetime) -> Log:
        path = log_path(project, week)
        if path not in logs:
            logs[path] = open_log(project, week, changes)
        return logs[path]

    for directory in project_dirs():  # carry open work into weeks with no PR activity yet
        names = {slug(n): n for n in CONFIG["projects"].values()}
        log_for(names.get(directory.name, directory.name), end)

    for key, pr in sorted(pull_requests(start).items()):
        repo, number = key
        project = project_name(repo)
        closed = pr.get("closed")
        if closed is not None and closed >= end:
            continue  # belongs to a later week
        week = end if closed is None or closed >= start else week_end(closed)
        target = log_for(project, week)
        current = log_for(project, end)
        if week != end and (i := current.find(key)) is not None:
            bullet = current.bullets.pop(i)
            if target.find(key) is None:
                target.bullets.append(bullet)
            changes.append(f"moved #{number} to {slug(project)}/{week.date().isoformat()}.md")
        i = target.find(key)
        if i is not None:
            bullet = target.bullets[i]
            was = status_of(bullet)
            if was in PR_STATUSES and was != pr["status"]:
                target.bullets[i] = f"- {pr['status']}: " + bullet[len(f"- {was}: "):]
                changes.append(f"#{number} {was} -> {pr['status']}")
            continue
        if week != end:
            continue  # do not add to past weeks while syncing this one
        target.bullets.append(f"- {pr['status']}: {short_title(pr['title'])} ([#{number}]({pr['url']})).")
        changes.append(f"added #{number} ({pr['status']}) to {slug(project)}")

    for log in logs.values():
        log.save()
    return changes


# ---------------------------------------------------------------- reminders and sending


def due_week(at: dt.datetime) -> dt.datetime | None:
    """The week whose update is due now: this one from Thursday, or last one for a day after."""
    end = week_end(at)
    if end - at <= REMIND_BEFORE:
        return end
    previous = end - dt.timedelta(days=7)
    if at - previous <= REMIND_AFTER:
        return previous
    return None


def unsent(end: dt.datetime) -> list[Log]:
    found = []
    for directory in project_dirs():
        path = directory / f"{end.date().isoformat()}.md"
        if path.exists():
            log = Log(path, directory.name, end)
            if log.bullets and not log.sent:
                found.append(log)
    return found


def main(argv: list[str]) -> int:
    at = now()
    if "--remind" in argv:
        end = due_week(at)
        pending = unsent(end) if end else []
        if pending:
            names = ", ".join(log.path.parent.name for log in pending)
            print(f"Weekly update for the week closing {end:%a %d %b %H:%M} is not sent yet for: "
                  f"{names}. Use the weekly-log skill.")
        return 0
    if "--sent" in argv:
        end = due_week(at) or week_end(at)
        wanted = set(argv[argv.index("--sent") + 1:])
        for log in unsent(end):
            if not wanted or log.path.parent.name in wanted:
                log.sent = True
                log.save()
                print(f"Marked {log.path.parent.name}/{log.path.name} as sent.")
        return 0
    if "--week" in argv:
        end = week_end_on(dt.date.fromisoformat(argv[argv.index("--week") + 1]))
    else:
        end = week_end(at)
    hook = "--hook" in argv
    if hook and STAMP.exists() and time.time() - STAMP.stat().st_mtime < HOOK_INTERVAL_SECONDS:
        return 0
    try:
        changes = sync(end)
    except Exception as error:  # a hook must never block a session
        print(f"Weekly log sync failed: {error}", file=sys.stderr)
        return 0 if hook else 1
    if "--week" not in argv:
        STAMP.touch()
    if changes:
        print(f"Weekly log, week closing {end.date().isoformat()}: " + "; ".join(changes) + ".")
    elif not hook:
        print(f"Weekly log, week closing {end.date().isoformat()}: up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
