---
name: majestic-skill-finder
description: Analyze the current project, recommend relevant Majestic Abilities, and install the user-selected skills into the project.
---

# Majestic Skill Finder

Recommend and install the complete relevant set of Majestic Abilities.

## Program

```text
finder     ← locate this project's majestic-skill-finder directory
catalog    ← capture the complete output of `npx skills add majesticlabs-dev/majestic-abilities --list`
categories ← map every catalog skill to its latest public repository category with local tools
installed  ← skill names in .agents/skills and .claude/skills
project    ← inspect repository manifests, dependencies, configuration, source, tests, documentation, and automation with local tools
profile    ← freeze the detected technologies, architecture, lifecycle, and recurring work types

for each category
  for each catalog skill in category
    trigger    ← read the catalog description as an installation trigger
    relevance  ← test trigger against profile, not only the current task
    assessment ← classify skill as installed, recommend, or not relevant

assert every catalog skill appears exactly once in assessment
matches ← all recommended skills grouped by category

show only:
  Recommended skills
  <category>
  <number>. <skill>: <project evidence>
  Select numbers, names, all, or none.
selection ← selected numbered or named matches | all matches | none
selected  ← resolve selection to skill names

if selected ≠ none
  ask:
    Install into:
    1. .agents/skills (default)
    2. .claude/skills
    Select 1 or 2.
  destination ← 1 | empty = .agents/skills; 2 = .claude/skills
  agent       ← destination = .agents/skills ? codex : claude-code
  run `npx skills add majesticlabs-dev/majestic-abilities --skill <selected> --agent <agent> --copy --yes`
  verify <destination>/<skill>/SKILL.md for each selected skill
  report installed paths

removal ← ask `Remove <finder> skill? yes/no`
if removal = yes
  remove <finder>
  verify <finder> is absent
halt
```

## Constraints

- Use the active harness for analysis and recommendation.
- Build and freeze the complete catalog before project analysis.
- Halt if the catalog or category map is incomplete.
- Assess every catalog skill category by category before showing recommendations.
- Recommend a skill when its catalog description matches a technology or recurring work type in the project profile.
- Treat implementation, planning, review, testing, debugging, maintenance, and scope control as recurring work for a maintained software project when a skill description applies to that work.
- Do not require a skill to match the current task.
- Do not recommend a specialized skill from a possible technology, business activity, or workflow that has no project evidence.
- Do not recommend a skill already installed in either project destination.
- Give each recommendation evidence from the project profile.
- Use one continuous numbered list across category headings.
- Show only categories that contain recommendations.
- Do not narrate analysis, exclusions, or progress.
- Present one final recommendation list. Do not discover or add recommendations after presenting it.
- `all` means all shown recommendations, not all available skills.
- Install only the selected skills into the selected project destination.
- Never install globally.
- Remove only the located project copy of `majestic-skill-finder`, and only after explicit confirmation.
