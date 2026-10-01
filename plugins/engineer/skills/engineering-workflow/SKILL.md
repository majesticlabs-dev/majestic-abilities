---
name: engineering-workflow
disable-model-invocation: true
description: "Coordinate scoped engineering work from investigation through implementation, review, verification, and handoff."
metadata:
  requires: "codebase-investigation,implementation-planning,code-review,test-reviewer,writing-pr,create-verification-skill,maintain-verification-skill,technical-writing"
---

# Engineering Workflow

Use this explicitly invoked cookbook to carry one engineering request from a stated outcome to evidence-backed completion. The main agent owns scope, planning, synthesis, the change set, and the final proof.

## Boundary and authority

- Start with the user's requested outcome, target repository, scope, non-goals, authority, and completion evidence.
- Keep edits, checks, delegation, and reports inside that scope. Preserve unrelated working-tree changes and follow the repository's branch and worktree rules.
- Investigation, analysis, and review requests are read-only. A debugging request remains read-only unless the user also requests a fix.
- A planning request ends with a plan. Do not implement while the requested deliverable is a plan.
- An implementation request permits the local edits, disposable checks, commits, feature-branch pushes, and draft pull requests that the user has authorized. Treat merges, production changes, deployments, publishing, and messages to other people as separate actions that require their own explicit authority.
- Honor persistent authorization for commits, pushes, and draft pull requests when the current request still has the same scope. Report each state separately.
- Before an authenticated external operation, verify the account and intended target. For Git or pull request writes, also verify the repository, branch, and remote.
- Re-establish scope for every new task. Persistent authorization does not carry forward an old file list, outcome, or implementation decision without checking the current request.
- Do not force a model, provider, panel, prototype, sticky session, scheduler, full-repository sweep, or universal pull request or deployment step.

If a missing decision would change the scope, behavior, or authority, ask one concise question. Otherwise record the assumption and continue.

## 1. Establish the request

Record:

- the user-visible outcome and acceptance conditions
- the repository, branch or revision, current working state, and relevant local guidance
- the files, services, consumers, and user paths in scope
- explicit exclusions, permissions, and cleanup boundaries
- the checks or observations that will prove completion

Choose the smallest workflow that matches the request:

- **Investigate or explain:** trace the real path and return findings. Keep the work read-only.
- **Review:** inspect the named change or artifact, report concrete findings, and keep the review read-only unless fixes are explicitly requested.
- **Plan:** establish current behavior, risks, steps, and verification, then stop before implementation.
- **Debug:** reproduce the reported behavior, trace the actual cause, and state the smallest correction. Implement only when the request authorizes a fix.
- **Implement:** make the smallest change that satisfies the accepted behavior, then verify it.

Do not convert an explanation, review, or plan into implementation because a defect or useful follow-up appears during the work.

For multi-step work, record the required steps and the evidence that closes each one. Track each step as pending, active, verified, or blocked. Mark a step that does not apply with its reason. Select only the routes needed for the current request.

## 2. Build the evidence base

Inspect the smallest relevant set of guidance, source, callers, consumers, tests, configuration, commands, and runtime boundaries. Use the `codebase-investigation` skill when the request needs a focused explanation of current behavior, historical rationale, or change impact. Keep current executable behavior separate from historical records, supported inference, hypotheses, and unknowns.

For a plan or material implementation choice, invoke `implementation-planning` when repository inspection, caller usage, risk tracing, or verification design is needed. Keep the plan proportional to the request. Use a disposable local experiment only when a material choice cannot be resolved from source and the experiment can run within the existing authority. A plan or experiment does not authorize implementation or production readiness.

Reuse project commands and checks. Do not add a dependency, abstraction, configuration rule, or broad test run without a concrete requirement or evidence gap.

## 3. Execute the requested work

Before execution, decide which work can be delegated when delegation is available and authorized. Use the host's native dispatch mechanism. Give each worker named file ownership, exact success criteria, relevant raw evidence, and allowed side effects. Tell workers to preserve others' edits. Run independent work in parallel and order work that shares files or depends on earlier results. The main agent owns integration and final proof.

### Bug fixes

Reproduce the failure before editing when the environment permits. Trace the real path through callers, state, boundaries, and failure handling. Correct the smallest proven cause. Add or update a regression check when it detects the reported behavior and does not mirror implementation details. Separate failures caused by the change from pre-existing or unavailable checks.

After the fix, rerun the original trigger with equivalent starting state. Include persisted state produced by the failure when it remains within the requested contract. Compare the observed result with the original expectation.

### Feature work

Use the accepted behavior and the repository's current design as the contract. Plan first when the feature has material design, integration, migration, permission, or rollout choices. Implement in small end-to-end increments. Add meaningful checks for observable behavior, important failure paths, and affected consumers. Stop when the requested scope is proven.

### Documentation work

Invoke `technical-writing` when technical documentation is part of the requested deliverable. Verify commands, symbols, versions, examples, and expected results against current sources. Use disposable or explicitly read-only state for runnable examples. Do not change product code or configuration to make documentation pass.

### Project-specific verification

Use an existing project verification skill when it covers the requested user path. Invoke `maintain-verification-skill` only when that skill is stale or its owned driver needs maintenance. Invoke `create-verification-skill` only when a project-specific verifier is needed and its creation is within the user's authorized scope. Creation is conditional and is never a prerequisite for ordinary product work or a reason to expand product scope.

Preserve the verifier's expected product behavior when the product fails. Report a product regression separately from stale verification instructions, a broken driver, an environment block, or an unrun path.

## 4. Review and verify

Run the narrowest existing project checks that prove the requested behavior. Use disposable data and an isolated or proven read-only environment. Confirm the running process uses the intended build when the request includes a build, install, or runtime check. Do not use shared or production state for local proof.

Invoke `code-review` when the user asks for a code review or the change has concrete risk that warrants a separate review. Invoke `test-reviewer` when test coverage, assertions, isolation, or failure cases need a separate review. Keep each review within the requested files and behavior.

Use a reviewer who did not write the change when independent review is requested or needed. Require each delegate's actual result before treating its work as complete. The main agent inspects the resulting change set, resolves material defects, and verifies any corrections.

When delegation is unavailable or not authorized, run the permitted checks inline and state that an independent review was not performed. Never claim a delegated review, tool result, or independent evidence that did not occur.

## 5. Report completion

Stop when the requested scope is proven or a concrete blocker requires user input. Return:

1. the outcome, scope, assumptions, and authority used
2. changed files and any delegated ownership
3. checks actually run, with their commands or project-native actions and results
4. review and user-path verification evidence
5. failures caused by the change, pre-existing failures, blocked checks, and unrun checks kept separate
6. remaining unknowns and the smallest next decision, when needed
7. commit, push, pull request, merge, deployment, and live-state status as separate claims

Invoke `writing-pr` when a pull request title or description is requested or authorized. Use the repository's final diff and actual verification evidence. Do not publish, merge, deploy, or send the description without the corresponding authority.

## Hard gates

- Read-only requests produce no edits or external writes.
- Plan requests stop before implementation.
- Bug fixes have reproduction or a clear reason reproduction was unavailable, plus a traced cause or an explicit unknown.
- Every material status claim has current evidence or is labeled unknown or unverified.
- Product failures are not hidden by changing expected verification results.
- Project verifiers are created or maintained only when needed and authorized.
- A delegated review is complete only when its actual result is available.
- The workflow stops at the requested scope instead of expanding into unrelated cleanup, whole-repository review, or future work.

## Installation

Install the cookbook and its dependencies:

```sh
npx skills add majesticlabs-dev/majestic-abilities --skill engineering-workflow \
  codebase-investigation implementation-planning code-review test-reviewer \
  writing-pr create-verification-skill maintain-verification-skill technical-writing
```
