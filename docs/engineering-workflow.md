# Engineering Workflow

## Install it first

Run this from the root of the project that will use the workflow. The command installs the workflow, its seven permanent dependencies, and the temporary setup skill used to create the project verifier:

```sh
npx skills add majesticlabs-dev/majestic-abilities \
  --skill engineering-workflow codebase-investigation implementation-planning \
  code-review test-reviewer writing-pr maintain-verification-skill \
  technical-writing create-verification-skill \
  --copy --yes
```

`create-verification-skill` is a setup tool. Remove it after the project verifier is built and its first execution is validated. Keep `engineering-workflow`, the generated project verifier, and every approved skill that the verifier calls.

The workflow is explicitly invoked. Use the invocation syntax supported by your agent:

```text
Use engineering-workflow to <describe the outcome, project, constraints, and required evidence>.
```

## Create project verification

Run this once for a project, or again when the existing verifier no longer covers the requested scope:

```text
Use create-verification-skill to analyze this project and its installed skills.
Inspect https://github.com/majesticlabs-dev/majestic-abilities for relevant skills.
Propose verification checks and dependencies with stable IDs.
Wait for my approval before installation or project changes.
```

The creator performs these phases:

1. It reads the target project's guidance, entrypoints, commands, tests, fixtures, runtime setup, and installed skills. It limits analysis to the requested workflows and their direct prerequisites.
2. It reads relevant Majestic skill descriptions and instructions from a local checkout or a fetched read-only catalog snapshot. It records the catalog source and revision used for the proposal.
3. It proposes verification checks and assessment skills, each with a stable ID.

A verifier has two kinds of layers:

- **Execution layer:** runs the user paths and gives each workflow `verified`, `failed`, `blocked`, or `unrun`. It uses an existing project skill, a Majestic skill to install, or a custom check in the generated verifier.
- **Assessment layers:** catalog or project skills that inspect the change, its tests, or the running result for one named risk, such as correctness and security, test quality, data integrity, privacy, performance, or rendered UI. They produce findings. They do not run or replace the project tests.

Each check has an ID, workflow, expected result, source of that expectation, execution layer, applicable assessment items, commands or drivers, evidence, cleanup, and side effects. Each assessment item has an ID, the risk it covers, the project evidence for that risk, its inputs, and its install status.

The proposal includes a catalog coverage table: for each relevant assessment layer, every shortlisted skill with its proposed or rejected status and the reason. Every candidate with project evidence is offered as a separate item. You reduce the scope at approval. The proposal must disclose supporting skills, dependencies, credentials, processes, files, data, network access, and other target-project side effects.

The creator pauses after the proposal. It does not install a skill, create a verifier, edit project files, or run target-project mutations until the user approves the proposal.

## Review and approve the proposal

Review the IDs and approve or reject them explicitly. For example:

```text
Approve V1, V2, A2, their listed dependencies, and the disclosed creator cleanup.
Reject A1. Build and validate only the approved plan, then remove the temporary
creator after its execution is validated.
```

The proposal must disclose all required dependencies before approval. A new dependency discovered afterward requires a revised proposal and approval before installation. Rejected items stay out of the verifier, and any resulting coverage gaps remain explicit.

After approval, the creator installs only approved skills, creates only approved verifier files, and records the exact source revisions. It then builds the project verifier with:

- the approved skill calls and their call order: the execution layer first, then the approved assessment skills;
- project commands, drivers, prerequisites, and scope;
- custom checks that have a concrete observable result;
- evidence paths and report format;
- failure classification and cleanup for resources created by the run.

The generated verifier calls the approved skills during verification. It does not require `create-verification-skill` to remain installed.

## Example

For a CSV export retry workflow, a proposal could contain:

| ID | Layer | Implementation | Check or risk | Source |
| --- | --- | --- | --- | --- |
| V1 | Execution | Existing `export-check` skill | Run normal export and retry with the same input. | The project's export contract |
| V2 | Execution | Custom verifier check | Seed existing output, retry the export, and inspect one row per ID. | The project's documented idempotency requirement |
| A1 | Assessment | Majestic `data-pipeline-testing` to install | Review replay and duplicate-key test coverage for the retry path. | The project's documented retry requirement |
| A2 | Assessment | Installed `test-reviewer` | Review whether the export tests detect duplicate rows. | The project's export tests |

The user can approve V1, V2, and A2 and reject A1. The generated `verify-export` coordinator calls `export-check`, runs the existing-state check, then calls `test-reviewer` and reports its findings separately from workflow status. It does not install or call `data-pipeline-testing`, and it records the coverage lost by rejecting A1.

## Validate and finish setup

The creator validates the assembled verifier against the intended build with isolated data. It checks build identity, runs the approved workflows through their supported user paths, captures evidence outside the checkout, and confirms cleanup.

Report verifier readiness separately from product results. Each approved workflow is `verified`, `failed`, `blocked`, or `unrun`, with its expected result, observed result, evidence, and failure cause. Assessment findings are reported by item ID in a separate section. A product defect can produce a `failed` check while the verifier is valid. A broken call, helper, missing expectation, or unsafe environment leaves the verifier invalid or blocked.

After this validation succeeds, remove only the project-local `create-verification-skill` files and the installation records that it owns. Do not remove the generated verifier, its approved runtime dependencies, or their installation records. If validation is incomplete, keep the setup skill so the project can resume the build.

## Use the finished verifier

Ask the verifier to prove a product change directly:

```text
Use verify-export to prove the CSV export retry behavior after this change.
Report verifier readiness, build identity, commands, evidence paths, cleanup,
and any failed, blocked, or unrun checks with their causes.
```

Then use the engineering workflow for implementation work. The creator is no longer needed:

```text
Use engineering-workflow to fix duplicate CSV rows after an export retry.
Use verify-export for the user-path proof. Investigate the cause, plan the
smallest authorized change, implement it, review the change, run the verifier,
and report the evidence. Do not create or install another verifier.
```

The workflow chooses only the routes needed by the request. It can use `codebase-investigation` for read-only findings, `implementation-planning` for a plan or unresolved design question, `code-review` and `test-reviewer` for review, `maintain-verification-skill` when the verifier is stale, `technical-writing` for documentation, and `writing-pr` when a pull request description is authorized.

## Boundaries

The proposal and approval process does not promise whole-project coverage. It covers the workflows and evidence scope that the user approves. It does not force delegation, a browser, a model, a package manager, a production connection, a deployment, a merge, or a full repository audit. If a required command, oracle, driver, or safe data boundary is unknown, the creator reports the gap instead of inventing one.

For an explanation or investigation, keep the boundary read-only:

```text
Use engineering-workflow to explain why retries duplicate CSV rows in checkout.
Use codebase-investigation for the trace. Do not edit files or write to external
systems. Return evidence, supported inferences, unknowns, and the next decision.
```

For a plan-only request, stop before implementation:

```text
Use engineering-workflow to plan idempotent export retries in checkout.
Use implementation-planning and return the plan with its verification route.
Do not edit product files.
```
