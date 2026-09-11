---
name: feedback-do-the-asked-change
description: "Make exactly the requested edit and stop; don't add unrequested caveats, banners, or reopen items Alex has deferred"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-08-25T00:00:00.000Z
---

Make the edit Alex asked for and stop there. Reminders about a concern are fine to voice once, but an item he has deferred or declined is closed until he reopens it — don't re-raise it inside the edit itself, and don't pad a requested change with unrequested material addressing that concern.

**Reconstruction notice:** this memory's file was accidentally truncated to empty by a stray shell redirect during a later session (`cat > file` used by mistake instead of a read). The paragraph above is reconstructed from the one-line index description in MEMORY.md, which is all that survived, plus the incident below from the session that caused the truncation — so treat the exact original wording as lost, the underlying rule as intact.

**Why:** two incidents so far.

The original (wording lost, per the note above): Alex deferred or declined something, and a later edit reopened or re-addressed it unprompted rather than treating the deferral as a closed decision.

2026-08-25: asked to "move it to reqs/" (a proposal document), I moved the file and *also* added an eight-line provenance banner to its top explaining why it wasn't really a client source. He replied: "I didn't ask for the banner. Remove it." The move was correct; the banner was scope he never asked for, justified in my own head by a real convention clash (`reqs/` is documented elsewhere as client-sources-only) — but voicing that concern once, which I had already done in the same turn as the move, was enough. Acting on it a second time inside the file itself was the extra, unwanted step.

**How to apply:** when a request is a single concrete action (move this, delete that, rename this), do that action and nothing else. If something about it seems worth flagging, say so once in your own reply — outside the artifact you're changing — and let Alex decide whether it needs more. Don't encode the flag into the deliverable unless he asks for that too. See [[feedback_fix_dont_defer]] for the opposite failure mode (sitting on a fix instead of making it) and [[feedback_frontload_fixes]] for how to report once you have made the asked-for change.
