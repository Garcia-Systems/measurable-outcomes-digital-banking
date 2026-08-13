# Chapter 5: Measuring Digital Task Completion

> **Status:** Implemented. All Harbor Federal Credit Union (Harbor FCU) sessions and events in this chapter are fictional and synthetic.

[← Previous chapter](../part-01-foundations/chapter-04-before-after-and-the-limits-of-causality.md) | [Contents](../../CONTENTS.md) | [Next chapter →](chapter-06-task-completion-without-vanity-metrics.md)

## Learning objectives

A technically correct page can receive traffic while preventing a member from finishing a job. This lesson defines the task boundary before counting it. Learners will calculate the chapter metrics, interpret tradeoffs, and state evidence limitations without inventing causality.

## Banking context

A prospective member may arrive at a working application and still fail to accomplish the intended digital task. Harbor FCU therefore observes the journey, not merely whether its software returned a page.

## Engineering concept

The fictional Harbor FCU digital account journey is `session_started → application_viewed → application_started → personal_info_completed → verification_started → verification_completed → review_viewed → application_submitted → confirmation_viewed`. A view is exposure, a click is an interaction, and activity is any event. The task **starts** only at `application_started`; it **completes** at a successful `application_submitted`. Confirmation is useful delivery evidence, but is not the submission itself.

## Measurable-outcome concept

Task completion rate has numerator = distinct sessions with `application_submitted` and denominator = distinct sessions with `application_started`, multiplied by 100. Incomplete sessions are starts minus completions. Sessions describes the whole observed population and is deliberately not the denominator. With no starts, the rate is undefined and the utility raises an error.

Traffic ≠ success. Clicks ≠ completion. Even completion is only a defined workflow outcome—not proof that an account was approved, funded, or valuable.

## Planned Harbor FCU scenario

The shared event schema is `session_id`, `event_type`, UTC `timestamp`, `step`, `result`, and elapsed `duration_ms`. Identifiers such as `session_0001` are not people. The generator is deterministic, and the provenance explicitly excludes real financial, tracking, or personal data.

## Metrics to measure

The lab reports numerator and denominator, percentages, counts, units, population, and relevant exclusions. It reuses nearest-rank `percentile` and Part I `Criterion` evaluation from `src/harbor_fcu/measurement.py` through `src/harbor_fcu/member_experience.py`.

## Implementation

Reusable calculations live in the package; the command is a thin report. Event collections are materialized where repeated passes are required. Empty or undefined populations raise `ValueError` rather than returning a persuasive-looking zero.

## Planned executable exercise

Run `python3 scripts/measure_completion.py`. It loads the committed events and derives session count, starts, completions, rate, and incomplete count; no reported total is embedded in the explanation. Inspect `data/synthetic/part2/application_before.csv`, then change the task boundary mentally and predict which denominator changes.

## What to observe and interpret

Follow the progression `software behavior → digital experience → member behavior → measured outcome → potential organizational impact`. Stop the claim at the last measured link. Page traffic, member happiness, assistance, revenue, and cost are separate measures unless explicitly observed.

## Engineering tradeoffs and evidence limitations

More instrumentation can improve diagnosis but adds event-quality, privacy, accessibility, and maintenance concerns. This small teaching model avoids a production analytics platform. Counts depend on event delivery and definitions; synthetic controlled results may not generalize to real populations. Preserve raw observations and investigate missing, duplicated, or out-of-order events.

## Automated tests

Run `python3 -m unittest tests.test_member_experience -v`. Edge cases cover no starts, empty durations, zero-stage reach, nearest-rank tails, stage timing, comparisons, and success criteria. Run the full suite before drawing conclusions.

## Exercises

1. Why would `application_viewed` overstate starts?
2. If confirmation telemetry fails, can submission still be measured?
3. Name evidence needed to claim successful account opening.

**Answer key:** (1) Viewing expresses exposure, not intent. (2) Yes, under the declared submission definition, while confirmation delivery becomes a guardrail. (3) A linked, synthetic approval/opening outcome with an explicit population and window.

## Expected takeaway

A technically correct application is an output. A defensible member-experience outcome requires a defined task, reproducible observations, multiple metrics, criteria, and claim restraint.

## Chapter summary

Chapter 5 connects observable member-journey behavior to measured outcomes while keeping possible organizational effects explicitly downstream and unproven.
