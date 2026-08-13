#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.backend_performance import backend_workload, create_database, measure_operation, account_history_joined, account_history_n_plus_one

w = backend_workload()
print("Harbor FCU Synthetic Backend Workload")
for component, duration in w["components_ms"].items():
    print(f"{component:20} {duration:4} modeled ms  {w['shares_pct'][component]:5.1f}%")
print(f"Bottleneck: {w['bottleneck']}; throughput: {w['operations_per_second']:.1f} operations/second")
for label, action in [("N+1", account_history_n_plus_one), ("batched", account_history_joined)]:
    result, measurement = measure_operation(label, action, create_database(indexed=label == "batched"))
    print(f"{label}: queries/request={measurement.query_count}, rows returned={measurement.rows_returned}, result_hash={measurement.result_hash}")
