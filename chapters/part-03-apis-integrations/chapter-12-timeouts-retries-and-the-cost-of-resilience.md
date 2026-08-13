# Chapter 12: Timeouts, Retries, and Recoverability

> **Implemented:** This chapter uses only deterministic, synthetic behavior for the fictional Harbor Federal Credit Union (Harbor FCU).

## Learning objectives

- Explain the integration behavior represented by each normalized observation.
- Calculate and interpret initial and eventual success, retries, requests per operation, total latency, and retry exhaustion.
- Bound conclusions to evidence gathered by the laboratory.

## Prerequisites and banking context

Chapters 0–4 supplied baselines, targets, comparisons, and evidence discipline. Chapters 5–9 connected technical signals to member workflows. Here the action passes through a Harbor application and adapter to a fictional external dependency; a vendor response either permits the workflow to continue or produces an observable failure. No laboratory performs a network call.

## Measurable-outcome concept

The scenario measures **bounded ClearVerify retries and a NorthstarPay transfer demonstration**. Bounded retries may improve eventual success while increasing latency and request volume; state-changing retries require idempotency.

Harbor normalizes vendor-specific representations into `SUCCESS`, `TIMEOUT`, `TRANSIENT_ERROR`, `PERMANENT_ERROR`, `INVALID_RESPONSE`, or `BUSINESS_REJECTION`. A SOAP fault and REST status can therefore express the same operational meaning. If important behavior is not observable, it is difficult to improve systematically.

## Architecture and implementation

```text
Member action → Harbor application → Harbor-owned adapter → fictional vendor
              ← normalized observation (vendor, operation, attempt, category, duration)
              → workflow result → technical and workflow measurements
```

Reusable records, adapters, retry policy, and the NorthstarPay idempotency simulator live in `src/harbor_fcu/integrations.py`; calculations live in `src/harbor_fcu/integration_metrics.py`. The telemetry answers which dependency and operation ran, duration, outcome category, attempt number, and eventual result after grouping by operation ID. Timestamps are fixed UTC teaching values.

## Planned Harbor FCU scenario

This formerly planned scope is now implemented as bounded ClearVerify retries and a NorthstarPay transfer demonstration. All vendors, operations, observations, members, and metrics are fictional and synthetic.

## Metrics to measure

- initial and eventual success, retries, requests per operation, total latency, and retry exhaustion.
- Numerators and denominators use the displayed synthetic request or distinct-operation population.
- Percentiles use the repository-standard nearest-rank method.

## Executable laboratory

Run from the repository root:

```bash
python3 scripts/simulate_retries.py
```

Inspect the small deterministic workload, rerun it, and change one scenario or threshold. The output remains human-readable so the calculation can be challenged rather than treated as a dashboard oracle.

## Planned executable exercise

The planned exercise is fulfilled by `scripts/simulate_retries.py` and its reusable implementation. No real REST, SOAP, payment, identity, or core service is contacted.

## What to observe and interpretation

Observe the population, categories, tail values, attempt counts, and operation-level result. Distinguish an individual request from eventual workflow completion. Compare the result with the declared criterion rather than selecting a favorable metric afterward.

A supported claim describes the integration under this simulated workload. A downstream workflow benefit is a hypothesis unless corresponding journey events were joined and evaluated. Satisfaction, production availability, abandonment, revenue, and vendor-wide performance are outside this experiment.

## Engineering tradeoffs

Normalization improves consistency but must preserve actionable meaning. Retries consume time and vendor capacity; timeouts leave ambiguous state; permanent and business failures should not be retried. Percentiles require enough observations, and synthetic determinism improves teaching and regression testing but cannot reproduce production distributions.

## Automated tests

```bash
python3 -m unittest tests.test_integrations -v
python3 -m unittest discover -s tests -v
```

Tests cover normalization, REST/SOAP adapters, nearest-rank tails, retry success and exhaustion, permanent-failure safety, operation metrics, idempotency, and experiment criteria.

## Exercises

1. Find an HTTP 200 observation that is not a successful business operation and explain why.
2. Add a transient scenario and predict request volume and eventual success before running it.
3. State one supported conclusion, one potential downstream effect, and one claim requiring additional evidence.
4. Explain why retrying a timed-out $100 transfer without a stable idempotency key can duplicate state.

## Expected takeaway

Bounded retries may improve eventual success while increasing latency and request volume; state-changing retries require idempotency.

## Chapter summary

An integration is not successful merely because a call returned. Harbor measures normalized reliability, tail latency, recoverability, request cost, safety, and the workflow result—and restricts its claims to those observations.

[Previous chapter](chapter-11-soap-integrations-measuring-contract-reliability.md) | [Contents](../../CONTENTS.md) | [Next chapter](chapter-13-dependency-failures-and-graceful-degradation.md)
