#!/usr/bin/env python3
"""Chapter 4: print a compact, extensible before/after measurement report."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from harbor_fcu.measurement import compare, evaluate, load_observations, percentage_improvement, summarize, Criterion  # noqa: E402
from harbor_fcu.scenarios import BASELINE, RELIABLE_CANDIDATE  # noqa: E402
b=summarize(load_observations(BASELINE)); a=summarize(load_observations(RELIABLE_CANDIDATE))
s=compare("verification_success_rate", b.success_rate_pct, a.success_rate_pct, "percentage points")
l=compare("p95_latency", b.p95_latency_ms, a.p95_latency_ms, "ms")
passed=evaluate(a.success_rate_pct, Criterion("success_rate_pct", ">=", 99)).passed
print("Harbor FCU engineering measurement report (synthetic)")
print(f"Metric: {s.metric}\nBaseline: {s.baseline:.1f}%\nAfter: {s.after:.1f}%")
print(f"Absolute change: {s.absolute_change:+.1f} percentage points\nRelative change: {s.relative_change_pct:+.2f}%")
print(f"Target: >= 99.0%\nResult: {'PASS' if passed else 'FAIL'}")
print(f"Latency p95: {l.baseline:.0f} ms -> {l.after:.0f} ms ({l.absolute_change:+.0f} ms; {percentage_improvement(l.baseline,l.after,True):.1f}% improvement)")
print("Supported outcome: success rate increased and p95 latency decreased under the measured workload.")
print("Limitation: this comparison alone does not prove member adoption, cost, retention, or revenue impact.")
