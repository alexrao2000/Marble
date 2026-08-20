---
name: feedback-pr-titles-cite-task
description: "PR titles name the requirement+criterion or sprint task, and never the issue number"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81a8e075-feb8-4cf0-807b-bacbbddc771d
  modified: 2026-08-07T00:12:25.943Z
---

A PR title names the **requirement and criterion** (or the sprint task) the work delivers, and **never the issue number**. The issue number goes at the bottom of the body only.

- Wrong: `API005 c10: withhold the caller field that redirects the provider (#365)`
- Right: `API005 c10: withhold the caller field that redirects the provider`

**Why:** two corrections, in order. First the user edited a title of mine from "Fix response model field, closes #312" to "…completes task 12, closes #312" — the *what was delivered* has to be in the title, not only the bug closed. Then on PRs #380/#381 they said the issue number should not be in the title at all: "I just noticed their titles contain the issue number. Don't do that. If you really want to add it, put it at the bottom next to '1430 tests passed…' as 'Issue: #{whatever}'."

**How to apply:** Title = `<REQ> c<N>: <imperative description>`, no issue number, no "closes". Keep the functional `Closes #N` at the bottom of the body — it is what auto-closes the issue on merge, so removing it would be a real regression rather than a formatting change. Use the plain `Issue: #N` form the user described only when referencing an issue the PR does not close. See [[feedback_pr_body_template]] for the body itself, and [[feedback_write_prs_for_outside_readers]] for register.
