# SEO Audit Detailed Reference

## Output Format

```markdown
## SEO Audit Report

**Scope:** [site, URL or template set, locale, device]
**Date:** [audit date]
**Permission:** [audit only | prepared recommendation | authorized local change]
**Inventory coverage:** [complete, sampled, or partial, with source and gaps]

### Executive Summary
[Evidence-backed summary. Do not claim a cause when evidence supports only a hypothesis.]

### Evidence Baseline
| Source | Scope/date | State | What it can establish | Limitation |
|---|---|---|---|---|
| Crawl or HTTP fetch | [scope/date] | observed/partial | [fact] | [gap] |
| Search Console | [property/window] | observed/partial | [metric] | [gap] |
| Analytics or logs | [scope/window] | observed/partial | [metric] | [attribution limit] |
| Owner-approved facts | [record/date] | observed/partial | [claim] | [gap] |

### Priority Findings
| ID | Observation and evidence | Severity | Confidence | Smallest fix | Verification |
|---|---|---|---|---|---|
| [ID] | [scoped observation] | [level] | [level/reason] | [bounded action] | [test/result] |

### Technical Findings
[HTTP, indexability, canonicals, redirects, mobile, performance, sitemap, and structured data. Record intentional controls separately.]

### Content Findings
[Intent, useful coverage, accuracy, originality, freshness, authorship, and reader comprehension.]

### AI and Answer Readiness
[Extractability and attributable facts. Do not promise crawling, recommendations, or citations.]

### Measurement
[Comparable query/page metrics, source dates, denominators, missing data, confounders, and next observation date.]

### Unresolved Questions
[Owner decisions, unavailable logs, disputed facts, and tests needed to falsify hypotheses.]
```

## Severity and Confidence

Severity describes the plausible impact in the scoped context, not a ranking penalty:

- `critical`: a verified issue blocks the intended page or important user action
- `high`: a verified issue materially prevents access, understanding, or measurement
- `medium`: a supported issue with meaningful but non-blocking impact
- `low`: a localized improvement with limited expected impact
- `informational`: an observation or opportunity without a demonstrated defect

Confidence describes evidence quality:

- `high`: directly reproduced or established by current, attributable evidence
- `medium`: supported by current evidence with a material limitation
- `low`: plausible hypothesis needing a targeted test or missing source

## Quick Audit Option

For a bounded audit, inspect:

1. HTTP status, redirects, canonical, robots, and noindex intent
2. Title, description, headings, links, and visible content
3. Intent, factual support, authorship, and freshness
4. Answer extractability and structured-data fit
5. Dated Search Console, analytics, or server evidence if diagnosis is requested

Return the top findings with evidence state, severity, confidence, smallest fix, verification, and limitations. Do not score the page or treat missing data as zero.

## Falsifiable Diagnosis Pattern

Use this structure when the user asks why performance changed:

1. **Observation:** [metric movement, exact scope, source, and dates]
2. **Candidate explanation:** [technical, demand, content, or search-change hypothesis]
3. **Evidence for:** [specific observations]
4. **Evidence against or missing:** [specific gaps]
5. **Test:** [smallest comparison, fetch, log check, or owner confirmation]
6. **Decision rule:** [what result would support or reject the hypothesis]

Do not label an age, authority, click, or machine-learning theory as the cause without attributable evidence. See [the bounded evidence vocabulary](../assets/google-ranking-signals.yaml) used by this skill.
