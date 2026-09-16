---
name: rhetorical-questions-are-actions
description: Alex's rhetorical questions often instruct Codex to perform the implied correction or next step
metadata:
  type: feedback
---

When Alex asks a rhetorical question in a work context, usually treat it as an instruction to
perform the implied action. A question such as “why shouldn't I do it in the CLI?” or “isn't this
private?” commonly means “use the CLI” or “make this private,” not merely “explain the tradeoff.”

**Why:** Answering only the literal question makes Alex repeat the instruction explicitly and
leaves expected work undone.

**How to apply:** Infer the concrete action from the surrounding task, state the interpretation
briefly when useful, and carry it out. Ask only when the implied action is materially ambiguous,
destructive, externally communicative, or requires authority Alex has not granted. This memory is
Codex-only; do not add it to the shared Claude memory index.
