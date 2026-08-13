#!/usr/bin/env python3
"""Chapter 2: machine-check a metric choice for a stated objective."""
import argparse
choices = {"latency_p95": "technical", "deployment_failure_rate": "delivery", "manual_reviews": "operational", "completion_rate": "member experience", "digital_adoption": "business"}
p = argparse.ArgumentParser(); p.add_argument("--answer", choices=choices, default="completion_rate"); args = p.parse_args()
print("Objective: reduce verification attempts that terminate before completion.")
for metric, category in choices.items(): print(f"- {metric} [{category}]")
correct = args.answer == "completion_rate"
print(f"Selected: {args.answer}")
print("Result: PASS — directly measures completed attempts." if correct else "Result: TRY AGAIN — useful context, but it does not directly measure completed attempts.")
raise SystemExit(0 if correct else 1)
