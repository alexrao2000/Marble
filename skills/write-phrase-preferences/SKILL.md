---
name: write-phrase-preferences
description: Use when the user explicitly states a lasting phrase preference or repeatedly uses a distinctive word or phrase in their own language, suggesting that Codex should remember it for future writing.
---

# Write Phrase Preferences

Write explicit and confidently inferred wording preferences to the shared phrase ledger.

## Workflow

1. Identify the exact phrase and classify it as `love` or `hate`.
2. Run `scripts/update_preferences.py love "<exact phrase>"` or `scripts/update_preferences.py hate "<exact phrase>"` from this skill directory.
3. Briefly confirm an explicit preference. Quietly record an inferred preference without interrupting the current task.
4. On a validation or write error, report the concise error. The updater leaves invalid existing data unchanged.

## Recording Boundary

Record explicit statements such as “I love the phrase …,” “I hate when you say …,” or “remember that I like …” immediately. Ask one concise question only when an explicit preference leaves the phrase or sentiment unclear.

Autonomously record a phrase as `love` when all of these are true:

- The same phrase, allowing trivial capitalization or punctuation differences, appears at least three times in the user's own recent language.
- The repetition reflects the user's voice, not pasted material, quotations, source text, code, required technical names, or another person's language.
- The phrase is distinctive enough to reuse meaningfully; do not record common connective words or unavoidable subject terms.

Repeated use can infer `love`, never `hate`. Do not wait for the user to label a phrase once the evidence meets this threshold.

## Example

If the user writes “rough edges” three times in their own recent messages, record `rough edges` as `love` and continue the current task. If they later say “I hate ‘rough edges’,” record it as `hate`; the updater moves it between lists.

## Common Mistakes

- Waiting for “I like this” after a clear repetition pattern defeats autonomous learning.
- Editing the JSON directly bypasses validation, deduplication, and atomic writes.
