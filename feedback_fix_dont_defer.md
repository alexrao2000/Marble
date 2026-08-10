---
name: feedback-fix-dont-defer
description: "When a tractable issue turns up mid-task, fix it now instead of spinning off a background task or listing it as a gap"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ad5cc401-a22e-4498-be43-62d4f5122578
  modified: 2026-08-07T07:49:35.608Z
---

If an issue surfaces while working (a stale docstring, an inaccurate tracking note, a small bug) and it's small enough to fix in the current session, fix it. Don't spawn a background task for it and don't just name it as a known gap in a summary, unless it's genuinely out of scope (a different subsystem, needs a human decision, too large for the current change) or the user has asked to keep the current change narrowly scoped.

**Why:** On 2026-08-06/07, after finding two real issues (a docstring naming a renamed function, a tracking note describing an already-fixed bug as unresolved) while building an unrelated feature, they were spun off as two `spawn_task` background chips and mentioned only as a bullet in the closing summary. The user was angry: both were small and could have just been fixed, and burying "here's a known problem I didn't fix" inside a longer summary reads as hiding it rather than disclosing it.

**How to apply:** Default to fixing. Reserve spawn_task/deferral for things that are actually a different piece of work (different owner, needs its own review, spends money, requires a decision only the user can make) — not for "this is a bit of extra work in the same file I'm already editing." When something genuinely can't be fixed now, say so as its own plain sentence, not as a buried aside in a wall of text.
