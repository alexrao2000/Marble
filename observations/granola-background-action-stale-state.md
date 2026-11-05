---
name: granola-background-action-stale-state
description: Granola background actions can commit while the immediate accessibility snapshot still shows the previous view.
metadata:
  type: observation
  subject: Granola macOS app through Codex Computer Use
  observed: 2026-11-05
  status: active
  recheck_after_days: 7
---

## Observed

Background navigation and note creation succeeded without raising the application. Some immediate action snapshots reported no change, and some subsequent actions reported an invalid element ID, although a later fresh app binding showed that navigation or creation had already completed. A screenshot also showed the home view while the accessibility tree showed a note editor.

## Evidence

During a twelve-note migration, an initial New note click returned an unchanged home tree. A later `cua.getApp('Granola')` exposed a new note with its own meeting ID. The connector independently confirmed the new title and empty private notes. Similar delayed navigation occurred when returning home. Once the app responded consistently, reading the full accessibility tree, deriving the current control index, acting, and checking the resulting tree allowed the remaining notes to be created and titled in batches. All twelve destinations were read back through the connector. No Raise action or application activation was used. This establishes that background actions can succeed; it does not establish the cause of the stale snapshots or guarantee that rebinding always fixes them.

## Re-check

On an authorized note creation, compare the immediate native action result with a fresh app binding and a connector read. Do not create an extra note only to test this observation.

## Apply

Treat an unchanged snapshot or stale-index error as an uncertain result. Refresh the view and check for the intended note before repeating a creation or other non-idempotent action. Derive controls from the current tree. Read saved content through the connector when possible. This costs an extra read and avoids duplicate notes.

## History

- 2026-11-05: Recorded after twelve background note creations were independently verified through the connector.
