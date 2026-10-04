---
name: agent-ready-repository
description: "Create root AGENTS.md guidance for a project, or fix guidance, commands, and boundaries when coding agents repeatedly misuse them."
---

# Agent-Ready Repository

Treat repeated agent failures as repository feedback. Fix missing context and deterministic enforcement before adding more generic instructions.

Use the **Create Root Guidance** route when the repository has no root `AGENTS.md`. Use the **Repair Workflow** when agents repeatedly misuse existing guidance, commands, or boundaries.

## Principles

1. **Evidence before policy:** Add guidance for observed mistakes, real boundaries, and repository-specific commands.
2. **Progressive context:** Keep root guidance short; place local rules near the subsystem they govern.
3. **Executable truth:** Prefer scripts, schemas, linters, and structural tests over prose that can drift.
4. **Teaching failures:** Validation errors should identify the violation, consequence, and correct path.
5. **Small maintenance loops:** Remove stale guidance and dead automation before they become trusted misinformation.

## Create Root Guidance

1. **Check runtime discovery.** Identify the target agent runtimes and how each discovers instruction files. If a runtime reads a different file, such as `CLAUDE.md`, link or import `AGENTS.md` from it instead of duplicating content.
2. **Collect repository facts.** Read the README, dependency manifests, task runners, CI configuration, and existing docs. Record only facts the repository supports:
   - purpose and main entry points
   - setup, test, lint, build, and run commands
   - which commands mutate data, shared resources, or external systems
   - module and dependency boundaries, generated files, and migrations
   - approval gates for destructive actions, external writes, and deployment
3. **Verify commands.** Run safe local commands where practical. Mark detected but unrun commands as unverified.
4. **Record the testing policy.** Map each kind of behavior to the project's test command at its acceptance boundary. Add a testing policy, such as the acceptance-first template in [patterns.md](references/patterns.md), only when the user or team adopts it. Do not install a policy by default.
5. **Write the smallest root file.** Include repository-wide commands, invariants, and gates. Link long rationale and runbooks instead of copying them. Do not add generic coding advice, framework tutorials, or rules for problems the repository does not have.
6. **Plan nested guidance separately.** Use `agents-md-hierarchy` when areas need different commands or rules.

Report the facts used, verified and unverified commands, adopted policies, and open questions.

## Repair Workflow

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

Use the reported failure to select the relevant checks below. A focused repair does not require a full repository audit.

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
- mandatory broad reading, repeated checks, or fixed test sequences without a concrete need

Keep completion criteria: implement the requested behavior, exercise it where practical, fix failures caused by the change, and continue to the agreed endpoint or a concrete blocker. Allow safe local verification with disposable data within the task's authorization. Retain approval boundaries for destructive actions, shared resources, external writes, and deployment.

Automated cleanup may propose changes, but destructive cleanup still requires normal review and validation.

Load [patterns.md](references/patterns.md) when creating root guidance, a guidance template, or a structural check.

## Completion Report

Report:

- failure evidence reviewed
- context or discoverability gaps found
- guidance changed and its scope
- deterministic checks added or updated
- stale rules removed
- commands used to verify the repository harness
- remaining failures that cannot yet be enforced
