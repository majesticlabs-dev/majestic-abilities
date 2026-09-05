---
name: agents-md-hierarchy
description: "Audit and refine scoped AGENTS.md guidance across a repository. Use only when a root AGENTS.md exists and a monorepo, multi-application project, package tree, or subsystem needs different local commands or rules."
---

# AGENTS.md Hierarchy

Create nested guidance only where project boundaries justify it.

## Preconditions

- Confirm that root repository guidance already exists. If it does not, stop. Run the target harness's initialization workflow when available, or create root guidance before designing a hierarchy.
- Identify the target agent runtimes and verify how each runtime discovers, scopes, and prioritizes instruction files.
- If a target runtime does not support nested `AGENTS.md` files, keep path-specific guidance in the root or another supported instruction mechanism.

## Workflow

1. Inventory existing root and nested instruction files.
   Read applicable guidance and inspect boundaries relevant to the requested scope. Expand to a repository-wide inventory only for a repository-wide audit.
2. Map stable repository boundaries using evidence such as:
   - independent dependency manifests or task runners
   - applications, packages, services, plugins, or deployable units
   - separate CI jobs or verification commands
   - documented architecture, ownership, or security boundaries
   - generated areas with distinct editing constraints
3. Record one row for every proposed nested file:

| Candidate path | Boundary evidence | Local delta | Local command | Verified? | Parent change |
| --- | --- | --- | --- | --- | --- |
| Real directory | Manifest, documentation, or configuration | Rule or command that differs from the parent | Focused verification command | yes or no | Link, removal, or clarification |

4. Reject a candidate unless all of these are true:
   - the directory represents a stable project boundary
   - at least one useful command, rule, or constraint differs from its parent
   - the guidance applies to recurring work, not one temporary task
   - nesting reduces ambiguity or root-file noise
5. Plan the hierarchy before editing:
   - retain repository-wide rules at the root
   - place only local deltas in nested files
   - remove duplicated or contradictory guidance
   - make precedence explicit only when supported by the target runtime
6. Apply the smallest change that produces a coherent hierarchy. Preserve valid existing instructions and show a diff before materially replacing them.
7. Verify every referenced path and run safe local commands where practical. Mark detected but unrun commands as unverified.
8. Report created, updated, retained, and rejected instruction files with the evidence for each decision.

## Content Shape

A nested file should normally contain only:

- the area's purpose and boundary
- local setup or verification commands
- rules that differ from the parent
- important local entry points
- common mistakes specific to that area

State the required outcome and safe operating permissions where they differ from the parent. Permit local checks with disposable data within an authorized implementation task. Retain explicit boundaries for shared data, external writes, destructive actions, and deployment.

## Anti-Patterns

- Creating nested files for every conventional source directory.
- Copying the root file into each child directory.
- Encoding generic framework advice without repository evidence.
- Assuming nearest-file precedence is universal across runtimes.
- Documenting a proposed architecture as though it already exists.
- Keeping nested files after their local distinction disappears.
- Requiring repository-wide reading or repeated file checks for every task.
- Prescribing fixed test sequences where focused checks and project requirements are sufficient.
- Repeating generic coding advice instead of defining the completion endpoint.
