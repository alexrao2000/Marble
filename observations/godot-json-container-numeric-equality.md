---
name: godot-json-container-numeric-equality
description: Godot 4.5.1 can compare a JSON number equal to an integer as a scalar while rejecting identical-looking arrays and dictionaries.
metadata:
  type: observation
  subject: Godot 4.5.1 GDScript JSON parsing and container equality on macOS
  observed: 2026-11-24
  status: active
  recheck_after_days: 90
---

## Observed

`JSON.parse_string("[12,4]")` produced an array with floating-point elements. Comparing its first element directly with integer `12` returned true. Comparing the parsed array with `[12,4]` returned false. Dictionaries with a single corresponding value of these two numeric types also compared unequal.

## Evidence

An isolated Godot 4.5.1 headless script returned types 3 and 2 for the parsed and literal elements, respectively. The parsed array equaled `[12.0,4.0]`. Reconstructing the parsed array with `int()` for both coordinates also made it equal to the integer literal. In Poem, the original array comparison falsely counted unchanged enemies as shifted when comparing imported tile locations to a fresh deployment. Normalizing the integral coordinates passed from source and both exported data packs. The [Godot 4.5 JSON documentation](https://docs.godotengine.org/en/4.5/classes/class_json.html) covers numeric parsing and round trips.

## Re-check

In GDScript, set `var decoded = JSON.parse_string("[12,4]")`. Print `decoded[0] == 12`, `decoded == [12,4]`, `{"x": decoded[0]} == {"x": 12}` and `decoded == [12.0,4.0]` in the same process. The measured sequence was true, false, false, true.

## Apply

Compare tile coordinates as their domain type, such as `Vector2i`. For a structured report that needs JSON arrays, normalize coordinates explicitly when building the report. Preserve fractional data and validate untrusted inputs before narrowing numbers to integers.

## History

- 2026-11-24 — Codex isolated and reproduced the false placement change during Poem's retry and retreat verification.
