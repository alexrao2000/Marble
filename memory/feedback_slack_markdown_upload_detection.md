---
name: slack-markdown-upload-detection
description: "A .md uploaded to Slack renders as Markdown only if Slack's own content sniffer agrees; non-ASCII bytes make it \"Binary\" and a few Pascal reserved words in the prose make it \"Pascal\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e409754c-da80-4d64-9818-f99b7884c695
  modified: 2026-09-14T22:11:44.797Z
---

When a `.md` file is uploaded to Slack, Slack ignores the extension and classifies the bytes
itself. Two classifications hide the document. Measured 2026-09-14 across eleven uploads Alex
made of the same runbook cut different ways:

- **"Binary"** - any non-printable byte. 44 em-dashes (three UTF-8 bytes each, two of them
  outside printable ASCII) and one emoji were enough. Pure ASCII fixed it.
- **"Pascal"** - Slack then runs a language detector over the text, and it fired on three
  words that happened to sit in one section: `label`, `string`, `records`. All three are
  Pascal reserved words. Replacing them with `tag`, `run`, `entries` fixed it, nothing else
  changed. Common English that is also Pascal (`and`, `to`, `not`, `in`) was dense everywhere
  and did not matter.

Ruled out, each by a controlled upload: file size (a 7 KB section failed while 9.6 KB and 10 KB
files rendered), fenced code blocks, a JSON line with braces, a heading inside a blockquote, and
markdown tables. None of pygments, highlight.js, or Google's magika reproduces Slack's verdict -
all three call every section markdown - so it cannot be checked locally; only an upload tells.

Slack's file-type label is also a dropdown: clicking it lets a reader force "Markdown" per
upload, which works but has to be redone every time.

**Why:** Alex hands runbooks to colleagues through Slack. A file that reads as Binary or as
Pascal source is not a runbook, and it cost six upload rounds to find three words. Slack has
not documented this and may change it; the observation is dated for that reason.

**How to apply:** Anything destined for a Slack file upload: write pure ASCII (hyphens, not
em-dashes; no emoji), and sweep the prose for distinctive Pascal reserved words - `label`,
`string`, `record(s)`, `set`, `type`, `unit`, `program`, `begin`, `end`, `procedure`,
`function`, `var`, `const`, `array`, `file`. `file` and `type` appeared in sections that rendered,
so the threshold is a few distinctive hits close together rather than any one. When it matters
that the reader sees the literal text, prefer a published page over the file; see
[[reference-claude-outfit-repo]] for where this note also lives.
