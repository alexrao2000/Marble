---
name: explicit-repository-visibility-permission
description: Repository visibility changes require explicit permission
metadata:
  type: feedback
  modified: 2026-11-19
---

Never change a repository's visibility without explicit permission for that
repository and direction. A request to purge sensitive history or fix a
security issue does not authorize making the repository private.

Before requesting permission, explain known irreversible effects, including
loss of stars and watchers. Do not treat incident containment as an exception.
When the user has explicitly authorized the visibility change, do not ask the
same permission question again unless the action or material risk changes.

The user has also requested a tool-level restriction. The versioned rule at
`codex/rules/repository-visibility.rules` is installed in
`~/.codex/rules/repository-visibility.rules` and forbids `gh repo edit`.
This makes CLI repository settings manual-only, including visibility changes.
Do not bypass this restriction with API calls, scripts, browser controls,
alternate executables, or other credentials. The user can change the setting
directly. This command rule is not a credential-level sandbox across all tools.
Codex must restart to load newly installed rules.
