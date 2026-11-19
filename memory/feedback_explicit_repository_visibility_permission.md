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
