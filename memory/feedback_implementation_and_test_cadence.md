---
name: implementation-and-test-cadence
description: Implement first, batch test work, and autonomously tune development cadence on real projects for the fastest verified delivery
metadata:
  type: feedback
  modified: 2026-11-25
---

Favor implementation momentum. Build a coherent piece of working behavior first,
then add or update meaningful tests as it settles. Space out test writing and runs
so related edits can proceed together. Choose checkpoints for their contribution
to delivery speed; checking after every small edit is not the default.

**Why:** Alex wants the fastest effective development cadence and expects the agent
to discover it autonomously while building real projects. Optimize total elapsed
time to a working, verified result, including test overhead and later rework.
Do not default to the most conservative or most frequent checking schedule.

**How to apply:** Use focused checks when a coherent slice is ready, when a result
will resolve an implementation question, or when feedback is likely to save time.
Broaden verification at integration and completion as the actual change requires.
Write tests that cover behavior and regressions; do not let batching turn into
indefinitely postponing tests. A test first is useful when it clarifies the design
or reproduces a bug cheaply, but a failing-test-first ritual or separate test-only
commit is not required. Follow the [completion checks](feedback_run_checks_before_committing.md)
before committing completed code, and repeat checks when new changes, failures,
or unresolved uncertainty justify them.

Gather lightweight data and autonomously A/B-test development cadences on
comparable pieces of actual project work. Vary batch size or checkpoint timing
and compare implementation time, test-writing time, execution and waiting time,
rework, and regressions discovered later. Account for task size and suite cost;
do not treat one unlike task as proof that a cadence is faster. Use the results
to adjust the next comparable piece of work. Keep measurement overhead small and
stop comparisons that cost more than they teach.

Keep delivering the requested project throughout. Choose and run the comparisons
without asking Alex to design them, run benchmarks, or manage a separate experiment
project. Keep brief measurements and the next adjustment in local notes under
`~/Marble/.private/development-cadence/`, separated by project. Reuse those notes
on later work and save general lessons in memory when evidence supports them.
Keep project identities and raw measurements out of shared memory. Report material
findings briefly alongside normal delivery updates.

This replaces older blanket preferences for tests before implementation, separate
test and implementation commits, and running the full check script after every edit.
