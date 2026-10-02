---
name: weekly-log
description: Keep a running log of the week's work, grouped by project, and turn it into the update sent every Thursday. Use whenever work worth reporting lands, is opened for review, or is deferred to a follow-up (a PR merged or opened, a deploy, a decision, a finding, a separate PR agreed), whenever Claude notices a pull request has merged, and when the user says "add this to the weekly log", "what did we do this week", or asks for the Thursday update. Also use at the end of a session that produced reportable work.
---

# Weekly Log

One file per week, sent every Thursday. A week runs Friday to Thursday, and the file is named
for its Thursday:

`~/sample-project/memory-and-skills/weekly-log/<YYYY-MM-DD of that Thursday>.md`

## Format

```markdown
# Week Ending 2026-10-08

## sample-project

- Next: make the `/login` routes unreachable from the internet (separate PR).
- In review: corrected both deployment plans on keyless routes ([#400](https://example.invalid/project)).
- Merged: ...
- Decided: ...

## sample-project

- ...
```

- One `##` section per project. `config.json` maps each repository to its project name; a
  repository missing from it gets its bare name, so add it to `config.json` when that happens.
- Each bullet opens with its status: `Next`, `Blocked`, `In review`, `Merged`, `Shipped`, `Closed`,
  `Decided` or `Found`. Bullets sort in that order within a section.
- One line per bullet. Say what changed or was decided, not how. No reasoning, statistics or
  file paths unless the point is the number. Link the PR or issue as `[#123](full URL)`.
- Headings are Title Case noun phrases.

## Keeping It Current

Pull requests are tracked by `sync.py`, so nobody has to remember them. For each account in
`config.json` it finds the PRs that account authored that merged or closed this week, or are open
and were active this week, and then:

- adds a bullet for any the log does not mention, worded from the PR title;
- corrects the status word of any bullet whose PR has since merged or closed, which is how an
  outdated log is detected and fixed;
- starts a new week's file when none exists, carrying the last week's `Next`, `Blocked` and
  `In review` bullets forward.

It never rewrites wording, only the status word before the colon.

When it runs:

- **At the start of every Claude Code session**, from two `SessionStart` hooks in
  `~/.claude/settings.json`. `sync.py --hook` runs in the background, so it never delays a session;
  it syncs at most once every 30 minutes. `sync.py --remind` makes no network call and prints the
  Thursday reminder into the session when the week's update is unsent. A new machine needs both:

  ```json
  "SessionStart": [{ "hooks": [
    { "type": "command", "shell": "bash", "timeout": 10,
      "command": "python3 ~/sample-project/memory-and-skills/skills/weekly-log/sync.py --remind 2>/dev/null || true" },
    { "type": "command", "shell": "bash", "timeout": 90, "async": true,
      "command": "python3 ~/sample-project/memory-and-skills/skills/weekly-log/sync.py --hook 2>/dev/null || true" }
  ]}]
  ```
- **Whenever Claude sees a PR merge or open**, in any session: run `sync.py` without `--hook`.
- **Before the Thursday update**: always run `sync.py` first.

Work that is not a PR (decisions, findings, deploys, agreed follow-ups) is added by hand under
its project as it happens. Bullets the sync adds are worded from PR titles; tighten any that is not
short and plain when you next touch the file.

## The Thursday Update

On Thursday the `--remind` hook adds a reminder to every session until the update is marked sent.
When asked for the update, or when reminded:

1. Run `python3 ~/sample-project/memory-and-skills/skills/weekly-log/sync.py`.
2. Read the week's file. Reword auto-added bullets so each is one short line, merge duplicates,
   and cut anything that is not news to the reader.
3. Show the result for approval. Never send it without a clear yes in chat.
4. After it is sent, run `sync.py --sent` so the reminder stops.
5. Commit and push this repository with `scripts/sync.sh`.

Where the update is sent is not decided yet. Ask the first time, then write the answer here.
