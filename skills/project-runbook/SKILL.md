---
name: project-runbook
description: Write or refresh a manual verification runbook for an implemented project. Use when the user asks for one or an agreed build workflow calls for one at handoff.
---

# Write a project runbook

During implementation, retain the setup, startup, test, and demo commands that work. Write the runbook against the final implementation after verification. Use the project's existing runbook location or create `RUNBOOK.md` at the project root.

## Establish what shipped

- Inspect the actual entry point, dependencies, configuration, public interfaces, test fixtures, and test results. Compare them with the agreed acceptance criteria. Call out missing behavior explicitly.
- Trace the main flow from the public interface to its outcome. Identify the implemented behaviors a reviewer needs to reproduce, including consequential failures and any state changes.
- Run the documented startup, test, and smoke commands against the final implementation when feasible. Use disposable local data for reset and failure checks. Record which paths were observed, which used test doubles, and which remain unverified.

## Make it reproducible

- Lead with the shortest verified path to a working demo. Give the working directory, prerequisites, dependency setup, required environment variable names, start command, and readiness check. Use placeholders for secrets.
- Give the exact test command and the latest observed result. Explain how to select offline or live mode and what each mode verifies when the project supports both.
- Provide copy-pasteable steps to manually verify every core acceptance criterion. Use a small set of examples that covers success, invalid input, and each consequential failure. Include the expected status, relevant output values, and state changes where applicable.
- Include the commands to stop the service or reset demo data when relevant, plus known setup problems and verification gaps. Keep the quick demo first and put the full checklist below it.

When a later change affects the documented behavior, update the affected commands, examples, and expected results in the existing runbook. Rerun the affected checks or label them unverified.
