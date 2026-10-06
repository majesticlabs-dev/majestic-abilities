# Research Recipes

Use these when paid keyword tools are unavailable or when the topic needs more than SERP scraping.

## SERP Teardown

1. Search the primary query.
2. Capture the top 5-10 organic pages.
3. Note content type, title, angle, freshness, depth, and missing proof.
4. Identify common sections and overused claims.
5. Choose the angle that adds the most useful missing information.

## Competitor Gap

1. List direct competitors and alternatives.
2. Identify their strongest pages on the topic.
3. Map what they explain, what they avoid, and what they cannot credibly claim.
4. Build the piece around the gap your brand can own.

## Buyer-Language Mining

Use forums, Reddit, reviews, sales notes, support tickets, or call transcripts.

Extract:

- exact phrases
- current workaround
- objections
- trigger events
- buying criteria
- risk language

Do not post, comment, or DM externally without approval.

## Internal Search Console Recipe

When Search Console data exists:

1. Find high-impression, low-CTR queries.
2. Find queries ranking positions 8-20.
3. Group by intent.
4. Prioritize pages with business-relevant queries and weak current coverage.

### Optional Question-Query Path

Use this to find one existing page that can better answer a relevant question.

1. Confirm the Search Console property, date range, and current filters. In Performance > Search results, add a Queries filter, choose Custom (regex) and Matches regex, then apply `^(\S+\s+){6,}\S+$`. This finds queries with seven or more whitespace-separated terms. Query length alone does not identify a question or an AI prompt.
2. Sort by impressions. Read the queries and select one question that matches the actual offer and a useful gap in the current content. Do not select a query only because it has high impressions or many words.
3. Select the query row to filter by that query, then open the Pages tab. Inspect the associated URLs and choose one relevant page with weak answer coverage. Most page data is assigned to the canonical URL, so confirm the actual target before proposing an edit. Stop if no suitable page is found.
4. Read the page. Add or improve a question heading only where it serves the reader; preserve natural wording instead of requiring an exact query match. Answer directly in the first two sentences below the heading. Include a relevant number or fact when it helps, using supplied or verified evidence. Do not invent specificity or repeat an answer already on the page.
5. Record the query, target URL, data window, filters, baseline metrics, and fact sources. Check the proposed section against the page's intent and verified facts. After authorized publication, compare the same query/page scope over comparable periods. Measure AI mentions or citations from recorded answer observations, not from the query-length filter.

The seven-term cutoff is an optional discovery heuristic. Search Console omits anonymized queries and some other query rows. Treat the results as partial evidence, and do not promise AI mentions or citations from this edit.

Sources: [Search Console filtering and regex](https://support.google.com/webmasters/answer/17011165?hl=en), [query and page data limits](https://support.google.com/webmasters/answer/17011259?hl=en), and [Google's AI optimization guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).

## AI Answer Gap

Ask what an answer engine would need to cite the brand:

- clear definition
- named framework
- source-backed fact
- specific comparison
- practical workflow
- concise FAQ answer

Then add those elements to the content.
