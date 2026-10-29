---
name: client-names
description: Use whenever a conversation, file, Slack thread, issue or document names a client of the user's company, or a person, product, agent, org or identifier that belongs to a client. Records the name so a git hook blocks it from reaching any repository that is not that client's. Also use before posting any PR description, issue, or comment to a repository, to check the text for client names.
---

# Client Names

Keep a client's names out of every repository that is not the client's own.

The private list is `.private/client-names.json` at this repository's root, or the path
set by `MARBLE_CLIENT_NAMES_PATH`. It stays local and ignored. The versioned `names.json`
is an empty template. A global git pre-push hook reads the local list and refuses a push that would carry a listed
name to a remote the client is not allowed on. The script is `scripts/client_names.py`.

## Recording a name

Record a name as soon as you are confident it is a client's. Do not wait to be told.

A name is a client's when the context says it belongs to the customer rather than to the user's
own company. Strong signals:

- It is the customer's company, its GitHub org, or a product or brand it owns.
- A person is described as working for the client: "the client's IT", "their CFO",
  "sample-project's approver", someone listed under "waiting on the client", or someone whose email
  domain is the client's.
- An agent, bot, or deliverable was built for that client and carries its name or its
  people's names.
- A channel, account, tenant, or ticket id that identifies the client's work.

Not a client's name:

- The user's own colleagues, even when they work on the client's project.
- Vendors and tools the client happens to use (QuickBooks, SharePoint, Okta).
- Placeholder or planted test names that are made up.
- Common words and common first names on their own. Record a full name ("Chris Tanaka"),
  not "Chris". The script refuses anything under three characters.

When a name is ambiguous, record it only if the context makes the client connection explicit.
Otherwise ask one short question.

Run from this skill's directory:

```bash
scripts/client_names.py add "<name>" --client "<client>" --kind <company|org|person|agent|product|identifier|other>
```

A new client also needs the remotes that may hold its names, usually its own GitHub org:

```bash
scripts/client_names.py add "<name>" --client "<client>" --kind company --allow-remote "github.com/<client-org>/*"
```

Each change saves the local private list. Never commit the list, its names, or its account
mappings to this repository, and never add an exemption for this personal repository.

## Before posting text to a repository

Git hooks do not see PR descriptions, issues, or comments. Before `gh pr create`, `gh pr edit`,
`gh issue create`, or any comment, write the text to a file and check it:

```bash
scripts/client_names.py scan-text <file> --remote github.com/<org>/<repo>
```

A non-zero exit means a client name is in the text. Rewrite it; do not post it.

## When the hook blocks a push

The hook prints each hit: the commit, where it is, and which name matched. Remove the name,
amend or rewrite the commit, and push again.

- Never push with `--no-verify` to get past this hook. If a hit is wrong, say so to the user.
- A name listed by mistake: `scripts/client_names.py remove "<name>"`.
- A remote that may legitimately hold the client's names:
  `scripts/client_names.py allow "github.com/<org>/*" --client "<client>"`.

## Other commands

- `scripts/client_names.py list` prints the list.
- `scripts/client_names.py install` sets the global `core.hooksPath` to this skill's `hooks/`
  and links the skill into `~/.claude/skills`. Run it once per machine.

## Limits

- A repository that sets its own `core.hooksPath` (husky, lefthook) overrides the global one,
  so the hook does not run there.
- The hook scans only what is being pushed: added lines, commit messages, and file paths. Text
  already in a repository is not re-checked.
- It matches whole words, case-insensitively. It cannot catch a paraphrase ("a large Japanese
  IT company"). Judgment still applies.
