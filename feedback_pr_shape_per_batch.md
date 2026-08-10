---
name: feedback-pr-shape-per-batch
description: "For a batch of many small bug fixes, ask whether to bundle into one PR or split one-per-issue each time — don't assume either default carries over from a prior batch"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81a8e075-feb8-4cf0-807b-bacbbddc771d
  modified: 2026-08-05T05:40:25.771Z
---

Alex has given opposite answers to "one PR or many?" for two different bug batches in the same
project. Earlier in this session he said "I would fix all of the bugs in one PR" for one batch.
Later, asked the same question for the 19-issue bug batch (2026-08-05), he chose "One PR per
issue (AGENTS.md's default)" instead.

**Why:** the choice isn't a standing preference — it depends on the batch (how related the
fixes are, how he wants to review them, whatever else is on his mind that day). AGENTS.md's own
default is one-concern-per-PR, and that default holds unless he says otherwise for a specific
batch.

**How to apply:** when starting a multi-issue bug-fix batch, ask which shape he wants for *that*
batch rather than assuming either the repo default or what he chose last time. Don't write a
memory generalizing either answer into a rule — this file exists to record that it doesn't
generalize, not to pick a winner.
