# Chapter 39: Capstone: The Measurable Outcomes Engineering Review

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

The fictional **Harbor Digital Account Opening Improvement** joins the member workflow, verification API, backend query work, observability, tests, security validation, release controls, and analytics. Success criteria are declared before evaluation: p95 API latency improves at least 20% and query count falls; verification success is at least 95% and MTTR at most 30 minutes; completion gains at least 5 points; security and release checks pass 100%; manual reviews fall; critical errors do not rise and correctness/security does not regress.

The report evaluates six layers: technical performance; reliability; delivery quality; member experience; operational efficiency; and business relevance. Every printed summary is calculated from the executable scenario observations. Assumption-dependent labor value is explicitly separated from measured and derived results.

### Outcome-statement generator

`classify_statement` uses deterministic templates—no generative AI or external service. A directly compared metric and an observed downstream metric are **SUPPORTED**; unmeasured downstream effects are **POTENTIAL**; satisfaction, revenue, retention, and realized savings are **NOT ESTABLISHED**.

### Interview translation

Use **PROBLEM** (what failed), **BASELINE** (how known), **INTERVENTION** (engineering change), **MEASUREMENT** (matched comparison), **OUTCOME** (bounded conclusion), and **BUSINESS RELEVANCE** (why it matters without invented ROI). Instead of “I optimized an integration,” explain that transient failures were measured, bounded retries/failure normalization were introduced, and eventual success improved within latency/request guardrails.

Harbor results are **simulated laboratory evidence**, never professional employment achievements. A learner may describe what the exercise taught and separately use authentic evidence from real professional experience; they must not claim fictional results as their own work history.

### Cumulative measurable-outcomes map

```text
CODE / SYSTEM (queries, tests, latency, errors)
  ↓ [relationship needs evidence]
RELIABILITY / PERFORMANCE (availability, MTTD, MTTR)
  ↓ [relationship needs evidence]
MEMBER EXPERIENCE (completion, abandonment, time)
  ↓ [relationship needs evidence]
OPERATIONS (manual review, support, engineering effort)
  ↓ [relationship needs evidence]
BUSINESS RELEVANCE (cost, risk, adoption, value)
```

Every arrow is a hypothesis until instrumentation supplies the connection. Measure as far down the chain as evidence allows—and stop when evidence stops.

### Final synthesis

A full-stack engineer delivering measurable outcomes can: (1) identify the desired outcome, (2) choose a meaningful metric, (3) establish a baseline, (4) define success criteria, (5) instrument the system, (6) implement the change, (7) measure afterward, (8) compare, (9) evaluate guardrails/tradeoffs, and (10) communicate only supported claims.

```text
DEFINE → MEASURE → BUILD → OBSERVE → COMPARE → LEARN → IMPROVE → COMMUNICATE
```

## Planned Harbor FCU scenario

The planned scaffold is now implemented as a controlled, deterministic Harbor FCU account-opening initiative. It extends the shared simulation and contacts no financial system, vendor, AI service, or network endpoint.

## Metrics to measure

- Baseline, after, absolute change, population, and units for every reported metric.
- Technical and downstream measures appropriate to the chapter.
- Predeclared targets and correctness/critical-error guardrails where evaluated.
- Explicit evidence class for every business statement.

## Planned executable exercise

The completed executable exercise runs from the repository root:

`python3 scripts/run_capstone.py`

All values are calculated locally from executable synthetic observations.

## Expected takeaway

Audit each report section back to `src/harbor_fcu/outcomes.py`. Passing criteria mean this declared laboratory initiative met its synthetic targets—not that production ROI, causality outside the control, member happiness, revenue, or retention was proven.

## Verification and reflection

1. Trace a displayed value to its numerator, denominator, or raw observation.
2. Identify which arrows in the outcome chain were measured and which remain hypotheses.
3. State one supported conclusion and one tempting claim the evidence does not establish.

[Previous chapter](chapter-38-dashboards-and-engineering-outcome-reports.md) | [Contents](../../CONTENTS.md)
