---
name: weekly-log
description: Keep a running log of each project's week in its own file, and turn it into that project's update, due when the week closes on Friday at 10:00. Use whenever work worth reporting lands, is opened for review, or is deferred to a follow-up (a PR merged or opened, a deploy, a decision, a finding, a separate PR agreed), whenever Claude notices a pull request has merged, and when the user says "add this to the weekly log", "what did we do this week", or asks for the weekly update. Also use at the end of a session that produced reportable work.
---

# Weekly Log

Each project keeps its own file per week, so every update is self-contained and goes to its own
audience. A week closes on **Friday at 10:00 local time** (`closes_friday_at` in `config.json`)
and the next one opens at that instant. Files are named for the Friday they close:

`~/sample-project/memory-and-skills/weekly-log/<project slug>/<YYYY-MM-DD of the closing Friday>.md`

For example `weekly-log/sample-project/2026-10-09.md` holds sample-project work from Friday 2 October
10:00 to Friday 9 October 10:00.

## Format

Each file is a summary on top and the raw log below it. The summary is what gets sent.

```markdown
# sample-project, Week Ending 2026-10-09

## Summary

- **Shipped:** per-key hourly rate limits and an audit trail of key changes.
- **Security:** fixed the critical Python package CVEs. In review: LiteLLM 1.93.2 (#413).
- **Decided:** keyless routes are blocked at the edge, not in the app.
- **Next:** add the WAF allow-list and redeploy dev.

## Log

- Next: make the `/login` routes unreachable from the internet (separate PR).
- In review: corrected both deployment plans on keyless routes ([#400](https://example.invalid/project)).
- Merged: ...
```

**Summary.** Three to six one-line bullets, each led by a bold theme (`Shipped`, `Security`,
`Decided`, `Research`, `Next`, or whatever the week was about). Group related PRs into one
outcome instead of listing them, and name a PR number only where the reader may want to follow
it. Plain language for someone who did not watch the work happen. `sync.py` never touches it.

**Log.** The raw record, which `sync.py` reconciles:

- `config.json` maps each repository to its project name; the slug is that name in lower case
  with hyphens. A repository missing from it gets its bare name, so add it when that happens.
- Each bullet opens with its status: `Next`, `Blocked`, `In review`, `Merged`, `Shipped`, `Closed`,
  `Decided` or `Found`. Bullets sort in that order.
- One line per bullet. Say what changed or was decided, not how. No reasoning, statistics or
  file paths unless the point is the number. Link the PR or issue as `[#123](full URL)`.
- Headings are Title Case noun phrases.

## Keeping It Current

Pull requests are tracked by `sync.py`, so nobody has to remember them. For each account in
`config.json` it finds the PRs that account authored that merged or closed this week, or are open
and were active this week, and then:

- adds a bullet to the project's file for any PR it does not mention, worded from the PR title;
- corrects the status word of any bullet whose PR has since merged or closed, which is how an
  outdated log is detected and fixed;
- moves a bullet into the right week's file when its PR closed in another week;
- starts each project's file for a new week, carrying its `Next`, `Blocked` and `In review`
  bullets forward.

`sync.py --week <closing Friday>` syncs a past week.

It never rewrites wording, only the status word before the colon.

When it runs:

- **At the start of every Claude Code session**, from two `SessionStart` hooks in
  `~/.claude/settings.json`. `sync.py --hook` runs in the background, so it never delays a session;
  it syncs at most once every 30 minutes. `sync.py --remind` makes no network call and prints a
  reminder into the session, from Thursday until a day after the close, naming each project
  whose update is unsent. A new machine needs both:

  ```json
  "SessionStart": [{ "hooks": [
    { "type": "command", "shell": "bash", "timeout": 10,
      "command": "python3 ~/sample-project/memory-and-skills/skills/weekly-log/sync.py --remind 2>/dev/null || true" },
    { "type": "command", "shell": "bash", "timeout": 90, "async": true,
      "command": "python3 ~/sample-project/memory-and-skills/skills/weekly-log/sync.py --hook 2>/dev/null || true" }
  ]}]
  ```
- **Whenever Claude sees a PR merge or open**, in any session: run `sync.py` without `--hook`.
- **Before writing an update**: always run `sync.py` first.

Work that is not a PR (decisions, findings, deploys, agreed follow-ups) is added by hand to its
project's log as it happens. After any change to a log, by hand or by `sync.py`, rewrite that
project's summary so it still matches, and delete a `Next` bullet once its work has a PR. Bullets the sync adds are worded from PR titles; tighten any that is not
short and plain when you next touch the file.

## The Weekly Update

Each project's update is due when its week closes, Friday 10:00. From Thursday the `--remind`
hook names the projects still unsent. When asked for an update, or when reminded:

1. Run `python3 ~/sample-project/memory-and-skills/skills/weekly-log/sync.py`.
2. Read each project's file for the week and rewrite its summary from the log, checking every
   status against the log rather than memory.
3. Show each project's summary for approval, separately. The summary is the update; the log stays
   behind as the record. Never send it without a clear yes in chat.
4. After one is sent, run `sync.py --sent <slug>` (or `--sent` for all) so its reminder stops.
5. Commit and push this repository with `scripts/sync.sh`.

Where each project's update is sent is not decided yet. Ask the first time, then write it here.
