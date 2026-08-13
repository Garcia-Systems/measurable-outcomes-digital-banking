# Chapter 7: Measuring Friction and Time to Complete

> **Status:** Implemented. All Harbor Federal Credit Union (Harbor FCU) sessions and events in this chapter are fictional and synthetic.


## Learning objectives

Completion can hide effort. Tail timing shows whether a minority waits far longer than the typical completed session. Learners will calculate the chapter metrics, interpret tradeoffs, and state evidence limitations without inventing causality.

## Banking context

A prospective member may arrive at a working application and still fail to accomplish the intended digital task. Harbor FCU therefore observes the journey, not merely whether its software returned a page.

## Engineering concept

Completion duration is submission timestamp minus start timestamp for completed sessions. Median is the midpoint; p95 uses Part I's documented nearest-rank method. `duration_ms` gives time since the previous event, allowing per-step median and p95. Incomplete journeys are excluded from completion-time statistics and must remain visible through completion rate.

## Measurable-outcome concept

An average can be pulled by extremes and does not describe the tail. Report median and p95 together, plus population and method. A long event interval may include thinking, interruption, network delay, retry, or instrumentation error: timing identifies friction, not cause. Faster ≠ automatically better if errors or abandonment worsen.

## Planned Harbor FCU scenario

The shared event schema is `session_id`, `event_type`, UTC `timestamp`, `step`, `result`, and elapsed `duration_ms`. Identifiers such as `session_0001` are not people. The generator is deterministic, and the provenance explicitly excludes real financial, tracking, or personal data.

## Metrics to measure

The lab reports numerator and denominator, percentages, counts, units, population, and relevant exclusions. It reuses nearest-rank `percentile` and Part I `Criterion` evaluation from `src/harbor_fcu/measurement.py` through `src/harbor_fcu/member_experience.py`.

## Implementation

Reusable calculations live in the package; the command is a thin report. Event collections are materialized where repeated passes are required. Empty or undefined populations raise `ValueError` rather than returning a persuasive-looking zero.

## Planned executable exercise

Run `python3 scripts/analyze_completion_time.py`. Compare the median and p95, find sessions at or beyond p95, then identify the stage with the highest p95 duration. The synthetic scenario makes one stage disproportionately slow, but the command intentionally does not assert why.

## What to observe and interpret

Follow the progression `software behavior → digital experience → member behavior → measured outcome → potential organizational impact`. Stop the claim at the last measured link. Page traffic, member happiness, assistance, revenue, and cost are separate measures unless explicitly observed.

## Engineering tradeoffs and evidence limitations

More instrumentation can improve diagnosis but adds event-quality, privacy, accessibility, and maintenance concerns. This small teaching model avoids a production analytics platform. Counts depend on event delivery and definitions; synthetic controlled results may not generalize to real populations. Preserve raw observations and investigate missing, duplicated, or out-of-order events.

## Automated tests

Run `python3 -m unittest tests.test_member_experience -v`. Edge cases cover no starts, empty durations, zero-stage reach, nearest-rank tails, stage timing, comparisons, and success criteria. Run the full suite before drawing conclusions.

## Exercises

1. Why might successful-session timing be biased?
2. What guardrails accompany a speed intervention?
3. What evidence distinguishes server delay from member pause?

**Answer key:** (1) Abandoners are excluded. (2) Completion and error rates, correctness, and accessibility. (3) Correlated server spans and client events under a controlled test, while respecting privacy.

## Expected takeaway

A technically correct application is an output. A defensible member-experience outcome requires a defined task, reproducible observations, multiple metrics, criteria, and claim restraint.

## Chapter summary

Chapter 7 connects observable member-journey behavior to measured outcomes while keeping possible organizational effects explicitly downstream and unproven.

[Previous chapter](chapter-06-task-completion-without-vanity-metrics.md) | [Contents](../../CONTENTS.md) | [Next chapter](chapter-08-navigation-experiments-and-responsible-conversion-claims.md)
