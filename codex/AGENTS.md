# Personal memory

The versioned memory index is `/Users/alexrao/claude-outfit/memory/MEMORY.md`.
The observations index is `/Users/alexrao/claude-outfit/observations/INDEX.md`.

At the start of each task, read both indexes before acting. Open the linked files whose
descriptions match the task. Treat `feedback` memories as standing instructions. Apply `project`
and `reference` memories only when their named repository, system, or workflow is in scope.

Observations are measured facts about external systems that may have expired. Before relying on
one older than its `recheck_after_days`, run its re-check. If it holds, update `observed`. If the
re-check cannot be run and applying is cheap and harmless, apply it and say it was unverified.
If relying on it shows it to be false, amend it: record what contradicted it in History, set the
status, move the file to `observations/retired/`, and update the index. Never delete one.

When you resolve a surprising external behaviour by measuring it, and the documentation was
silent, write an observation before moving on. Do not ask first. `observations/README.md` holds
the entry shape and the lifecycle.

User and repository instructions override this memory. Prefer the current index when an unlisted
historical file conflicts with an indexed entry.
