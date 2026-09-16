# Skill collision audit: 2026-09-15

## Scope and evidence

Base: `master` at `7a54c4878ded55a4fe71feeb4430a435b1a77b40`.
The catalog has 182 skills: 179 plugin skills, two repository skills, and one
installation tool. All are checked together because the tool can remain installed
beside the skills it installs. Category namespaces do not resolve selection
ambiguity when several categories are loaded.

`python3 scripts/check-skill-collisions.py --inventory` prints every parsed name,
description, source category, and declared invocation flag. The flag is source
metadata, not proof that every supported runtime enforces it.

## Findings

- F1: The original guard confused phrase matching with selection quality. A
  description can state a clear trigger without the words `Use when`. A manual
  skill can also explain when a user should invoke it. Removed these false
  failures. Manual metadata no longer hides duplicate descriptions.
- F2: The original audit excluded the installation tool from the shared catalog.
  Its own workflow permits it to remain installed. Added it to the same name and
  description collision checks as the skills it installs.
- F3: Several descriptions omitted the framework or library that limits their
  workflow. The branch adds these limits to Rails-specific skills so general
  UI, configuration, testing, and planning requests do not select them by mistake.
- F4: Several related skills claimed the same broad task despite different
  outputs or stages. The description review makes these boundaries visible
  before a skill body is loaded. See the selection examples below.
- F5: Exact name and normalized description collisions were not found in the
  current catalog. This is a structural result, not proof of unambiguous model
  selection for every possible request.

## Review method

Parse the full catalog with PyYAML, rejecting duplicate keys. Review descriptions
by capability and task stage, then read the bodies of possible collisions to
confirm their actual scope. Token-overlap ranking is an additional search aid,
not the semantic review itself. Low word overlap can still hide the same trigger.

Descriptions should state the task they own and the output they produce. Add a
framework, prerequisite, or exclusion only where it separates a likely competing
skill. A composed workflow should apply to the full requested sequence; a request
for one component should select that component. Related skills need not be
mutually exclusive when the user requests several distinct outputs.

## Selection examples

These are review cases, not measured model-routing results.

| Request | Selection boundary |
| --- | --- |
| Write Minitest tests for a Rails feature | `minitest-coder`: Ruby/Minitest implementation. |
| Wrap an Active Record JSON attribute in typed nested objects | `store-model-coder`: StoreModel, not general JSON validation. |
| Build a Rails ViewComponent with slots and previews | `viewcomponent-coder`: ViewComponent, not general UI components. |
| Generate an index at llms.txt | `llms-txt-builder`: that file, not a complete AI search visibility program. |
| Compare early product ideas in a guided interview | `brainstorm-product`: idea exploration, not a standalone demand verdict. |
| Check owners and support capacity for an existing launch plan | `launch-readiness`: operational preflight. |
| Plan code extraction from a large Rails controller | `layered-rails`: Rails responsibility boundaries, not general task planning. |
| Build a Rails modal using Turbo and Stimulus | `dialog-patterns`: this stack, not any overlay UI. |
| Produce one search-led article | `seo-content`: the article workflow, not keyword lists or tracking alone. |
| Map subquestions for one AI search question | `query-expansion-strategy`: one question; `topical-authority` covers a site's content portfolio. |
| Create a production calendar across content channels | `editorial-planning`: publishing priorities; `keyword-research` selects topics from search demand. |
| Apply an existing voice profile to a draft | `style-writer`: apply the profile; `voice-dna-kit` creates it from samples. |
| Build stateful Workers without the Agents SDK | `durable-objects`: the underlying primitive; `agents-sdk` requires that SDK. |
| Plan a manual customer service pilot | `manual-service-pilot`: test manual delivery, not every task before software development. |
| Review a Rails application change | `rails-code-review`: primary Rails review; `code-review` covers general changes and standalone Ruby. |
| Review infrastructure before deployment | `infrastructure-review`: overall review, with `infrastructure-security-review` as its security pass when relevant. |
| Audit infrastructure security only | `infrastructure-security-review`: focused security audit. |

## Automated checks and limits

`scripts/check-agent-plugins.sh` runs the collision guard and its regression tests.
The guard checks YAML, source paths, directory/name agreement, description types
and whitespace, invocation flag types, and exact duplicates across the catalog.
`--overlaps N` prints lexical overlap candidates for review.

Eight disposable-fixture tests cover natural trigger wording, manual invocation
wording, tool/plugin name collisions, duplicates hidden by manual metadata,
duplicate YAML keys, unknown paths, invalid invocation types, and advisory overlap.

The guard cannot prove semantic separation. Description changes require review
against nearby skills and their bodies. No runtime selection benchmark was run.

## Verification

- `scripts/check-agent-plugins.sh`: passed, including all 182 skills and eight tests.
- `scripts/check-codex-plugins.sh`: passed for all 15 plugins.
- `scripts/check-cookbooks.sh`: passed.
- `git diff --check`: passed.

The skill-creator validator passed for changed plugin and tool skills. It rejects
the repository's existing `disable-model-invocation` extension on `plugin-release`;
the repository validator accepts and checks that field. This is a validator schema
difference, not a failure introduced by these edits.

The prior branch reported a Skills CLI installation smoke test. This follow-up
does not rely on that historical result; install paths and dependencies did not
change. No release or version change is part of this source audit.
