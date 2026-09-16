---
name: meta-optimizer
description: "Optimize page titles, meta descriptions, and URLs for search."
---

# Meta Optimizer

Create accurate, useful titles, descriptions, and URL recommendations from the target page's visible content and search intent. Optimize for clarity and users, not fixed character rules or click promises.

## Principles

- The title must truthfully describe the page and its visible primary purpose.
- The meta description should summarize useful page content when supplied; Google may use on-page text instead and may rewrite the snippet.
- There is no universal title-element or meta-description length limit. Device width can truncate what is displayed, so preview length is an optional display heuristic, not a ranking or eligibility gate.
- Do not force emotional power words, clickbait, unsupported benefits, or a year merely to create freshness.
- Use relevant language naturally. Do not force a keyword into a fixed character position or repeat it unnaturally.
- URLs are stable by default. Do not rename an existing URL to satisfy a style limit.
- A proposed URL move requires explicit authorization and a plan for the redirect, canonical, internal links, sitemap, external dependencies, and rollback or validation.
- Never claim a metadata change will improve ranking, CTR, traffic, or conversion without a scoped measurement plan and observed evidence.

Current primary guidance:

- [Title links](https://developers.google.com/search/docs/appearance/title-link)
- [Control your snippets](https://developers.google.com/search/docs/appearance/snippet)
- [Google Search Essentials](https://developers.google.com/search/docs/essentials)

## Process

1. Record target URL, locale, device, audience, page intent, permission boundary, and date.
2. Read the visible heading, opening content, offer or task, supporting facts, canonical URL, and current metadata.
3. Identify the smallest accuracy or clarity issue. Treat missing data as unknown.
4. Draft 2-3 truthful title options and 2-3 description options only when alternatives help review.
5. Check that every claim and benefit is visible or approved. Remove invented urgency, awards, prices, dates, and guarantees.
6. Keep the current URL unless an authorized move has a clear user and technical reason.
7. Define target-specific verification: rendered source, canonical, snippet observation, and dated query/page metrics where available.

## Output Format

```markdown
## Meta Package

**Target:** [URL, locale, device]
**Intent:** [page purpose and audience]
**Permission:** [audit only | prepare | authorized change]
**Evidence:** [visible content and source/date]

### Current finding
[Observed issue, evidence state, severity, confidence, and limitation]

### Recommended metadata
- Title: [truthful title]
- Description: [truthful summary]
- URL: [keep current URL | proposed URL only with authorization]

### Alternatives
1. Title: [option]
   Description: [option]
2. Title: [option]
   Description: [option]

### Optional display preview
[Approximate device preview only. State viewport/device assumptions. It is not a limit or ranking rule.]

### Verification
- Visible-content check: [claims match the rendered page]
- Source check: [title/description/canonical in rendered or fetched HTML]
- URL-move check: [authorization, redirect, canonical, links, sitemap, and rollback plan, or not applicable]
- Measurement: [declared query/page scope and date window, or unavailable]

### Limitations
[Google may rewrite title/snippet; missing data, attribution, and deployment limits]
```

## URL Move Gate

Do not propose or apply a URL move for a style preference. If a move is materially justified, first obtain explicit authorization and record:

- old and new canonical URLs and the reason for the move
- one-to-one redirect behavior and loop/chain checks
- canonical and internal-link updates
- sitemap and structured-data URL updates
- external links and known integrations that need review
- publication and rollback plan
- post-deployment verification and measurement window

An audit-only request must not edit metadata, URLs, redirects, canonicals, links, or sitemaps.

## Platform Integration

The output can be translated into the consuming platform's metadata fields, but platform syntax does not change the evidence rules. Validate the rendered result in the target application rather than assuming a saved field was deployed.
