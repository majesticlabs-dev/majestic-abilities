---
name: rails-feature
description: "Use when the user invokes rails-feature by name or asks for a full feature workflow in a Rails project."
metadata:
  requires: "implementation-planning,dhh-rails-style,ruby-coder,minitest-coder,rails-lint,rails-code-review,test-reviewer"
---

# Rails Feature Workflow

Build the requested feature through verified behavior. Use the guidance below according to the change, existing project rules, and user instructions.

## Planning

Use `implementation-planning` when the feature needs a technical plan. For a small, clear change, proceed from the existing acceptance criteria. Ask only about unresolved choices that change scope, behavior, or permission.

## Implementation

Use `dhh-rails-style` for Rails design decisions and `ruby-coder` for Ruby design questions when project guidance does not already resolve them. Load only the guidance needed for the affected behavior.

Add regression tests for bugs and tests of observable behavior for feature changes. Use `minitest-coder` when the project uses Minitest and test design needs guidance. Follow a test-first process when the project or user requires it.

## Verification

Run the checks required by the project and those needed to verify the change. Safe local checks with disposable data can proceed within the implementation request. Confirm that they cannot affect production or shared resources.

### Lint

Use `rails-lint` for configured code-quality checks that apply to the change. Keep corrections within scope.

### Tests

Run tests for the changed behavior and affected consumers. Run the full suite when required by the project or when the change has broad effects. Fix failures caused by the change, then rerun affected checks. Report unrelated failures and unavailable checks separately.

### Review

Use `rails-code-review` when a Rails review is requested or the change risk warrants it. Use `test-reviewer` when test quality needs a separate review. Use an independent reviewer when required or when it adds useful evidence. Resolve material defects and verify the corrections; repeat review only for changed or unresolved concerns.

## Completion

Continue until the requested behavior works, relevant checks pass, and failures caused by the change are fixed, or a concrete blocker requires user input. For a runnable feature, exercise the affected path when the environment permits. For an authorized build or install, confirm that the running process uses the new artifact.

Report the result, verification evidence, and any remaining blocker. Distinguish local implementation from deployment and live verification. Do not commit, push, or deploy unless authorized by the user.

## Installation

Install the cookbook and its dependencies:

```sh
npx skills add majesticlabs-dev/majestic-abilities --skill rails-feature dhh-rails-style ruby-coder \
  minitest-coder rails-lint rails-code-review test-reviewer \
  implementation-planning
```
