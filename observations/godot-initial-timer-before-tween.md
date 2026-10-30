---
name: godot-initial-timer-before-tween
description: A short SceneTreeTimer during headless startup can expire before a newly created tween receives an automatic update.
metadata:
  type: observation
  subject: Godot 4.5.1 headless on macOS
  observed: 2026-10-29
  status: active
  recheck_after_days: 90
---

## Observed

In a SceneTree script started through `_initialize` and a deferred `run`, a short `create_timer` timeout did not imply that a just-created bound Tween had advanced automatically. A tween manually stepped to 0.04 seconds still reported 0.04, with `is_running()` true, after a 1 ms timer expired. After three `process_frame` signals, it reported 0.129696 seconds. A larger game test also observed unchanged tween time after a 60 ms timer during startup.

This is a startup/frame-order observation, not a claim that timers always precede tweens or that production tweens fail to run. Godot's Tween and SceneTreeTimer documentation say both process after nodes, but do not establish the relative first-update guarantee that the test had assumed.

## Evidence

Godot 4.5.1.stable.official.f62fdbde1, `--headless`, macOS. The minimal probe contained no game nodes, audio, imported resources or rendering. It printed:

```
timer: elapsed=0.04 initial=0.04 running=true
three process frames: elapsed=0.129696
```

The game test independently checked frozen actor processing and a free-standing tween. Pausing only the short hold timer, then observing actual frames, kept actor motion frozen while the unrelated tween advanced. A separate active hold timer still restored processing normally. No production hit-stop change was necessary.

References checked: https://docs.godotengine.org/en/4.5/classes/class_tween.html and https://docs.godotengine.org/en/4.5/classes/class_scenetreetimer.html.

## Re-check

Save the following as a temporary `.gd` script and run the installed Godot with `--headless --path /private/tmp --log-file /private/tmp/tween-first-frame.log --script /absolute/path/to/probe.gd`. Compare elapsed time at the timer and after the frame signals; a fixed ordering on a later engine may change the first result.

```gdscript
extends SceneTree
func _initialize():call_deferred("run")
func run():
 var node=Node3D.new();root.add_child(node)
 var motion=node.create_tween()
 motion.tween_property(node,"position:x",1.0,1.0)
 motion.custom_step(.04)
 await create_timer(.001).timeout
 print("timer: ",motion.get_total_elapsed_time()," running: ",motion.is_running())
 for frame in range(3):await process_frame
 print("frames: ",motion.get_total_elapsed_time())
 quit()
```

## Apply

For tests of per-frame processing or tween isolation, observe actual process frames rather than assuming a short timer guarantees an update. When inspecting a temporary freeze, pause only its expiry tween so observation cannot race expiry; test automatic restoration independently with its timer active. This changes test scheduling, not application timing. Do not generalize this into arbitrary sleeps in game code.

## History

- 2026-10-29 — Recorded after a minimal probe separated first-frame timer/tween ordering from actor-freeze behavior.
