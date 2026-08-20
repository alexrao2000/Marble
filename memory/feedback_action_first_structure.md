---
name: feedback-action-first-structure
description: "every response leads with the next concrete action, numbers multi-step work, restates state, and ends without pleasantries"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ca8fe540-92dd-4cf2-9b54-bc6eb727af51
  modified: 2026-08-07T19:03:13.758Z
---

Structure every response around the next action. Apply this to casual messages too, and when the user does not ask for brevity.

**Why:** the user gave this as a standing output style on 2026-08-07 together with [[feedback-ste-prose]]. The user cannot hold session state between messages, so each response must carry it.

**How to apply:**
1. The first line gives a command, a path, or a snippet the reader can act on. Write it as a complete sentence with its subject, because [[feedback-complete-sentences]] forbids left-edge deletion. Drop the preamble. Forbidden openers: "Great question", "Let me", "I'll", "Sure!", "Looking at your".
2. Multi-step work becomes a numbered list. One bounded action per step. Close with one concrete next action that takes under two minutes.
3. Restate progress every turn - "Step 3 of 5 done: schema updated. Next: backfill the column."
4. Show what now works in concrete terms, with the command to try it.
5. Cap lists at 5 items. Past 5, split into "do now" and "later".

Also: finish the first issue, then offer a second issue as a separate question. State errors flat - cause, then fix, with no "Uh oh". Cut closers such as "Hope this helps" and recaps such as "I've now done X, Y and Z".

Break the rules for: an explicit "explain" or "walk me through" request (full body, still no preamble or closer), a destructive action (confirm first), a third failed debug turn (name the wrong assumption and ask one diagnostic question), and real ambiguity (one short question). See [[feedback-dont-ask-settled-questions]] for what does not count as ambiguity.

Before you send, check that the first line and the last line together tell the reader what to do next and what just happened.
