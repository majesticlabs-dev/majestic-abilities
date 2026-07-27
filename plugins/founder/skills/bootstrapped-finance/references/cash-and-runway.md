# Cash And Runway

Use this reference when calculating runway, burn, working capital, or spend tradeoffs for a bootstrapped company.

## Definitions

| Term | Meaning |
| --- | --- |
| Available cash | Unrestricted cash the company can spend now |
| Restricted cash | Cash that cannot be freely used (tax withholdings, escrow, collateral, earmarked customer funds) |
| Gross burn | Cash operating outflows for the period |
| Net burn | Gross burn − collected operating inflows for the period; an operating metric, not automatically the runway denominator |
| Committed cash outflows | Operating spend plus taxes, debt service, capital expenditures, and other obligations due during the forecast |
| Net cash outflow | Committed cash outflows − all collected cash inflows for the period |
| Forecast period | Explicit window (weeks or months) and as-of date |
| Stable burn | Month-to-month net burn that does not swing enough to change the survival conclusion |

Always state currency and as-of date.

## Core Questions

- How much cash is actually available?
- What fixed obligations are unavoidable in the forecast window?
- How does variable spend change by scenario?
- When does money leave or arrive?
- How long does the business survive without new capital under each scenario?

## Review Discipline

- Separate booked revenue from collected cash.
- Watch customer concentration and collection delays.
- Treat hiring, founder compensation, and vendor commitments as runway choices.
- Revisit assumptions when pricing, churn, demand, or payment terms change.
- If required inputs are missing, request them before concluding.

## Runway Calculation

### Stable positive net cash outflow

```text
runway_months = available_cash / monthly_net_cash_outflow
```

Use only when monthly net cash outflow is positive, relatively stable, and includes every committed obligation due during the forecast. Operating burn alone is insufficient when taxes, debt service, capital expenditures, or other mandatory outflows are material.

### Lumpy, seasonal, or near break-even cash

Build a month-by-month cash schedule:

```text
ending_cash[m] = ending_cash[m-1] + collected_inflows[m] - outflows[m]
```

Report:

- first month ending cash would go negative (if any)
- minimum cash point and when it occurs
- key timing drivers (payroll, tax, large receivables, annual renewals)

### No finite runway

State that there is no finite runway only when durable collected inflows cover all committed cash outflows and no known lumpy obligation creates a future deficit. Still show downside sensitivity.

## Unit Economics

Branch by business model. Do not force SaaS formulas onto services, commerce, or other models.

### When subscription metrics apply

Define each input's period before computing:

```text
LTV = ARPA × gross_margin × (1 / periodic_churn)
CAC = (sales + marketing spend) / new_customers_acquired
Payback periods = CAC / (ARPA × gross_margin)
```

- ARPA, churn, and spend must share a consistent period.
- If churn ≤ 0, LTV via `1 / churn` is not meaningful; say so and use cohort or retention evidence instead.
- If new customers acquired = 0, CAC is not meaningful.
- Net new ARR and burn multiple apply only when ARR is a defined, supplied metric for this business.

### Services / project businesses

Prefer contribution margin per engagement, utilization, collection lag, and cash conversion over ARR or churn constructs.

### Commerce / inventory businesses

Prefer gross margin after returns, inventory days, payables days, and cash conversion over SaaS retention metrics.

### Optional context only

External benchmarks (LTV:CAC bands, Rule of 40, RPE bands, departmental spend ratios) are optional context. Use them only when sourced, dated, and matched to model and geography. Never treat unsourced thresholds as decision rules.

## Hiring And Tooling Evaluation

For each proposed hire or tool, state:

1. Fully loaded cash cost for the forecast window (do not assume a universal payroll multiplier)
2. Expected time to productivity or benefit
3. What evidence would show the spend is working
4. Reversibility and management load
5. What else the same cash could do
6. Effect on runway under base and downside cases

Reject vague justifications such as "look professional," "everyone has this role," or "we'll figure out impact later."

## Working Capital

Useful constructs when the model warrants them:

```text
cash_conversion_cycle = DSO + days_inventory − DPO
```

Interpret with the company's payment terms and seasonality. Do not impose universal DSO/DPO or annual-prepay targets.

## Scenario Design

Model at least:

| Scenario | Purpose |
| --- | --- |
| Base | Most likely collections and spend |
| Upside | Faster collections or stronger demand with explicit drivers |
| Downside / cash-stress | Delayed collections, higher churn or weaker demand, and sticky costs |

For each scenario list assumptions, missing inputs, and the action triggers if reality tracks that path.

## Decision Prompts For Major Spend

1. What cash returns, risk reduction, or capacity unlock is expected, and by when?
2. What happens if we wait?
3. Can we undo this if wrong?
4. What is the runway impact under base and downside cases?

## Review Cadence

| Cadence | Focus |
| --- | --- |
| Weekly | Cash position, near-term forecast, receivables aging, burn vs plan |
| Monthly | Actual vs plan, model-appropriate unit economics, cohort or margin checks |
| Quarterly | Scenario refresh, runway recalculation, hiring and vendor commitments |

## Anti-Patterns

| Pattern | Problem | Fix |
| --- | --- | --- |
| Single flattering forecast | Hides timing risk | Show base and downside with cash timing |
| Booked revenue as cash | Overstates survival | Use collections |
| Operating burn as the runway denominator | Ignores debt service, taxes, capital expenditures, or other commitments | Use total net cash outflow or a month-by-month schedule |
| Universal benchmark rules | Wrong model or market | Use founder numbers; cite benchmarks only as dated context |
| Hiring ahead of demand | Burns runway | Hire behind evidence; prefer reversible capacity |
| Copying venture burn | Different capital model | Size spend to own cash constraints |

## Output Checklist

Every finance answer should include:

- inputs used and inputs missing
- formulas with units and periods
- runway method (ratio vs month-by-month schedule)
- scenario assumptions
- confidence level
- action triggers and escalations (tax, debt covenants, accounting, legal)
