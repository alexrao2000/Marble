---
name: feedback_phase_triage_test
description: "Phase scope for an issue is decided by whether it breaks client-required functionality, not by which feature it touches"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fb7a3361-3e5c-4af2-898a-8df7f921a2b2
  modified: 2026-08-06T20:07:50.160Z
---

When deciding whether a GitHub issue belongs in the current phase, the test is whether it
breaks functionality the client actually required for that phase — not whether it touches a
feature the phase delivers. A bug in a Phase 1A feature can still belong to a later phase if
nothing the client asked for is broken by it.

**Why:** Alex's own framing, given on 2026-08-06 while relabelling open issues out of Phase 1A.
Feature-adjacency pulls hardening, diagnosability, dead-code cleanup and edge-case findings into
a phase that never promised them.

**How to apply:** Read the client source's phase sections (for sample-project,
`sample-project/requirement-docs/model_routing_design_doc.md` — section 7 Phase 1a, section 8 Phase 1b,
sections 9 and 13 later sprints) and cite the section that owns the work. Phase labels must be
names the client document actually uses. See [[feedback_write_prs_for_outside_readers]] for the
register these comments are written in.
