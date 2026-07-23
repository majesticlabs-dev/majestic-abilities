# Majestic Abilities

Portable agent skills organized by capability category and compatible with the Agent Skills format.

## Install

From this directory:

```sh
# List all available skills
npx skills add . --list

# Select skills interactively
npx skills add .

# Install every available skill
npx skills add . --skill '*'

# Install every SEO skill directly from the category
npx skills add ./skills/seo --skill '*'
```

After this repository is published, replace `.` with its GitHub `owner/repo` identifier. A category can be selected with an `owner/repo/skills/<category>` source path.

## Catalog

| Category | Skills | Path | Status |
| --- | ---: | --- | --- |
| SEO | 22 | [`skills/seo/`](skills/seo/) | Migrated and validated |

## SEO Skills

| Skill | Description |
| --- | --- |
| [`aeo-scorecard`](skills/seo/aeo-scorecard/) | Measure Answer Engine Optimization visibility, share of voice, citations, and referral demand. |
| [`ai-crawler-readiness`](skills/seo/ai-crawler-readiness/) | Configure HTTP-layer signals for LLM discovery, crawling, content negotiation, and referral measurement. |
| [`analyst-positioning`](skills/seo/analyst-positioning/) | Position people as recognizable industry experts with stronger authority and citation signals. |
| [`behavioral-seo`](skills/seo/behavioral-seo/) | Improve behavioral search signals such as click-through rate, dwell time, and engagement. |
| [`bofu-keywords`](skills/seo/bofu-keywords/) | Find and prioritize bottom-of-funnel keywords with strong purchase intent. |
| [`buyer-journey-mapper`](skills/seo/buyer-journey-mapper/) | Map personas and buyer stages into an answer-focused content matrix. |
| [`eeat-analyzer`](skills/seo/eeat-analyzer/) | Audit and improve Experience, Expertise, Authority, and Trust signals. |
| [`entity-triplets`](skills/seo/entity-triplets/) | Build consistent entity relationships that search engines and LLMs can recognize. |
| [`geo-content-optimizer`](skills/seo/geo-content-optimizer/) | Structure content for extraction and citation by ChatGPT, Perplexity, Gemini, and similar systems. |
| [`keyword-research`](skills/seo/keyword-research/) | Discover and prioritize content topics without expensive SEO tools. |
| [`keyword-strategist`](skills/seo/keyword-strategist/) | Analyze keyword usage and suggest semantic variations and related terms. |
| [`llms-txt-builder`](skills/seo/llms-txt-builder/) | Generate an `llms.txt` file that helps AI systems navigate a site. |
| [`meta-optimizer`](skills/seo/meta-optimizer/) | Create optimized meta titles, descriptions, and URL suggestions. |
| [`press-release-aeo`](skills/seo/press-release-aeo/) | Frame press releases for AI citation, authority building, and newswire distribution. |
| [`query-expansion-strategy`](skills/seo/query-expansion-strategy/) | Expand content coverage across LLM sub-questions and semantic query variations. |
| [`review-management`](skills/seo/review-management/) | Improve review presence and use customer-generated content as trust and recommendation signals. |
| [`schema-architect`](skills/seo/schema-architect/) | Create and audit Schema.org JSON-LD for rich results, AI Overviews, and search indexing. |
| [`seo-audit`](skills/seo/seo-audit/) | Audit technical SEO, content quality, E-E-A-T, and AI citation readiness. |
| [`seo-content`](skills/seo/seo-content/) | Produce a search-optimized content asset from opportunity selection through auditing and tracking. |
| [`snippet-hunter`](skills/seo/snippet-hunter/) | Format content for featured snippets and other search-result features. |
| [`structure-architect`](skills/seo/structure-architect/) | Improve headings, content structure, schema markup, and internal linking. |
| [`topical-authority`](skills/seo/topical-authority/) | Plan content clusters, identify coverage gaps, and build measurable topical authority. |

## Layout

```text
skills/
  <category>/
    <skill-name>/
      SKILL.md
      references/  # optional
      scripts/     # optional
      assets/      # optional
```

Each skill is self-contained. Category directories provide catalog organization and category-scoped installation, while installed skills are flattened into each agent's native skill directory.
