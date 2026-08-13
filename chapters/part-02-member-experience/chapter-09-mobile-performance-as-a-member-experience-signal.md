# Chapter 9: From Member Metrics to Business Claims

> **Status:** Implemented. All Harbor Federal Credit Union (Harbor FCU) sessions and events in this chapter are fictional and synthetic.

[← Previous chapter](chapter-08-navigation-experiments-and-responsible-conversion-claims.md) | [Contents](../../CONTENTS.md) | [Next chapter →](../part-03-apis-integrations/chapter-10-rest-integrations-define-success-before-coding.md)

## Learning objectives

Measurement controls the strength of the story: software behavior can influence experience and behavior, but business impact is downstream evidence, not a synonym for conversion. Learners will calculate the chapter metrics, interpret tradeoffs, and state evidence limitations without inventing causality.

## Banking context

A prospective member may arrive at a working application and still fail to accomplish the intended digital task. Harbor FCU therefore observes the journey, not merely whether its software returned a page.

## Engineering concept

Use the chain `engineering change → measured system improvement → measured member-behavior improvement → possible operational/business effect`. An **observation** restates measured values. An **interpretation** explains their bounded meaning. A **hypothesis** proposes an unmeasured effect for testing. A **causal claim** says the intervention produced an effect and requires an appropriate design; a quantified cost claim also needs cost observations.

## Measurable-outcome concept

Strongly supported: “Completion increased in the controlled measurement.” Reasonable interpretation: “More measured sessions completed the workflow.” Hypothesis: “This may reduce assisted-service demand.” Unsupported here: “Harbor saved $100,000.” Conversion improvement ≠ automatically revenue. Correlation ≠ causation. Satisfaction, calls, account funding, retention, and costs were not measured.

## Planned Harbor FCU scenario

The shared event schema is `session_id`, `event_type`, UTC `timestamp`, `step`, `result`, and elapsed `duration_ms`. Identifiers such as `session_0001` are not people. The generator is deterministic, and the provenance explicitly excludes real financial, tracking, or personal data.

## Metrics to measure

The lab reports numerator and denominator, percentages, counts, units, population, and relevant exclusions. It reuses nearest-rank `percentile` and Part I `Criterion` evaluation from `src/harbor_fcu/measurement.py` through `src/harbor_fcu/member_experience.py`.

## Implementation

Reusable calculations live in the package; the command is a thin report. Event collections are materialized where repeated passes are required. Empty or undefined populations raise `ValueError` rather than returning a persuasive-looking zero.

## Planned executable exercise

Run `python3 scripts/classify_claims.py` for the machine-checkable answer key, and `python3 scripts/compare_experience.py` for its evidence. Before viewing the key, label each statement observation, interpretation, hypothesis, or unsupported causal claim.

## What to observe and interpret

Follow the progression `software behavior → digital experience → member behavior → measured outcome → potential organizational impact`. Stop the claim at the last measured link. Page traffic, member happiness, assistance, revenue, and cost are separate measures unless explicitly observed.

## Engineering tradeoffs and evidence limitations

More instrumentation can improve diagnosis but adds event-quality, privacy, accessibility, and maintenance concerns. This small teaching model avoids a production analytics platform. Counts depend on event delivery and definitions; synthetic controlled results may not generalize to real populations. Preserve raw observations and investigate missing, duplicated, or out-of-order events.

## Automated tests

Run `python3 -m unittest tests.test_member_experience -v`. Edge cases cover no starts, empty durations, zero-stage reach, nearest-rank tails, stage timing, comparisons, and success criteria. Run the full suite before drawing conclusions.

## Exercises

Given before completion 80%, after 86%, before p95 11 minutes, after 7 minutes, and support calls not measured, classify: (1) the measured workflow became faster; (2) more measured sessions completed; (3) members are happier; (4) calls decreased; (5) Harbor saved money.

**Answer key:** (1) observation/bounded interpretation; (2) observation; (3) hypothesis; (4) unsupported; (5) unsupported. Measure satisfaction, call volume linked to the eligible population, and costs, with a design capable of supporting the intended attribution.

## Expected takeaway

A technically correct application is an output. A defensible member-experience outcome requires a defined task, reproducible observations, multiple metrics, criteria, and claim restraint.

## Chapter summary

Chapter 9 connects observable member-journey behavior to measured outcomes while keeping possible organizational effects explicitly downstream and unproven.
