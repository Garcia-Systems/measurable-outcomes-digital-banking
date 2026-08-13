# Chapter 1: Establishing a Baseline

> **Status:** Implemented using only deterministic, synthetic Harbor FCU observations.

## Learning objectives

Define a baseline and measurement window; explain sample size, representative workload, normal variation, and comparison periods; and reproduce a service baseline from raw observations.

## Banking context

Harbor FCU's fictional verification service feels “slow,” but an adjective is not a starting state. Before changing it, the team records success and latency for a declared workload.

## Engineering concept

A **baseline** is a measured reference state, not a remembered impression. Its **measurement window** states when collection begins and ends. **Sample size** is the eligible observation count. A **representative workload** resembles the traffic, operations, devices, and dependency conditions about which the team wants to speak.

Normal systems vary. A payday peak, cache warm-up, maintenance window, or one large request can shift a metric without code changing. One window cannot characterize **normal variation**. Repeated windows help reveal a range and seasonality. The **comparison period** should match relevant conditions: same operation definition, duration, workload mix, instrumentation, and percentile method.

**Reproducibility** means another learner can use the preserved input, definition, and code and obtain the same result. Version data and calculation logic; record UTC windows and filters.

## Measurable-outcome concept

A credible baseline records:

| Field | This laboratory |
|---|---|
| Question | How does verification behave before intervention? |
| Window | 2026-01-15 12:00–12:19 UTC |
| Population | 20 synthetic `member_verification` requests |
| Success | `successful=true` |
| Latency | request duration in milliseconds |
| Percentile | nearest-rank p50 and p95 |
| Exclusions | none |

Nearest-rank p95 sorts observations and selects rank `ceil(0.95 × n)`. For 20 requests it is the nineteenth value. Mean answers a different question and can hide a slow tail.

## Planned Harbor FCU scenario

The shared baseline contains 18 successful and two failed verification calls. It deliberately includes a latency tail.

## Metrics to measure

Request count; success rate = successful / all requests; error rate = failed / all requests; p50 and p95 latency. Together they describe reliability and typical/tail performance without claiming a member or business impact.

## Implementation

The CSV loader preserves each raw observation. `summarize` performs calculations, while `percentile` implements the repository's nearest-rank convention and rejects empty samples or invalid percentile values.

## Planned executable exercise

Run:

```bash
python3 scripts/measure_baseline.py
```

You should reproducibly see 20 requests, 90.0% success, 10.0% errors, 640 ms p50, and 1,250 ms p95. Change nothing in the CSV while recording this baseline; preservation is what makes later comparison auditable.

## What to observe and interpret

The p95 is much higher than p50, so the tail is slower than the typical request. Supported: “Under this synthetic workload, baseline p95 was 1,250 ms.” Unsupported: “All member verification is slow.” The sample covers one narrow window and no real members.

## Engineering tradeoffs and evidence limitations

Larger and repeated samples improve characterization but cost storage and analysis time. Broad windows can improve coverage yet mix unlike conditions. Narrow windows improve control but weaken generalizability. Do not cherry-pick the easiest comparison window after seeing results.

## Automated tests

Run `python3 -m unittest tests.test_part1_scenarios -v`. It derives expected values from the committed observations. The structural suite also ensures Chapters 5–39 remain present.

## Exercises

1. A weekend after-window is faster than a payday baseline. Name the confounder and a better comparison.
2. Three baseline p95 values are 1,100, 1,250, and 1,480 ms. Why is 1,250 alone incomplete?
3. If one request is observed, can its latency be calculated? Is it representative?

### Answer key

1. Workload/time-period mix; compare like weekdays and load bands or repeat both conditions under a controlled workload.
2. It omits normal between-window variation; report the series/range and collect more matched windows.
3. Yes, but representativeness is unsupported because sample size and workload coverage are inadequate.

## Expected takeaway

Targets and outcomes are interpretable only relative to a documented, reproducible starting state.

## Chapter summary

A baseline needs a window, population, definitions, preserved observations, and comparable conditions—not merely a number copied into a plan.
