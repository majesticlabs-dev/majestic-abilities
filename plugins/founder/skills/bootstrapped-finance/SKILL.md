---
name: bootstrapped-finance
description: "Analyze cash runway, burn, unit economics, working capital, hiring ROI, and spending tradeoffs for bootstrapped companies. Use when a founder asks how long cash will last, whether the business can afford a hire or tool, what to cut, whether growth economics are sustainable, or how base, upside, and downside scenarios affect survival."
---

# Bootstrapped Finance

Use this skill when the founder needs a practical view of cash, burn, commitments, and survival choices.

## References

Load [cash-and-runway.md](references/cash-and-runway.md) before calculating runway, unit economics, or spend tradeoffs.

## Required Inputs

Collect before concluding. Mark unknowns explicitly; do not invent figures.

- As-of date and currency
- Available cash vs restricted cash (taxes held, customer prepay reserves, escrow, collateral)
- Operating spend plus taxes, debt service, capital expenditures, and other committed cash outflows for the forecast window
- Receivables aging, payables, and known cash-timing lags
- Business model (SaaS, services, commerce, marketplace, other)
- Forecast horizon and whether burn is stable month to month
- For growth metrics: the period and denominator definitions the founder actually uses

Escalate to a qualified accountant, tax advisor, or counsel for tax filings, debt covenants, audited statements, or legal commitments. Request only necessary aggregates; avoid collecting unnecessary personal or confidential detail.

## Workflow

1. Establish the cash picture: available cash, obligations, variable spend, receivables, debt, and cash timing.
2. Separate operating burn from total cash movement:
   - Gross burn = cash operating outflows for the period
   - Net burn = gross burn − collected operating inflows for the period
   - Net cash outflow = all committed cash outflows due in the period, including operating spend, taxes, debt service, capital expenditures, and other obligations, minus all collected cash inflows
3. Calculate runway from total net cash outflow, not operating burn alone:
   - If monthly net cash outflow is positive, relatively stable, and includes every committed obligation: `runway months = available cash / monthly net cash outflow`
   - If collections or mandatory outflows are seasonal, lumpy, or near break-even: build a month-by-month cash schedule and report the minimum cash point and first month cash would go negative
   - If durable collected inflows cover all committed outflows and no known lumpy obligation creates a future deficit: report no finite runway under stated assumptions
4. Check unit economics and cash timing before recommending growth. Branch metrics by business model; do not apply SaaS ARR, churn, or Rule of 40 metrics to services, commerce, or other models unless the founder supplies equivalent definitions.
5. Identify the few decisions that most affect survival: hiring, pricing, collections, vendor spend, founder compensation.
6. Evaluate hiring and tooling by fully loaded cost, ramp time, reversibility, and management load.
7. Model base, upside, and downside (cash-stress) scenarios with explicit assumptions.
8. Recommend the smallest set of actions that meaningfully improves survival odds, plus trigger points and review cadence.

## Metric Rules

- State units, period, formula, and as-of date for every calculated figure.
- Return "not meaningful" when a denominator is zero or negative.
- Prefer collected cash over booked revenue for survival analysis.
- Treat external benchmarks as optional, sourced, dated context, not decision rules.
- If numbers are missing, ask for them before concluding.

## Standards

- Cash timing matters more than revenue vanity.
- Do not average away seasonality or collection risk.
- Do not hide uncertainty in a single forecast.
- If the business needs fundraising to survive, say that plainly.
- Prefer reversible cost cuts before irreversible commitments.
- Hand off priority and calendar execution to `founder-priorities`, investor-narrative review to `fundraising-ask-review`, pricing and packaging choices to `pricing-strategy`, and focus-metric selection to `north-star-metric`. Own numerical funding gaps, runway, margin, and cash tradeoffs here.

## Output

Return:

1. **Cash snapshot:** available vs restricted cash, currency, as-of date
2. **Runway view:** method used, calculation trace, minimum cash point if scheduled
3. **Scenario table:** base, upside, downside with assumptions
4. **Biggest cash risks:** timing, concentration, obligations
5. **Unit economics:** model-appropriate metrics only; unknowns labeled
6. **Hiring / spend tradeoffs:** fully loaded cost, ramp, reversibility
7. **Actions:** minimal survival-improving moves, triggers, next review cadence
8. **Confidence and escalations:** missing inputs, tax/covenant/legal handoffs
