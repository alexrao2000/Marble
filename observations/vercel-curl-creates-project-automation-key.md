---
name: vercel-curl-creates-project-automation-key
description: An authenticated GET through Vercel CLI 50.32.5 can create a persistent automation bypass key and select it as a deployment environment variable
metadata:
  type: observation
  subject: Vercel CLI 50.32.5 on macOS
  observed: 2026-11-24
  status: active
  recheck_after_days: 14
---

## Observed

With a protected project linked and no reusable automation secret, a GET through
\`vercel curl\` created a project-wide automation bypass credential. The project API
reported the new entry as \`isEnvVar: true\` after the CLI exited.

## Evidence

The CLI recorded credential creation and downloaded the page. The authenticated project
API showed a single recent automation entry selected as an environment variable. An
explicit revocation removed that entry. A follow-up read confirmed that authentication
still covered all deployments. The CLI command guide mentions automatic creation.
The additional measured behavior is the persistent environment-variable selection.

## Re-check

Inspect the installed CLI's token-creation path first. For a live check, use an authorized
disposable protected project with no bypass keys. Compare its project metadata before
and after a GET. Revoke the exact new key after the check.

## Apply

Treat automatic creation as a project security write. Prefer an authenticated read-only
artifact export or an existing authorized credential for backup work. Verify cleanup if
a credential is created. Keep token values out of logs.

## History

- 2026-11-24 — Measured creation, environment-variable selection, and exact revocation.
