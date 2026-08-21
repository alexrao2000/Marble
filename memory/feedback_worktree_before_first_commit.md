---
name: feedback-worktree-before-first-commit
description: "In sample-project another session can switch the shared checkout's branch mid-task; take a worktree before the first commit, not after"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1d8f3bd-afd4-47bc-969a-2a9276a15f39
  modified: 2026-08-19T01:11:20.722Z
---

On 2026-08-18 a concurrent session switched `/Users/alexrao/sample-project/sample-project` from my
branch to `issue-triage-track-phase` while I was mid-task, and left its own unstaged edit to
`.github/workflows/issue-triage.yml` in the tree. The next `gh stack rebase` failed on
"unstaged changes", and a `git add -A` at the wrong moment would have committed their
work-in-progress onto my branch.

**Why:** this checkout is shared by several sessions at once and nothing announces a branch
switch. The signals arrive only after the damage is possible: a foreign modified file, or
`git branch --show-current` answering something you did not check out.

**How to apply:** extends [[feedback_worktree_for_concurrent_sessions]]. Take the worktree
before the first commit rather than when a conflict appears — `git worktree add
../sample-project-<slug> <branch>`. Until then, stage explicit paths (`git add <path>`) and
never `git add -A`, and re-read `git branch --show-current` before any commit, rebase or
push. If you find someone's unstaged work, restore it exactly where it was
(`git stash push -- <path>` then `git stash pop` on their branch) before moving on. Note
`gh stack` does not find its `.git/gh-stack` state from inside a worktree, so finish a stack
there with plain `git rebase` plus `git push --force-with-lease` — the PR bases on GitHub are
already correct, so this is not the hand-rolled stack
[[feedback_stacked_prs_use_gh_stack]] warns about.
