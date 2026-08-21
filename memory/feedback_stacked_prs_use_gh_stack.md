---
name: feedback-stacked-prs-use-gh-stack
description: For dependent PRs use the gh stack extension; never hand-roll a stack with --base, even while warning the user about the risk
metadata:
  node_type: memory
  type: feedback
  originSessionId: 81a8e075-feb8-4cf0-807b-bacbbddc771d
  modified: 2026-08-13T00:06:33.263Z
---

When one PR depends on another, use the official `gh stack` extension (`gh extension install github/gh-stack`). Do not hand-roll a stack by setting `--base <parent-branch>` and leaving it there.

**Why:** GitHub only retargets a child PR to `main` when the parent's branch is **deleted** on merge. If the branch survives, the child merges *into the parent's branch* instead of `main` — and both PRs report MERGED while only one landed.

This has now happened twice, both times with the parent landing seconds before the child:
- 2026-08-09: #462 squashed to `main` at 08:09:20, #463 merged into `report-caller-filter` at 08:09:30.
- 2026-08-12: #518 squashed to `main` at 22:56:54, #541 merged into `task/sample-project-scaffold` at 22:56:57. Three seconds. The whole AGENTS.md split had to be rebuilt onto `main` as #545.

The second time is the one that matters: `gh stack` was already installed, this memory already existed, and I hand-rolled the stack anyway and then *warned Alex in writing* that the parent's branch had to be deleted on merge. Stating the risk is not a substitute for using the tool that removes it, and a warning delivered to a human who is merging quickly will lose the race.

**How to apply:** when the user says "stack it on X", reach for `gh stack` — do not open the PR with `--base` and narrate the hazard. If a hand-rolled base is unavoidable, retarget the child to `main` yourself the moment the parent merges, and verify by content rather than by badge: `git merge-base --is-ancestor <child merge commit> origin/main`, or check that a file the child added actually exists at `origin/main`. See [[feedback-push-implies-pr]] for the same lesson about trusting PR state over content, and [[feedback-worktree-for-concurrent-sessions]] for the separate concurrency question this is often confused with.
