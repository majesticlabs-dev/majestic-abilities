---
name: majestic-skill-finder
description: Analyze the current project, recommend relevant Majestic Abilities, and install the user-selected skills into the project.
---

# Majestic Skill Finder

Recommend and install the smallest relevant set of Majestic Abilities.

## Program

```text
project  ← inspect current task and repository with local tools
skills   ← run `npx skills add majesticlabs-dev/majestic-abilities --list`
matches  ← skills relevant to project

show project summary + matches(name, reason, evidence)
selection ← ask specific matches | all matches | none

if selection = none
  finish without changes
else
  destination ← ask .agents/skills (default) | .claude/skills
  agent       ← destination = .agents/skills ? codex : claude-code
  run `npx skills add majesticlabs-dev/majestic-abilities --skill <selection> --agent <agent> --copy --yes`
  verify <destination>/<skill>/SKILL.md for each selection

report installed paths
suggest removal of this temporary skill
halt
```

## Constraints

- Use the active harness for analysis and recommendation.
- Recommend only skills returned by `--list`.
- Give each recommendation project or task evidence.
- `all` means all shown recommendations, not all available skills.
- Install only the selected skills into the selected project destination.
- Never install globally.
- Do not remove `majestic-skill-finder`; only suggest its removal.
