---
name: cua-viewport-selected-tab
description: An in-app browser viewport override changed the most recently opened tab while another bound tab kept its native width.
metadata:
  type: observation
  subject: Codex desktop in-app browser viewport capability on macOS
  observed: 2026-11-03
  status: active
  recheck_after_days: 14
---

## Observed

A browser-level viewport override did not resize every bound tab. With a dashboard and a later-opened reference tab, setting 1280 by 1000 resized the reference tab while the dashboard remained 590 by 827.

## Evidence

After setting the override, read-only DOM measurements on the dashboard returned innerWidth 590 and innerHeight 827. The reference tab returned 1280 and 1000. Resetting the override, closing the temporary reference tab, and setting it again made the dashboard return 1280 and 1000. The capability documentation did not specify which tab receives the override. This is one measured case, not proof of every selection rule.

## Re-check

With two test tabs, set a viewport override and read innerWidth and innerHeight on each. Reset afterward. Check the intended target rather than assuming a successful set resized it.

## Apply

Measure the intended tab after setting an override. Close an unneeded temporary reference tab before responsive checks if the override affected that reference instead. Do not close user-owned tabs for this workaround. Reset overrides before finishing.

## History

- 2026-11-03 — Measured different viewport sizes on two bound tabs and recovered the intended target by closing the temporary reference tab.
