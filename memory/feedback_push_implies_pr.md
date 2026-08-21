---
name: feedback-push-implies-pr
description: "Never state a PR's status from memory — query it before pushing to it and before telling the user anything about it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81a8e075-feb8-4cf0-807b-bacbbddc771d
  modified: 2026-08-13T00:12:58.053Z
---

A push is never complete on its own. Before pushing, confirm a PR exists for that branch **and that its state is OPEN**. If the PR is merged or closed, branch off current `main` and open a new one instead of pushing more commits onto the dead branch.

**Why:** commits pushed to an already-merged PR are stranded — they never reach `main` and nobody reviews them. This happened repeatedly across one session: five times onto merged branches, and once with 25 commits pushed to a PR that had been merged mid-session. Printing the PR's state is not enough; the check has to gate the push.

**The same rule applies to talking about a PR, not just pushing to one.** Never say a PR is open, or list what is "still to merge", from recollection of having opened it — Alex merges continuously, so my picture is stale within minutes. Being told "I merged that already", repeatedly, is what this costs. Query first, every time, including in a closing summary.

**Verify a PR you just created carries the branch you meant.** `gh pr create` takes its head from the *current directory's* checked-out branch, so running it from the main checkout while the work sits in a worktree opens the PR from whatever that checkout happened to be on — and pushes that branch to `origin` as a side effect. On 2026-08-12 this opened #545 from `routing-demos`, an already-merged branch, wearing the AGENTS.md split's title and body and proposing an empty diff; it also re-created a remote branch that had been deleted on merge. A PR's head cannot be edited afterwards, so the only repair is close and reopen. Always `cd` into the worktree first **and** pass `--head <branch>` explicitly, then read back `gh pr view <n> --json headRefName,files` before reporting anything about it.

**How to apply:** `gh pr list --state open` before naming anything as outstanding, and `gh pr list --head <branch> --state open` and act on the result before `git push`. After a merge lands mid-session, compare *content* not commits — `git diff --stat origin/main origin/<branch>` — because squash merges leave every branch commit looking absent from `main` even when its content landed. Whatever the diff shows is what needs a fresh branch and a new PR. See [[feedback-pr-body-template]] and [[feedback-pr-titles-cite-task]] for the PR itself.
