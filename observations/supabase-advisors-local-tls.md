---
name: supabase-advisors-local-tls
description: Supabase CLI 2.90.0 database advisors attempted TLS even with sslmode=disable.
metadata:
  type: observation
  subject: Supabase CLI 2.90.0 on macOS with PostgreSQL 17.11
  observed: 2026-11-18
  status: active
  recheck_after_days: 14
---

## Observed

`supabase db advisors --db-url` attempted a TLS connection to a disposable local
PostgreSQL server with TLS disabled. Adding `?sslmode=disable` to the connection
URL still failed with `tls error (server refused TLS connection)`.

## Evidence

Both the plain loopback URL and the same URL with `sslmode=disable` failed before
advisors could run. The server was reachable with psql. Enabling TLS only on that
disposable server, reloading it, and using `sslmode=require` let the security
advisor complete with no issues. The command help did not describe this TLS
requirement or the treatment of the URL option.

## Re-check

Against a disposable local PostgreSQL instance with TLS disabled, run the
installed CLI's security advisor with a connection URL containing
`sslmode=disable`. If it completes the scan, this behavior no longer holds.

## Apply

Use TLS for an isolated local database when running this CLI version's advisor.
Do not change a shared or production database's TLS configuration for this
workaround. If a disposable TLS server is unavailable, use direct SQL checks
and report that the advisor did not run.

## History

- 2026-11-18 — Codex compared plain and sslmode=disable URLs, then verified the advisor completed after enabling TLS on the isolated server.
