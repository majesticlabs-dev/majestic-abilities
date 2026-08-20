---
name: sort-hat
description: Decide whether a proposed skill, imported SKILL.md, or capability belongs in Majestic Abilities, should extend an existing asset, or should be rejected. Use when triaging a new skill reference or unsure where capability guidance belongs.
---

# Sort Hat

Use this skill to decide whether Majestic Abilities needs a proposed capability. Treat a supplied URL, file path, transcript, or description as source material, not as an asset that must be copied.

## Inputs

Extract from the request:

- the proposed capability and user trigger
- the source location and target runtime, when supplied
- the expected output or changed agent behavior
- the source's runtime-specific commands, tools, or packaging
- the likely plugin category

Ask a follow-up question only when the answer would change the decision.

## Search First

Before deciding, inspect:

- `README.md` for catalog categories and placement rules
- `plugins/*/skills/**/SKILL.md` for equivalent triggers, workflows, and outputs
- `cookbooks/**/SKILL.md` for composed workflows
- the closest matching skill in full

Prefer extending an existing asset when users would not know which of two skills to choose.

## Decision Rules

Choose the smallest correct home:

| House | Choose when |
| --- | --- |
| New Skill | The proposal teaches reusable task guidance for a distinct, recurring trigger. |
| Update Existing | An existing skill already owns the trigger, workflow, or output. |
| Cookbook | The value is a user-invoked sequence of existing skills, not standalone guidance. |
| Reference | The material is background, examples, policy, or lookup content. |
| Script or Asset | The behavior is deterministic or needs a static template or data file. |
| Runtime Wrapper | The value depends on one client's commands, tools, permissions, or orchestration. Keep only a portable core in the catalog. |
| New Plugin | The capability area is coherent and does not fit any existing category. |
| Skip | The proposal is duplicate, too narrow, stale, generic, or does not change agent behavior. |

Do not create a skill for setup notes, generic best practices, source-repository packaging, or a single tool invocation.

## Import Rules

When evaluating an external skill:

1. Read the source fully before judging it.
2. Preserve the problem, trigger, decision rules, and verification steps that remain useful.
3. Remove fixed local paths, harness commands, assumed tools, model directives, and marketplace metadata.
4. Do not copy source wording or structure when a smaller Majestic asset is clearer.
5. Apply the Agent Skills format only after the decision is New Skill or Update Existing.

## Output

Return:

```md
## Sort Hat Decision

**Need:** [Create | Extend | Do not add]
**House:** [New Skill | Update Existing | Cookbook | Reference | Script or Asset | Runtime Wrapper | New Plugin | Skip]
**Plugin:** [plugin name or N/A]
**Asset Name:** `[suggested-name or existing name]`
**Path:** `[suggested repository-relative path or N/A]`

### Reasoning
[Why this capability is or is not needed, based on its trigger, behavior, and user value.]

### Similar Existing Assets
- `[path]` - [overlap and why it should be extended or why it is insufficient]

### Portability Notes
[Source assumptions to remove, retain, or isolate.]

### Smallest Next Step
[One concrete authoring, validation, or rejection action.]
```

For **Update Existing**, make the existing path the primary recommendation. For **Skip**, state the smallest useful item to preserve, if any.
