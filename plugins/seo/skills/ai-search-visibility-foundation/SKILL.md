---
name: ai-search-visibility-foundation
description: "Audit and establish a website's SEO, entity, AI navigation, crawler, structured-data, and AEO measurement foundations. Use when the user invokes /ai-search-visibility-foundation or wants a site-level AI search visibility program with validated implementation evidence."
---

# AI Search Visibility Foundation

Establish the visibility foundation for the site described in $ARGUMENTS. Complete the phases in order. Report implementation and measurement evidence without promising rankings, recommendations, or citations.

## Phase 1: Establish The Baseline

Invoke the `seo-audit` skill.

Record the audit date, domain and URL scope, technical SEO state, content quality, E-E-A-T signals, entity trust signals, and AI/GEO readiness. Separate site-wide blockers from page-level improvements and retain the URLs or evidence behind each finding.

Use `seo-audit` as an inventory framework, not as authority for undocumented ranking mechanics. Do not treat leaked signal names, fixed ranking stages, universal scoring weights, domain-authority caps, sandbox timelines, keyword-density targets, or character-count rules as established facts. Verify remediation claims against current primary documentation, label unsupported mechanics as hypotheses, and do not use them as gates or promises.

Do not claim improvement without this baseline.

## Phase 2: Define The Entity Model

Invoke the `entity-triplets` skill.

Audit current company, product, category, specialization, leadership, location, audience, and differentiator statements across first-party and trusted third-party sources. Produce a factual target set and an inconsistency remediation list.

Do not invent founding details, leadership, credentials, achievements, categories, or third-party recognition.

## Phase 3: Build AI Navigation

Invoke the `llms-txt-builder` skill.

Create or propose `/llms.txt` using canonical URLs for the homepage, core products or services, major categories, documentation, pricing, contact, support, and high-value resources. Validate every included link and keep descriptions factual.

Treat `/llms.txt` as a navigation aid and discoverability hedge, not a ranking or citation guarantee.

## Phase 4: Configure Crawler Readiness

Invoke the `ai-crawler-readiness` skill.

Work through the six layers in order:

1. robots policy by search, user-fetch, and training crawler purpose
2. Markdown shadow routes for priority content
3. HTML alternate links
4. HTTP `Link` headers
5. `Accept: text/markdown` negotiation with correct caching behavior
6. server-side bot and AI-referrer analytics

Verify current provider bot names and policies before changing a live robots policy. Do not opt into model-training crawlers without explicit site-owner approval.

## Phase 5: Implement Structured Data

Invoke the `schema-architect` skill.

Audit and implement only schema types supported by visible page content and the site's search goals. Validate JSON-LD with the relevant Google and Schema.org tools. Record pass, fail, and unsupported outcomes.

Structured data supports classic search, rich results, entity disambiguation, and Google AI Overviews. Do not claim that chat LLMs use it as a direct citation signal.

## Phase 6: Create The Measurement Baseline

Invoke the `aeo-scorecard` skill.

Define priority queries, comparison brands, observation method, visibility and citation evidence, bot and referral measurements, owners, and review cadence. Treat generic target percentages as hypotheses until the site's own baseline and economics justify them.

Repeated observations must preserve the same query set and method closely enough to support comparison.

## Phase 7: Report

Return:

1. dated baseline audit and scoped URL inventory
2. target entity triplets and inconsistency actions
3. `/llms.txt` status and link-validation result
4. six-layer crawler-readiness results
5. structured-data implementation and validator results
6. AEO scorecard baseline, owners, and next review date
7. blockers, unknowns, and unproven assumptions

Distinguish `IMPLEMENTED`, `VALIDATED`, `BLOCKED`, and `NOT APPLICABLE`. Never report expected visibility lift as observed performance.

## Requires

- `seo-audit` - Phase 1 SEO, content, trust, and GEO baseline
- `entity-triplets` - Phase 2 entity consistency model
- `llms-txt-builder` - Phase 3 AI navigation file
- `ai-crawler-readiness` - Phase 4 HTTP discovery and measurement layers
- `schema-architect` - Phase 5 structured-data implementation and validation
- `aeo-scorecard` - Phase 6 recurring visibility measurement

Install everything:

```sh
npx skills add OWNER/REPOSITORY --skill ai-search-visibility-foundation \
  seo-audit entity-triplets llms-txt-builder ai-crawler-readiness \
  schema-architect aeo-scorecard --agent claude-code --yes
```

Or as Claude Code plugins:

```sh
/plugin marketplace add OWNER/REPOSITORY
/plugin install majestic-seo@majestic-abilities
```

## Hard Gates

- Do not prescribe remediation without a dated domain and URL scope plus baseline evidence from current, attributable sources; undocumented ranking mechanics cannot justify a gate.
- Do not publish entity statements that lack first-party evidence or an attributable trusted source.
- Every URL included in `/llms.txt` must resolve and represent the described canonical resource.
- Record pass or fail evidence for each applicable crawler-readiness layer; later layers cannot compensate for a blocking robots policy.
- Structured data must match visible content and pass the applicable validator before being marked validated.
- Do not claim ranking, visibility, recommendation, referral, or citation lift without a comparable baseline and repeated observations.

Back link checks, HTTP response checks, structured-data validation, and analytics instrumentation with repository tests, deployment checks, or monitoring where the consuming project supports them.
