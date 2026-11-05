---
name: vercel-deployment-timeout-background-completion
description: A deployment request timed out while the same pinned Git release later became Ready on production.
metadata:
  type: observation
  subject: Vercel deployment API and CLI 50.32.5
  observed: 2026-11-05
  status: active
  recheck_after_days: 1
---

## Observed

A deployment API timeout did not mean the deployment was rejected. The requested
Git commit later reached Ready and owned the canonical production alias. A CLI
retry was still Building and could be cancelled without changing that release.
This was one slow incident, not an established latency guarantee.

## Evidence

A connected create_deployment call for an exact Git SHA returned an MCP request
timeout after several minutes. Project inspection still worked. An independent
CLI archive retry took about five minutes to return its deployment ID; its first
file upload progress appeared after roughly two minutes. Public asset hashes
then matched the Git SHA while that CLI deployment still reported Building.
An authenticated GET of /v13/deployments/<canonical-host> identified a different,
Ready Git deployment with the requested SHA and releaseCommit metadata. The
redundant CLI build was cancelled by its own deployment ID. The public status
page reported operational; the cause of the delay was not established.

## Re-check

During the next authorized release, record submission and response times. If a
request times out, resolve the canonical hostname through the deployment API
and compare its commit metadata and public asset hashes before creating a retry.
Do not deploy merely to re-check this observation.

## Apply

Treat a timed-out deployment mutation as an unknown outcome. Inspect the
canonical alias and exact SHA first; a read-only check costs one API request.
Cancel a redundant build only after identifying both deployment IDs and proving
the intended release is Ready. Do not assume the measured delay will recur.

## History

- 2026-11-05 — Codex measured background completion after a deployment timeout;
  recorded one incident and a read-only check for the next authorized release.
