# Harbor FCU evolving lab

Harbor Federal Credit Union and every artifact here are fictional. Part I uses the versioned observations in `../../data/synthetic/part1/` and shared functions in `../../src/harbor_fcu/measurement.py`.

## Part I path

1. Observe baseline success (`introduce_measurement.py`).
2. Characterize the same baseline (`measure_baseline.py`).
3. Choose a metric for the objective (`choose_metric.py`).
4. reject a fast candidate that violates guardrails (`evaluate_candidate.py`).
5. Compare the baseline with a reliable candidate (`run_experiment.py`).

This remains one evolving environment, not five chapter applications. Future chapters should extend its models and reports while preserving raw observations, measurement conditions, and evidence-bounded claims.
## Part II: digital application journey

Part II adds a deterministic, entirely fictional account-application journey in
`data/synthetic/part2`. Reusable event, funnel, timing, and comparison calculations
live in `src/harbor_fcu/member_experience.py`; the five learner-facing commands are
documented in the repository README. This remains an educational simulation, not a
production analytics platform.

## Part III: fictional integration laboratory

Part III extends the same environment with deterministic ClearVerify REST,
HeritageCore SOAP, and NorthstarPay transfer behavior. Adapters never open a
socket: scenario tables produce normalized telemetry for reliability, tail
latency, bounded retries, retry exhaustion, and idempotency measurement. Run the
five Part III commands listed in the repository README from the repository root.
