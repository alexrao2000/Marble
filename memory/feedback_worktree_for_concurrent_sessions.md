---
name: feedback-worktree-for-concurrent-sessions
description: "Use a worktree to isolate from a parallel ongoing session sharing the main checkout, not as a default per-task habit"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fb7a3361-3e5c-4af2-898a-8df7f921a2b2
  modified: 2026-08-06T22:36:29.864Z
---

A worktree exists to isolate from another session using the main checkout at the same time, not to give each task its own sandbox by default.

**Why:** On 2026-08-06, this session used a fresh worktree per fix (per PR), which was fine on its own terms. But the primary checkout (`sample-project` itself, not a worktree) ended the session on a completely different branch (`bench-mutation-gaps`) with uncommitted changes neither the user nor this session made — clear evidence another session was working in that same directory concurrently, unnoticed until a routine status check at the end. The user's correction: "We don't need a worktree per PR, we need a worktree if there's another parallel ongoing session. You should be able to deduce that on your own."

**How to apply:** Before git operations that touch the main checkout, check its state for signs it's already in use elsewhere — a branch that doesn't match what this session left it on, uncommitted changes not attributable to this conversation, or commits with no matching turn in this session's history. Read that as evidence of concurrency and switch to a worktree because of it, stated plainly, rather than mechanically creating one per task regardless of whether anything is actually at risk of colliding. The point is detecting shared use of the primary directory, not sandboxing habit.
