---
shaping: true
status: draft
selected_shape: none
---

# Skill selector shaping

## Frame and evidence

See [frame.md](frame.md) for the source request and intended outcome. This is a proposal for discussion, not an approved implementation plan.

At catalog revision `56bf813`, the previous inspection counted 177 plugin skills and cookbooks and about 2,100 description words. The finder selects installations from project evidence. Structural checks and eight collision tests passed in that inspection; these results do not measure task selection.

At the previously inspected SkillRanker revision `3fe85c4`, the CLI exposed configuration inspection through `doctor`, not `rank` or hooks. Its evaluation fixtures explicitly disclaimed benchmark evidence. Recheck these observations before a later adoption decision.

Relevant source: [finder](../../../tools/majestic-skill-finder/SKILL.md), [collision checks](../../../scripts/check-skill-collisions.py), [plan review boundary](../../../plugins/engineer/skills/plan-review/SKILL.md), and [requirements review boundary](../../../plugins/product/skills/requirements-quality/SKILL.md).

## Requirements

Only R0 and R1 directly reflect the user's stated outcome. Other requirements are proposals, with unresolved decisions marked Undecided.

| ID | Requirement | Status |
|---|---|---|
| R0 | Select useful instructions for the next action, including no skill or several skills when appropriate. | Core goal |
| R1 | Support relevant project skills and plugins without treating every installed skill as relevant to every request. | Must-have |
| R2 | Respect explicit requests, invocation restrictions, availability, and user authority. | Leaning yes |
| R3 | Run selection and load chosen instructions before task execution without manual skill selection. | Undecided |
| R4 | Resolve individual and plugin installations into the runtime's effective inventory without duplicate or hidden candidates. | Leaning yes |
| R5 | Reflect skill edits and installations without maintaining a second set of skill instructions. | Leaning yes |
| R6 | Make each selection inspectable and allow work to continue when selection fails. | Leaning yes |
| R7 | Demonstrate fewer selection errors within an agreed latency and context budget. | Leaning yes |

## CURRENT: Project finder and native selection

The finder recommends individual installations using project evidence. Category plugins provide another installation route. The runtime exposes available skills and the model chooses from their descriptions. The checker detects structural and exact-duplicate problems. Task selection quality and selection overhead have not been measured.

## A: Improve native selection

| Part | Mechanism | Unknown |
|---|---|---|
| A1 | Keep project selection in the existing finder; use individual skills or category plugins according to project evidence. | Plugin recommendation policy needs agreement. |
| A2 | Use failure cases to add missing action, input, and exclusion distinctions to existing descriptions. | Which descriptions cause actual errors. |
| A3 | Add project guidance to compare likely skill boundaries and permit no selection before relevant work. | Whether the runtime follows this consistently; this is advisory guidance. |

This is the smallest change. It does not create an enforced selection step or an independent selection record.

## B: Local inventory with selection by the active model

| Part | Mechanism | Unknown |
|---|---|---|
| B1 | Extend the finder to present relevant individual skills and plugin bundles with their included skills. Preserve user selection and installation verification. | When a whole plugin is preferable to selected members. |
| B2 | Build an index from the runtime's effective inventory. Store namespaced identity, source path, description, invocation policy, and content hash. Preserve runtime precedence; collapse only verified aliases of the same skill. | Runtime inventory and precedence interface. |
| B3 | Apply explicit request and eligibility rules. Pass the eligible index, current request, relevant project facts, and recent task state to the active model. Do not filter by plugin category alone. | Access to the active model at the required point in execution. |
| B4 | Have the model nominate candidates and read their current scope sections. Return selected identities with short task-based reasons, or an empty set. Resolve an ambiguous explicit name instead of selecting an arbitrary match. | Selection quality; candidate limits need measurement. |
| B5 | Revalidate identity, policy, and content hash; load selected instructions through the runtime before execution. Re-run selection for a new request, task phase, or changed inventory. | Supported runtime trigger and load mechanism. |
| B6 | Keep the current selection record available for inspection in the session. Persist candidate IDs, exclusions, selected IDs, source hashes, and timings only for an opt-in evaluation run. If selection fails, report the fallback and return control to native execution. | Runtime interface for exposing the record and available execution evidence. |

Generate descriptions and references from source. Read boundary text from skill bodies when needed; do not require a new metadata schema across the catalog. Start with the full eligible index and measure it before introducing retrieval.

One proposed selection record contains `selected_ids`, `reason_by_id`, `source_hashes`, and `fallback_reason`. An empty selection is valid. Already loaded instructions remain part of context; no design assumes that a new selection erases them.

B is the recommended direction for investigation, not a selected shape. Its runtime integration is unresolved. An optional selector skill or project instruction alone cannot satisfy R3.

## C: Separate ranking service

| Part | Mechanism | Unknown |
|---|---|---|
| C1 | Use the same project installation step and effective inventory described in B1 and B2. | Same inventory interface as B. |
| C2 | Send bounded task context and eligible candidates to a dedicated ranker. With SkillRanker, use its planned Jev ranking, fit checks, and no-match result. | Working ranking path, provider choice, data handling, cost, and accuracy. |
| C3 | Validate the ranker's output and load selected skills through a runtime adapter; fall back to native selection on failure. | Working adapter and measured operational behavior. |

SkillRanker is a design reference at the inspected revision. Adopting it would require completing and verifying its ranking workflow. A new custom service also adds a separate model call and provider configuration. Neither has a measured advantage here.

## Fit check

Pass means that the proposed mechanism addresses the requirement; it does not mean that an implementation has passed a test. Fail includes an unresolved mechanism. Words replace symbols to follow the user's formatting rules.

| Req | Requirement | Status | A | B | C |
|---|---|---|---|---|---|
| R0 | Select useful instructions for the next action, including no skill or several skills when appropriate. | Core goal | Pass | Fail | Fail |
| R1 | Support relevant project skills and plugins without treating every installed skill as relevant to every request. | Must-have | Pass | Pass | Pass |
| R2 | Respect explicit requests, invocation restrictions, availability, and user authority. | Leaning yes | Pass | Fail | Fail |
| R3 | Run selection and load chosen instructions before task execution without manual skill selection. | Undecided | Fail | Fail | Fail |
| R4 | Resolve individual and plugin installations into the runtime's effective inventory without duplicate or hidden candidates. | Leaning yes | Fail | Fail | Fail |
| R5 | Reflect skill edits and installations without maintaining a second set of skill instructions. | Leaning yes | Pass | Pass | Pass |
| R6 | Make each selection inspectable and allow work to continue when selection fails. | Leaning yes | Fail | Fail | Fail |
| R7 | Demonstrate fewer selection errors within an agreed latency and context budget. | Leaning yes | Fail | Fail | Fail |

A relies on the existing runtime for R0 and R2; it adds no separate source of selection or authority. This does not establish its selection accuracy. A cannot establish consistent automatic selection, inventory handling, or an inspectable record. B and C fail R0, R2, R3, R4, and R6 until their execution, inventory, policy, and inspection interfaces are verified. C also lacks an executable ranking and reporting path at the inspected revision. Every shape fails R7 until a budget and measured comparison exist.

## Evaluation proposal

| ID | Check | Proposed evidence |
|---|---|---|
| E1 | Useful selection | Use 60 to 100 real requests with task context. Label acceptable sets, required skills, forbidden skills, and no-skill cases. Report omissions and unnecessary selections separately. |
| E2 | Fair comparison | Freeze development and held-out cases by task family. Compare CURRENT, A, and B with the same model, project evidence, and available inventory. Repeat cases to expose variation. Keep C out until it can execute. |
| E3 | Policy correctness | Include explicit-only skills, ambiguous names, duplicate installations, stale content, unavailable skills, and changed user constraints. Require zero policy violations in the test set. |
| E4 | Actual use | On representative tasks, confirm that chosen instructions are read before the relevant action and improve task behavior. A selected ID alone is insufficient evidence. |
| E5 | Total cost | Measure selection latency, total input tokens including existing runtime descriptions, body reads, extra calls, and fallback frequency. Report typical and high-percentile latency. |

User owns acceptance labels and the cost limit; an implementer can prepare cases and run comparisons. No numeric quality target is accepted yet. A small pilot supports a next decision, not a claim of general reliability. Do not tune descriptions against the held-out set or use the selector's own choice as the expected answer.

## Decisions needed

| ID | Decision | State |
|---|---|---|
| Q1 | First supported runtime: Codex, Claude Code, or several runtimes. | Asked; unanswered. |
| Q2 | Automatic selection and loading, or recommendations for the active agent to review. | Asked; unanswered. |
| Q3 | Time budget and acceptable added latency and context cost. | Set after the baseline cost is known. |

## Boundaries and next decision

No implementation, catalog-wide schema change, vector database, background service, automatic installation, or automatic learning is proposed for this shaping pass. Token savings are not assumed when the runtime still exposes every skill description.

After Q1 and Q2 are answered, verify the runtime's inventory, selection trigger, active-model access, and instruction-loading path. If automatic integration is unavailable, explicitly decide whether advisory native selection is sufficient. Do not silently replace R3 with an optional skill.

Select A or B only after this check and the user's scope decision. Then map its concrete interactions and prepare implementation slices. The current draft is not ready for slicing.
