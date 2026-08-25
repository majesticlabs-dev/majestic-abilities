# Harness Adapter Contracts

This document locks the Cursor and OpenCode adapter contracts for Majestic Abilities. The contracts are fixed. There is no alternative layout.

Deterministic repository checks are always blocking. Authenticated Cursor discovery is conditional evidence only and requires explicit authorization.

## Canonical-tree invariant

Each catalog skill exists exactly once at:

`plugins/<category>/skills/<name>/SKILL.md`

Rules:

- Adapters contain no copied, generated, symlinked, or rewritten skill bodies.
- No `SKILL.md` may exist under `.opencode/`, `.claude-plugin/`, `.codex-plugin/`, or any other adapter directory.
- Cursor discovers only immediate `skills/*/SKILL.md` children. Deeper nesting is invalid.
- A category with a missing or empty `skills/` directory is invalid.
- Skill names must be unique across all categories.

Documented user-install symlinks may exist outside the repository. Those symlinks point at a canonical category root or at the OpenCode loader file. They do not copy skill bodies.

## Collision and error policy

| Condition | Validation | Runtime |
| --- | --- | --- |
| Duplicate skill names in the canonical catalog | Fail before release. Name the duplicate. | The path-only loader has no duplicate-name policy; repository validation prevents this invalid state from shipping. |
| Skill path or symlink that resolves outside `plugins/` | Fail. Name the escaping path. | Reject the path. Load no content from outside. Emit `majestic-abilities: escaping path: <path>`. |
| Missing or empty `plugins/<category>/skills/` | Fail. The category is invalid. | Skip a missing directory with one diagnostic: `majestic-abilities: missing skills directory: <path>`. Other valid paths still load. |
| Occupied Cursor install destination | Fail. Name the occupied path. Leave the destination unchanged. | Same. |
| Real client binary absent | Do not fail the structural repository check when the plan marks the check optional. | Record the exact `SKIPPED` reason. Deterministic proof remains authoritative. |

## Metadata field matrix

Each category root `plugins/<category>/plugin.json` is authoritative for shared identity metadata.

| Field | Canonical root | Claude manifest | Codex manifest | Claude marketplace | Codex marketplace |
| --- | --- | --- | --- | --- | --- |
| `name` | required | required | required | required | required |
| `version` | required | required | required | required | unsupported |
| `description` | required | required | required | required | unsupported |
| `author` | required | required | required | unsupported | unsupported |
| `homepage` | optional | conditional | conditional | unsupported | unsupported |
| `repository` | optional | conditional | conditional | unsupported | unsupported |
| `license` | required | required | required | unsupported | unsupported |
| `keywords` | required | required | required | unsupported | unsupported |

`conditional` means the field must equal the canonical value when the root declares it, and must be absent when the root omits it. `unsupported` means a synchronizer must neither add nor compare that field.

Native-only fields (`displayName`, `skills`, `interface`) and marketplace-only fields (`source`, `category`, `policy`, marketplace identity) are target-owned.

Cursor uses the existing root Agent Plugins manifests. There is no Cursor-native metadata record and no Cursor marketplace in this repository.

## Cursor adapter

### Package root

Each category remains at `plugins/<category>/` and uses its existing root `plugin.json`.

Do not add `.cursor-plugin/plugin.json` beside it. Do not add a root `.cursor-plugin/marketplace.json`.

Cursor consumes the Agent Plugins format and discovers immediate `skills/*/SKILL.md` children of that category root.

### User route

Install one absolute symlink per selected category:

```text
ln -s <checkout>/plugins/<category> ~/.cursor/plugins/local/majestic-<category>
```

The symlink target must be an absolute path. The destination must not already exist. An occupied destination fails with a diagnostic that names the occupied path. The occupied path stays unchanged.

Update:

```text
git -C <checkout> pull --ff-only
```

Then restart Cursor or run `Developer: Reload Window`.

Removal deletes only that symlink. The checkout target stays intact.

Official Marketplace submission and a root Cursor marketplace are out of scope.

### Real client

`cursor-agent --plugin-dir <checkout>/plugins/core` is the documented CLI load route. Structural validation is blocking. Availability of the `--plugin-dir` option is recorded when the binary exists.

An authenticated model call is never automatic. When not authorized, evidence records:

`SKIPPED: Cursor discovery requires authenticated model execution`

Do not call structural proof “client discovery.”

## OpenCode adapter

### Package root

Required file:

`.opencode/plugins/majestic-abilities.js`

The loader targets OpenCode V1 `1.18.22`. OpenCode V2 is unsupported in this stage.

The loader:

1. Resolves its real file path with `realpathSync(fileURLToPath(import.meta.url))`.
2. Ascends two directories to the checkout root.
3. Enumerates sorted absolute `plugins/<category>/skills` directories.
4. Rejects paths that resolve outside `plugins/`.
5. Adds each absolute skills path to `config.skills.paths` exactly once.

The loader does not derive commands, parse frontmatter, write files, or create, copy, or rewrite `SKILL.md`. OpenCode's native skill loader reads the already validated canonical `SKILL.md` files.

A minimal root `package.json` with `"type": "module"` exists only for ESM loading and local test scripts.

### Project route

Create an absolute symlink from the checkout loader to:

```text
<target-project>/.opencode/plugins/majestic-abilities.js
```

### User route

Create an absolute symlink from the checkout loader to:

```text
~/.config/opencode/plugins/majestic-abilities.js
```

`realpathSync` on the loader file must resolve through that symlink to the checkout loader, then ascend to the checkout root.

Update:

```text
git -C <checkout> pull --ff-only
```

Removal deletes only that symlink. The checkout loader stays intact.

No npm publication or user `opencode.json` rewrite is part of this contract.

### Real client

With fake `HOME` and `XDG_CONFIG_HOME`, pinned `opencode` `1.18.22` must load the symlink. `opencode debug config` must show every absolute skills path exactly once, and `opencode debug skill` must show known core skills such as `agent-ready-repository` and `agents-md-hierarchy`.

The release gate `scripts/check-opencode-loader.sh` requires the pinned `opencode` binary and fails when it is absent or the wrong version. The lower-level adapter check `scripts/check-adapter-contracts.sh --opencode` may record `SKIPPED: opencode unavailable` when the binary is absent; deterministic loader and escape checks remain blocking either way.

## Install, update, and removal

| Harness | Install | Update | Removal |
| --- | --- | --- | --- |
| Cursor | Absolute symlink from `<checkout>/plugins/<category>` to `~/.cursor/plugins/local/majestic-<category>`. Fail if the destination exists. Reload Cursor after install/update. | `git -C <checkout> pull --ff-only`, then reload. | Delete only that symlink. |
| OpenCode project | Absolute symlink from the checkout loader to `<target-project>/.opencode/plugins/majestic-abilities.js`. | `git -C <checkout> pull --ff-only` | Delete only that symlink. |
| OpenCode user | Absolute symlink from the checkout loader to `~/.config/opencode/plugins/majestic-abilities.js`. | `git -C <checkout> pull --ff-only` | Delete only that symlink. |

## Validation

`scripts/check-adapter-contracts.sh` proves the contracts without network access.

| Invocation | Result |
| --- | --- |
| no flag | Check the fixed Cursor and OpenCode contracts for `majestic-core`. Exit 0. |
| `--cursor` | Fake-HOME install against the portable `plugins/core/` package, occupied-destination rejection, symlink-only removal, and `cursor-agent --plugin-dir` availability when present. Exit 0. |
| `--opencode` | Temporary path-only loader import, idempotent config hook, project and user absolute symlinks, and real pinned OpenCode debug smoke when available. Exit 0. |
| `--invalid-fixtures` | Occupied Cursor destination and escaping OpenCode skill path. Print `FAIL` diagnostics that name both violations. Exit non-zero. |

All mutable fixtures live under one `mktemp -d` root. The checker must leave the worktree unchanged.

Cursor fixtures copy the real portable `plugins/core/` package. There is no static Cursor-native `plugin.json` fixture.

The adapter checker covers its one-category path registration, sort order, path spaces, missing directories, symlink escapes, and no-write invariant. Production-loader behavior is covered separately by `tests/opencode-loader.test.js`.
