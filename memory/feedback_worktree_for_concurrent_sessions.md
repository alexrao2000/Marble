---
name: feedback-worktree-for-concurrent-sessions
description: "Check for another agent in the checkout before touching it; use a worktree when one is found, not as a default per-task habit"
metadata:
  node_type: memory
  type: feedback
  originSessionId: fb7a3361-3e5c-4af2-898a-8df7f921a2b2
  modified: 2026-08-13T00:06:47.706Z
---

Check whether another agent is already working in the checkout **before** doing git work in it. If one is, spin up a worktree and work there. A worktree is for isolating from a parallel session, not for giving each task its own sandbox.

**Why:** Alex, 2026-08-12: "a smart agent will only spin one up if there is work currently being done." He dislikes accumulating worktrees, but is explicit that they are cheap and deletable and that the check is the part that must not be skipped — the cost of colliding with another session is far higher than the cost of one extra directory. The original correction, 2026-08-06, was the other half of the same rule: "We don't need a worktree per PR, we need a worktree if there's another parallel ongoing session. You should be able to deduce that on your own."

**How to apply:** before the first git operation, read the checkout's state for signs it is in use — a branch that does not match what this session left it on, uncommitted changes not attributable to this conversation, commits with no matching turn in this session's history, or a `.git/worktrees` list that has grown. Read any of those as concurrency, say so plainly, and cut a worktree because of it. Delete the worktree and its branch when the work merges, per [[feedback-delete-branches-after-merge]].

Do not let this rule absorb unrelated failures. On 2026-08-12 Alex attributed a lost pull request to a missing worktree check; the worktree check had in fact been done and the checkout was correctly isolated. The actual cause was a hand-rolled stacked PR merging into its parent branch — see [[feedback-stacked-prs-use-gh-stack]]. Worktrees isolate the working tree; they do nothing about remote branch topology, and treating them as the fix for a merge-order problem leaves the real one in place.
