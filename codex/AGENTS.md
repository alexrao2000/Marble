## New project locations

Create new repositories and named projects directly under /Users/alexr/<project-name> unless the user explicitly requests another location. Do not create new projects or generated work under /Users/alexr/Documents, Desktop, or an iCloud/OneDrive-synced folder by default. The existing ChatGPT project collection is located at /Users/alexr/ChatGPT. Existing explicitly selected project directories remain valid; do not relocate them without a request.

## Preserve application focus

When launching macOS applications, opening files, or opening URLs from the terminal, use `open -g` so the application stays in the background. For example: `open -g -a "Google Chrome"`. Do not activate or bring an application to the foreground unless the user explicitly asks.

# Personal memory

The versioned memory index is `/Users/alexr/Marble/memory/MEMORY.md`.
The Codex-only memory index is `/Users/alexr/Marble/codex/MEMORY.md`.
The observations index is `/Users/alexr/Marble/observations/INDEX.md`.

At the start of each task, run `/Users/alexr/Marble/scripts/sync.sh`, then read all three
indexes before acting. Open the linked files whose descriptions match the task. Treat `feedback`
memories as standing instructions. Apply `project` and `reference` memories only when their named
repository, system, or workflow is in scope.

Observations are measured facts about external systems that may have expired. Before relying on
one older than its `recheck_after_days`, run its re-check. If it holds, update `observed`. If the
re-check cannot be run and applying is cheap and harmless, apply it and say it was unverified.
If relying on it shows it to be false, amend it: record what contradicted it in History, set the
status, move the file to `observations/retired/`, and update the index. Never delete one.

When you resolve a surprising external behaviour by measuring it, and the documentation was
silent, write an observation before moving on. Do not ask first. `observations/README.md` holds
the entry shape and the lifecycle.

After changing a memory, observation, skill, or loader, stage explicit paths, commit the change,
and run `/Users/alexr/Marble/scripts/sync.sh` before ending the task. The script refuses
dirty, divergent, non-main, merge, and rebase states instead of guessing.

User and repository instructions override this memory. Prefer the current index when an unlisted
historical file conflicts with an indexed entry.
