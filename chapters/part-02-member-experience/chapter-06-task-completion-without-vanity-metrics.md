# Chapter 6: Funnels and Abandonment

> **Status:** Implemented. All Harbor Federal Credit Union (Harbor FCU) sessions and events in this chapter are fictional and synthetic.


## Learning objectives

A funnel turns the journey into ordered reach counts and makes loss between observable stages visible. Learners will calculate the chapter metrics, interpret tradeoffs, and state evidence limitations without inventing causality.

## Banking context

A prospective member may arrive at a working application and still fail to accomplish the intended digital task. Harbor FCU therefore observes the journey, not merely whether its software returned a page.

## Engineering concept

The laboratory counts each session at most once per stage. Stage conversion is current-stage reach divided by prior-stage reach. Stage abandonment is `100% − stage conversion`. Overall conversion uses submitted divided by viewed. The largest absolute difference between adjacent counts is the largest measurable drop-off.

## Measurable-outcome concept

A funnel assumes ordered, meaningful stages and consistent instrumentation. It can locate loss before identity verification, but it cannot say whether the cause was confusing copy, eligibility, interruption, accessibility, latency, privacy concern, or an event defect. **Abandonment location ≠ abandonment cause.** Add usability research, error logs, performance segmentation, accessibility review, surveys, and a controlled experiment before explaining why.

## Planned Harbor FCU scenario

The shared event schema is `session_id`, `event_type`, UTC `timestamp`, `step`, `result`, and elapsed `duration_ms`. Identifiers such as `session_0001` are not people. The generator is deterministic, and the provenance explicitly excludes real financial, tracking, or personal data.

## Metrics to measure

The lab reports numerator and denominator, percentages, counts, units, population, and relevant exclusions. It reuses nearest-rank `percentile` and Part I `Criterion` evaluation from `src/harbor_fcu/measurement.py` through `src/harbor_fcu/member_experience.py`.

## Implementation

Reusable calculations live in the package; the command is a thin report. Event collections are materialized where repeated passes are required. Empty or undefined populations raise `ValueError` rather than returning a persuasive-looking zero.

## Planned executable exercise

Run `python3 scripts/analyze_funnel.py`. The ASCII bars normalize stage reach to viewed sessions. Verify one row manually from distinct session IDs and calculate its adjacent conversion. The script reports the largest absolute drop, its rate, and overall conversion.

## What to observe and interpret

Follow the progression `software behavior → digital experience → member behavior → measured outcome → potential organizational impact`. Stop the claim at the last measured link. Page traffic, member happiness, assistance, revenue, and cost are separate measures unless explicitly observed.

## Engineering tradeoffs and evidence limitations

More instrumentation can improve diagnosis but adds event-quality, privacy, accessibility, and maintenance concerns. This small teaching model avoids a production analytics platform. Counts depend on event delivery and definitions; synthetic controlled results may not generalize to real populations. Preserve raw observations and investigate missing, duplicated, or out-of-order events.

## Automated tests

Run `python3 -m unittest tests.test_member_experience -v`. Edge cases cover no starts, empty durations, zero-stage reach, nearest-rank tails, stage timing, comparisons, and success criteria. Run the full suite before drawing conclusions.

## Exercises

1. Is the stage with the worst percentage loss always the largest absolute loss?
2. Propose two non-analytics sources for investigating verification loss.
3. What happens after a zero-reach stage?

**Answer key:** (1) No; name the decision rule. (2) Moderated usability testing and synthetic error traces are examples. (3) Later conversion is reported as zero rather than dividing by zero; interpret such a broken funnel cautiously.

## Expected takeaway

A technically correct application is an output. A defensible member-experience outcome requires a defined task, reproducible observations, multiple metrics, criteria, and claim restraint.

## Chapter summary

Chapter 6 connects observable member-journey behavior to measured outcomes while keeping possible organizational effects explicitly downstream and unproven.

[Previous chapter](chapter-05-mapping-the-digital-member-journey.md) | [Contents](../../CONTENTS.md) | [Next chapter](chapter-07-diagnosing-funnel-abandonment.md)
