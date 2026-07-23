---
name: ai-crawler-readiness
description: "Configure HTTP-layer signals for LLM discovery and citation. Use when auditing robots.txt for AI bots, serving Markdown alternates, adding alternate Link headers, handling Accept: text/markdown, or measuring AI-referrer traffic."
---

# AI Crawler Readiness

**Audience:** Developers configuring websites for AI visibility.
**Goal:** Make content discoverable, fetchable, and measurable through standard HTTP signals instead of content tricks.

**Related skills:**
- `llms-txt-builder` creates the `/llms.txt` navigation file.
- `geo-content-optimizer` improves citation-friendly content framing.
- `schema-architect` handles Google rich results and AI Overviews, not direct LLM citation.

## Scope

This skill covers the HTTP and transport layer. It does not write content, evaluate fact density, or generate `/llms.txt`.

| In scope | Out of scope |
|----------|--------------|
| robots.txt allowlist | Marketing copy |
| `.md` shadow routes | `/llms.txt` file content |
| `<link rel="alternate">` tag | Schema.org JSON-LD |
| HTTP `Link` response header | E-E-A-T strategy |
| `Accept: text/markdown` negotiation | Fact-density rewrites |
| AI-referrer analytics | Backlink building |

## The Six Layers

1. **robots.txt:** explicitly allow the AI crawlers you want to serve.
2. **Markdown shadow routes:** serve a clean `.md` twin beside important HTML pages.
3. **Discovery markup:** advertise the Markdown twin in HTML with `<link rel="alternate">`.
4. **HTTP discovery:** mirror the same hint with a `Link` response header.
5. **Content negotiation:** return Markdown for `Accept: text/markdown`.
6. **Analytics:** log AI bot fetches and AI referrer traffic separately.

Apply the layers in order. If `robots.txt` blocks the relevant crawler, later layers cannot help that crawler.

## Bot Taxonomy

Do not conflate search visibility with training consent. There are three separate decisions:

1. **Search and index crawlers:** drive discoverability in AI search products.
2. **User-fetch agents:** fetch URLs that users paste into AI products.
3. **Training and data-use crawlers:** collect or govern content for model training.

Read `references/bot-taxonomy.md` before editing `robots.txt`. Provider bot names and policies change, so verify the current operator docs when live accuracy matters.

For visibility, start from a search plus user-fetch allowlist. Do not opt into training crawlers unless the site owner has explicitly approved model-training data use.

## Markdown Shadow Routes

Serve a clean Markdown twin for every primary content URL. HTML often includes navigation, consent UI, and scripts; Markdown should expose the content only.

| HTML URL | Markdown URL |
|----------|--------------|
| `/blog/post-slug` | `/blog/post-slug.md` |
| `/docs/guide` | `/docs/guide.md` |
| `/` | `/index.md` |

Implementation patterns:
- Static sites: publish source Markdown beside generated HTML after removing frontmatter and unresolved components.
- Server-rendered apps: route the `.md` extension to a Markdown serializer with no layout or navigation.
- CMS-backed sites: expose the raw content body through a `.md` endpoint and omit sidebars, related posts, and banners.

Markdown payload rules:
- Use `Content-Type: text/markdown; charset=utf-8`.
- Preserve the same heading hierarchy as the HTML page.
- Include a canonical marker such as `<!-- canonical: https://example.com/blog/post-slug -->`.
- Convert internal links to absolute URLs when possible.
- Keep image alt text inline so comprehension does not require fetching images.

## Discovery Signals

Every HTML page with a Markdown twin should advertise it in the HTML head:

```html
<link rel="alternate" type="text/markdown" href="/blog/post-slug.md" />
```

Also add the same relationship as an HTTP response header for clients that do not parse HTML:

```http
Link: </blog/post-slug.md>; rel="alternate"; type="text/markdown"
```

Rules:
- Keep a one-to-one mapping between HTML pages and Markdown twins.
- Use the same absolute or path-relative URL style as the canonical URL.
- If multiple `Link` values exist, combine them according to the platform's header conventions.

## Content Negotiation

When a client sends `Accept: text/markdown`, return the Markdown body for the canonical URL without requiring a redirect.

| Request URL | Accept header | Response |
|-------------|---------------|----------|
| `/blog/post` | `text/html` or absent | HTML, status 200 |
| `/blog/post` | `text/markdown` | Markdown, status 200 |
| `/blog/post.md` | any | Markdown, status 200 |

Cache rules:
- Include `Vary: Accept`.
- Key edge caches on whether the request accepts Markdown.
- Do not serve different factual content by User-Agent. User-Agent sniffing for different content is cloaking.

## Analytics

The reliable success signal is server-side measurement. Track both bot fetches and user referrals.

Log these fields for every `.md`, `/llms.txt`, and `/llms-full.txt` request:
- timestamp
- path
- full `User-Agent`
- `Referer`
- `Accept`
- response status
- response bytes
- client IP when bot verification is needed

Bucket AI referrers by host:
- ChatGPT: `chatgpt.com`, `chat.openai.com`
- Claude: `claude.ai`
- Perplexity: `perplexity.ai`
- Gemini: `gemini.google.com`
- Copilot: `copilot.microsoft.com`
- Phind: `phind.com`
- You.com: `you.com`

Dashboard minimums:
- daily fetch count per bot bucket and path
- daily user-referral count per referrer bucket and path
- top 20 paths by combined AI bot and AI referrer traffic
- 7-day trend per bucket

## Workflow

1. Declare scope: local-code audit or live-site audit.
2. Refresh the bot taxonomy from operator docs when live accuracy matters.
3. Audit `robots.txt` against the intended search, user-fetch, and training decisions.
4. Inventory content URLs that should have Markdown twins.
5. Choose the generation strategy for the site's stack.
6. Add the HTML alternate link.
7. Add the HTTP `Link` response header.
8. Implement `Accept: text/markdown` with `Vary: Accept`.
9. Add structured logging for Markdown and AI navigation endpoints.
10. Build a baseline dashboard before claiming citation lift.
11. Cross-link with `llms-txt-builder`: `/llms.txt` should point to the Markdown URLs.

## Output

```text
AI Crawler Readiness Audit
==========================
Layer 1 robots.txt:     [PASS/FAIL] - N bots allowed, M blocked
Layer 2 .md routes:     [PASS/FAIL] - X/Y content URLs have .md twins
Layer 3 link tag:       [PASS/FAIL] - present on N/M pages
Layer 4 Link header:    [PASS/FAIL] - sample response checked
Layer 5 negotiation:    [PASS/FAIL] - Accept: text/markdown returns 200
Layer 6 analytics:      [PASS/FAIL] - endpoints instrumented Y/N

Priority Fixes:
1. [specific change]
2. [specific change]
3. [specific change]
```

## Caveats

- Major AI providers have not promised to read `/llms.txt`, Markdown alternates, or alternate `Link` headers. Treat them as discoverability hedges.
- Schema.org JSON-LD helps Google search features, but there is no public evidence that current chat LLMs parse JSON-LD when answering.
- Meta AI tags, HTML comments, and dedicated "AI info pages" are unproven. Skip them unless there is measurable demand.
