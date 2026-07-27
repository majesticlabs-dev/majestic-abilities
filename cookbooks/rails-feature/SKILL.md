---
name: rails-feature
description: "Build a Rails feature end-to-end: plan, implement in DHH style with TDD, then pass lint, test, and review quality gates. Use when the user invokes /rails-feature or asks for a full feature workflow in a Rails project."
---

# Rails Feature Workflow

Build the feature described in $ARGUMENTS by working through the phases below in order. Do not skip a phase, and do not proceed past a failing gate.

## Phase 1: Plan

Invoke the `implementation-planning` skill. Produce the smallest viable slice: explicit scope, ordered changes, and how each change will be verified. Present the plan before writing code.

## Phase 2: Implement (TDD)

Invoke the `dhh-rails-style` skill and follow it for every file touched. For Ruby-level design (method size, clarity, idiom), apply the `ruby-coder` skill.

Work test-first:

1. Write the failing test using the `minitest-coder` skill.
2. Implement the minimum code to pass it.
3. Refactor while keeping tests green.

## Phase 3: Quality Gates

Run each gate in order. A gate must pass before the next one starts.

### Gate A: Lint

Invoke the `rails-lint` skill: run the project's configured RuboCop, ERB Lint, and Brakeman checks and fix violations without changing behavior.

### Gate B: Tests

Run the project's full test suite (or the smallest suite the project's conventions define as the pre-push bar). All tests must pass. Report failures verbatim; never mark this gate passed with failing or skipped tests.

### Gate C: Review

Spawn a subagent with a fresh context to review the complete diff. The subagent applies the `pragmatic-rails-reviewer` skill (with the DHH simplicity lens) and the `test-reviewer` skill for test quality, and must finish with `APPROVED` or `NEEDS CHANGES`.

On `NEEDS CHANGES`: apply the feedback, re-run Gates A and B, then re-review. Repeat until `APPROVED`.

## Phase 4: Report

Summarize: what shipped, the plan deviations if any, and the outcome of each gate. Do not commit or push unless the user asked for it.

## Requires

- `implementation-planning` — Phase 1 planning contract
- `dhh-rails-style` — implementation and review style for all Rails code
- `ruby-coder` — Ruby-level design rules during implementation
- `minitest-coder` — test-writing conventions for the TDD loop
- `rails-lint` — Gate A tooling workflow
- `pragmatic-rails-reviewer` — Gate C review posture
- `test-reviewer` — Gate C test-quality review

Install everything:

```sh
npx skills add OWNER/REPOSITORY --skill rails-feature dhh-rails-style ruby-coder \
  minitest-coder rails-lint pragmatic-rails-reviewer test-reviewer \
  implementation-planning --agent claude-code --yes
```

## Hard Gates

Gates A and B are mechanical and must not depend on this skill being followed. Back them in the consuming project with hooks or CI, for example a `PostToolUse` hook running RuboCop on changed Ruby files and a `Stop` hook (or CI job) running the test suite.
