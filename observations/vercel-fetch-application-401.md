---
name: vercel-fetch-application-401
description: The connected Vercel fetch tool can label an application-generated 401 as deployment authentication failure.
metadata:
  type: observation
  subject: Vercel connected web_fetch_vercel_url tool and CLI 50.32.5 on macOS
  observed: 2026-11-18
  status: active
  recheck_after_days: 14
---

## Observed

An application-generated HTTP 401 behind Vercel Authentication was reported by the connected fetch tool as `deployment_authentication_required`, with `blockedAt: after_redirect`. This error alone did not establish that Vercel authorization failed.

## Evidence

The same private status route on the same exact deployment was requested using the connected fetch tool and authenticated `vercel curl`. The connected tool created a temporary share link, then returned the authentication error without the application response body. The CLI, using its own Vercel authorization without an application cookie, returned HTTP 401 with the application's explicit sign-in message. Adding the application's valid session cookie returned HTTP 200 and the expected status JSON. Project inspection confirmed persistent Vercel SSO remained enabled. No project protection change was needed.

The experiment identifies a misleading failure classification; it does not establish whether the connector reached the application on every internal retry or whether every application 401 behaves this way.

## Re-check

On an authorized protected deployment with a known application login gate, compare the connected fetch result with authenticated CLI requests to the identical route, first without and then with the application's own session. Confirm the project and exact deployment before requests. Do not create a deployment merely for this check.

## Apply

Use an existing authenticated CLI as a read-only fallback when the connector reports deployment authentication failure for a private application route. Inspect the response body before attributing a 401 to Vercel. Keep cookies and provider credentials out of logs; do not remove deployment protection to diagnose the response.

## History

- 2026-11-18 — Codex measured the connector error and paired CLI 401/200 responses with SSO unchanged.
