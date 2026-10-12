---
name: create-verification-skill
description: "Create a project-local verifier skill that runs the software through its user interfaces and produces evidence of correct, intended behavior."
---

# Create Verification Skill

Create a skill named `verifier` so an agent can verify its own work during `engineering-workflow`. The main method is to run the changed software and interact with it as a user or client would. Produce evidence that shows what works, how it meets the user's intent, and what remains unproven. The evidence should be easier to review than the full pull request.

The required result is a usable verifier, not a skill pack or a catalog assessment. Start with the project's existing commands, tests, and interaction tools. Additional skills and formal methods are optional.

## 1. Establish the verification contract

Read the project's applicable guidance and inspect its entrypoints, contracts, launch commands, tests, fixtures, and local skills. Derive project facts from current files, not from installed skill names.

For each user path in scope, identify:

- the intended behavior and its source, such as the request, acceptance criteria, or documented contract
- the starting state, user action, and observable expected result
- the real interface to exercise: UI, CLI, API, job boundary, library consumer, or another project interface
- the evidence that would let a reviewer assess that result

When the request is to create a project verifier without a named feature, make it select paths from each future task's acceptance criteria and changed interfaces. Include concrete project commands and representative flows. Do not require whole-project coverage for every change. Ask only when an unresolved product expectation, scope choice, or permission changes the result.

A request to create the verifier authorizes its local files and safe, disposable validation. Honor an explicit proposal-only request, but do not insert another approval phase into an already authorized build. Creation does not authorize product changes, new dependencies, production access, or deletion of existing skills.

## 2. Write the project skill

Use the project's existing local skill directory, or `.agents/skills/verifier/SKILL.md` when none is configured. Set frontmatter `name: verifier`. Its description must tell the agent to use it to verify changed behavior and capture evidence before reporting engineering work complete. Keep it usable without this creator or a fixed harness.

Inspect an existing verifier before editing it. Preserve supported checks and resources unless the requested change authorizes their replacement. Do not rename the catalog's `create-verification-skill`; `verifier` is the name of its generated project skill.

Include the project-specific instructions needed to perform this loop:

1. **Select proof.** Read the current task's acceptance criteria and diff. Map each material requirement to a user action, expected outcome, and evidence. Include the failure, retry, persistence, or access-control paths affected by the change. Derive expectations independently of the new implementation. For documentation-only work, use structural checks and validate changed commands as needed.
2. **Prepare and identify.** Use the supported build and launch commands, disposable data, and local services. Record the source revision and local changes, environment, and the process, binary, or served asset actually used. Confirm that a build or restart loaded the changed artifact. State prerequisites and how to stop or clean up resources created by the run.
3. **Exercise the interface.** Perform the actual user or client actions. Existing end-to-end tests can supply this interaction when they exercise the affected boundary and assert the intended result. Lint, compilation, mocked internals, a server health response, or code inspection alone do not prove a user workflow.
4. **Compare and capture.** Compare the observed state with the expected result. Save evidence for each requirement. Record failures and missing evidence, even when the test process exits successfully.
5. **Correct and repeat.** In an implementation task, return defects to the implementing agent, correct them within the task's authority, and rerun the failed path plus affected checks. In a verification-only task, report defects without changing product code. Never change an expectation just to make a failing implementation pass. Stop when the scoped contract is proven or a concrete blocker prevents it.
6. **Report and clean up.** Retain the review evidence before cleaning up only the resources created by the run. Report verified, failed, blocked, and unrun paths separately, with remaining limits.

Write exact commands, paths, data setup, and capture methods supported by the project. Do not invent a universal skill execution command. Add an owned helper only when an existing tool cannot reliably perform a required action or retain its evidence. Do not require a new script, registry, approval record, or skill dependency for an instruction-only verifier.

## 3. Make evidence reviewable

Choose artifacts that show the relevant behavior:

| Interface | Useful evidence |
| --- | --- |
| UI | Screenshots of the relevant states, or video for a sequence or timing behavior, with the actions and observed outcomes |
| CLI | Command, inputs, exit status, stdout/stderr, and the resulting file or state |
| API | Sanitized request and response, status, and evidence of the resulting state or side effect |
| Jobs or events | Trigger, observed state changes or deliveries, and relevant retry or failure results |
| Library | A real consumer invocation, its result, and checks of the public contract |

For UI work, require screenshots and/or video from the actual run. Inspect the captured artifacts. A screenshot proves appearance at a moment; pair it with assertions or recorded actions for interaction, persistence, and error behavior. Do not substitute mockups or generated images for runtime evidence. If capture fails, report the evidence gap.

Use one short report that links each acceptance criterion to its expected result, observed result, status, and artifact. Include reproduction commands, build identity, external substitutes, cleanup, and relevant limits. Save evidence outside the checkout or in the project's designated ignored artifact location. Remove secrets and private data before sharing. Do not claim deployment or live-service behavior from local test evidence.

For state-machine or concurrency risks, the verifier may use a TLA+ model or another suitable formal method when the task warrants it and tools are available. Retain the model, assumptions, checked properties, checker result, and any counterexample. Model checking proves properties of the model under those assumptions; it does not replace runtime proof of the implementation.

## 4. Keep additions optional

Inspect or install additional skills only when requested or when a specific proof gap justifies proposing one. Do not require a catalog scan, assessment table, skill pack, or reviewer panel to build or run the verifier. Missing optional skills must not block checks that the project can already execute.

Disclose new dependencies and external side effects before actions that need additional authority. Preserve existing authorization. Keep assessment findings separate from evidence produced by running the software.

Do not remove this creator, other skills, or lock entries by default. If the user requests creator cleanup, do it only after validation and only for the named project-local installation. The bundled `scripts/cleanup_project_creator.py` supports a dry run for that optional operation. Never remove the catalog source or a shared installation.

## 5. Validate and deliver

Validate the generated frontmatter and referenced commands, paths, and prerequisites. Then use the generated instructions on a representative disposable workflow: identify the build, perform the interaction, compare the result, capture and inspect evidence, and verify cleanup. Check that an unmet expectation or absent evidence would produce a failed or blocked result, not a success claim.

Report skill validation separately from product verification. A working verifier may expose a product defect. A missing environment, driver, expectation, or artifact leaves the affected proof blocked. Do not describe instructions that have not run as runtime-validated, or one representative run as full project coverage.

Return the `verifier` path, the workflow exercised, checks actually run, evidence links, and any failures or remaining limits. The agent can then load `verifier` during `engineering-workflow` without repeating setup or installing optional skills.
