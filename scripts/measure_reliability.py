#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from harbor_fcu.measurement import percentile
from harbor_fcu.reliability import endpoint_error_rates, observed_availability, reliability_requests

rows = reliability_requests()
print("Harbor FCU application reliability (synthetic)")
print(f"Requests: {len(rows)} | successful: {sum(row.successful for row in rows)} | failed: {sum(not row.successful for row in rows)}")
print(f"Request success rate / observed availability: {observed_availability(rows):.1f}%")
print(f"Error rate: {100-observed_availability(rows):.1f}% | p95 latency: {percentile([row.latency_ms for row in rows], 95)} ms")
print("Failures by endpoint:")
for endpoint, rate in endpoint_error_rates(rows).items():
    failures = sum(row.endpoint == endpoint and not row.successful for row in rows)
    print(f"  {endpoint:<12} failures={failures} error_rate={rate:.1f}%")
print("Observe: process liveness alone would not reveal failed useful work.")
