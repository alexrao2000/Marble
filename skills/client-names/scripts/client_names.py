#!/usr/bin/env python3
"""Keep client names out of repositories they do not belong in.

The list lives beside this script in ../names.json, inside Marble,
so it travels to every machine that syncs that repository.

Commands:
  add NAME --client C [--kind K] [--allow-remote PATTERN]   record a name
  remove NAME                                                forget a name
  allow PATTERN --client C                                   allow a remote for a client
  list                                                       print the list
  scan-text FILE --remote URL                                check text before posting it
  scan-push REMOTE_NAME URL < refs                           the pre-push hook entry point
  install                                                    point git at the hooks and link the skill

add, remove and allow commit names.json and run scripts/sync.sh, so the change
reaches every machine. Pass --no-sync to skip that.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
LIST_PATH = SKILL_DIR / "names.json"
REPO_DIR = SKILL_DIR.parent.parent
HOOKS_DIR = SKILL_DIR / "hooks"
ZERO = "0" * 40
KINDS = {"company", "org", "person", "agent", "product", "identifier", "other"}


# --- the list -----------------------------------------------------------------


def load(path: Path = LIST_PATH) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("clients"), list):
        raise ValueError(f"{path}: expected version 1 with a clients list")
    data.setdefault("allowed_everywhere", [])
    for c in data["clients"]:
        c.setdefault("allowed_remotes", [])
        c.setdefault("names", [])
    return data


def save(data: dict, path: Path = LIST_PATH) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".names.", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def client_entry(data: dict, client: str, create: bool) -> dict | None:
    for c in data["clients"]:
        if c["client"].casefold() == client.casefold():
            return c
    if not create:
        return None
    c = {"client": client, "allowed_remotes": [], "names": []}
    data["clients"].append(c)
    return c


def sync(message: str) -> None:
    rel = LIST_PATH.relative_to(REPO_DIR)
    subprocess.run(["git", "-C", str(REPO_DIR), "add", "--", str(rel)], check=True)
    staged = subprocess.run(
        ["git", "-C", str(REPO_DIR), "diff", "--cached", "--quiet", "--", str(rel)]
    )
    if staged.returncode == 0:
        return
    subprocess.run(
        ["git", "-C", str(REPO_DIR), "commit", "-q", "-m", message, "--", str(rel)],
        check=True,
    )
    result = subprocess.run([str(REPO_DIR / "scripts" / "sync.sh")])
    if result.returncode != 0:
        print(
            "client-names: committed locally, but sync.sh refused; run it again "
            "once the working tree is clean",
            file=sys.stderr,
        )


# --- matching -----------------------------------------------------------------


@dataclass(frozen=True)
class Term:
    text: str
    client: str
    kind: str
    pattern: re.Pattern[str]


def terms_for(data: dict, remote: str) -> list[Term]:
    """The names that must not appear in a push or post to this remote."""
    norm = normalize_remote(remote)
    if any(fnmatch.fnmatch(norm, p) for p in data["allowed_everywhere"]):
        return []
    out = []
    for c in data["clients"]:
        if any(fnmatch.fnmatch(norm, p) for p in c["allowed_remotes"]):
            continue
        for n in c["names"]:
            text = n["text"]
            pattern = re.compile(
                r"(?<![A-Za-z0-9])" + re.escape(text) + r"(?![A-Za-z0-9])",
                re.IGNORECASE,
            )
            out.append(Term(text, c["client"], n.get("kind", "other"), pattern))
    return out


def normalize_remote(url: str) -> str:
    """git@github.com-alias:org/repo.git, https://github.com/org/repo -> github.com/org/repo."""
    u = url.strip()
    u = re.sub(r"^[a-z+]+://", "", u)
    u = re.sub(r"^[^@/]+@", "", u)
    u = u.replace(":", "/", 1) if re.match(r"^[^/]+:", u) else u
    u = re.sub(r"\.git/?$", "", u).rstrip("/")
    host, _, rest = u.partition("/")
    host = re.sub(r"^github\.com-.*$", "github.com", host)
    return f"{host}/{rest}" if rest else host


@dataclass(frozen=True)
class Hit:
    where: str
    term: Term
    line: str


def scan_lines(where: str, lines, terms: list[Term]) -> list[Hit]:
    hits = []
    for line in lines:
        for t in terms:
            if t.pattern.search(line):
                hits.append(Hit(where, t, line.strip()[:160]))
    return hits


# --- git ------------------------------------------------------------------------


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True, errors="replace"
    ).stdout


def commits_to_push(local_sha: str, remote_sha: str) -> list[str]:
    if remote_sha != ZERO:
        try:
            return git("rev-list", local_sha, f"^{remote_sha}").split()
        except subprocess.CalledProcessError:
            pass  # remote tip unknown locally; fall back to everything not on a remote
    return git("rev-list", local_sha, "--not", "--remotes").split()


def scan_commit(sha: str, terms: list[Term]) -> list[Hit]:
    short = sha[:8]
    hits = scan_lines(f"{short} commit message", git("log", "-1", "--format=%B", sha).splitlines(), terms)
    paths = git("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", sha).splitlines()
    hits += scan_lines(f"{short} file path", paths, terms)
    current = "?"
    added = []
    for line in git("diff-tree", "--root", "--no-commit-id", "-r", "-p", "-U0", "--no-color", sha).splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else line[4:]
        elif line.startswith("+") and not line.startswith("+++"):
            added.append((current, line[1:]))
    for path, text in added:
        hits += scan_lines(f"{short} {path}", [text], terms)
    return hits


def report(hits: list[Hit], target: str) -> None:
    print(f"\nclient-names: blocked. Client names would reach {target}:\n", file=sys.stderr)
    for h in hits:
        print(f"  {h.where}: '{h.term.text}' ({h.term.client}, {h.term.kind})", file=sys.stderr)
        print(f"      {h.line}", file=sys.stderr)
    print(
        "\nRemove them and amend the commit(s). If a name is wrongly listed, run\n"
        f"  {Path(__file__)} remove '<name>'\n"
        "If this remote may hold that client's names, run\n"
        f"  {Path(__file__)} allow '<host/org/*>' --client '<client>'\n",
        file=sys.stderr,
    )


# --- commands -------------------------------------------------------------------


def cmd_scan_push(args) -> int:
    data = load()
    terms = terms_for(data, args.url)
    if not terms:
        return 0
    hits: list[Hit] = []
    seen: set[str] = set()
    for line in sys.stdin:
        parts = line.split()
        if len(parts) != 4:
            continue
        _local_ref, local_sha, _remote_ref, remote_sha = parts
        if local_sha == ZERO:
            continue  # deleting a branch pushes no content
        for sha in commits_to_push(local_sha, remote_sha):
            if sha not in seen:
                seen.add(sha)
                hits += scan_commit(sha, terms)
    if hits:
        report(hits, normalize_remote(args.url))
        return 1
    return 0


def cmd_scan_text(args) -> int:
    terms = terms_for(load(), args.remote)
    text = Path(args.file).read_text(encoding="utf-8", errors="replace") if args.file != "-" else sys.stdin.read()
    hits = scan_lines(args.file, text.splitlines(), terms)
    if hits:
        report(hits, normalize_remote(args.remote))
        return 1
    print("client-names: clean")
    return 0


def cmd_add(args) -> int:
    kind = args.kind or "other"
    if kind not in KINDS:
        raise SystemExit(f"kind must be one of {sorted(KINDS)}")
    text = args.name.strip()
    if len(text) < 3:
        raise SystemExit("a name must be at least three characters; short tokens match too much")
    data = load()
    for c in data["clients"]:
        for n in c["names"]:
            if n["text"].casefold() == text.casefold():
                print(f"client-names: '{text}' is already listed under {c['client']}")
                return 0
    c = client_entry(data, args.client, create=True)
    c["names"].append({"text": text, "kind": kind})
    for pattern in args.allow_remote or []:
        if pattern not in c["allowed_remotes"]:
            c["allowed_remotes"].append(pattern)
    save(data)
    print(f"client-names: recorded '{text}' ({kind}) for {c['client']}")
    if not args.no_sync:
        sync(f"Record a {kind} name for {c['client']}")
    return 0


def cmd_remove(args) -> int:
    data = load()
    removed = False
    for c in data["clients"]:
        before = len(c["names"])
        c["names"] = [n for n in c["names"] if n["text"].casefold() != args.name.strip().casefold()]
        removed |= len(c["names"]) != before
    if not removed:
        print(f"client-names: '{args.name}' is not listed")
        return 0
    save(data)
    print(f"client-names: removed '{args.name}'")
    if not args.no_sync:
        sync("Remove a client name")
    return 0


def cmd_allow(args) -> int:
    data = load()
    c = client_entry(data, args.client, create=False)
    if c is None:
        raise SystemExit(f"no client named {args.client}")
    if args.pattern not in c["allowed_remotes"]:
        c["allowed_remotes"].append(args.pattern)
        save(data)
        print(f"client-names: {c['client']} names may now go to {args.pattern}")
        if not args.no_sync:
            sync(f"Allow a remote for {c['client']}")
    return 0


def cmd_list(_args) -> int:
    data = load()
    print("allowed everywhere:", ", ".join(data["allowed_everywhere"]) or "-")
    for c in data["clients"]:
        print(f"\n{c['client']}  (allowed: {', '.join(c['allowed_remotes']) or 'nowhere'})")
        for n in c["names"]:
            print(f"  {n['kind']:<11} {n['text']}")
    return 0


def cmd_install(_args) -> int:
    current = subprocess.run(
        ["git", "config", "--global", "--get", "core.hooksPath"], capture_output=True, text=True
    ).stdout.strip()
    if current and Path(current).resolve() != HOOKS_DIR.resolve():
        print(
            f"client-names: core.hooksPath is already {current}; not overwriting it.\n"
            f"Add a call to {HOOKS_DIR / 'pre-push'} from that hook instead.",
            file=sys.stderr,
        )
        return 1
    subprocess.run(["git", "config", "--global", "core.hooksPath", str(HOOKS_DIR)], check=True)
    for base in (Path.home() / ".claude" / "skills",):
        base.mkdir(parents=True, exist_ok=True)
        link = base / SKILL_DIR.name
        if link.is_symlink() or link.exists():
            if link.resolve() == SKILL_DIR:
                continue
            print(f"client-names: {link} exists and is not this skill; left alone", file=sys.stderr)
            continue
        link.symlink_to(SKILL_DIR)
    print(f"client-names: git hooks now run from {HOOKS_DIR}")
    print(f"client-names: skill linked into ~/.claude/skills")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("name")
    a.add_argument("--client", required=True)
    a.add_argument("--kind")
    a.add_argument("--allow-remote", action="append")
    a.add_argument("--no-sync", action="store_true")
    a.set_defaults(fn=cmd_add)

    r = sub.add_parser("remove")
    r.add_argument("name")
    r.add_argument("--no-sync", action="store_true")
    r.set_defaults(fn=cmd_remove)

    al = sub.add_parser("allow")
    al.add_argument("pattern")
    al.add_argument("--client", required=True)
    al.add_argument("--no-sync", action="store_true")
    al.set_defaults(fn=cmd_allow)

    sub.add_parser("list").set_defaults(fn=cmd_list)

    st = sub.add_parser("scan-text")
    st.add_argument("file", help="file to check, or - for stdin")
    st.add_argument("--remote", required=True, help="where the text is going, e.g. github.com/sample-project/sample-project")
    st.set_defaults(fn=cmd_scan_text)

    sp = sub.add_parser("scan-push")
    sp.add_argument("remote_name")
    sp.add_argument("url")
    sp.set_defaults(fn=cmd_scan_push)

    sub.add_parser("install").set_defaults(fn=cmd_install)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
