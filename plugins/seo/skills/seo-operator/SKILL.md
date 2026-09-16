---
name: seo-operator
description: "Select and verify one evidence-led SEO action across an existing site."
metadata:
  requires: "seo-audit,meta-optimizer,seo-content,keyword-strategist,structure-architect,keyword-research,schema-architect,ai-crawler-readiness,aeo-scorecard,geo-content-optimizer"
---

# SEO Operator

Run one bounded SEO operating cycle for the site in the user's request. This is a named, user-invoked cookbook. It composes existing skills and does not replace them or auto-trigger a broad SEO program.

## Operating Contract

Before selecting work, establish:

- site, property, and URL scope
- the user's goal and the smallest useful outcome
- the evidence and data-access boundary
- the permission boundary, including whether production, external, destructive, or publishing changes are authorized
- the owner and follow-up date

Read available local SEO foundation and history, such as `.seo/brand.md`, `.seo/content-ledger.md`, `.seo/link-inventory.md`, keyword research, crawl exports, change records, and prior measurement records. Read without overwriting. Treat live pages as evidence of publication, not as authoritative proof of disputed product claims. Check those claims against owner-approved facts.

Label every important observation and measurement as available, unavailable, partial, capped, sampled, or stale. Reconcile known URL inventories across the available sources. State the source, date, inclusion rules, and gaps. Do not call an incomplete inventory whole-site coverage.

Keep three things separate:

- queries, pages, and sources
- missing data and zero data
- prepared, local-validated, and deployed-verified behavior

Do not promise ranking, citation, traffic, or conversion lifts. Use delegated skills as task guidance, not authority for undocumented search mechanics. Check remediation claims against current primary documentation. Label unsupported ranking stages, signal names, authority caps, sandbox timelines, keyword-density targets, and universal thresholds as hypotheses. They cannot justify a defect, eligibility gate, or repair.

## Seven-Lane Coverage

| Lane | Invoke | One-action boundary |
| --- | --- | --- |
| Technical repair | `seo-audit`, `meta-optimizer` | Diagnose one bounded technical or metadata repair and prepare the smallest safe artifact. |
| Existing-page refresh | `seo-content`, `keyword-strategist`, `meta-optimizer` | Refresh one known eligible page, including factual corrections only when the correction is verified against owner-approved facts. |
| Internal links | `structure-architect` | Propose or apply one bounded, relevant link change within the known inventory. |
| New search-led content | `keyword-research`, `seo-content` | Select or draft one search-led asset. Do not build free-tool automation, generate a programmatic collection, or publish. |
| Schema | `schema-architect` | Audit or prepare one schema change supported by visible content. Validate it before marking it validated. |
| Crawler readiness | `ai-crawler-readiness` | Prepare one HTTP, robots, Markdown, alternate-link, negotiation, or analytics readiness change. Verify provider policy before any live robots change. |
| AEO | `aeo-scorecard`, `geo-content-optimizer` | Establish or improve one measured answer-extraction baseline or one content artifact. Treat citation evidence as observation, not a guarantee. |

The matrix is a routing aid, not a requirement to run every lane. Use only the selected lane's skill or skills after the baseline. Skills that normally request broader output remain constrained to one action in this cookbook.

## Baseline And Selection

1. Record scope, goal, permissions, owner, date, and the local evidence sources.
2. Read the local foundation and persistent action register. Reconcile due outcomes before selection using the measurement rules below. Preserve immature outcomes as pending and identify stale, partial, sampled, capped, and unavailable inputs.
3. Reconcile the known URL inventory and eligible candidates. Keep source URL lists and exclusions visible.
4. Check every proposed product claim against owner-approved facts. Mark unresolved claims as blocked; never silently use a live page to settle a dispute.
5. List known candidates across the seven lanes. Mark unassessed lanes and explain missing evidence rather than inventing candidates. Give each candidate a stable ID, target, and evidence for every rating in the rubric below.
6. Apply eligibility gates first: the candidate needs a supported diagnosis, settled facts, sufficient permission for its exact artifact, a verification method, at least medium impact and confidence, and no more than medium risk. Exclude changes to a target with a pending outcome. A verified urgent correction may bypass only this pending-outcome exclusion; record contamination and keep all other gates.
7. Order eligible candidates by impact (high first), then confidence (high first), effort (low first), risk (low first), and finally stable candidate ID in ascending order. Select the first candidate. Choose no action when none qualifies. Ratings are review heuristics, not forecasts of recoverable clicks or expected revenue.
8. Persist the selected action or no-action decision, deferred candidates, evidence baseline, target, hypothesis, and exact planned artifact before invoking the selected lane.

| Rating | Low | Medium | High |
| --- | --- | --- | --- |
| Impact | Cosmetic or weak connection to the stated goal | Supported opportunity or defect on an in-scope page, without evidence of a critical blocker | Verified blocker, material false claim, or measured loss on a priority page named in the goal |
| Confidence | Missing, stale, disputed, or indirect evidence | Current attributable evidence supports the diagnosis, with stated limits | Direct reproduction or owner-approved facts establish the diagnosis, with applicable primary guidance |
| Effort | One localized edit with an existing check | One artifact needs research or several related edits and checks | New implementation, migration preparation, or several coordinated components |
| Risk | Reversible local draft or patch, no shared behavior change | Reversible shared behavior change with known affected scope and rollback | Irreversible effect, unknown affected scope, unresolved safety concern, or unauthorized execution |

Defer every non-selected candidate visibly with its reason. Give repeated candidates their existing IDs. A preparation candidate must rate the preparation artifact, not imply permission to deploy it.

## Authorization And Execution

Drafts, recommendations, and local patches are the default. Ask for explicit authorization before production, destructive, external, outreach, distribution, or publishing changes. Prepare migrations when needed, but do not run them. The initial slice excludes automated free-tool builds, programmatic content generation, outreach or distribution, and pruning or deletion.

Invoke only the selected lane skill or skills. Pass the established scope, evidence labels, fact boundary, primary-documentation requirement, one-action limit, permission boundary, and required verification state. Keep the underlying skill's output within the selected artifact. Do not expand a page refresh into a site refresh, a schema audit into unrelated markup, or a crawler review into a live policy change.

Verify the changed behavior at the strongest available level:

- prepared: the draft, recommendation, patch, or migration exists but is not applied
- local-validated: the local artifact or behavior passed relevant deterministic or fixture checks
- deployed-verified: the authorized deployed artifact was checked in its target environment

Never label an unrun migration, unpublished draft, or unobserved deployment as deployed-verified.

## Registration And Later Measurement

Use the project's existing durable action register, or create `.seo/action-register.md` if none exists. This is a project-local default, not an installation path. Append records and dated updates; never replace unrelated history. If the register cannot be written, stop before execution and report the blocker. A chat-only report is not registration.

Persist each run, including no-action runs, with:

- stable run and candidate IDs; selected and deferred actions with reasons and ratings
- evidence references, baseline, coverage labels, target, and bounded hypothesis
- exact prepared or changed artifact, authorization, and verification result with date
- observed deployment date and revision, or unknown if not observed
- outcome state: not-deployed, pending, resolved, or inconclusive
- primary metric, source, scope, before/after window dates and length, finalization criteria, owner, and follow-up date
- dated measurement results, confounders, and confidence adjustments linked to earlier records

Set the measurement plan before execution. For Search Console, default to equal 28-day before/after windows around the observed deployment date using finalized days. Record timezone, source filters, query/page scope, and any reason for a different duration. Prepared artifacts stay not-deployed; deployment starts pending measurement. Local validation does not start a traffic measurement window. For AEO observations, preserve the prompt set, platform/model, collection method, and observation schedule instead of imposing Search Console windows.

At the next run, reconcile records due for review. Keep incomplete windows pending and set a new review date; never treat missing rows as zero. Finalize only when the planned comparable windows or observations are complete and coverage is sufficient for the stated metric. Keep query, page, and source outcomes distinct. Record seasonal changes, other deployments, scope changes, and controls when available. Mark results inconclusive when contamination or missing evidence prevents comparison. Record verified urgent corrections as intervening changes, then revise the affected measurement plan rather than attributing the combined result to the earlier action.

Use comparable resolved records to review the confidence assigned to similar future candidates. Record the supporting action IDs and a reason to retain, raise, or lower confidence. A single before/after association cannot raise confidence or establish cause. Inconclusive or immature outcomes cannot count as wins or losses. Keep adjustments explicit and human-reviewable, never automatic learned weights, and never override current diagnosis, fact, or permission gates. Report observed metric movement with its limits, not a causal ranking or citation lift.

## Report

Return:

1. scope, goal, permission boundary, owner, and date
2. evidence baseline, URL inventory coverage, fact verification, and unavailable inputs
3. seven-lane candidate matrix with impact, confidence, effort, risk, and evidence
4. selected action or explicit no-action decision
5. deferred actions and reasons
6. selected lane output and exact artifact
7. prepared, local-validated, or deployed-verified status
8. registration record and follow-up date
9. limitations, confounders, and unresolved issues

## Installation

Install the cookbook and its dependencies:

```sh
npx skills add majesticlabs-dev/majestic-abilities --skill seo-operator \
  seo-audit meta-optimizer seo-content keyword-strategist structure-architect \
  keyword-research schema-architect ai-crawler-readiness aeo-scorecard \
  geo-content-optimizer
```

## Hard Gates

- No lane selection without a stated scope, goal, permission boundary, evidence baseline, and known-inventory limits.
- No whole-site claim from an incomplete URL inventory.
- No disputed product claim without owner-approved facts.
- No more than one selected action per operating cycle.
- No production, destructive, external, publishing, or migration execution without explicit authorization.
- No deployed-verified status without deployment access and direct verification.
- No outcome claim without comparable finalized windows and recorded limitations.
