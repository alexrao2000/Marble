---
name: always-commit
description: Always commit work to git; never leave changes only in scratchpad or working memory
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcb356c1-692c-4d12-a6dc-34826e360f3b
  modified: 2026-08-20T01:41:08.876Z
---

Always commit work to git. Do not leave generated files, scripts, or other deliverables in the scratchpad or other non-committed locations.

The only exceptions are:
- Files containing sensitive secrets (API keys, credentials, passwords)
- Large datasets that are not yet gitignored

**Why:** Work that is not committed is invisible to the user and to other sessions. The user has lost work multiple times because changes lived only in ephemeral locations. Committing is the default; not committing requires a reason.

**How to apply:** When you create a file that is part of the deliverable, commit it immediately. Use the scratchpad only for truly temporary intermediates that have no value after the current step completes.
