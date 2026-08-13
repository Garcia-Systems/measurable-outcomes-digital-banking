# Chapter 0: From Code to Outcomes

> **Status:** Implemented. Every Harbor Federal Credit Union (Harbor FCU) observation in this chapter is fictional and synthetic.

## Learning objectives

By the end, you can distinguish engineering activity, deliverable/output, metric, outcome, operational or member effect, and potential business impact; calculate a metric from observations; and keep a claim inside the evidence boundary.

## Banking context

A digital enrollment flow calls a member-verification service. Transient failures can stop an attempt. An engineer changes retry and timeout behavior. That story sounds useful, but usefulness is not yet measured.

```text
Engineering activity
        ↓
System change (output)
        ↓
Observable metric
        ↓
Measured outcome
        ↓
Member / operational effect
        ↓
Potential business impact
```

The arrows are questions, not automatic proof. Each step requires evidence.

## Engineering concept

An **activity** is work performed: investigate failures or modify an integration. A **deliverable/output** is what the work produces: retry handling, a deployment, or tests. Shipping proves the output exists; it does not prove it worked. This distinction prevents teams from treating effort as value.

## Measurable-outcome concept

A **metric** is a defined observation, such as successful requests divided by all eligible requests. An **outcome** is change in that metric from a baseline. An **effect** describes what that change means close to the system. **Impact** is a broader consequence, often requiring additional operational, member, or business evidence.

| Layer | Verification example | What would establish it? |
|---|---|---|
| Activity | Modify the verification integration | Work record |
| Output | New retry and timeout handling | Code/test/deployment evidence |
| Metric | Verification completion rate | Completed / eligible attempts |
| Outcome | Rate rises from baseline | Comparable before/after windows |
| Effect | Fewer attempts end on transient failure | Failure-reason or journey events |
| Potential impact | More members may enroll without help | Enrollment and assistance study |

Other examples reinforce the boundary:

* Adding an index is activity/output; p95 query latency is a metric; a measured fall in p95 is a technical outcome. Faster transfer screens are plausible until screen timing is measured.
* Adding deployment checks is an output; deployment-failure rate is a delivery metric; fewer failed deployments is an outcome. Lower operating cost is not established without cost measurement.
* Improving an error message is an output; self-service completion is a member-experience metric. Retention remains a possible business impact, not an automatic conclusion.

## Planned Harbor FCU scenario

This implemented scenario introduces the shared, synthetic verification environment. Twenty requests make one fixed measurement window. Eighteen are successful.

## Metrics to measure

**Verification success rate** = successful verification requests / all eligible verification requests × 100. The numerator is 18, denominator 20, unit percent, and scope is the committed baseline window. Empty windows are rejected rather than reported as a misleading zero.

## Implementation

`src/harbor_fcu/measurement.py` owns reusable loading and calculations. Data and provenance live under `data/synthetic/part1`; scripts remain thin. Later chapters reuse the same observations rather than inventing disconnected programs.

## Planned executable exercise

This is now an executable laboratory. From the repository root run:

```bash
python3 scripts/introduce_measurement.py
```

Expected deterministic core result: `Verification success rate: 90.0%`. Inspect the CSV and identify numerator and denominator. The command computes the answer; the prose does not substitute for data.

## What to observe and interpret

Observed: 18 of 20 requests succeeded, a 90.0% rate. Supported: the measured window had that rate. Not supported: a code change caused it, real members were happier, or revenue changed. There is no “after” window yet.

## Engineering tradeoffs and evidence limitations

A tiny deterministic sample teaches reproducibility, not production inference. Retries could increase completion while increasing latency and dependency load. A later experiment needs guardrails. Synthetic data demonstrates technique and makes no claim about any real credit union.

## Automated tests

`python3 -m unittest tests.test_measurement -v` checks the calculation and empty-input behavior. The full suite is `python3 -m unittest discover -s tests -v`.

## Exercises

1. Classify “deployed retry logic,” “90% success rate,” and “success rose four percentage points.”
2. If success rises, may you claim digital adoption rose? What would you measure?
3. Write one supported statement and one explicitly labeled hypothesis.

### Answer key

1. Output, metric, and outcome, respectively (the last requires a comparable baseline).
2. No. Measure eligible member adoption over comparable populations and investigate other changes.
3. Example supported: “Success was 90% in this window.” Hypothesis: “Higher verification success may reduce enrollment interruption.”

## Expected takeaway

A shipped feature is evidence of activity, not evidence of improvement. State observations precisely and label downstream effects as hypotheses until measured.

## Chapter summary

Engineering becomes a measurable intervention when the team defines the observation, measures a baseline and change, and matches every conclusion to its evidence.
