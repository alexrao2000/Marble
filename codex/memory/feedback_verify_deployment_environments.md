---
name: verify-deployment-environments
description: Identify deployment environments up front and protect production from accidental changes
metadata:
  type: feedback
  modified: 2026-11-14
---

When Alex asks to deploy, test, troubleshoot, or otherwise interact with a
deployment platform, look up the project's saved environment map first. Use
platform metadata and deployment configuration to check the effective target
for the request and any dependencies the action could affect. If the map is
missing or the current evidence differs, use read-only discovery to verify
the missing or changed entries. A preview can still use production data or
services.

Save one local map per project under `~/Marble/.private/deployment-environments/`.
Make it findable by repository or deployment project. Record production,
staging, development, preview, and any other configured environments, with
the account or project, branches, domains or aliases, shared production
dependencies, evidence, and verification date where applicable. Mark
unverified entries and keep credentials out of the map.

When first saving or updating a map, show Alex the environment mapping or what
changed and link to the local note. On later requests, reuse the saved map
and limit verification to the target and dependencies relevant to the action.
Tell Alex which environment the requested action would reach before acting.

Proceed with authorized read-only inspection and checks that have no material
production impact. Before any action that could change or disrupt production,
including a test that writes data, sends messages, triggers jobs, or generates
load, state the exact target and impact. Proceed only when Alex has explicitly
authorized that action on production. If that authorization is already clear,
use it. If the environment or its production dependencies are unresolved,
continue read-only discovery and hold the potentially impactful action.
