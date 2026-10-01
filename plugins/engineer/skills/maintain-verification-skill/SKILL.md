---
name: maintain-verification-skill
description: "Audit and update a project-specific verification skill against current code and runtime, preserving product failures as product findings."
---

# Maintain Verification Skill

Audit an existing project-specific verification skill when code, commands, dependencies, or runtime behavior may have changed. Update only the verification resources that the skill owns, then run the affected user paths and report the current evidence.

## Boundary

- Use the current project as the source of truth. Inspect repository guidance, source, build configuration, tests, scripts, runtime output, and the existing verification skill.
- Locate the existing skill through the project convention. If no path is configured, inspect `.agents/skills` for the requested skill.
- Audit only the requested workflows and their direct prerequisites. Do not turn a narrow maintenance request into a full-project audit.
- Keep changes inside the verification skill directory and its owned references or helpers. Do not edit product code, product tests, unrelated documentation, deployment configuration, shared drivers, or permissions.
- Reuse project-supported commands, drivers, fixtures, and runtime mechanisms. Do not assume a browser, API client, shell, native app controller, model, package manager, or fixed harness.
- Consult authoritative documentation for a specific command or supported-version question that local evidence cannot answer. Do not import external skills or install a controller as a side effect.
- Preserve the expected product contract when the product fails. A verification document must not be changed to make a regression look successful.

## Required inputs

Establish these before editing:

1. The project root and the existing verification skill path.
2. The requested audit scope, changed area, or reason for maintenance.
3. The project rules that apply to the skill and its helper files.
4. A disposable runtime or test environment with no production access.
5. An evidence location outside the checkout.

If the skill cannot be found, or the project cannot provide a safe environment, report the exact blocker and stop. Do not create a replacement skill as a side effect of maintenance.

## Workflow

### 1. Read and inventory the existing skill

Read the complete skill, its local references, and its owned scripts. Record:

- the workflows and prerequisites it claims to cover
- the commands, entrypoints, drivers, and cleanup actions it names
- the expected observables and failure signals
- the build identity check and disposable-state boundary
- evidence paths and reporting rules
- any unsupported assumptions or missing oracles

Treat the skill's statements as claims to verify. Do not accept a command, path, or expected result because it is written in the file.

### 2. Compare the map with the current project

Trace every mapped workflow in the audit scope to current source and repository evidence. Check for:

- renamed, removed, or newly required entrypoints
- changed commands, flags, ports, environment variables, or fixtures
- changed user actions, states, output, or failure behavior
- missing workflows within the requested scope
- references to helpers that are absent, stale, or outside the skill's ownership
- identity checks that can accept the wrong build
- cleanup that can delete shared or pre-existing state

Classify each item as `current`, `stale`, `missing`, `unknown`, or `out of scope`. Keep source observations, runtime observations, and assumptions separate.

### 3. Run the current instructions

Use the documented preparation and launch path in a disposable environment. Confirm the running build with the strongest project-supported identity signal, such as a revision, version, artifact path, process identity, or equivalent marker. Record the signal before testing workflows.

Run every applicable mapped workflow in the audit scope. Check each observable against the expected result in the skill, and run defined error or recovery paths when their prerequisites are available. Save command output, logs, response data, screenshots, or other project-supported proof outside the checkout before cleanup.

Classify failures by cause:

- `verification-stale`: the skill's path, command, map, or expectation no longer matches repository evidence
- `driver-failure`: an owned helper cannot perform the documented action even though the project path is valid
- `product-regression`: the documented action reaches the current product, but the product violates the expected behavior
- `environment-blocked`: a required safe prerequisite or runtime resource is unavailable
- `unrun`: the workflow was applicable but could not be exercised in this audit

Do not label a product regression as stale only because the result is unexpected. Keep the expected result and the observed result in the report.

### 4. Update owned verification resources

Change only what current evidence supports:

- update stale paths, commands, prerequisites, workflow actions, observables, identity checks, or cleanup rules
- add a missing workflow only when it is inside the requested scope and its expected result is supported by source or an explicit project contract
- repair an owned helper only when the project path is valid and the helper is the cause of the failed action
- remove a workflow only when repository evidence shows that the feature is gone or outside the agreed scope

Keep unsupported items marked `unknown` rather than inventing behavior. Do not change an expected result to match a failing product. Do not edit a shared driver or add permissions; report those blockers to the caller.

Change an expected product result only when an explicit contract or recorded intended behavior supports the change. Current implementation output alone cannot establish that a changed expectation is correct.

### 5. Re-run changed coverage

After edits, run the affected workflows again from a clean disposable state. Recheck build identity, evidence capture, and cleanup. Keep prior evidence when it explains a product regression or driver failure. The updated skill is current only when its changed instructions execute against the current project and its report names every applicable case that remains blocked or unrun.

### 6. Report the audit

Use a coverage table with one row per mapped workflow in the audit scope. Include out-of-scope rows only when they explain the boundary:

| Workflow | Scope | Expected result | Current status | Evidence | Cause or blocker |
| --- | --- | --- | --- | --- | --- |
| ... | in/out | ... | current/stale/verified/failed/blocked/unrun | absolute path | ... |

Report product regressions separately from verification-stale and driver-failure findings. Include the exact action, expected observable, actual observable, and evidence path for each product regression. State what was changed, what was left unchanged, and what could not be run.

## Quality gate

Before claiming maintenance is complete, confirm that:

- the existing skill and all owned resources were read in full
- the skill passes the project's structural validator or loader check, and its local references and owned helpers resolve
- every applicable mapped workflow in the audit scope was traced to current repository evidence
- the running build identity was checked
- disposable state was used and cleanup was verified
- evidence was saved outside the checkout before cleanup
- updates are limited to owned verification resources
- product regressions remain visible with their original expected result
- stale, missing, unknown, blocked, and unrun cases are explicit
- the updated instructions were executed for every changed workflow that could run
