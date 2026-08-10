---
name: feedback-write-prs-for-outside-readers
description: PR/issue/commit descriptions must be plainly readable by someone without the surrounding context
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 442e3c5d-c16f-4f25-b0ff-5dc10a9fb376
  modified: 2026-08-08T01:54:54.178Z
---

**Check before sending, every time. Repeated failures are not from missing the rule, they are from not re-reading it while drafting.**
- Sections are exactly Problem, Fix, Changes. Adding one ("What this costs", "Not done here", "Deliberately not done") breaks the template. Anything worth saying goes inside those three.
- Ban these constructions outright: "load-bearing", "the point rather than an omission", "X rather than Y" as a rhetorical frame, "which is what makes", "stated rather than discovered", "on its own reasoning", em-dash clause stacks.
- Every sentence: one idea, subject, verb. If it needs a second clause to land, split it.
- Expand every ID on first use: "ROUTE007 criterion 12", never bare `ROUTE007 c12`, and never a queue row number.
- A reader outside this project must follow it. They do not know what a band, a seam, a destination or the rented layer is.

On 2026-08-08 the user said the memory "is clearly still not fully tuned" after two PR bodies broke all of the above. The rule was not missing; it went unread while drafting.

Write PR bodies, GitHub issues, and commit messages so a reader who does not already share my context can follow them. On 2026-08-04 the user called an initial set "nobody knows what the fuck you're saying." On 2026-08-06, on a follow-up PR that still opened with two scene-setting sentences before the actual point, the user gave the fix in exact terms: "you talk like a psycho" — followed immediately by the exact required template.

**Why:** In this repo the temptation is strong to write in the spec tree's internal register — bare IDs (`EXEC_C006`, `BENCH_C007`), queue row numbers, and the clause-heavy style of `amending-the-spec.md`. That style is load-bearing inside the spec files, and it fails as communication in a PR or an issue, where the reader is deciding something rather than reading a specification. Even a "plain English" opening can still be preamble if it explains around the point instead of stating it.

**The required template, verbatim, and nothing else added on top of it:**
1. **Problem** — short, plain description of what was wrong. One or two sentences, no lead-in, no provenance clause.
2. **Fix** — short, plain description of what changed. Same register.
3. **Changes** — not one cherry-picked "best" snippet (corrected 2026-08-06: "don't call it best-of call it changes and list ALL the important changes"). List every change that matters, each as a snippet plus one plain-English sentence saying what it does and how it serves the fix. Still brief per change — this is a list of small entries, not a second essay. Skip only changes with nothing to say (a renamed variable, a moved comment) — "important" means a reader deciding whether to merge would want to see it.

Nothing else goes in the body by default: no "Detail" section, no restated verification essay. If test results matter enough to state, one line, not a section. This is a stricter and more literal version of the general "plain English first" rule below — when in doubt, this template wins.

**Every line is a complete sentence with an explicit subject and verb — no label fragments.** Corrected 2026-08-06 after a "Changes" section built entirely from noun-phrase headers: "Three new tests, two of which failed before the fix landed:" The user's own diagnosis: "is it 'We added three new tests'? Why not speak in complete sentences? It adds clarity... See how there's ambiguity here?" A fragment forces the reader to guess the missing verb — did we add them, run them, find them — and guessing is friction that full sentences remove for free. Fix: "Three new tests were added, and two of them were failing before this PR's changes landed." Every bullet, every bolded lead-in, every "X — Y:" construction gets checked for this before sending: does it have a subject and a verb, or is it a label pretending to be a sentence.

**How the general rule (still applies to prose outside this template, e.g. issue bodies):**
- Do not open with headers, an abstraction, "found while," or method narration. The first sentence is the answer to "what happened," full stop.
- Say what an ID *is* the first time it appears — "BENCH001 criterion 11 says…" — rather than assuming the reader can resolve it, and only introduce it when actually citing it.
- Short sentences. One idea each. Avoid stacked subordinate clauses and aphoristic constructions ("a sentence that still makes sense and just happens to be wrong") — this clause-heavy register is what "talk like a psycho" was about.
- Where a decision is needed, list the options plainly, name the downside of each, and say which one I would pick and why.
- Applies to the spec-tree prose too when a human is the audience for that passage.

Related: [[feedback-no-contrastive-hedging]] — the X-not-Y construction is one specific form of this same failure.
