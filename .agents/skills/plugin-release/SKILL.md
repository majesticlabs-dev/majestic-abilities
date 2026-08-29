---
name: plugin-release
description: Update one or more Majestic Abilities category plugin versions and publish an approved repository release. Use when changed plugin skills or metadata are ready to validate, version, commit, push, and verify on the public install route.
disable-model-invocation: true
---

# Plugin Release

Invoke this command manually with `/skill:plugin-release`. Use it to release category plugins from Majestic Abilities. Preserve unrelated work and do not publish until the user explicitly authorizes the release.

## Inputs

Determine:

- changed category plugins
- the version bump for each category
- the target branch and remote
- whether the user authorized commit and push

Use `git diff --name-only` to identify changed `plugins/<category>/` paths. A change outside a plugin does not create a category release by itself.

## Version Choice

Each category has an independent semantic version.

For a `0.x` plugin:

- patch: compatible guidance, reference, validation, or metadata correction
- minor: add, remove, or rename a public skill, or make another incompatible capability change

For a `1.x` or later plugin:

- patch: backward-compatible correction
- minor: backward-compatible capability addition
- major: incompatible public capability change

Every changed category plugin must receive a version bump before release. State the selected versions before editing. Do not change the private root `package.json` version or marketplace-level metadata versions for a category-only release.

## Update Plugin Metadata

Run once for each changed category:

```sh
python3 .agents/skills/plugin-release/scripts/update_plugin_version.py <category> <version>
```

The script updates:

- `plugins/<category>/plugin.json`
- `plugins/<category>/.claude-plugin/plugin.json`
- `plugins/<category>/.codex-plugin/plugin.json`
- the category entry in `.claude-plugin/marketplace.json`

It verifies that all current versions agree before writing. Codex and Cursor marketplace entries do not carry category versions and must remain unchanged.

## Validate Before Publication

Run the focused updater tests and all repository release checks:

```sh
python3 .agents/skills/plugin-release/scripts/test_update_plugin_version.py
scripts/check-agent-plugins.sh
scripts/check-codex-plugins.sh
scripts/check-cookbooks.sh
scripts/check-skills-cli.sh
```

Then run:

```sh
git diff --check
git status --short
git diff --stat
```

Stop when a check fails. Do not bypass or replace a failed check.

## Verify Identity and Scope

Before commit or push, verify:

```sh
gh auth status
gh api user --jq '.login + " " + (.name // "")'
git config user.name
git config user.email
git remote -v
git branch --show-current
```

Confirm that the authenticated GitHub account has push access to the intended repository. Review the complete diff and keep unrelated user changes out of the release commit.

## Publish

Only after explicit authorization:

1. Stage the approved release files.
2. Review the staged diff and confirm no unrelated paths are present.
3. Commit without a co-author line.
4. Push the commit to the approved remote branch.
5. Confirm the remote branch resolves to the local commit.

This repository publishes category plugins from the default branch. Do not create a tag, GitHub Release, or registry publication unless the user separately requests that release mechanism.

## Verify the Public Source

After push, test the public repository source:

```sh
scripts/check-skills-cli.sh https://github.com/majesticlabs-dev/majestic-abilities
```

Confirm that the remote commit is the pushed commit and that the running public install check used that source. Report the released plugin versions, commit, branch, checks, and any residual risk.
