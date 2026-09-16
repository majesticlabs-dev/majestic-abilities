# Skill collision audit — 2026-09-15

## Base and scope

- Base: `origin/master` at `7a54c4878ded55a4fe71feeb4430a435b1a77b40` after `git fetch --prune origin`.
- Inventory: 182 YAML-parsed `SKILL.md` files: 179 plugin skills, two repository-operating skills, and one isolated tool skill.
- Invocation: 181 model-invoked skills and one explicit user-invoked command (`plugin-release`).
- Native plugin invocations remain namespaced by category. The 179 plugin skills and two repository skills can also be discovered together by the Skills CLI, so names and model-facing descriptions are checked in one `combined-catalog` scope. `majestic-skill-finder` is a separately installed tool scope.

| Native scope | Skills |
| --- | ---: |
| `plugin:cloudflare` | 13 |
| `plugin:core` | 3 |
| `plugin:data` | 8 |
| `plugin:devops` | 10 |
| `plugin:engineer` | 11 |
| `plugin:founder` | 14 |
| `plugin:frontend` | 5 |
| `plugin:marketing` | 14 |
| `plugin:misc` | 5 |
| `plugin:product` | 15 |
| `plugin:rails` | 36 |
| `plugin:reasoning` | 4 |
| `plugin:sales` | 7 |
| `plugin:seo` | 24 |
| `plugin:writing` | 10 |
| `repository` | 2 |
| `tool:majestic-skill-finder` | 1 |

`python3 scripts/check-skill-collisions.py --inventory` emits the complete 182-row TSV inventory with path, declared name, kind, native scope, aggregate scope, invocation mode, and description. The check fails unless every discovered `SKILL.md` has a recognized classification, so the scope totals above cannot omit an unclassified file.

## Method

1. Read the repository README plus the `profile-skill-curation`, `writing-great-skills`, and `github-operations` guidance.
2. Parsed every frontmatter block with PyYAML and a duplicate-key-rejecting loader; the inventory and collision verdict do not extract YAML with regexes.
3. Classified every skill by kind, native scope, aggregate install scope, and model-versus-user invocation.
4. Checked path/name agreement, missing or malformed descriptions, multiline or padded descriptions, invalid invocation metadata, exact name collisions, exact model-facing description duplication, and trigger wording that contradicts invocation mode.
5. Ranked model-facing descriptions by deterministic token overlap and manually adjudicated the strongest candidates against their full skill boundaries.

## Findings and repairs

- F1 — Invocation contradiction: `.agents/skills/plugin-release/SKILL.md` was correctly marked `disable-model-invocation: true` but advertised a model-facing `Use when` trigger. Its description is now a human-facing summary; the manual-only body and release authorization gates are unchanged.
- F2 — Missing model trigger: `tools/majestic-skill-finder/SKILL.md` was model-invoked but described only its output. Its description now states the project-fit and named-invocation triggers.
- F3 — Generic technology triggers: the descriptions for `minitest-coder`, `store-model-coder`, `anycable-coder`, `viewcomponent-coder`, and `event-sourcing-coder` omitted the technology or mechanism that distinguishes them from neighboring Rails skills. Each description now names its owning technology and output without changing the body.
- F4 — Broad semantic overlaps: `llms-txt-builder` previously claimed general AI visibility and crawler discovery; `brainstorm-product` duplicated the demand-validation branch; `launch-readiness` overlapped the composed founder launch decision. Their descriptions now distinguish, respectively, `llms.txt` indexing, interactive ideation, and operational preflight of an existing launch plan.
- F5 — Exact collisions: none. All 182 declared names are unique in their applicable aggregate scopes, all names match their directories, and no two model-invoked skills in one aggregate scope have the same normalized description.

## Strongest overlap candidates adjudicated

| Candidate group | Classification | Boundary |
| --- | --- | --- |
| `performance-reviewer` / `simplicity-reviewer` | Intentional specialization | Runtime cost and bottlenecks versus unnecessary code complexity. |
| `solid-cache-coder` / `solid-queue-coder` | Distinct products | Database-backed caching versus background-job execution. |
| `lessons-learned` / `decision-retrospective` | Distinct evidence question | Reusable practices from completed work versus quality of a consequential decision process; both bodies explicitly exclude the other. |
| `keyword-strategist` / `query-expansion-strategy` | Distinct artifact stage | Existing-page wording and coverage versus LLM fan-out and content-cluster planning. |
| `agents-sdk` / `durable-objects` | Layered specialization | Cloudflare Agents SDK applications versus the lower-level Durable Objects primitive. |
| `feature-brief` / `product-requirements` | Explicit sequence | Exploration and decision record versus implementation-ready PRD after direction is approved. |
| `pr-screenshot-docs` / `visual-validator` | Distinct output | Capture and attach PR evidence versus skeptical UI validation. |
| `style-writer` / `voice-dna-kit` / `style-forensics` | Explicit sequence | Apply an existing voice, package a voice from samples, or measure and explain style. |
| `data-pipeline-design` / `data-pipeline-testing` / `data-validation` | Distinct lifecycle concerns | Pipeline architecture, verification strategy, and executable data contracts. |
| `code-review` / `rails-code-review` | Intentional generic/specialist pair | Language-neutral release review versus Rails-version and subsystem-specific review; native plugin namespacing preserves category isolation. |
| `infrastructure-review` / `infrastructure-security-review` | Intentional generic/specialist pair | Overall correctness and deployability versus exploitable security failures. |
| Cookbook/component pairs | Intentional composition | Cookbooks (`rails-feature`, `product-engineering-handoff`, `founder-launch-decision`, `ai-search-visibility-foundation`, `seo-operator`, `first-customers`, and `marketing-plan`) declare composed workflows; component descriptions own narrower outputs. |

Provider-specific similarities such as DigitalOcean versus Hetzner, or Solid Cache versus Solid Queue, are not collisions. Native category namespacing is preserved, but was not used to excuse ambiguity inside the combined catalog.

## Deterministic guard

`scripts/check-skill-collisions.py` now validates the full 182-file inventory and is called by `scripts/check-agent-plugins.sh`. It fails on:

- duplicate YAML keys or invalid frontmatter;
- unclassified runtime paths;
- path/name mismatches;
- missing, multiline, or padded descriptions;
- invocation-mode/trigger contradictions;
- exact name collisions inside an aggregate scope; and
- exact duplicate model-facing descriptions inside an aggregate scope.

`--overlaps N` prints deterministic semantic-review candidates. It is advisory because token similarity cannot decide whether two workflows are behaviorally identical. `--inventory` emits the complete per-file classification used by this audit.

## Verification

- `python3 -m py_compile scripts/check-skill-collisions.py` — pass.
- `scripts/check-agent-plugins.sh` — pass; 15 plugin manifests and all 182 skill files validated.
- `scripts/check-codex-plugins.sh` — pass; all 15 Codex plugins validated.
- `scripts/check-cookbooks.sh` — pass; cookbook placement, dependencies, install commands, and marketplaces resolve.
- `scripts/check-skills-cli.sh` — pass with Skills CLI 1.5.23; 181 public abilities discovered and the 20-skill cookbook/dependency installation smoke test completed.
- `git diff --check` — pass.

No plugin versions were changed because this audit opens a source PR and does not publish a plugin release.
