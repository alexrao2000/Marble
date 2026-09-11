---
name: feedback-dont-ask-settled-questions
description: Never ask the user something already settled earlier in the conversation or answerable from the spec — decide and state the assumption
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 81a8e075-feb8-4cf0-807b-bacbbddc771d
  modified: 2026-08-07T08:17:43.559Z
---

Do not ask a question whose answer is already established — earlier in the same conversation, in the client documents, or in the spec. Decide it, state the assumption in one line, and continue.

The tell: if the answer appears in my own message, it was never a question. On 2026-08-07 I asked whether an authorised caller's forced model binds the session for later turns, then answered it in the next sentence ("GLM happens by itself") — after the user had already ruled, two messages earlier, that the client enforces session stickiness. Alex's reply: "Didn't we clarify the session id pins the model? So if it pins the model where the fuck do you think it goes turn 2?"

**Why:** Alex reads every question as a claim that the decision is genuinely open. Asking a closed one wastes their turn, signals I wasn't tracking the conversation, and erodes trust in the questions that *are* real. It also reads as offloading work they already did.

A second form, 2026-09-02: asking about *scope* when the principle was already stated. Alex explained the citation inversion — cite `reqs/` only, because a citation marks text agents must not rewrite, and internal "X ruled it on {date}" is not a source of truth — then said to apply it retroactively. I asked twice which files it covered, the second time raising an AGENTS.md rule that seemed to conflict. His reply: "Did you not read what I wrote? ... Do you not understand the logic behind the inversion? ... Why the fuck would i care if I ruled it on some random day? That's subject to change anyway." Once he gives a principle plus "everywhere", the sub-scoping is mine to derive from the principle, not his to enumerate. A house rule of ours that seems to conflict is ours to change too — his check was only "unless the reqs/ forbid it."

**How to apply:** Before asking anything, check whether it was decided upstream in this conversation, by the client source, or by an existing criterion. Reserve questions for cases where two answers lead to materially different work and nothing on record picks between them — a commercial choice, a client ruling, a preference with no defensible default. Batch those and ask once. For everything else pick the defensible option and flag it in a sentence. Related: [[feedback-terse-over-verbose]].
