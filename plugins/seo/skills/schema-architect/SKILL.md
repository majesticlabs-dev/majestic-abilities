---
name: schema-architect
description: "Use when adding or auditing Schema.org structured data."
---

# Schema Architect

Design or audit Schema.org structured data from visible page content, the site's actual goal, and current documented Google feature eligibility. Schema.org validity can help other consumers, but it does not guarantee a Google result, Knowledge Panel, AI answer, or citation.

## Decision Rules

1. Identify the page's visible content, audience, and intended consumer.
2. Choose the most specific type supported by that content. Do not add markup only because an archetype table lists it.
3. Check the current [Google Search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) and [structured data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).
4. Include only facts supported by visible content and approved source records. Omit unknown optional fields; never fill them with guesses or placeholders in production.
5. For reviews and ratings, verify the actual reviewed entity, review source, aggregation method, content visibility, and policy eligibility. Do not mark self-controlled Organization or LocalBusiness reviews as eligible for Google's review feature.
6. Validate syntax and vocabulary separately from feature eligibility and deployment.
7. Treat actual search appearance as an observation that requires a dated target-environment check.

Current constraints:

- `FAQPage` remains valid Schema.org vocabulary for appropriate consumers, but FAQ rich results no longer appear in Google Search as of May 7, 2026.
- `HowTo` remains valid Schema.org vocabulary, but How-to rich results no longer appear in Google Search on desktop or mobile.
- Sitelinks search box markup is not a current Google Search feature. Ordinary sitelinks are not guaranteed by `WebSite`.
- `Organization` and `WebSite` do not guarantee a Knowledge Panel.
- `Service` and `Offer` are not generic promises of a Google price result. A price must be real, visible, current, and appropriate to the page and feature.
- `AggregateRating` is not a standalone promise of stars. Use a supported reviewed type and genuine, policy-compliant ratings.
- AI Overviews and AI Mode use ordinary search fundamentals. There is no special schema that guarantees AI citations.

Primary references:

- [Structured data feature gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
- [Structured data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [Review snippet policies](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)
- [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google Search updates](https://developers.google.com/search/updates)

## Schema Selection Checklist

- [ ] Page type and visible content are documented.
- [ ] Selected Schema.org type is semantically accurate.
- [ ] Every required and recommended field has approved evidence.
- [ ] Optional unknown fields are omitted.
- [ ] `sameAs`, author, publisher, logo, price, availability, dates, and ratings are checked against current visible facts.
- [ ] Reviews identify the reviewed entity and satisfy current policy.
- [ ] FAQ and HowTo markup is labeled for non-Google consumers when relevant, never as a Google rich-result promise.
- [ ] Google feature eligibility is checked independently from Schema.org validity.
- [ ] Deployment and actual appearance have separate verification records.

## Site Archetypes

See [references/site-archetypes.yaml](references/site-archetypes.yaml) for content-led mappings. They are starting points, not blanket priorities.

## Templates

See [references/schema-templates.yaml](references/schema-templates.yaml) for valid JSON-LD examples. Treat every placeholder as a value to verify before deployment. Templates are examples, not permission to emit unknown fields.

## Workflow and Verification States

1. **Inventory:** capture existing JSON-LD, visible page content, URL, and owner-approved facts.
2. **Select:** map content to a type and documented Google feature, if one applies.
3. **Prepare:** generate the smallest markup with verified fields only.
4. **Parse-validate:** confirm JSON-LD syntax and Schema.org vocabulary.
5. **Eligibility-review:** check current Google requirements and policy, including review rules.
6. **Deploy-verify:** confirm the intended production response contains the markup and matches visible content.
7. **Appearance-observe:** record actual Search Console or result observations with date, query, URL, and coverage limits.

Report each state as `not checked`, `pass`, `fail`, `unsupported`, `not applicable`, or `unknown`. A parse pass is not an eligibility pass. Eligibility is not deployment verification. Deployment verification is not an appearance guarantee.

## Output Format

```markdown
## Structured Data Plan

**Scope:** [URL/template and visible-content boundary]
**Goal:** [consumer or documented Google feature]
**Permission:** [audit, prepare, or authorized deployment]

| Type | Visible-content evidence | Schema validity | Google eligibility | Deployment | Appearance |
|---|---|---|---|---|---|
| [type] | [evidence/source/date] | [state] | [state and policy] | [state] | [observed/unknown] |

### Fields
- Include: [verified fields and sources]
- Omit: [unknown or unsupported optional fields]
- Review checks: [reviewed entity, source, policy result]

### Smallest change
[One bounded artifact or recommendation]

### Verification
[Parser, Schema.org, Google eligibility, production, and appearance checks]

### Limitations
[Missing facts, unavailable deployment, sample scope, and non-guarantees]
```
