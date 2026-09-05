---
name: session-handoff
description: "Use when handing work to another session or resuming work from HANDOFF.md."
---

# Session Handoff

Preserve active coding work in a structured file so another clean session can continue without the live message history. Treat files, repository state, and verified command results as authoritative.

## Boundary

This skill owns two operations:

- **Prepare:** capture the current task and repository state for another session.
- **Resume:** verify and continue from an existing handoff.

The handoff protocol is independent of the agent harness. Do not assume a specific command, hook name, model, tool, or session API.

A host can invoke this skill automatically, but the skill does not promise to monitor tokens, disable native compaction, stop a process, or start another session when the host does not expose those controls. Do not claim an automatic switch occurred without evidence.

Do not use a session handoff as a product specification, implementation plan, task decomposition, transcript archive, or substitute for committing required work.

Load [handoff-format.md](references/handoff-format.md) before writing or resuming a handoff.

## Triggers And Pressure Policy

Prepare a handoff when the user requests one or when the host reports a lifecycle event such as context pressure, pre-compaction, session end, repeated tool-result bloat, or an imminent session switch.

When the host supplies both used tokens and the model context limit, calculate `used / limit` and apply the host's configured policy. Use these defaults only when no policy exists:

| State | Usage | Action |
| --- | ---: | --- |
| Green | below 40% | Do nothing. |
| Yellow | 40% to below 55% | Refresh deterministic evidence and prepare a draft. Do not switch. |
| Orange | 55% to below 70% | Finish the current bounded operation, finalize the handoff, and prepare to switch. |
| Red | 70% or higher | Finalize the handoff now and switch when the host can do so. |

Treat pre-compaction as Red. Never estimate context pressure from conversation length or intuition. If telemetry is unavailable, act only on an explicit request or host lifecycle event.

A Yellow draft is not ready for transfer. Refresh it after later decisions, file changes, or verification results before finalization.

## Prepare Workflow

1. **Identify the chain.** Reuse the current `chain_id`. If none exists, create one stable opaque identifier. Do not derive it from a session ID.
2. **Resolve the store.** Follow an existing project convention. Otherwise use `.handoffs/<project>/<chain-id>/`, where `<project>` is a stable filesystem-safe project name.
3. **Inspect durable state.** Read the relevant source files and existing handoff. When Git is available, capture the absolute repository path, branch, HEAD, dirty state, changed and untracked paths, and a bounded diff summary.
4. **Capture execution evidence.** Record only commands and checks that actually ran, their results, and relevant failure details. Do not convert an unrun command into a successful check.
5. **Separate knowledge.** Distinguish settled user requirements, verified facts, implementation decisions, hypotheses, blockers, and unknowns. Record decision reasons that the next session cannot recover from code.
6. **Describe work in progress.** Name edited files, incomplete changes, temporary state, and the point where execution stopped. Do not hide partial or failing work.
7. **Set one next action.** Make it concrete enough for a clean session to start without asking the user to repeat settled context.
8. **Write safely.** For a final handoff, write the versioned history file first, then atomically replace `HANDOFF.md` with the same content. Never delete history. Do not overwrite a different existing history file.
9. **Validate the artifact.** Re-read it and confirm the schema, chain, repository identity, Git evidence, work status, verification results, blockers, and next action. Scan for secrets and remove raw credentials, tokens, private keys, and unnecessary sensitive output.
10. **Transfer control.** If the host has an authorized clean-session operation, start the new session with only the handoff path and an instruction to resume from it. Record the returned session ID in `to_session` when available. End the old session only after the final artifact is durable. Otherwise report the path and the resume instruction.

Use a temporary file in the destination directory for atomic replacement. Keep large tool output in its existing durable file and link to it instead of copying it into the handoff.

## Resume Workflow

1. Read the requested `HANDOFF.md`, or locate the latest one only within the confirmed project.
2. Validate `schema`, `chain_id`, repository path, and required sections before acting.
3. Compare the current repository path, branch, HEAD, dirty state, and changed paths with the recorded values. Report drift. Do not reset, checkout, clean, or discard changes to recreate the old state.
4. Read the named source files and tests. Prefer current files over stale descriptions in the handoff.
5. Reconstruct the objective, acceptance conditions, settled decisions, work in progress, blockers, verification state, and next action.
6. Update `to_session` atomically when the current host exposes a session ID. Do not rewrite the historical copy.
7. Continue the recorded next action unless repository drift, a blocker, or a newer user instruction makes it unsafe or obsolete.

Do not ask the user to repeat information already supported by the handoff and repository. Do not replay the full handoff in chat. State only material drift or blockers, then continue the task.

## Host Integration Contract

Optional automation can provide these capabilities without changing the handoff format:

- exact context usage and context limit
- lifecycle events and native compaction warning
- background draft generation
- current session and model identifiers
- clean-session creation with a short resume instruction
- status output

Each integration must degrade to file-only Prepare and Resume operations when a capability is absent. A configured summarizer can synthesize the structured sections, but deterministic repository evidence must be collected first and verified after synthesis.

## Completion Report

For Prepare, report:

- handoff path and chain ID
- trigger or measured pressure state
- recorded branch, HEAD, and dirty state
- artifact validation result
- new-session status, or the exact resume instruction when no lifecycle control exists

For Resume, report:

- handoff path and chain ID
- repository drift or blockers
- the next action started

## Quality Gate

Before transfer or continuation, confirm that:

- the artifact contains facts needed for the next action, not a transcript summary
- requirements, decisions, hypotheses, blockers, and unknowns are distinct
- every claimed command result came from recorded execution evidence
- partial changes and failures are explicit
- repository and Git metadata were verified or marked unavailable
- the next action is singular and executable
- history was preserved and `HANDOFF.md` was replaced atomically
- no secret or unnecessary sensitive output was persisted
- no unsupported host lifecycle action was claimed
