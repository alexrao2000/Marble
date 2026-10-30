---
name: cua-browser-user-repl-reset
description: A stale CUA REPL can report browser.user is unavailable for a live in-app tab; resetting the REPL restored access in two measured cases.
metadata:
  type: observation
  subject: Codex desktop CUA REPL and in-app browser on macOS
  observed: 2026-10-30
  status: active
  recheck_after_days: 14
---

## Observed

Across two follow-up turns, reading or reloading an existing in-app browser tab failed with `browser.user is unavailable`. Resetting the CUA JavaScript session and binding the same live tab again restored access without closing the browser or restarting the local server.

## Evidence

On both turns, `cua.getTab` failed in the retained REPL. In the second case, `cua.listTabs({browser: 'iab'})` still returned tab 1, while binding that exact ID failed. After `js_reset`, a fresh first invocation of `cua.getTab('1', {browser: 'iab'})` returned the current page accessibility tree. Reloads and screenshots then worked. This establishes a session reset workaround for this error, not its underlying cause.

## Re-check

If the same error occurs, list tabs once to confirm the tab still exists. Reset the CUA REPL, re-read its returned documentation, and bind the same tab ID. Confirm the current page can be read and captured. A missing tab is a different condition.

## Apply

For this specific error on a listed live tab, reset the REPL once and rebind the tab. Resetting discards JavaScript handles but leaves browser tabs and page state intact. Do not switch browsers or restart the site as a first response.

## History

- 2026-10-30 — Codex observed two failed retained-session bindings followed by successful fresh-session bindings to the same in-app tab.
