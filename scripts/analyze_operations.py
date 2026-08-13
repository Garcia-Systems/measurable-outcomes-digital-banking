#!/usr/bin/env python3
"""Chapter 30 descriptive analytics laboratory."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.intelligence import group_metrics, operational_requests

rows = operational_requests(); overall = group_metrics([{**row, "all": "all"} for row in rows], "all")["all"]
print("Harbor FCU Operational Analytics (synthetic)")
print(f"Overall error rate: {overall['error_rate_pct']:.1f}%")
print("\nBY VENDOR")
for vendor, metrics in group_metrics(rows, "vendor").items():
    print(f"{vendor:16} requests={metrics['count']:3.0f} error_rate={metrics['error_rate_pct']:.1f}% mean_latency={metrics['mean_latency_ms']:.1f} ms")
print("\nNorthstarPay is localized at 8.0%; the 3.7% aggregate hides that segment.")
