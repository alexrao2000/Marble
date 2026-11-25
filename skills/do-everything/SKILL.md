---
name: do-everything
description: >-
  Identify and execute all outstanding work items from a provided checklist, meeting notes,
  or Slack message. Triage each item as actionable or human-only, frontload questions, then
  work continuously until done. Use when the user says "do everything" or provides a list of
  outstanding items and asks for all of them to be completed.
---

# Do everything

## When to run

Run this skill when the user provides a list of outstanding work (from meeting notes, a Slack
message, a checklist, or their own words) and asks for all of it to be done. The trigger is
intent to clear a backlog in one session rather than to work one item.

## Procedure

### 1. Inventory

Read the provided material and list every item. For each item, classify it:

- **Actionable**: this session can do it (code, spec, research, documentation).
- **Human-only**: requires a human (client confirmation, live meeting, account access).
- **Already done**: the codebase or git history shows it is complete.

Present the inventory to the user. State the human-only items plainly and do not attempt them.

### 2. Frontload questions

Before starting any work, ask every question whose answer would change what you build. Ask
them all at once so the user answers in one pass. If there are no questions, say so and
proceed.

### 3. Execute

Work the actionable items in dependency order. For each item:

1. Read the project's AGENTS.md and active plan to confirm scope.
2. Do the work (spec amendment, code, research, documentation), implementing coherent slices first.
3. Batch test writing and runs at useful checkpoints. Follow the [development cadence preference](../../memory/feedback_implementation_and_test_cadence.md) and run relevant completion checks before committing completed code.
4. Note what was done.

Do not stop between items unless blocked.

### 4. Report

When all actionable items are done, report what was done and what remains (human-only items).
Follow the report-when-done skill if it is active.
