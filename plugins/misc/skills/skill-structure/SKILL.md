---
name: skill-structure
description: Decide whether reusable guidance should become an Agent Skill, reference, script, prompt, or deliberate omission, then design a compliant skill when justified. Use when creating, importing, splitting, or reviewing SKILL.md-based capabilities.
---

# Skill Structure

Choose the smallest correct asset before creating another skill. Treat imported material as raw input, not as a structure that must be preserved.

## Capability Test

Ask:

> Does this material teach a reusable capability that should alter agent behavior for a recognizable class of tasks?

Route based on the dominant value:

| Asset | Use when |
| --- | --- |
| Skill | Reusable task guidance or workflow judgment |
| Reference | Background, examples, policies, or detailed lookup material |
| Script | Deterministic behavior that prose would implement unreliably |
| Asset | Static template, schema, image, or data used in generated output |
| Prompt | Short reusable framing or mode supported by the target system |
| Runtime integration | Value depends on one client's commands, tools, permissions, or orchestration |
| Omit | Duplicate, obvious, too narrow, stale, or unjustified guidance |

Do not turn setup notes, generic best practices, or runtime packaging into skills.

## Duplicate Check

Before adding a skill:

1. Search existing skill names and descriptions.
2. Search bodies for the same trigger and output.
3. Prefer improving an existing skill when users would not know which duplicate to choose.
4. Split only when starting conditions, workflow, or deliverables are materially different.

## Standard Skill Directory

Follow the current [Agent Skills specification](https://agentskills.io/specification):

```text
skill-name/
├── SKILL.md
├── references/  # optional
├── scripts/     # optional
└── assets/      # optional
```

A repository may organize source skills under category folders when its installer supports that catalog layout. The installed unit must still be the `skill-name` directory containing `SKILL.md` and its own resources.

Keep supporting files local to the skill. Avoid dependencies on sibling skills unless they are optional routing suggestions.

## Frontmatter

Use minimal YAML frontmatter by default:

```yaml
---
name: skill-name
description: What the skill does. Use when concrete trigger situations occur.
---
```

Validate:

- `name` is 1 to 64 characters
- only lowercase letters, numbers, and single hyphens are used
- the name does not start or end with a hyphen
- the name matches the parent directory
- `description` is non-empty and no longer than 1024 characters
- the description explains both capability and activation triggers

The specification also defines optional `license`, `compatibility`, `metadata`, and experimental `allowed-tools` fields. Add optional fields only when required and supported by intended clients. Keep runtime-specific routing out of portable frontmatter.

## Naming

Name the capability or trigger, not its source runtime or implementation history.

Good names are:

- specific enough to distinguish neighboring skills
- broad enough to cover repeated use
- written in lowercase kebab-case
- aligned with the user's likely vocabulary

Avoid catch-all names, internal project jargon, redundant suffixes, and categories disguised as one oversized skill.

## Body Design

A useful `SKILL.md` should contain:

1. Clear boundary and exclusions
2. Required inputs
3. Ordered workflow with decision points
4. Output or deliverable shape
5. Quality or verification gate
6. Links to supporting resources only where needed

Use imperative instructions. Remove motivational filler and framework documentation the agent can retrieve when necessary.

## Progressive Disclosure

Keep the main file sufficient for correct execution. Move:

- detailed examples and policies to `references/`
- deterministic operations to `scripts/`
- templates and static data to `assets/`

Use relative links from `SKILL.md`. Avoid deep chains where one reference requires several more references to become useful.

## Portability Review

Remove or isolate:

- runtime-native commands
- tool names assumed to exist everywhere
- fixed user configuration paths
- model selection directives
- hidden dependencies on another repository
- orchestration syntax from a specific client

Document real environment requirements through instructions or the standard `compatibility` field when appropriate.

## Validation Checklist

- [ ] The capability test justifies a skill.
- [ ] No existing skill owns the same trigger.
- [ ] Directory and `name` match.
- [ ] Frontmatter parses as strict YAML.
- [ ] Description has concrete activation language.
- [ ] Main instructions are focused and actionable.
- [ ] Supporting links resolve locally.
- [ ] Scripts are executable, self-contained, and tested.
- [ ] Runtime-specific syntax is absent or intentionally isolated.
- [ ] The skill remains useful when installed by itself.
- [ ] The target installer discovers and copies all required files.
