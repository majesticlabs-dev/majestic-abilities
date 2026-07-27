# Foundation Setup

The SEO content skill works best with a small project-local foundation. Do not turn this into a huge content database. The point is enough state to prevent repeated generic work.

## Required When Available

```text
.seo/
  brand.md
  content-ledger.md
  link-inventory.md
```

Optional:

```text
.seo/keyword-research.json
.seo/search-console-notes.md
.seo/competitors.md
```

## Setup Flow

1. Create `.seo/brand.md` from `assets/brand-template.md`.
2. Create `.seo/content-ledger.md` from `assets/content-ledger-template.md`.
3. Create `.seo/link-inventory.md` from `assets/link-inventory-template.md`.
4. If keyword data exists, place it in `.seo/keyword-research.json`.
5. If no keyword data exists, use live search and label estimates as estimates.

## Minimum Brand Inputs

If the user wants speed, collect only:

- ICP
- primary offer
- main alternative
- differentiated proof
- claims that are off-limits
- preferred CTA

## Tooling Notes

Use paid keyword tools only when the user has approved or configured them. Otherwise use search results, competitor pages, and existing site inventory.

## Failure Modes

- No brand foundation: output sounds generic.
- No ledger: agents repeat old topics.
- No link inventory: internal linking becomes random.
- Old keyword data: opportunity scores get fake precision.
