---
name: feedback-delete-branches-after-merge
description: "Delete a branch as soon as its PR merges, locally and on the remote; do not leave stray branches for the user to find"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81a8e075-feb8-4cf0-807b-bacbbddc771d
  modified: 2026-08-09T08:17:57.925Z
---

When a PR merges, delete its branch immediately — `git push origin --delete <branch>` and `git branch -D <branch>` — rather than leaving it. Do not create a branch that will not carry a PR at all.

**Why:** Alex had to point out `declared-metadata` sitting locally, and nine stale branches had accumulated across one session. Stray branches are not just clutter here: a surviving parent branch is exactly what caused a stacked child PR to merge into it instead of `main`, so leaving them has already cost real work. See [[feedback-stacked-prs-use-gh-stack]].

**How to apply:** after a merge, verify the content landed on `main` by content rather than by the MERGED badge, then delete both refs. Before ending a session, list branches and clear any whose PR is merged — leave only `main`, branches with open PRs, and anything the user asked to keep.
