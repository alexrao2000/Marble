---
name: vercel-curl-non-interactive-flag
description: Vercel curl forwards the advertised --non-interactive flag to system curl.
metadata:
  type: observation
  subject: Vercel CLI 65.0.0 native on macOS
  observed: 2026-11-09
  status: active
  recheck_after_days: 14
---

## Observed

Vercel CLI 65.0.0 listed `--non-interactive` under global options in
`vercel curl --help`. The curl wrapper passed that flag to system curl.

## Evidence

On a linked project with an authenticated CLI, a GET to a protected deployment
failed with `curl: option --non-interactive: is unknown` and exit code 2.
The result was the same with the flag before the subcommand and after the
deployment selector. Omitting just that flag returned the expected response
without a prompt. The published curl command reference did not describe this
exception.

## Re-check

On the next CLI version in use, repeat a read-only request to a known protected
deployment with and without the flag. Compare the exit codes and HTTP response.

## Apply

In a linked checkout with working CLI authentication, omit the flag for
`vercel curl` and use an explicit deployment ID. This costs one command option.

## History

- 2026-11-09 — Codex reproduced the error with both flag placements and verified the same request succeeded without the flag.
