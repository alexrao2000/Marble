# observations/

Facts about systems nobody here controls, measured because their documentation was silent.
The Slack file classifier is the first. A GitHub UI quirk, a Docker Desktop default, an API's
undocumented limit are the shape of the rest.

These are not memories about the user, about how to work, or about a project. They differ in one
way that matters: they can become false without anyone here changing anything. So each carries a
date, a way to re-check itself, and a status that can move. Nothing is ever deleted.

## An entry

One file per observation, named for its subject. Frontmatter:

```yaml
---
name: <kebab-case slug>
description: <one line, the fact itself, used to decide relevance>
metadata:
  type: observation
  subject: <the external system, and its version where it has one>
  observed: <YYYY-MM-DD the measurement was made>
  status: active | superseded | retired
  recheck_after_days: <integer>
---
```

Body sections, in this order:

- **Observed.** What was seen. State it as behaviour, not as a rule.
- **Evidence.** What was done to establish it, in enough detail that nobody repeats the work.
  Controlled comparisons are worth more than one example; say what was ruled out.
- **Re-check.** The cheapest measurement that would show the observation still holds. This is
  the entry's own falsification test and the reason a stale entry can be trusted again without
  asking anyone.
- **Apply.** What to do differently because of it, and what applying costs. An observation that
  is cheap and harmless to apply can be applied even when it cannot be re-checked.
- **History.** Appended, never rewritten. Each line: date, who or what, and what changed.

## Lifecycle

**Saving.** An agent that resolves a surprising external behaviour by measuring it writes an
entry before moving on, and does not ask permission. The bar is: undocumented, measured rather
than read, and worth not rediscovering. Add a line to `INDEX.md`.

**Relying.** Before acting on an entry older than its `recheck_after_days`, run its re-check.
If the re-check passes, update `observed` in the frontmatter and note it in History. If the
re-check cannot be run, apply the entry anyway when applying is cheap and harmless, and say in
the work that it was applied unverified. Ask the user only when applying would be costly and
the re-check is out of reach.

**Amending.** An agent that finds an entry false while relying on it does not silently work
around it. It writes what contradicted the entry into History, sets the status, and moves on:

- `superseded` when a new measurement replaces the old one. Write the new entry, link both ways,
  move the old file to `retired/`.
- `retired` when the behaviour is confirmed gone or the subject no longer exists. Move the file
  to `retired/` with the counter-evidence in History.

Nothing is lost by this. A retired entry is the record that the question was already asked and
what the answer used to be, which is exactly what stops it being asked a third time.

## Index

`INDEX.md` lists active entries, one line each, with the subject and the observed date, and a
separate section for retired ones. Agents read the index first and open only what matches.
