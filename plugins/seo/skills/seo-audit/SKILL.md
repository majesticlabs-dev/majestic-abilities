---
name: seo-audit
description: "Evaluate search performance and diagnose ranking issues."
---

# SEO Audit Skill

A scoped, evidence-led audit of technical search foundations, page content, authorship, AI readability, and measurement. It separates observed facts from hypotheses and unknowns.

## When to Use

- Auditing existing content for SEO performance
- Reviewing new content before publication
- Identifying optimization opportunities
- Assessing AI citation readiness
- Evaluating E-E-A-T signals
- Checking technical SEO elements
- Diagnosing why content isn't ranking
- Reviewing a new domain or URL without assuming an age-based ranking restriction

## Evidence Rules

- Use the page, crawl, server, analytics, Search Console, and owner-approved content evidence that is actually available.
- Record each material observation as `observed`, `partial`, `unknown`, `unavailable`, or `hypothesis`, with source and date.
- Do not present leaked or external signal names, fixed ranking stages, authority caps, sandbox timelines, URL-history resets, machine-learning scores, or click behavior as established defects or repair gates.
- A before/after association does not prove causation. For traffic changes, compare scoped Search Console and analytics data while considering technical changes, seasonality, demand, and search changes.
- Never invent factual claims, authorship, ownership, performance, or a cause for missing clicks.
- An intentional `robots.txt` rule, `noindex`, or canonical is an observation first. Check the owner's intent and the eligible URL scope before calling it a defect.
- Audit-only requests produce findings and recommendations. They must not edit, publish, redirect, remove, or deploy anything.

Use current primary guidance where applicable:

- [Google Search Essentials](https://developers.google.com/search/docs/essentials)
- [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Debugging drops in Google Search traffic](https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops)
- [Title links](https://developers.google.com/search/docs/appearance/title-link)
- [Snippets](https://developers.google.com/search/docs/appearance/snippet)

## Audit Framework

### Phase 0: Scope and Evidence

Record:

- audit date, site/property, URL or template scope, locale, device, and requested question
- known URL inventory and its source, date, inclusion rules, and gaps
- available crawl, HTTP, rendered-page, Search Console, analytics, server-log, content, and owner-approved fact evidence
- permissions: audit only, prepared recommendation, or explicitly authorized local change
- unavailable inputs and what they prevent you from concluding

Do not call a sample or partial inventory a whole-site audit.

### Phase 1: Technical SEO Check

Evaluate only the URLs and evidence in scope:

**Page-Level Technical:**
- [ ] HTTP status, redirect chain, and final canonical URL
- [ ] Indexability controls: `robots.txt`, `noindex`, canonical, authentication, and rendered availability
- [ ] Title and description accurately describe visible page content; no fixed length rule
- [ ] H1 tag and meaningful page structure
- [ ] Heading hierarchy
- [ ] Image alt text where it conveys information
- [ ] Internal links (contextual, relevant)
- [ ] External links and cited claims where evidence is needed
- [ ] Structured data matches visible content and is valid for its intended consumer

**Site-Level Technical:**
- [ ] HTTPS enabled
- [ ] Mobile rendering and interaction
- [ ] Performance evidence from the selected URLs and measurement method
- [ ] XML sitemap inclusion
- [ ] `robots.txt` accessibility and intended rules
- [ ] Duplicate, redirect, canonical, and pagination patterns

**Intent checks before defects:**
- [ ] Confirm a `noindex`, disallow, or canonical is unintended before recommending a change.
- [ ] Confirm the requested URL is the intended representative URL before treating another canonical as an error.
- [ ] Confirm redirects are unnecessary or harmful before proposing a URL change.

### Phase 2: Content Quality Assessment

Assess whether the page helps its intended reader:

- [ ] Search intent and audience are explicit or reasonably evidenced
- [ ] The page answers the main need with useful, accurate, sufficiently complete information
- [ ] Claims, dates, statistics, and product facts have attributable evidence where material
- [ ] Original experience, examples, methods, or analysis are identified when present
- [ ] Freshness reflects substantive updates, not a date-only change
- [ ] The main answer is findable, with headings, lists, tables, or other structure that serves readers
- [ ] Important content is not hidden behind avoidable interaction, boilerplate, or inaccessible media
- [ ] Reading and comprehension issues are described concretely, without universal word-count or readability gates

Google does not publish a preferred word count. E-E-A-T is a useful quality assessment concept, not a numeric score or a standalone ranking factor.

### Phase 3: Keyword and Semantic Analysis

Assess intent and useful language, not density:

- [ ] Target query or task is known and matches the page's purpose
- [ ] Important concepts and entities are explained naturally where relevant
- [ ] The page covers material subquestions without padding or stuffing
- [ ] Terms in title, headings, links, and body are accurate and natural
- [ ] Competing pages are used as context for missing useful coverage, not as a quota
- [ ] Ambiguous entities, claims, and relationships are clarified with attributable sources

### Phase 4: E-E-A-T Evaluation

Assess what a reader can verify:

**Experience Signals:**
- [ ] First-hand experience indicated
- [ ] Case studies/examples included
- [ ] Original data/research
- [ ] Process documentation

**Expertise Signals:**
- [ ] Author credentials visible
- [ ] Technical accuracy
- [ ] Comprehensive coverage
- [ ] Expert quotes/interviews

**Authority Signals:**
- [ ] Authoritative external citations
- [ ] Industry recognition
- [ ] Brand mentions
- [ ] Published research

**Trust Signals:**
- [ ] Contact information
- [ ] Privacy policy
- [ ] Editorial guidelines
- [ ] Reviews/testimonials
- [ ] Security indicators

Do not infer a universal demotion from missing fields. State which reader question remains unanswered and what evidence would resolve it.

### Phase 5: AI and Answer Readiness

Assess extractability as an observed content property, not a citation promise:

**Extractability:**
- [ ] Summary or direct answer is easy to locate
- [ ] Clear topic sentences lead with useful facts
- [ ] Bullet lists for features
- [ ] Tables for comparisons
- [ ] Question-and-answer sections where the audience needs them

**Fact Density:**
- [ ] Statistics with sources
- [ ] Specific numbers/dates
- [ ] Verifiable data points
- [ ] Expert quotes with attribution

**Structure for AI:**
- [ ] Question-based headers
- [ ] Direct answers near top when useful
- [ ] Logical information hierarchy
- [ ] Structured data only where it describes visible content and serves a documented use

### Phase 6: Measurement and Diagnosis

Use attributable observations:

- [ ] Title and description accurately represent content
- [ ] Search Console impressions, clicks, CTR, position, and query/page scope are dated and comparable
- [ ] Analytics conversions and referrals have documented attribution limits
- [ ] Server or CDN logs, if used, distinguish verified fetches from response mentions or citations
- [ ] Technical changes, seasonality, demand, and search changes are considered before a cause is proposed
- [ ] Missing rows are `unknown` or `partial`, not zero

## Finding Contract

Every finding must include:

| Field | Required content |
| --- | --- |
| Observation | What was seen, where, source, date, and evidence state |
| Scope | URL, template, query, device, locale, or inventory boundary |
| Severity | `critical`, `high`, `medium`, `low`, or `informational`, tied to user/search impact |
| Confidence | `high`, `medium`, or `low`, with the reason and limits |
| Interpretation | Defect, opportunity, intentional control, unknown, or falsifiable hypothesis |
| Smallest fix | One bounded, authorized preparation or recommendation |
| Verification | Exact local or target-environment check and expected observable result |
| Limitation | Missing evidence, confounder, or unresolved owner decision |

Do not produce an overall numeric health score or subtract points for site age. Prefer prioritized findings over an invented aggregate.

## Detailed Reference

Load [detailed-reference.md](references/detailed-reference.md) for extended examples, templates, and advanced patterns.
