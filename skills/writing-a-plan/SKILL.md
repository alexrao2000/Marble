---
name: writing-a-plan
description: >-
  Write a plan someone else has to act on - a deployment plan, a migration plan, a rollout, a
  scoping note answering "what do you need from us". Orders the document by what a reader must do
  rather than by how the author reached it: title and one-line byline, the goal in a sentence, the
  numbered steps, what will be built, what will change, then the cross-cutting concerns, then the
  reasoning, then what is deferred. Step 1 is always to read the plan. Name no individuals in the
  steps. Use when a plan, scope or readiness document is going to a team, a client or a contractor
  who will execute it. Do not use for a design document, a specification, or an analysis nobody has
  to act on.
---

# Writing a plan

## Why this exists

A readiness document for the sample-project deployment was written on 2026-09-16 with the analysis
first: architecture options weighed, boundaries examined, gaps tabulated, open questions listed. It
was accurate and nobody could use it. The client's reply:

> this is very hard to follow, and the immediate ask gets lost ... That makes it difficult for
> [the contractor] to see and follow what they need to do now.

The rewrite kept almost every fact and changed only the order. It was accepted. The lesson is not
"be brief" - the second version was a third the length and still failed, because it was organised
around the *questions* rather than around the *work*. What worked was ordering the document by what
a reader does with it.

A plan has one reader: the person who has to execute it. They arrive wanting to know what to do.
Every paragraph before that is a toll.

## The order

1. **Title.** What this is. `# sample-project — Deployment Plan`.
2. **Byline, one line.** `2026-09-16, Alex Rao.` Nothing else. No logistics table of repository,
   branch, module, image, target, tracking - it reads as preamble and the reader skips it, and
   every fact in it belongs in the step that needs it.
3. **Goal, one or two sentences.** The end state in the reader's terms, not the system's.
   *"Run the router container as a service that customers call over the internet, over HTTPS, with
   an API key."*
4. **The steps.** Numbered, imperative, in execution order. This is the document; everything else
   supports it.
5. **What will be built.** The components the steps produce, one line each. The reader's mental
   model of the result.
6. **What we will change.** What exists today that does not fit, and what replaces it. Framed as
   commitments, not as a gap analysis.
7. **The cross-cutting concerns** the audience asked about - security, monitoring, cost. One
   section each, bullets, no prose.
8. **Background and decisions.** All of the reasoning, in `**Why X.**` paragraphs. A reader who
   trusts you never opens it; a reader who objects finds their objection already answered.
9. **Deferred.** Last. What is deliberately not in scope yet, and the condition that releases it.

## Rules for the steps

**Step 1 is to read the plan.** *"Read this document, including what will be built and what we
will change below."* It makes the sections after the steps part of the procedure rather than
optional context, and it gives the executor somewhere to have been told.

**Number them in execution order, including your own work.** If something you own must land before
step 9, it is step 2, not a bracketed aside at the end. A reader following a list top to bottom
must not have to jump.

**Name no individuals.** Not "Alex changes the module", not "sample-project creates the VPC". A plan with
names in it goes stale when people change, reads as an assignment rather than a procedure, and
invites the reader to skip the steps with someone else's name on them. Where ownership genuinely
differs, mark the side - *(Module side)* - not the person. The byline already says who wrote it.

**Make each step independently actionable.** Include the command, the field names, the exact value.
`max_budget` is USD; `rpm_limit` is requests per minute; the key cannot be retrieved again, only
revoked. A step that requires reading the background section is not finished.

**End with verification.** The last steps confirm the thing works from the outside - the endpoint
answers, the credential is accepted, a request without one is rejected, the alert arrives. A plan
whose last step is `terraform apply` has no definition of done.

## What not to do

**Do not present a decision as an option list when it has been made.** The first draft offered
three ways to expose the service and recommended one. The requirement was already internet access;
the options table converted a settled requirement back into a question and stalled the work. If a
decision is open, it goes in the blocking list with an owner. If it is made, the plan states what
is being built and the reasoning moves to the background section.

**Do not mix the near work with the eventual work.** Customer handover, multi-AZ, autoscaling and
load testing in among the deployment steps made every step look negotiable. They belong under
Deferred, with the condition that releases them, at the bottom.

**Do not lead with what is missing.** A gap analysis is the author's view - the shape of their
investigation. "What we will change" is the same information as a commitment, and it is shorter.

**Do not use a table where a list will do.** Tables invite a column for owner, a column for status
and a column for notes, and then the reader is parsing a spreadsheet. Reserve them for genuine
two-dimensional data, like today-against-needed.

## Checks before sending

- Can the reader find their first action within the first screen?
- Does any step require a section below it to be actionable?
- Is any individual named outside the byline?
- Is any settled decision still phrased as an option?
- Is anything in the steps releasable only after the service runs?
- Does the last step verify from outside the system?
