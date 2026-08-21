---
name: feedback-fold-dont-file
description: "Don't open Phase 1A issues for small findings — fix them and fold them into the current PR, or leave them"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81a8e075-feb8-4cf0-807b-bacbbddc771d
  modified: 2026-08-10T05:49:22.449Z
---

While Alex is wrapping up for release, do not open new `[Phase 1A]` issues for things found in passing. Take the initiative: fix it and fold it into the PR in flight. If it is not worth fixing now, leave it entirely rather than filing it.

**Why:** stated on 2026-08-09 — "I'm trying to wrap up and release, all I care about is that it works for the client. Either that or take initiative and fix the issue yourself then fold it into the PR". A filed issue is work handed back to him at exactly the moment he is trying to close the list. In one stretch of that session I filed four (#478, #485, #487 and one more) instead of fixing three of them inline.

**The bar for filing anyway:** it changes what the client sees or gets, and it cannot be fixed inside the current change — a wrong figure in the deliverable, a broken documented command, a security hole. A spec question with no obvious right answer still goes to a `[Discussion]` issue for a ruling, per [[feedback-phase-triage-test]].

**How to apply:** when something turns up mid-task, ask whether the PR in hand can carry the fix. Usually it can. Say in the PR body that it was found in passing and why it belongs there. See [[feedback-fix-dont-defer]] for the same instinct at a smaller scale.
