#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from harbor_fcu.reliability import compare_reliability, evaluate_part4_success, experiment_scenarios

before, after, before_alerts, after_alerts = experiment_scenarios()
result = compare_reliability(before, after, before_alerts, after_alerts, 12, 5)
criteria = evaluate_part4_success(result)
print("Harbor FCU structured reliability outcome report (synthetic)")
print("Predeclared criteria: MTTD improvement ≥50%; MTTR improvement ≥25%; false-positive rate must not rise.")
print("Metric                         BEFORE    AFTER    CHANGE")
print(f"MTTD (minutes)                 {result.before_mttd_minutes:6.1f}   {result.after_mttd_minutes:6.1f}   {result.detection_improvement_pct:5.1f}% better")
print(f"MTTR (minutes)                 {result.before_mttr_minutes:6.1f}   {result.after_mttr_minutes:6.1f}   {result.recovery_improvement_pct:5.1f}% better")
print(f"False-positive alert rate (%)  {result.before_false_positive_rate_pct:6.1f}   {result.after_false_positive_rate_pct:6.1f}")
print(f"Diagnostic queries             {result.diagnostic_queries_before:6d}   {result.diagnostic_queries_after:6d}")
for name, passed in criteria.items(): print(f"{name:<48} {'PASS' if passed else 'FAIL'}")
print(f"Overall: {'PASS' if all(criteria.values()) else 'FAIL'}")
print("Supported: the simulated monitoring process detected and restored these incidents sooner.")
print("Hypothesis only: lower response time may reduce engineering effort; cost was not measured.")
