# Chapter 35: Connecting Technical Metrics to Operational Outcomes

> **Implementation status:** Complete deterministic laboratory. Harbor Federal Credit Union (Harbor FCU), its vendors, people, accounts, transactions, and observations are entirely fictional and synthetic.

## Learning objectives

- Connect engineering, technical, downstream, and communication layers without skipping evidence.
- Calculate and interpret this chapter's cross-layer measurements.
- Separate measured facts, derivations, assumptions, estimates, hypotheses, and non-claims.

## Measurable-outcome concept

> Measure as far down the outcome chain as the available evidence allows—and stop when the evidence stops.

```text
ENGINEERING WORK → TECHNICAL MEASUREMENT → SYSTEM OUTCOME
                 → MEMBER / OPERATIONAL OUTCOME → BUSINESS RELEVANCE → COMMUNICATION
```

Technical evidence becomes operational evidence only when both layers are instrumented. A **technical metric** describes a system observation (latency); an **operational metric** describes work (investigation minutes); an **operational outcome** is a measured change in that work (shorter MTTR). The defensible chains are API reliability → workflow reliability → fewer measured failed operations; correlation IDs → faster diagnosis → lower measured MTTR; and regression checks → defects caught before release → fewer *known* escapes. None proves revenue or satisfaction.

The scorecard deliberately preserves integration success, p95 latency, MTTD, MTTR, defect escape, and release success as separate signals. Adding unlike units into an “engineering score” would hide tradeoffs and weighting assumptions.

## Planned Harbor FCU scenario

The planned scaffold is now implemented as a controlled, deterministic Harbor FCU account-opening initiative. It extends the shared simulation and contacts no financial system, vendor, AI service, or network endpoint.

## Metrics to measure

- Baseline, after, absolute change, population, and units for every reported metric.
- Technical and downstream measures appropriate to the chapter.
- Predeclared targets and correctness/critical-error guardrails where evaluated.
- Explicit evidence class for every business statement.

## Planned executable exercise

The completed executable exercise runs from the repository root:

`python3 scripts/operational_scorecard.py`

All values are calculated locally from executable synthetic observations.

## Expected takeaway

Interpret each baseline/after pair in its own unit and ask which link was observed. Integration success and latency are technical; MTTD/MTTR and release outcomes describe operations. The fixed 100-run workflow and initiative observations are synthetic. They support Harbor laboratory conclusions only, not causal production or financial claims.

## Verification and reflection

1. Trace a displayed value to its numerator, denominator, or raw observation.
2. Identify which arrows in the outcome chain were measured and which remain hypotheses.
3. State one supported conclusion and one tempting claim the evidence does not establish.

[Previous chapter](../part-07-analytics-ml/chapter-34-intelligent-alerting-with-human-guardrails.md) | [Contents](../../CONTENTS.md) | [Next chapter](chapter-36-member-experience-adoption-and-causal-restraint.md)
