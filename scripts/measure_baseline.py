#!/usr/bin/env python3
"""Chapter 1: calculate the reproducible verification-service baseline."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from harbor_fcu.measurement import load_observations, summarize  # noqa: E402
from harbor_fcu.scenarios import BASELINE  # noqa: E402
m = summarize(load_observations(BASELINE))
print("Harbor FCU synthetic verification baseline (2026-01-15 12:00–12:19 UTC)")
print(f"Sample: {m.count} requests")
print(f"Success rate: {m.success_rate_pct:.1f}%")
print(f"Error rate: {m.error_rate_pct:.1f}%")
print(f"p50 latency: {m.p50_latency_ms} ms")
print(f"p95 latency: {m.p95_latency_ms} ms")
