---
name: hyperlink-citations
description: Every citation is a hyperlink. An ADR, doc, issue, PR or file named in a PR, issue, comment or chat message links to it.
metadata:
  node_type: memory
  type: feedback
---

Every citation is a hyperlink. When a PR description, issue, comment or chat message names an ADR, a doc, an issue, a PR or a file, it links to that thing instead of naming it bare. Write `[ADR-0167](https://github.com/<org>/<repo>/blob/<branch>/docs/adr/0167-<slug>.md)`, not `ADR-0167`.

On GitHub, `#123` and commit hashes already link themselves. ADR numbers, doc paths and repo files don't. For an ADR that only exists on an open branch, link the file on that branch or the PR that adds it.

**Why:** Alex has asked for this repeatedly: first "If you cite an ADR, please hyperlink it", then again when a PR table cited ADR-0167 bare. A bare number makes the reader go and look it up. A link costs one bracket.

**How to apply:** Before posting any PR body, issue or comment, scan it for ADR numbers and file or doc paths that aren't already links, and link them. When editing an existing body, fix the bare citations in it too.
