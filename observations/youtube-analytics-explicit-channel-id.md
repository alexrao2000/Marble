---
name: youtube-analytics-explicit-channel-id
description: A YouTube OAuth token can retrieve an explicit channel report when the current channel resolves elsewhere
metadata:
  type: observation
  subject: YouTube Analytics API v2 and YouTube Data API v3
  observed: 2026-11-15
  status: active
  recheck_after_days: 30
---

## Observed

One read-only OAuth grant could retrieve reports for a known public channel by ID while the Data API's current-channel lookup returned a different channel. Using the Analytics API's current-channel selector returned the same zero activity as explicitly querying that different channel.

## Evidence

With the same OAuth access token, query reports using `channel==MINE`, the ID returned by Data API `channels.list?mine=true`, and the independently verified ID of the intended channel. For two matching calendar months a year apart, the first two selectors returned zeros. Both explicit reports for the intended channel returned views, watch time, subscriber changes, and view duration. A video breakdown for the intended channel returned watched videos. The reason the default channel differed was not established.

## Re-check

Using an existing authorized read-only grant and the independently verified channel ID, compare `channels.list?mine=true` with the explicit ID and query Analytics for a known active period using both selectors. Keep tokens out of output and use the official API origins.

## Apply

If the current channel differs from the intended channel, confirm the exact ID and try a read-only Analytics report for that ID before repeating OAuth. Use the explicit reporting channel only if the token can retrieve its reports.

## History

- 2026-11-15 — Recorded the current-channel and explicit-ID comparison using the same grant.
