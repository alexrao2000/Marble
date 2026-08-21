---
name: feedback-comments-frontloaded
description: "comments go in one block at the top of the file; inline means same-line, and any block needs a blank line before the code"
metadata:
  node_type: memory
  type: feedback
---

Put explanatory comments in **one block at the top of the file**, not scattered above the things they describe. Three rules:

1. **Frontload.** One block at the head of the file carries the reasoning for the whole file.
2. **Inline means same line.** If something must be explained where it sits, it is a trailing comment on the code line itself — `num_retries: 2  # attempts after the first`, never two lines above it.
3. **A block needs a blank line.** Where a block genuinely has to sit mid-file, separate it from the code with a newline so the reader can see where prose stops and code starts.

**Why:** Alex gave this on 2026-08-21 after `config/litellm.yaml` reached 288 comment lines against 172 of configuration, with a 165-line essay before the first setting and explanatory blocks stacked directly on top of every key. Reading the file meant scrolling past prose to find what it declared. Volume was the first complaint and placement was the second — cutting to 68 lines did not fix it, because the survivors were still interleaved with the code.

**How to apply:** this compounds with the restraint rule, so cut before you place. Where a specification, contract or design document owns a decision, the citation is the whole comment — `@spec EXEC006 c3` and nothing else. Keep prose only for what is recorded nowhere else, and check that claim with `grep` rather than assuming it: on that file, two of five candidates turned out to have no other owner in the tree and had to stay. An absence with an owner needs the owner named, not the case re-argued — six paragraphs arguing six deliberate absences became one line each.

Worth knowing where the obligation actually comes from: the client's method document (`reqs/sample-project-sdd-v0.2.md`) requires `@spec` annotations in **code and tests**, scoped to "every modified function". Configuration files and YAML are outside that, so citations there are our own convention and the prose around them is entirely discretionary. Related: [[feedback-terse-over-verbose]] for the same instinct in prose, and [[feedback-coding-report-two-sections]] for it in reports.
