---
name: run-checks-before-committing
description: Run available relevant tests and checks before committing code
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-17
---

Before committing code, run the relevant tests, linting, type checks, and build
checks when applicable. Use documented project commands where available.
Fix failures and rerun the checks. Do not knowingly commit broken changes.

For documentation-only changes, validate formatting, links, references, and
privacy. Review the exact changed files and diff before committing.

If a check cannot run because of missing dependencies, credentials, or an
unavailable environment, report which check was not run and why. Never
present an unrun check as passing. Passing local checks reduces avoidable
CI failures but does not guarantee that CI will pass.

The standing instruction to commit completed work does not override the
requirement to verify changes first.
