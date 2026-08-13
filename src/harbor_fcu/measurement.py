"""Small, reusable measurement primitives for the synthetic Harbor FCU labs."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Observation:
    timestamp: str
    operation: str
    successful: bool
    latency_ms: int


@dataclass(frozen=True)
class Measurement:
    count: int
    successes: int
    success_rate_pct: float
    error_rate_pct: float
    mean_latency_ms: float
    p50_latency_ms: int
    p95_latency_ms: int


@dataclass(frozen=True)
class MetricComparison:
    metric: str
    baseline: float
    after: float
    absolute_change: float
    relative_change_pct: float
    unit: str


@dataclass(frozen=True)
class Criterion:
    metric: str
    operator: str
    threshold: float


@dataclass(frozen=True)
class CriterionResult:
    criterion: Criterion
    actual: float
    passed: bool


def load_observations(path: Path) -> list[Observation]:
    """Load the documented CSV schema and reject an empty observation set."""
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise ValueError("measurement data must contain at least one observation")
    return [
        Observation(
            timestamp=row["timestamp"],
            operation=row["operation"],
            successful=row["successful"].strip().lower() == "true",
            latency_ms=int(row["latency_ms"]),
        )
        for row in rows
    ]


def percentile(values: Iterable[int], percentile_value: float) -> int:
    """Return a nearest-rank percentile (0 < percentile <= 100)."""
    ordered = sorted(values)
    if not ordered:
        raise ValueError("a percentile requires at least one value")
    if not 0 < percentile_value <= 100:
        raise ValueError("percentile must be greater than 0 and at most 100")
    return ordered[math.ceil(percentile_value / 100 * len(ordered)) - 1]


def success_rate(observations: Iterable[Observation]) -> float:
    items = list(observations)
    if not items:
        raise ValueError("success rate requires at least one observation")
    return 100 * sum(item.successful for item in items) / len(items)


def error_rate(observations: Iterable[Observation]) -> float:
    return 100 - success_rate(observations)


def summarize(observations: Iterable[Observation]) -> Measurement:
    items = list(observations)
    if not items:
        raise ValueError("measurement requires at least one observation")
    latencies = [item.latency_ms for item in items]
    successes = sum(item.successful for item in items)
    return Measurement(
        count=len(items), successes=successes,
        success_rate_pct=100 * successes / len(items),
        error_rate_pct=100 * (len(items) - successes) / len(items),
        mean_latency_ms=sum(latencies) / len(latencies),
        p50_latency_ms=percentile(latencies, 50),
        p95_latency_ms=percentile(latencies, 95),
    )


def compare(metric: str, baseline: float, after: float, unit: str = "") -> MetricComparison:
    """Compare values; a positive relative value means the measured value increased."""
    if baseline == 0:
        raise ValueError("relative change is undefined for a zero baseline")
    absolute = after - baseline
    return MetricComparison(metric, baseline, after, absolute, 100 * absolute / baseline, unit)


def percentage_improvement(baseline: float, after: float, lower_is_better: bool) -> float:
    """Express beneficial direction as positive, unlike raw relative change."""
    change = compare("value", baseline, after).relative_change_pct
    return -change if lower_is_better else change


def evaluate(actual: float, criterion: Criterion) -> CriterionResult:
    operators = {
        "<": lambda a, b: a < b, "<=": lambda a, b: a <= b,
        ">": lambda a, b: a > b, ">=": lambda a, b: a >= b,
        "==": lambda a, b: a == b,
    }
    if criterion.operator not in operators:
        raise ValueError(f"unsupported criterion operator: {criterion.operator}")
    return CriterionResult(criterion, actual, operators[criterion.operator](actual, criterion.threshold))


def evaluate_measurement(measurement: Measurement, criteria: Iterable[Criterion]) -> list[CriterionResult]:
    return [evaluate(float(getattr(measurement, item.metric)), item) for item in criteria]
