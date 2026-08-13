# Chapter 18: Measuring Detection and Recovery

## Learning objectives

- Reconstruct incident start, detection, investigation, mitigation, and restoration milestones.
- Calculate detection duration, incident/recovery duration, MTTD, and MTTR.
- State which meaning of “MTTR” is in use.
- Interpret an average beside individual incidents.

## Measurable-outcome concept

Organizations use MTTR for several different intervals. This textbook adopts precise definitions:

```text
Detection duration = detected_at − started_at
Recovery duration  = recovered_at − started_at
MTTD = arithmetic mean of detection durations
MTTR = arithmetic mean of start-to-service-restoration durations
```

Here **MTTR means Mean Time to Restore**, not time after detection, time to repair code, or time between failures. `incident_duration` is an alias for the same start-to-restoration interval. Service restoration means useful work recovered, not merely mitigation deployed.

Investigation start and mitigation timestamps remain in the record so learners can inspect handoffs, but they do not change these formulas.

## Planned Harbor FCU scenario

Three deterministic SEV-2 records affect the banking API through cache saturation, a dependency timeout, and query contention. Each has:

```text
incident_id, service, started_at, detected_at, investigation_started_at,
mitigated_at, recovered_at, severity, failure_category
```

The records yield detection durations of 8, 11, and 5 minutes and recovery durations of 32, 41, and 23 minutes. Therefore MTTD is 8 minutes and MTTR is 32 minutes. UTC ISO-8601 timestamps make the calculation reproducible.

## Metrics to measure

- Detection duration per incident.
- Start-to-restoration duration per incident.
- Aggregate MTTD and MTTR in minutes.
- The minimum, maximum, and distribution/individual records when the sample warrants them.

One unusually severe incident can pull an arithmetic mean upward. Three incidents are also a small, selected sample. Always retain each incident and consider median/percentiles with a larger population, reusing Chapter 11's percentile convention.

## Planned executable exercise

Run:

```bash
python3 scripts/measure_incident_response.py
```

Independently verify the first record: 10:00 to 10:08 is 8 minutes; 10:00 to 10:32 is 32 minutes. Then verify `(8 + 11 + 5) / 3 = 8` and `(32 + 41 + 23) / 3 = 32`.

The reusable functions reject empty aggregate populations and negative intervals. They do not infer incident start from telemetry; that remains an operational data-quality decision.

## Engineering tradeoffs and limitations

Choosing the first symptom as `started_at` may move MTTD earlier than choosing first confirmed user impact. Either can be valid if consistently defined. A quick mitigation may restore service while leaving a permanent repair unfinished. MTTR should not encourage declaring recovery before useful-work indicators stabilize.

Observed: these three simulated records averaged 8-minute detection and 32-minute restoration. Supported interpretation: the second incident took longest. Not established: a particular engineer or team performed poorly, or a real institution lost money.

## Automated tests

```bash
python3 -m unittest tests.test_reliability.IncidentResponseTest.test_durations_and_aggregate_definitions -v
```

## Exercises

1. Calculate each interval by hand before running the command.
2. Add a 120-minute recovery incident on paper. How does MTTR change, and what does the original average hide?
3. Explain why “time from detection to recovery” is not this repository's MTTR.
4. Which useful-work SLI would you require before setting `recovered_at` for a transfer incident?

## Expected takeaway

Incident response becomes improvable when milestones and interval definitions are explicit. Averages summarize a population; they never replace review of the underlying incidents.
