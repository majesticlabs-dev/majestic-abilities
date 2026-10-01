---
name: technical-writing
description: "Create or review source-grounded technical documentation with verified commands, symbols, examples, and reader purpose."
---

# Technical Writing

Create or review documentation that helps a reader use, understand, or look up a technical system. Ground claims and examples in the current product, repository, and supported versions.

## Boundary

Use this skill when technical accuracy, runnable instructions, API or configuration reference, or system explanation is part of the deliverable.

This skill is distinct from:

- general articles that do not depend on a technical system
- prose revision where the source facts and technical behavior are already fixed
- pull request descriptions, which describe a change for reviewers

Do not change product code, tests, configuration, or dependencies to make documentation examples pass. Do not publish or update a remote documentation system unless the user explicitly requests that operation.

## Required Inputs

Collect only information that changes the document:

1. The reader, task, question, or decision the document must support.
2. The target format and location, when specified.
3. The product, repository, component, API, or command being documented.
4. Supported versions, platform limits, required terminology, and supplied templates or style rules.
5. The source material and evidence available for claims, examples, and expected results.

Ask one concise batch of questions when missing information changes the document's purpose or could make instructions unsafe. Otherwise state assumptions and continue.

## Choose the Document Purpose

Choose one primary purpose. A short document may combine purposes when that improves use; do not create separate files only to satisfy this table.

| Purpose | Reader needs | Useful shape |
| --- | --- | --- |
| Tutorial | Learn a concept through a guided first success | Ordered lesson with a working result |
| Task guide | Complete a known task | Prerequisites, steps, checks, recovery |
| Reference | Look up exact behavior or options | Stable headings, fields, parameters, examples |
| Explanation | Understand a system, choice, or relationship | Context, model, evidence, tradeoffs |

If the request does not identify a purpose, infer it from the reader's desired outcome and state the choice. Do not force tutorial steps into a reference or add a reference catalog to a short task guide.

## Workflow

### 1. Define the documentation contract

Write the purpose in one sentence. Identify the reader's starting knowledge, the result they should obtain, and the scope and non-goals. Record any required headings, links, examples, template structure, terminology, or author constraints. Preserve a supplied template unless the user asks for a structural change.

### 2. Build a source and support inventory

Inspect the current repository, product source, tests, configuration, generated help, and existing documentation that govern the topic. Record:

- symbols, paths, commands, flags, fields, and configuration keys
- supported versions, platforms, prerequisites, and permissions
- observable success results and known failure modes
- claims that are supplied, verified, illustrative, stale, or unknown

Use the narrowest relevant sources. Do not invent API behavior, output, version support, error messages, examples, links, or user experience.

### 3. Design the document

Order sections around the reader's task or question. For every procedural step, include the action and the expected observable result. For reference material, define exact names, types, defaults, constraints, and examples when the source supports them. For explanations, connect the model to current behavior and mark uncertainty.

Keep examples small. Label an example as illustrative when it is not safe or possible to execute. Separate prerequisites and recovery guidance from the main path when that improves scanning.

### 4. Write with stable technical meaning

Use exact identifiers, command spelling, option names, paths, and version notation. Preserve code blocks and structured data unless the user asks to change them. Explain necessary terms at first use. Keep claims next to the source or evidence that supports them.

Do not add code changes, undocumented workarounds, unsupported compatibility promises, or remote links only to make the document appear complete. When the source is unclear, qualify the text or mark the gap.

### 5. Verify the document

Run checks that are safe, local, and relevant to the requested scope:

- resolve documented symbols, paths, configuration keys, and links against current sources
- run commands and examples in a disposable fixture or verified read-only local state
- compare documented output with the actual observable result
- check version and platform statements against repository metadata or authoritative project records
- confirm prerequisites, permissions, ordering, and failure guidance match the behavior

Do not run destructive, production, authenticated, or expensive actions merely to validate prose. Do not write to shared data, accounts, or external services. If the state boundary cannot be verified or an example cannot be run, state that it was not run and identify the evidence used instead.

### 6. Return the requested artifact or review

For authoring, return or write the document at the requested location and include material assumptions and verification limits. For review, report concrete accuracy, completeness, usability, or maintainability findings with their source and smallest documentation correction. Do not silently repair product code or publish the result.

## Quality Gate

Before delivery, confirm:

- the document has a clear primary purpose and fits its reader
- every command, symbol, path, version, and example is verified, qualified, or marked illustrative
- procedural steps have observable success conditions
- reference fields and constraints match the supported behavior
- supplied templates, terminology, and author constraints are preserved
- links and local references resolve when they are part of the requested scope
- no unsupported claim, code repair, remote write, or invented result was added
- checks run, checks not run, and evidence gaps are explicit

Keep the document as one artifact when that serves the reader. Split it only when the user or repository structure requires separate tutorial, guide, reference, or explanation documents.
