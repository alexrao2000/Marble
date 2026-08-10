---
name: feedback-no-contrastive-hedging
description: "Avoid vague contrastive hedge phrases like \"seen, not predicted\" in writing/output"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a9c19c1c-801e-455d-a5c2-0dabc20fd732
  modified: 2026-08-07T07:49:24.500Z
---

Don't use a terse "X, not Y" contrastive tag as a label or section heading — e.g. "Flagged, not fixed," "Not done here, by design:" — especially to describe something that wasn't done or was deferred. This is distinct from "rather than" used as ordinary connective prose (which is this codebase's own established style and is fine); the banned thing is the clipped labeling device, not the words themselves.

**Why:** Flagged three times. First as an unclear rhetorical crutch generally ("seen, not predicted" style). Second when "not just" specifically kept resurfacing under editing pressure. Third (2026-08-07), sharpest: a PR summary used "Flagged, not fixed" and "Not done here, by design" as literal bullet labels for two things that should have just been fixed instead of deferred to background tasks. The user was angry about both at once — the phrasing, and that it dressed up "I didn't do this" as a tidy contrast rather than just admitting it plainly or, better, doing the work. See [[feedback_fix_dont_defer]] for the deferral half.

**How to apply:** Never open a bullet, section, or sentence with a clipped "X, not Y" tag. If describing something you didn't do, say so as a plain sentence ("I didn't wire X into Y because...") rather than packaging it as a label. Scan chat responses, PR/issue bodies, and commit messages for this pattern before sending. Ordinary "rather than" inside a full sentence of explanation is not the target and doesn't need to be avoided.
