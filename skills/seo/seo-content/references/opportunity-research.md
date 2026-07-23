# Opportunity Research

Use this when the user asks what to publish next or gives a broad topic instead of a fixed keyword.

## Candidate Sources

- existing keyword research
- Search Console queries
- sales objections
- customer questions
- competitor pages
- Reddit and community threads
- support tickets or help docs
- product use cases
- AI answer gaps

## Scoring Model

Score each factor from 1 to 5.

| Factor | 1 | 3 | 5 |
|---|---|---|---|
| Buyer intent | curiosity only | problem-aware | actively comparing or buying |
| Winnability | dominated by strong sites | mixed SERP | weak/generic results |
| Content gap | already answered well | partial gaps | clear missing angle or outdated info |
| Internal-link fit | isolated topic | some link support | strong cluster fit |
| Pipeline relevance | vanity traffic | relevant audience | tied to offer, CTA, or sales motion |
| Freshness urgency | evergreen and stable | minor changes | fast-moving or stale SERP |

Total score range: 6-30.

## Decision Rule

Pick the highest score unless one of these overrides applies:

- a launch or sales push needs support now
- a major competitor owns a strategic narrative
- the topic captures buyer language needed for positioning
- legal, compliance, or product constraints block publication

## Output

```markdown
| Candidate | Intent | Winnability | Gap | Link Fit | Pipeline | Freshness | Total | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
```

## Low-Confidence Labels

Use these labels instead of pretending certainty:

- `estimated volume`
- `unverified SERP strength`
- `needs Search Console data`
- `requires SME proof`
