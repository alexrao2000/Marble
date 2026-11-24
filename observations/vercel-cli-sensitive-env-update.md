---
name: vercel-cli-sensitive-env-update
description: Vercel CLI 50.32.5 rejected a sensitive variable replacement that the authenticated edit API accepted
metadata:
  type: observation
  subject: Vercel CLI 50.32.5 on macOS and project environment variable API v9
  observed: 2026-11-24
  status: active
  recheck_after_days: 30
---

## Observed

The installed CLI exited with an error when updating an existing Production-only
sensitive project variable from standard input. The authenticated environment
variable edit API accepted the replacement and retained its type and target.

## Evidence

`vercel env update` exited 1 with and without `--sensitive`. The captured CLI
output mentioned sensitivity. Its full error text and the precise cause were
undetermined. A metadata query confirmed the existing variable was still
sensitive and Production-only after both attempts. `vercel api` then sent a
PATCH to `/v9/projects/{project}/env/{variable}` with a JSON body from standard
input. The API returned the same variable ID, sensitive type, and Production
target. A new deployment used the replacement successfully.

## Re-check

On an authorized disposable project, create a sensitive Production-only test
variable, submit a replacement via `vercel env update` from standard input,
and verify the result through metadata and an authorized deployment if needed.
Record the exact CLI version and redacted error if it fails.

## Apply

When this CLI command fails, inspect variable metadata before retrying. Use the
edit API with the exact variable ID and existing type and target. Pass the
replacement through standard input without printing or logging the value.

## History

- 2026-11-24 — Measured the CLI failure and verified the API replacement through a deployment.
