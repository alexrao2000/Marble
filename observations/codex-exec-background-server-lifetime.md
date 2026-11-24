---
name: codex-exec-background-server-lifetime
description: A web server launched with nohup inside a Codex command stopped when the command ended, while a server in a new POSIX session stayed reachable
metadata:
  type: observation
  subject: Codex desktop command tool, Next.js 16.4.3, Node 24.22.2, Python 3.13.7, macOS 27.0.1
  observed: 2026-11-24
  status: active
  recheck_after_days: 30
---

## Observed

A Next.js server launched as a background child with `nohup` listened on loopback while the Codex command ran. After the command returned, the listener had disappeared. A Python launcher using `subprocess.Popen` with `start_new_session=True` left the server reachable after its command returned.

## Evidence

The first launcher redirected standard input and output, verified successful HTTP requests, and removed its cleanup trap on success. The next command found no HTTP listener, and a request failed to connect. The PostgreSQL process launched through `pg_ctl` for that run still listened on its private Unix socket. The second launcher used the same local build, loopback port, and database. It verified an HTTP response before exiting. Two later commands still found the same server listening. These measurements establish the observed lifetime and leave the cause of the first exit undetermined.

## Re-check

Pick a free loopback port and use a disposable fixture. Start `python3 -m http.server --bind 127.0.0.1 <port>` with `nohup` and redirected streams in a Codex command. Verify a response before returning, then repeat the request from a separate command. Repeat with `subprocess.Popen(..., start_new_session=True)` on a second free port. Record the owned PIDs, and stop both fixtures at the end.

## Apply

Verify a preview from a second command after its launcher returns. If the preview needs to remain available, give its process a dedicated session, keep its PID, and stop it when the review ends.

## History

- 2026-11-24 — Measured a working HTTP response before the first launcher exited, the missing listener afterward, and the surviving listener from the second launcher.
