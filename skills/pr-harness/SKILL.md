---
name: pr-harness
description: >-
  Build a throwaway UI harness for the current branch's change: one HTML page that drives the
  real changed code (headless modules, services, API handlers) with inputs, live output, an event
  log and one-click edge cases, so the feature can be tried by hand. It lives in .harness/<branch>/,
  ignored through .git/info/exclude so it never reaches the repo. Use when the SessionStart hook
  says a branch has no harness or a stale one, when a PR is opened or its branch gets new commits,
  and when the user asks to try, poke at, see or test a change by hand. Always end by giving the
  user the one command that opens it.
---

# Throwaway UI harness per branch

## Why this exists

Headless code changes behaviour without changing anything on screen, so a PR is reviewed by
reading state transitions in your head. A harness puts the changed behaviour behind buttons. It
is disposable by design: generated per branch, never committed, rebuilt when the branch moves.

## Setup

Symlink this directory into `~/.claude/skills/`, and add `check.sh` to the `SessionStart` hooks
in `~/.claude/settings.json`:

```json
{ "type": "command", "shell": "bash", "timeout": 10,
  "command": "<path-to-this-repo>/skills/pr-harness/check.sh 2>/dev/null || true" }
```

## The one rule

**The harness drives the real code. It never reimplements it.** A page that mimics the feature
tests the mimic. Import the changed modules, call the changed functions, hit the changed
endpoints. Where something genuinely cannot run locally (a cluster, a paid API, a production
database), stub only that boundary, and label every stub on the page so nobody mistakes it for
the real thing.

## Steps

### 1. Find the change

```bash
top=$(git rev-parse --show-toplevel)
branch=$(git symbolic-ref --short HEAD); slug=${branch//\//-}
default=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null); default=${default#origin/}
base=$(git merge-base HEAD "origin/${default:-main}")
git diff "$base" --stat
```

Read the diff and the PR description if one exists (`gh pr view`). Write down, for yourself, each
behaviour the change adds or alters: the inputs, what should come out, and the edge cases the
diff or its tests handle (errors, empty input, limits, retries, ordering, concurrency).

If nothing in the diff is runnable behaviour (docs, CI config, dependency bumps, pure deletions),
write the reason to `.harness/<slug>/SKIP` and stop. The hook stays quiet for that branch.

### 2. Keep it out of git

```bash
exclude="$(git rev-parse --git-common-dir)/info/exclude"
grep -qxF '.harness/' "$exclude" 2>/dev/null || echo '.harness/' >> "$exclude"
```

Never add it to `.gitignore` and never commit anything under `.harness/`. `info/exclude` is local
to the clone and shared by all its worktrees.

### 3. Pick the mode

**Static**: the changed code runs in a browser (TS/JS with no Node-only, filesystem or server
dependencies). Write `.harness/<slug>/entry.ts` that imports the real modules from the repo and
wires them to the page. Bundle it with the repo's own esbuild if it has one, otherwise
`npx --yes esbuild@0.25.0`, as `--bundle --format=iife`, and inline the output into a `<script>`
in `index.html` so the page is a single file that works from `file://`. The open command is:

```bash
open .harness/<slug>/index.html
```

**Served**: everything else, which in practice means Python, backend services and API handlers.
Write `.harness/<slug>/serve.py` using only the standard library (`http.server`, `json`,
`webbrowser`):

- `GET /` serves `index.html` from its own folder.
- `POST /call/<name>` takes JSON, calls the real function imported from the repo, and returns its
  result, or the exception type, message and traceback as JSON. Put the repo root on `sys.path`.
- If the change is an HTTP endpoint and the service has a dev server, proxy `/api/*` to it instead
  of importing, so the page stays same-origin and needs no CORS. Print a clear message when the
  dev server is not up, with the command that starts it.
- Bind `127.0.0.1` on a free port, print the URL and call `webbrowser.open` on it.
- Support `--check`: import everything the harness calls, then exit 0 without serving.

Run it with the interpreter the repo uses (`uv run python`, the project venv, `poetry run`). The
open command is that invocation, from the repo root:

```bash
uv run python .harness/<slug>/serve.py
```

### 4. Build the page

One `index.html`, no CDN dependencies, readable in light and dark (`prefers-color-scheme`).

- Header: branch, the short SHA it was built at, the PR link if there is one, and which mode.
- One panel per behaviour from step 1: a form for its inputs with realistic defaults, a run
  button, and the output rendered readably (tables for lists, pretty JSON for objects, errors in
  red with the message first).
- For stateful code (stores, state machines, sessions, queues): a live view of the current state
  and an event log of every action and transition, with a reset button.
- A row of preset buttons per panel that load the edge cases from step 1. Reuse fixtures from the
  repo's tests where they exist rather than inventing data.
- A visible "stubbed" badge on anything that is not the real implementation.

Keep it plain HTML, CSS and a small script. It is throwaway; it should be quick to regenerate,
not polished.

### 5. Prove it loads

Static: the bundle builds without errors. Served: `serve.py --check` exits 0. Then exercise at
least one panel end to end yourself: for served mode, start the server in the background, `curl`
one `/call/` or `/api/` route, and stop it. Local port binding or `open` may be blocked by the
Bash sandbox; that is the sandbox, not the harness. Do not open the page for the user.

Write the short SHA to `.harness/<slug>/BUILT_AT`. The SessionStart hook compares it to `HEAD`
and asks for a rebuild when the branch has moved.

### 6. Hand it over

End with a sentence or two on what the page covers and anything stubbed, then the open command
from step 3 in its own `bash` block, with the real slug filled in and nothing else in the block.

## Housekeeping

- **Rebuilding**: regenerate from the current diff rather than patching the old page, unless the
  change since `BUILT_AT` is small. Overwrite in place.
- **Old harnesses**: if `.harness/` holds folders for branches that no longer exist locally
  (`git branch --list`), list them in your summary and offer to delete them. Don't delete
  unasked.
- **Signal to make one permanent**: if an older folder in `.harness/` drives the same module
  this one does, say so. A module that keeps getting a harness deserves a committed playground or
  story, and that decision belongs to the user.
