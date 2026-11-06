---
name: github-contribution-calendar-default-window
description: GitHub defaults to a rolling past-year contribution grid with leading week padding; explicit years use Jan–Dec.
metadata:
  type: observation
  subject: GitHub.com public contribution calendar
  observed: 2026-11-05
  status: active
  recheck_after_days: 30
---

## Observed

The public default calendar showed a rolling past-year window rather than the
latest calendar year. Its date cells included leading days to align the first
Sunday. Explicit calendar-year requests returned January 1 through December 31.
The padded default was not exactly 365 cells.

## Evidence

Fetched the public example endpoint
[default calendar](https://github.com/users/octocat/contributions), extracted
unique data-date attributes, and compared explicit from/to requests. The default
contained 370 dates, from 2025-11-02 to 2026-11-06, with an “in the last year”
heading. The first date was a Sunday. Explicit requests for 2025-01-01 through
2025-12-31 and 2026-01-01 through 2026-12-31 each returned exactly those 365 dates
and an “in YEAR” heading. No account authentication or private profile was used.
The measurement was made on November 5 in America/Los_Angeles; the default end
date was already November 6, so client-local today must not be inferred from it.
[Official documentation](https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile)
describes the past-year default but does not specify the observed padding.

## Re-check

Fetch that public endpoint without date parameters and extract sorted unique
data-date values. Compare it with the same endpoint using a complete past
calendar year in from/to parameters. Confirm the default crosses calendar years
and begins on a week boundary while the explicit year starts January 1 and ends
December 31. Do not rely on the sample cell count or sample end date as constants.

## Apply

Treat rolling-year and calendar-year modes as separate choices. If reproducing
the grid, account for leading padding separately from the logical date window;
do not assume exactly 365 rendered cells or copy the observed count of 370.

## History

- 2026-11-05 — Codex measured the public default and two explicit years while
  researching the intended Metrics calendar behavior.
