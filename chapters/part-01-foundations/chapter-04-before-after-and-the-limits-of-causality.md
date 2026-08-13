# Chapter 4: Before-and-After Measurement

> **Status:** Implemented. This chapter brings Part I together with a controlled, entirely synthetic Harbor FCU experiment.

## Learning objectives

Design a before/after comparison; calculate absolute and percentage change; distinguish improvement from regression; identify confounders; separate correlation from causation; and write a bounded outcome statement.

## Banking context

The fictional verification team has a baseline and a hypothesis: revised timeout and retry behavior will improve reliability and tail latency under the controlled workload without violating guardrails. It runs a new measurement rather than declaring success when code ships.

## Engineering concept

```text
Baseline
   ↓
Hypothesis
   ↓
Engineering intervention
   ↓
New measurement
   ↓
Comparison
   ↓
Outcome statement
```

Before and after must use the same metric definitions, instrumentation, percentile method, workload, and relevant conditions. Otherwise the intervention is only one possible explanation.

## Measurable-outcome concept

**Absolute change** is `after − baseline`. Success rising from 90% to 100% is `+10 percentage points`, not “+10 percent.” **Relative change** is `(after − baseline) / baseline × 100`, here `+11.11%`. State the denominator.

For a lower-is-better metric, raw latency change is negative: 1,250 to 760 ms is `−490 ms` or `−39.2%`. Calling that a **39.2% improvement** reverses the sign to express beneficial direction. Always name the convention.

An increase is not inherently improvement: error rate increasing is regression. Direction depends on the metric and declared objective.

## Planned Harbor FCU scenario

The preserved baseline and reliable-candidate windows each contain 20 synthetic requests for the same operation and controlled workload. Baseline success is 90%, after success is 100%; baseline p95 is 1,250 ms, after p95 is 760 ms.

## Metrics to measure

Success rate, p95 latency, absolute difference, relative change, and target result. The structured report uses stable fields—metric, baseline, after, absolute/relative change, target, result—so later chapters can extend it without building an analytics platform.

## Implementation

`compare` retains raw mathematical direction and rejects a zero baseline because relative change would be undefined. `percentage_improvement` requires the caller to declare whether lower is better. Criteria remain separate, so comparison and judgment are both inspectable.

## Planned executable exercise

```bash
python3 scripts/run_experiment.py
```

The report deterministically shows success `90.0% → 100.0%`, `+10.0 percentage points`, `+11.11%` relative change, target `PASS`, and p95 `1250 ms → 760 ms`, a 39.2% improvement.

## What to observe and interpret

A defensible outcome statement is:

> Under the controlled synthetic workload, verification success increased from 90.0% to 100.0%, while p95 latency decreased from 1,250 ms to 760 ms.

The observations support that the measured candidate behaved better in this scenario. They do not establish adoption, satisfaction, retention, operating cost, or revenue.

## Comparable conditions and confounders

A **confounder** changes alongside the intervention and offers another explanation: lighter traffic, a healthier dependency, warmed caches, altered eligibility, device mix, or instrumentation changes. Segment results, repeat windows, randomize or control the intervention when feasible, and document concurrent changes.

Correlation means two changes occur together. Causation means the intervention produced the outcome. A controlled replay strengthens attribution for technical behavior, but this before/after design still does not prove downstream member or business causality. Stronger designs can include concurrent controls, randomized rollout, interrupted time series, and repeated matched observations.

## Engineering tradeoffs and evidence limitations

Control improves internal validity but may reduce realism. Production observation improves realism but admits more confounders. Percentages can exaggerate small samples, so always report counts and absolute values. Avoid “the change increased revenue” unless a suitable business measurement and causal design support it.

## Automated tests

Run:

```bash
python3 -m unittest tests.test_measurement tests.test_part1_scenarios tests.test_cli_labs -v
```

Tests cover rates, nearest-rank percentiles, comparisons, thresholds, both scenarios, and deterministic command output.

## Exercises

1. Traffic was halved after release. Is lower latency attributable to code alone?
2. Write the absolute and relative changes from 94% to 98%.
3. Select the supported claim: (a) revenue increased; (b) the API became faster under the measured workload; (c) every member's workflow became faster.
4. What would strengthen a member-completion claim?

### Answer key

1. No; traffic is a confounder. Match load, segment by load, or use a concurrent/control replay.
2. `+4 percentage points`; `4 / 94 × 100 = +4.26%` relative.
3. (b). Claims (a) and (c) exceed the observation.
4. Link eligible journey events to the service, measure completion before/after under comparable populations, add controls or a randomized rollout, and check guardrails.

## Expected takeaway

A measured technical improvement is valuable evidence, but it is not permission to skip the causal steps between system behavior, member effect, and business impact.

## Chapter summary

Part I's method is: document the baseline, choose a meaningful metric, predeclare complete criteria, run a comparable experiment, calculate change, and communicate no more than the evidence supports.

## Part transition

Part I established the measurement vocabulary and evidence rules. Part II now applies them to what synthetic members can observe while completing a digital task.

[Previous chapter](chapter-03-targets-thresholds-and-success-criteria.md) | [Contents](../../CONTENTS.md) | [Next chapter](../part-02-member-experience/chapter-05-mapping-the-digital-member-journey.md)
