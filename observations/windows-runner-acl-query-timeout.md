---
name: windows-runner-acl-query-timeout
description: A hosted Windows runner exceeded a 10-second built-in PowerShell ACL query deadline while peer runners passed it.
metadata:
  type: observation
  subject: GitHub windows-latest runner, Python 3.13.17, Windows PowerShell 5
  observed: 2026-11-03
  status: active
  recheck_after_days: 14
---

## Observed

One hosted Windows runner timed out executing a bounded, noninteractive built-in PowerShell ACL query at ten seconds. Peer jobs using the same code passed that preflight. A subsequent run with a 30-second bound passed its Windows preflight. This does not identify whether startup, runner load, or the ACL operation caused the delay, or guarantee that 30 seconds will always suffice.

## Evidence

The failing log contained `subprocess.TimeoutExpired` for a PowerShell `Get-Acl`/`Set-Acl` fixture operation with `orig_timeout = 10`. The same job's read-only private-path query returned false, consistent with its fail-closed timeout handler. Other Windows jobs advanced past the same preflight. After increasing only the bounded process allowance and retaining denial tests, the fresh Windows preflight succeeded. Repository names, paths, identities, and private log contents are not retained here.

## Re-check

On an authorized Windows runner, execute the noninteractive ACL query against a disposable file and inspect timing and exit status. Compare a ten-second bound with a bounded longer allowance. A single fast run does not contradict an intermittent timeout; sustained comparable runner evidence is needed to retire it.

## Apply

Do not classify a timeout as proof that a correctly configured ACL is unsafe. Keep the application fail-closed on unavailable checks, but allow a realistic bounded process startup budget and retain actual unsafe-ACL rejection tests. Avoid duplicating an identical preflight unnecessarily across matrix jobs.

## History

- 2026-11-03: Codex recorded one Windows timeout among peer preflights and the subsequent successful preflight with a 30-second allowance.
