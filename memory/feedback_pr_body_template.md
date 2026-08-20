---
name: feedback-pr-body-template
description: "strict PR/issue body template - Problem, Fix, Changes, then the test-count line"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81a8e075-feb8-4cf0-807b-bacbbddc771d
  modified: 2026-08-06T22:45:19.020Z
---

Every PR and issue body uses this exact structure. PRs #380 and #381 are the canonical examples the user pointed at.

```
## Problem

What is actually wrong and what it costs, in plain words. Name the real
consequence, not the abstraction.

## Fix

One short paragraph. What was done, at a glance.

## Changes

**A full-sentence bolded lead-in saying what this change is and why it matters:**
```<lang>
the snippet, or the quoted spec text
```
A plain-sentence explanation underneath. Repeat this block for every
meaningful change, including tests and spec edits.

1430 tests passed, 0 failed, and ruff reported no issues.

Closes #365
```

**Why:** the user set this as a fixed template rather than a suggestion, after repeatedly rewriting my PR bodies. The failure it prevents is a body that lists what changed without saying what it means to a reader who was not in the session.

**How to apply:**
- Every `## Changes` entry gets **three parts**: a bolded full-sentence lead-in, a snippet or quoted spec text, and a plain-sentence explanation. Never a bare label fragment like "**Tests:**" or "**Spec:**".
- Say plainly which tests are new and that they were seen failing first — "We added three new tests, and two of them were failing before this PR's changes landed."
- Call out the one line that actually fixes the problem, and say the rest supports it: "this is the whole fix", "everything below either proves this works or writes down the rule".
- Say when there is *no* spec change and why, rather than leaving the absence unexplained.
- Test line is the literal shape "N tests passed, 0 failed, and ruff reported no issues." then `Closes #N`.
- No "not just X" or other contrastive-hedge constructions — see [[feedback_no_contrastive_hedging]].
- Plain words for outside readers — see [[feedback_write_prs_for_outside_readers]].
- Title rules are separate — see [[feedback_pr_titles_cite_task]].
