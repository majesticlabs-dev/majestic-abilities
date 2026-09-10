---
name: aeo-scorecard
description: "Use when discussing AEO/GEO metrics or AI visibility performance."
---

# AEO Scorecard: Measuring AI Visibility

Measure what an answer output, fetch log, analytics system, or survey actually shows. Do not turn one evidence class into another, and do not promise rankings, recommendations, citations, traffic, or conversions.

## Evidence Classes

Keep these measures separate:

| Measure | Definition | Evidence source | Does not establish |
| --- | --- | --- | --- |
| Mentions | The brand, site, product, or page was named in a recorded answer | Saved response and transcript | Recommendation, citation, crawl, or click |
| Recommendations | The recorded answer explicitly recommends or includes the entity for the stated task | Saved response, exact wording, and coding rule | Citation or causal influence |
| Citations | The response attributes a claim to a URL or source and links or names that source | Saved response, source attribution, URL, and prompt | A crawl or future visibility |
| Access | A crawler or fetcher requested a URL | Server/CDN logs with verification method | A mention, recommendation, citation, or indexing |
| Click referrals | A user session arrived through a measurable AI referral | Analytics referral data with scope and attribution rules | All AI-influenced visits |
| Self-reported discovery | A respondent says an AI product influenced discovery | Survey response with question, date, and sample | Verified referral or causal exposure |

A crawl or fetch is not a citation. GA4 is not complete raw bot logging. Bot user-agent strings can be spoofed, so use provider verification methods and server/CDN evidence where bot identity matters.

## Sample Design

Before collecting observations, record a dated plan:

| Field | Record |
| --- | --- |
| Platforms | Product and access mode, such as ChatGPT Search or Google AI feature |
| Model/version | Visible model label or `unknown` |
| Prompt set | Stable IDs, exact text, intent, and target entity |
| Locale/device | Locale, country, language, device, and logged-in state |
| Search mode | Search enabled, web mode, answer-only mode, or other exact mode |
| Collection date/time | Time zone and run identifier |
| Replicates | Number of independent runs per prompt and sampling reason |
| Coding rules | What counts as a mention, recommendation, citation, and correct attribution |
| Denominator | Eligible successful samples for each metric, not all planned samples |
| Baseline/target | Site-specific baseline, target, owner, and review date |

Repeat the same prompt IDs, platform/model, locale, search mode, coding rules, and sampling schedule closely enough to compare observations. If any of these change, mark the comparison as a method change.

## Scorecard Measures

Calculate each measure from its own eligible denominator:

- **Mention rate:** responses containing a coded brand/site mention / eligible completed responses
- **Recommendation rate:** responses meeting the recommendation rule / eligible completed responses
- **Citation rate:** responses with an attributable target citation / eligible responses that made a source-attribution claim or the predeclared citation denominator
- **Access rate:** verified fetches for the scoped URLs / relevant verified requests, if that denominator is meaningful
- **Referral rate:** measurable AI referrals / sessions in the declared analytics scope
- **Survey discovery rate:** respondents selecting an AI discovery option / valid survey responses

Report numerator, denominator, date range, query/prompt scope, and coding rule. A failed, blocked, malformed, or partial sample is `failed` or `partial`, not zero. Keep it in a coverage field and explain whether it is excluded from the eligible denominator.

## Bot and Access Controls

Use current provider documentation before changing robots policies or interpreting logs:

- [Google common crawlers and fetchers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers)
- [OpenAI bots](https://developers.openai.com/api/docs/bots)

`Google-Extended` is a robots control token. It has no separate HTTP user-agent. It governs Google's training and grounding uses and does not control Google Search inclusion or ranking. Do not tell users to find `Google-Extended` in GA4.

For OpenAI, keep roles distinct: `OAI-SearchBot` supports search, `GPTBot` concerns training, and `ChatGPT-User` is user-initiated retrieval. Search, training, and user-fetch permissions are separate. No bot-provider connection is required for this standalone scorecard. If logs are unavailable, record access as unavailable rather than inferring it from answer results.

## Scorecard Template

```markdown
## AI Visibility Scorecard

**Period:** [dates and time zone]
**Baseline:** [date, method, and site-specific baseline]
**Target:** [owner-approved target and review date]
**Coverage:** [completed / failed / partial / blocked samples]

| Evidence class | Numerator | Eligible denominator | Rate or count | Source and limitation |
|---|---:|---:|---:|---|
| Mentions | [n] | [n] | [rate] | saved responses |
| Recommendations | [n] | [n] | [rate] | saved responses and coding |
| Citations | [n] | [n] | [rate] | saved source attributions |
| Verified access | [n] | [n] | [count/rate] | server/CDN logs |
| Click referrals | [n] | [n] | [rate/count] | analytics |
| Survey discovery | [n] | [n] | [rate] | valid survey responses |

### Prompt and sample notes
[Platform/model, prompt IDs, locale, search mode, replicates, failures, coding changes]

### Findings
[Observed changes, repeated observations, site-specific comparison, and limitations]

### Next collection
[Exact repeat date, owner, and unchanged method]
```

## Interpretation Rules

- Compare the same evidence class and scope over time. Do not explain a response-rate change with bot access logs alone.
- Use repeated observations and a site-specific baseline before calling a difference meaningful.
- A citation can be recorded only when the response attributes the source. A page being fetched does not imply citation.
- A click referral records an attributed session, not dark traffic or every AI-influenced visit.
- A survey records a respondent's report, not verified exposure or complete attribution.
- A platform-wide change is a hypothesis unless the same stable sample shows it across comparable entities.
- Do not infer a universal diagnosis from a low rate, and do not trigger an all-page rewrite automatically.
- Report no performance promise. A favorable observation does not prove that a change caused it.

## Review Cadence and Actions

At each review:

1. Re-run the declared sample with the same method.
2. Reconcile completed, failed, partial, and blocked samples.
3. Compare each evidence class with its own baseline and denominator.
4. Review source provenance, bot verification, analytics attribution, and survey bias.
5. Select one bounded follow-up based on an observed gap and a verification method.

Potential follow-ups include clarifying visible factual content, checking a specific fetch policy, or improving measurement provenance. Record the smallest authorized action and its verification result. Do not use universal percentage thresholds as targets or action triggers.
