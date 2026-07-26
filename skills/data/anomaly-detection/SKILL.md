---
name: anomaly-detection
description: Design and evaluate anomaly detection for tabular, multivariate, or time-series data using context-appropriate statistical or model-based methods. Use when identifying unusual records, monitoring metric deviations, tuning alert thresholds, or investigating suspected outliers.
---

# Anomaly Detection

Detect observations that are unusual relative to a defined baseline. An anomaly is a review signal, not automatically an error, fraud event, or value to delete.

## Boundary

Use `data-quality` for ongoing service levels, scorecards, drift ownership, and incident response. Use `data-validation` for deterministic contract enforcement. This skill flags context-relative unusual observations rather than contract violations.

## Inputs

Establish:

1. Entity, metric, and grain being monitored.
2. Why anomalies matter and what action follows a flag.
3. Time range, seasonality, and known regime changes.
4. Available labels or previously investigated incidents.
5. Acceptable false-positive and false-negative costs.
6. Missing-value and data-quality behavior.

Do not choose a method before defining the operational decision.

## Workflow

### 1. Validate the data boundary

Check:

- units and transformations
- duplicate records
- missing and default values
- timestamp ordering and timezone
- known source or schema changes
- leakage from future information

Do not fill missing values with zero unless zero is the documented semantic value.

### 2. Choose a baseline

Select a comparison population that matches the question:

- global historical distribution
- peer group
- rolling historical window
- seasonal position
- forecast residual
- multivariate neighborhood

Segment before detecting when populations have structurally different behavior.

### 3. Select the smallest suitable method

| Situation | Candidate method | Main caution |
| --- | --- | --- |
| Approximately stable symmetric distribution | Z-score | Mean and standard deviation are outlier-sensitive |
| Skewed univariate distribution | IQR or quantile bounds | Weak for context-dependent anomalies |
| Robust univariate baseline | Median absolute deviation | Degenerate when MAD is zero |
| Trending series | Rolling residual or forecast residual | Window choice and leakage |
| Seasonal series | Seasonal decomposition residual | Correct period and enough history |
| Multivariate records | Isolation Forest or robust distance | Scaling, missingness, and contamination assumptions |
| Local-density differences | Local Outlier Factor | Expensive and sensitive to neighborhood size |

Start with an interpretable baseline. Add model complexity only when it measurably improves the operational outcome.

### 4. Calibrate thresholds

Use historical backtesting, reviewed incidents, or a labeled validation set. Report:

- number and rate of flags
- precision and recall when labels exist
- alert volume by segment and period
- detection delay
- stability across normal periods

Do not select a threshold solely because a textbook labels three standard deviations as anomalous.

### 5. Explain each flag

Return enough context to investigate:

- observed value
- expected baseline or interval
- deviation magnitude
- method and threshold
- peer or historical comparison
- contributing dimensions for multivariate methods
- nearby data-quality or schema events

If several methods are combined, method agreement is supporting context, not proof of correctness.

### 6. Separate anomaly types

Classify flags where possible:

- data-quality defect
- expected business event
- novel but valid behavior
- model or baseline failure
- unresolved anomaly

Do not mutate or remove records until the classification policy permits it.

### 7. Design monitoring

Define:

- baseline refresh cadence
- threshold ownership
- alert routing and deduplication
- suppression for known events
- feedback capture
- drift and regime-change detection
- rollback when a model floods alerts

## Output

```markdown
# Anomaly Detection Report

## Decision and Baseline
- Entity and grain: ...
- Action after detection: ...
- Baseline: ...

## Method
- Method and rationale: ...
- Threshold and calibration evidence: ...
- Known limitations: ...

## Results
| Record or period | Observed | Expected | Deviation | Explanation | Classification |
| --- | ---: | ---: | ---: | --- | --- |

## Evaluation
- Flag rate: ...
- Detection delay: ...
- Precision and recall: ... or unknown

## Monitoring Plan
- ...
```

## Quality Gate

- The baseline matches the population and time context.
- Missing values and regime changes are handled explicitly.
- Thresholds are calibrated to action costs.
- Flags include explanations and are not treated as automatic errors.
- Backtesting avoids future leakage.
- Monitoring includes feedback and alert-volume controls.
