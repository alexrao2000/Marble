---
name: godot-embedded-dialog-initial-wrap
description: A newly shown Godot 4.5.1 AcceptDialog can retain a form height measured before a wrapped label received its final width.
metadata:
  type: observation
  subject: Godot 4.5.1 embedded AcceptDialog on macOS headless
  observed: 2026-11-25
  status: active
  recheck_after_days: 90
---

## Observed

A newly opened embedded AcceptDialog could exceed its parent viewport. Setting explicit window dimensions brought the window into bounds, while the form inside it could remain too tall and push fields below the action row.

## Evidence

An isolated Godot 4.5.1 SceneTree used a 720 × 640 root window, an embedded AcceptDialog, and a VBoxContainer containing a short help Label and a vertically expanding TextEdit with a 240-pixel minimum height. After two process frames, the default dialog requested with `popup_centered(Vector2i(560, 480))` measured 55 × 1858, with a 1801-pixel form. Setting `wrap_controls=false` and `min_size=Vector2i(560, 480)` produced a 560 × 480 window with the same 1801-pixel form. Disabling automatic wrapping for the short help label reduced the form to 423 pixels in the same window. In Poem, a larger form with the same pattern put the JSON file controls below the dialog. The [Window documentation](https://docs.godotengine.org/en/4.5/classes/class_window.html#class-window-property-wrap-controls) describes how window sizing uses content minimums. The [AcceptDialog documentation](https://docs.godotengine.org/en/4.5/classes/class_acceptdialog.html) describes the dialog actions.

## Re-check

In headless Godot with a writable log path, use a project with a 720 × 640 root viewport and embedded subwindows. Add a VBoxContainer to a new AcceptDialog. Add a Label with the text “Copy this campaign or paste another Poem campaign document.” and set `autowrap_mode=TextServer.AUTOWRAP_WORD_SMART`. Add a TextEdit with `custom_minimum_size.y=240` and `size_flags_vertical=Control.SIZE_EXPAND_FILL`. Call `popup_centered(Vector2i(560, 480))` in the same frame. Measure the dialog, form, and lower action positions after two process frames. Repeat with explicit minimum dimensions and a non-wrapping help label.

## Apply

Check that both the embedded window and its controls fit their intended bounds. For a short fixed-width form, set the window dimensions explicitly and use non-wrapping labels where the text fits. Put long or variable content in a bounded scrolling control when it needs to wrap.

## History

- 2026-11-25 — Codex isolated window and form sizing while repairing offscreen controls in Poem's campaign editor.
