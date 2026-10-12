# Engineering Workflow

## Install the workflow

Run this from the target project root:

```sh
npx skills add majesticlabs-dev/majestic-abilities \
  --skill engineering-workflow codebase-investigation implementation-planning \
  code-review test-reviewer writing-pr maintain-verification-skill \
  technical-writing create-verification-skill \
  --copy --yes
```

This installs the workflow, its declared dependencies, and the verifier creation tool. The generated `verifier` uses the project's existing commands and interaction tools. It does not require an additional skill pack or the creator at runtime. Removing the creator after setup is optional and requires an explicit request.

## Create the verifier

Use the invocation syntax supported by your agent:

```text
Use create-verification-skill to create this project's verifier.
Use the current project commands and tests to exercise real user paths.
Capture evidence that shows correct behavior and matches the task's intent.
Validate it on a representative workflow with disposable data.
```

The creator reads the project's guidance, contracts, entrypoints, test tools, and installed skills. It creates `verifier/SKILL.md` in the project's skill directory, usually `.agents/skills/verifier/SKILL.md`, with frontmatter `name: verifier`.

The verifier selects proof for each engineering task instead of running every project check by default. It records the expected behavior, identifies the build, interacts with the affected interface, compares results, and saves reviewable evidence. Additional checks required by repository policy still apply.

For UI changes, evidence includes screenshots and/or video from the running application, with the actions and observed results. CLI evidence can include a command transcript, exit status, and resulting files. API evidence can include sanitized requests, responses, and state changes. Existing end-to-end tests can provide the interaction when they exercise the affected boundary.

Skill packs, catalog assessments, and formal methods are optional. For a state-machine problem, a TLA+ model can add evidence when justified. Its report must state the assumptions and checked properties; it does not prove that the running implementation matches the model.

## Use it during implementation

```text
Use engineering-workflow to fix duplicate CSV rows after an export retry.
Use verifier to run the export, retry it with the same input, and inspect
that each expected row appears once. Retain the command transcript and
output file with a short expected-versus-observed report.
```

The workflow investigates, implements, and verifies within the requested scope. When a check fails, it corrects the defect and repeats the affected proof. It does not change the expected behavior to match a defect. Use `maintain-verification-skill` when existing verifier instructions or drivers need correction.

The final evidence report links each material acceptance criterion to its expected result, observed result, status, and artifact. It identifies the revision and running build, records reproduction commands and cleanup, and separates verified, failed, blocked, and unrun paths. Local tests do not prove deployment or live-service behavior. A representative setup run validates that route, not the whole project.

If no verifier exists, the workflow uses sufficient existing checks and reports missing proof. A request to create a verifier authorizes its local setup and safe validation. It does not authorize new dependencies, production access, or removal of existing skills. Ask only when a missing decision changes scope, expected behavior, or authority.

## Read-only work

For an investigation or review, report findings without product edits:

```text
Use engineering-workflow to explain why retries duplicate CSV rows.
Trace the cause and return evidence and unknowns. Do not edit files.
```

For a plan-only request, return the plan and verification route without implementation. A verification-only request can run safe checks and report defects, but does not authorize product fixes.
