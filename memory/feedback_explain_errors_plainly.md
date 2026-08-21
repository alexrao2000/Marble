---
name: feedback-explain-errors-plainly
description: state a mistake in a line or two; padding it with mechanism reads as self-justification
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81a8e075-feb8-4cf0-807b-bacbbddc771d
  modified: 2026-08-13T20:30:56.879Z
---

When explaining an error, give the shortest true statement of it and stop. No mechanism section, no "why it went unnoticed", no caveats about what was and was not affected unless asked.

**Why:** after a cost-figure defect, Alex asked what "allocated cost" meant. The honest answer was two lines — `per_instance = arm_total / 300`, then `band_cost = per_instance x band_count`, i.e. the average used as if it were each task's actual cost. Instead there were sections on the mechanism, on why no test caught it, and on what was unaffected. His reaction: "It could've been a few lines... It almost reads like you're overexplaining to justify your mistake when your mistake was completely moronic." The padding does not read as thoroughness. It reads as building a case for why the error was understandable.

**How to apply:** name the error, give the arithmetic or the one-line cause, say what is being done about it. Nothing else. Show equations or numbers rather than prose describing them — Alex called the equation version "a lot simpler" than three paragraphs saying the same thing. Do not volunteer the blast radius, the reason it escaped review, or the mitigating context; answer those only if asked. This is the error-specific case of [[feedback-terse-over-verbose]], and it compounds with [[feedback-no-contrastive-hedging]]: an X-not-Y construction inside an error explanation reads as defending the X.
