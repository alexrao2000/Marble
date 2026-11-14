---
name: verify-deployment-environments
description: Identify deployment environments up front and protect production from accidental changes
metadata:
  type: feedback
  modified: 2026-11-14
---

When Alex asks to deploy, test, troubleshoot, or otherwise interact with a
deployment platform, start with read-only discovery. Identify the project's
production, staging, development, preview, and other targets that exist.
Verify the effective account, project, branch, domain or alias, and relevant
backing services against platform metadata and deployment configuration.
Names, URL patterns, and CLI defaults are clues. A preview can still use
production data or services.

Tell Alex which environment the requested action would reach before acting.
Record the verified mapping, evidence, and date in local project notes for
future sessions. Recheck the target and any dependencies the action could
affect before relying on the mapping.

Proceed with authorized read-only inspection and checks that have no material
production impact. Before any action that could change or disrupt production,
including a test that writes data, sends messages, triggers jobs, or generates
load, state the exact target and impact. Proceed only when Alex has explicitly
authorized that action on production. If that authorization is already clear,
use it. If the environment or its production dependencies are unresolved,
continue read-only discovery and hold the potentially impactful action.
