# Cookbooks

Cookbooks are recipes: multi-step workflows that sequence skills from `skills/` by name. They are the composition layer of this repository.

## How Cookbooks Differ From Skills

| | `skills/` | `cookbooks/` |
| --- | --- | --- |
| Contract | One decoupled capability; never references sibling skills | A procedure; references skills by exact `name:` |
| Trigger | Auto-triggered by description, or invoked directly | User-invoked (`/rails-feature ...`) |
| Portability | Installable alone | Requires the skills it names (see `## Requires` in each cookbook) |

Both use the same `SKILL.md` format, so the Skills CLI discovers and installs cookbooks exactly like skills.

## Installing A Cookbook

Each cookbook declares its dependencies in a `## Requires` section and includes the full install command. Always install the cookbook together with its required skills; the CLI does not resolve dependencies for you.

```sh
# Example: the rails-feature cookbook plus everything it names
npx skills add OWNER/REPOSITORY --skill rails-feature dhh-rails-style ruby-coder \
  minitest-coder rails-lint pragmatic-rails-reviewer test-reviewer \
  implementation-planning --agent claude-code --yes
```

## Scope Rules

- Cookbooks here are general recipes. Project-specific details (exact test commands, app-specific gates) belong in the consuming project: edit the installed copy or wrap the cookbook in a thin project skill.
- A cookbook orchestrates by instruction, not enforcement. Steps that must never be skipped (tests pass, lint clean) should be backed by hooks or CI in the consuming project; each cookbook lists which steps those are in its `## Hard Gates` section.
- Cookbooks may only reference skills that exist in this repository. `scripts/check-cookbooks.sh` verifies this; run it before committing a new or changed cookbook.

## Writing A New Cookbook

1. Create `cookbooks/<name>/SKILL.md` with standard frontmatter (`name`, `description`).
2. Sequence the steps, referencing skills by their exact frontmatter `name:`.
3. Add a `## Requires` section listing each referenced skill with a one-line reason, followed by the complete install command.
4. Add a `## Hard Gates` section naming the steps the consuming project should enforce with hooks or CI.
5. Run `scripts/check-cookbooks.sh`.
