#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from harbor_fcu.integration_metrics import percentile

dependencies = {"ClearVerify": [180]*90+[700]*5+[1800]*4+[4200], "HeritageCore": [240]*90+[800]*5+[1550]*4+[2600], "Harbor application": [40]*99+[80]}
print("Synthetic dependency latency (ms)")
for name, values in dependencies.items():
    print(f"{name:18} min={min(values):4} median={percentile(values,50):4} p90={percentile(values,90):4} p95={percentile(values,95):4} p99={percentile(values,99):4} max={max(values):4}")
print("Largest p99 contributor: ClearVerify")
print("This identifies a tail-latency contributor; abandonment was not measured.")
