# AI Bot Taxonomy

Use this reference when auditing `robots.txt` for AI visibility.

Provider bot names and policies change. Verify current operator documentation before deploying a live policy change.

## Operator Documentation

- OpenAI bot docs: `https://platform.openai.com/docs/bots`
- Anthropic crawler docs: search Anthropic support or docs for `ClaudeBot`, `Claude-User`, and `Claude-SearchBot`
- Google crawler docs: `https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers`
- Google-Extended overview: verify through current Google Search Central docs
- Applebot docs: `https://support.apple.com/en-us/119829`
- Perplexity bot docs: `https://docs.perplexity.ai/guides/bots`

## Search And Index Crawlers

Allow these when the site owner wants visibility in search-backed AI products.

| Bot | User-Agent token | Operator | Notes |
|-----|------------------|----------|-------|
| OAI-SearchBot | `OAI-SearchBot` | OpenAI | ChatGPT Search index |
| Claude-SearchBot | `Claude-SearchBot` | Anthropic | Claude Search index |
| PerplexityBot | `PerplexityBot` | Perplexity | Search index and answers |
| Applebot | `Applebot` | Apple | Crawls webpages for Apple search and assistant surfaces |
| Googlebot | `Googlebot` | Google | Classic search and AI Overviews source |
| Bingbot | `Bingbot` | Microsoft | Bing search and Copilot source |

## User-Fetch Agents

Allow these when the site owner wants AI products to fetch URLs that users paste directly.

| Bot | User-Agent token | Operator | Notes |
|-----|------------------|----------|-------|
| ChatGPT-User | `ChatGPT-User` | OpenAI | User-initiated URL fetches |
| Claude-User | `Claude-User` | Anthropic | User-initiated URL fetches |
| Perplexity-User | `Perplexity-User` | Perplexity | User-initiated URL fetches |

## Training And Data-Use Crawlers

Treat these as a separate consent decision. They are not required for search or user-fetch visibility.

| Bot | User-Agent token | Operator | Controls |
|-----|------------------|----------|----------|
| GPTBot | `GPTBot` | OpenAI | Training data collection |
| ClaudeBot | `ClaudeBot` | Anthropic | Training data collection |
| Google-Extended | `Google-Extended` | Google | Gemini data-use control; verify current policy |
| Applebot-Extended | `Applebot-Extended` | Apple | Apple Intelligence data-use control; pair with `Applebot` crawler policy |
| Bytespider | `Bytespider` | ByteDance | Training data collection |
| Meta-ExternalAgent | `Meta-ExternalAgent` | Meta | Training and agent data collection |

## Default Visibility Template

This template allows search and user-fetch agents without opting into training crawlers.

```text
User-agent: OAI-SearchBot
User-agent: Claude-SearchBot
User-agent: PerplexityBot
User-agent: Applebot
User-agent: ChatGPT-User
User-agent: Claude-User
User-agent: Perplexity-User
Allow: /

Sitemap: https://example.com/sitemap.xml
```

## Optional Training Consent Template

Use only when the site owner explicitly wants to permit model training on the content.

```text
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
Allow: /
```

Apple data-use controls are separate from Apple crawling. Keep `Applebot` allowed if Apple search discoverability matters, then choose the `Applebot-Extended` policy separately:

```text
User-agent: Applebot-Extended
Disallow: /
```

## Audit Checklist

- Search and index bots match the site's visibility goal.
- User-fetch agents are not accidentally blocked.
- Training and data-use tokens reflect explicit consent, not generic visibility goals.
- `Applebot` is treated as the crawler; `Applebot-Extended` is not treated as a crawler.
- `Sitemap:` is present.
- Crawl delays are not excessive for allowed crawlers.
- WAF or bot-protection settings do not silently block the bots allowed in `robots.txt`.
