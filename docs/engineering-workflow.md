# Engineering Workflow

## Installation

Run this command from your project's root. It installs the workflow and its eight required skills:

```sh
npx skills add majesticlabs-dev/majestic-abilities --skill engineering-workflow \
  codebase-investigation implementation-planning code-review test-reviewer \
  writing-pr create-verification-skill maintain-verification-skill technical-writing \
  --yes
```

List all required skills because the installer does not resolve cookbook dependencies.

## Start a task

Use `engineering-workflow` for one scoped engineering request. Give it the outcome, repository, constraints, authority, and evidence that must prove completion. It chooses the smallest route and keeps the main agent responsible for scope, changes, delegated work, and the final report.

The cookbook is explicit-only. Use your harness's normal skill invocation with this agent-neutral request:

```text
Use engineering-workflow to <describe the outcome, repository, constraints, and completion evidence>.
```

Do not assume that `/engineering-workflow` or another short slash command exists in every harness.

## One-time project verification

Create a project-specific verifier only when the requested user path needs repeatable proof and the project does not already have one. First ask the workflow to reuse an existing verifier when it covers the path:

```text
Use engineering-workflow to establish verification for CSV export in <project-root>.
Reuse an existing project verifier if it covers normal export and retry behavior.
If no verifier covers those paths, use create-verification-skill to create one from
the repository's commands, fixtures, and supported drivers. Run the documented
paths with disposable data, record build identity and evidence outside the
checkout, and report verified, failed, blocked, and unrun paths.
```

The workflow invokes `create-verification-skill` only when a new project verifier is needed. It does not create one for ordinary product work. If the verifier later becomes stale, use `maintain-verification-skill` to audit and update its owned instructions or helpers. Keep the product expectation when the product fails. Report a product regression separately from stale verification instructions, a broken driver, an environment block, or an unrun path.

`create-verification-skill` uses the requested workflows to define its scope. It reads their entrypoints, tests, scripts, fixtures, documentation, and existing project skills. For each workflow, it records the starting state, actions, supported commands, expected results, evidence, and cleanup. It marks unsupported commands or expectations as `unknown`. It does not search the Majestic catalog or download additional skills.

## Use it for each engineering task

Start each task with the user-visible result and the proof required. The workflow chooses among these routes:

| Request | Named route | Result |
| --- | --- | --- |
| Explain behavior or investigate a cause | `codebase-investigation` | Read-only findings with traced paths, evidence, rationale, and unknowns |
| Plan a change or resolve a material design question | `implementation-planning` | A bounded plan that stops before implementation |
| Implement a bug fix or feature | `implementation-planning` when needed, then the workflow's implementation stage | A scoped change with checks and user-path proof |
| Review a change | `code-review`, and `test-reviewer` when test quality needs a separate review | Findings and checks, without edits unless fixes are requested |
| Write or update technical documentation | `technical-writing` | Source-grounded documentation with checked commands, symbols, examples, and results |
| Prepare a pull request description | `writing-pr` | A title and description based on the final diff and actual evidence |

Delegation is conditional. When the user authorizes it and the host supports it, give each delegate named files, success criteria, raw evidence, and allowed side effects. Require an actual result before treating the delegated work as complete. When delegation is unavailable or not authorized, run the permitted checks in the main session and report that independent review did not occur.

## Bug-fix example

This request authorizes a feature-branch push and draft pull request. It stops before merge and deployment:

```text
Use engineering-workflow to fix duplicate CSV rows after an export retry in <project-root>.
Reproduce the failure with disposable data before editing. Trace the cause, add a
regression check for the duplicate-row behavior, and use the existing project
verifier for the real CLI if it covers this path. Maintain the verifier only if
its instructions are stale. Review the code and test, run the relevant checks,
commit the scoped change, push a feature branch, and open a draft pull request.
Report the reproduced failure, observed fix, checks and evidence, remaining gaps,
and separate commit, push, pull request, merge, and deployment status.
```

The likely named route is `codebase-investigation`, then `implementation-planning` when a material choice remains, the workflow's implementation stage, `code-review`, `test-reviewer` when needed, the project verifier, and `writing-pr` for the authorized draft pull request. The route can omit any step that the request does not need. Rerun the original trigger with equivalent starting state, including output left by the failure when that state is in scope. A health check or passing unit test alone does not prove the real CLI path. Verify the account, repository, branch, and remote before the authorized push or pull request write.

## Read-only investigation

Use an explicit read-only boundary when the user wants an explanation:

```text
Use engineering-workflow to explain why retries can duplicate CSV rows in <project-root>.
Use codebase-investigation to trace the current path and relevant history. Read
only. Return direct evidence, supported inferences, hypotheses, unknowns, and
the smallest next decision. Do not edit files or write to external systems.
```

The workflow stops with findings. It does not turn a discovered defect into an implementation task.

## Plan-only request

Use a plan-only boundary when implementation is not authorized:

```text
Use engineering-workflow to plan idempotent export retries in <project-root>.
Inspect callers and existing contracts. Use implementation-planning to define
scope, risks, steps, and verification. Use a disposable local experiment only
if current source and tests do not resolve a material design question. Return the
plan and stop before editing product files.
```

## Documentation-only request

Keep documentation work separate from product changes:

```text
Use engineering-workflow to update the CSV export task guide in <project-root>.
Use technical-writing. Verify commands, symbols, supported versions, examples,
and expected results against current sources. Use a disposable or read-only
environment for runnable examples. Change documentation only; do not change
product code or publish the result.
```

## Evidence and completion

The final report must distinguish checks that ran from checks that were recommended or unrun. Keep product failures, stale verification, driver failures, environment blocks, and missing evidence separate. Record the evidence path outside the checkout when a verifier produces runtime proof. Report commit, push, pull request, merge, deployment, and live-state status as separate claims. A commit does not prove a push, and a merge does not prove a deployment.
