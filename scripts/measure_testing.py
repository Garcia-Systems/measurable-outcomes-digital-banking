#!/usr/bin/env python3
"""Run the Chapter 25 deterministic regression experiment."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.quality import regression_experiment

print("Harbor FCU Automated Testing Experiment")
for label, included in (("Meaningful behavior test present", True), ("Behavior test absent", False)):
    result = regression_experiment(included)
    print(f"\n{label}")
    print(f"Tests executed       {result['tests_executed']}")
    print(f"Tests passed         {result['tests_passed']}")
    print(f"Tests failed         {result['tests_failed']}")
    print(f"Regression detected  {'YES' if result['regression_detected'] else 'NO'}")
