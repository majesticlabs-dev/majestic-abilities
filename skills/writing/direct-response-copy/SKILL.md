---
name: direct-response-copy
license: MIT (see LICENSE)
description: Create evidence-safe, conversion-oriented landing pages, sales emails, CTAs, ads, offers, and product microcopy from a reader moment, proof set, offer, and desired action. Use when writing or rewriting a complete commercial asset whose job is to earn a specific response.
---

# Direct Response Copy

Create persuasive copy that makes a truthful offer understandable and gives the right reader a clear next action.

## Boundary

Use this skill for a complete conversion-oriented asset.

- For general informational articles and guides, use a general drafting workflow.
- For a deliberate sprint of editorial headlines or subject-line candidates, use a headline workflow.
- For a report diagnosing existing copy, use an editorial-review workflow.
- For a clarity-only revision that does not reconsider persuasion strategy, use a rewriting workflow.

Persuasion does not permit deception, fabricated proof, hidden material terms, false urgency, or pressure that exploits a vulnerable audience.

## Inputs

Inspect supplied context before asking questions. Resolve:

1. **Reader moment:** Who sees this, what just happened, and what do they need now?
2. **Desired response:** What exact action should the reader take?
3. **Offer:** What is provided, for whom, at what price or commitment, and under what terms?
4. **Evidence:** Product facts, demonstrations, results, quotations, testimonials, limitations, and sources.
5. **Alternative:** What does the reader do today, and what cost or friction is supported by evidence?
6. **Surface:** Landing page, email, ad, CTA, product message, error, empty state, or another format.
7. **Voice and constraints:** Supplied guide, required claims, prohibited claims, legal terms, length, and channel rules.

Ask once, in a concise batch, for missing information that would materially change the copy. Never invent proof, product behavior, numbers, dialogue, testimonials, customer stories, scarcity, or guarantees.

## Delivery Modes

- **New asset:** Build the persuasion strategy and complete copy.
- **Rewrite:** Preserve verified facts and terms while changing structure and emphasis as needed.
- **File edit:** Change only requested prose; preserve metadata, links, code, data, and source notes.
- **Embedded handoff:** Return only the copy needed by the surrounding workflow.

## Workflow

### 1. Define the reader moment and action

Privately answer:

- What is the reader trying to understand, avoid, complete, or decide at this moment?
- What concern or objection must be resolved before the action is reasonable?
- What is the simplest accurate explanation of the offer?
- What is the smallest useful next action?

Judge copy against that moment, not against whether it sounds aggressive or clever.

### 2. Build a proof inventory

Use a table when the asset has several claims:

| Proposed claim | Supplied evidence | Status | Allowed wording |
| --- | --- | --- | --- |
| | | Verified, qualified, unsupported, or prohibited | |

Size every claim to its evidence. If proof is missing, ask for it, qualify the claim, replace it with a demonstrable fact, or omit it.

Testimonials must remain faithful to the supplied wording and permission. Do not turn an ordinary comment into a result claim.

### 3. Map the value

Trace each important feature through supported consequences:

```text
feature -> functional change -> practical consequence -> reader value
```

Stop where evidence stops. Do not invent emotional, financial, or operational outcomes merely because they would be persuasive.

Quantify a problem only from supplied or verified inputs. Show assumptions when a calculation depends on them.

### 4. Choose a structure for the surface

Do not force one funnel onto every asset.

- **Landing page:** clear promise, reader problem, solution, proof, offer and terms, objections, CTA.
- **Sales email:** relevant context, useful claim, proof, offer, one primary action.
- **Ad:** one supported angle, concrete benefit, audience fit, action.
- **CTA:** name the result or next step rather than a generic command.
- **Error:** state what happened, what remains safe, and how to recover.
- **Empty state:** explain the next action and what it enables.
- **Destructive confirmation:** name the exact consequence and whether it is reversible.

Omit sections that do not help the reader decide.

### 5. Draft from specifics

- Put proof before adjectives when the reader is skeptical.
- Prefer concrete objects, actions, constraints, and verified outcomes.
- Explain benefits in the reader's context without pretending to know their feelings.
- Use one primary action per surface unless multiple paths are genuinely required.
- Make price, commitment, limitations, eligibility, and material conditions visible.
- Use urgency or scarcity only when it is true, current, and relevant.
- Disqualify readers only for legitimate fit or safety reasons, not to manufacture exclusivity.

A story is usable only when its facts, attribution, and publication rights are supplied. If no true story is available, use a plain factual angle.

### 6. Validate

Read the copy as a skeptical buyer and verify:

1. The offer and next action are obvious.
2. Each factual claim maps to supplied or verified evidence.
3. Qualifications and material terms are visible.
4. The copy distinguishes benefits from guarantees.
5. The voice fits the reader moment and channel.
6. The CTA accurately describes what happens next.
7. No fabricated proof, testimonial, urgency, or personal story appears.

## Output

Return the complete requested asset, followed by:

- the chosen reader moment and desired response
- material proof used
- unresolved proof or approval gaps
- optional variants only when the request benefits from comparison

For embedded handoff or copy-only requests, return only the finished copy.

## Provenance

The reader-moment intake, proof-first framing, story pressure test, and product-microcopy principles were adapted from `mikiarlo3/ai-copywriter`. The upstream project and MIT license were verified at main commit `201f89a07d7a8d792a11165270591b3684c886a1`. See [LICENSE](LICENSE).

## Quality Gate

The copy is ready when:

- the reader can understand the offer and next action without decoding jargon
- claims are no stronger than their evidence
- proof and material limitations are easy to find
- persuasion serves an informed decision rather than manipulating attention
- the surface follows its real channel constraints
- the asset is complete without requiring another installed skill
