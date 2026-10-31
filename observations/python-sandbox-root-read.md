---
name: python-sandbox-root-read
description: Bundled CPython 3.12 needs literal root-directory read permission in a filesystem-allowlisted macOS sandbox
metadata:
  type: observation
  subject: Bundled CPython 3.12.14 / macOS 27.0.1 sandbox-exec
  observed: 2026-10-31
  status: active
  recheck_after_days: 30
---

## Observed

The bundled CPython 3.12.14 process aborted with signal 6 and empty stderr when
sandbox-exec denied file-read-data outside its interpreter, system, and temporary
directories. Adding `(literal "/")` to the read allowlist made it start normally.
This permits reading the root directory itself; it does not permit reading its
descendants generally.

## Evidence

A fixed program returned the integer 6. The same process, working directory,
input, interpreter, and profile succeeded with `(allow default)` and with network
or process-fork denial alone. Removing CPU and file-size resource limits did not
fix the allowlisted profile. Adding individual system or home-cache subpaths did
not fix it. Adding only `(literal "/")` did. With that exception, separate probes
still received PermissionError for a test file outside the allowlist and for a
loopback network connection.

## Re-check

Run the [standalone check](checks/python-sandbox-root-read.py) with the bundled
Python interpreter. It compares the same process without and with the literal
root exception. Expect `without_root=-6` and `with_root=0` with stdout `ok`.
If both succeed, this observation no longer holds for that interpreter/system.

## Apply

When denying file-read-data outside an interpreter allowlist, add the literal
root directory to the permitted reads. Keep home data, writes outside the work
directory, and network access restricted. The exception costs one directory read
permission; do not replace it with `(subpath "/")`, which permits all files.

## History

- 2026-10-31: Codex measured the controlled startup comparison while building an isolated generated-code grader; recorded the root-directory exception and confirmed file/network denials still applied.
