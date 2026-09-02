# Handoff Format

Use one chain directory for all sessions that continue the same task:

```text
.handoffs/<project>/<chain-id>/
  HANDOFF.md
  history/
    <timestamp>-<old-session-id>.md
```

`HANDOFF.md` is the latest finalized transfer. Each finalized transfer must also have an immutable history copy with identical content. Use a UTC timestamp that is safe in filenames, for example `20260514T193012Z`.

A host can keep a Yellow-stage draft beside these files, but the draft must not replace `HANDOFF.md` until it passes the final quality gate.

## Canonical Template

```markdown
---
schema: handoff/v1
chain_id: <stable opaque id across sessions>
from_session: <old session id or generated local id>
to_session: <new session id or pending>
created_at: <ISO 8601 UTC timestamp>
model: <model name or unknown>
context_used_tokens: <integer or null>
context_limit_tokens: <integer or null>
repo: <absolute path>
branch: <git branch or null>
head: <full git commit SHA or null>
dirty: <boolean or null>
---

# Session Handoff

## Task

### Objective
<The exact outcome being implemented.>

### User Requirements
- <Settled requirement stated by the user.>

### Acceptance Conditions
- [ ] <Observable condition that proves completion.>

### Non-goals
- <Explicit scope exclusion, or `None recorded`.>

## Current State

### Completed
- <Completed behavior with file or verification evidence.>

### In Progress
- <Partial change, current execution point, and what remains.>

### Not Started
- <Required work that has not started.>

## Decisions

| Decision | Status | Reason and evidence | Consequence |
| --- | --- | --- | --- |
| <Decision> | settled | <Why> | <Constraint for continuation> |

## Repository Evidence

- **Relevant paths:**
  - `<path>`: <role and current state>
- **Changed paths:** <bounded list or durable status-file reference>
- **Diff summary:** <bounded summary or durable diff-file reference>
- **Environment facts:** <only verified facts needed to continue>

## Verification

| Command or check | Result | Evidence |
| --- | --- | --- |
| `<exact command>` | passed, failed, or interrupted | <bounded output or file reference> |

### Checks Not Run
- `<command>`: <why it has not run>

## Failures And Blockers

- <Failure or blocker, evidence, and required resolution. Use `None` when empty.>

## Unknowns

- <Material unknown that can change the next action. Use `None` when empty.>

## Next Action

<One concrete action for the clean session.>

## Resume Instructions

1. Verify the repository path, branch, HEAD, and dirty state against this file.
2. Read the relevant paths before editing.
3. Resolve material drift or blockers without discarding existing work.
4. Continue with the single Next Action.
```

## Field Rules

- `schema` must be `handoff/v1`.
- `chain_id` remains unchanged across all sessions that continue the task.
- `from_session` identifies the session that finalized the transfer. Generate a local unique ID when the host exposes no session ID.
- `to_session` is `pending` until a new session ID is known.
- `created_at` is the finalization time, not the first draft time.
- `model` records the model that finalized the artifact. Use `unknown` when unavailable.
- Token fields are integers only when the host provides exact telemetry. Use `null` otherwise. Never estimate them.
- `repo` is an absolute, physically resolved path when the filesystem supports it.
- `branch`, `head`, and `dirty` record inspected Git state. Use `null` when Git is unavailable. Do not infer a clean state.

## Content Rules

- Keep the artifact sufficient but bounded. Link to durable logs, diffs, plans, or test reports when they already exist.
- Record what changed and why. Do not copy the full conversation.
- Keep exact user requirements when paraphrasing could change meaning.
- Include only decisions that constrain later work. Mark proposals and hypotheses as unsettled.
- State partial code, failing tests, background processes, temporary files, and uncommitted migrations explicitly.
- Use repository-relative paths in the body and the absolute path only in frontmatter.
- Do not use line numbers as the only pointer because edits make them stale.
- Do not include credentials, access tokens, cookies, private keys, secret environment values, or unnecessary personal data.

## Durable Write Procedure

For a finalized handoff:

1. Create `history/` if needed.
2. Render and validate the complete artifact in a temporary file under the chain directory.
3. Choose `history/<timestamp>-<from-session>.md` after making both values filesystem-safe.
4. Create the history file without replacing an existing file. If it exists, accept it only when its content is identical.
5. Atomically rename a validated temporary copy over `HANDOFF.md`.
6. Re-read both files and confirm that their content is identical.

If any step fails, keep the old `HANDOFF.md`, report the failure, and do not end the current session.

## Resume Instruction

When a host can start a clean session, inject a short instruction rather than the handoff contents:

```text
Resume the current task from <absolute-path-to-HANDOFF.md>. Validate the handoff against the repository, report only material drift or blockers, then continue its Next Action. Do not ask the user to repeat settled context.
```
