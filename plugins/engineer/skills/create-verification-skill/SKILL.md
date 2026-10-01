---
name: create-verification-skill
description: "Create a project-specific verification skill from local repository evidence, then run its user-path checks against an isolated build."
---

# Create Verification Skill

Create a self-contained verification skill when a project needs a repeatable way to prove user-visible behavior. The generated skill belongs to the target project and records how to start the project, reach its scoped workflows, observe their results, and leave evidence.

## Boundary

- Use the current project as the primary source. Read its guidance, source, build configuration, tests, scripts, existing skills, and development documentation before writing instructions.
- Use the project-established skill directory. If the project gives no location, use `.agents/skills/<skill-name>/`.
- Inspect only the requested product and workflow scope plus the direct prerequisites needed to run it. Do not inventory unrelated features.
- Reuse existing project commands, drivers, fixtures, and skills when they already cover part of the workflow. Copy only the facts needed by the generated skill so it remains usable by itself.
- Keep the generated skill within the requested product and workflow scope. Use documented dependency setup within the task's existing authorization. Do not repair product code, change product tests, add dependencies, deploy, access production, or grant permissions as part of creating the verifier.
- Do not assume a browser, API client, shell, native app controller, model, package manager, or other harness. Select the project-supported mechanism that can prove the workflow.
- Consult authoritative documentation for a specific command or supported-version question that local evidence cannot answer. Do not import external skills or install a controller as a side effect.

## Required inputs

Establish these before creating files:

1. The project root and the requested product or workflow scope.
2. The project rules that apply to the target path.
3. The existing skill location, if one is already configured.
4. The supported build, launch, test, and cleanup commands that the repository evidence supports.
5. The available runtime or test environment and any missing execution prerequisites.

A disposable environment is required before execution and readiness, but not before writing evidence-supported instructions. If it is unavailable, create the bounded skill with the exact blocker and mark it unready. Do not invent the missing setup.

## Workflow

### 1. Inspect the project

Read the applicable repository guidance first. Then inspect the files that define the requested path:

- application entrypoints and feature code
- build and dependency configuration
- development and test commands
- existing project-local skills and automation drivers
- fixtures, seed data, test accounts, and environment requirements
- documented shutdown and cleanup behavior

Separate facts observed in files or command output from assumptions. Record unknowns that could change how the workflow is exercised.

Check whether an existing project skill already owns the same verification scope. Extend it only when the requested behavior belongs there. Create a new skill only when the scope is materially different.

### 2. Define a bounded workflow map

Choose a short, descriptive skill name that matches the project convention. The generated skill must contain a workflow map for the requested scope. Keep one entry for each user path that the skill promises to verify. Each entry records:

- starting state and prerequisites
- user-visible actions, in order
- the supported command or driver used for each action
- the expected observable result
- failure signals and the state that must be checked after the action
- data, account, port, file, or other resources created by the run
- evidence to retain

Use concrete project paths and commands discovered during inspection. Do not fill gaps with guessed commands or generic acceptance language. Mark a workflow `unknown` when its entrypoint or oracle is not supported by repository evidence.

Keep the map in `SKILL.md` when it is small. Put it in a local `references/` file only when the map would make the entrypoint hard to use. Add scripts only when a repository-supported driver cannot express a required action; keep each helper narrow, dependency-free where possible, and owned by the generated skill.

### 3. Write the generated skill

Create the skill directory and a minimal frontmatter block. The generated instructions must be self-contained and must include:

- scope, exclusions, prerequisites, and safe test-data rules
- how to prepare and identify the build under test
- how to start, reach, and reset the project state
- the workflow map and its expected observables
- how to collect evidence for each result
- cleanup for only the resources created by the run
- a report with verified, failed, blocked, and unrun workflows

Prefer existing project drivers and commands. If a helper is necessary, document its inputs, outputs, failure behavior, and cleanup. Do not turn an existing skill into a runtime dependency. Do not add product fixes or broaden the project permissions to make the verifier pass.

### 4. Prove the running build

Before exercising a workflow, use the strongest project-supported identity signal available to confirm that the process, package, binary, or served asset comes from the intended source and build. Record the signal, such as a source revision, package version, artifact path, process identity, or equivalent project-native marker. A health response alone does not prove build identity.

Use a disposable state boundary. Prefer a temporary database, directory, port, account, or test environment that the project already supports. Keep secrets and personal data out of captured evidence. If the project offers no safe boundary, report the blocker instead of using shared or production state.

### 5. Execute the generated instructions

Follow the generated skill as a new user would. Run the documented preparation and launch instructions, then exercise each workflow in the requested scope. Check the observable result against the independent expectation recorded in the map. Exercise an error or recovery path when the project contract defines one.

Capture evidence while the runtime and disposable state still exist. Evidence can include command output, structured logs, response bodies, screenshots, accessibility output, database state, or another project-supported observation. Store it outside the project checkout and record an absolute path in the report. Redact credentials and sensitive data.

Clean up only resources created by this run, after evidence is saved. Confirm that the cleanup completed. Do not remove pre-existing files, processes, data, or user state.

### 6. Decide readiness

The generated skill is ready only when its own instructions run successfully against the intended build and produce proof for the scoped workflows. Report `blocked` or `unready` when a prerequisite, driver, build identity, workflow, oracle, or cleanup step cannot be proven. A passing health check without a real user-path proof is insufficient.

## Deliverable

Return:

1. The generated skill path and name.
2. The local evidence used to define its commands and workflow map.
3. The build identity signal and disposable-state boundary.
4. A coverage table with workflow, expected observable, result, and evidence path.
5. The commands or project-native actions run, with actual results.
6. Cleanup results and any resources left for the user to remove.
7. Blockers, unknowns, and scope exclusions.

Keep product failures separate from verification gaps. If the documented expectation fails during execution, retain the expected result, report the observed product behavior, and do not edit the verifier to describe the failure as success.

## Quality gate

Before declaring the generated skill ready, confirm that:

- the skill path follows the target project's convention or the `.agents/skills` default
- the skill passes the project's structural validator or loader check, and its local references and owned helpers resolve
- its instructions do not depend on a sibling catalog skill, fixed harness, or unverified command
- every mapped workflow has a concrete action and observable oracle
- the intended build identity was checked
- the required mapped workflows were exercised through their real user paths
- evidence was saved outside the checkout before cleanup
- disposable resources were isolated and cleaned up
- verified, failed, blocked, and unrun cases are explicit
