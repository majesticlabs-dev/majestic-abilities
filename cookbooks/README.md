# Cookbooks

Cookbooks are recipes: multi-step workflows that sequence catalog skills by name. They are the composition layer of this repository.

## Where A Cookbook Lives

Placement follows the plugins its required skills belong to:

| Required skills come from | The cookbook lives in | Install routes |
| --- | --- | --- |
| One plugin | That plugin, at `plugins/<category>/skills/<name>/` | Skills CLI or `/plugin install` |
| Two or more plugins | This directory, `cookbooks/<name>/` | Skills CLI only |

A cross-plugin cookbook is not part of any plugin, so there is nothing to `/plugin install`. Installing it as a plugin would drag in every category it touches and load all of their skill descriptions into every session. The Skills CLI installs exactly the named skills instead.

`scripts/check-cookbooks.sh` enforces this rule in both directions: a single-plugin cookbook left here fails, and a cross-plugin cookbook placed inside a plugin fails.

## How Cookbooks Differ From Skills

| | Catalog skills | Cookbooks |
| --- | --- | --- |
| Contract | One decoupled capability; never references sibling skills | A procedure; references skills by exact `name:` |
| Trigger | Auto-triggered by description, or invoked directly | User-invoked (`/rails-feature ...`) |
| Portability | Installable alone | Requires the skills it names (see `## Requires` in each cookbook) |

Both use the same `SKILL.md` format, so cookbooks install exactly like skills.

## Installing A Cookbook

Each cookbook declares its dependencies in a `## Requires` section and includes the complete install command. Always install the cookbook together with what it requires; neither installer resolves dependencies for you.

```sh
# Example: the rails-feature cookbook plus every skill it names
npx skills add OWNER/REPOSITORY --skill rails-feature dhh-rails-style ruby-coder \
  minitest-coder rails-lint pragmatic-rails-reviewer test-reviewer \
  implementation-planning --agent claude-code --yes
```

A single-plugin cookbook arrives with its plugin, so `/plugin install majestic-seo@majestic-abilities` is enough for `ai-search-visibility-foundation`.

## Scope Rules

- Cookbooks are general recipes. Project-specific details (exact test commands, app-specific gates) belong in the consuming project: edit the installed copy or wrap the cookbook in a thin project skill.
- A cookbook orchestrates by instruction, not enforcement. Steps that must never be skipped (tests pass, lint clean) should be backed by hooks or CI in the consuming project; each cookbook lists which steps those are in its `## Hard Gates` section.
- Cookbooks may only reference skills that exist in this repository. `scripts/check-cookbooks.sh` verifies this; run it before committing a new or changed cookbook.

## Writing A New Cookbook

1. List the skills the workflow needs and find which plugins own them. That decides the location: one plugin means `plugins/<category>/skills/<name>/SKILL.md`, two or more means `cookbooks/<name>/SKILL.md`.
2. Create `SKILL.md` there with standard frontmatter (`name`, `description`), and sequence the steps referencing skills by their exact frontmatter `name:`.
3. Add a `## Requires` section listing each referenced skill with a one-line reason, followed by the complete `npx skills` command naming the cookbook and every required skill. For a single-plugin cookbook, add the `/plugin install <plugin>@majestic-abilities` route too.
4. Add a `## Hard Gates` section naming the steps the consuming project should enforce with hooks or CI.
5. Run `scripts/check-cookbooks.sh`.
