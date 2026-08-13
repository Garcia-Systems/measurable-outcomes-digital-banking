"""Metrics for synthetic Harbor FCU API observations."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ApiMetrics:
    request_count: int
    success_rate_pct: float
    mean_latency_ms: float
    p95_latency_ms: int


def measure_api_requests(path: Path) -> ApiMetrics:
    """Calculate baseline metrics; success means an HTTP status below 400."""
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise ValueError("API request data must contain at least one observation")

    latencies = sorted(int(row["latency_ms"]) for row in rows)
    successes = sum(int(row["status_code"]) < 400 for row in rows)
    p95_index = math.ceil(0.95 * len(latencies)) - 1
    return ApiMetrics(
        request_count=len(rows),
        success_rate_pct=100 * successes / len(rows),
        mean_latency_ms=sum(latencies) / len(latencies),
        p95_latency_ms=latencies[p95_index],
    )
