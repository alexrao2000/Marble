---
name: slack-md-upload-classification
description: Slack ignores the .md extension on an uploaded file and classifies the bytes; non-ASCII makes it "Binary" and a few Pascal reserved words in the prose make it "Pascal", and neither renders as a document
metadata:
  type: observation
  subject: Slack file upload classifier (desktop and web client, no version exposed)
  observed: 2026-09-14
  status: active
  recheck_after_days: 90
---

## Observed

A `.md` file uploaded to Slack renders as a formatted document only if Slack's own content
sniffer agrees it is Markdown. Two classifications hide the document behind a download card:

- **"Binary"** when the file contains any non-printable byte. 44 em-dashes, three UTF-8 bytes
  each with two outside printable ASCII, plus one emoji were enough.
- **"Pascal"** when the text is pure ASCII but the prose contains a few distinctive Pascal
  reserved words. Three were enough: `label`, `string`, `records`. Common English that is also
  Pascal (`and`, `to`, `not`, `in`, `of`) was dense throughout and did not matter.

The label Slack shows is also a dropdown: a reader can force "Markdown" per upload. It works and
has to be redone every time.

## Evidence

Eleven uploads of the same 24 KB runbook, cut different ways, 2026-09-11 to 2026-09-14.

- The original, with em-dashes: Binary. Converted to pure ASCII, byte-identical otherwise: Pascal.
  So the two classifications are separate mechanisms.
- Split into three files by section: two rendered as Markdown, one (Parts 5 to 8) came up Pascal
  despite being the smallest at 7.1 KB. Size ruled out.
- That file split into its four sections, each alone: three rendered, one (Part 6) Pascal.
- Ruled out by controlled single-variable uploads: fenced code blocks (a 2.4 KB file with six
  rendered), a JSON line with braces (removing it changed nothing), a heading inside a blockquote
  (removing it changed nothing), Markdown tables (present in files that rendered).
- Vocabulary diff of Part 6 against the eight sections that rendered: exactly three tokens
  unique to Part 6 were Pascal reserved words, `label`, `string`, `records`. Replacing them with
  `tag`, `run`, `entries`, nothing else changed: the full 24 KB file rendered as Markdown.
- Not reproducible locally. pygments, highlight.js (full and restricted language sets) and
  Google's magika all call every section Markdown or something other than Pascal. Slack runs
  its own heuristic. Only an upload tells.

## Re-check

Upload two files of about 1 KB to any channel or a DM with yourself:

1. Plain ASCII prose containing the words `label`, `string` and `records` in ordinary sentences.
   Expected while this holds: the card reads "Pascal". If it reads "Markdown", the Pascal half
   has expired.
2. The same prose with one em-dash. Expected: "Binary". If it renders, the Binary half has
   expired.

Thirty seconds. Needs a Slack client; there is no API path that reproduces the classifier.

## Apply

Anything bound for a Slack file upload: write pure ASCII (hyphens for dashes, no emoji), and
sweep the prose for distinctive Pascal reserved words, replacing them with plain synonyms:
`label`, `string`, `record`, `set`, `type`, `unit`, `program`, `begin`, `end`, `procedure`,
`function`, `var`, `const`, `array`, `file`. `file` and `type` appeared in sections that rendered,
so the trigger is a few distinctive hits rather than any one word.

Applying costs nothing and cannot harm a document, so apply it even when the re-check cannot be
run, and say so. Where the reader must see the literal text, including braces or non-ASCII, a
published page is the safer vehicle than the file.

## History

- 2026-09-14 · Claude, in session with Alex · measured across eleven uploads; entry written.
  Slack documents none of this and may change it, which is why the entry is dated.
