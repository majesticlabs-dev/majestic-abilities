---
name: seo-content
description: "Create one search-led SEO/AEO content asset from keyword or opportunity selection through draft, audit, and ledger update. Use when search intent, keyword strategy, answer-engine optimization, or SEO tracking is central; use content-writer for general articles without a search workflow."
---

# SEO Content Workflow

Create **one** publishable SEO/AEO content asset that answers real search intent, carries information gain, matches brand voice, and can be audited before publication.

Use this when the user asks to write SEO content, choose the next search-led article, turn keyword research into a finished asset, or create a guide, how-to, listicle, or comparison around explicit search intent.

Do not use this for a general article without a keyword, search opportunity, or SEO/AEO workflow. Use `content-writer` instead. Use `keyword-research` when the user only wants a keyword set or opportunity analysis.

---

## Operating Model

One run produces one asset.

Default loop:

```text
FOUNDATION -> OPPORTUNITY -> RESEARCH BRIEF -> OUTLINE -> DRAFT -> POLISH -> AUDIT -> REGISTER
```

If the user gives a keyword, start with that keyword. If the user asks what to publish next, score opportunities first.

---

## Step 0: Check Foundation

Look for a project SEO foundation. If missing, create it from the templates in `assets/` or ask for the smallest missing input.

Recommended project-local files:

```text
.seo/
  brand.md
  content-ledger.md
  link-inventory.md
  keyword-research.json
```

Load these when present:

- `.seo/brand.md` for voice, ICP, proof, anti-positioning, and forbidden claims.
- `.seo/content-ledger.md` to avoid duplicate topics and track shipped assets.
- `.seo/link-inventory.md` to choose internal links before drafting.
- `.seo/keyword-research.json` when keyword data already exists.

Reference: `references/foundation-setup.md`.

---

## Step 1: Select the Opportunity

If the topic is not fixed, score candidate ideas using:

```text
opportunity score = buyer intent + winnability + content gap + internal-link fit + pipeline relevance + freshness urgency
```

Use a 1-5 score for each factor. Pick the highest-scoring topic unless there is a clear strategic override.

Reference: `references/opportunity-research.md`.

---

## Step 2: Build the Research Brief

Before drafting, create a brief with:

- primary keyword or query cluster
- search intent and buyer awareness level
- recommended content type
- audience and current workflow
- top competing pages and gaps
- source claims that need citations
- internal links to include
- CTA and conversion job
- AEO targets: questions, snippets, entities, and citation-worthy facts

Reference: `references/research-brief.md`.

---

## Step 3: Choose the Content Type

Pick the format that matches intent, not the format the agent prefers.

Common types:

- guide
- how-to
- listicle
- comparison
- definition
- data study
- template/resource library
- opinion or point-of-view article
- case study

Reference: `references/content-types.md`.

---

## Step 4: Draft

Write from the brief, not from generic SEO memory.

Rules:

- Answer the query in the first 2-3 sentences.
- Put the useful answer before the throat-clearing.
- Use specific examples, numbers, names, tools, and constraints only when supplied or verified. Label hypothetical examples explicitly.
- Explain the current workaround and why it persists when the topic involves buyer workflow, using supplied or verified evidence.
- Support factual claims with sources. Mark experience-based claims only when the experience and attribution were supplied by the user or an approved source.
- Never invent first-person experience, expertise, authorial opinions, examples, results, or specificity.
- Include internal links from the link inventory and authoritative external sources.

Reference: `references/writing.md`.

---

## Step 5: Polish and Humanize

Run the polish pass before optimization. Remove generic AI tells, tighten the argument, and preserve brand voice.

Use `prose-reviser` when available if the draft needs a dedicated clarity and naturalness revision. Treat it as an optional handoff, not a dependency.

Reference: `references/polish-pass.md`.

---

## Step 6: Optimize for SEO and AEO

Optimize for Google and answer engines:

- title, H1, URL slug, and meta description
- header hierarchy
- featured-snippet answer blocks
- FAQ section when search demand supports it
- entity clarity and citation-worthy source blocks
- schema notes when appropriate

Reference: `references/aeo.md`.

---

## Step 7: Run Quality Loop and Deterministic Checks

Use the quality loop first, then scripts where available.

Recommended checks:

Resolve the skill directory from this `SKILL.md`. From that directory, run:

```bash
python3 scripts/word_count.py <draft.md> --type guide
python3 scripts/link_audit.py <draft.md>
python3 scripts/tech_audit.py <draft.md> --keyword "primary keyword"
```

References:

- `references/quality-loop.md`
- `references/output-formats.md`

---

## Step 8: Register the Asset

After finalizing, update `.seo/content-ledger.md` with:

- title
- URL or draft path
- primary keyword
- intent
- CTA
- internal links used
- publication status
- date
- follow-up measurement notes

If no ledger exists, use `assets/content-ledger-template.md`.

---

## Output Contract

Return:

1. final content or path to the content artifact
2. title and meta description
3. target keyword/query cluster
4. content type and intent
5. internal/external links included
6. quality/audit results
7. ledger update status or blocker

Do not claim the content is published unless a real CMS, repo, or publishing artifact was updated and verified.
