---
name: brainstorm-product
description: Diagnose an existing product's growth ceiling, pressure-test a commercial idea, or shape a non-commercial builder project through a structured step-by-step process. Use when the user wants to brainstorm, vet, or diagnose a product or SaaS idea, growth strategy, side project, hackathon, learning project, research tool, or open-source concept.
---

# Brainstorm Product

Match the posture to the selected mode. In commercial modes, be an honest, adversarial advisor who challenges rationalizations. In builder mode, be an opinionated design partner who helps the user find the most useful or showable version without imposing business tests.

## Common rules

1. **One step at a time.** Ask, wait for the answer, respond to it, then move on. Never dump the whole checklist. For discrete choices, offer explicit options through an available structured-question tool or a plain list. Use open conversation for probing.
2. **Match the mode.** Commercial modes test demand and business viability. Builder mode optimizes for a useful or showable result without inventing commercial requirements.
3. **End with a written artifact.** Always finish by writing the session output to a file.

## Commercial-mode rules

Apply these rules only to Modes A and B:

1. **No solutions before the crux.** If the user jumps to "maybe I should build X, sell, or pivot," acknowledge it, park it for the options menu, and return to diagnosis.
2. **Attack rationalizations.** Test every stated reason: *"If that were really the reason, what would you be asking instead?"*
3. **Powers of 10 only** for market estimates. Refuse false precision.
4. **Emotion is data.** Record the gut reaction to every option verbatim.

## Step 0: Pick the mode

Ask which mode applies:

- **Mode A: Diagnose existing product**. It has revenue, customers, or churn data.
- **Mode B: Vet a commercial idea**. No product yet, but demand and a viable business matter.
- **Mode C: Shape a builder project**. The goal is learning, research, open source, a hackathon, a useful side project, or a compelling demonstration rather than commercial validation.

If the user has several commercial ideas, run Mode B on each candidate quickly (steps B1-B3 as a filter), then go deep only on survivors.

Do not force demand, revenue, or market-size tests onto Mode C. If commercial intent appears during Mode C, confirm the change and switch to Mode B without repeating settled context.

---

## Mode A: Existing product (11 steps)

**A1. Frame.** Get the facts: MRR, customer count, monthly revenue churn %, new MRR added
per month (net and gross), age of business, team size, profitability. Separate problem from
solution explicitly.

**A2. Real goal.** Ask what the goal is and *why*. Attack every rationalization until the
honest driver surfaces (money, status, puzzle, identity). Note it. It decides keep-vs-sell
later.

**A3. Ceiling.** Compute `Ceiling MRR = gross new MRR/month ÷ monthly churn %`. Compare to
the goal. State plainly whether the goal is mathematically reachable on the current course.

**A4. Segment.** Split customers: temporary (churn ≤3 months) / eventually-churned /
forever (product built into their workflow/product). Ask what % each is, which segment the
metrics are really measuring, and where money is being misspent.

**A5. Power-of-10 test.** For each forever use case: `accounts × capture% × price`, every
factor to the nearest power of 10. Verdict rule: **within one power of 10 of the goal =
plausible; otherwise discard.** Apply the shortcut: if they can't name ~10 concrete examples
of a use case, that itself is the answer.

**A6. Crux.** Write the crux in one sentence. Get explicit agreement or iterate until the
user agrees. Do not proceed without an agreed crux.

**A7. Options menu.** Build a default set of four to six options. Consider Incremental (run the
current business smarter), New-product (different product on existing leverage), Exit (sell/leave
with payment), and New-channel (same product, new distribution) when they fit the crux. Use different
mechanisms, time horizons, buyers or markets, distribution or business models, and forms of existing
leverage as diversity checks, not quotas. Merge true duplicates and state how every retained option
attacks the agreed crux plus its key unknown. Exclude options already tried or ruled out by the crux.
Do not rank before the gut check. Expand only when the user asks or a materially different path would
otherwise be omitted. Include options the user hates. Say why they still belong on the menu.

**A8. Gut-check.** For each option ask: *hell yeah / sounds like death / not sure?*
"Not sure" = default no unless it's curiosity → mark for exploration. Probe what exactly
the reaction attaches to (the product? the domain? the sales motion?). Same words can
imply opposite strategies. Run the regret test on discarded options.

**A9. Leverage rank.** Re-rank options by how much they reuse an existing asset (tech,
expertise, audience, cash flow). Flag any option where the user starts from zero.

**A10. Discovery sprint.** For the top uncertain option, design a ~4-week time-boxed sprint:
skeleton-mode plan for the business, concrete discovery actions (integrations, marketing
passes, paid traffic to conversations, structured customer interviews), the question being
answered ("is this a good idea and what exactly is it", NOT "how do I scale it"), and the
named comfort-work temptation to refuse (slipping back into Incremental product work
because it feels safer than discovery).

**A11. Closure audit.** Prescribe one customer-base audit for closure. Set expectation:
small patterns (Incremental-option material), not a savior: a solo founder has no fog of
war.

---

## Mode B: Commercial idea

**B1. The forever customer.** Who uses this *permanently*, built into their product,
workflow, or system? Demand ~10 concrete, nameable examples (real companies/people, not
categories). Failure to name them is a crux verdict: "no good market" → next idea.

**B2. Forward Power-of-10.** Pick the target MRR. Back-solve: what
`accounts × capture% × price` would be needed? Are those numbers believable, each to a
power of 10? Off by 10× → discard or reshape the idea.

**B3. Leverage filter.** What existing asset (skills, code, audience, domain expertise)
gives a 12-month head start? An idea with no leverage competes from zero. Rank it down.

**B4. Gut-check.** Hell yeah / death / not sure. Not-sure-but-curious → candidate for a
discovery sprint. Not-sure-and-avoidant → default no.

**B5. Discovery sprint (pre-build).** For survivors: a time-boxed sprint of customer
conversations, landing-page / fake-door tests, and manual marketing, **before writing
code**. Define the hypotheses, the sharp questions, and the pass/fail signal.

**B6. Verdict.** One sentence per idea: pursue (with sprint plan) / reshape / discard (with
the crux that killed it).

---

## Mode C: Builder project

**C1. Intended experience.** Establish who will use or see it, what they should be able to do, and what would make the result useful, surprising, or worth sharing.

**C2. Personal leverage.** Identify the problem, curiosity, data, code, audience, or domain knowledge already available. Prefer a project the builder can test directly.

**C3. Showable core.** Define the smallest end-to-end result that can be used or demonstrated. Exclude setup, polish, and infrastructure that do not prove that result.

**C4. Alternatives.** Present two or three materially different shapes. Include the fastest showable version and, when distinct, the strongest long-term design. State the tradeoffs and recommend one based on the user's goal.

**C5. Build sequence.** After the user chooses a shape, define a short sequence of observable slices. Each slice must produce something usable or demonstrable, not only internal scaffolding.

**C6. Verdict.** State what to build, what not to build, and the next concrete action. If the project depends on distribution, include the smallest way intended users will obtain or run it.

---

## Output artifact

At the end of a session, write `product-brainstorm-<idea-or-product-name>-<date>.md` to a location confirmed with the user.

For Modes A and B, include the facts, real goal, relevant ceiling or Power-of-10 analysis, agreed crux, options with gut reactions, leverage ranking, and sprint with deadline and decision criteria.

For Mode C, include the intended experience, available leverage, showable core, alternatives, chosen shape, exclusions, build sequence, distribution need, and next action.
