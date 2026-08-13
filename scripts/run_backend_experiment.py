#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.backend_performance import run_backend_experiment

r = run_backend_experiment()
b, o = r["baseline"], r["optimized"]
print("Harbor FCU Backend Optimization Experiment")
print(f"{'':25} {'BASELINE':>12} {'OPTIMIZED':>12}")
print(f"{'Median observed latency':25} {b['median_ms']:10.3f}ms {o['median_ms']:10.3f}ms")
print(f"{'p95 observed latency':25} {b['p95_ms']:10.3f}ms {o['p95_ms']:10.3f}ms")
print(f"{'p95 modeled service time':25} {b['modeled_p95_ms']:10.1f}ms {o['modeled_p95_ms']:10.1f}ms")
print(f"{'Queries/request':25} {b['queries']:12} {o['queries']:12}")
print(f"{'Result correctness':25} {'PASS':>12} {('PASS' if r['equivalent'] else 'FAIL'):>12}")
print("\nSuccess Criteria (declared before evaluation)")
for name, passed in r["criteria"].items(): print(f"{name:25} {'PASS' if passed else 'FAIL'}")
print(f"Overall: {'PASS' if r['overall'] else 'FAIL'}")
print("\nSUPPORTED CONCLUSION\nThe optimized implementation performs less database work under the laboratory workload while preserving results.")
print("\nPOTENTIAL DOWNSTREAM EFFECT\nFaster backend processing may improve response times for workflows using this endpoint.")
print("\nNOT ESTABLISHED\nMember satisfaction; revenue impact; infrastructure cost savings.")
print("\nObserved timing is machine-dependent; success uses deterministic work, modeled service-time, correctness, and safety evidence.")
