---
name: to-tasks
description: "Use when turning an approved plan into dependency-aware implementation tasks."
---

# To Tasks

Turn settled work into a small graph of complete, verifiable tasks that fresh implementation sessions can execute.

## Boundary

Use this skill after the required behavior and material implementation decisions are settled. Draft tasks by default.

Do not use it to discover product policy, replace implementation planning, triage unrelated incoming work, implement the tasks, or split work that fits safely in one implementation session. Do not create local files or external task records unless the user asks for them. Obtain explicit approval of the task breakdown before any external write.

If unresolved decisions would change task scope, dependencies, or acceptance, return `BLOCKED` with those decisions. Do not invent answers.

## Required Inputs

Establish:

- the complete source plan, specification, or settled conversation
- the intended outcome, scope, exclusions, and acceptance evidence
- the current repository state and applicable guidance when code is involved
- the target task system or local output location, if creation is requested
- the exact external write authority granted by the user

When the conversation is the source, record the supported decisions and open questions before decomposition. Missing context narrows the output; it does not authorize assumptions.

## Workflow

1. **Verify readiness.** Read the full source and identify the approved behavior, constraints, acceptance evidence, and unresolved decisions. Stop when a material decision is missing.
2. **Inspect the repository.** Trace the affected paths, tests, contracts, integrations, persistence, permissions, background work, and operational surfaces. Use project terminology. Include stable subsystem or file pointers only when verified and useful. Avoid brittle line numbers.
3. **Test whether decomposition is needed.** If the complete change fits safely in one fresh implementation session and has no useful dependency graph, return `SKIP TASKS` and recommend direct implementation. Do not create process without delivery value.
4. **Find necessary preparation.** Add preparatory work only when later tasks cannot otherwise stay understandable, verifiable, and green. If removing the preparation leaves the outcome achievable and proven, omit it.
5. **Draft vertical tasks.** Make each task a narrow, complete path to one observable behavior or operational outcome. Let a task cross data, application, interface, and test layers when required. Give it all tests and verification that grade its own outcome.
6. **Handle wide refactors.** When a mechanical change cannot remain green as a vertical task, use an expand-migrate-contract sequence:
   - expand by adding the new form beside the old form
   - migrate consumers in independently green batches
   - contract by removing the old form after all migrations finish
   If batches cannot remain green alone, state the integration-branch requirement and add a final integration and verification task.
7. **Build the dependency graph.** Assign stable task IDs such as `T01`. List only blockers that prevent safe start. Remove cycles, redundant edges, and dependencies created only by an artificial split. Tasks with no open blockers form the current frontier.
8. **Write owned acceptance criteria.** Each criterion must describe an observable result, be false or unproven at the starting state, and become provable by that task alone. Trace criteria to source requirement or scenario IDs when they exist.
9. **Review the draft.** Present the numbered graph before creation. Ask the user to approve the granularity, outcomes, and blocking edges, and to merge or split tasks where needed.
10. **Create approved tasks when authorized.** Follow the repository or task-system convention. Create blockers before dependents so references resolve. Use native dependency relations only when current tool support is verified; otherwise record `Blocked by` in the task body. Do not create labels, statuses, parent links, or other metadata without project evidence or user direction.
11. **Verify creation.** Re-read every created task. Confirm that the count, content, source traces, dependency references, and frontier match the approved draft. Report partial creation or unsupported relationships plainly.

## Task Standard

Every task must contain:

- **ID and title:** stable, concise, and behavior-oriented
- **Outcome:** the complete behavior or operational result that becomes available
- **Blocked by:** task IDs that genuinely prevent safe start, or `None`
- **Source:** requirement, scenario, plan step, or decision references
- **Acceptance criteria:** observable evidence owned by this task
- **Context:** verified constraints and stable repository pointers needed by a fresh session
- **Verification:** focused checks that prove the outcome

A task is ready only when a fresh session can complete it without hidden decisions. Session size is a judgment based on scope and repository evidence, not a fixed token, file, or time limit.

## Draft Output

Return:

1. **Readiness:** `READY`, `BLOCKED`, or `SKIP TASKS`
2. **Source and scope:** authoritative inputs, exclusions, assumptions, and open decisions
3. **Task graph:** numbered tasks in blocker-first order
4. **Frontier:** tasks that can start now
5. **Creation plan:** target system or local path, requested metadata, and write authorization state

For local Markdown, follow an existing project convention. If none exists and the user requests local files, use one file per task under `.scratch/<work-slug>/tasks/<NN>-<slug>.md`.

## Quality Gate

Before creating or returning tasks, confirm that:

- the source is settled enough to decompose without inventing behavior
- decomposition is necessary for the size or dependency shape of the work
- every normal task delivers a complete observable outcome rather than one technical layer
- every task owns its acceptance and verification evidence
- the dependency graph is acyclic, minimal, and blocker-first
- source requirements and scenarios remain traceable
- preparatory and migration tasks are necessary and can remain green at their stated boundary
- no arbitrary size limit, task count, label, or status was invented
- the user approved the graph before any external write
- every creation claim is supported by a read-back from the target system
