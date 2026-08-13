#!/usr/bin/env bash
# Run every Chapter 0–39 laboratory in curriculum order. Stop at the first error.
set -euo pipefail
cd "$(dirname "$0")/.."

commands=(
  "python3 scripts/introduce_measurement.py"
  "python3 scripts/measure_baseline.py"
  "python3 scripts/choose_metric.py --answer completion_rate"
  "python3 scripts/evaluate_candidate.py"
  "python3 scripts/run_experiment.py"
  "python3 scripts/measure_completion.py"
  "python3 scripts/analyze_funnel.py"
  "python3 scripts/analyze_completion_time.py"
  "python3 scripts/compare_experience.py"
  "python3 scripts/classify_claims.py"
  "python3 scripts/measure_api_reliability.py"
  "python3 scripts/analyze_api_latency.py"
  "python3 scripts/simulate_retries.py"
  "python3 scripts/compare_integrations.py"
  "python3 scripts/run_integration_experiment.py"
  "python3 scripts/measure_reliability.py"
  "python3 scripts/explore_observability.py"
  "python3 scripts/investigate_incident.py"
  "python3 scripts/measure_incident_response.py"
  "python3 scripts/run_reliability_experiment.py"
  "python3 scripts/measure_query_performance.py"
  "python3 scripts/compare_database_index.py"
  "python3 scripts/analyze_backend_workload.py"
  "python3 scripts/simulate_backend_concurrency.py"
  "python3 scripts/run_backend_experiment.py"
  "python3 scripts/measure_testing.py"
  "python3 scripts/analyze_defect_escape.py"
  "python3 scripts/run_security_validation.py"
  "python3 scripts/check_release_readiness.py"
  "python3 scripts/run_delivery_experiment.py"
  "python3 scripts/analyze_operations.py"
  "python3 scripts/detect_anomalies.py"
  "python3 scripts/forecast_workload.py"
  "python3 scripts/prioritize_incidents.py"
  "python3 scripts/run_intelligence_experiment.py"
  "python3 scripts/operational_scorecard.py"
  "python3 scripts/measure_member_outcomes.py"
  "python3 scripts/estimate_business_value.py"
  "python3 scripts/report_outcomes.py --audience engineer"
  "python3 scripts/run_capstone.py"
)

for index in "${!commands[@]}"; do
  chapter=$index
  printf '\n== Chapter %02d: %s ==\n' "$chapter" "${commands[$index]}"
  eval "${commands[$index]}"
done
printf '\nPASS: all 40 chapter laboratories completed in order.\n'
