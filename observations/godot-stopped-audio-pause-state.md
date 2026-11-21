---
name: godot-stopped-audio-pause-state
description: Godot 4.5.1 does not retain stream_paused on an AudioStreamPlayer with no playback; paused active playback reports playing false.
metadata:
  type: observation
  subject: Godot 4.5.1 AudioStreamPlayer on macOS, headless stream playback
  observed: 2026-11-21
  status: active
  recheck_after_days: 90
---

## Observed

Setting `stream_paused = true` on a stopped player leaves the getter false. An active player paused this way reports `stream_paused = true` and `playing = false`; resuming preserves its existing playback.

## Evidence

Poem's music-room integration compared playing, already-paused and stopped campaign voices with the same audition code. The stopped case remained silent but failed an assertion demanding a true paused flag. Diagnostics are in `build/review/verification/music-room-diagnose.log` once the feature is delivered; the live test is `tests/test_music_room.gd`.

The [4.5 API reference](https://docs.godotengine.org/en/4.5/classes/class_audiostreamplayer.html) does not explain the stopped setter case. The [4.5.1 implementation](https://github.com/godotengine/godot/blob/4.5.1-stable/scene/audio/audio_stream_player_internal.cpp) confirms the setter acts only on existing playbacks and the getter returns false when none exist.

## Re-check

With the current engine, assign a valid WAV to a stopped AudioStreamPlayer in the tree, set `stream_paused` true and read it back. Compare after `play()`, pause and resume. Check playback presence separately with `has_stream_playback()`.

## Apply

For temporary audition or modal audio, preserve each voice's prior paused state and leave stopped voices stopped. Assert silence for stopped voices rather than requiring a pause flag. Do not infer that paused playback was destroyed from `playing == false`. Cost: no extra playback or restart.

## History

- 2026-11-21 — Codex measured three playback states during Poem music-room testing and checked the version-pinned source.
