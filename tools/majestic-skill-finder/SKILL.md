---
name: majestic-skill-finder
description: Analyze the current project, recommend relevant Majestic Abilities, and install the user-selected skills into the project.
---

# Majestic Skill Finder

Recommend and install the complete relevant set of Majestic Abilities.

## Program

```text
root           ← locate the current project root
finder         ← locate this project's majestic-skill-finder directory
lock           ← root/skills-lock.json
lock_state     ← before other installs, classify lock as absent, temporary, or shared
                 temporary = lock.skills contains exactly majestic-skill-finder
                 shared = any other existing lock state
catalog_source ← shallow-clone the latest public majestic-abilities repository into a temporary directory
catalog        ← read only catalog_source/plugins/*/skills/*/SKILL.md
categories     ← derive each catalog skill's category from its plugins/<category>/ path
installed      ← skill names in root/.agents/skills and root/.claude/skills, except majestic-skill-finder
project        ← inspect repository manifests, dependencies, configuration, product source, tests, documentation, and automation with local tools
                 exclude root/.agents/skills, root/.claude/skills, root/skills-lock.json, and finder-generated files
profile        ← freeze the detected technologies, architecture, lifecycle, and recurring work types

assert every catalog path is below catalog_source/plugins
assert no skill from catalog_source/.agents, catalog_source/.claude, or catalog_source/tools is in catalog

for each category
  for each catalog skill in category
    trigger    ← read the catalog description as an installation trigger
    relevance  ← test trigger against direct project evidence in profile, not only the current task
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
  group selected skills by category
  for each selected category
    source ← https://github.com/majesticlabs-dev/majestic-abilities/tree/master/plugins/<category>/skills
    run `npx skills add <source> --skill <selected category skills> --agent <agent> --copy --yes`
  verify <destination>/<skill>/SKILL.md for each selected skill
  report installed paths

removal ← ask `Remove <finder> skill and its temporary installation files? yes/no`
if removal = yes
  remove finder
  if lock_state = temporary
    remove lock
  if lock_state = shared
    remove only the majestic-skill-finder entry from lock and preserve all other entries
    remove lock if no entries remain
  verify finder is absent
  verify lock is absent when lock_state = temporary
  verify lock has no majestic-skill-finder entry when lock_state = shared
remove catalog_source
halt
```

## Constraints

- Use the active harness for analysis and recommendation.
- Build and freeze the complete catalog before project analysis.
- The catalog consists only of skills under `plugins/*/skills/` in the temporary public checkout.
- Never use `.agents/skills/`, `.claude/skills/`, `tools/`, or `skills-lock.json` as catalog sources or project evidence.
- Use installed skill directories only to identify skills that are already installed.
- Halt if the catalog or category map is incomplete.
- Assess every catalog skill category by category before showing recommendations.
- Recommend a skill only when its catalog description matches a technology or recurring work type supported by direct project evidence.
- Do not infer project technologies or workflows from agent configuration, installed skills, lock files, or finder installation artifacts.
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
- Install each selection from its matching `plugins/<category>/skills` source. Never install from the repository root.
- Never install globally.
- Remove only the located project copy of `majestic-skill-finder`, and only after explicit confirmation.
- Treat `skills-lock.json` as temporary only when it recorded only `majestic-skill-finder` before this run installed any selected skills.
- Never delete unrelated lock entries.
