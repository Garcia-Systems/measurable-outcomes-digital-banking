# Chapter 19: Measuring an Incident-Response Improvement

This capstone evaluates a reliability-engineering change rather than asserting that “observability improved.” Harbor adds structured failure categories, shared request/operation IDs, a sustained error-rate alert, and an operational component view.

## Learning objectives

- Define success criteria before inspecting before/after results.
- Compare MTTD, MTTR, diagnostic effort, and false-positive alert rate.
- Evaluate improvement criteria automatically.
- Make claims no broader than the simulation evidence.

## Measurable-outcome concept

The outcome chain is:

```text
OUTPUT: correlation IDs + structured categories + tuned alert
  ↓
TECHNICAL EFFECT: failed operations can be reconstructed
  ↓
MEASURED OPERATIONAL OUTCOME: detection/restoration intervals decrease
  ↓
HYPOTHESIS: less engineering effort or user harm may result
```

The final step remains a hypothesis because this experiment measures neither labor cost nor user harm.

Before evaluation, Harbor declares:

| Criterion | Required result |
|---|---:|
| Detection | MTTD improves at least 50% |
| Recovery | MTTR improves at least 25% |
| Alert guardrail | False-positive alert rate does not increase |

Improvement uses `(before − after) / before × 100` because lower is better. False-positive rate is false alerts / all generated alerts × 100. Diagnostic query count is descriptive; no threshold was declared for it.

## Planned Harbor FCU scenario

Matched deterministic cohorts contain three dependency-timeout incidents each. The baseline uses generic logs and a noisy alert process; the candidate uses contextual logging and a sustained threshold. The fixture reports:

| Metric | Before | After |
|---|---:|---:|
| MTTD | 12 min | 4 min |
| MTTR | 42 min | 22 min |
| Diagnostic queries | 12 | 5 |
| False-positive alert rate | 50% | 25% |

These are calculated from incident and alert records rather than hard-coded report assertions. The cohorts are synthetic and small; matching category alone does not control every confounder.

## Metrics to measure

- MTTD and beneficial percentage improvement.
- MTTR and beneficial percentage improvement.
- False-positive alert rate as a noise guardrail.
- Diagnostic queries as a proxy requiring careful interpretation.
- Pass/fail for every predeclared criterion and overall success.

Availability and error budgets remain useful companion ideas: an SLO's error budget is the allowed fraction of unsuccessful useful work. This capstone focuses on response outcomes rather than claiming that shorter response automatically proves long-window SLO compliance.

## Planned executable exercise

Run:

```bash
python3 scripts/run_reliability_experiment.py
```

The structured report calculates cohort aggregates using the Chapter 18 definitions, evaluates each criterion, and labels supported versus hypothetical claims. All three declared criteria pass in the fixture.

Also run all Part IV laboratories in order:

```bash
python3 scripts/measure_reliability.py
python3 scripts/explore_observability.py
python3 scripts/investigate_incident.py
python3 scripts/measure_incident_response.py
python3 scripts/run_reliability_experiment.py
```

## Interpretation, tradeoffs, and evidence limitations

**Observation:** simulated MTTD changes from 12 to 4 minutes and MTTR from 42 to 22 minutes; false-positive rate falls from 50% to 25%.

**Supported interpretation:** the candidate configuration detected and restored these simulated incidents sooner without increasing the alert-noise guardrail.

**Potential operational effect:** engineers may begin diagnosis sooner, and fewer queries may indicate easier navigation.

**Not established:** Harbor saved money, prevented a particular amount of member harm, or would achieve the same result in production. Diagnostic query count is not direct labor time. Before/after cohorts can differ in hidden ways, and instrumentation changes can move recorded milestone timestamps.

A more sensitive threshold can reduce MTTD while increasing false alerts. Richer logs can reduce search effort while increasing storage, cardinality, privacy, and governance costs. The candidate is acceptable here because both speed criteria improve and the noise guardrail does not regress.

## Automated tests

```bash
python3 -m unittest tests.test_reliability -v
python3 -m unittest discover -s tests -v
```

The tests cover reliability and availability, endpoint errors, alert runs, identifiers, timeline ordering/filtering, incident durations, MTTD/MTTR, false positives, comparison direction, and capstone criteria.

## Exercises

1. Write an evidence-bounded outcome statement from the report.
2. Explain why reduced diagnostic queries do not prove reduced labor cost.
3. Raise alert sensitivity on paper. Which success metric and guardrail might move in opposite directions?
4. Design a larger matched evaluation and name likely confounders.
5. Identify the member-facing SLI needed to show that shorter MTTR also reduced failed transfers.

## Expected takeaway

Reliability work is measurable when it reduces failure frequency, user-visible impact, or detection/restoration time under explicit guardrails. This simulation supports a narrower incident-response claim—not an unmeasured organizational causal claim.
