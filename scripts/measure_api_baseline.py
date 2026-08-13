#!/usr/bin/env python3
"""Print a reproducible API baseline for the fictional Harbor FCU lab."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from harbor_fcu.api_metrics import measure_api_requests  # noqa: E402


def main() -> None:
    path = ROOT / "data" / "synthetic" / "api_requests.csv"
    metrics = measure_api_requests(path)
    print("Harbor FCU synthetic API baseline")
    print(f"Requests: {metrics.request_count}")
    print(f"Success rate: {metrics.success_rate_pct:.1f}%")
    print(f"Mean latency: {metrics.mean_latency_ms:.1f} ms")
    print(f"p95 latency: {metrics.p95_latency_ms} ms")


if __name__ == "__main__":
    main()
