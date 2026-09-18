---
shaping: true
status: draft
---

# Skill selector frame

## Source

> We have multiple skills and it's very hard for LLM to select the correct skill while solving the prompt request.
>
> We need efficient way to select the correct skill.
>
> There is /Users/dpaluy/projects/ai/skills/skillranker
>
> We can consider using it or we will build our own custom solution.
>
> I want you to evaluate it and guide me on next steps

> How can we provide a better way to select the correct skill to use?
>
> Step 1. Add a skill to the project based on relevancy
> Step 2. Add plugins and allow more efficient selection

> Is there a way to build a better skill selector?

> $shaping-skills:shaping this

## Problem

Project relevance and task relevance are different decisions. A project can need a skill without needing it for the current request. Plugins group capabilities for installation, but that grouping does not resolve which instructions fit the next action.

The current catalog has structural checks and an installation finder. It has no demonstrated measure of task selection accuracy. Some selection boundaries appear only inside skill bodies. The cause and rate of actual selection failures remain unknown.

## Outcome

The agent uses instructions that fit the current task without requiring the user to remember skill names. It respects explicit requests, can use no skill, and can use several skills when their roles are distinct. Any added selection cost must be justified by fewer errors or less total context use.

## Scope

Shape project installation and task selection as connected steps. Reuse the existing finder and plugin packaging where possible. Do not implement a selector, install plugins, or change the catalog in this shaping pass.

Runtime coverage, automatic loading, acceptable overhead, and the time budget remain user decisions. The proposed solution in [shaping.md](shaping.md) is not yet selected or ready for implementation.
