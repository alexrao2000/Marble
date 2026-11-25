---
name: run-checks-before-committing
description: Batch implementation and run available relevant checks before committing completed code
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-25
---

Before committing completed code, run the relevant tests, linting, type checks, and build
checks when applicable. Use documented project commands where available.
Fix failures and rerun the affected checks. Do not knowingly commit broken changes.

During implementation, group related edits and test work according to the
[development cadence preference](feedback_implementation_and_test_cadence.md).
This completion checkpoint does not require checks after every edit or tests
before implementation. Avoid artificial microcommits that force repeated checks.

For documentation-only changes, validate formatting, links, references, and
privacy. Review the exact changed files and diff before committing.

If a check cannot run because of missing dependencies, credentials, or an
unavailable environment, report which check was not run and why. Never
present an unrun check as passing. Passing local checks reduces avoidable
CI failures but does not guarantee that CI will pass.

The standing instruction to commit completed work does not override the
requirement to verify changes first.
