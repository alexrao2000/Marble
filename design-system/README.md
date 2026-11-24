# Marble design system

Use this as a starting point for interface work. Load it before choosing layout,
controls, or interaction patterns. Product design and accessibility requirements
take precedence. A project can map the rules to its own components and visual
tokens.

## Foundations

- Start with a shared spacing scale of 4, 8, 12, 16, 24, and 32 px. Use matching
  insets for related rows and panels and keep label baselines aligned.
- Keep one primary action per panel. Put frequent choices in the main workflow
  and setup controls in settings.
- Keep text readable and use a consistent hierarchy for titles, labels, help, and
  status. Allow long labels to wrap inside the label column.

## Controls

- Use semantic buttons, fields, radios, and checkboxes. Apply full-width field
  styles to text-entry controls. Give selection indicators their own fixed size
  and spacing so labels can never squeeze, stretch, or move them.
- Use one trailing indicator column for single-choice rows. Let the label use the
  remaining space. For compact choice groups, align the controls and keep target
  heights consistent when the group wraps.
- Use one clear keyboard focus ring. When a row shows the ring for its native
  control, keep the visual ring on the row. Keep keyboard progression and the
  selected state clear, including in high-contrast mode.
- Use one button layout for text and its icon. Center both on the same axis,
  use a fixed icon box, and leave consistent space between them.
- Tie conditional fields to actual selection state with a visible, hidden, and
  required state. Keep hidden fields out of keyboard and assistive navigation.

## Web starter and checks

Use the [web controls stylesheet](web/controls.css) as a baseline. Keep a
project-local copy or implement the same primitives in the project's component
system so builds are portable. Use `ds-field` for text entry, `ds-choice` for
native radios and checkboxes, `ds-choice-row` or `ds-choice-chip` for their
wrappers, and `ds-focus` for a standalone trigger.

Check the running interface at normal and narrow widths, including long labels,
keyboard focus, the selected and unselected states, and conditional fields.
Check repeatable constraints in the browser using computed bounds. Alignment
and sizing regressions deserve a test against the shared primitive or the
component that exercises it.
