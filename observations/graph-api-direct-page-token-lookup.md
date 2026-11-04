---
name: graph-api-direct-page-token-lookup
description: A direct Page token lookup can succeed when the same User token returns no managed Pages
metadata:
  type: observation
  subject: Social platform Graph API v26.0
  observed: 2026-11-04
  status: active
  recheck_after_days: 30
---

## Observed

A User access token returned an empty managed-Page list, yet a direct lookup of a known Page ID with that same token returned the matching Page access token. An empty list did not establish that the user lacked access to the Page.

## Evidence

With the same saved token, GET /me/permissions reported the required insights, Page listing, and Page engagement permissions as granted. GET /me/accounts?fields=id,name,access_token,tasks&limit=100 returned data: [] and no next page. GET /PAGE_ID?fields=id,name,access_token then returned the configured Page and a Page token. GET /me?fields=id,name using the returned token matched the requested Page ID. Insights queries with the derived token returned complete daily views and engagements and an end-date follower count for two matching calendar months a year apart. No permissions, Page roles, or account settings changed between the empty list and successful direct lookup. The reason the list omitted the Page was not established.

## Re-check

With an authorized existing User token and a separately known Page ID, compare the managed-Page listing with a direct lookup of that ID. Use the provider's fixed API origin and an Authorization header. If a Page token is returned, validate its identity through /me before saving it locally. Keep all tokens out of logs and tracked files. If the listing now includes the Page, the discrepancy is not reproduced for that account; do not generalize from a different account.

## Apply

When a Page list is empty, try the documented direct lookup for the user's known Page ID before concluding that another permission or Page role is necessary. This adds a read-only request. Never guess IDs or silently select another Page. Save a returned token only after verifying that it identifies the expected Page.

## History

- 2026-11-04 — Recorded the empty-list/direct-lookup comparison and successful Insights verification. No claim was made about the underlying cause.
