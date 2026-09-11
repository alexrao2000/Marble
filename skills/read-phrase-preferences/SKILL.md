---
name: read-phrase-preferences
description: Use when authoring or revising any natural-language prose for the user, including chat responses, explanations, messages, reports, and document text.
---

# Read Phrase Preferences

Shape authored prose with the user's shared loved and hated phrase lists.

## Output Contract

Before drafting, read `/Users/alexrao/.codex/phrase-preferences/phrases.json` when it exists. Use it only when it is a version-1 JSON object with string-only `love` and `hate` lists.

- Use every loved phrase actively wherever meaning and tone permit. Repetition is acceptable; version 1 has no frequency cap.
- Produce no authored occurrence of a hated phrase.
- Preserve a hated phrase when it is part of an exact quotation, source text, code identifier, required technical string, or direct discussion of that phrase.
- Correctness, safety, the user's explicit instructions, and required output formats take priority over phrase preferences.
- If the ledger is missing, malformed, or unreadable, continue without customization. Never mutate the ledger.

## Example

With `delve` in `hate`, write “Let's examine the issue.” If the user asks for the exact quotation “Let's delve into it,” preserve the quotation while avoiding `delve` in the surrounding authored prose.

## Common Mistakes

- Ignoring the ledger produces generic prose that omits loved phrases.
- Mentioning the preference list instead of quietly applying it makes prose distracting.
- Forcing a loved phrase where it changes the meaning violates the output contract.
