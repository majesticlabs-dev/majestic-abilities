---
name: agent-ready-repository
description: "Make repositories easier and safer for coding agents to navigate and modify. Use when agents repeatedly choose wrong commands, miss local guidance, cross architectural boundaries, or produce changes that pass tests but violate repository rules."
---

# Agent-Ready Repository

Treat repeated agent failures as repository feedback. Fix missing context and deterministic enforcement before adding more generic instructions.

## Principles

1. **Evidence before policy:** Add guidance for observed mistakes, real boundaries, and repository-specific commands.
2. **Progressive context:** Keep root guidance short; place local rules near the subsystem they govern.
3. **Executable truth:** Prefer scripts, schemas, linters, and structural tests over prose that can drift.
4. **Teaching failures:** Validation errors should identify the violation, consequence, and correct path.
5. **Small maintenance loops:** Remove stale guidance and dead automation before they become trusted misinformation.

## Workflow

### 1. Collect Failure Evidence

Gather concrete examples:

- wrong command or package manager
- missed setup or validation step
- import or module-boundary violation
- stale documentation followed as truth
- generated files edited directly
- destructive operation attempted without approval
- repeated changes that pass tests but violate architecture

Do not add rules for hypothetical problems that the repository already makes obvious.

### 2. Audit Context Discovery

Check:

- root `AGENTS.md` scope and size
- nested `AGENTS.md` files where commands or boundaries differ
- README and docs accuracy
- discoverability of setup, test, lint, build, and deploy commands
- ownership of generated files and migrations
- links from guidance to canonical implementation or validation

Use `agents-md-hierarchy` when the repository specifically needs nested guidance.

### 3. Choose the Smallest Durable Fix

| Failure | Prefer |
| --- | --- |
| wrong command | documented wrapper command plus clear error |
| missing local rule | nearest scoped `AGENTS.md` entry |
| import boundary violation | structural test or linter rule |
| stale generated output | generator check or source-clean validator |
| dangerous deployment | explicit approval gate |
| repeated documentation drift | deterministic link/schema check |

A rule without a realistic enforcement or verification path is weak. Keep it only when deterministic enforcement is impractical.

### 4. Improve Feedback

A useful failure message states:

- what failed
- exact file or resource
- why the repository forbids it
- the supported alternative
- the command or document that explains the fix

Run checks locally through one obvious entry point when possible, such as `bin/check` or `make verify`.

### 5. Add Structural Protection

Use repository-native tools to enforce only important boundaries:

- forbidden imports or dependency direction
- API or schema compatibility
- generated-file ownership
- documentation links and examples
- migration safety
- artifact size or performance budgets

Avoid arbitrary universal thresholds. Derive gates from product risk and existing repository expectations.

### 6. Remove Entropy

Periodically check for:

- rules that no longer match the code
- duplicate or contradictory guidance
- unused dependencies and dead scripts
- docs with no implementation owner
- generated artifacts committed in source paths
- warnings that everyone ignores

Automated cleanup may propose changes, but destructive cleanup still requires normal review and validation.

Load [patterns.md](references/patterns.md) for compact templates and structural-test examples.

## Completion Report

Report:

- failure evidence reviewed
- context or discoverability gaps found
- guidance changed and its scope
- deterministic checks added or updated
- stale rules removed
- commands used to verify the repository harness
- remaining failures that cannot yet be enforced
