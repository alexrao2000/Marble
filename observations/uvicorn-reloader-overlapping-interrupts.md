---
name: uvicorn-reloader-overlapping-interrupts
description: Uvicorn's reloader can remain alive after its worker exits under overlapping launcher interrupts
metadata:
  type: observation
  subject: Uvicorn 0.36.0, concurrently 9.1.2, Python 3.13.7, Node 22.23.4/npm 10.9.9, macOS 27.0.1
  observed: 2026-11-05
  status: active
  recheck_after_days: 30
---

## Observed

A development chain of make → npm → concurrently → npm → a Node Python launcher → Uvicorn --reload sometimes stayed alive after one process-group SIGINT. The worker logged “Finished server process”; process inspection showed that worker as a zombie while the reloader, Python launcher, npm and make remained alive. Adding Uvicorn's graceful request timeout fixed some runs but did not reliably stop the whole chain. This is an observation of that combination, not proof of a particular lock or a universal Uvicorn defect.

## Evidence

The disposable fixture used the Tuna launch commands at commit 3b0b940, a free loopback port, a small ASGI app with a 120-second HTTP request, and a harmless Node web-process stub. The test sent one SIGINT to its own make process group. The unbounded launch remained alive after five seconds. A three-second Uvicorn request deadline still left a reloader and zombie worker in a later run. No production database, provider account, microphone or existing development server was involved.

A launcher that gave the reloading Python API a dedicated POSIX process group, forwarded its first interrupt once, and killed only that group after five seconds returned the complete chain to the prompt. Both a pending-request run and a worker deliberately ignoring SIGINT/SIGTERM exited with no members left in the owned make/API process groups. Direct Uvicorn tests of all three development configurations also confirmed request cancellation and port release. The installed reloader source waits for its worker with an unbounded process.join(); the graceful-shutdown flag bounds requests in the worker, not that parent's join.

## Re-check

Use a temporary directory and the historical launch commands and Python launcher from Tuna commit 3b0b940; never signal an existing development process. Supply a loopback-only ASGI fixture whose /hold endpoint awaits a long sleep, and replace the web command with a Node interval. Start make dev in a new process group, open /hold, send one SIGINT to that group, then inspect its members after five seconds. Repeat with --timeout-graceful-shutdown 3. Check both the outer make group and any isolated API groups when comparing the current launcher. The current [API shutdown tests](/Users/alexr/university-ai/tests/backend/test_development_shutdown.py) check worker cancellation; the [launcher tests](/Users/alexr/university-ai/tests/desktop/python-env-settings.test.cjs) check the owned-group fallback. If the historical chain now exits consistently after dependency/runtime upgrades, retire this observation with the measured versions and results.

## Apply

Give development request shutdown a deadline and separately bound reloader cleanup. Track and terminate only processes owned by that invocation; do not use broad pkill patterns or kill by a shared port. Scope POSIX group handling to reloading APIs and test Windows behavior separately. The cost is a forced development-process stop when graceful cleanup fails; production commands need their own shutdown policy.

## History

- 2026-11-05 — Measured the hanging chain, the incomplete request-timeout-only remedy, and the successful owned-group fallback during Tuna development shutdown work.
