---
name: feedback-stacked-prs-use-gh-stack
description: For dependent PRs use the gh stack extension; never hand-roll a stack with --base without retargeting the child on merge
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81a8e075-feb8-4cf0-807b-bacbbddc771d
  modified: 2026-08-09T08:13:48.946Z
---

When one PR depends on another, use the official `gh stack` extension (`gh extension install github/gh-stack`). Do not hand-roll a stack by setting `gh pr edit <child> --base <parent-branch>` and leaving it there.

**Why:** GitHub only retargets a child PR to `main` when the parent's branch is **deleted** on merge. If the branch survives, the child merges *into the parent's branch* instead of `main` — and both PRs then report as MERGED while only one landed. This happened on 2026-08-09: #462 squashed into `main` at 08:09:20 and #463 merged into `report-caller-filter` at 08:09:30, ten seconds later, with the user following the merge order I gave. Telling someone to "merge the parent first" is not sufficient advice on its own.

**How to apply:** prefer `gh stack`. If stacking by hand anyway, retarget the child to `main` yourself the moment the parent merges, and verify by content afterwards — `git merge-base --is-ancestor <child merge commit> origin/main`, not the PR's MERGED badge. See [[feedback-push-implies-pr]] for the same lesson about trusting PR state over content.
