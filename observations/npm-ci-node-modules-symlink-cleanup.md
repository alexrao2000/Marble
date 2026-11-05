---
name: npm-ci-node-modules-symlink-cleanup
description: npm ci cleared the target of a node_modules directory symlink before removing the link.
metadata:
  type: observation
  subject: npm 11.19.1 / Node 24.22.2 on macOS
  observed: 2026-11-04
  status: active
  recheck_after_days: 30
---

## Observed

Running npm ci in a checkout whose node_modules was a symlink emptied the linked directory, then removed the symlink. A shared checkout's installed dependencies were cleared this way. Reinstalling from its unchanged lockfile restored them.

## Evidence

Two controlled, disposable fixtures used the same private package, an empty dependency set, and a version-3 lockfile. Each had a separate target directory containing sentinel.txt. The control had a real project/node_modules directory; the other had project/node_modules symlinked to the target. Both ran npm ci --offline --ignore-scripts --no-audit --no-fund with npm 11.19.1 on Node 24.22.2.

Both commands exited zero. The control preserved target/sentinel.txt. The symlink case removed target/sentinel.txt and left the target empty; project/node_modules no longer existed. No packages, lifecycle scripts, network access, or credentials were needed. The fixtures were removed afterward.

The [npm ci documentation](https://docs.npmjs.com/cli/v11/commands/npm-ci/) describes removal of an existing node_modules directory but does not describe cleanup through a directory symlink.

## Re-check

Create two temporary directories, project and target. Put a synthetic sentinel file in target. Give project an empty private package and matching lockfile, and symlink project/node_modules to target. Run npm ci --offline --ignore-scripts --no-audit --no-fund from project. Check both the sentinel and the symlink afterward. Repeat with a real node_modules directory as the control. Use disposable paths and remove the fixtures afterward.

## Apply

Before running npm ci in a worktree, check node_modules with lstat or test -L. If it is a symlink, unlink only that symlink before installing. Never run a clean install through a shared dependency-directory symlink. Prefer an independent install in each worktree.

## History

- 2026-11-04 — Measured a cleared shared dependency folder, restored it, and reproduced the symlink-target cleanup against a real-directory control using an offline package with no dependencies.
