---
name: feedback-check-method-before-restructuring
description: Before moving or renaming anything the SDD or another client source may prescribe (directory layout, document names, method steps), read that source first and push back if it conflicts; don't execute the instruction as given
metadata:
  type: feedback
---

When Alex directs a structural change — a directory move, a rename of a prescribed artefact, a change
to a method step — check `sample-project/reqs/sample-project-sdd-v0.2.md` and the other `reqs/` sources before
doing it. If a source prescribes the thing being changed, say so and stop rather than complying.

**Why:** On 2026-09-02 he asked for `docs/design/` to be "merged with the level above". I moved it
twice (up beside `docs/`, then flat into `docs/`) across three commits before he remembered the SDD
prescribes `docs/design/` for the HLD and LLDs (line 87), and asked for it all undone with "you should
double check me on stuff like this." A method prescription in a client source is not something a
session restructures on a reading of a chat message, and he wants to be caught when he forgets that.

**How to apply:** For any instruction touching layout, naming or process in `sample-project/`, grep the
SDD and `reqs/README.md` for the path or term first. If prescribed, reply with the line and don't move
it. If not prescribed, proceed. This sits alongside [[feedback-dont-ask-settled-questions]] — it is not
a reason to ask, it is a reason to check a source and report what it says.
