---
name: supabase-cli-project-visibility
description: The local Supabase CLI can list projects absent from the connected Supabase tool's results
metadata:
  type: observation
  subject: Supabase connected tools and CLI 2.90.0
  observed: 2026-11-17
  status: active
  recheck_after_days: 14
---

## Observed

The connected Supabase project list omitted projects that the existing local CLI login could list. Direct connector lookups of those omitted project references returned permission denied.

## Evidence

On the same machine, `list_projects` returned two projects in one organization. `supabase projects list --output json` returned four projects across three organizations, including both omitted references. One omitted project was paused and separately confirmed by a local application's URL and CLI project reference. The other was a marketplace-managed project. The underlying credential or organization-scoping difference was not established.

## Re-check

Compare the connected tool's project references with `supabase projects list --output json` under the existing authenticated CLI session. Do not print tokens or API keys.

## Apply

When a known project is absent or denied by the connector, try the existing authenticated CLI before concluding that the user lacks access. This is read-only discovery; it does not authorize changing the project.

## History

- 2026-11-17: Recorded after the CLI exposed two projects absent from the connected tool's list.
