---
name: session-recall
description: "Reconstruct prior work on a named topic from authorized records and current repository or pull request state."
---

# Session Recall

Reconstruct useful context from earlier work when the answer spans multiple chats, task records, or revisions. Return compact, evidence-based context that lets the current session make the next decision.

## Boundary

Use this skill for a named topic, project, repository, feature, incident, or decision whose history is distributed across available records.

This skill is read-only. It does not change files, instructions, task state, pull requests, or external systems. It does not start implementation, send messages, or treat a prior plan as permission for a new action.

Use a handoff workflow when one confirmed `HANDOFF.md` already contains the task's continuation state. Use this skill when the relevant context must be reconstructed from several records or when current state may have changed since the earlier work.

## Required Inputs

Define the recall question from the user's request and current context:

1. The named topic, project, repository, feature, incident, or decision.
2. The relevant scope, such as a branch, pull request, release, component, or person.
3. A time range only when the user supplied one or the question requires one.
4. The decision or next action the recalled context must support.

Do not invent an arbitrary time window. If the topic is too broad to search responsibly, ask one concise question or return the bounded context that can be verified.

## Evidence and Status

Keep record types and status claims separate:

- A chat, note, task, issue, or review can record intent, discussion, decisions, and reported results.
- The current repository, revision, checks, or pull request state can verify what exists now.
- A claim is **planned** when it is a stated future action without completion evidence.
- A claim is **running** when active execution is directly observed.
- A claim is **unverified** when someone reported it but no confirming evidence is available.
- A claim is **committed**, **pushed**, **merged**, or **deployed** only when the corresponding current or durable evidence proves that state.

When records conflict, use current executable repository or pull request state for current status. Preserve earlier intent and decisions as history, and show the conflict when the reason for it matters.

Report Git, pull request, and deployment status separately. A commit does not prove a push, a pull request does not prove a merge, and a merge does not prove a deployment.

## Workflow

### 1. Set the recall boundary

State the question, topic terms, project or repository, requested scope, and stopping condition. Use names, issue numbers, branch names, paths, dates, and unique phrases supplied by the user to narrow the search.

### 2. Inspect current durable state

Read the current repository state when a repository is in scope. Capture the absolute path, branch, revision, dirty state, changed paths, and relevant local log entries when available. For a pull request or release, read its current status through an authorized, current interface when one is available. Do not treat an old message as proof of current state.

### 3. Search authorized records narrowly

Use the available indexed search, task records, chat or conversation API, notes, issues, reviews, and durable logs that the current environment authorizes. Search topic terms and identifiers first. Read the smallest relevant excerpts, then expand only when a decision, failure, or contradiction needs context.

Do not assume a fixed transcript path, a particular client, a hidden archive, or an external service. Do not perform a broad history sweep when focused records answer the question. If a source is unavailable, record the gap instead of substituting guesswork.

### 4. Reconstruct the chain

Order the relevant events and decisions. For each item, record:

- the source and date or revision when available
- what was requested, decided, attempted, or observed
- the evidence strength and current status
- the consequence for the current task

Include failed attempts and unresolved decisions when they prevent repeated work. Remove conversational repetition and details that do not affect the next decision.

### 5. Check for state drift

Compare historical claims with the current repository and pull request state. Check branch and revision relationships, changed files, test evidence, merge state, release or deployment markers, and any other state that directly answers the question. Mark a result as `unknown` when the needed evidence is missing.

### 6. Return compact actionable context

Use this shape unless the user requests another format:

1. **Recall question and scope**
2. **Current verified state**
3. **Relevant decisions and rationale**
4. **Work status:** planned, running, unverified, committed, pushed, merged, or deployed
5. **Failures, conflicts, and unknowns**
6. **Next action or decision supported by the evidence**
7. **Evidence references:** concise paths, record identifiers, revisions, and dates

Do not turn the result into a new plan unless the user asks for one. Do not update instructions or begin the next action automatically.

## Quality Gate

Before returning the recall, confirm:

- the topic and scope came from the request or current context
- no arbitrary time window or fixed transcript location was introduced
- current repository or pull request state was checked when it was in scope
- every status claim has matching evidence or is labeled unverified or unknown
- decisions, failures, and unresolved conflicts that affect the next action are retained
- planned work is not described as completed
- the output is compact enough to use without replaying full records
- no files, instructions, task state, pull requests, or external systems were changed
