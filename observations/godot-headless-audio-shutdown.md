---
name: godot-headless-audio-shutdown
description: Godot headless tests can retain imported WAV playback at immediate exit; stopping voices and draining the mixer removes the warning.
metadata:
  type: observation
  subject: Godot 4.5.1 stable headless on macOS
  observed: 2026-10-29
  status: active
  recheck_after_days: 90
---

## Observed

A headless integration test that plays an imported short WAV, frees its owning node and quits after one process frame can report leaked `AudioStreamPlaybackWAV` / `AudioStreamWAV` instances and a resource still in use. An exit callback that stops the player does not by itself ensure that the mixer has released the resource before engine shutdown. Explicitly stopping playback while the node is alive, then allowing 200 ms of monotonic wall time to pass with process frames, removed the warnings in the measured cases.

This describes immediate test-engine shutdown. It is not evidence of a persistent resource leak during ordinary gameplay, nor a reason to delay normal UI actions.

## Evidence

Poem's promotion integration test began failing at engine exit after actual button presses gained a 145 ms confirmation cue. Its assertions passed, but verbose logs identified `res://assets/audio/ui_confirm.wav` and its playback as retained. A separate save-transfer test exposed a fading synchronized score that was not stopped with the current player.

A controlled probe instantiated the project's `ui_audio.gd`, played `confirm`, waited two process frames, freed the node, waited one frame and quit. It reproduced the imported WAV/playback warning. The same probe, with an explicit player stop and a 200 ms monotonic drain before freeing, produced no warning. A raw in-memory silent PCM probe did not reproduce the issue; do not generalize the result to every stream/driver combination.

Diagnostic logs at measurement time: `/private/tmp/poem-audio-immediate.log`, `/private/tmp/poem-audio-drained.log`, and `/private/tmp/poem-promotion-audio-leak.log`. Promotion, interface-audio, transfer and campaign-route integration suites passed without warnings after mixer-draining cleanup.

## Re-check

Use the current Godot binary and a Poem checkout containing the interface cues. Save this external script and run it with `--headless --verbose --path <checkout> --script <probe>`, then again with `-- drain` after the script argument:

```gdscript
extends SceneTree
func _initialize():call_deferred("run")
func run():
 var voice=load("res://scripts/ui_audio.gd").new()
 root.add_child(voice);voice.configure(-12);voice.cue("confirm")
 for frame in range(2):await process_frame
 if "drain" in OS.get_cmdline_user_args():
  voice.player.stop()
  var deadline=Time.get_ticks_usec()+200000
  while Time.get_ticks_usec()<deadline:await process_frame
 voice.queue_free();await process_frame
 quit()
```

Compare leaked-resource lines. The observation holds if immediate exit reports the imported WAV/playback and the drained run does not. If neither reproduces, recheck the actual promotion suite with and without its shutdown helper before retiring this timing-dependent observation.

## Apply

For integration tests that can trigger audio immediately before engine exit, explicitly stop all voices, cancel both sides of a score crossfade, and allow the audio mixer to drain before freeing the game and quitting. Poem centralizes this in `tests/helpers/game_shutdown.gd`. Use monotonic time for the drain rather than assuming a short startup SceneTreeTimer measures equivalent wall time. Cost: about 200 ms per game integration suite. Do not insert this delay into normal gameplay or menu navigation.

## History

- 2026-10-29 — Codex measured imported-cue shutdown against a stopped-and-drained control, fixed test cleanup, and recorded the result.
