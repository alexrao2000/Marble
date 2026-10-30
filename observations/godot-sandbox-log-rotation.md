---
name: godot-sandbox-log-rotation
description: Godot 4.5.1 may crash in its rotating logger when a sandboxed headless invocation cannot open the default user log; an explicit writable log path avoids the measured failure.
metadata:
  type: observation
  subject: Godot 4.5.1 headless on macOS under the Codex workspace-write sandbox
  observed: 2026-10-30
  status: active
  recheck_after_days: 30
---

## Observed

A sandboxed one-off Godot script failed before its asset check ran when the default user log could not be opened. The crash backtrace named RotatedFileLogger::rotate_file(). Repeating the same script with an explicit writable --log-file path completed successfully. This is a measured startup failure under this sandbox, not a claim that every unwritable Godot log crashes.

## Evidence

Engine 4.5.1.stable.official.f62fdbde1, project Poem. Invocation used --headless --path . --script /private/tmp/poem-check-ornament.gd. It printed a failure to open user://logs/godot2026-10-30T02.17.53.log, then signal 11 and the rotating-logger stack. Adding only --log-file /private/tmp/poem-check-ornament.log produced exit 0 and the expected result: imported SVG 96 by 96 pixels, 1,598 nontransparent stroke pixels. The script only loaded an isolated texture and inspected its image; it did not render the game.

The official command-line reference documents the log override, but does not describe this crash behavior: https://docs.godotengine.org/en/4.5/tutorials/editor/command_line_tutorial.html.

## Re-check

Under an equivalent restricted macOS sandbox, run a minimal SceneTree script that prints and quits, first without a log override and then with an absolute writable temporary log path. Use a disposable project; do not make the actual user directory unwritable. If both variants start cleanly, narrow or retire the observation rather than generalizing it.

## Apply

Give one-off headless commands an explicit --log-file path inside the workspace or temporary directory. Poem's maintained test/build scripts already do this. The override costs only a temporary log and does not require broadening filesystem access.

## History

- 2026-10-30 — Codex measured default-path startup crash and successful writable-log comparison; recorded the narrow sandbox condition.
