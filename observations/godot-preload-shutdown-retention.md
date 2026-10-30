---
name: godot-preload-shutdown-retention
description: In Poem on Godot 4.5.1, directly preloading the shared painted backdrop at the council call site retains unrelated static visual resources at shutdown; runtime load does not.
metadata:
  type: observation
  subject: Godot 4.5.1 headless on macOS, Poem script dependency graph
  observed: 2026-10-30
  status: active
  recheck_after_days: 30
---

## Observed

A new call-site `preload("res://scripts/painted_backdrop.gd").new()` in Poem's `show_camp()` caused deterministic shutdown retention of six resources, including campaign_map_unit.gd, combat_impact.gd, their dependencies, the commander icon and cached gradient resources. Replacing only that expression with `load(...).new()` removed the errors while preserving the same scene hiding, processing suspension and restoration. This is specific to the measured dependency graph; it is not evidence that all preload calls leak or that suspension itself leaks.

## Evidence

Godot 4.5.1.stable.official.f62fdbde1, headless. The new company interaction suite and the existing 564-layout menu suite both completed all assertions but exited with three dummy texture RIDs, one material RID, one shader RID and six resources still in use. Verbose output showed no retained scene nodes. An extra process frame and deferred quit did not change it. Changing preload to load made the company suite and existing menu suite exit cleanly. Logs: `/private/tmp/poem-company-leaks.log`, `poem-company-focused3.log`, `poem-company-runtime-background.log`, and `poem-company-final-focused.log`.

The official 4.5 GDScript reference documents general static-variable script retention and a static_unload bug, but does not explain this call-site-dependent shutdown result. The underlying engine cause has not been isolated to a minimal project. Reference: https://docs.godotengine.org/en/4.5/tutorials/scripting/gdscript/gdscript_basics.html#static-unload-annotation.

## Re-check

In an isolated source copy of Poem that includes the company-card change, import the project with the installed Godot headless editor. Run `GODOT_BIN=<engine> python3 scripts/test_local.py company menus`. Then change only the council's `load("res://scripts/painted_backdrop.gd")` to `preload(...)` and repeat. Compare both complete outputs, including engine shutdown after PASS. Do not change the active checkout or ignore resource-leak errors. If the preload variant also exits cleanly, retire or narrow this observation.

## Apply

Keep the council's shared-backdrop lookup as runtime load in this project. Godot's resource cache still shares the loaded script, and menu entry is infrequent. Do not broadly replace existing preloads or add cache clearing to unrelated renderers on this evidence.

## History

- 2026-10-30 — Recorded after controlled call-site comparison eliminated the retention without changing scene suspension or weakening cleanup checks; engine root cause remains unisolated.
