# Majestic Abilities

Majestic Abilities is a portable catalog of agent skills organized into 15 capability categories. It contains 168 catalog skills, five cookbooks, and two repository-operating skills, and follows the [Agent Skills](https://agentskills.io/) format.

You can install:

- a capability category as a native plugin for Claude Code or Codex;
- the complete catalog as a Pi package;
- individual skills, categories, or cookbooks for supported agents, including Cursor, with the [Vercel Skills CLI](https://github.com/vercel-labs/skills).

## Contents

- [Choose an installation route](#choose-an-installation-route)
- [Install native category plugins](#install-native-category-plugins)
- [Install the Pi package](#install-the-pi-package)
- [Install with the Skills CLI](#install-with-the-skills-cli)
- [Browse the catalog](#browse-the-catalog)
- [Cookbooks](#cookbooks)
- [Repository model](#repository-model)
- [Development](#development)

## Choose an Installation Route

| Need | Route | Installed scope |
| --- | --- | --- |
| One capability category in Claude Code or Codex | Native plugin | All abilities in that category |
| The complete catalog in Pi | Pi package | All category plugins, including their cookbooks |
| One or more selected abilities | Skills CLI | Only the named skills or cookbooks |
| The same selected abilities across several agents | Skills CLI | The named abilities for each selected agent |
| One local category in Cursor during development | Local symlink | All abilities in the linked category |

Native plugins keep skill descriptions namespaced by category. Installing only the categories you use reduces the descriptions loaded into each session.

## Install Native Category Plugins

Each `plugins/<category>/` directory is an Agent Plugins 1.0.0 package. Replace the example category names below with any plugin listed in the [catalog](#browse-the-catalog).

### Claude Code

Add this repository as a marketplace, then install the categories you need:

```sh
/plugin marketplace add majesticlabs-dev/majestic-abilities
/plugin install majestic-rails@majestic-abilities
/plugin install majestic-engineer@majestic-abilities
```

Use an absolute repository path instead of the GitHub source while developing locally.

Plugin skills are namespaced. For example, invoke `dhh-rails-style` from `majestic-rails` as:

```text
/majestic-rails:dhh-rails-style
```

Use `/plugin`, `claude plugin list`, and `claude plugin uninstall <name>` to manage installed plugins. `claude plugin details <name>` reports the projected description token cost.

### Codex

The repository contains a Codex marketplace at `.agents/plugins/marketplace.json`.

From the repository root:

```sh
codex plugin marketplace add .
codex plugin list --marketplace majestic-abilities-codex --available
codex plugin add majestic-rails@majestic-abilities-codex
codex plugin add majestic-engineer@majestic-abilities-codex
```

### Cursor

The supported public Cursor route is the Skills CLI below. There is no documented remote Cursor marketplace import for this repository. For local development from a checkout, symlink the categories you need:

```sh
mkdir -p ~/.cursor/plugins/local
ln -s "$(pwd)/plugins/rails" ~/.cursor/plugins/local/majestic-rails
ln -s "$(pwd)/plugins/engineer" ~/.cursor/plugins/local/majestic-engineer
```

Restart Cursor or run **Developer: Reload Window** after changing the links. The root `.cursor-plugin/marketplace.json` is retained for local manifest validation; it is not presented as a public remote-install route.

## Install the Pi Package

The root `package.json` exposes every category plugin, including its cookbooks, as one Pi package.

```sh
# Install for the current user
pi install git:github.com/majesticlabs-dev/majestic-abilities

# Install for the current project
pi install git:github.com/majesticlabs-dev/majestic-abilities -l
```

Use `pi config` to enable or disable package skills.

## Find and Install Relevant Skills

From the project root, temporarily install `majestic-skill-finder`:

```sh
npx skills add \
  https://github.com/majesticlabs-dev/majestic-abilities/tree/master/tools/majestic-skill-finder \
  --skill majestic-skill-finder \
  --agent codex \
  --yes
```

This installs the temporary finder in `.agents/skills`. The Skills CLI can also create `skills-lock.json` in the project root. Use a low-cost model with a 1M-token context window, such as `deepseek-v4-flash`. Then:

1. Ask your harness (Claude, Codex, Pi, Cursor, etc.) to run `majestic-skill-finder`.
2. Review the recommendations and select the skills to install.
3. Select `.agents/skills` (default) or `.claude/skills` as the project destination.
4. Confirm whether the finder should remove its temporary project files.

## Install with the Skills CLI

The CLI supports Claude Code, Codex, Pi, and Cursor.

List the available abilities:

```sh
# Published repository
npx skills add majesticlabs-dev/majestic-abilities --list

# Local checkout
npx skills add . --list
```

### Install Skills Manually

Install one skill into a project:

```sh
npx skills add majesticlabs-dev/majestic-abilities \
  --skill code-review \
  --agent claude-code \
  --yes
```

Select several agents to install the same skill for each one:

```sh
npx skills add majesticlabs-dev/majestic-abilities \
  --skill code-review \
  --agent claude-code codex pi cursor \
  --yes
```

Install a complete category:

```sh
npx skills add https://github.com/majesticlabs-dev/majestic-abilities/tree/master/plugins/engineer/skills \
  --skill '*' \
  --agent claude-code codex pi cursor \
  --yes
```

Install the complete catalog:

```sh
npx skills add majesticlabs-dev/majestic-abilities \
  --skill '*' \
  --agent claude-code codex pi cursor \
  --yes
```

Project installation is the default. Add `--global` or `-g` to any install command for a user-level installation. Omit `--agent` to choose from detected agents interactively.

Common management commands:

```sh
npx skills list --agent claude-code
npx skills list --global
npx skills update --project --yes
npx skills update --global --yes
npx skills remove code-review --agent claude-code --yes
```

The CLI normally recommends symlinks so several agents can share one canonical installation. Add `--copy` when the project requires materialized files.

## Browse the Catalog

The catalog contains 168 skills plus five cookbooks. Two repository-operating skills bring the Skills CLI inventory to 175 abilities. Follow a category link to browse its skill directories, or run `npx skills add majesticlabs-dev/majestic-abilities --list` to see the exact inventory.

| Category | Plugin | Skills | Focus |
| --- | --- | ---: | --- |
| [Cloudflare](plugins/cloudflare/skills/) | `majestic-cloudflare` | 13 | Cloudflare platform, Workers, Agents SDK, Durable Objects, security, infrastructure, and deployment |
| [Core](plugins/core/skills/) | `majestic-core` | 3 | Agent-ready repositories, nested guidance audits, and durable session handoffs |
| [Data](plugins/data/skills/) | `majestic-data` | 8 | Pipelines, contracts, quality controls, source assessment, and dbt |
| [DevOps](plugins/devops/skills/) | `majestic-devops` | 10 | OpenTofu, Ansible, cloud-init, Kamal, secrets, storage, and infrastructure review |
| [Engineer](plugins/engineer/skills/) | `majestic-engineer` | 10 | Scoping, planning, task decomposition, code review, testing, complexity, logging, and code simplification |
| [Founder](plugins/founder/skills/) | `majestic-founder` | 12 | Strategy, priorities, founder fit, finance, fundraising, go-to-market, and launch readiness |
| [Frontend](plugins/frontend/skills/) | `majestic-frontend` | 5 | Visual direction, performance, accessibility, validation, and screenshots |
| [Marketing](plugins/marketing/skills/) | `majestic-marketing` | 13 | Positioning, naming, research, content, campaigns, and growth experiments |
| [Misc](plugins/misc/skills/) | `majestic-misc` | 5 | Communication, lessons learned, visual explanations, skill grading, and skill structure |
| [Product](plugins/product/skills/) | `majestic-product` | 15 | Discovery, workflow mapping, requirements, planning, pricing, and retention |
| [Rails](plugins/rails/skills/) | `majestic-rails` | 36 | Rails and Ruby implementation, Hotwire, architecture, testing, and review |
| [Reasoning](plugins/reasoning/skills/) | `majestic-reasoning` | 4 | Decision retrospectives, challenge, premortems, and reasoning verification |
| [Sales](plugins/sales/skills/) | `majestic-sales` | 6 | ICP, outbound, pipeline, enablement, proposals, and account expansion |
| [SEO](plugins/seo/skills/) | `majestic-seo` | 22 | Technical SEO, content strategy, schema, AEO, and AI search visibility |
| [Writing](plugins/writing/skills/) | `majestic-writing` | 10 | Voice capture, brand voice, drafting, editing, copy, and structure |

Core contains foundational repository and agent-session capabilities. Other categories do not depend on it. Misc is a temporary home for useful portable skills whose long-term category is not settled.

## Repository Skills

Repository-operating skills live under `.agents/skills/`. They maintain this repository and are available when an agent works from this checkout:

- `plugin-release` updates category plugin versions, validates distribution, and publishes an authorized release.
- `sort-hat` decides whether proposed capability guidance belongs in the catalog.

These skills are discoverable through the Skills CLI but are not shipped by category plugins or the private Pi package.

## Cookbooks

Cookbooks are user-invoked workflows that sequence catalog skills by name. Catalog skills remain self-contained and do not reference sibling skills.

| Cookbook | Location | Required categories | Purpose |
| --- | --- | --- | --- |
| [`ai-search-visibility-foundation`](plugins/seo/skills/ai-search-visibility-foundation/) | SEO plugin | `majestic-seo` | Establish SEO, entity, crawler, structured-data, and AEO measurement foundations |
| [`founder-launch-decision`](plugins/founder/skills/founder-launch-decision/) | Founder plugin | `majestic-founder`, `majestic-sales` | Produce a founder-led launch decision |
| [`founder-next-stage-decision`](plugins/founder/skills/founder-next-stage-decision/) | Founder plugin | `majestic-founder`, `majestic-product` | Decide a founder's next growth stage with a time-boxed evidence sprint |
| [`product-engineering-handoff`](plugins/product/skills/product-engineering-handoff/) | Product plugin | `majestic-engineer`, `majestic-product` | Prepare an approved product direction for engineering |
| [`rails-feature`](plugins/rails/skills/rails-feature/) | Rails plugin | `majestic-engineer`, `majestic-rails` | Build and review a Rails feature end to end |

Each cookbook lives in the plugin that owns its primary user trigger and output. Supporting skills can come from other plugins. Cookbook frontmatter declares dependencies in the repository-defined string-valued `metadata.requires` key. Each cookbook's installation command includes the same dependency set because installers do not resolve dependencies.

## Repository Model

Each category has one shared skill tree and three manifest routes:

```text
.claude-plugin/marketplace.json       # Claude Code marketplace
.agents/plugins/marketplace.json      # Codex marketplace
.cursor-plugin/marketplace.json       # Cursor metadata for local validation
package.json                          # Pi package for the complete catalog
plugins/
  <category>/
    plugin.json                       # Portable Agent Plugins manifest
    .claude-plugin/plugin.json        # Claude Code compatibility manifest
    .codex-plugin/plugin.json         # Codex compatibility manifest
    skills/
      <skill-name>/
        SKILL.md
        references/                   # optional
        scripts/                      # optional
        assets/                       # optional
scripts/
  check-agent-plugins.sh
  check-codex-plugins.sh
  check-cookbooks.sh
  check-skills-cli.sh
```

The category root `plugin.json` is authoritative for metadata shared by the portable, Claude Code, and Codex manifests. Category versions are independent. When a category version changes, update its root and native manifests together, plus each marketplace entry that carries the version.

## Development

Create an isolated Python environment and install the source-controlled validation dependencies:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Run the repository checks before committing packaging or cookbook changes. The Codex check uses the Apache-2.0 validator vendored under `scripts/vendor/`; it does not require `~/.codex`.

```sh
scripts/check-agent-plugins.sh
scripts/check-codex-plugins.sh
scripts/check-cookbooks.sh
scripts/check-skills-cli.sh
```

The checks validate plugin manifests, the exact public inventory, cookbook placement, referenced skill names, cookbook installation commands, default Skills CLI discovery, and a real `rails-feature` install. The Skills CLI smoke check requires Node.js and network access for its pinned CLI package; pass a public repository source as its first argument to test the published source after release.
