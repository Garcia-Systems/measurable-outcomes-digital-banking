# Chapter 29: Measuring a Delivery Improvement

> **Synthetic-data notice:** Harbor Federal Credit Union, its releases, users, defects, transfers, and security cases are fictional.

## Learning objectives

- Explain the chapter's engineering control and measured outcome.
- Calculate its deterministic quality metrics.
- Separate observations, supported conclusions, potential effects, and unsupported claims.

## Banking context and engineering concept
The capstone follows code change → automated validation → defect and security detection → review → simulated deployment → measured outcome. The baseline has incomplete validation; the improved process applies the Part VI controls to deterministic release records.

## Measurable-outcome concept
Success is declared before evaluation: quality requires a lower known-defect escape rate; safety requires all seven defined security cases blocked; delivery requires all three intentionally invalid candidates blocked; the guardrail requires a valid candidate to pass. Results are calculated, not hard-coded conclusions.

## Planned Harbor FCU scenario
Before and after records contain checks, caught and escaped known defects, security cases blocked, invalid releases blocked, validation seconds, deployments, and simulated successes. The improved run grows from 8 to 19 checks and 120 to 360 seconds while escapes fall from 8 to 2.

## Metrics to measure
Test/security/gate pass rates, defect detection and escape rates, blocked invalid releases, deployment success rate, validation duration, and before/after differences. These records are fictional and deterministic.

## Planned executable exercise
```bash
python3 scripts/run_delivery_experiment.py
```
Observe the table and computed criteria. Recalculate escape rates: before `8/(4+8)` and after `2/(10+2)`. Inspect both the improved outcome and pipeline-time cost.

## Interpretation and tradeoffs
Supported: fewer known defects escaped and more defined security failures were detected before simulated deployment. Potential: fewer regressions and less incident-response work. Not established: complete security, zero future defects, member satisfaction, causality in production, or financial savings.

A pipeline changing from two minutes/eight escapes to six minutes/two escapes improved the measured escape count and regressed duration. It is not automatically better: an organization needs risk tolerance, delivery target, severity weighting, and an acceptable feedback-time objective.

## Automated tests
Tests verify calculated rates, every criterion, invalid blocking, and the valid-candidate guardrail.

## Exercises
What measurably improved and regressed in the duration scenario? Propose a target that adjudicates the tradeoff. Then identify a confounder that would weaken a real before/after causal claim.

## Expected takeaway

Tests, security controls, and deployment processes are outputs. Their value comes from defined failures detected or prevented and the reliability they help produce; evidence remains bounded to the observed fixtures.

## Chapter summary

The laboratory measures a quality control, preserves a valid-behavior guardrail, and states its limitations. Continue to the next chapter to move one step toward a measured delivery outcome.

## Part transition

Part VI measured delivery controls and escaped defects. Part VII reuses the resulting telemetry to evaluate analytics, automation, and scoring against simple baselines and operational outcomes.

[Previous chapter](chapter-28-secure-inputs-and-measurable-risk-reduction.md) | [Contents](../../CONTENTS.md) | [Next chapter](../part-07-analytics-ml/chapter-30-operational-analytics-from-events-to-decisions.md)
