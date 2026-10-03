---
name: maintain-verification-skill
description: "Audit and update an approved project verification coordinator against current code and runtime without silently changing its dependencies or contract."
---

# Maintain Verification Skill

Use this skill when a project-specific verification coordinator may be stale after a code, command, dependency, or runtime change. Audit the approved workflow and its exact skill calls, update only owned verification resources, and run the affected user paths.

## Boundary and approval

- Establish the project root, existing coordinator path, requested audit scope, applicable repository guidance, disposable environment, and evidence location outside the checkout.
- Read the complete coordinator, its approval record or generated call plan, all owned references and helpers, and the project evidence that supports the audited workflows.
- Keep changes inside the coordinator directory and its owned references or helpers. Do not edit product code, product tests, shared drivers, deployment configuration, permissions, or unrelated documentation.
- Do not silently install, replace, upgrade, remove, or re-resolve a referenced skill. Do not add a required workflow, skill call, dependency, permission, or custom artifact during maintenance.
- If an added or replaced call, dependency, expectation, or custom artifact is needed, show a proposal with its reason, source, scope, side effects, and coverage impact, then wait for explicit approval before editing or installing it.
- Preserve the approved product expectation when the product fails. Report a product regression separately from stale verification, a broken owned driver, an environment block, or an unrun path.
- Do not use installed skills as evidence of the product stack. Trace the current project from its source, contracts, commands, tests, and documentation.

## 1. Read the approved baseline

Locate the coordinator through the project's configured skill directory, or inspect `.agents/skills` for the requested skill. Read its full contents and record:

- approved scope, workflow IDs, prerequisites, and exclusions
- the exact approved skill names, local paths, source categories, revisions, and lock entries
- each call's inputs, order, expected result, evidence, failure behavior, and cleanup
- approved custom instructions and helper contracts
- build identity signal, disposable-state boundary, and evidence location

If the coordinator has no approval record or call plan, treat its current declared calls as the existing baseline. Do not infer permission for new calls from a missing record. If the skill cannot be found, stop and report the blocker. Do not create a replacement during maintenance.

## 2. Compare current project and dependencies

Trace every applicable workflow and call in the requested scope to current project evidence. Classify each as `current`, `stale`, `missing`, `unknown`, `out-of-scope`, or `blocked`. Check:

- entrypoints, commands, flags, ports, environment variables, fixtures, and reset actions
- expected results and failure signals against explicit contracts or established user-facing requirements
- exact installed skill paths and source revisions against the approved dependency resolution and project lock state
- whether each referenced skill still loads through the project's supported loader or active harness
- custom helper inputs, outputs, errors, ownership, and cleanup
- build identity checks and cleanup boundaries for shared or pre-existing state

Current implementation output alone does not authorize a changed expectation. A changed expectation requires an explicit contract, recorded intended behavior, or user approval.

## 3. Report changes before expanding scope

For every stale or missing item that can be corrected within the approved baseline, prepare the smallest update. For anything that would add or replace a call, dependency, custom helper, permission, or required workflow, stop and present a change proposal before editing. Include:

- a stable item ID and affected workflow
- the current evidence and the proposed source or replacement
- expected behavior, evidence, side effects, and cleanup
- dependency and source revision changes
- the coverage gained or lost if the item is rejected

Do not install or replace anything while waiting for approval. Rejected additions remain out of the coordinator and their coverage gaps stay explicit.

## 4. Run the existing instructions

Use the documented preparation and launch path in a disposable environment. Before workflows, confirm the running process, package, binary, or served asset with the strongest supported build identity signal and record it.

Run each applicable approved workflow in the audit scope, then the approved assessment-layer skill calls in their recorded order. Report assessment findings by item ID, separate from workflow status. Load the exact approved skills through the active harness's native mechanism when needed. Do not invent a universal skill execution command or force a harness, provider, model, or panel. If an approved dependency cannot load, report `blocked` or `verification-stale`; do not silently inline or replace it.

Save command output, logs, response data, screenshots, or other project-supported evidence outside the checkout before cleanup. Use no shared or production state. Clean only resources created by the run and verify cleanup.

Classify failures by cause:

- `verification-stale`: a path, call, command, dependency resolution, map, or expectation no longer matches approved project evidence
- `driver-failure`: an owned helper cannot perform a still-valid approved action
- `product-regression`: the current product violates the approved expected result
- `environment-blocked`: a required safe runtime or prerequisite is unavailable
- `unrun`: an applicable approved workflow could not be exercised

Keep the expected result and observed result together for every product regression. Do not edit the expectation to match the failure.

## 5. Update only approved resources

After approval for any scope expansion, or immediately for a correction inside the existing baseline, update only the coordinator and its owned references or helpers. Preserve:

- approved skill names, paths, source revisions, and call order unless the change was approved
- inputs, expected results, evidence rules, failure behavior, and cleanup contracts
- product failures and unsupported or unknown cases

Do not add a dependency because it seems useful, install a replacement because the original is missing, or create a helper to hide an environment blocker. Report those conditions for a new proposal.

## 6. Re-run changed coverage

Run changed workflows again from a clean disposable state. Recheck dependency resolution, skill loading, build identity, evidence capture, and cleanup. The coordinator is current only when the changed instructions execute against the current project and all remaining stale, missing, unknown, blocked, and unrun cases are named.

## Report

Return a table with one row per mapped workflow in scope:

| Workflow | Approved calls | Expected result | Observed result | Status | Evidence | Cause or blocker |
| --- | --- | --- | --- | --- | --- | --- |
| ... | exact skill names and paths | ... | ... | current/stale/verified/failed/blocked/unrun | absolute path | ... |

Also report:

1. the coordinator and owned resources changed
2. the exact approved dependencies and whether their paths, revisions, lock entries, and call contracts still resolve
3. any proposed additions or replacements awaiting approval
4. product regressions separately from verification-stale and driver-failure findings
5. evidence and cleanup results
6. unchanged, unknown, blocked, and unrun workflows

## Quality gate

Before declaring maintenance complete, confirm that:

- the coordinator, approval record or baseline call plan, and all owned resources were read in full
- every applicable workflow was traced to current project evidence
- exact approved dependencies and call contracts were checked without silent installs or replacements
- any new or replaced call or custom artifact received explicit approval
- the running build identity was checked in disposable state
- evidence was saved outside the checkout before cleanup
- changes are limited to approved verification resources
- product regressions retain their original expected results
- stale, missing, unknown, blocked, and unrun cases are explicit
- changed workflows were executed again when their environment allowed it
