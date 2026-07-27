# SEO Content Reference Index

This file stays as a compatibility entry point for agents that already know to load `references/detailed-reference.md`.

Use the focused references instead of treating this file as the whole playbook.

## Foundation

- `foundation-setup.md` for `.seo/` setup and required project-local state.
- `opportunity-research.md` for selecting the next topic.
- `research-brief.md` for the pre-draft brief.

## Drafting

- `content-types.md` for guide, how-to, comparison, definition, listicle, data study, resource, opinion, and case-study structures.
- `writing.md` for the writing rules.
- `polish-pass.md` for argument, information gain, naturalness, voice, and compression.

## Optimization and Review

- `aeo.md` for answer-engine and GEO structure.
- `quality-loop.md` for delivery blockers and review lenses.
- `output-formats.md` for final artifact, brief, audit, and ledger output.
- `research-recipes.md` for fallback research methods when paid tools are unavailable.

## Deterministic Checks

Resolve the skill directory from its `SKILL.md`. From that directory, run:

```bash
python3 scripts/word_count.py <draft.md> --type guide
python3 scripts/link_audit.py <draft.md>
python3 scripts/tech_audit.py <draft.md> --keyword "primary keyword"
```
