---
name: create-verification-skill
description: "Analyze a project, propose an approved set of verification skills and checks, then build and validate a project-specific verification coordinator."
---

# Create Verification Skill

Use this skill when a project needs a repeatable way to prove one or more user-visible workflows. It has two phases:

1. **Proposal:** inspect the project and available skills, then show a bounded proposal. This phase is read-only.
2. **Build:** after the user approves named checks, skills, and disclosed cleanup, install or create the approved resources, build the coordinator, run it against an isolated build, and remove this temporary creator.

Do not start the build phase until approval is present. The creator is a setup tool and must never be a runtime dependency of the generated coordinator.

## Scope and authority

- Establish the project root, requested product or workflow scope, applicable repository guidance, non-goals, and the evidence required for readiness.
- If no workflow scope is named, analyze the project and propose a bounded set of user paths from project evidence. The user selects the scope by approving or rejecting those proposal items. Do not silently create an all-project verifier.
- Inspect project files, commands, tests, fixtures, documentation, and installed skills. Do not change product code, product tests, product dependencies, deployment, production state, permissions, or unrelated project files.
- Read-only project analysis and catalog inspection are allowed before approval. Do not edit the target project, install or create skills, execute product workflows, or delete anything before the user approves the proposal.
- Treat a product failure and a broken verifier as different results. A verifier can be valid while reporting that the product fails its contract.
- Do not use an example, a remembered preference, an installed skill, or a possible technology as proof of the project's stack or expected behavior. Derive those facts from project evidence or an explicit user requirement.
- Do not add a default technology-specific skill or check. Propose one only when the project evidence or the user's requirement supports it.

## Phase 1: build the proposal

### 1. Inspect the project

Read applicable `AGENTS.md` files first. Then inspect only the requested scope and its direct prerequisites:

- entrypoints, source, contracts, and user-facing documentation
- build, launch, test, reset, and cleanup commands
- fixtures, seed data, accounts, ports, files, and environment requirements
- existing project-local skills and their supported invocation paths
- current verification skills, if any

Record facts separately from assumptions and unknowns. Inventory installed skills to know what is available, but derive the technology and workflow profile from the project itself. Prefer an existing project skill directory; otherwise propose `.agents/skills/<skill-name>/`.

### 2. Inspect the Majestic catalog

Use a read-only catalog snapshot in this order:

1. A checkout explicitly supplied by the user or project configuration.
2. An available checkout that contains the expected `plugins/*/skills/*/SKILL.md` catalog layout.
3. A shallow temporary checkout of `https://github.com/majesticlabs-dev/majestic-abilities`, using its canonical `master` source when network access is available.

Capture the absolute source location and revision before reading recommendations. Treat only `plugins/*/skills/*/SKILL.md` as catalog entries. Do not use `.agents/skills`, `.claude/skills`, `tools`, or lock files from the catalog checkout as catalog entries or project evidence. If no complete snapshot is available, report that Majestic recommendations are unavailable and continue only with project skills or approved custom checks.

Read names and frontmatter descriptions for the complete catalog snapshot, but do not read every skill body. Use those descriptions to shortlist candidates against direct project evidence and the requested workflow. Before including a candidate in the final proposal, read its complete `SKILL.md` and relevant linked references. Resolve the required supporting skills and other dependencies, including dependencies of composed skills, so the user can review the complete install and call plan. Reading a candidate does not authorize executing its instructions. Capture each proposed source path and revision, including local changes when the snapshot is not clean. Do not install the complete catalog by default.

### 3. Define stable proposal items

Give every proposed check and skill a stable ID that remains unchanged when another item is rejected. Do not use list position as identity. Each check proposal must include:

- `check_id` and the user workflow it proves
- starting state, concrete action, supported command or driver, and cleanup
- expected observable result and its independent source, such as a requirement, contract, or existing user-facing documentation
- failure signal, evidence to retain, and the isolated resources or side effects it creates
- implementation: existing project skill, Majestic skill to install, or custom coordinator instruction/helper
- skill source and status: project path, Majestic category/path plus revision, or `custom`
- all required dependencies, destination path, permissions, and side effects
- the result if this item is rejected, including any coverage gap

Propose skills and checks separately when that makes approval clearer. For example, a check can name an existing project skill, a specific Majestic skill to install, or a custom helper. Do not imply that approving a check approves an undisclosed dependency. Approval must name the items, or explicitly approve all disclosed dependencies for named items.

Show one final proposal. Do not add recommendations after the user has started reviewing it. Ask the user to approve or reject exact check IDs and skill IDs. Include a `CLEANUP` item for removing this temporary creator and its own project lock entry after successful validation. A prior explicit instruction that covers this exact cleanup is sufficient, but still disclose it.

Stop here and wait. A changed proposal requires approval of the changed items before continuing.

## Phase 2: build only the approved plan

### 4. Freeze approval and install approved skills

Record the approved check IDs, skill IDs, source revisions, destinations, and cleanup authorization. Rejected items stay out of the project and appear as coverage gaps. If an approved check lacks an approved dependency, stop and ask; do not install a substitute.

Install selected Majestic skills from their recorded catalog paths and revision, and selected project skills only through the project's supported installer or file operation. Prefer the project's existing skill destination; otherwise use the approved `.agents/skills` path. Never install globally, silently replace an existing skill, or use an invented harness-specific command. Preserve existing lock entries and record the temporary creator entry separately from the approved runtime dependencies.

Create custom verifier instructions or helpers only when their proposal item was approved. Keep them inside the generated skill's project-local directory or another explicitly approved project location. Do not add product code, product tests, or product dependencies to make verification possible.

### 5. Build the project coordinator

Generate a project-local coordinator that calls its approved skills and owns its approved custom checks. It must contain:

- scope, exclusions, prerequisites, and safe test-data rules
- the approved call plan in an explicit order
- for every approved skill call: installed name and path, purpose, inputs, expected result, evidence, and failure or stop behavior
- the approved custom instructions and helper contracts, including inputs, outputs, errors, and cleanup
- the project commands and drivers needed to prepare, start, reset, and identify the intended build
- a report with `verified`, `failed`, `blocked`, and `unrun` workflows

Use the active harness's native way to load or invoke a named installed skill when one exists. Do not invent a universal skill execution command, force a harness or model, or make the generated skill depend on this creator. If the active harness cannot load an approved skill, report the verifier as blocked instead of replacing or silently inlining that skill.

Keep setup approval, installation, and creator removal outside the generated verifier's runtime instructions. Store setup approval and source records separately or as non-executable metadata. Runtime steps must not load, invoke, or remove this creator or its cleanup helper. The creator performs its own removal after validating the generated verifier.

### 6. Validate the assembled verifier

Before running user paths:

1. Confirm every approved referenced skill and local helper exists and loads through the project-supported loader or active harness.
2. Confirm the process, package, binary, or served asset comes from the intended source and build. Record the strongest available identity signal.
3. Use a disposable database, directory, port, account, or other project-supported state boundary. Never use shared or production state.
4. Run the generated coordinator through the real project user paths. Check each result against the independently sourced expectation. Save evidence outside the checkout before cleanup and redact secrets.
5. Clean only resources created by this run and verify cleanup. Preserve product failures in the report.

The verifier is ready only when its instructions load, the approved calls execute, the required user paths produce evidence, and cleanup is proven. A skill-loading, driver, environment, or missing-expectation blocker leaves validation incomplete and the verifier unready. A product defect reported by a functioning verifier is a product result, not a verifier failure.

### 7. Remove this temporary creator

Remove the project-local installation of `create-verification-skill` only after the approved skills are installed, the coordinator is present, and validation has completed. Do not remove it when build, environment, driver, skill-loading, or cleanup blockers leave the result incomplete; report that it remains for recovery.

When Python 3 is available, prefer the bundled standard-library helper at `scripts/cleanup_project_creator.py`, relative to this installed creator's directory. Locate that helper and invoke it by its actual absolute path. Pass the approved absolute project root with `--project-root`, each approved creator installation or alias with repeatable `--skill-dir`, and the project's `skills-lock.json` with `--lock-file` when present. Run with `--dry-run` first and inspect its targets. Then repeat the same command without `--dry-run` within the approved cleanup authority. A directory symlink is unlinked; its target is retained. The helper refuses catalog plugin paths and unsafe roots and preserves unrelated lock entries. If Python 3 is unavailable, use a safe supported project installer or file operation with the same exact targets. Do not install a dependency to perform cleanup. If no safe supported operation is available, retain the creator and report the cleanup blocker.

Remove only the temporary project-local creator and its own lock entry. Never remove a catalog checkout, global or shared skill, an approved generated verifier, an approved runtime dependency, or unrelated lock entries.

## Deliverable

Before approval, return the proposal with its stable IDs, evidence, sources, dependencies, side effects, cleanup item, and explicit coverage gaps. After the build, return:

1. the generated skill path and approved scope
2. installed skill paths, source revisions, and the approved call order
3. the build identity and disposable-state boundary
4. coverage with expected result, observed result, status, and evidence path
5. commands or project-native actions actually run
6. cleanup result, including whether this creator was removed
7. product failures, verification gaps, blockers, unknowns, and unrun workflows separately

## Quality gate

Before declaring the project verifier ready, confirm that:

- project stack and workflow facts came from project evidence or explicit user requirements, not installed skills
- the catalog source revision and every selected skill source are recorded
- selected skills were shortlisted by description, then read in full with relevant references
- only approved checks, skills, custom resources, and cleanup actions were performed
- all approved dependencies and side effects were disclosed and honored
- the generated skill does not depend on this creator, a fixed harness, or an invented command
- approved referenced skills and helpers exist and load
- build identity was checked and user paths ran in isolated state
- evidence was stored outside the checkout before cleanup
- cleanup removed only resources created or explicitly approved for removal
- rejected items remain out of the project and their coverage gaps are explicit
- product failures remain visible and are not rewritten as verifier success
