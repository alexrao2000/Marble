---
name: keep-personal-setup-out-of-repositories
description: Keep credentials, authentication, and personal machine or cloud configuration out of project repositories
metadata:
  type: feedback
  modified: 2026-11-01
---

Keep credentials, tokens, authentication caches, local login files, and personal
machine or cloud configuration out of project repositories. This includes personal
profile names, project identifiers, account identifiers, and machine-specific paths
added during tool setup, even when they are not secrets.

A request to install, sign in, or configure a tool authorizes local setup. It does
not authorize saving those personal details in project documentation, agent rules,
commits, or remote repositories. Keep them in the tool's local user configuration.
Use generic placeholders in reusable project instructions when documentation is
needed. Only publish personal setup details when the user explicitly requests the
specific content and destination. Never commit live credentials or authentication
material; a private repository is not an exception.

Before committing or pushing setup-related changes, inspect the exact staged diff
and file list for secrets and personal configuration. Verify remote visibility
before describing it. Report what was checked and any limits; do not call a
pattern scan proof that no secrets exist. The always-commit instruction applies to
project deliverables, not personal configuration or sensitive audit evidence.
