---
name: codebase-investigation
description: "Explain current code behavior and relevant historical rationale by tracing real paths and checking focused repository evidence."
---

# Codebase Investigation

Answer a concrete question about an existing codebase with evidence from the current implementation and, when relevant, its recorded history. Produce an explanation that another engineer can check without repeating a broad repository search.

## Boundary

Use this skill when the main deliverable is an explanation of how code works, why a current design exists, or what a focused change would affect.

Do not use it to:

- implement or modify code, configuration, tests, or documentation
- produce an implementation plan when the requested output is a plan
- review an unbounded change set for defects
- infer intent from naming or style when no supporting evidence exists

Keep the investigation read-only. Use disposable fixtures for mutable checks, or verify that a local inspection command is read-only. Do not change repository, shared, production, or external state. If this boundary cannot be established, leave the runtime check unrun.

## Required Inputs

Establish:

1. The question to answer and the behavior or design area in scope.
2. The repository, branch or revision, and current working state when they are available.
3. The audience and requested depth, when they affect the explanation.
4. Any supplied issue, commit, pull request, file, symbol, or time range that narrows the search.

Ask one concise question only when missing scope would change the investigation. Otherwise state the working scope and continue.

## Evidence Rules

Treat evidence types differently:

- **Source evidence:** behavior defined in current code, tests, or configuration. An unrun test does not prove runtime behavior.
- **Runtime evidence:** behavior observed through a command or running process whose source and build identity were checked.
- **Historical evidence:** a recorded change, decision, or discussion. This can explain history but cannot prove current runtime behavior.
- **Supported inference:** a conclusion that follows from several observations. Name the observations.
- **Hypothesis:** a possible explanation that the available evidence does not establish.
- **Unknown:** information that was not available or could not be verified.

Do not present an inferred reason as a recorded design decision. A commit message, issue, review comment, or other durable record can support historical rationale. Code alone can show what a design does, but usually cannot prove why it was chosen.

## Workflow

### 1. Define the investigation

Write a short investigation question and boundary. Identify the entry point, changed behavior, or design decision to explain. Choose a stopping condition, such as tracing a request to its observable result or explaining the consumers of a shared contract.

### 2. Read repository guidance and current state

Read the applicable repository instructions and the smallest set of files needed to locate the behavior. Record the physical repository path, revision, and relevant dirty paths when Git is available. Do not silently use stale notes when current files disagree.

### 3. Trace the real path

Follow the behavior through the actual callers and consumers. Inspect the relevant:

- entry points, dispatch, and control flow
- state changes, data boundaries, and persistence
- error paths, retries, permissions, and external effects
- tests, fixtures, configuration, and documented contracts

Use exact symbols, paths, and commands from the repository. Stop expanding the search when the question is answered or when a missing dependency prevents a responsible answer.

### 4. Check focused history when it can answer why

Search only the history and records that relate to the question. Depending on what is available, this can include file history, blame context, commits, review records, issues, release notes, or pull request details. Start with the named file, symbol, change, or time range. Do not perform a fixed sweep of every source category.

Separate these results from the current behavior. Record the author or source and revision when available. If no durable rationale exists, say so and report the strongest supported inference or unknown instead.

### 5. Resolve conflicts and gaps

Compare code, tests, configuration, documentation, and history. Before treating runtime output as current behavior, verify the process or artifact identity against the recorded revision and relevant working changes. If that link cannot be checked, mark its source identity unknown. Preserve conflicting historical accounts as conflicts until the evidence resolves them. List meaningful gaps, such as an unavailable service, missing historical record, unexecuted path, or ambiguous caller.

### 6. Produce the explanation

Use the smallest useful structure:

1. **Question and scope:** what was investigated and at which revision.
2. **Current behavior:** the traced path, state, and observable result.
3. **Evidence:** the relevant files, symbols, tests, commands, and records.
4. **Rationale:** recorded reasons, supported inferences, hypotheses, and unknowns kept separate.
5. **Impact or next action:** only when the question asks for it, and only from the evidence.

Use a call tree, state sequence, or focused table when it makes the path easier to check. Keep citations or file links close to the claims they support.

## Quality Gate

Before returning the investigation, confirm:

- the traced path reaches the behavior or consumer that matters
- each material claim is labeled by evidence strength
- historical rationale is attributed to a durable source or marked as inference
- current repository state and revision are clear, or the limitation is stated
- meaningful gaps and conflicts are visible
- no code or external state was changed
- the answer stops at the requested scope

If the evidence cannot answer the question, return the verified partial path and state `unknown` for the missing conclusion.
