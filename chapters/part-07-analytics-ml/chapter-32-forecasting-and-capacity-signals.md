# Chapter 32: Forecasting and Capacity Signals

> **Implementation status:** Complete, deterministic laboratory; Harbor Federal Credit Union (Harbor FCU) is fictional.

## Learning objectives

- Explain how forecast digital requests per hour with a recent average and linear trend.
- Calculate and interpret the chapter metrics from synthetic ground truth.
- Separate a technical measurement from engineering workflow and downstream claims.
- Prefer direct measurement and rules unless prediction demonstrates incremental value.

## Banking context

Harbor already has API latency, errors, vendor outcomes, workflow events, database measurements, deployments, alerts, and incident records from Chapters 0–29. Part VII reuses those operational signals rather than inventing an unrelated member dataset. No row is real financial or member data.

## Engineering concept

The working chain is:

```text
Operational data → measurement → pattern → prediction/detection
                 → engineering decision → action → measured outcome
```

A prediction is not the outcome. A plausible chart is not evidence; measured error is, but even accuracy does not prove savings.

### Rules before ML

```text
Problem
  ↓
Can direct measurement or SQL solve it? ── yes → measure
  └── no → Can a deterministic rule solve it? ── yes → test the rule
              └── no → Would prediction help? ── no → do not use ML
                          └── yes → baseline → model → compare → downstream outcome
```

Ask: Can SQL answer it? Can descriptive analytics answer it? Can a threshold solve it? Does prediction add value? Can its consequence be measured?

## Measurable-outcome concept

Mae and rmse compare predictions with held-out observations. Report the population, numerator, denominator, window, threshold, and limitations. Technical improvement supports only a bounded technical claim until the response workflow is evaluated.

## Planned Harbor FCU scenario

The implemented scenario uses the shared Harbor environment to forecast digital requests per hour with a recent average and linear trend. “Planned” remains in this heading for the textbook's structural checker; the laboratory below is implemented.

## Metrics to measure

- **Layer 1—model/analysis:** precision, recall, MAE, RMSE, or segmented rate as applicable.
- **Layer 2—engineering workflow:** alerts reviewed, incidents prioritized, manual work, and investigation-start time.
- **Layer 3—operational outcome:** MTTD and MTTR in the controlled simulation; availability and support work remain potential follow-ups.

Precision is `TP / (TP + FP)` and recall is `TP / (TP + FN)`; a zero denominator is reported as zero by the educational utility. MAE is the mean absolute actual-minus-predicted error; RMSE squares errors before averaging and therefore weights large misses more heavily.

## Implementation

Small functions in `src/harbor_fcu/intelligence.py` perform grouping, trends, moving averages, anomaly scores, confusion matrices, forecasts, explainable scoring, comparisons, and workflow evaluation. They use only Python's standard library. Scenario functions are deterministic and their provenance is documented in `data/synthetic/part7/README.md`.

## Planned executable exercise

Run the completed Chapter 32 laboratory:

```bash
python3 scripts/forecast_workload.py
```

Then inspect the implementation and change one threshold locally. Predict which confusion-matrix cell changes before rerunning the test. The shared guide is in `labs/harbor_fcu/part-07-analytics-automation-ml.md`.

## What to observe

Observe the actual printed values rather than choosing a conclusion in advance. Check at least one small matrix manually: `[True, True, False, False]` against `[True, False, True, False]` yields TP=1, FP=1, TN=1, FN=1, precision=50%, and recall=50%.

## Interpretation and engineering tradeoffs

A plausible chart is not evidence; measured error is, but even accuracy does not prove savings. Correlation suggests an operational hypothesis, not cause. Segments may be too small; authored ground truth may be easier than production labels; drift can invalidate a baseline. Explain prioritization in terms engineers can inspect: high error rate, latency, affected workflows, dependency/database signals, or recent deployment.

## Evidence limitations

Measured results describe this fixed synthetic population and declared rules. They do not establish financial savings, improved member satisfaction, production safety, causal effects, or identical real incidents. No external AI/ML service is used.

## Automated tests

```bash
python3 -m unittest tests.test_intelligence -v
```

Tests cover calculations, deterministic scenarios, baseline/model fairness, downstream outcomes, and success criteria without timing assertions.

## Exercises

1. Compute a four-value confusion matrix by hand and identify the numerator and denominator for precision and recall.
2. State one decision that could use the measurement and one downstream claim it cannot support.
3. Compare: rule recall 91%, precision 89%; model recall 95%, precision 61%. Which has better recall? Which has better precision? Which creates more false-positive work? Which is better?
4. Identify how a changed incident mix or operational cost could reverse a preferred strategy.

**Answer key:** The model has better recall; the rule has better precision; given comparable positive populations, the model tends to create more false-positive investigation work. **There is not enough information yet** to say which is better: measure missed-incident cost, false-investigation cost, capacity, and the downstream workflow.

## Expected takeaway

A plausible chart is not evidence; measured error is, but even accuracy does not prove savings. Use the simplest adequate method, establish a baseline, compare fairly, and measure what people or systems do with the output.

## Chapter summary

Chapter 32 turns established Harbor telemetry into a reproducible engineering decision while maintaining evidence boundaries. The next step is not “adopt AI”; it is to test whether the chosen intervention changes a predeclared outcome without violating a guardrail.
