#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from harbor_fcu.integration_metrics import *

before, after=experiment("baseline"), experiment("after")
print("Harbor FCU Integration Experiment (synthetic)\n")
print("Metric                     Baseline      After")
print("-"*50)
print(f"Eventual success             {eventual_success_rate(before):5.1f}%      {eventual_success_rate(after):5.1f}%")
print(f"p95 total latency             {percentile(total_operation_latencies(before),95):4} ms      {percentile(total_operation_latencies(after),95):4} ms")
print(f"Timeout request rate          {timeout_rate(before):5.1f}%      {timeout_rate(after):5.1f}%")
print(f"Requests/operation             {requests_per_operation(before):.2f}        {requests_per_operation(after):.2f}")
print("\nSuccess criteria\n"+"-"*50)
for name, passed in evaluate_criteria(after).items(): print(f"{name:30} {'PASS' if passed else 'FAIL'}")
print("\nSupported conclusion:\nThe measured integration became more reliable under the matched simulated workload while meeting its latency, volume, and safety criteria.")
print("\nPotential downstream effect:\nFewer verification-related workflow interruptions could reduce member friction.")
print("\nNot established by this experiment:\nMember satisfaction, abandonment, production behavior, revenue, and causality were not measured.")
