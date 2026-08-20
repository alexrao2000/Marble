---
name: report-when-done
description: >-
  Work asynchronously and report results only when finished. Do not narrate progress or
  ask intermediate questions. Deliver a structured summary of what changed, what was
  skipped, and what remains. Use when the user says "get back to me when you're done"
  or asks for deferred reporting.
---

# Report when done

## When to run

Run this skill when the user asks to be notified after the work is complete rather than
during it. The trigger is deferred reporting: "get back to me", "let me know when you're
done", "report back after".

## Procedure

### 1. Acknowledge

Confirm what you are about to do in one sentence. Do not explain the plan in detail.

### 2. Work silently

Execute the task without intermediate status messages, progress updates, or questions.
If you hit a blocking question that cannot be resolved from the codebase, the spec tree,
or reasonable defaults, note it and continue with the remaining work.

### 3. Report

When the work is complete, deliver a structured summary:

**Fixed / Done:**
- One line per completed item. Lead with the file or artifact that changed.

**Skipped (human-only):**
- Items that require a human. State why.

**Blocked:**
- Items where a question prevented progress. State the question.

**Verification:**
- Whether the check script passed and the result (pass count, fail count).

Keep the report under 30 lines. Do not restate the original request.
