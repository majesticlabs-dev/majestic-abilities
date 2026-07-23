# SEO Audit Skill Detailed Reference

## Output Format

### SEO Audit Report

```markdown
## SEO Audit Report

**Page:** [URL or filename]
**Date:** [Audit date]
**Overall Score:** X/100
**Domain Status:** [Established/New (sandbox considerations)]

### Executive Summary
[2-3 sentence overview including pipeline stage bottlenecks]

### Scores by Category

| Category | Score | Status | Key Signal |
|----------|-------|--------|------------|
| Domain/History | X/10 | [Status] | siteAuthority |
| Technical SEO | X/15 | [Status] | titlematchScore |
| Content Quality | X/25 | [Status] | contentEffort |
| Keyword Optimization | X/10 | [Status] | Topicality |
| E-E-A-T Signals | X/20 | [Status] | Trust signals |
| AI/GEO Readiness | X/10 | [Status] | Extractability |
| User Behavior | X/10 | [Status] | NavBoost |

### Pipeline Bottleneck Analysis
[Which pipeline stage is the primary blocker? Mustang quality? Topicality match? NavBoost signals?]

### Priority Issues (Fix First)

1. **[Issue]** - [Impact] - [Fix] - [Signal affected]
2. **[Issue]** - [Impact] - [Fix] - [Signal affected]
3. **[Issue]** - [Impact] - [Fix] - [Signal affected]

### Domain Context
[Sandbox status, authority inheritance, URL history]

### Technical SEO Findings
[Detailed findings with specific recommendations]

### Content Quality Findings
[contentEffort indicators, token optimization, freshness]

### Keyword Analysis
[Primary keyword performance, semantic gaps, entity coverage]

### E-E-A-T Assessment
[Specific signals present/missing, disconnected entity risk]

### AI Visibility Assessment
[GEO readiness score and improvements]

### User Behavior Optimization
[Click quality, dwell time, engagement improvements]

### Action Plan

**Immediate (This Week):**
- [ ] Action 1
- [ ] Action 2

**Short-term (This Month):**
- [ ] Action 1
- [ ] Action 2

**Ongoing (Sandbox Graduation):**
- [ ] Consistent quality publishing
- [ ] Social signal building
- [ ] Backlink acquisition
- [ ] User engagement optimization
```

## Scoring Guide

**90-100:** Excellent - Minor optimizations only
**70-89:** Good - Some improvements needed
**50-69:** Needs Work - Significant gaps to address
**Below 50:** Critical - Major overhaul required

**New Domain Adjustment:** Subtract 10-15 points for sandbox limitations. Focus on graduation signals.

## Quick Audit Option

For faster audits, focus on:

1. **Domain Context** - Established or sandbox? URL history?
2. **Title & Meta** - Optimized for `titlematchScore`?
3. **Content Quality** - `contentEffort` indicators present?
4. **E-E-A-T** - Disconnected entity risk?
5. **AI Ready** - Inverted pyramid, extractable format?

Deliver top 5 issues with affected signals and fixes.

## Signal Reference

For detailed signal documentation, see:
`assets/google-ranking-signals.yaml`

Key signals to remember:
- `titlematchScore` - Title relevance to query
- `contentEffort` - ML-assessed content investment
- `OriginalContentScore` - Uniqueness (0-512 scale)
- `semanticDate` - Actual freshness of facts/sources
- `siteAuthority` - Domain-level authority cap
- `chromeInTotal` - Popularity via Chrome data
