---
name: interview-backend-design
description: Propose and review a backend design for a timed technical interview or dry run. Use when the user shares an interview brief or asks to propose a design for one.
---

# Design a backend mini-project

Treat an interview brief pasted on its own as a design request. Start implementation when the user explicitly asks to build. During design, inspect a provided starter read-only when relevant.

## Propose the design

- Identify the user-visible outcome and must-pass requirements. Separate stated rules from assumptions. Ask about gaps that materially change the contract or correctness and give a recommended default where possible.
- Recommend one design sized to the time limit. Show the API contract, the request-to-response flow, the state that must survive requests, and the failure behavior. Name one meaningful tradeoff and push back plainly on choices that risk correctness, the demo, or the user's ability to explain the code.
- If the app uses a model, identify which decisions it makes and which rules the backend enforces. Include how to test failures and run the service locally.
- End with the first working slice, the end-to-end acceptance cases, and decisions the user should confirm. Keep the design short enough to review aloud.

## After the user asks to build

- Use the supplied starter or agreed workspace. If a new project is requested, follow the user's default project-location instructions.
- Get one real request and one end-to-end test working early. Build the agreed scope and test each core requirement through the public API, including meaningful invalid inputs and failures. Fix failures, rerun the full suite, and report actual results. Distinguish checks that replace an external dependency from live checks.
- Deliver a short summary of the key choices, the exact test command and result, and remaining gaps. Include a manual runbook with setup, start and test commands, example requests, expected responses, and any reset step needed to reproduce the demo.
