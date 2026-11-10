---
name: backend-interview-workflow
description: Carry the design, build, verification, and runbook workflow into fresh backend interview chats
metadata:
  type: feedback
---

When Alex shares a backend technical interview brief or asks to propose a design for one, use [Interview Backend Design](../../skills/interview-backend-design/SKILL.md). This applies in fresh chats and workspaces. Propose and discuss the design first. Push back when a choice threatens correctness, the time limit, or Alex's ability to explain it. Once Alex asks to build, implement the agreed scope, run end-to-end tests through the public API, and deliver a summary and manual verification runbook. The supplied brief determines the domain and project scope.

Pretty-print and color HTTP response bodies and stored JSON in terminal verification commands. Enable JSON syntax highlighting even when the formatting command is part of a pipeline. Keep the HTTP status on its own line when it is part of the check. Show complete database values. Include the key verified commands in copyable shell blocks in the chat handoff as well as the runbook. When the user requests an HTML runbook, use compact, accessible Copy icons and keep its commands in sync with the Markdown version.
