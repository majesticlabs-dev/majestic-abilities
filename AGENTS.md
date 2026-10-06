# Version Policy

Every change must include a version bump in the same commit. Apply this rule before committing, including changes to guidance, references, documentation, scripts, assets, and configuration.

## Choose the Version

- For changes under `plugins/<category>/`, bump each affected category plugin. Do not bump the root package version for a category-only change.
- For shared changes that affect distributed plugins, bump every affected category plugin.
- For repository-only changes that do not affect a category plugin, bump the root `package.json` version.
- Use one bump per affected version for a single change, even when it touches several files.

Use semantic versioning:

- Patch: compatible corrections, guidance, references, documentation, or configuration changes.
- For a `0.x` plugin, use a minor bump to add, remove, or rename a public skill, or to make an incompatible capability change.
- For a `1.x` or later plugin, use a minor bump for a compatible capability addition and a major bump for an incompatible capability change.

## Update and Check

For category plugins, use `.agents/skills/plugin-release/scripts/update_plugin_version.py <category> <version>`. It updates the portable, Claude Code, and Codex manifests and the versioned Claude Code marketplace entry together. Do not change marketplace-level versions or entries that have no version field.

Check the complete diff and run the applicable validation commands in `README.md`. Confirm that all copies of each affected version agree. Report the old and new versions when the work is complete.

A version bump does not authorize a merge, production change, tag, registry publication, or release. Follow the user's authorization for those actions.
